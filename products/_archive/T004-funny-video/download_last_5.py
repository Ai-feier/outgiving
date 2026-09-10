#!/usr/bin/env python3
"""Download remaining 5 clips from Pexels with fixed search."""
import json, subprocess, sys, time, urllib.parse
from pathlib import Path

API_KEY = "VKFSkiruY3KFfWzr9FKkv13aUQlUnYTbAEf7CreVUbKqWKgNtzGnW9Pa"
DIR = Path("/home/aifeier/org-dev/bip/outgiving/ai-video/projects/T004-funny-video/assets/footage")

QUERIES = [
    ("autumn leaves falling", "pexels-new-autumn-leaves-01"),
    ("rain drops window", "pexels-new-rain-drops-01"),
    ("child playing happy", "pexels-new-child-playing-01"),
    ("elderly couple walking", "pexels-new-elderly-couple-01"),
    ("fireworks night sky", "pexels-new-fireworks-night-01"),
]

def search(q):
    url = f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page=3&orientation=landscape"
    raw = subprocess.run(["curl", "-s", "--max-time", "30", "-H", f"Authorization: {API_KEY}", url],
                         capture_output=True, timeout=40).stdout
    data = json.loads(raw)
    print(f"  results: {len(data.get('videos', []))}", end="", flush=True)
    best, best_score = None, 0
    for v in data.get("videos", []):
        for vf in v.get("video_files", []):
            w, h = (vf.get("width") or 0), (vf.get("height") or 0)
            score = w * h * (2 if vf.get("quality") == "uhd" else 1)
            if score > best_score and vf.get("link"):
                best_score = score
                best = vf
    return best

for i, (query, prefix) in enumerate(QUERIES, 1):
    fn = f"{prefix}.mp4"
    fp = DIR / fn
    if fp.exists() and fp.stat().st_size > 1000:
        print(f"[{i}/5] SKIP {fn}")
        continue
    print(f"[{i}/5] '{query}'...", end=" ", flush=True)
    vf = search(query)
    if not vf:
        print(" -> FAIL (no results)")
        continue
    link = vf["link"]
    print(f" -> {vf['width']}x{vf['height']} downloading...", end=" ", flush=True)
    subprocess.run(["curl", "-s", "-L", "--max-time", "120", "-o", str(fp), link],
                   capture_output=True, timeout=130)
    sz = fp.stat().st_size if fp.exists() else 0
    if sz > 1000:
        print(f"OK ({sz//1024}KB)")
    else:
        fp.unlink(missing_ok=True)
        print("FAIL")
    time.sleep(0.8)
print("Done.")
