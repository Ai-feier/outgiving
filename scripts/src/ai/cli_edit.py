"""ai edit 命令组：compose / clip / concat / speed / mute / profile。

独立模块注册到 ai CLI。Lazy import editor 模块——不用 edit 命令时不引入 ffmpeg-python。
"""

# pyright: reportUnusedFunction=false
# 注：click 装饰器注册即用途，嵌套函数定义会被 pyright 误报未使用

import sys
from pathlib import Path
from typing import Any, cast

import click
from rich.console import Console

console = Console()


def register_edit_commands(cli: click.Group) -> click.Group:
    """向 ai CLI 注册 edit 命令组。"""

    @cli.group()
    def edit():
        """Video editing — compose, clip, concat, speed, mute."""
        pass

    @edit.command("compose")
    @click.option("--manifest", "-m", required=True, type=click.Path(exists=True), help="Markdown manifest file")
    @click.option("--output", "-o", required=True, type=click.Path(), help="Output video path")
    @click.option("--no-probe", is_flag=True, help="Skip ffprobe asset detection")
    def _edit_compose(manifest: str, output: str, no_probe: bool) -> None:
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
    def _edit_clip(input: str, start: float, end: float, output: str) -> None:
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
    def _edit_concat(inputs: tuple[str, ...], output: str, input_list: str | None) -> None:
        """Concatenate videos in sequence."""
        import os
        import tempfile
        import ffmpeg  # type: ignore[reportMissingTypeStubs]
        ffmpeg = cast(Any, ffmpeg)  # ffmpeg-python 无类型桩，动态调用

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
    def _edit_speed(input: str, factor: float, output: str) -> None:
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
    def _edit_mute(input: str, output: str) -> None:
        """Remove audio track from video."""
        import ffmpeg  # type: ignore[reportMissingTypeStubs]
        ffmpeg = cast(Any, ffmpeg)  # ffmpeg-python 无类型桩，动态调用

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
    def _edit_profile(input: str, output_dir: str | None, threshold: float, batch: bool) -> None:
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

    return cli
