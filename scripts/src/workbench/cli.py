"""workbench CLI —— 人审表的渲染与四个写回动作。

命令沿用既有 CLI 入口（`ai workbench`）。所有动作只写回
`products/<id>-<slug>/review.md`，不改任何其他文件。
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import click

from workbench import review as R


@click.group()
def workbench() -> None:
    """人审表：看表 / 改表 / 追问 / 拍板 / 验收（md 是唯一事实源）。"""


def _load(project: str) -> tuple[Path, R.Review]:
    try:
        path, rv = R.load_project(project)
    except (FileNotFoundError, R.ReviewError) as e:
        raise click.ClickException(str(e)) from e
    return path, rv


def _apply(project: str, mutate: Callable[[R.Review], object]) -> R.Review:
    path, rv = _load(project)
    try:
        mutate(rv)
    except R.ReviewError as e:
        raise click.ClickException(str(e)) from e
    R.save(path, rv)
    return rv


@workbench.command("show")
@click.argument("project")
def show_cmd(project: str) -> None:
    """渲染单页人审表（表 + 关键决策 / 未锚假设 / 待你拍板 / 待回答）。"""
    _, rv = _load(project)
    click.echo(R.render_console(rv))


@workbench.command("edit")
@click.argument("project")
@click.argument("row")
@click.argument("field")
@click.argument("value")
def edit_cmd(project: str, row: str, field: str, value: str) -> None:
    """改表：把 <row> 行的 <field> 一格改成 <value>。"""
    _apply(project, lambda rv: R.edit(rv, row, field, value))
    click.echo(f"已改表：{row} · {field} → {value}")


@workbench.command("ask")
@click.argument("project")
@click.argument("row")
@click.argument("question")
def ask_cmd(project: str, row: str, question: str) -> None:
    """追问：对 <row> 行问「为什么这么定」，写进「待回答」。"""
    _apply(project, lambda rv: R.ask(rv, row, question))
    click.echo(f"已追问：{row} → 待回答")


@workbench.command("decide")
@click.argument("project")
@click.argument("index", type=int)
@click.argument("decision")
def decide_cmd(project: str, index: int, decision: str) -> None:
    """拍板：对「待你拍板」第 <index> 项（1 起）做决定。"""
    _apply(project, lambda rv: R.decide(rv, index, decision))
    click.echo(f"已拍板：待你拍板 第 {index} 项 → {decision}")


@workbench.command("accept")
@click.argument("project")
@click.option("--verdict", type=click.Choice(list(R.VERDICTS)), required=True)
@click.option("--note", default="", help="验收备注（可选）")
def accept_cmd(project: str, verdict: str, note: str) -> None:
    """验收：先看整表，逐条核对该表是否满足初衷，结论写回表。"""
    _, rv = _load(project)
    click.echo(R.render_console(rv))
    _apply(project, lambda r: R.accept(r, verdict, note))
    click.echo(f"已验收：{verdict}" + (f"（{note}）" if note else ""))
