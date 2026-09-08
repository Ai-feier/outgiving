"""
AutoDL (autodl.art) 公共模块——autodl_comfyui 与 autodl_minimax 两个 provider 共用。

职责：
- AUTODL_API_KEY 凭证读取（令牌在 autodl.art/large-model/tokens 创建，选 ComfyUI 组）
- AutoDLError 错误类型（与 volcengine 的 VolcError 平行，各自 provider 自己家）
- urllib HTTP 助手（Authorization 头直放 token——autodl 网关无 Bearer 前缀）
- 凭证就绪检查 check()（供 registry.check_connectivity 聚合）
"""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
from typing import Any
from urllib.error import HTTPError

AUTODL_BASE = "https://www.autodl.art"


class AutoDLError(Exception):
    """AutoDL API 调用错误。"""

    def __init__(self, code: str, message: str, request_id: str = ""):
        self.code = code
        self.message = message
        self.request_id = request_id
        super().__init__(
            f"[{code}] {message}" + (f" (request_id={request_id})" if request_id else "")
        )


def get_api_key() -> str:
    """读取 AUTODL_API_KEY（环境变量 > .env）。无凭证抛 RuntimeError。"""
    key = os.getenv("AUTODL_API_KEY")
    if not key:
        # 本文件位于 scripts/src/ai/providers/ → 项目根为 parents[4]（outgiving/）
        env_file = Path(__file__).resolve().parents[4] / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                if k.strip() == "AUTODL_API_KEY":
                    key = v.strip().strip('"').strip("'")
                    break
    if not key:
        raise RuntimeError(
            "Missing AutoDL API token. Set AUTODL_API_KEY "
            "(create at autodl.art/large-model/tokens, select ComfyUI group)."
        )
    return key


def check() -> bool:
    """凭证是否可用（不抛异常）。"""
    try:
        return bool(get_api_key())
    except Exception:
        return False


def headers() -> dict[str, str]:
    """认证头。autodl 网关：token 直放 Authorization，无 Bearer 前缀。"""
    return {
        "Content-Type": "application/json",
        "Authorization": get_api_key(),
    }


def _error_details(body_text: str) -> tuple[str, str]:
    """从错误响应体提取 (message, request_id)。非 JSON 时整体作 message。"""
    try:
        err = json.loads(body_text)
    except json.JSONDecodeError:
        return body_text, ""
    msg = err.get("msg")
    if not msg:
        msg = err.get("message")
    if not msg:
        msg = body_text
    rid = err.get("request_id")
    return msg, str(rid) if rid else ""


def post(path: str, body: dict[str, Any], timeout: int = 60) -> dict[str, Any]:
    """POST JSON，返回解析后的响应 dict。"""
    body_bytes = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{AUTODL_BASE}{path}", data=body_bytes, headers=headers(), method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))  # type: ignore[no-any-return]
    except HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        msg, request_id = _error_details(body_text)
        raise AutoDLError(str(e.code), msg, request_id) from e


def get(path: str, timeout: int = 30) -> dict[str, Any]:
    """GET JSON。"""
    req = urllib.request.Request(f"{AUTODL_BASE}{path}", headers=headers(), method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))  # type: ignore[no-any-return]
    except HTTPError as e:
        raise AutoDLError(str(e.code), e.read().decode("utf-8", errors="replace")) from e
