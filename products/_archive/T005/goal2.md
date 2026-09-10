---
unit: goal2
follows: [end-l1, seg1]
层: l2
---

# 段 2 目标 · Seg2 爆发（吃 seg1 末帧）

> 状态: 就绪

## ① 简层

段 2 交付：Seg2 爆发段 5s 横屏（睁眼血光→突进→黑红 Cero 洪流轰穿镜头）。输入 = 段 1 末帧 `assets/frames/seg1-h3-last.png`（seg1 end · Run 1 交接）。预期：形态连续（双角/血锁不漂移）、5.0s 段接缝无跳帧。

## ② 思考

- 段 1 交接输入：seg1 end · Run 1（末帧 YAVG 51.65 暗场，接爆发起幅）
- 段 2 范围：seg2 生成 + end（BGM/混音/拼接）收口；不回溯段 1 设计单元——如需回溯，开新段并写明理由

### 假设与未锚

- 假设：seg1 末帧作 ref_image_2 可保持形态连续；未锚：段接缝验证（生成后，Hard Rule 3）。

### grill 记录

## ③ 内容详情

交付：seg2 运行（seg1 末帧注入 ref_image_2，exec/video-prompt-h3-seg2.md）+ end 收口（BGM genbgm + 混音 + 10s 拼接）；执行在各单元 ④。

## ④ 执行

- agent: video-director
- skill: 无
- 交付指针：seg2 运行卡（本段单元）
- 交接：段 2 收口 = end 单元（BGM + 混音 + 10s 拼接）

## ⑤ 结果

⏳ 段 2 未开始。段 2 收口看 end 单元。
