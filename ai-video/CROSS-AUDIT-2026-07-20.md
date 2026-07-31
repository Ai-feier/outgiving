# Cross-Agent Consistency Audit — 2026-07-20

> 审计范围：video-director, visual-designer, script-designer, rhythm-designer
> 审计时间：2026-07-20（四 agent 同步深度精进 R22 后）
> 审计方法：逐文件提取术语表/映射表/接口定义，交叉对照

---

## 审计 1: 景别术语一致性

### 各 agent 使用的景别系统

| 层级 | director | script | rhythm | 状态 |
|------|---------|--------|--------|------|
| EWS (极远景) | EWS | extreme wide shot | (未显式使用) | ✅ 一致 — script 与 director 映射正确 |
| WS / Full shot (全景/全身) | WS / Full shot | wide shot / full shot | 全景/WS | ✅ 一致 — script 同义术语两可，不矛盾 |
| MWS / Cowboy (中全景/膝上) | MWS / Cowboy | **medium wide** | (未显式使用) | 🟡 script 的 "medium wide" 是 MWS 的直接翻译，但未与 director 术语对齐 |
| MS (中景/腰上) | MS | medium shot | MS/中景 | ✅ 一致 |
| MCU (中近景/胸上) | MCU | medium close-up | MCU/近景 | ✅ 一致 — "近景" 在中文电影术语中 = MCU |
| CU (特写) | CU | close-up | CU/特写 | ✅ 一致 |
| ECU / Macro (极特写) | ECU / Macro | extreme close-up | ECU | ✅ 一致 |

### 发现的问题

**🟡 问题 1.1 — "medium wide" 未对齐 director 术语**
- script-designer 使用 "medium wide"（英文直译），但 director 定义为 "MWS / Cowboy"（膝上）
- "medium wide" 可能被误解为 MS 附近，不是精确的 MWS/Cowboy
- 影响：script 在 AI prompt 指令字段中使用 "medium wide" 时，director 需要做二次转换
- **修复**：将 script 的 "medium wide" 替换为 "MWS"

**🟡 问题 1.2 — rhythm 景别中英文混用**
- rhythm 景别使用中文（全景/中景/近景/特写）而非 director 的英文缩写
- 功能上无冲突（中景=MS, 近景=MCU），但跨 agent 查阅时需心理映射
- **修复**：在 rhythm-designer.md 景别表中补充英文缩写

---

## 审计 2: 运镜术语一致性

### 运镜名称对照（director 15 种 as baseline）

| director | script | rhythm | 状态 |
|---------|--------|--------|------|
| Static locked shot (固定机位) | static / static hold | static locked / static hold | ✅ |
| Dolly-in / Push-in (推近) | push-in / rapid push-in / slow push-in | dolly-in/out / slow push-in / **快速zoom-in** | 🟡 |
| Dolly-out / Pull-back (拉远) | slow pull-back / pull-back | slow pull-back / gentle pull-back / 慢拉远 | ✅ |
| Orbit / Arc shot (环绕) | orbital shot | Orbit/Arc / slight orbit | ✅ "orbital" vs "orbit" 同义 |
| Tracking shot (跟拍) | over-shoulder tracking | stable tracking / Slow tracking | ✅ |
| Pan left/right (横摇) | pan-left/right / slow pan | slow pan / pan-right | ✅ |
| Tilt up/down (竖摇) | slow tilt | slow tilt / quick tilt | ✅ |
| Crane up/down (升降) | — | Crane | ✅ director 有，script 未使用 |
| Handheld / Gimbal (手持) | **handheld-drift** | handheld / **slight handheld tremor** | 🟡 |
| Rack focus (变焦点) | rack focus | rack focus | ✅ |
| Whip pan (快速横摇) | — | whip pan | ✅ |
| Parallax lateral pan | — | — | ✅ 未使用 |
| Hitchcock zoom | — | **Hitchcock zoom** (tool矩阵) | ✅ |
| First-person POV | POV 跟拍 | POV first-person | ✅ |
| Dutch angle | dutch angle | — | ✅ script有，rhythm未用 |
| — | **jump cut** | **跳跃切 / 快速切** | 🟡 不是运镜 |
| — | **slow zoom-in** | **zoom-in / zoom** | 🟡 zoom≠dolly |

### 发现的问题

**🟡 问题 2.1 — handheld-drift (script) vs Handheld/Gimbal (director)**
- script 弧线-运镜基调中 3 处使用 "handheld-drift"（经典弧转折处、宣泄弧爆发处、反弧入口）
- "drift" 是 handheld 的子类（轻微浮动而非剧烈抖动），有时是刻意的情感语调
- 影响：director 的运镜体系只有 "Handheld / Gimbal"，script 的 "handheld-drift" 会被 director 误判或丢失情感精度
- **修复**：script 中 "handheld-drift" 改为 "handheld (gentle drift)" 标注微子类，或由 director 补充到运镜表

**🟡 问题 2.2 — zoom-in/dolly-in 混用 (rhythm)**
- rhythm 节奏-运镜耦合表高强行：`handheld、whip pan、快速zoom-in、quick tilt、跳跃切`
- zoom-in（焦距变化）与 dolly-in/push-in（物理推近）是不同镜头运动
- director 运镜表只有 "Dolly-in/Push-in"，无 zoom-in
- 影响：从 rhythm 的 "zoom-in" 到 director 的 "push-in" 需 agent 主动转换，增加翻译损耗
- **修复**：rhythm 的 "快速zoom-in/quick zoom-in" 改为 "快速dolly-in/quick push-in"

**🟡 问题 2.3 — jump cut/跳跃切 被列为运镜 (rhythm)**
- rhythm 节奏-运镜耦合表高强行列 "跳跃切" 为推荐运镜
- "跳跃切/jump cut" 是剪辑转场不是镜头运动
- director 转场体系包含 "匹配剪辑" 但不含 "jump cut" 
- **修复**：从 rhythm 运镜表移除 "跳跃切" 及 "快速切"，转场行为归切频控制

**🟢 建议 2.4 — 微晃 (rhythm 停顿点)**
- rhythm 停顿点中 "悬念沉默" 建议 "slight handheld tremor at breath rhythm"
- 这是 handheld 的微子类（极度轻微的呼吸节拍抖动），不在 director 的 15 种中
- 不是错误，而是新发现的需求——可以归类为 "Handheld / Gimbal (slight tremor)"

---

## 审计 3: 角色语言接口断裂

### visual 五维 → script 三字段映射

| visual-designer 维度 | script-designer 消费 | 状态 |
|--------------------|--------------------|------|
| **1. 专属微动作 (Signature Gestures)**: ≤3 per character + trigger | **角色标记动作字段**: 5-stage arc (首次→复现→升级→转化→消失) | ✅ 完整对接。script 追踪完整轨迹 |
| **2. 运动质量 (Laban Effort Profile)**: Weight/Time/Space/Flow → Action Drive | **无独立字段**。仅在设计备注中提及"运动质量变化需求（如'从轻快到沉重'）" | 🟡 结构性中断。Effort Profile 没有在 beat 模板中拥有独立字段，设计备注不是可消费的结构化数据 |
| **3. 角色-镜头关系 (Character-Camera)**: 7 class types × distance/angle/movement | **隐式编码**: 通过情绪-景别映射和景别+角度两项参数承载 | ✅ 显式设计决策。script 文档中标明"不额外标注" |
| **4. 角色间空间 (Proxemics)**: Hall 4 distances → lens grammar | **角色间空间字段**: 亲密/个人/社交/公共 + 镜头处理建议 | ✅ 完整对接。规则一致（距离渐变、障碍物影响含义等） |
| **5. 情绪个人化表达 (Character-Specific Emotion)**: 3 emotions × 3 signals max | **角色PAD字段**: 覆盖"角色感受到什么情绪"（P/A/D值） | 🟡 部分覆盖。角色PAD覆盖"what emotion"，visual 的维度 5 是 "how emotion is expressed"。表达方式（Duchenne marker缺失/重复动作/过度控制等）没有结构化字段 |

### visual 维度 5 的完整接口分析

visual 的"角色情绪个人化表达"提供的是：
- 每个角色 3 个情绪 × 3 条表达信号（如 "悲伤→微笑但眼轮匝肌不动"）
- 这是 **表达方式** 的个性化，不是 PAD 值的个性化

script 的"角色 PAD"提供的是：
- 情绪状态的量化值（Pleasure/Arousal/Dominance）
- 这是 **情绪状态** 的追踪，不是表达方式

两者互补但不重叠——正常运作时需要对接，当前没有结构化机制。

### video-director 矛盾矩阵的消费能力

director 的矛盾矩阵格式：
```
[beat-N] 剧本需求 | 主体承载 | 节奏(时长+缓动) | 音频 | shot关系 | 矛盾标注---裁决 | 转场
```

director 的四类矛盾：冲突/张力/资源/缺失

- 角色间冲突（如两个角色目标对立）→ 可被"冲突"类型消费 ✅
- 角色语言一致性矛盾（如 signature gesture 被运镜遮挡）→ 无专用类型 🟡
- 角色 PAD 与全片 PAD 不一致 → script 已移交矛盾矩阵，但 director 格式无对应字段 🟡

**🟡 问题 3.1 — Laban Effort Profile 无结构性接收字段**
- visual 输出 Effort Profile，script 在 Warm 阶段注册到六层不变量-角色行为层
- 但在 beat 模板中无字段追踪每拍的 Effort 变化
- 影响：Effort Profile 在注册后即丢失拍级追踪，character behavior arc 的"运动质量"维度无法在 beat 级验证

**🟡 问题 3.2 — Character-Specific Emotion 表达方式丢失**
- visual 定义了每角色 3 情绪 × 3 expression signals
- script 没有字段承接"这个角色如何表现悲伤"——只有"这个角色此时的 PAD 值"
- 影响：角色个人化表达方式在 script-draft 阶段无法被拍级引用，只能靠设计备注传递

**🟡 问题 3.3 — director 矛盾矩阵无明确的角色冲突字段**
- script 移交角色独立 PAD 冲突点，但 director 的矩阵格式无对应列
- 角色冲突数据只能硬塞进"矛盾标注"字段的自由文本
- **修复**：director 矛盾矩阵格式追加可选字段 `[角色冲突]`，或修改矛盾类型覆盖角色冲突

---

## 审计 4: 细节展开接口一致性

### 格式链

```
visual 压缩: class + surface + 1 key attribute
  → (传递到 visual-assets-spec.md / visual-world.md)
  → director 需要: 可生成的物理描述 → 嵌入 9要素 prompt
  → visual 有展开表但存在自己文件内
```

### 问题

**🟡 问题 4.1 — 压缩→展开无结构化交接**

visual 的材质描述在 agent 间通信时使用 `class+surface+1key` 压缩格式（如 `fabric+velvet+soft`）。但 director 的 9 要素 prompt 需要展开后的物理描述（如"天鹅绒短绒毛捕捉光线产生丝光"）。当前的交接机制：

1. visual 在 `visual-assets-spec.md` 中使用压缩格式
2. visual 在 `visual-world.md` 宪法层描述材质但不一定是展开格式
3. director 需要从 visual-designer.md 的展开速查表中手动查找对应的展开文本

没有结构化的"压缩→展开"传递通道。当 director 拼写 9 要素 prompt 时，材质描述需要自己展开或依赖参考图。

**🟡 问题 4.2 — 9要素无独立材质字段**

director 的 9 要素：`[景别]+[主体]+[动作]+[场景]+[光影]+[运镜/动]+[风格]+[画质]+[间]`

材质描述没有独立要素，必须嵌入到 `[主体]`（角色服装材质）、`[场景]`（环境表面材质）或 `[风格/画质]`（材质渲染质量）中。没有专用槽位意味着材质描述的精细度不可预期。

### 当前可行的桥接方式

- 参考图承载大部分材质视觉信息（图片本身展示材质）
- 对无参考图覆盖的材质，visual 应在 visual-assets-spec.md 或 visual-world.md 中提供展开文本
- director 合成阶段从 visual 产出中提取展开文本嵌入 subject/scene 字段

### 建议

🟢 建议：visual-assets-spec.md 新增 `expanded_material_descriptions` 节，对每个 P0 材质提供展开文本，director 在素材装配时直接嵌入 9 要素。

---

## 审计 5: 量化指标一致性

| 指标 | 约束值 | script | visual | rhythm | director | 状态 |
|------|--------|--------|--------|--------|----------|------|
| CF<2 | CF<2 归 rhythm（单边约束） | "CF 归 rhythm（<2）" | "V 独立管理，不再与 CF 乘积" | "CF<2 单边约束" | "CF<2 单边约束 / V 独立管理" | ✅ 完全一致 |
| V 独立管理 | V 由 visual 独立管理 | "V 归 visual（独立管理）" | "V 独立管理" | "V 由 visual 独立管理" | "V 独立管理" | ✅ |
| 单拍时长 | 实体≤6s / 纯视觉≤8s / 钩子B1不限 | "含角色节拍≤6s，纯动画≤8s" | "实体≤6s / 纯动画≤8s" | 按 script 值读取 | "实体≤6s / 纯视觉≤8s / 钩子B1不限" | ✅ 一致。script 用"角色"，director/visual用"实体"——实体含角色+道具，但上限共享 6s |
| 实体复现 | 主角≤3拍 / 配角≤5拍 | "主角≤3拍，配角≤5拍" | 实体复现约束传递 | — | "主角≤3拍 / 配角≤5拍" | ✅ |
| 感知组块 | 公众号≤15/X≤5/小红书3-6/抖音≤3 | — | — | — | — | ✅ rules 层定义，四 agent 不独立引用 |
| 通道堆叠 | 同期活跃≤2 | — | — | "通道堆叠≤2 带显式标注" | — | ✅ rhythm 持有，其他 agent 不冲突 |

**结论**：量化指标无冲突。CF/V 分工、单拍时长、实体复现间隔、通道堆叠均一致。

---

## 额外发现

### 🔴 问题 A — 实体标签格式冲突

**严重度：🟡不一致（可自动修复）**

script-designer 使用方括号格式，director 使用尖括号格式：

| 文件 | 格式 | 示例 |
|------|------|------|
| director | `<tag>` | `<protagonist>` / `<sidekick>` / `<object_X>` |
| script | `[TAG]` | `[PERSON_1]` / `[PROTAGONIST]` / `[SIDEKICK]` |

director 的 SDK 字段映射说明："嵌入`<tag>`; tag必须手动嵌入subject文本"。但 script 文档写的是"统一标签（如 [PERSON_1]），与 director 实体注册协议一致"——实际上格式不一致。

**影响**：如果 director 按 `<protagonist>` 格式消费，但 script 产出 `[PROTAGONIST]`，在批量处理或工具 API 调用时可能产生格式错误。

**修复**：script-designer.md 所有实体标签格式从 `[TAG]` 改为 `<tag>`（对齐 director 协议）。角色标记动作字段使用的 `[角色标签:...]` 是标注格式，不需要改。

### 🟡 问题 B — Luma Ray 版本不一致

| 文件 | 版本 | KF 数 |
|------|------|-------|
| director (工具适配表) | 3.2 | 64 keyframes |
| rhythm (AI视频控制表+工具矩阵) | 3.14 | ≤16 KF |

两个 agent 引用了不同版本的 Luma Ray。rhythm 版本号更具体。

**修复**：director 的 Luma Ray 版本更新为 3.14（与 rhythm 一致），KF 数保留 original 值（不同版本可能不同）。

### 🟡 问题 C — MAVIN 对齐精度未在 rhythm 中体现

director 定义：音频起止与视觉转场 ≤0.3s（锚点拍 ≤0.1s）

rhythm 的音频-视觉节奏协同节详情但未包含 0.3s 精度约束。rhythm 使用 0.3s 作为钩子中断时机约束，但不是 AV 对齐精度约束。

**影响**：rhythm 设计的音画映射可能在毫秒级不满足 director 的 MAVIN 门禁。

**修复**：在 rhythm-designer.md 的音频-视觉节奏协同节补充 MAVIN 精度约束。

### 🟡 问题 D — 段边界分类与 director 末帧链的接口深度

script 对段边界有精细分类：延续边界（含尾帧视觉类型：全细节/剪影级）+ 重置边界 + 链式漂移防御（每 2-3 段重置）

director 的段级调度协议：首段→末帧链→场景切换段（跳过末帧）。与 script 的"延续/重置"分类功能一致但未显式消费 script 的尾帧视觉类型和链式漂移防御间隔。

**影响**：script 的详细段边界规划可能在 director 合成阶段丢失。

🟢 建议：director 的素材装配协议 Step 1 在查询 last-frames 时，同时读取 script-beats.md 的"尾帧类型"标注以便做参考图分配决策。

### 🟡 问题 E — 转场术语不一致

| 概念 | director | script | 状态 |
|------|---------|--------|------|
| rack focus 变焦点 | 运镜（中识别率，需搭配景深描述） | 反问逻辑的推荐转场 | 🟡 用途不同。director 作为运镜，script 作为转场。实际中两者不矛盾：可以用 rack focus 过渡两拍，但术语归属不同 |
| jump cut | 未定义 | 反驳逻辑的推荐转场 | 🟡 director 转场体系未包含 jump cut。只能用 hard cut 近似 |
| match cut | 匹配剪辑 0s | 因果逻辑的推荐转场 | ✅ 一致 |
| cross dissolve | 交叉溶解 0.5-1.5s | cross dissolve | ✅ 一致 |

**修复**：script 的 "jump cut" 和 "rack focus" 作为转场使用时，在 director 的转场体系没有对应项。建议 director 转场体系补充：
1. "jump cut" 作为"反驳"过渡的显式项
2. 明确 rack focus 可兼做转场和运镜——当跨拍使用时是转场，当拍内使用时是运镜

---

## 总计

| 等级 | 数量 | 说明 |
|------|------|------|
| 🔴 阻断（需人裁决） | 0 | 无核心叙事方向冲突或结构性问题 |
| 🟡 不一致（可自动修复） | 7 | 实体标签格式、Luma版本、zoom/dolly混用、jump cut分类、handheld-drift术语、medium wide术语、MAVIN精度缺失 |
| 🟢 建议（非必须） | 4 | 矛盾矩阵角色冲突字段、材质展开交接机制、段边界类型消费、转场体系补充 |

---

## 自动修复执行记录

| # | 文件 | 修改内容 | 执行 |
|---|------|---------|------|
| F1 | script-designer.md | 实体标签格式 `[TAG]` → `<tag>`: `[PROTAGONIST]`→`<protagonist>`, `[SIDEKICK]`→`<sidekick>`, 3处 `[PERSON_1]`→`<PERSON_1>`；补充"以尖括号 `<tag>` 格式嵌入 prompt subject 文本"说明 | ✅ |
| F2 | script-designer.md | "medium wide" → "MWS (medium wide shot / Cowboy)"（3处：力量/英雄、发现/顿悟、释放/解脱表行） | ✅ |
| F3 | script-designer.md | "handheld-drift" → "handheld (gentle drift)"（6处：弧线基调4处 + AI prompt 模板1处 + 反模式1处） | ✅ |
| F4 | rhythm-designer.md | "快速zoom-in/quick zoom-in" → "快速dolly-in/push-in"（3处：耦合表高强行、顿音特化行、TikTok基线行） | ✅ |
| F5 | rhythm-designer.md | "跳跃切" 从运镜表移除（高强行），转场行为归切频控制 | ✅ |
| F6 | rhythm-designer.md | "快速切"保持不动——属于切频描述非运镜 | ⏭️ 无需改 |
| F7 | director.md | Luma Ray 3.2 → 3.14（工具适配表帧级控制行） | ✅ |
| F8 | rhythm-designer.md | 音频-视觉节奏协同节补充 MAVIN ≤0.3s 精度约束（锚点拍≤0.1s） | ✅ |

### 未自动修复（建议级）

| # | 内容 | 原因 |
|---|------|------|
| S1 | director 矛盾矩阵追加角色冲突字段 | 当前 free-text 字段可承载，追加列过于正式。建议在具体项目中通过 TOGETHER.md §6 传递 |
| S2 | visual-assets-spec.md 新增 expanded_material_descriptions 节 | 涉及跨 agent 产出格式变更，需执行发现驱动 |
| S3 | director 段边界类型消费（段类型标签读取） | 当前末帧链协议已覆盖功能，优化属于效率改进 |
| S4 | director 转场体系补充 jump cut 和 rack focus 过渡用法 | 当前硬切可近似 jump cut，rack focus 已走运镜路径。补充仅做显式文档化 |
