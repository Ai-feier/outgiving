"""CLI 入口 —— click 命令行"""

from __future__ import annotations

import os
import re
from datetime import date
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from .channel import get as channel_get
from .id_gen import (
    Channel,
    ParsedId,
    doc_filename,
    draft_id,
    next_topic_id,
    parse_id,
    slugify_title,
)
from .lifecycle import TransitionError, assert_transition
from .parser import read, write
from .repo import Repo, find_repo_root
from .schema import (
    DraftFM,
    DraftStatus,
    Kind,
    TopicFM,
    TopicStatus,
)

console = Console()


slugify = slugify_title


def _today() -> date:
    """今天日期；CONTENT_TODAY=YYYY-MM-DD 可覆写（测试 / 回填历史数据）。"""
    env = os.environ.get("CONTENT_TODAY", "").strip()
    if env:
        try:
            return date.fromisoformat(env)
        except ValueError:
            pass
    return date.today()  # opengrep-allow: CLI 写入 frontmatter 的合法时钟


def _product_dir(root: Path, topic_id: str, title: str) -> Path:
    """选题目录：products/<id>-<slug>/（一个选题一个目录，全生命周期在内）。"""
    return root / "products" / f"{topic_id}-{slugify(title)}"


@click.group()
@click.option(
    "--root",
    type=click.Path(path_type=Path),
    default=None,
    help="仓库根目录；默认向上查找。",
)
@click.pass_context
def main(ctx: click.Context, root: Path | None) -> None:
    """多渠道内容创作数据管理"""
    ctx.ensure_object(dict)
    ctx.obj["root"] = (root or find_repo_root()).resolve()


# ────────────────────────── validate ──────────────────────────
@main.command()
@click.pass_context
def validate(ctx: click.Context) -> None:
    """校验所有 md 文件的 frontmatter 是否合法"""
    root = ctx.obj["root"]
    repo = Repo(root).scan()
    if repo.errors:
        console.print(f"[red]发现 {len(repo.errors)} 处错误：[/red]")
        for path, msg in repo.errors:
            console.print(f"  [yellow]{path}[/yellow]: {msg}")
        raise SystemExit(1)
    console.print(f"[green]✅ {len(repo.entries)} 份文档全部合规[/green]")


# ────────────────────────── index ──────────────────────────
@main.command()
@click.pass_context
def index(ctx: click.Context) -> None:
    """重建索引文件 .content-index.json"""
    root = ctx.obj["root"]
    repo = Repo(root).scan()
    path = repo.write_index()
    console.print(
        f"[green]已写入[/green] {path.relative_to(root)} "
        f"({len(repo.entries)} 条，{len(repo.errors)} 错误)"
    )


# ────────────────────────── list ──────────────────────────
@main.command(name="list")
@click.pass_context
def list_cmd(ctx: click.Context) -> None:
    """选题进度总览"""
    root = ctx.obj["root"]
    repo = Repo(root).scan()
    views = repo.by_topic()
    if not views:
        console.print("[yellow]没有选题。先 `content new <标题>` 创建一个。[/yellow]")
        return

    table = Table(title="选题总览", show_lines=False)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("标题", style="white")
    table.add_column("状态", style="yellow")
    for c in Channel:
        table.add_column(c.value, justify="center")
    table.add_column("发布", justify="center")
    table.add_column("复盘", justify="center")

    for tid in sorted(views.keys()):
        v = views[tid]
        chan_cells: list[str] = []
        for c in Channel:
            drafts = [d for d in v.drafts if d.channel == c.value]
            if drafts:
                latest = max(drafts, key=lambda d: d.id)
                chan_cells.append(f"[green]{latest.status[:4]}[/green]")
            else:
                chan_cells.append("[dim]·[/dim]")
        pub = f"[green]{len(v.published)}[/green]" if v.published else "[dim]·[/dim]"
        rev = "[green]✓[/green]" if v.analytics else "[dim]·[/dim]"
        table.add_row(tid, v.title, v.status, *chan_cells, pub, rev)

    console.print(table)
    s = repo.stats()
    console.print(f"\n[dim]共 {s['total']} 份文档；by_kind={s['by_kind']}[/dim]")


# ────────────────────────── show ──────────────────────────
@main.command()
@click.argument("topic_id")
@click.pass_context
def show(ctx: click.Context, topic_id: str) -> None:
    """显示某个选题的全部衍生物"""
    root = ctx.obj["root"]
    repo = Repo(root).scan()
    views = repo.by_topic()
    if topic_id not in views:
        console.print(f"[red]未找到 {topic_id}[/red]")
        raise SystemExit(1)
    v = views[topic_id]
    console.print(f"[bold cyan]{v.topic_id}[/bold cyan] · {v.title} · [yellow]{v.status}[/yellow]")
    if v.drafts:
        console.print("\n[bold]Drafts[/bold]")
        for d in v.drafts:
            console.print(f"  - {d.id}  ({d.status})  →  {d.path}")
    if v.published:
        console.print("\n[bold]Published[/bold]")
        for p in v.published:
            console.print(f"  - {p.id}  ({p.status})  →  {p.path}")
    if v.analytics:
        console.print(f"\n[bold]Analytics[/bold]: {v.analytics.id} ({v.analytics.status})")


# ────────────────────────── new ──────────────────────────
@main.command()
@click.argument("title")
@click.option("--audience", default=None, help="目标受众一句话")
@click.option(
    "--channels",
    default="wechat,xiaohongshu,x,douyin",
    help="逗号分隔，默认全部四个渠道",
)
@click.pass_context
def new(ctx: click.Context, title: str, audience: str | None, channels: str) -> None:
    """新建一个选题（products/<id>-<slug>/）"""
    root = ctx.obj["root"]
    repo = Repo(root).scan()
    tid = next_topic_id(repo.topic_ids())
    today = _today()
    chans = [Channel(c.strip()) for c in channels.split(",") if c.strip()]

    product_dir = _product_dir(root, tid, title)
    if product_dir.exists():
        console.print(f"[red]目录已存在：{product_dir}[/red]")
        raise SystemExit(1)

    brief = TopicFM(
        id=tid,
        topic_id=tid,
        title=title,
        status=TopicStatus.BRIEFING,
        audience=audience,
        channels_planned=chans,
        created_at=today,
        updated_at=today,
    )
    write(
        product_dir / doc_filename(Kind.TOPIC.value),
        brief,
        _BRIEF_BODY.format(title=title),
    )

    console.print(
        f"[green]✅ 已创建[/green] [cyan]{tid}[/cyan] - {title}\n"
        f"   {product_dir.relative_to(root)}/\n"
        f"   └── brief.md   (选题信息)\n\n"
        f"下一步: [bold]content adapt {tid} <渠道>[/bold]"
    )


# ────────────────────────── adapt ──────────────────────────
@main.command()
@click.argument("topic_id")
@click.argument("channel", type=click.Choice([c.value for c in Channel]))
@click.option("--revision", type=int, default=None, help="指定版本号；默认自增")
@click.pass_context
def adapt(ctx: click.Context, topic_id: str, channel: str, revision: int | None) -> None:
    """从选题派生一个渠道草稿"""
    root = ctx.obj["root"]
    repo = Repo(root).scan()
    if topic_id not in repo.topic_ids():
        console.print(f"[red]选题不存在：{topic_id}[/red]")
        raise SystemExit(1)
    chan = Channel(channel)

    # 自增版本号
    if revision is None:
        existing = [
            e
            for e in repo.entries
            if e.kind == Kind.DRAFT.value and e.topic_id == topic_id and e.channel == chan.value
        ]
        revision = (
            max(
                ((parse_id(e.id) or ParsedId()).get("revision", 0) for e in existing),
                default=0,
            )
            + 1
        )

    # 父 topic 标题
    topic_entry = next(
        e for e in repo.entries if e.kind == Kind.TOPIC.value and e.topic_id == topic_id
    )
    today = _today()

    fm = DraftFM(
        id=draft_id(topic_id, chan.value, revision),
        topic_id=topic_id,
        parent_id=topic_id,
        title=topic_entry.title,
        channel=chan,
        revision=revision,
        status=DraftStatus.DRAFT,
        created_at=today,
        updated_at=today,
    )

    spec = channel_get(chan.value)
    if spec is None:
        raise click.ClickException(f"未知渠道: {chan.value}")
    product_dir = _product_dir(root, topic_id, topic_entry.title)
    target = product_dir / doc_filename(Kind.DRAFT.value, chan.value)
    if target.exists():
        console.print(
            f"[yellow]目标已存在：{target.relative_to(root)}，已带版本号 v{revision}[/yellow]"
        )

    template_path = root / "assets" / "templates" / spec.template_file
    body = ""
    if template_path.exists():
        template = template_path.read_text(encoding="utf-8")
        # 去掉模板里旧的 frontmatter（如果有），保留正文部分
        body = re.sub(r"^---\n.*?\n---\n", "", template, count=1, flags=re.DOTALL)

    write(target, fm, body)
    console.print(f"[green]✅ 已派生[/green] [cyan]{fm.id}[/cyan] → {target.relative_to(root)}")


# ────────────────────────── transition ──────────────────────────
@main.command()
@click.argument("doc_id")
@click.argument("to_status")
@click.pass_context
def transition(ctx: click.Context, doc_id: str, to_status: str) -> None:
    """把任意文档的 status 推进到下一态"""
    root = ctx.obj["root"]
    repo = Repo(root).scan()
    entry = next((e for e in repo.entries if e.id == doc_id), None)
    if not entry:
        console.print(f"[red]未找到 {doc_id}[/red]")
        raise SystemExit(1)

    path = root / entry.path
    fm, body = read(path)
    try:
        assert_transition(Kind(entry.kind), entry.status, to_status)
    except TransitionError as e:
        console.print(f"[red]{e}[/red]")
        raise SystemExit(1)
    fm = fm.model_copy(update={"status": to_status})
    write(path, fm, body)
    console.print(f"[green]✅ {doc_id}[/green]: {entry.status} → [bold]{to_status}[/bold]")


# ────────────────────────── stats ──────────────────────────
@main.command()
@click.pass_context
def stats(ctx: click.Context) -> None:
    """全局统计"""
    root = ctx.obj["root"]
    repo = Repo(root).scan()
    s = repo.stats()
    console.print(f"[bold]Total[/bold]: {s['total']}  [dim](errors: {s['errors']})[/dim]")
    console.print(f"[bold]By kind[/bold]: {s['by_kind']}")
    console.print("[bold]By status[/bold]:")
    for k, v in sorted(s["by_status"].items()):
        console.print(f"  {k:32s} {v}")
    console.print("[bold]By channel[/bold]:")
    for chan, kinds in s["by_channel"].items():
        console.print(f"  {chan:14s} {kinds}")


# ────────────────────────── preview ──────────────────────────
@main.command()
@click.argument("topic_id", required=False)
@click.option("--port", type=int, default=8765, help="HTTP 端口，默认 8765")
@click.option("--host", default="0.0.0.0", help="绑定地址，默认 0.0.0.0 对外暴露")
@click.option("--no-browser", is_flag=True, help="不自动打开浏览器")
@click.pass_context
def preview(
    ctx: click.Context,
    topic_id: str | None,
    port: int,
    host: str,
    no_browser: bool,
) -> None:
    """启动浏览器预览。可选 topic_id 直接跳转到该选题对比页。

    示例：
        content preview              # 选题总览
        content preview T001         # 直达 T001 多渠道对比
    """
    from .preview import serve

    serve(port=port, host=host, open_browser=not no_browser, open_topic=topic_id)


# ────────────────────────── 模板正文（不含 frontmatter，frontmatter 由 write() 注入） ──────────────────────────
_BRIEF_BODY = """\
# 核心观点（一句话）

> 用一句话说清楚这篇内容到底想让读者「记住什么」。

# 目标受众

- 是谁：
- 在什么场景下读到：
- 读完后能做什么：

# 钩子（Hook）

- 反常识：
- 痛点：
- 利益点：

# 关键信息点（3-5 个）

1.
2.
3.

# CTA（行动召唤）

- 微信：
- 小红书：
- X：
- 抖音：

# 参考资料

- [ ]
"""

if __name__ == "__main__":
    main()
