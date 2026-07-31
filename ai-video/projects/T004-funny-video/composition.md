# Composition: 社交电量

Markdown manifest for the video editor.
All timestamps in seconds | 16:9 (1920x1080) | 30 fps

---

## Meta

- duration: 630
- width: 1920
- height: 1080
- fps: 30
- bg_color: "#000000"
- output: ./output/social-battery.mp4
- crf: 18
- preset: medium

---

## Assets

### video

- id: party-crowd
  src: assets/footage/pexels-party-crowd-01.mp4
- id: party-laughter
  src: assets/footage/pexels-party-laughter-01.mp4
- id: party-montage
  src: assets/footage/pexels-party-montage-01.mp4
- id: person-exhausted
  src: assets/footage/pexels-person-tired-01.mp4
- id: smile-dead-eyes
  src: assets/footage/pexels-fake-smile-01.mp4
- id: brain-mri
  src: assets/footage/pexels-brain-scan-01.mp4
- id: coconut-charger
  src: assets/footage/pexels-coconut-01.mp4
- id: family-dinner
  src: assets/footage/pexels-family-dinner-01.mp4
- id: gym-workout
  src: assets/footage/pexels-gym-01.mp4
- id: meeting-tired
  src: assets/footage/pexels-meeting-tired-01.mp4
- id: phone-call
  src: assets/footage/pexels-phone-call-01.mp4
- id: grocery-store
  src: assets/footage/pexels-grocery-01.mp4
- id: crowded-subway
  src: assets/footage/pexels-subway-01.mp4
- id: hiit-exercise
  src: assets/footage/pexels-hiit-01.mp4
- id: watch-checking
  src: assets/footage/pexels-watch-01.mp4
- id: person-calculating
  src: assets/footage/pexels-thinking-01.mp4
- id: eight-people
  src: assets/footage/pexels-group-conversation-01.mp4
- id: running-out
  src: assets/footage/pexels-running-01.mp4
- id: window-rain
  src: assets/footage/pexels-rain-window-01.mp4
- id: cafe-reading
  src: assets/footage/pexels-cafe-reading-01.mp4
- id: forest-path
  src: assets/footage/pexels-forest-path-01.mp4
- id: journal-writing
  src: assets/footage/pexels-journal-01.mp4
- id: cat-sleeping
  src: assets/footage/pexels-cat-sleep-01.mp4
- id: genuine-smile
  src: assets/footage/pexels-genuine-smile-01.mp4
- id: night-city
  src: assets/footage/pexels-night-city-01.mp4
- id: phone-charging
  src: assets/footage/pexels-phone-charge-01.mp4
- id: headphones
  src: assets/footage/pexels-headphones-01.mp4
- id: blanket-fort
  src: assets/footage/pexels-blanket-01.mp4
- id: phone-notification
  src: assets/footage/pexels-phone-notification-01.mp4
- id: cat-box
  src: assets/footage/pexels-cat-box-01.mp4
- id: coffee-two
  src: assets/footage/pexels-coffee-two-01.mp4
- id: do-not-disturb
  src: assets/footage/pexels-phone-dnd-01.mp4
- id: sleeping
  src: assets/footage/pexels-sleeping-01.mp4
- id: cozy-home
  src: assets/footage/pexels-cozy-home-01.mp4
- id: home-pan
  src: assets/footage/pexels-home-pan-01.mp4
- id: kafka-photo
  src: assets/footage/publicdomain-kafka-01.mp4
- id: hands-warm-drink
  src: assets/footage/pexels-warm-drink-01.mp4

### texture

- id: film-grain
  src: assets/footage/texture-film-grain.mp4
- id: light-leak
  src: assets/footage/texture-light-leak.mp4
- id: paper-texture
  src: assets/footage/texture-paper.mp4

### animation

- id: anim-title-card
  src: assets/animation/title-card.mp4
- id: anim-battery-drain
  src: assets/animation/battery-drain.mp4
- id: anim-brain-glow
  src: assets/animation/brain-glow.mp4
- id: anim-battery-compare
  src: assets/animation/battery-compare.mp4
- id: anim-spoontheory
  src: assets/animation/spoon-theory.mp4
- id: anim-stage-titles
  src: assets/animation/stage-titles.mp4
- id: anim-thought-bubble
  src: assets/animation/thought-bubble.mp4
- id: anim-game-ui
  src: assets/animation/game-ui-overlay.mp4
- id: anim-charge-complete
  src: assets/animation/charge-complete.mp4
- id: anim-ending-card
  src: assets/animation/ending-card.mp4
- id: anim-notifications
  src: assets/animation/notification-stack.mp4

### audio

- id: bgm-main
  src: assets/audio/bgm-lofi-main.mp3
- id: bgm-chapter3
  src: assets/audio/bgm-ambient-piano.mp3
- id: bgm-outro
  src: assets/audio/bgm-acoustic-outro.mp3
- id: vo-recording
  src: assets/audio/vo-recording.mp3
- id: sfx-bundle
  src: assets/audio/sfx-bundle.mp3

### font

- id: font-noto-sc
  src: assets/fonts/NotoSansSC-Regular.otf
- id: font-noto-sc-bold
  src: assets/fonts/NotoSansSC-Bold.otf

---

## Track: Main Video

order: 0
type: video
blend_mode: normal

segments:

  ### Hook (0:00-0:35)

  - asset: party-crowd
    start: 0.0
    end: 3.0
    speed: 0.8
    transform:
      scale: [1.0, 1.0]
    effects:
      color: { saturation: 1.15, contrast: 1.2 }

  - asset: party-laughter
    start: 3.0
    end: 5.0
    speed: 1.0
    effects:
      color: { saturation: 1.1 }

  - asset: party-montage
    start: 5.0
    end: 8.0
    speed: 1.5

  - asset: person-exhausted
    start: 8.0
    end: 13.0
    speed: 0.5
    effects:
      color: { saturation: 0.7, brightness: -0.1 }

  - asset: party-montage
    start: 13.0
    end: 20.0
    speed: 2.0
    effects:
      color: { saturation: 1.2, contrast: 1.1 }

  - asset: smile-dead-eyes
    start: 20.0
    end: 25.0
    speed: 0.6
    effects:
      color: { saturation: 0.5, brightness: -0.15 }
      vignette: { strength: 0.5 }

  - asset: anim-title-card
    start: 25.0
    end: 30.0
    speed: 1.0
    transform:
      scale: [1.0, 1.0]

  - asset: brain-mri
    start: 30.0
    end: 36.0
    speed: 1.0

  ### Chapter 1: 你的大脑不是手机 (0:35-3:00)

  - asset: brain-mri
    start: 36.0
    end: 44.0
    speed: 0.8
    effects:
      color: { saturation: 1.1 }

  - asset: coconut-charger
    start: 44.0
    end: 50.0
    speed: 1.0

  - asset: brain-mri
    start: 50.0
    end: 53.0
    speed: 1.0

  - asset: family-dinner
    start: 53.0
    end: 58.0
    speed: 1.0

  - asset: brain-mri
    start: 58.0
    end: 64.0
    speed: 1.0

  - asset: hiit-exercise
    start: 64.0
    end: 70.0
    speed: 0.9

  - asset: gym-workout
    start: 70.0
    end: 78.0
    speed: 1.0

  - asset: meeting-tired
    start: 78.0
    end: 82.0
    speed: 0.7
    effects:
      color: { saturation: 0.6 }

  - asset: phone-call
    start: 82.0
    end: 85.0
    speed: 0.8

  - asset: grocery-store
    start: 85.0
    end: 89.0
    speed: 1.0

  - asset: crowded-subway
    start: 89.0
    end: 92.0
    speed: 0.8
    effects:
      color: { saturation: 0.3 }

  - asset: phone-call
    start: 92.0
    end: 95.0
    speed: 1.0

  - asset: anim-battery-compare
    start: 95.0
    end: 105.0
    speed: 1.0

  - asset: anim-battery-drain
    start: 105.0
    end: 113.0
    speed: 1.2

  - asset: anim-brain-glow
    start: 113.0
    end: 120.0
    speed: 1.0

  ### Chapter 2: 五个阶段 (3:00-6:00)

  - asset: anim-stage-titles
    start: 120.0
    end: 123.0
    speed: 1.0

  - asset: party-crowd
    start: 123.0
    end: 131.0
    speed: 1.0

  - asset: smile-dead-eyes
    start: 131.0
    end: 137.0
    speed: 0.7

  - asset: anim-stage-titles
    start: 137.0
    end: 140.0
    speed: 1.0

  - asset: watch-checking
    start: 140.0
    end: 148.0
    speed: 1.0
    effects:
      color: { saturation: 1.2 }

  - asset: person-calculating
    start: 148.0
    end: 154.0
    speed: 1.0

  - asset: anim-game-ui
    start: 154.0
    end: 159.0
    speed: 1.0

  - asset: anim-stage-titles
    start: 159.0
    end: 162.0
    speed: 1.0

  - asset: eight-people
    start: 162.0
    end: 170.0
    speed: 0.6

  - asset: anim-thought-bubble
    start: 170.0
    end: 175.0
    speed: 1.0

  - asset: eight-people
    start: 175.0
    end: 180.0
    speed: 1.0

  - asset: anim-stage-titles
    start: 180.0
    end: 183.0
    speed: 1.0

  - asset: smile-dead-eyes
    start: 183.0
    end: 190.0
    speed: 0.5
    effects:
      color: { saturation: 0.4, brightness: -0.2 }

  - asset: person-exhausted
    start: 190.0
    end: 195.0
    speed: 0.8
    effects:
      color: { saturation: 0.5 }

  - asset: anim-stage-titles
    start: 195.0
    end: 198.0
    speed: 1.0

  - asset: running-out
    start: 198.0
    end: 206.0
    speed: 0.9

  - asset: person-exhausted
    start: 206.0
    end: 214.0
    speed: 0.4
    effects:
      color: { saturation: 0.7, brightness: 0.05 }

  - asset: window-rain
    start: 214.0
    end: 220.0
    speed: 0.6

  - asset: anim-battery-drain
    start: 220.0
    end: 226.0
    speed: 1.0

  ### Chapter 3: 一个人不等于孤独 (6:00-8:30)

  - asset: window-rain
    start: 226.0
    end: 238.0
    speed: 0.5
    effects:
      color: { saturation: 0.8, temperature: 0.15 }

  - asset: cafe-reading
    start: 238.0
    end: 248.0
    speed: 0.7
    effects:
      color: { saturation: 0.9, temperature: 0.1 }

  - asset: cafe-reading
    start: 248.0
    end: 256.0
    speed: 0.6
    transform:
      scale: [1.02, 1.02]

  - asset: forest-path
    start: 256.0
    end: 266.0
    speed: 0.6
    effects:
      color: { saturation: 0.8, contrast: 0.9 }

  - asset: anim-brain-glow
    start: 266.0
    end: 272.0
    speed: 0.8

  - asset: kafka-photo
    start: 272.0
    end: 278.0
    speed: 0.5
    effects:
      color: { saturation: 0.3, contrast: 1.2 }

  - asset: forest-path
    start: 278.0
    end: 284.0
    speed: 0.7

  - asset: journal-writing
    start: 284.0
    end: 294.0
    speed: 0.6
    effects:
      color: { temperature: 0.15 }

  - asset: cat-sleeping
    start: 294.0
    end: 302.0
    speed: 0.6

  - asset: genuine-smile
    start: 302.0
    end: 312.0
    speed: 0.5
    effects:
      color: { saturation: 1.0, contrast: 1.0 }

  - asset: night-city
    start: 312.0
    end: 320.0
    speed: 0.5

  - asset: night-city
    start: 320.0
    end: 328.0
    speed: 0.4
    transform:
      scale: [1.03, 1.03]

  - asset: hands-warm-drink
    start: 328.0
    end: 333.0
    speed: 0.6

  ### Chapter 4: 充电手册 (8:30-9:45)

  - asset: phone-charging
    start: 333.0
    end: 339.0
    speed: 1.0

  - asset: headphones
    start: 339.0
    end: 347.0
    speed: 0.8

  - asset: blanket-fort
    start: 347.0
    end: 353.0
    speed: 0.8

  - asset: phone-notification
    start: 353.0
    end: 359.0
    speed: 1.0

  - asset: cat-box
    start: 359.0
    end: 364.0
    speed: 0.8

  - asset: coffee-two
    start: 364.0
    end: 371.0
    speed: 1.0

  - asset: do-not-disturb
    start: 371.0
    end: 377.0
    speed: 1.0

  - asset: sleeping
    start: 377.0
    end: 383.0
    speed: 0.7

  - asset: anim-charge-complete
    start: 383.0
    end: 393.0
    speed: 1.0

  - asset: meeting-tired
    start: 393.0
    end: 396.0
    speed: 1.5

  ### Ending (9:45-10:30)

  - asset: cozy-home
    start: 396.0
    end: 404.0
    speed: 0.6
    effects:
      color: { temperature: 0.15 }

  - asset: home-pan
    start: 404.0
    end: 414.0
    speed: 0.5

  - asset: genuine-smile
    start: 414.0
    end: 422.0
    speed: 0.4

  - asset: anim-ending-card
    start: 422.0
    end: 434.0
    speed: 1.0

---

## Track: Texture Overlay

order: 1
type: video
blend_mode: overlay
opacity: 0.12

segments:

  - asset: film-grain
    start: 0.0
    end: 220.0
    speed: 1.0

  - asset: paper-texture
    start: 220.0
    end: 333.0
    speed: 1.0
    blend_mode: soft_light
    opacity: 0.08

  - asset: film-grain
    start: 333.0
    end: 434.0
    speed: 1.0

---

## Track: Light Leak Overlay

order: 2
type: video
blend_mode: screen
opacity: 0.25

segments:

  - asset: light-leak
    start: 20.0
    end: 25.0
    speed: 0.8

  - asset: light-leak
    start: 214.0
    end: 226.0
    speed: 0.5
    opacity: 0.15

  - asset: light-leak
    start: 396.0
    end: 414.0
    speed: 0.6
    opacity: 0.2

---

## Track: UI Animation Overlay

order: 3
type: video
blend_mode: screen

segments:

  - asset: anim-battery-drain
    start: 105.0
    end: 110.0
    speed: 1.0
    transform:
      position: [600, -400]
      scale: [0.5, 0.5]

  - asset: anim-game-ui
    start: 154.0
    end: 159.0
    speed: 1.0
    transform:
      scale: [0.7, 0.7]

  - asset: anim-thought-bubble
    start: 170.0
    end: 175.0
    speed: 1.0
    transform:
      position: [0, -200]
      scale: [0.6, 0.6]

  - asset: anim-notifications
    start: 353.0
    end: 359.0
    speed: 1.0
    transform:
      position: [500, 200]
      scale: [0.8, 0.8]

  - asset: anim-charge-complete
    start: 383.0
    end: 393.0
    speed: 1.0
    transform:
      position: [600, -400]
      scale: [0.4, 0.4]

---

## Track: BGM

order: 0
type: audio
segments:

  - asset: bgm-main
    start: 0.0
    end: 226.0
    volume: 0.35
    envelope:
      - time: 0.0, volume: 0.0
      - time: 3.0, volume: 0.35
      - time: 20.0, volume: 0.25
      - time: 25.0, volume: 0.0
      - time: 30.0, volume: 0.35
      - time: 120.0, volume: 0.40
      - time: 214.0, volume: 0.30
      - time: 224.0, volume: 0.10

  - asset: bgm-chapter3
    start: 226.0
    end: 333.0
    volume: 0.30
    envelope:
      - time: 226.0, volume: 0.0
      - time: 232.0, volume: 0.30
      - time: 312.0, volume: 0.25
      - time: 328.0, volume: 0.15

  - asset: bgm-main
    start: 333.0
    end: 396.0
    volume: 0.35
    envelope:
      - time: 333.0, volume: 0.0
      - time: 339.0, volume: 0.35
      - time: 380.0, volume: 0.30

  - asset: bgm-outro
    start: 396.0
    end: 434.0
    volume: 0.30
    envelope:
      - time: 396.0, volume: 0.0
      - time: 402.0, volume: 0.30
      - time: 425.0, volume: 0.20
      - time: 432.0, volume: 0.0

---

## Track: SFX

order: 1
type: audio
segments:

  - asset: sfx-bundle
    start: 0.0
    end: 0.5
    volume: 0.0

  ### Pattern: key moments have specific SFX triggers
  ### SFX cues (embedded in sfx-bundle.mp3):
  ###   0.0-1.0:  crowd ambience (loop)
  ###   5.0:      cut/glitch sound
  ###   25.0:     title slam
  ###   44.0:     pop (coconut)
  ###   120.0-195.0: stage transition whooshes ×5
  ###   170.0:    wind / tumbleweed
  ###   198.0:    door slam
  ###   206.0:    deep breath exhale
  ###   312.0:    music resolve chord
  ###   359.0:    cat purr
  ###   422.0:    charge-up sound

---

## Track: Voiceover

order: 2
type: audio
segments:

  - asset: vo-recording
    start: 0.0
    end: 434.0
    volume: 1.0
    envelope:
      - time: 0.0, volume: 0.0
      - time: 10.0, volume: 1.0
      - time: 430.0, volume: 1.0
      - time: 434.0, volume: 0.0

---

## Masks

- id: circle-spotlight-s05
  type: circle
  target: smile-dead-eyes
  timeline: [20.0, 25.0]
  params:
    cx: 0.5
    cy: 0.45
    radius: 0.28
    feather: 0.06

- id: circle-spotlight-s34
  type: circle
  target: eight-people
  timeline: [162.0, 170.0]
  params:
    cx: 0.5
    cy: 0.5
    radius: 0.25
    feather: 0.08

- id: circle-spotlight-s51
  type: circle
  target: genuine-smile
  timeline: [302.0, 312.0]
  params:
    cx: 0.5
    cy: 0.45
    radius: 0.3
    feather: 0.1

- id: linear-wipe-ch1
  type: linear
  target: anim-brain-glow
  timeline: [113.0, 120.0]
  params:
    x0: 0.0, y0: 1.0
    x1: 0.0, y1: 0.0
    feather: 0.15

- id: linear-wipe-ch3
  type: linear
  target: forest-path
  timeline: [256.0, 266.0]
  params:
    x0: 0.0, y0: 1.0
    x1: 0.0, y1: 0.0
    feather: 0.2

- id: linear-wipe-ending
  type: linear
  target: home-pan
  timeline: [404.0, 414.0]
  params:
    x0: 0.0, y0: 1.0
    x1: 1.0, y1: 0.0
    feather: 0.1

---

## Subtitles

### Key subtitle entries (full transcript in VO script)

- start: 10.0
  end: 14.0
  text: "你有没有过这种感觉——"
  style: subtitle-main

- start: 14.0
  end: 20.0
  text: "你在一个挺好的派对里。"
  style: subtitle-main

- start: 22.0
  end: 25.0
  text: "但你突然意识到——你没办法再笑一下了。"
  style: subtitle-main

- start: 28.0
  end: 30.0
  text: "社交电量"
  style: subtitle-title

- start: 32.0
  end: 35.0
  text: "今天我们来聊聊，你大脑里那块神秘的社交电池。"
  style: subtitle-main

- start: 36.0
  end: 44.0
  text: "首先，一个坏消息：你的大脑不是iPhone。"
  style: subtitle-main

- start: 50.0
  end: 53.0
  text: "这块叫前额叶皮层。你的社交过滤器。"
  style: subtitle-main

- start: 95.0
  end: 105.0
  text: "外向的人电池容量大。你的小——但快充支持。"
  style: subtitle-main

- start: 120.0
  end: 123.0
  text: "阶段一：我还行"
  style: subtitle-stage

- start: 137.0
  end: 140.0
  text: "阶段二：什么时候能走"
  style: subtitle-stage

- start: 159.0
  end: 162.0
  text: "阶段三：完蛋，我该说点什么"
  style: subtitle-stage

- start: 180.0
  end: 183.0
  text: "阶段四：1%"
  style: subtitle-stage

- start: 195.0
  end: 198.0
  text: "阶段五：逃"
  style: subtitle-stage

- start: 226.0
  end: 238.0
  text: "我们花了太多时间，觉得'一个人'是个需要被解决的问题。"
  style: subtitle-main

- start: 256.0
  end: 266.0
  text: "你只是一个正常的、需要独处来恢复能量的人。"
  style: subtitle-main

- start: 302.0
  end: 312.0
  text: "这其实是品质。不是缺陷。"
  style: subtitle-emphasis

- start: 320.0
  end: 328.0
  text: "是你选择了和自己待一会儿。"
  style: subtitle-emphasis

- start: 396.0
  end: 404.0
  text: "下次社交电量归零的时候——别跟自己过不去。"
  style: subtitle-main

- start: 414.0
  end: 422.0
  text: "轮到跟你自己待一会儿了。"
  style: subtitle-main

- start: 422.0
  end: 430.0
  text: "内向不是病。是你大脑的节能模式。"
  style: subtitle-emphasis

---

## Subtitle Styles

- id: subtitle-main
  font: font-noto-sc
  font_size: 52
  primary_color: "#FFFFFF"
  outline_color: "#000000"
  outline_width: 4
  blur: 0.5
  position: [0.5, 0.88]
  alignment: center
  margin_bottom: 60
  line_spacing: 1.4
  max_width: 1600

- id: subtitle-title
  font: font-noto-sc-bold
  font_size: 72
  primary_color: "#FFD700"
  outline_color: "#000000"
  outline_width: 5
  blur: 1.0
  position: [0.5, 0.5]
  alignment: center

- id: subtitle-stage
  font: font-noto-sc-bold
  font_size: 64
  primary_color: "#FF4444"
  outline_color: "#000000"
  outline_width: 5
  blur: 0.5
  position: [0.5, 0.25]
  alignment: center
  animation: bounce_in

- id: subtitle-emphasis
  font: font-noto-sc-bold
  font_size: 58
  primary_color: "#FFFFFF"
  outline_color: "#000000"
  outline_width: 5
  blur: 1.0
  position: [0.5, 0.5]
  alignment: center
  animation: fade_in

---

## Keyframes

- target: party-crowd
  property: scale
  type: vec2
  keyframes:
    - time: 0.0, value: [1.0, 1.0], easing: "ease_out_cubic"
    - time: 3.0, value: [1.06, 1.06], easing: "linear"

- target: person-exhausted
  property: scale
  type: vec2
  keyframes:
    - time: 8.0, value: [1.0, 1.0], easing: "ease_out_cubic"
    - time: 13.0, value: [1.04, 1.04], easing: "linear"

- target: smile-dead-eyes
  property: scale
  type: vec2
  keyframes:
    - time: 20.0, value: [1.0, 1.0], easing: "ease_out_cubic"
    - time: 25.0, value: [1.08, 1.08], easing: "linear"

- target: eight-people
  property: scale
  type: vec2
  keyframes:
    - time: 162.0, value: [1.0, 1.0], easing: "ease_out_cubic"
    - time: 170.0, value: [1.12, 1.12], easing: "linear"

- target: running-out
  property: scale
  type: vec2
  keyframes:
    - time: 198.0, value: [1.0, 1.0], easing: "ease_out_cubic"
    - time: 206.0, value: [1.02, 1.02], easing: "linear"

- target: window-rain
  property: scale
  type: vec2
  keyframes:
    - time: 226.0, value: [1.0, 1.0], easing: "ease_out_cubic"
    - time: 238.0, value: [1.05, 1.05], easing: "linear"

- target: forest-path
  property: scale
  type: vec2
  keyframes:
    - time: 256.0, value: [1.0, 1.0], easing: "ease_out_cubic"
    - time: 266.0, value: [1.06, 1.06], easing: "linear"

- target: genuine-smile
  property: scale
  type: vec2
  keyframes:
    - time: 302.0, value: [1.0, 1.0], easing: "ease_out_cubic"
    - time: 312.0, value: [1.05, 1.05], easing: "linear"

- target: night-city
  property: scale
  type: vec2
  keyframes:
    - time: 320.0, value: [1.0, 1.0], easing: "ease_out_cubic"
    - time: 328.0, value: [1.04, 1.04], easing: "linear"

- target: cozy-home
  property: scale
  type: vec2
  keyframes:
    - time: 396.0, value: [1.0, 1.0], easing: "ease_out_cubic"
    - time: 404.0, value: [1.03, 1.03], easing: "linear"

- target: phone-charging
  property: position
  type: vec2
  keyframes:
    - time: 333.0, value: [0, 0], easing: "ease_out_cubic"
    - time: 339.0, value: [0, -10], easing: "ease_in_out"

- target: cat-box
  property: rotation
  type: float
  keyframes:
    - time: 359.0, value: 0.0, easing: "linear"
    - time: 362.0, value: 2.0, easing: "ease_in_out"
    - time: 364.0, value: 0.0, easing: "ease_in_out"

---

## Chapter Markers

These are non-rendering metadata markers for editor navigation.

- marker: "Hook"
  time: 0.0
  color: "#FF6B6B"

- marker: "Ch1: 你的大脑不是手机"
  time: 36.0
  color: "#4ECDC4"

- marker: "Ch2: 五个阶段"
  time: 120.0
  color: "#FFE66D"

- marker: "Ch3: 一个人不等于孤独"
  time: 226.0
  color: "#95E1D3"

- marker: "Ch4: 充电手册"
  time: 333.0
  color: "#F38181"

- marker: "Ending"
  time: 396.0
  color: "#AA96DA"
