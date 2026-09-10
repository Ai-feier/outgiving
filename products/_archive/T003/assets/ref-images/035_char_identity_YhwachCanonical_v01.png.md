# 035_char_identity_YhwachCanonical_v01.png

## 来源

- **生成方式**：Seedream 5.0 (doubao-seedream-5-0-260128)
- **来源性质**：AI 生成 — 角色设计稿（三栏）
- **验证状态**：IaD 已完成（见 gates/image-gen-Yhwach.md §8）
- **生成时间**：2026-07-20 01:33 UTC

## 图片信息

- **分辨率**：2400×1600（3:2 横版）✓（≥1024px）
- **格式**：PNG (truecolor)
- **文件大小**：2.9MB

## 内容描述

Seedream 5.0 生成的三栏 Yhwach 角色设计稿。纯黑背景。三栏布局，每栏约 1/3 宽度：

- **左栏**：正面肖像（头至胸），中性表情，平行光线
- **中栏**：另一正面向肖像（意图为 3/4 侧面但实际渲染为正面）
- **右栏**：全身站姿（头至脚），白风衣+十字徽+暗红披风+黑手套+白裤+黑靴

面部特征：长黑发后梳，红瞳，八字胡+络腮胡，中性表情。服装和面部特征跨三栏基本一致。

## 已知缺陷（IaD 发现）

1. **中栏不是 3/4 侧面** — 与左栏同为正面视角，prompt 指定的 45 度旋转未渲染
2. **额横纹缺失** — prompt 指定的 "3 distinct deep horizontal forehead crease lines" 不可见
3. **无眉不彻底** — 眉骨区有残留阴影，非完全平滑
4. **年龄感偏年轻** — 面容似 30-35 岁而非 50+ 岁
5. **深眼窝不足** — 眉骨前突覆盖上眼睑的特征未呈现

## 用途

- **不推荐用于 Seedance 视频参考**（面部微特征不足、中栏视角错误）
- **可作为布局格式参考** — 展示 Seedream 5.0 对三栏设计稿的理解边界
- **可作为服装和整体轮廓的辅助参考**

## 生成参数

- Model: doubao-seedream-5-0-260128
- Size: 2400x1600
- Reference images: 033(official full body) + 034(official face) + 027(layout template)
- Watermark: false
- Optimize: standard
- Output format: png

## 参考图清单

| 参考图 | 用途 | 来源 |
|--------|------|------|
| 033_char_identity_YhwachOfficialFull_v01.png | 身份锚定 | bleach-anime.com 官方 |
| 034_char_identity_YhwachOfficialFace_v01.png | 面部补充 | bleach-anime.com 官方 |
| 027_lyt_layout_ThreeColumnCharSheet_v01.png | 布局模板 | ai:Seedream |

## 决策

v3 不晋升至 `assets/characters/`。需要 v4 策略调整（见 gates/image-gen-Yhwach.md §11.3）。
