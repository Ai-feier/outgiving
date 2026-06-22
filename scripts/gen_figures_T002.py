"""Generate 3 figures for T002.

Figure 1: prompt vs skill (对照/对比)
Figure 2: decision tree for what to skill (序列)
Figure 3: three-layer evolution: Prompt -> Skill -> Harness (层级)

手绘风. 白底黑线 + #d97757 唯一强调色.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "topics" / "T002-skill-设计：从调-prompt-到建工作流" / "assets"
OUT.mkdir(exist_ok=True)

BLACK = "#1e1e1e"
ACCENT = "#d97757"
LIGHT = "#e8e6dc"
GRAY = "#b0aea5"
INFO = "#767676"  # ~4.5:1 on white, WCAG AA compliant

_id = [0]


def nid():
    _id[0] += 1
    return f"e{_id[0]}"


# ── Excalidraw element builders ──

def _ex_rect(x, y, w, h, bg="transparent", stroke=BLACK, sw=2):
    return {
        "type": "rectangle", "id": nid(), "version": 1, "versionNonce": 1,
        "isDeleted": False,
        "fillStyle": "hachure" if bg != "transparent" else "solid",
        "strokeWidth": sw, "strokeStyle": "solid", "roughness": 1.3,
        "opacity": 100, "angle": 0, "x": x, "y": y,
        "strokeColor": stroke, "backgroundColor": bg,
        "width": w, "height": h, "seed": _id[0],
        "groupIds": [], "frameId": None,
        "roundness": {"type": 3}, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
    }


def _ex_text(x, y, w, h, s, size=20, color=BLACK, bold=False, align="center"):
    return {
        "type": "text", "id": nid(), "version": 1, "versionNonce": 1,
        "isDeleted": False,
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "angle": 0,
        "x": x, "y": y, "strokeColor": color,
        "backgroundColor": "transparent", "width": w, "height": h,
        "seed": _id[0], "groupIds": [], "frameId": None,
        "roundness": None, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
        "fontSize": size, "fontFamily": 1,
        "text": s, "textAlign": align, "verticalAlign": "middle",
        "containerId": None, "originalText": s, "lineHeight": 1.25,
    }


def _ex_arrow(x1, y1, x2, y2, color=ACCENT, sw=2, dash="solid"):
    return {
        "type": "arrow", "id": nid(), "version": 1, "versionNonce": 1,
        "isDeleted": False,
        "fillStyle": "solid", "strokeWidth": sw,
        "strokeStyle": dash, "roughness": 1.2,
        "opacity": 100, "angle": 0,
        "x": x1, "y": y1, "strokeColor": color,
        "backgroundColor": "transparent",
        "width": x2 - x1, "height": y2 - y1,
        "seed": _id[0], "groupIds": [], "frameId": None,
        "roundness": {"type": 2}, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
        "startBinding": None, "endBinding": None,
        "lastCommittedPoint": None,
        "startArrowhead": None, "endArrowhead": "arrow",
        "points": [[0, 0], [x2 - x1, y2 - y1]],
    }


def _ex_line(x1, y1, x2, y2, color=BLACK, sw=2, dash="solid"):
    return {
        "type": "line", "id": nid(), "version": 1, "versionNonce": 1,
        "isDeleted": False,
        "fillStyle": "solid", "strokeWidth": sw,
        "strokeStyle": dash, "roughness": 1.2,
        "opacity": 100, "angle": 0,
        "x": x1, "y": y1, "strokeColor": color,
        "backgroundColor": "transparent",
        "width": x2 - x1, "height": y2 - y1,
        "seed": _id[0], "groupIds": [], "frameId": None,
        "roundness": {"type": 2}, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
        "startBinding": None, "endBinding": None,
        "lastCommittedPoint": None,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
    }


def _ex_path(points, color=BLACK, sw=2, dash="solid"):
    """Polyline path: list of (dx, dy) from origin."""
    return {
        "type": "line", "id": nid(), "version": 1, "versionNonce": 1,
        "isDeleted": False,
        "fillStyle": "solid", "strokeWidth": sw,
        "strokeStyle": dash, "roughness": 1.2,
        "opacity": 100, "angle": 0,
        "x": points[0][0], "y": points[0][1],
        "strokeColor": color,
        "backgroundColor": "transparent",
        "width": points[-1][0] - points[0][0],
        "height": points[-1][1] - points[0][1],
        "seed": _id[0], "groupIds": [], "frameId": None,
        "roundness": {"type": 2}, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
        "startBinding": None, "endBinding": None,
        "lastCommittedPoint": None,
        "points": [[p[0] - points[0][0], p[1] - points[0][1]] for p in points],
    }


def _ex_doc(elements, title):
    return {
        "type": "excalidraw", "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "grid": False,
            "viewBackgroundColor": "#ffffff",
            "currentItemFontFamily": 1,
        },
        "files": {},
        "name": title,
    }


# ── SVG renderers ──

def _svg_rect(x, y, w, h, bg="transparent", stroke=BLACK, sw=2):
    fill = bg if bg != "transparent" else "none"
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" ry="6" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _svg_text(x, y, s, size=20, color=BLACK, bold=False, align="center"):
    weight = "700" if bold else "400"
    anchor = {"center": "middle", "left": "start", "right": "end"}[align]
    lines = s.split("\n")
    tspans = "".join(
        f'<tspan x="{x}" dy="{1.2 if i == 0 else 1.2}em">{ln}</tspan>'
        for i, ln in enumerate(lines)
    )
    return (f'<text x="{x}" y="{y}" '
            f'font-family="Virgil, Segoe UI, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}" '
            f'text-anchor="{anchor}" dominant-baseline="middle">'
            f'{tspans}</text>')


def _svg_arrow(x1, y1, x2, y2, color=ACCENT, sw=2, dash="solid"):
    da = "6,3" if dash == "dashed" else "none"
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{sw}" stroke-dasharray="{da}" '
            f'marker-end="url(#arrow-{color[1:]})" '
            f'stroke-linecap="round"/>')


def _svg_line(x1, y1, x2, y2, color=BLACK, sw=2, dash="solid"):
    da = "6,3" if dash == "dashed" else "none"
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{sw}" stroke-dasharray="{da}" '
            f'stroke-linecap="round"/>')


def _svg_path(pts, color=BLACK, sw=2, dash="solid", arrowhead=True):
    """Polyline: pts = [(x,y), ...], first is origin."""
    da = "6,3" if dash == "dashed" else "none"
    d = " ".join(f"L {x} {y}" if i > 0 else f"M {x} {y}" for i, (x, y) in enumerate(pts))
    marker = f'marker-end="url(#arrow-{color[1:]})"' if arrowhead else ""
    return f'<path d="{d}" stroke="{color}" stroke-width="{sw}" stroke-dasharray="{da}" fill="none" {marker} stroke-linecap="round" stroke-linejoin="round"/>'


def _svg_wrap(content, w, h, title):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Virgil, 'Segoe UI', sans-serif">
  <defs>
    <marker id="arrow-{ACCENT[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/>
    </marker>
    <marker id="arrow-{BLACK[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="{BLACK}"/>
    </marker>
    <marker id="arrow-{GRAY[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="{GRAY}"/>
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="white"/>
{content}
  <title>{title}</title>
</svg>'''


# ── Figures ──

# ---------------------------------------------------------------------------
# FIGURE 1: Prompt vs Skill (对照)
# Canvas 900 x 360
# ---------------------------------------------------------------------------

def fig1():
    ex = []
    svg = []

    # -- Left column: Prompt --
    # Title
    ex.append(_ex_text(80, 12, 200, 35, "Prompt 裸指令", 26, BLACK, bold=True))
    svg.append(_svg_text(80, 33, "Prompt 裸指令", 26, BLACK, bold=True, align="left"))

    # Prompt box (thin, no fill)
    ex.append(_ex_rect(40, 65, 220, 60, "transparent"))
    svg.append(_svg_rect(40, 65, 220, 60, "transparent"))
    ex.append(_ex_text(150, 95, 200, 25, "一次性 · 无结构", 16))
    svg.append(_svg_text(150, 95, "一次性 · 无结构", 16))

    # Arrow: dashed, gray, pointing to "?"
    ex.append(_ex_arrow(150, 125, 150, 195, GRAY, 2, "dashed"))
    svg.append(_svg_arrow(150, 125, 150, 195, color=GRAY, sw=2, dash="dashed"))

    # "?" mark (orange, large, bold)
    ex.append(_ex_text(135, 195, 30, 50, "?", 46, ACCENT, bold=True))
    svg.append(_svg_text(150, 220, "?", 46, ACCENT, bold=True))

    # Annotation
    ex.append(_ex_text(150, 255, 180, 25, "输出不可预测", 15, GRAY))
    svg.append(_svg_text(150, 268, "输出不可预测", 15, GRAY))

    # -- Center divider --
    ex.append(_ex_line(450, 30, 450, 330, GRAY, 1, "dashed"))
    svg.append(_svg_line(450, 30, 450, 330, GRAY, 1, "dashed"))

    # -- Right column: Skill --
    # Title (orange, emphasized)
    ex.append(_ex_text(580, 12, 200, 35, "Skill 封装", 26, ACCENT, bold=True))
    svg.append(_svg_text(685, 33, "Skill 封装", 26, ACCENT, bold=True))

    # Skill structured box (light fill, showing internal structure)
    ex.append(_ex_rect(540, 65, 290, 105, LIGHT))
    svg.append(_svg_rect(540, 65, 290, 105, LIGHT))

    ex.append(_ex_text(685, 88, 260, 25, "结构化 context 封装", 17, BLACK, bold=True))
    svg.append(_svg_text(685, 88, "结构化 context 封装", 17, BLACK, bold=True))

    # Four pillars inside skill
    ex.append(_ex_text(685, 120, 260, 25, "规则 · 流程 · 上下文 · 验证", 14, BLACK))
    svg.append(_svg_text(685, 120, "规则 · 流程 · 上下文 · 验证", 14, BLACK))

    # Input/output hint below pillars
    ex.append(_ex_text(685, 148, 260, 20, "按需注入的 context 单元", 13, INFO))
    svg.append(_svg_text(685, 148, "按需注入的 context 单元", 13, INFO))

    # Arrow: solid, thick, orange, pointing to checkmark
    ex.append(_ex_arrow(685, 170, 685, 215, ACCENT, 3, "solid"))
    svg.append(_svg_arrow(685, 170, 685, 215, ACCENT, 3))

    # Checkmark
    ex.append(_ex_text(668, 212, 30, 50, "✓", 46, ACCENT, bold=True))
    svg.append(_svg_text(685, 235, "✓", 46, ACCENT, bold=True))

    # Annotation
    ex.append(_ex_text(685, 255, 200, 25, "输出稳定可复用", 16, ACCENT, bold=True))
    svg.append(_svg_text(685, 268, "输出稳定可复用", 16, ACCENT, bold=True))

    # Footnote: data evidence
    note = "契约式 skill: 错误率 8.3% → 1.3% (Liu, arXiv:2605.22634, 2026)"
    ex.append(_ex_text(540, 310, 300, 20, note, 12, INFO))
    svg.append(_svg_text(685, 325, note, 12, INFO))

    return _ex_doc(ex, "fig1-prompt-vs-skill"), _svg_wrap("\n".join(svg), 900, 360, "fig1-prompt-vs-skill")


# ---------------------------------------------------------------------------
# FIGURE 2: Decision tree (序列)
# Canvas 820 x 400
# ---------------------------------------------------------------------------

def fig2():
    ex = []
    svg = []

    SPINE = 290  # x-center of decision boxes
    BW = 200     # box width
    BH = 50      # box height

    def decision(y, text):
        """Add a decision box centered at SPINE x."""
        x = SPINE - BW // 2
        ex.append(_ex_rect(x, y, BW, BH, LIGHT))
        svg.append(_svg_rect(x, y, BW, BH, LIGHT))
        ex.append(_ex_text(SPINE, y + BH // 2, BW - 20, BH - 10, text, 16, BLACK, bold=True))
        svg.append(_svg_text(SPINE, y + BH // 2, text, 16, BLACK, bold=True))
        return x

    def leaf_yes(y):
        """Orange '建 Skill' leaf."""
        x = SPINE - 80
        ex.append(_ex_rect(x, y, 160, 55, ACCENT))
        svg.append(_svg_rect(x, y, 160, 55, ACCENT))
        ex.append(_ex_text(SPINE, y + 28, 140, 30, "建 Skill", 18, "#ffffff", bold=True))
        svg.append(_svg_text(SPINE, y + 28, "建 Skill", 18, "#ffffff", bold=True))

    def leaf_no(y):
        """Gray '保留为 Prompt' leaf."""
        x = 530
        ex.append(_ex_rect(x, y, 150, 40, "transparent", GRAY, 1.5))
        svg.append(_svg_rect(x, y, 150, 40, "transparent", GRAY, 1.5))
        ex.append(_ex_text(x + 75, y + 20, 140, 20, "保留为 Prompt", 14, GRAY))
        svg.append(_svg_text(x + 75, y + 20, "保留为 Prompt", 14, GRAY))

    def yes_arrow(y_from):
        """Vertical arrow (Yes → next level)."""
        y_mid = y_from + BH
        y_to = y_mid + GAP
        ex.append(_ex_arrow(SPINE, y_mid, SPINE, y_to, BLACK, 2))
        svg.append(_svg_arrow(SPINE, y_mid, SPINE, y_to, BLACK, 2))
        # "是" label
        ex.append(_ex_text(SPINE - 70, y_mid + 5, 30, 18, "是", 14, ACCENT))
        svg.append(_svg_text(SPINE - 50, y_mid + 18, "是", 14, ACCENT))

    def no_arrow(y_from, y_leaf):
        """L-shaped arrow (No → leaf)."""
        x_from = SPINE + BW // 2
        y_mid = y_from + BH // 2
        x_leaf = 530
        y_leaf_mid = y_leaf + 20
        # Horizontal segment + vertical segment with arrowhead
        # SVG: use path
        svg.append(_svg_path([
            (x_from, y_mid),
            (x_leaf, y_mid),
            (x_leaf, y_leaf_mid),
        ], GRAY, 1.5))
        # Excalidraw: use a polyline
        ex.append(_ex_path([
            (x_from, y_mid),
            (x_leaf, y_mid),
            (x_leaf, y_leaf_mid),
        ], GRAY, 1.5))
        # "否" label
        ex.append(_ex_text(x_from + 30, y_mid - 22, 25, 18, "否", 13, GRAY))
        svg.append(_svg_text(x_from + 45, y_mid - 8, "否", 13, GRAY))

    # Layer spacing
    GAP = 30
    Y1 = 18
    Y2 = Y1 + BH + GAP
    Y3 = Y2 + BH + GAP
    Y4 = Y3 + BH + GAP  # final leaf — arrow ends right at top of leaf

    # Level 1
    decision(Y1, "重复 ≥3 次？")
    leaf_no(Y1 - 2)
    no_arrow(Y1, Y1 - 2)
    yes_arrow(Y1)

    # Level 2
    decision(Y2, "明确输入输出？")
    leaf_no(Y2 - 2)
    no_arrow(Y2, Y2 - 2)
    yes_arrow(Y2)

    # Level 3
    decision(Y3, "收益 > context 开销？")
    leaf_no(Y3 - 2)
    no_arrow(Y3, Y3 - 2)

    # Final Yes arrow
    yes_arrow(Y3)

    # Final leaf: 建 Skill
    leaf_yes(Y4)

    # Title at top
    ex.append(_ex_text(SPINE, 0, 300, 20, "什么值得封装？", 15, ACCENT))
    svg.append(_svg_text(SPINE, 12, "什么值得封装？", 15, ACCENT))

    return _ex_doc(ex, "fig2-skill-decision-tree"), _svg_wrap("\n".join(svg), 820, Y4 + 70, "fig2-skill-decision-tree")


# ---------------------------------------------------------------------------
# FIGURE 3: Three-layer evolution (层级)
# Canvas 760 x 500
# ---------------------------------------------------------------------------

def fig3():
    ex = []
    svg = []

    CX = 380  # center x

    # -- Layer 1: Prompt (bottom) --
    PY = 345
    PW, PH = 260, 60
    PX = CX - PW // 2
    ex.append(_ex_rect(PX, PY, PW, PH, "transparent"))
    svg.append(_svg_rect(PX, PY, PW, PH, "transparent"))
    ex.append(_ex_text(CX, PY + 18, PW - 10, 25, "Prompt", 22, BLACK, bold=True))
    svg.append(_svg_text(CX, PY + 18, "Prompt", 22, BLACK, bold=True))
    ex.append(_ex_text(CX, PY + 43, PW - 10, 18, "你问了什么 · 一次性", 14, INFO))
    svg.append(_svg_text(CX, PY + 43, "你问了什么 · 一次性", 14, INFO))

    # -- Layer 2: Skill (middle) --
    SY = 230
    SW, SH = 380, 80
    SX = CX - SW // 2
    ex.append(_ex_rect(SX, SY, SW, SH, LIGHT))
    svg.append(_svg_rect(SX, SY, SW, SH, LIGHT))
    ex.append(_ex_text(CX, SY + 20, SW - 20, 25, "Skill", 22, BLACK, bold=True))
    svg.append(_svg_text(CX, SY + 20, "Skill", 22, BLACK, bold=True))
    ex.append(_ex_text(CX, SY + 43, SW - 20, 18, "可复用的能力单元", 15, BLACK))
    svg.append(_svg_text(CX, SY + 43, "可复用的能力单元", 15, BLACK))
    ex.append(_ex_text(CX, SY + 63, SW - 20, 16, "规则 · 流程 · 上下文 · 验证", 13, INFO))
    svg.append(_svg_text(CX, SY + 63, "规则 · 流程 · 上下文 · 验证", 13, INFO))

    # -- Layer 3: Harness (top) --
    HY = 105
    HW, HH = 540, 90
    HX = CX - HW // 2
    ex.append(_ex_rect(HX, HY, HW, HH, LIGHT, ACCENT, 2.5))
    svg.append(_svg_rect(HX, HY, HW, HH, LIGHT, ACCENT, 2.5))
    ex.append(_ex_text(CX, HY + 22, HW - 20, 25, "Harness", 22, ACCENT, bold=True))
    svg.append(_svg_text(CX, HY + 22, "Harness", 22, ACCENT, bold=True))
    ex.append(_ex_text(CX, HY + 45, HW - 20, 18, "包裹 skill 的系统外壳", 15, ACCENT))
    svg.append(_svg_text(CX, HY + 45, "包裹 skill 的系统外壳", 15, ACCENT))
    ex.append(_ex_text(CX, HY + 66, HW - 20, 18, "编排 · 循环检测 · 自动映射 · 出口验证", 13, INFO))
    svg.append(_svg_text(CX, HY + 66, "编排 · 循环检测 · 自动映射 · 出口验证", 13, INFO))

    # -- Upward arrows between layers --
    # Prompt top → Skill bottom: (380, 345) → (380, 310)
    ex.append(_ex_arrow(CX, PY, CX, SY + SH, ACCENT, 2.5))
    svg.append(_svg_arrow(CX, PY, CX, SY + SH, ACCENT, 2.5))
    # Skill top → Harness bottom: (380, 230) → (380, 195)
    ex.append(_ex_arrow(CX, SY, CX, HY + HH, ACCENT, 2.5))
    svg.append(_svg_arrow(CX, SY, CX, HY + HH, ACCENT, 2.5))

    # -- Right-side annotations (inside Harness, outside Skill) --
    # Prompt layer annotation at right
    ex.append(_ex_text(620, PY + 30, 140, 18, "一次性的问法", 13, INFO))
    svg.append(_svg_text(620, PY + 30, "一次性的问法", 13, INFO, align="left"))
    # Skill layer annotation at right
    ex.append(_ex_text(620, SY + 40, 140, 18, "封装好的能力单元", 13, INFO))
    svg.append(_svg_text(620, SY + 40, "封装好的能力单元", 13, INFO, align="left"))
    # Harness layer annotation at right
    ex.append(_ex_text(620, HY + 45, 140, 18, "系统外壳 + 编排", 13, ACCENT))
    svg.append(_svg_text(620, HY + 45, "系统外壳 + 编排", 13, ACCENT, align="left"))

    # -- Bottom callout --
    ex.append(_ex_text(CX, PY + 85, 360, 20, "每层封装消除一层不确定性", 14, ACCENT, bold=True))
    svg.append(_svg_text(CX, PY + 85, "每层封装消除一层不确定性", 14, ACCENT, bold=True))

    # -- Formula --
    formula = "Prompt  ⊂  Skill  ⊂  Harness"
    ex.append(_ex_text(CX, PY + 110, 360, 22, formula, 18, BLACK, bold=True))
    svg.append(_svg_text(CX, PY + 110, formula, 18, BLACK, bold=True))

    # -- LangChain data --
    bench = "不换模型只改 harness: 52.8% → 66.5% (+26%)  —  LangChain Terminal Bench 2.0, 2026"
    ex.append(_ex_text(CX, PY + 132, 500, 16, bench, 12, INFO))
    svg.append(_svg_text(CX, PY + 132, bench, 12, INFO))

    H = PY + 150
    return _ex_doc(ex, "fig3-three-layer-evolution"), _svg_wrap("\n".join(svg), 780, H, "fig3-three-layer-evolution")


# ── Main ──

if __name__ == "__main__":
    for fn, slug in [
        (fig1, "fig1-prompt-vs-skill"),
        (fig2, "fig2-skill-decision-tree"),
        (fig3, "fig3-three-layer-evolution"),
    ]:
        _id[0] = 0
        ex_data, svg_data = fn()
        (OUT / f"{slug}.excalidraw").write_text(
            json.dumps(ex_data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (OUT / f"{slug}.svg").write_text(svg_data, encoding="utf-8")
        print(f"  {slug}.excalidraw + {slug}.svg")
    print(f"\nOutput: {OUT}")
