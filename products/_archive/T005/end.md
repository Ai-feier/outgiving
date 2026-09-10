---
unit: end
follows: [seg2]
gate: 是
层: l2
---

# 成片运行卡 · BGM + 混音 + 拼接

> 状态: 未开始

## ① 简层

本次运行：BGM 生成 + 混音 + 10s 拼接。BGM 设计见 `rhythm.md` ② · BGM 设计（genbgm 六段结构 + 硬同步点 4.6s/8.0s ±0.1s）；C1-A 裁决（门 3 §3①）若采 director 单锚 → 先改 genbgm 字段再执行。

## ② 思考

- 执行决策（引用，不复述）：
  - BGM 只执行不设计（设计归属 rhythm 单元）
  - 混音：`ai edit`（BGM 轨 + 画面内物理声；H3 音乐垫冲突则 mute 退法，红线见 `goal.md` ①/②）
  - 验收基准：硬同步点偏差 ±0.1s 内 + 5.0s 段接缝无跳帧（rhythm ② · 混音要求）

### 假设与未锚

- 假设：硬同步点 ±0.1s 可达成（rhythm 设计值）；未锚：实际混音偏差（生成后回校）。

### grill 记录

## ③ 内容详情

交付：10s 成片（seg1+seg2 硬切拼接）+ genbgm BGM（rhythm 六段结构）+ 混音参数记录；执行命令在 ④，全链成本/耗时汇总写 ⑤。

## ④ 执行

- bgm：`uv run --directory scripts ai generate bgm --prompt-file <rhythm.md ② · BGM prompt 字段> -o assets/bgm/`
- 混音：`ai edit`（seg1 + seg2 + bgm → `outputs/T005-final-10s.mp4`）
- 段接缝校验：5.0s 前后首末帧 SSIM / 肉眼

## ⑤ 结果

⏳ 待 seg1/seg2 出片且目验通过。交付：10s 成片 + BGM 文件 + 混音参数记录 + 全流程成本/耗时表（至此全链收口）。
