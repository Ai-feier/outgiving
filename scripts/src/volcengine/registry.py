"""
模型注册表。agent 不直接依赖具体实现，通过注册表获取服务。

使用方式：
    from volcengine.registry import get_tts, get_video_generator
    tts = get_tts()          # 返回当前配置的 TTS 实现
    video = get_video_generator()  # 返回当前配置的视频生成器

切换提供商：修改 model_config.json 或设置环境变量 VIDEO_PROVIDER / TTS_PROVIDER。
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from volcengine._auth import get_credentials

# ── 配置路径 ─────────────────────────────────────────────────────

_CONFIG_PATH = Path(__file__).resolve().parent / "model_config.json"


def _load_config() -> dict[str, Any]:
    """加载模型配置，环境变量覆盖文件配置。"""
    config: dict[str, Any] = {
        "video_provider": "seedance",
        "tts_provider": "volcengine",
        "music_provider": "volcengine_genbgm",
        "preferred_voice": "zh_female_shuangkuisi",
        "default_duration": 5,
    }

    if _CONFIG_PATH.exists():
        with open(_CONFIG_PATH) as f:
            file_config = json.load(f)
        config.update(file_config)

    # 环境变量覆盖
    for key in ("video_provider", "tts_provider", "music_provider"):
        env_val = os.getenv(key.upper())
        if env_val:
            config[key] = env_val

    return config


@lru_cache()
def _cached_config() -> dict[str, Any]:
    return _load_config()


# ── 服务工厂 ──────────────────────────────────────────────────────


def get_video_generator():
    """获取当前配置的视频生成器实例。"""
    config = _cached_config()
    provider = config["video_provider"]

    if provider == "seedance":
        from volcengine.seedance import SeedanceVideo
        return SeedanceVideo()

    raise ValueError(
        f"Unknown video provider: {provider}. "
        f"Set VIDEO_PROVIDER env var or update {_CONFIG_PATH}"
    )


def get_tts():
    """获取当前配置的 TTS 实例。"""
    config = _cached_config()
    provider = config["tts_provider"]

    if provider == "volcengine":
        from volcengine.tts import VolcengineTTS
        return VolcengineTTS()

    raise ValueError(
        f"Unknown TTS provider: {provider}. "
        f"Set TTS_PROVIDER env var or update {_CONFIG_PATH}"
    )


def get_music_generator():
    """获取当前配置的音乐生成器实例。"""
    config = _cached_config()
    provider = config["music_provider"]

    if provider == "volcengine_genbgm":
        from volcengine.genbgm import VolcengineBGM
        return VolcengineBGM()

    raise ValueError(
        f"Unknown music provider: {provider}. "
        f"Set MUSIC_PROVIDER env var or update {_CONFIG_PATH}"
    )


def get_config() -> dict[str, Any]:
    """获取当前模型配置（agent 可读）。"""
    return dict(_cached_config())


def available_models() -> dict[str, list[str]]:
    """列出所有可用的模型类型和提供商。"""
    return {
        "video": ["seedance"],
        "tts": ["volcengine"],
        "music": ["volcengine_genbgm"],
    }


def check_connectivity() -> dict[str, bool]:
    """快速检查凭证是否有效（不做实际 API 调用，只验证凭证存在）。"""
    try:
        creds = get_credentials()
        return {
            "credentials_ok": bool(creds.ak and creds.sk),
            "api_key_ok": bool(creds.api_key),
            "config_loaded": bool(_cached_config()),
        }
    except Exception as e:
        return {"error": str(e)}
