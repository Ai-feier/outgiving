---
name: prompt-engineering
description: 把分镜与视觉设计转成生成工具的提示词——9 要素公式、字段映射、全局一致性前缀、负向提示、9:16 竖屏契约、成本门与工具能力边界。写或评审视频生成提示词时使用。
---

# 提示词工程

把已经定好的镜头语言、视觉世界与节奏转成一个工具能执行的提示词。工具能力边界（各工具支持哪些运镜、单段上限、参考图槽、价格）在 [`tools.md`](tools.md)——本文件写公式与规则。

## 9 要素公式

```text
[景别] + [主体] + [动作] + [场景] + [光影] + [运镜/动] + [风格] + [画质] + [间]
```

对齐官方 8 要素，`[间]` 为第九要素（沉默/停顿，非零）。每拍至少含景别 + 运镜 + 角度（见 [`../shot-language/SKILL.md`](../shot-language/SKILL.md)「每拍必达三要素」）。

**映射到工具字段**（Seedance 适配器）：

| Prompt 要素 | 字段 |
| --- | --- |
| 景别 + 场景 | `scene` |
| 主体 + 动作 + 实体标签 | `subject` |
| 运镜 | `camera` |
| 光影 | `lighting` |
| 风格 + 画质 | `style` |
| `[间]` | 无独立字段 → 嵌入 `subject`/`scene` 文本末尾，如 `still 2s then pan right` |
| 负向提示 | `negative_prompt` |
| 时长 | `duration_hint`（整数，受工具单段上限约束） |

不可映射的要素用自然语言嵌入文本补偿。映射失败 = 工具不支持该维度 → 换表达或换工具，不反向适配。

## 全局一致性前缀

每段 prompt 头部放同一段**全局前缀**，声明整段共享的世界状态：风格、画质基调、实体标签注册、跨拍不变量（角色外观/光源方向/色调/材质语言）。各拍 prompt 只写这一拍的变化量。前缀是跨拍一致性的主要杠杆——同一前缀让模型把每拍认成同一个世界。

## 负向提示

3-5 词最佳；超 8 词改正向约束。默认模板：

```text
no text overlays, no watermarks, no blur, no low detail, no flat lighting
```

分层防护：结构 → `no deformed hands/fingers/faces`；运动 → `no flicker/jitter/warping`；身份 → `no extra characters/face swapping`。工具差异见 tools.md——有独立负向字段的写字段，只接受正向的工具用正向替代（如 `black not white`）。

## 9:16 竖屏契约

视频输出为 **9:16 竖屏**。在只按风格行推断画幅的工具里，必须在 `style` 行显式写 `9:16` / `portrait`；要横版时反而不能出现该字样。安全边界（左右 ≥10%，上下 ≥8%）是构图约束，见 [`../visual-world/reference.md`](../visual-world/reference.md)。

## 成本门

**每次生成前过成本门**：由 `--dry-run` 预览请求体与估算成本，人确认后才真跑。单段成本 = 时长 × 单价（见 tools.md）。批量生成前列出逐步成本，任一步超预算即停。

## 工具特殊分支：H3

工具 = H3（MiniMax）时，语法权威源是外部 skill [`../h3-prompt-writing/SKILL.md`](../h3-prompt-writing/SKILL.md)（`.pi/skills-lock.json` 锁定）——项目不复制其语法，只做映射：9 要素 → `integrated_multimodal_description`（`[Shot N]` 时间线）+ `overall_soundscape` + `non_diegetic_music`；参考图/视频/音频用 `<Picture N>`/`<Video N>`/`<Audio N>` 标签，跨节一致。

## 例子

输入（拍 3 的镜头语言 + 视觉世界 + 节奏）：

> `景别: MCU` · `运镜: slow dolly-in` · `角度: slight low angle` · 画面「鲸鱼娘端白米饭上高台，抬头」· 实体标签 `<whalechan>` · `[间]` 拍末 0.5s

输出（Seedance prompt 五行）：

```text
scene: 暖光高台供桌，暖色尘粒与香火灰飘落，背景人群稀疏虚化；单一连续四秒镜头，无转场。
subject: 蓝白女仆 Whale-chan（白发渐变、鲸鳍耳、呆毛、鲸尾）双手端着盛满白米饭的木碗登上高台，抬头望向画外高处的 Astra 娘；身体仰慕而脚步迟半拍，嘴唇抿紧；结尾静止 0.5s。实体绑定 <whalechan>。
camera: MCU，slow dolly-in，slight low angle；复合运动拆为纯推近，无横摇。
lighting: warm practical lamp 照亮供品，人物半在暗处，soft fill 补面部，长影。
style: 2D anime cel shading，9:16 portrait，sharp line art，moderate saturation，9:16 竖屏；no dialogue, no on-screen text, no subtitles。
```

负向：`no text overlays, no watermarks, no blur, no deformed hands, no extra characters`
