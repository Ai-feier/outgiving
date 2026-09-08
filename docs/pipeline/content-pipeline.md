# 文本内容管线

> 权威源：`.claude/skills/content-pipeline/SKILL.md` + `.claude/rules/project/workflow.md`——本文为人读摘要。

## 管线全景

```
选题 → gather-expert 研究 → brief → outline → style
  → 4 writer 并行（wechat/xiaohongshu/x/douyin）
  → figure-draftsman 出图 → validate + preview → human review
```

研究交给 gather-expert，出图交给 figure-draftsman，平台改写给对应 writer——不自己代劳。

## 数据模型

| kind | 路径 | ID 示例 | 状态机 |
|------|------|--------|--------|
| `topic` | `topics/T001-<slug>/brief.md` | `T001` | inbox→briefing→outlined→adapting→archived |
| `draft` | `platforms/<plat>/T001-<slug>/` | `T001-wechat-v1` | draft→reviewing→ready→scheduled→published→retired |
| `published` | `published/YYYY-MM/` | `T001-wechat-pub` | live→analyzing→closed |
| `analytics` | `analytics/` | `T001-review` | pending→t+3→t+7→final |

纯写作区（outline.md / style.md / article.md）无 frontmatter。父子由 `parent_id` 指向。

## 四平台契约

| 平台 | 读者状态 | 篇幅 | 钩子位置 | 核心信号（2026） |
|------|---------|------|---------|-----------------|
| 公众号 | 三入口：推荐流刷到坐下 / 搜索主动来访 / 贴图流进主页 | 2000-4000 字 | 前 3 句 | 完读率第一 |
| 小红书 | 被封面撞见 → 背调 → 评论区验证 | 800-1500 字 | 封面+首句 | CES；0.5s 没钩住 = 不存在 |
| X | 在信号流扫 → 判断 → 验证 | 短线程 3-7 条 / 长文 ≤4000 字 | 第一条 | 回复链最高权重 |
| 抖音 | 被打断，准备划走 | 60-90s / 知识型 30-60s | 前 3 秒 | 收藏率第一 |

感知组块上限（图）：公众号 ≤15 / X ≤5 / 小红书 3-6 / 抖音 ≤3（figure-draftsman 定义计数规则）。

## 交接点（人读版）

| 阶段 | 上游产出 | 下游 | 关键约束 |
|------|---------|------|---------|
| 研究→选题 | 证据锚点（判定行 + FRANQ） | brief 作者 + 4 writer | 证据 ≥1 跨谱系锚点；判定 3 秒可执行 |
| 选题→大纲 | 关键信息点列表 | outline 作者 | 每点一句话，可证伪 |
| 大纲→风格 | 结构共识 | style 作者 | 节点标注信息点编号 |
| 风格→写作 | style.md 写作宪法 | 4 writer | 写前必读 |
| 写作→出图 | 视觉资产规划 + `<!-- fig:N -->` 标记 | figure-draftsman | 图服务关键信息点；路径用 topic assets |

## 操作要点

- frontmatter 不手写：`content new` / `content adapt` 创建，`content transition` 推进状态
- 图片 `![](assets/figN.svg)`，不用 `../../../` 相对路径；`.svg` 单源
- 图不是配图——图和文字是同一个论点的两种形态，brief 阶段就定好
- 正文改完立刻 `validate` + `preview`，不攒到最后

## 共享写作宪法（摘要）

所有平台通用：一行一事、拒绝套话开头、链接行内融入、来源诚实标注、金句不连排。全文见 content-pipeline skill「写作风格宪法」；各平台专属宪法见 `.claude/agents/<平台>-writer.md`。选题级 `style.md` 依共享宪法实例化。
