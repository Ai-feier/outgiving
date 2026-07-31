"""TTS voiceover — Edge-TTS (free, no API key).

Usage:
    from editor.tts import synthesize
    synthesize("你好，欢迎收看。", "output/vo_001.mp3")
"""

from __future__ import annotations

import asyncio
import os
import subprocess
from pathlib import Path

_FFMPEG = os.environ.get("FFMPEG_BINARY", "ffmpeg")


def synthesize(text: str, output_path: str | Path, voice: str = "zh-CN-YunxiNeural",
               rate: str = "+0%", pitch: str = "+0Hz") -> Path:
    """Generate TTS audio using Edge-TTS (Microsoft, free).

    Args:
        text: Chinese text to speak.
        output_path: Where to save the mp3.
        voice: Voice name. Chinese options:
            zh-CN-YunxiNeural (男, 云希, recommended)
            zh-CN-YunyangNeural (男, 云扬, news style)
            zh-CN-XiaoxiaoNeural (女, 晓晓)
            zh-CN-XiaoyiNeural (女, 晓伊)
        rate: Speed adjustment, e.g. "+10%" or "-5%".
        pitch: Pitch adjustment, e.g. "+5Hz" or "-2Hz".

    Returns:
        Path to the generated mp3 file.
    """
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Use subprocess to call edge-tts CLI (avoids asyncio issues)
    cmd = [
        "edge-tts",
        "--voice", voice,
        "--text", text,
        "--rate", rate,
        "--pitch", pitch,
        "--write-media", str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=60)
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"edge-tts failed: {stderr[:200]}")

    return output_path


def synthesize_segments(segments: list[dict], output_dir: str | Path,
                        voice: str = "zh-CN-YunxiNeural") -> list[Path]:
    """Batch-generate TTS segments for a timeline.

    Args:
        segments: List of {"text": "...", "start": 0.5, "end": 2.5}.
        output_dir: Directory for output mp3 files.
        voice: Edge-TTS voice name.

    Returns:
        List of generated mp3 paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = []
    for i, seg in enumerate(segments):
        out = output_dir / f"vo_{i:03d}.mp3"
        if out.exists():
            paths.append(out)
            continue
        try:
            synthesize(seg["text"], out, voice=voice)
            paths.append(out)
        except Exception as e:
            print(f"  TTS FAIL [{i}]: {e}")
            # Fall back: generate silence
            dur = seg.get("end", 1.0) - seg.get("start", 0.0)
            _silence(dur, out)
            paths.append(out)
    return paths


def _silence(duration: float, output: Path) -> None:
    subprocess.run([
        _FFMPEG, "-y",
        "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={duration}",
        "-c:a", "libmp3lame", "-q:a", "2",
        str(output)
    ], capture_output=True, timeout=10)
