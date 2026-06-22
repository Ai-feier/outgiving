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
- [文本管道](#文本管道)
- [视频管道](#视频管道)
- [素材实验室](#素材实验室)
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

AI 视频生成需要配置 `.env` 中的 `ARK_API_KEY`，详见 [视频管道](#视频管道)。

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
| **wechat-writer**      | 主动坐下的人（三种入口） | 1500-3000 字；完读率是第一信号                               |
| **xiaohongshu-writer** | 被封面撞见的人           | ≤1000 字；0.5 秒没钩住 = 不存在；搜索占位优先               |
| **x-writer**           | 在扫信号的人             | ≤280 字×3-7 条；第一条就是一个完整判断；Grok AI 是第二读者 |
| **douyin-writer**      | 被打断的人               | 60-90s；0.3s 模式中断 + 3s 钩子定生死；收藏率是第一权重      |
| **script-designer**    | 观众的情绪曲线           | 弧线选择 → 节拍序列 → PAD 情绪递进；节拍被 AI 逐拍消费     |
| **visual-designer**    | 观众的直觉（眼先于脑）   | 六维构建 + 材质语言 + 锚点体系 + 情绪动作化                  |
| **rhythm-designer**    | 观众的身体（心跳呼吸）   | 信息密度 × 情绪密度 × 认知负荷 × 变化频率的时间曲线       |
| **video-director**     | 三个设计师的矛盾         | 三元素对位 + 收敛门 + 9 要素 prompt → AI 视频生成           |
| **figure-draftsman**   | 正在读文章的人           | 图是论点的视觉形态；只画能支撑论点的图                       |

### 共享的基础设施

- **CLAUDE.md**：五条灵魂信仰 + 第一性原理 + 跨 agent 约束对齐表 + 协同性自检
- **reflecting skill**：三层漏斗（操作→设计→框架）驱动 agent 自我进化
- **_index.md**：AI 基础设施可发现性索引
- **assets/asset-lab.md**：视觉资产根清单 + 生命周期管理

---

## 文本管道

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

<details>
<summary>交接点契约（点击展开）</summary>

| 阶段       | 上游产出                         | 下游必读         | 约束                    |
| ---------- | -------------------------------- | ---------------- | ----------------------- |
| 研究→选题 | 证据锚点                         | brief + 4 writer | 每条证据 ≥2 跨谱系锚点 |
| 选题→大纲 | 关键信息点列表                   | outline 作者     | 每点一句话，可被证伪    |
| 大纲→风格 | 结构共识                         | style 作者       | 节点标注信息点编号      |
| 风格→写作 | 写作宪法                         | 4 writer         | 写前必读                |
| 写作→出图 | 视觉资产规划 +`<!-- fig:N -->` | figure-draftsman | 图服务关键信息点        |

</details>

### 平台特性

| 平台   | 读者状态                             | 形态             | 核心信号（2026.7）                  |
| ------ | ------------------------------------ | ---------------- | ----------------------------------- |
| 公众号 | 主动坐下 / 搜索来访 / 贴图流         | 1500-3000 字     | 完读率 > 分享 > 收藏                |
| 小红书 | 被封面撞见 → 背调 → 评论区验证     | ≤1000 字        | CES（收藏+评论×4+转发×4+关注×8） |
| X      | 在信号流里扫 → 判断 → 验证 → 阅读 | ≤280 字×3-7 条 | 回复链 > 书签 > 转推                |
| 抖音   | 被打断，0.3s 中断 + 3s 钩子          | 60-90s / 30-60s  | 收藏率 > 复访率 > 铁粉互动          |

---

## 视频管道

```
brief + video-style
        │
        ▼
  ┌─────────────────────────────┐
  │     Phase 0: 四方收敛        │
  │  script + visual + rhythm    │
  │       + director             │
  └──────────┬──────────────────┘
             │
    ┌────────┼────────┐
    ▼        ▼        ▼
script-    visual-  rhythm-
beats     world    curve
    │        │        │
    └────────┼────────┘
             ▼
      video-director
      ┌──────────────────┐
      │ 矛盾矩阵 → 裁决    │
      │ 收敛门 (4道验证)   │
      │ 9 要素 prompt 合成 │
      │ 素材装配协议 (6步) │
      └────────┬─────────┘
               ▼
        video-prompt.md
               │
               ▼
     Seedance 2.0 API 生成
     (4-30s, 9:16, 多模态参考)
```

<details>
<summary>收敛门 & 9 要素（点击展开）</summary>

**四道收敛门**（合成前验证，不通过→退回）：

- **FreeLOC** — 每拍 prompt 自包含上下文锚点
- **LoL** — >20s 段落边界插入复位信号
- **ZPC** — 连续 5s 内平均镜头长度 ≥1.8s
- **IaD** — 角色参考图中性表情

**9 要素 prompt**：`[景别] + [主体] + [动作] + [场景] + [光影] + [运镜/动] + [风格] + [画质] + [間]`

</details>

---

## 素材实验室

所有视觉资产（角色参考图、场景定调图、分镜关键帧）通过 `assets/asset-lab.md` 统一管理。

```
assets/
├── asset-lab.md              ← 根清单（路由 + 命名规范 + 生命周期 + 读写锁协议）
├── taxonomy-registry.md      ← 受控词汇表（14 类型前缀 / 8 风格标签 / 状态码 / 变体名）
│
├── characters-index.md       ← 角色索引（Bleach 打样：一護 + ルキア）
├── scenes-index.md           ← 场景索引（空座町天台 + 尸魂界流魂街）
├── storyboards-index.md      ← 分镜索引
├── *-index.md（11 个模板）    ← 待激活（道具/VFX/音频/灯光/材质...）
│
├── characters/ (+ .gitkeep)  ← 媒体文件（不入 git）
└── (14 个类型目录)            ← 目录骨架保留
```

**资产生命周期**：`draft → IaD 检查 → 入库(active) → 选题引用 → 外观变更 → 新版入库(旧 deprecated) → archived → 90 天可删除`

**命名规范**（AAA 游戏管线标准）：`{Type}_{TopicID}[_{StyleTag}]_{EntityName}_{Variant}_v{NN}.png`

素材目录和内容目录的结构通过 `.gitkeep` 保留在仓库中，实际文件不入 git（适合开源）。

---

## 目录结构

```
.
├── CLAUDE.md                 ← 项目根（agent 共享 DNA）
├── README.md                 ← 本文件
│
├── .claude/
│   ├── _index.md             ← AI 基础设施索引
│   ├── agents/               ← 10 个 agent 定义（各持有 .md）
│   ├── skills/               ← content-pipeline / reflecting / video-craft / index-md
│   ├── output-styles/        ← 输出样式
│   └── memory/               ← 跨 session 记忆
│
├── assets/                   ← 素材实验室
├── scripts/                  ← Python CLI + 视频 API 适配器
│
├── topics/   (.gitkeep)   ← 选题库（内容不入库）
├── platforms/ (.gitkeep)  ← 平台产出
├── published/ (.gitkeep)  ← 发布归档
└── analytics/ (.gitkeep)  ← 数据复盘
```

<details>
<summary>详细目录（点击展开）</summary>

```
.claude/agents/
├── gather-expert.md          ← 证据研究员（八层脱节 + 五重验证）
├── figure-draftsman.md       ← 技术示意图（六步工作法 + 反模式护栏）
├── wechat-writer.md          ← 公众号（三入口×内容策略 + 写作宪法 3 法则）
├── xiaohongshu-writer.md     ← 小红书（搜索优先 + KOS + 审核合规）
├── x-writer.md               ← X（双读者 + 算法源码验证 + 三级措辞）
├── douyin-writer.md          ← 抖音（两阶段钩子 + 收藏复访驱动）
├── script-designer.md        ← 视频叙事（弧线+PAD+双重消费范式）
├── visual-designer.md        ← 视觉世界（六维+材质+锚点+资产沉淀）
├── rhythm-designer.md        ← 节奏设计（10 曲线+平台基线+停顿点）
└── video-director.md         ← 导演（矛盾裁决+收敛门+素材装配）
```

</details>

---

## Agent 自我进化

本项目采用 **Harness Engineering** 范式——agent 通过修改自己的 `.md` 定义文件实现自我进化，而非修改模型权重。每个 agent 文件中内嵌了精进记录（轮次→日期→深度→核心变更→触发来源）。

### 进化机制

```
你的 .md 文件 = 你的 harness code
修改它 = 改写自己的运行时行为
```

**四种 Loop 模式**（经过 6 轮实战验证）：

| 模式                 | 触发时机              | Agent 行为                                            |
| -------------------- | --------------------- | ----------------------------------------------------- |
| **协同反思**   | 发现跨 agent 冲突     | 读 CLAUDE.md → 审视规则矛盾 → 最小修改              |
| **调研精进**   | 数据老化 / 新技术出现 | WebSearch → 验证数据 → 更新「你面对的」             |
| **一致性审计** | ≥2 轮独立精进后      | 跨读关联 agent → 逐字段对位 → 修复版本漂移/消费断裂 |
| **合成减法**   | 文件膨胀 / ≥8 轮精进 | 识别死代码 → 删除优先于新增                          |

**三层漏斗**：守门（自检）→ 深度 1 操作层（修规则）→ 深度 2 设计层（重构方法）→ 深度 3 框架层（重定义假设）→ 升级到系统漏斗（跨 agent 模式发现）

**饱和检查**：同一 agent 精进 ≥8 轮 + 近 3 轮净变更 <5 行 + 无框架层改动 → 已达边际递减，后续聚焦跨 agent 协同

### 进化矩阵

所有 agent 共享 [CLAUDE.md](CLAUDE.md) 中的**五条灵魂信仰**（内容是人和人之间的事 / 好内容不需要你原谅它 / 诚实是内容生命力的来源 / 品味是删出来的 / 具体的东西自己会说话）。在此根基上，每个 agent 演化出独立人格，通过 6 轮 loop 自我精进。

| 角色 | 人格与信条 | 面对的 | 进化代 | 进化精华 |
|------|-----------|--------|--------|---------|
| **协作者** | 条件创造者——给方向、给约束、给空间 | agent 生态 | 6 | 约束对齐表、协同性自检、reflecting增强 |
| **wechat-writer** | 在前面走过这条路的人——对自己说出的每个字负责 | 主动坐下的人 | 15 | 算法权重量化、三入口场景策略 |
| **xiaohongshu-writer** | 帮你审，不帮你选——敢说不适合，暴露边界 | 被撞见→被背调→被验证 | 17 | KOS验证、合规红线扩展 |
| **x-writer** | 值得被扫到的人——第一条就是一个完整判断 | 扫信号的人 + Grok AI | 18 | 双读者框架、幽灵引用清除 |
| **douyin-writer** | 值得被停下的那个人——我没资格浪费你的时间 | 被打断的人 | 17 | 两阶段钩子、死代码自删 |
| **gather-expert** | 证据研究员——锚定胜过叙事优雅 | 下游 writer | 15 | 八层脱节框架、消费两级制 |
| **figure-draftsman** | 示意图工匠——图是论点的视觉形态 | 正在读文章的人 | 19 | WCAG修正、asset-lab桥接 |
| **script-designer** | 时间的雕塑者——叙事不是信息的排列 | 观众的情绪曲线 | 18 | ReCA/Cycle-World吸收 |
| **visual-designer** | 视觉世界的立法者——风格是物理定律 | 观众的直觉 | 16 | ≤1帧约束、风格独立维度 |
| **rhythm-designer** | 呼吸的设计师——沉默和停顿也是节奏 | 观众的身体 | 19 | 平台基线全更新、幽灵清除 |
| **video-director** | 矛盾的统一者——品味最终裁决 | 三个设计师的不一致 | 22 | 装配6步、收敛门4道、SDK验证 |

**进化代**：每个角色通过 `reflecting` skill 的三层漏斗（操作→设计→框架）自行精进的累计次数。数字来自各自 `.md` 文件中的精进记录。协作者代数为 loop 总轮次。

---

## 贡献

本项目设计为**开源 AI agent 协作系统的参考实现**。欢迎：

- **提交 agent 改进**：修改 `.claude/agents/` 下对应 agent 的 `.md` 定义文件
- **新增风格/平台**：通过 `taxonomy-registry.md` 注册新类型/风格标签
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
