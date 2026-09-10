# Seedance Seg1 — 压抑→觉醒→锁定（0.0–5.0s）· 纯文本自足（无参考图）

<!--
生成命令（可复制）：
uv run --directory scripts ai -p seedance generate video \
  --prompt-file ai-video/projects/T005/exec/video-prompt-seedance-seg1.md \
  --model mini --duration 5 \
  --negative-prompt "photorealistic rendering, 3D shading, white full-face mask, modern elements, on-screen text, subtitles, UI, watermark, multiple characters, pink candy colors, low contrast, gray midtones, whip pan, excessive camera shake, motion smearing on static frames, character breathing movement, cloth wind movement, ambient particle animation during still frames, micro-movement in locked shots" \
  -o ai-video/projects/T005/outputs/
格式：CLI 只解析 - **scene/subject/camera/lighting/style** 五行（值须单行）；
audio 约束并入 style 行尾；negative 走 --negative-prompt 参数；16:9 由 style 行无 portrait/9:16 字样保证。
-->

- **scene**: A pitch-black ink-wash void, dark ink tendrils drifting and pressing in from all sides, deep negative space with no ground or walls visible; one single continuous five-second transformation sequence: oppressive hold for the first 1.2 seconds, then chains shattering and mask spreading from 1.2 to 3.2 seconds, then the completed form locked in a formal ready stance from 3.2 to the end. No on-screen text, no UI, no modern elements.
- **subject**: A lone young man with long spiky orange hair and a black shinigami-style robe. Opening (0-1.2s): pre-transformation state with NO horns and NO mask, crouched low, head lowered, orange hair falling over his face, blood-red chain-like energy faintly flickering under his skin at his neck, wrists and ankles, body trembling slightly as if caged and pressed down. Middle (1.2-3.2s): the blood-red chains burst and shatter outward from neck, hands and feet, a black mask crawls across his face (a black half-hollow mask, NOT a white mask), two horns push out of his head, anime speed lines appear, and the long blade in his hand glows and transforms as he rises. End (3.2-5s): completed form with two full curved horns, the complete black mask, chains fully blazing at neck, wrists and ankles, the transformed blade held horizontally at his side in a formal ready stance, head raised, body perfectly still and charged, holding the pose until the very end on a clean, sharp frame with no motion blur.
- **camera**: Low-angle medium shot; the opening sits on a locked static frame with an almost imperceptible push-in; during the transformation the camera drifts with a gentle handheld sway and a quickening push-in; then a slow push-in settles into a completely static hold for the final 1.8 seconds. No whip pans, no crane, no fast spin.
- **lighting**: Near-pitch-black ink void lit only by self-emitting blood-red glow — first faint at the chains, then stronger from the transforming blade, then full from the complete chain system; deep shadows, very high contrast, blood-red as the single light source and accent color over the black.
- **style**: 2D anime cel shading, final-chapter Bleach aesthetic, sharp line art, ink-wash texture, high contrast, deep focus, 16:9 landscape; no dialogue, no on-screen text, no subtitles; ambient audio only (low rumble, chain cracks, whoosh); keep breathing and cloth motion minimal during the final still hold so the locked frame stays clean.
