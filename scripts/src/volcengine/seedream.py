"""
Seedream — AI 图像生成适配器 (ARK API)。

Volcengine ARK 平台，支持文生图/图生图/组图生成。
Model IDs: doubao-seedream-5-0-260128 / doubao-seedream-4-5-251128 / doubao-seedream-4-0。

Agent 使用路径：
    visual-designer → P0 参考图规格 → SeedreamImage.generate() → ref-images/*.png
"""

from __future__ import annotations

import base64
import json
import urllib.request
from pathlib import Path
from typing import Any

from volcengine._auth import Credentials, get_credentials
from volcengine._http import VolcError
from volcengine.models import ImagePrompt, ImageResult


ARK_BASE = "https://ark.cn-beijing.volces.com/api/v3"
ARK_IMAGES = f"{ARK_BASE}/images/generations"

MODELS = {
    "5.0": "doubao-seedream-5-0-260128",
    "4.5": "doubao-seedream-4-5-251128",
    "4.0": "doubao-seedream-4-0",
}


class SeedreamImage:
    """Seedream 图像生成器 (ARK API)。

    使用方式：
        gen = SeedreamImage()
        result = gen.generate(ImagePrompt(
            prompt="Bleach style anime, Ichigo Kurosaki in dual-wield form...",
            size="2K",
        ))
        for img in result.images:
            print(img["url"])

        # 保存到文件
        gen.generate_to_file(prompt, "ref-images/IchigoDualWield_v01.png")
    """

    def __init__(self, creds: Credentials | None = None, model: str = "5.0"):
        self._creds = creds or get_credentials()
        self._model = MODELS.get(model, model)

    # ── public API ──────────────────────────────────────────

    def generate(self, prompt: ImagePrompt) -> ImageResult:
        """提交图像生成（同步，直接返回结果）。"""
        body = self._build_request(prompt)
        data = self._call(body)
        return self._parse_response(data)

    def generate_to_file(
        self, prompt: ImagePrompt, output_path: str | Path
    ) -> ImageResult:
        """生成图像并下载到文件。支持组图——多张时自动编号。"""
        result = self.generate(prompt)
        path = Path(output_path).resolve()  # 强制绝对路径，避免工作目录依赖
        path.parent.mkdir(parents=True, exist_ok=True)

        if len(result.images) == 1:
            url = result.images[0].get("url", "")
            if url:
                urllib.request.urlretrieve(url, path)
        else:
            stem = path.stem
            suffix = path.suffix
            for i, img in enumerate(result.images):
                url = img.get("url", "")
                if url:
                    numbered = path.with_stem(f"{stem}_{i + 1:02d}")
                    urllib.request.urlretrieve(url, numbered)

        return result

    # ── private ─────────────────────────────────────────────

    def _build_request(self, prompt: ImagePrompt) -> dict[str, Any]:
        """将语义 ImagePrompt 转为 ARK Image Generation API 请求体。"""
        req: dict[str, Any] = {
            "model": self._model,
            "prompt": prompt.prompt,
            "size": prompt.size,
            "output_format": prompt.output_format,
            "response_format": prompt.response_format,
            "watermark": prompt.watermark,
        }

        # Gap 3: negative_prompt
        if prompt.negative_prompt:
            req["negative_prompt"] = prompt.negative_prompt

        # Gap 6: sequential_image_generation — 5.0 Pro 不支持
        if "5-0" in self._model and "pro" in self._model.lower():
            pass  # 5.0 Pro does not support sequential_image_generation
        else:
            req["sequential_image_generation"] = prompt.sequential_image_generation

        # Gap 7: optimize_mode — 5.0 不支持 "fast"
        is_5_0 = "5-0" in self._model
        if is_5_0 and prompt.optimize_mode == "fast":
            import warnings

            warnings.warn(
                "optimize_mode='fast' not supported for Seedream 5.0, "
                "falling back to 'standard'"
            )
            req.setdefault("optimize_prompt_options", {})["mode"] = "standard"
        elif prompt.optimize_mode:
            req.setdefault("optimize_prompt_options", {})
            req["optimize_prompt_options"]["mode"] = prompt.optimize_mode

        # 参考图（1-14 张）
        if prompt.reference_image_url:
            urls = (
                prompt.reference_image_url
                if isinstance(prompt.reference_image_url, list)
                else [prompt.reference_image_url]
            )
            req["image"] = urls[:14]

        return req

    def _call(self, body: dict[str, Any]) -> dict[str, Any]:
        body_bytes = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            ARK_IMAGES,
            data=body_bytes,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._creds.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))  # type: ignore[no-any-return]
        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8", errors="replace")
            try:
                err = json.loads(body_text)
                msg = err.get("error", {}).get("message", body_text)
            except json.JSONDecodeError:
                msg = body_text
            raise VolcError(str(e.code), msg) from e

    def _parse_response(self, data: dict[str, Any]) -> ImageResult:
        """解析 ARK Image API 响应。"""
        return ImageResult(
            images=data.get("data", []),
            created=data.get("created", 0),
            usage=data.get("usage", {}),
        )
