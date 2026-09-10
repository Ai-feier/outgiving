"""Editor end-to-end 渲染测试（marker: e2e，默认跳过；`uv run pytest -m e2e` 运行）。

依赖 T004 真实素材 + ffmpeg。重（10 段渲染，~5-10 分钟）——只在验证渲染管线
（segments/tracks/mask/keyframes/audio）改动后跑。
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from editor.compose import render
from editor.models import Asset, Composition, Keyframe, Segment, Track

REPO = Path(__file__).resolve().parents[2]
T004 = REPO / "products/_archive/T004-funny-video"
FOOTAGE = T004 / "assets/footage"
OUTPUT = T004 / "editor-tests"

CLIP_A = str(FOOTAGE / "pexels-ch12-person-running-01.mp4")  # 5.1s 1920x1080
CLIP_B = str(FOOTAGE / "pexels-ch14-night-city-01.mp4")  # 8.2s 1920x1080
CLIP_C = str(FOOTAGE / "pexels-ch12-business-meeting-01.mp4")  # 9.8s 1920x1080
BGM_MP3 = str(T004 / "assets/audio/bgm-lofi.mp3")

HAS_FOOTAGE = Path(CLIP_A).exists() and Path(CLIP_B).exists() and Path(CLIP_C).exists()
pytestmark = [pytest.mark.e2e, pytest.mark.skipif(not HAS_FOOTAGE, reason="T004 素材缺失")]


def _verify_output(path: Path, min_size: int = 1024) -> None:
    """验证输出文件存在、有视频流、时长 > 0。"""
    assert path.exists(), f"Output file {path} does not exist"
    assert path.stat().st_size >= min_size, (
        f"Output file {path} too small: {path.stat().st_size} bytes"
    )
    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=width,height,codec_type",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert r.returncode == 0, f"ffprobe failed: {r.stderr[:200]}"
    data: dict[str, Any] = json.loads(r.stdout)
    dur = float(data.get("format", {}).get("duration", 0))
    assert dur > 0, f"Output file {path} has zero duration"
    streams: list[Any] = list(data.get("streams") or [])
    has_video = any(st.get("codec_type") == "video" for st in streams)
    assert has_video, f"Output file {path} has no video stream"


def _assert_audio_aac(path: Path) -> None:
    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=codec_type,codec_name",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    data: dict[str, Any] = json.loads(r.stdout)
    streams: list[Any] = list(data.get("streams", []))
    assert any(s.get("codec_type") == "video" for s in streams), "Output has no video stream"
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
    assert audio_streams, f"Output has no audio stream — streams: {streams}"
    assert audio_streams[0].get("codec_name") == "aac", (
        f"Expected aac codec, got {audio_streams[0].get('codec_name')}"
    )


def _out(name: str) -> Path:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    return OUTPUT / name


def _assert_mask_visual(path: Path, t: float) -> None:
    """圆形 mask 视觉验证：t 时刻中心亮、角落黑（透明区 = 背景色）。"""
    r_probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=width,height",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    info: dict[str, Any] = json.loads(r_probe.stdout)
    w = int(info["streams"][0]["width"])
    h = int(info["streams"][0]["height"])
    r2 = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(t),
            "-i",
            str(path),
            "-vframes",
            "1",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "gray",
            "-",
        ],
        capture_output=True,
        timeout=15,
        check=False,
    )
    assert r2.returncode == 0, f"Could not extract frame at t={t}"
    assert len(r2.stdout) >= w * h, "Frame too small"
    pixels = r2.stdout
    corner_val = pixels[0]
    center_val = pixels[h // 2 * w + w // 2]
    assert center_val > corner_val + 20, (
        f"Mask not applied at t={t}: center={center_val}, corner={corner_val}"
    )


def test_01_mask_rendering() -> None:
    """Circle + linear mask。"""
    seg_a = Segment(
        id="circle-mask",
        asset_id="run_a",
        src_start=0,
        src_end=3.0,
        tl_start=0,
        mask="circle(0.5,0.5,0.6,feather=0.08)",
    )
    seg_b = Segment(
        id="linear-mask",
        asset_id="run_b",
        src_start=0,
        src_end=3.0,
        tl_start=3.5,
        mask="linear(0.5,0.5,0,feather=0.1)",
    )
    comp = Composition(
        name="test1-mask",
        width=1920,
        height=1080,
        fps=30,
        assets=[
            Asset(id="run_a", path=CLIP_A, type="video", duration=9.0, width=1920, height=1080),
            Asset(id="run_b", path=CLIP_A, type="video", duration=9.0, width=1920, height=1080),
        ],
        tracks=[Track(id="main", type="video", segments=[seg_a, seg_b])],
    )
    _verify_output(render(comp, str(_out("test1-mask.mp4"))))
    _assert_mask_visual(_out("test1-mask.mp4"), 1.5)


def test_02_keyframe_animation() -> None:
    asset = Asset(id="run", path=CLIP_A, type="video", duration=9.0, width=1920, height=1080)
    seg = Segment(
        id="zoom",
        asset_id="run",
        src_start=0,
        src_end=3.5,
        tl_start=0,
        keyframes=[
            Keyframe(at=0.0, scale=1.0, easing="ease-in-out"),
            Keyframe(at=3.0, scale=1.15, easing="ease-in-out"),
        ],
    )
    comp = Composition(
        name="test2-keyframe",
        width=1920,
        height=1080,
        fps=30,
        assets=[asset],
        tracks=[Track(id="main", type="video", segments=[seg])],
    )
    _verify_output(render(comp, str(_out("test2-keyframe.mp4"))))


def test_03_blend_mode_overlay() -> None:
    comp = Composition(
        name="test3-blend",
        width=1920,
        height=1080,
        fps=30,
        assets=[
            Asset(id="base", path=CLIP_B, type="video", duration=9.0, width=1920, height=1080),
            Asset(id="overlay", path=CLIP_A, type="video", duration=5.0, width=1920, height=1080),
        ],
        tracks=[
            Track(
                id="base",
                type="video",
                segments=[
                    Segment(id="base-seg", asset_id="base", src_start=0, src_end=3.0, tl_start=0)
                ],
            ),
            Track(
                id="overlay",
                type="video",
                segments=[
                    Segment(
                        id="overlay-seg",
                        asset_id="overlay",
                        src_start=0,
                        src_end=3.0,
                        tl_start=0,
                        blend="multiply",
                        opacity=0.6,
                    )
                ],
            ),
        ],
    )
    _verify_output(render(comp, str(_out("test3-blend.mp4"))))


def test_04_color_adjustments() -> None:
    asset = Asset(id="meeting", path=CLIP_C, type="video", duration=10.0, width=1920, height=1080)
    seg = Segment(
        id="color-adj",
        asset_id="meeting",
        src_start=0,
        src_end=3.0,
        tl_start=0,
        adjustments={"brightness": 0.1, "contrast": 1.2, "saturation": 0.8, "vignette": 0.3},
    )
    comp = Composition(
        name="test4-color",
        width=1920,
        height=1080,
        fps=30,
        assets=[asset],
        tracks=[Track(id="main", type="video", segments=[seg])],
    )
    _verify_output(render(comp, str(_out("test4-color.mp4"))))


def test_05_all_features_combined() -> None:
    asset = Asset(id="meeting", path=CLIP_C, type="video", duration=10.0, width=1920, height=1080)
    seg = Segment(
        id="all-features",
        asset_id="meeting",
        src_start=0,
        src_end=3.0,
        tl_start=0,
        speed=0.9,
        mask="circle(0.5,0.5,0.6,feather=0.08)",
        keyframes=[
            Keyframe(at=0.0, scale=1.0, easing="ease-in-out"),
            Keyframe(at=2.5, scale=1.12, easing="ease-in-out"),
        ],
        adjustments={"brightness": 0.05, "contrast": 1.1, "saturation": 0.9},
    )
    comp = Composition(
        name="test5-combined",
        width=1920,
        height=1080,
        fps=30,
        assets=[asset],
        tracks=[Track(id="main", type="video", segments=[seg])],
    )
    _verify_output(render(comp, str(_out("test5-combined.mp4"))))


def test_06_multitrack_composition() -> None:
    comp = Composition(
        name="test6-multitrack",
        width=1920,
        height=1080,
        fps=30,
        assets=[
            Asset(id="main", path=CLIP_A, type="video", duration=9.0, width=1920, height=1080),
            Asset(id="overlay", path=CLIP_B, type="video", duration=9.0, width=1920, height=1080),
        ],
        tracks=[
            Track(
                id="main",
                type="video",
                segments=[
                    Segment(
                        id="seg-0",
                        asset_id="main",
                        src_start=0,
                        src_end=2.0,
                        tl_start=0,
                        adjustments={"brightness": 0.05},
                    ),
                    Segment(
                        id="seg-1",
                        asset_id="main",
                        src_start=2.5,
                        src_end=4.5,
                        tl_start=2.5,
                        keyframes=[
                            Keyframe(at=0.0, scale=1.0, easing="ease-in"),
                            Keyframe(at=2.0, scale=1.1, easing="ease-in"),
                        ],
                    ),
                ],
            ),
            Track(
                id="overlay",
                type="video",
                segments=[
                    Segment(
                        id="overlay-seg",
                        asset_id="overlay",
                        src_start=0,
                        src_end=4.5,
                        tl_start=0,
                        blend="overlay",
                        opacity=0.15,
                    )
                ],
            ),
        ],
    )
    _verify_output(render(comp, str(_out("test6-multitrack.mp4"))))


def test_07_timeline_gaps() -> None:
    """tl_start 间隙 → 黑场；总时长 = 2 + 3(黑) + 2 = 7s。"""
    asset = Asset(id="run", path=CLIP_A, type="video", duration=5.12, width=1920, height=1080)
    comp = Composition(
        name="test7-gaps",
        width=1920,
        height=1080,
        fps=30,
        assets=[asset],
        tracks=[
            Track(
                id="main",
                type="video",
                segments=[
                    Segment(id="seg1", asset_id="run", src_start=0, src_end=2.0, tl_start=0),
                    Segment(id="seg2", asset_id="run", src_start=2.5, src_end=4.5, tl_start=5.0),
                ],
            )
        ],
    )
    result = render(comp, str(_out("test7-gaps.mp4")))

    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(result)],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    dur = float(json.loads(r.stdout).get("format", {}).get("duration", 0))
    assert abs(dur - 7.0) < 0.3, f"Expected ~7s total, got {dur}s"

    # 间隙中点（3.5s）应为黑帧
    r2 = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            "3.5",
            "-i",
            str(result),
            "-vframes",
            "1",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "gray",
            "-",
        ],
        capture_output=True,
        timeout=15,
        check=False,
    )
    if r2.returncode == 0 and len(r2.stdout) > 10:
        mean_brightness = sum(r2.stdout) / len(r2.stdout)
        assert mean_brightness < 10.0, (
            f"Gap frame at 3.5s is not black (mean={mean_brightness:.1f})"
        )


def test_08_audio_track_integration() -> None:
    comp = Composition(
        name="test8-audio",
        width=1920,
        height=1080,
        fps=30,
        assets=[
            Asset(id="vid", path=CLIP_A, type="video", duration=9.0, width=1920, height=1080),
            Asset(id="bgm", path=CLIP_B, type="audio", duration=9.0),
        ],
        tracks=[
            Track(
                id="main",
                type="video",
                segments=[Segment(id="main", asset_id="vid", src_start=0, src_end=3.0, tl_start=0)],
            ),
            Track(
                id="bgm",
                type="audio",
                segments=[
                    Segment(
                        id="bgm-seg",
                        asset_id="bgm",
                        src_start=0,
                        src_end=3.0,
                        tl_start=0,
                        volume=0.5,
                    )
                ],
            ),
        ],
    )
    result = render(comp, str(_out("test8-audio.mp4")))
    _assert_audio_aac(result)


def test_09_bgm_mp3() -> None:
    comp = Composition(
        name="test9-bgm",
        width=1920,
        height=1080,
        fps=30,
        assets=[
            Asset(id="vid", path=CLIP_A, type="video", duration=9.0, width=1920, height=1080),
            Asset(id="bgm", path=BGM_MP3, type="audio", duration=16.0),
        ],
        tracks=[
            Track(
                id="main",
                type="video",
                segments=[Segment(id="main", asset_id="vid", src_start=0, src_end=3.0, tl_start=0)],
            ),
            Track(
                id="bgm",
                type="audio",
                segments=[
                    Segment(
                        id="bgm-seg",
                        asset_id="bgm",
                        src_start=0,
                        src_end=3.0,
                        tl_start=0,
                        volume=0.5,
                    )
                ],
            ),
        ],
    )
    _assert_audio_aac(render(comp, str(_out("test9-bgm.mp4"))))


def test_10_mask_audio_combined() -> None:
    """PNG mask + BGM：双流输出 + 遮罩视觉验证（中心亮、角落黑）。"""
    comp = Composition(
        name="test10-mask-audio",
        width=1920,
        height=1080,
        fps=30,
        assets=[
            Asset(id="vid", path=CLIP_A, type="video", duration=9.0, width=1920, height=1080),
            Asset(id="bgm", path=BGM_MP3, type="audio", duration=16.0),
        ],
        tracks=[
            Track(
                id="main",
                type="video",
                segments=[
                    Segment(
                        id="masked-video",
                        asset_id="vid",
                        src_start=0,
                        src_end=3.0,
                        tl_start=0,
                        mask="circle(0.5,0.5,0.6,feather=0.08)",
                        keyframes=[
                            Keyframe(at=0.0, scale=1.0, easing="ease-in-out"),
                            Keyframe(at=2.5, scale=1.1, easing="ease-in-out"),
                        ],
                        adjustments={"brightness": 0.05, "contrast": 1.1},
                    )
                ],
            ),
            Track(
                id="bgm",
                type="audio",
                segments=[
                    Segment(
                        id="bgm-seg",
                        asset_id="bgm",
                        src_start=0,
                        src_end=3.0,
                        tl_start=0,
                        volume=0.5,
                        fade_in=0.3,
                        fade_out=0.5,
                    )
                ],
            ),
        ],
    )
    result = render(comp, str(_out("test10-mask-audio.mp4")))
    _assert_audio_aac(result)

    r_probe2 = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=width,height",
            "-of",
            "json",
            str(result),
        ],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    info_v: dict[str, Any] = json.loads(r_probe2.stdout)
    w = int(info_v["streams"][0]["width"])
    h = int(info_v["streams"][0]["height"])
    r2 = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            "1.5",
            "-i",
            str(result),
            "-vframes",
            "1",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "gray",
            "-",
        ],
        capture_output=True,
        timeout=15,
        check=False,
    )
    if r2.returncode == 0 and len(r2.stdout) >= w * h:
        pixels = r2.stdout
        corner_val = pixels[0]
        center_val = pixels[h // 2 * w + w // 2]
        assert center_val > corner_val + 20, (
            f"Mask not applied: center={center_val}, corner={corner_val}"
        )
