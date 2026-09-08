"""T005 → v4.1 迁移（一次性，2026-08-26）。

旧 4 节（① 简层 / ② 思考 / ③ 执行 / end 结果 + 段: 字段）→ 新 5 层
（① 简层 / ② 思考 / ③ 内容详情 / ④ 执行 / ⑤ 结果 + 层: 字段）。

设计单元：② 里的设计内容块挪进 ③；假设与未锚 + grill 记录留 ②；
旧 end 结果 → ⑤；旧 ③ 执行 → ④。
幂等：已迁移文件（含 `## ③ 内容详情`）跳过。
"""

from pathlib import Path

T005 = Path(__file__).parent

# 设计单元：② 内挪入 ③ 的内容块起点；终点 = 假设与未锚（各文件同在 ② 尾部）
DESIGN_SPLIT = {
    "research.md": "#### 1. 事实锚点（可引用）",
    "script.md": "#### 元信息",
    "visual.md": "#### 1. 视觉形态",
    "rhythm.md": "#### 元信息",
    "director.md": "#### 0. 工具决策与上游约束确认（Warm）",
}
ASSUME = "### 假设与未锚"
# rhythm 特有：对齐自报小节挪 ⑤（新契约：对齐自报在 ⑤）
EXTRA_TO_5 = {"rhythm.md": "#### 对齐自报（收口于本单元 end 结果）"}
GATE_UNITS = {"director.md", "seg1.md", "seg2.md", "end.md"}


def migrate(name: str) -> None:
    p = T005 / name
    text = p.read_text(encoding="utf-8")
    if "## ③ 内容详情" in text:
        print(f"skip（已迁移）: {name}")
        return

    # frontmatter：段 → 层
    text = text.replace("段: p1", "层: l1").replace("段: p2", "层: l2")
    # gate（frontmatter 段内插 gate: 是）
    if name in GATE_UNITS and "gate:" not in text.split("---")[1]:
        text = text.replace("层: l", "gate: 是\n层: l", 1)
    # 节改名
    text = text.replace("## ③ 执行", "## ④ 执行").replace("## end 结果", "## ⑤ 结果")

    i4 = text.index("## ④ 执行")
    if name in DESIGN_SPLIT:
        m_start = DESIGN_SPLIT[name]
        i2 = text.index("## ② 思考")
        region = text[i2 + len("## ② 思考") : i4]
        j = region.index(m_start)
        k = region.index(ASSUME, j)  # 假设与未锚在设计块之后
        keep_top = region[:j].rstrip() + "\n\n"
        moved = region[j:k]
        tail = region[k:].rstrip() + "\n\n"  # 假设与未锚 段（到 ④ 为止）
        extra5 = ""
        marker = EXTRA_TO_5.get(name)
        if marker and marker in moved:
            m5 = moved.index(marker)
            extra5 = "\n" + moved[m5:].rstrip() + "\n"
            moved = moved[:m5]
        new_2 = f"## ② 思考\n{keep_top}{tail}### grill 记录\n\n"
        new_3 = f"## ③ 内容详情\n{moved.rstrip()}\n\n"
        text = text[:i2] + new_2 + new_3 + text[i4:]
        if extra5:
            i5 = text.index("## ⑤ 结果")
            text = text[:i5] + "## ⑤ 结果" + extra5 + text[i5 + len("## ⑤ 结果") :]
    else:
        if "### grill 记录" not in text[:i4]:
            text = text[:i4].rstrip() + "\n\n### grill 记录\n\n" + text[i4:]

    p.write_text(text, encoding="utf-8")
    print(f"migrated: {name}")


for name in [
    "goal.md",
    "research.md",
    "script.md",
    "visual.md",
    "rhythm.md",
    "director.md",
    "seg1.md",
    "goal2.md",
    "seg2.md",
    "end.md",
]:
    migrate(name)
print("done")
