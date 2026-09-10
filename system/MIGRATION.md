# 搬迁清单（一次性）

> 执行本清单期间有效。**全部完成后删除本文件**——目标状态是仓库里唯一的状态。
> 依据：`system/PRODUCT.md`（产品定义）+ `system/CONVENTIONS.md`（结构规范）。

## 1. 新建

| 路径 | 内容 | 来源 |
| --- | --- | --- |
| `.pi/AGENTS.md` | harness 拓扑 + 归属模型 + 修改判断权 | 参照 building-in-public 同名文件 |
| `.pi/agents/harness-architect.md` | harness 信息架构维护岗位 | 从 `building-in-public/.pi/agents/harness-architect.md` 复制，改写路径引用 |
| `.pi/rules/` | 约束（每文件一条，可判定） | 重写自 `.claude/rules/project/` |
| `.pi/skills/ask/SKILL.md` | 入口路由：按流程阶段 → 具体 skill；创作阶段按形态分叉 | 新写 |
| `.pi/skills/channels/CHANNELS.md` | 渠道共有维度表 | 从 4 个 writer 的共有维度抽取（现散落 9 处） |
| `.pi/skills/channels/<channel>.md` | 渠道卡（每渠道一张） | 4 个 writer 的专属内容（占其 59%） |
| `.pi/skills/research-evidence/` | 研究：证据锚点等级、跨谱系、来源性质 | gather-expert 的知识部分 |
| `.pi/skills/narrative-structure/` | 结构：骨架类型与信息点序列 | script-designer 的结构部分 |
| `.pi/skills/writing-craft/` | 文本创作通用方法（诚实/具体/删） | 4 个 writer 的通用部分（44 行）+ 现有写作规则 |
| `.pi/skills/shot-language/` | 景别/运镜/角度/光学/光影/转场 | 现 `video-craft` 词汇表 + `video-director` 电影语言模块（**二者合一，消除重复**） |
| `.pi/skills/rhythm/` | 节奏曲线、认知负荷、停顿点 | rhythm-designer 与 video-craft 的节奏部分 |
| `.pi/skills/visual-world/` | 材质、环境、情绪动作化、角色语言 | visual-designer 与 video-craft 的视觉部分 |
| `.pi/skills/prompt-engineering/` | 提示词公式与工具能力边界 | video-director 的提示词部分 + video-craft 的公式 |
| `.pi/skills/asset-search/` | 参考素材搜索五步法 | 现 `find-ref` |
| `.pi/skills/verify-checklist/` | 校验清单（事实/契约/技术） | 新写 + 现有自评估规则归位 |
| `.agents/notes/{implemented,proposed,rejected}/` + `AGENTS.md` + `README.md` | 决策记录约定 | 参照 building-in-public |
| `scripts/check_harness.*` | 仓库级检查入口（见 CONVENTIONS「检查门」） | 新写 |
| `products/` | 选题树 | 迁移自 `topics/` + `platforms/` + `published/` + `analytics/` |

## 2. 改写（内容归位，原文件不保留）

| 现有 | 去向 |
| --- | --- |
| `.claude/agents/{wechat,xiaohongshu,x,douyin}-writer.md`（614 行） | 专属 59% → 4 张渠道卡；通用 7% → `writing-craft`；岗位 → `.pi/agents/writer.md`（1 个） |
| `.claude/agents/{script,visual,rhythm,video-director}.md`（1904 行） | 知识 43% → 对应知识 skill；契约 57% → 收成一份规格；岗位 → `.pi/agents/video-director.md`（1 个） |
| `.claude/agents/gather-expert.md` | 知识 → `research-evidence`；岗位 → `.pi/agents/researcher.md` |
| `.claude/agents/figure-draftsman.md` | 方法 → 视觉资产 skill；岗位 → `.pi/agents/visual-draftsman.md` |
| `.claude/skills/video-craft/SKILL.md`（248 行，零消费者） | **拆解归位**（shot-language / rhythm / visual-world / prompt-engineering），原文件删除 |
| `.claude/skills/reflecting/SKILL.md` | → `.pi/skills/reflecting/`（唯一被全部岗位消费的机制，保留） |
| `.claude/skills/content-pipeline/SKILL.md` | 流程方法并入 `ask` 与流程文档；CLI 部分指向 `scripts/` |
| `.claude/skills/index-md/SKILL.md` | 与新索引模型冲突（禁止集中索引）→ 删除 |
| `.claude/rules/project/{workflow,collaboration,conventions}.md` | 按新模型重写进 `.pi/rules/`（不整搬；平台状态机与视频状态机合并为流程阶段） |
| `.claude/skills/{engineering,productivity}/**`（35 目录） | → `.pi/skills/{engineering,productivity}/`，加 README 标明「通用工具包，不属于本仓流水线」 |
| `ai-video/DESIGN.md`（357 行） | 契约部分 → `.pi/` 或 `system/` 的规格；模型部分被本 spec 取代 |
| `ai-video/projects/T006/` | → `products/T006-*/`（主题与文字复用，文件形状按新规范重做，人审表重出） |
| `scripts/src/workbench/`（3528 行：chain 742 + server 513 + app.html 1979） | 砍到**一页表渲染器**：只渲染人审表 + 改/追问/拍板/验收四个写回入口；DAG/5 层/状态机/请求体装配全部移除 |
| `scripts/src/content/` | 数据模型适配 `products/`（目录与字段） |
| `docs/**`（11 md） | 与 `system/` 重复的删除；保留操作类（CLI 手册、踩坑、issue/triage 约定） |
| `AGENTS.md` / `CONTEXT.md` | 按新定位重写（词表：渠道取代平台等） |

## 3. 删除

| 路径 | 理由 |
| --- | --- |
| `.claude/` 整树 | 迁移完成后删除（单源在 `.pi/`） |
| `scripts/sync_pi_agents.sh` | 生成镜像机制取消 |
| `.claude/memory/*.md`（7 个） | 3 个孤儿直接删；其余转 `.agents/notes/` |
| `ai-video/IMAGE-DESC-TEMPLATE.md`、`-SCENE.md` | 零消费者 |
| `ai-video/DEV-PLAN.md` | 被本 spec 取代 |
| `scripts/gen_figures_T002.py` | 零引用 |
| `scripts/src/volcengine/_generate_ichigo.py` | 一次性脚本，零引用 |
| `ai-video/projects/T999-test/` | 测试残留 |
| `system/REFACTOR-SPEC.md` | issue 发布后删除 |
| `system/MIGRATION.md`（本文件） | 搬迁完成后删除 |

## 4. 归档（移出活目录，不迁格式）

| 路径 | 去向 |
| --- | --- |
| `ai-video/projects/T001/`、`T003/`、`T004-funny-video/`（~9000 行，无 `unit:` 不进链） | `archive/`（或 `products/_archive/`，二选一后写进 CONVENTIONS） |
| `ai-video/` 残余目录 | 归档后删除空壳 |

T005（链模型首个真项目）与 T006 一样冻结：主题文字可复用，格式不迁。

## 5. 保留不动

`scripts/tests/`（8 个测试，回归基线）· `scripts/src/{ai,editor}/`（生成与编辑引擎）· `scripts/src/{web_fetcher,stock_finder}/` · `assets/`（素材库，索引文件按需保留）· `inbox/` 与 `ref-inbox.md`（选题入口，命名随 `products/` 调整）· `.claude/settings.json` 的有效配置项（迁到 `.pi/settings.json`）· `pyrightconfig.json`、`skills-lock.json`（核对其作用后保留或删）

## 6. 执行顺序

1. **harness 单源**：建 `.pi/{rules,skills,agents}` + `.pi/AGENTS.md` + `.agents/notes/` + harness-architect → 删 `.claude/` 与同步脚本
2. **能力重建**：`ask` + 流程 skill + 渠道表/卡 + 知识 skill 落位 → 删旧 skill 与被拆解的原文件
3. **仓库树**：`products/` 迁移 + `system/` 落文档 + `docs/` 收敛 + workbench 缩减
4. **检查门 + 验收**：写 `check_harness` 并通过；用 T006 走一遍新流程验证人审面
5. **收尾**：删一次性文档（本文件、REFACTOR-SPEC）

## 7. 验收

- `scripts/check_harness.*` 通过（6 项检查全绿）
- 顶层恰好 7 项 + `AGENTS.md` + `CONTEXT.md`
- `grep -ri "平台"` 在路径、字段、规范中零残留（历史归档与 notes 除外）
- T006 走一遍新流程：改表 / 追问 / 拍板 / 验收**四个动作只在一张表上完成**（若必须打开其他文件才能判断 → 设计不成立，回炉）
- 每个 skill 都有消费者；无未消费知识
