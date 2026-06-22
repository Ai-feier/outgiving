"""仓库扫描 + 索引"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from .parser import read, read_raw
from .schema import AnyFM, Kind


@dataclass
class IndexEntry:
    id: str
    kind: str
    topic_id: str
    title: str
    status: str
    path: str
    platform: str | None = None


@dataclass
class TopicView:
    topic_id: str
    title: str
    status: str
    drafts: list[IndexEntry] = field(default_factory=list)
    published: list[IndexEntry] = field(default_factory=list)
    analytics: IndexEntry | None = None


@dataclass
class Repo:
    root: Path
    entries: list[IndexEntry] = field(default_factory=list)
    errors: list[tuple[str, str]] = field(default_factory=list)  # (path, message)

    # 仓库根目录下需要扫描的子目录
    SCAN_DIRS = ("topics", "platforms", "published", "analytics")

    # 路径中包含以下片段则跳过（写作区 / 模板 / 文档 / 研究素材）
    SKIP_NAME_PARTS = ("_TEMPLATE", "outline.md", "README.md", "style.md",
                       "research-", "min-", "review-", "appeal-")

    def scan(self) -> "Repo":
        for sub in self.SCAN_DIRS:
            base = self.root / sub
            if not base.exists():
                continue
            for md in base.rglob("*.md"):
                rel = str(md.relative_to(self.root))
                if any(s in rel for s in self.SKIP_NAME_PARTS):
                    continue
                try:
                    fm, _ = read(md)
                except Exception as e:
                    self.errors.append((str(md.relative_to(self.root)), str(e)))
                    continue
                self.entries.append(self._to_entry(fm, md))
        return self

    def _to_entry(self, fm: AnyFM, path: Path) -> IndexEntry:
        platform = getattr(fm, "platform", None)
        return IndexEntry(
            id=fm.id,
            kind=fm.kind if isinstance(fm.kind, str) else fm.kind.value,
            topic_id=fm.topic_id,
            title=fm.title,
            status=fm.status if isinstance(fm.status, str) else fm.status.value,
            path=str(path.relative_to(self.root)),
            platform=platform.value if hasattr(platform, "value") else platform,
        )

    def topic_ids(self) -> list[str]:
        """已存在的 topic_id 集合（按 kind=topic 的条目）"""
        return sorted({e.topic_id for e in self.entries if e.kind == Kind.TOPIC.value})

    def by_topic(self) -> dict[str, TopicView]:
        views: dict[str, TopicView] = {}
        for e in self.entries:
            if e.kind == Kind.TOPIC.value:
                views.setdefault(
                    e.topic_id,
                    TopicView(topic_id=e.topic_id, title=e.title, status=e.status),
                )
                views[e.topic_id].title = e.title
                views[e.topic_id].status = e.status

        for e in self.entries:
            view = views.setdefault(
                e.topic_id,
                TopicView(topic_id=e.topic_id, title=e.title, status="?"),
            )
            if e.kind == Kind.DRAFT.value:
                view.drafts.append(e)
            elif e.kind == Kind.PUBLISHED.value:
                view.published.append(e)
            elif e.kind == Kind.ANALYTICS.value:
                view.analytics = e
        return views

    def stats(self) -> dict:
        by_kind: defaultdict[str, int] = defaultdict(int)
        by_status: defaultdict[str, int] = defaultdict(int)
        by_platform: defaultdict[str, defaultdict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        for e in self.entries:
            by_kind[e.kind] += 1
            by_status[f"{e.kind}/{e.status}"] += 1
            if e.platform:
                by_platform[e.platform][e.kind] += 1
        return {
            "total": len(self.entries),
            "errors": len(self.errors),
            "by_kind": dict(by_kind),
            "by_status": dict(by_status),
            "by_platform": {k: dict(v) for k, v in by_platform.items()},
        }

    def write_index(self, path: Path | None = None) -> Path:
        path = path or (self.root / ".content-index.json")
        payload = {
            "generated_at": date.today().isoformat(),
            "root": str(self.root),
            "stats": self.stats(),
            "topics": {
                tid: {
                    "title": v.title,
                    "status": v.status,
                    "drafts": [e.id for e in v.drafts],
                    "published": [e.id for e in v.published],
                    "analytics": v.analytics.id if v.analytics else None,
                }
                for tid, v in self.by_topic().items()
            },
            "entries": [e.__dict__ for e in self.entries],
            "errors": [{"path": p, "message": m} for p, m in self.errors],
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path


def find_repo_root(start: Path | None = None) -> Path:
    """向上查找包含 inbox / topics 等顶级目录的仓库根。"""
    p = (start or Path.cwd()).resolve()
    markers = {"inbox", "topics", "platforms"}
    for candidate in [p, *p.parents]:
        if all((candidate / m).exists() for m in markers):
            return candidate
    return p  # 兜底：当前目录