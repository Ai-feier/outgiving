"""Track assembler — segments → assembled track with gap handling.

Renders each segment via SegmentRenderer, then assembles them into a single
track file respecting tl_start timeline positions. Gaps get black/silent filler.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path

from editor.models import Composition, Track
from editor.segments import render_audio_segment, render_video_segment

_FFMPEG = os.environ.get("FFMPEG_BINARY", "ffmpeg")
_FFPROBE = os.environ.get("FFPROBE_BINARY", "ffprobe")

# (tl_start, actual 渲染时长, 文件, tl_end)
Entry = tuple[float, float, Path, float]


def assemble_video_track(track: Track, comp: Composition) -> Path | None:
    """Render all segments in a video track, insert black for timeline gaps, concat."""
    entries: list[Entry] = []
    for i, seg in enumerate(track.segments):
        sf = render_video_segment(seg, comp, i)
        if sf:
            dur = _probe_duration(sf)
            entries.append((seg.tl_start, dur, sf, seg.tl_end))

    if not entries:
        return None

    entries.sort(key=lambda x: x[0])
    files = _fill_gaps(
        entries,
        gap_generator=lambda d: _blank_video(d, comp.width, comp.height, comp.fps or 30),
    )

    if len(files) == 1:
        return files[0]
    return _concat_demuxer(files, "video")


def assemble_audio_track(track: Track, comp: Composition) -> Path | None:
    """Render all segments in an audio track, insert silence for timeline gaps, concat."""
    entries: list[Entry] = []
    for i, seg in enumerate(track.segments):
        sf = render_audio_segment(seg, comp, i)
        if sf:
            dur = _probe_duration(sf)
            entries.append((seg.tl_start, dur, sf, seg.tl_end))

    if not entries:
        return None

    entries.sort(key=lambda x: x[0])
    files = _fill_gaps(entries, gap_generator=_silent_audio)

    if len(files) == 1:
        return files[0]
    return _concat_audio(files)


def overlay_tracks(video_files: list[Path], tracks: list[Track], W: int, H: int) -> Path:
    """Overlay multiple video tracks. Track 0 = base, track 1+ = overlays."""
    current = video_files[0]
    for i in range(1, len(video_files)):
        out_f = Path(tempfile.mkstemp(suffix=f".overlay{i}.mkv")[1])
        track = tracks[i] if i < len(tracks) else None
        blend = _track_blend(track) if track else ""
        alpha = ""
        if track is not None and 0.0 < track.opacity < 1.0:
            alpha = f",colorchannelmixer=aa={track.opacity}"
        mode = f"blend=all_mode={blend}:shortest=1" if blend else "overlay=0:0:shortest=1"
        subprocess.run(
            [
                _FFMPEG,
                "-y",
                "-i",
                str(current),
                "-i",
                str(video_files[i]),
                "-filter_complex",
                f"[1:v]scale={W}:{H}{alpha}[ov];[0:v][ov]{mode}",
                "-c:v",
                "ffv1",
                "-pix_fmt",
                "yuva420p",
                "-an",
                str(out_f),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            timeout=120,
            check=True,
        )
        current = out_f
    return current


def mix_audio(files: list[Path]) -> Path:
    """Mix multiple audio tracks into one."""
    out_f = Path(tempfile.mkstemp(suffix=".mix.mp3")[1])
    inputs: list[str] = []
    for f in files:
        inputs += ["-i", str(f)]
    n = len(files)
    subprocess.run(
        [_FFMPEG, "-y"]
        + inputs
        + [
            "-filter_complex",
            f"amix=inputs={n}:duration=longest",
            "-f",
            "mp3",
            str(out_f),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        timeout=120,
        check=True,
    )
    return out_f


# ── internals ──────────────────────────────────────────────


def _blank_video(duration: float, W: int, H: int, fps: float) -> Path:
    """时间线空隙填充——透明（alpha=0）而非黑：base 轨最终合成时露出背景色，
    overlay 轨露出下层。"""
    out_f = Path(tempfile.mkstemp(suffix=".blank.mkv")[1])
    subprocess.run(
        [
            _FFMPEG,
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c=black@0.0:s={W}x{H}:d={duration}:r={fps},format=yuva420p",
            "-c:v",
            "ffv1",
            "-pix_fmt",
            "yuva420p",
            "-g",
            "1",
            "-an",
            str(out_f),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        timeout=60,
        check=True,
    )
    return out_f


def _silent_audio(duration: float) -> Path:
    out_f = Path(tempfile.mkstemp(suffix=".silent.mp3")[1])
    subprocess.run(
        [
            _FFMPEG,
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"anullsrc=r=44100:cl=stereo:d={duration}",
            "-c:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(out_f),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        timeout=60,
        check=True,
    )
    return out_f


def _concat_demuxer(files: list[Path], label: str) -> Path:
    out_f = Path(tempfile.mkstemp(suffix=f".{label}.mkv")[1])
    list_f = Path(tempfile.mkstemp(suffix=".txt")[1])
    list_f.write_text("\n".join(f"file '{f}'" for f in files))
    subprocess.run(
        [
            _FFMPEG,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_f),
            "-c",
            "copy",
            str(out_f),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        timeout=120,
        check=True,
    )
    return out_f


def _concat_audio(files: list[Path]) -> Path:
    out_f = Path(tempfile.mkstemp(suffix=".aconcat.mp3")[1])
    inputs: list[str] = []
    for f in files:
        inputs += ["-i", str(f)]
    subprocess.run(
        [_FFMPEG, "-y"]
        + inputs
        + [
            "-filter_complex",
            f"concat=n={len(files)}:v=0:a=1",
            "-c:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(out_f),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        timeout=120,
        check=True,
    )
    return out_f


def _probe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            _FFPROBE,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    try:
        return float(result.stdout.strip())
    except (ValueError, TypeError):
        return 0.0


def _fill_gaps(
    entries: list[Entry],
    W: int = 0,
    H: int = 0,
    fps: float = 30,
    gap_generator: Callable[[float], Path] | None = None,
) -> list[Path]:
    """Insert gap fillers between segments based on tl_start positions.

    Physical position tracks by actual rendered duration. Overlaps (negative
    gaps) are silently ignored — the concat demuxer just plays files sequentially.
    This can cause cumulative drift, but the drift only affects gap sizing, not
    the final output duration (which equals sum of all file durations + gaps).
    """
    files: list[Path] = []
    physical = 0.0
    for tl_start, _actual_dur, sf, tl_end in entries:
        model_dur = tl_end - tl_start
        gap = tl_start - physical
        if gap > 0.01:
            if gap_generator is None:
                raise ValueError("_fill_gaps: 有间隙但没有 gap_generator")
            files.append(gap_generator(gap))
            physical = tl_start
        files.append(sf)
        physical += model_dur  # use model duration for consistent tracking
    return files


def _track_blend(track: Track | None) -> str:
    """YAML schema：track.blend_mode 优先；兼容旧语义：段级 blend 回退。"""
    if track is None:
        return ""
    if track.blend_mode and track.blend_mode != "normal":
        return track.blend_mode
    for seg in track.segments:
        if seg.blend:
            return seg.blend
    return ""
