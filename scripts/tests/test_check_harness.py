"""`scripts/check_harness.py` 的自测：全绿夹具 + 每类检查一个负例。

夹具是一个最小化的、结构上完全合规的仓库；负例在它上面只改一处，断言非零退出**且**命中的
是预期检查项——避免「因为别的原因红了」被当成通过。
"""

# pyright: reportMissingImports=false

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import check_harness as ch

SKILL_HEAD = "---\nname: {name}\ndescription: 演示用\n---\n\n# {name}\n\n## 例子\n\n输入：甲 → 输出：乙\n"
PLAIN_FILES = (
    ".agents/notes/proposed/2026-01-01-demo.md",
    ".githooks/pre-commit",
    ".pi/AGENTS.md",
    ".pi/rules/demo.md",
    "assets/.gitkeep",
    "products/_inbox/.gitkeep",
    "system/PRODUCT.md",
    "system/CONVENTIONS.md",
)


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build(root: Path) -> Path:
    """最小全绿仓库：若干 skill + 消费者 + 共有数值的唯一权威文件。"""
    _write(root, "AGENTS.md", "# 入口\n")
    _write(root, "CONTEXT.md", "# 词表\n")
    _write(root, ".gitignore", "*.tmp\n")
    for rel in PLAIN_FILES:
        _write(root, rel, "# 演示\n")

    canonical: dict[str, list[str]] = {}
    for value, _dimension, source in ch.SHARED_VALUES:
        canonical.setdefault(source, []).append(value)
    for rel, values in canonical.items():
        body = "# 唯一来源\n\n" + "".join(f"- {value}\n" for value in values)
        _write(root, rel, body + (SKILL_HEAD.format(name="s") if rel.endswith("SKILL.md") else ""))

    _write(root, ".pi/skills/demo/SKILL.md", SKILL_HEAD.format(name="demo"))
    consumers = "".join(f"- [`{rel}`](../skills/{ch.skill_key(rel)}/SKILL.md)\n" for rel in ch.skill_files(root))
    _write(root, ".pi/agents/demo.md", f"# 岗位\n\n{consumers}")
    return root


def findings_for(root: Path, key: str) -> list[ch.Finding]:
    return [f for f in ch.run(root) if f.check.startswith(f"{key} ")]


def test_green_fixture_passes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    build(tmp_path)
    assert ch.run(tmp_path) == []
    assert ch.main(["--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.count("[PASS]") == len(ch.CHECKS)


def test_extra_top_level_entry_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    build(tmp_path)
    _write(tmp_path, "junk/note.md", "越界的顶层目录\n")
    hits = findings_for(tmp_path, "1")
    assert [f.message for f in hits] == ["junk/ —— 未允许的顶层项（允许 .agents .githooks .pi assets products scripts system）"]
    assert ch.main(["--root", str(tmp_path)]) == 1
    capsys.readouterr()


def test_skill_without_consumer_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    build(tmp_path)
    _write(tmp_path, ".pi/skills/orphan/SKILL.md", SKILL_HEAD.format(name="orphan"))
    hits = findings_for(tmp_path, "2")
    assert [f.message for f in hits] == [
        ".pi/skills/orphan/SKILL.md —— 无消费者：没有任何别的文件引用它的路径"
    ]
    assert ch.main(["--root", str(tmp_path)]) == 1
    capsys.readouterr()


def test_channel_name_in_path_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    build(tmp_path)
    _write(tmp_path, "products/T001-wechat/note.md", "渠道名以 slug 形式进了路径\n")
    _write(tmp_path, "assets/wechat/note.md", "渠道名直接占了路径段\n")
    hits = findings_for(tmp_path, "3")
    assert [f.message for f in hits] == [
        "assets/wechat/note.md —— 路径段 `wechat` 是渠道名",
        "products/T001-wechat/note.md —— 路径段 `T001-wechat` 是渠道名",
    ]
    assert ch.main(["--root", str(tmp_path)]) == 1
    capsys.readouterr()


def test_duplicated_shared_value_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    build(tmp_path)
    skill = tmp_path / ".pi/skills/demo/SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8") + "\n时长按 60–90s 走。\n", encoding="utf-8")
    hits = findings_for(tmp_path, "4")
    assert len(hits) == 1
    assert hits[0].message.startswith(".pi/skills/demo/SKILL.md —— ")
    assert "`60–90s`" in hits[0].message
    assert ch.main(["--root", str(tmp_path)]) == 1
    capsys.readouterr()


def test_broken_relative_ref_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    build(tmp_path)
    agent = tmp_path / ".pi/agents/demo.md"
    agent.write_text(agent.read_text(encoding="utf-8") + "\n见 [`gone`](../skills/gone/SKILL.md)。\n", encoding="utf-8")
    hits = findings_for(tmp_path, "5")
    assert hits and hits[0].message.endswith("链接目标不存在：../skills/gone/SKILL.md")
    assert ch.main(["--root", str(tmp_path)]) == 1
    capsys.readouterr()


def test_skill_without_example_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    build(tmp_path)
    _write(tmp_path, ".pi/skills/plain/SKILL.md", "# plain\n\n没有例子段。\n")
    _write(tmp_path, ".pi/agents/plain.md", "# 岗位\n\n- [`plain`](../skills/plain/SKILL.md)\n")
    hits = findings_for(tmp_path, "6")
    assert [f.message for f in hits] == [
        ".pi/skills/plain/SKILL.md —— 无例子段：既无「例子/真例/示例/Example」标题，也无输入→输出代码块"
    ]
    assert ch.main(["--root", str(tmp_path)]) == 1
    capsys.readouterr()


def test_platform_residue_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    build(tmp_path)
    _write(tmp_path, ".pi/rules/demo.md", "# 约束\n\n跨平台分发。\n")
    hits = findings_for(tmp_path, "7")
    assert [f.message for f in hits] == [".pi/rules/demo.md:3 —— 「平台」残留：跨平台分发。"]
    assert ch.main(["--root", str(tmp_path)]) == 1
    capsys.readouterr()


def test_platform_rule_line_is_whitelisted(tmp_path: Path) -> None:
    build(tmp_path)
    rule = "- 不在路径、字段、文档里使用「平台」指代渠道\n"
    _write(tmp_path, "system/CONVENTIONS.md", f"# 规范\n\n## 禁止项\n\n{rule}")
    assert findings_for(tmp_path, "7") == []
    # 同一文件里换个说法就重新计入——白名单是行级的，不是文件级的。
    _write(tmp_path, "system/CONVENTIONS.md", "# 规范\n\n不要用平台这个词。\n")
    assert findings_for(tmp_path, "7") != []
