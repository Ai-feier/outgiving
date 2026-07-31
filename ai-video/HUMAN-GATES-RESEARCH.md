# 确认门研究基础 — 创意管线中的人机协作决策模式

> 补充而非替代 `HUMAN-GATES.md`。后者是门的具体设计，本文件是设计背后的研究证据。
> 每条发现标注来源 + 对我们管线的具体启示。

---

## 一、七个最关键的研究发现

### 发现 1：VFX/动画管线中，导演时间是限量资源

**来源**：FXiation Digitals — "The Approval Stack"；华盛顿大学动画 Capstone 四金律。

**发现**：专业动画/VFX 管线使用 **三层审批堆叠**（Internal QC → Supervisor Review → Director Review）。导演只看第三层，前两层是部门级把关。到导演手上时，技术问题已过滤，导演仅判断故事、表演、叙事契合度。

**理由**：导演时间是整个产线最贵的资源。允许导演看未经过滤的原始工作 → 管线退化为"导演一个人审所有东西"。

**对我们管线的启示**：
- 管线中的"人"（协作者）是导演角色。他应该只看 **agent 已经对齐过的矛盾**，不读原始三设计文件。
- `HUMAN-GATES.md` 的「门 3 — 设计对齐」正是这个模式：agent 先提取矛盾矩阵，人只裁决 ≤3 个最尖锐的矛盾。人读的是摘要，不是原始设计文档。
- **遵守门槛**：送给人看的设计矛盾必须是 agent 确认无法自动解决的。agent 能自己对齐的，不要让人看。

---

### 发现 2：游戏开发的里程碑门禁有明确的客观标准

**来源**：Packt 游戏生产流程；NextMars — "Concept-to-Production Milestone Gates"；Paperform 签收表单。

**发现**：游戏开发的每个里程碑（Pre-Alpha / Alpha / Beta / Gold）有 **明确的进入和退出标准**。例如 Alpha = feature-complete（功能完整），之后禁止加新功能。里程碑验收基于 **客观指标**（功能是否实现、Bug 密度是否达标）而非主观判断。

**关键设计原则**：
- 发布商有固定的审核窗口（如 5 个工作日）
- 被拒时必须提供具体理由（不可用"sole discretion"模糊拒绝）
- 每次提交包含标准包（构建+报告+演示视频）

**对我们管线的启示**：
- 每个确认门需要 **明确的进入条件**（什么算"准备好了给人看"）和 **退出标准**（什么算"通过"）。
- Agent 提交给人审核时，应有标准格式包：矛盾摘要 + 每个选项的推理 + 不选择的后果。
- 被拒时 agent 要能理解具体原因并迭代，而不是重头再来。

---

### 发现 3："Approval Before Action" 和 "Review After Action" 适用不同场景——错误代价决定模式

**来源**：Conductor OSS 文档；AgentsKit agents-playbook；port.io blog。

**发现**：两种模式不可互相替代：

| 维度 | Approval Before Action（门禁） | Review After Action（审计） |
|------|------|------|
| 执行 | 阻塞，等人类批准 | 立即执行，事后审核 |
| 人类角色 | 把关者/授权者 | 审计者/策略设计者 |
| 适用场景 | 不可逆/高成本操作 | 高频/中等风险操作 |
| 可扩展性 | 受限于人类带宽 | 高度可扩展 |
| 陷阱 | 审核疲劳→人开始无脑点通过 | 未定义升级阈值→失控 |

**关键原则**：同一管线的不同节点可混用两种模式。LangGraph 的生产实践是：低风险代理节点用 review-after（快速通过），高风险节点（DELETE / 发邮件 / 花钱）拦截为 approval-before。

**对我们管线的启示**：
- 视频管线中的 **credit 消耗** 类比"花钱"——生成调用是不可逆的资源消耗 → 最终生成调用前必须是 **Approval Before Action**（`HUMAN-GATES.md` 门 4 准确）。
- 设计阶段（script / visual / rhythm 产出）是低成本的，适合 **Review After Action**——agent 先生成，人再对齐。但门 3 的矛盾矩阵必须在合成前确认，因为矛盾累积后的修复成本高。
- **混合模式**：门 3 的"设计对齐"是 approval-before（合成前必须确认），但设计阶段内部的 exploration（如 visual-designer 出多版参考图）是 review-after。

---

### 发现 4：三个"确认门"是 AI 视频工具实践中的共识

**来源**：Lemonlight 四门模型；Gisteo 四门模型；dev.to "Stop AI Video Pipelines Before a Bad Render Gets Expensive"；上海国际电影节 AI 片场观察报告。

**发现**：五家独立来源的四门/五门模型高度一致。核心门禁重合点为：

| 门 | Lemonlight | Gisteo | dev.to 分析 | 上海电影节报告 |
|---|---|---|---|---|
| 1 | Strategy & Brief | Positioning & Message | Direction (hook+script) | 剧本/概念确定 |
| 2 | Script & Storyboard | Script & Voice | Visual Plan | 视觉风格确定 |
| 3 | Visual Review | Brand Taste | Timing | 技术一致性检查 |
| 4 | Final QC | Legal & Business | Final Preview | 终审交付 |

**关键发现**：所有来源都强调 **门 2（视觉计划）是最有价值的门**——在这个节点确认风格、构图、场景列表，能防止 80% 的后期重做。对应我们管线的视觉设计阶段（visual-world.md + visual-assets-spec.md）。

**门 1（Brief）** 是所有来源列出的第一个门。不在此处确认方向，后面全错。

**对我们管线的启示**：
- `HUMAN-GATES.md` 的四个门（Brief → Research → 设计对齐 → Prompt 终审）与行业共识基本一致，不需要增减门数。
- 需要加强的是 **门 2（Research）**——行业共识没有"研究门"这个节点。我们的独特性在于：gather-expert 产出本身就是"研究结论"，需要在设计开始前被人确认。这是我们的管线特征（先研究后设计）带来的新需求。

---

### 发现 5：LangGraph 的 interrupt 原语是 agent 管线 HITL 的最佳参考实现

**来源**：LangChain HITL 文档；Conductor OSS 文档；dev.to "Enhancing Multi-Agent Orchestration for Enterprise Production" (2026)。

**发现**：LangGraph 的 `interrupt()` 原语是当前最成熟的 agent 管线 human-in-the-loop 实现。关键设计：

1. **Checkpoint-and-resume**：执行到 interrupt 时，状态被持久化（SQLite/Postgres/Redis），恢复时从精确断点继续，而非从头重跑
2. **四种人类反馈类型**：Approve / Reject / Edit / Respond（覆盖从"放行"到"直接修改"的粒度）
3. **静态 + 动态断点**：静态（高风险节点预配置）vs 动态（运行时条件触发，如 amount > limit）
4. **可配置超时**：人类未响应时的默认动作（通常拒绝而非通过，防止审核疲劳）

**对我们管线的启示**：
- 我们不需要实现 LangGraph 级别的状态管理（我们的管线不是 agent 框架），但 **checkpoint-and-resume 理念** 很有价值：如果人在门 2 拒绝了某个断言，agent 应能记住该决策并在后续设计中不再使用该断言。
- **四种反馈类型** 可以简化：我们的门不需要 Edit（改设计是 agent 的工作），但需要 Approve / Reject / Redirect（人给出新方向）。
- **超时默认拒绝**：如果人在规定时间内未响应，门禁默认阻断（"你不说行，就是不行"）。这是审核疲劳的防御设计——如果人知道不回应等于默认拒绝，他们会在真正重要的事上回应。

---

### 发现 6：决策疲劳是管线的隐形杀手——格式设计直接影响决策质量

**来源**：Yahoo Tech — "One Best + Two Backups" prompt 策略；Stack Overflow Blog (May 2026) — "Coding agents are giving everyone decision fatigue"；BizWest — "The ROI of Live"（三选项规则）；Scientific Reports (2026) — AI 辅助格式对决策效率的影响。

**发现**：多个来源汇集到一个核心模式——**数量越少、结构越好，决策质量越高**：

- **80% 的 AI 生成内容在终稿前被编辑过**（Stack Overflow），意味着每一个输出都消耗一次人类的判断力
- **瓶颈从打字速度变成了决策质量**。AI 不减少决策量，它增加决策量——除非你主动压缩选项
- **呈现格式影响 11.8% 的认知负荷**（Scientific Reports 2026）：bullet-point 比 paragraph 格式降低 11.8% 的认知负荷
- **"一个最佳 + 两个备选"**是最高效的决策格式（Yahoo Tech）：
  1. AI 推荐唯一最佳选项
  2. 解释为什么它最佳
  3. 列出恰好两个备选，标注何时选它们

**对人类决策者呈现信息的最佳实践**（汇总多来源）：

| 原则 | 做法 | 来源 |
|------|------|------|
| 上限 3 个选项 | 任何问题不超过 3 个选择 | BizWest, Yahoo Tech |
| 推荐+解释 | 先推荐一个，解释理由 | Yahoo Tech |
| 备选有条件 | 备选标注何时使用 | Yahoo Tech |
| 结构化优先 | bullet-point > paragraph | Scientific Reports |
| 必要信息显式 | 折叠非关键信息 | 多来源共识 |
| 决策前先判断 | "这是不是必须现在决定的事" | 多来源共识 |

**对我们管线的启示**：
- 门 3（设计对齐）的每个决策点，agent 呈现不超过 3 个选项——`HUMAN-GATES.md` 正确做到了。但应加上 **推荐+解释**：不要给四个节奏定调选项让人选——agent 先推荐一个并解释为什么，人可以选择接受或选另一个。
- 每个门的人看的东西应该不超过 **一页**。如果 agent 需要人看超过一页的东西，说明它没有做好过滤。
- 可选 vs 必选字段分离——有些信息是辅助参考（如"agent 搜索时用过的来源列表"），有些是必须决策的（如"资源杠杆选哪两个"）。前者折叠，后者显式。

---

### 发现 7：最危险的模式不是"agent 全自动"，而是"人批准了但没真的理解"

**来源**：port.io 的文章 "Human in the loop: Do you need it at every step?"；Conductor OSS "The Scalability Trap"。

**发现**：**审核疲劳（Alert Fatigue）** 是 approval-before-action 模式的最大风险。当人需要审核的数量太大：

> "The queue grows. The human begins clicking through. They stop reading the JSON payloads. They click 'Approve' because the backlog is piling up."

这导致一个危险状态：**人在形式上批准了，但实质上没有审核**。更危险的是——这种情况下人在事后会误以为"我已经看过了"。

**防御机制**：
1. **限制每轮审核量**：LangGraph 动态断点只触发最关键的决策，不触发常规操作
2. **超时默认拒绝**：不响应 = 不通过，迫使人在真重要的节点上花时间
3. **审核深度 > 审核频率**：人一次性做好一个战略决策，比频繁做战术决策更有价值

**对我们管线的启示**：
- `HUMAN-GATES.md` 已经设计为 **少量但关键的门**（4 个）。这是正确的——宁可让人做 4 次重要的决策，也不要让人做 20 次微决策。
- 每个门需要的决策数应该 **不超过 5 项**。门 4 目前有 8 项 + 2 个开放问题——考虑压缩为 5 项必选 + 2 项折叠。
- 人的默认响应应该是 **"拒绝/不通过"**，而不是"通过"。设计门的时候默认状态是"人没看 = 不做"。

---

## 二、对我们管线最适用的模式总结

### 应该采用的模式

| 模式 | 在管线中的应用 | 证据来源 |
|------|---------------|---------|
| **三层审批堆叠** | agent 内部对齐 → agent 间矛盾摘要 → 人裁决 ≤3 个矛盾 | 发现 1 |
| **里程碑门禁 + 客观退出标准** | 每个门定义进入条件（什么算"准备好了"）和退出标准（什么算"通过了"） | 发现 2 |
| **混合 HITL 模式** | 探索阶段 review-after，资源消耗阶段 approval-before | 发现 3 |
| **三选项原则** | 每个决策点 ≤3 个选项，agent 推荐一个并解释 | 发现 6 |
| **超时默认阻断** | 人不回应 = 不通过，防止审核疲劳 | 发现 5, 7 |
| **四种反馈类型（简化版）** | Approve / Reject / Redirect / Defer to human-defined alternative | 发现 5 |

### 应该避免的模式

| 模式 | 为什么避免 | 替代方案 |
|------|-----------|---------|
| **每步都需要人批准** | 导致审核疲劳，最终实质无人审核 | 只有不可逆节点（生成调用）才 approval-before |
| **给人看原始设计文档** | 信息过载，人无法聚焦关键矛盾 | agent 先产出矛盾摘要 |
| **无上限的选项数** | 决策疲劳，降低决策质量 | ≤3 选项 + 折叠更多 |
| **默认通过** | 人在无意识状态下批准了不应该批准的事 | 默认不通过，人主动选择通过 |

---

## 三、确认门设计原则（10 条）

基于以上研究，以下是确认门设计的核心原则。每条的来源标注在末尾。

### 原则 1：只有不可逆的节点才需要 Approval Before Action
探索、搜索、内部对齐→ review-after。资源消耗（生成调用 / 发布）→ approval-before。把人脑放在必须判断的地方，不要放在可以 audit 的地方。 [发现 3, 5]

### 原则 2：给人看的必须是摘要，不是原始文档
信息经过三层过滤才送到人手上：agent 内部对齐 → agent 间矛盾提取 → 人裁决。人应该看"script 和 rhythm 在 B4 拍有冲突，两个方案如下"，而不是读原始 script-beats.md + rhythm-curve.md。 [发现 1]

### 原则 3：每个决策点不超过 3 个选项
三个选项对应：推荐项 / 备选 A / 备选 B。AI 推荐一个并解释理由。人的工作是确认或否定推荐，而非从无结构中构建答案。 [发现 6]

### 原则 4：超时默认阻断
如果人在规定时间内未响应，等效于不通过。"你不说行，就是不行"——这个默认值迫使人只在真正的关键节点回应，防止审核疲劳导致的虚假通过。 [发现 5, 7]

### 原则 5：每个门必须有明确的进入条件和退出标准
进入条件 = 什么算"准备好了可以给人看"。退出标准 = 什么算"这个门通过了"。没有这两个，门是虚的——agent 不知道什么时候该提交给人，人不知道什么时候该说"过了"。 [发现 2]

### 原则 6：否决必须附带具体理由
人拒绝一个选项时，必须给出具体原因（而非"不行"）。agent 才能基于理由迭代。这与游戏开发出版商的"拒绝必须基于具体规格"一致。 [发现 2]

### 原则 7：战略决策前置，战术决策后置
在管线中，影响范围大的决策（Brief / 设计对齐）放在前面做，影响范围小的决策（Prompt 措辞）放在后面做。四条原则支撑：决策成本随时间递增（越晚改越贵）；战略定调后战术自动收敛；人一次好的战略决策抵十次好的战术决策；上层做错下层做得再好也是错的。 [发现 4, 7]

### 原则 8：参考图是视觉确认的最小可行单元
在人确认"场景风格对不对"时，不应该让人看 prompt——应该让人看参考图/风格帧。视觉的东西用视觉确认。这在视觉计划门（门 3）和 prompt 终审门（门 4）都适用。 [发现 4]

### 原则 9：设计冲突优先让人裁决方向，而非具体细节
当 script 和 rhythm 在拍数/拍边界上冲突时，人只需要决定"以哪份设计为准"，不需要在"B4 应该是 3s 还是 7s"上逐条决策。方向一致后，具体对齐由 agent 执行。 [发现 1, 6]

### 原则 10：门的数量原则——尽可能少，但足够覆盖不可逆节点
四个门（Brief → Research → 设计对齐 → Prompt 终审）是下限。少于四个会遗漏不可逆决策点；多于四个会导致审核疲劳。每个门保留下来的标准是：如果这个门不存在，最坏情况是否可回滚？如果不可回滚，保留。 [发现 4, 7]

---

## 四、引用来源

1. FXiation Digitals — "The Approval Stack: Why VFX Supervisors Gate the Director" (https://fxiationdigitals.com/blog/approval-stack-vfx-supervisors-director/)
2. 华盛顿大学 CSE 460 — "Four Golden Rules for Animation Capstone" (https://courses.cs.washington.edu/courses/cse460/)
3. Packt — 游戏生产流程里程碑结构 (https://packt-plus-non-live.prod.packtpub.com/)
4. NextMars — "Concept-to-Production Milestone Gates" (https://www.nextmars.com/post/2026-production-directors-concept-to-production-milestone-gates-202603261900)
5. LangChain HITL 文档 (https://docs.langchain.com/oss/python/langchain/frontend/human-in-the-loop)
6. Conductor OSS — "Human-in-the-Loop: Durable Execution for workflows and agents" (https://docs.conductor-oss.org/devguide/ai/human-in-the-loop.html)
7. port.io — "Human in the loop: Do you need it at every step?" (https://www.port.io/blog/human-in-the-loop-for-ai-coding-agents)
8. AgentsKit agents-playbook — HITL 模式比较 (https://github.com/AgentsKit-io/agents-playbook)
9. Lemonlight — "Human-in-the-Loop AI Video Production" (https://www.lemonlight.com/blog/human-in-the-loop-ai-video-production/)
10. Gisteo — "Human-in-the-Loop AI Video Production" (https://gisteo.com/blogs/ai-videos/human-in-the-loop-ai-video-production/)
11. dev.to — "Stop AI Video Pipelines Before a Bad Render Gets Expensive" (https://dev.to/woshiliyana/stop-ai-video-pipelines-before-a-bad-render-gets-expensive-1p9m)
12. 上海国际电影节 — "AI 片场观察报告" (https://www.itsdw.cn/news/12059.html)
13. Yahoo Tech — "I stopped asking AI to brainstorm" prompt 策略 (https://tech.yahoo.com/ai/chatgpt/articles/stopped-asking-ai-brainstorm-only-071500838.html)
14. Stack Overflow Blog (May 2026) — "Coding agents are giving everyone decision fatigue" (https://stackoverflow.blog/2026/05/21/coding-agents-are-giving-everyone-decision-fatigue/)
15. BizWest — "The ROI of Live: Outsmarting decision fatigue" (https://bizwest.com/2026/01/26/the-roi-of-live-outsmarting-decision-fatigue/)
16. Scientific Reports (2026) — "Effects of AI-assisted review presentation formats on consumer decision-making efficiency" (https://link.springer.com/article/10.1038/s41598-026-45101-3)

---

*本文件由 gather-expert 基于 WebSearch 调研产出。验证模型：deepseek-v4-flash。研究方向覆盖 AI 视频工具 UX、agent 框架 HITL 机制、传统动画/游戏审批流程、决策疲劳与信息呈现。*

*与本文件搭配使用的实操文档：`ai-video/HUMAN-GATES.md`（四种确认门的具体设计）。*
