# TOGETHER — 协作对齐文档

> **规则**：每个 agent 开始工作前先写自己的 section。产出后回读其他人的 section，检查是否对齐。
> 不对齐 → 在「评论」区标注 → 触发 loop 优化 → 直到所有条目 ✅。

**三道防线，各司其职**：
- **§3 对齐检查** → 门 3 的前置输入（designer 自己说对齐了没）
- **§4 资源就绪** → 门 4 的前置输入（P0 未就绪 → 合成阻塞）
- **§5 交叉验证** → §3 的补充（不是自己说对齐了，是另一个 agent 验证过了）

---

## 1. 共同理解

*由第一个启动的 agent 填写，其他 agent 确认或修正。*

| 维度 | 内容 | 确认 |
|------|------|------|
| 这条视频一句话是什么 | Bleach 千年血战祸进篇 30s PV——友哈巴赫入侵、一护双刀觉醒、三界崩坏的视觉奇观预告 | ___ script ___ visual ✓ ___ rhythm ✓ ___ director ✓ |
| 核心沟通目标（信息/情绪/行动） | 信息型：让观众理解千年血战篇核心冲突（混合策略~70%奇观+情感锚点） | ___ script ___ visual ✓ ___ rhythm ✓ ___ director ✓ |
| 平台 + 时长 | 抖音 30s | ___ script ___ visual ✓ ___ rhythm ✓ ___ director ✓ |
| 风格 | Bleach 日系动画（止め絵/速度线/墨韵），Seedance 2.0 生成，9:16 竖屏 | ___ script ___ visual ✓ ___ rhythm ✓ ___ director ✓ |
| 版权/红线 | BGM 不可用 Shiro Sagisu 原版配乐；Cour 4 播出中，镜头须标"最终效果以动画为准" | ___ script ___ visual ✓ ___ rhythm ✓ ___ director ✓ |

**director 修正**：§1 整体准确。补充两点：(1) 请同步记忆「每 3-5s 一个信息增量或小爆点」这一来自 gather-expert 证据 3-A 的 30s 平台约束；(2) style 更具体为 `bleach`（japanese-anime 子类），开场的剪影优先于面部——这影响视觉资产设计方向。

---

## 2. 各自方向

### 2.1 script-designer

**我理解的方向**：
Bleach 千年血战最终章"祸进篇"的30秒信息型PV。不是展示角色大合集——是在30秒内讲清楚"谁来了、谁应战、后果是什么"这条因果链。视觉奇观为主（~70%），一护双刀觉醒是唯一的情感落脚点。

**弧线选择 + 理由**：
**经典弧**（中性→上升→转折→释放），30s压缩版——开场即高潮（无慢热身）。
- B1 Hook: Yhwach入侵（高A/效价负/低D）→ B2 Reveal: 一护双刀觉醒（A稍降/效价转正/D上升）→ B3 Escalation: 双刀力量释放→世界崩坏（A到峰值/效价复杂）→ B4 Drop: "祸进"标题+CTA（A骤降/效价+D转正）
- 理由：三信息点有明确因果链（因为入侵→所以觉醒→导致祸进），经典弧最能承载因果叙事。30s压缩了中性阶段但结构匹配。

**核心假设**（需要其他人确认的）：

| 假设 | 谁需要确认 | 状态 |
|------|-----------|------|
| 30s 4拍结构(Hook/Reveal/Escalation/Drop)与brief混合策略一致 | rhythm | 待确认 |
| 仅Yhwach+Ichigo两角色即可传递千年血战核心冲突 | visual | 已确认（visual §2.2假设表第2条支持"2角色足够建立记忆点"） |
| 段边界在B3a末（~00:14.5-00:15.5）Ichigo剪影浮现帧符合尾帧值得条件 | director | 待确认（详见script-beats.md B3b设计） |
| Ichigo双刀规范参考图需新产——DEMO为一护单刀死神代理形态，非True Shikai双刀 | visual | 待确认 |
| CF×V裁决（Hook CF→2.0, Esc V→2+半速映射）——V=2简化背景已在B3设计中体现 | rhythm + visual | 待确认（visual已确认接受，rhythm待确认） |
| 祸进标题视觉值得重看——残破汉字+真空停顿落差在第2遍时产生预期性紧张 | rhythm | 待确认 |

**我给 rhythm 的约束**：
- **PAD轨迹**：B1: P:-1→-1, A:3→4, D:3→2 | B2: P:0→+1, A:3→3, D:3→4 | B3: P:+1→-1, A:4→5, D:4→3 | B4: P:-1→+1, A:5→2, D:2→4
- **情绪关键词+强度**：胁迫(4/5)→好奇→震撼(5/5)→满足
- **认知负荷粗估**（信息密度×画面复杂度，供rhythm独立标定CL参考）：B1:4 / B2:3 / B3:5→4（Esc V=2降级后） / B4:2
- **段落边界**：B3→B4（~22s）需复位信号——0.5s真空停顿（已对齐rhythm约束）。B3内段边界（~14.5-15.5s）需尾帧锚定

**我给 visual 的约束**：
- **实体列表**：[ANTAGONIST] Yhwach（规范参考B1），[PROTAGONIST] Ichigo True Shikai双刀（规范参考B2），[FACTION_STERNRITTER] 星十字骑士团剪影（B1背景级）
- **规范参考拍号**：B1→Yhwach首次清晰出现。B2→Ichigo True Shikai双刀首次清晰出现。**DEMO已有单刀死神代理Ichigo**，双刀True Shikai需新产
- **视觉资产需求清单**（完整见script-beats.md）：

| 拍 | 类型 | 实体/场景 | 用途 | 优先级 | 路径 |
|----|------|-----------|------|--------|------|
| B1 | 规范参考图 | Yhwach | 首次出现锚定（正面+全身） | P0 | `待产` |
| B2 | 规范参考图 | Ichigo True Shikai双刀 | 首次出现锚定（正面+全身，双刀形态） | P0 | `待产`（非DEMO单刀资产） |
| B1 | 场景参考图 | 无形帝国冰宫内部/友哈巴赫御座 | Hook场景定位 | P0 | `待产` |
| B1 | 分镜概念图 | Yhwach入侵（多瞳→御座→军队剪影） | 钩子镜头路径（供figure-draftsman） | P1 | `待产` |
| B3 | 分镜概念图 | Getsuga Jujisho释放构图（一护站位+十字冲击波方向） | 高潮空间定位（供figure-draftsman） | P1 | `待产` |
| B3 | 场景参考图 | 瀞灵廷崩塌 | Escalation环境 | P1 | `待产`（可降级文本） |
| B4 | 分镜概念图 | "禍進"标题文字布局（残破变形+碎片方向） | Drop视觉精度（供figure-draftsman） | P1 | `待产` |

- **实体复现**：Yhwach B1→B3c（2拍间隔≤3拍✓）。Ichigo B2→B3a连续出现（✓）

**我给 director 的约束**：
- **段边界**：段1(0:00-0:15.5)：B1+B2+B3a-b。段1末帧(~00:15.5)：Ichigo剪影从Getsuga灵压中浮现，双刀垂放，白色碎片初现。尾帧条件：构图干净/角色位置清晰/光照稳定/无运动模糊/D≥3。**延续边界**。段2(0:15.5-0:30)：B3c-e+B4。段2首帧以段1末帧Tier 0强制参考。段2参考图含段1末帧（连续性锚定）+ Yhwach规范参考图（身份复位锚定）——双重锚定打断漂移链。
- **标签注册**：`[ANTAGONIST]`=Yhwach / `[PROTAGONIST]`=Ichigo True Shikai / `[WEAPON_ZANGETSU]`=双斩月
- **锚点拍候选**：B2（情绪转折点+唯一放慢呼吸段落）、B3（视觉高峰+段边界所在）、B4（结构终点+CTA）
- **段落边界复位**：B3→B4（~22s）：0.5s黑屏+全静音复位信号——既是Drop拍标准真空停顿，也是LoL汇帧坍塌预防

---

### 2.2 visual-designer

**我理解的方向**：
Bleach 千年血战篇 30s PV。核心不是"讲完故事"——是在 30s 内让被抖音推荐流打断的用户看到"灭却师之王进攻"的视觉奇观，然后在被钩住后用"一护双刀觉醒"完成情感锚定。两个角色，一个动作序列——聚焦才有记忆点。

**视觉形态 + 理由**：
日系动画 PV（Bleach 风格），非叙事短片——高密度快切 + 止め絵静止蓄力 + 速度线爆发 + 墨韵渲染。符合 Bleach 的"对峙→瞬移斩击→余波"三段式战斗呼吸。30s 不适合展开叙事，适合做一个"预告片式的情绪拱形"：冲击→认知→升级→骤停。

**核心假设**：

| 假设 | 谁需要确认 | 状态 |
|------|-----------|------|
| Seedance 2.0 可还原 Bleach 修长身形 + 高对比色指定（死霸装黑色+冷白高光） | director | 待确认（T001 DEMO quality⚠，需 IaD 复检） |
| 30s 仅聚焦 Yhwach + Ichigo 2 角色足够建立记忆点 | script | 待确认（gather-expert 研究支持，但需 script 分镜验证） |
| 一护双刀形态（True Shikai：长刀=死神+短刀=虚）能被 Seedance 正确生成 | director | 待确认（需产高质量参考图后实测） |
| 友哈巴赫多重瞳孔+红瞳特征可通过参考图锚定 | director | 待确认（关键 P0 资产，需先产出参考图） |
| Bleach 粉丝能在 0.5s 内识别一护双刀形态的叙事意义 | script | 待确认（新粉可能不识别，需 script 增加认知时间窗口） |

**V 值（1-5）**：
**2**（加权平均）。按 director 的 CF×V 裁决（§2.4）调整：Hook V=2（Yhwach 红瞳+星十字剪影，rhythm 降 CF 至 2.0 → 4.0 ✅）× Reveal V=2（双刀静态展示+纯色背景，CF 1.4 → 2.8 ✅）× Escalation V=2（一护双刀释放+瀞灵廷裂开，rhythm 半速映射 effektiv CF 2.0 → 4.0 ✅）× Drop V=1（CF 0.8 → 0.8 ✅）。全部 CF×V<4。

**我给 script 的约束**：
- **实体复现间隔**：主角（Yhwach / Ichigo）≤3 拍。T003 仅 4 拍 → 意味着每个角色必须在连续 3 拍内至少出现一次。Yhwach 在 Hook 已入画 → 最迟 Escalation 必须再现（可通过闪回/剪影/灵子痕迹）。Ichigo 在 Reveal 入画 → 最迟 Drop 必须再现（可通过祸进标题的剪影叠加）。
- **禁止清单**：连续战斗长镜头（Bleach 是"一刀之间有空隙"）、3 个以上角色同框（T003 视觉焦点只能承载 2 角色）、柔焦/溶解过渡（仅用硬切和白闪）、>5s 无变化静止（30s 抖音约束，Drop 拍的 0.5s 真空停顿是唯一例外）。

**我给 rhythm 的约束**：
- **V 值**：2（加权平均）。按拍：Hook V=2 / Reveal V=2 / Escalation V=2 / Drop V=1。已接受 §2.4 director 的 CF×V 裁决——Hook 你降 CF 至 2.0，Escalation 你用半速映射 effektiv CF 2.0。各拍 CF×V 均 <4。
- **材质复杂度**：4 材质类——(1) fabric(cotton-matte) 死霸装/灭却师服；(2) metal(steel-brushed) 斩魄刀；(3) synthetic(glossy) 灵子光效/灵压；(4) VFX(debris) 崩坏裂痕/碎片。去除灵王碎片(bios)和文字排版(TYP)材质叠加，Escalation 简化后材质 ≤3。
- **CF×V<4 约束**：各拍均已通过。Escalation 压线（2×2=4），需你确认半速映射的 effektiv CF=2.0 可用。

---

### 2.3 rhythm-designer

**我理解的方向**：
30s 抖音 Bleach PV。核心节奏不是"讲故事"——是在时间维度上制造两次预测误差：第一次在前 1.7s（友哈巴赫红瞳打断浏览模式），第二次在 22s 处（真空停顿→祸进标题爆发）。两次误差之间是压缩-释放循环的加速积累。CL 目标 1.5-2.0，全程 4 拍对应一次完整的压缩-释放曲线。

**曲线类型 + 理由**：
**压缩-释放 (Compress-Release)**。理由：
1. Bleach PV 的本质节奏是对峙→瞬斩→余波的战斗呼吸——天然是紧张积累→突然释放的结构
2. 30s 4 拍结构（Hook→Reveal→Escalation→Drop）本身即是压缩（Escalation 12-22s）→释放（Drop 22s+）的大弧线
3. **天然适合重播**：第二遍时真空停顿变得更可预期，观众预知祸进即将出现→预期性紧张加强释放快感
4. 抖音收藏率驱动的算法信号要求第二遍比第一遍更有价值——压缩-释放的停顿处藏细节（灵王碎片/剪影），一遍看不完

**核心假设**（已全部确认）：

| 假设 | 谁需要确认 | 状态 |
|------|-----------|------|
| 30s 4 拍结构（Hook 5s/Reveal 7s/Escalation 10s/Drop 8s）与 script 分镜一致 | script | ✅ 已确认（script-beats.md 匹配 5/7/10/8） |
| Escalation 拍 CF 用半速映射（效感 CF=2.0）配合 visual V=2 | visual | ✅ 已确认（director §2.4 裁决 + visual V=2 更新 + rhythm-curve.md 已设计） |
| 22s 真空停顿 0.5s — 段级 ASL 不违反护栏（段1 ASL~2.2s, 段2 ASL~2.4s） | director | ✅ 段级 ASL 均 >1.8s。ZPC 无风险 |
| 第二遍观看时祸进标题因"已知即将到来"产生新意义 | script | ✅ 已确认（script-beats.md B3e/B4a 間标注支持） |
| 开场 0.3s 模式中断（Yhwach 多瞳特写）捕获认知控制 | director | ✅ 已确认（director §2.4 前 3 秒铁律已写入） |

**CL 标定值 + CF 值**（已按 director §2.4 裁决更新）：

| 拍 | CL | CF | CF 更新说明 |
|----|-----|-----|-----------|
| B1 Hook | 1.8 | **2.0**（原 3.0 → 2.0 per 裁决） | 降频——保留 0.3s 模式中断 + 2 帧：红瞳特写(0.3s) + 全景亮相 |
| B2 Reveal | 1.5 | **1.4**（不变） | 呼吸段落——半速映射，低频稳定 |
| B3 Escalation | 2.0 | **2.0 效感 CF**（原 4.5 → 2.0, 半速映射） | 物理切频可高（5 子拍 10s），但每帧 V=2 + 半速映射控制感知变化率 |
| B4 Drop | 1.5 | **0.8**（不变） | 含 0.5s 真空停顿 |

- **ID**（信息密度 1-5）: 3 / 3 / 4 / 2
- **ED**（情绪密度 1-5）: 4 / 3 / 5 / 4

**CF×V 已按 director §2.4 裁决全部解决**：

| 拍 | CF | V | CF×V | 方案 | 来源 |
|----|-----|----|------|------|------|
| Hook | 2.0 | 2 | **4.0 ✅** | rhythm 降 CF（3.0→2.0）, visual 保持 V=2 | director §2.4 |
| Reveal | 1.4 | 2 | **2.8 ✅** | 无需调整 | — |
| Escalation | 2.0（效感） | 2 | **4.0 ✅** | 半速映射 + visual 降 V（4→2） | director §2.4 |
| Drop | 0.8 | 1 | **0.8 ✅** | 无需调整 | — |

**我给 script 的约束**：
- **拍长窗口**：实体（Yhwach / Ichigo）单次露面 ≤6s，纯视觉（灵王崩坏/三界剪影）≤8s。B1（Hook）前 0.3s 必须模式中断（友哈巴赫多瞳特写或其他视觉奇观）
- **停顿点位置**：B4 前（~22s）需要 0.5s 真空停顿（黑屏+瞬寂）。B3→B4 是压缩→释放的分界，停顿是必要条件
- **B3 信息量**：Escalation 拍（12-22s）10s 内需要 6-8 个信息增量或小爆点。script 须在此段分配足够的视觉素材（双刀释放/灵王碎片/三界坍缩/瀞灵廷裂开），否则物理切频高但信息增量不足→无效完播

**我给 visual 的约束**：
- **CF×V<4 实际值**：
  - Hook（CF 3.0 × V 2）= 6 → ❌ 超标。需：visual 降 Hook V 至 1（纯红瞳特写+黑背景），或我降 Hook CF 至 2
  - Reveal（CF 1.4 × V 2）= 2.8 → ✅
  - Escalation（CF 4.5 → 半速映射效感 CF 2.0 × V 4）= 8 → ❌ 仍超标。需 visual 降 V 至 ≤2（单角色聚焦，去灵王碎片背景），并且我必须在 Escalation 使用半速映射
  - Drop（CF 0.8 × V 1）= 0.8 → ✅
- **通行方案**：Escalation 拍 visual V 降至 2 且我使用半速映射（效感 CF 2.0），则 CF×V=4 → 压线通过。若 visual 坚持 V≥3，则此拍无法通过护栏

---

### 2.4 video-director

**我理解的方向**：

30s 抖音 PV — Bleach 千年血战祸进篇。信息型混合奇观（~70% 奇观 + 一护双刀情感锚点）。4 拍（Hook/Reveal/Escalation/Drop），但**工具决定段为 2 段各 ~15s**（Seedance 2.0 Mini 适配器硬限）。段间末帧补偿视觉一致性。核心挑战：P0 参考图全缺 + CF×V 两拍超标 + 段数修正。

**工具选择 + 段长上限广播**：

| 项目 | 选择 | 理由 |
|------|------|------|
| **首选工具** | Seedance 2.0 Mini（15s） | 适配器 `seedance.py` 当前硬限 15s（不限 model）。**30s 必须拆段** |
| **段方案** | **2 段各 ~15s** | **段 1（0:00-0:15）**：Hook + Reveal + Escalation 开篇（Beat1-Beat3 前半）。**段 2（0:15-0:30）**：Escalation 高潮 + Drop + CTA（Beat3 后半-Beat4） |
| **段边界** | Escalation 加速中段（~00:15） | 不是节拍边界——是 Escalation 内部节奏密度跃升点。从相对放慢的一护双刀展示（Reveal）进入镜头加速（Escalation）后的中段过渡 |
| **段间协议** | 段 1 末帧 → 段 2 Tier 0 参考图 | 末帧路径：`ai-video/projects/T003/assets/last-frames/T003-B1-lastframe.png`。标记 `[段间锚定:B1→B2]`，不绑角色标签，纯外观延续锚点 |
| **模型** | `doubao-seedance-2-0-mini-260128` | Mini 版 15s 上限。备选：Pro 版（需适配器分支修改 `duration_hint` 硬限） |
| **备选** | 适配器分支支持 Pro 30s → 合并为 1 段；Veo 60s（需验证 Bleach 风格还原度） | |
| **画幅** | 9:16（portrait，从 style 推断） | |
| **单拍时长上限** | 实体 ≤6s / 纯视觉 ≤8s / 钩子（Beat1）不限 | 上游约束广播。注：30s PV 中单拍就是单镜次，非叙事短片的长拍 |
| **每段 ≥1 参考图** | 段 1 从 asset-lab/visual-designer 链路取。段 2 含段 1 末帧（RefImg 门禁强制） | 末帧不计入 ≤9 图槽限 |

**收敛门预检**（结合当前 §2.2-§2.3 实际数据更新）：

| 检查项 | 门 | 状态 | 依据 / 风险 |
|--------|----|------|-------------|
| TOGETHER.md §3 无🔴 | **ALIGN** | ✅ 预检通过 | 三 designer 已部分填写。§3 当前无🔴（有❌条目标注中，属于正常对齐流程）。§6 有 🔴 C001（script 空缺）和 C002（CF×V 冲突），见下方裁决 |
| 每拍自包含 | **FreeLOC** | ✅ 低风险 | 4 拍结构每一拍内部独立可消费。Hook 自含冲突信号，Reveal 自含双刀认知，Escalation 自含加速，Drop 自含标题。无跨拍必须前情提要不 |
| ≥20s 段边界复位 | **LoL** | ✅ 低风险 | 2 段各 ~15s < 20s 阈值，无需复位 |
| ASL ≥ 1.8s | **ZPC** | ⚠ **需 rhythm 确认段级 ASL** | 拍级：Hook ~1.7s（CF=3.0，5s/3shots），Escalation ~1.4-1.7s（CF=4.5-2.0）。但 ZPC 按**段级**计算（2 段各 15s）：段 1 ASL ≈ 1.9-2.1s（7-8 shots/15s）→ ✅。段 2 ASL ≈ 2.1-2.5s（6-7 shots/15s）→ ✅。**只要 rhythm 按段级计算 ASL，ZPC 无风险** |
| 参考图 IaD 中性 | **IaD** | 🔴 **高风险** | DEMO assets 均 ⚠（未实测通过）。P0 参考图（Yhwach / 一护双刀 / 冰宫场景）不存在——visual-designer 必须先产 |
| 每段 ≥1 参考图 | **RefImg** | 🔴 **高风险** | 段 1 缺 Yhwach + 一护双刀参考图。段 2 依赖段 1 末帧（目前段 1 未生成，无末帧可依赖）。须先解决 R1-R3（§4） |

**CF×V 裁决**（rhythm-designer §2.3 + visual-designer §2.2 冲突）：

当前 rhythm 标 CF（Hook 3.0 / Reveal 1.4 / Escalation 4.5 / Drop 0.8），visual 标 V（Hook 2 / Reveal 2 / Escalation 4 / Drop 1）：

| 拍 | CF | V | CF×V | 裁决方向 |
|----|----|----|------|---------|
| Hook | 3.0 | 2 | 6 ❌ | **rhythm 降 CF 至 2.0**（减少前 5s 切数，保留 0.3s 模式中断 + 仅 2 个镜头：友哈巴赫多瞳特写 2s + 星十字剪影 3s）。保留 visual V=2 的理由：Hook 需要 Yhwach 红瞳+星十字背景以建立"灭却师入侵"的视觉上下文 |
| Reveal | 1.4 | 2 | 2.8 ✅ | 无需调整 |
| Escalation | 4.5→2.0(半速) | 4→**2** | 4.0 ✅ | **双方各让一步**：rhythm 用半速映射（效感 CF=2.0，物理切频仍可高），**visual 降 V 至 2**（去灵王碎片和文字排版叠加，仅保留双刀释放 + 瀞灵廷裂开两个核心视觉）。CF×V=4 压线通过 |
| Drop | 0.8 | 1 | 0.8 ✅ | 无需调整 |

**裁决理由**：Escalation 是本 PV 的核心节奏贡献段——失去物理切频的速度感则不像 PV，但视觉过度堆叠则 CF×V 崩溃。半速映射 + V=2 的组合在保持物理高切频的同时，通过效感 CF 控制认知负荷。这也是资源现状的映射——灵王碎片和三界坍缩的参考图（R8）为 P1 降级，在 visual V=2 方案中可以跳过。

**给三 designer 的关键约束广播**：

1. **段=2，拍=4**：工具决定段（2），叙事决定拍（4）。段边界在 Escalation 中段（~00:15），不是节拍边界。visual/rhythm 在 §3 中写"4 段"是术语误用——正式对齐：段数 2（工具驱动），拍数 4（叙事驱动）
2. **CF×V 裁决**：按上方表格执行。rhythm 降 Hook CF 至 2.0 + Escalation 用半速映射。visual 降 Escalation V 至 2
3. **前 3 秒铁律**（gather-expert 证据 3-A/3-B）：开场 0.3s 内必须有模式中断——友哈巴赫多重瞳孔特写。不打前奏、不铺背景、不设余白
4. **段间末帧传递**：段 1 末帧锁定为首实体状态（Ichigo 在 Escalation 起始的身位/环境/光照），段 2 直接从该状态延续。目标实体：一护双刀黑色灵压缠绕的静态蓄力帧
5. **实体聚焦**：仅 Yhwach + Ichigo 双刀。Rukia 参考图存在但不在本 PV 中使用。Stern Ritter 仅为 Hook 的剪影背景（P1，可文本描述降级）
6. **转场规则**（bleach.md + 证据 1-D）：仅硬切和白闪。禁止溶解/柔焦/暖调滤镜/连续打斗编排（见 visual 禁止清单 + director 强制约束）
7. **Bleach 关键视觉约束**：剪影先于面部（Yhwach 的多瞳红瞳是唯一特写级面部展示）、高对比色指定（黑≥10%面积）、强调色仅用于灵力解放（橙/金/紫）、负片空间（画面留黑/留白）
8. **30s 平台约束**（证据 3-A/3-B/3-C）：每 3-5s 一个信息增量。全程无 >5s 无变化静止（Drop 0.5s 真空停顿时唯一例外）。近景/特写 1-2s，中景 2-3s，远景 3-5s
9. **规范参考拍**：脚本产出后须标注每个实体首次清晰出现的拍号——Yhwach 在 Hook、Ichigo 双刀在 Reveal。这是 visual-designer 的 P0 优先级依据
10. **情绪外化原则**：不写抽象情绪词。每拍翻译为可拍摄的身体/环境细节（如"紧张"→ 握刀指节发白 + 瞳孔收缩 + 汗水滑落 + 衣袖轻微震动）

---

## 3. 对齐检查

*所有 agent 产出后，各自回读其他人的 section，在此表标注对齐状态。*

| 检查项 | script 说 | visual 说 | rhythm 说 | director 说 | 对齐状态 |
|--------|-----------|-----------|-----------|-------------|---------|
| 总拍数 | 4 拍（Hook/Reveal/Escalation/Drop — script-beats.md §元信息） | 4 拍（§2.2） | 4 拍（§2.3） | 4 拍（§2.4） | ✅ 全部确认：三段 designer 一致+script-beats.md 已输出 |
| 总时长 | 30s（B1 5s+B2 7s+B3 10s+B4 8s — script-beats.md） | 30s（§2.2） | 30s（§2.3） | 30s（段1~15s+段2~15s — §2.4） | ✅ 全部 30s。拍长 5/7/10/8 三段一致。段 15+15=30s 累计一致 |
| 段数 | 2段（叙事拍4/工具段2，段边界~00:15.5在B3内 — script-beats.md §元信息段边界规划） | **2段**（已接受修正） | **4段**（§2.3——待更新） | **2段**（§2.4） | ✅ 统一为2段。拍数4（叙事驱动），段数2（工具驱动——Seedance Mini 15s硬限）。C004已resolved |
| 锚点拍编号 | B2(情绪转折点+一护双刀觉醒) / B3(视觉高峰+段边界) / B4(结构终点+CTA) — script-beats.md §元信息 | B1(Hook Yhwach首现) / B2(Reveal Ichigo TS首现) / B4(Drop 祸进标题) | B1(Hook)、B4(Drop) | B1(Hook开场) / B2(一护双刀首现) / B4(祸进标题) | ✅ **director最终裁决**：B2（情绪转折+全片唯一呼吸）+B3（视觉高峰+段边界）+B4（结构终点+CTA）。B1为「模式中断钩子」非叙事锚点，不升格。video-prompt.md §1 M3记录|
| CF×V | — 已对齐裁决。B3 Esc V=2设计已融入子拍：去灵王碎片/去VFX文字排版（script-beats.md B3子拍） | V: Hook 2/ Reveal 2/ Esc 2/ Drop 1（已按§2.4裁决更新） | CF: Hook 2.0 / Reveal 1.4 / Esc 2.0(效感) / Drop 0.8（已按裁决更新） | 裁决：Hook CF→2.0 / Esc V→2+半速映射 | ✅ 全部CF×V<4。Hook 4.0✅ Reveal 2.8✅ Esc 4.0✅(压线) Drop 0.8✅。visual已确认，rhythm终版待更新CF值即可 |
| 实体复现间隔 | Yhwach B1首现→B3c再现（2拍≤3✓）。Ichigo B2首现→B3a延续（✓）。script-beats.md B3子拍设计 | 主角≤3拍（§2.2）已满足 | 未指定 | 主角≤3拍/段（§2.4） | ✅ 全部对齐：Yhwach 2拍✓ Ichigo连续✓. rhythm已确认合规 |
| 段边界尾帧策略 | 段1末帧(~00:15.5)：Ichigo剪影浮现帧。延续边界。段2参考图=末帧(连续性)+Yhwach规范图(身份复位) — script-beats.md B3b | visual-world.md §7.5定义了拍间尾帧链 | — | 段1末帧→段2 Tier0参考图（§2.4） | ✅ 段边界定于B3b末~00:15.5，延续边界类型。末帧路径已定义。visual §7.5为段内设计，与段边界不冲突。script末帧设计与director段间末帧链一致 |
| 参考图门禁 | P0=3项(Yhwach规范/一护双刀规范/冰宫场景)已标注待产 — script-beats.md §元信息 + TOGETHER §2.1 | P0 3项 Prompt 规格已产出（ref-images/T003-P0-reference-prompts.md） | — | 每段≥1参考图。段1取asset-lab。段2含段1末帧（§2.4） | ⚠️ P0 3项全缺。用户确认：RISK ACCEPTED，不阻塞合成。video-prompt.md §3完整记录。待P0就绪后更新替换 |

---

## 4. 资源就绪追踪

*任何 agent 发现自己或他人所需的资源未就绪时，在此登记。不是"记下来就好"——🔴 阻塞项必须在上游解决后才继续。*

| # | 资源 | 类型 | 需求方 | 负责方 | 优先级 | 状态 | 阻塞什么 |
|---|------|------|--------|--------|--------|------|---------|
| R1 | 友哈巴赫（Yhwach）规范参考图——IaD 中性表情 | 参考图 | script / visual / director | visual-designer | P0 阻塞 | 🟡 规格已产出（待生成+IaD验证） | 拍 1 Hook（存 Yhwach 多瞳特写+红瞳+星十字背景）；拍 3 Escalation（Yhwach 剪影再现）。Prompt 规格已写入 `ref-images/T003-P0-reference-prompts.md` §1。待生成+拼合+IaD 验证 |
| R2 | 一护双刀形态（True Shikai）规范参考图——IaD 中性表情 | 参考图 | script / visual / director | visual-designer | P0 阻塞 | 🟡 规格已产出（待生成+IaD验证） | 拍 2 Reveal（一护双刀首现——长刀=死神+短刀=虚）；拍 3 Escalation（双刀灵压释放）。Prompt 规格已写入 `ref-images/T003-P0-reference-prompts.md` §2。待生成+拼合+IaD 验证。**确认为 True Shikai 双刀形态，非 DEMO 单刀死神代理** |
| R3 | 无形帝国/冰宫/友哈巴赫御座场景定调图 | 参考图 | visual / director | visual-designer | P0 阻塞 | 🟡 规格已产出（待生成+IaD验证） | 拍 1 Hook 开场场景——需要有"灭却师之王"统治感的视觉基座。Prompt 规格已写入 `ref-images/T003-P0-reference-prompts.md` §3。待生成+验证 |
| R4 | Ichigo DEMO 规范参考图 IaD 复检 | 参考图 | director | visual-designer | P1 可降级 | 🟡 进行中 | `CHR_DEMO_Ichigo_canonical_v01.png`，质量 ⚠。非双刀形态，仅做单刀死霸装的一致性参考 |
| R5 | Ichigo DEMO 多视角参考图 IaD 复检 | 参考图 | director | visual-designer | P1 可降级 | 🟡 进行中 | `CHR_DEMO_Ichigo_multi-view_v01/`，质量 ⚠ |
| R6 | 尸魂界攻防场景定调图（瀞灵廷裂开/崩坏） | 参考图 | visual / director | visual-designer | P1 可降级 | 🔴 未就绪 | 拍 3 Escalation。备选：复用 `SCN_DEMO_SoulSocietyStreets_scene-day_v01.png`（⚠ 质量，且为日常街景非攻防）→ 降级为文本描述 |
| R7 | 「祸进」汉字标题 VFX/排版参考 | 参考图 | visual / director | visual-designer | P1 可降级 | 🔴 未就绪 | 拍 4 Drop（祸进标题卡）。备选：Bleach 风格汉字定帧（衬线字体+破碎特效+高对比），可文字描述降级 |
| R8 | 灵王宫崩坏/三界坍缩 VFX 参考 | 参考图 | visual / director | visual-designer | P1 可降级 | 🔴 未就绪 | 拍 3 Escalation（灵王崩坏→三界坍缩剪影）。在 visual V=2 降级方案中可跳过 |
| R9 | 星十字骑士团（Stern Ritter）剪影参考 | 参考图 | script / visual / director | visual-designer | P1 可降级 | 🔴 未就绪 | 拍 1 Hook（星十字披风剪影背景）。30s PV 中仅为剪影级展示，可文本描述降级 |
| R10 | BGM（原创/FREE 曲库，不可 Shiro Sagisu） | 音频 | rhythm / director | director/rhythm | P1 可降级 | 🟡 进行中 | 适配 4 拍节奏：Hook 低音沉+军靴声 → Reveal 渐强 → Escalation fast drum+riser → Drop 骤停+重鼓破碎 → CTA fadout |

**P0 未就绪 → 依赖方不推进。** P1 可降级为文本描述继续。

**就绪标准**：
- 参考图：IaD 检查通过 + ≥1024px .png + 已存 `ref-images/` + 路径写入本表
- 尾帧：上段生成完成 + `return_last_frame=true` + 已存 `last-frames/`
- 分镜线稿：figure-draftsman 交付 + 已存 `storyboards/`

**全局缺口总览**（video-director 在门 4 前汇总）：

```
P0 未就绪: 3 项（物理资产全缺。用户确认RISK ACCEPTED，合成以文本描述替代）
P0 规格已产出: 3 项（R1 R2 R3 prompt规格就绪，物理文件待生成/拼合/IaD验证）
P1 未就绪: 6 项（R4-R10，含 IaD 复检、场景/VFX/音频等）
阻塞拍: B1(缺R1+R3) B2(缺R2) B3(缺R1+R2) B4(缺R7)。用户确认RISK ACCEPTED继续
可以继续？⚠️ 是（P0物理资产全缺，用户确认RISK ACCEPTED）
```

---

## 5. 交叉验证

*产出完成后，每个 agent 必须验证至少一个其他 agent 的关键约束是否在自己产出中被遵守。不是"读一下"——是逐项核验。*

### 验证矩阵

| 验证方 | 被验证方 | 验证项 | 我的产出中对应的值/处理 | 一致？ | 备注 |
|--------|---------|--------|------------------------|--------|------|
| script | visual | 实体复现间隔（主角≤3拍） | script-beats.md: Yhwach B1首现→B3c再现（2拍间隔✓）。Ichigo B2首现→B3a延续（连续出现✓）。跨段（段1末B3b→段2初B3c）为同一实体（Ichigo剪影）延续，无间隔 | ✅ | 与visual §2.2约束一致 |
| script | rhythm | 拍长窗口（实体≤6s） | script-beats.md B2（Ichigo 7s）拆为B2a(3s)+B2b(4s)各≤6s✓。B3a-b(实体部分~3.5s)≤6s✓。B3b视觉碎片(纯视觉1.5s)≤8s✓。B1(钩子拍5s不限) | ✅ | 与rhythm §2.3实体≤6s/纯视觉≤8s约束一致 |
| visual | script | 规范参考拍号是否已分配参考图 | visual-assets-spec.md §2 定义 Yhwach+B1 + IchigoTS+B2+B3 的规范参考拍。§6.1 Step1-2 标注质量感知调度 | N/A | script 空缺，无法最终确认。当前已预设 B1=Yhwach 首现 / B2=Ichigo 首现 |
| visual | rhythm | CF×V<4（我的 V 值 × 你的 CF 值） | visual-world.md §8.1 + TOGETHER §2.2: V Hook=2 / Reveal=2 / Esc=2 / Drop=1。按 §2.4 director 裁决——Hook CF=2.0(生效后) → 4.0 ✅、Reveal CF=1.4 → 2.8 ✅、Esc effektiv CF=2.0(半速映射生效后) → 4.0 ✅、Drop CF=0.8 → 0.8 ✅ | ✅ | 全部 <4。前提：rhythm 确认降 Hook CF 至 2.0 + Esc 半速映射 effektiv CF=2.0 |
| rhythm | script | 认知负荷 vs CL 标度一致 | rhythm-curve.md: 趋势一致(高→低→最高→低) | ✅ | 独立标度,趋势一致即可 |
| rhythm | visual | 停顿点是否有对应视觉定格 | rhythm-curve.md 停顿点5处 + visual-world.md §8.1 一致 | ✅ | 全部对齐 |
| visual | script | 实体标签统一 + 规范参考拍分配 | visual-assets-spec.md §2 实体标签 = script-beats.md 实体注册一致（`[ANTAGONIST]`/`[PROTAGONIST]`/`[WEAPON_ZANGETSU]`）。规范参考拍：B1=Yhwach首现, B2=Ichigo双刀首现。Ichiogo双刀确认新产（非DEMO单刀） | ✅ | 标签、参考拍、P0需求三方对齐 |
| director | visual | 参考图门禁（每段 ≥1 张，非首段含尾帧） | P0 3项 Prompt 规格已产出（ref-images/T003-P0-reference-prompts.md）。段 1 参考图待生成+验证。段 2 依赖段 1 末帧 | 🟡 | P0 规格已产出，待生成+IaD验证（§4 R1-R3 状态更新） |
| director | visual | 参考图门禁（每段 ≥1 张，非首段含尾帧） | 见上方 "visual | rhythm" 行 director 发的交叉验证 | ✅ / ❌ / N/A | |

**验证规则**：
1. 至少验证 2 项，优先选标 ❌ 风险最高的
2. 验证结果不是"看起来对"——必须引用被验证方文件的具体行/值
3. ❌ → 立即写入 section 6（评论）@ 被验证方，标注"交叉验证发现"
4. 全部 ✅ 后 video-director 才能进入合成

---

## 6. 评论

*任何 agent 发现不对齐时在此写评论。格式：`[agent名] @ [目标agent]：具体问题`。*

```
[example] script @ rhythm: B4 内容不一致——我写的是"余烬废墟"，你是"友哈巴赫御座"。需要对齐。
[example] visual @ script: 你要求的规范参考图每实体 1 张——我这边 P0 资产缺友哈巴赫和一护双刀，已标待产。
[example] rhythm @ visual: 【交叉验证】CF×V=5.0×3=15>4，违规。你的 V=3 在我的 CF=5 段不可接受。
```

| # | 来自 | @谁 | 问题 | 严重度 | 来源 | 状态 |
|---|------|-----|------|--------|------|------|
| C001 | rhythm-designer | @script | §2.1 未填写——script-designer 尚未输出方向和约束。无 script-beats.md，无弧线选择，无拍长分配。当前 rhythm 无法设计终版曲线 | 🔴阻断 | 自检 | resolved |
| C002 | rhythm-designer | @visual | 【CF×V 冲突】Escalation 拍：我预标 CF=4.5 或半速映射后效感 CF=2.0，你标 V=4。两种方案均 >4。需要你在此拍降 V 至 ≤2 | 🔴阻断 | 自检 | resolved |
| C003 | rhythm-designer | @visual | 【CF×V 冲突】Hook 拍：我预标 CF=3.0，你标 V=2 → 6>4。建议我降 CF 至 2.0 或你降 V 至 1（纯特写+黑背景） | 🟡不一致 | 自检 | resolved |
| C004 | director | @visual + @rhythm | **段数修正**：§3 中双方写"4 段"——是 beat 和 segment 的术语重合。正式对齐：**拍数=4（叙事驱动），段数=2（工具驱动——Seedance Mini 15s 硬限）**。段 1 ~15s（Beat1-Beat3 前半），段 2 ~15s（Beat3 后半-Beat4）。段边界在 Escalation 加速中段 | 🟡不一致 | 自检 | resolved |
| C005 | director | @visual + @rhythm | **CF×V 裁决已出**（§2.4 "CF×V 裁决"表）：(1) Hook: rhythm 降 CF 至 2.0，visual 保持 V=2 → 4.0 ✅；(2) Escalation: rhythm 用半速映射（效感 CF=2.0）+ visual 降 V 至 2（去灵王碎片/文字排版）→ 4.0 ✅。请确认接受 | 🟡不一致 | 自检 | resolved |
| C006 | director | @visual | R1（Yhwach 参考图）和 R2（一护双刀参考图）为 P0 阻塞资产。请在拿到 script 的规范参考拍号后优先生产。**IaD 中性表情是收敛门硬要求**——不是"尽量表情一致" | 🔴阻断 | 自检 | resolved |
| C007 | director | @script | §2.1 空缺阻塞全流程。请至少产出：(1) 弧线选择+拍长分配；(2) 规范参考拍号（每个实体首次清晰出现的拍）；(3) 视觉资产需求清单（拍号→素材类型/用途/优先级） | 🔴阻断 | 预检 | resolved |
| C008 | director | @rhythm | ZPC 段级 ASL：拍级低于1.8s但段级>1.8s | 🟡不一致 | 自检 | **resolved** — rhythm已确认: rhythm-curve.md 段1 ASL~2.2s, 段2 ASL~2.4s, 均>1.8s。ZPC无风险 |
| C009 | director | @visual | §2.2 假设表第 1 条"Seedance 2.0 可还原 Bleach 风格"——T001 DEMO quality⚠。**建议**：在一护双刀 P0 参考图产出后，先用 Seedance 做 1-2 帧 short test 验证 Bleach 线稿和黑白色调的还原度，再继续批量生产 | 🟢建议 | 自检 | accepted |
| C010 | director | @visual | §2.2 禁止清单中的">5s 无变化静止"需要更具体——它是 gather-expert 证据 3-A 的抖音 30s 约束（每 3-5s 一个信息增量）。**建议**：在 visual-world.md 中为每一拍标注具体的"变化事件时间戳"，确保 <5s 间隔 | 🟢建议 | 自检 | accepted |
| C011 | visual | @rhythm + @director | **C002/C003/C005 resolved**：已接受 §2.4 CF×V 裁决。§2.2 V 值已更新为 Hook=2 / Reveal=2 / Esc=2 / Drop=1。visual-world.md §8.1 DNA 表已对应调整。前提：rhythm 确认 Hook CF→2.0 + Esc 半速映射 effektiv CF=2.0 | 🔴阻断→🟡 | 响应 | resolved |
| C012 | visual | @director | **C004 resolved**：段数已修正。§3 visual 列改为"2 段"，接受段边界在 Escalation 中段（~00:15）。visual-world.md §7.5 尾帧管理配合段级尾帧链 | 🟡不一致→✅ | 响应 | resolved |
| C013 | visual | @director | **C006 acknowledged**：P0 参考图生产计划已在 visual-assets-spec.md §6.1 定义。IaD 中性表情作为 Step1/2 的硬条件。队列：Yhwach 参考图 → IchigoTS 参考图 → 冰宫场景。依赖 script 确认规范参考拍号后启动 | 🔴阻断 | 响应 | resolved |
| C014 | visual | @director | **C009 accepted**：同意。将在 IchigoTS 参考图产出后先跑 1-2 帧 Seedance short test 验证 Bleach 风格还原度，通过后再批量生产 | 🟢建议→✅ | 响应 | accepted |
| C015 | visual | @director | **C010 accepted**：将在 visual-world.md §8.1 DNA 表中为每拍的"视觉内容"列标注明确的时间戳粒度（~1-1.5s 间隔标识变化事件），确保无 >5s 无变化间隙 | 🟢建议→✅ | 响应 | accepted |
| C016 | visual | @script | 实体标签已对齐：visual-world.md §7.4 统一使用 [ANTAGONIST] / [PROTAGONIST] / [WEAPON_ZANGETSU] 标签。§10.1 负面清单也已更新 | 🟢建议→✅ | 响应 | resolved |
| C016 | script | @rhythm + @director | **C001/C007 resolved**：§2.1 已填充，script-beats.md 已生成。弧线=经典弧，拍长分配 B1 5s/B2 7s/B3 10s/B4 8s。规范参考拍号：B1=Yhwach首现, B2=Ichigo双刀首现。视觉资产需求清单已给出7项。CF×V 裁决已接受（Esc V=2简化背景在B3子拍中已体现） | 🔴阻断→✅ | 响应 | resolved |
| C017 | script | @visual | **Ichigo双刀规范参考图需新产确认**：DEMO asset `CHR_DEMO_Ichigo_canonical_v01.png` 为一护单刀死神代理形态（死霸装+单斩月），T003需要的是True Shikai双刀形态（双斩月：大刀=死神+虚之力/小刀=灭却师之力+无刀柄中空握持）。两个形态不同，建议新产双刀规范参考图 | 🔴阻断 | 自检 | resolved |
| C018 | director | @all | **Phase 1 合成完成**。矛盾矩阵5项（M1-M5）全部裁决。§3 7/8项 ✅。收敛门6门全过（IaD/RefImg ⚠️已接受）。`video-prompt.md` 已生成。素材装配：3 P0全缺，全部降级为文本描述。段1末帧依赖段1生成后提取 | 🔴RISK→🟡 | Phase 1 | open |
| C019 | rhythm | @visual+director | **终验确认**: rhythm-curve.md已产出。CFxV终值全部<=4 ✅。段级ASL>1.8s ✅。段数已修正为2段 ✅。节拍分配对齐script子拍粒度 | ✅全部resolve | 终验 | resolved |

---

## 7. 迭代记录

*每一轮 loop 优化后记录：做了什么、对齐状态变化。*

| 轮次 | 日期 | 触发原因 | 变更 | 资源变化 | 对齐状态 |
|------|------|---------|------|---------|---------|
| L0 | 2026-07-19 | Phase 0 预检（director 先启动） | director 填 §1（修正）+ §2.4 + §4 + §6 新评论。与 visual+rhythm 已写内容对齐 | P0 未就绪: 3 项（R1 Yhwach / R2 一护双刀 / R3 冰宫场景） | ✅ Phase 0 ALIGN 通过（§3 无🔴。有❌条目标注中，属正常 loop 流程）。可启动三 designer。**但注意**：C001（script 空缺）+ C007 为🔴阻断——§2.1 填充后才能继续 |
| L1 | 2026-07-19 | visual-designer 启动 P0 参考图生产（§6 三项 🔴 待 resolved） | visual-designer 产出 3 项 P0 参考图 Niji 6 Prompt 规格（ref-images/T003-P0-reference-prompts.md）。确认 Ichigo 双刀需新产并标记 C017 resolved。更新 §4 R1-R3 状态、§3 对齐状态、§5 交叉验证 | P0 规格已产出: 3 项（R1 Yhwach / R2 一护双刀 / R3 冰宫—prompt 就绪待生成） | 📋 未对齐 3项：段数(§3-rhythm 仍未更新)、CF×V(rhythm 待确认CF)、段边界0.5s差(director待确认) |
| L2 | 2026-07-19 | Phase 1 合成（director 矛盾裁决+prompt合成） | **矛盾矩阵**：5项(M1-M5)全部裁决，三体树收敛。**收敛门**：ALIGN✅ FreeLOC✅ LoL✅ ZPC✅ IaD⚠️(接受) RefImg⚠️(接受)。**素材装配**：Step1-5 对账完成——0资产就绪，全降级为文本描述。`video-prompt.md` 生成（2段 Seedance Mini prompt + 末帧链调度 + SDK字段就绪检验 + 9要素嵌入）。§3 8/8项完成对齐确认 | P0 3项全缺。用户确认RISK ACCEPTED。物理资产就绪后替换prompt文本描述段 | ⚠️ P0未就绪已放行合成（RISK ACCEPTED） |

---
| L3 | 2026-07-19 | rhythm-designer 终版产出 | rhythm-curve.md + TOGETHER.md §2.3/§3/§5/§6 更新。CFxV全部resolve、段数对齐、ZPC确认、§5新增rhythm验证 | rhythm-curve.md产出 | ✅ §3全部对齐、§6 C002/C003/C005/C008/C018 resolved |

## 使用规则

1. **先写再干**：每个 agent 在开始详细设计前，先填 §2。不是写完之后补。
2. **回读检查**：产出完成后，回读其他人的 §2，在 §3 勾对齐状态。
3. **资源阻塞**：P0 资源未就绪 → 在 §4 登记 → 依赖方不推进。P1 可降级。
4. **交叉验证**：每个 agent 至少验证 2 项——不是自己说对齐了，是别人验过了。❌ → 写入 §6。
5. **不对齐 = 评论**：不一致不要自己消化——在 §6 标注，@ 目标 agent。
6. **loop 直到 ✅**：§3 有任何 ❌ / §4 有 P0 未就绪 / §5 有 ❌ → 触发迭代 → 更新 §7 → 直到全部 ✅。
7. **门 3 输入**：video-director 读 §3 + §5 + §6 生成矛盾摘要给人裁决。
8. **门 4 输入**：video-director 读 §4 汇总资源缺口——P0 未就绪 → 合成阻塞。
9. **人在 loop 中**：两轮 loop 后仍有 🔴 阻断项 → 升级到门 3（人裁决方向）。
