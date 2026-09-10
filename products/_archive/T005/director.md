---
unit: director
title: 导演收口
follows: [script, visual, rhythm]
gate: 是
层: l1
---

# 导演收口 · T005 可执行生成方案

> 状态: 完成

## ① 简层

把四条线的设计收口成可执行生成方案：A/B 对照（H3 多图参考 vs Seedance 纯文本）× 2 段各 5s；M1–M6 全裁决；产出 4 个机器可读 prompt 文件 + 末帧接续规范 + A/B 执行清单。

## ② 思考

### 自报 · video-director

**我理解的方向**：10s 一次呼吸的变身奇观——压抑 hold（1.2s）→ 锁断变身（2.0s）→ 正手持锁定（1.8s，时间停滞）→ 睁眼点燃（1.0s，时间停滞）→ 突进（2.0s）→ Cero 轰穿（2.0s，末 0.5s 吞没 hold）。收口为**可执行生成方案**：`director.md`（矛盾矩阵 M1–M6 全裁决 + 收敛门 + 执行清单）+ 4 个机器可读 prompt 文件（H3 Seg1/Seg2、Seedance Seg1/Seg2，全部 dry-run/解析全链路验证）。

**关键裁决**：

- **工具**：A 版 = H3（`-p autodl_comfyui`，workflow `lightx2v_v5`，768p横，5s，¥0.01/s 促销）；B 版 = Seedance mini（16:9，5s，纯文本自足——按任务设定 B 版不用参考图，A/B 对照的是「参考图锚定 vs 特征描述」）。Seg2 跟随赢家 provider，共 3 次生成。
- **H3 输入模式**：Seg1 = T2VA + 多图参考（2 张官方 CDN 直链 = **终态身份参考，非关键帧**——alignment 行显式 `NOT opening or closing keyframes`，M1 裁决落点）；Seg2 = I2VA（Seg1 赢家末帧 = ref_image_0，`For the target video, at 0.00 seconds ... is fully referenced`）。⚠️ 执行发现：本 CLI 的 H3 解析器按行切块，**三核心字段值必须各占单行**（实测，已写入 prompt 文件头注释）；Ref2VA 六段式不被 CLI 消费，不采用。
- **M2 默认裁决**：面具眼部写法 `light shines through and around the eye region of the mask`——覆眼与否皆可读，首生成目验回校。
- **M6 = 门 3 关注项**：A/B 两版若均不能 5s 内干净推进三态 → 门 3（压抑独立成拍或延长 Seg1）。
- **音频**：H3 原生音频按三字段生成（non_diegetic_music 按 genbgm 目标风格代拟）；最终 BGM 一律 genbgm 自产 + `ai edit` 混入（§1 红线）。Seedance 自动环境音可留作物理声层。
- **末帧接续**：H3 = I2VA 首帧条件化（强）；Seedance 当前适配器**无首帧字段** → 末帧作 reference_image 锚定 + 文本复述（弱），退法 = 纯文本复述 + 接缝评估。extract-lastframe `--time-offset 0.5`（落 1C 末 1.8s hold 窗口）。data URI 假设已 dry-run 验证装配链路，**网关接受度待 Seg2 生成前 dry-run 再确认**。

**我给三 designer 的确认/回写**：段边界 5.0s 延续边界 ✅ 采纳（三不变量：形态锁定/血红稳定辉光/构图居中无运动模糊）；实体标签 `<Ichigo>` ✅ 采纳（prompt 文本不写角色名，M5）；锚点拍 = 1C 末帧/2B/2C ✅ 确认为叙事节奏锚点；script 约束假设表 6 项 → M1/M5 已裁决、M2 默认裁决、M4 确认、M6 门 3 关注、段边界/末帧策略采纳。**待 rhythm**：CL 标定 + BGM 设计（我按 PAD 映射代拟了 H3 音频字段，genbgm 出片后回校）；**待 visual**：形态规范以 research §1.1 为准已采纳，参考图首生成回校机制保留。

**残余风险（P1，不阻塞）**：① visual-world/visual-assets-spec/rhythm-curve 三文档缺失（§2.2/§2.3 空白）→ 我以 script-beats 六层不变量 + research §1.1 为 interim 源收口；② 参考图内容未目验（IaD 🟡→放行）；③ Seedance 版成本未实测；④ H3 data URI（~1–3MB）网关接受度待 Seg2 dry-run 验证。详见 `director.md` §0/§7。

---

> 2×5s · 16:9 · 纯视觉无旁白无字幕 · 宣泄弧（压抑→觉醒→爆发，止于 Cero 峰值）
> A/B 策略：Seg1 = H3 多图参考（768p横）vs Seedance（16:9 mini，纯文本自足）；赢家末帧 → Seg2 接续；共 3 次生成。
> 本文件为收口方案；机器可读 prompt 已拆为 4 个文件（§3/§4 附全文），命令可直接复制。

### 假设与未锚

- 假设：见本层各「[假设需生成前验证]」标注；未锚：末帧接续效果以生成验证为准（5.2/5.3）。

### grill 记录

## ③ 内容详情

#### 0. 工具决策与上游约束确认（Warm）

##### 工具选择与约束广播

| 约束 | H3（A 版） | Seedance（B 版） |
| ---- | ---- | ---- |
| provider 切换 | `-p autodl_comfyui`（model_config 名 `autodl_comfyui`；非 `minimax_h3`） | `-p seedance`（默认） |
| 工作流/档位 | `--model lightx2v_v5`（minimax_h3_lightx2v_v5 多图参考） | `--model mini`（doubao-seedance-2-0-mini） |
| 时长上限 | 1–10s（本设计 5s ✓） | 4/5/6/8/10/12/15s 合法值（本设计 5s ✓） |
| 分辨率 | `--resolution 768p横`（9 档预设） | 无 resolution 参数；画幅由 style 行推断 → 必须 16:9（style 不写 portrait/9:16/竖屏） |
| 参考图 | ref_image_0 **必填** + ref_image_1..8（共 1–9 张；URL 或本地→data URI） | reference_image 0–9 张（锚定角色/风格/构图，**非首帧条件化**） |
| 负向提示 | 本 workflow 无 negative 字段 → **正向约束替代**（写入描述：black not white / clean sharp frame） | `--negative-prompt` 参数 → 请求体 `negative_prompt` |
| 音频 | 原生生成（overall_soundscape + non_diegetic_music 入 prompt） | `generate_audio=True` 默认自动环境音；BGM 由 genbgm 自产后 `ai edit` 混入 |
| 成本 | ¥0.01/s（768p 促销价）→ 5s ≈ **¥0.05**（CLI 显示 Est. cost） | 实测后回填（压测数据） |
| 凭证 | AUTODL_API_KEY（.env 已配） | 火山凭证（.env 已配） |

##### H3 输入模式裁决（Warm 广播：script + visual）

- **Seg1 = T2VA + 多图参考**：2 张官方 CDN 直链 = 终态身份参考（非关键帧）。[M1 裁决] 视频**不从**参考图状态开场——alignment 行显式声明「NOT opening or closing keyframes」，形态推进由 prompt 时序驱动（1A 无角无面具 → 1B 变身 → 1C 达到参考图形态）。
- **Seg2 = I2VA**：Seg1 赢家末帧 = `ref_image_0`（Tier 0，不计 9 图槽限）；关键帧对齐指令（H3 格式）：`For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.`
- **CLI 解析约束（实测 2026-08-24，硬约束）**：`h3_prompt.parse_fields` 按行切块——三核心字段值必须**各占单行**（字段值内换行/含「词: 」开头的行会提前 flush 丢内容）；alignment 行须含 `For the target video, at 0.00 seconds` 或 `How the reference pictures align` 才会被提升到 prompt 顶部。4 个 prompt 文件已按此写入并用 `--dry-run` 全链路验证。
- Ref2VA 六段式（subject_definitions/retention_analysis…）本 CLI 解析器**不消费**（只取三核心字段）→ 不采用，身份描述并入 integrated_multimodal_description。

##### 上游文档缺口（⚠️ 残余风险，P1）

`visual.md` / `exec/visual-assets-spec.md` / `rhythm.md` **不存在**（TOGETHER §2.2/§2.3 空白，§3 仅 script 自报）。director 以 `script.md`（六层不变量 + PAD/CL 粗估 + 各拍 AI prompt 指令 + FreeLOC 锚点）+ `research.md` §1.1 官方形态拆解 + TOGETHER §1 锁定方向为 interim 事实源继续收口。影响：CL 未 rhythm 标定、BGM 设计未 rhythm 出具（§3 H3 音频字段按 script PAD→音频映射代拟，genbgm 出片后回校）、视觉宪法缺位（以六层不变量代）。**非阻塞**（§1 全 ✅、§3 无 🔴）；若 visual/rhythm 后续补齐与本文件冲突 → 重走收敛门。（后记：visual/rhythm 已于 18:01/18:03 补齐，P1 残余风险解除；协作载体 TOGETHER.md 已拆解为本项目各单元文件——`goal.md` + 各单元 ①②③end；各单元文件按 unit id 命名（research/script/visual/rhythm/director.md），执行对象在 `exec/`，见 `gates/gate3-design-alignment.md` 与 `ai-video/workbench.md`。）

#### 1. 矛盾矩阵收口（M1–M6）

| # | 矛盾 | 裁决 | 落点 |
| --- | ---- | ---- | ---- |
| M1 | 参考图=血锁完全形态，1A 需变身前 | **裁决采用**：Seg1 描述 1A 显式 `no horns, no mask, pre-transformation`；参考图只作发色/装束/色调/终态锚点；alignment 行声明非开场关键帧 | H3 Seg1 [Shot 1] + Seedance seg1 subject 开头 |
| M2 | 面具眼部未目验，2A「睁眼血光」可读性 | **默认裁决**（两态皆可读）：写成 `blood-red light shining through and around the eye region of the mask`（光自面具眼区渗出，覆眼与否皆可成立）；首次生成后目验回校 | H3 Seg2 [Shot 1] + Seedance seg2 subject |
| M3 | Cero「轰穿镜头」构图风险 | 正向约束写入：`rushing directly at the camera lens, growing rapidly and punching through the frame until the entire image is filled`；P1 分镜概念图（figure-draftsman）**可选非阻塞**，若 2C 构图不成立再补 | H3 Seg2 [Shot 3] + Seedance seg2 subject 末 |
| M4 | 10s 压抑蓄力仅 ~1.2s | **rhythm 确认**：宣泄弧+低 D（被困/压制）+低频 hold，不做长热身；1.2s hold 为钩子 hold（≥1s ✓），靠「形态跳变幅度」而非时长蓄力 | 全部 |
| M5 | 版权过滤器（T003 教训：特征组合触发） | **执行记录**：两版 prompt 均用特征描述、不写角色名（Ichigo/Kira 等不入 prompt 文本）；style 保留「Bleach final-chapter aesthetic」词（T003 先例通过）；拦截行为 = 压测数据，写入日志 | §6 日志模板「拦截事件」列 |
| M6 | 单次 5s 内三态变身推进不确定 | **门 3 关注项**：prompt 已做三态时序串联 + 终态参考锚定 + 末 1.8s 落定 hold；A/B 两版若**均**不能干净推进三态（跳态/停滞/回退）→ 触发门 3：压抑独立成拍或延长 Seg1（改 7+3 或 3+2+5 结构） | 验收维度 #2 |

**品味否决**：未触发。
**叙事节奏锚点拍**：① 1C 末帧（5.0s，段边界接续锚点）② 2B 突进（速度峰值）③ 2C Cero 释放（全片唯一情感着陆）。
**[间] 标注（非零）**：1A hold 1.2s（压抑）/ 1C 末 1.8s 静止落定（时间停滞=段边界锚帧）/ 2A 静帧 1.0s（点燃）/ 2C 末 0.5s 吞没 hold（释放）。
**段边界（5.0s，延续边界）三不变量声明**：形态锁定（正手持+刀横置）/ 血红自发光稳定（无频闪）/ 构图居中且无运动模糊。

#### 2. 实体标签注册表

| 标签 | 实体 | 相位 | 规范参考 |
| ---- | ---- | ---- | ---- |
| `<Ichigo>` | 黑崎一护 / 血锁的一护（唯一角色） | A：压抑/变身前（0–1.2s，无角无面具，橙发+黑装） | 无参考图，prompt 基底描述 |
| `<Ichigo>` | 同上 | B：血锁一护完全形态（1C 起，双角+黑半虚化面具+颈/手/脚血锁锁链+卍解刀） | 子拍 1C（3.2–5.0s，GroundShot）；参考图 001+002 |

注意：`<Ichigo>` 为内部标签；**prompt 文本不出现角色名**（M5）。参考图未目验——形态规范以 research §1.1 官方文字为准，首生成后回校。

#### 3. H3 三核心字段 prompt（任务 1）

参考图：2 张官方 CDN 直链（不带 `?x=` 参数，2026-08-24 实测 GET 200；HEAD 不支持属 CDN 行为，服务端抓取用 GET 无碍）：

- `<Picture 1>` = `https://cimg.kgl-systems.io/camion/files/dengeki/85246/a4efdd2f969559e8b1c92e99f32ded48e.jpg`（001，1061×1500 竖，形态图 → 主身份锚）
- `<Picture 2>` = `https://cimg.kgl-systems.io/camion/files/dengeki/85246/a3fb5ed13afe8714a7e5d13ee506003dd.jpg`（002，1920×1080 横，场景图 → 构图/色调辅锚）
- **Seg2 额外**：`ref_image_0` = Seg1 赢家末帧（本地 PNG → CLI 自动转 data URI；[假设需生成前验证] 见 §5.2）。此时官方图顺延为 `<Picture 2>`/`<Picture 3>`。

##### 3.1 Seg1（文件：`exec/video-prompt-h3-seg1.md`，已 dry-run 验证）

```text
How the reference pictures align with the target video — Picture 1 and Picture 2 are official identity references for the target FINAL form (the horned, masked, blood-chain state); they are NOT opening or closing keyframes: the video opens in a pre-transformation state with no horns and no mask, and reaches the form shown in Picture 1 and Picture 2 only at the end of the final shot.

integrated_multimodal_description: [Shot 1] 2D-animated, high-contrast cel-shaded anime style, a medium low-angle shot frames a young man in a deep crouch with his head lowered and long orange hair falling over his face, wearing a black shinigami-style robe, with no horns on his head and no mask on his face in this pre-transformation state, inside a pitch-black ink-wash void where dark ink tendrils press in from all sides; blood-red chain-like spiritual energy flickers faintly and pulses under his skin at his neck, wrists and ankles like something caged, and his body trembles slightly with suppressed breathing; the camera holds a static shot with an almost imperceptible push in. [Shot 2] At 00:01.200, the shot cuts to the awakening: the blood-red chains erupt and shatter outward from his neck, hands and feet, a black half-hollow mask crawls rapidly across his face as he rises, two horns push out of his head, anime speed lines appear around him, and the long blade in his hand glows and begins to transform in the same instant; the camera drifts with a gentle handheld sway and pushes in. [Shot 3] At 00:03.200, the shot transitions to the completed form matching the character in Picture 1 and Picture 2: two full curved horns, a complete black mask that is black not white, the blood-red chains fully blazing at neck, wrists and ankles, the transformed blade held horizontally at his side in a formal ready stance, his head raised, his body still and charged with power; the ink-wash void and blood-red glow hold, the camera finishes a slow push in and holds a static shot for the final 1.8 seconds, ending on a clean, sharp frame without motion blur.

overall_soundscape: A low pressure rumble presses from all directions inside a near-silent void, then the blood-red chains creak and strain under tension before snapping and bursting outward with a sharp crack, the air tears as the black mask spreads across the face, and anime speed lines add a high whoosh of displaced air, ending in a deep resonant hum as the body locks into the ready stance.

non_diegetic_music: A low pulsing ostinato at a slow tempo with sustained deep strings underneath, gradually building in volume through the middle of the video and reaching a full crescendo exactly as the final pose locks, no vocals.
```

结构说明：alignment 行（1 行，终态参考声明）→ 三核心字段（各 1 行，含 [Shot 1/2/3] 时间线与 `<Picture 1/2>` 引用）；`At 00:01.200` / `At 00:03.200` = 1B/1C 切点（script.md 子拍边界 1.2s/3.2s）。无对白（不出现 `<d>`）。非 H3 负向：以正向约束替代（`black not white` / `clean, sharp frame without motion blur`）。

##### 3.2 Seg2（文件：`exec/video-prompt-h3-seg2.md`，已 dry-run 验证 data-URI 参考图路径）

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

How the reference pictures align with the target video — Picture 1 is the last frame of the previous segment, showing the completed form in the locked horizontal-blade stance; Pictures 2 and 3 are official identity references of the same character; keep the character, colors, mask, horns, chains and pose identical to Picture 1 from the start.

integrated_multimodal_description: [Shot 1] 2D-animated, high-contrast cel-shaded anime style, the shot begins on a close-up of the eye region of the black mask worn by the man shown in <Picture 1>, who remains in the exact locked stance of <Picture 1> — two full curved horns, complete black mask that is black not white, blood-red chains blazing at neck, wrists and ankles, the transformed blade held horizontally at his side, head raised — inside the pitch-black ink-wash void with its blood-red glow; both eyes open as a deep blood-red light shines through and around the eye region of the mask, and the whole figure holds a still, time-stopped pause while the chains pulse once; the camera holds a static shot then pulls back with small amplitude at slow speed to reveal the full figure, still held. [Shot 2] At 00:01.000, the shot cuts to the charge: the man lunges straight toward the camera, blade leading, full anime speed lines streaking to the frame edges, strong motion blur on the surroundings while his form stays sharp, the ink-wash void whipping past on both sides; the camera pushes in rapidly at fast speed as he closes the distance, the angle rising from low to eye level. [Shot 3] At 00:03.000, the shot transitions to the release: a massive black-red Cero torrent erupts and rushes directly at the camera lens, growing rapidly and punching through the frame until the entire image is filled with black and red ink-wash energy, the figure partially visible inside its own discharge, then the frame holds for the final 0.5 seconds with the energy fully filling the screen.

overall_soundscape: A low resonant hum with a single deep pulse of the chains in the still opening, then the sharp crack of displaced air as he lunges, a high tearing whoosh of speed lines through the middle second, and finally a massive roaring boom of black-red energy surging past the lens that swallows all other sound.

non_diegetic_music: The low pulsing ostinato carries from the previous segment to a peak with driving percussion over the first three seconds, then cuts abruptly to a single sustained low tone that decays into near-silence as the frame fills with the energy discharge, no vocals.
```

结构说明：双 alignment 行（I2VA 首帧全引用 + 参考图角色声明）→ [Shot 1] 0–1.0s 点燃静帧（eye-region 起幅→极缓 pull-out 出全形态，M2 写法）/ [Shot 2] 1.0–3.0s 突进 / [Shot 3] 3.0–5.0s Cero 轰穿（M3 正向约束 + 末 0.5s 吞没 hold）。切点 00:01.000 / 00:03.000 = 子拍 2A/2B/2C 边界。

**音频装配裁决**：H3 原生音频会按字段生成。BGM 红线（`goal.md` ①/②）：最终 BGM = genbgm 自产。执行：H3 的 `non_diegetic_music` 按 genbgm 目标风格代拟（低脉冲 ostinato → 峰值 → 瞬寂低频坠落），使 H3 内置音乐垫与后续 genbgm 同形；混音时（`ai edit`）若 H3 音乐垫可用则保留为环境+音乐垫，冲突则 `ai edit mute` 去音轨、以 genbgm BGM + 重抽环境声替代。Seedance 版同理（自动环境音可留作物理声层，BGM 一律 genbgm）。

#### 4. Seedance 六要素块 prompt（任务 2，16:9 mini，纯文本自足）

CLI 只解析 `- **scene/subject/camera/lighting/style**` 五行（值单行）；audio 约束并入 style 行尾；负向走 `--negative-prompt`。已 dry-run 验证：`ratio: 16:9`、无 9:16 触发词、无参考图入请求体。

##### 4.1 Seg1（文件：`exec/video-prompt-seedance-seg1.md`）

```text
- **scene**: A pitch-black ink-wash void, dark ink tendrils drifting and pressing in from all sides, deep negative space with no ground or walls visible; one single continuous five-second transformation sequence: oppressive hold for the first 1.2 seconds, then chains shattering and mask spreading from 1.2 to 3.2 seconds, then the completed form locked in a formal ready stance from 3.2 to the end. No on-screen text, no UI, no modern elements.
- **subject**: A lone young man with long spiky orange hair and a black shinigami-style robe. Opening (0-1.2s): pre-transformation state with NO horns and NO mask, crouched low, head lowered, orange hair falling over his face, blood-red chain-like energy faintly flickering under his skin at his neck, wrists and ankles, body trembling slightly as if caged and pressed down. Middle (1.2-3.2s): the blood-red chains burst and shatter outward from neck, hands and feet, a black mask crawls across his face (a black half-hollow mask, NOT a white mask), two horns push out of his head, anime speed lines appear, and the long blade in his hand glows and transforms as he rises. End (3.2-5s): completed form with two full curved horns, the complete black mask, chains fully blazing at neck, wrists and ankles, the transformed blade held horizontally at his side in a formal ready stance, head raised, body perfectly still and charged, holding the pose until the very end on a clean, sharp frame with no motion blur.
- **camera**: Low-angle medium shot; the opening sits on a locked static frame with an almost imperceptible push-in; during the transformation the camera drifts with a gentle handheld sway and a quickening push-in; then a slow push-in settles into a completely static hold for the final 1.8 seconds. No whip pans, no crane, no fast spin.
- **lighting**: Near-pitch-black ink void lit only by self-emitting blood-red glow — first faint at the chains, then stronger from the transforming blade, then full from the complete chain system; deep shadows, very high contrast, blood-red as the single light source and accent color over the black.
- **style**: 2D anime cel shading, final-chapter Bleach aesthetic, sharp line art, ink-wash texture, high contrast, deep focus, 16:9 landscape; no dialogue, no on-screen text, no subtitles; ambient audio only (low rumble, chain cracks, whoosh); keep breathing and cloth motion minimal during the final still hold so the locked frame stays clean.
```

##### 4.2 Seg2（文件：`exec/video-prompt-seedance-seg2.md`）

```text
- **scene**: The same pitch-black ink-wash void with its blood-red glow, continuing exactly from the final frame of the previous segment; one single continuous five-second sequence: a still ignition pause for the first 1 second, then a charge straight at the camera from 1 to 3 seconds, then a Cero torrent filling the frame from 3 to the end. No on-screen text, no UI.
- **subject**: The same lone young man from the previous segment in his completed transformed state — two full curved horns, a complete black mask (black, not white), long spiky orange hair, black shinigami-style robe, blood-red chains blazing at neck, wrists and ankles, the transformed blade held horizontally at his side — continuing EXACTLY from the locked ready stance of the previous segment's final frame, head raised, still. Opening (0-1s): both eyes open with a deep blood-red light shining through and around the eye region of the mask, the whole figure holds a still time-stopped pause, and the chains pulse once. Middle (1-3s): he lunges straight toward the camera, blade leading, full anime speed lines, strong motion blur on the surroundings while his form stays sharp, the ink void whipping past on both sides. End (3-5s): a massive black-red Cero torrent erupts and rushes directly at the camera, growing rapidly until the entire frame is filled with black and red energy, the figure partially visible inside its own discharge, holding the fully filled frame for the final 0.5 seconds.
- **camera**: Starts on a close-up of the mask's eye region, static, then a very slow pull-out reveals the full figure; then a rapid push-in with tracking as he charges toward the lens, the angle rising from low to eye level; then a static frame with a slight recoil as the energy hits, holding on the filled frame until the end.
- **lighting**: The blood-red eye glow opens the shot against the dark ink void; then the charging figure lit by his own blazing chains and streaking speed lines; finally the frame flooded by the self-luminous black-red Cero energy, the brightest moment of the sequence.
- **style**: 2D anime cel shading, final-chapter Bleach aesthetic, sharp line art, ink-wash texture, high contrast, deep focus, 16:9 landscape; no dialogue, no on-screen text; ambient audio only (hum, whoosh, roaring energy); the character must remain identical to the previous segment — same two horns, same black mask, same orange hair, same black robe, same chains.
```

##### 4.3 负向提示（两版共用，`--negative-prompt` 参数）

```text
photorealistic rendering, 3D shading, white full-face mask, modern elements, on-screen text, subtitles, UI, watermark, multiple characters, pink candy colors, low contrast, gray midtones, whip pan, excessive camera shake, motion smearing on static frames, character breathing movement, cloth wind movement, ambient particle animation during still frames, micro-movement in locked shots
```

（末两项 = 止め絵静止帧保护，静止帧负向优先级最高；Seg2 可追加 `character appearance changing between shots`。）

#### 5. 末帧接续规范（任务 3）

##### 5.1 extract-lastframe 用法

```bash
# 段 1 赢家视频生成后，立即执行（Hard Rule 2：末帧提取为硬性要求，路径不存在→阻塞 Seg2）
uv run --directory scripts ai extract-lastframe \
  <outputs/段1赢家_task_id>.mp4 \
  -o /home/aifeier/org-dev/bip/outgiving/ai-video/projects/T005/assets/last-frames/T005-seg1-winner-lastframe.png \
  --time-offset 0.5
```

- `--time-offset 0.5`（默认值）= 距片尾 0.5s 截帧 → 落在 1C 设计的**末 1.8s 落定 hold 窗口内**（4.5s 帧：姿态已锁定、无运动模糊、辉光稳定）。若目检 4.5s 帧有运动模糊/辉光频闪 → 改 `--time-offset 0.3`（仍在 hold 窗口内）重截。
- 命名：`{project}-seg1-winner-lastframe.png`，存 `assets/last-frames/`（工作台层，选题结束即清理）。
- **末帧质量门禁（提取后先过目，再进 Seg2）**：角色居中 / 双角+面具+横置刀全入画 / 光照稳定（无频闪）/ 构图干净无遮挡 / 无运动模糊。不过 → 该段 1 候选作废（回 A/B 另一候选或重生成段 1，3 轮上限）。

##### 5.2 末帧注入 Seg2：provider 路径对照

| 路径 | H3（`-p autodl_comfyui`） | Seedance（`-p seedance`） |
| ---- | ---- | ---- |
| 末帧角色 | **ref_image_0**（`-r` 第一个，本地 PNG → CLI `resolve_ref_uris` 自动转 data URI） | reference_image（`-r` 本地 PNG → data URI） |
| 条件化强度 | **强——I2VA 首帧条件化**：alignment 行 `For the target video, at 0.00 seconds ... <Picture 1> ... is fully referenced` 把视频起点绑到末帧 | **弱——仅参考锚定**：当前适配器 ARK 请求体只有 `reference_image` 角色（角色/风格/构图锚定），**无 first-frame 条件化字段**（未实现） |
| 辅助锚定 | 官方图 001/002 作 `<Picture 2/3>` 身份加强 + prompt 复述姿态 | subject/scene 文本复述落定姿态（`continuing EXACTLY from the locked ready stance ...`，FreeLOC 自包含锚点） |
| 不支持时的退法 | ref_image_0 必填，无退法可——**若 data URI 被网关拒**（尺寸/格式假设失败）：① 末帧重编码为 JPEG ≤500KB 再传；② 仍失败 → H3 版 Seg2 放弃 I2VA，改 T2VA 纯文本复述（一致性靠官方图+姿态文本，接缝靠剪辑） | ① 去 `-r` 走纯文本复述；② 接缝处生成后评估：漂移可感知 → 重生成（姿态描述再收紧）或剪辑层 0.3–0.5s 交叉溶解（ffmpeg xfade）/硬切兜底 |

**[假设需生成前验证]**：Seg2 末帧 = 本地文件 → data URI 入 H3 ref_image_0。已验证：CLI 装配链路（本地路径 → `image_to_data_uri` → 请求体）通过 dry-run；**未验证**：AutoDL 网关对 ~1–3MB data URI 的接受度与 `validate_reference_image` 短边 ≥768 校验（768p横末帧短边可能 720 → 仅 warn 不阻塞，但低清放大可能降身份保真度）。**执行前动作**：Seg2 生成前先跑 §6 Step 4 的 dry-run，确认请求体 ref_image_0 为 data URI 且无异常再提交。

##### 5.3 段接缝验证（生成后，Hard Rule 3）

段 1 末帧 vs 段 2 首帧：视觉不连续/闪光/跳变 → H3 版应接近零漂移（I2VA 强条件化）；Seedance 版允许轻微构图漂移 → 硬切可接受，否则 0.3–0.5s 交叉溶解（Bleach 风格忌长溶解；硬切优先）。

#### 6. A/B 执行清单（任务 4）

> 工作目录：`/home/aifeier/org-dev/bip/outgiving`（`uv run --directory scripts` 会切 cwd，**路径必须用绝对路径**——相对路径已实测失败）。
> 输出文件命名：`outputs/{task_id}.mp4`（task_id 见 CLI 输出，写入日志）。

##### Step 0 — dry-run 预检（不花钱，必须先过）

```bash
P=/home/aifeier/org-dev/bip/outgiving/ai-video/projects/T005
# H3 Seg1（2 张官方图直链）
uv run --directory scripts ai -p autodl_comfyui generate video \
  --prompt-file $P/exec/video-prompt-h3-seg1.md --model lightx2v_v5 --duration 5 --resolution 768p横 \
  -r "https://cimg.kgl-systems.io/camion/files/dengeki/85246/a4efdd2f969559e8b1c92e99f32ded48e.jpg" \
  -r "https://cimg.kgl-systems.io/camion/files/dengeki/85246/a3fb5ed13afe8714a7e5d13ee506003dd.jpg" \
  --dry-run
# Seedance Seg1
uv run --directory scripts ai -p seedance generate video \
  --prompt-file $P/exec/video-prompt-seedance-seg1.md --model mini --duration 5 \
  --negative-prompt "photorealistic rendering, 3D shading, white full-face mask, modern elements, on-screen text, subtitles, UI, watermark, multiple characters, pink candy colors, low contrast, gray midtones, whip pan, excessive camera shake, motion smearing on static frames, character breathing movement, cloth wind movement, ambient particle animation during still frames, micro-movement in locked shots" \
  --dry-run
```

通过标准：H3 请求体含 alignment 首行 + 三字段 + `ref_image_0/1`；Seedance 请求体 `ratio: 16:9`、`duration: 5`、无 image content。

##### Step 1 — Seg1 A/B 生成（两条并行或串行均可）

```bash
P=/home/aifeier/org-dev/bip/outgiving/ai-video/projects/T005
# A：H3（≈¥0.05）
uv run --directory scripts ai -p autodl_comfyui generate video \
  --prompt-file $P/exec/video-prompt-h3-seg1.md --model lightx2v_v5 --duration 5 --resolution 768p横 \
  -r "https://cimg.kgl-systems.io/camion/files/dengeki/85246/a4efdd2f969559e8b1c92e99f32ded48e.jpg" \
  -r "https://cimg.kgl-systems.io/camion/files/dengeki/85246/a3fb5ed13afe8714a7e5d13ee506003dd.jpg" \
  -o $P/outputs/
# B：Seedance mini（纯文本，成本实测后回填）
uv run --directory scripts ai -p seedance generate video \
  --prompt-file $P/exec/video-prompt-seedance-seg1.md --model mini --duration 5 \
  --negative-prompt "photorealistic rendering, 3D shading, white full-face mask, modern elements, on-screen text, subtitles, UI, watermark, multiple characters, pink candy colors, low contrast, gray midtones, whip pan, excessive camera shake, motion smearing on static frames, character breathing movement, cloth wind movement, ambient particle animation during still frames, micro-movement in locked shots" \
  -o $P/outputs/
```

##### Step 2 — 生成后自评估（每段必过，3 轮上限）

```bash
# 2a. 元数据 + 关键帧抽样（首2s/中点/末2s PNG）
ffprobe -v error -show_entries stream=width,height,duration,r_frame_rate,codec_name -of default=nw=1 $P/outputs/<task_id>.mp4
uv run --directory scripts ai verify $P/outputs/<task_id>.mp4 --expect-duration 5 -o $P/outputs/verify_<A或B>/
```

对照 §1 验收维度表逐条打勾；失败 → 修 prompt 重生成（最多 3 轮；3 轮未过 → 标注问题升级用户/门 3）。

##### Step 3 — 赢家判定 + 末帧提取

1. 按 §1 验收维度打分（权重：三态推进 ≥ 形态相似度 > 运动连贯 > 末帧可用性 > 成本/耗时）→ 赢家。
2. 末帧质量门禁（§5.1）过目 → 提取：

```bash
P=/home/aifeier/org-dev/bip/outgiving/ai-video/projects/T005
uv run --directory scripts ai extract-lastframe \
  $P/outputs/<赢家_task_id>.mp4 \
  -o $P/assets/last-frames/T005-seg1-winner-lastframe.png --time-offset 0.5
# 目检末帧（双角/面具/横置刀入画、无运动模糊）→ 不过则 --time-offset 0.3 重截
```

##### Step 4 — Seg2 生成（跟随赢家 provider，先 dry-run 验证 data URI 假设）

```bash
P=/home/aifeier/org-dev/bip/outgiving/ai-video/projects/T005
# 赢家=H3 → H3 Seg2（ref_image_0=末帧 data URI；官方图顺延 2/3）
uv run --directory scripts ai -p autodl_comfyui generate video \
  --prompt-file $P/exec/video-prompt-h3-seg2.md --model lightx2v_v5 --duration 5 --resolution 768p横 \
  -r $P/assets/last-frames/T005-seg1-winner-lastframe.png \
  -r "https://cimg.kgl-systems.io/camion/files/dengeki/85246/a4efdd2f969559e8b1c92e99f32ded48e.jpg" \
  -r "https://cimg.kgl-systems.io/camion/files/dengeki/85246/a3fb5ed13afe8714a7e5d13ee506003dd.jpg" \
  --dry-run   # 确认 ref_image_0 为 data:image 后再去掉 --dry-run 并提交
uv run --directory scripts ai -p autodl_comfyui generate video \
  --prompt-file $P/exec/video-prompt-h3-seg2.md --model lightx2v_v5 --duration 5 --resolution 768p横 \
  -r $P/assets/last-frames/T005-seg1-winner-lastframe.png \
  -r "https://cimg.kgl-systems.io/camion/files/dengeki/85246/a4efdd2f969559e8b1c92e99f32ded48e.jpg" \
  -r "https://cimg.kgl-systems.io/camion/files/dengeki/85246/a3fb5ed13afe8714a7e5d13ee506003dd.jpg" \
  -o $P/outputs/
# 赢家=Seedance → Seedance Seg2（末帧 reference_image 锚定 + 文本复述）
uv run --directory scripts ai -p seedance generate video \
  --prompt-file $P/exec/video-prompt-seedance-seg2.md --model mini --duration 5 \
  -r $P/assets/last-frames/T005-seg1-winner-lastframe.png \
  --negative-prompt "photorealistic rendering, 3D shading, white full-face mask, modern elements, on-screen text, subtitles, UI, watermark, multiple characters, pink candy colors, low contrast, gray midtones, motion smearing, character appearance changing between shots" \
  -o $P/outputs/
```

Seg2 生成后：Step 2 自评估 + **段接缝验证**（§5.3）。全片 = `ai edit concat`（硬切）拼接 2 段；BGM = genbgm（按 §0/§3.2 音频裁决）→ `ai edit` 合成混入。

##### 验收对照维度（A/B 逐版打分，写入日志）

| # | 维度 | 判据 |
| --- | ---- | ---- |
| 1 | 角色相似度 | 末帧 vs research §1.1：双角（两根/形质）/ 黑半虚化面具（非全白）/ 颈·手·脚血锁锁链 / 橙发 / 黑装 / 刀横置——7 项逐项 ✓/✗ |
| 2 | 三态推进（M6） | 0–1.2s 无角无面具（变身前）✓ / 1.2–3.2s 变身进行（面具蔓延+角顶出）✓ / 3.2–5.0s 完全形态锁定 ✓；无跳态/停滞/回退 |
| 3 | 运动连贯 | 锁链迸裂/面具蔓延/突进无肢体形变抖动；速度线合理；2B 突进方向=向镜头 |
| 4 | 末帧质量（段1 专属） | 居中/全入画/光照稳定/无运动模糊（§5.1 门禁） |
| 5 | 时长/分辨率 | ffprobe 实测 5.0s±0.5；分辨率记录实际值（H3 768p横 / Seedance 16:9，具体 WxH 回填） |
| 6 | 耗时 | 提交→完成（CLI Time 列） |
| 7 | 成本 | H3 ≈¥0.05（CLI Est. cost）；Seedance 实测回填 |
| 8 | 版权拦截（M5） | 是否被拦截 + 完整报错文本 + 判断触发特征组合（压测数据，非失败） |
| 9 | 音频 | H3：soundscape/music 是否按字段生成、可听度；Seedance：自动环境音有无 |

#### 7. 收敛门记录 + SDK 就绪 + 自检

| 门 | 状态 | 依据 |
| --- | ---- | ---- |
| ALIGN | ✅ | TOGETHER §3 无 🔴（仅 script 自报）；§4 资源 P0 全就绪（参考图×2/H3 通路/Seedance 通路）；上游 visual/rhythm 文档缺失已降级为 P1 残余风险（§0），未构成 §3 阻断 |
| FreeLOC | ✅ | 每拍自包含：script.md 各拍含 FreeLOC 锚点；Seg2 两版 prompt 均内嵌完整姿态复述（不依赖前段上下文即可理解） |
| LoL | ✅ | 单段 5s < 20s，无需复位；段边界三不变量已声明（§1） |
| ZPC | ✅ | 单拍时长 1.0–3.0s 为设计内子拍（AI 视角为连续 5s 一镜，非快切；子拍间过渡=因果/递进/空白，无 <1.8s 硬切碎片） |
| IaD | 🟡→放行 | 参考图为官方形态图（非中性表情立绘），无表情一致性任务（变身形态本身即表情载体）；内容未目验 → 首生成回校（research 未决项） |
| RefImg | ✅ | H3：Seg1 2 张官方直链（GET 200 实测）/ Seg2 末帧 data URI + 2 张直链（dry-run 验证装配）；Seedance：按任务设定纯文本自足（A/B 对照组，RefImg 门对 B 版豁免——记录于日志） |
| 生图确认门 | N/A | 无 AI 生图资产（参考图=官方已下载图）；P0 资产 = 官方图×2（✅ 已入库）+ 段1 末帧（生成后提取，Step 3） |

SDK 字段就绪（H3）：三核心字段 → 单一 prompt 文本（alignment 置顶 + 顺序 integrated→soundscape→music，dry-run 验证）；ref_image_0..2 → URL/data URI（验证）；duration/resolution/seed 透传（验证）；负向 → 无字段，正向约束替代（已内嵌）；音频 → 原生字段（设计目标，待实生成回校）。
SDK 字段就绪（Seedance）：五字段 → content[0].text（验证）；negative_prompt（验证）；ratio 16:9（验证）；duration 5 ∈ 合法值（验证）；参考图（Seg2）→ reference_image（装配链路验证）；`generate_audio` 无 CLI 开关（默认 True，音频裁决见 §3.2）；`return_last_frame` 未暴露（末帧走 ffmpeg 提取）。

自检：矛盾矩阵 M1–M6 全裁决（M6 门 3 关注）✓ / 叙事锚点 3 个 ✓ / [间] 4 处非零 ✓ / 段边界延续 + 三不变量 ✓ / 4 prompt 文件 dry-run/解析全链路验证 ✓ / 末帧链路径与阻塞规则 ✓ / 生成调度：Seg1 A/B → 末帧门禁 → 赢家 Seg2（P0 规范参考拍=1C 末帧，P1=2A/2B，P2=2C）✓

---

#### 生成日志模板（每次生成填一份，追加到本节或独立 `gen-log.md`）

```markdown
##### GEN-<序号>（<2026-08-XX HH:MM>）
- 段：Seg1-A(H3) / Seg1-B(Seedance) / Seg2(H3|Seedance)
- 命令：（粘贴实际执行的完整命令）
- Task ID：<task_id>
- 参考图：H3=[ref_image_0=末帧dataURI/001URL/002URL] | Seedance=[末帧reference_image / 无]
- 提交时间 / 完成时间 / 耗时：<...>
- 成本：H3=¥<Est. cost> | Seedance=<控制台实测>
- 分辨率/时长（ffprobe 实测）：<WxH / s>
- 拦截事件（M5）：无 / <完整报错 + 判断触发的特征组合>
- 验收打分（§6 维度 1–9）：角色相似度=<7项✓/✗> | 三态推进=<✓/✗+细节> | 运动连贯=<...> | 末帧质量=<...> | 时长分辨率=<...> | 耗时=<...> | 成本=<...> | 拦截=<...> | 音频=<...>
- verify 抽样帧路径：outputs/verify_<A/B|S2>/
- 末帧：路径=<assets/last-frames/T005-seg1-winner-lastframe.png / N/A> 截帧时刻=4.5s(offset 0.5) 门禁=<过/不过+原因>
- 结论：赢家候选 / 作废（原因）/ 升级（门3/用户）
```

## ④ 执行

交付：4 个 prompt 文件（全部 dry-run/解析全链路验证）：`exec/video-prompt-h3-seg1.md` / `exec/video-prompt-h3-seg2.md` / `exec/video-prompt-seedance-seg1.md` / `exec/video-prompt-seedance-seg2.md`；A/B 执行清单（② · 6. A/B 执行清单）；末帧接续规范（② · 5）；门 3 裁决包 → `gates/gate3-design-alignment.md`。

## ⑤ 结果

- director 自报（2026-08-24）：段数 2 × 5s 对齐 script ✅；段边界 5.0s 延续边界 + 三不变量采纳 ✅；M1–M6 全裁决（M6 门 3 关注）✅；A/B 工具方案 + 4 个 prompt 文件 dry-run 全链路验证 ✅（H3 768p横 5s / Seedance mini 16:9 5s）；末帧链规范 + 阻塞规则 ✅；收敛门：ALIGN ✅ / FreeLOC ✅ / LoL ✅ / ZPC ✅ / IaD 🟡（官方图未目验，首生成回校）/ RefImg ✅（H3 每段 ≥1 图；Seedance B 版按任务纯文本自足，豁免记录在日志）；上游 visual/rhythm 文档缺失 → P1 残余风险（§2.4）。
- 交接：seg1（H3 Seg1 prompt + 参考图 001/002 data URI + 执行清单 Step 1）、seg2（Seg2 prompt + 末帧注入路径 + 前置门禁）；M6 = 门 3 关注项（A/B 首生成验证三态推进）
