"""量測回報的處理時間預算(內部決定)。"""
from typing import Any

from .trace import trace

BUDGET_US = 50          # D-INT-02
COST_BASE_US = 5        # D-INT-02
COST_PER_NEIGH_US = 3   # D-INT-02
NEIGH_CAP = 16          # D-INT-01
BATCH_THRESHOLD = 8     # D-INT-02(修訂:第 9 筆起走批次路徑)
COST_PER_NEIGH_BATCH_US = 2  # D-INT-02(修訂,待 HW 小組確認)


@trace("D-INT-02")
def cost_us(n_neighbors: int) -> int:
    """估算處理一份回報所需微秒數。"""
    base = min(n_neighbors, BATCH_THRESHOLD)
    batched = max(n_neighbors - BATCH_THRESHOLD, 0)
    return COST_BASE_US + COST_PER_NEIGH_US * base + COST_PER_NEIGH_BATCH_US * batched


@trace("D-INT-01", "D-INT-02", "R-MR-03")
def admit(report: dict[str, Any]) -> tuple[bool, int]:
    """判斷回報是否在預算內可處理。"""
    n = len(report.get("neighbors", []))
    if n > NEIGH_CAP:
        return False, 0
    c = cost_us(n)
    return c <= BUDGET_US, c
