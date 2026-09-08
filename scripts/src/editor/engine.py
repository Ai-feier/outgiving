"""Composition engine — orchestrates the rendering pipeline.

The single public entry point: ``render(composition, output_path)``.

Pipeline: probe assets → render tracks → composite → subtitle burn → final encode.
Each stage delegates to the appropriate module (segments, tracks, subtitles).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

from editor.models import Composition, Track
from editor.subtitles import write_ass
from editor.tracks import assemble_audio_track, assemble_video_track, mix_audio, overlay_tracks

_FFMPEG = os.environ.get("FFMPEG_BINARY", "ffmpeg")
_FFPROBE = os.environ.get("FFPROBE_BINARY", "ffprobe")


def render(comp: Composition, output_path: str | Path, probe: bool = True) -> Path:
    """Render a Composition to a video file.

    Args:
        comp: Parsed Composition with assets, tracks, subtitles, and output settings.
        output_path: Where to write the final video.
        probe: Whether to probe assets for duration/resolution metadata.

    Returns:
        Path to the rendered video file.
    """
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if probe:
        _probe_assets(comp)

    video_tracks = [t for t in comp.tracks if t.type == "video"]
    audio_tracks = [t for t in comp.tracks if t.type == "audio"]

    # ── Render tracks ───────────────────────────────────────
    temp_files: list[Path] = []

    video_outputs: list[Path] = []
    for track in video_tracks:
        f = assemble_video_track(track, comp)
        if f:
            video_outputs.append(f)
            temp_files.append(f)

    audio_outputs: list[Path] = []
    for track in audio_tracks:
        f = assemble_audio_track(track, comp)
        if f:
            audio_outputs.append(f)
            temp_files.append(f)

    if not video_outputs and not audio_outputs:
        raise ValueError("No valid tracks to render")

    # ── Composite ───────────────────────────────────────────
    video_out = _composite(video_outputs, video_tracks, comp.width, comp.height)
    if video_out and video_out not in temp_files:
        temp_files.append(video_out)

    audio_out = _mix(audio_outputs)
    if audio_out and audio_out not in temp_files:
        temp_files.append(audio_out)

    # ── Final encode (with optional subtitle burn) ───────────
    _encode_final(video_out, audio_out, comp, output_path)

    # Self-diagnosis — the system watches its own output
    from editor.diagnose import diagnose_and_log

    diagnose_and_log(comp, output_path)

    # Cleanup
    for tf in temp_files:
        try:
            if tf.exists() and tf != output_path:
                tf.unlink()
        except OSError:
            pass

    return output_path


# ── pipeline stages ────────────────────────────────────────


def _probe_assets(comp: Composition) -> None:
    for asset in comp.assets:
        if asset.duration == 0 and Path(asset.path).exists():
            info = _probe(asset.path)
            asset.duration = info.get("duration", 0.0)
            w, h = info.get("width"), info.get("height")
            if isinstance(w, int):
                asset.width = w
            if isinstance(h, int):
                asset.height = h


def _composite(video_outputs: list[Path], tracks: list[Track], W: int, H: int) -> Path | None:
    if not video_outputs:
        return None
    if len(video_outputs) == 1:
        return video_outputs[0]
    return overlay_tracks(video_outputs, tracks, W, H)


def _mix(audio_outputs: list[Path]) -> Path | None:
    if not audio_outputs:
        return None
    if len(audio_outputs) == 1:
        return audio_outputs[0]
    return mix_audio(audio_outputs)


def _bg_color(comp: Composition) -> str:
    """背景色（ffmpeg 色彩语法）：bg_color 合法则用，否则 black。"""
    bg = comp.bg_color.strip()
    if re.fullmatch(r"#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?|^[a-zA-Z]+$", bg):
        return bg
    return "black"


def _encode_final(
    video_out: Path | None, audio_out: Path | None, comp: Composition, output_path: Path
) -> None:
    codec = comp.output.get("codec", "libx264")
    crf = comp.output.get("crf", "18")
    bitrate = comp.output.get("bitrate", "")

    cmd = [_FFMPEG, "-y"]
    if video_out:
        cmd += ["-i", str(video_out)]
    if audio_out:
        cmd += ["-i", str(audio_out)]

    if video_out:
        # 中间文件是 yuva420p（带 alpha）——最终合成时把透明区合成到背景色上，
        # 再编码丢 alpha。ffmpeg 4.4 没有 backgroundcolor 滤镜，用 color 源 +
        # overlay 实现同一效果。
        vinfo = _probe(str(video_out))
        try:
            dur = float(vinfo.get("duration") or 0.0)
        except (TypeError, ValueError):
            dur = 0.0
        if dur > 0:
            bg = _bg_color(comp)
            color_src = f"color=c={bg}:s={comp.width}x{comp.height}:d={dur}:r={comp.fps or 30}"
            cmd += ["-f", "lavfi", "-i", color_src]
            # color 源是最后一个输入：有音频时 index=2，否则 1
            color_idx = 2 if audio_out else 1
            fc = f"[{color_idx}:v][0:v]overlay=0:0:shortest=1"  # 背景在下，带 alpha 的视频在上
            if comp.subtitles:
                ass_path = write_ass(comp, output_path)
                if ass_path:
                    fc += f",ass={ass_path}"
            fc += "[v]"
            cmd += ["-filter_complex", fc, "-map", "[v]"]
            if audio_out:
                cmd += ["-map", "1:a"]
        elif comp.subtitles:
            # probe 失败降级：直接编码（alpha 丢失，透明区不保证背景色）
            ass_path = write_ass(comp, output_path)
            if ass_path:
                cmd += ["-vf", f"ass={ass_path}"]

    cmd += ["-c:v", codec, "-crf", crf]
    if bitrate:
        cmd += ["-b:v", bitrate]
    if audio_out:
        cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
    else:
        cmd.append("-an")
    cmd.append(str(output_path))

    result = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        timeout=300,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"ffmpeg failed: {stderr[-500:]}")


def _probe(path: str) -> dict[str, int | float]:
    cmd = [
        _FFPROBE,
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=width,height,codec_type",
        "-of",
        "json",
        path,
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=15, text=True, check=False)
    if result.returncode != 0:
        return {}
    try:
        data: dict[str, Any] = json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError, TypeError):
        return {}
    info: dict[str, int | float] = {"duration": 0.0}
    try:
        fmt: Any = data.get("format", {})
        info["duration"] = float(fmt.get("duration", 0))
        streams: list[Any] = list(data.get("streams", []))
        for s in streams:
            if s.get("codec_type") == "video":
                info["width"] = int(s.get("width", 0))
                info["height"] = int(s.get("height", 0))
                break
    except (TypeError, ValueError):
        pass
    return info
