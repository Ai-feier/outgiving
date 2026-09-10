# 规范

> 产品定义与质量标准见 [`PRODUCT.md`](PRODUCT.md)——本文件不复制其内容，只定义**结构与形状**。

## 目录约定

| 目录 | 放什么 | 禁止 |
| --- | --- | --- |
| `products/` | 一个选题一个目录，全生命周期在内（素材引用、各渠道产出、发布记录、复盘） | 不按渠道分顶层目录；不把未选题的草稿散在顶层 |
| `assets/` | 跨选题复用的素材：角色、场景、图、音、参考 | 不放单个选题的一次性产物 |
| `system/` | 产品设计、规范、目录约定、领域决策 | 不放流程性临时文件 |
| `scripts/` | 执行引擎：生成、渲染、检查 | 不放业务内容 |
| `.pi/rules/` | 必须遵守的约束 | 不写方法（方法是 skill） |
| `.pi/skills/` | 完成特定任务的方法与知识 | 不写岗位职责 |
| `.pi/agents/` | 岗位职责与路由 | 不内嵌知识 |
| `.agents/notes/` | 长期决策记录（含被否方案） | 不写实现细节；不建集中索引 |
| 根 | `AGENTS.md`（入口约束）、`CONTEXT.md`（领域词表） | 不放其他文件 |

顶层只允许 7 项（`.agents/` `.githooks/` `.pi/` `assets/` `products/` `scripts/` `system/`）+ 根两份入口文件（`AGENTS.md`、`CONTEXT.md`）。git 机制文件由检查门放行，当前只有 `.gitignore`（`.githooks/` 已计入 7 项）。新增顶层目录需要一条决策记录。

### 归档与收件箱

- **归档**：`products/_archive/<原选题目录>/`。旧格式项目**原样搬入**——不迁格式、不回改；活在 `products/` 顶层的是唯一目标状态。
- **选题入口**：`products/_inbox/`——未成选题的草稿落点；转正时移入 `products/<id>-<slug>/`。
- **素材收件箱**：`assets/ref-inbox.md`——人在外部发现的参考素材，粘 URL + 注用途；消费方法与流程见 [`.pi/skills/asset-search/SKILL.md`](../.pi/skills/asset-search/SKILL.md)。

下划线前缀（`_archive/` `_inbox/`）表示“不是选题”，不占选题 id。

## 文件形状

**skill**：`.pi/skills/<name>/SKILL.md`
frontmatter 仅 `name` + `description`（触发条件写在 description）；正文 = 方法 + ≥1 个真实例子。深层引用放同目录其他文件，不把大表塞进 SKILL.md。

**agent**：`.pi/agents/<name>.md`
frontmatter：`name` / `description`（职责与何时派发）/ `tools`；正文 = 职责边界 + 读哪些 skill + 不做什么。**不含知识本体**。

**rule**：`.pi/rules/<name>.md`
一条约束一个文件，可判定、可机械检查，不解释背景。

**决策记录**：`.agents/notes/{implemented,proposed,rejected}/<YYYY-MM-DD>-<slug>.md`
标题三行内说清决策；必须含「被否方案」一节；引用用相对链接；不建索引文件。

**渠道卡**：`.pi/skills/channels/<channel>.md`
只写该渠道专属内容（读者注意状态、算法机制及来源、专属法则、复盘节奏）。共有维度一律进 `CHANNELS.md`。

**项目产出**：`products/<id>-<slug>/`
固定入口是 `review.md`——一张人审表（字段见 [`PRODUCT.md`](PRODUCT.md)「人审面」），表下固定三块（关键决策 / 未锚假设 / 待你拍板）+ 追问区（待回答）。其余文件按需，但**人审只需 `review.md`**。

## 唯一事实源矩阵

| 信息 | 唯一位置 |
| --- | --- |
| 领域术语 | `CONTEXT.md` |
| 产品定位、流程、人审面 | `system/PRODUCT.md` |
| 结构、形状、命名 | `system/CONVENTIONS.md` |
| 渠道共有维度 | `.pi/skills/channels/CHANNELS.md` |
| 渠道专属知识 | `.pi/skills/channels/<channel>.md` |
| 专业方法与知识 | `.pi/skills/**` |
| 岗位职责与路由 | `.pi/agents/*.md` |
| 硬约束 | `.pi/rules/*.md` |
| 决策与取舍 | `.agents/notes/**` |
| 项目事实 | `products/<id>/**` 与 `assets/**` |

出现同一内容在两处 = 缺陷，不是冗余，必须删一处。

## 命名

| 对象 | 规则 | 示例 |
| --- | --- | --- |
| 选题 id | `T` + 三位数字 | `T006` |
| 选题目录 | `<id>-<中文 slug>`，≤60 字符 | `T006-请大佛开口` |
| 渠道名 | 小写单词，与渠道卡文件名一致 | `wechat` / `x` |
| skill / agent | kebab-case，动词或名词短语 | `shot-language` / `verifier` |
| 决策记录 | `<日期>-<kebab-slug>` | `2026-09-09-harness-single-source.md` |
| 素材 | `assets/<类别>/<语义名>` | `assets/styles/bleach.md` |

## 检查门

一个入口：`scripts/check_harness.py`。唯一命令：

```bash
uv run --directory scripts check_harness.py
```

一条命令跑完全部检查；失败即非零退出，逐条输出 `PASS`/`FAIL` + 失败原因 + `文件:行` 定位。
判定口径的作者源就是这个脚本，本节只写命令与需要文字定义的两处口径。

至少覆盖：

1. 顶层只有允许的 7 项 + 两份入口文件 + 已放行的 git 机制文件（清单见「目录约定」）
2. 每个 skill 有消费者（被 ≥1 个 agent 或流程引用）
3. 渠道名不出现在任何路径中
4. 共有维度不在两处定义（禁用词表：单拍时长、组块上限等）
5. 仓库内相对引用可解析（含决策记录）—— 扫描面 = 全仓 md 的 markdown 链接 + 根相对反引号路径（`.pi/`、`system/`、`scripts/`、`assets/`）
6. 每个 skill 含 ≥1 个例子——可判定的最小结构：SKILL.md 有一个含「例子 / 真例 / 示例 / 实例 / Example」的 ATX 标题，或一个同时含「输入」与「输出」的围栏代码块。只约束本仓作者源的 skill；`.pi/skills/engineering/`、`.pi/skills/productivity/`（外部引入的通用工具包）与 `.pi/skills/h3-prompt-writing/`（外部锁定 skill）豁免——质量标准是对本仓内容的要求，不对别人的源文件施加
7. 「平台」零残留——扫路径与文件内容；豁免「必须点出被禁词」的规则行本身，以及不指代内容出口的云服务商名称（行级白名单，条目与理由见 `scripts/check_harness.py`）

## 禁止项

- 不建生成镜像、不同步脚本：harness 只有一处作者源
- 不在两处定义同一内容
- 不在路径、字段、文档里使用「平台」指代渠道
- 不保留兼容读写、不做新旧并行
- 不写没有消费者的知识
- 不建集中索引文件（触发靠 frontmatter 的 description）
- 不把临时流程文件留在仓库里
