"""
原生数据结构 — 3 层：Asset → Segment/Track → Composition。
不绑定任何渲染引擎，纯数据。
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ── L1: 源素材 ────────────────────────────────────────────


@dataclass
class Asset:
    """一个源文件。资产的身份信息。"""

    id: str  # "clip-a"
    path: str  # 文件路径
    type: str = "video"  # "video" | "audio" | "image"
    duration: float = 0.0  # 秒，probe 自动填
    width: int = 0
    height: int = 0


# ── L2: 时间线片段 ─────────────────────────────────────────


@dataclass
class Keyframe:
    """变换关键帧。"""

    at: float  # 相对片段起点的秒数
    scale: float = 1.0
    position: tuple[float, float] = (0.5, 0.5)  # 相对画布中心
    rotation: float = 0.0
    easing: str = "linear"  # linear | ease-in | ease-out | ease-in-out


@dataclass
class Segment:
    """轨道上的一个片段 — 把源素材的 [src_start, src_end] 放到时间线的 tl_start。"""

    id: str  # "hook" | "body-1"
    asset_id: str  # → Asset.id
    src_start: float
    src_end: float
    tl_start: float
    # 处理指令（全部可选，空=不做）
    speed: float = 1.0
    volume: float = 1.0
    fade_in: float = 0.0
    fade_out: float = 0.0
    mask: str = ""  # "circle(0.5,0.5,0.6,feather=0.08)" | "linear(0.5,0.5,0,feather=0.1)"
    blend: str = ""  # "multiply" | "screen" | "overlay"
    opacity: float = 1.0
    keyframes: list[Keyframe] = field(default_factory=list)
    adjustments: dict[str, float] = field(default_factory=dict)  # {brightness, contrast, saturation, vignette}
    tags: list[str] = field(default_factory=list)  # ["hook", "reveal", "body"]

    @property
    def tl_end(self) -> float:
        """时间线上片段结束的时间。"""
        duration = self.src_end - self.src_start
        if self.speed and self.speed != 1.0:
            duration /= self.speed
        return self.tl_start + duration

    @property
    def src_duration(self) -> float:
        return self.src_end - self.src_start


@dataclass
class Track:
    """一条轨道。video 轨 index 大 = 画面上层；audio 轨自动混音。"""

    id: str  # "main" | "bgm"
    type: str = "video"  # "video" | "audio"
    segments: list[Segment] = field(default_factory=list)


# ── L3: 字幕 ───────────────────────────────────────────────


@dataclass
class Subtitle:
    """一条字幕。"""

    text: str
    start: float
    end: float
    font: str = "PingFang SC"
    size: int = 48
    color: str = "#FFFFFF"
    outline: int = 3
    outline_color: str = "#000000"
    position: str = "bottom,120"  # "bottom,120" | "center" | "top,80"


# ── L4: 合成清单 ───────────────────────────────────────────


@dataclass
class Composition:
    """顶层。这就是剪辑决策的全部数据。"""

    name: str
    width: int = 1920
    height: int = 1080
    fps: int = 24
    assets: list[Asset] = field(default_factory=list)
    tracks: list[Track] = field(default_factory=list)
    subtitles: list[Subtitle] = field(default_factory=list)
    output: dict[str, str] = field(default_factory=dict)

    def asset_by_id(self, id: str) -> Asset | None:
        for a in self.assets:
            if a.id == id:
                return a
        return None

    @property
    def total_duration(self) -> float:
        """时间线总长。"""
        end = 0.0
        for t in self.tracks:
            for s in t.segments:
                e = s.tl_end
                if e > end:
                    end = e
        for sub in self.subtitles:
            if sub.end > end:
                end = sub.end
        return end
