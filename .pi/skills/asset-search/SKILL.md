---
name: asset-search
description: 规范化参考素材搜索——图片/视频/音频/3D模型/设定图。五步法：明确需求 → 来源策略 → 搜索执行 → 素材验证 → 下载引用；含角色语言素材（动作/运动质量/空间关系/微表情）专项策略。当需要为锚定身份/场景/动作/风格找参考素材、或需要处理 ref-inbox 待处理条目时使用。
---

# asset-search — 参考素材搜索

为视觉阶段提供参考素材。与 researcher 互补：researcher 搜文本证据，本 skill 搜视觉/听觉素材。

## 与系统的关系

visual-draftsman 参考图流程「网上找」这一步的标准化执行者。产出 = 视觉阶段资产清单里的参考图声明。下载的素材存 `assets/ref-images/`（按主题子目录），验证后按 `assets/asset-lab.md` 规范登记子索引。

## 五步法

### 第一步：明确需求

| 问题 | 选项 |
| --- | --- |
| 类型 | 图片 / 视频 / 音频 / 3D模型 / 设计参照 |
| 用途 | 身份锚定 / 场景定调 / 动作参考 / 风格参考 / 情绪锚定 / 材质参考 |
| 预期数量 | 设定图 1-3 / 截图 3-5 / 模型 1-2 / 音频 1 段 |
| 质量门槛 | 图片 ≥1024px / 音频 ≥128kbps / 视频 ≥720p / 慢动作 ≥60fps |

**角色语言素材维度**（构建角色语言体系时额外启用）：

- **动作参考 (Motion Reference)**——signature gestures 定义前需真实人类动作参考
- **运动质量 (Laban Effort)**——Weight/Time/Space/Flow Effort Profile 视觉参考
- **空间关系 (Proxemics)**——角色间距离和空间关系视觉参考
- **微表情/微动作 (Micro-expression)**——情绪个人化表达的 FACS 级参考

**产出**：一行需求声明，如 `需求：T003 林北 动作参考 signature gesture "握拳横劈"，≥720p 慢动作优先，多角度。`

**约束**：身份锚定 → 设定图；场景定调 → 全景 + 关键角度；动作参考 → 多帧/视频 ≥60fps；运动质量 → 慢动作 + 角度标注；微表情 → 面部特写 + 慢动作。

### 第二步：来源策略

按可获取性组织。**首轮并行搜索可达层级**：

```text
P0 — 官方来源（官网/设定集/官方素材）⚠ 大概率不可达（Fandom/wiki Cloudflare 拦截）。文本确认存在性，P0 素材经 ref-inbox 进入。
P1 — 新闻/博客 CDN（⭐ 实际首选）→ web_fetcher download 直接下载，URL 模式去掉尺寸后缀拿原图
P2 — 游戏资源站（Spriters Resource / models-resource）
P3 — 同人/艺术站（DeviantArt / Pixiv）⚠ 索引不足，跳过自动搜索
P4 — 3D模型站（Cults3D / Sketchfab）
P5 — AI 生成 fallback（P1-P4 均无可用时）
```

**搜索规则**：首轮并行 P1 + P0(文本确认)；P1 命中 → 直接下载；P3 跳过；每轮记录 URL。

**角色语言素材来源优先级**：

| 素材类型 | 首选来源 | 关键词模板（英/中） |
| --- | --- | --- |
| 动作参考 | P1: 舞蹈/武术/体育慢动作视频 | "slow motion {action} reference dance" / "慢动作 {动作} 参考" |
| 运动质量(Laban) | P1: 现代舞录像 + 武术演示 | "laban effort heavy sustained contemporary dance" / "现代舞 动作质感" |
| 空间关系 | P1: 电影截图/剧照 | "cinematic two-shot film still" / "电影 双人镜头 构图" |
| 微表情 | P0: FACS 训练素材 / P1: 演员特写 | "micro-expression FACS reference AU{组合}" / "微表情 FACS 参考" |

**下载工具**：首选 `web_fetcher download`（`uv run --directory scripts`），回退 curl + UA。

### 第三步：搜索执行

**日志格式**：

```text
## 搜索日志 — {日期} | 需求：{声明}
| 优先级 | 关键词 | 站点 | 命中? | URL |
最佳结果：{...} / 未命中原因：{...}
```

**角色语言素材搜索策略**：

- **动作质感**：用「质感形容词 + 动作类型」而非角色名，如 "explosive punch slow motion reference"
- **Laban 术语映射**：heavy→grounded weight / light→floating delicate / sustained→continuous flow / sudden→explosive burst / direct→focused / indirect→wandering / bound→controlled tension / free→flowing release
- **Proxemics**：用距离描述词 (intimate/personal/social/public) + framing (close-up/two-shot/wide) + "film still"
- **微表情**：搜索特定 AU 组合，如 "AU4+AU7 anger micro-expression"，或情绪 + slow motion
- **首轮** ≥3 种关键词组合，中英文并行

### 第四步：素材验证

| 检查 | 判定 |
| --- | --- |
| 分辨率 ≥1024px(图) / ≥720p(视频) / 无压缩伪影 + 水印 | 通过/不通过 |
| 主体完整可见 / 用途匹配 / 无「禁止转载/商用」声明 | 通过/不通过 |

**动作类素材附加检查**：

- 慢动作帧率 ≥60fps（细节可见性），<30fps 标注「帧率受限」
- 标注角度覆盖（正面/侧面/背面），单角度标注「单角度」
- 连续帧截图 ≥3 张提取关键姿态

### 第五步：下载和引用

**存放**：`assets/ref-images/{TopicID}/{SEQ}_{Type}_{Purpose}_{Entity}_v{NN}.{ext}`

- SEQ 三位数字｜Type: CHR/SCN/KV/LYT/PROP/STYLE/ACTION/AUDIO/REF
- Purpose: identity/mood/motion/look｜Entity: PascalCase｜vNN

示例：`assets/ref-images/T003/001_CHR_identity_LinBei_v01.png`

**来源清单**（`ref-sources.md`）：

```text
| 文件 | 类型 | 用途 | URL | 来源性质 | 版权状态 | 验证状态 |
```

验证状态：已直接验证 / 未独立验证 / 推测。来源性质：官方设定集 / 动画截图 / 游戏资源 / 同人 / 模型站 / AI 生成。

**交接**：`参考图声明：正参考：{path}（{来源+特征}）负参考：{path}（{不匹配理由}）`——交给 visual-draftsman 的资产清单。

## 角色语言素材搜索速查表

| 需求类型 | 最佳来源 | 搜索关键词（英/中） | 质量标准 |
| --- | --- | --- | --- |
| Signature Gesture 定义 | 舞蹈/武术慢动作 P1 | "{action} slow motion reference dance" / "慢动作 动作 参考 角色" | ≥60fps, 多角度优先 |
| Laban Weight (strong∼light) | 现代舞/举重纪录片 P1 | "grounded weighted dance" / "现代舞 重量感 沉重" | 慢动作, 全身可见 |
| Laban Time (sudden∼sustained) | 武术/体育爆破 P1 | "explosive burst slow mo" / "爆发 慢动作 动作参考" | ≥60fps, 起止帧清晰 |
| Laban Space (direct∼indirect) | 舞者空间轨迹 P1 | "direct indirect space dance" / "空间轨迹 舞蹈 俯拍" | 俯拍/全景优先 |
| Laban Flow (bound∼free) | 即兴舞蹈/动物运动 P1 | "bound free improvisation dance" / "即兴舞蹈 流动 控制" | 持续运动 ≥3s |
| Proxemics 亲密 | 电影双人特写 P1 | "intimate close-up two-shot film still" / "亲密 电影 双人 特写" | 面部 + 肩部 |
| Proxemics 社交 | 电影中景构图 P1 | "social distance conversation film" / "社交 距离 电影 中景" | 半身, 空间关系清晰 |
| Proxemics 公共 | 全景/舞台照 P1 | "public distance wide shot theater" / "公共 距离 全景 舞台" | 全身 + 背景关系 |
| 微表情 Anger | FACS 训练 P0 / 演员特写 P1 | "AU4+AU7 micro expression anger" / "愤怒 微表情 演员" | 面部特写 ≥60fps |
| 微表情 Fear | FACS 训练 P0 | "AU1+AU2+AU4+AU5 micro expression fear" / "恐惧 微表情 FACS" | 全脸无遮挡 |
| 微表情 Surprise | 反应镜头 P1 | "eyebrow raise surprise slow motion" / "惊讶 微表情 慢动作" | 起止 + 中间帧连续 |

## 精进机制

每次用后记录：命中 Y/N、有效策略、无效策略、优化。连续 2 次 P0-P4 全未命中 / 来源失效 / 发现新站点时触发。**减法优先**：已有策略完整执行后无效，才有理由新增。记录走 [`.pi/skills/reflecting/SKILL.md`](../reflecting/SKILL.md) 的机制，本 skill 不另立日志文件。

## ref-inbox 消费

用户说「处理 ref-inbox」，或 `assets/ref-inbox.md` 待处理区有未处理条目时：

1. 下载 → `web_fetcher download`
2. 命名 → 按第五步规范
3. 注册 → 一行追加到 `assets/asset-lab.md` 指向的子索引
4. 标记已处理

路径关系：自动搜索 = 首选（P1 CDN 可达），ref-inbox = 自动盲区补位（P3 同人 / P0 设定集等需登录素材）。

## 禁止清单

不下载有「禁止转载/商用」声明的素材；不直接用于发布（仅 AI 生成参考）；不复制到渠道发布目录。

## 例子

真实输入：T003 Yhwach 角色参考图搜索。

真实输出：P1 新闻站 CDN 命中 5 张（如 `otakuusamagazine.com/wp-content/uploads/` 去尺寸后缀拿原图），P3 纸模 1 张，P0 官方 wiki 全未命中（Cloudflare 拦截）。下载 2 张通过验证，写入 `ref-sources.md`，交接 visual-draftsman 作为身份锚定正参考。
