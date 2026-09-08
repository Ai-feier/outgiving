"""
H3 workflow 输入装配（autodl_comfyui 的 H3 专用逻辑）。

MiniMax H3 多图参考生视频 workflow（minimax_h3_lightx2v_v5）的：
- 语义 VideoPrompt → workflow 请求体（prompt/duration/resolution/seed/ref_image_0..8）
- video-prompt-h3.md 三核心字段解析与装配（格式归格式的所有者）
- 分辨率预设与 style 推断、成本估算

API 约束（autodl.art 文档）：
- prompt 必填；duration 整数 1-10s（默认 5）
- resolution 9 档预设；ref_image_0 必填 + ref_image_1..8 选填（JPG/PNG/WebP URL）
"""

from __future__ import annotations

import re
from typing import Any

from ai.models import VideoPrompt

# ── video-prompt-h3.md 解析（三核心字段） ───────────────────

H3_FIELD_LABELS = (
    "integrated_multimodal_description",
    "overall_soundscape",
    "non_diegetic_music",
)

H3_ALIGN_KEYWORDS = ("For the target video, at 0.00 seconds", "How the reference pictures align")


def is_h3_prompt_file(content: str) -> bool:
    """检测 video-prompt-h3.md：含三核心字段任一标签。"""
    return any(label in content for label in H3_FIELD_LABELS)


def _is_block_start(line: str) -> bool:
    """判断一行是否为新的语义块（结束当前 H3 字段的值）。"""
    if not line:
        return False
    if line.startswith(("#", "---")):
        return True
    for label in H3_FIELD_LABELS:
        if line.startswith((label + ":", "**" + label + "**")):
            return True
    # 属性行：**名字**: / 名字： （输入模式、参考图声明块等）
    return bool(re.match(r"^\*?\*?[^\s*:：]+[^*]*\*?\*?\s*[:：]", line))


def parse_fields(content: str) -> dict[str, str]:
    """从 video-prompt-h3.md 提取三核心字段。

    值延续到下一个字段标签/标题/分隔线/属性行；段内空行保留。
    'alignment' 键存放 I2VA/FL2VA/L2VA 对齐指令（放到 prompt 首行）。
    非 H3 格式返回空 dict。
    """
    if not is_h3_prompt_file(content):
        return {}

    lines = content.split("\n")
    fields: dict[str, str] = {}
    alignment: list[str] = []
    current: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal current, buf
        if current is not None:
            value = "\n".join(buf).strip()
            if value:
                fields[current] = value
        current = None
        buf = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""

        matched: str | None = None
        for label in H3_FIELD_LABELS:
            if re.match(rf"^\*?\*?{re.escape(label)}\*?\*?\s*[:：]", stripped):
                matched = label
                break

        if matched:
            flush()
            current = matched
            parts = re.split(r"[:：]", stripped, maxsplit=1)
            value = parts[1].strip() if len(parts) == 2 else ""
            if value.startswith("**") and value.endswith("**"):
                value = value[2:-2]
            buf = [value] if value else []
        elif current is not None:
            if any(k in stripped for k in H3_ALIGN_KEYWORDS):
                alignment.append(stripped)  # 对齐指令提到 prompt 顶部
            elif _is_block_start(stripped):
                flush()
            elif not stripped:
                # 空行：仅当下行是新块时才结束字段，否则保留为段内空行
                if _is_block_start(next_line):
                    flush()
                else:
                    buf.append("")
            else:
                buf.append(line)
        else:
            if any(k in stripped for k in H3_ALIGN_KEYWORDS):
                alignment.append(stripped)

    flush()
    if alignment:
        fields["alignment"] = "\n".join(alignment).strip()
    return fields


def compose(fields: dict[str, str]) -> str:
    """装配最终 H3 prompt：对齐指令(若有) + 三核心字段，按 skill 顺序。"""
    parts: list[str] = []
    if fields.get("alignment"):
        parts.append(fields["alignment"])
    for label in H3_FIELD_LABELS:
        if fields.get(label):
            parts.append(f"{label}: {fields[label]}")
    return "\n\n".join(parts)


def parse_prompt_file(content: str) -> VideoPrompt | None:
    """解析 video-prompt-h3.md → VideoPrompt(raw_prompt=装配串)。非 H3 格式返回 None。

    参考图由 CLI 统一从 --ref-images 与文件 ![]() 提取，不在这里装配。
    """
    fields = parse_fields(content)
    if not fields:
        return None
    return VideoPrompt(scene="", subject="", raw_prompt=compose(fields))


# 分辨率预设（API 枚举）
RESOLUTIONS = (
    "480p竖",
    "480p横",
    "1080p横",
    "768p竖",
    "768p横",
    "1080p竖",
    "480p(1:1)",
    "768p(1:1)",
    "1080p(1:1)",
)

# 价格：元/秒（480p/768p 全场促销价 1 分/秒，2026-08；1080p 未入促销，按原价估）
COST_PER_SECOND = {"480p": 0.01, "768p": 0.01, "1080p": 0.10}

MIN_DURATION = 1
MAX_DURATION = 10
MAX_REF_IMAGES = 9

# 各 workflow 的时长上限（秒）。15s 版工作流放宽到 15；其余默认 10。
# 已知的 7 个 H3 工作流（autodl.art ComfyUI 组，2026-08 目录）：
#   minimax_h3_lightx2v_v5           多图参考（默认）
#   minimax_h3_lightx2v_v5_15s      多图参考 15s
#   minimax_h3_image_audio_to_video_v2       多图多音频
#   minimax_h3_image_audio_to_video_v2_15s   多图多音频 15s
#   minimax_h3_image_audio_to_video          图生音频同步（自动对口型）
#   minimax_h3_lightx2v                  首尾帧
#   minimax_h3_lightx2v_no_pic           文生视频（无参考图）
# 后 5 个尚未接（音频/首尾帧入参、无参考图装配未验证），见 __init__.py 的 RESERVED_WORKFLOWS。
WORKFLOW_DURATION_CAPS: dict[str, int] = {
    "minimax_h3_lightx2v_v5_15s": 15,
    "minimax_h3_image_audio_to_video_v2_15s": 15,
}


def snap_duration(hint: int, workflow: str = "minimax_h3_lightx2v_v5") -> int:
    """H3 合法时长：整数 1–上限（越界截断；上限随 workflow）。"""
    cap = WORKFLOW_DURATION_CAPS.get(workflow, MAX_DURATION)
    if hint < MIN_DURATION:
        return MIN_DURATION
    if hint > cap:
        return cap
    return hint


def resolution_from_style(style: str) -> str:
    """从 style 推断分辨率预设；无法推断时用 API 默认 768p竖。"""
    s = style.lower()
    if "portrait" in s or "9:16" in s or "竖" in s:
        return "768p竖"
    if "square" in s or "1:1" in s or "方块" in s:
        return "768p(1:1)"
    if "landscape" in s or "16:9" in s or "横" in s:
        return "768p横"
    return "768p竖"


def estimate_cost(duration: int, resolution: str) -> float:
    """按分辨率档位估算生成成本（元）。"""
    tier = next((t for t in ("480p", "768p", "1080p") if t in resolution), "768p")
    return duration * COST_PER_SECOND[tier]


def build_request(prompt: VideoPrompt, workflow: str) -> dict[str, Any]:
    """语义 VideoPrompt → H3 workflow API 请求体。

    - prompt 用 raw_prompt（CLI 装配的三核心字段）或 to_natural_language()
    - 参考图 ref_image_0..8（第 0 张必填——H3 多图参考约束）
    """
    text = prompt.raw_prompt or prompt.to_natural_language()

    duration = snap_duration(prompt.duration_hint, workflow)

    req: dict[str, Any] = {
        "prompt": text,
        "duration": duration,
        "resolution": _resolve_resolution(prompt),
    }
    if prompt.seed is not None:
        req["seed"] = prompt.seed

    refs = prompt.reference_image_url
    urls = refs if isinstance(refs, list) else ([refs] if refs else [])
    if not urls:
        raise ValueError(
            "MiniMax H3 multi-image reference requires at least 1 reference image "
            f"(ref_image_0 is mandatory for workflow {workflow}). "
            "Pass reference_image_url (local file → data URI, or http(s) URL), "
            "or switch to a text-to-video provider (e.g. VIDEO_PROVIDER=seedance) for T2VA."
        )
    if len(urls) > MAX_REF_IMAGES:
        import warnings

        warnings.warn(
            f"H3 supports at most {MAX_REF_IMAGES} reference images; "
            f"using the first {MAX_REF_IMAGES} (got {len(urls)})."
        )
    for i, url in enumerate(urls[:MAX_REF_IMAGES]):
        req[f"ref_image_{i}"] = url

    return req


def _resolve_resolution(prompt: VideoPrompt) -> str:
    if prompt.resolution:
        if prompt.resolution not in RESOLUTIONS:
            raise ValueError(
                f"Invalid H3 resolution: {prompt.resolution!r}. Choices: {', '.join(RESOLUTIONS)}"
            )
        return prompt.resolution
    return resolution_from_style(prompt.style)
