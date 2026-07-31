"""
AI video editor — 素材 → 合成清单 → 视频。

AGI-native: agent 写 markdown manifest，引擎渲染。

Quickstart:
    from editor import parse_manifest, render
    comp = parse_manifest("composition.md")
    render(comp, "output.mp4")
"""

from editor.models import Asset, Composition, Keyframe, Segment, Subtitle, Track
from editor.manifest import parse_manifest
from editor.compose import render

__all__ = [
    "Asset",
    "Segment",
    "Track",
    "Keyframe",
    "Subtitle",
    "Composition",
    "parse_manifest",
    "render",
]
