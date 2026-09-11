"""composition.md YAML schema 解析器测试（快，无 ffmpeg）。

覆盖：合成清单全量解析（mask/keyframes/envelope/transform/effects）、未知节/段/asset
引用报错（带名字）、keyframes 目标解析、subtitle style 解析、envelope 相对化、
speed→src 区间、yamlmini 基础形状。

清单样本全部内联（不依赖任何 products/ 项目目录）。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from editor import yamlmini
from editor.manifest import CompositionFormatError, from_markdown
from editor.models import Composition


def write(tmp_path: Path, name: str, text: str) -> Path:
    p = tmp_path / name
    p.write_text(text)
    return p


MINIMAL = """\
# Composition: 测试

## Meta

- width: 1920
- height: 1080
- fps: 30

## Assets

### video

- id: clip-a
  src: assets/footage/a.mp4

## Track: Main

order: 0
type: video

segments:

  - asset: clip-a
    start: 0.0
    end: 4.0
    speed: 2.0
"""


# ── 合成清单：mask / keyframes / envelope / transform 正向覆盖 ──

FULL = """\
# Composition: 合成样本

## Meta

- duration: 630
- width: 1920
- height: 1080
- fps: 30
- bg_color: "#000000"

## Assets

### video

- id: party-crowd
  src: assets/footage/party.mp4
- id: smile-dead-eyes
  src: assets/footage/smile.mp4
- id: forest-path
  src: assets/footage/forest.mp4

### texture

- id: film-grain
  src: assets/footage/grain.mp4

### audio

- id: bgm-main
  src: assets/audio/bgm-main.mp3

## Track: Main Video

order: 0
type: video
blend_mode: normal

segments:

  - asset: party-crowd
    start: 0.0
    end: 3.0
    speed: 0.8
    transform:
      scale: [1.0, 1.0]
    effects:
      color: { saturation: 1.15, contrast: 1.2 }

  - asset: forest-path
    start: 5.0
    end: 10.0
    speed: 1.0

  - asset: smile-dead-eyes
    start: 20.0
    end: 25.0
    speed: 1.0

## Track: Texture Overlay

order: 1
type: video
blend_mode: overlay
opacity: 0.12

segments:

  - asset: film-grain
    start: 0.0
    end: 25.0
    speed: 1.0

## Track: UI Animation Overlay

order: 3
type: video
blend_mode: screen

segments:

  - asset: smile-dead-eyes
    start: 40.0
    end: 44.0
    speed: 1.0
    transform:
      position: [600, -400]
      scale: [0.5, 0.5]

## Track: BGM

order: 0
type: audio

segments:

  - asset: bgm-main
    start: 30.0
    end: 60.0
    volume: 0.35
    envelope:
      - time: 30.0, volume: 0.0
      - time: 33.0, volume: 0.35

## Masks

- id: circle-spotlight
  type: circle
  target: smile-dead-eyes
  timeline: [20.0, 25.0]
  params:
    cx: 0.5
    cy: 0.45
    radius: 0.28
    feather: 0.06

- id: linear-wipe
  type: linear
  target: forest-path
  timeline: [5.0, 10.0]
  params:
    x0: 0.0, y0: 1.0
    x1: 0.0, y1: 0.0
    feather: 0.2

## Subtitles

- start: 0.0
  end: 2.0
  text: "第一句"
  style: subtitle-main

- start: 2.0
  end: 4.0
  text: "第二句"
  style: subtitle-title

## Subtitle Styles

- id: subtitle-main
  font_size: 60
  primary_color: "#FFFFFF"
  position: [0.5, 0.88]

- id: subtitle-title
  font_size: 96
  primary_color: "#FF6B6B"
  position: [0.5, 0.5]

## Keyframes

- target: smile-dead-eyes
  property: scale
  type: vec2
  keyframes:
    - time: 20.0, value: [1.0, 1.0], easing: "ease_out_cubic"
    - time: 25.0, value: [1.08, 1.08], easing: "linear"

## Chapter Markers

- marker: "Hook"
  time: 0.0
  color: "#FF6B6B"

- marker: "结尾"
  time: 40.0
  color: "#4ECDC4"
"""


def full(tmp_path: Path) -> Composition:
    return from_markdown(write(tmp_path, "full.md", FULL))


def test_full_manifest_parse(tmp_path: Path) -> None:
    comp = full(tmp_path)
    assert comp.name == "合成样本"
    assert (comp.width, comp.height, comp.fps) == (1920, 1080, 30)
    assert comp.bg_color == "#000000"
    assert len(comp.assets) == 5
    assert [t.id for t in comp.tracks] == [
        "Main Video",
        "Texture Overlay",
        "UI Animation Overlay",
        "BGM",
    ]
    assert comp.tracks[0].order == 0 and comp.tracks[2].order == 3
    assert comp.tracks[1].blend_mode == "overlay" and comp.tracks[1].opacity == 0.12
    assert len(comp.tracks[0].segments) == 3
    assert len(comp.masks) == 2
    assert len(comp.subtitles) == 2
    assert set(comp.subtitle_styles) == {"subtitle-main", "subtitle-title"}
    assert len(comp.keyframe_specs) == 1
    assert len(comp.chapter_markers) == 2
    # 时间线：start/end 就是时间线秒（speed 不进 tl_end）
    assert comp.total_duration == pytest.approx(60.0)
    seg0 = comp.tracks[0].segments[0]
    assert seg0.tl_end == pytest.approx(3.0)
    assert seg0.src_end == pytest.approx(3.0 / 0.8)  # speed 反推源区间


def test_keyframes_no_double_append(tmp_path: Path) -> None:
    """回归：旧 parser 把每行 keyframe append 两次。"""
    comp = full(tmp_path)
    sm = [s for s in comp.tracks[0].segments if s.asset_id == "smile-dead-eyes"][0]
    assert len(sm.keyframes) == 2  # time 20.0 + 25.0，各一条
    assert sm.keyframes[0].at == pytest.approx(0.0) and sm.keyframes[0].scale == 1.0
    assert sm.keyframes[0].easing == "ease-out"  # ease_out_cubic → ease-out
    assert sm.keyframes[1].at == pytest.approx(5.0) and sm.keyframes[1].scale == pytest.approx(1.08)
    assert sm.keyframes[1].easing == "linear"
    # 时间窗外的同 asset 段不分发
    assert comp.tracks[2].segments[0].keyframes == []


def test_masks_distributed(tmp_path: Path) -> None:
    comp = full(tmp_path)
    sm = [s for s in comp.tracks[0].segments if s.asset_id == "smile-dead-eyes"][0]
    assert sm.mask == "circle(0.5,0.45,0.56,feather=0.06)"  # radius 0.28 → size 0.56
    wipe = [s for s in comp.tracks[0].segments if s.asset_id == "forest-path"]
    assert any("linear(" in s.mask for s in wipe)
    # 时间窗不重叠 → 不分发
    assert comp.tracks[2].segments[0].mask == ""


def test_envelope_relative(tmp_path: Path) -> None:
    comp = full(tmp_path)
    bgm = [s for s in comp.tracks[3].segments if s.asset_id == "bgm-main"][0]
    assert bgm.envelope[0] == (0.0, 0.0)  # 时间线 30.0 - 段起点 30.0
    assert bgm.envelope[1] == (3.0, 0.35)


def test_transforms(tmp_path: Path) -> None:
    comp = full(tmp_path)
    ui = comp.tracks[2].segments[0]
    assert ui.transform_scale == (0.5, 0.5)
    assert ui.transform_position == (600.0, -400.0)


def test_effects(tmp_path: Path) -> None:
    comp = full(tmp_path)
    s = comp.tracks[0].segments[0]
    assert s.adjustments == {"contrast": 1.2, "saturation": 1.15}


# ── 报错路径（必须带名字，不能静默丢段）──────────────────────


def test_unknown_section_raises(tmp_path: Path) -> None:
    p = write(tmp_path, "m.md", MINIMAL.replace("## Meta", "## Banana"))
    with pytest.raises(CompositionFormatError, match="Banana"):
        from_markdown(p)


def test_unknown_asset_ref_raises(tmp_path: Path) -> None:
    p = write(tmp_path, "m.md", MINIMAL.replace("asset: clip-a", "asset: 不存在的素材"))
    with pytest.raises(CompositionFormatError, match="不存在的素材"):
        from_markdown(p)


def test_unknown_segment_field_raises(tmp_path: Path) -> None:
    body = MINIMAL.replace("speed: 2.0", "speed: 2.0\n    speed_dial: 7")
    p = write(tmp_path, "m.md", body)
    with pytest.raises(CompositionFormatError, match="speed_dial"):
        from_markdown(p)


def test_end_before_start_raises(tmp_path: Path) -> None:
    body = MINIMAL.replace("end: 4.0", "end: 0.0")
    p = write(tmp_path, "m.md", body)
    with pytest.raises(CompositionFormatError, match="end"):
        from_markdown(p)


def test_track_without_segments_raises(tmp_path: Path) -> None:
    body = MINIMAL.replace(
        "segments:\n\n  - asset: clip-a\n    start: 0.0\n    end: 4.0\n    speed: 2.0",
        "segments: []",
    )
    p = write(tmp_path, "m.md", body)
    with pytest.raises(CompositionFormatError, match="Main"):
        from_markdown(p)


def test_no_tracks_raises(tmp_path: Path) -> None:
    p = write(
        tmp_path,
        "m.md",
        MINIMAL.replace("## Track: Main", "## Meta Extra").replace(
            "order: 0\ntype: video\n\nsegments:\n\n  - asset: clip-a\n    start: 0.0\n    end: 4.0\n    speed: 2.0\n",
            "",
        ),
    )
    with pytest.raises(CompositionFormatError, match="Track"):
        from_markdown(p)


def test_subtitle_unknown_style_raises(tmp_path: Path) -> None:
    body = (
        MINIMAL
        + """
## Subtitles

- start: 0.0
  end: 1.0
  text: "hi"
  style: 未定义样式
"""
    )
    p = write(tmp_path, "m.md", body)
    with pytest.raises(CompositionFormatError, match="未定义样式"):
        from_markdown(p)


def test_keyframe_unknown_target_raises(tmp_path: Path) -> None:
    body = (
        MINIMAL
        + """
## Keyframes

- target: 幽灵素材
  property: scale
  keyframes:
    - time: 0.0, value: [1.0, 1.0]
"""
    )
    p = write(tmp_path, "m.md", body)
    with pytest.raises(CompositionFormatError, match="幽灵素材"):
        from_markdown(p)


def test_duplicate_asset_id_raises(tmp_path: Path) -> None:
    body = MINIMAL.replace(
        "src: assets/footage/a.mp4",
        "src: assets/footage/a.mp4\n- id: clip-a\n  src: assets/footage/b.mp4",
    )
    p = write(tmp_path, "m.md", body)
    with pytest.raises(CompositionFormatError, match="重复"):
        from_markdown(p)


def test_bad_yaml_line_number(tmp_path: Path) -> None:
    body = "## Assets\n\n### video\n\n- id: a\n  src: x.mp4\n    缩进坏掉: 1\n"
    p = write(tmp_path, "m.md", "# C\n\n" + body)
    with pytest.raises(CompositionFormatError, match="line"):
        from_markdown(p)


# ── 语义细节 ────────────────────────────────────────────────


def test_minimal_parse(tmp_path: Path) -> None:
    comp = from_markdown(write(tmp_path, "m.md", MINIMAL))
    assert comp.name == "测试"
    assert len(comp.tracks) == 1 and len(comp.tracks[0].segments) == 1
    s = comp.tracks[0].segments[0]
    assert s.tl_start == 0.0 and s.tl_end == pytest.approx(4.0)
    assert s.speed == 2.0 and s.src_end == pytest.approx(2.0)


def test_subtitle_style_resolution(tmp_path: Path) -> None:
    body = (
        MINIMAL
        + """
## Subtitles

- start: 0.0
  end: 1.0
  text: "你好"
  style: s1

## Subtitle Styles

- id: s1
  font_size: 60
  primary_color: "#FF4444"
  position: [0.5, 0.5]
"""
    )
    comp = from_markdown(write(tmp_path, "m.md", body))
    assert comp.subtitles[0].style_id == "s1"
    st = comp.subtitle_styles["s1"]
    assert st.font_size == 60 and st.primary_color == "#FF4444"


def test_chapter_markers_passthrough(tmp_path: Path) -> None:
    body = (
        MINIMAL
        + """
## Chapter Markers

这些是导航用的元数据。

- marker: "Hook"
  time: 0.0
  color: "#FF6B6B"
"""
    )
    comp = from_markdown(write(tmp_path, "m.md", body))
    assert comp.chapter_markers[0]["marker"] == "Hook"
    assert comp.chapter_markers[0]["time"] == 0.0


# ── yamlmini 基础 ──────────────────────────────────────────


def test_yamlmini_parse_block() -> None:
    items = yamlmini.parse_block(
        [
            "- a: 1",
            "  b: [x, y]",
            "- a: 2.5",
            "- '带 空格'",
        ]
    )
    assert items == [{"a": 1, "b": ["x", "y"]}, {"a": 2.5}, "带 空格"]


def test_yamlmini_split_blocks() -> None:
    blocks = yamlmini.split_blocks("### 甲\n- a: 1\n### 乙\n- b: 2")
    assert blocks == [("甲", ["- a: 1"]), ("乙", ["- b: 2"])]


def test_yamlmini_value_then_kv() -> None:
    items = yamlmini.parse_block(["- x0: 0.0, y0: 1.0", "  feather: 0.1"])
    assert items == [{"x0": 0.0, "y0": 1.0, "feather": 0.1}]


def test_yamlmini_flow_in_inline_kv() -> None:
    items = yamlmini.parse_block(['- time: 0.0, value: [1.0, 1.0], easing: "linear"'])
    assert items == [{"time": 0.0, "value": [1.0, 1.0], "easing": "linear"}]


def test_yamlmini_bad_indent_raises() -> None:
    with pytest.raises(yamlmini.YamlMiniError, match="line 3"):
        yamlmini.parse_block(["- a: 1", "  b: 2", "      c: 3"], start_line_no=1)


def test_compilation_smoke() -> None:
    """最小可渲染结构（供 e2e 参考）：解析不炸。"""
    c: Composition = from_markdown(write(Path("/tmp"), "smoke.md", MINIMAL))
    assert c.total_duration == pytest.approx(4.0)
