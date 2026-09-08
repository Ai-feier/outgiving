---
name: content-pipeline
description: 多平台内容创作工作流（微信公众号/小红书/X/抖音）。数据流通过 Python CLI 管理，所有 frontmatter 由 schema 校验。使用 args 子命令：list / new / adapt / show / transition / validate / stats / index / preview。
---

# 内容创作的核心原则【IMPORTANT】
1. 这是面向公共平台的流量的内容，必须合规合法
2. 做的内容必须要有内涵，做的突出重点，外部论点，论据必须依赖网络权威的信息源, 能够从网页截图的最好截图，更有说服力, 或者 excalidraw 的流程图片

# content-pipeline — 内容创作流水线

**所有 frontmatter 操作走 Python CLI（`scripts/`），不要手改 YAML。**

CLI 入口（在仓库任意位置都可运行）：

```bash
uv run --directory scripts content <subcommand>
```

## 数据模型

四类文档（topic/draft/published/analytics），schema 见 `scripts/src/content/schema.py`；状态机、路径与 CLI 见 `rules/project/workflow.md`。父子由 `parent_id` 指向，topic 是根。

## 命令清单

CLI 命令与状态机见 `rules/project/workflow.md`。要点：**任何动作前先 `content list`**；`adapt` 自动递增 revision。**平台名仅 4 个**：`wechat` / `xiaohongshu` / `x` / `douyin`。

## 创作约定

1. **不要手写 frontmatter**：通过 `content new` / `content adapt` 创建
2. **不要手改 status**：通过 `content transition` 推进
3. 正文随便写，frontmatter 由脚本管理，`updated_at` 自动刷新
4. 一个平台目录可以有**多个文件**（正文 + 辅助文件如封面/分镜/标签），预览侧栏会自动列出

## 平台改写工作流

`content adapt T001 <platform>` 之后，**将改写工作交给对应平台的创作 agent**：

| 平台 | Agent | 产出 |
|------|-------|------|
| `wechat` | `wechat-writer` | `platforms/wechat/T0XX-<slug>/article.md` |
| `xiaohongshu` | `xiaohongshu-writer` | `platforms/xiaohongshu/T0XX-<slug>/caption.md` |
| `x` | `x-writer` | `platforms/x/T0XX-<slug>/thread.md` |
| `douyin` | `douyin-writer` | `platforms/douyin/T0XX-<slug>/script.md` |

每个 agent 内置该平台的完整创作人格——平台直觉、写作宪法、反 AI 味自检、结构骨架。四个 agent 可**并行工作**，不互相等。

Agent 启动前确保已就绪：
- `topics/T0XX-*/style.md` — 写作风格宪法
- `topics/T0XX-*/brief.md` — 核心观点 / 受众 / 钩子 / CTA / 视觉资产规划
- `topics/T0XX-*/outline.md` — 主干结构
- gather-expert 的 min- 文件和 review — 可用论据

## 写作风格宪法（所有平台通用，所有 agent 遵守）

> 本节是硬约束。每条都来自踩坑。选题级 `style.md` 写作宪法依本节为具体选题实例化（平台差异写入各 writer agent 文件）。

### 句法
- **一行之内句句环环相扣**——前半句铺路，后半句落地
- **一行只讲一件事**——出现"并且/同时/另外"想塞第二件事时，另起一行
- **拒绝套话开头**——禁用"在当今/随着/众所周知/不可否认"；直接从一件具体事切入
- **拒绝修辞空转**——"如同/仿佛/宛如"后必须跟具体意象，否则删掉

### 段落
- **每段 ≤4 行**（wechat 硬规则，其他平台参考）
- **段落之间必须有显性衔接或自然过渡**——禁止两个不相关的段直接拼在一起
- **金句放段末独立一行**，但**禁止连续 2+ 行金句**——金句之间必须穿插叙述或论证

### 链接
- **禁止孤行链接**——`[名称](url)` 单独占一行是 AI 味最重的一种
- **链接必须行内融入**
- **多个相关链接合并到一句话**
- **卖方/厂商来源必须标注立场**

### 引用与论据
- **外部论点必须挂链接**
- **来源类型要诚实标注**——一手论文 / 厂商博客 / 评论文章 / 个人推文
- **未核实的来源明说**`（需核实原文）`

### 语气
- **不向"读者"演讲**——写得像在跟一个具体的朋友讲
- **不要装权威**——用"我"和"你"，少用"我们/大家"
- **幽默只在能加密度时加**——梗没承载信息就删

## 反 AI 味原则（所有平台通用）

- **每写完一段对照自检**：遮住这段能不能猜出在讲哪件具体事？有没有"首先/其次/最后"？有没有孤行链接？是不是 3 行以上抽象论述？金句连续 2+ 行？
- **不靠字数**——按内容自然长度
- **不靠结构**——不用"首先/其次/最后"、"问题→分析→总结"三段式
- **靠具体性**——开头必须有一件**具体的事**
- **靠诚恳**——写得像在跟一个具体的朋友讲

各平台有各自的平台专属写作宪法与反 AI 味检查，在 `.claude/agents/<平台>-writer.md` 里。

## 最小经验

### 流程上
- **brief 阶段图文一体**——每张图服务某号关键信息点，不写完正文再补图
- **闭环顺序**：gather-expert 研究 → brief → outline → style → 四个平台 agent 并行改 → figure-draftsman 出图 → validate → preview → human review
- **正文改完立刻** `content validate` + `content preview <T0XX>`

### 技术上
- **图片路径用 `![](assets/figN.svg)` 不要 `../../../`**——preview 服务器会智能解析
- **`.svg` 单源**——svg 可预览
- **图片生成交给 `figure-draftsman` agent**——不要手写 matplotlib
- **研究交给 `gather-expert` agent**——第一性原理收敛，不写综述
- **平台改写交给对应 `*-writer` agent**——不自己手动改写

## 故障排查

| 现象 | 解决 |
|---|---|
| `validate` 报「未知 kind」 | frontmatter 缺字段，用 `content new` / `adapt` 重新生成 |
| `transition` 报「不允许从 X→Y」 | 走完整状态链，如 draft→reviewing→ready |
| 命令找不到 | 在仓库根跑 `cd scripts && uv sync` |
| preview 端口占用 | `pkill -f "content preview"` 后重启 |
| preview 图片 404 | 检查正文是否用了 `../../../` 相对路径——改用 `assets/figN.svg` |
| 中文路径 404 | preview 已处理 Latin-1→UTF-8，重启服务；检查 `unquote` 是否被重复调用 |
