"""JSON 响应信封（TypedDict）——让 gateway 解析有类型纪律，消灭 cast 喷溅。

每个网关的 API 响应形状用 TypedDict 描述（total=False 容忍未知/缺失字段），
在 API 边界 cast 一次（json.loads → 信封类型），解析代码内全程类型安全。
"""

from __future__ import annotations

from typing import TypedDict

# ── autodl ComfyUI workflow 网关 ──────────────────────────────


class ComfyUIResultItem(TypedDict, total=False):
    url: str
    type: str
    file_type: str
    output_type: str


class ComfyUIData(TypedDict, total=False):
    status: str
    results: list[ComfyUIResultItem]
    task_id: str
    client_id: str


class ComfyUIEnvelope(TypedDict, total=False):
    msg: str
    code: str
    data: ComfyUIData
    request_id: str


# ── autodl MiniMax v2 原生网关 ────────────────────────────────
# 兼容两种响应形态：comfyui 风格包装（msg/code/data）与 minimax 官方风格（status/data）

class MiniMaxFileItem(TypedDict, total=False):
    url: str
    download_url: str
    file_url: str
    type: str  # 兼容 comfyui 风格 items（type: video）


class MiniMaxData(TypedDict, total=False):
    status: str
    results: list[MiniMaxFileItem]
    files: list[MiniMaxFileItem]
    task_id: str
    file_url: str
    url: str
    download_url: str


class MiniMaxEnvelope(TypedDict, total=False):
    msg: str
    code: str
    message: str
    status: str
    task_id: str
    results: list[MiniMaxFileItem]
    data: MiniMaxData
    request_id: str


# ── Volcengine ARK API ────────────────────────────────────────


class ArkError(TypedDict, total=False):
    message: str


class ArkContent(TypedDict, total=False):
    video_url: str


class ArkEnvelope(TypedDict, total=False):
    id: str
    status: str
    content: ArkContent
    error: ArkError
