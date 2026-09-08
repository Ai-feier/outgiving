"""PNG mask generation — fast static masks instead of per-frame geq.

Circle mask: ``circle(cx, cy, size, feather=0.08)``
Linear mask: ``linear(cx, cy, rotation, feather=0.1)``

White=visible, black=transparent. Uses Pillow to evaluate the mask function
once as a 2D image — orders of magnitude faster than per-frame geq evaluation.
"""

from __future__ import annotations

import math
import tempfile
from pathlib import Path


def generate(mask_str: str, W: int, H: int) -> Path | None:
    """Generate a grayscale PNG mask (white=visible, black=transparent).

    Circle mask: ``circle(cx, cy, size, feather=0.08)``
    Linear mask: ``linear(cx, cy, rotation, feather=0.1)``

    Returns Path to a temporary PNG file, or None on failure.
    Caller must unlink the returned path.
    """
    try:
        from PIL import Image, ImageDraw, ImageFilter
    except ImportError:
        return None

    try:
        mask_type, params = _parse(mask_str)
    except (ValueError, TypeError):
        return None

    try:
        if mask_type == "circle":
            cx = params.get("cx", 0.5)
            cy = params.get("cy", 0.5)
            size = params.get("size", 0.6)
            feather = params.get("feather", 0.0)

            cx_px = int(cx * W)
            cy_px = int(cy * H)
            radius = max(1, int(size / 2 * min(W, H)))

            img = Image.new("L", (W, H), 0)
            draw = ImageDraw.Draw(img)
            draw.ellipse(
                [cx_px - radius, cy_px - radius, cx_px + radius, cy_px + radius],
                fill=255,
            )

            if feather > 0:
                # Gaussian blur creates a smooth feather transition
                blur_radius = max(1.0, feather * min(W, H) / 2)
                img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        elif mask_type == "linear":
            cx = params.get("cx", 0.5)
            cy = params.get("cy", 0.5)
            rotation = math.radians(params.get("rotation", 0.0))
            feather = params.get("feather", 0.1)

            nx = math.cos(rotation)
            ny = math.sin(rotation)
            hf = feather / 2.0
            step = hf <= 0.0  # feather=0 → 硬边（不除零）

            img = Image.new("L", (W, H), 0)

            # Evaluates the linear projection for every pixel: O(W*H), ~0.5s
            # at 1920x1080. Still far cheaper than per-frame geq evaluation.
            buf = bytearray(W * H)
            for y in range(H):
                yn = y / H - cy
                yc = yn * ny
                row = y * W
                for x in range(W):
                    xn = x / W - cx
                    proj = xn * nx + yc
                    if step:
                        val = 255 if proj >= 0 else 0
                    elif proj > hf:
                        val = 255
                    elif proj < -hf:
                        val = 0
                    else:
                        val = int(255 * (1 - abs(proj) / hf))
                    buf[row + x] = val
            img.putdata(bytes(buf))  # pyright: ignore[reportUnknownMemberType]  # Pillow stub 含 Unknown 成员

        else:
            return None

        out = Path(tempfile.mkstemp(suffix=".mask.png")[1])
        img.save(str(out), "PNG")
        return out
    except (ValueError, TypeError, ZeroDivisionError, OverflowError):
        return None


def _f(s: str, ctx: str) -> float:
    """带保护的 float 转换（mask 参数非法 → ValueError）。"""
    try:
        return float(s)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid mask number '{s}' ({ctx})") from e


def _parse(s: str) -> tuple[str, dict[str, float]]:
    """Parse 'circle(0.5,0.5,0.6,feather=0.08)' → ('circle', {...})"""
    import re

    match = re.match(r"(\w+)\((.*)\)", s)
    if not match:
        raise ValueError(f"Invalid mask: {s}")
    mask_type = match.group(1)
    param_str = match.group(2)

    params: dict[str, float] = {}
    positional = {"circle": ["cx", "cy", "size"], "linear": ["cx", "cy", "rotation"]}
    pos_names = positional.get(mask_type, [])

    parts = [p.strip() for p in param_str.split(",")]
    pos_idx = 0
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            params[k.strip()] = _f(v.strip(), f"mask param '{k}'")
        else:
            if pos_idx < len(pos_names):
                params[pos_names[pos_idx]] = _f(p, f"positional '{pos_names[pos_idx]}'")
                pos_idx += 1
            elif "feather" not in params:
                params["feather"] = _f(p, "feather")

    return mask_type, params
