"""
渲染引擎 — re-export from modular abstractions.

engine.py    编排器：probe → render tracks → composite → subtitle burn → output
segments.py  分段渲染：trim + speed + color + keyframes + mask → temp file
tracks.py    轨道组装：gap 填充 + concat + overlay + audio mix
subtitles.py ASS 字幕：样式管理 + 重叠检测 + ASS 格式输出
keyframes.py 关键帧：scale/rotation + easing → ffmpeg 表达式
mask_png.py  PNG mask：Pillow 预生成 alpha mask（快 10-50x vs per-frame geq）
"""

from editor.engine import render

__all__ = ["render"]
