# AI 基础设施索引

> 本项目所有 AI 编程基础设施的统一入口。AI 通过此文件发现、使用、维护自身工具链。

## Skills（内容创作 / 治理 / 沉淀）

| Skill | 触发 | 说明 |
|-------|------|------|
| [content-pipeline](skills/content-pipeline/SKILL.md) | 选题、改写、发布、预览 | 多平台内容创作流水线：选题→研究→大纲→风格→改写→校验→预览→发布→复盘。**本项目的核心 skill** |
| [index-md](skills/index-md/SKILL.md) | 新增/修改 `.claude/` 文件后、定期巡检 | 通过 `_index.md` 反向引用体系管理 AI 基础设施的可发现性 |
| [reflecting](skills/reflecting/SKILL.md) | 会话收尾 / 内容 review 出问题 / 修改基础设施 / 手动 | 三层漏斗（Agent→协作者→系统）：4 深度递进→协同性审计→ABC 审视→元反思 |
| [video-craft](skills/video-craft/SKILL.md) | 视频选题、AI 视频生成 | AI 视频创作元知识：剧本/主体/节奏三元素相互成就的认知框架，不是工序流水线 |
| [find-ref](skills/find-ref/SKILL.md) | `/find-ref [query]` — 任何 agent 需要参考素材时 | 规范化参考素材搜索：五步法（需求→来源→搜索→验证→下载）+ 精进日志。与 visual-designer gate 流程对接 |

## Agents

所有 agent 平级放在 `.claude/agents/`，任何 skill 均可调用。

### 文本创作 Agent（content-pipeline）

| Agent | 平台 | 产出 |
|-------|------|------|
| [wechat-writer](agents/wechat-writer.md) | 微信公众号 | 图文长文 `article.md` |
| [xiaohongshu-writer](agents/xiaohongshu-writer.md) | 小红书 | 图集 + 短文案 `caption.md` |
| [x-writer](agents/x-writer.md) | X (Twitter) | 推文串 `thread.md` |
| [douyin-writer](agents/douyin-writer.md) | 抖音 | 短视频脚本 + 分镜 `script.md` |

### 视频创作 Agent（video-craft）

| Agent | 角色 | 本质 |
|-------|------|------|
| [script-designer](agents/script-designer.md) | 剧本设计 | 叙事架构——信息以什么顺序、什么情绪递进被接收。节拍直接翻译为 AI 生成指令 |
| [visual-designer](agents/visual-designer.md) | 主体设计 | 视觉世界——观众看见的世界的统一性法则 |
| [rhythm-designer](agents/rhythm-designer.md) | 节奏设计 | 时间呼吸——信息密度和情绪密度的曲线 |
| [video-director](agents/video-director.md) | 导演合成 | 三元素互洽 + 风格注入 → AI 视频生成 prompt |

### 共享 Agent

| Agent | 使用场景 | 说明 |
|-------|---------|------|
| [gather-expert](agents/gather-expert.md) | 选题研究 | 第一性原理资料收集 |
| [figure-draftsman](agents/figure-draftsman.md) | 出图 | 手绘风 .svg 单输出 |

### 工作流（文本）

```
选题 → gather-expert 研究 → brief → outline → style
                                                    │
                    ┌───────────────────────────────┼───────────────────────────────┐
                    ▼                               ▼                               ▼
            wechat-writer                  xiaohongshu-writer               x-writer / douyin-writer
                    │                               │                               │
                    ▼                               ▼                               ▼
              article.md                      caption.md                    thread.md / script.md
                    │                               │                               │
                    └───────────────────────────────┴───────────────────────────────┘
                                                    │
                                    figure-draftsman（并行出图）
                                                    │
                                          validate + preview
                                                    │
                                               human review
```

## Output Styles（输出样式）

| Style | 效果 |
|-------|------|
| [content-style](output-styles/content-style.md) | 操作简洁、元输出结构化、内容创作不受限 |

## Rules（项目管理宪法）

始终加载的操作约束。不同于 Skills（任务触发）、Agents（角色定义）——Rules 是**自动生效的约束**。

| Rule | 文件 | 说明 |
|------|------|------|
| 内容工作流 | [workflow](rules/project/workflow.md) | 生命周期状态机 + CLI + 质量门禁 + 协同性自检 |
| Agent 协作 | [collaboration](rules/project/collaboration.md) | 调用约定 + 共享文件协议 + 交接契约 + 指标对齐 |
| 项目约定 | [conventions](rules/project/conventions.md) | 命名 + frontmatter + 目录结构 + Git 约定 |

> 架构参考 [affaan-m/ECC](https://github.com/affaan-m/ECC) `.claude/rules`，为本项目特化。
> Rules 与 CLAUDE.md 的关系：CLAUDE.md 定义「为什么」（灵魂+第一性原理），Rules 定义「怎么做」（操作约束）。

## 项目全局入口

| 文件 | 角色 |
|------|------|
| `CLAUDE.md` | 项目协作权威入口：数据模型、命令、约定、协作者角色 |
| `rules/README.md` | Rules 系统说明：架构、优先级、维护规则 |
| `README.md` | 人类可读的项目说明 |

## 资产系统

资产沉淀体系的受控词汇表独立于 `_index.md` 管理：

| 文件 | 角色 | 维护者 |
|------|------|--------|
| `assets/taxonomy-registry.md` | 受控词汇表（类型前缀/风格标签/状态码/变体名/治理流程） | visual-designer |
| `assets/asset-lab.md` | 资产根清单（索引路由+生命周期规则） | visual-designer |
| `assets/*-index.md` | 类型级子索引 | visual-designer |

## 自审规则

每次修改 `.claude/` 后自审，每次 reflecting 触发时全面检查：

```
□ 去重        — skills/agents/rules 间无重复规则，冲突规则已合并
□ 过期        — 所有引用路径有效（链接目标存在），无失效引用
□ 行数        — 单个 SKILL.md ≤ 200 行，单个 rule ≤ 150 行，超限拆分
□ 交叉引用    — _index.md 覆盖全部 skills/agents/rules/output-styles/memory，无孤立文件
□ 触发条件    — 每个 skill 的触发条件准确，无漏触发/误触发
□ CLAUDE.md   — 项目级入口不超过 200 行，新增命令/约定已同步
□ Rules       — 规则不重复 CLAUDE.md 内容（灵魂信仰/第一性原理），规则定义操作约束
```
