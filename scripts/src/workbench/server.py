"""workbench server — 视频提示词工作台（标准库 ThreadingHTTPServer，零新依赖）。

定位：markdown 文件是唯一事实源（agent/CLI 照旧读写），web 是它的视图/编辑器/批注层。
- 看：块级渲染 md（设计四件套 + 单元链）
- 改：块级编辑写回 md（header 定址，body 逐字校验防并发覆盖）
- 门/门记录：append 进单元 ⑤ 结果（### 门 · …，DESIGN.md §3.6）
- 请求体层：复用 ai.providers 的 parse/build_request，看到的就是要发出去的
- 链：单元文件 frontmatter（unit/层/follows/gate）即链，无独立 chain.md——md 唯一事实源

API（JSON）:
  GET  /api/projects
  GET  /api/file?p=T005&f=video-prompt.md
  POST /api/file           {p, f, block_id, expected_body, new_body}
  GET  /api/prompt-body?p=&f=&provider=autodl_comfyui|seedance&duration=5&resolution=768p横&refs=url1,url2
  GET  /api/chain          {order, missing, layer_errors, layers, units(parts 5 层/gate/legacy)}
  GET  /api/chain/assemble?p=&unit=  运行单元 ④ 执行层的真实请求体 + 成本 + 命令
  POST /api/chain/part     {p, unit, part: claim|thinking|content|exec|result, expected_body, new_body} → 200/409
  POST /api/chain/state    {p, unit, state, expected}  → 200/409
  POST /api/chain/append   {p, unit, kind: run|grill|gate, idem, …}  → 200（幂等 60s）
静态:
  GET /           app.html
  GET /vendor/x   vendor 目录（marked.js 等）
"""

from __future__ import annotations

import json
import re
import threading
import time
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from workbench import assemble, chain, mdblocks

ROOT = Path(__file__).resolve().parents[3]  # .../outgiving
PROJECTS_DIR = ROOT / "ai-video" / "projects"
VENDOR_DIR = Path(__file__).parent / "vendor"

_MEDIA_CTYPE = {
    ".mp4": "video/mp4",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
}
PROJECT_RE = re.compile(r"^T\d{3}(-[\w-]+)?$")

# ── 并发写保护：per-file 锁（ThreadingHTTPServer 多线程写同文件串行化）──────────
_FILE_LOCKS: dict[str, threading.Lock] = {}
_LOCKS_GUARD = threading.Lock()


def _file_lock(path: Path) -> threading.Lock:
    key = str(path)
    with _LOCKS_GUARD:
        lk = _FILE_LOCKS.get(key)
        if lk is None:
            lk = threading.Lock()
            _FILE_LOCKS[key] = lk
        return lk


# ── append 幂等窗口（防双击双写；键 = (项目, 单元, kind, idem)，60s）──────
_IdemKey = tuple[str, str, str, str]
_IDEM_PENDING = object()
_IDEM: dict[_IdemKey, tuple[float, object]] = {}
_IDEM_GUARD = threading.Lock()
_IDEM_TTL = 60.0


def _idem_reserve(key: _IdemKey) -> tuple[bool, dict[str, object]]:
    """首次 → (False, {})；60s 内同键 → (True, 首次结果/dup 标记)。"""
    now = time.time()
    with _IDEM_GUARD:
        stale = [k for k, (ts, _) in _IDEM.items() if now - ts > _IDEM_TTL]
        for k in stale:
            del _IDEM[k]
        hit = _IDEM.get(key)
        if hit is not None and hit[1] is not _IDEM_PENDING:
            first = hit[1]
            if isinstance(first, dict):
                return True, {**first, "dup": True}
            return True, {"ok": True, "dup": True}
        if hit is not None:
            return True, {"ok": True, "dup": True}
        _IDEM[key] = (now, _IDEM_PENDING)
        return False, {}


def _idem_commit(key: _IdemKey, payload: dict[str, object]) -> None:
    with _IDEM_GUARD:
        _IDEM[key] = (time.time(), payload)


# ── 项目/文件访问 ────────────────────────────────────────────


def project_files(project: str) -> list[str]:
    d = PROJECTS_DIR / project
    if not d.is_dir():
        return []
    out: list[str] = []
    for p in sorted(d.rglob("*.md")):
        rel = p.relative_to(d).as_posix()
        out.append(rel)
    return out


def list_projects() -> list[dict[str, object]]:
    projects: list[dict[str, object]] = []
    for d in sorted(PROJECTS_DIR.iterdir()) if PROJECTS_DIR.is_dir() else []:
        if d.is_dir() and PROJECT_RE.match(d.name):
            projects.append({"id": d.name, "files": project_files(d.name)})
    return projects


def read_file(project: str, file: str) -> str:
    d = PROJECTS_DIR / project
    target = (d / file).resolve()
    if d.resolve() not in target.parents:
        raise PermissionError(f"path escape: {file}")
    if not target.is_file() or target.suffix != ".md":
        raise PermissionError(f"not a md file: {file}")
    return target.read_text(encoding="utf-8")


def write_file(project: str, file: str, content: str) -> None:
    d = PROJECTS_DIR / project
    target = (d / file).resolve()
    if d.resolve() not in target.parents:
        raise PermissionError(f"path escape: {file}")
    target.write_text(content, encoding="utf-8")


# ── 生产链（单元文件 frontmatter 即链） ─────────────────────────


def read_chain(project: str) -> chain.Chain:
    d = PROJECTS_DIR / project
    if not d.is_dir():
        raise FileNotFoundError(f"project not found: {project}")
    return chain.scan_units(d)


def _resolve_refs(raw: str, project_dir: Path) -> list[str] | None:
    refs = [r.strip() for r in raw.split(",") if r.strip()]
    if not refs:
        return None
    out: list[str] = []
    for r in refs:
        if r.startswith(("http://", "https://", "data:")):
            out.append(r)
            continue
        # 本地路径 → data URI，和 CLI 同一路径（预览 = 真请求）
        from ai._utils import image_to_data_uri

        p = (project_dir / r).resolve()
        if not p.is_file() or not str(p).startswith(str(project_dir.resolve())):
            raise FileNotFoundError(f"ref not found: {r}")
        out.append(image_to_data_uri(p))
    return out or None


def chain_assemble(project: str, unit_id: str) -> dict[str, object]:
    """装配某单元③执行层的请求体（复用 assemble，与 CLI 同套逻辑）。"""
    c = read_chain(project)
    u = chain.get_unit(c, unit_id)
    if u is None:
        raise KeyError(f"unit not found: {unit_id}")
    if chain.EXEC not in u.parts:
        raise PermissionError(f"unit has no 执行层（④）: {unit_id}")
    meta = chain.ExecMeta(u.exec_meta)
    prompt_file = meta.prompt_file
    if not prompt_file:
        return {
            "error": "③执行层未声明 prompt-file，无法装配（需 agent 在该层补 - prompt-file: ...）"
        }
    project_dir = PROJECTS_DIR / project
    content = read_file(project, prompt_file)
    provider = meta.provider
    duration = meta.duration
    resolution = meta.resolution
    try:
        refs = _resolve_refs(",".join(meta.refs), project_dir)
    except FileNotFoundError as e:
        return {"error": str(e)}
    result = assemble.assemble(
        content, provider, duration, resolution, refs, project_dir, prompt_file
    )
    result["unit_title"] = u.title
    return result


# ── HTTP 层 ─────────────────────────────────────────────────


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:  # 静默 access log
        pass

    def _json(self, code: int, payload: object) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict[str, object]:
        raw = self.headers.get("Content-Length", "0")
        try:
            length = int(raw)
        except (TypeError, ValueError):
            return {}
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {}

    def do_GET(self) -> None:
        url = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        try:
            if url.path in ("/", "/index.html"):
                self._serve_html(VENDOR_DIR.parent / "app.html")
            elif url.path.startswith("/vendor/"):
                self._serve_file(VENDOR_DIR / url.path[len("/vendor/") :])
            elif url.path == "/media" or url.path.startswith("/media/"):
                rel = q.get("rel", "") or url.path[len("/media/") :].lstrip("/")
                self._serve_media(q.get("p", ""), rel)
            elif url.path == "/api/projects":
                self._json(200, {"projects": list_projects()})
            elif url.path == "/api/file":
                content = read_file(q["p"], q["f"])
                blocks = [
                    {"id": b.id, "title": b.title, "level": b.level, "body": b.body}
                    for b in mdblocks.parse_blocks(content)
                ]
                self._json(200, {"path": q["f"], "content": content, "blocks": blocks})
            elif url.path == "/api/prompt-body":
                refs_raw = q.get("refs", "")
                refs = [r for r in refs_raw.split(",") if r] or None
                _dur_raw = q.get("duration")
                try:
                    _dur = int(_dur_raw) if _dur_raw else chain.DEFAULT_DURATION
                except (TypeError, ValueError):
                    _dur = chain.DEFAULT_DURATION
                result = assemble.assemble(
                    read_file(q["p"], q["f"]),
                    q.get("provider") or chain.DEFAULT_PROVIDER,
                    _dur,
                    q.get("resolution") or chain.DEFAULT_RESOLUTION,
                    refs,
                    PROJECTS_DIR / q["p"],
                    q["f"],
                )
                self._json(200, result)
            elif url.path == "/api/chain":
                self._serve_chain(q["p"])
            elif url.path == "/api/chain/assemble":
                self._json(200, chain_assemble(q["p"], q["unit"]))
            else:
                self._json(404, {"error": "not found"})
        except KeyError as e:
            self._json(400, {"error": f"missing param: {e}"})
        except PermissionError as e:
            self._json(403, {"error": str(e)})
        except FileNotFoundError:
            self._json(404, {"error": "file not found"})
        except Exception as e:  # noqa: BLE001
            self._json(500, {"error": f"{type(e).__name__}: {e}"})

    def do_POST(self) -> None:
        url = urlparse(self.path)
        try:
            data = self._body()
            if url.path == "/api/file":
                p, f = str(data["p"]), str(data["f"])
                with _file_lock((PROJECTS_DIR / p / f).resolve()):
                    content = read_file(p, f)
                    new_content = mdblocks.replace_block(
                        content,
                        str(data["block_id"]),
                        str(data["expected_body"]),
                        str(data["new_body"]),
                    )
                    write_file(p, f, new_content)
                blocks = [
                    {"id": b.id, "title": b.title, "level": b.level, "body": b.body}
                    for b in mdblocks.parse_blocks(new_content)
                ]
                self._json(200, {"ok": True, "content": new_content, "blocks": blocks})
            elif url.path == "/api/chain/part":
                p = str(data["p"])
                part = str(data["part"])
                if part not in chain.PART_ORDER:
                    self._json(
                        400,
                        {"error": f"unknown part: {part}（须 ∈ {'/'.join(chain.PART_ORDER)}）"},
                    )
                    return
                c = read_chain(p)
                u = chain.get_unit(c, str(data["unit"]))
                if u is None:
                    self._json(400, {"error": f"unit not found: {data['unit']}"})
                    return
                with _file_lock((PROJECTS_DIR / p / u.file).resolve()):
                    chain.replace_section(
                        PROJECTS_DIR / p / u.file,
                        part,
                        str(data["expected_body"]),
                        str(data["new_body"]),
                    )
                self._json(200, {"ok": True})
            elif url.path == "/api/chain/state":
                p = str(data["p"])
                new_state = str(data["state"])
                if new_state not in chain.STATES:
                    self._json(
                        400,
                        {"error": f"illegal state: {new_state}（须 ∈ {'/'.join(chain.STATES)}）"},
                    )
                    return
                c = read_chain(p)
                u = chain.get_unit(c, str(data["unit"]))
                if u is None:
                    self._json(400, {"error": f"unit not found: {data['unit']}"})
                    return
                with _file_lock((PROJECTS_DIR / p / u.file).resolve()):
                    chain.set_state(
                        PROJECTS_DIR / p / u.file,
                        str(data.get("expected", "")),
                        new_state,
                    )
                self._json(200, {"ok": True})
            elif url.path == "/api/chain/append":
                p = str(data["p"])
                kind = str(data["kind"])
                c = read_chain(p)
                u = chain.get_unit(c, str(data["unit"]))
                if u is None:
                    self._json(400, {"error": f"unit not found: {data['unit']}"})
                    return
                path = PROJECTS_DIR / p / u.file
                key: _IdemKey = (p, u.unit, kind, str(data.get("idem", "")))
                # 输入校验先于幂等预留：400 路径不留 PENDING 键，同 idem 重试不会拿到假 dup
                oneline = str(data.get("oneline", "")).strip() if kind in ("run", "gate") else ""
                text2 = str(data.get("text", "")).strip() if kind == "grill" else ""
                verdict = str(data.get("verdict", "")).strip() if kind == "gate" else ""
                if kind not in ("run", "grill", "gate"):
                    self._json(400, {"error": f"unknown kind: {kind}"})
                    return
                if kind == "run" and not oneline:
                    self._json(400, {"error": "oneline 必填（一句话结果）"})
                    return
                if kind == "grill" and not text2:
                    self._json(400, {"error": "text 必填"})
                    return
                if kind == "gate" and not oneline:
                    self._json(400, {"error": "oneline 必填（一句话理由）"})
                    return
                if kind == "gate" and verdict not in ("批准", "打回", "已决策跳过"):
                    self._json(400, {"error": "verdict 必填（批准/打回/已决策跳过）"})
                    return
                with _file_lock(path.resolve()):
                    dup, cached = _idem_reserve(key)
                    if dup:
                        self._json(200, cached)
                        return
                    if kind == "run":
                        provider = str(data.get("provider", ""))
                        outcome = str(data.get("outcome", "成功"))
                        _text = path.read_text(encoding="utf-8")
                        run_no = chain.next_run_no(_text)
                        ts = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
                        card = chain.render_run_card(
                            run_no,
                            provider,
                            ts,
                            outcome,
                            model=str(data.get("model", "")).strip(),
                            taskid=str(data.get("taskid", "")).strip(),
                            duration=str(data.get("duration", "")).strip(),
                            cost=str(data.get("cost", "")).strip(),
                            oneline=oneline,
                            detail=str(data.get("detail", "")).strip(),
                        )
                        chain.append_block_to_section(path, chain.EXEC, card)
                        payload: dict[str, object] = {"ok": True, "run_no": run_no}
                    elif kind == "gate":
                        gtype = str(data.get("type", "单元门")).strip() or "单元门"
                        ts3 = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
                        chain.append_block_to_section(
                            path,
                            chain.RESULT,
                            chain.render_gate_record(gtype, ts3, verdict, oneline),
                        )
                        payload: dict[str, object] = {"ok": True}
                    else:
                        ts2 = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
                        chain.append_thinking_grill(path, chain.render_grill_entry(ts2, text2))
                        payload = {"ok": True}
                _idem_commit(key, payload)
                self._json(200, payload)
            else:
                self._json(404, {"error": "not found"})
        except mdblocks.BlockMismatch as e:
            self._json(409, {"error": str(e)})
        except chain.ChainMismatch as e:
            self._json(409, {"error": str(e)})
        except KeyError as e:
            self._json(400, {"error": f"missing param: {e}"})
        except IndexError as e:
            self._json(400, {"error": str(e)})
        except PermissionError as e:
            self._json(403, {"error": str(e)})
        except Exception as e:  # noqa: BLE001
            self._json(500, {"error": f"{type(e).__name__}: {e}"})

    def _serve_html(self, path: Path) -> None:
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, path: Path) -> None:
        if not path.is_file() or not str(path.resolve()).startswith(str(VENDOR_DIR.resolve())):
            self._json(404, {"error": "not found"})
            return
        ctype = "application/javascript" if path.suffix == ".js" else "application/octet-stream"
        self._serve_bytes(path, ctype)

    def _serve_bytes(self, path: Path, ctype: str) -> None:
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_chain(self, project: str) -> None:
        c = read_chain(project)
        units: list[dict[str, object]] = []
        for u in c.units:
            units.append(
                {
                    "unit": u.unit,
                    "title": u.title,
                    "file": u.file,
                    "follows": u.follows,
                    "layer": u.layer,
                    "gate": u.gate,
                    "superseded_by": u.superseded_by,
                    "legacy": u.legacy,
                    "state": u.state,
                    "state_raw": u.state_raw,
                    "exec_kind": u.exec_kind,
                    "parts": chain.parts_api(u),
                    "meta": u.exec_meta,
                }
            )
        self._json(
            200,
            {
                "order": c.order,
                "missing": c.missing,
                "layer_errors": c.layer_errors,
                "layers": c.layers,
                "units": units,
            },
        )

    def _serve_media(self, project: str, rel: str) -> None:
        d = (PROJECTS_DIR / project).resolve()
        target = (d / rel).resolve()
        if d not in target.parents:
            self._json(403, {"error": "path escape"})
            return
        if not target.is_file():
            self._json(404, {"error": "media not found"})
            return
        ctype = _MEDIA_CTYPE.get(target.suffix.lower(), "application/octet-stream")
        self._serve_bytes(target, ctype)


def run(
    port: int = 8766, host: str = "127.0.0.1", project: str | None = None, open_browser: bool = True
) -> None:
    from rich.console import Console

    console = Console()
    server = ThreadingHTTPServer((host, port), Handler)
    local_url = f"http://localhost:{port}" + (f"?p={project}" if project else "")
    if open_browser:
        webbrowser.open(local_url)
    console.print(f"[green]workbench 已启动[/green]  {local_url}")
    console.print("  [dim]数据源: ai-video/projects/（md 文件唯一事实源）[/dim]")
    console.print("  [dim]Ctrl+C 停止[/dim]")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
