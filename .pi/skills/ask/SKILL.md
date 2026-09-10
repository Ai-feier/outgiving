---
name: ask
description: 内容生产的唯一入口。收到任何「做一条内容」的请求时先读本文件：先判定现在在哪个流程阶段，再路由到该阶段的方法 skill；只有创作阶段按交付形态（文本 / 视频）分叉。阶段定义、产出与人审点见 system/PRODUCT.md「流程骨架」，本文件只做路由。
---

# ask — 入口路由

任何内容生产请求从这里进来。本文件只做一件事：**判断现在在哪个阶段 → 指向该阶段的方法 skill**。

阶段顺序、每阶段产出与人审点见 [`system/PRODUCT.md`](../../../system/PRODUCT.md)「流程骨架」——本文件不复述，只引用。

## 路由表

| 阶段 | 路由到 | 交付 |
| --- | --- | --- |
| 研究 | [`research-evidence`](../research-evidence/SKILL.md) | 证据锚点表 |
| 结构 | [`narrative-structure`](../narrative-structure/SKILL.md) | 骨架表（信息点序列） |
| 创作·文本 | [`writing-craft`](../writing-craft/SKILL.md) | 成稿 |
| 创作·视频 | 下方「创作·视频」四张 | 分镜表 + 提示词 |
| 视觉 | [`visual-assets`](../visual-assets/SKILL.md) · [`asset-search`](../asset-search/SKILL.md) | 资产 / 关键帧 / 参考素材 |
| 校验 | [`verify-checklist`](../verify-checklist/SKILL.md) | 逐条核对表 |
| 收尾 | [`reflecting`](../reflecting/SKILL.md) | 复盘与基础设施精进 |

研究与结构两形态共用同一份产出——**只有创作阶段按形态分叉**。视觉按形态并行，不单独成阶段。

### 创作·视频

一张分镜表由四条线共同决定，缺一条就出不了表：

| 线 | skill |
| --- | --- |
| 镜头语言（景别 / 运镜 / 角度 / 光影 / 转场） | [`shot-language`](../shot-language/SKILL.md) |
| 节奏（每拍秒数 / 切频 / 停顿点） | [`rhythm`](../rhythm/SKILL.md) |
| 视觉世界（形态 / 材质 / 环境 / 角色一致性） | [`visual-world`](../visual-world/SKILL.md) |
| 提示词（公式 / 字段映射 / 工具能力边界） | [`prompt-engineering`](../prompt-engineering/SKILL.md) |

## 渠道是参数，不是路由轴

渠道表 [`channels/CHANNELS.md`](../channels/CHANNELS.md) 与渠道卡 `channels/<channel>.md` 在**每个阶段**被读为参数：研究阶段读渠道卡的读者注意状态，创作与校验阶段读渠道表的共有维度。

路由不按渠道分——**新增渠道只新增一张卡**，不改本文件、不加阶段、不加岗位。

## 执行

状态推进、生成、渲染、检查全部走 `scripts/`，本文件不复述命令。入口命令两组：

```bash
uv run --directory scripts content   # 选题与产出的数据操作
uv run --directory scripts ai        # 图像 / 视频生成与校验
```

## 真例

**输入**（真实项目 T006，创作·视频阶段）：

> T006 请大佛开口，抖音 60s 竖屏，证据表与骨架表都已过人审，开始排分镜。

**路由**：

1. 阶段 = 创作·视频 → 本文件「创作·视频」四张全读（节奏定秒数、镜头语言定景别运镜、视觉世界定角色一致性、提示词工程把画面转成生成输入）。
2. 渠道参数 = `douyin` → 读 [`channels/CHANNELS.md`](../channels/CHANNELS.md) 的 douyin 行（时长、感知组块上限、钩子位置）与 [`channels/douyin.md`](../channels/douyin.md) 的读者注意状态。共有维度的数值只在渠道表定义一处，本文件不复述。

**输出**：`products/T006-请大佛开口/review.md`——12 拍分镜表（拍 / 秒 / 画面 / 景别 / 运镜 / 台词），表下固定三块「关键决策 · 未锚假设 · 待你拍板」。全片 60s，第 1 拍 3s 是具体画面（香火燃起），不用概念开场。
