import base64
import io
from pathlib import Path


def image_to_data_uri(path: str | Path, mime: str | None = None) -> str:
    """将本地图片转为 base64 data URI。mime 自动探测 png/jpg/webp。"""
    path = Path(path).resolve()
    data = path.read_bytes()
    if mime is None:
        suffix = path.suffix.lower()
        mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
        mime = mime_map.get(suffix, "image/png")
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def validate_reference_image(uri: str, min_short_side: int = 768) -> bool:
    """校验参考图是否为 data URI 且分辨率达标。返回 True/False，不阻塞（只 warn）。

    对 URL 引用直接跳过（由服务端验证）；只检查 data URI 内嵌图片。
    """
    if not uri.startswith("data:image/"):
        return True  # URL, skip server-side check
    try:
        from PIL import Image  # lazy import — Pillow not required for editor ops
        header, encoded = uri.split(",", 1)
        data = base64.b64decode(encoded)
        img = Image.open(io.BytesIO(data))
        return min(img.size) >= min_short_side
    except Exception:
        return False  # can't validate, assume ok
