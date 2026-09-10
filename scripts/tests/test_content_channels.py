"""渠道注册表测试 — content/channel.py 是唯一事实源。

核心保证（drift test）：id_gen.Channel 的枚举成员 与 channel.CHANNELS
的 key 必须一一对应——加渠道时两边漏一处，这里立刻红。
"""

from __future__ import annotations

import pytest

from content import channel
from content.id_gen import Channel, doc_filename

# ── drift：枚举 ↔ 注册表 一致 ────────────────────────────────


def test_enum_members_match_registry() -> None:
    enum_values = {m.value for m in Channel}
    registry_keys = set(channel.CHANNELS.keys())
    assert enum_values == registry_keys, (
        f"Channel 枚举与 channel.CHANNELS 不一致：\n"
        f"  enum 多出: {sorted(enum_values - registry_keys)}\n"
        f"  registry 多出: {sorted(registry_keys - enum_values)}"
    )


def test_registry_fields_complete() -> None:
    """每个渠道 6 个字段都非空。"""
    for spec in channel.all():
        for field_name in (
            "value",
            "display",
            "emoji",
            "color_hex",
            "color_name",
            "template_file",
        ):
            val = getattr(spec, field_name)
            assert val, f"{spec.value}.{field_name} 为空"
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
    spec = channel.get(raw)
    assert spec is not None and spec.value == expected


def test_get_unknown_returns_none() -> None:
    assert channel.get("tiktok") is None
    assert channel.get(None) is None
    assert channel.is_channel("tiktok") is False
    assert channel.is_channel("wechat") is True


def test_names_order_stable() -> None:
    assert channel.names() == ["wechat", "xiaohongshu", "x", "douyin"]


# ── 产出文件名：单目录 products/<id>-<slug>/，渠道名不进顶层路径 ──


def test_doc_filename_by_kind_and_channel() -> None:
    assert doc_filename("topic") == "brief.md"
    assert doc_filename("draft", "wechat") == "wechat.md"
    assert doc_filename("published", "x") == "x-pub.md"
    assert doc_filename("analytics") == "analytics.md"


def test_doc_filename_rejects_unknown_kind() -> None:
    with pytest.raises(ValueError):
        doc_filename("media")


# ── slug 工具（id_gen）────────────────────────────────────────


def test_slugify_title_keeps_chinese() -> None:
    from content.id_gen import slugify_title

    assert slugify_title("AI 视频创作指南") == "ai-视频创作指南"


def test_slugify_title_punctuation() -> None:
    from content.id_gen import slugify_title

    assert slugify_title("a/b\\c:d*?") == "a-b-c-d"


def test_slugify_title_truncates_and_empty() -> None:
    from content.id_gen import slugify_title

    assert slugify_title("x" * 80) == "x" * 60
    assert slugify_title("   ") == "untitled"


def test_slugify_anchor_dedup() -> None:
    from content.id_gen import slugify_anchor

    used: dict[str, int] = {}
    a = slugify_anchor("## 标题 A", used)
    b = slugify_anchor("## 标题 A", used)
    assert a != b
    assert b == f"{a}-1"


def test_slugify_anchor_html_stripped() -> None:
    from content.id_gen import slugify_anchor

    assert slugify_anchor("<em>强调</em>词") == "强调词"
