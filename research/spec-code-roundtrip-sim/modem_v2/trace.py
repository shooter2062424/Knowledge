"""追溯標註:把函式連到規格條目 ID(R-* 外部規格 / D-* 內部決定)。"""
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable)


def trace(*ids: str) -> Callable[[F], F]:
    """標註函式實作了哪些規格條目。

    Args:
        *ids: 規格條目 ID,例如 "R-MR-01"、"D-INT-02"。

    Returns:
        原函式(附加 ``__trace__`` 屬性)。
    """
    def deco(fn: F) -> F:
        fn.__trace__ = ids  # type: ignore[attr-defined]
        return fn
    return deco
