"""
Web Fetcher — 浏览器指纹伪装的 HTTP 下载工具。

基于 curl_cffi 实现 TLS 指纹模仿，绕过 Cloudflare/Akamai 等 CDN 防护。
支持 Chrome / Safari / Firefox 多版本指纹切换，自动重试，图片下载，页面抓取。

Quickstart:
    from web_fetcher import download_image, fetch_page

    # 下载参考图
    path = download_image("https://example.com/image.jpg", "assets/ref.jpg")
    print(path)

    # 抓取 HTML 页面
    html = fetch_page("https://example.com", fingerprint="safari17_0")
    print(html[:200])
"""

from __future__ import annotations

import logging
import mimetypes
import os
import time
from pathlib import Path
from typing import Any

from curl_cffi.requests import BrowserType, Session
from curl_cffi.requests.exceptions import RequestException

logger = logging.getLogger(__name__)

# ── 支持的浏览器指纹 ─────────────────────────────────────────────

FINGERPRINTS: dict[str, BrowserType] = {
    # Chrome
    "chrome124": BrowserType.chrome124,
    "chrome131": BrowserType.chrome131,
    "chrome133": BrowserType.chrome133a,
    "chrome136": BrowserType.chrome136,
    "chrome142": BrowserType.chrome142,
    "chrome145": BrowserType.chrome145,
    "chrome146": BrowserType.chrome146,
    # Safari
    "safari17_0": BrowserType.safari17_0,
    "safari17_2_ios": BrowserType.safari17_2_ios,
    "safari18_0": BrowserType.safari18_0,
    "safari18_0_ios": BrowserType.safari18_0_ios,
    "safari260": BrowserType.safari260,
    # Firefox
    "firefox133": BrowserType.firefox133,
    "firefox135": BrowserType.firefox135,
    "firefox144": BrowserType.firefox144,
    "firefox147": BrowserType.firefox147,
    # Edge
    "edge101": BrowserType.edge101,
    # Tor
    "tor145": BrowserType.tor145,
}

DEFAULT_FINGERPRINT = "chrome131"
"""默认指纹。Chrome 131 兼容性最广。"""

VALID_IMAGE_TYPES = frozenset({
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/avif",
    "image/svg+xml",
    "image/bmp",
    "image/tiff",
})
"""认可的图片 MIME 类型。"""


# ── 异常 ────────────────────────────────────────────────────────


class WebFetchError(Exception):
    """下载失败。"""

    def __init__(self, message: str, url: str, status_code: int | None = None):
        self.url = url
        self.status_code = status_code
        super().__init__(f"[{status_code}] {message}" if status_code else message)


class UnsupportedContentType(WebFetchError):
    """服务器返回的 Content-Type 不是预期类型。"""

    def __init__(self, url: str, content_type: str, expected: str):
        self.content_type = content_type
        self.expected = expected
        super().__init__(
            f"Unexpected Content-Type: {content_type} (expected {expected})",
            url,
        )


# ── 核心下载器 ───────────────────────────────────────────────────


class WebFetcher:
    """带浏览器指纹伪装的 HTTP 下载器。

    参数:
        fingerprint: 浏览器指纹名（见 FINGERPRINTS 字典）。
        timeout: 请求超时秒数。
        max_retries: 失败后最多重试次数。
        retry_delay: 重试基础等待秒数（指数退避）。
        user_agent: 自定义 User-Agent（None 则 curl_cffi 自动选择）。
        follow_redirects: 是否跟随 3xx 重定向。
    """

    def __init__(
        self,
        fingerprint: str = DEFAULT_FINGERPRINT,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        user_agent: str | None = None,
        follow_redirects: bool = True,
    ):
        self._resolve = self._resolve_fingerprint(fingerprint)
        self.fingerprint = fingerprint
        self.fingerprint_value = self._resolve
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.user_agent = user_agent
        self.follow_redirects = follow_redirects

    def _resolve_fingerprint(self, name: str) -> BrowserType:
        """根据名称解析 BrowserType。支持大小写不敏感、下划线变连字符。"""
        # 先精确匹配
        if name in FINGERPRINTS:
            return FINGERPRINTS[name]
        # 大小写不敏感匹配
        name_lower = name.lower()
        for key, value in FINGERPRINTS.items():
            if key.lower() == name_lower:
                return value
        # 尝试把连字符换下划线
        alt_name = name.replace("-", "_").lower()
        for key, value in FINGERPRINTS.items():
            if key.lower() == alt_name:
                return value
        raise ValueError(
            f"Unknown fingerprint: {name!r}. "
            f"Available: {', '.join(sorted(FINGERPRINTS))}"
        )

    def _build_session(self) -> Session:
        """创建 curl_cffi Session，配置浏览器指纹伪装。"""
        s = Session(
            impersonate=self.fingerprint_value,
            timeout=self.timeout,
        )
        s.follow_redirects = self.follow_redirects
        if self.user_agent:
            s.headers.update({"User-Agent": self.user_agent})
        return s

    def _request(
        self,
        method: str,
        url: str,
        stream: bool = False,
        **kwargs: Any,
    ) -> Any:
        """发送请求，自动重试。

        Returns:
            stream=True → 原始 response 对象（调用者负责读取和关闭）
            stream=False → response 对象
        """
        last_exc: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                s = self._build_session()
                resp = s.request(method, url, stream=stream, **kwargs)
                resp.raise_for_status()
                return resp
            except RequestException as e:
                last_exc = e
                status = getattr(e, "status_code", None)
                logger.warning(
                    "Attempt %d/%d failed for %s [%s]: %s",
                    attempt + 1,
                    self.max_retries,
                    url,
                    status,
                    e,
                )
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)
                    time.sleep(delay)
                else:
                    raise WebFetchError(str(e), url, status_code=status) from e
            finally:
                # 每个尝试都用独立的 session，关闭前一个
                if "s" in locals():
                    s.close()

        # 理论上不会到这里，但给类型检查器一个交代
        raise WebFetchError(str(last_exc), url)

    def download_image(self, url: str, output_path: str | os.PathLike) -> Path:
        """下载图片到本地文件。

        验证 Content-Type 是否为图片类型。如果服务器返回非图片
        Content-Type 则抛出 UnsupportedContentType。

        返回:
            输出文件的绝对路径。

        异常:
            WebFetchError: 网络错误或重试耗尽。
            UnsupportedContentType: 返回内容不是图片。
        """
        resp = self._request("GET", url)
        content_type = resp.headers.get("Content-Type", "").split(";")[0].strip().lower()

        # 严格检查图片类型
        # 如果服务器没返回 Content-Type，我们根据扩展名推断并允许下载
        if content_type and content_type not in VALID_IMAGE_TYPES:
            raise UnsupportedContentType(url, content_type, "image/*")

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(resp.content)

        logger.info("Downloaded %s (%s, %.1f KB)", url, content_type or "unknown", len(resp.content) / 1024)
        return out.resolve()

    def fetch_page(self, url: str, encoding: str = "utf-8") -> str:
        """抓取 HTML 页面文本内容。

        参数:
            url: 目标 URL。
            encoding: 页面编码（默认 utf-8）。

        返回:
            页面文本内容。
        """
        resp = self._request("GET", url)
        resp.encoding = encoding
        text = resp.text
        logger.info("Fetched %s (%.1f KB, status=%d)", url, len(text) / 1024, resp.status_code)
        return text

    def fetch_json(self, url: str) -> Any:
        """抓取 JSON API 响应。

        返回:
            Python 对象（dict / list）。
        """
        resp = self._request("GET", url)
        data = resp.json()
        logger.info("Fetched JSON %s (status=%d)", url, resp.status_code)
        return data

    def head(self, url: str) -> dict[str, str]:
        """发送 HEAD 请求检查资源可访问性。

        返回:
            响应头字典。
        """
        resp = self._request("HEAD", url)
        logger.info("HEAD %s → %d", url, resp.status_code)
        return dict(resp.headers)


# ── 便利函数（无需创建 WebFetcher 实例） ─────────────────────────


def download_image(
    url: str,
    output_path: str | os.PathLike,
    fingerprint: str = DEFAULT_FINGERPRINT,
    timeout: float = 30.0,
    max_retries: int = 3,
) -> Path:
    """下载图片的便利函数。

    用法:
        >>> from web_fetcher import download_image
        >>> path = download_image("https://...", "ref.jpg", fingerprint="safari18_0")
    """
    f = WebFetcher(fingerprint=fingerprint, timeout=timeout, max_retries=max_retries)
    return f.download_image(url, output_path)


def fetch_page(
    url: str,
    fingerprint: str = DEFAULT_FINGERPRINT,
    timeout: float = 30.0,
    max_retries: int = 3,
) -> str:
    """抓取 HTML 页面的便利函数。"""
    f = WebFetcher(fingerprint=fingerprint, timeout=timeout, max_retries=max_retries)
    return f.fetch_page(url)


def fetch_json(
    url: str,
    fingerprint: str = DEFAULT_FINGERPRINT,
    timeout: float = 30.0,
    max_retries: int = 3,
) -> Any:
    """抓取 JSON 的便利函数。"""
    f = WebFetcher(fingerprint=fingerprint, timeout=timeout, max_retries=max_retries)
    return f.fetch_json(url)


__all__ = [
    # 常量
    "FINGERPRINTS",
    "DEFAULT_FINGERPRINT",
    "VALID_IMAGE_TYPES",
    # 异常
    "WebFetchError",
    "UnsupportedContentType",
    # 类
    "WebFetcher",
    # 便利函数
    "download_image",
    "fetch_page",
    "fetch_json",
]
