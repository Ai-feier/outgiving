"""
共享数据模型。所有服务的输入输出定义在此。

抽象原则：
- Prompt 模型是语义层（人类/AI 可读），不绑定具体 API 格式
- 每个服务的 adapter 负责将语义模型转为 API 请求体
- 更换模型提供商 = 写新的 adapter，语义模型不变
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ── 类型化 factory（pyright strict：裸 dict/list 会推断为 Unknown） ──


def _str_dict() -> dict[str, str]:
    return {}


def _str_list() -> list[str]:
    return []


def _dict_list() -> list[dict[str, Any]]:
    return []


def _any_dict() -> dict[str, Any]:
    return {}


# ── Duration ────────────────────────────────────────────

# Seedance 2.0 legal duration values (seconds)
LEGAL_DURATIONS = (4, 5, 6, 8, 10, 12, 15)


def snap_duration(hint: int) -> int:
    """Snap to nearest legal Seedance duration value."""
    hint = max(4, min(15, hint))
    return min(LEGAL_DURATIONS, key=lambda d: abs(d - hint))


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

    # 六块公式扩展（Gap 1）
    motion: str = ""
    audio: str = ""

    # Seedance 特有：多角色标签绑定
    entity_tags: dict[str, str] = field(default_factory=_str_dict)
    # 多模态参考（Seedance 2.0 支持）
    reference_image_url: str | list[str] | None = None  # 0-9 张参考图
    reference_video_url: str | list[str] | None = None  # 0-3 个参考视频
    reference_audio_url: str | list[str] | None = None  # 0-3 个参考音频
    # 负向提示
    negative_prompt: str = ""

    # H3 特有：输出分辨率预设（480p竖/480p横/768p竖/768p横/1080p竖/1080p横/…(1:1)）。
    # 留空则由适配器从 style 推断；Seedance 忽略该字段（用 style 推断 ratio）。
    resolution: str = ""
    # 原始提示词：H3 CLI 将 video-prompt-h3.md 三核心字段装配后原样传入。
    # 设置后 to_natural_language() 不生效；Seedance 忽略。
    raw_prompt: str = ""

    # ARK API 控制参数（Gap 5）
    generate_audio: bool = True
    seed: int | None = None
    watermark: bool = True
    return_last_frame: bool = False
    service_tier: str = "default"
    priority: str = "normal"

    def to_natural_language(self) -> str:
        """合成自然语言 prompt（六块公式结构）。

        对齐 ARK 社区验证格式：
        [Subject] + [Action/Motion] + [Camera] + [Setting & Lighting]
        + [Style] + [Audio/Constraints]
        """
        parts: list[str] = []

        # 1. Subject
        parts.append(f"{self.scene}, {self.subject}")

        # 2. Action/Motion
        if self.motion:
            parts.append(self.motion)

        # 3. Camera
        if self.camera:
            parts.append(self.camera)

        # 4. Setting & Lighting
        if self.lighting:
            parts.append(self.lighting)

        # 5. Style
        if self.style:
            parts.append(self.style)

        # 6. Audio/Constraints
        if self.audio:
            parts.append(self.audio)

        # entity_tags 嵌入（Gap 2）
        if self.entity_tags:
            tag_text = " ".join(f"[{k}] is {v}" for k, v in self.entity_tags.items())
            parts.append(tag_text)

        # @ 引用语法 — reference images as character/style anchor （Gap 1）
        if self.reference_image_url:
            count = (
                len(self.reference_image_url)
                if isinstance(self.reference_image_url, list)
                else 1
            )
            refs = " ".join(f"@Image{i+1}" for i in range(count))
            parts.append(f"{refs} as reference")

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

    genres: list[str] = field(default_factory=_str_list)  # ["Alternative R&B", "Neo-Soul"]
    instruments: list[str] = field(default_factory=_str_list)  # ["layered synths", "vinyl crackle"]
    vocal_style: str = ""  # "intimate male tenor, breathy delivery"
    bpm: int | None = None
    mood: str = ""  # "深夜天台数星星的孤独"
    duration_hint: int = 30  # 秒
    structure_tags: list[str] = field(default_factory=_str_list)  # ["[Verse]", "[Chorus]"]


@dataclass
class MusicResult:
    task_id: str = ""
    audio_url: str | None = None
    duration_ms: int = 0


# ── Image Generation ─────────────────────────────────────────────


@dataclass
class ImagePrompt:
    """图像生成的语义 prompt（Seedream ARK API）。

    对齐 visual-designer 的参考图生产需求：
    - prompt: 自然语言描述
    - reference_image_url: 参考图（1-14 张，用于风格/角色锚定）
    - size: 分辨率预设或 WxH
    - sequential_image_generation: 组图模式
    """

    prompt: str
    reference_image_url: str | list[str] | None = None  # 1-14 张参考图
    size: str = "2K"  # 1K/2K/3K/4K 或 WxH
    sequential_image_generation: str = "disabled"  # "auto" 组图 1-15 张
    output_format: str = "png"
    response_format: str = "url"  # "url" 或 "b64_json"
    watermark: bool = False
    optimize_mode: str = "standard"  # "standard" 质量优先 / "fast" 速度优先
    negative_prompt: str = ""


@dataclass
class ImageResult:
    images: list[dict[str, Any]] = field(default_factory=_dict_list)  # [{"url": "...", "size": "3104x1312"}]
    created: int = 0
    usage: dict[str, Any] = field(default_factory=_any_dict)
    error_message: str | None = None
