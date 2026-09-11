"""Editor end-to-end 渲染测试（marker: e2e，默认跳过；`uv run pytest -m e2e` 运行）。

素材自造：用 ffmpeg lavfi（testsrc2 + sine）在 session tmp 目录合成 5s 样本，
不依赖任何 products/ 项目目录；ffmpeg 不可用才 skip。重（10 段渲染）——只在
验证渲染管线（segments/tracks/mask/keyframes/audio）改动后跑。
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from editor.compose import render
from editor.manifest import from_markdown
from editor.models import Asset, Composition, Keyframe, Segment, Track

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg 不可用"),
]


@dataclass(frozen=True)
class Clips:
    a: str
    b: str
    c: str
    audio: str


def _make_video(path: Path, seconds: float) -> None:
    """testsrc2 画面 + sine 音轨。带音轨是必需的：test_08 把视频文件当 audio 源。"""
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"testsrc2=size=1920x1080:rate=30:duration={seconds}",
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=440:duration={seconds}",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-shortest",
            str(path),
        ],
        check=True,
        capture_output=True,
        timeout=120,
    )


def _make_audio(path: Path, seconds: float) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=440:duration={seconds}",
            "-c:a",
            "libmp3lame",
            str(path),
        ],
        check=True,
        capture_output=True,
        timeout=120,
    )


@pytest.fixture(scope="module")
def clips(tmp_path_factory: pytest.TempPathFactory) -> Clips:
    """3 段 video + 1 段 audio。5s = 现有断言最长 src 窗口（4.5s，test_06/07）所需。"""
    d = tmp_path_factory.mktemp("clips")
    a, b, c, audio = d / "a.mp4", d / "b.mp4", d / "c.mp4", d / "bgm.mp3"
    for p in (a, b, c):
        _make_video(p, 5.0)
    _make_audio(audio, 5.0)
    return Clips(a=str(a), b=str(b), c=str(c), audio=str(audio))


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


_output_dir: Path | None = None


def _out(name: str) -> Path:
    """输出落 session 级临时目录（惰性创建，非 e2e 运行不产生任何文件）。"""
    global _output_dir
    if _output_dir is None:
        _output_dir = Path(tempfile.mkdtemp(prefix="outgiving-editor-e2e-"))
    return _output_dir / name


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


def test_01_mask_rendering(clips: Clips) -> None:
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
            Asset(id="run_a", path=clips.a, type="video", duration=9.0, width=1920, height=1080),
            Asset(id="run_b", path=clips.a, type="video", duration=9.0, width=1920, height=1080),
        ],
        tracks=[Track(id="main", type="video", segments=[seg_a, seg_b])],
    )
    _verify_output(render(comp, str(_out("test1-mask.mp4"))))
    _assert_mask_visual(_out("test1-mask.mp4"), 1.5)


def test_02_keyframe_animation(clips: Clips) -> None:
    asset = Asset(id="run", path=clips.a, type="video", duration=9.0, width=1920, height=1080)
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


def test_03_blend_mode_overlay(clips: Clips) -> None:
    comp = Composition(
        name="test3-blend",
        width=1920,
        height=1080,
        fps=30,
        assets=[
            Asset(id="base", path=clips.b, type="video", duration=9.0, width=1920, height=1080),
            Asset(id="overlay", path=clips.a, type="video", duration=5.0, width=1920, height=1080),
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


def test_04_color_adjustments(clips: Clips) -> None:
    asset = Asset(id="meeting", path=clips.c, type="video", duration=10.0, width=1920, height=1080)
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


def test_05_all_features_combined(clips: Clips) -> None:
    asset = Asset(id="meeting", path=clips.c, type="video", duration=10.0, width=1920, height=1080)
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


def test_06_multitrack_composition(clips: Clips) -> None:
    comp = Composition(
        name="test6-multitrack",
        width=1920,
        height=1080,
        fps=30,
        assets=[
            Asset(id="main", path=clips.a, type="video", duration=9.0, width=1920, height=1080),
            Asset(id="overlay", path=clips.b, type="video", duration=9.0, width=1920, height=1080),
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


def test_07_timeline_gaps(clips: Clips) -> None:
    """tl_start 间隙 → 黑场；总时长 = 2 + 3(黑) + 2 = 7s。"""
    asset = Asset(id="run", path=clips.a, type="video", duration=5.12, width=1920, height=1080)
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


def test_08_audio_track_integration(clips: Clips) -> None:
    comp = Composition(
        name="test8-audio",
        width=1920,
        height=1080,
        fps=30,
        assets=[
            Asset(id="vid", path=clips.a, type="video", duration=9.0, width=1920, height=1080),
            Asset(id="bgm", path=clips.b, type="audio", duration=9.0),
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


def test_09_bgm_mp3(clips: Clips) -> None:
    comp = Composition(
        name="test9-bgm",
        width=1920,
        height=1080,
        fps=30,
        assets=[
            Asset(id="vid", path=clips.a, type="video", duration=9.0, width=1920, height=1080),
            Asset(id="bgm", path=clips.audio, type="audio", duration=16.0),
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


def test_10_mask_audio_combined(clips: Clips) -> None:
    """PNG mask + BGM：双流输出 + 遮罩视觉验证（中心亮、角落黑）。"""
    comp = Composition(
        name="test10-mask-audio",
        width=1920,
        height=1080,
        fps=30,
        assets=[
            Asset(id="vid", path=clips.a, type="video", duration=9.0, width=1920, height=1080),
            Asset(id="bgm", path=clips.audio, type="audio", duration=16.0),
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


MANIFEST = """\
# Composition: e2e fixture

## Meta

- width: 1920
- height: 1080
- fps: 30
- bg_color: "#000000"

## Assets

### video

- id: clip-a
  src: {a}
- id: clip-b
  src: {b}

### audio

- id: bgm
  src: {audio}

## Track: Main Video

order: 0
type: video

segments:

  - asset: clip-a
    start: 0.0
    end: 3.0
    speed: 1.0

  - asset: clip-b
    start: 3.0
    end: 6.0
    speed: 1.0
    transform:
      scale: [0.5, 0.5]
      position: [100, 0]

## Track: BGM

order: 0
type: audio

segments:

  - asset: bgm
    start: 0.0
    end: 6.0
    volume: 0.4
    envelope:
      - time: 0.0, volume: 0.0
      - time: 1.0, volume: 0.4

## Masks

- id: spotlight
  type: circle
  target: clip-a
  timeline: [0.0, 3.0]
  params:
    cx: 0.5
    cy: 0.5
    radius: 0.3
    feather: 0.05

## Keyframes

- target: clip-a
  property: scale
  type: vec2
  keyframes:
    - time: 0.0, value: [1.0, 1.0], easing: "ease_in_out"
    - time: 3.0, value: [1.1, 1.1], easing: "linear"
"""


def test_11_manifest_driven_render(tmp_path: Path, clips: Clips) -> None:
    """composition.md（内联 fixture 清单）→ 解析 → 渲染：mask/transform/envelope 全进管线。"""
    md = tmp_path / "composition.md"
    md.write_text(MANIFEST.format(a=clips.a, b=clips.b, audio=clips.audio))
    comp = from_markdown(md)
    assert comp.total_duration == pytest.approx(6.0)
    assert comp.tracks[0].segments[0].mask == "circle(0.5,0.5,0.6,feather=0.05)"
    assert comp.tracks[0].segments[1].transform_scale == (0.5, 0.5)
    assert comp.tracks[1].segments[0].envelope == [(0.0, 0.0), (1.0, 0.4)]
    result = render(comp, str(_out("test11-manifest.mp4")))
    _verify_output(result)
    _assert_audio_aac(result)
