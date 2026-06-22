# 分镜关键帧索引

> 资产根清单见 `assets/asset-lab.md`。
> 受控词汇表（类型前缀/风格标签/状态码/变体名）见 `assets/taxonomy-registry.md`。
> 字段说明和生命周期规则遵循根清单定义。

## 记录格式

| 名称 | 风格 | 版本 | 状态 | 质量 | 最后验证 | 路径 | beat编号 | `replaced_by` | `derived_from` | `appears_in_topic` | `appears_in_style` | 备注 |
| ---- | ---- | ---- | ---- | ---- | -------- | ---- | -------- | ------------- | -------------- | ------------------ | ------------------ | ---- |

**beat编号**：对应的 script-beats.md 中的拍号（如 `B1`、`B3`）。一个关键帧可能对应多拍。

## 命名规范

文件名格式：`{Type}_{TopicID}[_{StyleTag}]_{EntityName}_{Variant}_v{NN}.png`

| 段 | 规则 | 示例 |
|----|------|------|
| Type | `STB` | `STB` |
| TopicID | 来源选题 | `T002` |
| StyleTag | **可选**。仅单一风格专属时加入 | `bleach` / 省略 |
| EntityName | PascalCase | `LinBei_Entrance` |
| Variant | 拍号或视角描述 | `B1` / `overhead` |
| Version | v两位数字 | `v01` |

完整示例：`STB_T002_bleach_LinBei_Entrance_B1_v01.png`（风格专属） / `STB_T002_LinBei_Entrance_B1_v01.png`（风格中立）

## 状态

空（待首次选题生产）
