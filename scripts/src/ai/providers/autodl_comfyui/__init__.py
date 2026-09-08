"""
AutoDL ComfyUI 视频生成适配器（MiniMax H3 系列 workflow）。

provider 名：autodl_comfyui（-p autodl_comfyui 或 VIDEO_PROVIDER=autodl_comfyui 切换）。
默认工作流：minimax_h3_lightx2v_v5（env AUTODL_COMFYUI_WORKFLOW 可覆盖）。
凭证：AUTODL_API_KEY（autodl.art/large-model/tokens，选 ComfyUI 组）。

价格（元/秒）：480p/768p ¥0.01（全场促销价，2026-08），1080p ¥0.10。
参考图约束：ref_image_0 必填（1-9 张），纯文生视频请用 seedance 等 T2VA。

Agent 使用路径：
    video-director → video-prompt-h3.md（三核心字段） → AutoDLComfyUIVideo.submit()
"""

from __future__ import annotations

import os
from typing import Any

from ai.models import VideoPrompt, VideoResult, VideoStatus
from ai.providers.autodl import get_api_key

from . import gateway, h3_prompt

DEFAULT_WORKFLOW = "minimax_h3_lightx2v_v5"

# --model 别名 → workflow ID
WORKFLOWS = {
    "lightx2v_v5": "minimax_h3_lightx2v_v5",  # 多图参考（默认，≤10s）
    "lightx2v_v5_15s": "minimax_h3_lightx2v_v5_15s",  # 多图参考 15s（≤15s）
}

# 已知但尚未接入的 workflow（音频/首尾帧入参、无参考图装配未验证）。
# 选中时报错并指向待办，而不是默默发错请求体。
RESERVED_WORKFLOWS = {
    "minimax_h3_image_audio_to_video_v2": "多图多音频（音频入参未验证）",
    "minimax_h3_image_audio_to_video_v2_15s": "多图多音频 15s（音频入参未验证）",
    "minimax_h3_image_audio_to_video": "图生音频同步/自动对口型（音频入参未验证）",
    "minimax_h3_lightx2v": "首尾帧（first_frame/last_frame 入参未验证）",
    "minimax_h3_lightx2v_no_pic": "文生视频（无参考图装配未验证）",
}


def _resolve_workflow(model: str, env_workflow: str | None) -> str:
    """model/alias/env → workflow ID，预留项报清晰错误。"""
    if env_workflow:
        return env_workflow
    if model in WORKFLOWS:
        return WORKFLOWS[model]
    if model in ("pro", "fast", "mini"):
        # registry/CLI 默认传 "mini"；H3 无模型档位，落到默认 workflow
        return DEFAULT_WORKFLOW
    if model in RESERVED_WORKFLOWS or model in WORKFLOWS.values():
        reason = RESERVED_WORKFLOWS.get(model, "已注册别名")
        raise ValueError(
            f"workflow {model} 尚未接入（{reason}）。"
            f"可用：{', '.join(WORKFLOWS)}；或先验证 API 入参后再在 RESERVED_WORKFLOWS 解除标注。"
        )
    # 未知 model：兼容旧行为——当作 workflow ID 直传（gateway 会报 404）
    return model


class AutoDLComfyUIVideo:
    """AutoDL ComfyUI workflow 视频生成器（H3 多图参考）。

    实现 VideoGenerator 契约（submit/query/wait/submit_with_retry）。
    额外提供 build_request / estimate_cost，供 CLI --dry-run 与成本显示。
    """

    def __init__(self, creds: Any | None = None, model: str = "lightx2v_v5"):
        # creds 参数保留接口对称性；实际凭证从 AUTODL_API_KEY 读
        self._token = get_api_key()
        self._workflow = _resolve_workflow(model, os.getenv("AUTODL_COMFYUI_WORKFLOW"))

    @property
    def workflow(self) -> str:
        """当前工作流 ID。"""
        return self._workflow

    # ── VideoGenerator 契约 ───────────────────────────────

    def submit(self, prompt: VideoPrompt) -> VideoResult:
        """提交生成任务，返回 task_id，不阻塞。"""
        body = self.build_request(prompt)
        task_id = gateway.submit_workflow(self._workflow, body)
        return VideoResult(task_id=task_id, status=VideoStatus.QUEUED)

    def query(self, task_id: str) -> VideoResult:
        """查询任务状态。"""
        return gateway.query_result(task_id)

    def wait(self, task_id: str, poll_interval: int = 5, timeout: int = 600) -> VideoResult:
        """轮询直到完成或超时。"""
        return gateway.wait_for(task_id, poll_interval=poll_interval, timeout=timeout)

    def submit_with_retry(self, prompt: VideoPrompt, max_retries: int = 3) -> VideoResult:
        """提交并等待，失败自动重试（指数退避）。参数错误不重试。"""
        import time

        last_error: str | None = None
        for attempt in range(max_retries):
            result = self.submit(prompt)
            if not result.task_id:
                last_error = result.error_message or "No task_id"
                time.sleep(2**attempt)
                continue
            final = self.wait(result.task_id)
            if final.status == VideoStatus.COMPLETED:
                return final
            last_error = final.error_message or "Unknown error"
            if attempt < max_retries - 1:
                time.sleep(2**attempt)
        return VideoResult(
            task_id="",
            status=VideoStatus.FAILED,
            error_message=f"All {max_retries} retries failed. Last: {last_error}",
        )

    # ── 额外能力（CLI 用） ─────────────────────────────────

    def build_request(self, prompt: VideoPrompt) -> dict[str, Any]:
        """语义 VideoPrompt → H3 workflow 请求体（CLI --dry-run 预览）。"""
        return h3_prompt.build_request(prompt, self._workflow)

    def estimate_cost(self, duration: int, resolution: str) -> float:
        """估算生成成本（元）。"""
        return h3_prompt.estimate_cost(duration, resolution)

    def parse_prompt_file(self, content: str) -> VideoPrompt | None:
        """解析 video-prompt-h3.md 三核心字段；非 H3 格式返回 None。

        CLI 先调用本方法（hasattr 探测），不识别时走通用标准格式解析。
        """
        return h3_prompt.parse_prompt_file(content)
