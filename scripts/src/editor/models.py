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
    rotation: float = 0.0  # 度
    easing: str = "linear"  # linear | ease-in | ease-out | ease-in-out


@dataclass
class PropertyKeyframe:
    """按属性的关键帧（YAML schema：time + value + easing）。"""

    time: float  # 时间线绝对秒
    value: object  # float（rotation/volume）或 [x, y]（scale/position）
    easing: str = "linear"


@dataclass
class KeyframeSpec:
    """一组关键帧：target（asset id）+ property（scale/position/rotation）。"""

    target: str
    property: str
    values: list[PropertyKeyframe] = field(default_factory=lambda: list[PropertyKeyframe]())


@dataclass
class Mask:
    """蒙版定义（YAML Masks 节；target = asset id，timeline = [起, 止] 时间线秒）。"""

    id: str
    type: str  # circle | linear
    target: str
    timeline: tuple[float, float]
    params: dict[str, float] = field(default_factory=lambda: dict[str, float]())


@dataclass
class SubtitleStyle:
    """字幕样式（YAML Subtitle Styles 节；Subtitle.style_id 引用）。"""

    id: str
    font: str = ""
    font_size: int = 48
    primary_color: str = "#FFFFFF"
    outline_color: str = "#000000"
    outline_width: int = 3
    blur: float = 0.5
    position: tuple[float, float] = (0.5, 0.88)
    alignment: str = "center"
    animation: str = ""
    margin_bottom: int = 0
    line_spacing: float = 1.0
    max_width: int = 0


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
    blend_mode: str = ""  # YAML 语义：段级混合模式（与 track 级叠加）
    opacity: float = 1.0
    keyframes: list[Keyframe] = field(default_factory=lambda: list[Keyframe]())
    adjustments: dict[str, float] = field(
        default_factory=lambda: dict[str, float]()
    )  # {brightness, contrast, saturation, vignette, temperature}
    tags: list[str] = field(default_factory=lambda: list[str]())  # ["hook", "reveal", "body"]
    # YAML schema 扩展字段（composition.md 声明，引擎逐步消费）
    envelope: list[tuple[float, float]] = field(
        default_factory=lambda: list[tuple[float, float]]()
    )  # [(time, volume)] 音量包络
    transform_scale: tuple[float, float] | None = None  # [sx, sy]
    transform_position: tuple[float, float] | None = None  # [dx, dy] 像素偏移
    tl_span: float | None = (
        None  # YAML schema：时间线占位长度（end-start，权威）；None = 旧 src/speed 公式
    )

    @property
    def tl_end(self) -> float:
        """时间线上片段结束的时间。"""
        if self.tl_span is not None:
            return self.tl_start + self.tl_span
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
    order: int = 0
    blend_mode: str = "normal"  # normal | overlay | screen | multiply | soft_light
    opacity: float = 1.0
    segments: list[Segment] = field(default_factory=lambda: list[Segment]())


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
    style_id: str = ""  # YAML：引用 Subtitle Styles 节；空 = 用上面内联字段


# ── L4: 合成清单 ───────────────────────────────────────────


@dataclass
class Composition:
    """顶层。这就是剪辑决策的全部数据。"""

    name: str
    width: int = 1920
    height: int = 1080
    fps: int = 24
    assets: list[Asset] = field(default_factory=lambda: list[Asset]())
    tracks: list[Track] = field(default_factory=lambda: list[Track]())
    subtitles: list[Subtitle] = field(default_factory=lambda: list[Subtitle]())
    output: dict[str, str] = field(default_factory=lambda: dict[str, str]())
    # YAML schema 扩展（composition.md 声明）
    masks: list[Mask] = field(default_factory=lambda: list[Mask]())
    subtitle_styles: dict[str, SubtitleStyle] = field(
        default_factory=lambda: dict[str, SubtitleStyle]()
    )
    keyframe_specs: list[KeyframeSpec] = field(default_factory=lambda: list[KeyframeSpec]())
    chapter_markers: list[dict[str, object]] = field(
        default_factory=lambda: list[dict[str, object]]()
    )
    bg_color: str = ""
    extra_meta: dict[str, str] = field(
        default_factory=lambda: dict[str, str]()
    )  # crf/preset 等非渲染元数据

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
                end = max(end, e)
        for sub in self.subtitles:
            end = max(end, sub.end)
        return end
