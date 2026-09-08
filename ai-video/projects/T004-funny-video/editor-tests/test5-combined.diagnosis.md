# Diagnosis: test5-combined.diagnosis

**Status**: `ERROR`
**Summary**: 1 error(s), 1 warning(s). Duration 3s (Δ=0.3s).

## Output

| Metric | Value |
|--------|-------|
| Duration | 3.0s (expected 3s, Δ=10.0%) |
| Streams | video |
| Video | 1920×1080 h264 |

## Issues

**1. [ERROR] timing_drift**
> Video 3s vs expected 3s (10.0% off)

**2. [WARNING] no_audio**
> No audio stream in output. Add an audio track to improve quality.
> **Fix**: Add track bgm with asset: assets/audio/bgm-lofi.mp3 (volume: 0.2)
