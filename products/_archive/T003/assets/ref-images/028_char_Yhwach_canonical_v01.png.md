# 028_char_Yhwach_canonical_v01.png — Yamach 规范参考图

## 来源

| 字段 | 值 |
|------|-----|
| 生成服务 | Seedream 5.0 Pro (`doubao-seedream-5-0-260128`) |
| 来源 | AI 生成（Seedream Image API） |
| 生图确认门 | `ai-video/projects/T003/gates/image-gen-Yhwach.md` |
| 生成脚本 | `ai-video/projects/T003/_gen_yhwach.py` |
| 生成时间 | 2026-07-20 00:23 CST |

## 参数

| 参数 | 值 |
|------|-----|
| Prompt | 见 gate 文件 §.3 |
| Negative | 见 gate 文件 §.4 |
| Size | 1440x2560 (9:16) |
| Output format | PNG |
| Watermark | false |
| optimize_mode | standard |
| Reference images | 1（`010_scene_look_full_yhwach_v01.webp` — 全身比例+服装参考） |

## 质量评估

### IaD 检查

| 要求 | 状态 | 备注 |
|------|------|------|
| 三栏完整（正面/3/4/全身） | 通过 | 三栏均正确渲染，每栏约 1/3 宽度 |
| 中性表情 | 通过 | 无笑容/愤怒/傲慢，口自然闭合 |
| 红瞳多瞳 | 边缘 | 红瞳已呈现，多瞳结构近似但非精确 |
| 纯黑背景 | 通过 | 无意外场景元素 |
| 无眉毛错误 | 通过 | 细眉已实现，非粗眉 |
| 胡须形态正确 | 通过 | 络腮胡+八字胡，下颌干净 |
| 无武器/无特效 | 通过 | 无刀剑/灵压特效 |
| 服装细节 | 通过 | 白风衣/十字徽/暗红披风/黑手套/黑靴 |
| 角色三栏一致性 | 通过 | 同一发型/服装/面部特征 |
| 线稿/着色风格 | 通过 | Bleach cel-shaded, 硬阴影, rim light |

### 偏差记录

| 偏差 | 程度 | 影响 |
|------|------|------|
| 多瞳孔结构未精确呈现 | 轻微 | 对角色锚定影响低——面部比例/服装/胡须抓住了主要身份特征 |
| 局部光照在三栏间不完全对称 | 轻微 | 可接受——角色设计稿形式优先于光照完美 |
| 十字徽章细节非精确复刻 | 轻微 | 金色十字已呈现，精确徽章细节可在参考图使用中通过图像质量和整体轮廓锁定 |

## 产出文件清单

| 文件 | 路径 | 状态 |
|------|------|------|
| 主图 | `ai-video/projects/T003/assets/ref-images/028_char_Yhwach_canonical_v01.png` | 2.9MB, 1440x2560 |
| 描述文件 | 本文件 | — |

## 晋升前计划

晋升至 `assets/characters/CHR_T003_bleach_Yhwach_canonical_v01.png` 条件：
- [ ] IaD 检查通过（本表已完成）
- [ ] Resolution >= 1024px short edge（通过，2560px）
- [ ] .png format（通过）
- [ ] 至少一段视频验证有效（尚未执行，需 video-director 后续验证）
- [ ] 命名符合全局规范（晋升时执行）
