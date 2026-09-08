"""
生成 Ichigo True Shikai 角色设计稿。
- 布局参考图：Yhwach_design-sheet_v01.png（本地文件，base64 data URI）
- Seedream 5.0，单图生成
- 输出：IchigoTS_design-sheet_v01.png
"""

import sys
from pathlib import Path

# 将项目根加入 sys.path
_project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_project_root))

from scripts.src.ai.providers.volcengine.seedream import SeedreamImage
from scripts.src.ai.models import ImagePrompt
from scripts.src.ai._utils import image_to_data_uri


def main():
    # 路径
    ref_image = Path(
        _project_root
        / "ai-video/projects/T003/assets/ref-images/Yhwach_design-sheet_v01.png"
    )
    output_path = Path(
        _project_root
        / "ai-video/projects/T003/assets/ref-images/IchigoTS_design-sheet_v01.png"
    )

    # 参考图 → data URI
    print(f"[1/4] 读取布局参考图: {ref_image}")
    ref_uri = image_to_data_uri(ref_image)
    print(f"      base64 data URI: {len(ref_uri)} chars")

    # Prompt（来自 gate 文件）
    prompt_text = """Character design sheet of Ichigo Kurosaki from Bleach Thousand Year Blood War arc, True Shikai form. Same layout format and art style as the reference image: three-panel composite on solid dark grey background.

[LEFT PANEL — front portrait, head to chest]
Front-facing portrait, young man with sharp pointed jawline, narrow chin. Thin sharp eyes with slight upward tilt at outer corners. Angular prominent nose bridge with straight bridge from brows to tip. Thin straight mouth, slightly tightened — neutral expression, no smile. Eyes slightly lowered looking down-left at 15 degree angle. Orange spiky hair in thick pointed tufts — 4-5 front tufts rising upward at different angles, 2-3 side tufts flaring outward, each tuft tapered to sharp point, vibrant orange #E8760B. Black shihakusho collar open at neck, white inner layer visible at collarbone. Bleach cel-shaded anime style, high contrast flat shading. Lighting: cold rim light from upper-right on left face edge, deep blue-black shadow #0D0D14 on right face side.

[MIDDLE PANEL — 3/4 profile view, head to waist]
3/4 profile showing torso depth and blade positioning. Orange spiky tufts visible from angle showing depth and volume. Sharp jawline profile visible. Dual Zangetsu blades crossed in X-shape before chest: (1) Long blade in right hand, lower position — dark metallic grey-black blade #2A2A3A, purple handle with faint 卍 (manji) pattern, dark pentagonal handguard, hollowed section near handle; (2) Short blade in left hand, upper position — same dark metallic grey-black but irregular jagged edges like bitten blade, pure black handle held through hollow center. Black shihakusho with wide sleeves, white inner wraps at wrists where sleeves pull back. Cold rim light from upper-right on face, shoulder, and blade edges creating metallic white highlight #B0B0C0 on blade edge.

[RIGHT PANEL — full body standing, head to toe]
Full body standing pose, body facing front with slight 1/8 turn. Orange spiky hair, neutral expression. Black shihakusho with wide hakama pants falling straight to just above ankle. White ankle wraps with straw sandals (geta). Black belt at waist. NO scabbard — important distinction. Dual Zangetsu blades crossed in X-shape before chest matching middle panel. Stance: standing straight, weight centered evenly on both feet, shoulders-width apart, neutral calm posture.

Style: clean cel-shaded anime lineart, high contrast flat color blocks, bleach thousand year blood war aesthetic. No soft gradient, no bloom, no photorealistic.

Prohibited: no smile, no bankai, no single blade, no horn of salvation, no scabbard, no action pose, no energy effects, no reiatsu, no weapon glow, no dramatic lighting, no soft shading, no complex background."""

    # 构建 ImagePrompt
    print("[2/4] 构建 ImagePrompt...")
    prompt = ImagePrompt(
        prompt=prompt_text,
        reference_image_url=ref_uri,  # 布局参考图
        size="2K",
        output_format="png",
        watermark=False,
        optimize_mode="standard",
    )

    # 生成
    print(f"[3/4] Seedream 5.0 生成中... (输出: {output_path})")
    gen = SeedreamImage(model="5.0")
    result = gen.generate_to_file(prompt, output_path)

    # 结果
    print(f"[4/4] 完成!")
    print(f"      文件: {output_path}")
    print(f"      result.images: {result.images}")
    print(f"      result.created: {result.created}")

    # 文件大小
    if output_path.exists():
        size_kb = output_path.stat().st_size / 1024
        print(f"      文件大小: {size_kb:.0f} KB")

    return 0


if __name__ == "__main__":
    sys.exit(main())
