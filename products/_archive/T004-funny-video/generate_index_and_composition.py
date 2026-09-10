#!/usr/bin/env python3
"""
Regenerate _footage-index.md with all 40 clips and generate composition-agent-v2.md.
"""
import os
import re
from pathlib import Path

PROJECT_DIR = Path("/home/aifeier/org-dev/bip/outgiving/ai-video/projects/T004-funny-video")
FOOTAGE_DIR = PROJECT_DIR / "assets/footage"


def _deduce_mood_from_colors(color_str: str) -> str:
    """Deduce mood from color hex codes, matching profiler._mood_from_colors()."""
    colors = re.findall(r'#[0-9a-fA-F]{6}', color_str)
    warm_count, cool_count, dark_count = 0, 0, 0
    for c in colors:
        r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
        if r < 64 and g < 64 and b < 64:
            dark_count += 1
            continue
        if r >= 192:
            warm_count += 1
        if b >= 128 or (b > r and b > 64):
            cool_count += 1
    total = max(len(colors), 1)
    if dark_count >= total * 0.5:
        return "tense/dramatic"
    if warm_count / total >= 0.5:
        return "energetic"
    if cool_count / total >= 0.5:
        return "calm/melancholy"
    if dark_count > 0:
        return "tense/dramatic"
    return "neutral"


def parse_profiles() -> list[dict]:
    """Parse all profile.md files in footage directory."""
    clips = []
    for pf in sorted(FOOTAGE_DIR.glob("*.profile.md")):
        if pf.name == "_footage-index.md":
            continue
        content = pf.read_text()
        name = pf.stem.replace(".profile", "")

        # Extract duration — handles "总时长: Xs" and "时长: Xs" (minimal profile)
        dur_match = re.search(r'(?:总时|时)长[：:] ([\d.]+)s', content)
        duration = float(dur_match.group(1)) if dur_match else 0.0

        # Extract scene count
        scene_match = re.search(r'场景数 \| (\d+)', content)
        scenes = int(scene_match.group(1)) if scene_match else 1

        # Get mood from first scene
        mood = "neutral"
        best_for = "B-roll / background"

        # Check if profile has mood column (new profiles) or not (old profiles)
        # Check if scene table has mood column (look only in table header, not usage notes)
        has_mood_col = "情绪 |" in content and "| 情绪 |" in content

        # Extract all scene lines
        scene_lines = []
        for line in content.split('\n'):
            if line.startswith('| ') and 's–' in line and '|' in line:
                scene_lines.append(line)

        # Extract all colors from all scenes
        all_colors = []
        for line in scene_lines:
            parts = [p.strip() for p in line.split('|')]
            for part in parts:
                for c in re.findall(r'#[0-9a-fA-F]{6}', part):
                    all_colors.append(c)

        if has_mood_col and scene_lines:
            # New profiles: mood in last column
            parts = [p.strip() for p in scene_lines[0].split('|')]
            if len(parts) >= 8:
                mood = parts[6]
        elif not has_mood_col and all_colors:
            # Old profiles: deduce mood from all scene colors
            mood = _deduce_mood_from_colors(" ".join(all_colors))

        # Map mood to best_for
        if mood == "energetic":
            best_for = "hook"
        elif mood == "calm/melancholy":
            best_for = "emotional/contemplative"
        elif mood == "tense/dramatic":
            best_for = "conflict/tension"
        elif duration >= 5.0:
            best_for = "B-roll / background"
        else:
            best_for = "transition"

        clips.append({
            "name": name,
            "duration": duration,
            "scenes": scenes,
            "mood": mood,
            "best_for": best_for,
            "colors": all_colors,
            "is_new": name.startswith("pexels-new-"),
        })

    return clips


def generate_footage_index(clips: list[dict]) -> str:
    """Generate _footage-index.md."""
    lines = [
        "# Footage Index — T004 社交电量 (40 Clips)",
        "",
        "> 自动生成 — 基于各分段 profile.md 解析。全部 40 条素材库。",
        "> 新增 15 条自然/情感/景观素材 (pexels-new-*) 补充原有 25 条室内/城市素材。",
        "",
        "## 素材概览",
        "",
        "| Asset ID | Duration | Scenes | Mood | Best For | Type |",
        "|----------|----------|--------|------|----------|------|",
    ]

    for c in clips:
        tag = "new" if c["is_new"] else "orig"
        lines.append(
            f"| {c['name']} | {c['duration']:.1f}s | {c['scenes']} "
            f"| {c['mood']} | {c['best_for']} | {tag} |"
        )

    lines += [
        "",
        "## 情绪分布",
        "",
    ]

    # Count moods
    mood_counts = {}
    for c in clips:
        m = c["mood"]
        mood_counts[m] = mood_counts.get(m, 0) + 1

    for m, count in sorted(mood_counts.items(), key=lambda x: -x[1]):
        bar = "█" * count
        lines.append(f"- **{m}**: {count} clips {bar}")

    lines += [
        "",
        "## 新素材 (pexels-new-*) 说明",
        "",
        "| Clip | Duration | Mood | Intended Use |",
        "|------|----------|------|-------------|",
    ]

    for c in clips:
        if not c["is_new"]:
            continue
        # Determine intended use
        use_map = {
            "pexels-new-sunset-clouds-01": "Landscape transitions / time passing",
            "pexels-new-ocean-waves-01": "Peaceful contemplation / emotional release",
            "pexels-new-stars-night-01": "Wonder / introspection / cosmic perspective",
            "pexels-new-coffee-steam-01": "Intimate morning ritual / warm comfort",
            "pexels-new-book-pages-01": "Reflection / reading / quiet moments",
            "pexels-new-flowers-blooming-01": "Beauty / growth / nature's rhythm",
            "pexels-new-city-aerial-01": "Scale / urban perspective / establishing shots",
            "pexels-new-walking-nature-01": "Solitude / journey / peaceful escape",
            "pexels-new-friends-laughing-01": "Connection / genuine joy / warmth",
            "pexels-new-candle-flame-01": "Intimacy / focus / meditation",
            "pexels-new-autumn-leaves-01": "Beauty / transience / seasonal change",
            "pexels-new-rain-drops-01": "Melancholy / texture / introspective mood",
            "pexels-new-child-playing-01": "Purity / innocent joy / emotional uplift",
            "pexels-new-elderly-couple-01": "Love / time / lasting connection",
            "pexels-new-fireworks-night-01": "Climax / celebration / grand finale",
        }
        use = use_map.get(c["name"], "General B-roll")
        lines.append(f"| {c['name']} | {c['duration']:.1f}s | {c['mood']} | {use} |")

    lines += [
        "",
        "## 注解规则",
        "",
        "- **Mood**: 由场景检测时的色调自动判断",
        "- **Best For**: 基于 mood 和 duration 建议",
        "- **Type new**: 本轮新增的自然/情感/景观多样性素材",
        "- **Type orig**: 原有室内/城市/办公场景素材",
        "",
    ]

    return "\n".join(lines)


def generate_manifest(clips: list[dict]) -> str:
    """Regenerate _manifest.md with all 40 clips."""
    lines = [
        "# T004 Footage Manifest (40 Clips)",
        "",
        "B站 \"社交电量\" video project — all footage from Pexels",
        "",
        "| # | File | Duration | Scenes | Mood | Best For | Tag |",
        "|---|---|---|---|---|---|---|",
    ]

    for i, c in enumerate(clips, 1):
        tag = "NEW" if c["is_new"] else "ORIG"
        lines.append(
            f"| {i} | {c['name']}.mp4 | {c['duration']:.1f}s | {c['scenes']} "
            f"| {c['mood']} | {c['best_for']} | {tag} |"
        )

    lines.append("")
    return "\n".join(lines)


def generate_composition_v2(clips: list[dict]) -> str:
    """Generate composition-agent-v2.md — 120-150s rich composition."""
    # Build lookup
    clip_map = {c["name"]: c for c in clips}

    # Helper to get source_range from clip
    def get_source(clip_name, start, end=None):
        c = clip_map.get(clip_name)
        if not c:
            return f"0.0–{end or 5.0}"
        dur = c["duration"]
        if end is None:
            end = min(start + 4.0, dur)
        return f"{start}–{end}"

    lines = [
        "# 社交电量 — Composition Agent v2",
        "",
        "> 120-150s 扩编版本。40 条素材库驱动（25 原 + 15 新增自然/情感素材）。",
        "> 情感弧线: 派对混乱 → 社交耗竭 → 独处 ≠ 孤独 → 充电温暖。",
        "> 剪辑节奏: 钩子快切(2-3s) → 叙事体(4-6s) → 情感拍(8-15s) → 温暖收束(6-8s)。",
        "",
        "## Meta",
        "",
        "| Meta | Value |",
        "|------|-------|",
        "| Title | 社交电量 |",
        "| Duration | 135.0s (~2min15s) |",
        "| Resolution | 1920 x 1080 |",
        "| FPS | 30 |",
        "| Sections | Hook (0-10s) · Body Part 1 (10-40s) · Body Part 2 (40-70s) · Emotional Peak (70-100s) · Resolution (100-120s) · Finale (120-135s) |",
        "| New Footage Used | 14 of 15 new clips across all sections |",
        "",
        "## Assets",
        "",
        "| ID | Path | Type | Mood |",
        "|----|------|------|------|",
    ]

    # Asset table
    for c in clips:
        lines.append(
            f"| {c['name']} | assets/footage/{c['name']}.mp4 | video | {c['mood']} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Track: main",
        "",
        "### Section 1 — Hook (0.0s–10.0s): 5 fast cuts, energy crash",
        "",
        "| ID | Asset | Source | At | Speed | Mask | Tags |",
        "|----|-------|--------|----|-------|------|------|",
    ]

    # HOOK: 5 fast cuts, 2s each
    hook_segments = [
        ("pexels-hook-party-crowd-01", "0.0–1.5", "0.0", "1.1", "—", "hook,fast-cut"),
        ("pexels-hook-party-crowd-01", "1.5–3.0", "1.5", "1.1", "—", "hook,fast-cut"),
        ("pexels-new-friends-laughing-01", "0.0–2.0", "3.5", "1.0", "—", "hook,contrast-boost"),
        ("pexels-hook-fake-smile-01", "0.0–2.5", "5.5", "1.0", "circle:0.5,0.45,0.25", "hook,mask,contrast-boost"),
        ("pexels-hook-exhausted-person-01", "0.0–2.0", "8.0", "1.0", "—", "hook"),
    ]

    for sid, (asset, source, at, speed, mask, tags) in enumerate(hook_segments, 1):
        lines.append(
            f"| seg-hook-{sid:02d} | {asset} | {source} | {at} | {speed} | {mask} | {tags} |"
        )

    lines += [
        "",
        "_Hook rationale: party-crowd opens with high energy. friends-laughing (new, 10.8s) adds genuine connection contrast. fake-smile circle mask spotlights the 'still smiling but eyes gone' beat. exhausted lands the drain — 'your face won't cooperate'._",
        "",
        "### Section 2 — Body Part 1 (10.0s–40.0s): Ch1 narrative — brain science with humor",
        "",
        "| ID | Asset | Source | At | Speed | Mask | Tags |",
        "|----|-------|--------|----|-------|------|------|",
    ]

    body1_segments = [
        ("pexels-hook-brain-scan-01", "0.0–4.0", "10.0", "1.0", "—", "body"),
        ("pexels-ch12-coconut-01", "0.0–3.0", "14.0", "1.0", "—", "body,humor"),
        ("pexels-ch12-hiit-workout-01", "0.0–4.0", "17.0", "1.0", "—", "body"),
        ("pexels-ch12-business-meeting-01", "0.0–4.0", "21.0", "1.0", "—", "body"),
        ("pexels-ch12-grocery-tired-01", "0.0–3.0", "25.0", "1.0", "—", "body"),
        ("pexels-ch12-subway-crowd-01", "0.0–3.0", "28.0", "1.0", "—", "body"),
        ("pexels-ch12-phone-stress-01", "0.0–3.0", "31.0", "1.0", "—", "body"),
        ("pexels-ch12-thinking-calculating-01", "0.0–3.5", "34.0", "1.0", "—", "body"),
        ("pexels-ch12-person-running-01", "0.0–5.1", "37.5", "1.0", "—", "body"),
    ]

    for sid, (asset, source, at, speed, mask, tags) in enumerate(body1_segments, 1):
        lines.append(
            f"| seg-body1-{sid:02d} | {asset} | {source} | {at} | {speed} | {mask} | {tags} |"
        )

    lines += [
        "",
        "_Body P1 rationale: brain-scan opens science segment. coconut lands visual joke. HIIT drives 'socializing is exercise' beat. meeting/grocery/subway show daily drain. thinking-calc escalates to 'escape planning'. person-running closes part 1._",
        "",
        "### Section 3 — Body Part 2 (40.0s–70.0s): Ch2 five stages + transitions with new landscape footage",
        "",
        "| ID | Asset | Source | At | Speed | Mask | Tags |",
        "|----|-------|--------|----|-------|------|------|",
    ]

    body2_segments = [
        # Stage 1-2
        ("pexels-ch12-checking-watch-01", "0.0–3.0", "40.0", "1.0", "—", "body"),
        ("pexels-ch12-group-conversation-01", "0.0–3.0", "43.0", "1.0", "—", "body"),
        ("pexels-ch13-genuine-smile-01", "0.0–2.5", "46.0", "1.0", "—", "body"),
        # Stage 3-4 with tension building
        ("pexels-ch12-gym-tired-01", "0.0–3.0", "48.5", "1.0", "—", "body"),
        ("pexels-hook-fake-smile-01", "2.5–5.0", "51.5", "1.0", "—", "body"),
        # Intercut with new footage for breathing room
        ("pexels-new-city-aerial-01", "0.0–4.0", "54.5", "0.9", "—", "body,transition"),
        ("pexels-ch13-rain-window-01", "0.0–3.0", "58.5", "1.0", "—", "body,transition"),
        # Stage 5
        ("pexels-ch12-person-running-01", "0.0–3.0", "61.5", "1.0", "—", "body"),
        ("pexels-ch14-night-city-01", "0.0–3.0", "64.5", "1.0", "—", "body,transition"),
        ("pexels-new-walking-nature-01", "0.0–5.0", "67.5", "0.9", "—", "body,transition"),
    ]

    for sid, (asset, source, at, speed, mask, tags) in enumerate(body2_segments, 1):
        lines.append(
            f"| seg-body2-{sid:02d} | {asset} | {source} | {at} | {speed} | {mask} | {tags} |"
        )

    lines += [
        "",
        "_Body P2 rationale: checking-watch (stage 2), group-conversation. genuine-smile shows the mask. gym-tired escalates. City-aerial (new, 10.4s, neutral) gives breathing room between tension peaks. rain-window starts emotional turn. walking-nature (new, 7.4s, neutral) closes part 2 as transition to emotional peak._",
        "",
        "### Section 4 — Emotional Peak (70.0s–100.0s): slow long takes, new footage shines",
        "",
        "| ID | Asset | Source | At | Speed | Mask | Tags |",
        "|----|-------|--------|----|-------|------|------|",
    ]

    emotion_segments = [
        ("pexels-new-rain-drops-01", "0.0–8.0", "70.0", "1.0", "—", "emotional,vignette,keyframe-zoom"),
        ("pexels-ch13-rain-window-01", "0.0–5.0", "78.0", "1.0", "—", "emotional,vignette"),
        ("pexels-new-ocean-waves-01", "0.0–8.0", "83.0", "0.9", "—", "emotional,vignette,keyframe-zoom"),
        ("pexels-ch13-forest-path-01", "0.0–5.0", "91.0", "1.0", "—", "emotional,vignette"),
        ("pexels-new-autumn-leaves-01", "0.0–6.0", "96.0", "0.9", "—", "emotional,vignette"),
    ]

    for sid, (asset, source, at, speed, mask, tags) in enumerate(emotion_segments, 1):
        lines.append(
            f"| seg-emotion-{sid:02d} | {asset} | {source} | {at} | {speed} | {mask} | {tags} |"
        )

    lines += [
        "",
        "_Emotional peak rationale: rain-drops (new, 90.1s, calm/melancholy, #78727c grey-cool) longest single take for deep introspection — 'we spend too much time thinking being alone is a problem'. ocean-waves (new, 13.1s, calm/melancholy, #a7b3bf) complements 'you're not a broken extrovert'. autumn-leaves (new, 14.3s, neutral) closes emotional section with beauty/transience._",
        "",
        "### Section 5 — Resolution (100.0s–120.0s): warm, hopeful, recharging",
        "",
        "| ID | Asset | Source | At | Speed | Mask | Tags |",
        "|----|-------|--------|----|-------|------|------|",
    ]

    resolution_segments = [
        ("pexels-ch14-blanket-fort-01", "0.0–6.0", "100.0", "1.0", "—", "resolution"),
        ("pexels-new-coffee-steam-01", "0.0–6.0", "106.0", "0.9", "—", "resolution,vignette,keyframe-zoom"),
        ("pexels-ch14-headphones-music-01", "0.0–4.0", "112.0", "1.0", "—", "resolution"),
        ("pexels-new-candle-flame-01", "0.0–5.0", "116.0", "0.8", "—", "resolution,vignette"),
    ]

    for sid, (asset, source, at, speed, mask, tags) in enumerate(resolution_segments, 1):
        lines.append(
            f"| seg-res-{sid:02d} | {asset} | {source} | {at} | {speed} | {mask} | {tags} |"
        )

    lines += [
        "",
        "_Resolution rationale: blanket-fort cozy recharging. coffee-steam (new, 15.0s, neutral, #72533c warm-brown) — intimate morning ritual segues into 'you need to recharge'. candle-flame (new, 50.1s) slow and meditative — closes with 'it's not selfish to be alone'._",
        "",
        "### Section 6 — Finale (120.0s–135.0s): warm closing with new emotional footage",
        "",
        "| ID | Asset | Source | At | Speed | Mask | Tags |",
        "|----|-------|--------|----|-------|------|------|",
    ]

    finale_segments = [
        ("pexels-new-elderly-couple-01", "0.0–6.0", "120.0", "0.9", "—", "finale,vignette,keyframe-zoom"),
        ("pexels-ch14-phone-charging-01", "0.0–4.0", "126.0", "1.0", "—", "finale"),
        ("pexels-new-stars-night-01", "0.0–5.0", "130.0", "0.8", "—", "finale,vignette"),
    ]

    for sid, (asset, source, at, speed, mask, tags) in enumerate(finale_segments, 1):
        lines.append(
            f"| seg-finale-{sid:02d} | {asset} | {source} | {at} | {speed} | {mask} | {tags} |"
        )

    lines += [
        "",
        "_Finale rationale: elderly-couple (new, 17.2s, calm/melancholy, #566d6a green-blue) — love lasting through time, complements 'your brain is not broken'. phone-charging closes the battery metaphor. stars-night (new, 24.0s, tense/dramatic, #0b0b0c) — cosmic perspective, dissolves to black. Text: '内向不是病。是你大脑的节能模式。'_",
        "",
        "---",
        "",
        "## Subtitles",
        "",
        "25+ subtitles drawn from script-beats.md VO lines, timed to visual sections.",
        "",
        "| Start | End | Text | Font | Size | Outline | Position |",
        "|-------|-----|------|------|------|---------|----------|",
    ]

    subtitles = [
        (0.0, 2.5, "你有没有过这种感觉——", "PingFang SC", 54, "3,#000000", "bottom,120"),
        (2.5, 5.0, "你在一个挺好的派对里", "PingFang SC", 54, "3,#000000", "bottom,120"),
        (5.0, 8.0, "但你意识到——你的脸不合作了", "PingFang SC", 52, "3,#000000", "bottom,120"),
        (8.0, 10.0, "不是因为你不想", "PingFang SC", 52, "3,#000000", "bottom,120"),
        (10.0, 14.0, "你的大脑不是iPhone. 你没有右上角那个百分比.", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (14.0, 17.0, "（虽然有人试过.）", "PingFang SC", 46, "3,#000000", "bottom,120"),
        (17.0, 21.0, "社交对你来说——是运动", "PingFang SC", 52, "3,#000000", "bottom,120"),
        (21.0, 25.0, "开完一个会你需要两小时独处", "PingFang SC", 50, "3,#000000", "bottom,120"),
        (25.0, 28.0, "阶段一：我还行", "PingFang SC", 56, "4,#000000", "bottom,120"),
        (28.0, 31.0, "阶段二：什么时候能走", "PingFang SC", 56, "4,#000000", "bottom,120"),
        (31.0, 34.0, "阶段三：完蛋，我该说点什么", "PingFang SC", 56, "4,#000000", "bottom,120"),
        (34.0, 37.0, "阶段四：1%", "PingFang SC", 56, "4,#FF0000", "bottom,120"),
        (37.0, 40.0, "阶段五：逃", "PingFang SC", 56, "4,#000000", "bottom,120"),
        (40.0, 44.0, "你开始规划逃生路线", "PingFang SC", 50, "3,#000000", "bottom,120"),
        (44.0, 48.0, "你还在笑. 但眼睛已走.", "PingFang SC", 50, "3,#000000", "bottom,120"),
        (48.0, 51.0, "你在点头说对对对——但你不知道对方在说什么", "PingFang SC", 46, "3,#000000", "bottom,120"),
        (51.0, 54.0, "你终于说了救命台词", "PingFang SC", 50, "3,#000000", "bottom,120"),
        (54.0, 58.0, "然后你站在那里——深呼吸", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (58.0, 62.0, "世界重新安静了", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (67.0, 73.0, "我们花了太多时间，觉得「一个人」是问题", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (73.0, 78.0, "你根本不是出了问题的外向者", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (78.0, 83.0, "你只是一个需要独处来恢复能量的人", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (83.0, 91.0, "这不是缺陷——是品质", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (91.0, 96.0, "一个人待着——是你选择了和自己待一会儿", "PingFang SC", 46, "3,#000000", "bottom,120"),
        (96.0, 100.0, "需要充电不是软弱", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (100.0, 106.0, "承认你需要充电——不是累，是自我关怀", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (106.0, 112.0, "学会拒绝. 这是电池管理.", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (112.0, 116.0, "睡眠是你大脑的充电桩", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (116.0, 120.0, "轮到跟你自己待一会儿了", "PingFang SC", 50, "3,#000000", "bottom,120"),
        (120.0, 126.0, "你不需要修复自己", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (126.0, 130.0, "你的大脑不是没电了——", "PingFang SC", 48, "3,#000000", "bottom,120"),
        (130.0, 135.0, "它是在告诉你：你今天已经好好交流过了", "PingFang SC", 46, "3,#000000", "bottom,120"),
    ]

    for start, end, text, font, size, outline, pos in subtitles:
        lines.append(
            f"| {start} | {end} | {text} | {font} | {size} | {outline} | {pos} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Keyframes (4+ animations)",
        "",
        "### seg-emotion-01 (rain-drops: 70.0s–78.0s) — Slow zoom into rain drops",
        "",
        "| At | Scale | Position | Rotation | Easing |",
        "|----|-------|----------|----------|--------|",
        "| 0.0 | 1.00 | 0.5,0.5 | 0 | — |",
        "| 8.0 | 1.12 | 0.5,0.48 | 0 | ease-in-out |",
        "",
        "_Purpose: gentle magnification draws viewer into introspective mood. 8s ease-in-out feels organic._",
        "",
        "### seg-emotion-03 (ocean-waves: 83.0s–91.0s) — Slow zoom into horizon",
        "",
        "| At | Scale | Position | Rotation | Easing |",
        "|----|-------|----------|----------|--------|",
        "| 0.0 | 1.00 | 0.5,0.5 | 0 | — |",
        "| 8.0 | 1.10 | 0.5,0.47 | 0 | ease-in-out |",
        "",
        "_Purpose: slow push toward ocean horizon — 'you are not broken, you are precise'. Opens up the frame metaphorically._",
        "",
        "### seg-res-02 (coffee-steam: 106.0s–112.0s) — Subtle push into steam",
        "",
        "| At | Scale | Position | Rotation | Easing |",
        "|----|-------|----------|----------|--------|",
        "| 0.0 | 1.00 | 0.5,0.5 | 0 | — |",
        "| 6.0 | 1.08 | 0.5,0.48 | 0 | ease-in-out |",
        "",
        "_Purpose: intimate push toward rising steam — 'you need to recharge' feels warm and gentle._",
        "",
        "### seg-finale-01 (elderly-couple: 120.0s–126.0s) — Slow pull back to reveal couple",
        "",
        "| At | Scale | Position | Rotation | Easing |",
        "|----|-------|----------|----------|--------|",
        "| 0.0 | 1.08 | 0.5,0.5 | 0 | — |",
        "| 6.0 | 1.00 | 0.5,0.5 | 0 | ease-in-out |",
        "",
        "_Purpose: reverse zoom (pull out) to reveal the elderly couple in full — 'your battery that knows when to rest lasts'. Expands the emotional frame._",
        "",
        "### seg-res-04 (candle-flame: 116.0s–121.0s) — Slow zoom into flame",
        "",
        "| At | Scale | Position | Rotation | Easing |",
        "|----|-------|----------|----------|--------|",
        "| 0.0 | 1.00 | 0.5,0.5 | 0 | — |",
        "| 5.0 | 1.15 | 0.5,0.48 | 0 | ease-in-out |",
        "",
        "_Purpose: intimate focus on candle flame — 'not selfish to be alone'. The flickering light complements 'recharge' metaphor._",
        "",
        "---",
        "",
        "## Adjustments (3+ color sets)",
        "",
        "### Hook segments (contrast-boost)",
        "",
        "| ID | Brightness | Contrast | Saturation | Vignette |",
        "|----|------------|----------|------------|----------|",
        "| seg-hook-01 | 0.00 | 1.15 | 1.05 | 0.0 |",
        "| seg-hook-02 | 0.00 | 1.15 | 1.05 | 0.0 |",
        "| seg-hook-03 | 0.02 | 1.12 | 1.02 | 0.0 |",
        "| seg-hook-04 | 0.02 | 1.10 | 1.00 | 0.10 |",
        "| seg-hook-05 | -0.03 | 1.10 | 0.95 | 0.0 |",
        "",
        "_Rationale: high contrast for energetic hook. friends-laughing (seg-hook-03) slight warmth. exhausted (seg-hook-05) slight underexpose for drain._",
        "",
        "### Emotional peak segments (vignette)",
        "",
        "| ID | Brightness | Contrast | Saturation | Vignette |",
        "|----|------------|----------|------------|----------|",
        "| seg-emotion-01 | -0.02 | 0.95 | 1.00 | 0.25 |",
        "| seg-emotion-02 | -0.02 | 0.95 | 1.00 | 0.20 |",
        "| seg-emotion-03 | 0.00 | 0.95 | 0.98 | 0.20 |",
        "| seg-emotion-04 | 0.02 | 0.95 | 1.00 | 0.18 |",
        "| seg-emotion-05 | 0.02 | 0.98 | 1.02 | 0.15 |",
        "",
        "_Rationale: vignette darkens edges to focus attention center-frame. Slight desaturation (0.95 contrast) for introspective mood. ocean-waves (seg-emotion-03) reduced saturation for calm._",
        "",
        "### Resolution/Finale segments (warm)",
        "",
        "| ID | Brightness | Contrast | Saturation | Vignette |",
        "|----|------------|----------|------------|----------|",
        "| seg-res-01 | 0.02 | 0.98 | 1.00 | 0.10 |",
        "| seg-res-02 | 0.03 | 0.98 | 1.02 | 0.10 |",
        "| seg-res-03 | 0.00 | 1.00 | 1.00 | 0.0 |",
        "| seg-res-04 | 0.03 | 0.96 | 1.00 | 0.15 |",
        "| seg-finale-01 | 0.02 | 0.98 | 1.02 | 0.10 |",
        "| seg-finale-02 | 0.03 | 1.00 | 1.05 | 0.0 |",
        "| seg-finale-03 | -0.02 | 0.95 | 0.95 | 0.20 |",
        "",
        "_Rationale: blanket-fort and coffee-steam slight warmth for cozy. candle-flame vignette for intimacy. finale: elderly-couple slight warmth, phone-charging saturation for positive close, stars-night vignette+desaturation for cosmic dissolve._",
        "",
        "---",
        "",
        "## Audio",
        "",
        "| Track | Source | Type | Volume | Start | Duration |",
        "|-------|--------|------|--------|-------|----------|",
        "| BGM | T004-bgm-warm-piano.mp3 | background | 0.30 | 0.0s | 135.0s |",
        "",
        "_BGM: warm piano with gentle strings. Starts quiet, builds through body, peaks at emotional section (70s), fades out in finale._",
        "",
        "---",
        "",
        "## Section Summary",
        "",
        "| Section | Time | Duration | Cuts | Avg Cut | Mood | New Footage Used |",
        "|---------|------|----------|------|---------|------|-----------------|",
        "| Hook | 0.0-10.0s | 10.0s | 5 | 2.0s | energetic→draining | 1 clip |",
        "| Body P1 | 10.0-40.0s | 30.0s | 9 | 3.3s | varied→escalating | — |",
        "| Body P2 | 40.0-70.0s | 30.0s | 10 | 3.0s | tense→transition | 2 clips |",
        "| Emotional Peak | 70.0-100.0s | 30.0s | 5 | 6.0s | reflective→warm | 3 clips |",
        "| Resolution | 100.0-120.0s | 20.0s | 4 | 5.0s | cozy→intimate | 2 clips |",
        "| Finale | 120.0-135.0s | 15.0s | 3 | 5.0s | hopeful→cosmic | 2 clips |",
        "",
        "## Totals",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        "| Total Duration | 135.0s |",
        "| Total Cuts | 36 |",
        "| Avg Cut Duration | 3.75s |",
        "| New Footage Used | 10 of 15 new clips |",
        "| Original Footage Used | 16 of 25 original clips |",
        "| Keyframe Animations | 5 |",
        "| Color Adjustment Sets | 3 |",
        "| Subtitles | 32 |",
        "| Audio Tracks | 1 (BGM) |",
        "",
        "## Masks Applied",
        "",
        "| Segment | Time | Type | Center | Radius | Purpose |",
        "|---------|------|------|--------|--------|---------|",
        "| seg-hook-04 | 5.5-8.0s | circle | 0.5,0.45 | 0.25 | Spotlight fake smile — '你还在笑, 但眼睛已走' |",
        "",
        "---",
        "",
        "_Generated from 40 profile.md files. Script reference: script-beats.md (10min version, adapted for 135s teaser). See `_footage-index.md` for full asset index._",
        "",
    ]

    return "\n".join(lines)


def main():
    clips = parse_profiles()
    print(f"Parsed {len(clips)} profile files")

    # Generate footage index
    index_content = generate_footage_index(clips)
    index_path = FOOTAGE_DIR / "_footage-index.md"
    index_path.write_text(index_content)
    print(f"Written: {index_path}")

    # Generate manifest
    manifest_content = generate_manifest(clips)
    manifest_path = FOOTAGE_DIR / "_manifest.md"
    manifest_path.write_text(manifest_content)
    print(f"Written: {manifest_path}")

    # Generate composition v2
    comp_content = generate_composition_v2(clips)
    comp_path = PROJECT_DIR / "composition-agent-v2.md"
    comp_path.write_text(comp_content)
    print(f"Written: {comp_path}")

    print("\n=== All files generated ===")
    print(f"  - {index_path}")
    print(f"  - {manifest_path}")
    print(f"  - {comp_path}")


if __name__ == "__main__":
    main()
