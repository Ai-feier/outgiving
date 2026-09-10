#!/usr/bin/env python3
"""
Download 15 diverse clips from Pexels for T004 project.
Uses curl subprocess (Pexels blocks python urllib).
"""
import json
import os
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

API_KEY = "VKFSkiruY3KFfWzr9FKkv13aUQlUnYTbAEf7CreVUbKqWKgNtzGnW9Pa"
FOOTAGE_DIR = Path("/home/aifeier/org-dev/bip/outgiving/ai-video/projects/T004-funny-video/assets/footage")

QUERIES = [
    ("sunset timelapse clouds", "pexels-new-sunset-clouds-01"),
    ("ocean waves calm morning", "pexels-new-ocean-waves-01"),
    ("stars night sky timelapse", "pexels-new-stars-night-01"),
    ("coffee steam close up morning", "pexels-new-coffee-steam-01"),
    ("book pages turning close up", "pexels-new-book-pages-01"),
    ("flowers blooming timelapse", "pexels-new-flowers-blooming-01"),
    ("city aerial drone skyline", "pexels-new-city-aerial-01"),
    ("person walking alone nature", "pexels-new-walking-nature-01"),
    ("friends laughing together genuine", "pexels-new-friends-laughing-01"),
    ("candle flame close up dark", "pexels-new-candle-flame-01"),
    ("autumn leaves falling sunlight", "pexels-new-autumn-leaves-01"),
    ("rain drops window bokeh", "pexels-new-rain-drops-01"),
    ("child playing innocent joy", "pexels-new-child-playing-01"),
    ("elderly couple holding hands", "pexels-new-elderly-couple-01"),
    ("fireworks celebration night sky", "pexels-new-fireworks-night-01"),
]

FOOTAGE_DIR.mkdir(parents=True, exist_ok=True)


def curl_get(url: str, max_timeout: int = 30) -> bytes:
    """GET via curl subprocess (bypasses Pexels urllib block)."""
    result = subprocess.run(
        ["curl", "-s", "--max-time", str(max_timeout),
         "-H", f"Authorization: {API_KEY}", url],
        capture_output=True, timeout=max_timeout + 10
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl exit code {result.returncode}: {result.stderr.decode()[:200]}")
    return result.stdout


def search_pexels(query: str) -> list[dict]:
    """Search Pexels videos API via curl."""
    encoded = urllib.parse.quote(query)
    url = f"https://api.pexels.com/videos/search?query={encoded}&per_page=3&orientation=landscape"

    try:
        raw = curl_get(url)
        data = json.loads(raw.decode())
    except Exception as e:
        print(f"  ERROR searching: {e}")
        return []

    candidates = []
    for video in data.get("videos", []):
        video_id = video.get("id")
        duration = video.get("duration", 0)

        best = None
        best_score = 0
        for vf in video.get("video_files", []):
            w = vf.get("width", 0) or 0
            h = vf.get("height", 0) or 0
            score = w * h
            if vf.get("quality") == "uhd":
                score *= 2
            if score > best_score and vf.get("link"):
                best_score = score
                best = vf

        if best:
            candidates.append({
                "video_id": video_id,
                "duration": duration,
                "width": best.get("width", 0),
                "height": best.get("height", 0),
                "quality": best.get("quality", ""),
                "link": best["link"],
            })

    return candidates


def download_file(url: str, outpath: Path) -> bool:
    """Download via curl with resume support."""
    result = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "120",
         "-C", "-",  # resume if partial
         "-o", str(outpath), url],
        capture_output=True, timeout=130
    )
    size = outpath.stat().st_size if outpath.exists() else 0
    if size < 1000:
        print(f"  ERROR: file too small ({size} bytes)")
        outpath.unlink(missing_ok=True)
        return False
    # Print human-readable size
    if size > 1024 * 1024:
        print(f"  Downloaded: {size // (1024*1024)}MB")
    else:
        print(f"  Downloaded: {size // 1024}KB")
    return True


def main():
    total = len(QUERIES)
    succeeded = 0
    skipped = 0
    failed = 0

    for i, (query, prefix) in enumerate(QUERIES, 1):
        filename = f"{prefix}.mp4"
        filepath = FOOTAGE_DIR / filename

        if filepath.exists() and filepath.stat().st_size > 1000:
            print(f"[{i}/{total}] SKIP: {filename} ({filepath.stat().st_size // 1024}KB)")
            skipped += 1
            continue

        print(f"[{i}/{total}] Searching: '{query}'")
        candidates = search_pexels(query)
        if not candidates:
            print(f"  FAIL: no results")
            failed += 1
            continue

        best = candidates[0]
        print(f"  Best: {best['width']}x{best['height']} {best['quality']} "
              f"({best['duration']}s) id={best['video_id']}")

        ok = download_file(best["link"], filepath)
        if ok:
            print(f"  OK -> {filename}")
            succeeded += 1
        else:
            print(f"  FAILED")
            failed += 1

        time.sleep(0.8)  # rate limit

    print(f"\n=== Summary: {succeeded} ok, {skipped} skip, {failed} fail ===")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
