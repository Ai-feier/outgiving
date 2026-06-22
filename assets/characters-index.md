# 角色参考图索引

> 资产根清单见 `assets/asset-lab.md`。字段说明和生命周期规则遵循根清单定义。
> 受控词汇表（类型前缀/风格标签/状态码/变体名）见 `assets/taxonomy-registry.md`。
> 风格文件参考：`.claude/skills/video-craft/references/styles/`

## 查询提示

常用过滤命令：
```
# 查 bleach 风格 active 角色
grep 'bleach' assets/characters-index.md | grep 'active'

# 查跨选题角色复用
grep 'appears_in_topic.*\[T00[2-4]' assets/characters-index.md
```

## 记录格式

版本间关系通过 `derived_from` 维护。`appears_in_topic` 记录跨选题引用，`appears_in_style` 记录跨风格引用。

| 名称 | 风格 | 版本 | 状态 | 质量 | 最后验证 | 路径 | `replaced_by` | `derived_from` | `appears_in_topic` | `appears_in_style` |
| ---- | ---- | ---- | ---- | ---- | -------- | ---- | ------------- | -------------- | ------------------ | ------------------ |
| Ichigo | bleach | v01 | active | ⚠ | 2026-07-18 | `characters/CHR_DEMO_Ichigo_canonical_v01.png` | — | — | DEMO | bleach |
| Ichigo | bleach | v01 | active | ⚠ | 2026-07-18 | `characters/CHR_DEMO_Ichigo_multi-view_v01/` | — | canonical | DEMO | bleach |
| Rukia | bleach | v01 | active | ⚠ | 2026-07-18 | `characters/CHR_DEMO_Rukia_canonical_v01.png` | — | — | DEMO | bleach |
| Rukia | bleach | v01 | active | ⚠ | 2026-07-18 | `characters/CHR_DEMO_Rukia_multi-view_v01/` | — | canonical | DEMO | bleach |

> **质量标记**：`⚠` = 待 IaD 中性表情实测验证（首次入库，规格已定义但尚未经过 AI 生成验证）。通过后升级为 `✓`。

---

## 角色规格（供 visual-designer 生产参考图）

### 黒崎一護 (Kurosaki Ichigo) — 死神代理

**风格**：Bleach / 久保带人

**外观特征**（来自 bleach.md 视觉语言）：
- 体型：修长瘦削，宽肩窄腰。不追求肌肉量，追求线条
- 面部：锐利下颌线，细长眼睛，棱角分明鼻梁。表情克制——嘴角和眉梢 1-2px 偏移即有信息量
- 头发：橙色刺状不规则发束，不受重力——发型=气场延伸+剪影辨识度核心
- 服装：黑色死霸装，褶皱锐利分明。腰间斩魄刀 Zangetsu——刀柄卍字纹样是剪影标识
- 姿势：重心偏移——单手插兜或刀斜倚，非标准站姿。姿势本身是态度

**色指定**（bleach.md 色指定）：
- 基调：中低明度、中低饱和。黑色 ≥10% 面积
- 亮部偏冷白，暗部深蓝黑
- 强调色：橙色 #E8760B（月牙天冲 Getsuga Tenshō）——仅用于灵力/斩魄刀解放

**线稿**：锐利肯定有速度感，外轮廓强调。静止场景线条收细

**IaD 要求**（规范参考图 — 中性表情）：
- 面部：中性表情，嘴角微微下抿（一護默认冷酷表情），眼神平视前方
- 身体：直立，双臂自然下垂或单手握刀柄（非战斗姿态）
- 三通道：面部承载身份（中性）、身体承载情绪（克制的待命感）、3D偏移场承载可编辑表情

---

### 朽木ルキア (Kuchiki Rukia) — 十三番隊副隊長

**风格**：Bleach / 久保带人

**外观特征**：
- 体型：女性高挑纤细，线条优美不追求曲线量感
- 面部：锐利下颌线，眼睛较一護略圆但保持 Bleach 棱角感
- 头发：黑色短发，前额刘海整齐，发梢微翘不受重力。头顶蟋蟀发饰 = 剪影标识
- 服装：黑色死霸装女性剪裁，袖口领口褶皱锐利。腰间斩魄刀 Sode no Shirayuki——白色缎带 = 剪影标识
- 姿势：站姿端正（贵族出身），重心稳定。和一護的斜倚形成对比——姿势即性格

**色指定**：
- 基调：中低明度中低饱和
- 亮部偏冷白，暗部深蓝黑
- 强调色：白色 + 淡蓝 #B8D4E8（袖白雪冰系解放）

**线稿**：锐利肯定。静止场景线条收细。外轮廓强调

**IaD 要求**（规范参考图 — 中性表情）：
- 面部：中性表情，眼神平视略微上扬（贵族自信底色），嘴唇自然闭合
- 身体：直立，站姿端正，双臂自然下垂
- 三通道独立：面部=身份，身体=情绪，3D偏移场=可编辑表情
