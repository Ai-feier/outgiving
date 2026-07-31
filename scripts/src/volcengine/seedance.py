"""
Seedance 2.0 — AI 视频生成适配器 (ARK API)。

Volcengine ARK 平台，支持文生视频/图生视频/视频编辑/延长。
Model IDs: doubao-seedance-2-0-260128 / -fast / -mini。
4-15s，最高 4K 10-bit。

Agent 使用路径：
    video-director → video-prompt.md → SeedanceVideo.submit()
"""

from __future__ import annotations

import json
import time
import urllib.request
from typing import Any

from volcengine._auth import Credentials, get_credentials
from volcengine._http import VolcError
from volcengine.models import (
    LEGAL_DURATIONS,
    VideoPrompt,
    VideoResult,
    VideoStatus,
    snap_duration,
)


# ARK API endpoint
ARK_BASE = "https://ark.cn-beijing.volces.com/api/v3"
ARK_TASKS = f"{ARK_BASE}/contents/generations/tasks"

# Available model IDs (must be activated in console first)
MODELS = {
    "pro": "doubao-seedance-2-0-260128",
    "fast": "doubao-seedance-2-0-fast-260128",
    "mini": "doubao-seedance-2-0-mini-260615",
}


class SeedanceVideo:
    """Seedance 2.0 视频生成器 (ARK API)。

    使用方式：
        video = SeedanceVideo()
        result = video.submit(VideoPrompt(
            scene="medium shot",
            subject="a developer typing on keyboard",
            camera="slow tracking shot",
            lighting="golden hour, soft rim light",
            style="cinematic, 24fps",
            duration_hint=5,
            # 可选：多模态参考
            reference_image_url="https://example.com/ref.jpg",
            reference_video_url="https://example.com/ref.mp4",
            reference_audio_url="https://example.com/ref.mp3",
        ))
        final = video.wait(result.task_id)
        print(final.video_url)
    """

    def __init__(self, creds: Credentials | None = None, model: str = "mini"):
        self._creds = creds or get_credentials()
        self._model = MODELS.get(model, model)

    # ── public API ──────────────────────────────────────────

    def submit(self, prompt: VideoPrompt) -> VideoResult:
        """提交视频生成任务。返回 task_id，不阻塞。"""
        body = self._build_request(prompt)
        resp = self._call(body)
        return VideoResult(
            task_id=resp.get("id", ""),
            status=VideoStatus.QUEUED,
        )

    def query(self, task_id: str) -> VideoResult:
        """查询任务状态。"""
        url = f"{ARK_TASKS}/{task_id}"
        req = urllib.request.Request(url, headers=self._headers(), method="GET")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise VolcError(str(e.code), e.read().decode("utf-8", errors="replace")) from e
        return self._parse_response(data, task_id)

    def wait(self, task_id: str, poll_interval: int = 10, timeout: int = 600) -> VideoResult:
        """轮询直到任务完成或超时（视频生成需 1-5 分钟）。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            result = self.query(task_id)
            if result.status in (VideoStatus.COMPLETED, VideoStatus.FAILED):
                return result
            time.sleep(poll_interval)
        return VideoResult(
            task_id=task_id,
            status=VideoStatus.FAILED,
            error_message="Timeout waiting for video generation",
        )

    def submit_with_retry(self, prompt: VideoPrompt, max_retries: int = 3) -> VideoResult:
        """提交并等待，失败自动重试（最多 max_retries 次）。

        31% 首次失败率（Seedance 2.0 ARK 实测），自动重试提升可靠性。
        """
        last_error: str | None = None
        for attempt in range(max_retries):
            result = self.submit(prompt)
            if not result.task_id:
                last_error = result.error_message or "No task_id"
                time.sleep(2 ** attempt)  # exponential backoff
                continue
            final = self.wait(result.task_id)
            if final.status == VideoStatus.COMPLETED:
                return final
            last_error = final.error_message or "Unknown error"
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
        return VideoResult(
            task_id="",
            status=VideoStatus.FAILED,
            error_message=f"All {max_retries} retries failed. Last: {last_error}",
        )

    # ── private ─────────────────────────────────────────────

    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._creds.api_key}",
        }

    def _build_request(self, prompt: VideoPrompt) -> dict[str, Any]:
        """将语义 VideoPrompt 转为 ARK Content Generation API 请求体。

        Seedance 2.0 支持多模态 content 数组：
        - {"type": "text", "text": "..."}
        - {"type": "image_url", "image_url": {"url": "..."}, "role": "reference_image"}
        - {"type": "video_url", "video_url": {"url": "..."}, "role": "reference_video"}
        - {"type": "audio_url", "audio_url": {"url": "..."}, "role": "reference_audio"}

        reference_image: 0-9 张，用于角色/风格/构图锚定
        reference_video: 0-3 个，用于运镜/动作/风格参考
        reference_audio: 0-3 个，用于音色/旋律/对话参考
        """
        natural_text = prompt.to_natural_language()

        content: list[dict[str, Any]] = [
            {"type": "text", "text": natural_text},
        ]

        # 参考图片（0-9 张）
        if prompt.reference_image_url:
            urls = prompt.reference_image_url if isinstance(prompt.reference_image_url, list) else [prompt.reference_image_url]
            for url in urls[:9]:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": url},
                    "role": "reference_image",
                })

        # 参考视频（0-3 个）
        if prompt.reference_video_url:
            urls = prompt.reference_video_url if isinstance(prompt.reference_video_url, list) else [prompt.reference_video_url]
            for url in urls[:3]:
                content.append({
                    "type": "video_url",
                    "video_url": {"url": url},
                    "role": "reference_video",
                })

        # 参考音频（0-3 个）
        if prompt.reference_audio_url:
            urls = prompt.reference_audio_url if isinstance(prompt.reference_audio_url, list) else [prompt.reference_audio_url]
            for url in urls[:3]:
                content.append({
                    "type": "audio_url",
                    "audio_url": {"url": url},
                    "role": "reference_audio",
                })

        # entity_tags → reference image association (Gap 2)
        if prompt.entity_tags and prompt.reference_image_url:
            ref_urls = prompt.reference_image_url if isinstance(prompt.reference_image_url, list) else [prompt.reference_image_url]
            for i, (key, val) in enumerate(prompt.entity_tags.items()):
                if i < len(ref_urls):
                    content.append({
                        "type": "text",
                        "text": f"[{key}] ({val}) maps to Image{i+1}",
                    })
                else:
                    content.append({
                        "type": "text",
                        "text": f"[{key}] is {val}",
                    })

        req: dict[str, Any] = {
            "model": self._model,
            "content": content,
            "duration": snap_duration(prompt.duration_hint),  # Gap 4
        }

        # 画面比例
        if prompt.style:
            req["ratio"] = _ratio_from_style(prompt.style)
        else:
            req["ratio"] = "16:9"

        # 可选参数
        if prompt.negative_prompt:
            req["negative_prompt"] = prompt.negative_prompt

        # ARK API 控制参数 (Gap 5)
        req["generate_audio"] = prompt.generate_audio
        if prompt.seed is not None:
            req["seed"] = prompt.seed
        req["watermark"] = prompt.watermark
        req["return_last_frame"] = prompt.return_last_frame
        req["service_tier"] = prompt.service_tier
        req["priority"] = prompt.priority

        return req

    def _call(self, body: dict[str, Any]) -> dict[str, Any]:
        body_bytes = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            ARK_TASKS, data=body_bytes, headers=self._headers(), method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))  # type: ignore[no-any-return]
        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8", errors="replace")
            try:
                err = json.loads(body_text)
                msg = err.get("error", {}).get("message", body_text)
            except json.JSONDecodeError:
                msg = body_text
            raise VolcError(str(e.code), msg) from e

    def _parse_response(self, data: dict[str, Any], task_id: str) -> VideoResult:
        """解析 ARK API 响应。"""
        status_str = data.get("status", "")

        status_map = {
            "succeeded": VideoStatus.COMPLETED,
            "failed": VideoStatus.FAILED,
            "running": VideoStatus.PROCESSING,
            "pending": VideoStatus.QUEUED,
        }
        status = status_map.get(status_str, VideoStatus.PROCESSING)

        video_url = None
        content = data.get("content", {})
        if isinstance(content, dict):
            video_url = content.get("video_url") or None

        error_msg = None
        err = data.get("error")
        if err and isinstance(err, dict):
            error_msg = err.get("message", "")

        return VideoResult(
            task_id=task_id,
            status=status,
            video_url=video_url,
            error_message=error_msg,
        )


def _ratio_from_style(style: str) -> str:
    """从风格推断画幅比。"""
    style_lower = style.lower()
    if "portrait" in style_lower or "9:16" in style_lower or "竖屏" in style_lower:
        return "9:16"
    if "square" in style_lower or "1:1" in style_lower or "方块" in style_lower:
        return "1:1"
    return "16:9"
