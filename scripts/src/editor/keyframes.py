"""Keyframe expression builder — Keyframe list → ffmpeg filter expression.

Generates ffmpeg ``if(lte(t,...))`` expression chains for per-frame evaluation.
Supports scale and rotation with linear/ease-in/ease-out/ease-in-out easing.
"""

from __future__ import annotations

from editor.models import Keyframe


def build_keyframe_filter(kfs: list[Keyframe]) -> str:
    """Build ffmpeg filter string for scale + rotation keyframe animation.

    Returns empty string if no animation is needed (all frames at default values).
    """
    if not kfs:
        return ""

    kfs = sorted(kfs, key=lambda k: k.at)
    parts = []

    # Scale
    if any(kf.scale != 1.0 for kf in kfs):
        expr = _build_attr_expr(kfs, "scale", 1.0)
        parts.append(f"scale=iw*({_escape(expr)}):ih*({_escape(expr)}):eval=frame")

    # Rotation
    if any(kf.rotation != 0.0 for kf in kfs):
        expr = _build_attr_expr(kfs, "rotation", 0.0)
        rad_expr = f"({_escape(expr)})*PI/180"
        parts.append(f"rotate={rad_expr}:ow=iw:oh=ih:eval=frame")

    return ",".join(parts)


# ── expression building ────────────────────────────────────


def _build_attr_expr(kfs: list[Keyframe], attr: str, default: float) -> str:
    """Build nested if(lte(t,...),...,default) expression for a keyframe attribute."""
    # Build from last to first (innermost to outermost)
    expr = str(default)
    for i in range(len(kfs) - 2, -1, -1):
        v0 = _get_attr(kfs[i], attr, default)
        v1 = _get_attr(kfs[i + 1], attr, default)
        t0, t1 = kfs[i].at, kfs[i + 1].at
        if t1 <= t0:
            continue
        seg = _lerp(v0, v1, t0, t1, kfs[i + 1].easing)
        expr = f"if(lte(t,{t1}),{seg},{expr})"

    # Handle t=0 to first keyframe
    if kfs[0].at > 0:
        v1 = _get_attr(kfs[0], attr, default)
        seg = _lerp(default, v1, 0, kfs[0].at, kfs[0].easing)
        expr = f"if(lte(t,{kfs[0].at}),{seg},{expr})"

    return expr


def _get_attr(kf: Keyframe, attr: str, default: float) -> float:
    return getattr(kf, attr, default)


def _lerp(v0: float, v1: float, t0: float, t1: float, easing: str) -> str:
    """Return a ffmpeg expression string for linear/eased interpolation."""
    if t1 <= t0:
        return str(v0)
    if easing == "linear" or not easing:
        return f"{v0}+({v1}-{v0})*(t-{t0})/{t1 - t0}"
    # Normalized t in [0, 1]
    nt = f"(t-{t0})/{t1 - t0}"
    if easing == "ease-in":
        curve = f"pow({nt},2)"
    elif easing == "ease-out":
        curve = f"1-pow(1-({nt}),2)"
    elif easing == "ease-in-out":
        curve = f"if(lt({nt},0.5),2*pow({nt},2),1-pow(-2*({nt})+2,2)/2)"
    else:
        curve = str(nt)
    return f"{v0}+({v1}-{v0})*({curve})"


def _escape(s: str) -> str:
    """Escape commas and colons for ffmpeg filter argument syntax."""
    return s.replace(",", "\\,").replace(":", "\\:")
