"""
凭证管理（火山引擎）。优先读取环境变量，其次 .env 文件。

环境变量：
    VOLC_AK           — Access Key (OpenAPI 签名用)
    VOLC_SK           — Secret Key (OpenAPI 签名用)
    ARK_API_KEY       — ARK API Key (Seedance 2.0 / Seedream 等 ARK 服务用)
    VOLC_API_KEY      — 旧 API Key (兼容)
    VOICE_API_KEY     — TTS 服务专用 Key (兼容)
"""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Credentials:
    ak: str = ""
    sk: str = ""
    api_key: str | None = None
    ark_api_key: str | None = None
    voice_api_key: str | None = None


def get_credentials() -> Credentials:
    """读取凭证，优先级：环境变量 > .env 文件。"""
    ak = os.getenv("VOLC_AK")
    sk = os.getenv("VOLC_SK")
    api_key = os.getenv("ARK_API_KEY") or os.getenv("VOLC_API_KEY")
    ark_api_key = os.getenv("ARK_API_KEY")
    voice_api_key = os.getenv("VOICE_API_KEY")

    # fallback: 从项目根 .env 读取
    env_file = Path(__file__).resolve().parents[5] / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip('"').strip("'")
            if key == "VOLC_AK" and not ak:
                ak = val
            elif key == "VOLC_SK" and not sk:
                sk = val
            elif key == "ARK_API_KEY" and not ark_api_key:
                ark_api_key = val
                if not api_key:
                    api_key = val
            elif key == "VOICE_API_KEY" and not voice_api_key:
                voice_api_key = val

    if not api_key and (not ak or not sk):
        raise RuntimeError(
            "Missing Volcengine credentials. Set ARK_API_KEY "
            "or VOLC_AK+VOLC_SK environment variables."
        )

    return Credentials(ak=ak or "", sk=sk or "", api_key=api_key, ark_api_key=ark_api_key, voice_api_key=voice_api_key)


def check() -> bool:
    """凭证是否可用（供 registry.check_connectivity 聚合）。不抛异常。"""
    try:
        return bool(get_credentials().api_key)
    except Exception:
        return False
