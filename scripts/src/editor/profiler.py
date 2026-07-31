"""
素材画像自动生成 — 让 agent 理解素材内容。

场景检测 + profile.md 产出。借鉴 nyx研究所 的帧直方图对比法，
用 Pillow + ffmpeg 纯本地，不依赖外部模型。
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import tempfile
from pathlib import Path

_FFMPEG = os.environ.get("FFMPEG_BINARY", "ffmpeg")


def profile_video(video_path: str, output_dir: str | None = None,
                  sample_interval: float = 0.5, threshold: float = 0.15) -> str:
    """Analyze a video and generate a profile.md with scene boundaries.

    Args:
        video_path: Path to video file.
        output_dir: Where to write profile.md (default: same dir as video).
        sample_interval: Seconds between frame samples for scene detection.
        threshold: Histogram difference threshold for scene cut detection.

    Returns:
        Path to the generated profile.md.
    """
    video_path = str(Path(video_path).resolve())
    if output_dir is None:
        output_dir = str(Path(video_path).parent)
    else:
        output_dir = str(Path(output_dir))

    # Step 1: Extract frames at sample_interval
    frames_dir = Path(tempfile.mkdtemp(suffix="_frames"))
    frame_pattern = str(frames_dir / "frame_%06d.png")

    subprocess.run([
        _FFMPEG, "-y",
        "-i", video_path,
        "-vf", f"fps=1/{sample_interval},scale=320:-1",
        "-vframes", "1000",
        frame_pattern
    ], capture_output=True, timeout=60)

    # Step 2: Compute frame histograms
    frames = sorted(frames_dir.glob("frame_*.png"))
    if len(frames) < 2:
        return _write_minimal_profile(video_path, output_dir)

    histograms: list[list[float]] = []
    for fp in frames:
        try:
            hist = _frame_histogram(fp)
            histograms.append(hist)
        except Exception:
            histograms.append([0.0] * 64)

    # Step 3: Detect scene boundaries
    cuts: list[float] = [0.0]
    for i in range(1, len(histograms)):
        diff = _histogram_diff(histograms[i - 1], histograms[i])
        if diff > threshold:
            t = i * sample_interval
            cuts.append(t)
    cuts.append(float("inf"))  # sentinel

    # Step 4: Build scene descriptions
    duration = _probe_duration(video_path)
    scenes = []
    for i in range(len(cuts) - 1):
        start = cuts[i]
        end = min(cuts[i + 1], duration)
        if end - start < 0.1:
            continue
        mid_frame = frames[min(int(start / sample_interval), len(frames) - 1)]
        dominant = _dominant_colors(mid_frame)
        scenes.append({
            "start": round(start, 1),
            "end": round(end, 1),
            "duration": round(end - start, 1),
            "dominant_colors": dominant,
        })

    # Step 5: Write profile.md
    profile = _build_profile_md(video_path, scenes, duration)
    out_path = Path(output_dir) / (Path(video_path).stem + ".profile.md")
    out_path.write_text(profile)

    # Cleanup
    for fp in frames:
        try:
            fp.unlink()
        except OSError:
            pass
    try:
        frames_dir.rmdir()
    except OSError:
        pass

    return str(out_path)


# ── frame analysis ────────────────────────────────────────


def _frame_histogram(image_path: Path) -> list[float]:
    """Compute a 64-bin normalized color histogram for a frame."""
    from PIL import Image
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.getdata())
    bins = [0.0] * 64
    for r, g, b in pixels:
        # Quantize each channel to 4 levels → 4³ = 64 bins
        ri = r // 64
        gi = g // 64
        bi = b // 64
        bins[ri * 16 + gi * 4 + bi] += 1
    total = max(1, sum(bins))
    return [b / total for b in bins]


def _histogram_diff(h1: list[float], h2: list[float]) -> float:
    """Chi-squared distance between two histograms."""
    diff = 0.0
    for a, b in zip(h1, h2):
        if a + b > 0:
            diff += (a - b) ** 2 / (a + b)
    return diff / 2


def _mood_from_colors(colors: list[str]) -> str:
    """Auto-detect mood/vibe from dominant color hex codes.

    Clasifies based on warmth, coolness, and darkness:
    - Warm (#F, #E, #D in R channel for any given color): energetic/excited
    - Cool (#0, #6, #8 in B channel): calm/melancholy
    - Dark (all channels < #40): tense/dramatic
    - Mix of warm and cool or neither dominant: neutral

    Args:
        colors: List of hex color strings like ["#572e1c", "#6f513b"]

    Returns:
        Mood label string.
    """
    warm_count = 0
    cool_count = 0
    dark_count = 0

    for c in colors:
        c = c.lstrip("#")
        if len(c) != 6:
            continue
        try:
            r_val = int(c[0:2], 16)
            b_val = int(c[4:6], 16)
        except ValueError:
            continue

        # Dark: all channels < 0x40 (64)
        g_val = int(c[2:4], 16)
        if r_val < 64 and g_val < 64 and b_val < 64:
            dark_count += 1
            continue

        # Warm: R channel is #F, #E, #D range (>= 0xD0 = 208)
        if r_val >= 192:
            warm_count += 1

        # Cool: B channel is medium (#60-#9F) or we check R < B for blue dominance
        if b_val >= 128 or (b_val > r_val and b_val > 64):
            cool_count += 1

    total = len(colors)
    if total == 0:
        return "neutral"

    # If most colors are dark
    if dark_count >= total * 0.5:
        return "tense/dramatic"

    # Prefer warm over cool if both present
    warm_ratio = warm_count / total
    cool_ratio = cool_count / total

    if warm_ratio >= 0.5:
        return "energetic"
    if cool_ratio >= 0.5:
        return "calm/melancholy"
    if dark_count > 0:
        return "tense/dramatic"

    return "neutral"


def _best_for(mood: str, duration: float, scene_count: int) -> str:
    """Suggest the best usage category for a clip based on its profile."""
    if duration < 2.0:
        return "quick cut"
    if mood == "energetic":
        return "hook"
    if mood == "calm/melancholy":
        return "emotional/contemplative"
    if mood == "tense/dramatic":
        return "conflict/tension"
    # neutral
    if duration >= 5.0:
        return "B-roll / background"
    return "transition"


def _dominant_colors(image_path: Path) -> list[str]:
    """Get 3 dominant color hex codes from a frame."""
    from PIL import Image
    img = Image.open(image_path).convert("RGB").resize((80, 45))
    pixels = list(img.getdata())
    # Simple color averaging in 3 horizontal bands
    h = 45
    colors = []
    for band in range(3):
        band_pixels = pixels[band * h // 3 * 80:(band + 1) * h // 3 * 80]
        if band_pixels:
            r = sum(p[0] for p in band_pixels) // len(band_pixels)
            g = sum(p[1] for p in band_pixels) // len(band_pixels)
            b = sum(p[2] for p in band_pixels) // len(band_pixels)
            colors.append(f"#{r:02x}{g:02x}{b:02x}")
    return colors


# ── metadata ───────────────────────────────────────────────


def _probe_duration(video_path: str) -> float:
    """Get video duration via ffprobe."""
    result = subprocess.run([
        _FFMPEG.replace("ffmpeg", "ffprobe"), "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ], capture_output=True, text=True, timeout=10)
    try:
        return float(result.stdout.strip())
    except (ValueError, TypeError):
        return 0.0


# ── profile.md generation ──────────────────────────────────


def _build_profile_md(video_path: str, scenes: list[dict], duration: float) -> str:
    """Build a markdown profile document that agents can read."""
    name = Path(video_path).stem
    lines = [
        f"# {name}.profile",
        "",
        "> 自动生成 — 场景检测基于帧直方图对比。",
        f"> 来源: `{Path(video_path).name}` | 总时长: {duration:.1f}s",
        "",
        "## 元信息",
        "",
        f"| 属性 | 值 |",
        f"|------|----|",
        f"| 文件 | `{Path(video_path).name}` |",
        f"| 时长 | {duration:.1f}s |",
        f"| 场景数 | {len(scenes)} |",
        f"| 平均场景长 | {sum(s['duration'] for s in scenes) / max(len(scenes), 1):.1f}s |",
        "",
        "## 场景切分",
        "",
        "| # | 时间 | 时长 | 主色调 | 可用？ | 情绪 |",
        "|---|------|------|--------|--------|------|",
    ]

    for i, s in enumerate(scenes):
        colors = " · ".join(s["dominant_colors"]) if s["dominant_colors"] else "—"
        usable = "✓" if s["duration"] >= 1.0 else "⚠ 太短"
        mood = _mood_from_colors(s["dominant_colors"]) if s["dominant_colors"] else "—"
        lines.append(
            f"| {i + 1} | {s['start']:.1f}s–{s['end']:.1f}s "
            f"| {s['duration']:.1f}s | {colors} | {usable} | {mood} |"
        )

    lines += [
        "",
        "## 用法",
        "",
        "agent 读取此文件后，可以：",
        "- 根据「时间」列确定 `source_range`",
        "- 根据「时长」判断是否适合做 hook（<1s 太短，3-5s 合适）",
        "- 根据「主色调」判断情绪基调（暖色→能量，冷色→安静）",
        "",
        "在 composition.md 中引用格式：",
        "```",
        f"| seg-id | {name} | 2.5–5.0 | 0.0 | 1.0 | — | hook |",
        "```",
    ]

    return "\n".join(lines)


def _write_minimal_profile(video_path: str, output_dir: str) -> str:
    """Write a minimal profile when scene detection fails."""
    name = Path(video_path).stem
    duration = _probe_duration(video_path)
    content = (
        f"# {name}.profile\n\n"
        f"> 自动生成 — 场景检测失败（帧数不足）。\n"
        f"> 文件: `{Path(video_path).name}` | 时长: {duration:.1f}s\n\n"
        f"## 场景切分\n\n"
        f"| # | 时间 | 时长 | 可用？ |\n"
        f"|---|------|------|--------|\n"
        f"| 1 | 0.0s–{duration:.1f}s | {duration:.1f}s | ✓ |\n\n"
        f"## 用法\n\n"
        f"单场景视频，整个文件作为一个素材段使用。\n"
    )
    out = Path(output_dir) / f"{name}.profile.md"
    out.write_text(content)
    return str(out)
