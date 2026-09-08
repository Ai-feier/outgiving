"""
凭证分发。核心层不硬编码任何 provider 的 .env 格式——各家凭证读取逻辑
收在自己的 provider 子包 auth.py 里，这里只做聚合查询。

约定：每个 provider 子包暴露 `check() -> bool`（凭证是否可用，不抛异常）。
"""

from __future__ import annotations

from typing import Callable


def _load(name: str) -> Callable[[], bool]:
    """懒加载 provider 的 check 函数。"""
    import importlib

    module = importlib.import_module(f"ai.providers.{name}.auth")
    return module.check  # type: ignore[no-any-return]


def provider_credentials_ok(name: str) -> bool:
    """查询单个 provider 凭证是否就绪。未知 provider → False。"""
    try:
        return _load(name)()
    except Exception:
        return False


def all_credentials() -> dict[str, bool]:
    """聚合所有已注册 provider 的凭证状态（供 check_connectivity）。"""
    result: dict[str, bool] = {}
    for name in ("volcengine", "autodl_comfyui", "autodl_minimax"):
        result[name] = provider_credentials_ok(name)
    return result
