"""AI generation CLI — provider-agnostic。

原则：CLI 只认识语义层（VideoPrompt），不认识任何 provider。
- prompt 文件格式由 provider 的 parse_prompt_file 声明（hasattr 探测），通用标准格式兜底
- 分辨率/成本/dry-run 等 provider 差异全部收在适配器接口里
- 新增 provider = 注册表一行 + 可选能力实现，CLI 零改动
"""

import json
import re
import sys
import time
import urllib.request
from dataclasses import replace
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# 确保 scripts/src/ 在 sys.path 中
_scripts_src = Path(__file__).resolve().parent.parent
if str(_scripts_src) not in sys.path:
    sys.path.insert(0, str(_scripts_src))

from ai import ImagePrompt, VideoPrompt, get_image_generator, get_video_generator
from ai._utils import image_to_data_uri
from ai.formats import parse_standard_prompt_file

# ── Stock footage finder (optional integration) ──────────
try:
    from stock_finder.cli import stock_group as _stock_group
except ImportError:
    _stock_group = None

console = Console()


# ── 通用参考图/文件工具（格式无关） ───────────────────────


def resolve_ref_uris(values: tuple[str, ...] | list[str]) -> list[str]:
    """将 --ref-images 值解析为 URI 列表：本地路径 → data URI，http(s) URL → 原样。"""
    refs: list[str] = []
    for raw in values:
        if raw.startswith(("http://", "https://")):
            refs.append(raw)
            continue
        p = Path(raw)
        if not p.exists():
            raise click.UsageError(f"Reference image not found: {raw}")
        refs.append(image_to_data_uri(p))
    return refs


def extract_markdown_image_uris(md: str, base_dir: Path) -> list[str]:
    """从 markdown 提取 ![](path) 参考图：本地文件 → data URI，URL 保留。"""
    import re

    refs: list[str] = []
    for m in re.finditer(r"!\[[^\]]*\]\(([^)\s]+)\)", md):
        raw = m.group(1)
        if raw.startswith(("http://", "https://")):
            refs.append(raw)
            continue
        path_part = raw.split(" ", 1)[0].split("#", 1)[0]
        p = Path(path_part)
        if not p.is_absolute():
            cand = base_dir / p
            if not cand.exists():
                cand = Path.cwd() / p
            p = cand
        if p.exists():
            refs.append(image_to_data_uri(p))
        else:
            console.print(f"[yellow]prompt file ref skipped (not found): {path_part}[/]")
    return refs


@click.group()
@click.option("--provider", "-p", default=None, help="Provider name (default from config)")
@click.pass_context
def cli(ctx: click.Context, provider: str | None) -> None:
    ctx.ensure_object(dict)
    ctx.obj["provider"] = provider


# Attach stock subcommand group if stock_finder is available.
if _stock_group is not None:
    cli.add_command(_stock_group, "stock")

# 后处理与编辑命令（独立模块注册，避免 cli.py 膨胀）
from ai.cli_edit import register_edit_commands
from ai.cli_verify import register_verify_commands

register_verify_commands(cli)
register_edit_commands(cli)


@cli.command("workbench")
@click.argument("project", default=None, required=False)
@click.option("--port", default=8766, type=int, help="Port（默认 8766；8765 留给 content preview）")
@click.option("--host", default="127.0.0.1", help="绑定地址（默认仅本机——可写 md）")
@click.option("--no-browser", is_flag=True, help="不自动打开浏览器")
def workbench_cmd(project: str | None, port: int, host: str, no_browser: bool) -> None:
    """启动视频提示词工作台（web 看/改/提意见；md 文件仍为唯一事实源）。"""
    import click as _click

    if project and not re.match(r"^T\d{3}(-[\w-]+)?$", project):
        _click.echo(f"Invalid project: {project}（应为 TXXX，如 T005）")
        raise SystemExit(1)
    from workbench.server import run

    run(port=port, host=host, project=project, open_browser=not no_browser)


@cli.group()
def generate() -> None:
    """AI generation commands."""


@generate.command("image")
@click.option("--prompt", default=None, help="Prompt text")
@click.option(
    "--prompt-file", default=None, type=click.Path(exists=True), help="Read prompt from file"
)
@click.option(
    "--ref-images", "-r", multiple=True, help="Reference images: local path or http(s) URL"
)
@click.option("--size", default="2K", help="Image size (2K/3K/4K or WxH)")
@click.option("--model", default="5.0", help="Model version")
@click.option("--negative-prompt", default=None, help="Negative prompt")
@click.option("--output", "-o", required=True, type=click.Path(), help="Output file path")
@click.pass_context
def generate_image(
    ctx: click.Context,
    prompt: str | None,
    prompt_file: str | None,
    ref_images: tuple[str, ...],
    size: str,
    model: str,
    negative_prompt: str | None,
    output: str,
) -> None:
    """Generate an image using AI."""
    if prompt_file:
        prompt = Path(prompt_file).read_text().strip()
    if not prompt:
        raise click.UsageError("--prompt or --prompt-file required")

    ref_uris = resolve_ref_uris(ref_images) or None

    console.print("[bold]Generating image...[/]")
    console.print(f"  Model: {model}, Size: {size}")
    if ref_uris:
        console.print(f"  Reference images: {len(ref_uris)}")

    t0 = time.time()
    generator = get_image_generator(model=model, provider=ctx.obj.get("provider"))
    img_prompt = ImagePrompt(
        prompt=prompt,
        reference_image_url=ref_uris,
        negative_prompt=negative_prompt or "",
        size=size,
        output_format="png",
        watermark=False,
        optimize_mode="standard",
    )
    result = generator.generate_to_file(img_prompt, Path(output))
    elapsed = time.time() - t0

    if result.error_message:
        console.print(f"[red]Error: {result.error_message}[/]")
        sys.exit(1)

    output_path = Path(output)
    size_mb = output_path.stat().st_size / (1024 * 1024) if output_path.exists() else 0

    table = Table(title="Image Generated")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Output", str(output_path))
    table.add_row("Size", f"{size_mb:.1f} MB")
    table.add_row("Time", f"{elapsed:.1f}s")
    table.add_row("Model", model)
    console.print(table)


@generate.command("video")
@click.option(
    "--prompt-file",
    default=None,
    type=click.Path(exists=True),
    help="Markdown prompt file（provider 专属格式，或标准 9 要素格式）",
)
@click.option("--scene", default=None, help="Scene description")
@click.option("--subject", default=None, help="Subject description")
@click.option("--camera", default=None, help="Camera description")
@click.option("--lighting", default=None, help="Lighting description")
@click.option("--style", default=None, help="Style description")
@click.option(
    "--duration", default=15, type=int, help="Duration in seconds（provider 上限不同，适配器截断）"
)
@click.option(
    "--ref-images", "-r", multiple=True, help="Reference images (0-9): local path or http(s) URL"
)
@click.option("--model", default="mini", help="Model/工作流档位（provider 相关）")
@click.option("--negative-prompt", default=None, help="Negative prompt")
@click.option(
    "--resolution", default=None, help="分辨率预设（provider 专属枚举，透传给适配器校验）"
)
@click.option("--seed", default=None, type=int, help="Random seed（同参同 seed 结果相近）")
@click.option("--dry-run", is_flag=True, help="打印 API 请求体后退出（不提交不花钱）")
@click.option(
    "--output-dir", "-o", type=click.Path(), help="Output directory（--dry-run 时可不填）"
)
@click.pass_context
def generate_video(
    ctx: click.Context,
    prompt_file: str | None,
    scene: str | None,
    subject: str | None,
    camera: str | None,
    lighting: str | None,
    style: str | None,
    duration: int,
    ref_images: tuple[str, ...],
    model: str,
    negative_prompt: str | None,
    resolution: str | None,
    seed: int | None,
    dry_run: bool,
    output_dir: str | None,
) -> None:
    """Generate a video using AI (provider-agnostic)。"""
    if not dry_run and not output_dir:
        raise click.UsageError("--output-dir required（除非 --dry-run）")

    generator = get_video_generator(model=model, provider=ctx.obj.get("provider"))

    # ── 1. prompt 装配：provider 专属格式优先，标准格式兜底 ──
    video_prompt: VideoPrompt | None = None
    file_refs: list[str] = []
    if prompt_file:
        content = Path(prompt_file).read_text()
        parser = getattr(generator, "parse_prompt_file", None)
        if parser is not None:
            parsed = parser(content)
            video_prompt = parsed if isinstance(parsed, VideoPrompt) else None
        if video_prompt is None:
            video_prompt = parse_standard_prompt_file(
                content,
                scene=scene,
                subject=subject,
                camera=camera,
                lighting=lighting,
                style=style,
            )
        file_refs = extract_markdown_image_uris(content, Path(prompt_file).parent)

    if video_prompt is None:
        if not scene:
            raise click.UsageError("--scene or --prompt-file required")
        video_prompt = VideoPrompt(
            scene=scene or "",
            subject=subject or "",
            camera=camera or "",
            lighting=lighting or "",
            style=style or "",
        )

    if not video_prompt.scene and not video_prompt.raw_prompt:
        raise click.UsageError("--scene or --prompt-file required（无 scene 也无原始 prompt）")

    # ── 2. CLI 覆盖项（时长/参考图/负向/分辨率/seed） ──
    refs = resolve_ref_uris(ref_images)
    if not refs and file_refs:
        refs = file_refs
    video_prompt = replace(
        video_prompt,
        duration_hint=duration,
        reference_image_url=refs or None,
        negative_prompt=negative_prompt or video_prompt.negative_prompt,
        resolution=resolution or video_prompt.resolution,
        seed=seed if seed is not None else video_prompt.seed,
    )

    # ── 3. dry-run（provider 有 build_request 才可预览） ──
    if dry_run:
        build = getattr(generator, "build_request", None)
        if build is None:
            console.print("[yellow]当前 provider 不支持 dry-run 预览[/]")
            return
        try:
            body = build(video_prompt)
        except ValueError as e:
            # 参数门禁（如 H3 缺参考图）：干净显示错误 + 已装配 prompt
            console.print(f"[yellow]{e}[/]")
            console.print("[yellow]提示：可加 --ref-images（本地文件或 URL）后再预览完整请求体[/]")
            text = video_prompt.raw_prompt
            if not text:
                text = video_prompt.to_natural_language()
            console.print("[yellow]以下为已装配的 prompt：[/]")
            console.print(text)
            return
        console.print(json.dumps(body, ensure_ascii=False, indent=2))
        return

    # ── 4. 提交 ──
    console.print("[bold]Submitting video generation...[/]")
    console.print(f"  Provider: {type(generator).__name__}, Duration: {duration}s")
    est = getattr(generator, "estimate_cost", None)
    if est is not None:
        try:
            cost = est(duration, resolution or "")
        except (ValueError, TypeError, KeyError):
            cost = None
        if cost is not None:
            console.print(f"  Est. cost: ¥{cost:.2f}")
    if refs:
        console.print(f"  Reference images: {len(refs)}")

    t0 = time.time()
    try:
        result = generator.submit(video_prompt)
    except ValueError as e:
        console.print(f"[red]{e}[/]")
        sys.exit(1)
    console.print(f"  Task ID: {result.task_id}")

    console.print(f"  Processing (task: {result.task_id})...")
    with Progress(SpinnerColumn(), TextColumn("[progress]Waiting for completion...")) as progress:
        task = progress.add_task("", total=None)
        final = generator.wait(result.task_id, poll_interval=10, timeout=600)
        progress.remove_task(task)

    elapsed = time.time() - t0

    if final.status.value == "failed":
        console.print(f"[red]Generation failed: {final.error_message}[/]")
        sys.exit(1)

    # download video
    out_dir = Path(output_dir or ".")
    out_dir.mkdir(parents=True, exist_ok=True)
    video_path = out_dir / f"{result.task_id}.mp4"

    if final.video_url:
        console.print("  Downloading video...")
        urllib.request.urlretrieve(final.video_url, str(video_path))

    table = Table(title="Video Generated")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Task ID", result.task_id)
    table.add_row("Output", str(video_path))
    table.add_row("Time", f"{elapsed:.1f}s")
    table.add_row("Model", model)
    console.print(table)


if __name__ == "__main__":
    cli()
