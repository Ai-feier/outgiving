#!/usr/bin/env python3
"""Generate _footage-index.md from all .profile.md files in footage directory."""

import re
import sys
from pathlib import Path

_scripts_src = Path("/home/aifeier/org-dev/bip/outgiving/scripts/src")
if str(_scripts_src) not in sys.path:
    sys.path.insert(0, str(_scripts_src))

from editor.profiler import _mood_from_colors, _best_for


def parse_profile(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    src_file = ""
    m = re.search(r'\|\s*文件\s*\|\s*`([^`]+)`\s*\|', text)
    if m:
        src_file = m.group(1)
    asset_id = path.stem.replace(".profile", "")
    duration = 0.0
    m = re.search(r'\|\s*时长\s*\|\s*([\d.]+)s\s*\|', text)
    if m:
        duration = float(m.group(1))
    scene_count = 0
    m = re.search(r'\|\s*场景数\s*\|\s*(\d+)\s*\|', text)
    if m:
        scene_count = int(m.group(1))
    all_colors = []
    scene_rows = re.findall(
        r'^\|\s*\d+\s*\|.*?\|.*?\|(.*?)\|\s*[✓⚠]',
        text, re.MULTILINE
    )
    for colors_str in scene_rows:
        colors_str = colors_str.strip()
        colors = [c.strip() for c in re.split(r'\s*[·•]\s*', colors_str)
                  if c.strip() and c.strip() != '—']
        all_colors.extend(colors)
    mood = _mood_from_colors(all_colors) if all_colors else "neutral"
    best_for = _best_for(mood, duration, scene_count)
    return {"asset_id": asset_id, "src_file": src_file, "duration": duration,
            "scene_count": scene_count, "mood": mood, "best_for": best_for}


def main():
    footage_dir = Path("/home/aifeier/org-dev/bip/outgiving/ai-video/projects/T004-funny-video/assets/footage")
    profiles = sorted(footage_dir.glob("*.profile.md"))
    if not profiles:
        print(f"No .profile.md files found in {footage_dir}")
        sys.exit(1)
    results = []
    for p in profiles:
        if p.name == "_footage-index.md":
            continue
        try:
            info = parse_profile(p)
            results.append(info)
        except Exception as e:
            print(f"Warning: failed to parse {p.name}: {e}", file=sys.stderr)

    def sort_key(r):
        aid = r["asset_id"]
        if "hook" in aid:
            return (0, aid)
        elif "ch12" in aid:
            return (1, aid)
        elif "ch13" in aid:
            return (2, aid)
        elif "ch14" in aid:
            return (3, aid)
        return (4, aid)

    results.sort(key=sort_key)

    lines = [
        "# Footage Index — T004 社交电量",
        "",
        "> 自动生成 — 基于各分段 profile.md 解析。帮助 agent 快速了解素材库全貌。",
        "",
        "| Asset ID | Duration | Scenes | Mood | Best For |",
        "|----------|----------|--------|------|----------|",
    ]
    for r in results:
        lines.append(
            f"| {r['asset_id']} | {r['duration']:.1f}s | {r['scene_count']} | {r['mood']} | {r['best_for']} |"
        )
    lines += [
        "",
        "## 注解规则",
        "",
        "- **Mood**: 由 _mood_from_colors() 自动判断——暖色→energetic，冷色→calm/melancholy，暗色→tense/dramatic，混合→neutral",
        "- **Best For**: 由 _best_for() 建议：hook / emotional/contemplative / conflict/tension / B-roll / transition",
        "- 能量偏高的素材适合开头钩子或高潮，能量偏低的适合过渡或情感瞬间",
        "",
    ]
    out_path = footage_dir / "_footage-index.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Written: {out_path} ({len(results)} entries)")


if __name__ == "__main__":
    main()
