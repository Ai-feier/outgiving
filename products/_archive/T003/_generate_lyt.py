"""
T003 — LYT 布局参考图生成脚本。

调用 Seedream 5.0 Pro 生成三栏角色设计稿布局参考图。
使用 002_keyvisual 作为画风参考（仅 style lock，非身份锚定）。

Usage: uv run --directory scripts python ../../ai-video/projects/T003/_generate_lyt.py
"""

import sys
from pathlib import Path

# 将 scripts 目录加入 path
SCRIPTS_DIR = Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from src.volcengine.seedream import SeedreamImage
from src.volcengine.models import ImagePrompt


OUTPUT_DIR = Path(__file__).resolve().parent / "assets" / "ref-images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPT = (
    "Anime character design reference sheet in 9:16 portrait orientation, "
    "pure black background (#000000). "
    "The image is divided vertically into three equal columns "
    "by thin white vertical divider lines:\n\n"
    "Left column (1/3 width): Front-facing portrait of a generic anime-style girl "
    "with short blue hair, neutral expression. Head and shoulders framing, "
    "eyes looking directly at camera. Symmetrical lighting on face.\n\n"
    "Center column (1/3 width): Three-quarter (3/4) profile view of the same character, "
    "head and shoulders framing. Face rotated approximately 45 degrees to show "
    "facial depth and side profile. Subtle shadow on the far side of face.\n\n"
    "Right column (1/3 width): Full-body standing pose, facing forward, "
    "arms at sides naturally. Complete figure visible from head to toe, "
    "showing full outfit (simple school uniform) and body proportions.\n\n"
    "All three views show the same character with consistent coloring, "
    "hairstyle, clothing, and lighting. Professional anime character design sheet format. "
    "Thin vertical divider lines clearly separate the three columns. "
    "No background elements, no text labels, no logos. "
    "Sharp clean linework, flat color with cel-shaded style."
)

NEGATIVE_PROMPT = (
    "realistic, 3D, photorealistic, Yhwach, Bleach character, "
    "multiple characters, weapons, action pose, smiling, angry, "
    "text, labels, numbers, watermark, signature, logo, "
    "detailed background, gradient background, grey background"
)


def main():
    gen = SeedreamImage(model="5.0")

    prompt = ImagePrompt(
        prompt=PROMPT,
        reference_image_url=[
            "https://static.animecorner.me/2023/07/bleach-tybw-part-2-visual.jpg",
        ],
        size="1440x2560",
        output_format="png",
        optimize_mode="standard",
        watermark=False,
        negative_prompt=NEGATIVE_PROMPT,
    )

    output_path = str(OUTPUT_DIR / "027_lyt_layout_ThreeColumnCharSheet_v01.png")
    print(f"Generating LYT layout reference image...")
    print(f"Output: {output_path}")
    print(f"Prompt length: {len(PROMPT)} chars")
    print(f"Reference: 002_keyvisual_TYBW_Part2_Yhwach_Uryu_v01.jpg (style only)")

    result = gen.generate_to_file(prompt, output_path)

    if result.images:
        print(f"\nSUCCESS: {len(result.images)} image(s) generated")
        for i, img in enumerate(result.images):
            print(f"  [{i}] url={img.get('url', 'N/A')}, size={img.get('size', 'N/A')}")
    else:
        print(f"\nFAILED: no images returned")
        if hasattr(result, 'error_message') and result.error_message:
            print(f"  error={result.error_message}")


if __name__ == "__main__":
    main()
