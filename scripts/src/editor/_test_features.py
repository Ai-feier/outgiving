#!/usr/bin/env python3
"""Test ALL editor features end-to-end.

Usage: cd /home/aifeier/org-dev/bip/outgiving && PYTHONPATH=scripts/src python3 scripts/src/editor/_test_features.py
"""

import os
import sys
import time
from pathlib import Path

# Ensure we're in the right directory
os.chdir("/home/aifeier/org-dev/bip/outgiving")

from editor.models import Asset, Composition, Keyframe, Segment, Track
from editor.compose import render

FOOTAGE = Path("ai-video/projects/T004-funny-video/assets/footage")
OUTPUT = Path("ai-video/projects/T004-funny-video/editor-tests")
OUTPUT.mkdir(parents=True, exist_ok=True)

CLIP_A = str(FOOTAGE / "pexels-ch12-person-running-01.mp4")      # 5.1s  1920x1080
CLIP_B = str(FOOTAGE / "pexels-ch14-night-city-01.mp4")         # 8.2s  1920x1080
CLIP_C = str(FOOTAGE / "pexels-ch12-business-meeting-01.mp4")   # 9.8s  1920x1080
BGM_MP3 = "ai-video/projects/T004-funny-video/assets/audio/bgm-lofi.mp3"

results = []


def test(name: str, fn, **kwargs):
    """Run a test function, catch errors, record [PASS]/[FAIL]."""
    timeout = kwargs.get("timeout", 120)
    try:
        fn(timeout=timeout)
        results.append((name, "PASS", ""))
        print(f"  [PASS] {name}")
    except Exception as e:
        results.append((name, "FAIL", str(e)))
        print(f"  [FAIL] {name}: {e}")


def _verify_output(path: Path, min_size: int = 1024) -> None:
    """Verify output file exists and has reasonable size."""
    assert path.exists(), f"Output file {path} does not exist"
    assert path.stat().st_size >= min_size, f"Output file {path} too small: {path.stat().st_size} bytes"
    # Quick ffprobe to check validity
    import subprocess, json
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height,codec_type",
         "-of", "json", str(path)],
        capture_output=True, text=True, timeout=15
    )
    assert r.returncode == 0, f"ffprobe failed: {r.stderr[:200]}"
    data = json.loads(r.stdout)
    dur = float(data.get("format", {}).get("duration", 0))
    assert dur > 0, f"Output file {path} has zero duration"
    has_video = any(s.get("codec_type") == "video" for s in data.get("streams", []))
    assert has_video, f"Output file {path} has no video stream"


def _short_asset(asset_id: str, path: str, dur: float = 3.0) -> tuple[Asset, Segment, Asset]:
    """Create an Asset and a 3s Segment at tl_start=0."""
    asset = Asset(id=asset_id, path=path, type="video", duration=9.0, width=1920, height=1080)
    seg = Segment(
        id=asset_id,
        asset_id=asset_id,
        src_start=0,
        src_end=dur,
        tl_start=0,
    )
    return asset, seg


# ── Test 1: Mask rendering ─────────────────────────────────────

def run_test_1(timeout=120):
    assets = []
    tracks = []
    segments = []

    # Circle mask segment
    asset_a, seg_a = _short_asset("run_a", CLIP_A, 3.0)
    seg_a.mask = "circle(0.5,0.5,0.6,feather=0.08)"
    seg_a.id = "circle-mask"
    assets.append(asset_a)
    segments.append(seg_a)

    # Linear mask segment (after the circle one, at tl_start=3.5)
    asset_b, seg_b = _short_asset("run_b", CLIP_A, 3.0)
    seg_b.mask = "linear(0.5,0.5,0,feather=0.1)"
    seg_b.id = "linear-mask"
    seg_b.tl_start = 3.5
    assets.append(asset_b)
    segments.append(seg_b)

    track = Track(id="main", type="video", segments=segments)
    tracks.append(track)

    comp = Composition(
        name="test1-mask", width=1920, height=1080, fps=30, assets=assets, tracks=tracks
    )

    out = OUTPUT / "test1-mask.mp4"
    result = render(comp, str(out))
    _verify_output(result)


# ── Test 2: Keyframe animation ─────────────────────────────────

def run_test_2(timeout=120):
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
    track = Track(id="main", type="video", segments=[seg])
    comp = Composition(
        name="test2-keyframe", width=1920, height=1080, fps=30, assets=[asset], tracks=[track]
    )
    out = OUTPUT / "test2-keyframe.mp4"
    result = render(comp, str(out))
    _verify_output(result)


# ── Test 3: Blend mode overlay ─────────────────────────────────

def run_test_3(timeout=120):
    # Track 0: base video
    asset_base = Asset(id="base", path=CLIP_B, type="video", duration=9.0, width=1920, height=1080)
    seg_base = Segment(
        id="base-seg", asset_id="base",
        src_start=0, src_end=3.0, tl_start=0,
    )

    # Track 1: overlay with blend=multiply
    asset_over = Asset(id="overlay", path=CLIP_A, type="video", duration=5.0, width=1920, height=1080)
    seg_over = Segment(
        id="overlay-seg", asset_id="overlay",
        src_start=0, src_end=3.0, tl_start=0,
        blend="multiply", opacity=0.6,
    )

    track0 = Track(id="base", type="video", segments=[seg_base])
    track1 = Track(id="overlay", type="video", segments=[seg_over])
    comp = Composition(
        name="test3-blend", width=1920, height=1080, fps=30,
        assets=[asset_base, asset_over],
        tracks=[track0, track1],
    )
    out = OUTPUT / "test3-blend.mp4"
    result = render(comp, str(out))
    _verify_output(result)


# ── Test 4: Color adjustments ──────────────────────────────────

def run_test_4(timeout=120):
    asset = Asset(id="meeting", path=CLIP_C, type="video", duration=10.0, width=1920, height=1080)
    seg = Segment(
        id="color-adj",
        asset_id="meeting",
        src_start=0,
        src_end=3.0,
        tl_start=0,
        adjustments={"brightness": 0.1, "contrast": 1.2, "saturation": 0.8, "vignette": 0.3},
    )
    track = Track(id="main", type="video", segments=[seg])
    comp = Composition(
        name="test4-color", width=1920, height=1080, fps=30, assets=[asset], tracks=[track]
    )
    out = OUTPUT / "test4-color.mp4"
    result = render(comp, str(out))
    _verify_output(result)


# ── Test 5: All features combined ──────────────────────────────

def run_test_5(timeout=120):
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
    track = Track(id="main", type="video", segments=[seg])
    comp = Composition(
        name="test5-combined", width=1920, height=1080, fps=30, assets=[asset], tracks=[track]
    )
    out = OUTPUT / "test5-combined.mp4"
    result = render(comp, str(out))
    _verify_output(result)


# ── Test 6: Multi-track composition ────────────────────────────

def run_test_6(timeout=120):
    # Track 0: main video with two segments (each with effects)
    asset_main = Asset(id="main", path=CLIP_A, type="video", duration=9.0, width=1920, height=1080)
    seg_0 = Segment(
        id="seg-0", asset_id="main",
        src_start=0, src_end=2.0, tl_start=0,
        adjustments={"brightness": 0.05},
    )
    seg_1 = Segment(
        id="seg-1", asset_id="main",
        src_start=2.5, src_end=4.5, tl_start=2.5,
        keyframes=[
            Keyframe(at=0.0, scale=1.0, easing="ease-in"),
            Keyframe(at=2.0, scale=1.1, easing="ease-in"),
        ],
    )

    # Track 1: overlay with blend=overlay, low opacity
    asset_over = Asset(id="overlay", path=CLIP_B, type="video", duration=9.0, width=1920, height=1080)
    seg_over = Segment(
        id="overlay-seg", asset_id="overlay",
        src_start=0, src_end=4.5, tl_start=0,
        blend="overlay", opacity=0.15,
    )

    track0 = Track(id="main", type="video", segments=[seg_0, seg_1])
    track1 = Track(id="overlay", type="video", segments=[seg_over])
    comp = Composition(
        name="test6-multitrack", width=1920, height=1080, fps=30,
        assets=[asset_main, asset_over],
        tracks=[track0, track1],
    )
    out = OUTPUT / "test6-multitrack.mp4"
    result = render(comp, str(out))
    _verify_output(result)


# ── Test 7: Timeline gaps with tl_start ─────────────────────────

def run_test_7(timeout=120):
    """Test that tl_start gaps produce blank video between segments.

    Clip A is 5.12s long. All src_end values must be < 5.12.
    Layout: seg1(0-2s) + gap(3s) + seg2(2.5-4.5s, 2s) = 7s
    """
    asset = Asset(id="run", path=CLIP_A, type="video", duration=5.12, width=1920, height=1080)

    seg1 = Segment(
        id="seg1", asset_id="run",
        src_start=0, src_end=2.0, tl_start=0,
    )
    # seg2 at tl_start=5.0 → 3s gap after seg1 ends at t=2
    seg2 = Segment(
        id="seg2", asset_id="run",
        src_start=2.5, src_end=4.5, tl_start=5.0,
    )

    track = Track(id="main", type="video", segments=[seg1, seg2])
    comp = Composition(
        name="test7-gaps", width=1920, height=1080, fps=30,
        assets=[asset], tracks=[track],
    )
    out = OUTPUT / "test7-gaps.mp4"
    result = render(comp, str(out))
    _verify_output(result)

    # Verify total duration: seg1(2s) + gap(3s) + seg2(2s) = 7s
    # Allow ~0.2s tolerance for frame-boundary rounding
    import subprocess, json
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(result)],
        capture_output=True, text=True, timeout=15,
    )
    data = json.loads(r.stdout)
    dur = float(data.get("format", {}).get("duration", 0))
    assert abs(dur - 7.0) < 0.3, f"Expected ~7s total, got {dur}s"

    # Verify the gap is actually black — sample a frame mid-gap at ~3.5s
    r2 = subprocess.run(
        ["ffmpeg", "-y", "-ss", "3.5", "-i", str(result), "-vframes", "1",
         "-f", "rawvideo", "-pix_fmt", "gray", "-"],
        capture_output=True, timeout=15,
    )
    if r2.returncode == 0 and len(r2.stdout) > 10:
        # All pixels should be near-zero (black in gray = 16 for limited range,
        # but lavfi color produces full-range black = 0). Check mean < 10.
        pixels = list(r2.stdout)
        mean_brightness = sum(pixels) / len(pixels)
        assert mean_brightness < 10.0, \
            f"Gap frame at 3.5s is not black (mean={mean_brightness:.1f})"


# ── Test 8: Audio track integration ─────────────────────────────

def run_test_8(timeout=120):
    """Test that audio tracks produce output with an audio stream.

    Uses pexels-ch14-night-city-01.mp4 (CLIP_B) as the audio source
    because it has a detectable audio stream.
    """
    # Video track (video-only, no audio)
    asset_v = Asset(id="vid", path=CLIP_A, type="video", duration=9.0, width=1920, height=1080)
    seg_v = Segment(
        id="main", asset_id="vid",
        src_start=0, src_end=3.0, tl_start=0,
    )

    # Audio track (BGM sourced from a clip that has audio)
    BGM_PATH = CLIP_B  # pexels-ch14-night-city-01.mp4 has audio
    asset_a = Asset(id="bgm", path=BGM_PATH, type="audio", duration=9.0)
    seg_a = Segment(
        id="bgm-seg", asset_id="bgm",
        src_start=0, src_end=3.0, tl_start=0,
        volume=0.5,
    )

    video_track = Track(id="main", type="video", segments=[seg_v])
    audio_track = Track(id="bgm", type="audio", segments=[seg_a])

    comp = Composition(
        name="test8-audio", width=1920, height=1080, fps=30,
        assets=[asset_v, asset_a],
        tracks=[video_track, audio_track],
    )
    out = OUTPUT / "test8-audio.mp4"
    result = render(comp, str(out))
    _verify_output(result)

    # Verify audio stream exists in output
    import json, subprocess
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name",
         "-of", "json", str(result)],
        capture_output=True, text=True, timeout=15,
    )
    data = json.loads(r.stdout)
    streams = data.get("streams", [])
    has_video = any(s.get("codec_type") == "video" for s in streams)
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    assert has_video, "Output has no video stream"
    assert has_audio, f"Output has no audio stream — streams: {streams}"

    # Verify the audio codec is aac (our target)
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
    assert audio_streams[0].get("codec_name") == "aac", \
        f"Expected aac codec, got {audio_streams[0].get('codec_name')}"


# ── Test 9: Real BGM MP3 audio + video ────────────────────────────

def run_test_9(timeout=120):
    """Test with the actual BGM MP3 file as audio source."""
    asset_v = Asset(id="vid", path=CLIP_A, type="video", duration=9.0, width=1920, height=1080)
    seg_v = Segment(
        id="main", asset_id="vid",
        src_start=0, src_end=3.0, tl_start=0,
    )

    # Use the extracted BGM MP3 file
    asset_a = Asset(id="bgm", path=BGM_MP3, type="audio", duration=16.0)
    seg_a = Segment(
        id="bgm-seg", asset_id="bgm",
        src_start=0, src_end=3.0, tl_start=0,
        volume=0.5,
    )

    video_track = Track(id="main", type="video", segments=[seg_v])
    audio_track = Track(id="bgm", type="audio", segments=[seg_a])

    comp = Composition(
        name="test9-bgm", width=1920, height=1080, fps=30,
        assets=[asset_v, asset_a],
        tracks=[video_track, audio_track],
    )
    out = OUTPUT / "test9-bgm.mp4"
    result = render(comp, str(out))
    _verify_output(result)

    # Verify audio stream exists in output
    import json, subprocess
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name",
         "-of", "json", str(result)],
        capture_output=True, text=True, timeout=15,
    )
    data = json.loads(r.stdout)
    streams = data.get("streams", [])
    has_video = any(s.get("codec_type") == "video" for s in streams)
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    assert has_video, "Output has no video stream"
    assert has_audio, f"Output has no audio stream — streams: {streams}"
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
    assert audio_streams[0].get("codec_name") == "aac", \
        f"Expected aac codec, got {audio_streams[0].get('codec_name')}"


# ── Test 10: Combined mask + audio (fix integration test) ─────────

def run_test_10(timeout=180):
    """Test that PNG mask + BGM audio produce correct output with both streams.

    Verifies both Issue 1 (fast PNG mask) and Issue 2 (audio in final video).
    """
    asset_v = Asset(id="vid", path=CLIP_A, type="video", duration=9.0, width=1920, height=1080)
    seg_v = Segment(
        id="masked-video", asset_id="vid",
        src_start=0, src_end=3.0, tl_start=0,
        mask="circle(0.5,0.5,0.6,feather=0.08)",
        keyframes=[
            Keyframe(at=0.0, scale=1.0, easing="ease-in-out"),
            Keyframe(at=2.5, scale=1.1, easing="ease-in-out"),
        ],
        adjustments={"brightness": 0.05, "contrast": 1.1},
    )

    asset_a = Asset(id="bgm", path=BGM_MP3, type="audio", duration=16.0)
    seg_a = Segment(
        id="bgm-seg", asset_id="bgm",
        src_start=0, src_end=3.0, tl_start=0,
        volume=0.5, fade_in=0.3, fade_out=0.5,
    )

    video_track = Track(id="main", type="video", segments=[seg_v])
    audio_track = Track(id="bgm", type="audio", segments=[seg_a])

    comp = Composition(
        name="test10-mask-audio", width=1920, height=1080, fps=30,
        assets=[asset_v, asset_a],
        tracks=[video_track, audio_track],
    )
    out = OUTPUT / "test10-mask-audio.mp4"
    result = render(comp, str(out))
    _verify_output(result)

    # Verify both video and audio streams
    import json, subprocess
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name",
         "-of", "json", str(result)],
        capture_output=True, text=True, timeout=15,
    )
    data = json.loads(r.stdout)
    streams = data.get("streams", [])
    has_video = any(s.get("codec_type") == "video" for s in streams)
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    assert has_video, "Output has no video stream"
    assert has_audio, f"Output has no audio stream — streams: {streams}"
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
    assert audio_streams[0].get("codec_name") == "aac", \
        f"Expected aac codec, got {audio_streams[0].get('codec_name')}"

    # Verify the mask is visually applied: extract one grayscale frame,
    # check that the center pixel (inside circle) is bright and corner is dark
    r_probe2 = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=width,height",
         "-of", "json", str(result)],
        capture_output=True, text=True, timeout=15,
    )
    info_v = json.loads(r_probe2.stdout)
    w = info_v["streams"][0]["width"]
    h = info_v["streams"][0]["height"]

    r2 = subprocess.run(
        ["ffmpeg", "-y", "-ss", "1.5", "-i", str(result), "-vframes", "1",
         "-f", "rawvideo", "-pix_fmt", "gray", "-"],
        capture_output=True, timeout=15,
    )
    if r2.returncode == 0 and len(r2.stdout) >= w * h:
        pixels = r2.stdout  # bytes, each byte = luma value 0-255
        # Corner pixel (top-left) — should be masked out (black)
        corner_val = pixels[0]
        # Center pixel — should be visible through circle mask (bright)
        center_idx = h // 2 * w + w // 2
        center_val = pixels[center_idx]
        assert center_val > corner_val + 20, \
            f"Mask not applied: center={center_val}, corner={corner_val}"
        print(f"      Mask verified: center={center_val}, corner={corner_val} (OK)")


# ── Runner ──────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Editor Feature Verification Tests")
    print("=" * 60)
    print(f"Footage: {FOOTAGE}")
    print(f"Output:  {OUTPUT}")
    print()

    tests = [
        ("Test 1: Mask rendering (circle + linear)", run_test_1),
        ("Test 2: Keyframe animation (scale 1.0->1.15 ease-in-out)", run_test_2),
        ("Test 3: Blend mode overlay (multiply)", run_test_3),
        ("Test 4: Color adjustments (brightness/contrast/saturation/vignette)", run_test_4),
        ("Test 5: All features combined (mask+keyframe+color+speed)", run_test_5),
        ("Test 6: Multi-track composition (main+overlay with blend)", run_test_6),
        ("Test 7: Timeline gaps (tl_start with 3s blank between clips)", run_test_7),
        ("Test 8: Audio track integration (verify audio stream + aac codec)", run_test_8),
        ("Test 9: Real BGM MP3 audio file", run_test_9),
        ("Test 10: Combined PNG mask + BGM audio (fix integration)", run_test_10),
    ]

    for label, fn in tests:
        print(f"\n--- {label} ---")
        test(label, fn)

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    all_pass = True
    for name, status, err in results:
        if status == "FAIL":
            all_pass = False
            print(f"  [FAIL] {name}")
            print(f"         Error: {err}")
        else:
            print(f"  [PASS] {name}")

    if all_pass:
        print(f"\nAll {len(results)} tests PASSED")
    else:
        fails = [r for r in results if r[1] == "FAIL"]
        print(f"\n{len(fails)}/{len(results)} tests FAILED")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
