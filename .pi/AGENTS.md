# Harness 拓扑与归属

`.pi/` 是 AI harness 的**唯一作者源**。仓库根 [`AGENTS.md`](../AGENTS.md) 是入口约束，本文件只描述 `.pi/` 的拓扑、信息归属与修改判断权。

## 目录拓扑

| 目录 | 放什么 |
| --- | --- |
| `rules/` | 必须遵守的约束。一条约束一个文件，可判定、可机械检查 |
| `skills/` | 完成特定任务的方法与知识。单 skill 为 `skills/<name>/SKILL.md` |
| `agents/` | 岗位职责与路由。触发条件以各文件 frontmatter 的 `description` 为准 |
| `tasks/` | 运行时产物（任务日志），不是作者源，不手动编辑 |

`.pi/settings.json` 是项目级配置；`skills-lock.json` 锁定外部 skill 的来源与哈希，只引用不维护。

## 单一真相源

- harness 只有一处作者源：rules 单源 `rules/`，skills 单源 `skills/`，agents 单源 `agents/`。改约束从 `rules/` 改起。
- 不存在生成镜像与同步脚本，也没有外部索引文件。
- skill / agent 的触发条件以各自 frontmatter 的 `description` 为真源。

## 信息归属

能进 rule 或 skill 的不写进 AGENTS.md；能引用单一来源定义的不复制。

| 层 | 唯一位置 |
| --- | --- |
| 入口约束 | 根 [`AGENTS.md`](../AGENTS.md) |
| 领域术语 | [`CONTEXT.md`](../CONTEXT.md) |
| 产品定义、流程、人审面 | [`system/PRODUCT.md`](../system/PRODUCT.md) |
| 结构、形状、命名 | [`system/CONVENTIONS.md`](../system/CONVENTIONS.md) |
| 硬约束 | `rules/*.md` |
| 方法、知识 | `skills/**` |
| 岗位职责与路由 | `agents/*.md` |
| 长期决策与取舍 | [`.agents/notes/`](../.agents/notes/) |

同一内容出现在两处 = 缺陷，必须删一处。

## 修改 harness 的判断权

| 变更 | 判断权 | 约束 |
| --- | --- | --- |
| harness 层（`rules/`、`skills/`、`agents/`、本文件） | [`harness-architect`](agents/harness-architect.md) | 先理解现有 harness 再改；改后自审边界、去重与引用 |
| 产品定义、规范、目录约定（`system/`） | 人 | 目标状态唯一，不记录历史、不保留兼容层 |
| 内容产出（`products/`、`assets/`） | 对应流程岗位 | 人审面只有一张表；内部件不进人视野 |
| 执行引擎（`scripts/`） | 实现者 | 约定 → 机械门；不为单个渠道分支 |

## 不承载（各有真源）

- 一流公民、流程骨架、人审面 → [`system/PRODUCT.md`](../system/PRODUCT.md)
- 目录约定、文件形状、命名、唯一事实源矩阵 → [`system/CONVENTIONS.md`](../system/CONVENTIONS.md)
- 领域术语 → [`CONTEXT.md`](../CONTEXT.md)
- 决策记录约定 → [`.agents/notes/AGENTS.md`](../.agents/notes/AGENTS.md)
