# 生图确认门: Yhwach 规范参考图 v3

> **资产**：`CHR_T003_bleach_Yhwach_canonical_v01.png`（晋升后命名）
> **状态**：🟡 **已生成，待 v4 决策**
> **生成结果**：035_char_identity_YhwachCanonical_v01.png (2920 KB, 2400x1600)
> **IaD 评估**：部分通过 — 5/13 项 FAIL，2 项模糊
> **依赖**：无（优先产出 — 首个 P0 资产）
> **前置历史**：v1 (028_v01, 9:16, 1 ref) + v2 (028_v02, 3:2, 3 refs: 030+027+010) — 均因参考图质量不足导致面部微特征丢失。**v3 使用新获取的 033 官方全身立绘 + 034 官方面部表情图替代 010 和 030**。

---

## 1. 搜索与查重记录

### 1.1 资产查重（assets/）

| 索引                           | 结果                              |
| ------------------------------ | --------------------------------- |
| `assets/characters-index.md` | 无 Yhwach 条目存在                |
| `assets/characters/`         | 空目录                            |
| **结论**                 | Yhwach 为全新 P0 资产，需从头生产 |

### 1.2 网上搜索记录

已有系统搜索记录参见 `ref-sources-yhwach.md`（2026-07-19，WebSearch + curl 工具链）。关键发现：

| 来源                        | 文件                                                 | 分辨率       | 用途                        |
| --------------------------- | ---------------------------------------------------- | ------------ | --------------------------- |
| bleach-anime.com 官方角色页 | `033_char_identity_YhwachOfficialFull_v01.png`     | 1050x1500 ✓ | **P0 官方全身立绘**   |
| bleach-anime.com 官方表情页 | `034_char_identity_YhwachOfficialFace_v01.png`     | 670x340      | **P0 官方面部表情集** |
| 用户提供                    | `030_char_identity_YhwachLineArtMultiView_v01.png` | 447x447      | 面部线稿（已评估）          |

### 1.3 布局参考图（已有）

`027_lyt_layout_ThreeColumnCharSheet_v01.png` — Seedream 5.0 生成的三栏角色设计稿布局模板，1440x2560。提供 Seedream 所需的多视图空间布局格式。

---

## 2. 参考图声明

### 正参考（Positive References）

| 文件                                                                          | 类型 | 用途                 | 来源             | 质量     |
| ----------------------------------------------------------------------------- | ---- | -------------------- | ---------------- | -------- |
| ![ref-033](../assets/ref-images/033_char_identity_YhwachOfficialFull_v01.png) | CHR  | id+outfit+color (P0) | bleach-anime.com | 1050/H/N |
| ![ref-034](../assets/ref-images/034_char_identity_YhwachOfficialFace_v01.png) | CHR  | id+face (P0)         | bleach-anime.com | 340/L/N  |
| ![ref-027](../assets/ref-images/027_lyt_layout_ThreeColumnCharSheet_v01.png)  | LYT  | layout               | ai:Seedream      | 1440/H/N |

**三图分工**：

- **033**（最高权重）：角色身份锚定。全身比例、服装细节（白风衣+十字徽+暗红披风+黑手套+白裤+黑靴）、发型、胡须、中性表情。官方源 — 权威性最高。
- **034**（补充面部）：面部特写。多瞳红瞳结构、眼窝深度、额头皱纹、无眉眉骨。官方源。分辨率 670px 虽未达 1024 门槛，但作为官方面部参考权威性弥补分辨率不足。
- **027**（布局格式）：提供 Seedream 所需的「左肖像 / 中3/4面 / 右全身」三栏布局格式。泛用角色填充，不参与身份锚定。

### 负面参考（Negative References）

无。所有文件均与 T003 Bleach TYBW 风格一致。

### 参考图策略对比（v2 vs v3）

|          | v2 (028_v02)           | v3 (本门)                          | 改进理由                                                                                  |
| -------- | ---------------------- | ---------------------------------- | ----------------------------------------------------------------------------------------- |
| ref[0]   | 030 面部线稿 (447x447) | **033 官方全身** (1050x1500) | v2 尝试用 030 做面部锚定，但 447px 过低 → 模型无法提取微特征。033 作为身份锚定权重最高   |
| ref[1]   | 027 布局模板           | 027 布局模板 (不变)                | 布局参考需求不变                                                                          |
| ref[2]   | 010 场景图 (1920x1080) | **034 官方面部** (670x340)   | 010 为场景截图（Wahrwelt 冰宫前全身），非中立身份参考，可能引入场景偏见。034 为纯面部参考 |
| 数量     | 3                      | 3                                  | 不变，符合 1-3 铁律                                                                       |
| 030 线稿 | 作为 ref 传入          | 降级为 prompt 文本描述             | 030 细节通过精确文本描述传递，不依赖低分辨率图片                                          |

---

## 3. Seedream Prompt

### 3.1 Prompt 文本

> **设计思路**：v2 的 prompt 已在面部微特征（额横纹、无眉、深眼窝）上做了精确描述，但模型未能从 030 的低分辨率线稿提取这些特征。v3 保持 v2 的面部描述精度（已验证为正确的特征描述），将身份锚定图从 010（场景截图）改为 033（官方全身立绘），并新增 034（官方面部表情集）作为面部补充参考。面部微特征的精确文本描述 + 官方彩色面部参考图（034）的组合有望弥补 v2 的不足。

```
BLEACH anime style character design reference sheet in 3:2 landscape horizontal canvas (2400x1600), pure black background #000000. The image is divided vertically into three equal columns.

All three views share the same neutral expression character with identical facial structure, hair, and clothing across all columns.

---

LEFT COLUMN (1/3 width = ~800px): FRONT-FACING PORTRAIT
Frame: head to upper chest. Character centered vertically in the column area.
Expression: NEUTRAL — zero expression. Mouth naturally closed, lips forming a straight horizontal line. Eyelids half-closed at approximately N/3 opening, upper eyelid covering the top 1/3 of the iris. Pupils looking straight forward at camera — symmetrical and centered.
Face: Rectangular broad face with wide jaw and chin. Deep-set eyes with pronounced brow ridge overhang — the brow ridge projects forward noticeably above the eye socket, casting a shadow over the upper eyelid. Mutton chop sideburns starting from front of each ear, extending along jawline to connect with mustache at mouth corners. Chin center clean-shaven. Mustache covering upper lip only, not extending below lip line. NO eyebrows — the brow ridge area is completely smooth with zero hair marks. Deep horizontal forehead crease — 3 distinct deep lines across the full width of the forehead, clearly visible and prominent. High prominent cheekbones creating shadow planes beneath them.
Lighting: Symmetrical front-top 45-degree light, minimal shadow on face.
Hair: Long black hair brushed back, temple hairline receded, widow's peak at center, sideburns reaching jaw angle.

---

CENTER COLUMN (1/3 width = ~800px): THREE-QUARTER (3/4) PROFILE PORTRAIT
Frame: head to upper chest, matching left column height. Character rotated approximately 45 degrees to right, showing facial depth.
Face: Same facial features as left column from rotated angle. Deep eye socket visibly recessed — the 3/4 view shows the orbital bone depth clearly with the brow ridge casting a visible shadow over the recessed eye. Mutton chop sideburn visible along the visible jawline edge. Mustache visible on upper lip profile. Ear visible — standard human ear shape, no pointed features. Forehead wrinkles visible in profile — 3 horizontal lines across the forehead surface.
Lighting: 45-degree top-left sidelight. Deep shadow on far side of face. Cool white rim light (1-2px) on the profile edge separating the jawline and nose bridge from the background.
Note: The fur collar of the white Quincy coat is visible at the bottom of this frame.

---

RIGHT COLUMN (1/3 width = ~800px): FULL-BODY STANDING POSE
Frame: Full figure from head to toe, centered vertically in column. Character facing forward, standing upright.
Pose: Arms lowered naturally at sides, hands slightly visible. Feet shoulder-width apart. Weight balanced evenly on both legs.
Clothing (head to toe):
  - White double-breasted Quincy trench coat — long white coat reaching below the knees, black inner layer visible at the lapel opening. Double row of black buttons. Wandenreich golden cross emblem centered on chest (symmetrical four-pointed cross with short arms).
  - Tattered ankle-length crimson-black cape draped over both shoulders. Dark red-black color with subtle fabric wear at the edges. Red ribbon tied near the neck at the front. Single large button closure on the left side.
  - Black tight gloves reaching from wrist to just below the elbow cuff of the coat. Gloves are skin-tight with subtle wrinkle lines at the knuckles.
  - White straight-leg trousers, falling cleanly with minimal folds.
  - Black trench boots — mid-calf height, flat sole, no buckles or decorations.
  - Fur collar visible at the top of the coat — dark grey fur trim around the collar edge.

Physical build: Imposing tall broad-shouldered older male build, 200cm height (extremely tall figure compared to standard anime proportions — the full-body should show a towering vertical presence).

---

CONSISTENCY ACROSS ALL THREE VIEWS:
- Same hair: Long black hair reaching mid-back, brushed back, temple hairline receded with widow's peak. Sideburns reaching jaw angle. Strands lie flat and smooth with subtle separation lines.
- Same skin: Pale skin tone with warm undertone #D4C4B4 base.
- Same eye color: Red iris color #CC2233 (outer ring) to #FF4466 (inner ring) gradient — multi-pupil structure where the inner iris has a secondary pupil-like ring visible, creating a layered "almighty eye" appearance. Eyes are static and non-glowing — the red is the natural iris color not an emission.
- Same facial features: rectangular face, broad chin, high cheekbones, deep-set eyes with prominent brow ridge, mutton chop sideburns + mustache, NO eyebrows (smooth brow ridge), deep forehead crease (3 distinct lines).
- Same clothing and proportions across all views.

STYLE AND RENDERING:
- Sharp clean linework with strong outer silhouette (Bleach cel-shading standard).
- Hard cel-shaded flat colors with deep blue-black shadows at 10% brightness.
- 45-degree top-left sidelight casting deep shadows. Shadow areas shift toward deep blue-black, not neutral grey.
- Cool white rim light (1-3px) on character edges separating figure from pure black background — present in all three views.
- Background is pure black #000000. No texture, no gradient, no atmospheric effect.

No text labels, no annotations, no arrows, no color swatches, no measurement lines. No logos, no watermarks. No weapons, no sword, no bow. No smile, no anger, no arrogance, no action pose, no fighting stance. No multiple characters. Pure black background only. Professional anime character design sheet presentation.
```

### 3.2 Negative Prompt

```
realistic, 3D, photorealistic, smiling, arrogant expression, angry, laughing, grimace, smirking, action pose, fighting stance, weapon, sword, bow, gun, blade, zanpakuto, glowing eyes, glowing aura, spiritual pressure, holy energy, text, labels, numbers, annotations, arrows, color swatches, measurement lines, watermark, signature, logo, detailed background, gradient background, multiple characters, Uryu, Ishida, secondary character, Stern Ritter, Quincy army, school uniform, modern clothes, street, building, daytime, sunlight, warm lighting, full beard, goatee, stubble, chin hair, soul patch, eyebrows, thick eyebrows, bushy eyebrows, heavy eyebrows, visible eyebrows, looking away, looking up, looking down, side-eye, portrait, vertical, 9:16, ice palace, Wahrwelt, ice, snow, castle, frost, warm glow filter, soft focus, dissolve, gradient transition
```

---

## 4. 生成参数

| 参数                         | 值                                               | 理由                                                                                                       |
| ---------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| **Model**              | `doubao-seedream-5-0-260128` (5.0 Pro)         | 目前可用最高版本。5.0 支持`reference_image_url` 布局锚定                                                 |
| **Size**               | `2400x1600` (3:2 横版)                         | 三栏设计稿需要横版。每栏 ~800px 宽度为面部细节提供足够像素。遵循 asset-lab §4 "多视图合成帧使用横版" 约束 |
| **Output format**      | `png`                                          | 晋升要求                                                                                                   |
| **Watermark**          | `false`                                        | 参考图不需要水印                                                                                           |
| **optimize_mode**      | `standard`                                     | Pro 模型默认优化等级                                                                                       |
| **Reference count**    | 3                                                | 符合铁律 1a（1-3 张）                                                                                      |
| **Reference image[0]** | `033_char_identity_YhwachOfficialFull_v01.png` | **身份锚定（P0 官方）** — 全身立绘，服装/比例/胡须/瞳色权威参考                                     |
| **Reference image[1]** | `034_char_identity_YhwachOfficialFace_v01.png` | **面部补充（P0 官方）** — 面部表情集，额横纹/眼窝/多瞳结构官方参考                                  |
| **Reference image[2]** | `027_lyt_layout_ThreeColumnCharSheet_v01.png`  | **布局模板** — 三栏空间布局格式，不参与身份锚定                                                     |

---

## 5. 构图描述

三栏角色设计稿，纯黑背景 `#000000`：

```
┌─────────────────────────────────────────────────────────────┐
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  │
│  │  正面肖像      │  │  3/4 侧面     │  │  全身站姿      │  │
│  │  (头至胸)      │  │  (头至胸)     │  │  (头至脚)      │  │
│  │               │  │               │  │               │  │
│  │  中性表情     │  │  中性表情     │  │  白风衣+披风   │  │
│  │  平视镜头     │  │  45度右转     │  │  十字徽章可见  │  │
│  │  无眉/深眼窝  │  │  深眼窝表现   │  │  黑手套+白裤   │  │
│  │  额横纹3条    │  │  额横纹侧视   │  │  黑靴+双手垂放 │  │
│  │               │  │               │  │               │  │
│  │  侧顶光45°    │  │  左上侧光     │  │  全局侧顶光    │  │
│  └───────────────┘  └───────────────┘  └───────────────┘  │
│                   纯黑背景 #000000                          │
└─────────────────────────────────────────────────────────────┘
```

设计原则：

1. **身份信息密度最大化** — 三栏展示不同视角，满足 Argus 身份分布需求 + KeyFrame-Compass ≤1 帧约束
2. **中性表情**（零表情）— 面部通道仅承载身份信息，表情由 3D 偏移场独立控制（三维解耦原则）
3. **纯黑背景** — 消除背景干扰，角色轮廓清晰，便于 Seedance Reference Lock 提取稳定特征

---

## 6. v3 vs v1/v2 改进总结

| 对比项       | v1 (028_v01)   | v2 (028_v02)                                           | v3 (本门)                                                                   |
| ------------ | -------------- | ------------------------------------------------------ | --------------------------------------------------------------------------- |
| 比例         | 9:16 竖屏      | 3:2 横版                                               | 3:2 横版（沿袭 v2 改进）                                                    |
| 参考图数量   | 1              | 3                                                      | 3                                                                           |
| 参考图来源   | 010 场景截图   | 030(线稿)+027(布局)+010(场景)                          | **033(官方全身)+034(官方面部)+027(布局)**                             |
| 核心身份锚定 | 场景截图 (010) | 线稿 (030, 447px)                                      | 官方全身立绘 (033, 1050px)                                                  |
| 面部参考     | 无             | 线稿 (030, 447px)                                      | 官方彩色面部 (034, 670px)                                                   |
| v2 遗留问题  | —             | 额横纹未呈现、眉毛未完全消失、眼窝深度不足、面容偏年轻 | **待验证** — 预期通过 033(高分辨率官方源) + 034(官方面部) 的组合改善 |
| 030 线稿处理 | —             | 作为 ref 传入（模型未能提取细节）                      | 降级为 prompt 文本描述（精确术语保留）                                      |

---

## 7. 风险登记

| #            | 风险                                                                 | 等级         | 缓解措施                                                           | v3 实际结果                                                                                             |
| ------------ | -------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| R1           | 034 分辨率 670px 仍不足以让模型提取额横纹/无眉等微特征               | 中           | 三层强化：精确术语 + explicit prohibition + 033 辅助               | **未缓解** — 额横纹缺失、无眉仍不确定。纯文本+低分辨率面部参考不足以克服模型默认的"年轻平滑"偏好 |
| R2           | 033 为全身立绘，面部在整图中占比小，对面部参考价值有限               | 低           | 面部特写依赖 034 + prompt 文本。033 负责服装/比例                  | **如预期** — 服装/比例/身份正确捕获，面部微特征仍靠 034                                          |
| R3           | 模型持续忽略"无眉"特征                                               | 高           | 追加负面词。若 v3 仍未解决 → 需更高分辨率面部图                   | **部分缓解** — 眉区有残留阴影，pixel-level 不干净                                                |
| R4           | 面容偏年轻/修长                                                      | 中           | older male 描述词 + 方形脸描述 + 033 年长面容参考                  | **未缓解** — 面容仍偏年轻（30-35 岁而非 50+）。模型无法从文本推断年龄感                          |
| **R5** | Seedream 5.0 无法理解"同一角色在不同栏位呈现不同视角"的布局语义      | **高** | 左栏和中心栏均为正面视角。模型按"整体一致性"优化，不擅长差异化渲染 | **v3 确认** — 从 v1(单图) 到 v2/v3(三栏) 均未解决视角差异化                                      |
| **R6** | 三栏设计稿每栏 ~800px 宽，面部细节不足以用于 Seedance Reference Lock | 中           | 即使生成成功，每栏面部 ~200x300px 对视频身份锚定不足               | **v3 确认** — 三栏设计稿适合作"案例参考"，不适合直接作为视频参考图                               |

---

## 8. 生成后验证清单（Step 2 — 已完成）

> **验证时间**：2026-07-20 01:35 UTC
> **IaD 检查人**：visual-designer（手动 IaD）
> **总体评估**：**部分通过** — 成功捕获三栏设计稿布局和基础身份特征，但在面部微特征（3/4 侧面、额横纹、眉骨结构）和角色年龄感上存在不足。不建议晋升至 assets/。需要 v4 策略调整。

- [X] **比例正确**：3:2 横版 2400x1600 ✓
- [X] **三栏完整性**：左/中/右三栏正确渲染 ✓
- [ ] **IaD 中心栏 3/4 侧面**：**FAIL** — 中心栏与左栏均为正面视角，未按 prompt 渲染为 45 度 3/4 侧面。这是 prompt 最明确的指令之一。模型未能理解"左右不同视角"的布局语义
- [X] **IaD 中性表情**：零表情，口自然闭合，无笑容/愤怒/傲慢 ✓
- [ ] **额横纹（034 验证）**：**FAIL** — 3 条深横纹不可见。面部平滑，缺乏中老年角色应有的额纹
- [ ] **无眉（034 验证）**：**模糊** — 从 2000x1333 显示比例观察，眉骨区接近平滑但仍有微妙阴影。原始分辨率（2400x1600）下需进一步确认，但大概率仍有眉部残留
- [ ] **深眼窝（034 验证）**：**FAIL** — 眼眶深度不足。未呈现"眉骨前突覆盖上眼睑"的标志性深眼窝
- [X] **胡须形态（033 验证）**：络腮胡+八字胡+下颌中央干净 ✓
- [X] **红瞳（033+034 验证）**：红瞳可见 ✓（多瞳结构在面部占比下难以确认）
- [X] **纯黑背景**：纯黑 #000000 无意外元素 ✓
- [X] **角色三栏一致性**：同一面部/服装/发型跨三栏一致 ✓
- [X] **服装完整（033 验证）**：白风衣+金十字徽+暗红披风+黑手套+白裤+黑靴 ✓
- [X] **无武器/无特效**：无刀剑/灵压/灵力特效 ✓
- [X] **分辨率**：短边 1600 ≥ 1024px ✓
- [ ] **年龄感**：**FAIL** — 面容偏年轻。prompt 指定 "imposing tall broad-shouldered older male" 但生成的更像 30-35 岁而非 Yhwach 应有的 50+ 岁面容。这是 v2 的遗留问题，v3 使用 033 官方立绘仍未改善

---

## 9. 产出文件清单（Step 2 — 已完成）

| 文件     | 路径                                                                                      | 大小               | 状态                          |
| -------- | ----------------------------------------------------------------------------------------- | ------------------ | ----------------------------- |
| 主图     | `ai-video/projects/T003/assets/ref-images/035_char_identity_YhwachCanonical_v01.png`    | 2920 KB, 2400x1600 | ✅ 已生成（草稿命名，未晋升） |
| 描述文件 | `ai-video/projects/T003/assets/ref-images/035_char_identity_YhwachCanonical_v01.png.md` | 2325 B             | ✅ 已创建                     |
| 晋升目标 | `assets/characters/CHR_T003_bleach_Yhwach_canonical_v01.png`                            | —                 | ❌ 暂缓 — IaD 不通过         |

## 10. 晋升条件（Step 2 — 评估结果）

- [ ] IaD 检查通过（本文件 §8 5/13 FAIL）— **不通过，暂缓晋升**
- [X] 分辨率 ≥1024px 短边 — **通过**（1600px）
- [X] .png 格式 — **通过**
- [ ] 至少一段 Seedance 视频验证有效 — **未执行**（IaD 未通过则不进行视频验证）
- [ ] 命名按全局规范 — **不执行**
- [ ] 更新 `assets/characters-index.md` — **不执行**

> **决策**：v3 不晋升至 assets/characters/。需要 v4 策略调整。

---

## 11. v3 生成总结与分析

### 11.1 与 v1/v2 对比

| 对比项     | v1         | v2                          | v3                                    |
| ---------- | ---------- | --------------------------- | ------------------------------------- |
| 比例       | 9:16 单图  | 3:2 三栏                    | 3:2 三栏                              |
| 参考图     | 1 场景截图 | 3（线稿+布局+场景）         | 3（**官方全身+官方面部+布局**） |
| 布局       | 单肖像     | 三栏                        | 三栏                                  |
| 面部微特征 | —         | 额横纹/无眉/深眼窝 均未呈现 | **同 v2 — 仍未改善**           |
| 3/4 侧面   | —         | ❌ 未渲染                   | ❌ 同 v2                              |
| 服装正确率 | 中         | 高                          | **高** ✓                       |
| 年龄感     | 年轻       | 偏年轻                      | **偏年轻（同 v2）**             |

### 11.2 根本原因分析

v3 的核心假设是：用**官方源**（033 全身立绘 + 034 面部表情集）替代**低质源**（030 线稿 + 010 场景截图）可以改善面部微特征。结果证伪：

1. **Seedream 5.0 的能力边界**：该模型擅长生成"好看的单一角色图"，但在以下方面有系统性限制：

   - **多视角布局理解**：无法理解"同一角色在不同栏位呈现不同视角"的布局语义（三栏均正面）
   - **面部微特征控制**：无法从低分辨率面部参考（670px）或 prompt 文本提取细微的面部特征
   - **年龄感推断**：无法从 "older male" 文本推断出 50+ 面容，默认输出 30-35 岁
2. **三栏设计稿策略的系统性问题**：

   - 每栏 ~800px 宽，面部区域 ~200x300px — 不适合用作 Seedance 视频生成的身份锚定参考
   - 即使完美生成，也需要拆分为单独的高分辨率面部/全身图供视频阶段使用
3. **034 670px 的分辨率瓶颈**：官方面部参考图仅 670px（短边不足 1024px），模型无法从中提取额横纹/无眉等微特征。这在 v3 中被标记为中风险，实际结果证实了风险。

### 11.3 v4 策略推荐

| 策略                             | 说明                                                                                                                                      | 优先级 |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| **放弃三栏设计稿**         | Seedream 5.0 不适合生成多视图布局。改为生成**单图高质量角色肖像**（正面/中性表情/纯色背景）作为主要身份参考                         | P0     |
| **分图策略**               | 不再尝试用"一张图包含所有视图"。改为生成 2-3 张独立参考图：(1) 高分辨率正面肖像 (2) 全身服装图 (3) 半侧面部特写。每张图独立生成，独立质控 | P0     |
| **寻找更高分辨率面部参考** | 034 的 670px 不够。尝试搜索 ≥1024px 的 Yhwach 面部特写设定图                                                                             | P1     |
| **改用单图-单角色-单视图** | 移除复杂的布局要求。prompt 简化为"正面肖像，纯色背景，角色全身"，降低模型理解负担                                                         | P1     |
| **验证工具边界**           | 如果连续 4 次 Seedream 失败 → 考虑更换工具（如 ComfyUI 手动组合、或直接使用官方动画截图作为参考，不经过 Seedream 生成）                  | P2     |
