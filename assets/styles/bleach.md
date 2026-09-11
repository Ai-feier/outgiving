# Bleach / Tite Kubo Style

> 久保带人。不是"少年漫"，是黑白之间的视觉哲学。

## 核心美学

**剪影先于面部。** 角色不需要看到脸——看到轮廓就知道是谁。久保的角色设计建立在极致的剪影辨识度上：发型轮廓、服装廓形、站姿角度、武器形状。每一帧都可以被识别为黑白剪影。

**黑与白之间有一千种灰。** 不是"暗黑风"。是黑与白之间的张力——死神黑、虚白、破面骨白、斩魄刀的银、和服的图案黑。颜色不在调色盘里——在"哪个角色属于哪个灰度"的体系里。

**静态是蓄力，动态是释放。** 战斗节奏：长静止 → 瞬间爆发 → 静止。静止帧不是偷懒——是让观众消化"刚才发生了什么"以及"接下来会怎样"的蓄力空间。每一刀之间有空隙，每一段台词之间有留白。

**时尚感是世界观的一部分。** 角色不是"穿衣服"——是在穿自己的态度。死霸装的褶皱位置、破面的服装残缺感、现世的便服——服装设计不服务于"好看"，服务于"这个角色选择以什么形象存在"。

## 视觉语言

### 角色

- 体型：修长、瘦削。男性宽肩窄腰、女性高挑。不追求肌肉量，追求线条
- 面部：锐利的下颌线、细长的眼睛、棱角分明的鼻梁。表情克制——嘴角和眉梢的微小变化比夸张表情更有信息量
- 头发：发型 = 身份标识。刺状不规则发束、发色对比强烈。头发几乎不受重力——它是角色气场的延伸
- 姿势：站立时重心偏移（一只手插兜/靠墙/刀斜倚），不是标准站姿。姿势本身是态度

### 色指定

- 基调：中低明度、中低饱和。黑色至少 10% 面积
- 高对比：亮部偏冷白、暗部深蓝黑
- 强调色：仅用于灵力/虚闪/斩魄刀解放——橙色（月牙天冲）、紫色（虚闪）、金色（灵力）。强调色是高饱和的，和低饱和基调形成对比
- 角色灰度体系：死神（黑+白+银）→ 破面（骨白+灰）→ 灭却师（纯白+蓝）→ 虚（白+黑面具）
- 禁止：明亮暖色调大面积使用、粉色/糖果色

### 线稿

- 线条锐利、肯定、有速度感。长直线（衣纹、刀痕）和短断线（头发束、阴影线）交替
- 外轮廓强调——角色和背景之间有清晰的黑白分界
- 战斗场景：线条变粗、变快、有笔触飞白感
- 静止场景：线条收细、更干净

### 背景

- 现代日本都市 + 超自然侵入：高中校园、河边空地、仓库街、夜空——日常场景被超自然元素"撕开"
- 尸魂界：江户/明治传统建筑 + 零番队超现实悬浮结构
- 虚圈：白色沙漠 + 无限地平线 + 孤立的建筑——不是"黑暗"，是"空"
- 背景服务于前景角色——角色始终是画面的绝对焦点，背景退后为情绪基调

### 摄影处理

- 高对比度：暗部压黑、亮部不让步，中间调偏少
- 动态模糊 + 速度线：用于战斗瞬移/斩击——不是连续运动，是"消失→出现"的断续节奏
- 负片空间：画面大量留黑/留白，角色在画面边缘或中心极小——用空表达孤独和力量差
- 禁止：柔焦、过渡曝光、暖调滤镜

## 时间与战斗节奏

**三段式战斗呼吸。** 对峙（静态宽景）→ 交锋（瞬移 + 一招定胜负，0.5-2s）→ 余波（烟雾/碎衣/台词，3-8s）。三段之间的过渡是硬切，不用溶解。

**一招的重量。** 不是连续打斗——是一刀一刀之间的呼吸。斩击之前有蓄力（刀背的反光、衣袖的飘动、眼神锁定的特写），斩击之后有时间给观众和角色一起消化后果。

**台词是战斗的一部分。** 不是"边打边说"——是"打完一段，说一句话"。每句话之后都有沉默。沉默的长度和上一句话的重量成正比。

## AI Prompt 约束

```yaml
style: bleach-kubo
line_art: sharp_angular_lines, strong_outer_silhouette, speed_varying_line_weight
shading: high_contrast, hard_cel_with_deep_shadows, cool_highlight_warm_none
color: low_key, desaturated, 10%_black_minimum, high_saturation_only_for_power_effects
lighting: stark_directional, deep_shadows, rim_light_on_character_edges
camera: wide_static_during_standoff, snap_zoom_during_strike, negative_space_composition
motion: stillness_then_instant_burst, hard_cut_transitions, speed_lines_not_motion_blur
character: tall_slender, sharp_jawline, hairstyle_as_identity_silhouette, angular_features
costume: black_dominant_with_faction_accent, draped_fabric_with_sharp_folds
background: modern_urban_with_supernatural_intrusion, high_contrast_sky, minimal_midtones
prohibited: warm_glow_filters, soft_focus, pink_candy_colors, continuous_fight_choreography, dissolve_transitions
```

## 参考视觉锚点

- 死神代理篇 — 现代都市 + 灵的透明感
- 尸魂界篇 — 传统建筑 + 天空留白 + 宽景对峙
- 虚圈篇 — 白色沙漠 + 骨白色调 + 孤绝感
- 千年血战篇 — 色彩回归 + 灭却师纯白 + 更锐利的线稿
- 斩魄刀解放 — 强调色爆发的范本（橙/紫/金/蓝在低饱和世界中的冲击力）
