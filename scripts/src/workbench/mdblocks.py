"""Markdown 块解析与写回。

块 = 一个锚点行及其内容，直到下一个分割锚点为止。两种锚点：

- 标题行（#~######）：分割规则 = 下一个**同级或更高级**标题；更深标题留在块内。
- 字段标签行（level 7，最深）：
  - H3 三字段：``integrated_multimodal_description:`` / ``overall_soundscape:`` / ``non_diegetic_music:``
  - 标准六元素：``- **scene**:`` / ``- **subject**:`` 等（``- **key**:`` 行）
  - 标签行总是分割前一块（含在标题块内部切块），使 prompt 文件可按字段独立编辑。

第一个锚点之前的内容算 preamble（level 0，可编辑）。
块 ID 由锚点文字 slug 化（重复追加序号），锚点文字不动则 ID 稳定。
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

_HEADER_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_H3_LABEL_RE = re.compile(
    r"^(integrated_multimodal_description|overall_soundscape|non_diegetic_music):(.*)$"
)
_STD_LABEL_RE = re.compile(r"^-\s+\*\*([A-Za-z_][\w-]*)\*\*:\s*(.*)$")


def _slug(title: str) -> str:
    """锚点文字 → 块 ID：保留中日韩/字母数字，其余折叠为 '-'。"""
    s = unicodedata.normalize("NFKC", title).strip().lower()
    s = re.sub(r"[`*_~\[\]()（）]", "", s)
    s = re.sub(r"[^0-9a-z\u4e00-\u9fff\u3040-\u30ff]+", "-", s).strip("-")
    return s or "block"


def _anchor(line: str) -> tuple[str, int, str] | None:
    """行 → (kind, level, title)；非锚点行返回 None。label 恒为 level 7。"""
    m = _HEADER_RE.match(line)
    if m:
        return "header", len(m.group(1)), m.group(2).strip()
    m = _H3_LABEL_RE.match(line)
    if m:
        return "label", 7, m.group(1)
    m = _STD_LABEL_RE.match(line)
    if m:
        return "label", 7, m.group(1)
    return None


def _anchors(text: str) -> list[tuple[int, str, int, str]]:
    """[(line_idx, kind, level, title)] 按行序。"""
    out: list[tuple[int, str, int, str]] = []
    for i, line in enumerate(text.split("\n")):
        a = _anchor(line)
        if a:
            out.append((i, a[0], a[1], a[2]))
    return out


def _splits(kind: str, level: int, next_kind: str, next_level: int) -> bool:
    """next 锚点是否分割 kind/level 的块。"""
    if next_kind == "label":
        return True  # 标签恒分割（含在标题块内部）
    return next_level <= level  # header 只被同级/更高级 header 分割


@dataclass
class Block:
    id: str
    kind: str  # "header" | "label" | "preamble"
    header: str  # 原始锚点行（preamble 为 ""）
    title: str  # 标题文字 / 标签名（preamble 为 "(前言)"）
    level: int  # header 1-6；label 7；preamble 0
    body: str  # 锚点行之后到下一分割锚点之前的原文（含内部空行）
    start: int  # 锚点行行号（preamble 为 0）
    end: int  # 块末尾行号（exclusive；preamble 到第一锚点）


def parse_blocks(text: str) -> list[Block]:
    lines = text.split("\n")
    anchors = _anchors(text)

    blocks: list[Block] = []
    if anchors:
        preamble = "\n".join(lines[: anchors[0][0]])
        if preamble.strip():
            blocks.append(
                Block("_preamble", "preamble", "", "(前言)", 0, preamble, 0, anchors[0][0])
            )

    used: dict[str, int] = {}
    for pos, (idx, kind, level, title) in enumerate(anchors):
        end = len(lines)
        for j in range(pos + 1, len(anchors)):
            if _splits(kind, level, anchors[j][1], anchors[j][2]):
                end = anchors[j][0]
                break
        body = "\n".join(lines[idx + 1 : end])
        base = _slug(title)
        n = used.get(base, 0) + 1
        used[base] = n
        bid = base if n == 1 else f"{base}-{n}"
        blocks.append(Block(bid, kind, lines[idx], title, level, body, idx, end))
    if not blocks:
        blocks.append(Block("_preamble", "preamble", "", "(全文)", 0, text, 0, len(lines)))
    return blocks


def get_block(text: str, block_id: str) -> Block | None:
    for b in parse_blocks(text):
        if b.id == block_id:
            return b
    return None


class BlockMismatch(Exception):
    """块内容已变（并发编辑/文件被其他方改动），拒绝写入。"""


def replace_block(text: str, block_id: str, expected_body: str, new_body: str) -> str:
    """替换块 body（锚点行保留）。expected_body 必须与当前 body 逐字一致。"""
    target = get_block(text, block_id)
    if target is None:
        raise KeyError(f"block not found: {block_id}")
    if target.body != expected_body:
        raise BlockMismatch(f"block body changed since load: {block_id}")

    lines = text.split("\n")
    if target.kind == "preamble":
        return new_body.rstrip("\n") + "\n"
    return "\n".join(lines[: target.start + 1] + new_body.split("\n") + lines[target.end :])
