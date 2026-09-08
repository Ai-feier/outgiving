"""生产链解析与写回 —— 单元文件模型（frontmatter 即链）。

项目目录顶层每个带 frontmatter ``unit:`` 的 .md 即一个链节点（一个单元一份文件）：

    ---
    unit: director          # 链节点 id（项目内唯一）
    层: l1                  # 所属层（可选；缺省 = default 层；遗留 段: 只读兼容）
    title: 导演收口          # 展示名（可选，默认 = unit）
    follows: [script, visual, rhythm]  # 上游单元（可多、可跨层，前置统一 D39）
    gate: 是                # 可选，单元门
    ---
    # 显示标题
    ## ① 简层      人话：是什么、要什么感觉（人写或 AI 起草）
    ## ② 思考      agent 怎么想的：过程说明（可 grill）
    ## ③ 内容详情   交付物本身 / 完整提示词
    ## ④ 执行      真正发出去的：工具调用记录 + Run 卡
    ## ⑤ 结果      指标 + 对齐自报 + 交接 + 门记录

遗留 4 节文件（## ③ 执行 / ## end 结果）只读兼容：③ 执行 → exec、end 结果 → result，
unit.legacy = True（层视图告警"旧 4 节格式，待迁移"）。
链序 = ``follows`` 拓扑序（前置统一：多前置、跨层边合法，D39）。
md 仍是唯一事实源，本模块只做扫描/解析/写回（expected_body 逐字校验防并发覆盖）。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# 5 层 H2 部分
CLAIM, THINKING, CONTENT, EXEC, RESULT = "claim", "thinking", "content", "exec", "result"
PART_ORDER = [CLAIM, THINKING, CONTENT, EXEC, RESULT]
_HEAD_LABEL = {
    CLAIM: "## ① 简层",
    THINKING: "## ② 思考",
    CONTENT: "## ③ 内容详情",
    EXEC: "## ④ 执行",
    RESULT: "## ⑤ 结果",
}
_LEGACY_PART = {EXEC: "## ③ 执行", RESULT: "## end 结果"}  # 遗留 4 节文件的建节标签

_FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
_SECTION_H2_RE = re.compile(r"^##\s+(①|②|③|④|⑤|end)\b")
_NUM_PART = {"①": CLAIM, "②": THINKING, "③": CONTENT, "④": EXEC, "⑤": RESULT}


def heading_to_part(line: str) -> tuple[str, bool] | None:
    """H2 行 → (part_key, 是否遗留格式)；非部分标题 → None。

    遗留判定：``## ③ 执行`` → exec、``## end 结果`` → result。
    """
    m = _SECTION_H2_RE.match(line)
    if not m:
        return None
    num = m.group(1)
    suffix = line[m.end() :].strip()
    if num == "③" and "执行" in suffix:
        return EXEC, True
    if num == "end":
        return RESULT, True
    part = _NUM_PART.get(num)
    if part is None:
        return None
    return part, False


def parse_frontmatter(text: str) -> tuple[dict[str, str | list[str]], str]:
    """拆 frontmatter（仅支持 ``k: v`` 与 ``k: [a, b]`` 两种行）→ (meta, 正文)。"""
    m = _FM_RE.match(text)
    if not m:
        return {}, text
    meta: dict[str, str | list[str]] = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            meta[k] = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        else:
            meta[k] = v
    return meta, text[m.end() :]


def parse_sections(body: str) -> tuple[dict[str, Section], bool]:
    """按 H2 编号切 5 部分；body 到下一个任意 H2 为止 → (parts, legacy)。"""
    lines = body.split("\n")
    heads: list[tuple[int, str]] = []
    legacy = False
    for i, ln in enumerate(lines):
        hp = heading_to_part(ln)
        if hp is None:
            continue
        part, is_legacy = hp
        legacy = legacy or is_legacy
        heads.append((i, part))
    out: dict[str, Section] = {}
    for sj, key in heads:
        s_start = sj + 1
        nxt = len(lines)
        for j in range(sj + 1, len(lines)):
            if lines[j].startswith("## "):
                nxt = j
                break
        out[key] = Section(key, "\n".join(lines[s_start:nxt]), s_start, nxt)
    return out, legacy


@dataclass
class Section:
    key: str
    body: str
    start: int  # 行号（body 首行，相对正文，0-based）
    end: int  # exclusive


# 单元状态（五态；H1 后 3 行内状态行解析，缺省 = 未开始）
STATES = ("未开始", "就绪", "运行中", "完成", "失败")
DEFAULT_STATE = "未开始"
_STATE_RE = re.compile(r"^>\s*状态[:：]\s*(\S+)")
_RUN_HEAD_RE = re.compile(r"^###\s+Run\s+(\d+)")

# ④ 执行层 exec-meta 默认值（单点：chain_assemble / /api/prompt-body 共用）
# ④ 执行层 exec-meta 默认值（单点：chain_assemble / /api/prompt-body 共用）
DEFAULT_PROVIDER = "autodl_comfyui"
DEFAULT_DURATION: int = 5
DEFAULT_RESOLUTION = "768p横"
EXEC_DEFAULTS: dict[str, str | int] = {
    "provider": DEFAULT_PROVIDER,
    "duration": DEFAULT_DURATION,
    "resolution": DEFAULT_RESOLUTION,
}


def _find_state_line(lines: list[str], h1: int) -> tuple[int | None, str | None]:
    """H1 后 3 行内（允许 1 个空行或空 blockquote 行）找状态行 → (行号, 原值)；无 → (None, None)。"""
    blanks = 0
    for j in range(h1 + 1, min(h1 + 4, len(lines))):
        ln = lines[j]
        if not ln.strip() or ln.strip() == ">":
            blanks += 1
            if blanks > 1:
                return None, None
            continue
        m = _STATE_RE.match(ln)
        return (j, m.group(1).strip()) if m else (None, None)
    return None, None


def parse_state(body: str) -> tuple[str, str]:
    """body 内解析状态 → (归一化五态, 原值)；无 H1 / 无状态行 → (未开始, "")。"""
    lines = body.split("\n")
    h1 = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
    if h1 is None:
        return DEFAULT_STATE, ""
    _idx, raw = _find_state_line(lines, h1)
    if raw is None:
        return DEFAULT_STATE, ""
    return (raw if raw in STATES else DEFAULT_STATE), raw


@dataclass
class Unit:
    unit: str
    title: str
    file: str  # 相对项目目录
    follows: list[str] = field(default_factory=list[str])
    parts: dict[str, Section] = field(default_factory=dict[str, Section])
    exec_meta: dict[str, str] = field(default_factory=dict[str, str])
    exec_body: str = ""  # ④执行去掉头部元数据行后的正文
    layer: str = "default"  # frontmatter `层:`（遗留 `段:` 只读兼容）；缺省 default
    gate: bool = False  # frontmatter `gate: 是`
    superseded_by: str = ""
    legacy: bool = False  # 旧 4 节格式（## ③ 执行 / ## end 结果）
    state: str = DEFAULT_STATE  # 归一化五态
    state_raw: str = ""  # 状态行原值（非法值保留）
    exec_kind: str = "design"  # "run"（④ 含 prompt-file 或 Run 卡）| "design"


@dataclass
class Chain:
    title: str
    units: list[Unit]
    order: list[str]  # 拓扑序（unit id）
    missing: list[str]  # follows 指向不存在的单元 id
    layers: list[dict[str, object]] = field(default_factory=list[dict[str, object]])
    layer_errors: list[str] = field(default_factory=list[str])


_META_LINE_RE = re.compile(r"^-\s+([a-z][\w-]*):\s*(.*)$")


def _extract_exec_meta(body: str) -> tuple[dict[str, str], str]:
    """从执行层正文头部抽 ``- key: value`` 元数据（允许前导空行）；返回 (meta, 剩余正文)。"""
    meta: dict[str, str] = {}
    lines = body.split("\n")
    n = 0
    while n < len(lines) and not lines[n].strip():
        n += 1
    while n < len(lines):
        m = _META_LINE_RE.match(lines[n])
        if not m:
            break
        meta[m.group(1)] = m.group(2).strip()
        n += 1
    return meta, "\n".join(lines[n:]).lstrip("\n")


def scan_units(project_dir: Path) -> Chain:
    """扫描项目目录顶层 .md，取带 ``unit:`` frontmatter 的文件为链节点，拓扑排序。

    同时解析：层（frontmatter ``层:``/遗留 ``段:``，缺省 default）、状态行（五态）、
    运行单元判定（④ 含 prompt-file 或 Run 卡 → run）。
    """
    units: list[Unit] = []
    for p in sorted(project_dir.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        if "unit" not in meta:
            continue
        uid = str(meta["unit"]).strip()
        follows = meta.get("follows") or []
        if isinstance(follows, str):
            follows = [follows]
        parts, legacy = parse_sections(body)
        exec_full = parts[EXEC].body if EXEC in parts else ""
        exec_meta, exec_rest = _extract_exec_meta(exec_full)
        h1 = next((ln[2:].strip() for ln in body.splitlines() if ln.startswith("# ")), "")
        title = str(meta.get("title", "")) or h1 or uid
        state, state_raw = parse_state(body)
        layer = str(meta.get("层", "")).strip() or str(meta.get("段", "")).strip() or "default"
        gate = str(meta.get("gate", "")).strip().lower() in ("是", "true", "yes")
        has_run_card = any(_RUN_HEAD_RE.match(ln) for ln in exec_full.split("\n"))
        units.append(
            Unit(
                uid,
                title,
                p.name,
                [str(x) for x in follows],
                parts,
                exec_meta,
                exec_rest,
                layer=layer,
                gate=gate,
                superseded_by=str(meta.get("superseded_by", "")).strip(),
                legacy=legacy,
                state=state,
                state_raw=state_raw,
                exec_kind="run" if ("prompt-file" in exec_meta or has_run_card) else "design",
            )
        )
    order = _topo_order(units)
    layers, layer_errors = _analyze_layers(units, order)
    return Chain("chain", units, order, _missing_refs(units), layers, layer_errors)


def _topo_order(units: list[Unit]) -> list[str]:
    """Kahn；同层按扫描序（文件名序）。环 → 剩余节点按扫描序兜底追加。"""
    known = {u.unit for u in units}
    indeg = {u.unit: 0 for u in units}
    deps: dict[str, list[str]] = {u.unit: [] for u in units}
    for u in units:
        for f in u.follows:
            if f in known:
                indeg[u.unit] += 1
                deps[f].append(u.unit)
    order: list[str] = []
    ready = [u.unit for u in units if indeg[u.unit] == 0]
    while ready:
        n = ready.pop(0)
        order.append(n)
        for d in deps[n]:
            indeg[d] -= 1
            if indeg[d] == 0:
                ready.append(d)
    for u in units:  # 环兜底
        if u.unit not in order:
            order.append(u.unit)
    return order


def _missing_refs(units: list[Unit]) -> list[str]:
    known = {u.unit for u in units}
    out: list[str] = []
    for u in units:
        for f in u.follows:
            if f not in known and f not in out:
                out.append(f)
    return out


def _analyze_layers(
    units: list[Unit], order: list[str]
) -> tuple[list[dict[str, object]], list[str]]:
    """层分析：层始（goal，层内入边 0，恰好 1）/层末（end，层内无后继，恰好 1），
    违规进 layer_errors；跨层前置不限（D39 前置统一）；层序按跨层边拓扑。"""
    by_id: dict[str, Unit] = {u.unit: u for u in units}
    groups: dict[str, list[str]] = {}
    for u in units:  # 扫描序（文件名序）保证层 id 顺序稳定
        groups.setdefault(u.layer, []).append(u.unit)

    starts: dict[str, set[str]] = {}
    ends: dict[str, set[str]] = {}
    errors: list[str] = []
    for lid, ids in groups.items():
        idset = set(ids)
        s = {uid for uid in ids if not (set(by_id[uid].follows) & idset)}
        followed = {f for uid in ids for f in by_id[uid].follows if f in idset}
        e = {uid for uid in ids if uid not in followed}
        starts[lid], ends[lid] = s, e
        if len(s) != 1:
            errors.append(f"层 {lid}：层始单元应为恰好 1 个，实际 {len(s)}（{sorted(s)}）")
        if len(e) != 1:
            errors.append(f"层 {lid}：层末单元应为恰好 1 个，实际 {len(e)}（{sorted(e)}）")

    # 层序：跨层边拓扑（任意跨层边合法，D39；去重边对）
    indeg = {lid: 0 for lid in groups}
    deps: dict[str, list[str]] = {lid: [] for lid in groups}
    seen: set[tuple[str, str]] = set()
    for u in units:
        for f in u.follows:
            if f not in by_id or by_id[f].layer == u.layer:
                continue
            key = (by_id[f].layer, u.layer)
            if key in seen:
                continue
            seen.add(key)
            indeg[u.layer] += 1
            deps[by_id[f].layer].append(u.layer)
    layer_order: list[str] = []
    ready = [lid for lid in groups if indeg[lid] == 0]
    while ready:
        n = ready.pop(0)
        layer_order.append(n)
        for d in deps[n]:
            indeg[d] -= 1
            if indeg[d] == 0:
                ready.append(d)
    for lid in groups:  # 环兜底
        if lid not in layer_order:
            layer_order.append(lid)

    out: list[dict[str, object]] = []
    for lid in layer_order:
        ids = groups[lid]
        idset = set(ids)
        s1 = next((uid for uid in order if uid in starts.get(lid, set())), "")
        e1 = next((uid for uid in order if uid in ends.get(lid, set())), "")
        lunits = [uid for uid in order if uid in idset]
        start_u = by_id.get(s1)
        plan = (
            parse_goal_plan(start_u.parts[CONTENT].body)
            if start_u and CONTENT in start_u.parts
            else []
        )
        out.append(
            {
                "id": lid,
                "title": start_u.title if start_u else lid,
                "units": lunits,
                "start": s1,
                "end": e1,
                "state": _layer_state(by_id, lunits, e1),
                "plan": plan,
                "legacy": any(by_id[x].legacy for x in lunits),
            }
        )
    return out, errors


def _layer_state(by_id: dict[str, Unit], units: list[str], end_uid: str) -> str:
    """层状态派生（DESIGN §2.5）：任一失败→失败；任一运行中→运行中；层末完成且全层无失败→完成；否则进行中。"""
    sts = [by_id[u].state for u in units]
    if "失败" in sts:
        return "失败"
    if "运行中" in sts:
        return "运行中"
    if end_uid and by_id[end_uid].state == "完成":
        return "完成"
    return "进行中"


def parse_goal_plan(content_body: str) -> list[dict[str, str]]:
    """goal ③ 单元计划表 → 行 [{unit, claim, agent, gate, order}]（无表 → []）。

    识别「计划单元」标记后的 GFM 表格（行首可缩进）；表头/分隔行跳过。
    """
    lines = content_body.split("\n")
    idx = next((i for i, ln in enumerate(lines) if "计划单元" in ln), None)
    if idx is None:
        return []
    rows: list[dict[str, str]] = []
    header_seen = False
    for ln in lines[idx + 1 :]:
        s = ln.strip()
        if s.startswith("## "):
            break
        if not s.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not header_seen:
            header_seen = True
            continue
        if all(not c or set(c) <= set("-: ") for c in cells):
            continue  # 分隔行
        if len(cells) >= 5 and cells[0] and cells[0] not in ("unit",):
            rows.append(
                {
                    "unit": cells[0],
                    "claim": cells[1],
                    "agent": cells[2],
                    "gate": cells[3],
                    "order": cells[4],
                }
            )
    return rows


class ChainMismatch(Exception):
    """单元内容已变（并发编辑），拒绝写入。"""


def get_unit(chain: Chain, unit_id: str) -> Unit | None:
    return next((u for u in chain.units if u.unit == unit_id), None)


def replace_section(path: Path, section_key: str, expected_body: str, new_body: str) -> None:
    """替换某单元文件某部分的 body。expected_body 必须与当前逐字一致（frontmatter 保留）。"""
    text = path.read_text()
    m = _FM_RE.match(text)
    prefix = text[: m.end()] if m else ""
    body = text[m.end() :] if m else text
    lines = body.split("\n")
    target = None
    for i, ln in enumerate(lines):
        hp = heading_to_part(ln)
        if hp is not None and hp[0] == section_key:
            target = i
            break
    if target is None:
        raise KeyError(f"section not found: {path.name}/{section_key}")
    s_start = target + 1
    s_end = next((j for j in range(s_start, len(lines)) if lines[j].startswith("## ")), len(lines))
    current = "\n".join(lines[s_start:s_end])
    if current != expected_body:
        raise ChainMismatch(f"section changed since load: {path.name}/{section_key}")
    new_body = new_body if new_body.endswith("\n") else new_body + "\n"
    path.write_text(prefix + "\n".join(lines[:s_start] + new_body.split("\n") + lines[s_end:]))


def set_state(path: Path, expected: str, new_state: str) -> None:
    """写单元状态行（H1 后 3 行内）。expected = 当前状态值（无状态行传 ""），
    逐字不匹配抛 ChainMismatch；无状态行时插到 H1 下一行。"""
    text = path.read_text(encoding="utf-8")
    m = _FM_RE.match(text)
    prefix = text[: m.end()] if m else ""
    blines = (text[m.end() :] if m else text).split("\n")
    h1 = next((i for i, ln in enumerate(blines) if ln.startswith("# ")), None)
    if h1 is None:
        raise ValueError(f"no H1 to anchor state line: {path.name}")
    idx, raw = _find_state_line(blines, h1)
    current = raw if raw is not None else ""
    if current != expected:
        raise ChainMismatch(
            f"state changed since load: {path.name}（当前 {current!r}，期望 {expected!r}）"
        )
    line = f"> 状态: {new_state}"
    if idx is not None:
        blines[idx] = line
    else:
        blines.insert(h1 + 1, line)
    path.write_text(prefix + "\n".join(blines), encoding="utf-8")


def next_run_no(text: str) -> int:
    """全文内 `### Run N` 最大值 + 1（无则 1）。

    扫全文而非仅 ④ 执行层：即使 Run 卡因外部工具误入其他小节，编号仍单调不撞。"""
    best = 0
    for ln in text.split("\n"):
        m = _RUN_HEAD_RE.match(ln)
        if m:
            try:
                best = max(best, int(m.group(1)))
            except ValueError:
                continue
    return best + 1


# ── Run 卡 / 门记录 / grill 条目：渲染 + 解析单一 owner（DESIGN §3.5/§3.6）─────
# 卡片形状只在这里定义：server 只传数据，改形状只动这里；parse_render 互为镜像（测试锁）。


@dataclass
class ExecMeta:
    """④ 执行层 `- key: value` 元数据的类型化视图；默认值与 EXEC_DEFAULTS 同源。"""

    raw: dict[str, str] = field(default_factory=dict[str, str])

    @property
    def provider(self) -> str:
        return self.raw.get("provider") or DEFAULT_PROVIDER

    @property
    def model(self) -> str:
        return self.raw.get("model", "")

    @property
    def duration(self) -> int:
        try:
            return int(self.raw.get("duration") or DEFAULT_DURATION)
        except (TypeError, ValueError):
            return DEFAULT_DURATION

    @property
    def resolution(self) -> str:
        return self.raw.get("resolution") or DEFAULT_RESOLUTION

    @property
    def prompt_file(self) -> str:
        return self.raw.get("prompt-file", "")

    @property
    def refs(self) -> list[str]:
        return [r.strip() for r in self.raw.get("refs", "").split(",") if r.strip()]


@dataclass
class RunCard:
    """④ 内一张 Run 卡（canonical：`### Run N · provider · ts · outcome` + kv + 一句话 [+ 详情]）。"""

    run_no: int
    provider: str
    ts: str
    outcome: str
    kv: dict[str, str] = field(default_factory=dict[str, str])
    oneline: str = ""
    detail: str = ""


# Run 卡 kv 行（中文键：时长/成本；model/task-id 为 ASCII）
_RUN_KV_RE = re.compile(r"^-\s+(model|task-id|时长|成本)\s*[:：]\s*(.*)$")


def render_run_card(
    run_no: int,
    provider: str,
    ts: str,
    outcome: str,
    model: str = "",
    taskid: str = "",
    duration: str = "",
    cost: str = "",
    oneline: str = "",
    detail: str = "",
) -> str:
    """Run 卡 canonical 渲染。空 kv 不占行；oneline/detail 缺失则省（与 2026-08-26 前已落盘卡片同形）。"""
    head = f"### Run {run_no} · {provider} · {ts} · {outcome}"
    kv = [
        f"- {k}: {v}"
        for k, v in (("model", model), ("task-id", taskid), ("时长", duration), ("成本", cost))
        if v
    ]
    parts = [head]
    if kv:
        parts.append("\n".join(kv))
    if oneline:
        parts.append(oneline)
    if detail:
        parts.append("**详情**\n" + detail)
    return "\n\n".join(parts)


def parse_run_cards(body: str) -> list[RunCard]:
    """解析文本内全部 Run 卡（④ 执行层或全文）；卡片边界 = 下一 `### Run` 或下一 H2。"""
    lines = body.split("\n")
    heads: list[tuple[int, re.Match[str]]] = []
    for i, ln in enumerate(lines):
        m = _RUN_HEAD_RE.match(ln)
        if m:
            heads.append((i, m))
    cards: list[RunCard] = []
    for n, (i, hm) in enumerate(heads):
        run_no = int(hm.group(1)) if hm.group(1).isdigit() else 0
        rest = lines[i][hm.end() :].strip().lstrip("·").strip()
        fields = [f.strip() for f in rest.split(" · ")] if rest else []
        provider = fields[0] if len(fields) > 0 else ""
        ts = fields[1] if len(fields) > 1 else ""
        outcome = fields[2] if len(fields) > 2 else ""
        end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        j = i + 1
        while j < end and not lines[j].startswith("## "):
            j += 1
        block = lines[i + 1 : min(end, j)]
        while block and not block[-1].strip():
            block.pop()
        kv: dict[str, str] = {}
        oneline_parts: list[str] = []
        detail_parts: list[str] = []
        in_detail = False
        for ln in block:
            if ln.strip() == "**详情**":
                in_detail = True
                continue
            mk = _RUN_KV_RE.match(ln)
            if mk and not in_detail:
                kv[mk.group(1)] = mk.group(2).strip()
                continue
            if ln.strip():
                (detail_parts if in_detail else oneline_parts).append(ln)
        cards.append(
            RunCard(
                run_no,
                provider,
                ts,
                outcome,
                kv,
                "\n".join(oneline_parts).strip(),
                "\n".join(detail_parts).strip(),
            )
        )
    return cards


@dataclass
class GateRecord:
    """⑤ 结果（或 goal ③）内一条门记录（canonical：`### 门 · 类型 · ts · 裁决 · 一句话`）。"""

    gtype: str
    ts: str
    verdict: str
    oneline: str


GATE_VERDICTS = ("批准", "打回", "已决策跳过")
_GATE_RE = re.compile(
    r"^###\s+门\s*·\s*(?P<g>[^·]+?)\s*·\s*(?P<ts>[^·]+?)\s*·\s"
    r"(?P<v>" + "|".join(GATE_VERDICTS) + r")\s*·\s*(?P<o>.*)$"
)


def render_gate_record(gtype: str, ts: str, verdict: str, oneline: str) -> str:
    return f"### 门 · {gtype} · {ts} · {verdict} · {oneline}"


def parse_gate_records(body: str) -> list[GateRecord]:
    out: list[GateRecord] = []
    for ln in body.split("\n"):
        m = _GATE_RE.match(ln)
        if m:
            out.append(GateRecord(m.group("g"), m.group("ts"), m.group("v"), m.group("o")))
    return out


def render_grill_entry(ts: str, text: str) -> str:
    """grill 条目 canonical（`- ts · user` + 缩进正文）。"""
    lines = [f"- {ts} · user"] + ["  " + ln for ln in text.split("\n")]
    return "\n".join(lines)


def _section_span(lines: list[str], section_key: str) -> tuple[int | None, int]:
    """H2 段在 lines 内的 (段内首行, 结束行 exclusive)；段不存在 → (None, len)。"""
    for i, ln in enumerate(lines):
        hp = heading_to_part(ln)
        if hp is not None and hp[0] == section_key:
            s = i + 1
            e = next((j for j in range(s, len(lines)) if lines[j].startswith("## ")), len(lines))
            return s, e
    return None, len(lines)


def append_block_to_section(path: Path, section_key: str, block_text: str) -> None:
    """append-only：把 block 追加到指定 H2 段尾（段不存在则建在文件尾；遗留文件用遗留标签）。"""
    text = path.read_text(encoding="utf-8")
    m = _FM_RE.match(text)
    prefix = text[: m.end()] if m else ""
    lines = (text[m.end() :] if m else text).split("\n")
    s, e = _section_span(lines, section_key)
    block_lines = block_text.rstrip("\n").split("\n")
    if s is None:
        legacy = any((hp := heading_to_part(ln)) is not None and hp[1] for ln in lines)
        label: str = (
            (_LEGACY_PART.get(section_key) or _HEAD_LABEL[section_key])
            if legacy
            else _HEAD_LABEL[section_key]
        )
        if lines and lines[-1].strip():
            lines.append("")
        lines = lines + [label] + block_lines
    else:
        ins = e
        while ins > s and not lines[ins - 1].strip():
            ins -= 1
        at = ins + 1  # 保留 1 行空行
        lines = lines[:at] + block_lines + lines[at:]
    path.write_text(prefix + "\n".join(lines), encoding="utf-8")


def append_thinking_grill(path: Path, entry_text: str) -> None:
    """append-only：把 grill 条目追加到 ② 段 `### grill 记录` 小节尾（小节不存在则先建）。"""
    text = path.read_text(encoding="utf-8")
    m = _FM_RE.match(text)
    prefix = text[: m.end()] if m else ""
    lines = (text[m.end() :] if m else text).split("\n")
    s, e = _section_span(lines, THINKING)
    entry_lines = entry_text.rstrip("\n").split("\n")
    if s is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines = lines + ["## ② 思考", "### grill 记录"] + entry_lines
    else:
        h3 = next((i for i in range(s, e) if lines[i].startswith("### grill 记录")), None)
        if h3 is None:
            ins = e
            while ins > s and not lines[ins - 1].strip():
                ins -= 1
            at = ins + 1
            lines = lines[:at] + ["### grill 记录"] + entry_lines + lines[at:]
        else:
            e3 = next(
                (
                    j
                    for j in range(h3 + 1, e)
                    if lines[j].startswith("### ") or lines[j].startswith("## ")
                ),
                e,
            )
            ins = e3
            while ins > h3 + 1 and not lines[ins - 1].strip():
                ins -= 1
            at = ins + 1
            lines = lines[:at] + entry_lines + lines[at:]
    path.write_text(prefix + "\n".join(lines), encoding="utf-8")


def parts_api(u: Unit) -> dict[str, dict[str, str]]:
    """供 API 序列化：{key: {body}}（5 层，存在的部分才返回）。"""
    return {k: {"body": u.parts[k].body} for k in PART_ORDER if k in u.parts}
