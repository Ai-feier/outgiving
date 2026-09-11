"""人审表 —— 人在任何时刻只面对的一张表。

`products/<id>-<slug>/review.md` 是唯一事实源：一张表 + 表下固定块
（关键决策 / 未锚假设 / 待你拍板）+ 追问区（待回答）。

人的四个动作只写回这一个文件：

- 改表：直接改任一格
- 追问：对某一行问「为什么这么定」，进「待回答」
- 拍板：对「待你拍板」项做决定
- 验收：逐条核对该表是否满足初衷，结论写回 frontmatter

agent 内部件（思考过程、执行记录、单元分节、对齐自报、门记录）不进人视野。
本模块只做解析 / 渲染 / 写回，不承载任何流程状态机。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # .../outgiving
PRODUCTS_DIR = ROOT / "products"

REVIEW_FILE = "review.md"

VIDEO_FIELDS = ("拍", "秒", "画面（一句话）", "景别", "运镜", "台词/字幕")
TEXT_FIELDS = ("段", "作用", "要点", "证据锚点", "字数")

# 表下固定三块 + 追问区；渲染顺序固定，缺则补空
SECTION_ORDER = ("关键决策", "未锚假设", "待你拍板", "待回答")

VERDICTS = ("通过", "打回")

_FM_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
_ITEM_RE = re.compile(r"^-\s+(?:\[[ xX]\]\s*)?(.*)$")
_DECIDED_RE = re.compile(r"\s*→\s*决定[:：].*$")


class ReviewError(ValueError):
    """人审表操作非法（未知字段 / 未知行 / 未知项）。"""


@dataclass
class Review:
    """一张人审表。meta = frontmatter，rows = 表体（cells 已 strip）。"""

    meta: dict[str, str] = field(default_factory=dict[str, str])
    fields: list[str] = field(default_factory=list[str])
    rows: list[list[str]] = field(default_factory=list[list[str]])
    sections: dict[str, list[str]] = field(default_factory=dict[str, list[str]])

    @property
    def heading(self) -> str:
        return " · ".join(x for x in (self.meta.get("id"), self.meta.get("title")) if x)

    def row(self, key: str) -> list[str]:
        """按首格取值定位行（视频 = 拍号，文本 = 段号）。"""
        for cells in self.rows:
            if cells and cells[0] == key:
                return cells
        raise ReviewError(f"表中没有 {self.fields[0] if self.fields else '行'} {key}")

    def section(self, name: str) -> list[str]:
        return self.sections.setdefault(name, [])


# ── 解析 / 序列化 ────────────────────────────────────────────


def _cells(line: str) -> list[str]:
    s = line.strip().removeprefix("|").removesuffix("|")
    return [c.strip() for c in s.split("|")]


def _is_separator(line: str) -> bool:
    cells = _cells(line)
    return bool(cells) and all(c and set(c) <= set("-:") for c in cells)


def _trim(lines: list[str]) -> list[str]:
    out = list(lines)
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def parse(text: str) -> Review:
    """review.md 文本 → Review。frontmatter 只认扁平 `key: value`。"""
    meta: dict[str, str] = {}
    body = text
    fm = _FM_RE.match(text)
    if fm:
        for line in fm.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        body = text[fm.end() :]

    fields: list[str] = []
    rows: list[list[str]] = []
    sections: dict[str, list[str]] = {}
    current: str | None = None

    for line in body.split("\n"):
        head = _HEADING_RE.match(line)
        if head:
            name = head.group(1)
            current = name
            sections.setdefault(name, [])
            continue
        if current is None:
            if not line.strip().startswith("|"):
                continue
            if not fields:
                fields = _cells(line)
            elif _is_separator(line):
                continue
            else:
                rows.append(_cells(line))
            continue
        sections[current].append(line)

    return Review(
        meta=meta,
        fields=fields,
        rows=rows,
        sections={k: _trim(v) for k, v in sections.items()},
    )


def _ordered_sections(sections: dict[str, list[str]]) -> list[str]:
    """固定块按 SECTION_ORDER 在前，其余保持原序。"""
    names = [n for n in SECTION_ORDER]
    names += [n for n in sections if n not in SECTION_ORDER]
    return names


def render_md(review: Review) -> str:
    """Review → 规范形状的 review.md 文本（表列宽对齐，不做逐字保留）。"""
    out: list[str] = ["---\n"]
    for k, v in review.meta.items():
        out.append(f"{k}: {v}\n")
    out.append("---\n\n")
    out.append(f"# 人审表 · {review.heading}\n\n")

    out.append("| " + " | ".join(review.fields) + " |\n")
    out.append("| " + " | ".join("---" for _ in review.fields) + " |\n")
    for cells in review.rows:
        padded = list(cells) + [""] * (len(review.fields) - len(cells))
        out.append("| " + " | ".join(padded[: len(review.fields)]) + " |\n")

    for name in _ordered_sections(review.sections):
        out.append(f"\n## {name}\n\n")
        body = review.sections.get(name) or []
        if body:
            out.append("\n".join(body) + "\n")
    return "".join(out)


def render_console(review: Review, width: int = 120) -> str:
    """Review → 单页终端视图：表 + 表下固定块。人审只需看这一段。"""
    from rich.console import Console
    from rich.table import Table

    buf = StringIO()
    console = Console(file=buf, width=width, no_color=True, force_terminal=False, highlight=False)

    console.print(f"[bold]{review.heading}[/bold]")
    for key in ("形态", "阶段", "初衷", "验收", "验收备注"):
        if review.meta.get(key):
            console.print(f"{key}：{review.meta[key]}")
    console.print()

    table = Table(show_header=True, header_style="bold", box=None, pad_edge=False)
    for name in review.fields:
        table.add_column(name)
    for cells in review.rows:
        table.add_row(*[cells[i] if i < len(cells) else "" for i in range(len(review.fields))])
    console.print(table)

    for name in _ordered_sections(review.sections):
        body = review.sections.get(name) or []
        console.print(f"\n[bold]## {name}[/bold]")
        if not body:
            console.print("（空）")
            continue
        for line in body:
            console.print(line if line.strip() else "")
    return buf.getvalue()


# ── 读写 ────────────────────────────────────────────────────


def project_review_path(project: str, root: Path | None = None) -> Path:
    """选题 id（T006）→ products/<id>-<slug>/review.md。"""
    base = PRODUCTS_DIR if root is None else root
    if not base.is_dir():
        raise FileNotFoundError(f"products 目录不存在: {base}")
    exact = base / project
    if exact.is_dir():
        return exact / REVIEW_FILE
    matches = sorted(d for d in base.iterdir() if d.is_dir() and d.name.startswith(f"{project}-"))
    if len(matches) == 1:
        return matches[0] / REVIEW_FILE
    if not matches:
        raise FileNotFoundError(f"没找到选题目录: {base}/{project}*")
    raise ReviewError(f"选题目录不唯一: {[m.name for m in matches]}")


def load(path: Path) -> Review:
    if not path.is_file():
        raise FileNotFoundError(f"人审表不存在: {path}")
    return parse(path.read_text(encoding="utf-8"))


def save(path: Path, review: Review) -> None:
    path.write_text(render_md(review), encoding="utf-8")


def load_project(project: str, root: Path | None = None) -> tuple[Path, Review]:
    path = project_review_path(project, root)
    return path, load(path)


# ── 四个动作 ────────────────────────────────────────────────


def edit(review: Review, row_key: str, field_name: str, value: str) -> Review:
    """改表：把 <row_key> 行的 <field_name> 一格改成 <value>。"""
    if field_name not in review.fields:
        raise ReviewError(f"表里没有这一格: {field_name}（可选：{' / '.join(review.fields)}）")
    cells = review.row(row_key)
    cells[review.fields.index(field_name)] = value
    return review


def ask(review: Review, row_key: str, question: str) -> Review:
    """追问：对某一行问「为什么这么定」，写进「待回答」。"""
    review.row(row_key)  # 行必须存在——追问挂在一行上
    label = f"{review.fields[0]} {row_key}" if review.fields else row_key
    body = review.section("待回答")
    if body and body[-1].strip():
        body.append("")
    body.append(f"- {label}：{question}")
    return review


def decide(review: Review, index: int, decision: str) -> Review:
    """拍板：对「待你拍板」第 <index> 项（1 起）做决定。"""
    body = review.section("待你拍板")
    items = [i for i, line in enumerate(body) if _ITEM_RE.match(line.strip())]
    if not items:
        raise ReviewError("「待你拍板」是空的，没有可拍板的项")
    if index < 1 or index > len(items):
        raise ReviewError(f"「待你拍板」只有 {len(items)} 项，给的是 {index}")
    at = items[index - 1]
    text = _DECIDED_RE.sub("", _ITEM_RE.match(body[at].strip()).group(1)).strip()  # type: ignore[union-attr]
    body[at] = f"- [x] {text} → 决定：{decision}"
    return review


def accept(review: Review, verdict: str, note: str = "") -> Review:
    """验收：逐条核对后给结论，写回 frontmatter。"""
    if verdict not in VERDICTS:
        raise ReviewError(f"验收结论须 ∈ {' / '.join(VERDICTS)}")
    review.meta["验收"] = verdict
    if note:
        review.meta["验收备注"] = note
    return review
