"""
ComfyUI workflow REST 客户端（autodl.art）。

端点：
- 提交：POST /api/v1/comfyui/comfyui_workflow/{workflow_id}
- 查询：GET  /api/v1/comfyui/comfyui_workflow/result/{task_id}

响应结构（网关统一包装）：{msg, code, data: {status, results[], task_id, client_id}, request_id}
状态值兼容双拼写：文档 QUEUED/RUNNING/SUCCESS/FAILED 与实测样例 completed。
"""

from __future__ import annotations

import time
from typing import Any, cast

from ai.json_types import ComfyUIEnvelope
from ai.models import VideoResult, VideoStatus
from ai.providers import autodl
from ai.providers.autodl import AutoDLError

SUBMIT_PATH = "/api/v1/comfyui/comfyui_workflow"
RESULT_PATH = "/api/v1/comfyui/comfyui_workflow/result"


def submit_workflow(workflow_id: str, body: dict[str, Any]) -> str:
    """提交 workflow，返回 task_id。失败抛 AutoDLError。"""
    resp = cast("ComfyUIEnvelope", autodl.post(f"{SUBMIT_PATH}/{workflow_id}", body))
    data = resp.get("data")
    task_id = str(data.get("task_id") or "") if data else ""
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
        data = autodl.get(f"{RESULT_PATH}/{task_id}")
    except AutoDLError as e:
        if e.code == "404":
            return VideoResult(task_id=task_id, status=VideoStatus.QUEUED)
        raise
    return parse_response(cast("ComfyUIEnvelope", data), task_id)


def parse_response(data: ComfyUIEnvelope, task_id: str) -> VideoResult:
    """解析网关响应为语义 VideoResult。"""
    code = str(data.get("code") or "").lower()
    msg = str(data.get("msg") or "")
    payload = data.get("data")
    if payload:
        status_str = str(payload.get("status") or "").lower()
        results = payload.get("results")
        returned_id = str(payload.get("task_id") or task_id)
    else:
        status_str = str(payload or "").lower()
        results = None
        returned_id = task_id

    if code and code != "success":
        return VideoResult(
            task_id=returned_id,
            status=VideoStatus.FAILED,
            error_message=msg or f"Gateway error: code={code}",
        )

    if status_str in ("completed", "success", "succeeded"):
        video_url: str | None = None
        if results:
            for r in results:
                if r.get("type") == "video":
                    raw_url = r.get("url")
                    video_url = raw_url if isinstance(raw_url, str) else None
                    break
        return VideoResult(
            task_id=returned_id, status=VideoStatus.COMPLETED, video_url=video_url
        )
    if status_str in ("failed", "error", "failure"):
        return VideoResult(
            task_id=returned_id,
            status=VideoStatus.FAILED,
            error_message=msg or "H3 generation failed",
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
        error_message="Timeout waiting for ComfyUI workflow result",
    )
