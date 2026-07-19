# Rules — 项目管理宪法

> 参考 [affaan-m/ECC](https://github.com/affaan-m/ECC) `.claude/rules` 架构，为本项目特化。
> 规则 = 始终加载的操作约束。不同于 Skills（任务触发）、Agents（角色定义）。

## 结构

```
.claude/rules/
├── README.md                # 本文件
└── project/                 # 项目规则（所有 session 自动加载）
    ├── workflow.md          # 内容生命周期 + 质量门禁
    ├── collaboration.md     # Agent 协作 + 交接契约
    └── conventions.md       # 命名 + frontmatter + 目录 + Git
```

## 与 CLAUDE.md 的关系

| 文件 | 定义 | 修改频率 |
|------|------|---------|
| `CLAUDE.md` | 灵魂信仰 + 第一性原理（为什么） | 低 |
| `rules/` | 操作约束（怎么做） | 随项目演进 |

CLAUDE.md 与 rules 冲突 → CLAUDE.md 的信仰/第一性原理赢。

## 优先级

项目 rules > 用户级 rules。新增规则文件后下次 session 自动生效。

## 维护

- 单文件 ≤ 150 行，超过→拆分
- 新增/删除规则时更新本 README
- 不保留注释掉的死规则
