"""AI video editing CLI — agent 的剪辑界面."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

from editor.manifest import parse_manifest
from editor.compose import render

console = Console()


@click.group()
def edit():
    """Video editing commands — compose, clip, concat, speed, mute."""


@edit.command("compose")
@click.option("--manifest", "-m", required=True, type=click.Path(exists=True), help="Markdown manifest file")
@click.option("--output", "-o", required=True, type=click.Path(), help="Output video path")
@click.option("--no-probe", is_flag=True, help="Skip ffprobe asset detection")
def compose_cmd(manifest: str, output: str, no_probe: bool):
    """Render a composition manifest to video."""
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
def clip_cmd(input: str, start: float, end: float, output: str):
    """Extract a clip from a video."""
    from editor.models import Asset, Composition, Segment, Track

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
def concat_cmd(inputs: tuple, output: str, input_list: str | None):
    """Concatenate videos in sequence."""
    import os

    paths: list[str] = list(inputs)
    if input_list:
        paths += [l.strip() for l in Path(input_list).read_text().splitlines() if l.strip() and not l.strip().startswith("#")]

    if not paths:
        raise click.UsageError("At least one input required")

    console.print(f"[bold]Concatenating {len(paths)} files...[/]")

    # Use ffmpeg concat demuxer via a temp file list
    concat_list = "\n".join(f"file '{os.path.abspath(p)}'" for p in paths)
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(concat_list)
        list_path = f.name

    import ffmpeg
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
def speed_cmd(input: str, factor: float, output: str):
    """Change video playback speed."""
    from editor.models import Asset, Composition, Segment, Track

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
def mute_cmd(input: str, output: str):
    """Remove audio track from video."""
    import ffmpeg

    console.print("[bold]Removing audio...[/]")
    node = ffmpeg.input(str(Path(input).resolve()))
    out = ffmpeg.output(node.video, str(Path(output).resolve()), vcodec="libx264", crf=18, an=None)
    out = out.overwrite_output()
    out.run(capture_stdout=True, capture_stderr=True)
    size_mb = Path(output).stat().st_size / (1024 * 1024)
    console.print(f"[green]Done: {output} ({size_mb:.1f} MB)[/]")
