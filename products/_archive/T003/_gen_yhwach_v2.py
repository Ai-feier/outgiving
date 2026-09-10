"""
生成 Yhwach 规范参考图 v2 — 3:2 横版三栏角色设计稿。

v2 改进（vs v1 — 028_v01 9:16）：
  - 比例：9:16 竖屏 → 3:2 横版 (2400x1600)，每栏 ~800px
  - 参考图：1 张 → 3 张（030 面部线稿锚定 + 027 布局模板 + 010 全身服装）
  - 面部锚定：纯文本 → 030 多视图线稿精确锚定（胡须/眼窝/无眉线稿级验证）
  - 额头/发际线：遗漏 → 3 条深横纹 + 发际线后移（030 确认）

Gate: ai-video/projects/T003/gates/image-gen-Yhwach.md (v2)
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_project_root))

from scripts.src.volcengine.seedream import SeedreamImage
from scripts.src.volcengine.models import ImagePrompt
from scripts.src.volcengine._utils import image_to_data_uri


def main():
    base = Path(_project_root) / "ai-video/projects/T003/assets/ref-images"

    # ── 参考图路径 ──────────────────────────────────────────────
    ref_030 = base / "030_char_identity_YhwachLineArtMultiView_v01.png"   # image[0]: 面部锚定（最高权重）
    ref_027 = base / "027_lyt_layout_ThreeColumnCharSheet_v01.png"        # image[1]: 布局模板
    ref_010 = base / "010_scene_look_full_yhwach_v01.webp"                # image[2]: 全身服装
    output_path = base / "028_char_Yhwach_canonical_v02.png"

    # ── 读取参考图 → data URI ─────────────────────────────────
    print(f"[1/4] 读取 3 张参考图...")
    uri_030 = image_to_data_uri(ref_030)                     # PNG
    uri_027 = image_to_data_uri(ref_027)                     # PNG
    uri_010 = image_to_data_uri(ref_010, mime="image/webp")  # WebP
    print(f"      030 (面部锚定):  {len(uri_030)} chars")
    print(f"      027 (布局模板):  {len(uri_027)} chars")
    print(f"      010 (全身服装):  {len(uri_010)} chars")

    # ── Prompt（来自 gate v2，030 线稿精确锚定版）───────────────
    prompt_text = """BLEACH anime style character design reference sheet in 3:2 landscape horizontal canvas (2400x1600), pure black background #000000. The image is divided vertically into three equal columns.

All three views share the same neutral expression character with identical facial structure, hair, and clothing across all columns.

---

LEFT COLUMN (1/3 width = ~800px): FRONT-FACING PORTRAIT
Frame: head to upper chest. Character centered vertically in the column area.
Expression: NEUTRAL — zero expression. Mouth naturally closed, lips forming a straight horizontal line with no visible detail. Eyelids half-closed at approximately N/3 opening, upper eyelid covering the top 1/3 of the iris. Pupils looking straight forward at camera — symmetrical and centered.
Face: Rectangular broad face with wide jaw and chin. Deep-set eyes with pronounced brow ridge overhang. Mutton chop sideburns starting from front of each ear, extending along jawline to connect with mustache at mouth corners. Chin center clean-shaven. Mustache covering upper lip only, not extending below lip line. Virtually NO eyebrows visible — brow ridge area smooth with zero hair marks. Deep horizontal forehead crease — 3 distinct lines across full forehead width. High prominent cheekbones creating shadow planes.
Lighting: Symmetrical front-top 45-degree light, minimal shadow on face.
Hair: Long black hair brushed back, temple hairline receded, widow's peak at center, sideburns reaching jaw angle.

---

CENTER COLUMN (1/3 width = ~800px): THREE-QUARTER (3/4) PROFILE PORTRAIT
Frame: head to upper chest, matching left column height. Character rotated approximately 45 degrees to right, showing facial depth.
Face: Same facial features as left column from rotated angle. Deep eye socket visibly recessed — the 3/4 view shows the orbital bone depth clearly. Mutton chop sideburn visible along the visible jawline edge, thickness approximately 2cm following jaw contour. Mustache visible on upper lip profile. Ear visible — standard human ear shape, no pointed features.
Lighting: 45-degree top-left sidelight. Deep shadow on far side of face. Cool white rim light (1-2px) on the profile edge separating the jawline and nose bridge from the background.
Note: The fur collar of the white Quincy coat is visible at the bottom of this frame.

---

RIGHT COLUMN (1/3 width = ~800px): FULL-BODY STANDING POSE
Frame: Full figure from head to toe, centered vertically in column. Character facing forward, standing upright.
Pose: Arms lowered naturally at sides, hands slightly visible. Feet shoulder-width apart. Weight balanced evenly on both legs.
Clothing (head to toe):
  - White double-breasted Quincy trench coat — long white coat reaching below the knees, black inner layer visible at the lapel opening. Double row of black buttons. Wandenreich golden cross emblem centered on chest (symmetrical four-pointed cross with short arms).
  - Tattered ankle-length crimson-black cape draped over both shoulders. Dark red-black color with subtle fabric wear at the edges. Red ribbon tied near the neck at the front. Single large button closure on the left side.
  - Black tight gloves reaching from wrist to just below the elbow cuff of the coat. Gloves are skin-tight with subtle wrinkle lines at the knuckles.
  - White straight-leg trousers, falling cleanly with minimal folds.
  - Black trench boots — mid-calf height, flat sole, no buckles or decorations.
  - Fur collar visible at the top of the coat — dark grey fur trim around the collar edge.

Physical build: Imposing tall broad-shouldered older male build, 200cm height (extremely tall figure compared to standard anime proportions — the full-body should show a towering vertical presence).

---

CONSISTENCY ACROSS ALL THREE VIEWS:
- Same hair: Long black hair reaching mid-back, brushed back, temple hairline receded with widow's peak. Sideburns reaching jaw angle. Strands lie flat and smooth with subtle separation lines.
- Same skin: Pale skin tone with warm undertone #D4C4B4 base.
- Same eye color: Red iris color #CC2233 (outer ring) to #FF4466 (inner ring) gradient — multi-pupil structure where the inner iris has a secondary pupil-like ring visible, creating a layered "almighty eye" appearance. Eyes are static and non-glowing — the red is the natural iris color not an emission.
- Same facial features: rectangular face, broad chin, high cheekbones, deep-set eyes, mutton chop sideburns + mustache, no eyebrows, deep forehead crease.
- Same clothing and proportions across all views.

STYLE AND RENDERING:
- Sharp clean linework with strong outer silhouette (Bleach cel-shading standard).
- Hard cel-shaded flat colors with deep blue-black shadows at 10% brightness.
- 45-degree top-left sidelight casting deep shadows. Shadow areas shift toward deep blue-black, not neutral grey.
- Cool white rim light (1-3px) on character edges separating figure from pure black background — present in all three views.
- Background is pure black #000000. No texture, no gradient, no atmospheric effect.

No text labels, no annotations, no arrows, no color swatches, no measurement lines. No logos, no watermarks. No weapons, no sword, no bow. No smile, no anger, no arrogance, no action pose, no fighting stance. No multiple characters. Pure black background only. Professional anime character design sheet presentation."""

    negative_prompt = """realistic, 3D, photorealistic, smiling, arrogant expression, angry, laughing, grimace, smirking, action pose, fighting stance, weapon, sword, bow, gun, blade, zanpakuto, glowing eyes, glowing aura, spiritual pressure, holy energy, text, labels, numbers, annotations, arrows, color swatches, measurement lines, watermark, signature, logo, detailed background, gradient background, multiple characters, Uryu, Ishida, secondary character, Stern Ritter, Quincy army, school uniform, modern clothes, street, building, daytime, sunlight, warm lighting, full beard, goatee, stubble, chin hair, soul patch, eyebrows, thick eyebrows, bushy eyebrows, heavy eyebrows, visible eyebrows, looking away, looking up, looking down, side-eye, portrait, vertical, 9:16, ice palace, Wahrwelt, ice, snow, castle, frost, warm glow filter, soft focus, dissolve, gradient transition"""

    # ── 构建 ImagePrompt ───────────────────────────────────────
    print("[2/4] 构建 ImagePrompt (3 参考图, 2400x1600)...")
    prompt = ImagePrompt(
        prompt=prompt_text,
        reference_image_url=[uri_030, uri_027, uri_010],  # 3 张参考图
        negative_prompt=negative_prompt,
        size="2400x1600",  # 3:2 横版（非 9:16！）
        output_format="png",
        watermark=False,
        optimize_mode="standard",
    )

    # ── 生成 ────────────────────────────────────────────────────
    print(f"[3/4] Seedream 5.0 生成中... (输出: {output_path})")
    gen = SeedreamImage(model="5.0")
    result = gen.generate_to_file(prompt, output_path)

    # ── 结果 ────────────────────────────────────────────────────
    print(f"[4/4] 完成!")
    print(f"      文件: {output_path}")
    print(f"      result.images: {result.images}")
    print(f"      result.created: {result.created}")

    if output_path.exists():
        size_kb = output_path.stat().st_size / 1024
        print(f"      文件大小: {size_kb:.0f} KB")

    return 0


if __name__ == "__main__":
    sys.exit(main())
