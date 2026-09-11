# 镜头语言词汇表

本文件是全线唯一的镜头语言术语源。任何一个岗位提到景别/运镜/角度/光影名，含义以本表为准。工具支持状态见 [`../prompt-engineering/tools.md`](../prompt-engineering/tools.md)——本表只定义"是什么、什么时候用"。

## 景别 7 级

| 标记 | 名称 | 功能 |
| --- | --- | --- |
| EWS | 极远景 | 建立空间/环境/孤寂感 |
| WS / Full shot | 全景/全身 | 全身+环境/动作空间 |
| MWS / Cowboy | 中全景 | 膝上/人物+环境/西部经典 |
| MS | 中景（腰上） | 对话/中性叙事 |
| MCU | 中近景（胸上） | 情绪+环境上下文 |
| CU | 特写（面部） | 情感聚焦/细节 |
| ECU / Macro | 极特写 | 眼睛/纹理/产品细节 |

## 运镜 15 种

单拍一种主导运镜。复合运动拆时序——`Start: slow dolly-in. Then: gentle pan right for final 2s`。速度只用 slow / medium / fast。

| 运镜 | 描述 | 使用场景 |
| --- | --- | --- |
| Static locked shot | 固定机位 | 对话/纪实/稳定情绪/停顿点 |
| Dolly-in / Push-in | 推近 | 强调/揭示/情感推进 |
| Dolly-out / Pull-back | 拉远 | 揭示环境/孤立/结束 |
| Orbit / Arc shot | 环绕 | 产品展示/角色登场（需指定方向+半径） |
| Tracking shot | 跟拍 | 侧面/前后跟随运动 |
| Pan left/right | 横摇 | 空间揭示/扫视 |
| Tilt up/down | 竖摇 | 角色登场/空间垂直揭示 |
| Crane up / down | 升降 | 规模揭示/上帝视角 |
| Handheld / Gimbal | 手持/稳定器 | 沉浸/纪实感 |
| Rack focus | 变焦点 | 注意力跨平面转移（需搭配景深描述） |
| Whip pan | 快速横摇 | 转场/能量爆发 |
| Parallax lateral pan | 视差横移 | 深度空间展示（需前景/中景/背景三层） |
| Hitchcock zoom | 滑动变焦 | 眩晕/紧张/揭示（需复合描述） |
| First-person POV | 第一人称 | 主观视角/沉浸 |
| Dutch angle | 荷兰角（倾斜构图） | 不安/失衡/心理压迫 |

**运动语法**：单拍一种主导运镜。push-in 的落幅须有足够视觉密度，否则推到最后信息不够。

## 角度 6 种

| 角度 | 心理效果 |
| --- | --- |
| Eye level | 中性/客观/纪实感 |
| Low angle | 力量/英雄感/压迫/宏大 |
| High angle | 脆弱/被审视/概览 |
| Over-the-shoulder (OTS) | 第三人称/对话 |
| Dutch angle | 不安/失衡/心理扭曲 |
| Bird's eye | 上帝视角/抽象 |

## 光学与景深

**焦距桶**

| 焦距 | 效果 |
| --- | --- |
| Wide (24-28mm) | 沉浸/空间夸张/渺小 |
| Normal (35-50mm) | 自然/中性/纪实（通用默认） |
| Telephoto (85mm+) | 亲密/压缩背景/主体突出 |

**景深语法**：shallow DOF（电影感/主体聚焦）；deep focus（信息量/全景清晰）；rack focus（注意力跨平面转移，prompt 写成 `focus shifts from foreground to face`）。

**特殊光学**：anamorphic（宽银幕/水平炫光，标注 `anamorphic lens`）；tilt-shift（微缩模型，标注 `tilt-shift miniature effect`）。

模型对焦距数值理解弱（认识 close-up，不认识 85mm）——景别词优先，焦距作补充标注。

## 光影语法

情绪词对 AI 无意义。每拍用具体光照条件和摄影术语替换抽象情绪。

**自然光**：golden hour（暖/长影/浪漫/史诗）· blue hour（冷/静谧/忧郁）· overcast（柔和/无阴影/纪实）· harsh noon sun（强对比/紧张）· moonlight（低照度/冷/神秘）

**可控光**：high-key（明亮/均匀/商业）· low-key（高对比/戏剧/悬疑）· Rembrandt（三角光/油画感）· split（半明半暗/二元冲突）· butterfly/paramount（时尚/对称）· loop（自然人像/轻微侧光）

**边缘/特殊光**：rim / backlight（轮廓分离/剪影）· volumetric / god rays（光束/穿透/尘埃）· practical（画面内光源：台灯/霓虹/蜡烛/屏幕光）· side light（纹理揭示/立体感）· ambient occlusion（阴影层次/深度感）

**光照-情绪速查**（把情绪翻译成光照条件）

| 情绪 | 光照条件 |
| --- | --- |
| 希望 | golden hour backlight + warm amber |
| 绝望 | low-key + hard overhead + deep shadows |
| 孤独 | blue hour + single practical lamp + long shadows |
| 悬疑 | low-key + split lighting + volumetric dust |
| 力量 | rim backlight + low angle + god rays |
| 亲密 | warm practical lamp + shallow DOF + soft fill |
| 科技/冷 | blue hour + cool neon + hard edge shadows |
| 回忆 | soft overcast + slight bloom/halation + muted palette |

## 转场 6 种

| 转场 | 时长 |
| --- | --- |
| 硬切 | 0s |
| 交叉溶解 | 0.5-1.5s |
| 渐黑白 | 1-2s |
| 匹配剪辑 | 0s |
| 音频先行 | 0.3-1s |
| 快速横摇（whip pan） | 0.3-0.5s |

动作低缓连续是跨风格基础原则——快速运镜增加 motion blur 与身份漂移风险。默认硬切；只有需要"时间流逝"才用溶解。
