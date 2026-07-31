"""Self-diagnosis — the system watches its own output and reports issues.

This is what makes the pipeline AGI-native: after each render, the system
analyzes the output and produces a structured report that the next agent
iteration can use to improve the composition.

Usage:
    from editor.diagnose import diagnose
    report = diagnose(composition, output_path)
    if report["issues"]:
        print(report["summary"])
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from editor.models import Composition

_FFPROBE = os.environ.get("FFPROBE_BINARY", "ffprobe")


def diagnose(comp: Composition, output_path: Path, expected_duration: float | None = None) -> dict:
    """Analyze rendered output and return a structured diagnostic report.

    Returns a dict that an agent can read and act on:
        {
            "status": "ok" | "warning" | "error",
            "duration": {"expected": 136.0, "actual": 138.2, "delta_pct": 1.6},
            "streams": ["video", "audio"],
            "video": {"width": 1920, "height": 1080, "codec": "h264"},
            "audio": {"present": true, "codec": "aac"},
            "subtitles": {"count": 32, "total_coverage_pct": 85},
            "issues": [
                {"severity": "warning", "type": "timing_drift", "detail": "..."},
            ],
            "summary": "2 issues: timing drift 1.6%, 3 subtitle gaps",
        }
    """
    if expected_duration is None:
        expected_duration = max(s.tl_end for t in comp.tracks for s in t.segments if t.type == "video")

    report: dict = {"status": "ok", "issues": [], "duration": {"expected": expected_duration}}

    # Probe output
    cmd = [_FFPROBE, "-v", "error",
           "-show_entries", "format=duration:stream=codec_type,width,height,codec_name",
           "-of", "json", str(output_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

    if result.returncode != 0 or not result.stdout.strip():
        report["status"] = "error"
        report["issues"].append({"severity": "error", "type": "probe_failed", "detail": result.stderr[:200]})
        return report

    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    fmt = data.get("format", {})

    # Duration check
    actual = float(fmt.get("duration", 0))
    delta_pct = abs(actual - expected_duration) / expected_duration * 100 if expected_duration > 0 else 0
    report["duration"]["actual"] = actual
    report["duration"]["delta_pct"] = round(delta_pct, 1)

    if delta_pct > 5:
        report["issues"].append({
            "severity": "error",
            "type": "timing_drift",
            "detail": f"Video {actual:.0f}s vs expected {expected_duration:.0f}s ({delta_pct:.1f}% off)"
        })
        report["status"] = "error"
    elif delta_pct > 1:
        report["issues"].append({
            "severity": "warning",
            "type": "timing_drift",
            "detail": f"Minor drift: {actual:.0f}s vs {expected_duration:.0f}s ({delta_pct:.1f}%)"
        })
        if report["status"] == "ok":
            report["status"] = "warning"

    # Stream check
    stream_types = [s.get("codec_type") for s in streams]
    report["streams"] = stream_types

    for s in streams:
        if s.get("codec_type") == "video":
            report["video"] = {"width": s.get("width"), "height": s.get("height"), "codec": s.get("codec_name")}
        elif s.get("codec_type") == "audio":
            report["audio"] = {"present": True, "codec": s.get("codec_name")}

    if "audio" not in report:
        report.setdefault("audio", {})["present"] = False
        basename = output_path.stem
        report["issues"].append({
            "severity": "warning",
            "type": "no_audio",
            "detail": f"No audio stream in output. Add an audio track to improve quality.",
            "suggestion": f"Add track bgm with asset: assets/audio/bgm-lofi.mp3 (volume: 0.2)"
        })
        if report["status"] == "ok":
            report["status"] = "warning"

    # Subtitle coverage check
    if comp.subtitles:
        total_dur = actual if actual > 0 else expected_duration
        sub_coverage = sum(s.end - s.start for s in comp.subtitles)
        coverage_pct = sub_coverage / total_dur * 100 if total_dur > 0 else 0
        report["subtitles"] = {"count": len(comp.subtitles), "total_coverage_pct": round(coverage_pct, 1)}

        # Detect gaps between subtitles (> 5s without text = potential dead air)
        sorted_subs = sorted(comp.subtitles, key=lambda s: s.start)
        gaps = []
        for i in range(len(sorted_subs) - 1):
            gap = sorted_subs[i + 1].start - sorted_subs[i].end
            if gap > 5:
                gaps.append({"from": sorted_subs[i].end, "to": sorted_subs[i + 1].start, "duration": gap})
        if gaps:
            report["issues"].append({
                "severity": "info",
                "type": "subtitle_gaps",
                "detail": f"{len(gaps)} gaps >5s without subtitles",
                "gaps": gaps,
            })

    # Segment-level check: find segments with zero-duration (failed to render)
    # Note: we can't probe individual segments post-render, so we flag based on model
    zero_segs = [s.id for t in comp.tracks for s in t.segments if t.type == "video" and (s.src_end - s.src_start) <= 0]
    if zero_segs:
        report["issues"].append({
            "severity": "error",
            "type": "zero_duration_segments",
            "detail": f"{len(zero_segs)} segments have zero source duration",
            "segments": zero_segs,
        })

    # Build summary
    issue_count = len(report["issues"])
    if issue_count == 0:
        report["summary"] = f"All checks passed. {actual:.0f}s, {len(stream_types)} streams."
    else:
        sev = [i["severity"] for i in report["issues"]]
        errs = sev.count("error")
        warns = sev.count("warning")
        parts = []
        if errs: parts.append(f"{errs} error(s)")
        if warns: parts.append(f"{warns} warning(s)")
        report["summary"] = f"{', '.join(parts)}. Duration {actual:.0f}s (Δ={abs(actual-expected_duration):.1f}s)."

    return report


def diagnose_and_log(comp: Composition, output_path: Path) -> dict:
    """Run diagnosis and write a report alongside the output."""
    report = diagnose(comp, output_path)
    log_path = output_path.with_suffix(".diagnosis.md")
    _write_md_report(report, log_path)
    return report


def _write_md_report(report: dict, path: Path) -> None:
    """Write a human/agent-readable markdown diagnosis file."""
    lines = [
        f"# Diagnosis: {path.stem}",
        f"",
        f"**Status**: `{report['status'].upper()}`",
        f"**Summary**: {report['summary']}",
        f"",
        f"## Output",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Duration | {report['duration'].get('actual', '?'):.1f}s (expected {report['duration'].get('expected', '?'):.0f}s, Δ={report['duration'].get('delta_pct', 0):.1f}%) |",
        f"| Streams | {', '.join(report.get('streams', []))} |",
    ]
    if "video" in report:
        v = report["video"]
        lines.append(f"| Video | {v.get('width', '?')}×{v.get('height', '?')} {v.get('codec', '?')} |")
    if report.get("audio", {}).get("present"):
        lines.append(f"| Audio | {report['audio'].get('codec', '?')} |")
    if "subtitles" in report:
        s = report["subtitles"]
        lines.append(f"| Subtitles | {s['count']} items, {s['total_coverage_pct']}% coverage |")

    if report["issues"]:
        lines += ["", "## Issues", ""]
        for i, issue in enumerate(report["issues"]):
            lines.append(f"**{i+1}. [{issue['severity'].upper()}] {issue['type']}**")
            lines.append(f"> {issue['detail']}")
            if "suggestion" in issue:
                lines.append(f"> **Fix**: {issue['suggestion']}")
            lines.append("")

    if report["status"] == "ok":
        lines += ["", "## Next Steps", "", "No issues detected. Ready for TTS voiceover integration."]

    path.write_text("\n".join(lines))
