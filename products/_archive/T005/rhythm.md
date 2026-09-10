---
unit: rhythm
title: 节奏曲线
follows: [script, visual]
层: l1
---

# 节奏曲线 · T005 血锁一護压缩-释放

> 状态: 完成

## ① 简层

10s 变身 = 一次呼吸的压缩-释放：0–5s 压缩（弹簧压满，末 1.8s 静帧）→ 4.6–5.8s 瞬静拍（时间停滞）→ 5.8–10s 释放（6.0s 骤起 → 8.0s Cero 轰击 → 末 0.5s 吞没帧），止于峰值无平复。

## ② 思考

### 自报 · rhythm-designer

**我理解的方向**：10s 变身奇观 = 一次呼吸的压缩-释放：0–5s 压缩（压抑 hold→1.2s 破锁 0.2s 爆起→2.0s 变身陡升→1.8s 落定静帧=弹簧压满）→ 4.6–5.8s 瞬静拍（时间停滞·空白即节拍，全片最大压缩点）→ 5.8–10s 释放（6.0s 突进骤起→8.0s Cero 轰击→末 0.5s 吞没帧余韵），止于峰值无平复。爽感核心 = 5.0–6.0s 跨边界「双静」（共 2.8s 近静）× 6.0s 骤起对比。

**曲线类型**：压缩-释放（主）× 空白即节拍（段边界静帧）× 落地/余韵（末 0.5s）。第二遍成立：循环接缝 = 10.0s 黑红满屏 + sub-bass drone → 0.0s 墨韵虚空 + 同族 drone（色续+音续）；第二遍奖励 = 锁链搏动细节 / 5.2s 点状高频 / 锁链四向迸裂方向。

**CL 标定（终值；script 粗估 2/3/3/3/3/4 → rhythm 标定）**：1A=2 / 1B=3 / 1C=3 / **2A=2⬇**（静帧空白拍，ED4/CL2 解耦）/ **2B=4⬆**（运动密度峰值）/ 2C=4；曲线均值 CL=3.0。CF（单边归 rhythm）：1/4/2/2/5/4——CF5 仅 2B 2.0s<3s；无 post-edit 切，ASL=5s/段≥1.8s；通道堆叠=2（视觉+BGM，显式标注无文字层）。rhythm_intensity：1.5/3.25/3.0/2.5/4.25/4.25。细节+护栏自检 → `rhythm.md`。

**M4 正式确认**：压抑 ~1.2s 足够（1A=A2 非中性热身；蓄力=低运动+低频 hold；释放压缩=1C 1.8s+2A 1.0s+4.6–5.8s 瞬静拍共 2.8s 近静，全片 ~40% 为压抑/蓄力材质）→ 不延长 Seg1；M6 若触发门 3，节拍表按新结构重锚。

**镜头-动势映射**（rhythm-designer 推荐，video-director 矛盾矩阵裁决）：1A static locked（extremely slow）｜1B handheld drift + medium push-in（1.2s 跳变后 0.2s 爆起）｜1C slow push-in→static（4.6s 归零）｜2A static hold｜2B rapid push-in/tracking（fast）｜2C static recoil→末 0.5s hold。One verb per shot；1C 释放前静帧=刻意「意外停顿」（Adams 双因子：低运动由 ED/CL 补偿）。

**BGM 设计（genbgm 自产）**：总时长恰好 10.0s（duration_hint=10）/ 140 BPM / 六段结构 `[0–1.2 暗黑低频 hold]→[1.2–3.2 主题起现]→[3.2–4.6 主题全现]→[4.6–5.8 瞬静拍（近寂）]→[5.8–8.0 峰值突进]→[8.0–10.0 低频坠落+afterglow]`；硬同步点：4.6s 瞬静 ±0.1s（锚）/ 8.0s 轰击 ±0.1s（锚）/ 1.2·3.2·5.2s ±0.15s；10.0s 帧=sub-bass drone（循环接缝，不放 fade）。完整 prompt = genbgm 结构化字段集（genres 风格堆叠 / instruments 乐器质感 / mood / structure_tags；无已有曲目、无 vocals）+ 文字版等价描述 + 混音要求 + 结构遵循度退法 → `rhythm.md` §BGM。

**冲突标注**：⚠️ C1——我的 BGM「4.6–5.8s 瞬静拍」与 director.md §3 H3 `non_diegetic_music` 代拟形态（5.0s 渐强顶）不一致 → **与 director 收口冲突，待门 3 裁决**（非阻塞：最终 BGM=genbgm 红线，genbgm 结构以 `rhythm.md` 六段为准；H3 内置垫有 `ai edit mute` 退法）。其余时码/无切/ASL 与 director 收口一致（`rhythm.md` §冲突检查 C2–C5）。

**对齐自报**：总拍数 6 子拍（2×3）/ 总时长 10s / 段数 2 / 段边界 5.0s（延续边界）——与 script 自报 0 差异；CF/V 归属与通道堆叠显式标注。

> 2×5s · 16:9 · 纯视觉无旁白无字幕 · 宣泄弧（压抑→觉醒→爆发，止于 Cero 峰值）
> 输入源：`goal.md` ②（共同理解）/ `script.md` ② · 自报（定稿，PAD 曲线 + M1–M6）/ `director.md` ② · 自报（director 收口 17:36）
> 上游状态：script ✅ 定稿；director ✅ 收口（H3 音频字段=代拟，本文件 BGM 设计即其「genbgm 出片后回校」基准）；visual §2.2 未填——**不阻塞 rhythm**（CL/CF 标定不依赖 V，V 由 visual 独立管理，通道堆叠已按 ≤2 显式标注）

### 假设与未锚

- 假设：BGM 六段结构 + 硬同步点 4.6s/8.0s 为设计值；未锚：genbgm 实际产出是否对齐（生成后回校）。

### grill 记录

## ③ 内容详情

#### 元信息

- 总时长 10s = 2 生成单元 × 5s（Seg1 压抑→觉醒 / Seg2 爆发）；子拍为设计标注：6 子拍（1A 1.2s / 1B 2.0s / 1C 1.8s / 2A 1.0s / 2B 2.0s / 2C 2.0s）
- 子拍间**无 post-edit 硬切**：AI 生成视角每 5s 为连续一镜，子拍转场 = prompt 驱动的镜内状态推进（与 director ZPC 门一致：「子拍间过渡=因果/递进/空白，无 <1.8s 硬切碎片」）
- 曲线类型：**压缩-释放（主）× 空白即节拍（5.0s 边界瞬静拍）× 落地/余韵（末 0.5s 吞没帧）**
- 第二遍成立（曲线自反性）：循环接缝 = 10.0s 黑红满屏 hold + sub-bass drone → 0.0s 墨韵虚空 + 同族 drone（色续：黑底+血红高光两侧同族，音续：同族低频）；第二遍奖励 = 1A 锁链搏动细节 / 4.6–5.8s 瞬静拍点状高频 / 1B 锁链四向迸裂方向（详见 §可重看性）

#### 节奏总览

| 项 | 值 |
| -- | -- |
| 曲线类型 | 压缩-释放（主）：0–5s 压缩（压抑 hold→1.2s 破锁 0.2s 爆起→2.0s 变身陡升→1.8s 落定静帧=弹簧压满）→ 4.6–5.8s 瞬静拍（最大压缩点，空白即节拍）→ 5.8–10s 释放（6.0s 突进骤起→8.0s Cero 轰击→吞没帧余韵），止于峰值无平复 |
| 平台 | 内部压测（暂不发布）→ 无算法约束；节奏参照 = 快动作/TikTok 类基线（切频 1–2s、钩子窗口 1.7s，仅作参照系） |
| 曲线级 CL | 每拍 CL 1–5 标定（下表，范围 2–4，均值 3.0）；NRI 倒 U 目标带 1.5–2.0： novelty 事件 2 个（1B 形态变化 / 2B 速度峰值）+ 主题复现拍 4 个（1A 意象预置 / 1C 锁定 / 2A 静帧 / 2C 峰值复现），novelty 均匀分布于 10s、无连续 CF≥4 段 >3s → 处倒 U 带中上区（不闷不死、不过载） |
| CF/V 归属 | CF（变化密度/切频）= 本节奏单边主张；V（视觉密度/组块）= visual 独立管理；通道堆叠 = 2（视觉 + BGM 音频），显式标注：无文字层/无 UGC 第三通道 |
| 映射模式 | 同频（默认：镜内状态跳变点 1.2s/3.2s/6.0s/8.0s 全部落在 BGM transient 锚点上，MAVIN 精度见 §BGM 硬同步点）+ 反拍式对位（4.6–5.8s：视觉静帧 × 音频近寂 = 双通道空白，沉默在说话） |
| 钩子/中断 | 无公开钩子约束（内部片）；按设计纪律：前 0.3s 中断 = t=0.1–0.3s 锁链辉光微闪（视觉 0.1s）+ 0.0s 低频 thump（音频）= 双通道微中断，不揭示形态（维持压抑）；觉醒起 1.2s = 本片真钩子点（1.7s 基准窗口内 ✓） |

#### 节拍分配

| 拍号 | 时码 | 时长 | ID | ED | CL | CF | 转场（至下一拍） | 偏差 |
| ---- | ---- | ---- | -- | -- | -- | -- | ---- | ---- |
| 1A 压抑 | 0.0–1.2 | 1.2s | 1 | 2 | 2 | 1 | 因果·hard cut→handheld 起（script 规划；见注①） | 开场 0.3s 中断微事件（rhythm-designer 建议，见注②） |
| 1B 觉醒 | 1.2–3.2 | 2.0s | 3 | 3 | 3 | 4 | 递进·连续，落定 hold | 1.2s 状态跳变=prompt 内跳变（见注①） |
| 1C 正手持锁定 | 3.2–5.0 | 1.8s | 3 | 4 | 3 | 2 | 空白（段边界·时间停滞） | 释放前刻意静帧（注③） |
| 2A 点燃 | 5.0–6.0 | 1.0s | 2 | 4 | **2** | 2 | 因果（点燃→突进） | CL 标定 3→2⬇（静帧空白拍，ED4/CL2 解耦） |
| 2B 突进 | 6.0–8.0 | 2.0s | 3 | 5 | **4** | 5 | 因果（突进→Cero 释放） | CL 标定 3→4⬆（运动密度峰值） |
| 2C Cero 洪流 | 8.0–10.0 | 2.0s | 4 | 5 | 4 | 4 | （结束·峰值截断，无下一拍） | CF4=单一能量流非高频切；末 0.5s hold=落地/余韵 |

rhythm_intensity（=（ID+ED+CL+CF）/4，供运镜映射）：**1A=1.5（低强）/ 1B=3.25（中强）/ 1C=3.0（中强下沿）/ 2A=2.5（中低）/ 2B=4.25（高强）/ 2C=4.25（高强）**

注① 段内「hard cut」（1.2s / 6.0s）：单次连续 5s 生成中无 post-edit 切点，它们是 prompt 驱动的镜内状态跳变（director H3 prompt `At 00:01.200 / 00:03.200`、`At 00:01.000 / 00:03.000` 与 Seedance 时序描述同位）。若 A/B 生成出干净跳变 → 视为镜内硬切（节奏收益 ≈0.1s 微瞬寂）；若模型抹成 morph → 节奏退回连续加速，仍成立（1B/2B 靠运动密度承载 tempo）。不单改，M6 相关；若门 3 触发结构变更（7+3 或 3+2+5），本表重锚。
注② 0.3s 中断微事件（rhythm-designer 建议）：1A prompt 追加「t=0.1–0.3s 锁链辉光单次微闪（0.1s）后回落到被压制状态」。1A prompt 在 script 定稿文件内，不单方修改 → 请 visual/director 吸收进 1A 段描述。
注③ 释放前静帧（Adams 双因子）：1C CF2 + 运动 4.6s 衰减归零 = 低运动由 ED4/CL3 补偿 tempo（shot_length × motion：时长+情绪定速）。属**刻意**的「意外停顿」（释放前屏息），非节奏-运镜不一致需纠偏项。

##### 护栏自检

- **ASL**：无 post-edit 切，2 连续镜各 5s → ASL=5s/段 ≥1.8s ✓；无连续 5s ASL<1.8s ✓
- **CF5 不持续 ≥3s**：CF5 仅 2B（2.0s）✓；CF≥4 边界后停顿：1B(CF4)→1C 落定 hold 1.8s ≥1s ✓；2B→2C 无镜边界（同连续镜），WM 压力由 9.5–10.0s 吞没帧 hold 吸收 ✓
- **0.66s 窗口放关键信息**：1.2–1.86s 锁链迸裂起（觉醒确认）/ 3.2–3.86s 完全形态锁定（形态揭示）/ 5.0–5.66s 睁眼血光（点燃）/ 8.0–8.66s Cero 起（释放）——关键信息均落在各拍前 0.66s ✓。V≥4 时（visual 侧 1B 变身密度 / 2C 满屏能量）窗口可延至 ~1.2s，1B/2C 各 2.0s 节拍容得下
- **偏差 <40%**：CL 标定偏差 2 项，各 ±1/3≈33%（2A 降 / 2B 升，理由见下表）✓
- **通道堆叠 ≤2**：视觉 + BGM，无第三通道，显式标注 ✓

#### 子拍强度标定（script 粗估 → rhythm 标定）

| 子拍 | 粗估 | 标定 | 理由 |
| ---- | ---- | ---- | ---- |
| 1A | 2 | **2** | 单实体低信息姿态（ID1）；新增信息仅锁链辉光搏动。压抑是情绪（ED2）不是信息 |
| 1B | 3 | **3** | 四变化同现（锁链迸裂/面具蔓延/角顶出/刀形变），但同实体连续 morph = 单个可读「变身」事件；2.0s 窗口变化率高但不碎片 |
| 1C | 3 | **3** | 完全形态读出 + GroundShot 规范参考质量；「静止蓄满」= 低变化高情绪（ED4），CL3 为形态信息读出的上限 |
| 2A | 3 | **2** ⬇ | 静帧空白拍：信息增量仅「睁眼+辉光」（ID2），体感是情绪（ED4）。ED4/CL2 解耦正是此拍目的——观众「感受」而不「处理」，为 2B/2C 爆发预留 WM |
| 2B | 3 | **4** ⬆ | 全片运动密度峰值：角色突进+镜头 fast push-in/tracking 双运动+速度线满屏+运动模糊，变化率与处理负载全片最高，粗估偏低 |
| 2C | 4 | **4** | 满屏能量+角色部分可见（双层结构）+ Cero=主题意象峰值；末 0.5s hold 衰减为单色满屏（4 为前段值，尾部实际下降） |

曲线均值 CL = (2+3+3+2+4+4)/6 = **3.0**（与 script 粗估均值相同，两处偏移互抵）。
PAD 交叉验证（script PAD → 运动/音频双通道）：[P-1,A2,D2]→1A（低运动+低频 hold）/ [P0,A3,D3]→1B（主题起现+handheld drift）/ [P+1,A4,D4]→1C（主题全现+落定）/ [P+1,A4,D4]→2A（瞬静拍）/ [P+1,A5,D4]→2B（峰值+fast push-in）/ [P+2,A5,D5]→2C（轰击+低频坠落）。rhythm_intensity 轨迹 1.5→3.25→3.0→2.5→4.25→4.25，唯一「凹点」= 2A（瞬静拍，刻意设计；PAD 的 D4 不降，情绪未退，非单调性违例）。

#### 每段情绪/动势轨迹

##### Seg1（0.0–5.0s）压抑→觉醒

- **情绪轨迹（A/D 通道）**：A2（压抑·屏息）→ A3（觉醒·破笼）→ A4（全力量蓄满·张力顶）；D2（被困）→ D3（挣脱）→ D4（受控蓄满）
- **动势轨迹**：静（1A：近零运动、呼吸微颤）→ **0.2s 爆起**（1.2s 锁链迸裂）→ 2.0s 陡升（1B 变身，handheld drift + medium push-in）→ **硬停**（1C：slow push-in 于 4.6s 衰减归零，static hold 至 5.0s）。曲线 = 「S 形蓄力」：缓起→陡升→骤停。末 1.8s 静帧不是松，是压满的弹簧——释放在候场。
- **镜头动势**（rhythm-designer 推荐，video-director 矛盾矩阵裁决）：1A static locked（extremely slow，近零运动，时长定拍）｜1B handheld gentle drift + medium push-in（1.2s 状态跳变后 0.2s 爆起）｜1C slow push-in → static（4.6s 归零，hold 至 5.0s）。One verb per shot ✓；运动速度标量：extremely slow / medium / 归零 ✓

##### Seg2（5.0–10.0s）爆发

- **情绪轨迹**：A4（点燃·聚焦）→ A5（峰值速度）→ A5/D5（峰值释放）；P+1 → P+2
- **动势轨迹**：静止一拍（2A：时间停滞 + 锁链搏动一次）→ **0.3s 骤起**（6.0s 突进）→ 2.0s 全速（2B：fast push-in/tracking、速度线拉满）→ **8.0s 轰击**（2C Cero 起）→ 吞没（能量吞没角色与镜头，末 0.5s hold=落地/余韵）。无衰减——止于峰值（宣泄弧无平复）。
- **镜头动势**：2A static hold + extremely slow push-in（近零运动，时间停滞感）｜2B rapid push-in / tracking（fast）｜2C static recoil（轰击微震）→ 末 0.5s hold。
- **爽感核心**：5.0–6.0s「双静」（1C 落定 × 2A 静帧，跨边界共 2.8s 近静）× 6.0s 骤起 = 全片最大压缩-释放对比（止住→冲穿）。这是第二遍的奖励点。

#### 停顿/瞬静拍设计（間：前状态→间隔→后状态 + 镜头/音频行为）

| 时码 | 类型 | 时长 | 間结构（前状态→间隔→后状态） | 镜头行为（rhythm-designer 推荐） | 音频行为 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| 0.0–1.2s | 开场 hold（压抑，非空白） | 1.2s | 墨韵虚空→锁链辉光搏动（被压制）→迸裂 | static locked + extremely slow push-in | 低频 hold + 心跳式低脉冲；0.0s 低频 thump（中断） |
| 3.2–5.0s | 消化性/蓄满沉默 | 1.8s | 变身完成→蓄满静止→（段边界） | slow push-in → static hold（4.6s 运动归零） | 主题全现 → 4.6s 入瞬静 |
| 4.6–5.8s | 瞬静拍（时间停滞·空白即节拍） | 1.2s | 蓄满→悬停（2A 静帧·睁眼）→释放 | static hold + extremely slow push-in（近零运动） | 近寂：仅 sub-bass 基音+金属余响；~5.2s 0.1s 点状高频（睁眼） |
| 9.5–10.0s | 落地/余韵（吞没帧） | 0.5s | 轰击→吞没（黑红满屏）→循环 | static recoil → hold | 低频坠落 + afterglow 衰减 → sub-bass drone（循环接缝，与 0.0s 同族） |

注：全片仅此 3 处空白类停顿 + 1 处开场 hold。转场逻辑分布（因果×3/递进×1/空白×1）与 script 一致。

#### BGM 设计（genbgm 自产 · 总片 10s）

##### 工具接口确认（已核验）

genbgm = 火山引擎 `VolcengineBGM`（`scripts/src/ai/providers/volcengine/genbgm.py`），消费**结构化** `MusicPrompt(genres[], instruments[], vocal_style, bpm, mood, duration_hint, structure_tags[])`——非自由文本。以下为可直接组装的字段集（风格堆叠=genres / 乐器质感=instruments / mood=mood；全程无已有曲目，纯新生成）。

##### 结构要求（硬同步点 · ai edit 对齐与回校基准）

- **总时长**：恰好 **10.0s**（`duration_hint=10`；hint 非硬约束——若服务返回非 10s，ai edit 以 4.6s/8.0s 两个锚点为基准裁对齐到 10.0s）
- **BPM 锚点**：140 BPM；0–1.2s 以 half-time 感播放（sub-bass 心跳脉冲每 2 拍，≈50bpm 感 = 压迫呼吸）；1.2s 起全拍
- **六段结构**（与子拍对齐）：
  `[0.0–1.2s 暗黑低频 hold] → [1.2–3.2s 主题起现+爬升] → [3.2–4.6s 主题全现] → [4.6–5.8s 瞬静拍（近寂）] → [5.8–8.0s 峰值突进] → [8.0–10.0s 低频坠落+afterglow 衰减]`
- **硬同步点**（ai edit 对齐容差；MAVIN：锚点 ≤0.1s，其余 ≤0.3s）：

  | 时码 | 音频事件 | 容差 | 视觉对应 |
  | ---- | ---- | ---- | ---- |
  | 1.2s | 锁链迸裂 transient | ±0.15s | 1A→1B 状态跳变 |
  | 3.2s | 主题全现 | ±0.15s | 1C 落定 |
  | 4.6s | 瞬静 onset | **±0.1s（锚）** | 1C 静止→2A 时间停滞 |
  | 5.2s | 0.1s 点状高频（睁眼） | ±0.15s | 2A 睁眼血光 |
  | 8.0s | Cero 轰击 | **±0.1s（锚）** | 2C Cero 起 |

- **尾态**：8.0–10.0s = 低频坠落+afterglow 衰减，10.0s 帧停在 sub-bass 持续 drone（**不放** fade-to-silence——视频止于峰值；循环时 10.0s drone 与 0.0s 开场 drone 同族无缝）
- **结构遵循度风险与退法**（P1）：GenBGM 对 timecoded `structure_tags` 的遵循度未实测。回校顺序：① 出片后按上表 5 点验时序 → 偏差在容差内 → 直接混入；② 锚点错位但结构形状对 → ai edit 以 4.6s/8.0s 为轴 trim/对齐（10s 级裁切成本低）；③ 结构整体走形 → 退法 A：`structure_tags` 降为三段式再生成（`[dark hold]`→`[build→climax→near-silence]`→`[peak charge→impact→drop tail]`）；退法 B：BGM 无角色一致性要求 → 两段分生成（0–4.6s + 4.6–10s）在 4.6s 处拼接，段级可控。

##### BGM prompt（可直接喂 genbgm · 字段集）

```python
from ai.models import MusicPrompt

bgm_prompt = MusicPrompt(
    genres=[
        "Anime Battle Score",
        "Dark Epic Orchestral",
        "Cinematic Hybrid Orchestral",
    ],
    instruments=[
        "deep sub-bass drone",
        "brass stabs",
        "synth stabs",
        "timpani",
        "staccato strings",
        "taiko-style percussion",
        "electric bass riff",
        "metallic chain-shatter transient",
        "noise shockwave",
    ],
    vocal_style="no vocals, no lyrics, no choir words",
    bpm=140,
    mood=(
        "墨韵虚空中被囚之物：先 1.2 秒压抑屏息（低频心跳、近乎静默的压迫感），"
        "血锁迸裂的瞬间觉醒，主题刺入并爬升，力量蓄满至完全形态；"
        "4.6 秒处突然瞬静、时间冻结（只剩最低基音，像屏住呼吸的一拍）；"
        "随后骤然点燃、全速突进（铜管峰值+太鼓驱动、肾上腺素感），"
        "8.0 秒黑红洪流轰穿镜头——峰值释放、无平复、止于最高处。"
        "全曲为新生成，不引用任何已有曲目或旋律。"
    ),
    duration_hint=10,
    structure_tags=[
        "[0.0-1.2s] dark sub-bass hold, half-time heartbeat pulse, near-silence oppressive",
        "[1.2-3.2s] metallic chain-shatter transient + heroic brass motif stabs in and climbs, timpani rolls + fast staccato strings at full tempo",
        "[3.2-4.6s] full theme statement climax, layered brass + low electric-bass riff + urgent strings",
        "[4.6-5.8s] near-silence beat: mids and highs cut, only deep sub-bass fundamental + faint metallic ring-out; one tiny pinpoint high harmonic ping around 5.2s",
        "[5.8-8.0s] ignition whoosh into peak charge: blazing brass blast, driving taiko percussion, fast tremolo strings, distorted synth stabs",
        "[8.0-10.0s] massive sub-bass impact + noise shockwave, low-frequency drop, sparse afterglow harmonics decaying to a sustained dark sub-bass drone (loop-friendly, no fade to silence)",
    ],
)
```

**字段语义对照**（回校时逐条听诊）：

- `genres`（风格堆叠）：日系动画战斗 BGM × 暗黑史诗管弦 × 电影化混合编制——「Bleach 系变身」质感，不含任何已有曲风指认
- `instruments`（乐器质感）：sub-bass drone（压抑/瞬静基底）/ 铜管 stabs + synth stabs（主题刺入）/ 定音鼓（爬升）/ 断奏弦乐（紧张）/ 太鼓（突进驱动）/ electric bass riff（全现段）/ 金属锁链 transient（1.2s 迸裂）/ noise shockwave（8.0s 轰击）
- `mood`：四段情绪弧（压抑屏息→觉醒爬升→瞬静冻结→峰值释放无平复），与 script PAD A2→A3→A4→(瞬静)→A5→A5/D5 逐段对应
- `bpm=140`：1.2s 起全拍节奏锚；0–1.2s half-time 感由 structure_tags 第 1 段承载
- `duration_hint=10`：与总片 1:1；`structure_tags` 6 段 = 子拍 6 拍的时间码镜像
- `vocal_style`：显式无 vocals（纯视觉片无旁白，BGM 亦不引入人声通道）

**文字版等价描述**（备用：若 genbgm 后续开放文本 prompt 通道，或需人工向另一音乐工具转述；非喂入字段）：

> Cinematic dark-epic anime transformation battle score, Japanese TV-animation battle music blended with cinematic hybrid orchestral; 140 BPM; A minor; exactly 10 seconds; no vocals, no lyrics, no existing melodies. 0.0–1.2s: oppressive near-silence, deep sub-bass drone pulsing slowly like a held breath (half-time feel), faint dark noise texture and dim metallic low shimmer. 1.2s: sharp metallic chain-shatter transient; immediately a short heroic brass-and-synth motif stabs in and climbs in pitch with rising timpani rolls, fast staccato strings and a dark driving pulse. 3.2s: the motif becomes a full-statement climax with layered brass, a low electric-bass riff and urgent strings. 4.6s: sudden near-silence, all mids and highs cut, only a deep sub-bass fundamental and faint metallic ring-out remain, a suspended time-stopped feeling for about 1.2 seconds, with one tiny pinpoint high harmonic ping around 5.2s. 5.8s: an ignition whoosh launches the peak charge, blazing brass blast, driving taiko-style percussion, fast tremolo strings, distorted synth stabs, pure adrenaline until 8.0s. 8.0s: a massive cinematic sub-bass impact with a noise shockwave, then a low-frequency drop with sparse bright afterglow harmonics decaying, ending on a sustained dark sub-bass drone at 10.0s (loop-friendly, no resolution, no fade to silence). Texture keywords: ink-black void atmosphere, blood-crimson energy glow, anime speed-line whooshes, stop-frame sudden-silence moment. Mood arc: oppressive held-breath tension → awakening eruption → explosive peak release, ends at the peak without resolution.

##### 混音要求（ai edit · 供参考）

- BGM = 唯一音乐轨；H3 内置音乐垫（director 代拟形态）与 genbgm BGM 两形态并存时：共混 → BGM 为主（垫降 3–6dB 作环境底层）；冲突明显（重点 4.6–5.8s 瞬静 vs H3 垫的 5.0s 渐强）→ `ai edit mute` H3 音乐垫，以 genbgm BGM + 重抽环境声替代（director 音频裁决退法，director.md §3.2）
- 4.6–5.8s 瞬静拍：残响保留 3–5dB（真 0dB 会破坏循环连续性）
- 8.0s 轰击：低频可瞬间冲顶（能量峰值），随后 -6dB 进衰减
- 环境声层（锁链迸裂/whoosh/Cero roar）独立于 BGM：1.2s/8.0s 的 transient 峰值位归环境层（重抽或独立合成），BGM 只承担节拍锚——避免双层 transient 打架

#### 与 director.md（director 收口 17:36）冲突检查

| # | 项 | 我的方案 | director 收口 | 判定 |
| - | -- | ---- | ---- | ---- |
| C1 | H3 `non_diegetic_music` 形态 | 3.2–4.6s 主题全现 → **4.6–5.8s 瞬静拍**（近寂跨 5.0s 边界）→ 5.8s 起峰值 | 5.0s 渐强顶（`reaching a full crescendo exactly as the final pose locks`）→ 5.0–8.0s 连续峰值（driving percussion）→ 8.0s 骤切低频 tone | **与 director 收口冲突，待门 3 裁决**（非阻塞：最终 BGM = genbgm 自产红线，genbgm 结构以本文件六段为准；H3 内置垫有 `ai edit mute` 退法，director.md §3.2。差异根源：script PAD 映射 1C=A4「主题全现+突进前瞬静一拍」/ 2A=「瞬静一拍（时间停滞）」指向 4.6–5.8s；director 代拟把瞬静放在了 8.0s Cero 处——而 8.0s 轰击+低频坠落在我的方案中同样保留，即我的方案是「双锚」（4.6s 瞬静 + 8.0s 轰击坠落），director 方案是「单锚」（8.0s）） |
| C2 | 子拍时码 | 1.2 / 3.2 / 5.0 / 6.0 / 8.0s | H3 `At 00:01.200 / 00:03.200`（Seg1）、`At 00:01.000 / 00:03.000`（Seg2 相对 = 全片 6.0/8.0s） | ✅ 一致 |
| C3 | M4（压抑 ~1.2s 够否） | 确认（正式，理由见下） | 已标「rhythm 确认」 | ✅ 一致 |
| C4 | 无 post-edit 切 / ASL | 2 连续 5s 镜，ASL=5s/段 | ZPC 门「子拍为设计内，非快切」 | ✅ 一致 |
| C5 | 段内「hard cut」 | prompt 内状态跳变（注①） | H3 [Shot 2]「the shot cuts to…」（同理解释） | ⚠️ 一致；执行风险归 M6（门 3） |

**M4 正式确认**：1.2s 压抑**足够**。理由：(a) 1A 是 A2（紧张）非 A1（中性热身），hold 不是「等开始」而是「被囚」；(b) 蓄力靠低运动+低频 hold 承载，不靠时长；(c) 真正的释放压缩 = 1C 1.8s 落定静帧 + 2A 1.0s 静帧 + 4.6–5.8s 瞬静拍（跨边界共 2.8s 近静）——全片约 4.0s（40%）为压抑/蓄力材质，宣泄弧够用；(d) 爆发爽感来自 6.0s 骤起的对比度，不来自前段静帧的长度。**结论：M4 确认，不延长 Seg1**（除非 M6 触发门 3，届时节拍表按新结构重锚）。

#### 可重看性（第二遍）

- **循环接缝**：10.0s 帧（黑红满屏 hold + sub-bass drone）→ 0.0s 帧（墨韵虚空+微红锁链辉光 + 同族 drone）：色续（黑底+血红高光两侧同族）+ 音续（同族低频），循环无割裂
- **第二遍奖励**：① 1A 锁链搏动细节（第一遍读作「压抑」，第二遍皮下搏动节律可见）② 4.6–5.8s 瞬静拍（第一遍=「时间停了」，第二遍读出 5.2s 点状高频与锁链搏动一次）③ 1B 锁链四向迸裂方向（第一遍运动模糊，第二遍颈/手/脚迸裂方向可逐读）
- **曲线自反性**：压缩-释放 + 空白即节拍 + 止帧静帧均为重播友好曲线要素；CL 均值 3.0、NRI 处倒 U 带中上区，第二遍不闷（有细节奖励）也不过载（无信息洪峰）

## ④ 执行

交付即本文件：节拍分配 + 护栏自检 + CL/CF 标定 + 停顿/瞬静拍设计 + BGM 设计（genbgm 结构化字段集 §BGM，可直接喂 genbgm；硬同步点 4.6s/8.0s ±0.1s）。

## ⑤ 结果

#### 对齐自报（收口于本单元 end 结果）

总拍数 = 6 子拍（2 生成单元 × 3 子拍）/ 总时长 10s / 段数 2 / 段边界 5.0s（延续边界）——与 script 自报 **0 差异**；M4 确认；⚠️ C1：BGM 瞬静拍 4.6–5.8s 与 director 收口 director.md §3 H3 音频字段代拟形态（5.0s 渐强）冲突——**与 director 收口冲突，待门 3 裁决**（非阻塞，genbgm 红线 + mute 退法）。

- 对齐自报：见 ② · 对齐自报（M4 确认 / CL 终值 2/3/3/2/4/4 / CF 1/4/2/2/5/4 / 0 差异）
- 交接：end 单元（BGM genbgm 六段结构 + 硬同步点 + 混音要求）、director（镜头-动势映射 + M4 确认）；⚠️ C1-A 冲突（BGM 瞬静拍 vs director 单锚渐强）待门 3 裁决（`gates/gate3-design-alignment.md` §3①，推荐采 rhythm 双锚）
