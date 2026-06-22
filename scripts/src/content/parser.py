"""Markdown ↔ Frontmatter 读写"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import frontmatter

from .schema import AnyFM, parse_frontmatter


def _yaml_default(obj: object) -> object:
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    return obj


def read(path: Path) -> tuple[AnyFM, str]:
    """读取 md → (frontmatter 模型, 正文)。frontmatter 不合法会抛异常。"""
    post = frontmatter.load(str(path))
    fm = parse_frontmatter(post.metadata)
    return fm, post.content


def read_raw(path: Path) -> tuple[dict, str]:
    """不做 schema 校验，原样读"""
    post = frontmatter.load(str(path))
    return dict(post.metadata), post.content


def write(path: Path, fm: AnyFM, body: str) -> None:
    """模型 → md，自动更新 updated_at"""
    fm = fm.model_copy(update={"updated_at": date.today()})
    meta = fm.model_dump(mode="json", exclude_none=False)
    post = frontmatter.Post(body, **meta)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(frontmatter.dumps(post) + "\n", encoding="utf-8")


def write_raw(path: Path, meta: dict, body: str) -> None:
    """跳过 schema，原样写（用于 migrate）"""
    post = frontmatter.Post(body, **meta)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(frontmatter.dumps(post) + "\n", encoding="utf-8")