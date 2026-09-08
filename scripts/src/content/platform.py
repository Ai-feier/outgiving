"""平台注册表 —— 平台属性的唯一事实源。

加一个新平台 = 这里加一行 PLATFORMS（+ id_gen.Platform 加一个成员；
scripts/tests/test_content_platform.py 的 drift 测试保证两边一致）。

所有平台属性收在 PlatformSpec：
- value:        ID/目录 token（稳定，历史数据在用，不可改）
- display:      中文显示名（CLI 表格、预览侧栏）
- emoji:        预览侧栏图标
- dir_name:     扫描目录（相对 repo 根）
- color_hex:    预览主色（hex）
- color_name:   预览 Tailwind 颜色名
- default_file: draft 主文件名（platforms/<plat>/<id>-<slug>/ 下）
- template_file: 写作模板（assets/templates/<file>）
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PlatformSpec:
    value: str
    display: str
    emoji: str
    dir_name: str
    color_hex: str
    color_name: str
    default_file: str
    template_file: str


PLATFORMS: dict[str, PlatformSpec] = {
    "wechat": PlatformSpec(
        value="wechat",
        display="微信公众号",
        emoji="💬",
        dir_name="platforms/wechat",
        color_hex="#07c160",
        color_name="emerald",
        default_file="article.md",
        template_file="wechat.md",
    ),
    "xiaohongshu": PlatformSpec(
        value="xiaohongshu",
        display="小红书",
        emoji="📕",
        dir_name="platforms/xiaohongshu",
        color_hex="#ff2442",
        color_name="rose",
        default_file="caption.md",
        template_file="xhs.md",
    ),
    "x": PlatformSpec(
        value="x",
        display="X",
        emoji="𝕏",
        dir_name="platforms/x",
        color_hex="#1d9bf0",
        color_name="sky",
        default_file="thread.md",
        template_file="x.md",
    ),
    "douyin": PlatformSpec(
        value="douyin",
        display="抖音",
        emoji="🎬",
        dir_name="platforms/douyin",
        color_hex="#fe2c55",
        color_name="pink",
        default_file="script.md",
        template_file="douyin.md",
    ),
}


def all() -> list[PlatformSpec]:
    """全部平台（注册顺序 = 展示顺序）。"""
    return list(PLATFORMS.values())


def names() -> list[str]:
    """平台 token 列表（注册顺序）。"""
    return list(PLATFORMS.keys())


def get(value: str | None) -> PlatformSpec | None:
    """按 token 查平台（归一化：大小写 / - / _ 不敏感）。未知 → None。"""
    if value is None:
        return None
    normalized = str(value).lower().replace("-", "").replace("_", "")
    for spec in PLATFORMS.values():
        if spec.value == normalized:
            return spec
    return None


def is_platform(value: str | None) -> bool:
    return get(value) is not None


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
