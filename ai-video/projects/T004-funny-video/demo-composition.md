# T004-demo-hook — 社交电量 Hook Demo

## Meta

| Meta | Value |
|------|-------|
| resolution | 720 x 1280 |
| fps | 24 |
| output | demo-hook.mp4 |

## Assets

| ID | Path | Type |
|----|------|------|
| clip-a | ../T003/output/T003-segment1-clipa.mp4 | video |
| clip-b | ../T003/output/T003-segment1-clipb.mp4 | video |

## Track: main

| ID | Asset | Source | At | Speed | Mask | Tags |
|----|-------|--------|----|-------|------|------|
| hook-1 | clip-a | 0.0–1.5 | 0.0 | 1.0 | — | chaos |
| hook-2 | clip-a | 3.0–4.0 | 1.5 | 1.0 | circle(0.5,0.5,0.4,feather=0.15) | interrupt |
| hook-3 | clip-b | 2.0–4.5 | 2.5 | 1.0 | — | reveal |
| hook-4 | clip-a | 5.0–7.0 | 5.0 | 0.8 | — | slow-mo |
| hook-5 | clip-b | 1.0–3.0 | 7.5 | 1.0 | — | title |
| blackout | clip-a | 14.0–14.5 | 9.5 | 1.0 | — | ending |

## Track: overlay-texture

| ID | Asset | Source | At | Blend | Opacity | Tags |
|----|-------|--------|----|-------|---------|------|
| grain | clip-a | 8.0–10.0 | 0.0 | overlay | 0.12 | texture |

## Track: bgm

| ID | Asset | Source | At | Volume | Fade In | Fade Out |
|----|-------|--------|----|--------|---------|----------|
| music | clip-a | 0.0–10.0 | 0.0 | 0.15 | 2.0 | 2.0 |

## Subtitles

| Start | End | Text | Font | Size | Outline | Position |
|-------|-----|------|------|------|---------|----------|
| 0.0 | 1.5 | 你有没有过这种感觉 | PingFang SC | 52 | 4,#000000 | bottom,120 |
| 1.5 | 2.5 | 你在一个挺好的派对里 | PingFang SC | 52 | 4,#000000 | bottom,120 |
| 2.5 | 5.0 | 但你突然发现 | PingFang SC | 56 | 4,#000000 | center |
| 5.5 | 7.5 | 你没办法再笑一下了 | PingFang SC | 48 | 4,#000000 | bottom,120 |
| 7.5 | 10.0 | 不是因为你不开心 | PingFang SC | 48 | 4,#000000 | bottom,120 |

## Keyframes: hook-3

| At | Scale | Position | Rotation | Easing |
|----|-------|----------|----------|--------|
| 0.0 | 1.0 | 0.5,0.5 | 0 | — |
| 1.5 | 1.12 | 0.5,0.48 | 0 | ease-in-out |
| 2.0 | 1.0 | 0.5,0.5 | 0 | ease-out |

## Output

| Format | Codec | Bitrate |
|--------|-------|---------|
| mp4 | libx264 | 6M |
