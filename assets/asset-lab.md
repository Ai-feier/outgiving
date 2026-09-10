# 视觉资产实验室（Asset Lab）— 根清单（Root Manifest）

> 角色、场景、分镜参考图的**索引路由 + 生命周期策略**。
> 资产记录分布在类型级子索引中，本文件仅维护路由信息和全局规则。
> **受控词汇表（类型前缀/风格标签/状态码/变体名）统一注册在 `taxonomy-registry.md`，是本文件的上位规范。**

## 索引路由

| 资产类型   | 类型前缀 | 媒体目录                    | 子索引文件                          | 前次查询 |
| ---------- | -------- | --------------------------- | ----------------------------------- | -------- |
| 角色参考图 | CHR      | `assets/characters/`      | `assets/characters-index.md`      | active   |
| 场景定调图 | SCN      | `assets/scenes/`          | `assets/scenes-index.md`          | active   |
| 分镜关键帧 | STB      | `assets/storyboards/`     | `assets/storyboards-index.md`     | active   |
| 道具物件   | PRP      | `assets/props/`           | `assets/props-index.md`           | active   |
| 视觉特效   | VFX      | `assets/vfx/`             | `assets/vfx-index.md`             | active   |
| 音频素材   | AUD      | `assets/audio/`           | `assets/audio-index.md`           | active   |
| 灯光设定   | LGT      | `assets/lighting/`        | `assets/lighting-index.md`        | active   |
| 材质纹理   | MAT      | `assets/materials/`       | `assets/materials-index.md`       | active   |
| 概念艺术   | CNC      | `assets/concepts/`        | `assets/concepts-index.md`        | active   |
| 模板预设   | TPL      | `assets/templates/`       | `assets/templates-index.md`       | active   |
| 绑定骨架   | RIG      | `assets/rigging/`         | `assets/rigging-index.md`         | active   |
| 调色板     | CLP      | `assets/palettes/`        | `assets/palettes-index.md`        | active   |
| 字体排版   | TYP      | `assets/typography/`      | `assets/typography-index.md`      | active   |
| 数字绘景   | MNT      | `assets/matte-paintings/` | `assets/matte-paintings-index.md` | active   |

**扩展路径**：新增类型 → 在 `taxonomy-registry.md` 注册前缀 → 创建目录 + 子索引（从已有子索引模板复制） → 更新本表。**禁止凭空创建目录后不注册前缀。**

**查询原则**：agent 只读取相关类型的子索引，不扫描全表。例如 narrative-architect 查角色规范参考 → 读 `characters-index.md`。video-director 收参考素材 → 读所有子索引。

## 命名规范

所有资产文件名必须遵循以下模式（拒绝"小林-v1"式随意命名）：

```
{Type}_{TopicID}[_{StyleTag}]_{EntityName}_{Variant}_v{NN}.png
```

其中 `{_StyleTag}` 为**可选段**——仅当资产为单一风格专属时加入，便于快速视觉过滤。通用资产省略。

| 段         | 规则                                                                    | 示例值                                                            |
| ---------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Type       | 大写三字母，`assets/taxonomy-registry.md` 注册                        | `CHR`(角色) / `SCN`(场景) / `VFX`(特效)                     |
| TopicID    | 来源选题编号                                                            | `T002`                                                          |
| StyleTag   | **可选**。小写 kebab-case，受控于 `taxonomy-registry.md` 风格表 | `bleach` / `cyberpunk`                                        |
| EntityName | PascalCase，无空格无缩写                                                | `LinBei`                                                        |
| Variant    | 小写 kebab-case，受控于`taxonomy-registry.md` 变体表                  | `canonical` / `multi-view` / `outfit-{名}` / `scene-{名}` |
| Version    | v + 两位数字                                                            | `v01`                                                           |

完整示例：

- 风格专属：`CHR_T002_bleach_LinBei_canonical_v01.png`
- 风格中立（无风格段）：`MAT_T002_SteelPlate_brushed_v01.png`

禁止：空格、中文、特殊字符、`-改`/`-终`/`-新` 等模糊后缀。
来源：Kokku Games AAA 管线命名规范 + Jack Henry Design Tokens 层级结构。

## 全局生命周期管理

```
draft（visual-draftsman 产出）
  → IaD 检查 → 按命名规范入库对应子目录 → 更新对应子索引（状态=active，记录 appears_in_topic + appears_in_style）
  → 外观变更 → 新版本入库（revision/variant 类型标注），旧版标记 deprecated
  → 选题结束 → 如 appears_in_topic 中无 active 选题引用 → 标记 archived
  → archived 超过 90 天 → 源文件可删除，子索引保留行供溯源码
```

**版本类型定义**（源自 MovieLabs OMC 分类）：

| 版本类型   | 含义                   | 何时使用                     | 影响                                    |
| ---------- | ---------------------- | ---------------------------- | --------------------------------------- |
| Revision   | 同上下文的小修改       | 修bug、色彩微调、构图小改    | 版本号递增（v01→v02），旧版 deprecated |
| Variant    | 不同上下文的变体       | 新妆造、新季节场景、不同视角 | 独立条目，通过`derived_from` 链接原版 |
| Derivation | 基于原资产创作的新资产 | 从角色参考图衍生出场景分镜   | 新条目标注`derived_from` 原路径       |

## Agent 读写协调

**问题**：visual-draftsman 写入子索引时，video-director/narrative-architect 可能同时读取，读到半更新状态。

**协议**（低开销，无需分布式锁）：

1. **写锁**：visual-draftsman 在开始更新子索引前，于同一目录创建 `.asset-lab.lock`，内容为 `visual-draftsman|PID|YYYY-MM-DD HH:MM:SS`
2. **原子写入**：写临时文件 → `mv` 覆盖（`asset-lab.md.tmp` → `asset-lab.md`）
3. **清锁**：写入完成后删除 `.asset-lab.lock`
4. **读检测**：读取 agent 检测锁文件存在 → 等 1s 重试，最多 3 次 → 超时报"索引被锁定"，不读脏数据

## 全局上架规则

1. **IaD 门禁**：角色参考图入库前须经中性表情检查。不合规 → 退回 visual-draftsman 重产。
2. **查重前置**：新选题生产前先查对应子索引。同角色已存在且六维+风格兼容 → 直接引用路径 + 更新该资产的 `appears_in_topic` + `appears_in_style` 字段。
3. **风格一致性复核**：跨风格复用资产时（如 Bleach 的角色用于赛博朋克变体），visual-draftsman 必须确认六维推导在该风格下仍成立。不成立 → 需新资产，不复用。
4. **版本关系**：外观变更 → 判断是 Revision（递增版本号）还是 Variant（新建条目 + `derived_from` 链接）。旧版标记 `deprecated`，保留 30 天后可归档。
5. **跨引用保护**：标记 archived 前检查 `appears_in_topic` 列表——如有 active 选题仍引用，不允许归档。
6. **视角要求**：每角色≥1帧组合图（正面+半侧+全身，KeyFrame-Compass ≤1帧约束）。
7. **格式与分辨率**：`.png`，短边 ≥1024px。多视角分布图（分别入 Seedance 50 槽）用于动态身份锚定。
8. **质量复检**：每次复用前检查 IaD 合规状态，超过 60 天未验证的资产标 `⚠` 提醒复检。

## 跨维度查询模式

子索引为 markdown 表格，不支持 SQL。在 < 500 条目规模下，使用 grep 流水线实现多维度过滤：

```
# 例 1：查 bleach 风格下所有 active 角色资产
grep 'bleach' assets/characters-index.md | grep 'active'

# 例 2：查 T002 在各类型中的 P0 资产（across types）
grep 'T002' assets/characters-index.md assets/scenes-index.md

# 例 3：查 deprecated 但仍有 active 选题引用的资产
grep 'deprecated' assets/*-index.md | grep -E 'appears_in_topic.*\[T'

# 例 4：按类型 + 质量交叉查询
grep -E 'active.*✓' assets/characters-index.md
```

> 当资产条目 > 500 或跨类型查询频率超过 10 次/选题时 → 迁移至 `_scripts/asset-query.py`（JSON 索引 + 结构化查询）。

## 消费路径

```
visual-draftsman 产角色/场景图 → 按命名规范入库 → 更新对应子索引
narrative-architect 查询 characters-index.md 确认规范参考 → visual-draftsman 协调分镜线稿（入库 assets/storyboards/ + 更新 storyboards-index.md）
video-director 查所有子索引收集参考素材 → 编入 9 要素 prompt
选题结束后 → 协作者审计各子索引 + taxonomy-registry.md，清理 archived 超 90 天资产
```

## 索引状态

- **注册表**：`assets/taxonomy-registry.md` — 14 类型前缀 / 8 风格标签 / 3 状态码 / 3 质量码 / 10 变体名
- **角色索引**：`assets/characters-index.md` — 2 角色 4 条目（Ichigo / Rukia，DEMO 打样，待 AI 生成验证）
- **场景索引**：`assets/scenes-index.md` — 2 场景（Karakura-Rooftop / SoulSociety-Streets，DEMO 打样）
- **分镜索引**：`assets/storyboards-index.md` — 空
- **活跃索引**（3/14）：characters / scenes / storyboards — 有 DEMO 打样数据
- **待激活索引**（11/14）：props / vfx / audio / lighting / materials / concepts / templates / rigging / palettes / typography / matte-paintings — 模板就绪，首次生产时激活
- **当前活跃风格**：Bleach（`styles/bleach.md`）
- **上次全库审计**：2026-07-18
