# T003 死神祸进篇 30s PV — Video Prompt

> **生成版本**：v1 | **日期**：2026-07-20 | **状态**：合成（Yhwach/Ichigo P0 参考图已就绪；冰宫仍缺，文本描述补偿）
> **文案语言**：全 prompt 中文/英文混合（符合 Seedance 多语言能力）| **画幅**：9:16 portrait (1080×1920)
> **总时长**：30s | **段数**：2（Seedance 2.0 Mini 15s 硬限驱动）
> **工具**：Seedance 2.0 Mini (`doubao-seedance-2-0-mini-260128`)

---

## 1. 矛盾矩阵（Phase 1 裁决确认）

| #  | 矛盾                                                      | 甲                                                                               | 乙                                  | 裁决                                                                                                                                                                                                                                    |
| -- | --------------------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M1 | 段数：3 designer 写"4 段" vs 工具驱动 2 段                | script/visual/rhythm 最初写"4 段"                                                | Seedance Mini 15s 硬限 → 须拆 2 段 | **最终裁决**：拍数=4（叙事），段数=2（工具）。段边界在 B3b 末（~00:15.5），延续边界类型。已贯通三 designer。**状态**：✅                                                                                                    |
| M2 | CF×V 超标：Hook 6.0 / Escalation 18.0                    | rhythm 原始 CF（Hook 3.0 / Esc 4.5）                                             | visual 原始 V（Hook 2 / Esc 4）     | **最终裁决**：Hook rhythm 降 CF 至 2.0（保留 V=2 → 4.0 ✅）。Escalation 各让一步：rhythm 半速映射效感 CF 2.0 + visual 降 V 至 2（去灵王碎片/文字排版叠加 → 4.0 ✅）。**状态**：✅（visual 已确认，rhythm 待终版文件确认） |
| M3 | 锚点拍定义不统一                                          | script: B2+B3+B4                                                                 | visual: B1+B2+B4                    | rhythm: B1+B4                                                                                                                                                                                                                           |
| M4 | ZPC 拍级 ASL < 1.8s vs 段级 ASL ≥ 1.8s                   | 拍级 Hook ~1.7s, Esc ~1.4-1.7s 低于阈值                                          | ZPC 按段级计算                      | **最终裁决**：段 1（~15.5s / 8 shots ≈ 1.9s ASL ✅），段 2（~14.5s / 6 shots ≈ 2.4s ASL ✅）。按段级 ASL 通过 ZPC。**状态**：✅                                                                                           |
| M5 | P0 参考图状态变更（原全缺→Yhwach/Ichigo 就绪，冰宫仍缺） | §4 R1-R3 原🔴→Yhwach/Ichigo ✅（033+034+036+037 官方源已就绪），冰宫 R3 仍缺🔴 | 用户确认：标注风险但不阻塞合成      | **最终裁决**：Yhwach (033+034) + Ichigo (036+037) 官方源已就绪并直接引用为 reference_image。冰宫场景仍缺，以文本描述补偿。**状态**：🟡 P0 部分就绪（冰宫仍缺）                                                              |

### 三体树状态

| 元素                   | 当前值                                                                   | 调整影响                                                                   | 收敛状态                  |
| ---------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------- | ------------------------- |
| **脚本（脚本）** | 4 拍经典弧，30s 压缩版，70% 奇观+一护情感锚点                            | —                                                                         | ✅                        |
| **视觉（视觉）** | Bleach 高对比，V=2 简化，无文字排版/灵王碎片叠加                         | Escalation V 从 4 降至 2（去 R8 灵王碎片），拍级视觉复杂度受控             | ✅                        |
| **节奏（节奏）** | Hook CF=2.0 / Reveal CF=1.4 / Esc 半速映射 effektiv CF=2.0 / Drop CF=0.8 | Hook 从 3.0 降至 2.0（减少切数但保留模式中断），Esc 物理切频保留但效感受控 | ⚠️（rhythm 待终版确认） |

**回 brief：** 30s 抖音 PV，核心沟通目标=信息型混合奇观（让观众理解千年血战篇核心冲突并导向搜索）。无一元素需回 brief 调整。三体树收敛。

---

## 2. 实体标签注册表

| 标签                      | 实体                        | 首次拍      | 再现拍          | 外观不变量                                                                              | 可变特征                                          |
| ------------------------- | --------------------------- | ----------- | --------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `[ANTAGONIST]`          | 友哈巴赫 Yhwach             | B1 (0:00)   | B3c (0:15.5)    | 白色双排扣军服+三枚银色衣领勋章、深红长斗篷、黑色长发及腰、红色多瞳眼睛、无眉毛、无武器 | 多重瞳孔密度（全知全能发动时增加）                |
| `[PROTAGONIST]`         | 黑崎一护 Ichigo True Shikai | B2 (0:05)   | B3a (0:12) 延续 | 橙色刺状发束（不受重力）、黑色死霸装（锐利褶皱）、双斩月                                | 灵压颜色（黑→橙渐变），释放 Getsuga 时橙色高饱和 |
| `[WEAPON_ZANGETSU]`     | 双斩月                      | B2 (0:05)   | B3a (0:12)      | 大刃纯黑有细长镂空纹理（死神+虚）、小刃纯黑如匕首无刀柄（灭却师）                       | 橙色灵压缠绕程度                                  |
| `[FACTION_STERNRITTER]` | 星十字骑士团                | B1 (0:01.7) | —              | 白色披风+星十字徽章，仅剪影                                                             | 不展示面部                                        |

**标签唯一性检查**：无碰撞。同一 role tag 不同角色不共享。

---

## 3. 参考素材清单

### 需求-库存对账

| 拍 | 类型       | 实体/场景                             | 优先级 | asset-lab 状态                                                                                                                                                                                                                             | 实际可用 | 处理                                                                            |
| -- | ---------- | ------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------- |
| B1 | 规范参考图 | [ANTAGONIST] Yhwach                   | P0     | ![](assets/ref-images/033_char_identity_YhwachOfficialFull_v01.png) 033 官方全身立绘 (1050×1500, 官方源, bleach-anime.com)![](assets/ref-images/034_char_identity_YhwachOfficialFace_v01.png) 034 官方面部表情集（P0 已就绪）             | 就绪     | 直接引用为参考图锚定：B1 Yhwach 身份/军服/多瞳红瞳锚定                          |
| B2 | 规范参考图 | [PROTAGONIST] Ichigo True Shikai 双刀 | P0     | ![](assets/ref-images/036_char_identity_IchigoOfficialFull_v01.png) 036 官方全身立绘 (1050×1500, 单刀已确认, 官方源, bleach-anime.com)![](assets/ref-images/037_char_identity_IchigoOfficialFace_v01.png) 037 官方面部表情集（P0 已就绪） | 就绪⚠️ | 直接引用为参考图锚定（身体/面部）。双刀细节仍以文本描述补偿（官方图为单刀形态） |
| B1 | 场景参考图 | 无形帝国冰宫/御座                     | P0     | 不存在（待产）。无对应参考图就绪                                                                                                                                                                                                           | 缺货     | **降级为文本描述**。冰宫场景仍缺，以文本描述补偿                          |
| B3 | 场景参考图 | 瀞灵廷崩塌（剪影）                    | P1     | 不存在（待产）                                                                                                                                                                                                                             | 缺货     | 降级为文本描述（V=2 方案中本已简化）                                            |
| B4 | 分镜概念图 | "禍進"标题文字布局                    | P1     | 不存在（待产）                                                                                                                                                                                                                             | 缺货     | 降级为文本描述                                                                  |
| B3 | 分镜概念图 | Getsuga Jujisho 释放构图              | P1     | 不存在（待产）                                                                                                                                                                                                                             | 缺货     | 降级为文本描述                                                                  |

### 段末帧

| 段边界                  | 末帧来源            | 路径                                                                | 状态                            | 用途                                  |
| ----------------------- | ------------------- | ------------------------------------------------------------------- | ------------------------------- | ------------------------------------- |
| 段 1 → 段 2 (~00:15.5) | 段 1 生成后提取末帧 | `ai-video/projects/T003/assets/last-frames/T003-B1-lastframe.png` | **未生成**（段 1 未产出） | 段 2 Tier 0 强制参考，不计入 9 图槽限 |

**⚠ 风险标注**：当前 P0 状态：Yhwach 官方源就绪 (+033 +034) ✅ / Ichigo 官方源就绪 (+036 +037，单刀形态) ✅ / 冰宫仍缺 🔴 + 段 1 末帧未生成。合成推后补齐规则：

- 段 1 生成后手动提取末帧 → 存入 `last-frames/` → 段 2 prompt 引用
- 冰宫参考图产出后 → 替换 B1 Shot 1.2 中冰宫场景的文本描述
- 段 2 当前 prompt 写的末帧参考图缺省，以 `[段间锚定:待末帧就绪后嵌入]` 标记

### 候选池裁剪记录

P0 状态更新：Yhwach (033+034) + Ichigo (036+037) 官方源已就绪。冰宫 (P0 场景) 仍缺。候选池装配排序：

- **Tier 0**：段 1 末帧（前段末帧，锚定段间延续）不计 9 图槽限
- **Tier 1**：033 Yhwach 官方全身立绘 (iaD ✓, 1050×1500) + 034 Yhwach 官方面部表情集 (iaD ✓) + 036 Ichigo 官方全身立绘 (iaD ✓, 1050×1500, 单刀) + 037 Ichigo 官方面部表情集 (iaD ✓)
- **Tier 2**：瀞灵廷崩塌参考图 (P1，现有场景池可选配)
- **Tier 3**：Getsuga 释放 + 祸进标题 分镜概念 (P1)

---

## 4. 全局一致性前缀

```
Bleach anime style, high contrast black and white, cold white highlights, deep blue-black shadows, sharp angular lines, strong outer silhouettes, negative space composition, 9:16 portrait aspect ratio.

All transitions: hard cut only, no dissolve, no white flash except for Getsuga burst moment.

Color key: Bleach low-key desaturated. 10% black minimum. Orange #E8760B and cold blue only for power effects. No pink, no candy colors, no warm glow filters, no soft focus.

Art direction: sharp angular line art with speed-varying weight, strong outer silhouettes, high contrast cel shading. Bleach-Kubo style.

Prohibited: no photorealistic rendering, no 3D shading, no continuous fight motion, no whip-pan, no crane shot, no complex tracking, no dissolve transitions, no soft focus, no warm tone filters.

Character registry:
[ANTAGONIST] Yhwach — tall broad-shouldered, white double-breasted military uniform with three silver medals on collar, dark red long cape flowing to floor, long black hair to waist, red multiple-pupil eyes, deep eye sockets, thick beard connecting sideburns to jaw, no eyebrows, no weapon drawn, seated or standing still with absolute stillness.

[PROTAGONIST] Ichigo True Shikai — tall slender build, orange spiky hair tufts defying gravity (4-5 tufts front, 2-3 on sides, each tip sharp), black shinigami robe (sharaku) with sharp folds, white straw sandals with ankle wraps. Dual Zangetsu blades: long sword in right hand (held lower on grip, pure black blade with elongated hollow texture, purple zigzag pattern on hilt, irregular pentagon black tsuba) — represents Shinigami + Hollow power. Short dagger in left hand (held through hollow center of handle, no tsuba, pure black blade with jagged edges as if bitten) — represents Quincy power. Two blades form X shape when crossed.

[WEAPON_ZANGETSU] — dual blades always present in B2 onwards. Long blade: silver-white blade surface, purple zigzag pattern on hilt, 120cm length. Short blade: black irregular edge, 50cm length, no hilt wrapping.

[FACTION_STERNRITTER] — white cloaks with star-cross emblem, silhouette only, no facial detail required.
```

---

## 5. 节拍序列 → 段 Prompt

### 本段引用参考图

本段各 beat 使用的参考图（Seedance reference_image 输入）：

| 拍    | 参考图                                                                                              | 用途                                                                      |
| ----- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| B1    | `033_char_identity_YhwachOfficialFull_v01.png` + `034_char_identity_YhwachOfficialFace_v01.png` | [ANTAGONIST] Yhwach 身份+军服+多瞳红瞳锚定                                |
| B2    | `036_char_identity_IchigoOfficialFull_v01.png` + `037_char_identity_IchigoOfficialFace_v01.png` | [PROTAGONIST] Ichigo 身份+死霸装+表情锚定（单刀形态；双刀细节由文本补偿） |
| B3a-b | `036_char_identity_IchigoOfficialFull_v01.png`（间接锚定）                                        | Ichigo 剪影+身体轮廓延续                                                  |

> 图片预览：
> ![](assets/ref-images/033_char_identity_YhwachOfficialFull_v01.png) ![](assets/ref-images/034_char_identity_YhwachOfficialFace_v01.png)
> ![](assets/ref-images/036_char_identity_IchigoOfficialFull_v01.png) ![](assets/ref-images/037_char_identity_IchigoOfficialFace_v01.png)
> ⚠ 冰宫场景参考图仍缺（P0），B1 Shot 1.2 场景以文本描述补偿。

### 段 1（0:00-0:15.5, ~15.5s）

**段类型**：首段，延续边界。段末帧为 Ichigo 剪影+Getsuga 余辉。

#### Beat 1：Invasion（入侵）[0:00-0:05]

**规范参考拍**：此拍提供 [ANTAGONIST] Yhwach 首次清晰出现。P0 官方参考图已就绪（033 官方全身立绘 + 034 官方面部表情集）。生成后仍建议人工检查 Yhwach 外观一致性。

**Shot 1.1 [0:00-0:02.5]：Yhwach 多瞳红瞳特写（2.5s）**

- **scene**: 纯黑背景。无空间环境——仅有 Yhwach 左眼占据画面 90%。极端特写，眼睑半闭，红色多瞳如同万花筒层叠
- **subject**: [ANTAGONIST] Yhwach left eye extreme close-up. Red iris with multiple concentric pupils. Eye completely still — no blinking, no movement. Deep red #CC2233 iris color against pure black skin tone. Eye half-lidded (N/3 open), no expression. Layers of concentric pupils visible like kaleidoscope depth
- **camera**: static extreme close-up, no movement. 1.5s hold on static eye, then 1s slow fade transition (not dissolve — bleach hard cut style, just extreme close-up held then cut)
- **lighting**: no ambient light. Only red iris self-luminescence as light source. Surrounding skin in deep shadow
- **style**: Bleach anime, high contrast, negative space, sharp angular lines
- **quality**: 9:16 portrait, 1080×1920, sharp details on iris texture
- **[间]**: 静止 1.5s 无运动——纯粹的静止=力量感。0.3s 模式中断在开场帧完成

**Shot 1.2 [0:02.5-0:05]：Yhwach 中景 + 星十字剪影（2.5s）**

- **scene**: Silbern 冰之宫殿内部。冷色顶光，纯白冰柱与几何化建筑结构。背景两侧星十字骑士团以白色披风剪影列阵。无窗无自然光——纯人工冷光
- **subject**: [ANTAGONIST] Yhwach seated on throne center frame. Full upper body visible. White double-breasted military uniform with three silver medals on collar. Dark red flowing cape draping from shoulders to ground. Long black hair to waist. Red multi-pupil eyes looking slightly down. Zero expression — absolute stillness. Background: [FACTION_STERNRITTER] white cloak silhouettes standing in regimented rows on both sides, marching boots in unison
- **camera**: snap zoom-out from extreme close-up to medium shot. 0.5s rapid pull-back revealing Yhwach seated on elevated throne. Then static hold 2s
- **lighting**: cold back overhead light, deep blue-black shadows at 10% brightness. Red eyes as only warm color point in frame (2000K vs 7000K environment). White uniform emerges from darkness
- **style**: Bleach anime, high contrast cel shading, cold blue-black shadows, sharp angular folds on cape, negative space composition
- **quality**: 9:16, high contrast, no midtones, sharp edge lines on uniform
- **[间]**: 急拉后保持静止 2s。静止=灭却师之王的不可挑战性

**【过渡 B1→B2】**：硬切。从 Yhwach 中景（冷色/白色/霜之宫殿）→ Ichigo 中景（黑色/橙色/纯黑背景）。对比转场——入侵者→应战者。

---

#### Beat 2：Awakening（觉醒）[0:05-0:12]

**规范参考拍**：此拍提供 [PROTAGONIST] Ichigo True Shikai 双刀的首次清晰规范参考。P0 官方参考图已就绪（036 官方全身立绘 + 037 官方面部表情集）。⚠ 注意：官方图为单刀形态，双刀细节（大刃镂空+小刃无柄中空）仍需文本描述补偿。生成后建议人工检查双刀形态是否可辨。

**Shot 2.1 [0:05-0:08]：双刀展示（3s）**

- **scene**: 纯黑虚化背景（负片空间——角色为画面唯一内容）。单一定向侧光（左上方 45° 偏冷白），右侧大面积阴影。黑色灵压雾在镜头前缓慢涡旋
- **subject**: [PROTAGONIST] Ichigo True Shikai standing center-left in frame, facing slightly right. Orange spiky hair tufts sharply defined (4-5 front tufts, 2-3 side tufts). Black shinigami robe (sharaku) with sharp angular folds. [WEAPON_ZANGETSU] dual blades: long Zangetsu in right hand held lower on grip (120cm, pure black blade with elongated hollow texture, purple zigzag on hilt, irregular pentagon black tsuba). Short dagger in left hand held through hollow center handle (50cm, pure black jagged edge blade, no tsuba). Blades crossed in X-shape in front of chest. Black spiritual pressure mist slowly swirling around arms and blades. Neutral expression — mouth slightly closed, eyes half-lidded looking slightly down-left. Cold white rim light on blade edges and shoulder silhouette
- **camera**: medium shot fixed, slight slow dolly-in (0.3m over 3s). Ichigo positioned left 1/3, facing right. Double blades clearly visible with cold white side light revealing blade texture details
- **lighting**: single directional side light from upper-left 45°, cool white (6500K). Deep shadow on right side (15% brightness). Blade cold white highlights as brightest elements in frame. No fill light
- **style**: Bleach anime, negative space background, sharp angular folds on shinigami robe, cold rim light on character edge, high contrast
- **quality**: 9:16, sharp line details on blade textures, clear distinction between long and short blade forms
- **[间]**: 3s 缓慢推近——这是全片唯一的呼吸段落。推近速度几乎不可见，观众有机会看清双刀差异

**Shot 2.2 [0:08-0:12]：觉醒姿态（4s）**

- **scene**: 同 Shot 2.1。保持纯黑背景。黑色灵压雾从 Ichigo 双肩向双刀蔓延，缠绕密度缓慢增加
- **subject**: [PROTAGONIST] Ichigo True Shikai — same position, same X-blade stance. No visible camera movement — static frame. Black spiritual pressure mist density increases slightly, first wisps of orange glow starting at blade edges. Last 1s: Ichigo's eyes shift from half-lidded to focused — subtle change (1-2px iris shift) as battle intent activates. Orange spiritual pressure begins faintly flickering at blade tips. This is the signal that release is coming
- **camera**: static fixed medium shot. No movement for 3s, then final 1s micro-movement as orange glow flicker begins
- **lighting**: same side light. Orange glow at blade edges adds second color temperature to frame (warm orange against cool white rim light). Very subtle — orange at <5% brightness, just visible
- **style**: Bleach anime, still frame = charge posture, orange glow as power release precursor
- **quality**: 9:16, stable frame, focus on eyes
- **[间]**: 静帧 4s——但最后 1s 的橙色灵压闪烁是「安静中的危险信号」。整个 B2 没有镜头切，保持统一静止。这是给观众认知时间消化双刀信息

**【过渡 B2→B3】**：硬切。从 Ichigo 展示静帧（暗/黑/橙色暗示）→ Getsuga Jujisho 橙色十字爆发（亮/橙/白）。从蓄力到释放的直接连接。

---

#### Beat 3a-b：Getsuga 释放 + 剪影浮现 [0:12-0:15.5]

**Shot 3.1 [0:12-0:14]：Getsuga Jujisho 十字冲击（2s）**

- **scene**: 纯黑背景前。橙色灵压从交叉双刀交汇点爆发，形成巨大十字型冲击波向画面右方扩散。画面 80% 被橙色高饱和灵压充满，但 Ichigo 剪影轮廓在灵压后方保持可见（Bleach 高反差原则——橙色在黑背景中极度突出）
- **subject**: [PROTAGONIST] Ichigo True Shikai silhouette behind orange cross blast. Blades crossed at center point. Orange spiritual pressure explosion from blade intersection forms perfect cross shape. Ichigo's black silhouette visible through semi-transparent orange energy — outline of head, shoulders, dual blades identifiable. V=2: only two visual elements — orange cross + black silhouette. No background texture, no auxiliary VFX
- **camera**: medium-close fixed frame. Energy expands from center outward at moderate speed. 1.5s to reach full size then cut
- **lighting**: orange self-luminescence from Getsuga energy. No external light source. High contrast — orange at 100% saturation in center, fading to black at edges
- **style**: Bleach anime, speed lines radiating from cross center. Orange #E8760B pure saturation against black. Sharp energy edge lines
- **quality**: 9:16, high saturation orange burst
- **[间]**: 2s 快速爆发——Getsuga 从出现到全尺寸 1.5s。没有蓄力展示（蓄力在 B2 末尾已完成），这是释放

**Shot 3.2 [0:14-0:15.5]：消散·剪影浮现（1.5s）**

- **scene**: 橙色十字以中等速度消散。Ichigo 全黑剪影从残余橙色光芒中浮现。双刀垂放于两侧，黑色剪影在橙色 rim light 中轮廓清晰。白色碎片（灵王崩坏的前兆）开始从黑暗中浮现并缓慢飘落。高对比——亮部橙色冷退至边缘，暗部近全黑。V=2：仅剪影+边缘光+飘落白碎片，无其他视觉元素
- **subject**: [PROTAGONIST] Ichigo pure black silhouette with only rim light visible. Zangetsu blades hanging at sides. White fragments beginning to fall from top of frame. Silhouette position: centered, clear outline of head, shoulders, blades recognizable. Orange rim light fading to cool. White fragments and debris floating in dark void
- **camera**: static medium wide shot. No camera movement — only energy dissipation and fragment falling provide motion
- **lighting**: orange rim light on silhouette edges fading to cool white. White fragments self-lit with cool tone. Ichigo inner body pure black. Ambient light dropping to near zero by end of shot
- **style**: Bleach anime, high contrast negative space, silhouette dominant. White fragments as Escalation prelude
- **quality**: 9:16, clean silhouette, stable lighting, no motion blur, D=3
- **[间]**: 1.5s 消散过渡——Getsuga 冲击后的余韵。能量退去后剪影重新清晰。白色碎片开始浮现——这是「下一件事要来了」的信号

---

**← SEGMENT 1 END [~00:15.5] →**

**段 1 末帧**：Ichigo 全黑剪影，橙色 rim light 在轮廓边缘消退。双刀垂放，白色碎片开始从上方飘落。构图干净（中央对称剪影），角色位置清晰，光照稳定（无频闪/闪烁），无运动模糊，D=3。

---

### 本段引用参考图

本段各 beat 使用的参考图（Seedance reference_image 输入）：

| 拍  | 参考图                                                                                              | 用途                                                  |
| --- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| B3c | `033_char_identity_YhwachOfficialFull_v01.png` + `034_char_identity_YhwachOfficialFace_v01.png` | [ANTAGONIST] Yhwach 身份复位锚定（全知全能面貌+多瞳） |
| B3d | 文本描述（无对应 P0 参考图就绪）                                                                    | 瀞灵廷崩塌以剪影+裂痕文本描述锚定                     |
| B3e | 文本描述（无对应参考图）                                                                            | 三界碎裂圆环以纯抽象几何文本描述                      |
| B4  | 文本描述（无对应参考图）                                                                            | 祸进标题+CTA 纯文字设计                               |

> 图片预览：
> ![](assets/ref-images/033_char_identity_YhwachOfficialFull_v01.png) ![](assets/ref-images/034_char_identity_YhwachOfficialFace_v01.png)
>
> Tier 0 段间锚定：段 1 末帧（待生成后嵌入，不计 9 图槽限）。
>
> 瀞灵廷崩塌/三界碎裂/祸进标题均为纯新视觉或文字，无对应既成参考图需求。

### 段 2（0:15.5-0:30, ~14.5s）

**段类型**：非首段。开场须以段 1 末帧为 Tier 0 强制参考。本 prompt 以 **text placeholder** 标记末帧嵌入点。待段 1 生成完成后更新。

---

**参考图分配（段 2）**：

- `<image1>` `[段间锚定:待末帧就绪后嵌入]` — Tier 0 强制参考，不计 9 图槽限。用途：延续段 1 Ichigo 剪影+白色碎片的视觉状态
- `<image2>` `033_char_identity_YhwachOfficialFull_v01.png` — P0 官方全身立绘。用途：[ANTAGONIST] Yhwach 身份复位锚定（B3c 全知全能面貌）
- `<image3>` `034_char_identity_YhwachOfficialFace_v01.png` — P0 官方面部表情集。用途：[ANTAGONIST] Yhwach 多瞳红瞳特写锚定（B3c 全知全能眼部）
- 瀞灵廷崩塌/三界碎裂/祸进标题均为纯新视觉元素，以文本描述锚定，无参考图需求

---

#### Beat 3c-d：Yhwach 全知全能 + 瀞灵廷崩塌 [0:15.5-0:19.5]

**Shot 3.3 [0:15.5-0:17.5]：Yhwach 全知全能（2s）**

- **scene**: 白色碎片持续从黑暗中飘落（延续段 1 末帧视觉状态）。Yhwach 面部特写于碎片中浮现——全知全能发动，红瞳变为密集多瞳结构如同万花筒。1/3 面部在阴影中。V=2：仅面部+碎片+阴影，无其他视觉元素
- **subject**: [ANTAGONIST] Yhwach face extreme close-up emerging through falling white fragments. Red eyes fully transformed to Almighty state — eyes completely covered in dense multiple concentric pupils like kaleidoscope. Red pupils in high saturation against white fragments. Eye whites visible but secondary to pupil density. 1/3 of face in deep shadow. Thick beard texture visible. Lower face in shadow. White fragments cross in front of face at varying depths, creating depth layering. Zero expression — Yhwach does not need expression to convey power
- **camera**: static face close-up. Eyes as absolute focal point. Fragments floating at multiple depths create parallax layering. No camera movement
- **lighting**: no ambient light source — white fragments as only illumination (self-lit, cool tone). Yhwach skin emerges from pure black, red eyes as only warm color point. High contrast — bright fragments against dark face
- **style**: Bleach anime, negative space, high contrast face lighting, red multi-pupil eyes as visual anchor
- **quality**: 9:16, extreme close-up face sharp, fragment depth visible
- **[间]**: 2s 静态面部——Yhwach 的静止=力量。他只是看着，全知全能自动运作。拒绝不展示攻击/手势

**Shot 3.4 [0:17.5-0:19.5]：瀞灵廷崩塌（2s）**

- **scene**: 白色剪影——瀞灵廷的白色城墙从顶部开始横向裂开，碎片下坠。传统建筑线条（江户风屋顶，入母屋造）在裂痕中断裂。全高对比，无中间调。V=2：白色建筑剪影+黑色天空+碎裂白线作为裂痕，无材质纹理/无粒子细节
- **subject**: Soul Society white palace silhouette against black sky. Traditional Edo-style roofs (irimoya-zukuri) visible as white silhouette shapes. Horizontal crack line starting from top of building cluster — crack spreads left to right across frame. White debris pieces falling from crack points. Black sky completely empty — no stars, no clouds. Architecture simple white silhouette — no material texture, no wood grain, no roof tile individual detail. Just pure white shape with fracture lines
- **camera**: wide angle fixed — building in center of frame, crack line entering from top of frame. Static frame with only crack propagation and debris falling as motion
- **lighting**: no direct light source — architecture self-illuminated as pure white silhouette. Crack interior visible as bright white glow. Black sky background at 0% brightness
- **style**: Bleach anime, pure white silhouette against absolute black, crack lines as sharp angular strokes. Negative space dominant
- **quality**: 9:16, simple geometric white silhouette
- **[间]**: 2s 单镜头——建筑裂开是连续运动，但镜头本身不动。裂痕以中等速度展开，让观众看清「连尸魂界本身也在碎裂」

**Shot 3.5 [0:19.5-0:22]：三界碎裂（2.5s）**

- **scene**: 三个圆环轮廓在黑暗中浮现（具象代表现世/尸魂界/虚圈），呈三角排列在画面中。其中一个（右侧圆环）从边缘开始碎裂→碎片四散→另两个随之出现裂痕。镜头在 2.5s 内从中景拉远至全景——从「看得清碎片」到「看得清全貌」。画面结束时接近全黑，仅保留一个碎裂轮廓的最后一帧。V=2：仅圆环线条+碎裂切线+全黑背景——极简抽象几何。无材质纹理/无粒子细节/无颜色
- **subject**: Three ring silhouettes arranged in triangle formation in dark void. Right ring starts cracking from edge — sharp white fracture lines spreading inward. Fragments separate from main ring edge. Then the other two rings begin showing crack lines. Frame pulls back from medium to wide shot over 2.5s — from seeing individual fragments to seeing the full triangle composition. Final frame: near black with one fractured ring silhouette barely visible
- **camera**: slow pull-back (dolly-out) from medium to wide over 2.5s. Speed accelerates slightly — starts slow (0-1s), accelerates (1-2s), ends fast. Move from "seeing fragments" to "seeing the whole picture"
- **lighting**: no ambient light. Ring silhouettes as pure white line art against absolute black. Self-illuminated line quality. Crack interiors as bright white glow lines
- **style**: Bleach anime, abstract geometric minimal, pure white lines on black. Speed lines radiating from crack points
- **quality**: 9:16, pure black background, white line silhouette
- **[间]**: B3e 最后 0.5s 无音效（在画面剪辑层）——以「半静默」收束。画面还在运动但音频减弱至静音，为 B4 真空停顿蓄力

**【过渡 B3→B4】**：硬切至纯黑。B3e 最后一帧是接近全黑的碎裂剪影 → B4a 开头的 0.5s 全黑真空停顿。举例过渡——B3 展示了抽象的「崩坏」，B4 用「禍進」命名了它

---

#### Beat 4：Calamity（祸进）+ CTA [0:22-0:30]

**Shot 4.1 [0:22-0:24.5]：祸进标题（2.5s）**

- **0:22-0:22.5 — 真空停顿（0.5s）**：全黑，全静默。无画面无声音。这是 30s 中唯一的完整静止帧
- **0:22.5-0:24.5 — 标题冲击（2s）**：
- **scene**: 纯黑背景。无环境空间
- **subject**: Two Chinese characters "禍進" exploding into frame center. Font style: worn clerical script variant (lishu) with broken edges as if cut by blade strokes. White characters (100% brightness) against absolute black. Character surface has micro-fracture lines visible. After 1.5s hold, characters begin shattering from center — fragments dispersing outward in all directions as pure white angular pieces. Character edges show ink-splash gradient from pure white to cool gray #8A8A9A at edges
- **camera**: fixed absolute frame center. No camera movement. Only character shattering provides motion
- **lighting**: character self-lit at full white brightness. No ambient light. Shatter fragments as white line art strokes fading to black
- **style**: Bleach anime, high contrast negative space, white calligraphy on black, broken brush-ink edge treatment, fracture dispersion
- **quality**: 9:16, pure black background, white characters, sharp fracture details
- **[间]**: 0.5s 真空全黑静默——全片最重要的間。在 30s 的冲击序列后，这半秒的绝对安静让前 22s 的所有信息真正落定。不是空档——是蓄力之后的落点

**Shot 4.2 [0:24.5-0:27.5]：CTA 文字（3s）**

- **scene**: 纯黑背景
- **subject**: Two lines of text on pure black. Line 1: "BLEACH 千年血战篇" — white sans-serif small font positioned at upper 1/4 of frame. Fade in 0.5s. Hold for 1.5s. Line 2: "搜索"千年血战"看完整动画" — bold white larger font at lower 3/4 of frame. Fade in 0.5s after Line 1 appears. Both lines coexist on screen for 1s. Then both lines fade out over final 0.5s
- **camera**: fixed. No movement, no effects
- **lighting**: text self-illuminated. Pure white characters at 100% brightness against absolute black
- **style**: clean minimal text card. No decoration, no gradients, no effects
- **quality**: 9:16, sharp text, clean composition
- **[间]**: 3s 的 CTA 文本展示——不是着急结束。给观众足够的认知窗口消化「去哪里看」

**Shot 4.3 [0:27.5-0:30]：收束余白（2.5s）**

- **scene**: absolute black. No image, no text, no light
- **[间]**: 2.5s 全黑静默——给观众一个「放下手机搜索」的认知窗口。不着急结束——留下余韵给祸进标题的冲击去扩散

---

## 6. 段级 Prompt 组织（Seedance 2.0 Mini 格式）

### 本段引用参考图（Seedance reference_image）

段 1 生成时传入以下 reference_image：

- `assets/ref-images/033_char_identity_YhwachOfficialFull_v01.png` — [ANTAGONIST] Yhwach 身份锚定（B1 全身+军服+斗篷+多瞳红瞳）
- `assets/ref-images/034_char_identity_YhwachOfficialFace_v01.png` — [ANTAGONIST] Yhwach 面部特写锚定（B1 多瞳结构+胡须+无眉眉骨）
- `assets/ref-images/036_char_identity_IchigoOfficialFull_v01.png` — [PROTAGONIST] Ichigo 身份锚定（B2 身体+死霸装+单刀。注意：官方图为单刀形态，双刀细节由文本描述补偿）
- `assets/ref-images/037_char_identity_IchigoOfficialFace_v01.png` — [PROTAGONIST] Ichigo 面部特写锚定（B2 橙发+表情+瞳色）

### 段 1 Prompt（~15.5s）

```text
duration_hint: 15
negative_prompt: photorealistic rendering, 3D shading, continuous fight motion, soft focus, dissolve transitions, warm glow filters, pink candy colors, multiple characters in same frame (max 2 characters), whip-pan, crane shot, complex tracking

scene: [B1] Silbern ice palace interior deep perspective, cold overhead light, Yhwach throne on elevated platform, white cape silhouettes of Stern Ritter regiments on both sides. Deep blue-black shadows. V=2 — only cold light + white uniform + red eyes. [B2] Pure black negative space void background, single directional side light from upper-left 45°, cool white. Black spiritual pressure mist slowly swirling. V=2 — character only frame, no background. [B3a] Pure black background, orange Getsuga cross explosion from center, Ichigo silhouette behind energy. Only two visual elements — orange cross + black silhouette. V=2. [B3b] Orange energy dissipating, Ichigo pure black silhouette emerging with orange rim light fading, white fragments beginning to fall. V=2 — silhouette + rim light + fragments only

subject: [ANTAGONIST] Yhwach left eye extreme close-up, red multiple concentric pupils, kaleidoscope depth, half-lidded, zero expression, absolute stillness. Then [ANTAGONIST] Yhwach seated on throne, white double-breasted military uniform with three silver medals, dark red flowing cape, long black hair to waist, red multi-pupil eyes, seated absolute stillness, [FACTION_STERNRITTER] white cloak silhouettes. Then [PROTAGONIST] Ichigo True Shikai, orange spiky hair tufts defying gravity, black shinigami robe with sharp angular folds, [WEAPON_ZANGETSU] dual Zangetsu blades — long blade right hand (pure black elongated hollow texture, purple zigzag hilt) and short blade left hand (pure black jagged edge, no-handle hollow center grip). Blades crossed in X-shape. Neutral expression, half-lidded eyes, pure black void background. Black spiritual pressure mist swirling around arms and blades. Then Ichigo cross-shaped orange Getsuga Jujisho explosion, power release, silhouette behind energy. Then Ichigo pure black silhouette emerging from dissipating orange energy, dual blades hanging at sides, white fragments beginning to fall

camera: extreme close-up static (0-2.5s) then snap zoom-out to medium shot revealing Yhwach on throne (2.5-5s). Then hard cut to medium shot Ichigo with slow dolly-in 0.3m over 3s (5-8s). Then static frame (8-12s). Then medium-close static Getsuga burst (12-14s). Then medium wide static silhouette shot (14-15.5s). All hard cuts. No dissolve, no whip pan, no crane

lighting: [B1] cold back overhead 7000K, red eyes as only warm 2000K point, deep shadows 10% brightness. [B2] single directional side light upper-left 45° cool white 6500K, deep shadows 15% brightness, cold rim light on blade edges. [B3a] orange Getsuga self-luminescence. [B3b] orange rim light fading to cool, fragment white self-light

style: Bleach anime, high contrast cel shading, sharp angular line art, strong outer silhouettes, speed-varying line weight, cold blue-black shadows, negative space composition, orange #E8760B as only power effect color, 9:16 portrait
```

**[间 embedded]**: Yhwach eye close-up still for 1.5s with zero movement — stillness as power statement. Then Ichigo showcase slow dolly-in 0.3m over 3s — whole video's only breathing moment. Then 4s static with final 1s orange spark — silent danger signal. Then Getsuga burst 2s. Then dissipation 1.5s.

### 本段引用参考图（Seedance reference_image）

段 2 生成时传入以下 reference_image：

- `assets/ref-images/033_char_identity_YhwachOfficialFull_v01.png` — [ANTAGONIST] Yhwach 身份复位锚定（B3c 面部+全知全能姿态参考）
- `assets/ref-images/034_char_identity_YhwachOfficialFace_v01.png` — [ANTAGONIST] Yhwach 多瞳红瞳特写锚定（B3c 全知全能眼部参考）

Tier 0 段间末帧锚定：`[待段 1 末帧就绪后嵌入 — T003-B1-lastframe.png]`（不计入 9 图槽限，用于延续段 1 Ichigo 剪影+白色碎片视觉状态）。

### 段 2 Prompt（~14.5s）

```text
duration_hint: 15
negative_prompt: photorealistic rendering, 3D shading, continuous fight motion, soft focus, dissolve transitions, warm glow filters, pink candy colors, multiple characters in same frame (max 2 characters), whip-pan, crane shot, complex tracking, text rendering artifacts

reference_image: assets/ref-images/033_char_identity_YhwachOfficialFull_v01.png — [ANTAGONIST] Yhwach full body identity anchor, P0 official source, bleach-anime.com. assets/ref-images/034_char_identity_YhwachOfficialFace_v01.png — [ANTAGONIST] Yhwach face close-up for Almighty eye reference, P0 official source, bleach-anime.com. [段间锚定:待段1末帧就绪后嵌入—T003-B1-lastframe.png] — Tier 0 forced reference, not counted in 9-image limit. Purpose: continuity anchor, extend segment 1 Ichigo silhouette visual state into segment 2 opening

scene: [B3c] Falling white fragments continuing from segment 1, dark void background, Yhwach face emerging through fragments. V=2 face + fragments only. [B3d] Soul Society white palace silhouette against absolute black sky, traditional Edo-style architecture, horizontal crack line spreading, white debris falling. V=2 white silhouette + crack lines + black sky. [B3e] Three ring silhouettes arranged in triangle formation in dark void, white line art, crack lines spreading from one ring edge to all three. Pull-back from medium to wide. V=2 rings + crack lines + black void. [B4a] Absolute black. Then Chinese characters "禍進" exploding into center frame, broken clerical script style, white 100% brightness, micro-fractures on surface, shatter after 1.5s. [B4b] Pure black, white text CTA. [B4c] Absolute black 2.5s silence

subject: [ANTAGONIST] Yhwach face extreme close-up emerging through falling white fragments, red eyes transformed to Almighty state — dense multiple concentric pupils covering entire visible iris, kaleidoscope pattern, 1/3 face in deep shadow, thick beard texture, zero expression, [段间锚定:延续段1剪影状态]. Then Soul Society white palace pure silhouette, simple geometric silhouette, Edo-style roofs, horizontal crack lines, white debris fall. Then three ring silhouettes forming as pure white line art in triangle arrangement, fracture propagation one after another, frame pulls back. Then absolute black vacuum pause 0.5s. Then "禍進" characters center frame, white 100% broken clerical script, fractured edges, ink-splash gradient to cool gray, shatter dispersion after 1.5s. Then text "BLEACH 千年血战篇" upper 1/4 small font, "搜索"千年血战"看完整动画" lower 3/4 bold large font on black. Then absolute black 2.5s

camera: static face close-up with fragment depth layering (15.5-17.5s). Static wide angle building shot (17.5-19.5s). Slow pull-back medium to wide over 2.5s (19.5-22s). Fixed frame center for "禍進" (22.5-24.5s). Fixed frame text card (24.5-27.5s). Absolute black (27.5-30s). All hard cuts

lighting: [B3c] white fragment self-lit cool tone, Yhwach face emerges from black, red eyes warm. High contrast — bright fragment vs dark face. [B3d] architecture self-illuminated pure white, crack interior bright white glow, no external light. [B3e] ring line art self-illuminated, no ambient light. [B4] character self-lit, no environment light

style: Bleach anime, high contrast, negative space dominant, abstract geometric minimal for B3e, broken brush-ink calligraphy for B4, pure white on absolute black, 9:16 portrait

**[间 embedded]**: Yhwach static face 2s — eye movement alone carries meaning. Building crack 2s — continuous fracture motion with static camera. Three rings pull-back 2.5s — accelerating camera, last 0.5s silence building. Vacuum pause 0.5s absolute black and absolute silence — the most important MA in whole video. CTA 3s reading window. Afterglow black 2.5s action window
```

---

## 7. 负向提示（全局）

```
photorealistic rendering, 3D shading, continuous fight motion, soft focus, dissolve transitions, warm glow filters, pink candy colors, multiple characters in same frame (max 2 characters), whip-pan, crane shot, complex tracking, smooth motion blur, blur effects, low contrast, gray midtones, realistic fabric physics, real-time rendering artifacts, uncanny valley, text rendering artifacts, glowing eyes (Yhwach only exception), motion smearing on fast cuts, frame interpolation artifacts
```

---

## 8. 跨节拍不变量

### 视觉不变量

| 维度     | 不变量                                                                                                                         | 覆盖拍    |
| -------- | ------------------------------------------------------------------------------------------------------------------------------ | --------- |
| 角色 1   | [ANTAGONIST] Yhwach — 白色军服+深红斗篷+红瞳多瞳+无武器+绝对静止。可变：全知全能时瞳孔密度                                    | B1, B3c   |
| 角色 2   | [PROTAGONIST] Ichigo True Shikai — 黑色死霸装+橙刺发+双斩月（大刃镂空+小刃无柄中空）。可变：灵压颜色（黑→橙）                | B2, B3a-b |
| 场景色调 | B1: 冷色域（蓝白黑）+ 红瞳唯一暖色 → B2: 中性偏冷（黑+橙）→ B3: 色彩冲突（冷蓝+暖橙）→ B4: 纯黑白                           | 全拍      |
| 光照     | 全片高对比，暗部深蓝黑 5-15%，冷白 rim light                                                                                   | 全拍      |
| 转场     | 仅硬切，禁止溶解/柔焦/渐变/翻页                                                                                                | 全拍      |
| 构图     | 剪影优先，负空间构图，角色在画面边缘或中心极小                                                                                 | 全拍      |
| 景别     | 特写浅景深→中景固定→全景深广角                                                                                               | 按拍分配  |
| 材质     | 4 材质类：fabric(cotton-matte) 死霸装/灭却师服、metal(steel-brushed) 斩魄刀、synthetic(glossy) 灵压/灵子、VFX(debris) 裂痕碎片 | 全拍      |
| 禁止色   | 粉色、糖果色、高饱和绿、暖调滤镜、大面积高明度色彩                                                                             | 全拍      |

### 不变量重合度

| 相邻拍对   | 不变量重合                                          | 保护策略                                    |
| ---------- | --------------------------------------------------- | ------------------------------------------- |
| B1 → B2   | 高对比光照系统 + 硬切转场 + 剪影优先构图            | 角色突变被光照系统一致性补偿                |
| B2 → B3   | [PROTAGONIST] + [WEAPON_ZANGETSU] 外观 + 负空间构图 | Ichigo 实体连续出现 + 黑背景统一            |
| B3a → B3b | 同一场景（橙色消散） + Ichigo 剪影 + 全黑背景       | 物理连续性——能量释放后余韵                |
| B3b → B3c | 白色碎片延续 + 全黑背景                             | **段边界唯一强制不变量**：碎片+黑背景 |
| B3c → B3d | 碎片延续（Yhwach → 瀞灵廷） + 黑白高对比           | 视觉主题延续（崩坏主题）                    |
| B3d → B3e | 碎裂主题 + 黑白极简 + 无背景                        | 从建筑崩坏递进到三界崩坏                    |
| B3e → B4  | 碎裂主题 → 祸进标题 + 绝对黑背景                   | 举例过渡——从抽象崩坏到具体命名            |

### 身份漂移防御

| 策略                       | 实施                                                                                         |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| 段间末帧强制参考（段边界） | 段 1 末帧 → 段 2 Tier 0 参考，锚定 Ichigo 剪影/碎片/黑背景                                  |
| 锚点复位（段 2 开场）      | B3c prompt 强制引用 Yhwach 外观不变量（见全局一致性前缀）+ Ichigo 外观不变量                 |
| 3-5 拍不变量声明           | B1（Yhwach 首现）→ B3c（Yhwach 再现）间隔 2 拍（≤3 ✓）。B2 的 Ichigo 不变量声明覆盖 B3a-b |
| 光源方向复位               | 每拍在 scene/lighting 字段声明光源方向，不依赖「上一拍延续」                                 |
| 色调一致                   | 首拍（B1 冷色顶光）与尾拍（B4 纯黑白）通过全片高对比不变量连接                               |

---

## 9. 收敛门记录

| 门                | 检查项                 | 状态                        | 依据                                                                                                                                                                                          |
| ----------------- | ---------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ALIGN**   | TOGETHER.md §3 无🔴   | ✅                          | §3 全部 ❌ 已裁决为 ✅/⚠️，无🔴 阻断项。§6 有 🔴 C006/C013（P0 参考图），用户已确认继续                                                                                                   |
| **FreeLOC** | 每拍自包含，不依赖前情 | ✅                          | B1 三重锚定（字幕+星十字徽章剪影+白色军服）；B2 双刀视觉自明；B3 纯奇观无叙事依赖；B4 汉字自为解释 + CTA 明确。script-beats.md 每拍含 FreeLOC 标注                                            |
| **LoL**     | ≥20s 段边界复位       | ✅                          | 2 段各 ~15.5s / ~14.5s < 20s，无需复位。B3→B4 的 0.5s 黑屏复位为节奏设计非 LoL 强制                                                                                                          |
| **ZPC**     | 段级 ASL ≥ 1.8s       | ✅                          | 段 1：~15.5s / 8 shots ≈ 1.9s ASL ✅（B1: 2 shots / B2: 1 shot/2 subshots / B3a-b: 2 shots）。段 2：~14.5s / 6 shots ≈ 2.4s ASL ✅（B3c: 1 shot / B3d: 1 shot / B3e: 1 shot / B4: 3 shots） |
| **IaD**     | 参考图中性表情         | 🟡**部分通过**        | Yhwach 官方源（033 全身+034 面部）✅ 中性表情，官方角色立绘。Ichigo 官方源（036 全身+037 面部）✅ 中性表情，官方角色立绘（单刀形态）。冰宫场景 P0 仍缺，降级为文本描述                        |
| **RefImg**  | 每段 ≥1 参考图        | 🟡**段1通过/段2部分** | 段 1：✅ Yhwach (033+034) + Ichigo (036+037) 参考图已就绪（≥1 ✅）。段 2：⚠️ 依赖段 1 末帧（未生成），已就绪 P0 参考图可作额外身份复位锚定                                                 |

---

## 10. 生成调度

### 拍级调度（段内优先级）

| 优先级                     | 拍                                     | 理由                                                                                |
| -------------------------- | -------------------------------------- | ----------------------------------------------------------------------------------- |
| **P0（规范参考拍）** | B1（Yhwach 首现）+ B2（IchigoTS 首现） | 这两拍的 prompt 精度决定全片 Yhwach/Ichigo 一致性天花板。生成后须人工检查外观一致性 |
| **P1（依赖拍）**     | B3a-e（加速序列） + B4（CTA）          | 依赖 B1/B2 的实体状态延续。B3c 依赖 B3b 段 1 末帧的白色碎片/剪影状态                |
| **P2（新视觉拍）**   | B3e（三界碎裂）+ B4a（祸进标题）       | 全新视觉元素（圆环/汉字），不依赖已有实体。可独立验证后再整合                       |

### 段级调度（末帧链）

```
段 1 生成（首段，无末帧依赖）
  → 提取段 1 末帧（Ichigo 剪影 + 白色碎片）
  → 写入 ai-video/projects/T003/assets/last-frames/T003-B1-lastframe.png
  → 更新段 2 prompt 的 reference_image 字段引用该文件
  → 段 2 生成（以段 1 末帧为 Tier 0 强制参考）
```

**阻塞条件**：段 1 生成失败 → 段 2 无末帧可参考 → 段 2 暂停。此时以文本描述替代（无参考图状态），但视觉一致性下降。

---

## 11. 缝接方案 & 容错

### 最佳情况（P0 参考图就绪后）

1. P0 产出 Yhwach + IchigoTS + 冰宫 参考图 → 替换段 1 prompt 中的文本描述 → 重新生成段 1
2. 段 1 生成后提取末帧 → 段 2 prompt 引用 → 重新生成段 2
3. 最终 2 段硬切拼接（Segment 2 直接承接 Segment 1）

### 容错方案（当前无参考图状态）

| 风险                                     | 影响                   | 补偿                                                                                                                 |
| ---------------------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Seedance 无法正确生成 Yhwach 多瞳红瞳    | 全片 Yhwach 一致性丧失 | ① prompt 精度提升（具体到"iris depth with multiple concentric layers"）；② 参考图产出后替换重生成                  |
| Seedance 无法区分双刀长短刀              | B2 信息点传递失败      | ① 极精确的尺寸比（120cm vs 50cm）+ 握持位置（右手靠下+左手穿中空）描述；② 以「观众看到两把不同形状的刀」为底线目标 |
| 段 1 末帧状态不稳定（运动模糊/光照闪烁） | 段 2 开场无法锚定      | ① B3b 末帧刻意设计为静态剪影+浅 rim light，最低运动状态；② 多生 1-2 段候选末帧选择最佳；③ 纯文本锚定段 2 开场状态 |
| Seedance 15s 硬限导致段 1/2 边缘崩掉     | 段边界切不自然         | 段 1 末帧截取有 0.5s 余量（~00:15.5），Seedance 输出 ~00:14.5-15.5 窗口均可用                                        |
| "禍進" 汉字渲染成乱码                    | B4 Drop 拍失效         | CTA 改为纯英文 "BLEACH: THE CALAMITY — search the full anime now" + 祸进以破碎图形替代文字                          |

### 缝接参数

| 项目            | 值                                                                                                  |
| --------------- | --------------------------------------------------------------------------------------------------- |
| 段间过渡        | 段 1 → 段 2：硬切（末帧→段 2 首帧直接衔接）。B3b 末帧剪影 → B3c 开场碎片延续                     |
| 拍间转场        | 全硬切。0s 过渡。例外：B3a（Getsuga 爆发）从全黑到全橙 = 有效闪白瞬间                               |
| 交叉溶解        | 不使用。Bleach 风格禁止柔和过渡                                                                     |
| B3→B4 真空停顿 | 0.5s 全黑+全静默。在段 2 内部完成，不跨段                                                           |
| BGM 对齐        | B1 低音沉+军靴声 / B2 渐强 / B3 鼓点加速+riser / B4 停顿→重鼓碎裂→fade out→静默。边界误差 ≤0.3s |

---

## 12. SDK 字段就绪检验

| 9 要素             | Seedance 字段       | 映射状态                                | 补偿                                                                                                |
| ------------------ | ------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------- |
| 景别+场景          | `scene`           | ✅ 直接组合                             | —                                                                                                  |
| 主体+动作+实体 tag | `subject`         | ✅ 嵌入`<tag>`                        | entity_tags 字典定义但`to_natural_language()` 未使用，tag 手动嵌入 subject 文本。**已验证** |
| 运镜/动            | `camera`          | ✅ 直接拼入                             | 仅兼容运镜（静态/推/拉）                                                                            |
| 光影               | `lighting`        | ✅ 直接拼入                             | —                                                                                                  |
| 风格+画质          | `style`           | ✅ 拼入                                 | 含 "portrait" 推断 9:16                                                                             |
| **[间]**     | 无字段              | ✅**嵌入 subject/scene 文本末尾** | 见每段末尾`[间 embedded]` 段落                                                                    |
| **负向提示** | `negative_prompt` | ✅ 写入 API 请求体                      | 见 §7                                                                                              |
| **时长**     | `duration_hint`   | ✅ 硬限 15s，int 类型                   | 段 1 ~15.5s（取整 15），段 2 ~14.5s（取整 15）。适配器硬限 15s，超出部分截断                        |

### 丢失字段补偿

- **[间]**：无独立 API 字段 → 嵌入每段 prompt 末尾的 `[间 embedded]` 段落，用自然语言描述停顿/留白/时延
- **entity_tags**：SDK 定义了但未送入 API → 所有 `<tag>` 手动嵌入 `subject` 文本（已在全局一致性前缀和每拍 subject 中实现）
- **参考图引用**：Yhwach 033+034 / Ichigo 036+037 官方源已就绪 → 段 1 直接引用为 reference_image。段 2 末帧锚定仍维持 `[段间锚定:待末帧就绪后嵌入]` 占位，P0 参考图补充为额外引用

---

## 13. 自检

- [X] **裁决完成**：矛盾矩阵完整（M1-M5），三体树收敛，品味否决已检（无触发），叙事节奏锚点确定（B2/B3/B4）
- [X] **节奏完成**：每拍标注镜头/转场/[间]/shot关系。BPM 映射：B1 降 CF=2.0（~2快切）→ B2 CF=1.4（~3中速）→ B3 半速映射 effektiv CF=2.0（物理切频保留）→ B4 CF=0.8（1定帧→3文字镜头）
- [X] **一致性**：跨拍不变量表已声明（§8）+ 相邻拍不变量重合 ≥1 + 首尾拍光源/色调一致（高对比全片）。身份漂移防御已规划（段间末帧+锚点复位+3-5拍声明）
- [X] **prompt 合规**：9要素每拍完整 + Seedance 语法格式化。SDK 就绪（[间]嵌入场景/主体文本，tag嵌入 subject，negative_prompt 已填）。情绪词全部外化（见每拍 mood/lighting/动作描述）
- [X] **工具+段边界**：Seedance 2.0 Mini 选定，15s 硬限驱动 2 段方案。生成调度已规划（P0 P1 P2 + 段级末帧链）
- [X] **收敛门通过**：ALIGN ✅ / FreeLOC ✅ / LoL ✅ / ZPC ✅ / IaD 🟡（Yhwach/Ichigo 官方源已就绪并验证；冰宫仍缺）/ RefImg 🟡（段 1 Yhwach+Ichiogo 参考图已就绪；段 2 依赖段 1 末帧未生成）
- [X] **TOGETHER.md 对齐**：§3 无🔴 阻断；§6 评论已逐条核实并纳入矛盾矩阵；P0 参考图 Yhwach/Ichigo 已就绪（见 §3 对账表更新）
- [X] **素材装配完成**：需求-库存对账已更新（Yhwach/Ichigo P0 就绪 + 冰宫缺货）。候选池已装配（033+034+036+037，Tier 1 优先）。物料催办 backlog 待创建后通知 visual-designer
- [X] **无图阻塞放行**：段 1 ≥1 参考图已就绪（Yhwach 033+034 + Ichigo 036+037 ✅）。段 2 依赖段 1 末帧（未生成）。IaD 已验证 P0 官方源中性表情 ✅
