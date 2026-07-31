"""Segment renderer — one segment, one temp file.

Each segment carries its processing instructions (trim, speed, color, keyframes, mask).
The renderer executes them via ffmpeg subprocess and returns a temp file path.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

from editor.models import Composition, Segment
from editor.mask_png import generate as _generate_mask_png
from editor.keyframes import build_keyframe_filter

_FFMPEG = os.environ.get("FFMPEG_BINARY", "ffmpeg")


def render_video_segment(seg: Segment, comp: Composition, idx: int = 0) -> Path | None:
    """Render one video segment → temp mp4 file. Returns None if asset missing."""
    asset = comp.asset_by_id(seg.asset_id)
    if not asset or not Path(asset.path).exists():
        return None

    duration = seg.src_end - seg.src_start
    if duration <= 0:
        return None

    W, H = comp.width, comp.height
    out_f = Path(tempfile.mkstemp(suffix=f".vseg{idx}.mp4")[1])
    vf_parts = [_scale_crop(W, H)]

    # Color adjustments
    if seg.adjustments:
        vf_parts.append(_eq_filter(seg.adjustments))
        if seg.adjustments.get("vignette", 0) > 0:
            vf_parts.append(f"vignette=PI/4*{seg.adjustments['vignette']}")

    # Speed + PTS reset
    speed = seg.speed if seg.speed > 0 else 1.0
    vf_parts.append(f"setpts=(PTS-STARTPTS)/{speed}")

    # Keyframe animation: two-pass. ffmpeg 4.4 has a heap corruption bug with
    # scale(eval=frame) that crashes on segments longer than ~3s at 1080p.
    # Workaround: skip animation for longer segments on affected versions.
    _kf_safe = duration <= 3.0 or _ffmpeg_version_ok()
    if seg.keyframes and _kf_safe:
        kf = build_keyframe_filter(seg.keyframes)
        if kf:
            vf_base = ",".join(vf_parts)
            # Pass 1: render without keyframes
            pass1 = Path(tempfile.mkstemp(suffix=f".vseg{idx}p1.mp4")[1])
            cmd1 = [
                _FFMPEG, "-y",
                "-ss", str(seg.src_start), "-t", str(duration),
                "-i", asset.path,
                "-vf", vf_base,
                "-c:v", "libx264", "-crf", "18", "-an",
                "-r", str(comp.fps or 30), "-preset", "ultrafast",
                str(pass1)
            ]
            try:
                subprocess.run(cmd1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            except (subprocess.TimeoutExpired, Exception):
                return None
            if not pass1.exists() or pass1.stat().st_size == 0:
                return None
            # Pass 2: apply keyframe animation only (isolated to avoid heap corruption)
            vf_kf = f"setpts=PTS-STARTPTS,{kf}"
            if seg.mask:
                mask_png = _generate_mask_png(seg.mask, W, H)
                if mask_png:
                    result = _run_two_input(str(pass1), mask_png, 0, duration,
                                            f"[0:v]{vf_kf}[vid];[vid][1:v]alphamerge", comp, out_f)
                    try: pass1.unlink()
                    except OSError: pass
                    return result
            cmd2 = [
                _FFMPEG, "-y", "-i", str(pass1),
                "-vf", vf_kf,
                "-c:v", "libx264", "-crf", "18", "-an",
                "-r", str(comp.fps or 30), "-preset", "ultrafast",
                str(out_f)
            ]
            try:
                subprocess.run(cmd2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            except (subprocess.TimeoutExpired, Exception):
                try: pass1.unlink()
                except OSError: pass
                return None
            try: pass1.unlink()
            except OSError: pass
            return out_f if out_f.exists() and out_f.stat().st_size > 0 else None

    vf = ",".join(vf_parts)

    # Mask: two-input alphamerge with PNG
    if seg.mask:
        mask_png = _generate_mask_png(seg.mask, W, H)
        if mask_png:
            return _run_two_input(
                asset.path, mask_png, seg.src_start, duration,
                f"[0:v]{vf}[vid];[vid][1:v]alphamerge",
                comp, out_f
            )

    # Single pass, no mask, no keyframes
    cmd = [
        _FFMPEG, "-y",
        "-ss", str(seg.src_start), "-t", str(duration),
        "-i", asset.path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "18", "-an",
        "-r", str(comp.fps or 30), "-preset", "ultrafast",
        str(out_f)
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    except (subprocess.TimeoutExpired, Exception):
        return None
    return out_f if out_f.exists() and out_f.stat().st_size > 0 else None


def render_audio_segment(seg: Segment, comp: Composition, idx: int = 0) -> Path | None:
    """Render one audio segment → temp mp3 file. Returns None if asset missing."""
    asset = comp.asset_by_id(seg.asset_id)
    if not asset or not Path(asset.path).exists():
        return None

    duration = seg.src_end - seg.src_start
    if duration <= 0:
        return None

    out_f = Path(tempfile.mkstemp(suffix=f".aseg{idx}.mp3")[1])
    af_parts = []

    # Speed (atempo: 0.5-2.0 range, chain if needed)
    if seg.speed != 1.0 and seg.speed > 0:
        s = seg.speed
        while s > 2.0:
            af_parts.append("atempo=2.0"); s /= 2.0
        while s < 0.5:
            af_parts.append("atempo=0.5"); s /= 0.5
        if s != 1.0:
            af_parts.append(f"atempo={s}")

    if seg.volume != 1.0:
        af_parts.append(f"volume={seg.volume}")

    eff_dur = duration / max(seg.speed, 0.001)
    if seg.fade_in > 0:
        af_parts.append(f"afade=t=in:d={seg.fade_in}")
    if seg.fade_out > 0:
        af_parts.append(f"afade=t=out:st={max(0, eff_dur - seg.fade_out)}:d={seg.fade_out}")

    af = ",".join(af_parts) if af_parts else "anull"

    cmd = [
        _FFMPEG, "-y",
        "-ss", str(seg.src_start), "-t", str(duration),
        "-i", asset.path,
        "-af", af, "-f", "mp3",
        str(out_f)
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=30)
    except (subprocess.TimeoutExpired, Exception):
        return None
    return out_f if out_f.exists() and out_f.stat().st_size > 0 else None


# ── helpers ────────────────────────────────────────────────


def _scale_crop(W: int, H: int) -> str:
    return f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"


def _eq_filter(adj: dict) -> str:
    parts = []
    for k in ("brightness", "contrast", "saturation"):
        if k in adj:
            parts.append(f"{k}={adj[k]}")
    return "eq=" + ":".join(parts) if parts else ""


def _run_two_input(video_path: str, mask_png: Path, start: float, duration: float,
                   filter_complex: str, comp: Composition, out_f: Path) -> Path | None:
    """Run ffmpeg with two inputs (video + PNG mask). Cleans up mask on return."""
    cmd = [
        _FFMPEG, "-y",
        "-ss", str(start), "-t", str(duration),
        "-i", video_path,
        "-i", str(mask_png),
        "-filter_complex", filter_complex,
        "-c:v", "libx264", "-crf", "18", "-an",
        "-r", str(comp.fps or 30), "-preset", "ultrafast",
        str(out_f)
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    except (subprocess.TimeoutExpired, Exception):
        try: mask_png.unlink()
        except OSError: pass
        return None
    try: mask_png.unlink()
    except OSError: pass
    return out_f if out_f.exists() and out_f.stat().st_size > 0 else None


def _ffmpeg_version_ok() -> bool:
    """Check if ffmpeg version supports scale(eval=frame) without heap corruption.

    ffmpeg 4.4 crashes on scale(eval=frame) for >3s segments at 1080p.
    ffmpeg 5.0+ works correctly. Returns True if version >= 5.0.
    """
    try:
        import re
        result = subprocess.run([_FFMPEG, "-version"], capture_output=True, text=True, timeout=5)
        m = re.search(r"ffmpeg version (\d+)\.(\d+)", result.stdout)
        if m:
            return int(m.group(1)) >= 5
    except Exception:
        pass
    return False
