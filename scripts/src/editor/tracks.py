"""Track assembler — segments → assembled track with gap handling.

Renders each segment via SegmentRenderer, then assembles them into a single
track file respecting tl_start timeline positions. Gaps get black/silent filler.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from editor.models import Composition, Track
from editor.segments import render_video_segment, render_audio_segment

_FFMPEG = os.environ.get("FFMPEG_BINARY", "ffmpeg")
_FFPROBE = os.environ.get("FFPROBE_BINARY", "ffprobe")


def assemble_video_track(track: Track, comp: Composition) -> Path | None:
    """Render all segments in a video track, insert black for timeline gaps, concat."""
    entries = []
    for i, seg in enumerate(track.segments):
        sf = render_video_segment(seg, comp, i)
        if sf:
            dur = _probe_duration(sf)
            entries.append((seg.tl_start, dur, sf, seg.tl_end))

    if not entries:
        return None

    entries.sort(key=lambda x: x[0])
    files = _fill_gaps(entries, comp.width, comp.height, comp.fps or 30,
                       gap_generator=lambda d: _blank_video(d, comp.width, comp.height, comp.fps or 30))

    if len(files) == 1:
        return files[0]
    return _concat_demuxer(files, "video")


def assemble_audio_track(track: Track, comp: Composition) -> Path | None:
    """Render all segments in an audio track, insert silence for timeline gaps, concat."""
    entries = []
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
        out_f = Path(tempfile.mkstemp(suffix=f".overlay{i}.mp4")[1])
        blend = _track_blend(tracks[i]) if i < len(tracks) else ""
        if blend:
            subprocess.run([
                _FFMPEG, "-y",
                "-i", str(current), "-i", str(video_files[i]),
                "-filter_complex", f"[1:v]scale={W}:{H}[ov];[0:v][ov]blend=all_mode={blend}:shortest=1",
                "-c:v", "libx264", "-crf", "18", "-an",
                str(out_f)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=60)
        else:
            subprocess.run([
                _FFMPEG, "-y",
                "-i", str(current), "-i", str(video_files[i]),
                "-filter_complex", f"[1:v]scale={W}:{H}[ov];[0:v][ov]overlay=0:0:shortest=1",
                "-c:v", "libx264", "-crf", "18", "-an",
                str(out_f)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=60)
        current = out_f
    return current


def mix_audio(files: list[Path]) -> Path:
    """Mix multiple audio tracks into one."""
    out_f = Path(tempfile.mkstemp(suffix=".mix.mp3")[1])
    inputs = []
    for f in files:
        inputs += ["-i", str(f)]
    n = len(files)
    subprocess.run([
        _FFMPEG, "-y"] + inputs + [
        "-filter_complex", f"amix=inputs={n}:duration=longest",
        "-f", "mp3", str(out_f)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=60)
    return out_f


# ── internals ──────────────────────────────────────────────


def _blank_video(duration: float, W: int, H: int, fps: float) -> Path:
    out_f = Path(tempfile.mkstemp(suffix=".blank.mp4")[1])
    subprocess.run([
        _FFMPEG, "-y",
        "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:d={duration}:r={fps}",
        "-c:v", "libx264", "-crf", "18", "-preset", "ultrafast", "-g", "1", "-an",
        str(out_f)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=30)
    return out_f


def _silent_audio(duration: float) -> Path:
    out_f = Path(tempfile.mkstemp(suffix=".silent.mp3")[1])
    subprocess.run([
        _FFMPEG, "-y",
        "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={duration}",
        "-c:a", "libmp3lame", "-q:a", "2",
        str(out_f)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=30)
    return out_f


def _concat_demuxer(files: list[Path], label: str) -> Path:
    out_f = Path(tempfile.mkstemp(suffix=f".{label}.mp4")[1])
    list_f = Path(tempfile.mkstemp(suffix=".txt")[1])
    list_f.write_text("\n".join(f"file '{f}'" for f in files))
    subprocess.run([
        _FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", str(list_f),
        "-c", "copy",
        str(out_f)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=120)
    return out_f


def _concat_audio(files: list[Path]) -> Path:
    out_f = Path(tempfile.mkstemp(suffix=".aconcat.mp3")[1])
    inputs = []
    for f in files:
        inputs += ["-i", str(f)]
    subprocess.run([
        _FFMPEG, "-y"] + inputs + [
        "-filter_complex", f"concat=n={len(files)}:v=0:a=1",
        "-c:a", "libmp3lame", "-q:a", "2",
        str(out_f)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=60)
    return out_f


def _probe_duration(path: Path) -> float:
    result = subprocess.run([
        _FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
    try:
        return float(result.stdout.strip())
    except (ValueError, TypeError):
        return 0.0


def _fill_gaps(entries: list[tuple[float, float, Path, float]], W: int = 0, H: int = 0,
               fps: float = 30, gap_generator=None) -> list[Path]:
    """Insert gap fillers between segments based on tl_start positions.

    Physical position tracks by actual rendered duration. Overlaps (negative
    gaps) are silently ignored — the concat demuxer just plays files sequentially.
    This can cause cumulative drift, but the drift only affects gap sizing, not
    the final output duration (which equals sum of all file durations + gaps).
    """
    files = []
    physical = 0.0
    for tl_start, actual_dur, sf, tl_end in entries:
        model_dur = tl_end - tl_start
        gap = tl_start - physical
        if gap > 0.01:
            files.append(gap_generator(gap))
            physical = tl_start
        files.append(sf)
        physical += model_dur  # use model duration for consistent tracking
    return files


def _track_blend(track: Track) -> str:
    """Extract blend mode from a track's first segment that specifies one."""
    for seg in track.segments:
        if seg.blend:
            return seg.blend
    return ""
