"""浏览器预览 —— 侧栏 + Tailwind Typography，区分平台

技术栈：
- markdown-it-py：commonmark 渲染（删掉了手写正则）
- Tailwind CDN + @tailwindcss/typography：零构建排版
- 平台用配色 token 区分，不追求像素级还原
"""

from __future__ import annotations

import re
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlparse

from markdown_it import MarkdownIt

from .id_gen import Platform
from .parser import read_raw
from .repo import Repo, find_repo_root

# markdown 渲染器（HTML 内联，启用表格、删除线、自动链接）
_MD = MarkdownIt("commonmark", {"html": True, "linkify": True, "typographer": True}).enable(
    ["table", "strikethrough"]
)


# 侧栏分组定义：(标题, emoji, 目录前缀, 平台 token)
# 平台 token 决定右侧主体的配色（None 表示无平台特定色）
_GROUPS: list[tuple[str, str, str, str | None]] = [
    ("母版", "📋", "topics", None),
    ("微信公众号", "💬", "platforms/wechat", "wechat"),
    ("小红书", "📕", "platforms/xiaohongshu", "xiaohongshu"),
    ("X", "𝕏", "platforms/x", "x"),
    ("抖音", "🎬", "platforms/douyin", "douyin"),
    ("已发布", "📊", "published", None),
    ("复盘", "📈", "analytics", None),
]

# 平台配色（Tailwind 颜色名 + 主色 hex；用于强调线和 badge）
_PLATFORM_COLORS = {
    "wechat":      ("#07c160", "emerald"),    # 微信绿
    "xiaohongshu": ("#ff2442", "rose"),       # 小红书红
    "x":           ("#1d9bf0", "sky"),        # X 蓝
    "douyin":      ("#fe2c55", "pink"),       # 抖音粉
}


# ────────────────────────── 文件收集 ──────────────────────────

def _collect_topic_files(root: Path, topic_id: str) -> dict[str, list[Path]]:
    """按分组收集与某 topic 相关的所有 md 文件。

    返回 {group_title: [paths...]}；包含没 frontmatter 的 outline.md。
    路径含 topic_id 子串或前缀 = 命中。
    """
    result: dict[str, list[Path]] = {}
    for title, _, prefix, _ in _GROUPS:
        base = root / prefix
        if not base.exists():
            result[title] = []
            continue
        matched: list[Path] = []
        for md in sorted(base.rglob("*.md")):
            rel = str(md.relative_to(root))
            # 跳过 README / TEMPLATE
            if "_TEMPLATE" in rel or rel.endswith("README.md"):
                continue
            # 关联判断：路径里含 topic_id（如 T001-xxx/ 或 T001.md 或 T001-wechat.md）
            if topic_id in str(md):
                matched.append(md)
        result[title] = matched
    return result


def _group_for_path(rel_path: str) -> tuple[str, str, str | None]:
    """根据相对路径找到 (group_title, emoji, platform_token)"""
    for title, emoji, prefix, plat in _GROUPS:
        if rel_path.startswith(prefix):
            return title, emoji, plat
    return "其他", "📄", None


# ────────────────────────── HTML 渲染 ──────────────────────────

def _html_shell(body_html: str, title: str = "Content Pipeline") -> str:
    """统一 HTML 外壳：Tailwind CDN + typography 插件，零构建"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script src="https://cdn.tailwindcss.com?plugins=typography"></script>
<style>
  /* 平台主色 CSS 变量 */
  .platform-wechat      {{ --pc: #07c160; }}
  .platform-xiaohongshu {{ --pc: #ff2442; }}
  .platform-x           {{ --pc: #1d9bf0; }}
  .platform-douyin      {{ --pc: #fe2c55; }}
  .platform-neutral     {{ --pc: #6b7280; }}

  /* 正文内 blockquote / 链接 / 选中 用平台色 */
  .prose blockquote {{ border-left-color: var(--pc, #6b7280) !important; }}
  .prose a          {{ color: var(--pc, #1a73e8) !important; }}

  /* 抖音深色模式：在 .platform-douyin 容器里反转 prose */
  .platform-douyin {{ background: #111; color: #f5f5f5; }}
  .platform-douyin .prose,
  .platform-douyin .prose * {{ color: #f5f5f5 !important; }}
  .platform-douyin .prose h1,
  .platform-douyin .prose h2,
  .platform-douyin .prose h3,
  .platform-douyin .prose strong {{ color: #fff !important; }}
  .platform-douyin .prose code {{ background: #2a2a2a !important; color: #f5f5f5 !important; }}
  .platform-douyin .prose pre  {{ background: #1f1f1f !important; }}
</style>
</head>
<body class="bg-slate-50 text-slate-800">
{body_html}
</body>
</html>"""


def _render_index(repo: Repo) -> str:
    views = repo.by_topic()
    if not views:
        body = """
        <div class="max-w-2xl mx-auto p-12 text-center text-slate-500">
            <p class="text-lg">还没有选题。</p>
            <p class="mt-4 font-mono text-sm bg-slate-100 inline-block px-3 py-1 rounded">content new "标题"</p>
        </div>"""
        return _html_shell(body, "选题总览")

    rows = ""
    for tid in sorted(views):
        v = views[tid]
        drafts = " ".join(
            f'<span class="inline-block px-1.5 py-0.5 rounded text-xs bg-slate-100 text-slate-600">{d.platform}</span>'
            for d in v.drafts
        ) or '<span class="text-slate-300">—</span>'
        rows += f"""
        <tr class="border-b border-slate-100 hover:bg-slate-50">
            <td class="py-3 px-4 font-mono text-sm"><a class="text-sky-600 hover:underline" href="/t/{tid}">{tid}</a></td>
            <td class="py-3 px-4"><a class="text-slate-800 hover:underline" href="/t/{tid}">{v.title}</a></td>
            <td class="py-3 px-4"><span class="text-xs px-2 py-0.5 rounded bg-amber-100 text-amber-800">{v.status}</span></td>
            <td class="py-3 px-4 space-x-1">{drafts}</td>
        </tr>"""

    body = f"""
    <div class="max-w-5xl mx-auto p-8">
        <h1 class="text-2xl font-semibold mb-1">📋 选题总览</h1>
        <p class="text-sm text-slate-500 mb-6">共 {len(repo.entries)} 份文档</p>
        <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <table class="w-full">
            <thead class="bg-slate-50 text-left text-xs uppercase text-slate-500">
                <tr>
                    <th class="py-2 px-4">ID</th><th class="py-2 px-4">标题</th>
                    <th class="py-2 px-4">状态</th><th class="py-2 px-4">平台</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        </div>
    </div>"""
    return _html_shell(body, "选题总览")


def _render_topic_view(repo: Repo, topic_id: str, file_rel: str | None) -> str:
    """侧栏 + 主体布局。file_rel 是相对仓库根的 md 路径。"""
    views = repo.by_topic()
    if topic_id not in views:
        return _html_shell(
            f'<div class="max-w-2xl mx-auto p-12 text-center text-slate-500">未找到 <code>{topic_id}</code></div>'
        )
    view = views[topic_id]
    grouped = _collect_topic_files(repo.root, topic_id)

    # 选中文件：未指定时取第一个有内容的（通常是 brief.md）
    selected_path: Path | None = None
    if file_rel:
        candidate = repo.root / file_rel
        if candidate.exists() and candidate.is_file():
            selected_path = candidate
    if selected_path is None:
        for files in grouped.values():
            if files:
                selected_path = files[0]
                break

    # ── 侧栏 ──
    sidebar_items = ""
    for title, emoji, _prefix, _plat in _GROUPS:
        files = grouped.get(title, [])
        if not files:
            sidebar_items += f"""
            <div class="px-4 py-2 mt-3 text-xs uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <span>{emoji}</span><span>{title}</span>
            </div>
            <div class="px-6 py-1 text-xs text-slate-300">—</div>"""
            continue
        sidebar_items += f"""
        <div class="px-4 py-2 mt-3 text-xs uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
            <span>{emoji}</span><span>{title}</span>
        </div>"""
        for fp in files:
            rel = str(fp.relative_to(repo.root))
            name = fp.name.replace(".md", "")
            is_active = selected_path is not None and fp == selected_path
            cls = (
                "bg-slate-900 text-white"
                if is_active
                else "text-slate-600 hover:bg-slate-100"
            )
            sidebar_items += f"""
            <a href="/t/{topic_id}?f={rel}"
               class="block px-6 py-1.5 text-sm rounded-r-md {cls}">{name}</a>"""

    # ── 主体 ──
    if selected_path is None:
        main = '<div class="p-12 text-slate-500 text-center">这个选题还没有任何文件。</div>'
        platform_class = "platform-neutral"
        breadcrumb = ""
    else:
        fm, raw_body = read_raw(selected_path)
        rel = str(selected_path.relative_to(repo.root))
        group_title, group_emoji, plat = _group_for_path(rel)
        platform_class = f"platform-{plat or 'neutral'}"

        # frontmatter 摘要：只显 id / status / platform / revision / updated_at
        fm_keys = ("id", "status", "platform", "revision", "updated_at", "url")
        fm_chips = ""
        for k in fm_keys:
            if k in fm and fm[k] not in (None, ""):
                fm_chips += f"""<span class="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-600 mr-1.5">
                    <span class="text-slate-400">{k}</span><span class="font-mono">{fm[k]}</span></span>"""

        content_html = _MD.render(raw_body)
        # 重写 img src：相对路径 → /raw/<规范化后的路径>，处理 .. 与中文
        import posixpath
        from urllib.parse import quote, unquote
        md_dir = str(selected_path.parent.relative_to(repo.root))

        def _rewrite_src(m: re.Match) -> str:
            prefix, src, suffix = m.group(1), m.group(2), m.group(3)
            if src.startswith(("http://", "https://", "/")):
                return m.group(0)
            # markdown-it 可能把中文 encode 过一次，先还原
            src = unquote(src)
            # 拼接 md 所在目录 + src，再用 normpath 消解 ..
            joined = posixpath.normpath(posixpath.join(md_dir, src))
            # 不允许跑出 repo root（防止 .. 遍历）
            if joined.startswith("../") or joined == "..":
                return m.group(0)
            encoded = quote(joined, safe="/")
            return f'{prefix}/raw/{encoded}{suffix}'

        content_html = re.sub(r'(src=")([^"]+)(")', _rewrite_src, content_html)
        breadcrumb = f"""
        <div class="text-xs text-slate-500 mb-2 flex items-center gap-2 flex-wrap">
            <span>{group_emoji} {group_title}</span>
            <span class="text-slate-300">/</span>
            <code class="text-slate-700">{rel}</code>
        </div>
        <h1 class="text-2xl font-semibold mb-3 text-slate-900">{selected_path.stem}</h1>
        <div class="mb-6 pb-4 border-b border-slate-200">{fm_chips}</div>"""
        main = f"""
        {breadcrumb}
        <article class="prose prose-slate max-w-none prose-headings:font-semibold prose-img:rounded-lg prose-pre:bg-slate-100">
            {content_html}
        </article>"""

    # ── 页头 ──
    header = f"""
    <header class="px-6 py-3 bg-white border-b border-slate-200 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <a href="/" class="text-sm text-slate-500 hover:text-slate-800">← 选题总览</a>
            <span class="text-slate-300">|</span>
            <span class="font-mono text-sm">{topic_id}</span>
            <span class="text-slate-800 font-medium">{view.title}</span>
        </div>
        <span class="text-xs px-2 py-0.5 rounded bg-amber-100 text-amber-800">{view.status}</span>
    </header>"""

    body = f"""
    {header}
    <div class="flex" style="height: calc(100vh - 49px);">
        <aside class="w-64 bg-white border-r border-slate-200 overflow-y-auto py-2 flex-shrink-0">
            {sidebar_items}
        </aside>
        <main class="flex-1 overflow-y-auto {platform_class}">
            <div class="max-w-3xl mx-auto px-8 py-8">
                {main}
            </div>
        </main>
    </div>"""
    return _html_shell(body, f"{topic_id} · {view.title}")


# ────────────────────────── HTTP 路由 ──────────────────────────

class PreviewHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        pass

    def do_GET(self) -> None:
        # self.path 是 latin-1 解码的 str，中文 UTF-8 字节被拆开。还原成真实 URL。
        try:
            raw_path = self.path.encode("latin-1").decode("utf-8")
        except (UnicodeDecodeError, UnicodeEncodeError):
            raw_path = self.path
        parsed = urlparse(raw_path)
        path = parsed.path
        repo = Repo(find_repo_root()).scan()

        if path == "/":
            html = _render_index(repo)
        elif path.startswith("/t/"):
            topic_id = path[len("/t/"):]
            # ?f=<relative path>
            file_rel: str | None = None
            for kv in parsed.query.split("&"):
                if kv.startswith("f="):
                    file_rel = unquote(kv[2:])
            html = _render_topic_view(repo, topic_id, file_rel)
        elif path.startswith("/raw/"):
            rel = unquote(path[len("/raw/"):])
            fp = repo.root / rel
            if not fp.exists() or not fp.is_file():
                self.send_error(404, f"Not found: {rel}")
                return
            data = fp.read_bytes()
            ext = fp.suffix.lower()
            ctype = {
                ".svg": "image/svg+xml",
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".gif": "image/gif",
                ".webp": "image/webp",
                ".excalidraw": "application/json",
            }.get(ext, "application/octet-stream")
            self.send_response(200)
            self.send_header("Content-Type", f"{ctype}; charset=utf-8" if ext in (".svg",) else ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        else:
            self.send_error(404, f"Not found: {path}")
            return

        data = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def _detect_lan_ip() -> str | None:
    """对外 UDP socket 探测本机在局域网中的 IP（不会真正发包）"""
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return None
    finally:
        s.close()


def serve(
    port: int = 8765,
    host: str = "0.0.0.0",
    open_browser: bool = True,
    open_topic: str | None = None,
) -> None:
    from rich.console import Console

    console = Console()
    server = HTTPServer((host, port), PreviewHandler)
    local_url = f"http://localhost:{port}"
    target = f"{local_url}/t/{open_topic}" if open_topic else local_url

    if open_browser:
        webbrowser.open(target)

    console.print(f"[green]预览服务已启动[/green]  绑定 [cyan]{host}:{port}[/cyan]")
    console.print(f"  [bold]本机访问[/bold]:    {local_url}")
    if host == "0.0.0.0":
        lan = _detect_lan_ip()
        if lan and lan not in ("127.0.0.1", "127.0.1.1"):
            console.print(f"  [bold]局域网访问[/bold]:  http://{lan}:{port}")
    if open_topic:
        console.print(f"  [bold]直达[/bold]:        {target}")
    console.print("  [dim]路由: /  /t/<topic_id>[?f=<file>][/dim]")
    console.print("  [dim]Ctrl+C 停止[/dim]")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        console.print("\n[dim]预览已停止[/dim]")
