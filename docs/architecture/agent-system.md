# Agent 系统

> 权威源：`.claude/_index.md` + `.claude/agents/*.md`——本文为人读地图。10 个 agent 平级，通过共享文件协作。

## 角色地图

| Agent | 角色 | 面对的人/物 | 核心 |
|-------|------|------------|------|
| gather-expert | 证据研究员 | 下游 writer | 证据锚定胜过叙事优雅；幽灵引用防护；三级措辞 |
| wechat-writer | 公众号 | 主动坐下的人（三入口） | 2000-4000 字；完读率第一；AI 搜索防御 |
| xiaohongshu-writer | 小红书 | 被撞见 → 背调 → 验证 | 搜索占位优先；审核最严；KOS 意识 |
| x-writer | X | 扫信号的人 + Grok AI | 第一条即完整判断；回复链最高权重；双读者 |
| douyin-writer | 抖音 | 被打断的人 | 两阶段钩子（0.3s 中断 + 3s 落地）；收藏率第一 |
| script-designer | 视频叙事 | 观众的情绪曲线 | 弧线 → 节拍 → PAD；镜头叙事映射；被 AI 双重消费 |
| visual-designer | 视觉世界 | 观众的直觉（眼先于脑） | 六维构建 + 材质 + 锚点体系 + 情绪动作化 |
| rhythm-designer | 时间呼吸 | 观众的身体（心跳呼吸） | 密度 × 认知负荷 × 停顿；节奏-运镜耦合 |
| video-director | 导演合成 | 三设计师的矛盾 | 三元素对位 + 收敛门 + 9 要素 / H3 输出分支 |
| figure-draftsman | 示意图工匠 | 正在读文章的人 | 图是论点的视觉形态；只画支撑论点的图 |

协作者（人）：给方向不给方法——agent 的自主性是第一位。

## 协作模式

- **共享**：五条灵魂信仰 + 第一性原理（CLAUDE.md）。差异在「你面对的人处于什么注意状态」
- **不共享**：写作规则、搜证方法、分镜规则——各 agent 在自己的 `.md` 定义
- **通信**：agent 间通过共享文件（outline.md → style.md → gather-expert 产出 → figN.svg），不通过对话历史
- **交接点契约与量化指标对齐**（单拍时长/CF vs V/感知组块/实体复现等）：`.claude/rules/project/collaboration.md`
- 冲突裁决：视频由 video-director，文本通过 reflecting 深度 2

## 自我进化

- **Harness Engineering**：agent 通过修改自己的 `.md` 定义文件实现进化（文件 = harness code），非修改模型权重
- **reflecting 三层漏斗**：守门自检 → 深度 1 操作层（最小修改 .md）→ 深度 2 设计层（重构规则组 → memory）→ 深度 3 框架层（重定义「你面对的」）→ 系统漏斗（跨 agent 模式）
- 精进记录：各 agent 文件内嵌 + `.claude/reflecting-log.md`（全局）
- 四种 loop 模式：协同反思 / 调研精进 / 一致性审计 / 合成减法（删除优先于新增）

## 资产体系

视觉资产（角色/场景/分镜）由 visual-designer 维护，三个文件：`assets/asset-lab.md`（根清单 + 路由 + 生命周期）+ `assets/taxonomy-registry.md`（受控词汇）+ 类型级子索引（characters-index 等）。

- 生命周期：draft → IaD 检查 → active → deprecated → archived → 90 天可删除
- 命名：`{Type}_{TopicID}[_{StyleTag}]_{EntityName}_{Variant}_v{NN}`（如 `CHR_T002_bleach_Ichigo_canonical_v01.png`）
- 跨题复用：查子索引 → `appears_in_style` 验证 → visual-designer 六维终裁
