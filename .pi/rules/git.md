# Git

- 分支：`main` ← `{topic-id}-{描述}`；不在 `main` 上直接编辑内容。
- Commit 格式：`<type>(<scope>): <描述>`，type ∈ `content` / `review` / `publish` / `asset` / `infra` / `fix` / `research`。
- Scope：选题 ID 或 infra 组件名。
- 每个产出后一个 commit；每次状态推进后一个 commit。
- 所有 commit 尾部加 `Co-Authored-By: Claude <noreply@anthropic.com>`。
- Hook 安装：`git config core.hooksPath .githooks`。
- 禁止：commit 二进制 >5MB、force push `main`、commit 敏感信息。
