# Agent 协作

## 调用原则

下发 agent 前自检：prompt 是在替 agent 思考还是在创造条件？
过半内容是「告诉他们怎么做」→ 重写。不给 agent 定义人格，不写「严禁偷懒」，不设「至少 N 次搜索」。
给方向、给约束、给空间。

## 共享文件协议

Agent 间通过**共享文件**通信，不通过对话历史：

| 文件 | 用途 | 最低读取集 |
|------|------|-----------|
| `outline.md` | 结构共识 | 所有 agent |
| `style.md` | 写作宪法 | 4 writer |
| gather-expert 产出 | 证据锚点 | brief 作者 + 所有 writer + figure-draftsman |
| figure-draftsman 产出 | `assets/figN.svg` | 所有引用图的 agent |

读取顺序：先 `style.md` → 先论据后论点 → 论据不够标「推测」→ 外部论点挂链接+来源性质。

## 交接点契约

| 交接点 | 上游 | 下游必读 | 格式约束 |
|--------|------|---------|---------|
| 研究→选题 | gather-expert 证据锚点 | brief 作者 + 4 writer + figure-draftsman | 每证据 ≥2 跨谱系锚点，证据块首行含判定 |
| 选题→大纲 | brief.md 关键信息点 | outline 作者 | 每点一句话可证伪 |
| 大纲→风格 | outline.md | style 作者 | 结构节点标注信息点编号 |
| 风格→写作 | style.md | 4 writer | 写前必须 Read |
| 写作→出图 | brief 视觉规划 + `<!-- fig:N -->` | figure-draftsman | 图服务信息点，路径用相对 topic assets |
| 三元素→合成 | script-beats / visual-world / rhythm-curve | video-director | 各文件在 director 读取前完成 |

## 量化指标对齐

设计阶段同步确认，不一致时 video-director（视频）或 reflecting 深度 2（文本）裁决：

| 指标 | 涉及 agent | 对齐结果 |
|------|-----------|---------|
| 单拍时长 | script-designer → video-director | 实体≤6s / 纯视觉≤8s / 钩子不限 |
| CF vs V | script ↔ rhythm ↔ visual | CF 归 rhythm，V 归 visual，乘积<4 |
| 感知组块 | figure-draftsman → 所有引用图 agent | 公众号≤15 / X≤5 / 小红书 3-6 / 抖音≤3 |
| 实体复现 | script ↔ visual ↔ director | 主角≤3拍 / 配角≤5拍 |
| 通道堆叠 | douyin-writer ↔ rhythm | 同期活跃≤1 |
| 认知负荷 | script → rhythm | script 粗估(1-5) ≠ rhythm CL(1.5-2.0) |

## 来源标注

所有 agent 引用外部内容标注：日期 + 验证状态（已直接验证/未独立验证/推测）。
gather-expert FRANQ：事实性做引用门禁，忠实性做来源忠实度检查。

## 平台变化广播

发现平台规则/算法变化 → 1) 修改自己 .md 2) 广播相关 agent 3) 更新 reflecting 审计 4) 下轮精进吸收。
