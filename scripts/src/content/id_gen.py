"""
ID 生成 / 解析 —— 人读 ID 规则：

  topic:      T{NNN}               T001, T002
  draft:      T{NNN}-{chan}-v{N}   T001-wechat-v1
  published:  T{NNN}-{chan}-pub    T001-wechat-pub
  analytics:  T{NNN}-analytics     T001-analytics

产出文件名由 doc_filename() 决定：同一选题的全部文件落在
products/<id>-<slug>/ 单目录内，以渠道名区分渠道产出。
"""

from __future__ import annotations

import re
from enum import Enum
from typing import TypedDict

from . import channel as _channel


class ParsedId(TypedDict, total=False):
    """parse_id 的返回——revision 仅 draft 有，channel 仅 draft/published 有。"""

    kind: str
    topic_num: int
    channel: str
    revision: int


TOPIC_PATTERN = re.compile(r"^T(\d{3})$")
DRAFT_PATTERN = re.compile(r"^T(\d{3})-(\w+)-v(\d+)$")
PUBLISHED_PATTERN = re.compile(r"^T(\d{3})-(\w+)-pub$")
ANALYTICS_PATTERN = re.compile(r"^T(\d{3})-analytics$")


class Channel(str, Enum):
    WECHAT = "wechat"
    XHS = "xiaohongshu"
    X = "x"
    DOUYIN = "douyin"

    @classmethod
    def _missing_(cls, value: object) -> Channel | None:
        """归一化查找（大小写 / - / _ 不敏感）——规则在 channel 注册表。"""
        if isinstance(value, str):
            spec = _channel.get(value)
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


def draft_id(topic_id: str, channel: str, revision: int = 1) -> str:
    return f"{topic_id}-{channel}-v{revision}"


def published_id(topic_id: str, channel: str) -> str:
    return f"{topic_id}-{channel}-pub"


def analytics_id(topic_id: str) -> str:
    return f"{topic_id}-analytics"


def doc_filename(kind: str, channel: str | None = None) -> str:
    """产物在 products/<id>-<slug>/ 内的文件名。

    topic → brief.md；draft → <channel>.md；published → <channel>-pub.md；
    analytics → analytics.md。人审表 review.md 由 workbench 管理，不在此列。
    """
    if kind == "topic":
        return "brief.md"
    if kind == "draft":
        return f"{channel}.md"
    if kind == "published":
        return f"{channel}-pub.md"
    if kind == "analytics":
        return "analytics.md"
    raise ValueError(f"未知 kind: {kind!r}")


def parse_id(raw: str) -> ParsedId | None:
    """返回 {kind, topic_num, channel?, revision?} 或 None"""
    if m := TOPIC_PATTERN.match(raw):
        return {"kind": "topic", "topic_num": _int_group(m, 1)}
    if m := DRAFT_PATTERN.match(raw):
        return {
            "kind": "draft",
            "topic_num": _int_group(m, 1),
            "channel": m.group(2),
            "revision": _int_group(m, 3),
        }
    if m := PUBLISHED_PATTERN.match(raw):
        return {
            "kind": "published",
            "topic_num": _int_group(m, 1),
            "channel": m.group(2),
        }
    if m := ANALYTICS_PATTERN.match(raw):
        return {"kind": "analytics", "topic_num": _int_group(m, 1)}
    return None


# ── slug 工具（content 域的两个不同用途，勿混用）─────────────


def slugify_title(title: str) -> str:
    """标题 → 目录/文件名 slug。中文保留，空格/标点转 -，连续 - 折叠，截断 60。"""
    s = title.strip().lower()
    s = re.sub(r"[\s\\/:*?\"<>|]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:60] if s else "untitled"


def slugify_anchor(raw: str, used: dict[str, int] | None = None) -> str:
    """heading 文字 → HTML 锚点 id。传 used 时做重复去重（-2/-3 后缀）。"""
    plain = re.sub(r"<[^>]+>", "", raw).strip()
    plain = re.sub(r"[^\w一-鿿-]", "", plain)
    plain = re.sub(r"_", "-", plain)
    plain = re.sub(r"\s+", "-", plain).strip("-").lower()
    if not plain:
        plain = "section"
    if used is not None:
        if plain in used:
            used[plain] += 1
            plain = f"{plain}-{used[plain]}"
        else:
            used[plain] = 0
    return plain
