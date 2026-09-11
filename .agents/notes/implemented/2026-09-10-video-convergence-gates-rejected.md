# 决策：视频链模型的两处作废——收敛门不变量与风格库

状态：implemented

## 问题

单源化把原来的 5 层链模型（四个视频岗位各自持知识）重写成薄岗位 + skill，链上的两份知识随之失去位置：

1. 旧岗位文件里定义的一组「收敛门不变量」（FreeLOC / LoL / ZPC / IaD / RefImg）与「参考图配额与尾帧链」（生图 1-3 张、生视频 3-7 张、末帧链、Tier 0 不计配额）。它们的消费者是链模型文档本身——`.pi/agents/video-director.md`、`.pi/agents/script-designer.md` 与（已删的）`docs/pipeline/video-pipeline.md`。
2. 被当作视频专属素材删掉的风格库（`styles.md` + 单风格文件）。

两者都要给出「补回还是作废」的裁决，否则每次看目录树都会重开一次。

## 决策

- **一、收敛门不变量与参考图配额不补回**：这组不变量、配额与末帧链随旧链模型文档一并作废，不在 [`.pi/skills/`](../../../.pi/skills/) 下重建。理由：它们服务的是已被**人审表**取代的 5 层链，链路本身不存在了，为链路服务的收敛门与配额也就没有消费者。

- **二、风格库复位到 [`assets/styles/`](../../../assets/styles/)**：风格库不随旧视频 skill 目录删除，作为跨选题复用的参考素材落位。理由：它是**参考素材**不是岗位知识；[`assets/taxonomy-registry.md`](../../../assets/taxonomy-registry.md) 的「风格文件绑定」规则（每个非 `generic` 风格必须有对应的风格文件）直接引用它，[`assets/asset-lab.md`](../../../assets/asset-lab.md) 的「风格一致性复核」也依赖它。消费指针加在 [`.pi/skills/visual-world/SKILL.md`](../../../.pi/skills/visual-world/SKILL.md) 一行，不复制风格库内容。

## 被否方案

- **补回 `.pi/skills/prompt-engineering/` 与 `.pi/skills/visual-assets/` 承载收敛门与配额** —— 否决理由是**用户裁决**（不补回）。本条不附带技术论证。
- **风格库连旧视频 skill 目录一起删除，并删掉 `taxonomy-registry.md` 的「风格文件绑定」规则** —— 否决：风格库是跨选题复用素材，不是视频岗位的私有物；为了让删除显得干净而连带删掉一条仍然成立的不变量，是把不变量当目录整洁的交换品。

## 后果

- `.pi/` 内不再存在收敛门不变量与参考图配额的定义；视频侧的一致性约束只由 [`.pi/skills/visual-world/SKILL.md`](../../../.pi/skills/visual-world/SKILL.md)「实体一致性」一节承担。
- `assets/styles/` 是风格文件的唯一位置：`styles.md` 是风格总览，`<tag>.md` 是单风格定义。消费者是视觉岗位与 `assets/` 下的资产索引。
- 检查门的相对引用扫描面已扩到 `assets/`（[`system/CONVENTIONS.md`](../../../system/CONVENTIONS.md) 检查门第 5 条），风格库路径失效会被机械拦住。
