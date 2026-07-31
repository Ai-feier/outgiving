# ai-video — AI 视频生成工作区

> 与文本 content-pipeline 独立。共享选题 brief，独立的视频生产管线。

## 目录

```
ai-video/
├── README.md              # 本文件 — 规则 + 资产约定
├── IMAGE-DESC-TEMPLATE.md    # 图片描述模板（每张参考图必配）
└── projects/              # 按选题隔离
    └── T001/
        ├── TOGETHER.md                   # 协作对齐文档（agent 间交叉 review）
        ├── research-gather-expert.md     # gather-expert 研究产出
        ├── script-beats.md               # script-designer 叙事节拍
        ├── visual-world.md               # visual-designer 视觉宪法
        ├── visual-assets-spec.md         # visual-designer 资产规格
        ├── rhythm-curve.md               # rhythm-designer 节奏曲线
        ├── video-prompt.md               # video-director 合成 prompt
        ├── gates/                        # 确认门记录（人做的决策存档）
        ├── assets/        # 项目级工作素材
        │   ├── ref-images/    # 参考图草稿（人物正面/场景定调）
        │   ├── last-frames/   # 上一段视频尾帧（段间锚定用）
        │   └── storyboards/   # 分镜线稿
        └── outputs/       # 生成产物（视频文件）
```

**所有视频设计文件都在 `ai-video/projects/TXXX/` 下。** `topics/TXXX/` 只保留 brief.md（与文本 pipeline 共享层）。视频 agent 不写入 topics/。

## 三条铁律

### 1a. 生图引用 1-3 张参考图

参考图优先网上找（官方设定集/动画截图/同人作品），下载到本地 `ref-images/`。找不到再用 Seedream fallback。

| 用途       | 推荐                                     | 说明                           |
| ---------- | ---------------------------------------- | ------------------------------ |
| 角色设计稿 | 1-3 张（布局参考 + 面部锚定 + 风格参考） | web 优先，Seedream 是 fallback |

### 1b. 生视频引用 3-7 张参考图

API 硬上限 9 张。少于 3 → 锚定不足，多于 7 → 帧过密（KeyFrame-Compass 2026）。

| 类型   | 推荐                                           | 说明               |
| ------ | ---------------------------------------------- | ------------------ |
| 含角色 | 3-5 张（正面+半侧+全身 + 场景定调 + 风格参考） | 锚定身份+空间+美学 |
| 纯场景 | 3-4 张（场景定调 + 风格参考 + 构图模板）       | 锚定色调+材质+构图 |

**参考图必须先下载到本地 `ref-images/`**，再作为参考传入生成 API。

**每次生图/生视频的 prompt 或确认门必须声明用了哪些参考图**：

```
参考图清单：
  - ref-images/Ichigo_front_v01.png（正面，角色锚定）
  - ref-images/Ichigo_fullbody_v01.png（全身，服装锚定）
  - ref-images/Seireitei_scene_v01.png（场景定调）
  负面参考：ref-images/Yhwach_front_v01.png（脸型骷髅化，不使用）
```

参考图来源：**优先网上找**（官方设定集/动画截图/同人作品，下载到 `ref-images/`）→ 找不到再用 Seedream 生成 → 产出存入项目 `ref-images/`。

**所有 md 文件中引用本地图片必须用 `![]()` 内联预览**，让读者看到图而非只有文件名：

```
| ID | T | 内容 | … |
|----|---|------|---|
| 001_char_Yhwach_v01.png<br />![001_char_Yhwach_v01.png](001_char_Yhwach_v01.png) | CHR | Yhwach | … |
```

`_index.md`、`ref-sources-*.md`、`gates/*.md` 等所有含图片引用的 md 均遵循此格式。

### 2. 非首段视频必须用前一段的尾帧（尾帧不计入 1b 配额）

段间一致性靠尾帧传递，不靠 prompt 描述：

```
段 1 生成 → 取末帧 → 存入 last-frames/ → 段 2 用其为参考图
段 2 生成 → 取末帧 → 存入 last-frames/ → 段 3 用其为参考图
...
```

尾帧命名：`{project}-{segment-id}-lastframe_v{NN}.png`（如 `T002-B2-lastframe_v01.png`），详见下节「尾帧管理」。

**例外**：场景切换（真人→数据动画）可不用尾帧，但需场景定调图替代。

## 与 assets/ 的关系

**`ai-video/` 是工作台，`assets/` 是图书馆。**

|                    | ai-video/                                     | assets/                                                       |
| ------------------ | --------------------------------------------- | ------------------------------------------------------------- |
| **性质**     | 生产流水线，写多读多                          | 成品仓库，读多写少                                            |
| **资产状态** | 草稿、未验证、使用中                          | 已验证、已入库、可复用                                        |
| **命名**     | 宽松（`{project}_{desc}_{type}_v{NN}.png`） | 严格（`{Type}_{TopicID}_{EntityName}_{Variant}_v{NN}.png`） |
| **索引**     | 无，`find`/`ls` 即可                      | taxonomy-registry + 14 类子索引                               |
| **跨题复用** | 不直接复用——晋升`assets/` 后复用          | 查子索引 → 六维兼容复核                                      |

**一条路径，两个阶段**：

```
visual-designer 生产
  → ai-video/projects/TXXX/assets/ref-images/（草稿，写多）
  → Seedance 生成验证
  → 晋升 assets/（重命名 + 更新子索引）
  → 全管线可复用（读多）
```

晋升条件（同时满足）：IaD 检查通过 / ≥1024px .png / 至少一段视频验证有效 / 命名转全局规范。

### 尾帧管理

尾帧是段间一致性传递的硬锚点。**不进 assets/**——临时工作产物，选题结束即清理。

命名：`{project}-{segment-id}-lastframe_v{NN}.png`（如 `T002-B2-lastframe_v01.png`）。

- 同版本重生成 → 覆盖
- 内容重大变更 → 版本号递增，旧版保留 1 份于 `last-frames/archive/`
- 选题结束 → 清理全部尾帧
- 例外：关键定格帧 → 以 STB 类型晋升 `assets/storyboards/`

### 消费顺序

video-director 组装 prompt 时查资产的优先级：

```
1. ai-video/projects/TXXX/assets/ref-images/（项目草稿）
2. assets/ 子索引（全局正式资产，已有就别重复生产）
3. 无 → 通知 visual-designer 生产
```

尾帧单独处理：非首段直接取 `last-frames/`，不存在 → 阻塞（RefImg 门禁）。

## 工作流

```
选题 brief (topics/TXXX/brief.md)
  → 【门 1】人确认：方向/平台/红线
  → gather-expert 研究 → research-gather-expert.md
  → 【门 2】人确认：研究范围/置信度
  → 三 designer 并行启动
       │ 每个 agent 先在 TOGETHER.md §2 写方向+假设
       │ 产出后回读 §3 勾对齐、§5 交叉验证
       │ 不对齐 → §6 评论+@ → loop → §7
       │
  → 【门 3】人看设计矛盾摘要，裁决方向
  → visual-designer 生图确认门（参考图 1-3，铁律 1a + web 优先 + 布局参考图）
       │ 人确认 prompt + 参考图声明
       │ → SeedreamImage.generate()
       │ → 下载到 ref-images/ + 描述文件 + 更新 ref-images/index.md
       │
  → video-director 合成 video-prompt.md
  → 【门 4】人终审 prompt（含参考图数量 3-7 检查）+ 印象确认
  → SeedanceVideo.submit()
  → 尾帧 → last-frames/
  → 验证通过的参考图 → 晋升 assets/
```

**TOGETHER.md** = agent 间的协作对齐文档（模板 `ai-video/TOGETHER.md`）。每个选题 copy 到 `projects/TXXX/TOGETHER.md`。
**HUMAN-GATES.md** = 人机决策门（`ai-video/HUMAN-GATES.md`）。门记录存档在 `projects/TXXX/gates/`。

## 当前状态

- **活跃选题**：T002（skill 设计）
- **已有产出**：script-beats.md / visual-world.md / rhythm-curve.md / video-prompt.md（在 `topics/T002/` 下）
- **待迁移**：将 T002 视频产出从 `topics/T002/` 迁移或链接到 `ai-video/projects/T002/`
