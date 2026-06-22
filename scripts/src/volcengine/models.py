"""
共享数据模型。所有服务的输入输出定义在此。

抽象原则：
- Prompt 模型是语义层（人类/AI 可读），不绑定具体 API 格式
- 每个服务的 adapter 负责将语义模型转为 API 请求体
- 更换模型提供商 = 写新的 adapter，语义模型不变
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ── Video Generation ────────────────────────────────────────────


class VideoStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class VideoPrompt:
    """视频生成的语义 prompt。

    与 visual-designer 的六维构建法对齐：
    - scene: 景别 + 场景描述
    - subject: 主体（含实体标签和动作描述）
    - camera: 运镜指令
    - lighting: 光影
    - style: 风格 + 画质约束
    - duration_hint: 期望时长（秒），实际由模型决定
    """

    scene: str
    subject: str
    camera: str = "static camera"
    lighting: str = "natural window light"
    style: str = "cinematic, 4K"
    duration_hint: int = 5

    # Seedance 特有：多角色标签绑定
    entity_tags: dict[str, str] = field(default_factory=dict)
    # 多模态参考（Seedance 2.0 支持）
    reference_image_url: str | list[str] | None = None  # 0-9 张参考图
    reference_video_url: str | list[str] | None = None  # 0-3 个参考视频
    reference_audio_url: str | list[str] | None = None  # 0-3 个参考音频
    # 负向提示
    negative_prompt: str = ""

    def to_natural_language(self) -> str:
        """合成自然语言 prompt（通用格式）。"""
        parts = [
            f"{self.scene}, {self.subject}",
            self.camera,
            self.lighting,
            self.style,
        ]
        return ", ".join(p for p in parts if p)


@dataclass
class VideoResult:
    task_id: str
    status: VideoStatus
    video_url: str | None = None
    error_message: str | None = None


# ── TTS ──────────────────────────────────────────────────────────


class AudioFormat(str, Enum):
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"


@dataclass
class TTSOptions:
    """TTS 语音合成选项。

    对齐 rhythm-designer 的音频设计：
    - speed: 语速（0.5-2.0），默认 1.0
    - pitch: 音调偏移（-12~12），默认 0
    - volume: 音量（0.1-3.0），默认 1.0
    """

    text: str
    voice: str = "zh_female_shuangkuisisi_moon_bigtts"  # 默认中文女声
    format: AudioFormat = AudioFormat.MP3
    speed: float = 1.0
    pitch: float = 0.0
    volume: float = 1.0
    sample_rate: int = 24000


@dataclass
class TTSResult:
    audio_url: str | None = None
    audio_data: bytes | None = None  # 小音频直接返回 bytes
    duration_ms: int = 0
    format: AudioFormat = AudioFormat.MP3


# ── Music Generation ─────────────────────────────────────────────


@dataclass
class MusicPrompt:
    """音乐生成的语义 prompt。

    对齐 music-prompt skill 的核心公式：
    风格堆叠 + 乐器质感 + 人声特性 + 结构标签 + 物象场景
    """

    genres: list[str] = field(default_factory=list)  # ["Alternative R&B", "Neo-Soul"]
    instruments: list[str] = field(default_factory=list)  # ["layered synths", "vinyl crackle"]
    vocal_style: str = ""  # "intimate male tenor, breathy delivery"
    bpm: int | None = None
    mood: str = ""  # "深夜天台数星星的孤独"
    duration_hint: int = 30  # 秒
    structure_tags: list[str] = field(default_factory=list)  # ["[Verse]", "[Chorus]"]


@dataclass
class MusicResult:
    task_id: str = ""
    audio_url: str | None = None
    duration_ms: int = 0
