---
unit: seg2
follows: [goal2]
gate: 是
层: l2
---

# Seg2 运行卡 · 爆发（吃 seg1 末帧）

> 状态: 就绪

## ① 简层

本次运行：Seg2 · 爆发 生成（H3，5s，768p横），注入 seg1 末帧作 ref_image_2。内容见 `script.md` ② · 节拍序列 · 段 2。前置门禁：seg1 end 出片 + 人目验通过 + 门 4 终审。

## ② 思考

- 执行决策（引用，不复述）：
  - 末帧注入路径：H3 = 追加 `ref_image_2`（`director.md` ② · 5. 末帧接续规范 · 5.2 provider 对照）
  - 与 seg1 同 provider 同规格（A/B 可比性）
  - 生成后段接缝验证：Hard Rule 3（director ② · 5.3）

### 假设与未锚

- 假设：seg1 末帧作 ref_image_2 可保持形态连续；未锚：段接缝 SSIM 验证（生成后，Hard Rule 3）。

### grill 记录

## ③ 内容详情

执行对象：`exec/video-prompt-h3-seg2.md`（三镜时序 + 末帧注入 ref_image_2，见 director.md ③ · 3.2）；产出 = seg2 mp4（④ 执行后写 Run 卡）。

## ④ 执行

- prompt-file: exec/video-prompt-h3-seg2.md
- provider: autodl_comfyui
- duration: 5
- resolution: 768p横
- refs: assets/ref-images/001_char_KessaIchigo_official_85246_img2.jpg, assets/ref-images/002_char_KessaIchigo_official_85246_img1.jpg, assets/frames/seg1-h3-last.png
- agent: video-director
- skill: 无
- model: minimax_h3_lightx2v_v5
- 命令（末帧就位后执行）：`uv run --directory scripts ai -p autodl_comfyui generate video --prompt-file <abs> -r <001 abs> -r <002 abs> -r <末帧 abs> -d 5 -o <abs>`

- [x] dry-run（director 已验证 4 prompt）
- [x] refs 可解析（含 seg1 末帧）
- [x] 成本 ≤¥0.05

## ⑤ 结果

⏳ 待执行。出片后本 end 写：Run N · provider · 日期 · 视频/首尾帧/SSIM/成本/耗时 + 段接缝验证结果 + 交接 end 单元。
