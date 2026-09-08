# ai-video — AI 视频生成工作区

> 视频管线的生产工作区。管线流程人读摘要见 **[docs/pipeline/video-pipeline.md](../docs/pipeline/video-pipeline.md)**；层级链模型 / 写作规格 / 工作台见 **[DESIGN.md](DESIGN.md)**（唯一设计事实源）——本文件只保留工作区结构与规则。

## 目录

```
ai-video/
├── README.md                # 本文件 — 工作区导航
├── DESIGN.md                # 唯一设计事实源（层级链模型 + 写作规格 + workbench）
├── DEV-PLAN.md              # 执行计划（阶段 / 迁移 / 测试 / 验收）
├── IMAGE-DESC-TEMPLATE*.md  # 参考图描述模板（每张参考图必配）
└── projects/                # 按选题隔离
    └── TXXX/
        ├── goal.md / goal2.md          # 各层 goal 单元（验收标准 + 共同理解 + 单元计划）
        ├── research/script/visual/rhythm/director.md  # 中间单元（一个单元一份 md）
        ├── seg1.md / seg2.md / end-l1.md / end.md     # 运行单元 + 层末 end 单元
        ├── exec/                       # prompt 文件 / 交付件（运行单元 ③ prompt-file 引用）
        ├── assets/                     # 项目级工作素材
        │   ├── ref-images/             # 参考图草稿
        │   ├── last-frames/            # 上一段视频尾帧（段间锚定用）
        │   └── storyboards/            # 分镜线稿
        └── outputs/                    # 生成产物（视频文件）
```

链节点 = 带 `unit:`/`层:` frontmatter 的 md 文件（模型与写作规格见 DESIGN.md §2/§3，此处不重复）。

## 工作区规则

- **所有视频设计文件都在 `ai-video/projects/TXXX/` 下。** `topics/TXXX/` 只保留 brief.md（与文本管线共享层）。视频 agent 不写入 topics/。
- **工作台 vs 图书馆**：`ai-video/` 是草稿工作台（写多读多，宽松命名），`assets/` 是成品仓库（读多写少，严格命名）。验证通过后晋升 `assets/`，尾帧选题结束即清理。
- **参考图铁律**（生图 1-3 / 生视频 3-7 / 非首段必用尾帧）与消费顺序详见 docs/pipeline/video-pipeline.md。
- 所有 md 中引用本地图片用 `![]()` 内联预览。
