"""
模型注册表。agent 不直接依赖具体实现，通过注册表获取服务。

使用方式：
    from ai import get_tts, get_video_generator
    tts = get_tts()
    video = get_video_generator()

切换提供商：修改 model_config.json 或设置环境变量
VIDEO_PROVIDER / IMAGE_PROVIDER / TTS_PROVIDER / MUSIC_PROVIDER。
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

_CONFIG_PATH = Path(__file__).resolve().parent / "model_config.json"


def _load_file_config() -> dict[str, Any]:
    """读取 model_config.json（仅文件内容；env 覆盖在 _load_config 层叠加）。

    文件缺失/损坏 → 空配置（走默认值），不阻塞启动。
    """
    try:
        with open(_CONFIG_PATH) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


@lru_cache
def _cached_file_config() -> dict[str, Any]:
    return _load_file_config()


def _load_config() -> dict[str, Any]:
    """合并默认值 + 文件配置 + 环境变量覆盖。

    env 每次调用时叠加（不被缓存吞掉），文件内容才 lru_cache。
    """
    config: dict[str, Any] = {
        "video_provider": "seedance",
        "tts_provider": "volcengine",
        "music_provider": "volcengine_genbgm",
        "image_provider": "seedream",
        "preferred_voice": "zh_female_shuangkuisi",
        "default_duration": 5,
    }
    config.update(_cached_file_config())

    # 环境变量覆盖（每次叠加，支持进程内切换测试）
    for key in ("video_provider", "image_provider", "tts_provider", "music_provider"):
        env_val = os.getenv(key.upper())
        if env_val:
            config[key] = env_val

    return config


def _cached_config() -> dict[str, Any]:
    """合并配置（文件内容已缓存；env 每次叠加，不缓存）。"""
    return _load_config()


# ── 服务工厂 ──────────────────────────────────────────────────────


def get_video_generator(model: str = "mini", provider: str | None = None):
    """获取当前配置的视频生成器实例。

    provider 取值：seedance（默认）/ autodl_comfyui / autodl_minimax。
    显式 provider（CLI -p）> 环境变量 VIDEO_PROVIDER > model_config.json。
    """
    provider = provider or _cached_config()["video_provider"]

    if provider == "seedance":
        from ai.providers.volcengine.seedance import SeedanceVideo

        return SeedanceVideo(model=model)
    if provider == "autodl_comfyui":
        from ai.providers.autodl_comfyui import AutoDLComfyUIVideo

        return AutoDLComfyUIVideo(model=model)
    if provider == "autodl_minimax":
        from ai.providers.autodl_minimax import AutoDLMiniMaxVideo

        return AutoDLMiniMaxVideo(model=model)

    raise ValueError(
        f"Unknown video provider: {provider}. Set VIDEO_PROVIDER env var or update {_CONFIG_PATH}"
    )


def get_image_generator(model: str = "5.0", provider: str | None = None):
    """获取当前配置的图像生成器实例。"""
    provider = provider or _cached_config().get("image_provider", "seedream")

    if provider == "seedream":
        from ai.providers.volcengine.seedream import SeedreamImage

        return SeedreamImage(model=model)

    raise ValueError(
        f"Unknown image provider: {provider}. Set IMAGE_PROVIDER env var or update {_CONFIG_PATH}"
    )


def get_tts():
    """获取当前配置的 TTS 实例。"""
    provider = _cached_config()["tts_provider"]

    if provider == "volcengine":
        from ai.providers.volcengine.tts import VolcengineTTS

        return VolcengineTTS()

    raise ValueError(
        f"Unknown TTS provider: {provider}. Set TTS_PROVIDER env var or update {_CONFIG_PATH}"
    )


def get_music_generator():
    """获取当前配置的音乐生成器实例。"""
    provider = _cached_config()["music_provider"]

    if provider == "volcengine_genbgm":
        from ai.providers.volcengine.genbgm import VolcengineBGM

        return VolcengineBGM()

    raise ValueError(
        f"Unknown music provider: {provider}. Set MUSIC_PROVIDER env var or update {_CONFIG_PATH}"
    )


def get_config() -> dict[str, Any]:
    """获取当前模型配置（agent 可读）。"""
    return dict(_cached_config())


def available_models() -> dict[str, list[str]]:
    """列出所有可用的模型类型和提供商。"""
    return {
        "video": ["seedance", "autodl_comfyui", "autodl_minimax"],
        "image": ["seedream"],
        "tts": ["volcengine"],
        "music": ["volcengine_genbgm"],
    }


def check_connectivity() -> dict[str, bool | str]:
    """快速检查凭证是否有效（不做实际 API 调用，只验证凭证存在）。"""
    from ai.auth import all_credentials

    result: dict[str, bool | str] = {"config_loaded": bool(_cached_config())}
    result.update(all_credentials())
    return result
