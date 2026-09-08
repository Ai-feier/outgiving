# docs — 项目文档体系

> 人类知识库：系统的**最终形态**（结构/流程/操作/踩坑）。AI agent 执行指令见 `.claude/`，项目概览见根 `README.md`。写作标准见 `AGENTS.md`。

## 地图

| 目录 | 内容 | 入口 |
| ------ | ------ | ------ |
| `pipeline/` | 内容管线与视频管线如何运作 | `content-pipeline.md` / `video-pipeline.md` |
| `architecture/` | 系统架构：agent 系统、AI 基础设施 | `agent-system.md` / `ai-infra.md` |
| `operations/` | 操作手册：CLI、Git 约定 | `cli.md` / `git-conventions.md` |
| `troubleshooting/` | 踩坑与解决 | `index.md` |

## 权威源（防重复）

docs 只放人读摘要，规则以权威源为准——两套体系不一致时权威源赢：

| 主题 | 权威源 | docs 中的角色 |
| ------ | -------- | -------------- |
| 数据模型 / 状态机 / CLI | `.claude/rules/project/workflow.md` | 人读摘要 |
| 命名 / Git / frontmatter | `.claude/rules/project/conventions.md` | 人读摘要 |
| 协作契约 / 交接点 | `.claude/rules/project/collaboration.md` | 链接 |
| Agent 定义 | `.claude/agents/*.md` + `.claude/_index.md` | 人读地图 |
| 管线方法 | `.claude/skills/` | 人读全景 |
| 资产体系 | `assets/asset-lab.md` + `assets/taxonomy-registry.md` | 链接 |

## 文档归位历史

2026-08 统一管理：根目录 `HANDOFF.md`（踩坑归入 troubleshooting，状态性内容过时删除）、`ai-video/` 过程文档（H3-INTEGRATION / CROSS-AUDIT / PEER-REVIEW / HUMAN-GATES-RESEARCH / reference-strategy-evidence 删除）、`README.md` 与 `ai-video/README.md` 深度内容归入 docs 后精简为入口/导航。运行时工件（HUMAN-GATES / TOGETHER / IMAGE-DESC-TEMPLATE / ref-inbox / assets 索引）保留原位，docs 链接。

2026-08-26 ai-video 文档体系统一：`HUMAN-GATES.md` / `TOGETHER.md` / `workbench.md` / `workbench-product-plan.md` 删除并入 `ai-video/DESIGN.md`（唯一设计事实源，全文归档于 git 历史）；gates/ 与 annotations.md 运行时工件退役（门记录改写入单元 ③ `### 门 · …`）。
