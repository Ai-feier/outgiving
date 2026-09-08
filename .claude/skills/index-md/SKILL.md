---
name: index-md
description: >
  通过 _index.md 反向引用体系管理 AI 基础设施和内容资产的可发现性。
  触发：新增/修改 .claude/ 文件后、定期巡检、手动 /index-md [search|update|check]
argument-hint: "[search|update|check]"
---

# _index.md 反向引用管理

## 两层索引

本项目有两套索引体系，本 skill 管理第一层：

| 层 | 位置 | 管理者 | 内容 |
|----|------|--------|------|
| AI 基础设施索引 | `.claude/_index.md` | 本 skill | skills / agents / output-styles / memory 的交叉引用 |
| 内容资产索引 | `.content-index.json` | `content index` CLI | topics / drafts / published / analytics 的程序化索引 |

**本 skill 不管理 `.content-index.json`**——那是 Python CLI 的职责。本 skill 只管理 `.claude/` 下的 AI 资产。

## 四种模式

### 检索（做任何事之前）

1. 读 `.claude/_index.md` → 找到相关 skill / agent
2. 读对应 SKILL.md → 理解工作流和约束
3. 读 `CLAUDE.md` → 理解项目全局约定
4. 确认没有遗漏的 memory（读 `.claude/memory/MEMORY.md`）

### 沉淀（新增/修改 .claude/ 文件后）

1. **去重** — 搜 `.claude/` 全量已有内容，确认新增不重复；重复则合并
2. **合并** — 同一关注点有多个文件时合并，删除冗余，更新 `_index.md`
3. **更新** — 修改了 skill/agent 的触发条件或职责 → 更新 `_index.md` 对应行
4. **废弃** — 标记或删除不再需要的文件，更新所有引用
5. **索引** — 新增文件后必须在 `_index.md` 添加条目

### 检查（手动触发 / reflecting 触发）

```
□ 去重：同一规则是否在多个 skill 中出现
□ 信息密度：是否有大段叙述可压缩为列表/矩阵
□ 死链：_index.md 引用的文件是否存在
□ 索引完整：_index.md 是否覆盖全部 .claude/skills/*/SKILL.md
□ 孤立文件：.claude/ 下是否有未被 _index.md 引用的文件
□ CLAUDE.md 行数：是否超过 200 行
```

```bash
# 列出所有 SKILL.md，对照 _index.md
find .claude/skills -name "SKILL.md" | sort
# 列出所有 agent
find .claude/agents -name "*.md" | sort
# 列出所有 memory
find .claude/memory -name "*.md" -not -name "MEMORY.md" | sort
```

### 维护（持续）

闭环后定期检查 AI 基础设施健康度：

| 检查项 | 规则 |
|--------|------|
| 去重 | 同一规则不出现在 2+ 文件中，重复内容合并到权威源 |
| 密度 | 单个 SKILL.md ≤ 200 行（元知识层 video-craft/reflecting ≤ 250，超限拆分）；优先列表、矩阵、一句话高密度 |
| 引用 | `_index.md` 引用的文件必须存在；新增文件必须被引用 |
| 废弃 | 已不再触发的规则标记或删除 |

## 注意事项

- 只记引用，不复制规则内容到 `_index.md`
- 文件存在才引用，目录变更时修正相对路径
- **沉淀 = 体系维护**：去重 > 合并 > 更新 > 废弃，不盲目追加
- `.content-index.json` 不在此 skill 范围内——用 `content index` 重建
