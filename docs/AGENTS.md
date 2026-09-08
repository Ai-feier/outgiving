# docs/AGENTS.md — 文档体系规划 + 内容规范

> 本文件定义：文档体系怎么规划、目录怎么放、内容怎么写。重写/新增任何文档前先读这里。
> 读者：人 + 维护文档的 agent。

## 1. 文档体系规划

三层，各管一件事，不越界：

| 层 | 位置 | 回答 | 读者 |
| ---- | ---- | ---- | ---- |
| 入口 | 根 `README.md` / `AGENTS.md` | 这是什么、怎么跑起来 | 新人 / agent |
| 知识库 | `docs/` + `ai-video/DESIGN.md` 等 | 为什么这样、全局长什么样、怎么操作 | 人 |
| 执行契约 | `.claude/`（agents / rules / skills / _index） | 怎么做、门禁、方法 | AI agent |

Diataxis 四象限对位（写新文档先归类，一类一篇，不混写）：

| 象限 | 读者状态 | 本项目落位 |
| ---- | ---- | ---- |
| tutorial | 从零建东西 | 暂无；需要时放 `docs/` 顶层 |
| how-to | 会基础、要完成具体任务 | `docs/operations/*`、`docs/pipeline/*`（流程章）、根 README 快速开始 |
| reference | 查确切事实 | `docs/pipeline/*`（铁律/参数）、`docs/troubleshooting/`、`ai-video/DESIGN.md` §3/§5 |
| explanation | 理解为什么 | `docs/architecture/*`、`ai-video/DESIGN.md` §2/§8 |

**单一事实源**：每个知识点只有一个权威文件，其他位置只引用不复述。权威源总表见 `docs/README.md`。两套文件不一致 → 权威源赢，另一份是 bug。

## 2. 目录结构

```
根/
├── AGENTS.md              # 项目入口 + 操作手册（pi 读）；CLAUDE.md 为其镜像（软链）
├── README.md              # 人入口：一句话定位 + 快速开始 + 地图
├── docs/                  # 人类知识库（只写最终形态）
│   ├── AGENTS.md          # 本文件
│   ├── README.md          # 文档地图 + 权威源总表
│   ├── architecture/      # explanation：agent-system / ai-infra
│   ├── pipeline/          # how-to + reference：content-pipeline / video-pipeline
│   ├── operations/        # how-to：cli / git-conventions
│   └── troubleshooting/   # reference：踩坑 index
├── ai-video/              # 视频生产区
│   ├── DESIGN.md          # 唯一设计事实源（产品 + 核心模型 + 写作规格 + UI + API + 决策）
│   ├── DEV-PLAN.md        # 执行计划（迁移、兼容、风险只在这里允许出现）
│   ├── README.md          # 工作区结构与规则（入口级，深度内容在 DESIGN/docs）
│   ├── IMAGE-DESC-TEMPLATE*.md  # 参考图描述模板
│   └── projects/TXXX/     # 生产数据（单元文件/资产/成片），不是文档
└── .claude/               # AI 执行契约
    ├── _index.md          # agent/rule/skill 反向索引（skill: index-md 维护）
    ├── agents/*.md        # 10 个 agent 的完整工作契约
    ├── rules/project/     # 工作流 / 协作契约 / 命名约定
    └── skills/*/SKILL.md  # 按需触发的工作流
```

非文档区（不动）：`topics/` `platforms/` `published/` `analytics/`（内容数据）、`assets/`（资产索引）、`ref-inbox.md`（运行时收件箱）、`ai-video/projects/`。

## 3. 内容规范（写/改文档时逐条对照）

1. **最终态 only（核心铁律）**：文档只描述“系统现在是什么样”。迁移、新旧对照、审计、过程记录一律进计划文档（`DEV-PLAN.md`）或 `~/.gstack` 过程存档，不进规格。
   - 禁止：`~~删除线~~` 决策、死亡/存活表、“旧 X → 新 Y”对照、“沿用 vN”“原 XX.md 压缩”措辞、“已退役”存根文件。
   - 退役一个文档 = 删文件 + 修全部引用。不保留占位。
   - 验收：全仓 grep `固定四层|end 结果|annotations|TOGETHER|HUMAN-GATES|门 3|门 4|已退役|~~` 零命中。
2. **功能点可验证**：每个功能点指得回文件 / 命令 / 行为（路径、CLI、API、grep 式）。不写无法验证的形容词（“高效”“优雅”“健壮”）。
3. **清晰简单**：表格优先；单文件 ≤150 行（`ai-video/DESIGN.md` 与 `.claude/agents/*` 契约豁免至 ≤500 行）；一节只说一件事；删掉不影响读者理解/决策/行动的段落。
4. **决策记录归位**：计划文档可写 决策 = 上下文 / 决定 / 为什么 / 备选 / 代价；规格文档只写结论 + 一句话理由，理由指向计划文档。
5. **链接有效**：引用必须存在（无孤儿链接）；任何文档从 README 出发 ≤2 跳可达；改文件名/位置后全仓修引用。
6. **不确定显式**：未实测标 `[待实测]`，开放问题标 `[开放]`。不假装确定；精度高于完整。
7. **语气**：一个人对一个人说话。中文，不套话、不企业腔、不自夸。读者是聪明但没读过代码的人。
8. **证据先行**：写文档前先读对应代码/配置/测试；重要断言可追溯（文件:行 / 命令输出 / 实测值）。不发明细节凑完整。

## 4. 本轮全量重写执行清单（2026-08-26，范围 C）

| # | 文件 | 动作 | 状态 |
| ---- | ---- | ---- | ---- |
| 0 | `docs/AGENTS.md` | 本文件：规划 + 结构 + 规范重写 | ✅ |
| 1 | `CLAUDE.md` | 与 `AGENTS.md` 分叉（旧版）→ 改软链 | ✅ |
| 2 | `ai-video/DESIGN.md` | 重写为纯终态规格（去 §7 迁移章/死亡存活表/删除线/旧模型对照；决策审计改终态措辞；保留 §4.4–4.10 UX 契约） | ✅ |
| 3 | `ai-video/DEV-PLAN.md` | 清理过渡措辞；迁移细节（实现 v3→v4 + T005 数据迁移）保留在执行计划里 | ✅ |
| 4 | `.claude/agents/video-director.md` | 按 v4 重写生产链段落（3 部分单元 / 层 / gate / 4 触点；去 annotations/门 3/固定四层/end 自报） | ✅ |
| 5 | `.claude/agents/{script,visual,rhythm}-designer.md` | 同上 | ✅ |
| 6 | `AGENTS.md` | 去过渡措辞（“annotations 已退役”“旧四层模型见 git 历史”） | ✅ |
| 7 | `.claude/agents/douyin-writer.md` | 修断链（workbench.md → DESIGN.md）+ 管线描述改 v4 | ✅ |
| 8 | `docs/pipeline/video-pipeline.md` | “管线全景/工作区与门禁”章重写为 v4；铁律/引擎章按规范校验 | ✅ |
| 9 | `ai-video/{HUMAN-GATES,TOGETHER,workbench,workbench-product-plan}.md` | 删除（退役存根） | ✅ |
| 10 | `ai-video/README.md` `docs/README.md` `docs/pipeline/content-pipeline.md` `docs/architecture/*` `docs/operations/*` `docs/troubleshooting/index.md` | 按 §3 规范逐条校验 + 修断链（不重写无残留部分） | ✅ |
| 11 | `.claude/agents/{wechat,x,xiaohongshu}-writer.md` `gather-expert.md` `figure-draftsman.md` `.claude/rules/*` `.claude/skills/*` `.claude/_index.md` `scripts/src/AGENTS.md` | 按 §3 校验（零 v3 残留项仅查链接/密度/规范） | ✅ |
| 12 | `.claude/_loop-ai-infra-progress.md` | 进度跟踪文件 = 中间态 → 处置（删或归档 ~/.gstack） | ✅（归档 `~/.gstack/projects/outgiving/archive/`） |
| 13 | 全仓验收 | grep 验收（§3.1）+ 孤儿链接扫描 + README 2 跳可达抽查 | ✅（残留命中全在允许类别：历史 changelog / 规范元引用 / DEV-PLAN 迁移映射 / scripts 代码属 P1·P3 / T005 数据属 P3；文档与契约零违规，零孤儿链接） |

完成后跑 `bash scripts/sync_pi_agents.sh`（`.claude/agents` → `.pi/agents` 同步）。
