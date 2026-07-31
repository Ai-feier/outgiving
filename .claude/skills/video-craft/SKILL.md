---
name: video-craft
description: AI 视频创作的元知识 — 剧本/主体/节奏三元素相互成就的认知框架。四 agent 共享的镜头词汇表、细节增强原则、角色语言体系和 Prompt 工程速查。不是工序流水线，是理解 AI 视频创作本质的底层知识。
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

两个 pipeline **独立运行**，共享 brief 里的核心观点、受众、钩子、关键信息点、视觉资产规划。文本走"写作"心智，视频走"导演"心智——不是同一件事，不该用同一套流程。视频管线内部，本文件是所有 4 个 video agent 共享的知识基座（元知识层），各 agent 的具体实现细节在各 `.md` 中。

## 核心设计哲学

AI 视频创作的本质是**导演**，不是编剧。

三个设计维度——剧本、主体、节奏——不是三个步骤，是**相互成就的三个力**。它们同时存在、互相约束、一起呼吸：

- **剧本**决定了什么在发生、什么顺序、什么情绪递进 → 给主体制造了"需要看见什么"的需求
- **主体**定义了视觉世界的一致性法则 → 反过来约束剧本"什么可以在这个世界里发生"
- **节奏**是两者的呼吸——剧本的情绪曲线通过节奏具象化，主体的视觉复杂度通过节奏被消化

改变任何一个，另外两个必须重新调谐。三者在矛盾和对位中找到平衡——这个平衡点就是创作。

**风格**是贯穿三者的元参数——同一个剧本在"纪录片"和"动画"风格下，主体和节奏完全不同。

**共享镜头词汇表是本 skill 的核心产出：** 经过四 agent 同步精进，以下镜头语言体系成为全线统一术语——script-designer 用它们写节拍的镜头意图，visual-designer 用它们定义视觉形态，rhythm-designer 用它们描述运镜节奏，video-director 用它们写最终 prompt。**同一个景别/运镜/角度词在全线有相同含义。**

## 共享镜头词汇表

以下词汇表是四 agent 的统一引用标准。各 agent 在自己的 `.md` 中有完整推导细节和风格约束；此处仅列术语速查，确保跨 agent 沟通时术语一致。

### 景别 7 级

| 标记 | 名称 | 功能 | 风格偏好 |
|------|------|------|---------|
| EWS | 极远景 | 建立空间/孤寂感 | 日系少用；纪录片开场 |
| WS / Full shot | 全景/全身 | 全身+环境/动作空间 | 纪录片基线；日系可接受 |
| MWS / Cowboy | 中全景 | 膝上/人物+环境 | 商业产品环绕 |
| MS | 中景(腰上) | 对话/中性叙事 | 纪录片核心 |
| MCU | 中近景(胸上) | 情绪+环境上下文 | **日系默认** |
| CU | 特写(面部) | 情感聚焦/细节 | **日系默认**；纪录片情绪点 |
| ECU / Macro | 极特写 | 眼睛/纹理/产品细节 | 商业核心；日系少用 |

### 运镜 15 种

每拍只指定一种主导运镜。复合运动拆为时序节拍：「Start: slow dolly-in. Then: gentle pan right for final 2s」。速度标量统一用 slow / medium / fast。

| 运镜 | Seedance 识别率 | 风格约束 |
|------|----------------|---------|
| Static locked shot | 极高 | 各风格通用 |
| Dolly-in / Push-in | 高 | 日系偏好 slow；高强节奏用 fast |
| Dolly-out / Pull-back | 高 | 结尾/释放感 |
| Orbit / Arc shot | 高(需方向+半径) | 商业产品展示 |
| Tracking shot | 高 | 侧面跟随为主 |
| Pan left/right | 高 | 空间揭示 |
| Tilt up/down | 高 | 角色登场/垂直揭示 |
| Crane up/down | 中 | 规模揭示，日系禁 |
| Handheld / Gimbal | 高 | **日系禁过度抖动**；纪录片默认 |
| Rack focus | 中(需景深描述) | 注意力转移 |
| Whip pan | 中 | **日系禁**；高强转场 |
| Parallax lateral pan | 中 | 深度空间展示(需三层) |
| Hitchcock zoom | 低(需复合描述) | 紧张/眩晕 |
| First-person POV | 中 | 沉浸感 |
| Dutch angle | 中 | 不安/心理压迫 |

### 角度 6 种

| 角度 | 心理效果 | 日系偏好 |
|------|---------|---------|
| Eye level | 中性/客观 | 默认 |
| Low angle | 力量/压迫/宏大 | **常用**——力量关系 |
| High angle | 脆弱/被审视 | **常用**——情绪截面 |
| Over-the-shoulder (OTS) | 第三人称/对话 | 可用 |
| Dutch angle | 不安/失衡 | 心理扭曲时用 |
| Bird's eye | 上帝视角/抽象 | 可用 |

### 光学与景深

| 焦距桶 | 效果 | 日系偏好 |
|--------|------|---------|
| Wide (24-28mm) | 沉浸/空间夸张 | 少用 |
| Normal (35-50mm) | 自然/中性 | 通用默认 |
| Telephoto (85mm+) | 亲密/压缩背景 | **极常用** |

景深语法：shallow DOF(电影感，动画 default=deep focus)；deep focus(信息量，日系默认)；rack focus(注意力转移)。

### 光影 4 类

**自然光**：golden hour(暖色/浪漫) / blue hour(冷色/忧郁) / overcast(柔和/纪录片) / harsh noon(强对比) / moonlight(神秘)

**可控光**：high-key(明亮/商业) / low-key(悬疑/戏剧) / Rembrandt(三角光) / split(二元冲突) / butterfly(时尚对称)

**边缘/特殊光**：rim/backlight(轮廓分离) / volumetric / god rays(神圣/穿透) / practical(画面内光源) / side light(纹理揭示)

**情绪→光照速查**（替代抽象情绪词写 prompt）：
希望→golden hour backlight+warm amber；绝望→low-key+hard overhead+deep shadows；孤独→blue hour+single practical lamp；悬疑→low-key+split lighting+volumetric dust；力量→rim backlight+low-angle+god rays；亲密→warm practical lamp+shallow DOF+soft fill

### 转场 6 种

硬切 0s / 交叉溶解 0.5-1.5s / 渐黑白 1-2s / 匹配剪辑 0s / 音频先行 0.3-1s / whip pan 0.3-0.5s。

日系禁止 whip pan/fast spin；首选交叉溶解+硬切。快速运镜增加 motion blur 和身份漂移风险。

## 细节增强原则

AI agent 之间通信使用**压缩格式**（如 `fabric+velvet+soft`、`low-key`），但最终 prompt 层必须**展开为可生成的物理描述**。以下是压缩→展开的三条核心原则：

### 1. 材质：从压缩到物理化

压缩格式 `class+surface+1key` → 展开为四层物理描述：(a)表面状态(刮痕/氧化/磨损/水渍/包浆) (b)光表面交互(镜面/漫射/透明/粗糙度) (c)老化痕迹(新旧程度/磨损/修补) (d)不规则纹理(木纹/石纹/裂缝)。完整展开速查表在 visual-designer.md「材质展开速查」。

`[STYLE-DEP]` 日系：精简（三色法）、去纹理；写实：全展开；赛博朋克：追加锈蚀/漏光。

### 2. 环境：四要素激活

环境 dressing 缺失是"画面空洞"首要原因。每场景激活 ≥1 项：(a)**大气效果**选 ≤2 项（丁达尔光/热浪扭曲/蒸汽/薄雾/呼吸白气等）(b)**天气/时间**（黄金/蓝调/阴/雨/雪/雾/强风）(c)**飘落物与环境粒子**每场景 ≤1 种主飘落物（花瓣/余烬/雪/叶/尘埃/萤火虫等）(d)**背景人群**（稀疏/适中/密集），综合要素在 visual-designer.md「环境细节层次」。

### 3. 布光：单方向 → 多层光源

「key+fill+rim+ambient+practical」五层光源替代单维「暖光/冷光」。阴影质量（接触阴影/AO/软硬阴影）、光影交互（焦散/次表面散射/体积光）。完整语法在 visual-designer.md「布光」节。

## 角色语言体系

AI 不理解抽象情绪词。每拍把情绪翻译为**可拍摄的身体和空间细节**——这是角色语言的核心原则。

### 情绪动作化三通道

| 通道 | 描述 | 完整参考 |
|------|------|---------|
| **微表情维度** | FACS 级肌肉位移编码，7 情绪（悲伤/愤怒/恐惧/惊讶/快乐/厌恶/轻蔑），每个由 3-4 个因果关系短语构成 | visual-designer.md「微表情维度」 |
| **微动作维度** | 手部微动作/呼吸模式/姿态微偏移/目光动态 4 通道 | visual-designer.md「微动作维度」 |
| **环境交互维度** | 情绪在空间中留下痕迹——6 情绪各自的空间行为模式 | visual-designer.md「环境交互维度」 |

### 角色行为指纹概念

Signature Gestures + Laban Effort Profile + Camera Relationship + Proxemics 四维构成角色的行为识别系统——角色不仅"长什么样"，也"怎么动"：专属手势模式（手指敲击频率/放松时手的位置）、身体运动质量（流畅/急促/沉重/轻盈）、与镜头的关系（直视/躲避/无视）、人际距离偏好。这是 visual-designer 正在构建的系统——概念层预备，agent 各自 .md 精进时吸收。

`[STYLE-DEP]` 日系：压抑型情绪用目光/呼吸替代面部位移；欧美：FACS 级描述可直接用。环境交互幅度也受文化约束。

## 节奏-镜头耦合原则

节奏强度（rhythm_intensity）不仅决定切频——也决定运镜类型和景别选择。以下为四层耦合速查：

| 强度 | 推荐运镜 | 推荐景别 | 切频 |
|------|---------|---------|------|
| 高强 (4-5) | handheld, whip pan, fast zoom-in, quick tilt | CU/MCU 为主，偶用 ECU | 0.5-1.5s |
| 中强 (3-3.9) | dolly-in/out, stable tracking, slight orbit, slow pan | MS+MCU 交替 | 2-4s |
| 中低 (2-2.9) | slow push-in, static+micro movement, slow tilt | MS 为主，偶用 WS | 4-8s |
| 低强 (1-1.9) | static locked, extremely slow dolly, wide hold | WS+MS 为主 | 8s+ |

**Adams 双因子**：节奏感知 = shot_length × motion。两者可互补——长拍+高运动≈中强节奏感；短拍+低运动≈中强节奏感。设计时权衡两个因子。

**停顿点的镜头行为**（6 种）：消化性→static hold + 极微 push-in；预期性→rack focus 或 slow pull-back；悬念→静态 + 心跳频率微晃；场景边界→全景拉远→停顿→推入新场景；落地→定格/freeze-frame；余韵→slow pull-back 或渐暗。

完整曲线特化规则和工具-运镜能力矩阵在 rhythm-designer.md「节奏-运镜耦合」节。

## 工具能力边界

所有视频 agent 设计时必须在工具能力内展开。以下是核心边界速查：

| 维度 | Seedance 2.0 | Kling 3.0 | Veo / Luma |
|------|-------------|-----------|------------|
| 单段上限 | 15s(mini) / 30s(pro) * | 15s | 60s / 20s |
| 角色一致 | 50 槽锚定，强 | Subject Binding | 中等 |
| 镜头控制 | 自然语言+R2V，强 | Multi-Shot+vCoT | JSON / KF 帧级 |
| 动漫风格 | 优秀 | 日系真但漂移 | 中等 |
| 参考图限 | ≤9 图 / 推荐 3-7 / 尾帧不计槽 | ≤6 图 | ≤4 图 / KF |
| 中文 | 支持 | Omni 支持 | 有限 |
| 物理模拟 | 中等 | 强 | 中等 |

* `uv run --directory scripts ai generate video` 当前适配器硬限 15s（不限 model），需 30s 须 CLI 分支处理。

**Seedance 2.0 版权过滤器**：不拦截单角色名，拦截**特征组合**（如"spiky orange hair + black robe + paired blades"→Bleach）。绕过：按角色域拆分生成段，不在同段混用不同 IP 特征。特征级规避优于名称级规避。

**P0 双意提示**：find-ref 的 P0-P5 是**来源可获取性**层级；visual-designer 的 P0/P1 是**生产关键性**层级。两套正交，不互相推导。

**综合自检**：设计前确认目标工具对所需运镜的支持状态（见 rhythm-designer.md 工具-运镜能力矩阵）。工具不支持→换表达或换工具，不反向适配。

## Prompt 工程速查

### 六块公式（简化版，适配合多种工具）

```
[Subject] + [Action] + [Camera] + [Setting & Lighting] + [Style & Quality] + [Audio]
```

### 九要素公式（Seedance 特化）

```
[景别] + [主体+动作+实体tag] + [场景] + [光影] + [运镜/动] + [风格+画质] + [间]
```

### 核心规则

| 规则 | 说明 |
|------|------|
| **一个镜头只做一件事** | 单拍单一动作/单一运镜，复合运动拆为时序 |
| **中文定义主体，英文嵌入专业术语** | "一位白发老人在雨中行走" + "slow dolly-in, volumetric god rays, shallow DOF" |
| **duration 合法值** | {4,5,6,8,10,12,15}（int，不限 model 均 15s 封顶） |
| **参考图：少>多** | KeyFrame-Compass 证明参考帧密度↑→忠实度↓。推荐 ≤4 图+1 运镜+1 音频。角色 ≤1 图/实体。 |
| **负向 prompt** | 3-5 词最佳，超 8 词删负向改正向约束。Seedance 追加末尾；Kling 独立字段；Ray/Veo 用正向替代否定式 |
| **情绪词外化** | 不写 "sad/moody"，写光照条件+身体锚点+环境交互 |
| **[间]日系必填** | 嵌入 subject/scene 文本末尾，如 "still 2s then pan right" |

### 每拍必达三要素（script-designer → video-director 最小交付）

每拍 prompt 至少指定：**景别**（定框架）+ **运镜**（定运动）+ **角度**（定情绪）。三者缺一则 AI 模型自由发挥的空间过大。

## Agent 能力清单

| Agent | 角色 | 新增能力维度（2026-07 深度精进后） |
|-------|------|----------------------------------|
| **script-designer** | 叙事架构 | 镜头叙事映射（12 情绪→景别 / 8 弧线→运镜基调 / 7 过渡→镜头关系 / 4 镜头物象化模式）；AI prompt 指令从标签升级为结构化参数；物象化阶梯三级（文字→动作→镜头）；段边界尾帧设计 + 链式漂移防御（每 2-3 段重置边界） |
| **visual-designer** | 视觉世界 | 细节展开系统（9 材质类压缩→prompt 展开速查）；环境四要素体系（大气/天气/飘落物/背景人群）；多层光源语法（key+fill+rim+ambient+practical）；负向 prompt 体系（分层防护+平台差异+迭代策略）；情绪动作化扩展为三通道（微表情 FACS 7 表/微动作 4 通道/环境交互 6 表）；视觉锚点体系（硬锚/软锚/意锚/记忆策略四级） |
| **rhythm-designer** | 时间呼吸 | 节奏-运镜耦合规则（intensity→运镜+景别+切频映射）；曲线×运镜特化（8 种曲线各自高/低能段运镜规则）；停顿点 6 种镜头行为（消化性/预期性/悬念/边界/落地/余韵）；工具-运镜能力矩阵（8 运镜×3 工具）；平台基线表扩展（典型运镜+景别+镜头语言原因） |
| **video-director** | 导演合成 | 电影语言完整模块（7 景别+15 运镜+6 角度+光学 DOF+4 光影类+6 转场）；9 要素 SDK 字段映射表；素材装配协议 3 步；收敛门六道（FreeLOC/LoL/ZPC/IaD/RefImg/ALIGN）；生成调度（GroundShot P0→P1→P2 + 段间末帧链）；japanese-anime 风格约束全局标注；工具约束应对策略（版权过滤器/P0 双意） |

## 风格参考

[风格库](references/styles.md) — 电影感 / 纪录片 / Vlog / 动画 / 数据叙事。选题自己的 `video-style.md` 优先于风格库。

## 命令

```bash
# 为已有选题初始化视频产出目录
uv run --directory scripts content adapt <T0XX> douyin
# 视频 prompt 输出到 platforms/doujin/T0XX-*/video-prompt.md
# AI 视频生成
uv run --directory scripts ai generate video --scene "..." --subject "..." -o ./out/
uv run --directory scripts ai generate image --prompt "..." -o out.png
uv run --directory scripts ai extract-lastframe in.mp4 -o frame.png
```

## 输出

每个选题的视频产出放在 `ai-video/projects/TXXX/` 下：

- `video-prompt.md` — 合成的 AI 视频生成提示词
- `script-beats.md` — 剧本节拍（含镜头叙事映射和情绪-景别推导）
- `visual-world.md` — 视觉世界定义（含细节展开、环境四要素、多层光源）
- `rhythm-curve.md` — 节奏曲线（含节奏-运镜耦合和停顿点镜头行为）
