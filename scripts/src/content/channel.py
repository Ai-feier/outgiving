"""渠道注册表 —— 渠道属性的唯一事实源。

加一个新渠道 = 这里加一行 CHANNELS（+ id_gen.Channel 加一个成员；
scripts/tests/test_content_channels.py 的 drift 测试保证两边一致）。

所有渠道属性收在 ChannelSpec：
- value:         ID token（稳定，历史数据在用，不可改）
- display:       中文显示名（CLI 表格、预览侧栏）
- emoji:         预览侧栏图标
- color_hex:     预览主色（hex）
- color_name:    预览颜色名
- template_file: 写作模板（assets/templates/<file>）

渠道是出口参数，不是结构轴：渠道名不进顶层路径段。产出落在
products/<id>-<slug>/ 单目录内，以渠道名区分文件（见 id_gen.doc_filename）。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChannelSpec:
    value: str
    display: str
    emoji: str
    color_hex: str
    color_name: str
    template_file: str


CHANNELS: dict[str, ChannelSpec] = {
    "wechat": ChannelSpec(
        value="wechat",
        display="微信公众号",
        emoji="💬",
        color_hex="#07c160",
        color_name="emerald",
        template_file="wechat.md",
    ),
    "xiaohongshu": ChannelSpec(
        value="xiaohongshu",
        display="小红书",
        emoji="📕",
        color_hex="#ff2442",
        color_name="rose",
        template_file="xhs.md",
    ),
    "x": ChannelSpec(
        value="x",
        display="X",
        emoji="𝕏",
        color_hex="#1d9bf0",
        color_name="sky",
        template_file="x.md",
    ),
    "douyin": ChannelSpec(
        value="douyin",
        display="抖音",
        emoji="🎬",
        color_hex="#fe2c55",
        color_name="pink",
        template_file="douyin.md",
    ),
}


def all() -> list[ChannelSpec]:
    """全部渠道（注册顺序 = 展示顺序）。"""
    return list(CHANNELS.values())


def names() -> list[str]:
    """渠道 token 列表（注册顺序）。"""
    return list(CHANNELS.keys())


def get(value: str | None) -> ChannelSpec | None:
    """按 token 查渠道（归一化：大小写 / - / _ 不敏感）。未知 → None。"""
    if value is None:
        return None
    normalized = str(value).lower().replace("-", "").replace("_", "")
    for spec in CHANNELS.values():
        if spec.value == normalized:
            return spec
    return None


def is_channel(value: str | None) -> bool:
    return get(value) is not None
