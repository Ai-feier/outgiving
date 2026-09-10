# Seedance Seg2 — 爆发（段内 0.0–5.0s）· 末帧锚定 + 文本复述

<!--
生成命令（可复制；末帧路径由段 1 赢家决定，见 director.md §5）：
uv run --directory scripts ai -p seedance generate video \
  --prompt-file ai-video/projects/T005/exec/video-prompt-seedance-seg2.md \
  --model mini --duration 5 \
  -r ai-video/projects/T005/assets/last-frames/T005-seg1-winner-lastframe.png \
  --negative-prompt "photorealistic rendering, 3D shading, white full-face mask, modern elements, on-screen text, subtitles, UI, watermark, multiple characters, pink candy colors, low contrast, gray midtones, motion smearing, character appearance changing between shots" \
  -o ai-video/projects/T005/outputs/
说明：当前 Seedance 适配器无首帧条件化字段（仅 reference_image 角色）→ 末帧作
reference_image（角色/姿态/构图锚定）+ subject 文本复述落定姿态。若 -r 被拒或接缝漂移
> 可感知 → 去掉 -r 走纯文本复述（FreeLOC 自包含锚点），接缝处硬切 + 生成后评估。
格式：CLI 只解析 - **scene/subject/camera/lighting/style** 五行（值须单行）；audio 约束并入 style 行尾。
-->

- **scene**: The same pitch-black ink-wash void with its blood-red glow, continuing exactly from the final frame of the previous segment; one single continuous five-second sequence: a still ignition pause for the first 1 second, then a charge straight at the camera from 1 to 3 seconds, then a Cero torrent filling the frame from 3 to the end. No on-screen text, no UI.
- **subject**: The same lone young man from the previous segment in his completed transformed state — two full curved horns, a complete black mask (black, not white), long spiky orange hair, black shinigami-style robe, blood-red chains blazing at neck, wrists and ankles, the transformed blade held horizontally at his side — continuing EXACTLY from the locked ready stance of the previous segment's final frame, head raised, still. Opening (0-1s): both eyes open with a deep blood-red light shining through and around the eye region of the mask, the whole figure holds a still time-stopped pause, and the chains pulse once. Middle (1-3s): he lunges straight toward the camera, blade leading, full anime speed lines, strong motion blur on the surroundings while his form stays sharp, the ink void whipping past on both sides. End (3-5s): a massive black-red Cero torrent erupts and rushes directly at the camera, growing rapidly until the entire frame is filled with black and red energy, the figure partially visible inside its own discharge, holding the fully filled frame for the final 0.5 seconds.
- **camera**: Starts on a close-up of the mask's eye region, static, then a very slow pull-out reveals the full figure; then a rapid push-in with tracking as he charges toward the lens, the angle rising from low to eye level; then a static frame with a slight recoil as the energy hits, holding on the filled frame until the end.
- **lighting**: The blood-red eye glow opens the shot against the dark ink void; then the charging figure lit by his own blazing chains and streaking speed lines; finally the frame flooded by the self-luminous black-red Cero energy, the brightest moment of the sequence.
- **style**: 2D anime cel shading, final-chapter Bleach aesthetic, sharp line art, ink-wash texture, high contrast, deep focus, 16:9 landscape; no dialogue, no on-screen text; ambient audio only (hum, whoosh, roaring energy); the character must remain identical to the previous segment — same two horns, same black mask, same orange hair, same black robe, same chains.
