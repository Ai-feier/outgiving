# Git 与命名约定

> 权威源：`.claude/rules/project/conventions.md`——本文为人读摘要。

## 分支

`main` ← `{topic-id}-{描述}`（如 `T001-wechat-draft`）。**不在 main 上直接编辑内容文件。**

## Commit 格式

```
<type>(<scope>): <描述>
```

- Type：`content` / `review` / `publish` / `asset` / `infra` / `fix` / `research`
- Scope：选题 ID 或 infra 组件名
- 时机：每个 agent 产出后一个 commit，状态推进后一个 commit
- 所有 commit 尾部加 `Co-Authored-By: Claude <noreply@anthropic.com>`
- Hook：`git config core.hooksPath .githooks`（提交前自动 `content validate`）

## 命名

| 对象 | 格式 | 示例 |
|------|------|------|
| 选题 ID | `T` + 三位数字 | `T001` |
| 草稿 ID | `{topic}-{platform}-v{rev}` | `T001-wechat-v1` |
| 发布 ID | `{topic}-{platform}-pub` | `T001-wechat-pub` |
| 目录 slug | 中文保留，空格/标点→`-`，≤60 字符 | `T001-ai-xie-zuo` |
| 图片 | `figN.svg` | `fig1.svg` |
| 平台值 | `wechat` / `xiaohongshu` / `x` / `douyin` | — |

## Frontmatter

**不手写**：`content new` / `content adapt` 创建，`content transition` 推进状态。纯写作区（outline.md / style.md / article.md）无 frontmatter。

## 禁止项

- 不 commit 二进制 >5MB
- 不 force push main
- 不 commit 敏感信息
- 不在 agent 文件中复制 CLAUDE.md 灵魂信仰
- 不多个 agent 独立重复调研同一问题
- 正文不用 `../../../` 相对路径引用图片（用 `assets/figN.svg`）
- 不复制 `.svg` 到平台目录（`.svg` 单源）
