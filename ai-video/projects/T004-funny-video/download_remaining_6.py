#!/usr/bin/env python3
"""Download remaining 6 clips from Pexels."""
import json, subprocess, sys, time, urllib.parse
from pathlib import Path

API_KEY = "VKFSkiruY3KFfWzr9FKkv13aUQlUnYTbAEf7CreVUbKqWKgNtzGnW9Pa"
DIR = Path("/home/aifeier/org-dev/bip/outgiving/ai-video/projects/T004-funny-video/assets/footage")

QUERIES = [
    ("candle flame close up dark", "pexels-new-candle-flame-01"),
    ("autumn leaves falling sunlight", "pexels-new-autumn-leaves-01"),
    ("rain drops window bokeh", "pexels-new-rain-drops-01"),
    ("child playing innocent joy", "pexels-new-child-playing-01"),
    ("elderly couple holding hands", "pexels-new-elderly-couple-01"),
    ("fireworks celebration night sky", "pexels-new-fireworks-night-01"),
]

def search(q):
    url = f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page=3&orientation=landscape"
    raw = subprocess.run(["curl", "-s", "--max-time", "30", "-H", f"Authorization: {API_KEY}", url],
                         capture_output=True, timeout=40).stdout
    data = json.loads(raw)
    best, best_s = None, 0
    for v in data.get("videos", []):
        for vf in v.get("video_files", []):
            w, h = (vf.get("width") or 0), (vf.get("height") or 0)
            s = w * h * (2 if vf.get("quality") == "uhd" else 1)
            if s > best_s and vf.get("link"):
                best_s, best = s, vf
    return best

for i, (query, prefix) in enumerate(QUERIES, 1):
    fn = f"{prefix}.mp4"
    fp = DIR / fn
    if fp.exists() and fp.stat().st_size > 1000:
        print(f"[{i}/6] SKIP {fn} ({fp.stat().st_size//1024}KB)")
        continue
    print(f"[{i}/6] '{query}'...", end=" ", flush=True)
    vf = search(query)
    if not vf:
        print("FAIL (no results)")
        continue
    link = vf["link"]
    print(f"{vf['width']}x{vf['height']} -> {fn}", end=" ", flush=True)
    subprocess.run(["curl", "-s", "-L", "--max-time", "90", "-o", str(fp), link],
                   capture_output=True, timeout=100)
    sz = fp.stat().st_size if fp.exists() else 0
    if sz > 1000:
        print(f"OK ({sz//1024}KB)")
    else:
        fp.unlink(missing_ok=True)
        print("FAIL")
    time.sleep(0.8)
print("Done.")
