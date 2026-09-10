# 社交电量 — Composition Agent v1

> 90s teaser composition. Data-driven scene selection from 25 footage profiles.
> Emotional arc: party chaos → social drain → alone ≠ lonely → recharge.

## Meta

| Meta | Value |
|------|-------|
| Title | 社交电量 |
| Duration | 90.0s |
| Resolution | 1920 x 1080 |
| FPS | 30 |
| Sections | Hook (0-8s) · Body (8-45s) · Emotional Peak (45-70s) · Resolution (70-90s) |

## Assets

| ID | Path | Type |
|----|------|------|
| party-crowd | assets/footage/pexels-hook-party-crowd-01.mp4 | video |
| fake-smile | assets/footage/pexels-hook-fake-smile-01.mp4 | video |
| exhausted | assets/footage/pexels-hook-exhausted-person-01.mp4 | video |
| brain-scan | assets/footage/pexels-hook-brain-scan-01.mp4 | video |
| coconut | assets/footage/pexels-ch12-coconut-01.mp4 | video |
| hiit-workout | assets/footage/pexels-ch12-hiit-workout-01.mp4 | video |
| biz-meeting | assets/footage/pexels-ch12-business-meeting-01.mp4 | video |
| grocery-tired | assets/footage/pexels-ch12-grocery-tired-01.mp4 | video |
| check-watch | assets/footage/pexels-ch12-checking-watch-01.mp4 | video |
| thinking-calc | assets/footage/pexels-ch12-thinking-calculating-01.mp4 | video |
| phone-stress | assets/footage/pexels-ch12-phone-stress-01.mp4 | video |
| person-running | assets/footage/pexels-ch12-person-running-01.mp4 | video |
| rain-window | assets/footage/pexels-ch13-rain-window-01.mp4 | video |
| forest-path | assets/footage/pexels-ch13-forest-path-01.mp4 | video |
| genuine-smile | assets/footage/pexels-ch13-genuine-smile-01.mp4 | video |
| blanket-fort | assets/footage/pexels-ch14-blanket-fort-01.mp4 | video |
| headphones | assets/footage/pexels-ch14-headphones-music-01.mp4 | video |
| phone-charging | assets/footage/pexels-ch14-phone-charging-01.mp4 | video |

---

## Track: main

### Section 1 — Hook (0.0s–8.0s): 3 fast cuts, energetic-to-drain descent

| ID | Asset | Source | At | Speed | Mask | Tags |
|----|-------|--------|----|-------|------|------|
| seg-hook-01 | party-crowd | 0.0–1.5 | 0.0 | 1.0 | — | hook,contrast-boost |
| seg-hook-02 | party-crowd | 1.5–4.0 | 1.5 | 1.0 | — | hook,contrast-boost |
| seg-hook-03 | fake-smile | 0.0–2.5 | 4.0 | 1.0 | circle:0.5,0.45,0.25 | hook,mask,contrast-boost |
| seg-hook-04 | exhausted | 0.0–2.0 | 6.5 | 1.0 | — | hook,contrast-boost |

_Hook rationale: party-crowd scene1 (#572e1c warm-dark) establishes energy; scene2 (#3e1f13 deeper warm-dark) continues chaos. fake-smile (#41392e) with circle mask spotlights the "smile but eyes dead" beat from script (0:20-0:25). exhausted (#617170 cool-grey) lands the drain — transition to body._

### Section 2 — Body (8.0s–45.0s): varied pacing, Ch1-Ch2 narrative

| ID | Asset | Source | At | Speed | Mask | Tags |
|----|-------|--------|----|-------|------|------|
| seg-body-01 | brain-scan | 0.0–4.5 | 8.0 | 1.0 | — | body |
| seg-body-02 | coconut | 0.0–3.0 | 12.5 | 1.0 | — | body |
| seg-body-03 | hiit-workout | 0.0–4.0 | 15.5 | 1.0 | — | body |
| seg-body-04 | biz-meeting | 0.0–4.0 | 19.5 | 1.0 | — | body |
| seg-body-05 | grocery-tired | 0.0–2.5 | 23.5 | 1.0 | — | body |
| seg-body-06 | check-watch | 0.0–3.0 | 26.0 | 1.0 | — | body |
| seg-body-07 | thinking-calc | 0.0–3.5 | 29.0 | 1.0 | — | body |
| seg-body-08 | phone-stress | 0.0–3.0 | 32.5 | 1.0 | — | body |
| seg-body-09 | grocery-tired | 2.5–6.0 | 35.5 | 1.0 | — | body |
| seg-body-10 | person-running | 0.0–5.1 | 39.0 | 1.0 | — | body |

_Body rationale: brain-scan (#6f6964 cool-grey) opens "your brain is not an iPhone". coconut (#928d84 warm) lands the visual joke. hiit-workout (#2e2e2f very dark) drives "socializing is exercise". biz-meeting (#9aa1a5 cool-grey) and grocery-tired (#b08f76 warm-beige) show daily drain. checking-watch (#b2a6a0 warm-beige) starts "stage 2: when can I leave" script beat. thinking-calc (#93827a warm) and phone-stress (#96907e) escalate. person-running (#d8d8d8 grey, 5.1s full clip) closes body with escape — transition to emotional peak._

### Section 3 — Emotional Peak (45.0s–70.0s): slow, long takes

| ID | Asset | Source | At | Speed | Mask | Tags |
|----|-------|--------|----|-------|------|------|
| seg-emotion-01 | rain-window | 0.0–10.0 | 45.0 | 1.0 | — | emotional,vignette,keyframe-zoom |
| seg-emotion-02 | forest-path | 0.0–8.0 | 55.0 | 1.0 | — | emotional,vignette,keyframe-zoom |
| seg-emotion-03 | genuine-smile | 2.0–9.0 | 63.0 | 1.0 | circle:0.5,0.5,0.30 | emotional,mask,vignette |

_Emotional peak rationale: rain-window (#00165e deepest blue — cool/calm/sad) is the emotional turn — longest single take at 10s. forest-path (#898667 green-warm) is peaceful recovery. genuine-smile (#496b80 cool-blue) with circle mask spotlights the "eyes finally smiling for real" moment from script 8:00-8:15. genuine-smile uses source 2.0-9.0 to skip initial setup and capture the warmest expressions._

### Section 4 — Resolution (70.0s–90.0s): warm/cozy ending

| ID | Asset | Source | At | Speed | Mask | Tags |
|----|-------|--------|----|-------|------|------|
| seg-res-01 | blanket-fort | 0.0–8.0 | 70.0 | 1.0 | — | resolution |
| seg-res-02 | headphones | 0.0–6.0 | 78.0 | 1.0 | — | resolution |
| seg-res-03 | phone-charging | 0.0–6.0 | 84.0 | 1.0 | — | resolution |

_Resolution rationale: blanket-fort (#234856 cool-dark cozy) — long take for decompression. headphones (#354c54 cool-dark) — the recharge ritual. phone-charging (#8b6949 warm-brown) closes on the battery metaphor from script ending._

---

## Subtitles

Subtitles drawn from script-beats.md VO lines, mapped to visual sections.

| Start | End | Text | Font | Size | Outline | Position |
|-------|-----|------|------|------|---------|----------|
| 0.0 | 2.5 | 你有没有过这种感觉—— | PingFang SC | 54 | 3,#000000 | bottom,120 |
| 4.0 | 6.5 | 你在一个挺好的派对里 | PingFang SC | 54 | 3,#000000 | bottom,120 |
| 6.5 | 8.0 | 但你意识到——你的脸不合作了 | PingFang SC | 52 | 3,#000000 | bottom,120 |
| 8.0 | 12.5 | 你的大脑不是iPhone. 你没有右上角那个百分比. | PingFang SC | 48 | 3,#000000 | bottom,120 |
| 12.5 | 15.5 | （虽然有人试过.） | PingFang SC | 46 | 3,#000000 | bottom,120 |
| 15.5 | 19.5 | 社交对你来说——是运动 | PingFang SC | 52 | 3,#000000 | bottom,120 |
| 19.5 | 23.5 | 开完一个会你需要两小时独处 | PingFang SC | 50 | 3,#000000 | bottom,120 |
| 23.5 | 26.0 | 阶段一：我还行 | PingFang SC | 56 | 4,#000000 | bottom,120 |
| 26.0 | 29.0 | 阶段二：什么时候能走 | PingFang SC | 56 | 4,#000000 | bottom,120 |
| 29.0 | 32.5 | 阶段三：完蛋，我该说点什么 | PingFang SC | 56 | 4,#000000 | bottom,120 |
| 32.5 | 35.5 | 阶段四：1% | PingFang SC | 56 | 4,#FF0000 | bottom,120 |
| 35.5 | 39.0 | 阶段五：逃 | PingFang SC | 56 | 4,#000000 | bottom,120 |
| 39.0 | 45.0 | 然后你站在那里——深呼吸. 世界安静了. | PingFang SC | 48 | 3,#000000 | bottom,120 |
| 45.0 | 55.0 | 我们花了太多时间, 觉得「一个人」是问题 | PingFang SC | 48 | 3,#000000 | bottom,120 |
| 55.0 | 63.0 | 你是一个正常的、需要独处来恢复的人 | PingFang SC | 48 | 3,#000000 | bottom,120 |
| 63.0 | 70.0 | 你不是「怕人」——这是品质, 不是缺陷 | PingFang SC | 48 | 3,#000000 | bottom,120 |
| 70.0 | 78.0 | 承认你需要充电——不是累, 是自我关怀 | PingFang SC | 48 | 3,#000000 | bottom,120 |
| 78.0 | 84.0 | 学会拒绝. 关机. 这不是失礼, 是电池管理. | PingFang SC | 48 | 3,#000000 | bottom,120 |
| 84.0 | 90.0 | 轮到跟你自己待一会儿了. | PingFang SC | 50 | 3,#000000 | bottom,120 |

---

## Keyframes

### seg-emotion-01 (rain-window: 45.0s–55.0s) — Slow zoom into rain

| At | Scale | Position | Rotation | Easing |
|----|-------|----------|----------|--------|
| 0.0 | 1.00 | 0.5,0.5 | 0 | — |
| 10.0 | 1.12 | 0.5,0.48 | 0 | ease-in-out |

_Purpose: gentle magnification draws viewer into introspective mood. Rain drops become more visible as zoom progresses. 10s ease-in-out feels organic._

### seg-emotion-02 (forest-path: 55.0s–63.0s) — Slow zoom into sunlight

| At | Scale | Position | Rotation | Easing |
|----|-------|----------|----------|--------|
| 0.0 | 1.00 | 0.5,0.5 | 0 | — |
| 8.0 | 1.08 | 0.5,0.47 | 0 | ease-in-out |

_Purpose: slow push toward the sunlit path. Complements "you're not broken" VO — opens up the frame metaphorically._

### seg-emotion-03 (genuine-smile: 63.0s–70.0s) — Subtle push into smile

| At | Scale | Position | Rotation | Easing |
|----|-------|----------|----------|--------|
| 0.0 | 1.00 | 0.5,0.5 | 0 | — |
| 7.0 | 1.06 | 0.5,0.48 | 0 | ease-in-out |

_Purpose: barely perceptible push into the genuine smile to amplify emotional weight of "this is quality, not defect" line._

### seg-res-01 (blanket-fort: 70.0s–78.0s) — Subtle pull-back to show space

| At | Scale | Position | Rotation | Easing |
|----|-------|----------|----------|--------|
| 0.0 | 1.05 | 0.5,0.5 | 0 | — |
| 8.0 | 1.00 | 0.5,0.5 | 0 | ease-in-out |

_Purpose: reverse zoom (pull out) to reveal the cozy fort space — "you need to recharge" feels like expanding comfort._

---

## Adjustments

### Hook segments (tags: contrast-boost)

| ID | Brightness | Contrast | Saturation | Vignette |
|----|------------|----------|------------|----------|
| seg-hook-01 | 0.00 | 1.15 | 1.05 | 0.0 |
| seg-hook-02 | 0.00 | 1.15 | 1.05 | 0.0 |
| seg-hook-03 | 0.02 | 1.12 | 1.00 | 0.10 |
| seg-hook-04 | -0.03 | 1.10 | 0.95 | 0.0 |

_Rationale: boosted contrast (+0.15) for punchy hook. fake-smile (seg-hook-03) gets slight vignette to frame the mask circle. exhausted (seg-hook-04) slight underexpose to sell the drained feeling._

### Emotional peak segments (tags: vignette)

| ID | Brightness | Contrast | Saturation | Vignette |
|----|------------|----------|------------|----------|
| seg-emotion-01 | -0.02 | 0.95 | 1.00 | 0.25 |
| seg-emotion-02 | 0.02 | 0.95 | 1.00 | 0.20 |
| seg-emotion-03 | 0.03 | 0.98 | 1.02 | 0.15 |

_Rationale: vignette darkens edges to focus attention center-frame. Slight desaturation (0.95 contrast) pulls back from body's high energy. brightness nudges up for forest-path (hopeful) and smile (warm)._

### Resolution segments (tags: resolution)

| ID | Brightness | Contrast | Saturation | Vignette |
|----|------------|----------|------------|----------|
| seg-res-01 | 0.02 | 0.98 | 1.00 | 0.10 |
| seg-res-02 | 0.00 | 1.00 | 1.00 | 0.0 |
| seg-res-03 | 0.03 | 1.00 | 1.05 | 0.0 |

_Rationale: blanket-fort slight warmth and vignette to keep cozy intimate. phone-charging slight brightness and saturation — closes on a positive, warm note._

### Body segments (default)

| ID | Brightness | Contrast | Saturation | Vignette |
|----|------------|----------|------------|----------|
| seg-body-01 | 0.00 | 1.00 | 1.00 | 0.0 |
| seg-body-02 | 0.00 | 1.00 | 1.00 | 0.0 |
| seg-body-03 | 0.00 | 1.00 | 1.00 | 0.0 |
| seg-body-04 | 0.00 | 1.00 | 1.00 | 0.0 |
| seg-body-05 | 0.00 | 1.00 | 1.00 | 0.0 |
| seg-body-06 | 0.00 | 1.00 | 1.00 | 0.0 |
| seg-body-07 | 0.00 | 1.00 | 1.00 | 0.0 |
| seg-body-08 | 0.00 | 1.00 | 1.00 | 0.0 |
| seg-body-09 | 0.00 | 1.00 | 1.00 | 0.0 |
| seg-body-10 | 0.00 | 1.00 | 1.00 | 0.0 |

---

## Section Summary

| Section | Time | Duration | Cuts | Avg Cut | Mood | Key Profile Colors Used |
|---------|------|----------|------|---------|------|------------------------|
| Hook | 0.0-8.0s | 8.0s | 4 | 2.0s | chaotic→draining | #572e1c · #3e1f13 · #41392e · #617170 |
| Body | 8.0-45.0s | 37.0s | 10 | 3.7s | varied→escalating | #6f6964 · #928d84 · #2e2e2f · #9aa1a5 · #b08f76 · #b2a6a0 · #93827a · #96907e · #d8d8d8 |
| Emotional Peak | 45.0-70.0s | 25.0s | 3 | 8.3s | reflective→warm | #00165e · #898667 · #496b80 |
| Resolution | 70.0-90.0s | 20.0s | 3 | 6.7s | cozy→hopeful | #234856 · #354c54 · #8b6949 |

## Masks Applied

| Segment | Time | Type | Center | Radius | Purpose |
|---------|------|------|--------|--------|---------|
| seg-hook-03 | 4.0-6.5s | circle | 0.5,0.45 | 0.25 | Spotlight fake smile face — "你还在笑, 但眼睛已走" |
| seg-emotion-03 | 63.0-70.0s | circle | 0.5,0.5 | 0.30 | Spotlight genuine smile — "这是品质, 不是缺陷" |

## Keyframe Animations Applied

| Segment | Time | Type | From→To | Easing |
|---------|------|------|---------|--------|
| seg-emotion-01 | 45.0-55.0s | slow zoom in | 1.00→1.12 | ease-in-out |
| seg-emotion-02 | 55.0-63.0s | slow zoom in | 1.00→1.08 | ease-in-out |
| seg-emotion-03 | 63.0-70.0s | subtle zoom in | 1.00→1.06 | ease-in-out |
| seg-res-01 | 70.0-78.0s | slow pull out | 1.05→1.00 | ease-in-out |

## Color Adjustments Applied

| Group | Contrast | Vignette | Brightness | Mood |
|-------|----------|----------|------------|------|
| Hook (contrast-boost) | +0.15 | — | — | punchy, high-energy |
| Emotional Peak (vignette) | -0.05 | 0.20-0.25 | -0.02~+0.03 | intimate, focused |

## Output

| Format | Codec | Bitrate | Resolution |
|--------|-------|---------|------------|
| mp4 | libx264 | 8M | 1920x1080 |

---

_Generated from 25 profile.md files. See `assets/footage/_manifest.md` for master asset list and `script-beats.md` for narrative arc reference._
