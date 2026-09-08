"""
⚠️ 兼容 shim（DEPRECATED）。

AI 基础设施已分层重构：核心层 → `ai/`，实现层 → `ai/providers/`。
本包仅为旧 import 路径（`from volcengine import ...`）提供转发，**不要在新代码中使用**。

新用法：
    from ai import get_video_generator, get_image_generator, get_tts, get_music_generator
    from ai.models import VideoPrompt, ImagePrompt, ...
    from ai.providers.volcengine import SeedanceVideo, SeedreamImage, VolcengineTTS, VolcengineBGM
"""

import warnings

warnings.warn(
    "`volcengine` 包已废弃，请改用 `ai`（核心层）或 `ai.providers.volcengine`（实现层）。",
    DeprecationWarning,
    stacklevel=2,
)

from ai.models import (  # noqa: E402
    AudioFormat,
    ImagePrompt,
    ImageResult,
    MusicPrompt,
    MusicResult,
    TTSOptions,
    TTSResult,
    VideoPrompt,
    VideoResult,
    VideoStatus,
)
from ai.providers.volcengine.seedance import SeedanceVideo  # noqa: E402
from ai.providers.volcengine.seedream import SeedreamImage  # noqa: E402
from ai.providers.volcengine.tts import VolcengineTTS  # noqa: E402
from ai.providers.volcengine.genbgm import VolcengineBGM  # noqa: E402
from ai.registry import (  # noqa: E402
    available_models,
    check_connectivity,
    get_config,
    get_image_generator,
    get_music_generator,
    get_tts,
    get_video_generator,
)

__all__ = [
    "SeedanceVideo",
    "SeedreamImage",
    "VolcengineTTS",
    "VolcengineBGM",
    "get_video_generator",
    "get_image_generator",
    "get_tts",
    "get_music_generator",
    "get_config",
    "available_models",
    "check_connectivity",
    "VideoPrompt",
    "VideoResult",
    "VideoStatus",
    "ImagePrompt",
    "ImageResult",
    "TTSOptions",
    "TTSResult",
    "MusicPrompt",
    "MusicResult",
    "AudioFormat",
]
