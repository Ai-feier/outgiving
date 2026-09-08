"""AI 生成基础设施——核心层（provider 无关）。

分层：核心层 ai/ → 实现层 ai/providers/。依赖方向唯一：
核心层在运行时通过 registry 懒加载 providers；适配器只依赖 ai.models + 自家 auth。

注意：本包**不急切导入任何 provider**——某个 provider 挂掉不影响 `import ai`。
provider 类通过注册表获取（get_video_generator 等），或直接 `ai.providers.<name>` 导入。

用法（agent）：
    from ai import get_video_generator, get_image_generator, get_tts, get_music_generator
    from ai.models import VideoPrompt, VideoResult
"""

from ai.models import (
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
from ai.registry import (
    available_models,
    check_connectivity,
    get_config,
    get_image_generator,
    get_music_generator,
    get_tts,
    get_video_generator,
)

__all__ = [
    # 注册表（推荐入口）
    "get_video_generator",
    "get_image_generator",
    "get_tts",
    "get_music_generator",
    "get_config",
    "available_models",
    "check_connectivity",
    # 模型
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
