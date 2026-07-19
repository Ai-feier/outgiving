# 项目约定

## 目录结构

```
topics/T001-<slug>/           # 选题（brief.md + outline.md + style.md + assets/）
platforms/<plat>/T001-<slug>/ # 平台草稿（article.md）
published/YYYY-MM/            # 已发布存档
analytics/                    # 数据分析
scripts/                      # Python CLI
.claude/                      # AI 基础设施（agents/ skills/ rules/ output-styles/）
```

## 命名

| 对象 | 格式 | 示例 |
|------|------|------|
| 选题 ID | `T` + 三位数字 | `T001` |
| 草稿 ID | `{topic}-{platform}-v{rev}` | `T001-wechat-v1` |
| 发布 ID | `{topic}-{platform}-pub` | `T001-wechat-pub` |
| 目录 slug | 中文保留，空格/标点→`-`，≤60 字符 | `T001-ai-xie-zuo` |
| 图片 | `figN.svg` / `figN.excalidraw` | `fig1.svg` |
| 平台值 | `wechat` / `xiaohongshu` / `x` / `douyin` | — |

## Frontmatter

**不手写**，用 `content new` / `content adapt` 创建，`content transition` 推进。

### TopicFM 必填
`id`, `kind`, `topic_id`, `title`, `status`, `created_at`, `updated_at`

### DraftFM 必填
`id`, `kind`, `topic_id`, `parent_id`, `platform`, `revision`, `status`, `title`, `created_at`, `updated_at`

### 纯写作区
`outline.md` / `style.md` / `article.md` 无 frontmatter。

## Agent 文件

- 平级在 `.claude/agents/`，文件名 kebab-case
- ≤500 行，定义自己的规则/方法/分镜
- 不复制 CLAUDE.md 的灵魂信仰

## Git

### 分支
`main` ← `{topic-id}-{描述}`（如 `T001-wechat-draft`）
不在 main 上直接编辑内容文件。

### Commit 格式
```
<type>(<scope>): <描述>
```
Type: `content` / `review` / `publish` / `asset` / `infra` / `fix` / `research`
Scope: 选题 ID 或 infra 组件名

### 时机
每个 agent 产出后一个 commit，状态推进后一个 commit。

### 禁止
- 不 commit 二进制 >5MB
- 不 force push main
- 不 commit 敏感信息
- 所有 commit 尾部加 `Co-Authored-By: Claude <noreply@anthropic.com>`

### Hook
```bash
git config core.hooksPath .githooks
```

## 禁止项

- 不在 agent 文件中复制 CLAUDE.md 灵魂信仰
- 不多个 agent 独立重复调研同一问题
- 正文不用 `../../../` 相对路径引用图片
- 不复制 `.svg` 到平台目录
