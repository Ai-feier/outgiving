"""共享测试夹具：AUTODL_API_KEY 模拟 + ai 包路径。"""

# pyright: reportUnusedFunction=false
# 注：pytest fixture 经装饰器注册即用途，函数定义会被误报未使用

import sys
from pathlib import Path
from typing import Callable

import pytest

# 确保 scripts/src 在路径中
_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


@pytest.fixture(autouse=True)
def _autodl_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """所有测试默认带 AUTODL_API_KEY（避免真实令牌依赖）。"""
    monkeypatch.setenv("AUTODL_API_KEY", "test-token")


@pytest.fixture
def video_provider(monkeypatch: pytest.MonkeyPatch) -> Callable[[str], None]:
    """设置 VIDEO_PROVIDER（env 每次叠加，无需清缓存）。"""

    def _set(provider: str) -> None:
        monkeypatch.setenv("VIDEO_PROVIDER", provider)

    return _set
