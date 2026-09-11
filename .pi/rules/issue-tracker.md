# Issue tracker

- Issue 与 spec 一律存 GitHub Issues（`Ai-feier/outgiving`），读写一律走 `gh` CLI；不建本地 issue 文件。仓库由 `git remote -v` 推断，`gh` 在克隆内自动解析。
- 外部 PR 不作为需求面，不进 triage 队列。
- GitHub 的 issue 与 PR 共用一个编号空间：裸 `#42` 先用 `gh pr view 42` 解析，失败再 `gh issue view 42`。

| 动作 | 命令 |
| --- | --- |
| 建 | `gh issue create --title "…" --body "…"`（多行用 heredoc） |
| 读 | `gh issue view <n> --comments` |
| 列 | `gh issue list --state open --json number,title,labels` |
| 评论 | `gh issue comment <n> --body "…"` |
| 加/去标签 | `gh issue edit <n> --add-label "…"` / `--remove-label "…"` |
| 关闭 | `gh issue close <n> --comment "…"` |

标签字符串见 [`triage-labels.md`](triage-labels.md)。
