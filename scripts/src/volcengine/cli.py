"""AI generation CLI — provider-agnostic, default volcengine."""

import sys
import time
import shutil
import subprocess
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Spinner, Progress

# 确保 scripts/src/ 在 sys.path 中
_scripts_src = Path(__file__).resolve().parent.parent
if str(_scripts_src) not in sys.path:
    sys.path.insert(0, str(_scripts_src))

from volcengine import (
    get_image_generator, get_video_generator,
    ImagePrompt, VideoPrompt,
)
from volcengine._utils import image_to_data_uri

# ── Stock footage finder (optional integration) ──────────
try:
    from stock_finder.cli import stock_group as _stock_group
    _has_stock = True
except ImportError:
    _has_stock = False

console = Console()


@click.group()
@click.option("--provider", "-p", default=None, help="Provider name (default from config)")
@click.pass_context
def cli(ctx, provider):
    ctx.ensure_object(dict)
    ctx.obj["provider"] = provider


# Attach stock subcommand group if stock_finder is available.
if _has_stock:
    cli.add_command(_stock_group, "stock")


@cli.group()
def generate():
    """AI generation commands."""
    pass


@generate.command("image")
@click.option("--prompt", default=None, help="Prompt text")
@click.option("--prompt-file", default=None, type=click.Path(exists=True), help="Read prompt from file")
@click.option("--ref-images", "-r", multiple=True, type=click.Path(exists=True), help="Reference images")
@click.option("--size", default="2K", help="Image size (2K/3K/4K or WxH)")
@click.option("--model", default="5.0", help="Model version")
@click.option("--negative-prompt", default=None, help="Negative prompt")
@click.option("--output", "-o", required=True, type=click.Path(), help="Output file path")
@click.pass_context
def generate_image(ctx, prompt, prompt_file, ref_images, size, model, negative_prompt, output):
    """Generate an image using AI."""
    # resolve prompt
    if prompt_file:
        prompt = Path(prompt_file).read_text().strip()
    if not prompt:
        raise click.UsageError("--prompt or --prompt-file required")

    # resolve ref images
    ref_uris = [image_to_data_uri(p) for p in ref_images] if ref_images else None

    console.print(f"[bold]Generating image...[/]")
    console.print(f"  Model: {model}, Size: {size}")
    if ref_uris:
        console.print(f"  Reference images: {len(ref_uris)}")

    t0 = time.time()
    generator = get_image_generator(model=model)
    img_prompt = ImagePrompt(
        prompt=prompt,
        reference_image_url=ref_uris,
        negative_prompt=negative_prompt,
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
@click.option("--prompt-file", default=None, type=click.Path(exists=True), help="Markdown prompt file (video-prompt.md format)")
@click.option("--scene", default=None, help="Scene description")
@click.option("--subject", default=None, help="Subject description")
@click.option("--camera", default=None, help="Camera description")
@click.option("--lighting", default=None, help="Lighting description")
@click.option("--style", default=None, help="Style description")
@click.option("--duration", default=15, type=int, help="Duration in seconds (4-15)")
@click.option("--ref-images", "-r", multiple=True, type=click.Path(exists=True), help="Reference images (0-9)")
@click.option("--model", default="mini", help="Model: pro/fast/mini")
@click.option("--negative-prompt", default=None, help="Negative prompt")
@click.option("--output-dir", "-o", required=True, type=click.Path(), help="Output directory")
@click.pass_context
def generate_video(ctx, prompt_file, scene, subject, camera, lighting, style, duration, ref_images, model, negative_prompt, output_dir):
    """Generate a video using AI."""
    # parse from file or options
    if prompt_file:
        content = Path(prompt_file).read_text()
        # simple markdown field extraction for video-prompt.md format
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("- **scene**:") and not scene:
                scene = line.split(":", 1)[1].strip()
            elif line.startswith("- **subject**:") and not subject:
                subject = line.split(":", 1)[1].strip()
            elif line.startswith("- **camera**:") and not camera:
                camera = line.split(":", 1)[1].strip()
            elif line.startswith("- **lighting**:") and not lighting:
                lighting = line.split(":", 1)[1].strip()
            elif line.startswith("- **style**:") and not style:
                style = line.split(":", 1)[1].strip()

    if not scene:
        raise click.UsageError("--scene or --prompt-file required")

    # resolve ref images
    ref_uris = [image_to_data_uri(p) for p in ref_images] if ref_images else None

    console.print(f"[bold]Submitting video generation...[/]")
    console.print(f"  Model: {model}, Duration: {duration}s")
    if ref_uris:
        console.print(f"  Reference images: {len(ref_uris)}")

    generator = get_video_generator(model=model)
    video_prompt = VideoPrompt(
        scene=scene,
        subject=subject or "",
        camera=camera or "",
        lighting=lighting or "",
        style=style or "",
        duration_hint=duration,
        reference_image_url=ref_uris,
        negative_prompt=negative_prompt,
    )

    t0 = time.time()
    result = generator.submit(video_prompt)
    console.print(f"  Task ID: {result.task_id}")

    console.print(f"  Processing (task: {result.task_id})...")
    with Progress(Spinner(), "[progress]Waiting for completion...") as progress:
        task = progress.add_task("", total=None)
        final = generator.wait(result.task_id, poll_interval=10, timeout=600)
        progress.remove_task(task)

    elapsed = time.time() - t0

    if final.status.value == "failed":
        console.print(f"[red]Generation failed: {final.error_message}[/]")
        sys.exit(1)

    # download video
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    video_path = out_dir / f"{result.task_id}.mp4"

    if final.video_url:
        console.print(f"  Downloading video...")
        import urllib.request
        urllib.request.urlretrieve(final.video_url, str(video_path))

    table = Table(title="Video Generated")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Task ID", result.task_id)
    table.add_row("Output", str(video_path))
    table.add_row("Time", f"{elapsed:.1f}s")
    table.add_row("Model", model)
    console.print(table)


@cli.command("extract-lastframe")
@click.argument("input", type=click.Path(exists=True))
@click.option("--output", "-o", required=True, type=click.Path(), help="Output PNG path")
@click.option("--time-offset", default=0.5, type=float, help="Seconds from end (default 0.5)")
def extract_lastframe(input, output, time_offset):
    """Extract the last frame from a video file using ffmpeg."""
    if not shutil.which("ffmpeg"):
        console.print("[red]ffmpeg not found. Install: sudo apt install ffmpeg[/]")
        sys.exit(1)

    cmd = [
        "ffmpeg", "-y",
        "-sseof", f"-{time_offset}",
        "-i", str(input),
        "-vframes", "1",
        "-q:v", "2",
        str(output)
    ]
    console.print(f"[dim]{' '.join(cmd)}[/]")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        console.print(f"[red]ffmpeg error: {result.stderr[-200:]}[/]")
        sys.exit(1)

    size_kb = Path(output).stat().st_size / 1024
    console.print(f"[green]Last frame saved: {output} ({size_kb:.0f} KB)[/]")


# ── Editor commands ─────────────────────────────────────────
# Lazy import to avoid requiring ffmpeg-python unless edit commands are used


@cli.group()
def edit():
    """Video editing — compose, clip, concat, speed, mute."""
    pass


@edit.command("compose")
@click.option("--manifest", "-m", required=True, type=click.Path(exists=True), help="Markdown manifest file")
@click.option("--output", "-o", required=True, type=click.Path(), help="Output video path")
@click.option("--no-probe", is_flag=True, help="Skip ffprobe asset detection")
def _edit_compose(manifest, output, no_probe):
    """Render a composition manifest to video."""
    from editor.manifest import parse_manifest
    from editor.compose import render

    md_path = Path(manifest).resolve()
    console.print(f"[bold]Parsing manifest:[/] {md_path.name}")
    comp = parse_manifest(md_path)

    console.print(f"  Name: {comp.name}")
    console.print(f"  Resolution: {comp.width}x{comp.height} @ {comp.fps}fps")
    console.print(f"  Assets: {len(comp.assets)}, Tracks: {len(comp.tracks)}, Subtitles: {len(comp.subtitles)}")

    console.print(f"\n[bold]Rendering...[/]")
    out = render(comp, Path(output).resolve(), probe=not no_probe)

    size_mb = out.stat().st_size / (1024 * 1024) if out.exists() else 0
    console.print(f"[green]Done: {out} ({size_mb:.1f} MB)[/]")


@edit.command("clip")
@click.option("--input", "-i", required=True, type=click.Path(exists=True), help="Input video")
@click.option("--start", "-s", required=True, type=float, help="Start time (seconds)")
@click.option("--end", "-e", required=True, type=float, help="End time (seconds)")
@click.option("--output", "-o", required=True, type=click.Path(), help="Output path")
def _edit_clip(input, start, end, output):
    """Extract a clip from a video."""
    from editor.models import Asset, Composition, Segment, Track
    from editor.compose import render

    asset = Asset(id="src", path=str(Path(input).resolve()), type="video")
    seg_v = Segment(id="clip", asset_id="src", src_start=start, src_end=end, tl_start=0.0)
    seg_a = Segment(id="clip-audio", asset_id="src", src_start=start, src_end=end, tl_start=0.0)
    track_v = Track(id="main", type="video", segments=[seg_v])
    track_a = Track(id="audio", type="audio", segments=[seg_a])
    comp = Composition(
        name="clip", assets=[asset], tracks=[track_v, track_a],
        output={"codec": "libx264", "crf": "18"},
    )
    console.print(f"[bold]Clipping:[/] {start}s → {end}s ({end - start:.1f}s)")
    out = render(comp, Path(output).resolve(), probe=True)
    console.print(f"[green]Done: {out}[/]")


@edit.command("concat")
@click.option("--inputs", "-i", multiple=True, type=click.Path(exists=True), help="Input videos in order")
@click.option("--output", "-o", required=True, type=click.Path(), help="Output path")
@click.option("--input-list", type=click.Path(exists=True), help="File with one input path per line")
def _edit_concat(inputs, output, input_list):
    """Concatenate videos in sequence."""
    import os
    import tempfile
    import ffmpeg

    paths = list(inputs)
    if input_list:
        paths += [l.strip() for l in Path(input_list).read_text().splitlines()
                  if l.strip() and not l.strip().startswith("#")]

    if not paths:
        raise click.UsageError("At least one input required")

    console.print(f"[bold]Concatenating {len(paths)} files...[/]")
    concat_list = "\n".join(f"file '{os.path.abspath(p)}'" for p in paths)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(concat_list)
        list_path = f.name

    try:
        node = ffmpeg.input(list_path, format="concat", safe=0)
        out = ffmpeg.output(node, str(Path(output).resolve()), vcodec="libx264", crf=18)
        out = out.overwrite_output()
        out.run(capture_stdout=True, capture_stderr=True)
    finally:
        os.unlink(list_path)

    size_mb = Path(output).stat().st_size / (1024 * 1024)
    console.print(f"[green]Done: {output} ({size_mb:.1f} MB)[/]")


@edit.command("speed")
@click.option("--input", "-i", required=True, type=click.Path(exists=True), help="Input video")
@click.option("--factor", "-f", required=True, type=click.FloatRange(min=0.001), help="Speed factor (2.0 = double speed)")
@click.option("--output", "-o", required=True, type=click.Path(), help="Output path")
def _edit_speed(input, factor, output):
    """Change video playback speed."""
    from editor.models import Asset, Composition, Segment, Track
    from editor.compose import render

    asset = Asset(id="src", path=str(Path(input).resolve()), type="video")
    seg_v = Segment(id="sped", asset_id="src", src_start=0.0, src_end=3600.0, tl_start=0.0, speed=factor)
    seg_a = Segment(id="sped-audio", asset_id="src", src_start=0.0, src_end=3600.0, tl_start=0.0, speed=factor)
    track_v = Track(id="main", type="video", segments=[seg_v])
    track_a = Track(id="audio", type="audio", segments=[seg_a])
    comp = Composition(
        name="speed", assets=[asset], tracks=[track_v, track_a],
        output={"codec": "libx264", "crf": "18"},
    )
    console.print(f"[bold]Speed:[/] {factor}x")
    out = render(comp, Path(output).resolve(), probe=True)
    console.print(f"[green]Done: {out}[/]")


@edit.command("mute")
@click.option("--input", "-i", required=True, type=click.Path(exists=True), help="Input video")
@click.option("--output", "-o", required=True, type=click.Path(), help="Output path")
def _edit_mute(input, output):
    """Remove audio track from video."""
    import ffmpeg

    console.print("[bold]Removing audio...[/]")
    node = ffmpeg.input(str(Path(input).resolve()))
    out = ffmpeg.output(node.video, str(Path(output).resolve()), vcodec="libx264", crf=18, an=None)
    out = out.overwrite_output()
    out.run(capture_stdout=True, capture_stderr=True)
    size_mb = Path(output).stat().st_size / (1024 * 1024)
    console.print(f"[green]Done: {output} ({size_mb:.1f} MB)[/]")


@edit.command("profile")
@click.option("--input", "-i", required=True, type=click.Path(exists=True), help="Input video file or directory (with --batch)")
@click.option("--output-dir", "-o", type=click.Path(), help="Output directory for profile.md")
@click.option("--threshold", type=float, default=0.15, help="Scene detection threshold (0-1)")
@click.option("--batch", is_flag=True, help="Profile all .mp4 files in input directory, skip existing")
def _edit_profile(input, output_dir, threshold, batch):
    """Generate a scene-detection profile for a video or batch."""
    if batch:
        from pathlib import Path
        from editor.profiler import profile_video
        d = Path(input)
        if not d.is_dir():
            console.print("[red]--batch requires input to be a directory[/]")
            sys.exit(1)
        mp4s = sorted(d.glob("*.mp4"))
        if not mp4s:
            console.print("[yellow]No .mp4 files found in directory[/]")
            return
        skipped = 0
        profiled = 0
        for mp4 in mp4s:
            if Path(str(mp4).replace(".mp4", ".profile.md")).exists():
                skipped += 1
                continue
            console.print(f"  Profiling: {mp4.name}")
            profile_video(str(mp4), output_dir=output_dir or str(mp4.parent), threshold=threshold)
            profiled += 1
        console.print(f"[green]Done: {profiled} profiled, {skipped} skipped (already exist)[/]")
    else:
        from editor.profiler import profile_video
        console.print(f"[bold]Profiling:[/] {input}")
        out = profile_video(input, output_dir=output_dir, threshold=threshold)
        console.print(f"[green]Profile: {out}[/]")


if __name__ == "__main__":
    cli()
