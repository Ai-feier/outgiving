"""平台注册表测试 — content/platform.py 是唯一事实源。

核心保证（drift test）：id_gen.Platform 的枚举成员 与 platform.PLATFORMS
的 key 必须一一对应——加平台时两边漏一处，这里立刻红。
"""

from __future__ import annotations

import pytest

from content import platform
from content.id_gen import Platform

# ── drift：枚举 ↔ 注册表 一致 ────────────────────────────────


def test_enum_members_match_registry() -> None:
    enum_values = {m.value for m in Platform}
    registry_keys = set(platform.PLATFORMS.keys())
    assert enum_values == registry_keys, (
        f"Platform 枚举与 platform.PLATFORMS 不一致：\n"
        f"  enum 多出: {sorted(enum_values - registry_keys)}\n"
        f"  registry 多出: {sorted(registry_keys - enum_values)}"
    )


def test_registry_fields_complete() -> None:
    """每个平台 8 个字段都非空。"""
    for spec in platform.all():
        for field_name in (
            "value",
            "display",
            "emoji",
            "dir_name",
            "color_hex",
            "color_name",
            "default_file",
            "template_file",
        ):
            val = getattr(spec, field_name)
            assert val, f"{spec.value}.{field_name} 为空"
        assert spec.dir_name.startswith("platforms/"), spec.dir_name
        assert spec.color_hex.startswith("#"), spec.color_hex


# ── 查找 ────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("wechat", "wechat"),
        ("WECHAT", "wechat"),
        ("we-chat", "wechat"),
        ("we_chat", "wechat"),
        ("X", "x"),
        ("douyin", "douyin"),
        ("xiaohongshu", "xiaohongshu"),
    ],
)
def test_get_normalizes(raw: str, expected: str) -> None:
    spec = platform.get(raw)
    assert spec is not None and spec.value == expected


def test_get_unknown_returns_none() -> None:
    assert platform.get("tiktok") is None
    assert platform.get(None) is None
    assert platform.is_platform("tiktok") is False
    assert platform.is_platform("wechat") is True


def test_names_order_stable() -> None:
    assert platform.names() == ["wechat", "xiaohongshu", "x", "douyin"]


# ── slug 工具 ───────────────────────────────────────────────


def test_slugify_title_keeps_chinese() -> None:
    assert platform.slugify_title("AI 视频创作指南") == "ai-视频创作指南"


def test_slugify_title_punctuation() -> None:
    assert platform.slugify_title("a/b\\c:d*?") == "a-b-c-d"


def test_slugify_title_truncates_and_empty() -> None:
    assert platform.slugify_title("x" * 80) == "x" * 60
    assert platform.slugify_title("   ") == "untitled"


def test_slugify_anchor_dedup() -> None:
    used: dict[str, int] = {}
    a = platform.slugify_anchor("## 标题 A", used)
    b = platform.slugify_anchor("## 标题 A", used)
    assert a != b
    assert b == f"{a}-1"


def test_slugify_anchor_html_stripped() -> None:
    assert platform.slugify_anchor("<em>强调</em>词") == "强调词"
