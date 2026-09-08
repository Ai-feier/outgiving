"""YAML 子集解析器（零新依赖）—— 只覆盖 agent 实际写 composition.md 的形状。

支持：
- 缩进字典（2 空格层级）：嵌套 key: value
- 列表项：``- key: value``（首 key 内联）与 ``- <标量>``
- 列表项内联多 kv：``- time: 0.0, volume: 0.0`` → {"time": 0.0, "volume": 0.0}
- flow 列表 ``[a, b]`` / flow map ``{k: v, k2: v2}``（单层）
- 标量：str（带/不带引号）/ int / float / bool（true|false）/ null（null|~|空）
- 整行 ``#`` 注释与行尾注释（引号外）；``###`` 组标题行视为分隔（上层 split_blocks 处理）

不支持（agent 形状之外）：多行字符串（| >）、锚点/引用（& *）、嵌套 flow、行内缩进字典。
形状越界 → 抛 YamlMiniError（带行号），不静默丢段。
"""

from __future__ import annotations

import re

Scalar = "str | int | float | bool | None"


class YamlMiniError(ValueError):
    """YAML 子集解析错误（带 1-based 行号）。"""

    def __init__(self, msg: str, line_no: int) -> None:
        super().__init__(f"line {line_no}: {msg}")
        self.line_no = line_no


def parse_block(lines: list[str], start_line_no: int = 1) -> list[object]:
    """解析一个 YAML 块（一个列表，或标量序列）→ 值列表。

    空块 → []。块内只允许列表项 + 嵌套内容；顶层非列表内容 → 报错（agent 形状约束）。
    """
    items, _ = _parse_list(lines, 0, 0, start_line_no)
    return items


def split_blocks(body: str) -> list[tuple[str, list[str]]]:
    """按 ``### `` 组标题切块 → [(组名, 块行)]。

    无 ``###`` 的 body → [("", 全行)]。组名保留原样（Assets 里 = 素材类型，
    Track 里 = 章节注释组，由调用方按节语义决定用不用）。
    """
    lines = body.split("\n")
    blocks: list[tuple[str, list[str]]] = []
    name = ""
    cur: list[str] = []
    for ln in lines:
        if ln.strip().startswith("### "):
            if name or cur:
                blocks.append((name, cur))
            name = ln.strip()[4:].strip()
            cur = []
        else:
            cur.append(ln)
    if name or cur:
        blocks.append((name, cur))
    return blocks


def strip_comment(s: str) -> str:
    """去掉引号外的行尾注释（公开 API）。"""
    return _strip_comment(s)


def line_indent(line: str) -> int:
    """行首空格数（公开 API）。"""
    return _indent(line)


def parse_doc(
    lines: list[str], start: int, indent: int, line_no_base: int
) -> tuple[dict[str, object], int]:
    """解析顶层 dict 块（如 track body）→ (dict, 下一行下标)（公开 API）。"""
    return _parse_dict_block(lines, start, indent, line_no_base)


# ── 内部 ────────────────────────────────────────────────────

_FLOWS = re.compile(r"^(\[.+\]|\{.+\})$")


def _scalar(tok: str) -> object:
    t = tok.strip()
    if t == "" or t in ("null", "~"):
        return None
    if t.startswith('"') and t.endswith('"') and len(t) >= 2:
        return t[1:-1]
    if t.startswith("'") and t.endswith("'") and len(t) >= 2:
        return t[1:-1]
    if t.lower() in ("true", "false"):
        return t.lower() == "true"
    try:
        return int(t)
    except ValueError:
        pass
    try:
        return float(t)
    except ValueError:
        pass
    return t


def _strip_comment(s: str) -> str:
    """去掉引号外的行尾注释。"""
    out: list[str] = []
    in_q: str | None = None
    for i, ch in enumerate(s):
        if in_q:
            out.append(ch)
            if ch == in_q:
                in_q = None
            continue
        if ch in ('"', "'"):
            in_q = ch
            out.append(ch)
            continue
        if ch == "#" and (i == 0 or s[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def _split_flow(inner: str) -> list[str]:
    parts: list[str] = []
    depth = 0
    in_q: str | None = None
    cur = ""
    for ch in inner:
        if in_q:
            cur += ch
            if ch == in_q:
                in_q = None
            continue
        if ch in ('"', "'"):
            in_q = ch
            cur += ch
            continue
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


def _parse_flow(tok: str, line_no: int) -> object:
    t = tok.strip()
    if t.startswith("[") and t.endswith("]"):
        inner = t[1:-1]
        if not inner.strip():
            return []
        return [
            _parse_flow(p, line_no) if _FLOWS.match(p.strip()) else _scalar(p)
            for p in _split_flow(inner)
        ]
    if t.startswith("{") and t.endswith("}"):
        inner = t[1:-1]
        if not inner.strip():
            return {}
        out: dict[str, object] = {}
        for p in _split_flow(inner):
            if ":" not in p:
                raise YamlMiniError(f"flow map 缺冒号: {p!r}", line_no)
            k, v = p.split(":", 1)
            out[k.strip()] = _scalar(v)
        return out
    return _scalar(t)


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _parse_list(
    lines: list[str], i: int, indent: int, line_no_base: int
) -> tuple[list[object], int]:
    """从 lines[i] 起解析缩进为 indent 的列表；返回 (值列表, 下一行下标)。"""
    items: list[object] = []
    n = len(lines)
    while i < n:
        raw = lines[i]
        stripped = _strip_comment(raw)
        if not stripped.strip():
            i += 1
            continue
        ind = _indent(raw)
        if ind < indent:
            break
        if ind > indent:
            raise YamlMiniError(
                f"缩进异常（期望 {indent} 空格，实际 {ind}）: {raw.strip()!r}",
                line_no_base + i,
            )
        s = stripped.strip()
        if not s.startswith("-"):
            if items:
                break  # 列表结束（如尾随 meta 行）
            raise YamlMiniError(f"期望列表项（- 开头），实际: {s!r}", line_no_base + i)
        rest = s[1:]
        if not rest.strip():
            items.append(None)
            i += 1
            continue
        # 首 key 行：`- key: value` 或 `- <标量>` 或 `- key:  (嵌套块)`
        m = re.match(r"^([^\s:][^:]*):(.*)$", rest.strip())
        if m:
            key = m.group(1).strip()
            val_raw = m.group(2).strip()
            d: dict[str, object] = {}
            if val_raw and _FLOWS.match(val_raw):
                d[key] = _parse_flow(val_raw, line_no_base + i)
            elif val_raw and "," in val_raw and _is_value_then_kv(val_raw):
                _fill_value_then_kv(d, key, val_raw, line_no_base + i)
            elif val_raw:
                d[key] = _scalar(val_raw)
            i += 1
            # 后续更深的 key（同项嵌套）
            key_ind: int | None = None
            while i < n:
                raw2 = lines[i]
                stripped2 = _strip_comment(raw2)
                if not stripped2.strip():
                    i += 1
                    continue
                ind2 = _indent(raw2)
                if ind2 < indent + 1:
                    break
                s2 = stripped2.strip()
                if s2.startswith("- ") and ind2 == indent + 1 and key == _first_key_name(s2[2:]):
                    # 嵌套列表挂在当前 key 下（key: 后空值）
                    vals, i = _parse_list(lines, i, indent + 1, line_no_base)
                    d.setdefault(key, vals)
                    continue
                if key_ind is None:
                    key_ind = ind2
                elif ind2 != key_ind:
                    raise YamlMiniError(
                        f"缩进异常（期望 {key_ind} 空格，实际 {ind2}）: {s2!r}",
                        line_no_base + i,
                    )
                m2 = re.match(r"^([^\s:][^:]*):(.*)$", s2)
                if not m2:
                    raise YamlMiniError(f"期望 'key: value'，实际: {s2!r}", line_no_base + i)
                k2, v2 = m2.group(1).strip(), m2.group(2).strip()
                i += 1
                if v2:
                    d[k2] = (
                        _parse_flow(v2, line_no_base + i - 1) if _FLOWS.match(v2) else _scalar(v2)
                    )
                else:
                    # key 后无值 → 嵌套字典或嵌套列表
                    j = i
                    while j < n and not _strip_comment(lines[j]).strip():
                        j += 1
                    if j < n and _indent(lines[j]) > ind2:
                        if _strip_comment(lines[j]).strip().startswith("- "):
                            vals, i = _parse_list(lines, j, _indent(lines[j]), line_no_base)
                            d[k2] = vals
                        else:
                            child, i = _parse_dict_block(lines, j, _indent(lines[j]), line_no_base)
                            d[k2] = child
                    else:
                        d[k2] = None
            items.append(d)
        else:
            # 标量列表项或内联多 kv：`- time: 0.0, volume: 0.0`
            s_norm = rest.strip()
            if re.match(r"^[^\s:][^:]*: ", s_norm) and "," in s_norm:
                d = {}
                for p in _split_flow(s_norm):
                    if ":" not in p:
                        raise YamlMiniError(f"内联 kv 段缺冒号: {p!r}", line_no_base + i)
                    k, v = p.split(":", 1)
                    v = v.strip()
                    d[k.strip()] = (
                        _parse_flow(v, line_no_base + i) if _FLOWS.match(v) else _scalar(v)
                    )
                items.append(d)
            else:
                items.append(
                    _parse_flow(s_norm, line_no_base + i)
                    if _FLOWS.match(s_norm)
                    else _scalar(s_norm)
                )
            i += 1
    return items, i


def _first_key_name(s: str) -> str:
    m = re.match(r"^([^\s:][^:]*):", s)
    return m.group(1).strip() if m else ""


def _is_value_then_kv(v: str) -> bool:
    """'0.0, y0: 1.0' — 首段是值（无冒号），后续段全是 k: v。"""
    parts = _split_flow(v)
    return (
        len(parts) >= 2
        and ":" not in parts[0]
        and all(re.match(r"^[^\s:][^:]*:", p.strip()) for p in parts[1:])
    )


def _fill_value_then_kv(d: dict[str, object], k: str, v: str, line_no: int) -> None:
    """'k: 0.0, k2: 1.0' → d[k]=0.0, d[k2]=1.0。"""
    parts = _split_flow(v)
    p0 = parts[0].strip()
    d[k] = _parse_flow(p0, line_no) if _FLOWS.match(p0) else _scalar(p0)
    for p in parts[1:]:
        k2, v2 = p.split(":", 1)
        v2 = v2.strip()
        d[k2.strip()] = _parse_flow(v2, line_no) if _FLOWS.match(v2) else _scalar(v2)


def _parse_dict_block(
    lines: list[str], i: int, indent: int, line_no_base: int
) -> tuple[dict[str, object], int]:
    """解析一个纯字典块（无 - 列表项）→ (dict, 下一行下标)。"""
    out: dict[str, object] = {}
    n = len(lines)
    while i < n:
        raw = lines[i]
        stripped = _strip_comment(raw)
        if not stripped.strip():
            i += 1
            continue
        ind = _indent(raw)
        if ind < indent:
            break
        s = stripped.strip()
        m = re.match(r"^([^\s:][^:]*):(.*)$", s)
        if not m:
            raise YamlMiniError(f"期望 'key: value'，实际: {s!r}", line_no_base + i)
        k, v = m.group(1).strip(), m.group(2).strip()
        i += 1
        if v:
            if _FLOWS.match(v):
                out[k] = _parse_flow(v, line_no_base + i - 1)
            elif "," in v and _is_value_then_kv(v):
                _fill_value_then_kv(out, k, v, line_no_base + i - 1)
            else:
                out[k] = _scalar(v)
        else:
            j = i
            while j < n and not _strip_comment(lines[j]).strip():
                j += 1
            if j < n and _indent(lines[j]) > ind:
                if _strip_comment(lines[j]).strip().startswith("- "):
                    out[k], i = _parse_list(lines, j, _indent(lines[j]), line_no_base)
                else:
                    out[k], i = _parse_dict_block(lines, j, _indent(lines[j]), line_no_base)
            else:
                out[k] = None
    return out, i
