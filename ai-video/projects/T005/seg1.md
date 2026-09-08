---
unit: seg1
follows: [director]
gate: 是
层: l1
---

# Seg1 运行卡 · 压抑→觉醒（H3）

> 状态: 完成

## ① 简层

本次运行：Seg1 A/B 首生成（H3 多图参考，5s，768p横）。内容见 `script.md` ② · 节拍序列 · 段 1；生成策略见 `director.md` ② · 自报 + `gates/gate3-design-alignment.md` §1。

## ② 思考

- 执行决策（全部引用，不复述内容）：
  - 为什么先跑 H3：A/B 对照（director ② · 自报；gate3 §1）——H3 多图参考 vs Seedance 纯文本，同段对照
  - 参考图 = 终态身份锚，非关键帧（gate3 §1）
  - 参考图走 data URI：autodl 服务端拉不了 Cloudflare CDN（管线发现，见 end）
  - 音频：H3 内置垫按 genbgm 目标风格代拟，mute 退法（红线：最终 BGM=genbgm 自产，`goal.md` ①/②）
  - 成本预算 ¥0.05（促销 1 分/秒）

### 假设与未锚

- 假设：H3 内置垫代拟 BGM 风格（mute 退法，红线见 goal ①/②）；未锚：画面内容待人/视觉模型目验（end · 待办）。

### grill 记录

## ③ 内容详情

执行对象：`exec/video-prompt-h3-seg1.md`（H3 三核心字段 prompt，alignment 终态声明 + 三镜时序，见 director.md ③ · 3.1）；产出 = seg1-h3.mp4（④ Run 1）。

## ④ 执行

- prompt-file: exec/video-prompt-h3-seg1.md
- provider: autodl_comfyui
- duration: 5
- resolution: 768p横
- refs: assets/ref-images/001_char_KessaIchigo_official_85246_img2.jpg, assets/ref-images/002_char_KessaIchigo_official_85246_img1.jpg
- agent: video-director
- skill: 无
- model: minimax_h3_lightx2v_v5
- 命令：`uv run --directory scripts ai -p autodl_comfyui generate video --prompt-file <abs路径> -r <abs路径1> -r <abs路径2> -d 5 -o <abs路径>`
  （坑：`--directory scripts` 下相对路径按 scripts/ 解析，必须绝对路径）

- [x] dry-run / 装配验证
- [x] refs 可解析（本地 → data URI）
- [x] 成本 ≤¥0.05

## ⑤ 结果

### Run 1 · autodl_comfyui · 2026-08-24 20:32 · 成功

- 视频：[seg1-h3.mp4](outputs/8202e964-5de6-4b6c-9930-6a56c24f5473.mp4) · H.264+AAC · 1344×768（768p横 ✓）· 5.167s · 4.2MB
- 客观帧指标（ffmpeg SSIM，信息级）：0.5→1.5s 0.208（爆发段）/ 1.5→2.5s 0.497 / 2.5→3.5s 0.329（形态完成）/ 3.5→4.5s 0.573（落定 hold）/ 首→尾 0.228（全片大幅变化 ✓）
- 首帧 YAVG 85.8（暗）→ 尾帧 51.65（转暗，无过曝/糊；Y 范围 16→235）
- 抽帧：[6 格总览](assets/frames/seg1-h3-contact.png) · [末帧（→ seg2 的 ref_image_2）](assets/frames/seg1-h3-last.png)
- 成本/耗时：¥0.05 / 132.9s；task ID `8202e964-5de6-4b6c-9930-6a56c24f5473`
- 待办：画面需人/视觉模型目验（对照 `assets/ref-images/` 两图 + `research.md` ② · 1.1；回校通道 OQ-1…9 = `exec/visual-assets-spec.md` ② · 3）——兼门 3 M6 证据
- 管线发现：① Cloudflare CDN 图需本地化/data URI ② `uv run --directory scripts` 相对路径按 scripts/ 解析
- 重生成：改 ①/② 或上游设计单元 → 重跑 ③ 命令 → 本 end 追加 Run 2（Run 1 保留）
