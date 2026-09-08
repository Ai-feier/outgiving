# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownParameterType=false, reportUnknownLambdaType=false
# 理由：parser 把 object 树收窄为 dict/list（isinstance 收窄 → dict[Unknown, Unknown]）；
# 边界转换全部过 _float/_int/str() 助手并抛 CompositionFormatError，类型风险已受控。
"""
Markdown manifest 解析器 — YAML schema（agent 写 composition.md 的实际形状）。


节合同（## 标题，大小写不敏感；未知节 → CompositionFormatError 带节名）：
  # Title            → composition 名
  ## Meta            → 列表项：duration/width/height/fps/bg_color/output/crf/preset
  ## Assets          → ### <type> 组；每项 {id, src}
  ## Track: <id>     → 顶层 dict {order,type,blend_mode,opacity} + segments 列表
                       段字段：asset/start/end/speed/volume/transform/effects/
                       blend_mode/opacity/fade_in/fade_out/mask/tags
                       （start/end = 时间线绝对秒；src 区间由 speed 反推）
  ## Masks           → 列表 {id,type,target,timeline,params}
  ## Subtitles       → 列表 {start,end,text,style?}
  ## Subtitle Styles → 列表 {id,font,font_size,primary_color,...}
  ## Keyframes       → 列表 {target,property,type,keyframes:[{time,value,easing}]}
  ## Chapter Markers → 列表（非渲染元数据）
  ## Output          → 列表项 format/codec/bitrate/file

所有解析错误抛 CompositionFormatError（带行号 + 节名/段名），不静默丢段。
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import cast

from editor import yamlmini
from editor.models import (
    Asset,
    Composition,
    Keyframe,
    KeyframeSpec,
    Mask,
    PropertyKeyframe,
    Segment,
    Subtitle,
    SubtitleStyle,
    Track,
)
from editor.yamlmini import YamlMiniError, parse_doc


class CompositionFormatError(Exception):
    """manifest 违反 schema。message 含节名/段名 + 行号。"""

    def __init__(self, section: str, msg: str, line_no: int = 0) -> None:
        loc = f" [{section}]" if section else ""
        ln = f" (line {line_no})" if line_no else ""
        super().__init__(f"composition.md{loc}: {msg}{ln}")
        self.section = section
        self.line_no = line_no


# ── 入口 ───────────────────────────────────────────────────


def from_markdown(md_path: str | Path) -> Composition:
    """解析 composition.md（YAML schema）→ Composition。"""
    p = Path(md_path).resolve()
    text = p.read_text()
    lines = text.split("\n")
    base_dir = p.parent

    comp = Composition(name="untitled")
    sections: list[tuple[str, int, list[str]]] = []  # (header, line_no, body)
    cur_header = ""
    cur_no = 0
    cur_body: list[str] = []

    for no, line in enumerate(lines, start=1):
        s = line.strip()
        if s.startswith("# ") and not s.startswith("## "):
            comp.name = s[2:].strip().removeprefix("Composition:").strip() or comp.name
            continue
        if s.startswith("## "):
            if cur_header or cur_body:
                sections.append((cur_header, cur_no, cur_body))
            cur_header = s[3:].strip()
            cur_no = no
            cur_body = []
            continue
        if cur_header:
            cur_body.append(line)
    if cur_header or cur_body:
        sections.append((cur_header, cur_no, cur_body))

    if not sections:
        raise CompositionFormatError("", "没有任何 ## 节", 1)

    styles_section: tuple[str, int, list[str]] | None = None
    track_sections: list[tuple[str, int, list[str]]] = []

    for header, no, body in sections:
        key = header.lower()
        if key.startswith("meta"):
            _ingest_meta(key, no, body, comp)
        elif key.startswith("assets"):
            _ingest_assets(key, no, body, comp, base_dir)
        elif key.startswith("track:"):
            track_sections.append((header, no, body))
        elif key.startswith("masks"):
            _ingest_masks(key, no, body, comp)
        elif key.startswith("subtitles"):
            _ingest_subtitles(key, no, body, comp)
        elif key.startswith("subtitle styles"):
            styles_section = (header, no, body)
        elif key.startswith("keyframes"):
            _ingest_keyframes(key, no, body, comp)
        elif key.startswith("chapter markers"):
            comp.chapter_markers = _as_dicts(key, no, body)
        elif key.startswith("output"):
            for item in _as_dicts(key, no, body):
                for k, v in item.items():
                    if isinstance(v, str):
                        comp.output[k] = v
        else:
            raise CompositionFormatError(header, f"未知节 '## {header}'", no)

    for header, no, body in track_sections:
        _ingest_track(header, no, body, comp)

    if styles_section:
        _ingest_subtitle_styles(styles_section[0], styles_section[1], styles_section[2], comp)

    _distribute_masks(comp)
    _distribute_keyframes(comp)
    _validate(comp)
    return comp


# 兼容旧名（cli_edit.py / editor/__init__ 用）
parse_manifest = from_markdown


# ── 各节 ingest ────────────────────────────────────────────


def _ingest_meta(section: str, no: int, body: list[str], comp: Composition) -> None:
    rows = _as_dicts(section, no, body)
    for r in rows:
        for k, v in r.items():
            _apply_meta(k, section, no, v, comp)


def _apply_meta(k: str, section: str, no: int, v: object, comp: Composition) -> None:
    if k == "duration":
        return  # 元数据：总时长由时间线计算，不覆盖
    if k == "width":
        comp.width = _int(v, section, no, "width")
    elif k == "height":
        comp.height = _int(v, section, no, "height")
    elif k == "fps":
        comp.fps = _int(v, section, no, "fps")
    elif k == "bg_color":
        comp.bg_color = str(v)
    elif k in ("output", "output_file"):
        comp.output["file"] = str(v)
    elif k in ("crf", "preset", "format", "codec", "bitrate", "file"):
        comp.extra_meta[k] = str(v)
    else:
        raise CompositionFormatError(section, f"Meta 未知键 '{k}'", no)


def _ingest_assets(
    section: str, no: int, body: list[str], comp: Composition, base_dir: Path
) -> None:
    for group, gbody in yamlmini.split_blocks("\n".join(body)):
        gname = group.lower()
        if gname and gname not in (
            "video",
            "audio",
            "image",
            "texture",
            "animation",
            "font",
            "other",
        ):
            raise CompositionFormatError(section, f"Assets 未知素材类型组 '### {group}'", no)
        atype = gname or "video"
        items = _as_dicts(section, no, gbody)
        for r in items:
            iid = str(r.get("id") or "")
            src = str(r.get("src") or r.get("path") or "")
            if not iid or not src:
                raise CompositionFormatError(section, f"asset 缺 id 或 src: {r!r}", no)
            if comp.asset_by_id(iid):
                raise CompositionFormatError(section, f"asset id 重复: '{iid}'", no)
            path = src if src.startswith("/") else str(base_dir / src)
            asset = Asset(id=iid, path=path, type=atype)
            if "duration" in r:
                asset.duration = _float(r["duration"], section, no, f"{iid}.duration")
            comp.assets.append(asset)


def _ingest_track(header: str, no: int, body: list[str], comp: Composition) -> None:
    track_id = header.split(":", 1)[1].strip()
    lines = _clean(body, strip_groups=True)
    doc, _ = _parse_doc(lines, no)
    allowed = {"order", "type", "blend_mode", "opacity", "segments"}
    unknown = set(doc) - allowed
    if unknown:
        raise CompositionFormatError(header, f"track 顶层未知键: {sorted(unknown)}", no)
    order = _int(doc.get("order", 0), header, no, f"track.{track_id}.order")
    track = Track(
        id=track_id,
        type=str(doc.get("type", "video")),
        order=order,
        blend_mode=str(doc.get("blend_mode", "normal")),
        opacity=_float(doc.get("opacity", 1.0), header, no, f"track.{track_id}.opacity"),
    )
    if track.type not in ("video", "audio"):
        raise CompositionFormatError(header, f"track type 必须是 video|audio: '{track.type}'", no)
    segs_raw = doc.get("segments")
    if not isinstance(segs_raw, list):
        raise CompositionFormatError(header, f"track '{track_id}' 缺 segments 列表", no)
    for idx, item in enumerate(list(segs_raw)):
        if not isinstance(item, dict):
            raise CompositionFormatError(header, f"track '{track_id}' 第 {idx + 1} 段不是 dict", no)
        seg = _make_segment(track, idx, cast("dict[str, object]", item), no, header)
        track.segments.append(seg)
    if not track.segments:
        raise CompositionFormatError(header, f"track '{track_id}' 没有 segments", no)
    comp.tracks.append(track)


_SEG_KEYS = {
    "asset",
    "start",
    "end",
    "speed",
    "volume",
    "envelope",
    "transform",
    "effects",
    "blend_mode",
    "opacity",
    "fade_in",
    "fade_out",
    "mask",
    "tags",
}


def _make_segment(
    track: Track, idx: int, item: dict[str, object], no: int, section: str
) -> Segment:
    unknown = set(item) - _SEG_KEYS
    if unknown:
        raise CompositionFormatError(
            section,
            f"段 {idx + 1} (asset={item.get('asset', '?')}) 未知字段: {sorted(unknown)}",
            no,
        )
    asset_id = str(item.get("asset") or "")
    if not asset_id:
        raise CompositionFormatError(section, f"track '{track.id}' 第 {idx + 1} 段缺 asset", no)
    start = _float(item.get("start"), section, no, f"{asset_id}.start")
    end = _float(item.get("end"), section, no, f"{asset_id}.end")
    if end <= start:
        raise CompositionFormatError(
            section,
            f"段 {asset_id}: end({end}) 必须 > start({start})",
            no,
        )
    speed = _float(item.get("speed", 1.0), section, no, f"{asset_id}.speed")
    if speed <= 0:
        raise CompositionFormatError(section, f"段 {asset_id}: speed 必须 > 0", no)
    tl_start = start
    tl_span = end - start
    src_start = 0.0
    src_end = tl_span / speed  # 源素材需播放的时长（引擎 setpts 变速）

    tf_raw = item.get("transform")
    if tf_raw is not None and not isinstance(tf_raw, dict):
        raise CompositionFormatError(section, f"段 {asset_id}: transform 必须是 map", no)
    tf: dict[str, object] = cast("dict[str, object]", tf_raw) if tf_raw is not None else {}
    t_scale = _vec2(tf.get("scale"), section, no, f"{asset_id}.transform.scale")
    t_pos = _vec2(tf.get("position"), section, no, f"{asset_id}.transform.position")

    eff_raw = item.get("effects")
    if eff_raw is not None and not isinstance(eff_raw, dict):
        raise CompositionFormatError(section, f"段 {asset_id}: effects 必须是 map", no)
    eff: dict[str, object] = cast("dict[str, object]", eff_raw) if eff_raw is not None else {}
    adjustments: dict[str, float] = {}
    color_raw = eff.get("color")
    if isinstance(color_raw, dict):
        color: dict[str, object] = cast("dict[str, object]", color_raw)
        for ck in ("brightness", "contrast", "saturation", "temperature"):
            if ck in color:
                adjustments[ck] = _float(color[ck], section, no, f"{asset_id}.effects.color.{ck}")
    vig_raw = eff.get("vignette")
    if isinstance(vig_raw, dict) and "strength" in vig_raw:
        vig: dict[str, object] = cast("dict[str, object]", vig_raw)
        adjustments["vignette"] = _float(vig["strength"], section, no, f"{asset_id}.vignette")
    for ek in sorted(set(eff) - {"color", "vignette"}):
        raise CompositionFormatError(section, f"段 {asset_id}: 未知 effect '{ek}'", no)

    env_raw = item.get("envelope")
    envelope: list[tuple[float, float]] = []
    if isinstance(env_raw, list):
        for p in list(env_raw):
            if not isinstance(p, dict) or "time" not in p or "volume" not in p:
                raise CompositionFormatError(
                    section, f"段 {asset_id}: envelope 项缺 time/volume", no
                )
            pd: dict[str, object] = cast("dict[str, object]", p)
            rel = _float(pd["time"], section, no, f"{asset_id}.envelope") - start
            envelope.append((rel, _float(pd["volume"], section, no, f"{asset_id}.envelope")))
    elif env_raw is not None:
        raise CompositionFormatError(section, f"段 {asset_id}: envelope 必须是列表", no)

    tags_raw = item.get("tags")
    tags = [str(t) for t in tags_raw] if isinstance(tags_raw, list) else []

    return Segment(
        id=f"{track.id}-{idx}",
        asset_id=asset_id,
        src_start=src_start,
        src_end=src_end,
        tl_start=tl_start,
        speed=speed,
        volume=_float(item.get("volume", 1.0), section, no, f"{asset_id}.volume"),
        fade_in=_float(item.get("fade_in", 0.0), section, no, f"{asset_id}.fade_in"),
        fade_out=_float(item.get("fade_out", 0.0), section, no, f"{asset_id}.fade_out"),
        mask=_normalize_mask(str(item.get("mask", ""))),
        blend_mode=str(item.get("blend_mode", "")),
        opacity=_float(item.get("opacity", 1.0), section, no, f"{asset_id}.opacity"),
        adjustments=adjustments,
        tags=tags,
        envelope=envelope,
        transform_scale=t_scale,
        transform_position=t_pos,
        tl_span=tl_span,
    )


def _ingest_masks(section: str, no: int, body: list[str], comp: Composition) -> None:
    for r in _as_dicts(section, no, body):
        missing = [k for k in ("id", "type", "target", "timeline") if not r.get(k)]
        if missing:
            raise CompositionFormatError(section, f"mask 缺字段 {missing}: {r.get('id', '?')}", no)
        tl = r["timeline"]
        if not isinstance(tl, (list, tuple)) or len(tl) != 2:
            raise CompositionFormatError(section, f"mask {r['id']}: timeline 必须是 [起, 止]", no)
        params_raw = r.get("params")
        if params_raw is not None and not isinstance(params_raw, dict):
            raise CompositionFormatError(section, f"mask {r['id']}: params 必须是 map", no)
        params: dict[str, object] = (
            cast("dict[str, object]", params_raw) if params_raw is not None else {}
        )
        t0 = _float(tl[0], section, no, f"mask.{r['id']}.timeline[0]")
        t1 = _float(tl[1], section, no, f"mask.{r['id']}.timeline[1]")
        comp.masks.append(
            Mask(
                id=str(r["id"]),
                type=str(r["type"]),
                target=str(r["target"]),
                timeline=(t0, t1),
                params={
                    str(k): _float(v, section, no, f"mask.{r['id']}.{k}") for k, v in params.items()
                },
            )
        )


def _ingest_subtitles(section: str, no: int, body: list[str], comp: Composition) -> None:
    for r in _as_dicts(section, no, body):
        missing = [k for k in ("start", "end", "text") if r.get(k) in (None, "")]
        if missing:
            raise CompositionFormatError(section, f"字幕缺字段 {missing}", no)
        style_id = str(r.get("style") or "")
        comp.subtitles.append(
            Subtitle(
                text=str(r["text"]),
                start=_float(r["start"], section, no, "subtitle.start"),
                end=_float(r["end"], section, no, "subtitle.end"),
                style_id=style_id,
            )
        )


def _ingest_subtitle_styles(section: str, no: int, body: list[str], comp: Composition) -> None:
    for r in _as_dicts(section, no, body):
        if not r.get("id"):
            raise CompositionFormatError(section, f"subtitle style 缺 id: {r!r}", no)
        st = SubtitleStyle(
            id=str(r["id"]),
            font=str(r.get("font", "")),
            font_size=_int(r.get("font_size", 48), section, no, f"style.{r['id']}.font_size"),
            primary_color=str(r.get("primary_color", "#FFFFFF")),
            outline_color=str(r.get("outline_color", "#000000")),
            outline_width=_int(
                r.get("outline_width", 3), section, no, f"style.{r['id']}.outline_width"
            ),
            blur=_float(r.get("blur", 0.5), section, no, f"style.{r['id']}.blur"),
            position=_vec2(r.get("position", [0.5, 0.88]), section, no, f"style.{r['id']}.position")
            or (0.5, 0.88),
            alignment=str(r.get("alignment", "center")),
            animation=str(r.get("animation", "")),
            margin_bottom=_int(
                r.get("margin_bottom", 0), section, no, f"style.{r['id']}.margin_bottom"
            ),
            line_spacing=_float(
                r.get("line_spacing", 1.0), section, no, f"style.{r['id']}.line_spacing"
            ),
            max_width=_int(r.get("max_width", 0), section, no, f"style.{r['id']}.max_width"),
        )
        comp.subtitle_styles[st.id] = st


def _ingest_keyframes(section: str, no: int, body: list[str], comp: Composition) -> None:
    for r in _as_dicts(section, no, body):
        if not r.get("target") or not r.get("property"):
            raise CompositionFormatError(section, f"keyframe 缺 target/property: {r!r}", no)
        vals_raw = r.get("keyframes")
        if not isinstance(vals_raw, list) or not vals_raw:
            raise CompositionFormatError(
                section, f"keyframe target={r.get('target')}: 缺 keyframes 列表", no
            )
        values: list[PropertyKeyframe] = []
        for v in list(vals_raw):
            if not isinstance(v, dict) or "time" not in v or "value" not in v:
                raise CompositionFormatError(
                    section,
                    f"keyframe target={r.get('target')}: 项缺 time/value: {v!r}",
                    no,
                )
            kv: dict[str, object] = cast("dict[str, object]", v)
            values.append(
                PropertyKeyframe(
                    time=_float(kv["time"], section, no, "kf.time"),
                    value=kv["value"],
                    easing=str(kv.get("easing", "linear")),
                )
            )
        comp.keyframe_specs.append(
            KeyframeSpec(
                target=str(r["target"]),
                property=str(r["property"]),
                values=values,
            )
        )


# ── 分发：masks / keyframes → segments ─────────────────────


def _distribute_masks(comp: Composition) -> None:
    segs_by_asset: dict[str, list[Segment]] = {}
    for t in comp.tracks:
        for s in t.segments:
            segs_by_asset.setdefault(s.asset_id, []).append(s)
    for m in comp.masks:
        for s in segs_by_asset.get(m.target, []):
            if s.tl_start < m.timeline[1] and m.timeline[0] < s.tl_end:
                s.mask = _mask_to_str(m)


def _mask_to_str(m: Mask) -> str:
    p = m.params
    if m.type == "circle":
        cx = p.get("cx", 0.5)
        cy = p.get("cy", 0.5)
        size = p.get("radius", p.get("size", 0.3)) * 2  # mask_png: size=直径比例
        return f"circle({cx},{cy},{size},feather={p.get('feather', 0.0)})"
    # linear: 由 (x0,y0)→(x1,y1) 推中心 + 方向角（度）
    x0, y0 = p.get("x0", 0.0), p.get("y0", 1.0)
    x1, y1 = p.get("x1", 1.0), p.get("y1", 0.0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rot = math.degrees(math.atan2(y1 - y0, x1 - x0))
    return f"linear({cx},{cy},{rot},feather={p.get('feather', 0.1)})"


_EASING_MAP = {
    "linear": "linear",
    "ease_in": "ease-in",
    "ease_out": "ease-out",
    "ease_in_out": "ease-in-out",
    "ease_in_cubic": "ease-in",
    "ease_out_cubic": "ease-out",
}


def _distribute_keyframes(comp: Composition) -> None:
    segs_by_asset: dict[str, list[Segment]] = {}
    for t in comp.tracks:
        for s in t.segments:
            segs_by_asset.setdefault(s.asset_id, []).append(s)
    for spec in comp.keyframe_specs:
        for s in segs_by_asset.get(spec.target, []):
            span = s.tl_end - s.tl_start
            for kf in spec.values:
                at = kf.time - s.tl_start
                if at < -1e-3 or at > span + 1e-3:
                    continue  # 该关键帧不在这个段的时间窗口内
                easing = _EASING_MAP.get(kf.easing, "linear")
                if (
                    spec.property == "scale"
                    and isinstance(kf.value, (list, tuple))
                    and len(kf.value) >= 1
                ):
                    s.keyframes.append(
                        Keyframe(
                            at=at,
                            scale=_float(kf.value[0], "keyframes", 0, f"{spec.target}.scale[0]"),
                            easing=easing,
                        )
                    )
                elif spec.property == "rotation":
                    try:
                        rot = _float(kf.value, "keyframes", 0, f"{spec.target}.value")
                    except CompositionFormatError:
                        continue
                    s.keyframes.append(Keyframe(at=at, rotation=rot, easing=easing))
                # position: 像素偏移语义与旧 Keyframe 不同，暂不入段（引擎轨道级消费）


# ── 校验 ──────────────────────────────────────────────────


def _validate(comp: Composition) -> None:
    for t in comp.tracks:
        for s in t.segments:
            a = comp.asset_by_id(s.asset_id)
            if a is None:
                raise CompositionFormatError(
                    f"track: {t.id}",
                    f"段引用了不存在的 asset: '{s.asset_id}'",
                    0,
                )
            if a.type not in ("video", "image", "texture", "animation") and t.type == "video":
                raise CompositionFormatError(
                    f"track: {t.id}",
                    f"段 {s.asset_id} 的 asset 类型 '{a.type}' 不可用于 video 轨",
                    0,
                )
    if not comp.tracks:
        raise CompositionFormatError("", "没有任何 ## Track 节 — 没有可渲染的轨")
    if not any(t.segments for t in comp.tracks):
        raise CompositionFormatError("", "所有 track 都没有 segments — 没有可渲染的内容")
    # 字幕 style 引用必须存在
    for sub in comp.subtitles:
        if sub.style_id and sub.style_id not in comp.subtitle_styles:
            raise CompositionFormatError(
                "subtitles",
                f"字幕引用了未定义的 style: '{sub.style_id}'",
                0,
            )
    # keyframe target 必须是 asset 或 segment
    valid_targets = {a.id for a in comp.assets} | {s.id for t in comp.tracks for s in t.segments}
    for spec in comp.keyframe_specs:
        if spec.target not in valid_targets:
            raise CompositionFormatError(
                "keyframes",
                f"keyframe target 不存在: '{spec.target}'",
                0,
            )
    for m in comp.masks:
        if m.target not in {a.id for a in comp.assets}:
            raise CompositionFormatError("masks", f"mask {m.id} 的 target 不存在: '{m.target}'", 0)


# ── helpers ────────────────────────────────────────────────


def _clean(body: list[str], strip_groups: bool = False) -> list[str]:
    """去掉 --- 分隔线；strip_groups=True 时去掉 ### 组标题（在 YAML 流里是注释）。"""
    out: list[str] = []
    for ln in body:
        s = ln.strip()
        if s == "---":
            continue
        if strip_groups and s.startswith("### "):
            continue
        out.append(ln)
    return out


def _drop_prose(lines: list[str]) -> list[str]:
    """去掉顶层散文行（无冒号、非列表项）——agent 在节里写的说明段落。"""
    out: list[str] = []
    for ln in lines:
        s = yamlmini.strip_comment(ln).strip()
        if not s:
            out.append(ln)
            continue
        if yamlmini.line_indent(ln) == 0 and not s.startswith("-") and ":" not in s:
            continue
        out.append(ln)
    return out


def _as_dicts(section: str, no: int, body: list[str]) -> list[dict[str, object]]:
    """解析一节的列表项 → dict 列表（容忍顶层散文行）。"""
    lines = _drop_prose(_clean(body))
    try:
        items = yamlmini.parse_block(lines, start_line_no=no)
    except YamlMiniError as e:
        raise CompositionFormatError(section, f"YAML 解析失败: {e}", no + e.line_no) from e
    out: list[dict[str, object]] = []
    for it in items:
        if isinstance(it, dict):
            out.append(it)
        elif it is not None:
            raise CompositionFormatError(section, f"期望 dict 列表项，实际标量: {it!r}", no)
    return out


def _parse_doc(lines: list[str], no: int) -> tuple[dict[str, object], int]:
    """解析顶层 dict（track body）。"""
    j = 0
    while j < len(lines) and not yamlmini.strip_comment(lines[j]).strip():
        j += 1
    if j >= len(lines):
        return {}, j
    try:
        return parse_doc(lines, j, yamlmini.line_indent(lines[j]), no)
    except YamlMiniError as e:
        raise CompositionFormatError("track", f"YAML 解析失败: {e}", no + e.line_no) from e


def _float(v: object, section: str, no: int, what: str) -> float:
    if isinstance(v, bool):
        raise CompositionFormatError(section, f"{what} 不是数字: {v!r}", no)
    if isinstance(v, int | float):
        try:
            return float(v)
        except (TypeError, ValueError) as e:
            raise CompositionFormatError(section, f"{what} 不是数字: {v!r}", no) from e
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError as e:
            raise CompositionFormatError(section, f"{what} 不是数字: {v!r}", no) from e
    raise CompositionFormatError(section, f"{what} 不是数字: {v!r}", no)


def _int(v: object, section: str, no: int, what: str) -> int:
    if isinstance(v, bool):
        raise CompositionFormatError(section, f"{what} 不是整数: {v!r}", no)
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        try:
            return int(v) if v.is_integer() else (_fail_int(v, section, no, what))
        except (TypeError, ValueError, OverflowError) as e:
            raise CompositionFormatError(section, f"{what} 不是整数: {v!r}", no) from e
    if isinstance(v, str):
        try:
            return int(v)
        except ValueError as e:
            raise CompositionFormatError(section, f"{what} 不是整数: {v!r}", no) from e
    raise CompositionFormatError(section, f"{what} 不是整数: {v!r}", no)


def _fail_int(v: object, section: str, no: int, what: str) -> int:
    raise CompositionFormatError(section, f"{what} 不是整数: {v!r}", no)


def _vec2(v: object, section: str, no: int, what: str) -> tuple[float, float] | None:
    if v is None:
        return None
    if not isinstance(v, (list, tuple)) or len(v) != 2:
        raise CompositionFormatError(section, f"{what} 必须是 [x, y]: {v!r}", no)
    return (_float(v[0], section, no, what + "[0]"), _float(v[1], section, no, what + "[1]"))


def _normalize_mask(mask: str) -> str:
    if not mask or mask in ("—", "-", "--", "none", ""):
        return ""
    if "(" in mask:
        return mask
    for mtype in ("circle", "linear"):
        if mask.startswith(mtype + ":"):
            return f"{mtype}({mask[len(mtype) + 1 :]})"
    return mask
