# H3 Seg2 — 爆发（5.0–10.0s，段内 0.0–5.0s）· I2VA

Input Mode: I2VA（ref_image_0 = 段 1 赢家末帧，本地 PNG → CLI 自动转 data URI；<Picture 2> = 官方形态图 001, <Picture 3> = 官方场景图 002，身份加强参考）
Duration: 5s（CLI --duration 5）
Resolution: 768p横（CLI --resolution）
Purpose: 段 2 生成单元；首帧 = 段 1 末帧（正手持落定姿态），经「0.00s fully referenced」对齐指令承接
Parser 约束: 三核心字段值必须各占单行（CLI 按行切块，字段值内换行会丢内容——实测 2026-08-24）
前置门禁: 段 1 末帧必须已存在（assets/last-frames/），否则阻塞本段生成（Hard Rule 2）

For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

How the reference pictures align with the target video — Picture 1 is the last frame of the previous segment, showing the completed form in the locked horizontal-blade stance; Pictures 2 and 3 are official identity references of the same character; keep the character, colors, mask, horns, chains and pose identical to Picture 1 from the start.

integrated_multimodal_description: [Shot 1] 2D-animated, high-contrast cel-shaded anime style, the shot begins on a close-up of the eye region of the black mask worn by the man shown in <Picture 1>, who remains in the exact locked stance of <Picture 1> — two full curved horns, complete black mask that is black not white, blood-red chains blazing at neck, wrists and ankles, the transformed blade held horizontally at his side, head raised — inside the pitch-black ink-wash void with its blood-red glow; both eyes open as a deep blood-red light shines through and around the eye region of the mask, and the whole figure holds a still, time-stopped pause while the chains pulse once; the camera holds a static shot then pulls back with small amplitude at slow speed to reveal the full figure, still held. [Shot 2] At 00:01.000, the shot cuts to the charge: the man lunges straight toward the camera, blade leading, full anime speed lines streaking to the frame edges, strong motion blur on the surroundings while his form stays sharp, the ink-wash void whipping past on both sides; the camera pushes in rapidly at fast speed as he closes the distance, the angle rising from low to eye level. [Shot 3] At 00:03.000, the shot transitions to the release: a massive black-red Cero torrent erupts and rushes directly at the camera lens, growing rapidly and punching through the frame until the entire image is filled with black and red ink-wash energy, the figure partially visible inside its own discharge, then the frame holds for the final 0.5 seconds with the energy fully filling the screen.

overall_soundscape: A low resonant hum with a single deep pulse of the chains in the still opening, then the sharp crack of displaced air as he lunges, a high tearing whoosh of speed lines through the middle second, and finally a massive roaring boom of black-red energy surging past the lens that swallows all other sound.

non_diegetic_music: The low pulsing ostinato carries from the previous segment to a peak with driving percussion over the first three seconds, then cuts abruptly to a single sustained low tone that decays into near-silence as the frame fills with the energy discharge, no vocals.
