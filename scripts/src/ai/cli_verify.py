"""ai 后处理与自评估命令：extract-lastframe / verify。

独立模块注册到 ai CLI，避免 cli.py 膨胀。ffmpeg/ffprobe 按需探测。
"""

# pyright: reportUnusedFunction=false
# 注：click 装饰器注册即用途，嵌套函数定义会被 pyright 误报未使用

import json
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Any, cast

import click
from rich.console import Console
from rich.table import Table

console = Console()


def _to_float(value: Any, default: float = 0.0) -> float:
    """安全转 float（ffprobe JSON 字段可能是任意类型）。"""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value: Any, default: int = 0) -> int:
    """安全转 int。"""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def register_verify_commands(cli: click.Group) -> click.Group:
    """向 ai CLI 注册 extract-lastframe 与 verify 命令。"""

    @cli.command("extract-lastframe")
    @click.argument("input", type=click.Path(exists=True))
    @click.option("--output", "-o", required=True, type=click.Path(), help="Output PNG path")
    @click.option("--time-offset", default=0.5, type=float, help="Seconds from end (default 0.5)")
    def _extract_lastframe(input: str, output: str, time_offset: float) -> None:
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
            str(output),
        ]
        console.print(f"[dim]{' '.join(cmd)}[/]")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            console.print(f"[red]ffmpeg error: {result.stderr[-200:]}[/]")
            sys.exit(1)

        size_kb = Path(output).stat().st_size / 1024
        console.print(f"[green]Last frame saved: {output} ({size_kb:.0f} KB)[/]")

    @cli.command("verify")
    @click.argument("input", type=click.Path(exists=True))
    @click.option("--expect-duration", default=None, type=float,
                  help="Expected duration in seconds (tolerance 0.5s)")
    @click.option("--expect-resolution", default=None,
                  help="Expected resolution WxH, e.g. 1080x1920 (9:16 vertical)")
    @click.option("--sample-frames/--no-sample-frames", default=True,
                  help="Extract sample frames at first-2s / mid / last-2s (default: on)")
    @click.option("--output-dir", "-o", default=None, type=click.Path(),
                  help="Directory for sample PNGs (default: alongside input)")
    def _verify(input: str, expect_duration: float | None, expect_resolution: str | None,
                sample_frames: bool, output_dir: str | None) -> None:
        """Verify a generated video before delivery.

        Probes metadata (duration / resolution / codec / fps / bitrate / audio) via
        ffprobe, checks against expectations, and extracts sample frames at first-2s,
        midpoint, and last-2s for visual inspection. Exit 1 if any expectation failed.

        Designed for the video-director post-generation self-eval gate: run this on
        `ai generate video` output before showing the user.
        """
        if not shutil.which("ffprobe"):
            console.print("[red]ffprobe not found. Install: sudo apt install ffmpeg[/]")
            sys.exit(1)

        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format", "-show_streams",
            str(input),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            console.print(f"[red]ffprobe error: {result.stderr[-200:]}[/]")
            sys.exit(1)

        try:
            probe: dict[str, Any] = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            console.print(f"[red]ffprobe output not JSON: {e}[/]")
            sys.exit(1)
        fmt: dict[str, Any] = cast("dict[str, Any]", probe.get("format", {}))
        streams: list[Any] = cast("list[Any]", probe.get("streams", []))

        duration = _to_float(fmt.get("duration"))
        v_stream: dict[str, Any] = next(
            (s for s in streams if s.get("codec_type") == "video"),
            cast("dict[str, Any]", {}),
        )
        a_stream: dict[str, Any] = next(
            (s for s in streams if s.get("codec_type") == "audio"),
            cast("dict[str, Any]", {}),
        )

        width = _to_int(v_stream.get("width"))
        height = _to_int(v_stream.get("height"))
        codec = v_stream.get("codec_name", "?")
        fps_str = v_stream.get("avg_frame_rate", "0/1")
        try:
            num, den = fps_str.split("/")
            fps = int(num) / int(den) if int(den) else 0.0
        except (ValueError, ZeroDivisionError):
            fps = 0.0
        bit_rate_raw = fmt.get("bit_rate")
        bit_rate = _to_int(bit_rate_raw)
        has_audio = bool(a_stream)
        a_codec = a_stream.get("codec_name", "-") if has_audio else "none"

        exp_w = exp_h = None
        if expect_resolution:
            try:
                exp_w, exp_h = (int(x) for x in expect_resolution.lower().split("x"))
            except ValueError:
                raise click.UsageError("--expect-resolution must be WxH, e.g. 1080x1920")

        dur_ok = expect_duration is None or abs(duration - expect_duration) < 0.5
        res_ok = exp_w is None or (width == exp_w and height == exp_h)

        checks = [
            ("Duration", f"{duration:.2f}s",
             f"{expect_duration}s" if expect_duration else "-", dur_ok),
            ("Resolution", f"{width}x{height}",
             f"{exp_w}x{exp_h}" if exp_w else "-", res_ok),
            ("Codec", codec, "-", None),
            ("FPS", f"{fps:.2f}", "-", None),
            ("Bitrate", f"{bit_rate / 1000:.0f} kbps" if bit_rate else "?", "-", None),
            ("Audio", a_codec, "-", None),
        ]

        sample_paths: list[tuple[str, float, Path]] = []
        if sample_frames and duration > 0:
            out_dir = Path(output_dir) if output_dir else Path(input).parent
            out_dir.mkdir(parents=True, exist_ok=True)
            stem = Path(input).stem
            if duration > 4:
                points = [("first2s", 2.0), ("mid", duration / 2), ("last2s", max(0.0, duration - 2.0))]
            else:
                points = [("mid", duration / 2)]
            for label, ts in points:
                frame_path = out_dir / f"{stem}-sample-{label}.png"
                cmd = ["ffmpeg", "-y", "-ss", f"{ts:.2f}", "-i", str(input),
                       "-vframes", "1", "-q:v", "2", str(frame_path)]
                r = subprocess.run(cmd, capture_output=True, text=True)
                if r.returncode == 0 and frame_path.exists():
                    sample_paths.append((label, ts, frame_path))
                else:
                    console.print(f"[yellow]sample {label} failed: {r.stderr[-120:]}[/]")

        table = Table(title=f"Video Verify: {Path(input).name}")
        table.add_column("Field", style="cyan")
        table.add_column("Actual", style="green")
        table.add_column("Expected", style="yellow")
        table.add_column("OK")
        for field, actual, expected, ok in checks:
            if ok is None:
                ok_str = "-"
            elif ok:
                ok_str = "[green]✓[/]"
            else:
                ok_str = "[red]✗[/]"
            table.add_row(field, actual, expected, ok_str)
        console.print(table)

        if sample_paths:
            s_table = Table(title="Sample Frames (visual inspection)")
            s_table.add_column("Label", style="cyan")
            s_table.add_column("Time", style="green")
            s_table.add_column("Path", style="dim")
            for label, ts, p in sample_paths:
                s_table.add_row(label, f"{ts:.2f}s", str(p))
            console.print(s_table)

        failed = [c for c in checks if isinstance(c[3], bool) and not c[3]]
        if failed:
            console.print(f"[red]FAIL: {len(failed)} expectation(s) mismatched[/]")
            sys.exit(1)
        console.print("[green]PASS: all expectations met[/]")

    return cli
