# 决策：单源化后的三项边界裁决

状态：implemented

## 问题

harness 单源化要先定三条边界，否则后续搬迁无法判定完成：顶层到底放几项、`docs/` 整体怎么办、外部锁定的 skill 落在哪。三条都做过权衡，落选方案不记下来会反复重开。

## 决策

- **A — 顶层恰好 7 项**：`assets/` `products/` `scripts/` `system/` `.pi/` `.agents/` `.githooks/`；根另放 `.gitignore` 等 git 机制文件、`AGENTS.md`、`CONTEXT.md`。检查门放行 git 机制文件，其余顶层项一律不允许。
- **B — `docs/` 整体删除**：内容按 [`system/CONVENTIONS.md`](../../../system/CONVENTIONS.md) 的唯一事实源矩阵归位；具体文件的归位动作在 T9，不属于本决策。本决策只定「不保留 `docs/` 这一层」。
- **C — 外部 skill 落位**：`h3-prompt-writing` 移入 [`.pi/skills/h3-prompt-writing/`](../../../.pi/skills/h3-prompt-writing/)；`skills-lock.json` 移入 [`.pi/skills-lock.json`](../../../.pi/skills-lock.json)；仓库内指向旧路径的引用同步改写。

## 被否方案

- **保留 `docs/` 作为第 8 项** —— 否决：`docs/` 与 `system/` 内容大量重叠，留着就是第二事实源，必然漂移。
- **不把 `.githooks/` 计入 7 项** —— 否决：hook 是仓库结构的可判定组成部分，显式计入才能让「恰好 7 项」机械检查。
- **把 `.agents/` 并进 `.pi/`** —— 否决：harness 作者源与长期决策是两类东西；混在一起会让决策记录被 harness 的版本变动裹挟。
- **保留 `docs/` 并把 `system/` 并进去** —— 否决：[`system/`](../../../system/) 是唯一的产品定义层，把人类知识库并进去会重新制造双源。
- **逐文件筛 `docs/`，只留操作类** —— 否决：硬切原则要求全量归位；半保留会留下无人维护的中间态。
- **把 `docs/` 归档而不删** —— 否决：一个已废弃的人类知识库没有消费者，归档只是把死内容换个位置。
- **`h3-prompt-writing` 留在 `.agents/skills/`** —— 否决：与 `.pi/skills/` 构成双源，且 `.agents/` 的定位是决策记录而非 skill 库。
- **移到 `.pi/vendor/` 之类的新目录** —— 否决：外部 skill 同样是 skill，消费者按 `.pi/skills/<name>` 找它，多一层目录没有收益。
- **不搬本地副本，只在 lock 文件里指向外部路径** —— 否决：锁定后仍需本地副本才能离线消费，外部来源不稳定。

## 后果

- 顶层 7 项由检查门（`scripts/check_harness.*`）机械校验，新增顶层目录需要一条新决策记录。
- `docs/` 的具体归位在 T9；本记录不定义文件级去向。
- 引用已同步：[`.pi/agents/video-director.md`](../../../.pi/agents/video-director.md) 与（当时的）`.pi/skills/video-craft/SKILL.md` 指向 `.pi/skills/h3-prompt-writing/`。
