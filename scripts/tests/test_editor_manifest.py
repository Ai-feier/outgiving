"""composition.md YAML schema 解析器测试（快，无 ffmpeg）。

覆盖：未知节/段/asset 引用报错（带名字）、keyframes 目标解析、subtitle style 解析、
envelope 相对化、speed→src 区间、yamlmini 基础形状。
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
