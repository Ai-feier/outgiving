"""
MiniMax v2 原生视频生成 REST 客户端（autodl.art）。

端点：
- 提交：POST /api/v1/minimax/v2/video_generation
- 查询：GET  {query_path}/{task_id} —— **路径待实测**。autodl 文档未给出，
  默认按自家 URL 风格猜测，可用 env AUTODL_MINIMAX_QUERY_PATH 覆盖。
  （aiping 网关同款 API 的查询为 /api/v1/multimodal/minimax/videos/query/video_generation/{task_id}）

请求 schema（已核实，aiping 网关 + MiniMax 官方 v2 文档两处一致）：
    {"model": "MiniMax-H3",
     "content": [text / image_url / video_url / audio_url 多模态数组],
     "resolution": "768P"|"2K",
     "duration": 4-15,
     "ratio": "adaptive"|"21:9"|"16:9"|"4:3"|"1:1"|"3:4"|"9:16",
     "aigc_watermark": false}
约束：content 至少含一个非空 text；reference_* role 与 first_frame/last_frame 互斥。

价格（autodl，会员9折）：768P ¥0.45-0.50/s，2K ¥0.72-0.80/s；
图片输入 5 张内免费、超出 ¥0.18-0.20/张；视频输入按时长计费；音频免费。
"""

from __future__ import annotations

import os
import time
from typing import Any, cast

from ai.json_types import MiniMaxEnvelope, MiniMaxFileItem
from ai.models import VideoResult, VideoStatus
from ai.providers import autodl
from ai.providers.autodl import AutoDLError

SUBMIT_PATH = "/api/v1/minimax/v2/video_generation"
# 待实测：autodl 的 minimax 任务查询路径（env 可覆盖）
DEFAULT_QUERY_PATH = "/api/v1/minimax/v2/video_generation/query"


def query_path() -> str:
    """查询端点（env AUTODL_MINIMAX_QUERY_PATH 覆盖默认猜测）。"""
    return os.getenv("AUTODL_MINIMAX_QUERY_PATH") or DEFAULT_QUERY_PATH


def submit_generation(body: dict[str, Any]) -> str:
    """提交生成任务，返回 task_id。"""
    resp = cast("MiniMaxEnvelope", autodl.post(SUBMIT_PATH, body))
    data = resp.get("data")
    task_id = str(data.get("task_id") or "") if data else ""
    if not task_id:
        # 兼容平铺响应 {task_id: ...}
        task_id = str(resp.get("task_id") or "")
    if not task_id:
        raise AutoDLError(
            "EMPTY_TASK",
            str(resp.get("msg") or f"Submit returned no task_id: {str(resp)[:300]}"),
            str(resp.get("request_id") or ""),
        )
    return task_id


def query_result(task_id: str) -> VideoResult:
    """查询任务状态。404 / 空 data → 按 QUEUED 继续轮询。"""
    try:
        data = autodl.get(f"{query_path()}/{task_id}")
    except AutoDLError as e:
        if e.code == "404":
            return VideoResult(task_id=task_id, status=VideoStatus.QUEUED)
        raise
    return parse_response(cast("MiniMaxEnvelope", data), task_id)


def parse_response(data: MiniMaxEnvelope, task_id: str) -> VideoResult:
    """解析查询响应为语义 VideoResult。

    兼容两种响应形态（待实测后收敛）：
    - comfyui 风格包装：{msg, code, data: {status, results[], task_id}}
    - minimax 官方风格：{status, data: {file_url|files[]}, task_id}
    """
    payload = data.get("data")
    status_str = ""
    results: list[MiniMaxFileItem] | None = None
    returned_id = task_id

    if payload:
        status_str = str(payload.get("status") or "").lower()
        res = payload.get("results") or payload.get("files")
        results = res if isinstance(res, list) else None
        returned_id = str(payload.get("task_id") or task_id)
    else:
        status_str = str(payload or "").lower()
    if not status_str:
        status_str = str(data.get("status") or "").lower()
        res2 = data.get("results")
        results = res2 if isinstance(res2, list) else None

    code = str(data.get("code") or "").lower()
    msg = str(data.get("msg") or data.get("message") or "")

    if code and code != "success":
        return VideoResult(
            task_id=returned_id,
            status=VideoStatus.FAILED,
            error_message=msg or f"Gateway error: code={code}",
        )

    if status_str in ("completed", "success", "succeeded"):
        video_url: str | None = None
        if payload:
            # minimax 官方风格：URL 直接挂在 data.file_url / download_url / url
            for key in ("file_url", "download_url", "url", "video_url"):
                raw = payload.get(key)
                if isinstance(raw, str):
                    video_url = raw
                    break
        if video_url is None and results:
            for r in results:
                raw = r.get("url") or r.get("download_url") or r.get("file_url")
                if isinstance(raw, str):
                    video_url = raw
                    break
        return VideoResult(
            task_id=returned_id, status=VideoStatus.COMPLETED, video_url=video_url
        )
    if status_str in ("failed", "error", "failure"):
        return VideoResult(
            task_id=returned_id,
            status=VideoStatus.FAILED,
            error_message=msg or "MiniMax video generation failed",
        )
    if status_str in ("queued", "pending"):
        return VideoResult(task_id=returned_id, status=VideoStatus.QUEUED)
    # running/processing/未知 → 继续轮询
    return VideoResult(task_id=returned_id, status=VideoStatus.PROCESSING)


def wait_for(
    task_id: str, poll_interval: int = 5, timeout: int = 600
) -> VideoResult:
    """轮询直到完成或超时。"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = query_result(task_id)
        if result.status in (VideoStatus.COMPLETED, VideoStatus.FAILED):
            return result
        time.sleep(poll_interval)
    return VideoResult(
        task_id=task_id,
        status=VideoStatus.FAILED,
        error_message="Timeout waiting for MiniMax video generation",
    )
