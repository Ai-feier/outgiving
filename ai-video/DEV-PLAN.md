# 开发计划 · ai-video 生产链

> 依据：`DESIGN.md`（唯一设计事实源）。本计划是执行序 + 文件分工 + 验收，不是设计。
> 状态：P0 部分完成（见 P0.剩余）。
> 约束：不 git commit（除非人明确要）；改 `.claude/agents/` 后必须跑 `bash scripts/sync_pi_agents.sh`；workbench 服务器改 chain.py/server.py 后必须重启才生效（app.html 每次请求重读）。
> 文档全量重写（2026-08-26）的执行清单见 `docs/AGENTS.md` §4。

## 前置门（P1 不解锁条件）

**纸面演练**：新开 scratch 项目（T006 或 T999-test），主会话 + ≥1 designer agent 按 DESIGN.md §3 手工跑完**一个完整层**（goal ①②③ → 动态中间单元 → end 验收表）。验收：end ② 验收表逐行回答 goal ①，人逐条过目确认。规格没被真实生产验证前，不写一行 P1 代码。

## 阶段总览

| 阶段 | 内容 | 文件面 | 依赖 |
| ---- | ---- | ------ | ---- |
| P0 | 文档统一 + agent 契约改写 | ai-video/*.md（已完成）· .claude/agents/*.md · AGENTS.md · rules/project/collaboration.md | 前置门 |
| P1 | 后端：5 层解析 + 层模型 + 门 API | scripts/src/workbench/{chain,server}.py | P0 |
| P2 | 前端：层列视图 + 4 触点 + UX 契约 | scripts/src/workbench/app.html | P1（按 §5 契约并行） |
| P3 | T005 迁移 + 测试 + E2E | ai-video/projects/T005/*.md · scripts/tests/ | P1+P2 |
| P4 | 验收 | 全 | P3 |

P1/P2 文件不相交（后端 vs 前端），可并行；P2 按 DESIGN.md §5 的 API 契约写，不等 P1 完成。

## P0 · 文档统一

**已完成（2026-08-25/26）**：

- [x] `ai-video/DESIGN.md`（唯一设计事实源，§0-§8，纯终态规格）
- [x] `ai-video/DEV-PLAN.md`（本文件）
- [x] 4 个旧文档删除（workbench.md / workbench-product-plan.md / HUMAN-GATES.md / TOGETHER.md；内容已并入 DESIGN.md，全文归档于 git 历史）
- [x] `AGENTS.md`「生产链」段 = 层级链速览 + 指向 DESIGN.md
- [x] 文档全量重写启动：规范 + 执行清单见 `docs/AGENTS.md` §3/§4

**已完成（2026-08-26）**：

- [x] `.claude/agents/{script,visual,rhythm}-designer.md` + `video-director.md` 按 DESIGN.md §6 改写（v4.1：5 层模板 + ⑤ 对齐自报/门记录 + 前置统一表达）；grep 验收 `grep -n "固定四层\|end 结果\|annotations\|workbench.md" .claude/agents/*designer*.md` 命中为 0
- [x] `rules/project/collaboration.md` 交接点契约补主会话职责（DESIGN.md §6 末段）
- [x] `bash scripts/sync_pi_agents.sh`

**剩余**：`uv run --directory scripts content validate`（本阶段不动 frontmatter schema，随 P3 一起跑）

## P1 · 后端（scripts/src/workbench/chain.py + server.py）

现状：chain.py 解析单元 4 节（`## ① 简层` / `## ② 思考` / `## ③ 执行` / `## end 结果`）+ `段:` 分组。目标：DESIGN.md §2/§3/§5。

1. **解析**：单元 → 5 层（`## ① 简层` / `## ② 思考` / `## ③ 内容详情` / `## ④ 执行` / `## ⑤ 结果`，编号必须、后缀可省）。现有 4 节文件（`## ③ 执行` / `## end 结果`）→ 只读兼容：③ 执行 → exec、end 结果 → result + `layer_errors[]` 警告"旧四节格式，待迁移"。
2. **frontmatter**：`层:` 字段（+ `gate:` / `superseded_by:` / `title:`）；`段:` 只读兼容（同值并入，UI 标"旧字段"）。
3. **层模型**：层分组 / 层始（goal，层内入边 0，恰好 1）/ 层末（end，层内无后继，恰好 1）/ **跨层前置不限**（follows 可指向任意层任意单元，D39）/ `layer_errors[]`（替代 phase_errors）/ 层状态派生（规则见 DESIGN.md §2.5）。
4. **exec_kind**：④ exec 含 `prompt-file:` 或 Run 卡 → run，否则 design。
5. **API**（DESIGN.md §5）：
   - `GET /api/chain`：返回 `layers[]`（含 state）+ `units[]`（含 `层`/`gate`/`planned`/`parts:{claim,thinking,content,exec,result}`/`meta`/`state`）
   - `POST /api/chain/part`（替代 /section）：`{p,unit,part,expected_body,new_body}` → 409 stale
   - `POST /api/chain/state`：不变
   - `POST /api/chain/append`：`kind=run`（append 进 ④ exec，服务端算 Run#）/ `kind=grill`（append 进 ②）/ **`kind=gate`（新增：append 门记录进 ⑤ result，字段 verdict + oneline）**；幂等键 60s + per-file `threading.Lock` 不变
   - `GET /api/chain/assemble`：不变
   - **删除** `GET /api/annotations*` / `POST /api/annotations*` / `POST .../resolve`（含路由与静态文件读写）
6. 重启验证：`uv run --directory scripts ai workbench T005 --no-browser`（现有 4 层文件应带警告条可读，不崩）

## P2 · 前端（scripts/src/workbench/app.html）

**已完成（2026-08-26，v4.1 5 层 + 层模型 + 门 + 4 触点 + 状态矩阵）**：

- [x] LAYERS 常量 4 节 → 5 层（① claim ② thinking ③ content ④ exec ⑤ result）；API `u.sections` → `u.parts`
- [x] 层列视图：`layers[]`（兼容 phases）+ `layer_errors` 告警条 + 旧格式 chip（legacy）+ 层间交接箭头（「交接 · Lx end → 下层 goal（待审批）」）
- [x] 4 触点：改①（/api/chain/part）· grill②（append kind=grill）· 过门（单元门 批准/打回 + goal 层放行，门记录进 ⑤，E2E 验证落 md）· 记录运行（append kind=run，④ Run 卡）
- [x] 运行单元：④ 上「看请求体」+「记录运行」；前置清单点勾走 /api/chain/part
- [x] 默认选中 = 第一个可行动单元（DESIGN §4.4）
- [x] 15s 轮询（hasFocus 限定）+ header [⟳] + 最后同步时间（D35）
- [x] sessionStorage 持久化选中（刷新恢复）
- [x] 文件视图（📄 切换：块编辑 + 请求体装配）保留，E2E 验证来回合切
- [x] 删除：annotations 视图/弹窗/批注徽标（意见走单元 ② grill；文件视图「提意见」→ 提示语）
- [x] 验收：T005（旧 4 节）+ T999-test（新 5 层）0 JS 错误；门打回 E2E 落 md；截图 designs/workbench-ux-20260825/shot-t005.png / shot-t999.png
- [ ] 遗留（P4 验收时补）：层折叠状态 sessionStorage 持久化 · 折叠 ②③④ 单行摘要（现为空折叠行）· DAG 跨层前置不同色

1. **层列视图（图设计，DESIGN §4.1）**：层块序列（拓扑序），块头 = L 徽标 + goal H1 + 层状态 + 单元数 + 验收计数（n✅m⚠️k❌，解析 end ⑤ 验收表）；块内 = 真 DAG（拓扑列布局、follows 边全绘制、多前置多收敛、跨列曲线、跨层前置不同色 + 单元名、纯链才压单行）；计划单元 = 虚线节点；块间交接箭头（标注"待审批 L(k+1) goal"）。
2. **goal 卡**：① 常显可改（写回 part=claim）+ [已放行/放行] 标记（读 ③ 门记录 `层放行`）。
3. **中间单元**：① 常显可改；②③④⑤ 各折叠单行摘要（DESIGN §4.8）；卡头 ≤5 元素（前置不进卡头，只上图与侧栏）。
4. **end 卡**：② 验收表常显（表格渲染）+ ③ 交接块常显 + [验收通过/打回] 按钮（打回 → 意见进下层 goal ② 草案 或 提示开新层）。
5. **4 触点入口**：改①（编辑器）/ grill②（追加表单）/ 过门（gate 单元 ③ [批准][打回]；运行单元含「看请求体」装配视图 + 成本 + 命令，复用 /assemble）/ 验收 end（上条）。
6. **保留**：前置清单点勾（part=output 整段写回）· 记录运行表单（append kind=run）· 409 特判文案 + 重试 · 媒体内联 + onerror 占位 · 文件视图（块编辑 + prompt-body）· 5 态下拉（/chain/state）· agent 徽标 · DOMPurify 全量。
7. **删除**：annotations 视图与工单交互。
8. 验收：0 JS 错误；动态 HTML 全部走 `setHTML()`。
9. **命令条与当前位置（DESIGN §4.4 / D32）**：阻塞点解析（第一个未完成层 → 其中第一个可行动单元）+ 下一动作 + 主按钮；默认选中 = 第一个可行动单元；载入自动滚到当前层。
10. **侧栏 = unit inspector（DESIGN §4.5）**：按单元类型内容契约——设计 = ② 自报摘要 + 未解决 grill 数 + 上游/下游跳转；运行 = exec panel（清单 n/m + 成本 + 请求体 + 命令 + [记录运行]，装配失败禁用记录）；gate = [批准][打回] + §4.3 门参考展开 + 代价表；end = 验收表 + 交接块 + [验收][打回]；metadata 降为折叠单行（非空才显示）。
11. **状态矩阵（DESIGN §4.6）**：加载骨架；告警条覆盖 layer_errors/missing/非法状态值三类；15s 轮询（`document.hasFocus()` 限定）+ header [⟳] + 最后更新时间；sessionStorage 持久化（project/选中/层折叠/滚动）。
12. **视觉契约（DESIGN §4.8 / D33-D34）**：选中色与 failed 色解耦（选中 = 中性 outline，accent 专属 primary action）；卡头 ≤5 元素且不换行（follows 移出）；折叠 ②③ 单行摘要；字号 floor 11px；DAG marker-end 指向 `url(#cmarr${ph.id})` + `firstCol === undefined` 判定；纯线性链紧凑单行。
13. **a11y 与视口（DESIGN §4.9/4.10 / D36）**：a11y floor 硬契约（tabindex/role/Enter-Space · role=dialog+全局 Esc · focus-visible）+ focus 契约（模态关闭回触发元素、打开聚焦首输入、flash/409 `aria-live=polite`、状态下拉可见 label）；最小宽 1100px（更窄提示加宽）+ 侧栏折叠开关。

## P3 · T005 迁移 + 测试 + E2E

1. **迁移映射**（现文件 → 迁后；迁移只动 T005，exec/ 与 assets/ 不动）：

   | 现文件 | 迁后 |
   | ---- | ---- |
   | goal.md（段 p1） | l1 goal：① → 验收标准（4 行 claim + 红线）；② 保留共同理解 + 分解理由；③ = 单元计划 |
   | research/script/visual/rhythm/director.md | 5 层化：② 里设计内容挪 ③ 内容详情；原"end 结果"（对齐自报等）挪 ⑤；④ = 无；`段: p1` → `层: l1` |
   | seg1.md | l1 中间单元：原 ③ + end → ④ 执行（Run 1 保留）+ ⑤ 结果；director/seg1 加 `gate: 是`（成本门） |
   | （新增）end-l1.md | l1 end：③ 层产出（seg1-h3.mp4 胜出 + 末帧）+ ⑤ 验收表（对 goal ① 4 行，证据从现 seg1 end 段搬运）+ 交接块 |
   | goal2.md（段 p2） | l2 goal：① 验收标准（3 行：seg2 5s/形态连续/接缝无跳帧 + 继承 L1 红线）；follows: [end-l1, seg1]（跨层前置，D39 合法） |
   | seg2.md / end.md | l2 中间 / l2 end（5 层化）；end 的 BGM/混音/拼接 claim 进 ① |
   | gates/gate3-design-alignment.md | 移 `archive/`（旧门裁决包内容已在 director ② 关键裁决内；新项目门记录进单元 ③ `### 门 · …`） |
   | annotations.md | 移 `archive/`（审计用） |

   非链文件区（迁移不动，文件视图可开）：`exec/`（prompt/交付件）· `assets/`（参考图/抽帧/素材描述 md）· `outputs/`（成片）。
   旧项目（无 `unit:` frontmatter 的平铺 md，如 T001/T003）：不进链，文件视图可开，不动。

2. **pytest**（`scripts/tests/test_workbench_chain.py`）：
   - 5 层解析（含旧 4 节兼容映射 + 警告）
   - 层分组（T005 l1/l2 + 无层默认 + layer_errors 三例：双层始/双层末/跨层边错指）
   - 状态解析 5 边界（未开始/就绪/运行中/完成/失败 + 非法值回退）
   - /chain/state 409 · /chain/append run 编号（0→Run1、Run3→Run4）+ 幂等 · grill append · **gate append（新）**
   - 层写回不伤状态行 / frontmatter
3. **headless E2E**（playwright，executable_path 显式指向缓存的 chromium_headless_shell）：层块渲染（2 层 + 交接箭头 + 虚线计划节点）· 0 JS 错误 · 改 ① 写回 · grill 提交 · 门批准（gate 记录落 md）· 记录运行（Run 卡 canonical 格式）· 409 路径。
4. 跑通：`uv run --directory scripts pytest tests/test_workbench_chain.py -q`

## P4 · 验收

1. T005（迁移后）链视图 = 2 个层块 + 块间交接箭头；块内 = 拓扑布局 DAG（director 3 前置收敛可见，不是直线）；跨层前置（goal2 ← seg1/end-l1）着色可见；层状态点正确（l1 完成、l2 进行中）
2. end-l1 验收表逐行可点查；打回 → 意见落 l2 goal ② 草案
3. gate 单元（director/seg1）③ 出 [批准][打回]；运行单元「看请求体」出真实 JSON + 成本 + 命令
4. 旧项目（无 `层:` 无状态行，如 T001/T003）打开不报错，单默认层
5. P3 测试全绿 + E2E 通过
6. grep 可验证：`.claude/agents/*designer*.md` 无 "固定四层/end 结果/annotations" 残留；DESIGN.md 含 §0-§8 全节
7. UX 契约验收（DESIGN §4.4–4.10）：命令条在 T005 上回答"现在该做什么"（l2：seg2 可看请求体/可记录运行）；选中高亮与 failed 态颜色不同；DAG 箭头可见；15s 轮询在有焦点时生效、后台标签页不发请求；sessionStorage 刷新恢复选中；E2E 加模态 focus 回归路径

## 风险

| 风险 | 缓解 |
| ---- | ---- |
| 5 层解析破坏旧项目只读体验 | 旧 4 节/无 frontmatter 全兼容（只读 + 告警），迁移只动 T005 |
| 动态单元让链视图"形状未知" | 计划单元虚线节点 + goal ③ 计划表常显；形状本身可 grill |
| 门机制漏掉原检查清单 | 门内容参考在 DESIGN.md §4.3（审批 UI 展开对照）；T001 代价表随门记录展示 |
| agent 契约改写漏改 → 单元文件写回旧格式 | P0 验收 grep + P3 测试含旧格式兼容路径（写旧格式可读不崩） |

## 架构 Review（2026-08-26，外部 review 7 项）

顺序按杠杆/安全性排定：#1 → #3 → #6 → #2 → #7 → #4 → #5。

| # | 项 | 状态 |
| - | ---- | ---- |
| 1 | chain.py 深模块（render/parse 孪生 + exec-meta 单源） | 完成：`render_run_card`/`parse_run_cards`、`GateRecord`、`ExecMeta`、`DEFAULT_*` 单源；32 测试绿 + live 验证 |
| 3 | composition from_markdown 修 YAML bug | 完成：yamlmini.py（零依赖 YAML 子集）+ models/manifest 重写 + e2e 11 测试；T004 真实清单解析通过（7 轨 87 段）；顺带修 mask alpha 管线（中间文件 ffv1/yuva420p/mkv + 最终 color 源 overlay 合成，ffmpeg 4.4 无 backgroundcolor） |
| 6 | 平台注册表（+1 平台 = 1 处改） | 完成：`content/platform.py`（PlatformSpec 8 字段 + 归一化查找 + 两个 slug 工具）；cli/preview/id_gen 全部从注册表取；drift 测试锁枚举↔注册表一致；scratch 全链路验证过 |
| 2 | content Document 深实体（lifecycle.py 可删） | 未开始 |
| 7 | profiler⇄index 换 dataclass | 未开始 |
| 4 | AI 传输缝（可注入 client + clock） | 未开始 |
| 5 | ai.pipeline.complete_video | 未开始 |
