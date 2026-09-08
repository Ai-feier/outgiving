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
from typing import TypedDict

from . import platform as _platform


class ParsedId(TypedDict, total=False):
    """parse_id 的返回——revision 仅 draft 有，platform 仅 draft/published 有。"""

    kind: str
    topic_num: int
    platform: str
    revision: int


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
    def _missing_(cls, value: object) -> Platform | None:
        """归一化查找（大小写 / - / _ 不敏感）——规则在 platform 注册表。"""
        if isinstance(value, str):
            spec = _platform.get(value)
            if spec is not None:
                for member in cls:
                    if member.value == spec.value:
                        return member
        return None


def _int_group(m: re.Match[str], i: int) -> int:
    r"""带保护的数字组提取（regex 已保证 \d+，此处是防御 + 满足检查规则）。"""
    try:
        return int(m.group(i))
    except (TypeError, ValueError) as e:
        raise ValueError(f"数字组 {i} 非法: {m.group(i)!r}") from e


def parse_topic_id(raw: str) -> int | None:
    """从 T001 提取数字 1，失败返回 None"""
    m = TOPIC_PATTERN.match(raw)
    return _int_group(m, 1) if m else None


def format_topic_id(num: int) -> str:
    """1 → T001"""
    return f"T{num:03d}"


def next_topic_id(existing: list[str]) -> str:
    """['T001', 'T003'] → 'T002' (填补空洞)"""
    nums: list[int] = []
    for e in existing:
        n = parse_topic_id(e)
        if n is not None:
            nums.append(n)
    if not nums:
        return "T001"
    nums = sorted(nums)
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


def parse_id(raw: str) -> ParsedId | None:
    """返回 {kind, topic_num, platform?, revision?} 或 None"""
    if m := TOPIC_PATTERN.match(raw):
        return {"kind": "topic", "topic_num": _int_group(m, 1)}
    if m := DRAFT_PATTERN.match(raw):
        return {
            "kind": "draft",
            "topic_num": _int_group(m, 1),
            "platform": m.group(2),
            "revision": _int_group(m, 3),
        }
    if m := PUBLISHED_PATTERN.match(raw):
        return {
            "kind": "published",
            "topic_num": _int_group(m, 1),
            "platform": m.group(2),
        }
    if m := ANALYTICS_PATTERN.match(raw):
        return {"kind": "analytics", "topic_num": _int_group(m, 1)}
    return None
