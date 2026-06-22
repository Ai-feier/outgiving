"""
ID 生成 / 解析 —— 人读 ID 规则：

  topic:      T{NNN}               T001, T002
  draft:      T{NNN}-{plat}-v{N}   T001-wechat-v1
  published:  T{NNN}-{plat}-pub    T001-wechat-pub
  analytics:  T{NNN}-review         T001-review
"""

from __future__ import annotations

import re
from enum import Enum

TOPIC_PATTERN = re.compile(r"^T(\d{3})$")
DRAFT_PATTERN = re.compile(r"^T(\d{3})-(\w+)-v(\d+)$")
PUBLISHED_PATTERN = re.compile(r"^T(\d{3})-(\w+)-pub$")
ANALYTICS_PATTERN = re.compile(r"^T(\d{3})-review$")


class Platform(str, Enum):
    WECHAT = "wechat"
    XHS = "xiaohongshu"
    X = "x"
    DOUYIN = "douyin"

    @classmethod
    def _missing_(cls, value: object) -> "Platform | None":
        if isinstance(value, str):
            normalized = value.lower().replace("-", "").replace("_", "")
            for member in cls:
                if member.value == normalized:
                    return member
        return None


def parse_topic_id(raw: str) -> int | None:
    """从 T001 提取数字 1，失败返回 None"""
    m = TOPIC_PATTERN.match(raw)
    return int(m.group(1)) if m else None


def format_topic_id(num: int) -> str:
    """1 → T001"""
    return f"T{num:03d}"


def next_topic_id(existing: list[str]) -> str:
    """['T001', 'T003'] → 'T002' (填补空洞)"""
    nums = sorted(parse_topic_id(e) for e in existing if e)
    if not nums:
        return "T001"
    for i, n in enumerate(nums, start=1):
        if i != n:
            return format_topic_id(i)
    return format_topic_id(nums[-1] + 1)


def draft_id(topic_id: str, platform: str, revision: int = 1) -> str:
    return f"{topic_id}-{platform}-v{revision}"


def published_id(topic_id: str, platform: str) -> str:
    return f"{topic_id}-{platform}-pub"


def analytics_id(topic_id: str) -> str:
    return f"{topic_id}-review"


def parse_id(raw: str) -> dict | None:
    """返回 {kind, topic_num, platform?, revision?} 或 None"""
    if m := TOPIC_PATTERN.match(raw):
        return {"kind": "topic", "topic_num": int(m.group(1))}
    if m := DRAFT_PATTERN.match(raw):
        return {
            "kind": "draft",
            "topic_num": int(m.group(1)),
            "platform": m.group(2),
            "revision": int(m.group(3)),
        }
    if m := PUBLISHED_PATTERN.match(raw):
        return {
            "kind": "published",
            "topic_num": int(m.group(1)),
            "platform": m.group(2),
        }
    if m := ANALYTICS_PATTERN.match(raw):
        return {"kind": "analytics", "topic_num": int(m.group(1))}
    return None