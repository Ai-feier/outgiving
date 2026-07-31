"""
Markdown manifest 解析器。agent 写 markdown 表格，parser 产出 Composition。
每节表格的 header row 定义了列名映射。
"""

from __future__ import annotations

import re
from pathlib import Path

from editor.models import Asset, Composition, Keyframe, Segment, Subtitle, Track


def parse_manifest(md_path: str | Path) -> Composition:
    """解析 markdown manifest → Composition。"""
    text = Path(md_path).read_text()
    base_dir = Path(md_path).resolve().parent
    lines = text.split("\n")

    comp = Composition(name="untitled")

    # Split into sections: each ## header starts a new block
    sections: list[tuple[str, list[str]]] = []
    current_header = ""
    current_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            comp.name = stripped[2:].strip()
            continue
        if stripped.startswith("## "):
            if current_header or current_lines:
                sections.append((current_header, current_lines))
            current_header = stripped[3:].strip()
            current_lines = []
            continue
        if current_header:
            current_lines.append(line)

    if current_header or current_lines:
        sections.append((current_header, current_lines))

    # Parse each section — handle multiple tables + ### sub-sections
    for header, body_lines in sections:
        key = header.lower()

        if key.startswith("keyframes"):
            # keyframes section may have ### seg-id sub-headers
            _ingest_keyframes_section(body_lines, comp, key)
            continue
        if key.startswith("adjustments"):
            _ingest_adjustments_section(body_lines, comp, key)
            continue

        all_rows = _parse_tables(body_lines)
        if not all_rows:
            continue

        if key.startswith("meta"):
            _ingest_meta(all_rows, comp)
        elif key.startswith("assets"):
            _ingest_assets(all_rows, comp, base_dir)
        elif key.startswith("track:"):
            _ingest_track(header.split(":", 1)[1].strip(), all_rows, comp)
        elif key.startswith("subtitles"):
            _ingest_subtitles(all_rows, comp)
        elif key.startswith("output"):
            _ingest_output(all_rows, comp)

    return comp


# ── table parser ───────────────────────────────────────────


def _parse_tables(lines: list[str]) -> list[dict[str, str]]:
    """Parse one or more markdown tables within a section. Header rows start new tables."""
    result: list[dict[str, str]] = []
    header_row: list[str] = []
    data_rows: list[list[str]] = []

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if _is_sep(stripped):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells or all(c == "" for c in cells):
            continue

        # Check if this looks like a header row (contains column-name-like cells)
        if _looks_like_header(cells):
            # Flush previous table
            result.extend(_rows_from_table(header_row, data_rows))
            header_row = [h.lower().replace(" ", "_") for h in cells]
            data_rows = []
        elif header_row:
            data_rows.append(cells)

    # Flush last table
    result.extend(_rows_from_table(header_row, data_rows))
    return result


def _looks_like_header(cells: list[str]) -> bool:
    """Check if cells look like column headers (not data)."""
    header_keywords = {"id", "asset", "source", "at", "speed", "mask", "tags",
                       "start", "end", "text", "font", "size", "color", "outline", "position",
                       "meta", "value", "path", "type", "key",
                       "scale", "rotation", "easing",
                       "format", "codec", "bitrate", "file",
                       "brightness", "contrast", "saturation", "vignette"}
    matches = sum(1 for c in cells if c.lower() in header_keywords)
    return matches >= 2  # At least 2 cells match known header names


def _rows_from_table(header: list[str], data: list[list[str]]) -> list[dict[str, str]]:
    if not header or not data:
        return []
    result = []
    for cells in data:
        row: dict[str, str] = {}
        for i, h in enumerate(header):
            if i < len(cells) and cells[i]:
                row[h] = cells[i]
        if row:
            result.append(row)
    return result


def _parse_table(lines: list[str]) -> list[dict[str, str]]:
    """Parse markdown table with header row → list of dicts keyed by normalized column name."""
    # Find header and data all_rows
    header_row: list[str] = []
    data_all_rows: list[list[str]] = []

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if _is_sep(stripped):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells or all(c == "" for c in cells):
            continue

        if not header_row:
            header_row = [h.lower().replace(" ", "_") for h in cells]
        else:
            data_all_rows.append(cells)

    if not header_row or not data_all_rows:
        return []

    result = []
    for cells in data_all_rows:
        row: dict[str, str] = {}
        for i, h in enumerate(header_row):
            if i < len(cells) and cells[i]:
                row[h] = cells[i]
        if row:
            result.append(row)
    return result


def _is_sep(line: str) -> bool:
    return bool(re.match(r"^\|[\s\-:]+\|", line))


# ── section ingest ─────────────────────────────────────────


def _ingest_meta(all_rows: list[dict[str, str]], comp: Composition) -> None:
    """Meta table: | key | value |"""
    for r in all_rows:
        key = r.get("meta", r.get("key", "")).lower()
        val = r.get("value", r.get("", ""))
        if not val:
            # Single-row table where each column is a key
            for k, v in r.items():
                _apply_meta_key(k, v, comp)
            continue
        _apply_meta_key(key, val, comp)


def _apply_meta_key(key: str, val: str, comp: Composition) -> None:
    k = key.replace(" ", "_").replace("-", "_")
    if k in ("resolution", "width_x_height", "size"):
        parts = re.split(r"[x×X]", val.lower().replace(" ", ""))
        if len(parts) == 2:
            comp.width = int(parts[0].strip())
            comp.height = int(parts[1].strip())
    elif k == "fps":
        comp.fps = int(val)
    elif k in ("output", "output_file"):
        comp.output["file"] = val


def _ingest_assets(all_rows: list[dict[str, str]], comp: Composition, base_dir: Path) -> None:
    """Assets table: | id | path | type |"""
    for r in all_rows:
        path_str = r.get("path", "")
        if path_str and not path_str.startswith("/"):
            path_str = str(base_dir / path_str)
        asset = Asset(
            id=r.get("id", ""),
            path=path_str,
            type=r.get("type", "video"),
        )
        comp.assets.append(asset)


def _ingest_track(track_id: str, all_rows: list[dict[str, str]], comp: Composition) -> None:
    """Track table: | id | asset | source | at | speed | mask | blend | opacity | volume | fade_in | fade_out | tags |"""
    # Determine type from track id
    is_audio = any(kw in track_id.lower() for kw in ("bgm", "audio", "voice", "music", "sfx", "sound"))
    track = Track(id=track_id, type="audio" if is_audio else "video")

    for r in all_rows:
        source = r.get("source", "0-0")
        seg = Segment(
            id=r.get("id", ""),
            asset_id=r.get("asset", ""),
            src_start=_range_start(source),
            src_end=_range_end(source),
            tl_start=_f(r, "at", "timeline"),
            speed=_f(r, "speed", default=1.0),
            volume=_f(r, "volume", default=1.0),
            fade_in=_f(r, "fade_in", default=0.0),
            fade_out=_f(r, "fade_out", default=0.0),
            mask=_normalize_mask(r.get("mask", "")),
            blend=r.get("blend", ""),
            opacity=_f(r, "opacity", default=1.0),
            tags=_tags(r.get("tags", "")),
        )
        track.segments.append(seg)

    comp.tracks.append(track)


def _ingest_subtitles(all_rows: list[dict[str, str]], comp: Composition) -> None:
    """Subtitles table: | start | end | text | font | size | color | outline | position |
    outline can be "3" or "3,#000000" (width,color combined).
    """
    for r in all_rows:
        # Parse outline: "3,#000000" → (3, "#000000")
        outline_raw = r.get("outline", "3")
        outline_val = 3
        outline_color_val = "#000000"
        if "," in outline_raw:
            parts = outline_raw.split(",", 1)
            try:
                outline_val = int(parts[0].strip())
            except ValueError:
                outline_val = 3
            outline_color_val = parts[1].strip() if len(parts) > 1 else "#000000"
        else:
            try:
                outline_val = int(outline_raw)
            except ValueError:
                outline_val = 3

        sub = Subtitle(
            text=r.get("text", ""),
            start=_f(r, "start"),
            end=_f(r, "end"),
            font=r.get("font", "PingFang SC"),
            size=int(r.get("size", "48") or "48"),
            color=r.get("color", "#FFFFFF"),
            outline=outline_val,
            outline_color=outline_color_val,
            position=r.get("position", "bottom,120"),
        )
        comp.subtitles.append(sub)


def _ingest_keyframes_section(body_lines: list[str], comp: Composition, _section_key: str) -> None:
    """Handle keyframes section with optional ### seg-id sub-headers."""
    current_target = ""
    current_lines: list[str] = []
    blocks: list[tuple[str, list[str]]] = []

    for line in body_lines:
        stripped = line.strip()
        if stripped.startswith("### "):
            if current_lines:
                blocks.append((current_target, current_lines))
            current_target = stripped[4:].strip().split()[0]  # "seg-emotion-01 (rain...)" → "seg-emotion-01"
            current_lines = []
            continue
        current_lines.append(line)
    if current_lines:
        blocks.append((current_target, current_lines))

    for target, block_lines in blocks:
        rows = _parse_tables(block_lines)
        if not rows:
            continue
        seg_id = target or _section_key.split(":", 1)[1].strip() if ":" in _section_key else target
        if seg_id:
            _ingest_keyframes(seg_id, rows, comp)


def _ingest_adjustments_section(body_lines: list[str], comp: Composition, _section_key: str) -> None:
    """Handle adjustments section — rows may have 'id' column specifying which segment."""
    all_rows = _parse_tables(body_lines)
    for r in all_rows:
        seg_id = r.get("id", r.get("segment", ""))
        if seg_id:
            seg = _find_segment(comp, seg_id)
            if seg:
                for col in ("brightness", "contrast", "saturation", "vignette"):
                    if r.get(col):
                        seg.adjustments[col] = float(r[col])


def _position(pos_str: str) -> tuple[float, float]:
    """Parse '0.5,0.5' → (0.5, 0.5)"""
    parts = [float(x.strip()) for x in pos_str.split(",") if x.strip()]
    return (parts[0] if parts else 0.5, parts[1] if len(parts) > 1 else 0.5)


def _ingest_one_keyframe(seg_id: str, r: dict[str, str], comp: Composition) -> None:
    seg = _find_segment(comp, seg_id)
    if not seg:
        return
    seg.keyframes.append(Keyframe(
        at=_f(r, "at"),
        scale=_f(r, "scale", default=1.0),
        position=_position(r.get("position", "0.5,0.5")),
        rotation=_f(r, "rotation", default=0.0),
        easing=r.get("easing", "linear"),
    ))


def _ingest_keyframes(target: str, all_rows: list[dict[str, str]], comp: Composition) -> None:
    """Keyframes table: | at | scale | position | rotation | easing |
    target is the section header suffix. If empty (just 'keyframes'), rows must include
    an 'id' or 'segment' column to specify which segment they belong to.
    """
    # If target is generic, rows carry their own segment id
    if not target:
        for r in all_rows:
            seg_id = r.get("id", r.get("segment", ""))
            if seg_id:
                _ingest_one_keyframe(seg_id, r, comp)
        return

    # Target specified in header: all rows apply to that segment
    seg = _find_segment(comp, target)
    if not seg:
        return
    for r in all_rows:
        seg.keyframes.append(Keyframe(
            at=_f(r, "at"),
            scale=_f(r, "scale", default=1.0),
            position=_position(r.get("position", "0.5,0.5")),
            rotation=_f(r, "rotation", default=0.0),
            easing=r.get("easing", "linear"),
        ))
        pos = r.get("position", "0.5,0.5")
        pos_parts = [float(x.strip()) for x in pos.split(",") if x.strip()]
        kf = Keyframe(
            at=_f(r, "at"),
            scale=_f(r, "scale", default=1.0),
            position=(
                pos_parts[0] if len(pos_parts) > 0 else 0.5,
                pos_parts[1] if len(pos_parts) > 1 else 0.5,
            ),
            rotation=_f(r, "rotation", default=0.0),
            easing=r.get("easing", "linear"),
        )
        seg.keyframes.append(kf)


def _ingest_adjustments(target: str, all_rows: list[dict[str, str]], comp: Composition) -> None:
    """Adjustments table: single row with brightness/contrast/saturation/vignette."""
    seg = _find_segment(comp, target)
    if not seg or not all_rows:
        return
    r = all_rows[0]
    for col in ("brightness", "contrast", "saturation", "vignette"):
        if r.get(col):
            seg.adjustments[col] = float(r[col])


def _ingest_output(all_rows: list[dict[str, str]], comp: Composition) -> None:
    """Output table: | format | codec | bitrate |"""
    if all_rows:
        r = all_rows[0]
        for k in ("format", "codec", "bitrate", "file"):
            if r.get(k):
                comp.output[k] = r[k]


# ── helpers ────────────────────────────────────────────────


def _f(row: dict[str, str], *keys: str, default: float = 0.0) -> float:
    """Get float from row by first matching key."""
    for k in keys:
        v = row.get(k, "")
        if v:
            return float(v)
    return default


def _range_start(s: str) -> float:
    parts = re.split(r"[–\-—]", s)
    return float(parts[0].strip()) if parts else 0.0


def _range_end(s: str) -> float:
    parts = re.split(r"[–\-—]", s)
    return float(parts[1].strip()) if len(parts) > 1 else 0.0


def _tags(s: str) -> list[str]:
    if not s or s in ("—", "-", "–"):
        return []
    return [t.strip() for t in s.split(",") if t.strip()]


def _normalize_mask(mask: str) -> str:
    """Normalize mask syntax: 'circle:0.5,0.45,0.25' → 'circle(0.5,0.45,0.25)'"""
    if not mask or mask in ("—", "-", "--", "none", ""):
        return ""
    # Already correct format: mask_type(...)
    if "(" in mask:
        return mask
    # Convert circle:params or linear:params
    for mtype in ("circle", "linear"):
        if mask.startswith(mtype + ":"):
            params = mask[len(mtype) + 1:]
            return f"{mtype}({params})"
    return mask


def _find_segment(comp: Composition, seg_id: str) -> Segment | None:
    for t in comp.tracks:
        for s in t.segments:
            if s.id == seg_id:
                return s
    return None
