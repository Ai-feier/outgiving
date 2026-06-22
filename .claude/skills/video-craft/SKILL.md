---
name: video-craft
description: AI 视频创作的元知识 — 剧本/主体/节奏三元素相互成就的认知框架。不是工序流水线，是理解 AI 视频创作本质的底层知识。独立于文本 pipeline，共享选题 brief。
argument-hint: "[new|design|direct|style]"
---

# video-craft — AI 视频创作元知识

## 和 content-pipeline 的关系

```
选题 brief + outline（共享层）
        │
        ├─ content-pipeline ─→ 4 平台 writer agent ─→ 文本产出
        │
        └─ video-pipeline  ─→ 3 设计师 agent ─→ video-director ─→ AI 视频 prompt
```

两个 pipeline **独立运行**，共享 brief 里的核心观点、受众、钩子、关键信息点、视觉资产规划。文本走"写作"心智，视频走"导演"心智——不是同一件事，不该用同一套流程。

## 核心设计哲学

AI 视频创作的本质是**导演**，不是编剧。

三个设计维度——剧本、主体、节奏——不是三个步骤，是**相互成就的三个力**。它们同时存在、互相约束、一起呼吸：

- **剧本**决定了什么在发生、什么顺序、什么情绪递进 → 给主体制造了"需要看见什么"的需求
- **主体**定义了视觉世界的一致性法则 → 反过来约束剧本"什么可以在这个世界里发生"
- **节奏**是两者的呼吸——剧本的情绪曲线通过节奏具象化，主体的视觉复杂度通过节奏被消化

改变任何一个，另外两个必须重新调谐。三者在矛盾和对位中找到平衡——这个平衡点就是创作。

**风格**是贯穿三者的元参数——同一个剧本在"纪录片"和"动画"风格下，主体和节奏完全不同。

## 工作流

```
brief → outline → video-style（可选，该选题的视觉美学偏好）
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
  script-designer      visual-designer       rhythm-designer
  叙事架构               视觉世界               时间呼吸
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                       交叉对话，互洽调谐
                              │
                              ▼
                       video-director
                        三元素合成
                        + 风格参数
                              │
                              ▼
                      AI 视频生成 prompt
                   （Sora / Runway / Kling / ...）
```

三元素 agent 不是串行——它们拿到 brief 后**并行设计**，然后在 video-director 处交叉对话：剧本说我需要这个情绪，节奏说你给的节拍太少我呼吸不过来，主体说你们要的那个场景在我的视觉世界里不成立——这些矛盾正是创作发生的地方。

## Agent 清单

| Agent | 角色 | 本质 |
|-------|------|------|
| [script-designer](agents/script-designer.md) | 剧本设计 | 叙事架构——信息以什么顺序、什么情绪递进被接收 |
| [visual-designer](agents/visual-designer.md) | 主体设计 | 视觉世界——观众在整个视频中看见的世界的统一性 |
| [rhythm-designer](agents/rhythm-designer.md) | 节奏设计 | 时间呼吸——信息密度和情绪密度的曲线 |
| [video-director](agents/video-director.md) | 导演合成 | 三元素互洽 → AI 视频生成 prompt |

## 风格参考

[风格库](references/styles.md) — 电影感 / 纪录片 / Vlog / 动画 / 数据叙事。选题自己的 `video-style.md` 优先于风格库。

## 命令

```bash
# 为已有选题初始化视频产出目录
uv run --directory scripts content adapt <T0XX> douyin  # 先有抖音脚本
# 视频 prompt 输出到 platforms/douyin/T0XX-*/video-prompt.md
```

## 输出

每个选题的视频产出放在 `platforms/douyin/T0XX-<slug>/` 下（与抖音脚本同目录）：

- `video-prompt.md` — 合成的 AI 视频生成提示词
- `script-beats.md` — 剧本节拍（script-designer 产出）
- `visual-world.md` — 视觉世界定义（visual-designer 产出）
- `rhythm-curve.md` — 节奏曲线（rhythm-designer 产出）
