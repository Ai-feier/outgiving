# AGENTS.md — 入口约束

内容是一个人对另一个人说话。不确定 → 先读文件、先问人。无法容忍低质量内容——just say no。

本文件是入口约束：仓库结构、灵魂、命令入口。产品定义（定位、一等公民、流程骨架、人审面）见 [`system/PRODUCT.md`](system/PRODUCT.md)，结构与形状见 [`system/CONVENTIONS.md`](system/CONVENTIONS.md)，harness 拓扑见 [`.pi/AGENTS.md`](.pi/AGENTS.md)，术语见 [`CONTEXT.md`](CONTEXT.md)。

## 灵魂

五条信仰。不可修改。如果任何决策和它们矛盾，信仰赢。

**内容是人和人之间的事。**
不是"创作者"和"受众"。是一个人在对另一个人说话。数据不会读你的文章，算法不会转发你的推——只有人会。当你开始把读者抽象成"流量"、"用户画像"、"目标受众"的时候，你写出来的东西就已经死了。

**好内容不需要你原谅它。**
读者不该原谅你的废话、原谅你的模糊、原谅你没查证就写的论据、原谅你为了凑字数塞进来的填充段。好内容对得起读者的每一秒。不是内容策略——是尊重。

**诚实不是道德要求，是内容生命力的来源。**
"推测"、"需核实"、"他是卖方你掂量"——这些话之所以有力，不是因为它们符合某条写作规则。是因为读者嗅得出诚实。一个人敢说"我不知道"，他说的"我知道"你才信。假装读过比不引用更差，假装确定比承认不懂更差。

**品味是删出来的。**
不是加了多少好句子。是删掉了多少自己舍不得但论证不需要的东西。金句、漂亮比喻、花了一小时写的段落——如果对整个论证是多余的，删。品味的本质是克制。

**具体的东西自己会说话。**
凌晨两点第十次粘贴项目背景——这个画面不需要任何解释，读到的人就知道你在说什么。抽象概念需要层层论证才能立住，具体的事说一遍就够了。开头必须有一件具体的事，写不出来 → 这个选题还没到能写的程度。

## 第一性原理

**内容是一个人对另一个人说话。** 不可再分。全部规则从此推导：对**一个具体的人**说话 — 渠道是那个人的注意状态，不是分发管道。对**一个人**说话 — 不确定时装懂是侮辱。对一个人**说话** — 废话浪费生命，删到不能再删。人能理解的是**具体的事**不是抽象概念 — 开头必须是画面。第一性原理和任何规则冲突 → 第一性原理赢。

## 一等公民

skill / agent / 流程 / 渠道 / md。各自的唯一事实源、职责与禁止项见 [`system/PRODUCT.md`](system/PRODUCT.md)「一等公民」。一条信息只有一个权威来源，别处**引用不复制**。

## 仓库结构

顶层恰好 7 项，根另放 `AGENTS.md` 与 `CONTEXT.md`；`.gitignore` 等 git 机制文件由检查门放行。

| 目录 | 放什么 |
| --- | --- |
| `products/` | 一个选题一个目录，全生命周期在内 |
| `assets/` | 跨选题复用的素材 |
| `system/` | 产品设计、规范、目录约定 |
| `scripts/` | 执行引擎：生成、渲染、检查 |
| `.pi/` | harness 单源：`rules/` `skills/` `agents/` |
| `.agents/` | 长期决策记录（`notes/`） |
| `.githooks/` | git hook |

## 流程与 harness

流程是一套固定阶段，末端按交付形态分叉；定义见 [`system/PRODUCT.md`](system/PRODUCT.md)「流程骨架」，约束见 [`.pi/rules/workflow.md`](.pi/rules/workflow.md)。

harness 只有一处作者源：`.pi/{rules,skills,agents}`。不存在生成镜像与同步脚本；改约束从 `.pi/rules/` 改起。归属与修改判断权见 [`.pi/AGENTS.md`](.pi/AGENTS.md)。

## 命令入口

```bash
# 内容管线
uv run --directory scripts content list              # 选题总览
uv run --directory scripts content new "标题"         # 新建选题
uv run --directory scripts content adapt T001 wechat  # 派生渠道草稿
uv run --directory scripts content show T001          # 选题详情
uv run --directory scripts content transition T001-wechat-v1 ready
uv run --directory scripts content validate           # 校验 frontmatter
uv run --directory scripts content preview T001       # 多渠道并排预览

# AI 生成（provider-agnostic，默认火山引擎）
uv run --directory scripts ai generate image --prompt "..." -o out.png
uv run --directory scripts ai generate video --scene "..." --subject "..." -o ./out/
uv run --directory scripts ai extract-lastframe in.mp4 -o frame.png
uv run --directory scripts ai verify in.mp4 --expect-duration 15 --expect-resolution 1080x1920

# 工具
uv run --directory scripts web-fetcher download <url> -o <path>
```

渠道名：`wechat` / `xiaohongshu` / `x` / `douyin`。首次在 `scripts/` 跑 `uv sync`。
Hook: `git config core.hooksPath .githooks`。

## 协作

- **Issue tracker**：Issues 存 GitHub Issues（`Ai-feier/outgiving`），用 `gh` CLI 读写。
- **Triage 标签**：五角色标签，标签字符串即角色名——`needs-triage` / `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`。
- **决策记录**：长期决策与取舍写入 [`.agents/notes/`](.agents/notes/)，三态目录 + 入口约定，引用用相对链接，不建索引。
