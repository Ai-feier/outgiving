# 视频管线

> 权威源：`ai-video/DESIGN.md`（链模型 + 写作规格）+ `.claude/agents/video-director.md` + `.claude/skills/video-craft/SKILL.md`——本文为人读摘要。

## 管线全景

```
选题 brief + 视觉风格
  → goal ① 验收标准（人放行 = 层边界审批）
  → 中间单元（research / script / visual / rhythm 等，按 goal ③ 计划动态生成）
  → 收口单元（video-director：矛盾裁决 + 对齐自报总检，gate: 是）
  → 运行单元（segN：prompt 装配 + 成本门 + Run 卡）
  → end（验收表逐条回答 goal ① + 交接下一层）
```

与文本管线独立运行，共享选题 brief（核心观点/受众/钩子/关键信息点）。每层一份契约：goal 立标准 ⇔ end 交答卷；人的触点 4 个：改 ① / grill ② / 过门 / 验收 end（DESIGN.md §2.8）。

## 三元素分工（中间单元 = 一次 AI 事务，交付在 ③）

| 角色 | 单元文件 | 本质 |
| ------ | ------ | ------ |
| script-designer | `script.md` | 叙事架构：弧线 → 节拍 → PAD 情绪递进；节拍被 AI 双重消费 |
| visual-designer | `visual.md`（+ visual-assets-spec 交付件） | 视觉世界：六维 + 材质 + 锚点 + 情绪动作化 + 资产沉淀 |
| rhythm-designer | `rhythm.md` | 时间呼吸：信息密度 × 认知负荷 × 停顿；平台基线 |
| video-director | `director.md`（收口单元，gate: 是） | 三元素对位 + 矛盾裁决 + 收口门 + 工具适配（最终裁决） |

对齐自报在各设计单元 ⑤（回读其他单元 ③ 后逐项 🔴/🟡/✅）；🔴 未关闭 → grill 对方 ② 或触发收口单元门（DESIGN.md §2.8）。

## 工作区与门

- 所有视频设计文件在 `ai-video/projects/TXXX/`（一个单元一份 md，带 `unit:`/`层:` frontmatter；`topics/` 只保留 brief 共享层）
- 门 = 层边界审批（goal ① 放行）+ 单元 `gate: 是`（research / 收口 / 运行单元）；门内容参考 + T001 代价表见 DESIGN.md §4.3
- 收敛门不变量（prompt 级）：FreeLOC（自包含锚点）/ LoL（段边界复位）/ ZPC（ASL≥1.8s）/ IaD（中性表情）/ RefImg（每段 ≥1 参考图）
- 生成后自评估：`ai verify`（ffprobe + 关键帧抽样），3 轮上限；交付前独立 subagent 终审（7 维度）
- 构图安全边界：左右 ≥10%，上下 ≥8%

## 参考图铁律

- 生图 1-3 张参考；生视频 3-7 张（API 硬上限 9；>7 帧过密降质量，KeyFrame-Compass）
- 参考图先下载到 `ai-video/projects/TXXX/assets/ref-images/`；prompt / 门必须声明参考图清单
- 非首段必用前段末帧（尾帧链，`last-frames/`，Tier 0 不计入配额）；场景切换用场景定调图替代
- 工作台（ai-video）→ 图书馆（assets/）：验证通过后晋升，命名转全局规范；尾帧选题结束即清理

## 生成引擎

### Seedance 2.0（默认，火山引擎）

- 9 要素 prompt：`[景别]+[主体+动作+实体tag]+[场景]+[光影]+[运镜]+[风格+画质]+[间]`（[间] 为独创第九要素，日系必填）
- 单段硬限 15s（CLI 适配器）；参考图 ≤9
- 版权过滤器：拦截**特征组合**而非单角色名（如「橙发+黑长袍+双刀」→Bleach），规避策略见 video-director.md

### H3 (MiniMax) — 第二引擎

切换：`VIDEO_PROVIDER=minimax_h3` / `model_config.json`。语法权威源为外部 skill `.agents/skills/h3-prompt-writing/`（MiniMax 官方，skills-lock.json 锁定）——项目不复制语法，只做映射。

- **输入模式与段边界映射**：延续边界段 → I2VA（前段末帧为 `<Picture 1>` @0.00s 全引用）；首尾双锚段 → FL2VA；收束段 → L2VA；多角色/多参考 → Ref2VA（`subject_definitions` + `retention_analysis`，GroundShot 落点）；纯文本 → T2VA
- **三核心字段**：`integrated_multimodal_description`（[Shot N] 时间线）/ `overall_soundscape`（环境+物理声）/ `non_diegetic_music`（BGM）——原生音频字段是相对 Seedance 的核心差异
- **9 要素 → H3 映射**与参考标签协议（`<Picture/Subject/Video/Audio N>`）见 video-director.md「H3 输出分支」
- **[待实测]**：API 字段 / 时长上限（skill 要求匹配 4-15s）/ 参考数量 / 中文 / 版权过滤器 / 成本——实测后回填
