# Editor Feature Verification Report

**Date:** 2026-07-28
**Environment:** ffmpeg 4.4.2, Python 3.10+, Ubuntu 22.04
**Editor Module:** `scripts/src/editor/compose.py`
**Test Footage:** `ai-video/projects/T004-funny-video/assets/footage/`

## Summary

| Test | Status | Output File | Size | Duration |
|------|--------|-------------|------|----------|
| 1. Mask rendering (circle + linear) | PASS | test1-mask.mp4 | 2.3 MB | 6.54s |
| 2. Keyframe animation (scale 1.0->1.15 ease-in-out) | PASS | test2-keyframe.mp4 | 3.5 MB | 3.50s |
| 3. Blend mode overlay (multiply) | PASS | test3-blend.mp4 | 1.7 MB | 3.00s |
| 4. Color adjustments (brightness/contrast/saturation/vignette) | PASS | test4-color.mp4 | 2.8 MB | 3.00s |
| 5. All features combined (mask+keyframes+color+speed 0.9) | PASS | test5-combined.mp4 | 1.9 MB | 3.32s |
| 6. Multi-track composition (main + overlay with blend) | PASS | test6-multitrack.mp4 | 4.6 MB | 4.52s |
| 7. Timeline gaps (3s blank between clips) | PASS | test7-gaps.mp4 | 3.6 MB | 7.04s |
| 8. Audio track integration (aac codec + verify stream) | PASS | test8-audio.mp4 | 3.3 MB | 3.00s |

**All 8 tests PASSED.** All outputs are 1920x1080 video with valid codec streams.

## Bugs Found and Fixed

### Bug 1: `_probe()` uses `ffmpeg` instead of `ffprobe`
- **File:** `compose.py:32-37`
- **Description:** The `_probe()` function invoked `ffmpeg -show_entries ...`, but `-show_entries` is an `ffprobe`-only option. This caused the function to always return `{}` silently.
- **Fix:** Changed `_FFMPEG` to `_FFPROBE` and added `_FFPROBE` as a configurable binary (via `FFPROBE_BINARY` env var).

### Bug 2: Linear mask expression uses invalid syntax
- **File:** `compose.py:428-432` (original)
- **Description:** The linear mask GEQ expression used `pow({w}-{cx})` which is invalid — `pow()` in ffmpeg takes two arguments, but only one was provided. The `X/` prefix was accidentally dropped, making it `pow(W-cx)` instead of `(X/W-cx)`.
- **Fix:** Changed all three occurrences from `pow({w}-{cx})` to `(X/{w}-{cx})` to match the circle mask convention.

### Bug 3: Keyframe "all identical" check skips implicit first segment
- **File:** `compose.py:506` (original)
- **Description:** When all keyframes shared the same value (`len(set(vals)) == 1`), the function returned a constant, skipping the implicit-first-segment interpolation from `t=0` to the first keyframe. A single keyframe at `t=3, scale=1.15` would return constant `1.15` instead of animating from `1.0` to `1.15`.
- **Fix:** Changed the check to `all(v == default for v in vals)` — only return early when all keyframe values equal the default (i.e., no animation needed).

### Bug 4: Geq `a=` option unsupported in ffmpeg 4.4; alphamerge approach unworkable
- **File:** `compose.py:236-239` (original)
- **Description:** The original implementation used `geq=a=expr` followed by `alphamerge` to apply masks. Two issues:
  - `geq` in ffmpeg 4.4 does not support the `alpha`/`a` option (added in later versions).
  - `libx264` in mp4 containers does not support alpha channels anyway.
- **Fix:** Replaced the entire mask approach. Instead of `geq=a=...+alphamerge`, use `geq` to zero out pixel values outside the mask (Y=0, Cb=128, Cr=128). This produces visible black masked areas in any codec.

### Bug 5: ffmpeg 4.4 heap corruption with `scale(eval=frame)` + `geq` in same filter chain
- **File:** `compose.py:334-372` 
- **Description:** When keyframe animation (using `scale=...:eval=frame`) and mask (using `geq`) are applied in the same ffmpeg filter chain, ffmpeg 4.4 crashes with "corrupted double-linked list" (SIGABRT, heap corruption). Known ffmpeg bug triggered by combining frame-level expression evaluation with per-pixel GEQ evaluation.
- **Fix:** Two-pass workaround: when both scale-keyframe animation and mask are present on a segment, render the segment in two passes — first all filters except the mask GEQ, then apply the mask GEQ on the intermediate output.

### Bug 6: GEQ per-pixel filter timeout
- **File:** `compose.py:348,356,374` (renamed)
- **Description:** The `geq` filter evaluates per-pixel-per-frame, making it extremely slow on 1920x1080 footage. The default 60-second timeout was insufficient for complex masks with feathering.
- **Fix:** Increased all GEQ-related timeouts from 60s to 180s.

## Architecture Notes

### Filter Chain Order
The segment-level video filter chain is assembled in this order:
1. Scale + crop to target resolution
2. Color adjustments (`eq`, `vignette`)
3. Speed/PTS (`setpts`)
4. Keyframe animation (`scale=...:eval=frame`)
5. Opacity (`format=rgba,colorchannelmixer=aa`, only without mask)
6. Mask (`geq` zeroing out pixels outside mask region)

### Mask Implementation
Masks use a `geq` filter that compares each pixel's normalized position against a mask expression:
- **Circle:** `if(lt(pow(X/W-cx,2)+pow(Y/H-cy,2), radius^2), pass_through, black)`
- **Linear:** `if(lt(abs((X/W-cx)*nx+(Y/H-cy)*ny), feather), gradient, half-plane)`
- Optional feather creates smooth transition at mask boundary.

### Keyframe Expression Engine
Keyframes are compiled into nested `if(lte(t, timestamp), lerp, ...)` ffmpeg expressions supporting:
- `linear`, `ease-in`, `ease-out`, `ease-in-out` easing functions
- Scale (via `scale=iw*(expr):ih*(expr):eval=frame`)
- Rotation (via `rotate=(expr)*PI/180`)

### Two-Pass Workaround (ffmpeg 4.4)
When both keyframe scale animation and mask are on the same segment, rendering is split:
- Pass 1: Render segment without mask GEQ filter
- Pass 2: Apply mask GEQ on intermediate output
- Only activates when `seg.keyframes` has at least one `scale != 1.0` AND `seg.mask` is non-empty

## Output Files

All test outputs located at:
`/home/aifeier/org-dev/bip/outgiving/ai-video/projects/T004-funny-video/editor-tests/`
