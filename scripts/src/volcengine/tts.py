"""
Volcengine TTS — 语音合成适配器 (Seed Audio 1.0)。

新版豆包语音 API：openspeech.bytedance.com，X-Api-Key 鉴权。
支持纯文本/参考音频/参考图片生成，最长 120s 输出。

Agent 使用路径：
    douyin-writer 口播文案 → TTSOptions → VolcengineTTS → 音频文件
"""

from __future__ import annotations

import base64
import json
import uuid
import urllib.request
from pathlib import Path
from typing import Any

from volcengine._auth import Credentials, get_credentials
from volcengine._http import VolcError
from volcengine.models import TTSOptions, TTSResult, AudioFormat


# Seed Audio 1.0 API
TTS_URL = "https://openspeech.bytedance.com/api/v3/tts/create"
TTS_MODEL = "seed-audio-1.0"

# 预置音色 ID（豆包语音合成模型 2.0 音色）
PRESET_SPEAKERS = {
    "zh_female_qingxue": "zh_female_qingxue_moon_bigtts",
    "zh_female_shuangkuisi": "zh_female_shuangkuisi_moon_bigtts",
    "zh_female_tianmei": "zh_female_tianmei_moon_bigtts",
    "zh_male_qingse": "zh_male_qingse_moon_bigtts",
    "zh_male_wennuan": "zh_male_wennuan_moon_bigtts",
}


class VolcengineTTS:
    """豆包语音合成 (Seed Audio 1.0)。

    使用方式：
        tts = VolcengineTTS()
        result = tts.synthesize(TTSOptions(
            text="你好，欢迎收看本期视频。",
            voice="zh_male_wennuan",
        ))
        # result.audio_data 包含 mp3 字节
        tts.synthesize_to_file(options, "output/voice.mp3")
    """

    def __init__(self, api_key: str | None = None):
        creds = get_credentials()
        self._api_key = api_key or creds.voice_api_key or creds.api_key or ""
        if not self._api_key:
            raise RuntimeError("Missing TTS API Key. Set VOICE_API_KEY env var.")

    # ── public API ──────────────────────────────────────────

    def synthesize(self, options: TTSOptions) -> TTSResult:
        """合成语音，返回 TTSResult（含 audio_data bytes）。"""
        body = self._build_request(options)
        resp = self._call(body)

        audio_b64 = resp.get("audio", "")
        audio_data = base64.b64decode(audio_b64) if audio_b64 else None

        return TTSResult(
            audio_data=audio_data,
            duration_ms=int(resp.get("duration", 0) * 1000),
            format=options.format,
            audio_url=resp.get("url"),
        )

    def synthesize_to_file(self, options: TTSOptions, output_path: str | Path) -> TTSResult:
        """合成语音并写入文件。"""
        result = self.synthesize(options)
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if result.audio_data:
            path.write_bytes(result.audio_data)
        elif result.audio_url:
            urllib.request.urlretrieve(result.audio_url, path)
        return result

    # ── private ─────────────────────────────────────────────

    def _build_request(self, options: TTSOptions) -> dict[str, Any]:
        """将语义 TTSOptions 转为 Seed Audio API 请求体。"""
        req: dict[str, Any] = {
            "model": TTS_MODEL,
            "text_prompt": options.text,
            "audio_config": {
                "format": options.format.value,
                "sample_rate": options.sample_rate,
                "speech_rate": int((options.speed - 1.0) * 100),
                "pitch_rate": int(options.pitch),
                "loudness_rate": int((options.volume - 1.0) * 100),
            },
        }

        # 音色：优先使用预置 speaker ID
        speaker = PRESET_SPEAKERS.get(options.voice, options.voice)
        if speaker:
            req["speaker"] = speaker

        return req

    def _call(self, body: dict[str, Any]) -> dict[str, Any]:
        body_bytes = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            TTS_URL,
            data=body_bytes,
            headers={
                "Content-Type": "application/json",
                "X-Api-Key": self._api_key,
                "X-Api-Request-Id": str(uuid.uuid4()),
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8", errors="replace")
            try:
                err = json.loads(body_text)
                msg = err.get("message", body_text)
            except json.JSONDecodeError:
                msg = body_text
            raise VolcError(str(e.code), msg) from e

        code = data.get("code", -1)
        if code != 0:
            raise VolcError(str(code), data.get("message", "Unknown error"))

        return data
