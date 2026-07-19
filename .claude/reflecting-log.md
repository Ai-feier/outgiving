# Reflecting Log

> building-in-public. 每次 reflecting 修改基础设施（agent/skill/CLAUDE.md/rules/）后追加一行。
> 同一 pattern 5 条内 ≥2 次 → 修复无效，升级深度。

| 日期 | 触发源 | 目标 | 问题 | 效果 |
|------|--------|------|------|------|
| 2026-07-19 | T001 三 designer 产出不一致 | ai-video/HUMAN-GATES.md | 缺人机确认门 | 4 门: brief/研究/设计对齐/prompt终审 |
| 2026-07-19 | T001 三 designer 产出不一致 | ai-video/TOGETHER.md | agent 并行缺对齐机制 | 7 节: 共同理解/各自方向/对齐检查/资源追踪/交叉验证/评论/迭代 |
| 2026-07-19 | agent 产出路径混乱 | ai-video/README.md | topics/ vs ai-video/ 边界不清 | 铁律: 视频产出统一 ai-video/projects/TXXX/ |
| 2026-07-19 | 生图无参考图 | ai-video/README.md | 缺参考图铁律 | 铁律 1a/1b: 生图 1-3 web优先 / 生视频 3-7 + 尾帧不计入 |
| 2026-07-19 | 生图确认门被跳过 | ai-video/README.md | 工作流缺生图确认门 | 加入 visual-designer→Seedream 生图确认门 |
| 2026-07-19 | 首张图质量不达标 | visual-designer.md | 艺术肖像≠角色设计稿 | 角色设计稿格式: 多视图+中性+纯色背景 |
| 2026-07-19 | Seedream 无法理解三栏 | visual-designer.md | 缺布局参考图 | 布局参考图策略: 给现成设计稿当模板→单图生成 |
| 2026-07-19 | composite.py 修症状 | visual-designer.md + seedream.py | 拼合是症状, 参考图是根因 | 删除 composite.py, 改为布局参考图 |
| 2026-07-19 | 缺生图适配器 | scripts/src/volcengine/ | 无图像生成能力 | 新增 seedream.py + ImagePrompt/ImageResult |
| 2026-07-19 | 缺参考素材搜索 | .claude/skills/find-ref/ | agent 各自搜索, 无统一流程 | 新增 find-ref skill: P0-P5 来源优先级 |
| 2026-07-19 | ref-images/ 60 张图无索引 | ref-images/_index.md | LLM 无法定位 | _index.md: 七字段表, grep 快速定位 |
| 2026-07-19 | 图片无描述 | IMAGE-DESC-TEMPLATE.md | 其他 agent 不知道图的内容 | 每图配 .md 描述: 来源/特征/用途/质量 |
| 2026-07-19 | 生图生视频参考图数量混用 | ai-video/README.md | 过度标准化 | 拆 1a(生图1-3) + 1b(生视频3-7) |
| 2026-07-19 | coordinator 替 agent 做根因分析 | CLAUDE.md | dispatch prompt 在替 agent 思考 | 协作者自检增加"人在loop中" |
| 2026-07-19 | coordinator 跳过门 2 | 行为修正 | gather-expert 完成后直接下发 designer | 门 2: 必须展示摘要让人确认 |
| 2026-07-19 | agent .md 精进日志臃肿 | .claude/reflecting-log.md | 精进历史堆在操作文件里 | 单文件 reflecting-log.md, agent 只留指针 |
| 2026-07-19 | /reflecting ABC 审视 | visual-designer.md + README.md | 铁律 1a/1b 拆分后 visual-designer 未同步：4 处生图参考图数量仍写 3-7（应为 1-3）；Seedance 上限 ≤4 与 1b 的 3-7 矛盾 | 全修正为 1-3(生图) / 3-7(生视频)；find-ref skill 嵌入 visual-designer 工作流 |
| 2026-07-19 | 用户要求 md 内联图片 | _index.md + ref-sources-*.md + README.md | 参考图清单只有文件名无预览 | 所有 md 图片引用统一 `![]()` 内联；README 新增约定 |
