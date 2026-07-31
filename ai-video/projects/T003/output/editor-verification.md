# Editor Module Verification

Date: 2026-07-28
Target: `/home/aifeier/org-dev/bip/outgiving/scripts/src/editor/`

## Files

| File | Lines | Role |
|------|-------|------|
| `models.py` | 136 | Dataclasses: Asset, Segment, Track, Keyframe, Subtitle, Composition |
| `manifest.py` | 294 | Markdown manifest -> Composition parser |
| `compose.py` | 405 | Composition -> ffmpeg-python filter graph -> video file |
| `cli.py` | 140 | Standalone CLI (duplicate; actual entry point is volcengine/cli.py) |

## Integration

CLI entry point: `ai = "volcengine.cli:cli"` (pyproject.toml), commands:
- `ai edit compose --manifest <md> --output <mp4>`
- `ai edit clip --input <mp4> --start <s> --end <s> --output <mp4>`
- `ai edit concat --inputs <a> <b> --output <mp4>`
- `ai edit speed --input <mp4> --factor <n> --output <mp4>`
- `ai edit mute --input <mp4> --output <mp4>`

`editor/cli.py` is a standalone copy of the same commands, NOT wired to the `ai` entry point. Both were fixed in this pass.

## Test Results

| Test | Status | Notes |
|------|--------|-------|
| clip (3s extract) | PASS | Output: 3.0s video-only (original code dropped audio — FIXED) |
| clip with audio | PASS | Output: 3.0s video + AAC audio |
| concat (2 segments) | PASS | Output: 7.0s video + audio |
| speed 2x | PASS | Output: 2.58s for 5s source (expected ~2.5s) |
| speed 4x (atempo chain) | PASS | Output: 2.08s for 8s source (expected 2.0s) |
| speed with audio | PASS | Video + audio both sped |
| mute | PASS | Video only, no audio stream |
| composition manifest | PASS | Full pipeline: markdown -> render |
| subtitles (ASS burn) | PASS | Fixed: `#000` shorthand hex parsing |
| circle mask | PASS | geq(lum) + alphamerge |
| linear mask | PASS | geq(lum) + alphamerge |
| keyframes (parsing only) | PASS | Data model works; renderer ignores keyframes |

## Bugs Found and Fixed

### 1. `#000` shorthand hex not handled (compose.py:_hex_to_ass)

**Severity**: High — subtitle outline color was silently wrong.

Input `#000` (3-char hex) was treated as invalid and returned `&HFFFFFF&` (white outline instead of black). ffmpeg's ASS renderer would draw white-on-white text, making subtitles invisible unless the input was full `#000000`.

**Fix**: Expand 3-char hex to 6-char by doubling each digit (`#RGB` -> `#RRGGBB`). Also changed fallback from `&HFFFFFF&` to `&H000000&` (black, safer for outline).

### 2. geq filter alpha/cb/cr params unavailable in ffmpeg 4.4 (compose.py:_build_mask)

**Severity**: High — mask rendering crashed with `Option 'alpha' not found`.

The `geq` filter in ffmpeg 4.4 does not support `alpha`, `cb`, or `cr` parameters (they were added in ffmpeg 5.0). The `alphamerge` filter only needs the second input's **luma** channel as alpha, so `geq(lum=expr)` is sufficient.

**Fix**: Changed `geq(lum=..., cb=..., cr=..., alpha=...)` to `geq(lum=...)` for both circle and linear masks.

### 3. Linear mask missing `cy` parameter (compose.py:_build_mask)

**Severity**: High — linear mask caused `UnboundLocalError`.

The expression `(Y/H-{cy})*{ny}` referenced `cy` but the variable was never extracted from the parameter dict.

**Fix**: Added `cy = params.get("cy", 0.5)`.

### 4. clip / speed commands dropped audio (volcengine/cli.py, editor/cli.py)

**Severity**: Medium — CLI convenience commands produced video-only output without warning.

The `clip` and `speed` commands created a single video track, silently discarding the original audio stream.

**Fix**: Added a second audio track with the same time range and speed factor.

### 5. Speed factor validation (volcengine/cli.py, editor/cli.py)

**Severity**: Low — speed=0 or negative would produce degenerate or broken ffmpeg graphs.

**Fix**: Changed `type=float` to `type=click.FloatRange(min=0.001)` on the `--factor` option, rejecting non-positive values at the CLI level.

### 6. Dead code: `editor/cli.py` not wired to CLI entry point

**Severity**: Low — the file exists but is never invoked through `ai edit *`.

The `pyproject.toml` entry point `ai = "volcengine.cli:cli"` routes `ai edit *` to `volcengine/cli.py`, which has its own copies of all edit commands. `editor/cli.py` has a duplicate `edit` group with no registration.

**Status**: Documented but left as-is. Both copies were patched with audio fixes for consistency.

## Limitations (Not Implemented)

These features exist in the data model (`models.py`) and manifest parser (`manifest.py`) but are **not consumed by the renderer** (`compose.py`):

| Feature | Data Model | Manifest Parser | Renderer | Impact |
|---------|-----------|-----------------|----------|--------|
| Keyframe animations (scale/position/rotation) | Segment.keyframes | `## Keyframes:` section parsed, attached to segment | **No** — `_build_video_segment` ignores keyframes | Segment renders at default 1.0 scale, center position, 0 rotation |
| Blend mode | Segment.blend | Parsed | **No** — line 172: `"Will be applied at overlay stage"` but no code | Blend mode is silently ignored |
| Opacity | Segment.opacity | Parsed | **No** — not applied | Always fully opaque |
| Adjustments (brightness/contrast/saturation/vignette) | Segment.adjustments | `## Adjustments:` section parsed | **No** | Adjustments are silently ignored |

To add keyframe support, `_build_video_segment` would need to:
1. Insert `split()` after trim/speed
2. Apply `geq` or `perspective`/`rotate` filters for each keyframe
3. Use `interpolate` or overlay chain for transitions

## Edge Cases Checked

- [x] Empty tracks -> `ValueError("Composition has no valid tracks to render")`
- [x] Missing asset files -> segment silently skipped
- [x] Single segment per track -> returned directly (no concat overhead)
- [x] Single input to concat -> works (concat demuxer handles 1 file)
- [x] speed=4.0 -> atempo chained as `atempo=2.0,atempo=2.0`
- [x] speed=0.25 -> atempo chained as `atempo=0.5,atempo=0.5`
- [x] mask feather=0 -> inner==outer, division is `(0.1156-0.0676)=0.048` not zero
- [x] subtitle with 3-char hex -> `#000` now expands to `&H000000&`

## Usage Notes

- Asset paths in manifests: absolute paths work; relative paths resolve from the manifest file's parent directory
- The `compose` command parses markdown and renders in one step
- The `clip`, `speed`, `concat`, `mute` commands are convenience shorthands that create Composition objects in-memory
- All rendered outputs use libx264 at CRF 18 unless overridden in the manifest's `## Output` section
