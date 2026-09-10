# 场景定调图索引

> 资产根清单见 `assets/asset-lab.md`。
> 受控词汇表（类型前缀/风格标签/状态码/变体名）见 `assets/taxonomy-registry.md`。
> 风格文件参考：`assets/styles/`

## 查询提示

```sh
# 查 bleach 风格 active 场景
grep 'bleach' assets/scenes-index.md | grep 'active'

# 查跨选题场景复用
grep 'appears_in_topic.*\[T' assets/scenes-index.md
```

## 记录格式

| 名称 | 风格 | 版本 | 状态 | 质量 | 最后验证 | 路径 | `replaced_by` | `derived_from` | `appears_in_topic` | `appears_in_style` |
| ---- | ---- | ---- | ---- | ---- | -------- | ---- | ------------- | -------------- | ------------------ | ------------------ |
| Karakura-Rooftop | bleach | v01 | active | ⚠ | 2026-07-18 | `scenes/SCN_DEMO_KarakuraRooftop_scene-dusk_v01.png` | — | — | DEMO | bleach |
| SoulSociety-Streets | bleach | v01 | active | ⚠ | 2026-07-18 | `scenes/SCN_DEMO_SoulSocietyStreets_scene-day_v01.png` | — | — | DEMO | bleach |

> `⚠` = 待 AI 生成验证

## 命名规范

文件名格式：`{Type}_{TopicID}[_{StyleTag}]_{EntityName}_{Variant}_v{NN}.png`

| 段 | 规则 | 示例 |
| ---- | ------ | ------ |
| Type | `SCN` | `SCN` |
| TopicID | 来源选题 | `T002` |
| StyleTag | **可选**。仅单一风格专属时加入 | `bleach` / 省略 |
| EntityName | PascalCase，场景描述 | `RainStreet` / `CafeInterior` |
| Variant | `scene-{条件}` | `scene-night` / `scene-rain` / `scene-dusk` |
| Version | v两位数字 | `v01` |

## 场景规格

### 空座町天台 (Karakura Rooftop) — 黄昏

**风格**：Bleach 现代日本都市 + 超自然侵入（bleach.md 背景）

- 高中校园天台，黄昏天空占画面 60%+
- 色彩：暖橙暮光 + 冷蓝天光渐层——Bleach 高对比天空中少量中调
- 光源：低角度夕阳光（暖偏橙），角色边缘 rim light 冷白
- 材质：混凝土围栏（粗糙亚光）、铁丝网（氧化金属）、地面（灰色水泥）
- 超自然侵入提示：天空边缘可留一缕不自然的黑雾
- 构图：广角俯视——天台地面占下部 1/3，天空占上部 2/3。角色位置偏左 1/3 留白

### 尸魂界流魂街 (Soul Society Streets) — 白天

**风格**：Bleach 尸魂界 = 江户/明治传统建筑（bleach.md 背景）

- 传统木造建筑街道，石板路面
- 色彩：低饱和木色 + 灰白墙面。天空留白（尸魂界天空永远是淡白蓝色）
- 光源：漫射自然光——无明确主光源，全局柔光
- 材质：老木（风化粗面）、石板（不规则磨损）、纸窗（半透光散射）
- 构图：纵深街道视角——两侧建筑形成引导线，远处街角留白。角色在画面中下位置偏小（负片空间表达孤绝感）
