# T005 血锁的一护 — 视觉资产规格

> 本文件定义角色规范、参考图使用、open question 清单、双 provider 适配、末帧资产与负向 prompt 规格。
> **规范来源声明**：角色形态规范以 `research.md` §1.1 官方文字描述（电击在线 85246，Aniplex 通稿原文）为**唯一依据**。参考图 001/002 未经目验（当前模型无视觉能力）——所有「仅参考图可见、文字未覆盖」的项在 §3 标为 open question（OQ-1…OQ-9），首生成后回校。
> 上游对齐：与 `director.md`（director 收口）+ 4 个 prompt 文件逐条核对；冲突处标注「与 director 收口冲突，待门 3 裁决」。
> 配套宪法：`visual.md`（六维/情绪/调色板/材质/锚点/排除/负面清单）。

---

## 1. 资产总览

| # | 资产名 | 类型 | 优先级 | 状态 | 依赖 | 存于 |
| --- | -------- | ------ | -------- | ------ | ------ | ------ |
| 1 | 血锁一护·完全形态 规范参考 | 角色 | **P0** | ✅ 官方图已入库（未目验）；规范文本块已定稿（§2.4） | 无（优先） | `assets/ref-images/`（001/002） |
| 2 | 血锁一护·变身前基底 规范 | 角色 | P0 | ✅ 纯文本规范（§2.2） | 无 | prompt 内 |
| 3 | 墨韵虚空 场景 | 场景 | P2 | **不产**（script 裁决：抽象 void 由 001/002 覆盖，防参考帧过密） | — | prompt 内（§2.5） |
| 4 | Seg1 末帧（段边界接续锚点） | 尾帧 | **P0** | 生成后提取 | Seg1 A/B 生成完成 | `assets/last-frames/` |
| 5 | 2C Cero 构图分镜概念图 | 分镜 | P1（可选） | 待产（figure-draftsman/director，M3） | 若 2C 首生成构图不成立 | `gates/storyboard-2C.md` + `assets/storyboards/` |

**无 AI 生图资产**：参考图 = 官方已下载图（非图像生成器产物），生图确认门 N/A（与 director §7 收敛门一致）。

---

## 2. 角色规范

### 2.1 血锁的一护（Kessa no Ichigo）— 完全形态（相位 B）

**官方文字依据（research §1.1 逐条）**：

| 官方要素 | 官方描述 | 规范裁决（text-based） |
| ---------- | --------- | ---------------------- |
| 基础状态 | 「虚の血を呼び覚まし、半虚化した」 | 保留一护的橙色头发、黑色死神装束；**非完全虚化（非全白面具）**——半虚化 |
| 卍解 | 「卍解し、斬魄刀と共に変化した究極の姿」 | 刀随形体而变（形变后形态 = [OQ-4]）；卍解瞬间有爆发感 |
| 角 | 「完全虚化を思わせる二本の角を戴き」 | **两根**、令人联想到完全虚化的角；形质文字未覆盖 = [OQ-1]，默认「large curved」 |
| 血锁灵压 | 「首・手・足には血鎖の霊圧が迸る」 | 颈、手（腕）、脚（踝）三处迸发血色锁链状灵压；链之形质（真链/能量流）= [OQ-3] |
| 能力 | 「霊圧・身体機能・反応速度、すべてにおいて新たな次元」 | 表现层：速度线拉满 + 时间停滞感（2B/2A），非新资产 |
| 设计 | 久保帯人描き下ろし、官方命名（第45话登场） | 官方形态——锚点可信度最高（放送中） |

**五特征辨识锚（P0，验收 7 项 = 双角/面具/链/发/装/刀/配色）**：

1. **双角**：两根，头部两侧顶出（曲度/长度/颜色/材质 = OQ-1）
2. **黑半虚化面具**：覆盖面部，哑黑硬壳质感（覆眼与否/纹理/能量线 = OQ-2；**黑，非白**为最高优先否定项）
3. **血锁锁链灵压**：颈 + 双手腕 + 双脚踝三处，自发光血红（形质 = OQ-3）
4. **卍解刀**：长刀，形变完成态（形变后外观 = OQ-4）；1C/2A 横置正手持，2B 前导
5. **不变基底**：橙色刺状长发 + 黑色死神装束（发型/装束在完全形态是否变化 = OQ-5）

**面部**：眼睛状态——2A 睁开血红辉光（虹膜色细节 = OQ-6）；1A–1C 面部被橙发/面具遮蔽（身体通道为主，面部次级）。

### 2.2 变身前基底态（相位 A，仅 1A）

**规范**：年轻男性，橙色刺状长发（垂落可遮面），黑色死神装束；**无角、无面具**；平静棕色虹膜（OQ-6 回校项）；颈/手/脚处血红锁链状灵压**在皮下明灭**（未出体，被压制）；深蹲蓄力姿态（G1）。

**M1 防过早全形态约束**：1A prompt 显式 `no horns, no mask, pre-transformation state`；参考图（H3 版）仅作发色/装束/色调/终态锚点，alignment 行声明 `NOT opening or closing keyframes`（与 director 收口一致 ✅）。

### 2.3 两相位一致性规则

- 相位 A→B 是**设计性状态递进**，非一致性错误（script 六层不变量）：橙发/黑装全程不变；角/面具/链辉强度/刀形态为递进变量。
- 跨段（Seg1→Seg2）：相位 B 全特征锁定 + 正手持姿态锁定（末帧三不变量，见 visual.md §7.4）。

### 2.4 双 provider 自足特征块（核心交付——provider-agnostic 规范文本）

> 用途：H3 版 = 参考图锚定 + 此文本复述；Seedance 版 = 纯文字锚定（**文本即全部依据，必须自足**）。此块为规范参考的软锚本体，同文本贯穿 4 个 prompt 文件（director 已内嵌等价措辞，A/B 实机前无需改动；若 OQ 回校修订，两方同步更新）。

**`[KESSA_Ichigo_FINAL]` — 血锁完全形态**：

```
A young man in his ultimate transformed state: long spiky orange hair,
a black shinigami-style robe, two large curved horns on his head,
a complete matte-black half-hollow mask over his face (black, NOT white),
blood-red chain-like spiritual energy blazing around his neck, wrists
and ankles, and a long transformed sword held horizontally at his side
in a formal ready stance.
```

**`[ICHIGO_BASE]` — 变身前基底**：

```
A young man with long spiky orange hair and a black shinigami-style
robe, with NO horns on his head and NO mask on his face
(pre-transformation state); blood-red chain-like energy faintly
flickering under his skin at his neck, wrists and ankles.
```

**Seg2 姿态复述块（接在形态块后，两 provider 共用）**：

```
continuing exactly from the locked ready stance: head raised, body
perfectly still and charged, the transformed blade held horizontally
at his side
```

### 2.5 墨韵虚空（场景规范，纯文本，无参考图）

```
a pitch-black ink-wash void, matte dark ink tendrils drifting and
pressing in from all sides, deep negative space, no ground, no walls,
no modern elements; the blood-red self-emitting glow of the chains
is the only light source
```

动态规则：1A 触须向角色收拢（压）；1B 被迸裂链辉撕开光缝；1C 起退至画幅边缘（被威压推开）；2B 向两侧飞掠；2C 被 Cero 吞没。飘落物 0 种 / 大气效果 ≤1 项（触须本身）——日系留白。

---

## 3. Open Question 清单（仅参考图可见、文字未覆盖）

> 每项含：问题 / 当前默认（已写入 prompt 的假设）/ 回校触发 / 裁决后动作。
> 回校手段：① 首生成后人工目检（H3 版输出 vs 001/002）② 人工直接查看 001/002（当前管线无视觉模型，需人）③ 未来接入视觉模型。
> **默认值与 director 收口 prompt 措辞一致**——首生成前不改动任何 prompt 文件。

| # | Open Question | 默认（prompt 现用） | 回校触发 | 裁决后动作 |
| --- | -------------- | -------------------- | --------- | ----------- |
| **OQ-1** | 双角形质：曲度/长度/颜色/材质（与面具同壳？骨白？黑？）/头顶位置 | 「two large curved horns」（黑色系，同面具质感） | 首生成 vs 001 对照 / 人工看 001 | 偏差 → 修订 `[KESSA_Ichigo_FINAL]` 角描述 + H3 alignment 行 + Seedance subject 行（四处同步） |
| **OQ-2** | 面具覆眼与否 + 纹理（纯黑？血红色能量沿线？骨质纹？） | 哑黑无缝硬壳 + 边缘微血红能量线；**M2 双可读写法**：`light shines through and around the eye region of the mask`（覆眼/不覆眼 2A 皆可读） | 2A 生成可读性 / 人工看 001 | 覆眼 → 维持双可读；不覆眼 → 可加虹膜描述（联动 OQ-6）；纹理偏差 → 修面具描述 |
| **OQ-3** | 血锁锁链形质：真金属链 / 能量链 / 锁链形态灵压团；粗细；是否离体悬浮 vs 贴身缠绕 | 「blood-red chain-like spiritual energy, chain-link form, self-luminous」（能量链，贴身缠绕三处） | 首生成 vs 001 对照 | 偏差 → 修链描述（颈/手/脚三处位置不变——script 不变量） |
| **OQ-4** | 卍解刀形变后形态：刀身形状/颜色/刃宽/刀镡/是否双刃/能量刃 | 长刀、银黑刀身 + 血红刃缘能量（「a long transformed sword」，不指定刀镡细节防过度约束） | 首生成 vs 001/002 对照 / 人工看图 | 偏差 → 修刀描述；刀为 P0 特征（末帧 7 项验收之一） |
| **OQ-5** | 完全形态下橙发/黑装是否变化（更长？掺黑？装束加层/破损？灵压衣纹？） | 橙发+黑装**完全保留**（不变基底假设） | 首生成 vs 001 对照 | 若官方形态有变化 → 修订形态块 + 更新 §2.1 五特征锚（橙色发色仍保留——research 明示「保留一护的橙色头发」） |
| **OQ-6** | 眼睛：2A 睁眼时虹膜色/辉光纹理（纯血红光？瞳孔结构？）；1A 基底态虹膜 | 血红辉光自眼区渗出（不写虹膜细节）；1A 默认棕色虹膜 | 2A 生成可读性 / 人工看 001 | 可读性不足 → 加「deep blood-red eyes」；虹膜结构偏差 → 修 OQ-2 联动项 |
| **OQ-7** | 002 内容验证：推测为第45话登场场景截图——是否确为血锁形态？能否作构图/色调辅锚？ | 按「场景辅锚」使用（H3 `<Picture 2>`）；**不作为形态身份主锚**（主锚 = 001） | 人工看 002 / 首生成 H3 双图对照 | 若 002 非血锁形态 → 从 H3 参考组移除（降为 1 图）或重新取图；更新 `_index.md` 用途列 |
| **OQ-8** | 皮肤/体表变化：半虚化是否改变肤色、体表有无非锁点能量纹/刻印 | 年轻肤色 + 锁点处皮下血红透光（SSS），无其他体表纹 | 首生成 vs 001 对照 | 偏差 → 修皮肤描述（P1，非验收 7 项） |
| **OQ-9** | Cero 色彩结构：黑核心+红缘 vs 红核心+黑缘；「黑红」比例 | 黑心红缘（`black-red Cero torrent`，black 在前） | 2C 生成观感（峰值可读性） | 若观感发闷 → 反转红心黑缘；属表现层（P1） |

**与 script M2 的关系**：OQ-2/OQ-6 即 M2 的 open 侧——director 已按「双可读写法」默认裁决并写入两版 prompt（一致 ✅）；OQ 机制 = 首生成目验后的正式回校通道。

---

## 4. 参考图使用（双 provider 对照）

| 资产 | H3（A 版） | Seedance（B 版） |
| ------ | ----------- | ----------------- |
| 001（1061×1500 竖，形态图，CDN 直链） | Seg1：`<Picture 1>` 主身份锚；Seg2：`<Picture 2>` 身份加强 | 不用（纯文本自足——A/B 对照设计） |
| 002（1920×1080 横，场景图，CDN 直链）[OQ-7] | Seg1：`<Picture 2>` 构图/色调辅锚；Seg2：`<Picture 3>` | 不用 |
| Seg1 末帧 | Seg2：`ref_image_0`（data URI，I2VA 首帧强条件化，Tier 0） | Seg2：`reference_image`（弱锚定，无首帧字段）+ 姿态文本复述 |

**参考密度合规**：每段 ≤3 图（H3）/ 1 图（Seedance Seg2）——KeyFrame-Compass ≤1 帧/实体最优原则的放宽说明：001/002 为**官方**身份锚（最高可信度），且 H3 版双图一主一辅（形态 vs 构图/色调），非同实体堆叠；Seg2 末帧 = 同实体延续锚（Tier 0 不计槽限）。防过密裁决维持：不另加场景图。

---

## 5. 末帧资产规格（Seg1 → Seg2）

- **产出**：`assets/last-frames/T005-seg1-winner-lastframe.png`（extract-lastframe `--time-offset 0.5` → 4.5s 帧，落在 1C 末 1.8s 落定 hold 窗口内）
- **质量门禁（提取后先过目再进 Seg2，P0）**：
  1. 角色居中（±10% 内）
  2. 双角 + 黑面具 + 横置刀 + 颈/手/脚链 全入画（7 项验收同 director §6）
  3. 光照稳定（无频闪/无辉光跳动）
  4. 构图干净（无遮挡/无多余元素）
  5. 无运动模糊
- **不过门禁**：改 `--time-offset 0.3` 重截（仍在 hold 窗口）；仍不过 → 该候选作废（回 A/B 另一候选或重生成段 1，3 轮上限）
- **注入**：H3 = ref_image_0 强条件化；Seedance = reference_image + subject 复述（§2.4 姿态块）
- **清理**：选题结束即清理 `assets/last-frames/`（工作台层）

---

## 6. 分镜确认门（Storyboard Gate）状态

| 拍 | P0 关键拍判定 | 本任务处理 |
| ---- | ------------- | ----------- |
| 1A（钩子拍 B1） | 表格标准=必须 | **降级为文本足够**——钩子 = 压抑 hold（V=2、无构图风险、单主体负空间居中）；本任务为 A/B 压测，生成即预览，不前置分镜图。若人要求生成前帧预览 → 以 001/002 + §2.4 文本块走图像生成器出 1C 帧（见下） |
| 1C（规范参考拍） | 必须 | **由 001 官方形态图事实承担**——规范参考帧即官方图的时序复刻；生成前帧预览 = 用 001/002 作参考图出「1C 落定帧」概念图（可选，非阻塞） |
| 2C（情绪转折/PAD 峰值） | 必须 | **P1 可选**（与 script 一致）：M3 构图风险（Cero 轰穿镜头）→ 若 2C 首生成构图不成立，figure-draftsman 补产 `gates/storyboard-2C.md`（光束冲向镜头、迅速放大充满画幅、墨韵+血红；9:16 不适用——本片 16:9） |

**结论**：本片不设 P0 阻塞性分镜门（与 script 视觉资产需求 + director 收口执行计划一致——共 3 次生成、无分镜前置步骤）。若门 3 要求生成前帧确认 → 唯一候选帧 = 1C 落定帧（图像生成器 + 001/002 参考），走生图确认门 `gates/image-gen-1C-frame.md`。

---

## 7. 负向 prompt 规格

**Seedance（`--negative-prompt`，director 收口版，dry-run 已验证）**：

```
photorealistic rendering, 3D shading, white full-face mask, modern elements,
on-screen text, subtitles, UI, watermark, multiple characters, pink candy
colors, low contrast, gray midtones, whip pan, excessive camera shake,
motion smearing on static frames, character breathing movement, cloth wind
movement, ambient particle animation during still frames, micro-movement in
locked shots
```

- 末 4 项 = 静帧保护（⚠️ 其中微动否定与宪法默认「静止中的微动」冲突 = C1，待门 3 裁决；执行跟 director）
- Seg2 可追加：`character appearance changing between shots`
- 视觉侧 per-entity 约束（no white mask / no extra characters / no face swapping / 1A: no horns no mask）已全部包含于上表或正向声明中，无新增

**H3（无 negative 字段 → 正向替代，director 已执行）**：`black not white` / `clean, sharp frame without motion blur` / `no horns... no mask`（1A 显式）

**图像生成器（若产 1C 帧/2C 概念图）**：不支持负向 → 正向约束（`matte black mask, not white` / `centered composition, all elements in frame`）

**迭代策略**：首轮默认 → 特定缺陷追加 1-2 词 → 超 8 词改正向约束（遵循负向 prompt 体系）。

---

## 8. 角色语言在 Reference Lock 中的插入（Seedance 版）

```
Preserve: long spiky orange hair, black shinigami robe, two curved horns,
matte-black mask, blood-red chains at neck/wrists/ankles, transformed
blade.
Behavioral lock: G1 head-lowered charge (pre-transform only) → G2
horizontal-blade formal ready stance (locked from 1C, blade-leading in 2B)
→ G3 blood-red eye glow (2A); Effort: Wring hold (1A) → Slash burst (1B)
→ Press lock (1C) → Dash charge (2B); Camera: low-angle MS-MWS,
static to slow push-in, final still hold.
Scene: pitch-black ink-wash void, blood-red self-emit only.
Camera: per sub-beat (see visual.md §8).
```

---

## 9. 调度与验证

### 9.1 产出序列（质量感知调度）

```
Step 1: 角色规范文本块（§2.4，本文件已定稿）→ 已内嵌 4 个 prompt 文件 ✅
Step 2: 001/002 官方图（已入库，未目验）→ H3 Seg1 双图 / H3 Seg2 双图加强
Step 3: Seg1 A/B 生成（director 执行清单 Step 1）
Step 4: 末帧提取 + 门禁（§5）→ Seg2 生成（Step 4）
Step 5: 首生成回校 OQ-1…OQ-9（§3）→ 偏差项修订（两处以上同步：形态块 + 对应 prompt 文件 + 本文件）
Step 6: （可选，门 3 要求时）1C 落定帧 / 2C 概念图 → 生图确认门 → 图像生成器
```

### 9.2 验收 7 项（末帧 vs research §1.1，与 director §6 维度 1 一致）

双角（两根/形质）✓ / 黑半虚化面具（非全白）✓ / 颈·手·脚血锁锁链 ✓ / 橙发 ✓ / 黑装 ✓ / 刀横置 ✓ / 配色（黑底+血红+橙）✓

### 9.3 闭环

VLM/目检问题定位 → 仅重生成问题段（recall-first，3 轮上限）→ OQ 坐实偏差 → 更新规范参考 + spec §3 裁决列 → 广播 video-director（触及参考素材来源/优先级时交叉读 peer 文件）。

### 9.4 跨题复用

T003 资产（Yhwach/IchigoTS 双刀形态）不复用——血锁一护为全新官方形态（形态不兼容）；T003 可复用项 = 风格验证结论（`Bleach final-chapter aesthetic` 风格词过版权过滤器先例，M5 安全区）。
