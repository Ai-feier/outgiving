# T004 社交电量 — Composition v2

> Hook (0:00-0:35) + Chapter 3 (0:36-3:00)
> Emotional arc: chaos -> mode interrupt -> reflection -> re-frame -> tear-jerking peak -> closing warmth
> Format: 16:9 horizontal, 1920x1080, 30fps | Bilibili

## Meta

| Meta          | Value       |
| ------------- | ----------- |
| resolution    | 1920 x 1080 |
| fps           | 30          |
| total_duration| 180.0       |

## Assets

| ID               | Path                                     | Type  |
| ---------------- | ---------------------------------------- | ----- |
| party-01         | assets/footage/pexels-party-01.mp4       | video |
| tired-01         | assets/footage/pexels-tired-01.mp4       | video |
| fake-smile-01    | assets/footage/pexels-fake-smile-01.mp4  | video |
| brain-scan-01    | assets/footage/pexels-brain-scan-01.mp4  | video |
| rain-window-01   | assets/footage/pexels-rain-window-01.mp4 | video |
| cafe-reading-01  | assets/footage/pexels-cafe-reading-01.mp4 | video |
| forest-path-01   | assets/footage/pexels-forest-path-01.mp4 | video |
| journal-01       | assets/footage/pexels-journal-01.mp4     | video |
| cat-sleep-01     | assets/footage/pexels-cat-sleep-01.mp4   | video |
| genuine-smile-01 | assets/footage/pexels-genuine-smile-01.mp4 | video |
| texture-grain    | assets/textures/film-grain-01.mp4        | video |

## Track: main

| ID    | Asset             | Source          | At      | Speed | Mask                                       | Tags                      |
| ----- | ----------------- | --------------- | ------- | ----- | ------------------------------------------ | ------------------------- |
| h01   | party-01          | 0.0-2.0         | 0.0     | 1.0   | --                                         | hook                      |
| h02   | party-01          | 5.0-7.0         | 2.0     | 1.0   | --                                         | hook                      |
| h03   | tired-01          | 0.0-5.0         | 4.0     | 0.8   | --                                         | hook,mode-interrupt       |
| h04   | fake-smile-01     | 0.0-4.0         | 9.0     | 1.0   | --                                         | hook                      |
| h05   | party-01          | 10.0-11.5       | 13.0    | 1.3   | --                                         | hook,montage              |
| h06   | party-01          | 15.0-16.5       | 14.5    | 1.3   | --                                         | hook,montage              |
| h07   | party-01          | 20.0-21.5       | 16.0    | 1.3   | --                                         | hook,montage              |
| h08   | party-01          | 25.0-26.5       | 17.5    | 1.3   | --                                         | hook,montage              |
| h09   | fake-smile-01     | 4.0-9.0         | 19.0    | 1.0   | --                                         | hook                      |
| h10   | --                | --              | 24.0    | --    | --                                         | black,silence             |
| h11   | --                | --              | 26.0    | --    | --                                         | title-card                |
| h12   | brain-scan-01     | 0.0-5.0         | 31.0    | 1.0   | --                                         | hook,transition           |
| c01   | rain-window-01    | 0.0-19.0        | 36.0    | 1.0   | --                                         | ch3                       |
| c02   | cafe-reading-01   | 0.0-20.0        | 55.0    | 0.9   | circle(0.5,0.5,0.28,feather=0.1)           | ch3,spotlight             |
| c03   | forest-path-01    | 0.0-20.0        | 75.0    | 1.0   | --                                         | ch3                       |
| c04   | brain-scan-01     | 5.0-18.0        | 95.0    | 1.0   | --                                         | ch3                       |
| c05   | journal-01        | 0.0-14.0        | 108.0   | 1.0   | --                                         | ch3                       |
| c06   | cat-sleep-01      | 0.0-8.0         | 122.0   | 1.0   | --                                         | ch3                       |
| c07   | genuine-smile-01  | 0.0-20.0        | 130.0   | 1.0   | --                                         | ch3,peak                  |
| c08   | rain-window-01    | 19.0-34.0       | 150.0   | 1.0   | --                                         | ch3                       |
| c09   | brain-scan-01     | 0.0-15.0        | 165.0   | 0.7   | --                                         | ch3,closing               |

## Track: overlay

| ID      | Asset          | Source       | At      | Speed | Mask | Tags                                    |
| ------- | -------------- | ------------ | ------- | ----- | ---- | --------------------------------------- |
| grain-1 | texture-grain  | 0.0-180.0    | 0.0     | 1.0   | --   | overlay,blend:overlay,opacity:0.12      |

## Subtitles

| Start | End   | Text | Font | Size | Outline       | Position      |
| ----- | ----- | ---- | ---- | ---- | ------------- | ------------- |
| 9.5   | 12.5  | 你有没有过这种感觉—— | PingFang SC | 56 | 4,#000000 | bottom,120    |
| 13.5  | 18.5  | 你在一个挺好的派对里。音乐不错。人也不错。 | PingFang SC | 52 | 4,#000000 | bottom,120    |
| 19.5  | 23.5  | 但你突然意识到——你没办法再笑一下了。 | PingFang SC | 52 | 4,#000000 | bottom,120    |
| 24.5  | 26.0  | 不是因为你不想。是你的脸……它不合作了。 | PingFang SC | 48 | 4,#000000 | bottom,120    |
| 31.5  | 35.0  | 我们今天就来聊聊，你大脑里那块神秘的社交电池。 | PingFang SC | 48 | 4,#000000 | bottom,120    |
| 37.0  | 54.0  | 我们花了太多时间，觉得「一个人」是个需要被解决的问题。 | PingFang SC | 44 | 3,#000000 | bottom,100    |
| 56.0  | 74.0  | 「你一个人吗？」——这句话听起来像在问「你还好吗？」 | PingFang SC | 44 | 3,#000000 | bottom,100    |
| 76.0  | 94.0  | 但你有没有想过——你根本不是出了问题的外向者。你只是一个正常的、需要独处来恢复能量的人。 | PingFang SC | 42 | 3,#000000 | bottom,100    |
| 96.0  | 107.0 | 你大脑里的那个社交过滤器——它不是坏了。它是一个精密敏感的仪器。它需要定期关闭维护。 | PingFang SC | 42 | 3,#000000 | bottom,100    |
| 110.0 | 121.0 | 历史上几乎所有你想得起来的思想家——Kafka、村上、宫崎骏——都需要大量独处时间。不是因为他们是天才。是因为创造力需要安静。 | PingFang SC | 42 | 3,#000000 | bottom,100    |
| 123.0 | 129.0 | 安静的时候，你大脑才开始做最重要的工作——整理记忆、建立平时在人群里建立不了的联系。 | PingFang SC | 42 | 3,#000000 | bottom,100    |
| 132.0 | 149.0 | 所以你不是「怕人」。你只是认真对待每一次社交。你把每次交流当作真的交流不是客套。这其实是品质。不是缺陷。 | PingFang SC | 44 | 3,#000000 | bottom,100    |
| 152.0 | 164.0 | 一个人待着——不是没有人选择你。是你选择了和自己待一会儿。 | PingFang SC | 46 | 3,#000000 | bottom,100    |

## Keyframes: h03

| At   | Scale | Position | Rotation | Easing    |
| ---- | ----- | -------- | -------- | --------- |
| 0.0  | 1.0   | 0.5,0.5  | 0        | --        |
| 5.0  | 1.15  | 0.5,0.44 | 0        | ease-out  |

> Slow push toward the back of the person's head during mode interruption. Creates the "something is wrong" unease.

## Keyframes: c03

| At   | Scale | Position | Rotation | Easing       |
| ---- | ----- | -------- | -------- | ------------ |
| 0.0  | 1.0   | 0.5,0.5  | 0        | --           |
| 20.0 | 1.08  | 0.48,0.5 | 0.3      | ease-in-out  |

> Gentle leftward drift during forest path. Subtle breathing motion to match the "definition reversal" VO.

## Keyframes: c07

| At   | Scale | Position | Rotation | Easing    |
| ---- | ----- | -------- | -------- | --------- |
| 0.0  | 1.0   | 0.5,0.5  | 0        | --        |
| 20.0 | 1.18  | 0.5,0.46 | 0        | ease-in   |

> Slow zoom into the genuine smile. This is the emotional peak — the camera should arrive at the tightest framing right when VO says "品质。不是缺陷。"

## Keyframes: c09

| At   | Scale | Position | Rotation | Easing    |
| ---- | ----- | -------- | -------- | --------- |
| 0.0  | 1.0   | 0.5,0.5  | 0        | --        |
| 15.0 | 1.12  | 0.5,0.48 | 0        | ease-out  |

> Final slow pull toward the brain scan as the closing music swells. Leads into end card.

## Output

| Format | Codec   | Bitrate |
| ------ | ------- | ------- |
| mp4    | libx264 | 12M     |
