"""
Volcengine GenBGM — AI 音乐/背景音乐生成适配器。

支持风格+乐器+情绪的结构化 prompt，输出音频 URL。

Agent 使用路径：
    rhythm-designer 节奏曲线 → MusicPrompt → VolcengineBGM → BGM 音轨
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

from .auth import Credentials, get_credentials
from .http import VolcError
from ai.models import MusicPrompt, MusicResult


class VolcengineBGM:
    """火山引擎 GenBGM 服务。

    使用方式：
        bgm = VolcengineBGM()
        result = bgm.generate(MusicPrompt(
            genres=["Atmospheric", "Electronic"],
            bpm=95,
            mood="专注而冷静，有轻微紧张感",
            duration_hint=50,
        ))
        print(result.audio_url)
    """

    def __init__(self, creds: Credentials | None = None):
        self._creds = creds or get_credentials()
        self._host = "open.volcengineapi.com"
        self._service = "ace"

    # ── public API ──────────────────────────────────────────

    def generate(self, prompt: MusicPrompt) -> MusicResult:
        """提交音乐生成任务（同步等待简单生成）。"""
        body = self._build_request(prompt)
        resp = self._call("POST", "/", body, action="GenBGM")

        result_data = resp.get("ResponseMetadata", {}).get("Result", resp.get("data", {}))
        return MusicResult(
            task_id=result_data.get("TaskId", result_data.get("task_id", "")),
            audio_url=result_data.get("audio_url", result_data.get("AudioUrl", "")),
        )

    def generate_async(self, prompt: MusicPrompt) -> str:
        """异步提交，返回 task_id。"""
        body = self._build_request(prompt)
        body["async_mode"] = True
        resp = self._call("POST", "/", body, action="GenBGMAsyncSubmit")
        result_data = resp.get("ResponseMetadata", {}).get("Result", resp.get("data", {}))
        return result_data.get("TaskId", result_data.get("task_id", ""))

    def query(self, task_id: str) -> MusicResult:
        """查询异步任务。"""
        body = {"task_id": task_id}
        resp = self._call("POST", "/", body, action="GenBGMAsyncGetResult")
        result_data = resp.get("ResponseMetadata", {}).get("Result", resp.get("data", {}))
        return MusicResult(
            task_id=task_id,
            audio_url=result_data.get("audio_url", result_data.get("AudioUrl", "")),
        )

    def wait(self, task_id: str, poll_interval: int = 3, timeout: int = 300) -> MusicResult:
        deadline = time.time() + timeout
        while time.time() < deadline:
            result = self.query(task_id)
            if result.audio_url:
                return result
            time.sleep(poll_interval)
        return MusicResult(task_id=task_id)

    # ── private ─────────────────────────────────────────────

    def _build_request(self, prompt: MusicPrompt) -> dict[str, Any]:
        """将语义 MusicPrompt 转为 GenBGM API 请求体。

        对齐 music-prompt skill 的核心公式：
        风格堆叠 + 乐器质感 + 人声特性 + 结构标签 + 物象场景
        """
        req: dict[str, Any] = {
            "genres": prompt.genres,
            "instruments": prompt.instruments,
            "duration": prompt.duration_hint,
        }

        if prompt.vocal_style:
            req["vocal_style"] = prompt.vocal_style
        if prompt.bpm:
            req["bpm"] = prompt.bpm
        if prompt.mood:
            req["mood"] = prompt.mood
        if prompt.structure_tags:
            req["structure"] = prompt.structure_tags

        return req

    def _call(
        self,
        method: str,
        path: str,
        body: dict[str, Any],
        action: str = "",
    ) -> dict[str, Any]:
        from .http import sign_request

        full_body = {
            "Action": action,
            "Version": "2022-08-01",
            **body,
        }
        body_bytes = json.dumps(full_body).encode("utf-8")
        headers = sign_request(
            self._creds,
            method,
            self._host,
            path,
            "",
            body_bytes,
            "cn-north-1",
            self._service,
        )

        url = f"https://{self._host}{path}"
        req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))  # type: ignore[no-any-return]
        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8", errors="replace")
            try:
                err_data = json.loads(body_text)
                msg = (
                    err_data.get("ResponseMetadata", {})
                    .get("Error", {})
                    .get("Message", body_text)
                )
            except json.JSONDecodeError:
                msg = body_text
            raise VolcError(str(e.code), msg) from e
