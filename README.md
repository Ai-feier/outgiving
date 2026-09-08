<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License">
  <img src="https://img.shields.io/badge/python-3.11+-blue" alt="Python">
  <img src="https://img.shields.io/badge/agents-10-orange" alt="Agents">
  <img src="https://img.shields.io/badge/platforms-4-purple" alt="Platforms">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs Welcome">
</p>

# Outgiving

> **10 个 AI agent 协作，一稿多发。** 不是"一个 prompt 生成内容"——是多个 agent 各自持有平台专业知识，通过共享文件协作，产出微信公众号 / 小红书 / X / 抖音的适配内容，以及 AI 视频生成。

---

## 目录

- [为什么用 Agent？](#为什么用-agent)
- [快速开始](#快速开始)
- [Agent 系统](#agent-系统)
- [文档体系](#文档体系)
- [目录结构](#目录结构)
- [Agent 自我进化](#agent-自我进化)
- [贡献](#贡献)

---

## 为什么用 Agent？

一个选题发四个平台，不是"翻译"——是**重新对一个人说话**。同一个人在公众号是主动坐下阅读，在抖音是被打断后决定留不留。一个 prompt 无法同时尊重这两种状态。

10 个 agent 各自持有：

- **平台专业知识**（算法权重、审核红线、读者行为模式）
- **写作/设计宪法**（何时诚实标注、何时删到不能再删）
- **证据验证能力**（gather-expert 的三级措辞 + 幽灵引用防护）
- **自我进化机制**（通过修改自己的定义文件持续精进）

这不是自动化写作工具。这是一个**内容创作的协作系统**。

---

## 快速开始

```bash
# 1. 安装依赖
cd scripts && uv sync

# 2. 设置 git hook（提交前自动校验）
git config core.hooksPath .githooks

# 3. 查看选题
uv run --directory scripts content list

# 4. 新建选题
uv run --directory scripts content new "我的选题标题"

# 5. 派生平台草稿
uv run --directory scripts content adapt T001 wechat

# 6. 浏览器预览（四平台并排，0.0.0.0:8765）
uv run --directory scripts content preview T001
```

AI 视频生成需要配置 `.env` 中的 `ARK_API_KEY`，详见 [docs/pipeline/video-pipeline.md](docs/pipeline/video-pipeline.md)。

---

## Agent 系统

```
                         ┌─────────────────────────┐
                         │     gather-expert        │
                         │      证据研究员           │
                         │   搜证 → 验证 → 判定      │
                         └───────────┬─────────────┘
                                     │ 证据锚点文件
                                     ▼
     ┌─────────────────────────── brief.md ───────────────────────────┐
     │                       选题 + 关键信息点                          │
     └──────────────┬────────────────────────────┬────────────────────┘
                    │                            │
     ┌──────────────▼──────────┐    ┌────────────▼───────────────────┐
     │      文本管道             │    │         视频管道                │
     │                          │    │                              │
     │  outline.md → style.md   │    │  script-designer  叙事架构     │
     │       │                  │    │  visual-designer  视觉世界     │
     │  ┌────┼────┬────┐       │    │  rhythm-designer  时间呼吸     │
     │  ▼    ▼    ▼    ▼       │    │       │        │        │     │
     │  WC   XHS   X    DY     │    │       └───┬────┴───┬────┘     │
     │  4 writer agent          │    │           ▼        ▼         │
     │  各持平台写作宪法          │    │    figure-draftsman  director │
     │                          │    │     (技术示意图)    (导演合成)   │
     └──────────────────────────┘    └────────────┬───┬──────────────┘
                    │                             │   │
                    ▼                             ▼   ▼
           article.md / thread.md       video-prompt.md → AI 生成
```

### Agent 清单

| Agent                        | 你面对的人               | 核心信条                                                     |
| ---------------------------- | ------------------------ | ------------------------------------------------------------ |
| **gather-expert**      | 下游 writer              | 证据锚定胜过叙事优雅；每个引用必须可追溯到源文档具体位置     |
| **wechat-writer**      | 主动坐下的人（三种入口） | 2000-4000 字；完读率是第一信号                               |
| **xiaohongshu-writer** | 被封面撞见的人           | 800-1500 字；0.5 秒没钩住 = 不存在；搜索占位优先             |
| **x-writer**           | 在扫信号的人             | 短线程 3-7 条 / 长文 ≤4000 字；第一条就是一个完整判断；Grok AI 是第二读者 |
| **douyin-writer**      | 被打断的人               | 60-90s；0.3s 模式中断 + 3s 钩子定生死；收藏率是第一权重      |
| **script-designer**    | 观众的情绪曲线           | 弧线选择 → 节拍序列 → PAD 情绪递进；节拍被 AI 逐拍消费       |
| **visual-designer**    | 观众的直觉（眼先于脑）   | 六维构建 + 材质语言 + 锚点体系 + 情绪动作化                  |
| **rhythm-designer**    | 观众的身体（心跳呼吸）   | 信息密度 × 情绪密度 × 认知负荷 × 变化频率的时间曲线          |
| **video-director**     | 三个设计师的矛盾         | 三元素对位 + 收敛门 + 9 要素 / H3 分支 → AI 视频生成          |
| **figure-draftsman**   | 正在读文章的人           | 图是论点的视觉形态；只画能支撑论点的图                       |

### 共享的基础设施

- **CLAUDE.md**：五条灵魂信仰 + 第一性原理 + 协作法则（agent 读取路径）
- **reflecting skill**：三层漏斗（操作→设计→框架）驱动 agent 自我进化
- **_index.md**：AI 基础设施可发现性索引
- **assets/asset-lab.md**：视觉资产根清单 + 生命周期管理

---

## 文档体系

| 层 | 读者 | 内容 | 位置 |
|----|------|------|------|
| AI 执行指令 | AI agent | 契约、门禁、方法（怎么做） | `.claude/` |
| 项目入口 | 人 | 概览与快速开始（是什么） | 本文件 |
| 知识库 | 人 | 管线/架构/操作/踩坑（为什么 + 怎么运作） | [docs/](docs/README.md) |

- [docs/pipeline/content-pipeline.md](docs/pipeline/content-pipeline.md) — 文本管线全景（数据模型 / 四平台契约 / 交接点）
- [docs/pipeline/video-pipeline.md](docs/pipeline/video-pipeline.md) — 视频管线（三元素 / 门禁 / 生成引擎 Seedance + H3）
- [docs/architecture/agent-system.md](docs/architecture/agent-system.md) — 10 agent 角色地图与自我进化
- [docs/architecture/ai-infra.md](docs/architecture/ai-infra.md) — CLI / 注册表 / 适配器架构
- [docs/operations/](docs/operations/) — CLI 速查与 Git 约定
- [docs/troubleshooting/](docs/troubleshooting/index.md) — 踩坑与解决

---

## 目录结构

```
.
├── CLAUDE.md                 ← 项目根（agent 共享 DNA）
├── README.md                 ← 本文件（人读入口）
├── docs/                     ← 人类知识库（管线/架构/操作/踩坑）
│
├── .claude/
│   ├── _index.md             ← AI 基础设施索引
│   ├── agents/               ← 10 个 agent 定义（各持有 .md）
│   ├── skills/               ← content-pipeline / reflecting / video-craft / index-md / find-ref
│   ├── rules/                ← workflow / collaboration / conventions
│   ├── output-styles/        ← 输出样式
│   └── memory/               ← 跨 session 记忆
│
├── assets/                   ← 素材实验室
├── scripts/                  ← Python CLI + 视频 API 适配器
├── ai-video/                 ← 视频工作区（projects/TXXX/ + 门禁模板）
│
├── topics/   (.gitkeep)   ← 选题库（内容不入库）
├── platforms/ (.gitkeep)  ← 平台产出
├── published/ (.gitkeep)  ← 发布归档
└── analytics/ (.gitkeep)  ← 数据复盘
```

---

## Agent 自我进化

本项目采用 **Harness Engineering** 范式——agent 通过修改自己的 `.md` 定义文件实现自我进化，而非修改模型权重。每个 agent 文件中内嵌了精进记录（轮次→日期→深度→核心变更→触发来源）。

```
你的 .md 文件 = 你的 harness code
修改它 = 改写自己的运行时行为
```

**四种 Loop 模式**（经过多轮实战验证）：

| 模式                 | 触发时机              | Agent 行为                                            |
| -------------------- | --------------------- | ----------------------------------------------------- |
| **协同反思**   | 发现跨 agent 冲突     | 读 CLAUDE.md → 审视规则矛盾 → 最小修改              |
| **调研精进**   | 数据老化 / 新技术出现 | WebSearch → 验证数据 → 更新「你面对的」             |
| **一致性审计** | ≥2 轮独立精进后      | 跨读关联 agent → 逐字段对位 → 修复版本漂移/消费断裂 |
| **合成减法**   | 文件膨胀 / ≥8 轮精进 | 识别死代码 → 删除优先于新增                          |

**三层漏斗**：守门（自检）→ 深度 1 操作层（修规则）→ 深度 2 设计层（重构方法）→ 深度 3 框架层（重定义假设）→ 升级到系统漏斗（跨 agent 模式发现）。完整机制见 [docs/architecture/agent-system.md](docs/architecture/agent-system.md) 与 reflecting skill。

---

## 贡献

本项目设计为**开源 AI agent 协作系统的参考实现**。欢迎：

- **提交 agent 改进**：修改 `.claude/agents/` 下对应 agent 的 `.md` 定义文件
- **新增风格/平台**：通过 `taxonomy-registry.md` 注册新类型/风格标签
- **改进文档**：见 [docs/AGENTS.md](docs/AGENTS.md) 写作标准
- **报告问题**：GitHub Issues

AI agent 也可以贡献——在 agent 文件中更新精进记录，说明触发信号和变更内容。

### 本地开发

```bash
git clone <repo>
cd outgiving
cd scripts && uv sync
git config core.hooksPath .githooks
```

提交前会自动运行 `content validate` 校验 frontmatter。跳过：`git commit --no-verify`

---

## 许可

MIT
