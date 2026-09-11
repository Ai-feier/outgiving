# 决策：历史项目全删，`products/` 清零

状态：implemented

## 问题

五个历史选题（T001 / T003 / T004 / T005 在 `products/_archive/`，T006 在 `products/` 顶层）不参与任何流程阶段：没有消费者、没有推进、没有人审。它们却持续被 skill 的真例、检查门的豁免口径与测试引用——一条已死的路径，每被引用一次就要求一次维护。删掉一批选题，问题从来不是"文件要不要留"，是"指向它们的引用由谁收敛"。

## 决策

- **`products/` 清零**：T001 / T003 / T004 / T005 / T006 全部删除，`products/` 只留 `products/_inbox/`（选题入口）。可恢复性由 git 历史承担，不做备份。
- **归档位置不存在**：[`system/CONVENTIONS.md`](../../../system/CONVENTIONS.md) 删除「归档」一条，下划线前缀只剩 `_inbox/`。
- **检查门不放宽**：[`scripts/check_harness.py`](../../../scripts/check_harness.py) 删除 `ARCHIVE_PREFIX` 与它的四处跳过——口径没有变，是那一类路径没有了；检查门其余判定一字未动。
- **人审表自带**：人审表的唯一生产者变成建选题这一步。[`scripts/src/content/cli.py`](../../../scripts/src/content/cli.py) 的 `content new` 除 `brief.md` 外同时生成 `review.md`，形状由 [`scripts/src/workbench/review.py`](../../../scripts/src/workbench/review.py) 的 `Review` / `save` 渲染，不另立模板；形态未定（流程末端才分叉），表列按文本形起步。

## 被否方案

- **保留 `products/_archive/` 作为冻结归档** —— 否决：用户裁决「历史项目全删，不保留归档目录」。这是裁决，不是技术比较；被否的是「为历史内容保留任何位置」这个前提本身。

## 后果

- skill 真例改成自包含片段：指向具体选题文件的活路径换成 `products/<id>-<slug>/` 形状，项目名换成处境描述；例子的内容与教学价值不变。
- `scripts/tests/test_editor_manifest.py` 中 6 个读 T004 真实清单的用例随样本删除（真实清单已不可得），解析器其余用例保留；`scripts/tests/test_editor_e2e.py` 依赖 T004 素材，现在只会在素材缺失时 skip。
- 新选题从第一天起就有人审表；`content new` 的产物由 `scripts/tests/test_workbench_review.py` 的契约测试守住。
