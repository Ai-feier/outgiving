"""
AI video editor — 素材 → 合成清单 → 视频。

AGI-native: agent 写 markdown manifest（YAML schema），引擎渲染。

Quickstart:
    from editor import from_markdown, render
    comp = from_markdown("composition.md")
    render(comp, "output.mp4")
"""

from editor.models import (
    Asset,
    Composition,
    Keyframe,
    KeyframeSpec,
    Mask,
    PropertyKeyframe,
    Segment,
    Subtitle,
    SubtitleStyle,
    Track,
)
from editor.manifest import CompositionFormatError, from_markdown, parse_manifest
from editor.compose import render

__all__ = [
    "Asset",
    "Segment",
    "Track",
    "Keyframe",
    "PropertyKeyframe",
    "KeyframeSpec",
    "Mask",
    "Subtitle",
    "SubtitleStyle",
    "Composition",
    "CompositionFormatError",
    "from_markdown",
    "parse_manifest",
    "render",
]
