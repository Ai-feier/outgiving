"""时钟缝 — content 管线唯一触碰墙钟的位置。

CONTENT_TODAY=YYYY-MM-DD 可覆写日期（测试 / 回填历史数据）；
CONTENT_NOW=YYYY-MM-DD[THH:MM] 可覆写时间戳。
其他模块一律 import clock.today()/now()，不直接调 date.today()。
"""

from __future__ import annotations

import os
from datetime import date, datetime


def today() -> date:
    env = os.environ.get("CONTENT_TODAY", "").strip()
    if env:
        try:
            return date.fromisoformat(env)
        except ValueError:
            pass
    return date.today()


def now() -> datetime:
    env = os.environ.get("CONTENT_NOW", "").strip()
    if env:
        try:
            return datetime.fromisoformat(env)
        except ValueError:
            pass
    return datetime.now()
