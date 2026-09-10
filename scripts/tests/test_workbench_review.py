"""人审表（products/<id>-<slug>/review.md）渲染与四个写回动作的契约测试。

契约：改表 / 追问 / 拍板 / 验收四个动作只写回这一个文件——人审不需要打开任何其他文件。
运行方式：uv run --directory scripts pytest tests/test_workbench_review.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from workbench import review as R
from workbench.cli import workbench as workbench_cli

VIDEO_REVIEW = """---
id: T900
title: 试片
形态: 视频
阶段: 创作·视频
初衷: 60s 竖屏，主角只开口一次
---

# 人审表 · T900 试片

| 拍 | 秒 | 画面（一句话） | 景别 | 运镜 | 台词/字幕 |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 香案上一炷香燃起 | 特写 | 推 | — |
| 2 | 5 | 鲸鱼娘端饭上供 | 中景 | 摇 | 字幕：供奉一碗 |

## 关键决策

1. 主角只开口一次

## 未锚假设

- 鲸尾跨拍一致性未知

## 待你拍板

- [ ] 第一画面用香火还是排队
- [ ] 单拍成本门阈值

## 待回答
"""

TEXT_REVIEW = """---
id: T901
title: 试稿
形态: 文本
阶段: 创作·文本
初衷: 一段话说明白为什么删掉了一半
---

# 人审表 · T901 试稿

| 段 | 作用 | 要点 | 证据锚点 | 字数 |
| --- | --- | --- | --- | --- |
| 1 | 钩子 | 凌晨两点第十次粘贴项目背景 | 采访记录 2026-08-11 | 80 |

## 关键决策

1. 删掉全部金句

## 未锚假设

- 读者是否吃过这种苦

## 待你拍板

- [ ] 是否把第 1 段再砍 20 字

## 待回答
"""


@pytest.fixture()
def store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """临时 products/：一个视频选题 + 一个文本选题。"""
    monkeypatch.setattr(R, "PRODUCTS_DIR", tmp_path)
    for name, text in (("T900-试片", VIDEO_REVIEW), ("T901-试稿", TEXT_REVIEW)):
        d = tmp_path / name
        d.mkdir()
        (d / R.REVIEW_FILE).write_text(text, encoding="utf-8")
    return tmp_path


def read(store: Path, topic: str) -> str:
    return (store / topic / R.REVIEW_FILE).read_text(encoding="utf-8")


# ── 渲染：一屏就是全部 ──────────────────────────────────────


def test_render_is_one_page(store: Path):
    """单页含：表 + 表下三块 + 追问区；判断所需的信息全在这一页。"""
    _, rv = R.load_project("T900")
    out = R.render_console(rv)
    for token in (
        "T900",
        "试片",
        "初衷",
        "60s 竖屏，主角只开口一次",
        "香案上一炷香燃起",
        "鲸鱼娘端饭上供",
        "关键决策",
        "未锚假设",
        "待你拍板",
        "待回答",
        "第一画面用香火还是排队",
    ):
        assert token in out, token


def test_render_text_form_fields(store: Path):
    _, rv = R.load_project("T901")
    out = R.render_console(rv)
    assert rv.fields == list(R.TEXT_FIELDS)
    for token in ("段", "作用", "要点", "证据锚点", "字数", "采访记录 2026-08-11"):
        assert token in out, token


def test_md_roundtrip(store: Path):
    _, rv = R.load_project("T900")
    again = R.parse(R.render_md(rv))
    assert again.fields == rv.fields
    assert again.rows == rv.rows
    assert again.meta == rv.meta
    assert {k: v for k, v in again.sections.items() if v} == {
        k: v for k, v in rv.sections.items() if v
    }


# ── 动作一：改表 ────────────────────────────────────────────


def test_edit_cell_writes_back(store: Path):
    path, rv = R.load_project("T900")
    R.edit(rv, "2", "景别", "近景")
    R.save(path, rv)

    reloaded = R.load(path)
    assert reloaded.row("2")[reloaded.fields.index("景别")] == "近景"
    assert reloaded.row("1") == ["1", "3", "香案上一炷香燃起", "特写", "推", "—"]
    assert "| 2 | 5 | 鲸鱼娘端饭上供 | 近景 | 摇 |" in read(store, "T900-试片")


def test_edit_rejects_unknown_row_and_field(store: Path):
    _, rv = R.load_project("T900")
    with pytest.raises(R.ReviewError):
        R.edit(rv, "9", "景别", "近景")
    with pytest.raises(R.ReviewError):
        R.edit(rv, "1", "情绪", "炸")


# ── 动作二：追问 ────────────────────────────────────────────


def test_ask_appends_to_pending_answers(store: Path):
    path, rv = R.load_project("T900")
    R.ask(rv, "1", "为什么第一拍必须是香火")
    R.save(path, rv)

    text = read(store, "T900-试片")
    assert "- 拍 1：为什么第一拍必须是香火" in text
    assert R.load(path).section("待回答") == ["- 拍 1：为什么第一拍必须是香火"]


def test_ask_requires_existing_row(store: Path):
    _, rv = R.load_project("T900")
    with pytest.raises(R.ReviewError):
        R.ask(rv, "7", "为什么不这么定")


# ── 动作三：拍板 ────────────────────────────────────────────


def test_decide_marks_item_done(store: Path):
    path, rv = R.load_project("T900")
    R.decide(rv, 2, "每拍 ≤ 3 元")
    R.save(path, rv)

    text = read(store, "T900-试片")
    assert "- [x] 单拍成本门阈值 → 决定：每拍 ≤ 3 元" in text
    assert "- [ ] 第一画面用香火还是排队" in text


def test_decide_rejects_out_of_range(store: Path):
    _, rv = R.load_project("T900")
    with pytest.raises(R.ReviewError):
        R.decide(rv, 3, "没有这一项")


# ── 动作四：验收 ────────────────────────────────────────────


def test_accept_records_verdict(store: Path):
    path, rv = R.load_project("T900")
    R.accept(rv, "打回", "第 1 拍不够具体")
    R.save(path, rv)

    reloaded = R.load(path)
    assert reloaded.meta["验收"] == "打回"
    assert reloaded.meta["验收备注"] == "第 1 拍不够具体"
    assert "验收：打回" in R.render_console(reloaded)


def test_accept_rejects_unknown_verdict(store: Path):
    _, rv = R.load_project("T900")
    with pytest.raises(R.ReviewError):
        R.accept(rv, "差不多")


# ── CLI：四个动作各一条命令 ─────────────────────────────────


def test_cli_show(store: Path):
    result = CliRunner().invoke(workbench_cli, ["show", "T900"])
    assert result.exit_code == 0, result.output
    assert "关键决策" in result.output
    assert "香案上一炷香燃起" in result.output


def test_cli_four_actions(store: Path):
    runner = CliRunner()

    assert runner.invoke(workbench_cli, ["edit", "T900", "1", "运镜", "推近"]).exit_code == 0
    assert runner.invoke(workbench_cli, ["ask", "T900", "1", "为什么是香火"]).exit_code == 0
    assert runner.invoke(workbench_cli, ["decide", "T900", "1", "用香火"]).exit_code == 0
    accepted = runner.invoke(workbench_cli, ["accept", "T900", "--verdict", "通过"])
    assert accepted.exit_code == 0, accepted.output

    text = read(store, "T900-试片")
    assert "| 1 | 3 | 香案上一炷香燃起 | 特写 | 推近 |" in text
    assert "- 拍 1：为什么是香火" in text
    assert "- [x] 第一画面用香火还是排队 → 决定：用香火" in text
    assert "验收: 通过" in text


def test_cli_reports_missing_topic(store: Path):
    result = CliRunner().invoke(workbench_cli, ["show", "T888"])
    assert result.exit_code != 0
    assert "T888" in result.output
