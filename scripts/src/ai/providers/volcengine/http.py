"""
HTTP 客户端。统一的请求签名、重试、错误处理。
"""

import hashlib
import hmac
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

from .auth import Credentials


class VolcError(Exception):
    """API 调用错误。"""

    def __init__(self, code: str, message: str, request_id: str = ""):
        self.code = code
        self.message = message
        self.request_id = request_id
        super().__init__(f"[{code}] {message}" + (f" (request_id={request_id})" if request_id else ""))


def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sign_request(
    creds: Credentials,
    method: str,
    host: str,
    path: str,
    query: str,
    body: bytes,
    region: str,
    service: str,
) -> dict[str, str]:
    """Volcengine Signature V4 签名。与官方 SDK signv4.py 对齐。"""
    now = datetime.now(timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")

    canonical_uri = path or "/"
    payload_hash = _sha256_hex(body)

    # 只签名 Content-Type, Content-Md5, Host, X-* 头（与官方 SDK 一致）
    all_headers = {
        "Content-Type": "application/json",
        "Host": host,
        "X-Content-Sha256": payload_hash,
        "X-Date": amz_date,
    }

    signed_headers: dict[str, str] = {}
    for k, v in all_headers.items():
        if k in ("Content-Type", "Content-Md5", "Host") or k.startswith("X-"):
            signed_headers[k.lower()] = v

    # 去掉 Host 的默认端口
    if "host" in signed_headers:
        v = signed_headers["host"]
        if ":" in v:
            port = v.split(":")[1]
            if port in ("80", "443"):
                signed_headers["host"] = v.split(":")[0]

    # 构建 canonical headers 字符串
    signed_str = ""
    for key in sorted(signed_headers.keys()):
        signed_str += f"{key}:{signed_headers[key]}\n"
    signed_headers_string = ";".join(sorted(signed_headers.keys()))

    # URL-encode query parameters
    from urllib.parse import quote
    if query:
        params: dict[str, str] = {}
        for pair in query.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                params[k] = v
        canonical_qs_parts: list[str] = []
        for k in sorted(params.keys()):
            canonical_qs_parts.append(f"{quote(k, safe='-_.~')}={quote(params[k], safe='-_.~')}")
        canonical_querystring = "&".join(canonical_qs_parts)
    else:
        canonical_querystring = ""

    canonical_request = (
        f"{method}\n{canonical_uri}\n{canonical_querystring}\n"
        f"{signed_str}\n{signed_headers_string}\n{payload_hash}"
    )

    credential_scope = f"{date_stamp}/{region}/{service}/request"
    string_to_sign = (
        f"HMAC-SHA256\n{amz_date}\n{credential_scope}\n"
        f"{_sha256_hex(canonical_request.encode('utf-8'))}"
    )

    # 密钥派生：直接用 SK，不加 "AWS4" 前缀（与官方 SDK 一致）
    k_date = _sign(creds.sk.encode("utf-8"), date_stamp)
    k_region = _sign(k_date, region)
    k_service = _sign(k_region, service)
    k_signing = _sign(k_service, "request")

    signature = hmac.new(k_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    authorization = (
        f"HMAC-SHA256 Credential={creds.ak}/{credential_scope}, "
        f"SignedHeaders={signed_headers_string}, Signature={signature}"
    )

    return {
        "Authorization": authorization,
        "X-Content-Sha256": payload_hash,
        "X-Date": amz_date,
        "Content-Type": "application/json",
    }


def request(
    creds: Credentials,
    method: str,
    host: str,
    path: str,
    body: dict[str, Any] | None = None,
    query: str = "",
    region: str = "cn-north-1",
    service: str = "iam",
    max_retries: int = 3,
) -> dict[str, Any]:
    """发送带签名的请求，自动重试。"""
    body_bytes = json.dumps(body or {}).encode("utf-8")
    headers = sign_request(creds, method, host, path, query, body_bytes, region, service)

    url = f"https://{host}{path}"
    if query:
        url += f"?{query}"

    last_error = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data  # type: ignore[no-any-return]
        except urllib.error.HTTPError as e:
            last_error = e
            body_text = e.read().decode("utf-8", errors="replace")
            try:
                err_data = json.loads(body_text)
                msg = err_data.get("ResponseMetadata", {}).get("Error", {}).get("Message", body_text)
            except json.JSONDecodeError:
                msg = body_text
            if attempt < max_retries - 1:
                time.sleep(2**attempt)
            else:
                raise VolcError(str(e.code), msg) from e
        except (urllib.error.URLError, OSError) as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(2**attempt)

    raise VolcError("NETWORK", str(last_error))
