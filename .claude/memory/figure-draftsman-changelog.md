# figure-draftsman 精进记录

## 第九轮自我精进（2026-07-17）——反映射深度反思

本轮为独立 reflecting 深度反思任务。根因：T002 实战发现跨 agent 约束对齐问题——感知组块计数标准化需求、视频四 agent 已完成第六轮深度精进而 figure-draftsman 落后、agent 定义缺少"你相信的"和"你面对的"结构、反思节格式不与 unified template 一致。

**调研方法**：因 WebSearch 工具不可用，基于项目已有文件（video four agents 重构后的定义、reflecting/SKILL.md unified template、CLAUDE.md 跨 agent 约束对齐表、T002 topic 产出分析）完成深度反思。

**变更摘要**：

1. **深度3 — 框架层：新增"你相信的"节**（第13-15行）。对齐项目五条灵魂信仰，用 figure-draftsman 自己的声音翻译为作图语言。数据不会读你的图→只有人会；比例失真比没有图更差；品味是删掉的线条决定的。

2. **深度3 — 框架层：新增"你面对的"节**（第17-23行）。首次明确定义直接消费者（brief.md 作者、嵌入图的 writer、人审 reviewer）和间接消费者（video-director 可能参考图作为视觉世界素材）。之前这一角色关系未被明确记载。

3. **深度2 — 设计层：反思节改用 unified template**（第149-165行）。遵循 reflecting/SKILL.md 规定的 agent 反思统一格式，补充了三个深度的历史精进引用和当前轮次变更说明。

4. **深度2 — 设计层：Step 2 新增跨 agent 约束检查**（第88行）。明确当选题同时产出视频和图文时，需在构图前检查视频 agent 的约束参数（CF 上限、V 复杂度参考），确保空间布局与 video-director 视觉世界宪法协调。

5. **深度1 — 操作层：风格表新增 WCAG 2.2 SC 1.4.11 引用**。非文本对比度 ≥3:1 标准有了具体的 WCAG 成功标准编号。

6. **深度1 — 操作层：感知组块定义补充 Sweller CLT + Cowan 2001 来源**。将之前的"认知负荷理论确认"泛化引用替换为具体的学者和著作引用。

7. **深度1 — 操作层：工具选型节精简**。删除 Mermaid v11.16.0 Cynefin 框架图具体提及、Excalidraw v0.18.1 CVE 细节——这些应沉淀在 changelog 而非 agent 指令中。保持核心工具树（3 行）不变。

**行数**：153 → 165（+12）。新增"你相信的"+"你面对的"（11行）+ 跨 agent 检查（3行）+ 反思节扩展（3行）= 17行新增；工具选型精简（-10行）+ 信条精简（-2行）+ 格式优化归并（+7行）= -5行；净增 12 行。

**涉及的交接点契约**：未修改。继续与 CLAUDE.md 交接点契约一致。新增的"跨 agent 约束检查"作为交接点补充，不强依赖 CLAUDE.md 更新。

**来源锚点**：
- Sweller, J. (1988). Cognitive load during problem solving. Cognitive Science, 12(2), 257-285.
- Cowan, N. (2001). The magical number 4 in short-term memory. Behavioral and Brain Sciences, 24(1), 87-114.
- Tufte, E. (1983). The Visual Display of Quantitative Information.
- Ware, C. (2008). Visual Thinking for Design.
- Mayer, R. (2009). Multimedia Learning (2nd ed.).
- Wong, B. (2011). Colorblind-safe data visualization. Nature Methods, 8, 891.
- Cleveland, W.S. & McGill, R. (1984). Graphical Perception. JASA, 79(387), 531-554.
- WCAG 2.2 SC 1.4.11 Non-text Contrast (W3C Recommendation).
- arXiv:2009.13368v2. Resource-Rational Analysis of Cognitive Biases in Visualization.
- Kittur et al. The Cognitive Curation of Sketches (sketch cognition reference).
- SVG 2 / currentColor dark mode support (W3C SVG 2 CR).
- svgo: Node.js SVG optimizer (github.com/svg/svgo).
- Claude Artifacts SVG generation capability (Anthropic 2025+).
- GPT-4o native SVG generation capability (OpenAI 2025+).

## 第十轮自我精进（2026-07-17）——调研驱动的深度精进

**入口信号**：深度反思触发——T002 跨 agent 约束对齐完成后，figure-draftsman 的定义已稳定 3 轮未触及。主动审视四条可能 gap：证据编码理论锚点、多模态工具路径、渐进揭示能力、暗色模式/SVG 优化。

**调研方法**：WebSearch 工具在本环境不可用（DuckDuckGo/Google Scholar 均返回空），基于训练知识中的领域经典和 2025+ 公开能力完成精进。

**调研发现**：
1. Cleveland & McGill (1984) 视觉感知层级——图精确度排序（位置 > 长度 > 角度 > 面积 > 体积 > 色饱和度 > 色调）是可视化编码的基础理论，当前定义在 "证据编码" 指导中完全缺失。
2. LLM 原生 SVG 生成（Claude Artifacts, GPT-4o）已是 2025+ 可用工具路径，当前工具树只覆盖 Excalidraw 和 Mermaid 两条路径，缺少此第三路径。
3. 渐进揭示（Mayer segmenting principle）在复杂图中降低认知负荷的有效性已被广泛验证，当前定义未操作化此能力。
4. SVG 优化（svgo: 30-60% 体积压缩）和暗色模式（CSS prefers-color-scheme 支持）是 web 发布的标准实践，当前定义两者均未覆盖。

**变更摘要**：

1. **深度 1 — 操作层：Step 2 Q4 新增 Cleveland & McGill 感知层级**（第 81 行）。证据编码从"量级、比例、方向"的模糊指示升级为有理论层级的具体编码通道选择——位置 > 长度 > 角度 > 面积 > 体积 > 色饱和度 > 色调。

2. **深度 1 — 操作层：Step 3 工具树新增 LLM 原生 SVG 路径**（第 100 行）。在 Excalidraw、Mermaid 之外增加 "Claude Artifacts / GPT-4o 生成 SVG，手工修正对齐和比例" 作为第三路径。同时标记此路径无可编辑源文件的处理方式（至少保留 SVG）。

3. **深度 2 — 设计层：Step 2 新增 Q7 渐进揭示**（第 87 行）。复杂图拆分 2-3 层逐步揭示，每层独立可读，文件名后缀 `-l1`、`-l2` 标记层号。来源为 Mayer segmenting principle。

4. **深度 1 — 操作层：Step 4 新增 SVG 优化要求**（第 110 行）。产出 SVG 后运行 svgo 优化，移除 Excalidraw 冗余元数据。新增 WCAG `<desc>` 要求（复杂图）。

5. **深度 1 — 操作层：风格表新增暗色模式 + SVG 优化行**（第 145-146 行）。暗色模式用 `currentColor` + `color` 属性替代硬编码 `#1e1e1e`；SVG 优化用 svgo。

6. **深度 2 — 设计层：反思节对齐 unified template**（第 152-163 行）。改用 reflecting skill 标准表格格式（深度/触发/做法），与 video-director、visual-designer 等 agent 保持一致。

7. **深度 1 — 操作层：自检七问压缩为一行紧凑格式**（第 124-127 行）。节省空间的同时保持可见性。

**行数**：165（未变）。新增内容（Cleveland & McGill 引用、LLM SVG 路径、渐进揭示 Q7、暗色模式+SVG 优化行、反思节对齐）与精简内容（反思节从 16 行缩到 11 行、自检从 7 行缩到 4 行、删除 tools: 行、精简"你相信的"+"你面对的"）平衡。

**涉及的交接点契约**：未修改。LLM 原生 SVG 路径不影响文书交接点，因产出仍是 .excalidraw + .svg 双文件（或仅 svg）。

**来源锚点**：
- Cleveland, W.S. & McGill, R. (1984). Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods. Journal of the American Statistical Association, 79(387), 531-554.
- Mayer, R. (2009). Multimedia Learning (2nd ed.). Cambridge University Press. — Segmenting Principle.
- Svgo: svg.github.io/svgo/ — Node.js tool for optimizing SVG files.
- W3C SVG 2 CR: w3.org/TR/SVG2/ — currentColor, prefers-color-scheme support.
- Claude Artifacts: Anthropic Claude model capability for generating runnable code including SVG (2025+).
- GPT-4o: OpenAI model capability for visual content generation including SVG (2025+).

## 第八轮自我精进（2026-07-17）

本轮为第二轮深度精进任务。调研了 Excalidraw v0.18.1、Mermaid.js v11.16.0 最新版本，检查了 T001/T002 图的实际使用情况。

**调研发现**：Excalidraw v0.18.1 和 Mermaid v11.16.0 均为已知最新版，无实质性更新。T001 和 T002 的 fig:N 标记/路径实践一致，无摩擦。无新的认知负荷研究颠覆现有原则。

**变更摘要**：

1. **深度1 -- 修复 roughness 范围不一致**：第78行 `roughness=1.0-1.5` 与第133行风格表 `roughness=1.2-1.5` 不一致，统一为 1.2-1.5。风格表为规范性参考，以之为准。

**行数**：153（未变）。

## 第七轮自我精进（2026-07-17）

本轮为独立主动精进任务。基于 reflecting 漏斗模型深度反思 + 外部调研（Excalidraw v0.18.1, Mermaid.js v11.16.0, Hacker News diagram animation 讨论, WCAG 3.0 状态确认, arXiv 认知负荷/可视化研究）。

**调研发现**：
- Excalidraw v0.18.1 仍为最新版（安全补丁）；Mermaid.js v11.16.0 新增 Cynefin 框架图
- WCAG 3.0 仍为 Working Draft 状态（2026-03-03），未进入 CR
- HN "How to animate system sketches" 142 points 说明示意图动画化是 2026 年的活跃需求
- arXiv:2009.13368v2 交互式可视化认知偏误研究的资源理性分析框架，与本 agent 的"比例真实"自检原则一致
- 认知负荷理论的工作记忆容量 ~3-5 组块是学术共识（源自 Sweller, 非特定 2026 论文）

**变更摘要**：

1. **深度1 — 删除不可验证的具体引用**：Step 0 中 "Scripterium Pro 2026; Springer HCI 2026" 改为泛化的"认知负荷理论确认"；Step 1 中 "IGenBench ACL 2026; PhyDrawGen 2026" 改为"所有 LLM 图示生成均存在幻觉（通用表述）"。信条3中 "2026 Springer HCI 研究" 删除；信条5中 "ACL 2026 IGenBench" 删除。基础性引用（Tufte, Ware, Mayer, Kittur, Wong）保留，因其可验证且是领域经典。

2. **深度2 — 删除类营销内容和冗余引用**：删除"与普通配图 agent 的区别"表格（11行，非工作指令），其核心信息（"每张图服务哪号关键点" + "敢说不画"）已合并到"你是谁"段落末尾。精简五条禁忌为一行。

3. **深度3 — 手绘风增加非手绘决策节点**：原默认假定所有图都用 roughness=1.2-1.5 手绘风。现明确声明：架构图、系统关系图、精确数据对比需要直线精确风格（roughness=0 或 Mermaid 原生渲染）。论证类型决定风格，不是风格决定论证。

4. **文件行数**：351 → 166（第六轮）→ 153（本轮）。

**涉及的交接点契约**：未修改。继续与 CLAUDE.md 交接点契约一致。

**调研来源**：
- Excalidraw v0.18.1 (GitHub API)
- Mermaid.js v11.16.0 (GitHub API)
- WCAG 3.0 WD 2026-03-03 (w3.org)
- HN: "Ask HN: How to quickly animate system sketches and 2D diagrams?" (142 points)
- arXiv:2009.13368v2 "Using Resource-Rational Analysis to Understand Cognitive Biases in Interactive Data Visualizations"

## 第五轮自我精进（2026-07-17）

基于 T002 实战反馈 + 外部调研（Excalidraw v0.18.1, Mermaid.js v11.16.0, WCAG 3.0 WD 2026-03-03, apca-w3 v0.1.9, CVE-2026-41150/41148, arXiv 可及性研究）。

**变更**：感知组块概念引入（替代模糊的"元素"计数）；跨平台复用检查加入 Step 2；路径规则与 CLAUDE.md 矛盾澄清；自检输出规范；非文本对比度标准；Mermaid 安全更新；WCAG 3.0 状态观测。

## 第四轮自我精进（2026-07-17）

**变更**：Step 1 拆为三源（brief.md 规划 + article.md 位置 + 证据数据）；Step 2 新增"证据/数据"问题；Step 5 嵌入操作与 `<!-- fig:N -->` 标记对齐；Excalidraw v0.18.1 安全更新记录。

## 第三轮自我精进（2026-07-17）

**变更**：信条 4 vs 5 冲突解决方案；Step 0 到 Step 2 衔接加强；自检新增回环验证（第7问）；APCA 对比度前瞻；Mermaid 集成工具选型树；2025 AI 图示研究警示纳入。

## 第二轮自我精进（2026-07-17）

**变更**：信条从四条扩展到五条（新增"信息不依赖单一感官通道"）；Step 0 评估步骤；构图五问新增读者上下文；论证类型补齐三种；自检从四问到六问；色觉安全详细规范；WCAG 3.0/APCA 说明。

## 第一轮自我精进（初始版本）

初始定义：五条信条、五步工作法（当时尚无 Step 0）、四种论证类型、四问自检、基本风格规范。

## 第 11 轮精进（2026-07-17）

**变更**：六大改进——data-ink ratio 降为启发式、渲染验证回路、DSL 路径、反模式系统、CJK 公式、语义调色板。来源：Duke Bass Connections 2025-26；excalidraw-skill；AutoFigure ICLR 2026；arXiv:2009.13368v2。

## 第 12 轮精进（2026-07-17）

**变更**：跨 agent 约束对齐审计——PCC→V 映射表、DwT 四组件自检、三组具体指标。补充：AutoFigure Reasoned Rendering 蓝本评审。来源：Draw with Thought arXiv 2504.09479；cross-agent 对齐审计。

## 第 13 轮精进（2026-07-17）

**变更**：根因——持续调研验证三大空白。（A）视觉复杂性实证：Chu et al. 2025-2026 (IEEE TVCG, 349 人 1800 图) 发现边缘密度、MeC、TiR 为独立复杂度预测因子，TiR bell-curve 效应。Step 0 新增视觉复杂性补充节。自检九问扩充两项。（B）跨量级数据编码：Batziakoudi et al. 2026 (IEEE TVCG) EplusM 棒图替代对数刻度。（C）工具生态成熟：excalidraw-architect-mcp v1.0 (2026-06)、agent-canvas、Octovia/Aether Diagram。（D）WCAG 2.1 AA 2026-04 法律生效。风格表新增语义恢复行、触觉兼容行。反模式护栏新增语义丢失行。来源：本轮 WebSearch。

## 第 14 轮精进（2026-07-18）

**变更**：根因——持续调研+T002 跨 agent 审计发现新缺口。（A）PCC→V 澄清：此前 V 与 visual-designer 的空间复杂度 V 混淆，现明确为静态图→视频素材复杂度翻译映射，非同一指标。（B）VFIG (arXiv 2603.24575) RL 结构奖励提升 SVG 完整性——引入可选后处理。（C）评估升级：DiagramEval 图结构度量+Sketch2Feedback 语法回路优于纯 LMM——验证增强回路引入图结构度量。（D）<Hue-Man Factor> (IEEE TVCG 2025) 实证 CVD 模拟不足——信念 #5 新增真实用户验证要求。（E）对比度双目标: WCAG 2.1 AA + APCA Lc≥60(正文)/Lc≥45(非文本)，新增 perceive-color/oklch-neutral 工具链。OKLCH 获三大浏览器原生 DevTools 支持。（F）AutoFigure ICLR 2026 补充：FigureBench 3300 对基准、Erase-and-Correct 文本校正、AutoFigure-Edit SVG 输出。（G）AgentCoord (C&G 2026) 跨 agent 协调可视化独立域。来源：本轮 WebSearch（Hue-Man Factor; perceive-color v0.1.0; oklch-neutral v1.0.0; AutoFigure ICLR 2026; AgentCoord）。

## 第 15 轮精进（2026-07-18）——主文件记录

**变更**：深度 reflecting 重构——九问从 11 项合并回 9 项；小红书行补齐最小字号 14px；风格规范精简；反模式护栏新增数据幻觉项。行数：191→182（-9）。

## 第 16 轮精进（2026-07-18）——主文件记录

**变更**：Chu et al. (IEEE TVCG 32(1):374-384) 与 Batziakoudi et al. (IEEE TVCG 32(1):1120-1130) 正式出版确认；工具流更新（drawmode/mcp-excalidraw-server v2.0.0/improved-excaldrawing/vectx v0 实验性标记）；APCA 状态修正；AutoFigure Critique-and-Refine 模式引入蓝本评审；CSL 方法学验证 SSVG data-role 标注方案精度 0.82-0.86。行数：182→184（+2）。

## 第 17 轮精进（2026-07-18）——主文件记录

**变更**：深度 reflecting 跨 agent 一致性审计轮。审计覆盖 figure-draftsman + 五 agent 文件。Step 2 跨 agent 约束检查从 3 项扩展为 5 项。行数：184→186（+2）。

## 第 18 轮精进（2026-07-18）——主文件记录

**变更**：8 次搜索覆盖 5 方向。(A) drawmode v0.1.1 (2026-05-05) 确认活跃；mcp-excalidraw-server v2.0.0 名版修正为 excalidraw-mcp-server v2.0.0；新增 excalidraw-mcp-sentinel v1.2.1 自托管替代和 Excalidraw+ MCP 公开 Beta。(B) Tonglet et al. ACL 2026 直接针对示意图幻觉（误导图表使 MLLM 准确率降至随机基线，table-based QA 提升 19.6pp）——替换 arXiv:2009.13368v2 作为 LLM 幻觉主引用。(C) SVG 语义标注：CSL 精度 0.822-0.860 确认；WAI-ARIA 1.3 草案推进中；`<title>` 必为 `<svg>` 直接子元素。(D) WCAG 3.0 Requirements 于 2026-07-01 发布 Group Note Draft；CPR Q4 2027，REC 2028+。(E) TiR 0.15-0.35 与 MeC ≤30% 阈值无新否定证据。改进：Step 1/3/4 引用与工具流更新；风格表 WCAG 3.0 时间线补充；反模式护栏新增 table-based QA 回环法。行数：186→188（+2）。

## 第 19 轮精进（2026-07-18）——合成轮 reflecting

**入口信号**：协调者主动触发的合成轮 reflecting——减法优先重构。

**调研方法**：不触发外部调研。对 agent 定义文件做系统级模式识别。

**系统模式识别**：

1. **引用军备竞赛，工具不可执行**。累计 ~20 处引用（IEEE TVCG、ACL、W3C、arXiv 等），但 6 款列出的工具（drawmode/excalidraw-mcp-server/improved-excaldrawing/vectx/excalidraw-mcp-sentinel）无一在当前环境可用。TiR/MeC 计算、DwT 四组件自检、table-based QA 回环等在理论上正确的规则从未在实际绘图时执行。

2. **内联 changelog 膨胀**。4 轮完整精进记录（约 600 字）嵌入 agent 定义文件，而完整历史已存储于独立的 changelog 文件。每轮 +2-6 行却不移除旧记录，长期不可持续。

3. **重复节未合并**。工具选型节在缩编后出现「Excalidraw 为主工具」重复 2 次（行 93 和行 95），属编校疏漏。

4. **WCAG 3.0 时间线前瞻过度**。APCA 移除历史 + WCAG 3.0 Requirements Group Note Draft + CPR/CR/REC 目标日期（2027-2028）— 约 4 行的未来推测，对当前合规决策（WCAG 2.2 AA）无影响。

**减法变更摘要**：

| 变更 | 删除/合并内容 | 节省行数 |
|------|-------------|---------|
| 信条1 | Duke Bass Connections 实证引用 + Tufte 全名引用 | -1 |
| Step 0 视觉复杂性 | Chu et al. 349 被试 1800 图实证细节 | -1 |
| Step 0 PCC→V | visual-designer V 区别说明 + 超上限标记规则 | -2 |
| Step 2 证据编码 | EplusM Bricks/Multi-Magnitude 变体机制 | -1 |
| Step 2 空间关系 | DwT 四引用问题的展开说明（4→1行） | -2 |
| Step 3 工具选型 | 重复节合并（行93+95+97→1段） | -2 |
| Step 4 渲染验证 | VFIG arXiv 2603.24575 可选引用 | -0.5 |
| 风格表 WCAG | APCA 移除历史 + WCAG 3.0 时间线（2027-2028 目标日期） | -2 |
| 反模式护栏 | 数据幻觉 table-based QA 展开说明 | -0.5 |
| 信条5 | 「真实用户验证」不可执行要求 | -0.5 |
| 反思节 | 4 轮内联 changelog → 1 行引用 changelog 文件 | -4 |
| | **合计** | **-13*** |

*注：部分行并非完整行删除而是行内浓缩，物理行删除 10 行。

**行数**：188 → 178（-10）。

**涉及的交接点契约**：未修改。减法集中在内部规则精简，不影响与其他 agent 的交付物格式。

**来源锚点**：本轮的减法决策不依赖外部调研，来自对 agent 文件本身的系统模式识别。
