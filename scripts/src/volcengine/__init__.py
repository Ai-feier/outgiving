"""
火山引擎 AI 模型抽象层。

设计原则：
- 每个服务类型定义 Protocol 接口，具体实现可替换
- 凭证管理通过环境变量（不硬编码）
- 结构化输入输出（Pydantic 模型）
- 同步 API，agent 可直接调用

Quickstart:
    from volcengine import SeedanceVideo, VolcengineTTS, VolcengineBGM
    video = SeedanceVideo()
    result = video.submit(VideoPrompt(...))
"""

from volcengine.models import (
    VideoPrompt,
    VideoResult,
    VideoStatus,
    TTSOptions,
    TTSResult,
    MusicPrompt,
    MusicResult,
    AudioFormat,
)
from volcengine.seedance import SeedanceVideo
from volcengine.tts import VolcengineTTS
from volcengine.genbgm import VolcengineBGM
from volcengine._auth import get_credentials
from volcengine.registry import (
    get_tts,
    get_video_generator,
    get_music_generator,
    get_config,
    available_models,
    check_connectivity,
)

__all__ = [
    # Services (direct instantiation or via registry)
    "SeedanceVideo",
    "VolcengineTTS",
    "VolcengineBGM",
    # Registry (recommended for agents)
    "get_video_generator",
    "get_tts",
    "get_music_generator",
    "get_config",
    "available_models",
    "check_connectivity",
    # Models
    "VideoPrompt",
    "VideoResult",
    "VideoStatus",
    "TTSOptions",
    "TTSResult",
    "MusicPrompt",
    "MusicResult",
    "AudioFormat",
    # Auth
    "get_credentials",
]
