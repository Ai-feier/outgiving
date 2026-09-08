---
unit: goal
title: 全局目标
follows: []
层: l1
---

# 全局目标 · T005 血锁一護变身奇观

> 状态: 完成

## ① 简层

人的一句话：给我一段 **16:9 横屏纯视觉 AI 视频**——Bleach 最终章新形态「血锁的一护」，核心是**最强形态变身 + 王虚的闪光**的冲击感；两段各 5 秒；内部压测用，先不考虑版权与发布。
（感受词：压迫 → 炸开 → 亮瞎。参考素材：人给零张，由 research 单元去找。）

## ② 思考

### 共同理解（四方已确认）

*主会话预填（用户需求已锁定，agent 确认或修正，不改需求）。*

| 维度 | 内容 | 确认 |
| ------ | ------ | ------ |
| 这条视频一句话是什么 | Bleach 最终章新形态"血锁的一护"变身纯视觉奇观：2×5s 横屏，压抑→觉醒→爆发 | ✅ script visual ***rhythm*** director |
| 核心沟通目标 | 纯视觉冲击/变身爽感——形态揭示（双角+血锁灵压）+ 王虚的闪光爆发。无叙事无信息负担 | ✅ script visual ***rhythm*** director |
| 平台 + 时长 | 内部压测用（暂不发布），16:9 横屏，2 段各 5s | ✅ script visual ***rhythm*** director |
| 风格 | Bleach 日系动画质感（止め絵/速度线/墨韵），全 AI 生成 | ✅ script visual ***rhythm*** director |
| 生成策略 | Seg1 出 A/B 两版：H3 多图参考（768p横，2 张官方图） vs Seedance（16:9 mini）；赢家的末帧作 Seg2 的 ref_image_0 接续；共 3 次生成 | ✅ script visual ***rhythm*** director |
| 音频 | 无对白；genbgm 生成氛围 BGM，ai edit 合成混入 | ✅ script visual ***rhythm*** director |
| 版权/红线 | 用户明确：本轮先不考虑版权与发布；BGM 必须 genbgm 自产，不用鷺巣詩郎原声 | ✅ script visual ***rhythm*** director |
| 两段切分 | Seg1=压抑→觉醒（0–5s，末帧：双角与面具成型、刀横置，作接续锚点）；Seg2=爆发（5–10s，睁眼血光→突进→黑红 Cero 洪流轰穿镜头） | ✅ script visual ***rhythm*** director |

**主会话管线备注（agent 无需确认，背景信息）**：

- 官方形态描述与参考图见 `research.md`（② · 1.1 官方描述逐条拆解 + 1.2 参考图 2 张 + 3. 技术备注）
- Seedance 版权过滤器为已知风险（T003 教训）：A/B 时直接记录拦截行为，是压测数据的一部分，不是失败

### 假设与未锚

- 假设：A/B 同段对照（H3 vs Seedance），赢家末帧接续 Seg2（② · 切分计划已锁定）。未锚：生成策略终局以门 3 裁决为准（gates/gate3-design-alignment.md）。

### grill 记录

## ③ 内容详情

### 切分计划（1 goal → n 单元）

- 设计链：research → script → visual / rhythm（并行）→ director
- 生成链：seg1（A/B）→ 赢家末帧 → seg2 → end（BGM + 混音拼接）
- A/B 策略：H3 多图参考 vs Seedance 纯文本，同 Seg1 对照；末帧接续决定 Seg2 走哪条
- 门：门 3 裁决包 `gates/gate3-design-alignment.md`（人裁决点）；门 4 = 工作台终审请求体

## ④ 执行

- 派单顺序：主会话直接做 research（本轮 4-agent 范围不含 gather-expert）→ 4 designer 并行（script 先广播方向）→ director 收口 → 门 3 → seg1 生成
- 工作台数据面：本目录所有带 `unit:` frontmatter 的 md 即链节点（本文件为链头）

## ⑤ 结果

- 资源就绪（设计完成时点）：

| 资源 | 状态 | 备注 |
| ------ | ------ | ------ |
| 官方参考图 ×2 | ✅ P0 就绪 | 001（1061×1500 竖）/ 002（1920×1080 横）；画面内容未目验（无视觉模型），首次生成即验证 |
| H3 通路 | ✅ P0 就绪 | AUTODL_API_KEY 已通，768p横 ¥0.05/5s（促销 1 分/秒） |
| Seedance 通路 | ✅ P0 就绪 | 火山凭证 OK，mini 档 16:9 |
| BGM | ⏳ P1 | genbgm，rhythm 给设计后生成（设计已出，见 `rhythm.md` ② · BGM 设计） |

- 链（段→段）：`段 p1（goal → research → script → visual/rhythm → director → seg1）→ 段 p2（goal2 → seg2 → end）`；段交接 = 段末 end 段 → 下段 goal（各单元 end 段里有交接）
