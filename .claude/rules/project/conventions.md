# 项目约定

## 目录结构

```
topics/T001-<slug>/           # 选题（brief.md + outline.md + style.md + assets/）
platforms/<plat>/T001-<slug>/ # 平台草稿（article.md）
published/YYYY-MM/            # 已发布存档
analytics/                    # 数据分析
scripts/                      # Python CLI
ai-video/                     # AI 视频项目（projects/TXXX/ + gates/ + assets/）
.claude/                      # AI 基础设施（agents/ skills/ rules/ output-styles/）
```

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

## 视觉资产

### 参考资产格式

参考资产（角色设计稿/场景参考图/布局模板）的尺寸比例由**内容布局需求**决定，不由最终产出格式决定。

| 资产类型 | 推荐比例 | 理由 |
|---------|---------|------|
| 多视图合成帧（三栏/四栏角色设计稿） | 横版 16:9 或 3:2 | 多列并排需要宽度 |
| 单角色肖像/正面 | 竖版 3:4 可 | 单视图无并排需求 |
| 场景参考 | 保留原图比例 | 裁剪会丢失空间信息 |
| 布局模板 | 横版（和它服务的多视图资产同比例） | 多视图布局需宽度，不因最终视频是 9:16 就将布局模板设为竖屏 |

铁律：**不因为「最终视频是 9:16」就把参考资产都设成 9:16。** 参考资产和最终产出是两类东西。

### 图片引用

正文引用 `![](assets/figN.svg)`，不用 `../../../` 相对路径。`.svg` 单源。

## 禁止项

- 不在 agent 文件中复制 CLAUDE.md 灵魂信仰
- 不多个 agent 独立重复调研同一问题
- 正文不用 `../../../` 相对路径引用图片
- 不复制 `.svg` 到平台目录
