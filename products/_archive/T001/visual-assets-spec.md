# 死神祸进篇 — 视觉资产规格

> 对应 `topics/T001/visual-world.md` 视觉宪法。产出自 visual-designer。
> 工作流：先存 `ai-video/projects/T001/assets/ref-images/`（草稿命名）→ 视频验证有效后晋升 `assets/{characters,scenes}/`（规范命名 + 更新子索引）。

---

## 0. 复用查重结果

### 角色资产（assets/characters-index.md）

| 资产 | 路径 | 质量 | 风格 | 复用决策 |
|------|------|------|------|---------|
| Ichigo canonical | `assets/characters/CHR_DEMO_Ichigo_canonical_v01.png` | ⚠ | bleach | **有条件复用** — 单刀形态参考面部/体型，但 TYBW 核心为双刀形态，需新建资产 |
| Ichigo multi-view | `assets/characters/CHR_DEMO_Ichigo_multi-view_v01/` | ⚠ | bleach | **有条件复用** — 多视角面部分布有效，可入 Seedance 槽辅助面部锚定 |
| Rukia canonical | `assets/characters/CHR_DEMO_Rukia_canonical_v01.png` | ⚠ | bleach | **待复检后复用** — TYBW 露琪亚设计无大改，IaD 复检通过后直接引用 |

### 场景资产（assets/scenes-index.md）

| 资产 | 路径 | 质量 | 风格 | 复用决策 |
|------|------|------|------|---------|
| Karakura-Rooftop | `assets/scenes/SCN_DEMO_KarakuraRooftop_scene-dusk_v01.png` | ⚠ | bleach | **有条件复用** — PV 开场色调可参考（暖橙暮光），但主线不在天台 |
| SoulSociety-Streets | `assets/scenes/SCN_DEMO_SoulSocietyStreets_scene-day_v01.png` | ⚠ | bleach | **有条件复用** — 尸魂界传统建筑参考，但需新产战后废墟版 |

### 复用条件

1. **先 IoD 复检**：DEMO 资产最后验证日 2026-07-18，距当前 > 60 天 → 标 ⚠。须通过中性表情验证
2. **风格兼容**：六维推导在 bleach 下成立（已确认，见 visual-world.md 第 2 节）
3. **索引更新**：复检通过后更新子索引 `appears_in_topic: T001` + `appears_in_style: bleach`

---

## 1. CHR — 一护双刀形态（P0）

| 字段 | 值 |
|------|----|
| **工作命名**（ref-images 阶段） | `T001_IchigoDualWield_ref_v01.png` |
| **规范命名**（晋升 assets/ 后） | `CHR_T001_bleach_Ichigo_canonical_v01.png` |
| **视角要求** | 1 帧复合图（正面 + 轻微半侧 15° + 全身入画） |
| **IaD 状态** | 中性表情，眼神平视前方，嘴角微微下抿（一护默认冷酷） |
| **背景** | 纯色深色 #101418，无环境干扰。角色剪影可以清晰剥离 |
| **材质压缩** | `fabric(shinigami-shroud: black, sharp-fold, semi-matte) + bios(hair: spiky, orange, specular) + metal(dual-zanpakuto: silver, polished-edge, high-reflect)` |

### 外观特征

| 部位 | 描述 |
|------|------|
| 姿势 | 直立重心偏左，双刀自然垂握（非战斗态），刀尖触地或悬垂 |
| 面部 | 锐利下颌线，棱角分明鼻梁。眉梢微压（常驻冷酷表情基底） |
| 头发 | 橙色刺状不规则发束，发束顶面有连续亮橙高光带跨越多束。发型=剪影辨识度核心 |
| 服装 | 黑色死霸装，宽肩窄腰。褶皱锐利分明，线条干脆肯定。并非布艺，是态度 |
| 短刀 | 虚代表。黑色刀鞘，刀柄卍字纹样。刀身较窄，收于腰右侧 |
| 长刀 | 死神代表。银色刀鞘，刀柄深蓝灰。刀身较宽大，收于腰左侧 |
| 腰带 | 死霸装黑腰带，简单结系 |

### 色指定

| 部位 | 基色 | 阴影色 | 高光色 |
|------|------|--------|--------|
| 发 | #D0700B | #502808 | #F09830 |
| 死霸装 | #1A1E28 | #060810 | #E0E8F0（边缘 rim） |
| 肌肤 | #F0E8E0 | #B8A8B0 | #FFFFFF（鼻梁/颧骨） |
| 短刀 | 刀柄 #101418 / 刀刃 #C0C8D0 | — | #FFFFFF（刃线） |
| 长刀 | 刀柄 #283038 / 刀刃 #D0D8E0 | — | #FFFFFF（刃线） |

---

## 2. CHR — 友哈巴赫（P0）

| 字段 | 值 |
|------|----|
| **工作命名**（ref-images 阶段） | `T001_Yhwach_ref_v01.png` |
| **规范命名**（晋升 assets/ 后） | `CHR_T001_bleach_Yhwach_canonical_v01.png` |
| **视角要求** | 1 帧复合图（正面，半身入画，轻微俯视 10° 彰显威压） |
| **IaD 状态** | 中性表情，眼神平视远端（非直视镜头），嘴角微含 — 居高临下的平静 |
| **背景** | 纯色暗红黑 #180810，暗示灭却师黑暗气质 |
| **材质压缩** | `fabric(quicy-cape: black, flowing, semi-gloss) + fabric(quicy-inner: white, silk-like, smooth) + bios(eye: multi-pupil, red-irised, ominous)` |

### 外观特征

| 部位 | 描述 |
|------|------|
| 姿势 | 直立，黑色披风完全垂地覆盖大部分身体。双臂交叠于胸前或自然下垂。肩部放松（绝对自信） |
| 面部 | 锐利下颌线，鼻梁高挺。山羊胡（黑色，覆盖下巴区域）与长发一体成轮廓 |
| 头发 | 黑色中长发，部分遮面。发质偏直顺，不僵硬——长发从头顶自然垂坠 |
| 服装 | 黑色长大披风（外）+ 白色灭却师传统内装（领口）+ 黑色长裤。灭却师十字缀饰可见于领口/胸前 |
| 眼睛 | **标志性多瞳**——眼白中多个黑色瞳孔同心分布。这是角色辨识度最高特征。眼白略偏黄 |
| 手 | 手指修长，指甲清晰。手部线条锐利 |

### 色指定

| 部位 | 基色 | 阴影色 | 高光色 |
|------|------|--------|--------|
| 发/须 | #101418 | #000000 | #404448 |
| 披风 | #101418 | #000000 | #C8D0D8（rim edge） |
| 内装 | #E8ECF0 | #A0B0C0 | #FFFFFF |
| 肌肤 | #E8DCD0 | #A09080 | #FFFFFF（颧骨） |
| 眼 | 眼白 #F0F0E8 | — | 瞳 #000000（多瞳布局） |

---

## 3. SCN — 尸魂界战场废墟（P0）

| 字段 | 值 |
|------|----|
| **工作命名**（ref-images 阶段） | `T001_SoulSocietyBattlefield_ref_v01.png` |
| **规范命名**（晋升 assets/ 后） | `SCN_T001_bleach_SoulSocietyBattlefield_scene-war_v01.png` |
| **视角要求** | 广角俯视宽景（24mm 等效），画面中下 60% 废墟 + 上部 40% 天空留白 |
| **构图** | 传统建筑残骸从画面底部向深处延伸，引导线指向远方天际线 |
| **材质压缩** | `natural(building: aged-wood, weathered, rough) + synthetic(smoke: volume, scattered, dark) + natural(stone: rubble, irregular, fractured)` |

### 场景要求

| 维度 | 描述 |
|------|------|
| 内容 | 瀞灵廷传统木造建筑群破坏后废墟。保留部分传统建筑轮廓（瓦片屋顶残骸、木梁、纸窗碎片）以辨识为尸魂界 |
| 氛围 | 战后静寂 + 灭却师入侵痕迹 + 压倒性绝望感 |
| 色彩 | 淡白蓝天 #C0D0E0 + 灰建筑废墟 #808890 + 黑烟 #181818 + 零星橙红火光 #E06020 |
| 光源 | 漫射天光，无明确主光源。废墟投下深阴影。火光作为第二光源产生橙色调 |
| 破坏细节 | 残垣断壁不圆滑——边缘锐利断裂。烧焦痕迹。石板路面碎裂。木梁歪斜。纸窗破碎 |

### 视觉规则
- 线稿比角色线细 40%（前景废墟除外）
- 色彩饱和度比角色低一个层级（角色从场景中浮出）
- 天空留白 = 尸魂界标志性淡白蓝

---

## 4. SCN — Wahrwelt 冰之宫殿（P1）

| 字段 | 值 |
|------|----|
| **工作命名**（ref-images 阶段） | `T001_WahrweltIcePalace_ref_v01.png` |
| **规范命名**（晋升 assets/ 后） | `SCN_T001_bleach_Wahrwelt_scene-ice_v01.png` |
| **视角要求** | 低角度仰视 + 无限延伸地平线。冰平台从画面下缘突出，上部无限冷光天空 |
| **材质压缩** | `glass(ice: semi-translucent, frost, internal-glow) + metal(architecture: cold, brushed, matte) + synthetic(reiatsu-light: emissive, blue, particle)` |

### 场景要求

| 维度 | 描述 |
|------|------|
| 内容 | 无形帝国冰之宫殿（Wahrwelt）——悬浮冰平台群 + 无限延伸的冷光地平线 |
| 氛围 | 孤绝、极寒、压倒性的灭却师美学。空和冷是其核心感受 |
| 色彩 | 冰蓝 #80B8D0 + 纯白 #FFFFFF + 极淡灰 #E0E8F0 |
| 光源 | 冷荧光（灵子光）从建筑内部透出——环境光等于自发光。无自然光 |
| 建筑特征 | 冰结构尖锐有几何感——冰柱尖顶、冰桥连接不同平台。表面半透光，冰裂纹理可见 |

---

## 5. CHR — 露琪亚（P1，复用 DEMO 复检）

| 字段 | 值 |
|------|----|
| **现有路径** | `assets/characters/CHR_DEMO_Rukia_canonical_v01.png` |
| **动作** | IaD 复检 → 质量码 ⚠→✓ → 更新 `appears_in_topic: T001` + `appears_in_style: bleach` |
| **调整需求** | 无额外调整。六维兼容已确认 |

---

## 生产路线图

### 文件组织

```
ai-video/projects/T001/
├── assets/
│   ├── ref-images/        ← 工作素材：概念描述/草稿（当前阶段）
│   │   ├── T001_IchigoDualWield_ref_v01.png  （待 AI 生成，替换此文件）
│   │   ├── T001_Yhwach_ref_v01.png            （待 AI 生成）
│   │   └── T001_SoulSocietyBattlefield_ref_v01.png （待 AI 生成）
│   ├── last-frames/       ← 尾帧锚定缓存
│   ├── storyboards/       ← 分镜线稿（figure-draftsman 产出）
│   └── outputs/           ← Seedance 生成视频
└── ...
```

### 晋升条件（ref-images → assets/）

每张参考图须通过三项检查后方可晋升：

| 条件 | 检查项 |
|------|--------|
| 1. IaD 验证 | 中性表情。面部锚点通过 IaD 检查（非微笑/非愤怒/非悲伤） |
| 2. 分辨率 | 短边 ≥1024px，格式 .png |
| 3. 实用验证 | 经过至少 1 次 Seedance 生成验证，确认身份保持无漂移 |

晋升动作：
1. 重命名（草稿名 → `{Type}_{TopicID}_bleach_{EntityName}_{Variant}_v{N}.png`）
2. 移入 `assets/characters/` 或 `assets/scenes/`
3. 创建 `.asset-lab.lock` → 更新对应子索引 → 删除锁文件
4. 子索引更新：`appears_in_topic: T001` + `appears_in_style: bleach` + `status: active` + `quality: ✓`

---

> 资产规格版本：v01 | 维护者：visual-designer | 最后更新：2026-07-19
> 对应 visual-world.md v01 | 所有 P0 资产优先生产（Phase 0）
