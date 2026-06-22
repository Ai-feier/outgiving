# 分类法注册表 — 受控词汇表

> 所有资产分类标签（类型前缀 / 风格标签 / 状态码 / 变体名）的唯一权威来源。
> 新增标签前必须先在此注册，禁止未注册标签。
> 根清单见 `assets/asset-lab.md`，各子索引见 `assets/*-index.md`。

---

## 1. 资产类型前缀

### 已注册类型

| 前缀 | 类型名称 | 描述 | 资产目录 | 注册选题 | 状态 |
|------|---------|------|---------|---------|------|
| CHR | Character | 角色参考 / 表情模板 | `assets/characters/` | v1.0 | active |
| SCN | Scene | 环境空间参考 | `assets/scenes/` | v1.0 | active |
| STB | Storyboard | 分镜关键帧 | `assets/storyboards/` | v1.0 | active |
| PRP | Prop | 道具 / 物件 / 关键物品 | `assets/props/` | v1.1 | active |
| VFX | VisualEffect | 视觉特效 / 粒子 / 能量效果参考 | `assets/vfx/` | v1.1 | active |
| AUD | Audio | 音频素材（BGM / SFX / 旁白） | `assets/audio/` | v1.1 | active |
| LGT | Lighting | 灯光设定参考 / 光位图 | `assets/lighting/` | v1.1 | active |
| MAT | Material | 材质 / 纹理参考 | `assets/materials/` | v1.1 | active |
| CNC | ConceptArt | 概念艺术 / 情绪板 / 风格帧 | `assets/concepts/` | v1.1 | active |
| TPL | Template | 可复用模板（prompt / 构图 / 节奏） | `assets/templates/` | v1.2 | active |
| RIG | Rigging | 3D 绑定 / 动作骨架参考 | `assets/rigging/` | v1.2 | active |
| CLP | ColorPalette | 调色板 / 色指定参考 | `assets/palettes/` | v1.2 | active |
| TYP | Typography | 字体 / 文字排版参考 | `assets/typography/` | v1.2 | active |
| MNT | MattePainting | 数字绘景 / 背景合成参考 | `assets/matte-paintings/` | v1.2 | active |

### 保留区间

未占用但预留，防止与未来类型碰撞：

| 区间 | 用途 | 分配规则 |
|------|------|---------|
| RGA – RGZ | AI 自动生成资产（AI-tagged, not human-verified） | 仅用于 AI 自动分类的临时资产。human review 后转正为正式前缀 |
| XXA – XXZ | 第三方 / 外部来源资产（非本管线生产） | 仅引用外部素材时使用，不用于本管线资产 |
| ZZA – ZZZ | 扩展溢出（当 3 字母代码耗尽时启用） | 当前主表满 26x26 = 676 前缀后启用 |

### 新增注册流程

1. **提议**：任何 agent 发现当前前缀表无法覆盖的资产类型时，向 visual-designer 提议
2. **验证**：visual-designer 确认三条件——(a) 3 字母前缀未被占用；(b) 不与保留区间冲突；(c) 资产目录路径尚未被其他类型使用
3. **注册**：visual-designer 更新本表，分配前缀 + 资产目录
4. **广播**：visual-designer @ all four video agents
5. **创建**：建立对应资产目录 + 子索引文件（从已有子索引模板复制）

---

## 2. 风格标签

### 已注册风格

| 标签 | 显示名 | 风格文件 | 六维推导 | 类型亲和性 | 注册选题 |
|------|-------|---------|---------|-----------|---------|
| bleach | Bleach | `styles/bleach.md` | `japanese-anime.md` | CHR, SCN, STB, PRP, VFX | v1.0 |
| jp-anime | Japanese Anime (General) | `styles/japanese-anime.md` | 自身 | CHR, SCN, STB | v1.0 |
| kyoani | Kyoto Animation | `styles/kyoto-animation.md` | `japanese-anime.md` | CHR, SCN, LGT, MAT | v1.0 |
| generic | Style-Agnostic | — | — | PRP, MAT, AUD, TPL | v1.1 |
| cyberpunk | Cyberpunk | `styles/cyberpunk.md` | 待定义 | CHR, SCN, MAT, LGT, VFX | v1.2 |
| wuxia | Wuxia/Ancient Chinese | `styles/wuxia.md` | 待定义 | CHR, SCN, MAT, PRP | v1.2 |
| realistic | Live-Action Realism | `styles/realistic.md` | 待定义 | CHR, SCN, MAT, LGT | v1.2 |
| sci-fi | Science Fiction | `styles/sci-fi.md` | 待定义 | CHR, SCN, LGT, MAT, VFX | v1.2 |

### 风格标签规则

1. **单资产可多风格**：一个资产可出现在多个风格中（如通用道具）。`appears_in_style` 字段记录。
2. **`generic` 保留**：用于风格中性资产（道具模板、材质参考、音频样本等），不带视觉风格特征。
3. **风格文件绑定**：每个非 `generic` 风格必须有对应的风格文件（`.claude/skills/video-craft/references/styles/{tag}.md`），定义其六维推导。
4. **标签格式**：小写字母 + 连字符，最长 20 字符。禁止空格、特殊字符。

### 新增注册流程

1. **发起**：用户或 visual-designer 新建风格文件时
2. **必要条件**：风格标签 + 显示名 + 风格文件路径 + 至少一种类型亲和性
3. **审批**：visual-designer（生产者）+ video-director（消费者）两方确认——验证风格文件完整性（含六维推导）
4. **注册**：visual-designer 更新本表
5. **广播**：@ 所有 video agent + gather-expert（风格研究依赖）
6. **风格文件**：写入 `.claude/skills/video-craft/references/styles/{tag}.md`

### 移除/弃用

- 风格标签无 active 资产引用 + 无 active 选题使用 → 标记 `deprecated`
- 标记 `deprecated` 超 180 天 → 可移除
- 移除前广播所有 agent

---

## 3. 状态码

受控，新增前必须注册：

| 码 | 含义 | 消费者行为 |
|----|------|-----------|
| `draft` | 刚产出，待 IaD/质量检查 | 不可消费，生产者唯一访问 |
| `active` | 质量检查通过，可正产消费 | 正常引用 |
| `deprecated` | 有更新版本取代 | 可临时使用（标注风险），通知生产者更新 |
| `archived` | 已归档（无 active 选题引用） | 视为不存在，需重产 |

---

## 4. 质量码

受控：

| 码 | 含义 | 消费者行为 |
|----|------|-----------|
| `✓` | 通过 IaD 验证 + 分辨率合规 + 风格一致 | 正常引用 |
| `⚠` | 待复检（超 60 天未验证 / IaD 有疑点 / 首次入库未实测） | 可用，P0 记录风险 |
| `✗` | 验证失败 | 不可用，通知 visual-designer 重产 |

---

## 5. 变体名规范

`Variant` 字段的受控命名。新增前必须在此注册。

| 变体名 | 适用类型 | 含义 |
|--------|---------|------|
| `canonical` | CHR, SCN | 规范参考（首次清晰出现用，中性表情 + ≤1 帧组合图） |
| `multi-view` | CHR | 多视角身份分布（正面 + 半侧 + 全身分别入 Seedance 50 槽） |
| `outfit-{name}` | CHR | 特定妆造 / 服装变体 |
| `scene-{name}` | SCN | 场景条件变体（如 scene-dusk, scene-rain） |
| `beat-{N}` | STB | 对应拍号关键帧 |
| `concept` | CNC, STB | 早期概念探索 |
| `moodboard` | CNC | 情绪板 / 视觉参考板 |
| `expression-{name}` | CHR | 特定表情变体（非规范参考用） |
| `setup` | LGT, MAT | 技术设定参考（灯光布置 / 材质节点） |
| `loop` | VFX, AUD | 循环素材 |

---

## 6. 治理机制

### 6.1 负责人

| 角色 | 持有者 | 职责 |
|------|-------|------|
| 分类法拥有者 | visual-designer | 批准新类型/风格/变体；季度审计；仲裁命名冲突 |
| 消费者审计 | video-director | 验证资产分类与实际生成结果一致；反馈误分类 |
| 用户覆写 | 人类用户 | 当分类法造成生产力障碍时，用户可直接指定，更新 registry |

### 6.2 季度审计清单

每季度由 visual-designer 执行：

- [ ] 检查 `deprecated` 资产：还有 active 选题在引用？→ 通知升级。无引用 → 标记 `archived`
- [ ] 检查 `archived` 超 90 天资产：可删除源文件（子索引保留行）
- [ ] 检查风格标签：任一标签无任何风格文件依赖？→ 标 `deprecated`
- [ ] 检查类型前缀：任一前缀无任何 active 资产？→ 标 `unused`
- [ ] 检查变体名：是否有概念重复的变体名？→ 合并
- [ ] 检查 `appears_in_style`：是否有资产标记了不存在的风格标签？→ 修正
- [ ] 更新本文件顶部日期

### 6.3 冲突解决

| 冲突场景 | 决断者 | 规则 |
|---------|--------|------|
| 提议前缀与保留区间冲突 | visual-designer | 保留区间优先，提议者换前缀 |
| 同一实体两个不同风格标签名 | video-director | 按风格文件完整性 + 已有资产数量裁决 |
| 变体名重复 | visual-designer | 先注册者保留，新提议用描述性后缀 |
| 标签 vs 用户直觉冲突 | 用户 | 用户覆写，更新 registry |

---

> 最后更新：2026-07-18 | 由视觉资产沉淀体系的第 16 轮 reflecting 建立。
> 来源：DAM 分类法设计最佳实践（Frontify/Bynder/Orange Logic/DAM News）、
> MovieLabs OMC 资产本体论、
> 设计模式（Correia & Aguiar — Controlled Vocabulary Pattern）、
> 游戏管线资产复用策略（Walla Walla Studio / Perforce / Unreal Engine）。
