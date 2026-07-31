"""Subtitle engine — Composition → ASS subtitle file.

Handles style deduplication, overlap resolution, and ASS-format output.
ASS (Advanced SubStation Alpha) supports font styling, outlines, shadows,
and precise positioning — all rendered by ffmpeg's libass filter.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from editor.models import Composition, Subtitle


def write_ass(comp: Composition, output_path: Path) -> Path | None:
    """Generate an ASS subtitle file for the composition.

    Resolves temporal overlaps by truncating earlier subtitles.
    Returns path to the .ass file, or None if no subtitles present.
    """
    if not comp.subtitles:
        return None

    ass_path = output_path.with_suffix(".ass")
    W, H = comp.width or 1920, comp.height or 1080

    # Sort by start time, resolve overlaps
    subs = _resolve_overlaps(sorted(comp.subtitles, key=lambda s: s.start))

    # Deduplicate styles
    styles = _collect_styles(subs)

    # Write ASS file
    lines = _ass_header(W, H)
    lines += _ass_styles(styles)
    lines += _ass_events(subs, styles)

    ass_path.write_text("\n".join(lines), encoding="utf-8")
    return ass_path


# ── overlap resolution ─────────────────────────────────────


def _resolve_overlaps(subs: list[Subtitle]) -> list[Subtitle]:
    """Clip subtitle end times so no two subtitles overlap."""
    for i in range(len(subs) - 1):
        if subs[i + 1].start < subs[i].end:
            subs[i].end = subs[i + 1].start
    return subs


# ── style collection ───────────────────────────────────────


def _collect_styles(subs: list[Subtitle]) -> dict[str, dict]:
    """Build a deduplicated style map from subtitle list."""
    styles: dict[str, dict] = {}
    for sub in subs:
        key = f"{sub.font}_{sub.size}_{sub.outline}_{sub.outline_color}_{sub.position}"
        if key not in styles:
            styles[key] = {
                "name": f"S{len(styles)}",
                "font": sub.font,
                "size": sub.size,
                "color": _hex_to_ass(sub.color),
                "outline_color": _hex_to_ass(sub.outline_color),
                "outline": sub.outline,
                "alignment": _pos_to_align(sub.position),
                "margin_v": _margin_v(sub.position, H=1080),
            }
    return styles


# ── ASS format writers ─────────────────────────────────────


def _ass_header(W: int, H: int) -> list[str]:
    return [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {W}",
        f"PlayResY: {H}",
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
        "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    ]


def _ass_styles(styles: dict[str, dict]) -> list[str]:
    lines = []
    for s in styles.values():
        lines.append(
            f"Style: {s['name']},{s['font']},{s['size']},{s['color']},&H00000000,"
            f"{s['outline_color']},&H00000000,0,0,0,0,100,100,0,0,1,"
            f"{s['outline']},0,{s['alignment']},10,10,{s['margin_v']},1"
        )
    return lines


def _ass_events(subs: list[Subtitle], styles: dict[str, dict]) -> list[str]:
    lines = ["", "[Events]",
             "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for sub in subs:
        key = f"{sub.font}_{sub.size}_{sub.outline}_{sub.outline_color}_{sub.position}"
        style = styles[key]["name"]
        start = _secs_to_ass(sub.start)
        end = _secs_to_ass(sub.end)
        text = sub.text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
        lines.append(f"Dialogue: 0,{start},{end},{style},,0,0,0,,{text}")
    return lines


# ── format helpers ─────────────────────────────────────────


def _hex_to_ass(hex_color: str) -> str:
    """#RRGGBB or #RGB → &HBBGGRR& (ABGR hex)"""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c + c for c in h)
    if len(h) == 6:
        return f"&H{h[4:6]}{h[2:4]}{h[0:2]}&"
    return "&HFFFFFF&"


def _pos_to_align(position: str) -> int:
    """Convert position string to ASS alignment (numpad 1-9)."""
    p = position.lower()
    if p.startswith("top"):    return 8   # top-center
    if p.startswith("center") or p.startswith("middle"): return 5  # middle-center
    return 2  # bottom-center


def _margin_v(position: str, H: int) -> int:
    """Extract vertical margin from 'bottom,120' format."""
    try:
        parts = position.split(",")
        if len(parts) > 1:
            return int(parts[1].strip())
    except (ValueError, IndexError):
        pass
    return 120 if "bottom" in position.lower() else 10


def _secs_to_ass(seconds: float) -> str:
    """Convert seconds to ASS timestamp H:MM:SS.cc."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"
