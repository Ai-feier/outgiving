# Agent 协作

## 调用原则

下发 agent 前自检：prompt 是在替 agent 思考还是在创造条件？
过半内容是「告诉他们怎么做」→ 重写。不给 agent 定义人格，不写「严禁偷懒」，不设「至少 N 次搜索」。
给方向、给约束、给空间。

## 共享文件协议

Agent 间通过**共享文件**通信，不通过对话历史：

| 文件 | 用途 | 最低读取集 |
| ------ | ------ | ----------- |
| `outline.md` | 结构共识 | 所有 agent |
| `style.md` | 写作宪法 | 4 writer |
| gather-expert 产出 | 证据锚点 | brief 作者 + 所有 writer + figure-draftsman |
| figure-draftsman 产出 | `assets/figN.svg` | 所有引用图的 agent |

读取顺序：先 `style.md` → 先论据后论点 → 论据不够标「推测」→ 外部论点挂链接+来源性质。

## 交接点契约

| 交接点 | 上游 | 下游必读 | 格式约束 |
| -------- | ------ | --------- | --------- |
| 研究→选题 | gather-expert 证据锚点 | brief 作者 + 4 writer（最低读取集）+ figure-draftsman（进阶读取集） | 每证据 ≥1 跨谱系锚点；单谱系来源标注「置信度受限」；证据块首行含判定 |
| 选题→大纲 | brief.md 关键信息点 | outline 作者 | 每点一句话可证伪 |
| 大纲→风格 | outline.md | style 作者 | 结构节点标注信息点编号 |
| 风格→写作 | style.md | 4 writer | 写前必须 Read |
| 写作→出图 | brief 视觉规划 + `<!-- fig:N -->` | figure-draftsman | 图服务信息点，路径用相对 topic assets |
| 三元素→收口 | script / visual / rhythm 单元文件（② 自报 + ⑤ 对齐自报） | video-director（收口单元） | 各单元 ⑤ 对齐自报完成后 director 才读取；🔴 → 收口单元门 |
| 视觉设计→资产 | visual.md（②③）+ exec/visual-assets-spec.md | video-director + figure-draftsman + asset-lab.md | IaD 中性表情；分镜线稿标 beat 编号；入库前 asset-lab 去重 |
| 视觉→分镜确认 | 分镜确认门（门记录在 visual 单元 ⑤）+ 分镜图 | video-director（RefImg 门禁） | P0 关键拍分镜图未确认 → 阻塞 director Phase 0 preflight |
| 收口→AI 生成 | exec/ prompt 文件（收口单元 ③ 交付指针；运行单元 ④ `prompt-file:` 引用） | `ai generate video` CLI | 9 要素 prompt + 全局一致性前缀；9:16 竖屏；运行单元 `gate: 是`（成本门：花钱前看请求体） |

## 主会话职责（ai-video 层级链）

层级链模型与写作规格见 `ai-video/DESIGN.md` §2/§3/§6。主会话（操作员）专属职责：

| 职责 | 落点 |
| ------ | ------ |
| 创建/落地中间单元文件（frontmatter + ① 草案，agent 填 ②③④⑤） | 单元文件（goal ③ 单元计划驱动） |
| 写 goal ③ 单元计划（计划单元 + 派发 agent + 顺序 + gate 标注） | goal 单元 ③ |
| 层被替代时标 `superseded_by: l(k+1)`（旧层不改写） | 旧层单元 frontmatter |
| 门记录代写（人经 workbench 批准后落 md） | goal ⑤ / gate 单元 ⑤ `### 门 · …` |
| 中间单元提议新增/删改单元 → 主会话落地 | 单元 ② 假设与未锚 |

## 量化指标对齐

设计阶段同步确认，不一致时 video-director（视频）或 reflecting 深度 2（文本）裁决：

| 指标 | 涉及 agent | 对齐结果 |
| ------ | ----------- | --------- |
| 单拍时长 | script-designer → video-director | 实体≤6s / 纯视觉≤8s / 钩子不限 |
| CF vs V | script ↔ rhythm ↔ visual | CF 归 rhythm（<2 单边约束），V 归 visual（独立管理） |
| 感知组块 | figure-draftsman → 所有引用图 agent | 公众号≤15 / X≤5 / 小红书 3-6 / 抖音≤3 |
| 实体复现 | script ↔ visual ↔ director | 主角≤3拍 / 配角≤5拍 |
| 通道堆叠 | douyin-writer ↔ rhythm | 同期活跃≤2 带显式标注 |
| 认知负荷 | script → rhythm | script 粗估(1-5) ≠ rhythm CL(1.5-2.0) |
| gather-expert 三级措辞 | gather-expert → 所有 writer | 暗示/与…一致/表明；writer 据此决定引用立场 |
| gather-expert FRANQ | gather-expert → 所有 writer | 事实性（✓/✗/不可判）做引用门禁，忠实性（✓/✗/不可判）做来源忠实度检查 |

## 来源标注

所有 agent 引用外部内容标注：日期 + 验证状态（已直接验证/未独立验证/推测）。gather-expert FRANQ 消费见「量化指标对齐」表。

## 平台变化广播

发现平台规则/算法变化 → 1) 修改自己 .md 2) 广播相关 agent 3) 更新 reflecting 审计 4) 下轮精进吸收。

发现通用工具/方法改进 → 判断是否跨 writer 适用 → 若是，写入精进记录并标注 `可广播至: [writer列表]`。
