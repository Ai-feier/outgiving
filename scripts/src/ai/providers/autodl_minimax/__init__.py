"""
AutoDL MiniMax 原生 v2 视频生成适配器。

provider 名：autodl_minimax（VIDEO_PROVIDER=autodl_minimax 切换）。
模型：MiniMax-H3（env AUTODL_MINIMAX_MODEL 可覆盖）。
端点：POST /api/v1/minimax/v2/video_generation（多模态 content 数组）。
凭证：AUTODL_API_KEY（与 autodl_comfyui 共用）。

价格（元/秒，autodl；会员 9 折）：768P ¥0.45-0.50，2K ¥0.72-0.80。
输入素材：图片 5 张内免费、超出 ¥0.18-0.20/张；视频按输入时长计费（与输出分辨率同价）；音频免费。
时长：4-15s（官方 schema 硬限）；分辨率：768P / 2K。
注意：reference_* 参考素材与首尾帧互斥（本适配器当前走参考素材路径）。

⚠️ 查询端点路径待实测（env AUTODL_MINIMAX_QUERY_PATH 可覆盖，见 gateway.py）。
"""

from __future__ import annotations

import os
from typing import Any

from ai.models import VideoPrompt, VideoResult, VideoStatus
from ai.providers.autodl import get_api_key
from . import gateway

DEFAULT_MODEL = "MiniMax-H3"

# 时长（官方 schema）：4-15s
MIN_DURATION = 4
MAX_DURATION = 15

# 价格：元/秒（regular；member 打 9 折）
COST_PER_SECOND = {"768P": 0.50, "2K": 0.80}
COST_PER_SECOND_MEMBER = {"768P": 0.45, "2K": 0.72}
# 超出免费额度的图片：元/张（regular；member 9 折）
IMAGE_OVERAGE_COST = 0.20
IMAGE_FREE_COUNT = 5


def snap_duration(hint: int) -> int:
    """MiniMax v2 合法时长：整数 4-15s（越界截断）。"""
    if hint < MIN_DURATION:
        return MIN_DURATION
    if hint > MAX_DURATION:
        return MAX_DURATION
    return hint


def resolution_from_style(style: str) -> str:
    """从 style 推断分辨率（768P/2K）；无法推断默认 768P。"""
    s = style.lower()
    if "2k" in s or "4k" in s or "1080" in s:
        return "2K"
    return "768P"


def ratio_from_style(style: str) -> str:
    """从 style 推断画幅比；无法推断返回 ""（API 用 adaptive）。"""
    s = style.lower()
    if "portrait" in s or "9:16" in s or "竖" in s:
        return "9:16"
    if "square" in s or "1:1" in s or "方块" in s:
        return "1:1"
    if "landscape" in s or "16:9" in s or "横" in s:
        return "16:9"
    return ""


def estimate_cost(duration: int, resolution: str, member: bool = False) -> float:
    """估算生成成本（元）。member=True 按会员 9 折价。"""
    tier = resolution.upper() if "2K" in resolution.upper() else "768P"
    table = COST_PER_SECOND_MEMBER if member else COST_PER_SECOND
    return duration * table[tier]


class AutoDLMiniMaxVideo:
    """AutoDL MiniMax v2 原生视频生成器。

    实现 VideoGenerator 契约（submit/query/wait/submit_with_retry）。
    额外提供 build_request / estimate_cost，供 CLI --dry-run 与成本显示。
    """

    def __init__(self, creds: Any | None = None, model: str = "MiniMax-H3"):
        # creds 参数保留接口对称性；实际凭证从 AUTODL_API_KEY 读
        self._token = get_api_key()
        self._model = os.getenv("AUTODL_MINIMAX_MODEL") or DEFAULT_MODEL

    @property
    def model_name(self) -> str:
        return self._model

    # ── VideoGenerator 契约 ───────────────────────────────

    def submit(self, prompt: VideoPrompt) -> VideoResult:
        """提交生成任务，返回 task_id，不阻塞。"""
        body = self.build_request(prompt)
        task_id = gateway.submit_generation(body)
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
            try:
                result = self.submit(prompt)
            except ValueError:
                raise
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
        """语义 VideoPrompt → MiniMax v2 请求体（多模态 content 数组）。

        content 结构（已核实）：
            text / image_url(role=reference_image) / video_url(role=reference_video)
            / audio_url(role=reference_audio)
        reference_* 与 first_frame/last_frame 互斥——本适配器当前走参考素材路径。
        """
        text = prompt.raw_prompt or prompt.to_natural_language()
        content: list[dict[str, Any]] = [{"type": "text", "text": text}]

        refs = prompt.reference_image_url
        urls = refs if isinstance(refs, list) else ([refs] if refs else [])
        for url in urls[:9]:
            content.append(
                {"type": "image_url", "image_url": {"url": url}, "role": "reference_image"}
            )

        vrefs = prompt.reference_video_url
        vurls = vrefs if isinstance(vrefs, list) else ([vrefs] if vrefs else [])
        for url in vurls[:3]:
            content.append(
                {"type": "video_url", "video_url": {"url": url}, "role": "reference_video"}
            )

        arefs = prompt.reference_audio_url
        aurls = arefs if isinstance(arefs, list) else ([arefs] if arefs else [])
        for url in aurls[:3]:
            content.append(
                {"type": "audio_url", "audio_url": {"url": url}, "role": "reference_audio"}
            )

        req: dict[str, Any] = {
            "model": self._model,
            "content": content,
            "resolution": self._resolve_resolution(prompt),
            "duration": snap_duration(prompt.duration_hint),
        }
        ratio = ratio_from_style(prompt.style)
        if ratio:
            req["ratio"] = ratio
        req["aigc_watermark"] = False
        return req

    def estimate_cost(self, duration: int, resolution: str, member: bool = False) -> float:
        """估算生成成本（元）。"""
        return estimate_cost(duration, resolution, member=member)

    # ── private ───────────────────────────────────────────

    def _resolve_resolution(self, prompt: VideoPrompt) -> str:
        if prompt.resolution:
            upper = prompt.resolution.upper()
            if upper in ("768P", "2K"):
                return upper
            # 兼容 comfyui 风格档位（480p竖/768p横/1080p(1:1)…）：取 P 前数字
            import re

            m = re.search(r"(\d+)\s*P", upper)
            if m:
                return "2K" if len(m.group(1)) >= 4 else "768P"
            raise ValueError(
                f"Invalid MiniMax resolution: {prompt.resolution!r}. Choices: 768P / 2K"
            )
        return resolution_from_style(prompt.style)
