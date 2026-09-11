# Harness 单源

- AI harness 只有一处作者源：`.pi/{rules,skills,agents}`。
- 禁止生成镜像与同步脚本；不得存在第二份可编辑副本。
- 一条信息只有一个权威来源，别处只引用；矩阵见 [`system/CONVENTIONS.md`](../../system/CONVENTIONS.md)。
- 不在两处定义同一内容；出现即是缺陷，删一处。
- 不建集中索引文件；触发靠各文件 frontmatter 的 `description`。
- 不保留兼容读写，不做新旧并行。
- 不写没有消费者的知识。
- 临时流程文件不留在仓库里。
