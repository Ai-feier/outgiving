"""状态机推进 + 校验"""

from __future__ import annotations

from .schema import Kind, can_transition


class TransitionError(Exception):
    pass


def assert_transition(kind: Kind, from_status: str, to_status: str) -> None:
    if from_status == to_status:
        return
    if not can_transition(kind, from_status, to_status):
        raise TransitionError(
            f"{kind.value}: 不允许从 {from_status!r} → {to_status!r}"
        )