"""Segment renderer — one segment, one temp file.

Each segment carries its processing instructions (trim, speed, color, keyframes, mask).
The renderer executes them via ffmpeg subprocess and returns a temp file path.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

from editor.keyframes import build_keyframe_filter
from editor.mask_png import generate as _generate_mask_png
from editor.models import Composition, Segment

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
    out_f = Path(tempfile.mkstemp(suffix=f".vseg{idx}.mkv")[1])
    vf_parts = [_scale_crop(W, H)]

    # Transform（YAML schema：transform.scale）— 画布缩放
    if seg.transform_scale:
        sx, sy = seg.transform_scale
        if sx != 1.0 or sy != 1.0:
            vf_parts.append(f"scale=iw*{sx}:ih*{sy}")

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
            pass1 = Path(tempfile.mkstemp(suffix=f".vseg{idx}p1.mkv")[1])
            cmd1 = [
                _FFMPEG,
                "-y",
                "-ss",
                str(seg.src_start),
                "-t",
                str(duration),
                "-i",
                asset.path,
                "-vf",
                f"{vf_base},format=yuva420p",
                "-c:v",
                "ffv1",
                "-pix_fmt",
                "yuva420p",
                "-an",
                "-r",
                str(comp.fps or 30),
                str(pass1),
            ]
            try:
                subprocess.run(
                    cmd1,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=120,
                    check=False,
                )
            except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
                return None
            if not pass1.exists() or pass1.stat().st_size == 0:
                return None
            # Pass 2: apply keyframe animation only (isolated to avoid heap corruption)
            vf_kf = f"setpts=PTS-STARTPTS,{kf}"
            if seg.mask:
                mask_png = _generate_mask_png(seg.mask, W, H)
                if mask_png:
                    result = _run_two_input(
                        str(pass1),
                        mask_png,
                        0,
                        duration,
                        f"[0:v]{vf_kf}[vid];[vid][1:v]alphamerge",
                        comp,
                        out_f,
                    )
                    try:
                        pass1.unlink()
                    except OSError:
                        pass
                    return result
            cmd2 = [
                _FFMPEG,
                "-y",
                "-i",
                str(pass1),
                "-vf",
                f"{vf_kf},format=yuva420p",
                "-c:v",
                "ffv1",
                "-pix_fmt",
                "yuva420p",
                "-an",
                "-r",
                str(comp.fps or 30),
                str(out_f),
            ]
            try:
                subprocess.run(
                    cmd2,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=120,
                    check=False,
                )
            except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
                try:
                    pass1.unlink()
                except OSError:
                    pass
                return None
            try:
                pass1.unlink()
            except OSError:
                pass
            return out_f if out_f.exists() and out_f.stat().st_size > 0 else None

    vf = ",".join(vf_parts) + ",format=yuva420p"

    # Mask: two-input alphamerge with PNG
    if seg.mask:
        mask_png = _generate_mask_png(seg.mask, W, H)
        if mask_png:
            return _run_two_input(
                asset.path,
                mask_png,
                seg.src_start,
                duration,
                f"[0:v]{vf}[vid];[vid][1:v]alphamerge",
                comp,
                out_f,
            )

    # Single pass, no mask, no keyframes
    cmd = [
        _FFMPEG,
        "-y",
        "-ss",
        str(seg.src_start),
        "-t",
        str(duration),
        "-i",
        asset.path,
        "-vf",
        vf,
        "-c:v",
        "ffv1",
        "-pix_fmt",
        "yuva420p",
        "-an",
        "-r",
        str(comp.fps or 30),
        str(out_f),
    ]
    try:
        subprocess.run(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120, check=False
        )
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
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
    af_parts: list[str] = []

    # Speed (atempo: 0.5-2.0 range, chain if needed)
    if seg.speed != 1.0 and seg.speed > 0:
        s = seg.speed
        while s > 2.0:
            af_parts.append("atempo=2.0")
            s /= 2.0
        while s < 0.5:
            af_parts.append("atempo=0.5")
            s /= 0.5
        if s != 1.0:
            af_parts.append(f"atempo={s}")

    if seg.envelope:
        # 音量包络（YAML schema：envelope 点 → 分段线性 volume 表达式）
        af_parts.append(f"volume='{_envelope_expr(seg.envelope)}':eval=frame")
    elif seg.volume != 1.0:
        af_parts.append(f"volume={seg.volume}")

    eff_dur = duration / max(seg.speed, 0.001)
    if seg.fade_in > 0:
        af_parts.append(f"afade=t=in:d={seg.fade_in}")
    if seg.fade_out > 0:
        af_parts.append(f"afade=t=out:st={max(0, eff_dur - seg.fade_out)}:d={seg.fade_out}")

    af = ",".join(af_parts) if af_parts else "anull"

    cmd = [
        _FFMPEG,
        "-y",
        "-ss",
        str(seg.src_start),
        "-t",
        str(duration),
        "-i",
        asset.path,
        "-af",
        af,
        "-f",
        "mp3",
        str(out_f),
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=30, check=False)
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        return None
    return out_f if out_f.exists() and out_f.stat().st_size > 0 else None


# ── helpers ────────────────────────────────────────────────


def _scale_crop(W: int, H: int) -> str:
    return f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"


def _eq_filter(adj: dict[str, float]) -> str:
    parts: list[str] = []
    for k in ("brightness", "contrast", "saturation"):
        if k in adj:
            parts.append(f"{k}={adj[k]}")
    return "eq=" + ":".join(parts) if parts else ""


def _envelope_expr(points: list[tuple[float, float]]) -> str:
    """[(time, volume)] → ffmpeg 分段线性表达式（t 为段内相对秒）。"""
    pts = sorted((max(0.0, t), v) for t, v in points)
    if not pts:
        return "1"
    expr = str(pts[-1][1])
    for i in range(len(pts) - 2, -1, -1):
        (t0, v0), (t1, v1) = pts[i], pts[i + 1]
        if t1 <= t0:
            continue
        lerp = f"{v0}+({v1}-{v0})*(t-{t0})/({t1}-{t0})"
        expr = f"if(lte(t,{t1}),{lerp},{expr})"
    if pts[0][0] > 0:
        expr = f"if(lte(t,{pts[0][0]}),{pts[0][1]},{expr})"
    return expr


def _run_two_input(
    video_path: str,
    mask_png: Path,
    start: float,
    duration: float,
    filter_complex: str,
    comp: Composition,
    out_f: Path,
) -> Path | None:
    """Run ffmpeg with two inputs (video + PNG mask). Cleans up mask on return.

    输出 ffv1/yuva420p（无损 + 保留 alpha）——中间文件必须带 alpha 才能传到最终合成。
    """
    cmd = [
        _FFMPEG,
        "-y",
        "-ss",
        str(start),
        "-t",
        str(duration),
        "-i",
        video_path,
        "-loop",
        "1",
        "-t",
        str(duration),
        "-i",
        str(mask_png),
        "-filter_complex",
        filter_complex,
        "-c:v",
        "ffv1",
        "-pix_fmt",
        "yuva420p",
        "-an",
        "-r",
        str(comp.fps or 30),
        str(out_f),
    ]
    try:
        subprocess.run(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120, check=False
        )
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        try:
            mask_png.unlink()
        except OSError:
            pass
        return None
    try:
        mask_png.unlink()
    except OSError:
        pass
    return out_f if out_f.exists() and out_f.stat().st_size > 0 else None


def _ffmpeg_version_ok() -> bool:
    """Check if ffmpeg version supports scale(eval=frame) without heap corruption.

    ffmpeg 4.4 crashes on scale(eval=frame) for >3s segments at 1080p.
    ffmpeg 5.0+ works correctly. Returns True if version >= 5.0.
    """
    try:
        import re

        result = subprocess.run(
            [_FFMPEG, "-version"], capture_output=True, text=True, timeout=5, check=False
        )
        m = re.search(r"ffmpeg version (\d+)\.(\d+)", result.stdout)
        if m:
            return int(m.group(1)) >= 5
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError, ValueError):
        pass
    return False
