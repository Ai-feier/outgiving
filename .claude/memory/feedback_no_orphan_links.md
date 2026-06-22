---
name: 禁止孤行链接，链接必须行内融入
description: 正文 md 里 [名称](url) 单独占一行是 AI 味最重的一种，必须嵌入句子里
type: feedback
---

正文写作禁止"孤行链接"——`[名称](url)` 单独占一行。链接必须行内融入。

**Why:** 2026-06-22 踩坑——article.md 初稿写完正文后又单独贴了 3 行链接（`[Attention Is All You Need](url)` / `[GPT-3 论文](url)` / `[In-context Learning and Induction Heads](url)`），用户反馈"链接的引入都很突兀"。孤行链接是 AI 生成内容最明显的标记之一。

**How to apply:**
- 行内嵌入：`Google 那篇[《Attention Is All You Need》](url) 把 Transformer 架构摆出来`
- 多链接合并：`Anthropic 两篇：[Building effective agents](url) 讲 loop，[Effective harnesses](url) 讲 harness`
- 卖方来源加立场标注：`注意他们是卖方，你读的时候自己掂量`
- 已写入 `.claude/skills/content-pipeline/SKILL.md` 的「写作风格宪法 · 链接」节
