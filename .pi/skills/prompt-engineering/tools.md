# 生成工具能力边界

写 prompt 前先确认目标工具支持所需的运镜与参考图策略；不支持 → 换表达或换工具，不反向适配。2026-07 数据；工具升级后回填本表。

## 能力速查

| 维度 | Seedance 2.0 | Kling 3.0 | H3 (MiniMax) |
| --- | --- | --- | --- |
| 单段上限 | 30s Pro / 15s Mini（当前适配器硬限 15s） | 15s | 4-15s（ComfyUI workflow 1-10s） |
| 角色一致 | 50 槽锚定 + `@` 锁 | Subject Binding | Ref2VA `subject_definitions` + `retention_analysis` |
| 镜头控制 | 自然语言 + R2V | Multi-Shot + vCoT | `[Shot N]` 时间线 + camera motion 自然英语 |
| 参考图限 | 0-9 图（尾帧不计槽，推荐 3-7） | ≤6 图 | `<Picture/Video/Audio N>` 标签体系 |
| 负向提示 | `--negative-prompt` 参数 | 独立字段 | 本 workflow 无 negative 字段 → 正向约束替代 |
| 原生音频 | 自动环境音 | 6 语对话 + 口型 | `overall_soundscape` + `non_diegetic_music` |
| 分辨率 | 由 style 行推断画幅 | 预设 | 9 档预设 |

## 工具-运镜能力矩阵

`✓` 原生支持 `△` 间接实现 `✗` 不支持 `?` 未验证。运镜定义见 [`../shot-language/vocabulary.md`](../shot-language/vocabulary.md)。

| 运镜 | Seedance 2.0 | Kling 3.0 | H3 |
| --- | --- | --- | --- |
| Static locked | ✓ 极高 | ✓ 最高稳定 | ✓ |
| Dolly-in / Push-in | ✓ 支持 slow/medium/fast | ✓ 精准 | ✓ 自然英语 Push In |
| Dolly-out / Pull-back | ✓ | ✓ | ✓ Pull Out |
| Orbit / Arc | ✓ 单拍，需指定方向+半径 | △ 需多镜头拼接 | ✓ Arc Shot |
| Tracking | ✓ | ✓ 需显式空间锚点 | ✓ Tracking Shot |
| Pan / Tilt | ✓ | ✓ | ✓ Pan Left/Right, Tilt Up/Down |
| Crane up/down | ✓ | △ 拆成复合指令 | ✓ Pedestal Up/Down |
| Handheld | ✓ | △ Motion Brush | ✓ Shake Slightly |
| Rack focus | ✓ 复合指令 | ? | ? |
| Whip pan | ✓ | ✗ | ? |
| Hitchcock zoom | ✓ 复合描述 | ? | ? |
| POV first-person | ✓ | △ 需多镜头 | ✓ POV |

## 成本门与单价

- **Seedance 2.0**：按秒计费，Mini/Pro 两档；成本以 `--dry-run` 预览返回值为准。
- **H3 · autodl_comfyui**（workflow `minimax_h3_lightx2v_v5`）：480p/768p ¥0.01/s，1080p ¥0.10/s；ref_image_0 必填。
- **H3 · autodl_minimax**（原生 v2）：768P ¥0.45-0.50/s，2K ¥0.72-0.80/s；图片输入 5 张内免费，超出 ¥0.18-0.20/张。
- 生成前一律 `--dry-run` 预览请求体与估算成本，人确认后真跑。

## 版权过滤器

Seedance 2.0（2026-07 实测）不拦截单角色名，拦截**特征组合**（辨识度达阈值时整段拦截）。规避：按角色域拆分生成段；参考图避免完整标志性特征；特征级规避优于名称级规避。H3 行为待实测——若存在特征组合拦截，沿用同策略。执行发现写入时标注 `[源:执行发现·单次验证]`，同一观察 ≥2 次后升级为正式约束。
