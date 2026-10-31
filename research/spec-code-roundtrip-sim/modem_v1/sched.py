"""量測回報的處理時間預算(內部決定)。"""
from typing import Any

from .trace import trace

BUDGET_US = 50          # D-INT-02
COST_BASE_US = 5        # D-INT-02
COST_PER_NEIGH_US = 3   # D-INT-02
NEIGH_CAP = 8           # D-INT-01


@trace("D-INT-02")
def cost_us(n_neighbors: int) -> int:
    """估算處理一份回報所需微秒數。"""
    return COST_BASE_US + COST_PER_NEIGH_US * n_neighbors


@trace("D-INT-01", "D-INT-02", "R-MR-03")
def admit(report: dict[str, Any]) -> tuple[bool, int]:
    """判斷回報是否在預算內可處理。"""
    n = len(report.get("neighbors", []))
    if n > NEIGH_CAP:
        return False, 0
    c = cost_us(n)
    return c <= BUDGET_US, c
