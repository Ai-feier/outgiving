"""workbench 生产链（单元 5 层 + 层模型 + 门 + 状态 + 运行卡）契约测试。

按 ai-video/DESIGN.md v4.1 §2/§3/§5 写（测试契约，不测实现快照）：
- GET  /api/chain：layers / layer_errors / units[].{layer, gate, legacy, state, exec_kind, parts(5)}
- POST /api/chain/part：{p, unit, part: claim|thinking|content|exec|result, expected_body, new_body} → 409 stale
- POST /api/chain/state：行级 expected + 409；缺状态行时 expected="" 插入 H1 下一行
- POST /api/chain/append：kind=run（④ 执行层 `### Run N`，服务端算号，全文扫描不撞号）
  / kind=grill（② `### grill 记录`）/ kind=gate（⑤ 结果 `### 门 · …`，verdict 校验）；幂等键 (p,unit,kind,idem)
- 遗留 4 节格式（## ③ 执行 / ## end 结果 + 段: 字段）只读兼容：legacy=True，exec→exec、end→result

运行方式：uv run --directory scripts pytest tests/test_workbench_chain.py -q
"""

import http.client
import json
import sys
import threading
from collections.abc import Callable
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from workbench import chain
from workbench import server as wb

J = dict[str, Any]  # JSON 对象

# 一次 API 调用：(method, path[, body]) → (HTTP 状态码, JSON dict)
API = Callable[..., tuple[int, J]]


# ── 夹具 ─────────────────────────────────────────────────────


@pytest.fixture()
def api(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """真实 workbench server（随机端口），PROJECTS_DIR 指向 tmp。返回 (call, projects_root)。"""
    monkeypatch.setattr(wb, "PROJECTS_DIR", tmp_path)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), wb.Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    port = httpd.server_address[1]

    def call(method: str, path: str, body: J | None = None) -> tuple[int, J]:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        if method == "GET":
            conn.request("GET", path)
        else:
            conn.request(
                method,
                path,
                body=json.dumps(body or {}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
        r = conn.getresponse()
        raw = r.read()
        conn.close()
        try:
            data: J = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            data = {}
        return r.status, data

    yield call, tmp_path
    httpd.shutdown()


def make_unit(
    unit: str,
    follows: list[str],
    layer: str | None,
    h1: str = "某单元",
    state_line: str | None = None,
    claim: str = "简层内容",
    thinking: str = "思考内容",
    content: str = "内容详情",
    exec_body: str = "- agent: test-agent",
    result_body: str = "结果内容",
    with_h1: bool = True,
    gate: bool = False,
    legacy: bool = False,
) -> str:
    """单元文件样板。legacy=True → 旧 4 节（③ 执行/end 结果 + 段: 字段）。"""
    fm = f"---\nunit: {unit}\nfollows: [{', '.join(follows)}]"
    if layer:
        fm += f"\n{'段' if legacy else '层'}: {layer}"
    if gate:
        fm += "\ngate: 是"
    fm += "\n---\n"
    lines: list[str] = []
    if with_h1:
        lines.append(f"# {h1}")
        lines.append("")
    if state_line is not None:
        lines.append(state_line)
        lines.append("")
    if legacy:
        lines += [
            "## ① 简层",
            claim,
            "",
            "## ② 思考",
            thinking,
            "",
            "## ③ 执行",
            exec_body,
            "",
            "## end 结果",
            result_body,
            "",
        ]
    else:
        lines += [
            "## ① 简层",
            claim,
            "",
            "## ② 思考",
            thinking,
            "",
            "## ③ 内容详情",
            content,
            "",
            "## ④ 执行",
            exec_body,
            "",
            "## ⑤ 结果",
            result_body,
            "",
        ]
    return fm + "\n".join(lines)


def build_layout(root: Path, project: str = "T099") -> Path:
    """l1（设计+seg1）/ l2（seg2+end）；goal2 跨层前置 [seg1, visual]（含非层始，D39 合法）。"""
    d = root / project
    d.mkdir(parents=True)
    files: dict[str, tuple[str, list[str]]] = {
        "goal": ("l1", []),
        "research": ("l1", ["goal"]),
        "script": ("l1", ["research"]),
        "visual": ("l1", ["script"]),
        "rhythm": ("l1", ["script", "visual"]),
        "director": ("l1", ["script", "visual", "rhythm"]),
        "seg1": ("l1", ["director"]),
        "goal2": ("l2", ["seg1", "visual"]),
        "seg2": ("l2", ["goal2"]),
        "end": ("l2", ["seg2"]),
    }
    for u, (layer, f) in files.items():
        if u == "seg1":
            exec_body = (
                "- agent: video-director\n"
                "- provider: autodl_comfyui\n"
                "- prompt-file: exec/video-prompt-h3.md\n"
            )
        else:
            exec_body = "- agent: script-designer"
        state = "> 状态: 完成" if layer == "l1" else None
        (d / f"{u}.md").write_text(
            make_unit(u, f, layer, h1=u, state_line=state, exec_body=exec_body),
            encoding="utf-8",
        )
    return d


def get_chain(call: API, project: str) -> J:
    st, d = call("GET", f"/api/chain?p={project}")
    assert st == 200, f"GET /api/chain 应 200：{d}"
    return d


def get_units(call: API, project: str) -> tuple[dict[str, J], J]:
    d = get_chain(call, project)
    return {u["unit"]: u for u in d["units"]}, d


def scan_state(call: API, root: Path, project: str, content: str, unit: str = "u1") -> J:
    """把 content 写成项目下唯一单元文件，返回其 /api/chain 单元对象。"""
    d = root / project
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{unit}.md").write_text(content, encoding="utf-8")
    units, _ = get_units(call, project)
    return units[unit]


def file_text(root: Path, project: str, unit: str) -> str:
    return (root / project / f"{unit}.md").read_text(encoding="utf-8")


# ── 1. 5 层解析与遗留兼容 ───────────────────────────────────


def test_five_parts_new_format(api: tuple[API, Path]):
    call, root = api
    d = root / "T099"
    d.mkdir()
    (d / "u1.md").write_text(
        make_unit("u1", [], "l1", exec_body="- prompt-file: exec/p.md", gate=True),
        encoding="utf-8",
    )
    units, _ = get_units(call, "T099")
    u = units["u1"]
    assert set(u["parts"].keys()) == {"claim", "thinking", "content", "exec", "result"}
    assert u["parts"]["content"]["body"].strip() == "内容详情"
    assert u["parts"]["exec"]["body"].startswith("- prompt-file:")
    assert u["exec_kind"] == "run"  # ④ 含 prompt-file
    assert u["gate"] is True
    assert u["legacy"] is False
    assert u["layer"] == "l1"


def test_legacy_four_section_compat(api: tuple[API, Path]):
    call, root = api
    d = root / "T099"
    d.mkdir()
    (d / "u1.md").write_text(
        make_unit(
            "u1",
            [],
            "p1",
            legacy=True,
            exec_body="- prompt-file: exec/p.md\n",
            result_body="交接说明",
        ),
        encoding="utf-8",
    )
    units, chain_d = get_units(call, "T099")
    u = units["u1"]
    # 旧 ③ 执行 → exec；旧 end 结果 → result；无 content
    assert set(u["parts"].keys()) == {"claim", "thinking", "exec", "result"}
    assert u["legacy"] is True
    assert u["exec_kind"] == "run"
    assert u["layer"] == "p1"  # 段: 只读兼容并入层
    layers = chain_d["layers"]
    assert len(layers) == 1 and layers[0]["legacy"] is True


def test_exec_kind_by_run_card(api: tuple[API, Path]):
    call, root = api
    d = root / "T099"
    d.mkdir()
    (d / "u1.md").write_text(
        make_unit(
            "u1", [], None, exec_body="无元数据\n\n### Run 1 · p · 2026-08-26 10:00 · 成功\n一句话"
        ),
        encoding="utf-8",
    )
    units, _ = get_units(call, "T099")
    assert units["u1"]["exec_kind"] == "run"  # ④ 含 Run 卡
    assert units["u1"]["layer"] == "default"  # 无层/段字段


# ── 2. 层模型 ───────────────────────────────────────────────


def test_layers_layout_a(api: tuple[API, Path]):
    call, root = api
    build_layout(root)
    d = get_chain(call, "T099")
    assert d["layer_errors"] == []
    layers = {L["id"]: L for L in d["layers"]}
    assert [L["id"] for L in d["layers"]] == ["l1", "l2"]  # 跨层边拓扑序
    assert layers["l1"]["start"] == "goal"
    assert layers["l1"]["end"] == "seg1"
    assert layers["l1"]["units"] == [
        "goal",
        "research",
        "script",
        "visual",
        "rhythm",
        "director",
        "seg1",
    ]
    assert layers["l2"]["start"] == "goal2"
    assert layers["l2"]["end"] == "end"
    # goal2 跨层前置 [seg1, visual]（含非层始 visual）→ D39 合法，无 error
    assert layers["l1"]["state"] == "完成"
    assert layers["l2"]["state"] == "进行中"


def test_layer_errors_two_starts_and_two_ends(api: tuple[API, Path]):
    call, root = api
    d = root / "T099"
    d.mkdir()
    (d / "a.md").write_text(make_unit("a", [], "l1"), encoding="utf-8")
    (d / "b.md").write_text(make_unit("b", [], "l1"), encoding="utf-8")  # 双始
    (d / "c.md").write_text(make_unit("c", ["a"], "l1"), encoding="utf-8")
    (d / "d.md").write_text(make_unit("d", ["b"], "l1"), encoding="utf-8")  # 双末
    d2 = get_chain(call, "T099")
    assert any("层始" in e for e in d2["layer_errors"])
    assert any("层末" in e for e in d2["layer_errors"])


def test_layer_state_failed_and_running(api: tuple[API, Path]):
    call, root = api
    d = root / "T099"
    d.mkdir()
    (d / "g.md").write_text(make_unit("g", [], "l1", state_line="> 状态: 完成"), encoding="utf-8")
    (d / "m.md").write_text(
        make_unit("m", ["g"], "l1", state_line="> 状态: 运行中"), encoding="utf-8"
    )
    d2 = get_chain(call, "T099")
    assert d2["layers"][0]["state"] == "运行中"
    (d / "m.md").write_text(
        make_unit("m", ["g"], "l1", state_line="> 状态: 失败"), encoding="utf-8"
    )
    d3 = get_chain(call, "T099")
    assert d3["layers"][0]["state"] == "失败"


def test_goal_plan_parsed(api: tuple[API, Path]):
    call, root = api
    d = root / "T099"
    d.mkdir()
    plan = (
        "- 计划单元：\n"
        "  | unit | ① 草案 | agent | gate | 顺序 |\n"
        "  | ---- | ------ | ----- | ---- | ---- |\n"
        "  | research | 找参考 | gather-expert | 是 | 1 |\n"
        "  | script | 写节拍 | script-designer | 否 | 2 |\n"
    )
    (d / "g.md").write_text(
        make_unit("g", [], "l1", content=plan),
        encoding="utf-8",
    )
    d2 = get_chain(call, "T099")
    plan_rows = d2["layers"][0]["plan"]
    assert [r["unit"] for r in plan_rows] == ["research", "script"]
    assert plan_rows[0]["agent"] == "gather-expert"


# ── 3. 状态解析（5 边界）────────────────────────────────────


def test_state_no_h1(api: tuple[API, Path]):
    call, root = api
    u = scan_state(call, root, "T099", "---\nunit: u1\n---\n无标题行\n## ① 简层\nx\n")
    assert u["state"] == "未开始"
    assert u["state_raw"] == ""


def test_state_no_line(api: tuple[API, Path]):
    call, root = api
    u = scan_state(call, root, "T099", "---\nunit: u1\n---\n# T\n\n正文\n")
    assert u["state"] == "未开始"


def test_state_normal(api: tuple[API, Path]):
    call, root = api
    u = scan_state(call, root, "T099", "---\nunit: u1\n---\n# T\n> 状态: 运行中\n\n正文\n")
    assert u["state"] == "运行中"
    assert u["state_raw"] == "运行中"


def test_state_fullwidth_colon(api: tuple[API, Path]):
    call, root = api
    u = scan_state(call, root, "T099", "---\nunit: u1\n---\n# T\n> 状态：完成\n\n正文\n")
    assert u["state"] == "完成"


def test_state_blank_line_and_sticky(api: tuple[API, Path]):
    call, root = api
    u = scan_state(call, root, "T099", "---\nunit: u1\n---\n# T\n\n> 状态: 就绪\n\n正文\n")
    assert u["state"] == "就绪"
    # 状态行前非空非状态行 → 停
    u2 = scan_state(call, root, "T099", "---\nunit: u1\n---\n# T\n> 说明: 备注\n> 状态: 就绪\n")
    assert u2["state"] == "未开始"


def test_state_invalid_value(api: tuple[API, Path]):
    call, root = api
    u = scan_state(call, root, "T099", "---\nunit: u1\n---\n# T\n> 状态: 乱态\n")
    assert u["state"] == "未开始"
    assert u["state_raw"] == "乱态"


def test_state_blank_blockquote_line_tolerated(api: tuple[API, Path]):
    """lint autofix 会在状态行上方插一行裸 `>`；解析须容忍。"""
    call, root = api
    u = scan_state(call, root, "T099", "---\nunit: u1\n---\n# T\n>\n> 状态: 完成\n")
    assert u["state"] == "完成"


# ── 4. 写回 ─────────────────────────────────────────────────


def test_state_write_success_and_conflict(api: tuple[API, Path]):
    call, root = api
    build_layout(root)
    st, _ = call(
        "POST",
        "/api/chain/state",
        {"p": "T099", "unit": "goal", "state": "运行中", "expected": "完成"},
    )
    assert st == 200
    st, _ = call(
        "POST",
        "/api/chain/state",
        {"p": "T099", "unit": "goal", "state": "失败", "expected": "完成"},
    )
    assert st == 409  # 已变
    st, _ = call(
        "POST",
        "/api/chain/state",
        {"p": "T099", "unit": "goal", "state": "乱态", "expected": "运行中"},
    )
    assert st == 400


def test_state_insert_when_missing(api: tuple[API, Path]):
    call, root = api
    build_layout(root)
    st, _ = call(
        "POST", "/api/chain/state", {"p": "T099", "unit": "seg2", "state": "就绪", "expected": ""}
    )
    assert st == 200
    assert "> 状态: 就绪" in file_text(root, "T099", "seg2")


def test_part_write_and_conflict(api: tuple[API, Path]):
    call, root = api
    build_layout(root)
    units, _ = get_units(call, "T099")
    cur = units["goal"]["parts"]["content"]["body"]
    st, _ = call(
        "POST",
        "/api/chain/part",
        {
            "p": "T099",
            "unit": "goal",
            "part": "content",
            "expected_body": cur,
            "new_body": "新内容详情\n",
        },
    )
    assert st == 200
    text = file_text(root, "T099", "goal")
    assert "## ③ 内容详情\n新内容详情" in text
    assert "> 状态: 完成" in text  # 状态行保留
    st, _ = call(
        "POST",
        "/api/chain/part",
        {"p": "T099", "unit": "goal", "part": "content", "expected_body": cur, "new_body": "x"},
    )
    assert st == 409
    st, _ = call(
        "POST",
        "/api/chain/part",
        {"p": "T099", "unit": "goal", "part": "bogus", "expected_body": "", "new_body": "x"},
    )
    assert st == 400


def test_part_write_legacy_exec_heading(api: tuple[API, Path]):
    """遗留文件 exec part 对应 `## ③ 执行` 标题，写回不得误伤。"""
    call, root = api
    d = root / "T099"
    d.mkdir()
    (d / "u1.md").write_text(
        make_unit("u1", [], "p1", legacy=True),
        encoding="utf-8",
    )
    units, _ = get_units(call, "T099")
    cur = units["u1"]["parts"]["exec"]["body"]
    st, _ = call(
        "POST",
        "/api/chain/part",
        {
            "p": "T099",
            "unit": "u1",
            "part": "exec",
            "expected_body": cur,
            "new_body": "- provider: x\n",
        },
    )
    assert st == 200
    text = file_text(root, "T099", "u1")
    assert "## ③ 执行\n- provider: x" in text
    assert "## end 结果" in text


# ── 5. Run 卡 / grill / 门 ──────────────────────────────────


def test_run_numbering_starts_at_one(api: tuple[API, Path]):
    call, root = api
    build_layout(root)
    st, body = call(
        "POST",
        "/api/chain/append",
        {
            "p": "T099",
            "unit": "seg1",
            "kind": "run",
            "provider": "autodl_comfyui",
            "oneline": "一句话结果",
            "idem": "r1",
        },
    )
    assert st == 200 and body["run_no"] == 1
    text = file_text(root, "T099", "seg1")
    assert "### Run 1 · autodl_comfyui" in text
    assert "一句话结果" in text


def test_run_numbering_follows_max(api: tuple[API, Path]):
    call, root = api
    build_layout(root)
    text = file_text(root, "T099", "seg1")
    text = text.replace(
        "## ④ 执行\n", "## ④ 执行\n### Run 3 · p · 2026-08-25 10:00 · 成功\n旧结果\n\n", 1
    )
    (root / "T099" / "seg1.md").write_text(text, encoding="utf-8")
    st, body = call(
        "POST",
        "/api/chain/append",
        {"p": "T099", "unit": "seg1", "kind": "run", "provider": "p", "oneline": "x", "idem": "r2"},
    )
    assert st == 200 and body["run_no"] == 4


def test_run_numbering_scans_whole_file(api: tuple[API, Path]):
    """Run 卡误入 ⑤ 时编号仍单调（全文扫描）。"""
    call, root = api
    build_layout(root)
    text = file_text(root, "T099", "seg1")
    text = text.replace(
        "## ⑤ 结果", "## ⑤ 结果\n### Run 7 · p · 2026-08-25 10:00 · 成功\n误入\n", 1
    )
    (root / "T099" / "seg1.md").write_text(text, encoding="utf-8")
    st, body = call(
        "POST",
        "/api/chain/append",
        {"p": "T099", "unit": "seg1", "kind": "run", "provider": "p", "oneline": "x", "idem": "r3"},
    )
    assert st == 200 and body["run_no"] == 8
    # 新卡落在 ④
    new_text = file_text(root, "T099", "seg1")
    i4 = new_text.index("## ④ 执行")
    i5 = new_text.index("## ⑤ 结果")
    assert new_text.index("### Run 8") > i4 and new_text.index("### Run 8") < i5


def test_run_append_preserves_frontmatter_and_state(api: tuple[API, Path]):
    call, root = api
    build_layout(root)
    call(
        "POST",
        "/api/chain/append",
        {"p": "T099", "unit": "seg1", "kind": "run", "provider": "p", "oneline": "x", "idem": "r4"},
    )
    text = file_text(root, "T099", "seg1")
    assert text.startswith("---\nunit: seg1")
    assert "> 状态: 完成" in text


def test_grill_append_creates_subsection(api: tuple[API, Path]):
    call, root = api
    build_layout(root)
    st, _ = call(
        "POST",
        "/api/chain/append",
        {"p": "T099", "unit": "script", "kind": "grill", "text": "为什么这么切？", "idem": "q1"},
    )
    assert st == 200
    text = file_text(root, "T099", "script")
    assert "### grill 记录" in text
    assert "为什么这么切？" in text
    # 第二次追加不重建小节
    st, _ = call(
        "POST",
        "/api/chain/append",
        {"p": "T099", "unit": "script", "kind": "grill", "text": "第二个问题", "idem": "q2"},
    )
    assert st == 200
    assert file_text(root, "T099", "script").count("### grill 记录") == 1
    assert "第二个问题" in file_text(root, "T099", "script")
    # 幂等：同 idem 60s 内 → dup
    st2, body2 = call(
        "POST",
        "/api/chain/append",
        {"p": "T099", "unit": "script", "kind": "grill", "text": "为什么这么切？", "idem": "q1"},
    )
    assert st2 == 200 and body2.get("dup") is True
    assert file_text(root, "T099", "script").count("为什么这么切？") == 1


def test_gate_append_to_result(api: tuple[API, Path]):
    call, root = api
    build_layout(root)
    st, _ = call(
        "POST",
        "/api/chain/append",
        {
            "p": "T099",
            "unit": "director",
            "kind": "gate",
            "verdict": "批准",
            "oneline": "设计对齐",
            "idem": "g1",
        },
    )
    assert st == 200
    text = file_text(root, "T099", "director")
    m = [l for l in text.splitlines() if l.startswith("### 门")]
    assert len(m) == 1
    assert m[0].startswith("### 门 · 单元门 · ") and m[0].endswith("· 批准 · 设计对齐")
    assert text.index(m[0]) > text.index("## ⑤ 结果")  # 落在 ⑤
    # 门记录追加后状态行/frontmatter 保留
    assert text.startswith("---\nunit: director")


def test_gate_verdict_required(api: tuple[API, Path]):
    call, root = api
    build_layout(root)
    st, _ = call(
        "POST",
        "/api/chain/append",
        {
            "p": "T099",
            "unit": "director",
            "kind": "gate",
            "verdict": "随便",
            "oneline": "x",
            "idem": "g2",
        },
    )
    assert st == 400
    st, _ = call(
        "POST",
        "/api/chain/append",
        {
            "p": "T099",
            "unit": "director",
            "kind": "gate",
            "verdict": "批准",
            "oneline": "",
            "idem": "g3",
        },
    )
    assert st == 400


def test_gate_append_legacy_creates_end_section(api: tuple[API, Path]):
    """遗留文件 ⑤ 不存在 → 按遗留标签 `## end 结果` 建节。"""
    call, root = api
    d = root / "T099"
    d.mkdir()
    (d / "u1.md").write_text(
        make_unit("u1", [], "p1", legacy=True, result_body=""), encoding="utf-8"
    )
    st, _ = call(
        "POST",
        "/api/chain/append",
        {
            "p": "T099",
            "unit": "u1",
            "kind": "gate",
            "verdict": "打回",
            "oneline": "参考不足",
            "idem": "g4",
        },
    )
    assert st == 200
    text = file_text(root, "T099", "u1")
    assert "### 门 · 单元门" in text and "打回" in text


# ── 7. chain 纯函数：Run 卡 / 门 / grill / ExecMeta（render/parse 单一 owner）──────


def test_render_parse_run_card_roundtrip():
    card = chain.render_run_card(
        2,
        "autodl_comfyui",
        "2026-08-26 19:43",
        "成功",
        model="h3",
        taskid="abc-123",
        duration="5s",
        cost="¥0.05",
        oneline="seg1 出片",
        detail="ffprobe 5.167s\n末帧稳定",
    )
    cards = chain.parse_run_cards(card)
    assert len(cards) == 1
    c = cards[0]
    assert (c.run_no, c.provider, c.ts, c.outcome) == (
        2,
        "autodl_comfyui",
        "2026-08-26 19:43",
        "成功",
    )
    assert c.kv == {"model": "h3", "task-id": "abc-123", "时长": "5s", "成本": "¥0.05"}
    assert c.oneline == "seg1 出片"
    assert "ffprobe" in c.detail and "末帧" in c.detail


def test_render_run_card_minimal_no_kv_or_detail():
    """空 kv/详情不占行（与已落盘旧卡片同形：head + 一句话）。"""
    card = chain.render_run_card(4, "probe", "2026-08-26 19:45", "成功", oneline="位置探针")
    lines = card.split("\n")
    assert lines[0] == "### Run 4 · probe · 2026-08-26 19:45 · 成功"
    assert (
        lines[-1] == "位置探针"
    )  # head + 空行 + oneline（canonical 固定空行分隔，与 append 后渲染一致）
    # 再解析回
    assert chain.parse_run_cards(card)[0].oneline == "位置探针"


def test_parse_run_cards_segregates_consecutive():
    """两张连续 Run 卡不串块（kv/oneline/detail 各归各卡）。"""
    body = "\n\n".join(
        [
            chain.render_run_card(1, "p", "2026-08-26 10:00", "成功", model="m1", oneline="第一次"),
            chain.render_run_card(2, "p", "2026-08-26 10:05", "失败", oneline="第二次失败"),
        ]
    )
    cards = chain.parse_run_cards(body)
    assert len(cards) == 2
    assert cards[0].run_no == 1 and cards[0].kv["model"] == "m1" and cards[0].oneline == "第一次"
    assert cards[1].run_no == 2 and cards[1].outcome == "失败" and cards[1].oneline == "第二次失败"


def test_gate_record_roundtrip():
    rec = chain.render_gate_record("单元门", "2026-08-26 20:00", "批准", "请求体 OK，放行")
    parsed = chain.parse_gate_records(rec)
    assert len(parsed) == 1
    g = parsed[0]
    assert (g.gtype, g.ts, g.verdict, g.oneline) == (
        "单元门",
        "2026-08-26 20:00",
        "批准",
        "请求体 OK，放行",
    )


def test_render_grill_entry_indents_body():
    entry = chain.render_grill_entry("2026-08-26 20:01", "为什么切这几个单元？\n第二行")
    lines = entry.split("\n")
    assert lines[0] == "- 2026-08-26 20:01 · user"
    assert lines[1] == "  为什么切这几个单元？"
    assert lines[2] == "  第二行"


def test_exec_meta_defaults_single_source():
    """空 meta → 默认值（provider/duration/resolution）与 EXEC_DEFAULTS 同源。"""
    m = chain.ExecMeta({})
    assert m.provider == chain.EXEC_DEFAULTS["provider"]
    assert m.duration == chain.EXEC_DEFAULTS["duration"] == 5
    assert m.resolution == chain.EXEC_DEFAULTS["resolution"]
    assert m.prompt_file == "" and m.model == "" and m.refs == []
    # 显式值覆盖；非法 duration 回落 5
    m2 = chain.ExecMeta({"provider": "seedance", "duration": "10", "refs": "a.jpg, b.png"})
    assert m2.provider == "seedance" and m2.duration == 10 and m2.refs == ["a.jpg", "b.png"]
    assert chain.ExecMeta({"duration": "abc"}).duration == 5
