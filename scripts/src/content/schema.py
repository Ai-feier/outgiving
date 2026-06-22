"""
Frontmatter Schema —— Pydantic 模型 + 状态机定义。

四类文档：topic / draft / published / analytics
每个文档头部 YAML frontmatter 必须能被对应 schema 解析通过。
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from .id_gen import Platform


class Kind(str, Enum):
    TOPIC = "topic"
    DRAFT = "draft"
    PUBLISHED = "published"
    ANALYTICS = "analytics"


class TopicStatus(str, Enum):
    INBOX = "inbox"          # 仅在 inbox/ 出现
    BRIEFING = "briefing"    # brief.md 起草中
    OUTLINED = "outlined"    # outline.md 完成
    ADAPTING = "adapting"    # 至少一个平台在改写
    ARCHIVED = "archived"    # 已结束生命周期


class DraftStatus(str, Enum):
    DRAFT = "draft"
    REVIEWING = "reviewing"
    READY = "ready"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    RETIRED = "retired"


class PublishedStatus(str, Enum):
    LIVE = "live"
    ANALYZING = "analyzing"
    CLOSED = "closed"


class AnalyticsStatus(str, Enum):
    PENDING = "pending"
    T3 = "t+3"
    T7 = "t+7"
    FINAL = "final"


class HookType(str, Enum):
    COUNTER_INTUITIVE = "counter-intuitive"
    PAIN = "pain"
    BENEFIT = "benefit"
    STORY = "story"
    NUMBER = "number"


class Priority(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"


# 状态机：每个 kind 允许的转移
TRANSITIONS: dict[Kind, dict[str, set[str]]] = {
    Kind.TOPIC: {
        TopicStatus.INBOX: {TopicStatus.BRIEFING},
        TopicStatus.BRIEFING: {TopicStatus.OUTLINED, TopicStatus.ARCHIVED},
        TopicStatus.OUTLINED: {TopicStatus.ADAPTING, TopicStatus.ARCHIVED},
        TopicStatus.ADAPTING: {TopicStatus.ARCHIVED},
        TopicStatus.ARCHIVED: set(),
    },
    Kind.DRAFT: {
        DraftStatus.DRAFT: {DraftStatus.REVIEWING, DraftStatus.RETIRED},
        DraftStatus.REVIEWING: {DraftStatus.READY, DraftStatus.DRAFT, DraftStatus.RETIRED},
        DraftStatus.READY: {DraftStatus.SCHEDULED, DraftStatus.PUBLISHED, DraftStatus.RETIRED},
        DraftStatus.SCHEDULED: {DraftStatus.PUBLISHED, DraftStatus.READY},
        DraftStatus.PUBLISHED: {DraftStatus.RETIRED},
        DraftStatus.RETIRED: set(),
    },
    Kind.PUBLISHED: {
        PublishedStatus.LIVE: {PublishedStatus.ANALYZING},
        PublishedStatus.ANALYZING: {PublishedStatus.CLOSED},
        PublishedStatus.CLOSED: set(),
    },
    Kind.ANALYTICS: {
        AnalyticsStatus.PENDING: {AnalyticsStatus.T3},
        AnalyticsStatus.T3: {AnalyticsStatus.T7},
        AnalyticsStatus.T7: {AnalyticsStatus.FINAL},
        AnalyticsStatus.FINAL: set(),
    },
}


class Base(BaseModel):
    """所有 frontmatter 共享的字段"""

    model_config = ConfigDict(use_enum_values=True, extra="allow")

    id: str
    kind: Kind
    topic_id: str = Field(description="所属选题 ID；topic 自己 = topic_id")
    title: str
    status: str
    created_at: date
    updated_at: date
    tags: list[str] = Field(default_factory=list)


class TopicFM(Base):
    kind: Literal[Kind.TOPIC] = Kind.TOPIC
    status: TopicStatus = TopicStatus.BRIEFING
    audience: str | None = None
    hook_type: HookType | None = None
    platforms_planned: list[Platform] = Field(default_factory=list)
    priority: Priority = Priority.P1


class DraftFM(Base):
    kind: Literal[Kind.DRAFT] = Kind.DRAFT
    parent_id: str = Field(description="父文档 ID，通常 = topic_id")
    platform: Platform
    revision: int = 1
    status: DraftStatus = DraftStatus.DRAFT
    word_count: int = 0
    hook: str | None = None
    cta: str | None = None
    cover_image: str | None = None
    scheduled_at: datetime | None = None


class PublishedFM(Base):
    kind: Literal[Kind.PUBLISHED] = Kind.PUBLISHED
    parent_id: str = Field(description="上游 draft ID")
    platform: Platform
    status: PublishedStatus = PublishedStatus.LIVE
    published_at: datetime
    url: str
    title_final: str | None = None


class PlatformMetric(BaseModel):
    model_config = ConfigDict(extra="allow")
    url: str | None = None
    views: int = 0
    likes: int = 0
    comments: int = 0
    favorites: int = 0
    forwards: int = 0
    new_followers: int = 0
    completion_rate: float | None = None
    impressions: int | None = None
    reposts: int | None = None
    measured_at: datetime | None = None


class AnalyticsFM(Base):
    kind: Literal[Kind.ANALYTICS] = Kind.ANALYTICS
    status: AnalyticsStatus = AnalyticsStatus.PENDING
    platforms_data: dict[Platform, PlatformMetric] = Field(default_factory=dict)
    best_platform: Platform | None = None
    best_hook: str | None = None
    next_improvements: list[str] = Field(default_factory=list)


AnyFM = Annotated[
    Union[TopicFM, DraftFM, PublishedFM, AnalyticsFM],
    Field(discriminator="kind"),
]


def parse_frontmatter(data: dict) -> AnyFM:
    """根据 kind 派发到对应 Schema，失败抛 pydantic ValidationError"""
    kind = data.get("kind")
    if kind == Kind.TOPIC:
        return TopicFM.model_validate(data)
    if kind == Kind.DRAFT:
        return DraftFM.model_validate(data)
    if kind == Kind.PUBLISHED:
        return PublishedFM.model_validate(data)
    if kind == Kind.ANALYTICS:
        return AnalyticsFM.model_validate(data)
    raise ValueError(f"未知 kind: {kind!r}")


def can_transition(kind: Kind, from_status: str, to_status: str) -> bool:
    """状态机校验"""
    allowed = TRANSITIONS.get(kind, {}).get(from_status, set())
    return to_status in allowed