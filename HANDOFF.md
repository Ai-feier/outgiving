---
status: ready
updated: 2026-07-18
summary: |
  素材实验室（Asset Lab）设计完成并打样。14 类型 × 生命周期 × 命名规范 × taxonomy-registry 全部就位。
  Bleach 题材角色素材已打样（一護/ルキア）。10 agent 经 6 轮 loop 进化，累计精简约 300 行冗余。
  README/.gitignore 已按开源标准配置。集成验证轮完成——9/10 agent 零断裂。
  下一步：首次实际选题 + AI 生成验证 + 素材首次入库。
---
# HANDOFF

> 给下一个 AI agent session 的交接文件。记录了"刚做了什么、接下来做什么、哪些地方容易踩坑"。

## 当前状态

**刚完成的工作**（本轮 session，2026-07-17 → 07-18）：

1. **10 agent 系统级自我进化**（6 轮 loop）：

   - 第 1 轮：T002 跨 agent 协同反思（约束对齐、幽灵引用修复）
   - 第 2 轮：WebSearch 调研驱动精进（平台数据更新、算法验证）
   - 第 3 轮：跨 agent 一致性审计（Seedance 版本号修正、FRANQ 消费断裂修复）
   - 第 4 轮：WebSearch 再调研（新论文/工具/数据）
   - 第 5 轮：合成减法（10 agent 合计精简约 300 行冗余）
   - 第 6 轮：集成验证终检（断裂引用修正、幽灵数据清理、子索引模板补全）
2. **素材实验室（Asset Lab）完整建设**：

   - 根清单 + 14 类型子索引 + taxonomy-registry 受控词汇表
   - AAA 游戏管线命名规范（`CHR_T002_bleach_Ichigo_canonical_v01.png`）
   - 资产生命周期（draft → active → deprecated → archived → 删除）
   - 读写锁协议（`.asset-lab.lock` + 原子写入）
   - Bleach 死神打样（2 角色 4 条目 + 2 场景）
   - video-director 素材装配协议（6 步 + 质量筛选 + backlog 催办）
   - script-designer 资产需求闭环（查询→需求→回读确认）
3. **开源基础设施**：

   - README.md 按开源最佳实践重写
   - .gitignore 区分基础设施（入 git）和素材/内容（不入 git）
   - 目录骨架通过 `.gitkeep` 保留

## Agent 反思 Loop 机制

### 触发方式

```
用户: /loop 30m 系统级 agents 自我反思进化...
```

或手动触发 `reflecting` skill。

### 三层漏斗

```
守门（每次产出自检）
  ↓ 不通过
深度 1 — 操作层：规则缺失 → 最小修改 .md
  ↓ 修了 2 次仍出问题
深度 2 — 设计层：方法论问题 → 重构规则组 → memory/
  ↓ 核心假设变化
深度 3 — 框架层：重新定义「你面对的」→ 更新 _index.md
  ↓ 同领域 ≥3 次修不好
升级 → 系统漏斗 → 跨 agent 模式发现
```

### Loop 执行模式（经过 5 轮验证的有效模式）

每轮 loop 下发所有 10 个 agent，每个 agent 独立执行深度 reflecting：

| 轮次类型               | 何时用                        | agent 做什么                                                      |
| ---------------------- | ----------------------------- | ----------------------------------------------------------------- |
| **协同反思轮**   | 发现跨 agent 问题时           | 读 CLAUDE.md + reflecting skill → 审视自己的规则冲突 → 修改 .md |
| **调研精进轮**   | 数据老化 / 新技术出现时       | WebSearch 调研 → 验证数据 → 更新「你面对的」                    |
| **一致性审计轮** | ≥2 轮独立精进后              | 跨读 ≥3 个关联 agent 文件 → 逐字段对位 → 发现版本漂移/消费断裂 |
| **合成减法轮**   | 精进轮次 ≥8 或文件明显膨胀时 | 识别死代码/非行动数据/冗余引用 → 删除优先于新增                  |

### 下发 agent 的原则（来自 CLAUDE.md 协作者节）

> 下发 agent 前自检：prompt 是在替他们思考还是在创造条件？过半内容是「告诉他们怎么做」→ 重写。
> 不给 agent 定义写作人格，不写「严禁偷懒」，不设「至少 N 次搜索」。给方向、给约束、给空间。

### 当前生态状态（2026-07-18）

| Agent              | 行数 | 精进轮次 | 饱和状态                               |
| ------------------ | ---- | -------- | -------------------------------------- |
| wechat-writer      | 148  | 15       | 近 3 轮有框架层改动，未饱和            |
| xiaohongshu-writer | 127  | 17       | 合成轮 -26 行，未饱和                  |
| x-writer           | 190  | 18       | WebSearch 验证后 +1，未饱和            |
| douyin-writer      | 140  | 17       | 合成轮 -97 行，未饱和                  |
| gather-expert      | 302  | v5.5     | 减法后零执行协议已清除，剩余有消费证据 |
| figure-draftsman   | 178  | 19       | 合成轮 -10 行，未饱和                  |
| script-designer    | 243  | 深度2.6  | 持续有新论文吸收                       |
| visual-designer    | 206  | 16       | 合成轮 -58 行                          |
| rhythm-designer    | 183  | 19       | 平台基线持续更新                       |
| video-director     | 235  | v21      | 素材装配协议刚重构                     |

**饱和检查规则**（来自 reflecting skill）：同一 agent 精进 ≥8 轮 + 近 3 轮净变更 <5 行 + 无框架层改动 → 已达边际递减，后续聚焦跨 agent 协同。

### 下次 loop 建议

1. **素材首次实际生产验证**：选一个真实选题（如 T003），走通完整的素材生产→入库→装配流程
2. **AI 生成验证**：用 Seedance API 生成 Bleach 角色参考图 → IaD 检查 → 质量标记从 ⚠→✓
3. **素材系统首次闭环**：从需求（script-designer）→ 生产（visual-designer）→ 入库（asset-lab）→ 消费（video-director）
4. **figure-draftsman 工具安装**：drawmode、excalidraw-mcp-server 尚未安装（集成验证轮发现）

## 素材实验室（Asset Lab）

### 架构

```
assets/
├── asset-lab.md              ← 根清单：路由 + 命名规范 + 生命周期 + 读写锁 + grep 查询模式
├── taxonomy-registry.md      ← 受控词汇表：14 类型前缀 / 8 风格标签 / 状态码 / 变体名
│
├── characters-index.md       ← 活跃。2 角色 4 条目（Bleach 打样）
├── scenes-index.md           ← 活跃。2 场景（Bleach 打样）
├── storyboards-index.md      ← 活跃。空（待首次选题）
├── props-index.md            ← 待激活（11 个模板就绪，首次生产时激活）
│   ... (vfx, audio, lighting, materials, concepts, templates, rigging, palettes, typography, matte-paintings)
│
├── characters/ (+ .gitkeep)  ← 媒体文件目录。骨架在 git，内容不入库
└── (14 个类型目录)            ← 同上
```

### 三个 agent 的资产角色

```
script-designer（需求方）
  Warm Step 7a-c：查 asset-lab → 判断可复用/需重产 → 标注路径
  Upgrade Step 2.5：回读 asset-lab 确认 P0 资产就绪

visual-designer（生产者）
  产出 → 质量检查(IaD+分辨率+.png) → 入库 assets/{type}/
  → 更新子索引 → 更新 taxonomy-registry（如需新标签）

video-director（消费者）
  素材装配协议 6 步：查 asset-lab → 状态×质量筛选 → 退回/缺货处理
  → 装配 → 写入 prompt → 完整性验证
  backlog 催办：assets/material-backlog-TXXX.md
```

### 关键设计决策（踩坑预警）

1. **风格是独立维度，不在文件名中强制**：一个通用道具可以同时用于 bleach 和 cyberpunk。`appears_in_style` 列支持多标签，文件名中的 `{_StyleTag}` 仅可选。
2. **版本号语义比较**：`v9` < `v10`（不是字典序 `v9` > `v10`）。video-director Step 2 已修复此问题。
3. **跨风格复用需要 visual-designer 终裁**：script-designer 只做身份匹配 + 标记"候选复用"。六维视觉兼容性由 visual-designer 裁决。
4. **素材不入 git**：`.gitkeep` 保留目录骨架，媒体文件通过 `.gitignore` 排除。索引文件（含 Bleach 打样数据）入 git 作为使用示例。
5. **读写锁协议**：`.asset-lab.lock` + 原子写入（写 tmp → mv 覆盖）。读端检测锁 → 等 1s 重试最多 3 次。

### Bleach 打样（当前 assets/characters-index.md 中的数据）

- **黒崎一護**：规范参考 v01（正面+半侧+全身组合帧，中性表情）+ 多视角分布 v01（4 槽入 Seedance）
- **朽木ルキア**：规范参考 v01 + 多视角分布 v01
- **场景**：空座町天台（黄昏）+ 尸魂界流魂街（白天）
- 质量全部 `⚠`（待 AI 生成后验证 IaD 合规）

## 常见踩坑

1. **不要跳过 asset-lab 直接生产**：先查是否已有可复用资产。重复生产是素材系统熵增的第一来源。
2. **修订 vs 变体要区分**：小修改（修 bug、色彩微调）→ Revision，版本号递增。不同上下文（新妆造、新季节）→ Variant，新建条目 + `derived_from`。
3. **标记 archived 前检查 appears_in**：跨选题引用保护——有 active 选题仍在引用就不能归档。
4. **Seedance 版本号**：技术版本 2.0（SDK model ID `doubao-seedance-2-0-*`）。全生态统已一修正。
5. **gather-expert 消费两级制**：writer 至少读 3 字段（判定/事实性/关键引用）。进阶字段按需——不要要求 writer 读全部 9 字段。

## 下一步

1. **首次实际选题**：创建 T003，走通文本管道 + 素材首次入库
2. **AI 生成验证**：用 Seedance API 生成 Bleach 角色参考图 → IaD 检查 → 质量标记 ⚠→✓
3. **素材系统首次闭环**：需求（script）→ 生产（visual）→ 入库（asset-lab）→ 消费（director）
4. **figure-draftsman 工具安装**：drawmode、excalidraw-mcp-server 尚未安装（集成验证轮发现）
