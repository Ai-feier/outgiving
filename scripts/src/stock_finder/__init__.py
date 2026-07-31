"""
Stock footage & image finder — Pexels & Pixabay search and download.

Provider-agnostic design: each source implements the same interface.
No external dependencies beyond stdlib (urllib.request).
Rate limits handled with exponential backoff.

Quickstart:
    from stock_finder import search_videos, search_images, download_video
    results = search_videos("funny cat", count=5, source="pexels")
    download_video(results[0]["url"], "output.mp4")

Environment variables:
    PEXELS_API_KEY   — required for source="pexels"  (api.pexels.com)
    PIXABAY_API_KEY  — required for source="pixabay" (pixabay.com/api)
"""

import os
import json
import time
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

__all__ = [
    "search_videos",
    "search_images",
    "download_video",
    "StockFinderError",
    "RateLimitError",
    "AuthError",
    "PEXELS_BASE",
    "PIXABAY_BASE",
]

PEXELS_BASE = "https://api.pexels.com"
PIXABAY_BASE = "https://pixabay.com/api"

_MAX_RETRIES = 3
_BASE_DELAY = 2  # seconds, doubles each retry


# ── Exceptions ─────────────────────────────────────────────


class StockFinderError(Exception):
    """Base exception for all stock finder operations."""


class RateLimitError(StockFinderError):
    """API rate limit exceeded (HTTP 429)."""


class AuthError(StockFinderError):
    """API key missing, invalid, or rejected."""


# ── Auth helpers ───────────────────────────────────────────


def _pexels_headers():
    """Return Authorization header dict for Pexels API."""
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        raise AuthError(
            "PEXELS_API_KEY not set. "
            "Get a free key at https://www.pexels.com/api/"
        )
    return {"Authorization": key}


def _pixabay_key():
    """Return raw Pixabay API key from environment."""
    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        raise AuthError(
            "PIXABAY_API_KEY not set. "
            "Get a free key at https://pixabay.com/api/"
        )
    return key


# ── Low-level HTTP ─────────────────────────────────────────


def _request(url, headers=None, retries=_MAX_RETRIES):
    """JSON GET with rate-limit retry and exponential backoff.

    Args:
        url: Full URL to fetch.
        headers: Optional dict of HTTP headers.
        retries: Max retry count on 429 or transient errors.

    Returns:
        Parsed JSON dict.

    Raises:
        RateLimitError: After exhausting retries on HTTP 429.
        AuthError: On HTTP 401.
        StockFinderError: On other HTTP or network errors.
    """
    req = urllib.request.Request(url, headers=headers or {})
    last_error = None

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code == 429:
                if attempt < retries - 1:
                    delay = _BASE_DELAY * (2**attempt)
                    time.sleep(delay)
                    continue
                raise RateLimitError(
                    f"Rate limit exceeded on {url}. "
                    f"Retried {retries} times."
                ) from e
            elif e.code == 401:
                raise AuthError(f"Authentication failed: {e.reason}") from e
            raise StockFinderError(f"HTTP {e.code}: {e.reason}") from e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_error = e
            if attempt < retries - 1:
                delay = _BASE_DELAY * (2**attempt)
                time.sleep(delay)
                continue
            raise StockFinderError(
                f"Request failed after {retries} retries: {e}"
            ) from e

    # Should not reach here, but satisfy the return type.
    raise StockFinderError(f"Request returned no data after {retries} retries") from last_error


# ── Search APIs ────────────────────────────────────────────


def search_videos(query, count=10, source="pexels", orientation="landscape"):
    """Search stock video footage.

    Args:
        query: Free-text search term.
        count: Max results (capped at 80 per provider limit).
        source: ``"pexels"`` or ``"pixabay"``.
        orientation: ``"landscape"`` | ``"portrait"`` | ``"square"``.

    Returns:
        List of dicts with keys:
        ``id``, ``url``, ``duration``, ``width``, ``height``,
        ``thumbnail``, ``description``.
    """
    count = min(count, 80)

    if source == "pexels":
        return _search_pexels_videos(query, count, orientation)
    elif source == "pixabay":
        return _search_pixabay_videos(query, count)
    else:
        raise ValueError(f"Unknown source: {source!r} (use 'pexels' or 'pixabay')")


def search_images(query, count=10, source="pexels"):
    """Search stock images.

    Args:
        query: Free-text search term.
        count: Max results (capped at 80).
        source: ``"pexels"`` or ``"pixabay"``.

    Returns:
        List of dicts with keys:
        ``id``, ``url``, ``width``, ``height``, ``thumbnail``.
    """
    count = min(count, 80)

    if source == "pexels":
        return _search_pexels_images(query, count)
    elif source == "pixabay":
        return _search_pixabay_images(query, count)
    else:
        raise ValueError(f"Unknown source: {source!r} (use 'pexels' or 'pixabay')")


# ── Pexels ─────────────────────────────────────────────────


def _search_pexels_videos(query, count, orientation="landscape"):
    headers = _pexels_headers()
    params = urllib.parse.urlencode({
        "query": query,
        "per_page": count,
        "orientation": orientation,
    })
    url = f"{PEXELS_BASE}/videos/search?{params}"
    data = _request(url, headers)

    results = []
    for v in data.get("videos", []):
        video_files = v.get("video_files", [])
        # Pick the highest-resolution file available.
        video_file = max(
            video_files,
            key=lambda f: (f.get("width") or 0) * (f.get("height") or 0),
            default=None,
        )
        file_url = video_file["link"] if video_file and video_file.get("link") else ""
        # Fallback description from the Pexels page slug.
        desc = query
        page_url = v.get("url", "")
        if page_url:
            slug = page_url.rstrip("/").split("/")[-1]
            desc = slug.replace("-", " ").replace("_", " ") if slug else query

        results.append({
            "id": str(v["id"]),
            "url": file_url,
            "duration": v.get("duration", 0),
            "width": video_file.get("width", 0) if video_file else 0,
            "height": video_file.get("height", 0) if video_file else 0,
            "thumbnail": v.get("image", ""),
            "description": desc,
        })
    return results


def _search_pexels_images(query, count):
    headers = _pexels_headers()
    params = urllib.parse.urlencode({
        "query": query,
        "per_page": count,
        "orientation": "portrait",
    })
    url = f"{PEXELS_BASE}/v1/search?{params}"
    data = _request(url, headers)

    results = []
    for p in data.get("photos", []):
        src = p.get("src", {})
        results.append({
            "id": str(p["id"]),
            "url": src.get("original", ""),
            "width": p.get("width", 0),
            "height": p.get("height", 0),
            "thumbnail": src.get("medium", src.get("small", "")),
        })
    return results


# ── Pixabay ────────────────────────────────────────────────


def _search_pixabay_videos(query, count):
    api_key = _pixabay_key()
    params = urllib.parse.urlencode({
        "key": api_key,
        "q": query,
        "per_page": count,
        "safesearch": "true",
    })
    url = f"{PIXABAY_BASE}/videos/?{params}"
    data = _request(url)

    results = []
    for v in data.get("hits", []):
        # Pick best available quality: large > medium > small > tiny.
        videos = v.get("videos", {})
        video_url = ""
        width, height = 0, 0
        for quality in ("large", "medium", "small", "tiny"):
            entry = videos.get(quality)
            if entry and entry.get("url"):
                video_url = entry["url"]
                width = entry.get("width", 0)
                height = entry.get("height", 0)
                break

        # Thumbnail: prefer large video thumbnail, fall back to user avatar.
        thumb = (
            videos.get("large", {}).get("thumbnail")
            or v.get("userImageURL", "")
        )

        results.append({
            "id": str(v["id"]),
            "url": video_url,
            "duration": v.get("duration", 0),
            "width": width,
            "height": height,
            "thumbnail": thumb,
            "description": v.get("tags", query),
        })
    return results


def _search_pixabay_images(query, count):
    api_key = _pixabay_key()
    params = urllib.parse.urlencode({
        "key": api_key,
        "q": query,
        "per_page": count,
        "safesearch": "true",
    })
    url = f"{PIXABAY_BASE}/?{params}"
    data = _request(url)

    results = []
    for p in data.get("hits", []):
        results.append({
            "id": str(p["id"]),
            "url": p.get("largeImageURL", p.get("webformatURL", "")),
            "width": p.get("imageWidth", 0),
            "height": p.get("imageHeight", 0),
            "thumbnail": p.get("previewURL", p.get("webformatURL", "")),
        })
    return results


# ── Download ───────────────────────────────────────────────


def download_video(video_url, output_path):
    """Download a video file to the local filesystem.

    Args:
        video_url: Direct URL to the video file (from search results).
        output_path: Local path to save the file.

    Returns:
        ``Path`` to the downloaded file.

    Raises:
        StockFinderError: On download failure.
    """
    if not video_url:
        raise StockFinderError("Empty video URL — nothing to download")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        urllib.request.urlretrieve(video_url, str(out))
    except Exception as exc:
        raise StockFinderError(f"Download failed: {exc}") from exc

    return out


def download_image(image_url, output_path):
    """Download an image file to the local filesystem.

    Args:
        image_url: Direct URL to the image file (from search results).
        output_path: Local path to save the file.

    Returns:
        ``Path`` to the downloaded file.

    Raises:
        StockFinderError: On download failure.
    """
    if not image_url:
        raise StockFinderError("Empty image URL — nothing to download")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        urllib.request.urlretrieve(image_url, str(out))
    except Exception as exc:
        raise StockFinderError(f"Download failed: {exc}") from exc

    return out
