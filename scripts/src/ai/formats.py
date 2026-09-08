"""标准 video-prompt.md 格式解析（9 要素命名字段）。

通用默认格式——任何 provider 都能消费；provider 有专属格式时（如 H3 的
video-prompt-h3.md），由适配器的 parse_prompt_file 优先接管，本模块兜底。
"""

from __future__ import annotations

from ai.models import VideoPrompt

FIELD_KEYS = ("scene", "subject", "camera", "lighting", "style")


def parse_standard_prompt_file(
    content: str,
    scene: str | None = None,
    subject: str | None = None,
    camera: str | None = None,
    lighting: str | None = None,
    style: str | None = None,
) -> VideoPrompt:
    """解析 video-prompt.md：`- **scene**: xxx` 命名字段行。

    CLI 显式传参优先于文件值；文件缺字段时用语义默认值。
    scene 必填——调用方负责校验。
    """
    values: dict[str, str] = {}
    for line in content.split("\n"):
        line = line.strip()
        for key in FIELD_KEYS:
            marker = f"- **{key}**:"
            if line.startswith(marker):
                values[key] = line.split(":", 1)[1].strip()
                break

    explicit = {"scene": scene, "subject": subject, "camera": camera, "lighting": lighting, "style": style}
    merged: dict[str, str] = {k: (explicit[k] or values.get(k) or "") for k in FIELD_KEYS}

    return VideoPrompt(
        scene=merged["scene"],
        subject=merged["subject"],
        camera=merged["camera"] or "static camera",
        lighting=merged["lighting"] or "natural window light",
        style=merged["style"] or "cinematic, 4K",
    )
