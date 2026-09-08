"""请求体层：把 md 提示词装配成"真正会发出去的" API 请求体。

复用 ai.providers 的 parse/build_request（与 CLI 同一套逻辑，零重写）：
- H3（autodl_comfyui）: h3_prompt.parse_prompt_file → build_request
- Seedance（volcengine）: 标准 9 要素解析（兜底整文件文本）→ SeedanceVideo.build_request

输出附：快照时长（provider 截断）、成本估算、可复制的 CLI 命令。
"""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any

from ai.formats import parse_standard_prompt_file
from ai.models import VideoPrompt
from ai.providers.autodl_comfyui import h3_prompt

H3_WORKFLOW_DEFAULT = "minimax_h3_lightx2v_v5"


def detect_format(content: str) -> str:
    """h3 / standard / plain（plain = 整文件当提示词文本）。"""
    if h3_prompt.is_h3_prompt_file(content):
        return "h3"
    if any(f"- **{k}**:" in content for k in ("scene", "subject", "camera", "lighting", "style")):
        return "standard"
    return "plain"


def assemble(
    content: str,
    provider: str,
    duration: int,
    resolution: str,
    refs: list[str] | None,
    project_dir: Path | str,
    file_path: str,
    model: str = "mini",
) -> dict[str, Any]:
    """装配请求体。返回 {format, request|error, duration, cost, command}。"""
    project_dir = Path(project_dir)
    refs = [r for r in (refs or []) if r] or None
    try:
        duration = int(duration)
    except (TypeError, ValueError):
        duration = 5  # model_config default_duration
    if provider == "autodl_comfyui":
        return _assemble_h3(content, duration, resolution, refs, project_dir, file_path)
    return _assemble_seedance(content, duration, refs, project_dir, file_path, model)


def _assemble_h3(
    content: str,
    duration: int,
    resolution: str,
    refs: list[str] | None,
    project_dir: Path,
    file_path: str,
) -> dict[str, Any]:
    fmt = "h3" if h3_prompt.is_h3_prompt_file(content) else "plain-h3"
    vp = h3_prompt.parse_prompt_file(content)
    if vp is None:
        vp = VideoPrompt(scene="", subject="", raw_prompt=content.strip())
    try:
        vp = replace(
            vp, duration_hint=duration, resolution=resolution, reference_image_url=refs or None
        )
        req = h3_prompt.build_request(vp, H3_WORKFLOW_DEFAULT)
    except ValueError as e:
        return {
            "format": fmt,
            "error": str(e),
            "command": _h3_command(file_path, refs, resolution, duration, project_dir),
        }
    return {
        "format": fmt,
        "request": req,
        "duration": req.get("duration"),
        "cost": h3_prompt.estimate_cost(req.get("duration", duration), req.get("resolution", "")),
        "command": _h3_command(file_path, refs, resolution, duration, project_dir),
    }


def _assemble_seedance(
    content: str,
    duration: int,
    refs: list[str] | None,
    project_dir: Path,
    file_path: str,
    model: str,
) -> dict[str, Any]:
    from ai.registry import get_video_generator

    if detect_format(content) == "standard":
        vp = parse_standard_prompt_file(content)
    else:
        vp = VideoPrompt(scene=content.strip(), subject="")
    try:
        vp = replace(vp, duration_hint=duration, reference_image_url=refs or None)
        gen = get_video_generator(model=model, provider="seedance")
        req = gen.build_request(vp)
    except ValueError as e:
        return {
            "format": "seedance",
            "error": str(e),
            "command": _seedance_command(file_path, duration, project_dir),
        }
    dur = duration
    return {
        "format": "seedance",
        "request": req,
        "duration": dur,
        "cost": None,  # Seedance 成本走火山计费，不在此估算
        "command": _seedance_command(file_path, duration, project_dir),
    }


def _h3_command(
    file_path: str, refs: list[str] | None, resolution: str, duration: int, project_dir: Path
) -> str:
    abs_file = (project_dir / file_path).resolve()
    parts = [
        "uv run --directory scripts ai -p autodl_comfyui generate video",
        f"--prompt-file {abs_file}",
    ]
    for r in refs or []:
        parts.append(f'--ref-images "{r}"')
    parts.append(f"--resolution {resolution}")
    parts.append(f"--duration {duration}")
    parts.append(f"-o {project_dir / 'outputs'}")
    return " \\\n  ".join(parts)


def _seedance_command(file_path: str, duration: int, project_dir: Path) -> str:
    abs_file = (project_dir / file_path).resolve()
    return " \\\n  ".join(
        [
            "uv run --directory scripts ai generate video",
            f"--prompt-file {abs_file}",
            f"--duration {duration}",
            f"-o {project_dir / 'outputs'}",
        ]
    )


def assemble_json(
    content: str,
    provider: str,
    duration: int,
    resolution: str,
    refs: list[str] | None,
    project_dir: Path,
    file_path: str,
) -> str:
    """供 API 返回的 JSON 串。"""
    return json.dumps(
        assemble(content, provider, duration, resolution, refs, project_dir, file_path),
        ensure_ascii=False,
        indent=2,
    )
