# 内容工作流

## 数据模型

| kind | 路径前缀 | ID 示例 |
|------|---------|---------|
| `topic` | `topics/T001-<slug>/` | `T001` |
| `draft` | `platforms/<plat>/T001-<slug>/` | `T001-wechat-v1` |
| `published` | `published/YYYY-MM/` | `T001-wechat-pub` |
| `analytics` | `analytics/` | `T001-review` |

## 状态机

**Topic**: `inbox → briefing → outlined → adapting → archived`
**Draft**: `draft → reviewing → ready → scheduled → published → retired`（均可 → retired）
**Published**: `live → analyzing → closed`
**Analytics**: `pending → t+3 → t+7 → final`

状态推进必须用 `content transition <id> <new-status>`，不手改 frontmatter。
创建文档用 `content new` / `content adapt`，不手写 frontmatter。

## CLI

```bash
uv run --directory scripts content list              # 选题总览
uv run --directory scripts content new "标题"         # 新建选题
uv run --directory scripts content adapt T001 wechat  # 派生平台草稿
uv run --directory scripts content show T001          # 选题详情
uv run --directory scripts content transition T001-wechat-v1 ready
uv run --directory scripts content validate           # 校验 frontmatter
uv run --directory scripts content index              # 重建索引
uv run --directory scripts content stats              # 全局统计
uv run --directory scripts content preview T001       # 浏览器四平台并排预览（0.0.0.0:8765）
```

## 工作流

```
选题 → gather-expert 研究 → brief → outline → style
        → wechat-writer / xiaohongshu-writer / x-writer / douyin-writer
        → figure-draftsman（并行出图）→ validate + preview → human review
```

- 研究 → `gather-expert` agent，不自己搜
- 出图 → `figure-draftsman` agent，不自己画
- 图放 topic 级 `assets/`，正文引用 `![](assets/figN.svg)`，不复制到平台目录
- `.svg` 单源

## 质量门禁

### briefing → outlined

- [ ] 关键信息点每点一句话可证伪，gather-expert 证据 ≥1 跨谱系锚点（单谱系标注「置信度受限」）
- [ ] 视觉资产规划节已写，研究结论诚实标注（可引用/须注明/不可引用）

### draft → reviewing

- [ ] 正文完成，字数符合平台契约，论据全部挂靠 gather-expert 产出
- [ ] 推测/未验证已标注，外部论点有链接+来源性质
- [ ] 图片标记 `<!-- fig:N -->` 已插入，`content validate` 通过

### reviewing → ready

**文本产出**：
- [ ] 至少一轮 review 完成，标题/钩子/CTA/封面已确认

**视频产出**（独立终审 - 交付前必做）：
由独立 subagent（干净上下文，非 video-director 自己）执行，避免确认偏差。每条结论附帧号/截图。在 video-director 生成后自评估（3 轮上限）通过后执行--自检是第一道，独立终审是交付前第二道。
- [ ] 产品目标：brief 关键信息点是否被视频承载
- [ ] 视觉一致性：角色/场景/风格跨段一致（锚点验证，无幻觉携带）
- [ ] 镜头语言：景别/运镜/角度符合 script-designer 节拍意图
- [ ] 节奏：时长/停顿点/能量曲线符合 rhythm-designer
- [ ] 技术质量：`ai verify` 报告通过（分辨率/时长/码率/边缘裁剪）
- [ ] 安全边界：元素在左右≥10%/上下≥8% 内
- [ ] 来源可追溯：参考素材无幽灵引用

### 平台维度约束

| 维度 | 公众号 | 小红书 | X | 抖音 |
|------|--------|--------|---|------|
| 字数/时长 | 2000-4000 | 800-1500 | 双路径: 短线程3-7条 / 单条长文1条4000字 | 60-90s |
| 感知组块 | ≤15 | 3-6 | ≤5 | ≤3 |
| 钩子位置 | 前 3 句 | 封面+首句 | 第一条 | 前 3 秒 |

### 视频维度

单拍实体≤6s / 纯视觉≤8s，通道堆叠≤2 带显式标注，rhythm CL 1.5-2.0

### 协同性自检（每轮 loop）

- [ ] 交接点格式一致 / 无平台变化未广播 / 无 agent 间隐含矛盾 / 无重复调研
- [ ] 共享文件被所有下游实际读取 / 量化指标统一定义 / 无幽灵引用 / 共享假设一致
