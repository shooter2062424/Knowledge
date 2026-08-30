#!/usr/bin/env python3
"""因果安全(causality-safe)的 K 線回測工具。

用途:拿「某人在某個時間點說的一個方向性判斷」,對照**那個時間點之後**的
K 線,算出他到底說對沒有。核心約束只有一條:

    進場價 = 預測時間點之後「第一個尚未開盤的交易日」的開盤價。

講話當下已經開出來的那根 K 棒不算數 —— 這是本模組存在的理由。
所有時間比較一律在**交易所當地時區**進行,不用 UTC 日期硬切。

主要 API:
    * :func:`load_ohlcv` —— 取日 K(含本地 CSV 快取)
    * :func:`next_tradable_session` —— 因果安全的進場日
    * :func:`evaluate_call` —— 評分單一個方向判斷
    * :func:`aggregate` —— 彙總成命中率、超額報酬、t 值、p 值
    * :func:`benjamini_hochberg` —— 多重比較校正(比較多個來源時必用)

用法:
    python scripts/market/candlestick.py check --ticker NVDA \\
        --at 2026-06-03T21:30:00+00:00 --direction long --benchmark ^GSPC

    python scripts/market/candlestick.py score --calls calls.jsonl --out report.json

注意:
    * 報酬用 yfinance 的 ``auto_adjust=True``,已還原分割與配息。
    * 預設以**超額報酬**(相對 benchmark)判定對錯 —— 大盤本身長期上漲,
      只看「漲了沒」會讓所有看多的人自動及格。
    * n 太小時 hit_rate 沒有意義,請一併看 t 值與信賴區間。
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Iterable, Sequence
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# 交易所設定
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Exchange:
    """一個交易所的時區與開收盤時間。

    Attributes:
        tz: IANA 時區名稱,例如 ``America/New_York``。
        open_time: 當地開盤時間。
        close_time: 當地收盤時間。
    """

    tz: str
    open_time: time
    close_time: time


EXCHANGES: dict[str, Exchange] = {
    "US": Exchange("America/New_York", time(9, 30), time(16, 0)),
    "TW": Exchange("Asia/Taipei", time(9, 0), time(13, 30)),
    "HK": Exchange("Asia/Hong_Kong", time(9, 30), time(16, 0)),
    "JP": Exchange("Asia/Tokyo", time(9, 0), time(15, 0)),
    "CN": Exchange("Asia/Shanghai", time(9, 30), time(15, 0)),
}

# ticker 後綴 → 交易所代碼。無後綴一律視為美股。
_SUFFIX_MAP: dict[str, str] = {
    ".TW": "TW",
    ".TWO": "TW",
    ".HK": "HK",
    ".T": "JP",
    ".SS": "CN",
    ".SZ": "CN",
}

DEFAULT_HORIZONS: tuple[int, ...] = (1, 5, 21, 63)  # 交易日:約 1 日 / 1 週 / 1 月 / 1 季
DIRECTIONS: frozenset[str] = frozenset({"long", "short", "flat"})

CACHE_DIR = Path(os.environ.get("CANDLESTICK_CACHE", Path.home() / ".cache" / "candlestick"))


def _utf8_stdout() -> None:
    """把 stdout/stderr 切成 UTF-8,避免 Windows cp950 印中文時直接中斷。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except Exception:  # pragma: no cover
            pass


def exchange_for(ticker: str) -> Exchange:
    """由 ticker 後綴推斷所屬交易所。

    Args:
        ticker: 代號,例如 ``NVDA``、``2330.TW``、``^GSPC``。

    Returns:
        對應的 :class:`Exchange`;無法辨識的後綴一律回傳美股設定。
    """
    upper = ticker.upper()
    for suffix, code in _SUFFIX_MAP.items():
        if upper.endswith(suffix):
            return EXCHANGES[code]
    return EXCHANGES["US"]


# --------------------------------------------------------------------------
# 資料存取
# --------------------------------------------------------------------------


def _cache_path(ticker: str) -> Path:
    """回傳某個 ticker 的快取 CSV 路徑(``^`` 會被換成 ``IDX_`` 以免檔名非法)。"""
    safe = ticker.replace("/", "_").replace("^", "IDX_")
    return CACHE_DIR / f"{safe}.csv"


def load_ohlcv(
    ticker: str,
    start: str | date | None = None,
    end: str | date | None = None,
    *,
    use_cache: bool = True,
    refresh: bool = False,
) -> pd.DataFrame:
    """取得日線 OHLCV。

    index 為 :class:`datetime.date`(交易所當地日曆日),欄位為
    ``Open`` / ``High`` / ``Low`` / ``Close`` / ``Volume``。
    首次抓取會把完整歷史寫進 CSV 快取,之後只在區間不足時重抓。

    Args:
        ticker: 代號。
        start: 起始日(含)。``None`` 表示不裁切。
        end: 結束日(含)。``None`` 表示不裁切。
        use_cache: 是否讀寫本地快取。
        refresh: 強制重抓並覆寫快取。

    Returns:
        依日期排序的 DataFrame。

    Raises:
        ValueError: 遠端沒有回傳任何價格資料(代號錯誤或已下市)。
    """
    path = _cache_path(ticker)
    cached: pd.DataFrame | None = None

    if use_cache and not refresh and path.exists():
        cached = pd.read_csv(path, parse_dates=["Date"])
        cached["Date"] = cached["Date"].dt.date
        cached = cached.set_index("Date").sort_index()

    # 快取涵蓋範圍不足以滿足請求時才重抓,避免每次呼叫都打網路。
    need_fetch = refresh or cached is None
    if cached is not None and start is not None and cached.index.min() > pd.Timestamp(start).date():
        need_fetch = True
    if cached is not None and end is not None and cached.index.max() < pd.Timestamp(end).date():
        need_fetch = True

    if need_fetch:
        import yfinance as yf

        raw = yf.Ticker(ticker).history(period="max", auto_adjust=True)
        if raw.empty:
            raise ValueError(f"no price data returned for {ticker!r}")

        idx = raw.index
        if isinstance(idx, pd.DatetimeIndex) and idx.tz is not None:
            idx = idx.tz_convert(exchange_for(ticker).tz)
        raw = raw.copy()
        raw.index = pd.Index([d.date() for d in idx], name="Date")

        keep = [c for c in ("Open", "High", "Low", "Close", "Volume") if c in raw.columns]
        cached = raw[keep].sort_index()
        if use_cache:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cached.to_csv(path, index_label="Date")

    df = cached
    assert df is not None
    if start is not None:
        df = df[df.index >= pd.Timestamp(start).date()]
    if end is not None:
        df = df[df.index <= pd.Timestamp(end).date()]
    return df


# --------------------------------------------------------------------------
# 因果性
# --------------------------------------------------------------------------


def parse_ts(ts: str | int | float | datetime, default_tz: str = "UTC") -> datetime:
    """把各種時間表示法正規化成帶時區的 datetime。

    接受 :class:`datetime`、ISO 8601 字串,以及 **epoch 秒**。
    yt-dlp 的 ``timestamp`` 欄位就是 epoch,直接丟給 ``fromisoformat`` 會拋例外。

    Args:
        ts: 時間。可為 datetime、ISO 字串、epoch 秒(int/float/純數字字串)。
        default_tz: 當輸入沒有時區資訊時套用的時區。

    Returns:
        帶時區的 :class:`datetime`。

    Raises:
        ValueError: 字串既不是純數字也不是合法的 ISO 8601 格式。
    """
    if isinstance(ts, datetime):
        dt = ts
    elif isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    else:
        text = str(ts).strip()
        if text.lstrip("-").isdigit():  # 例如 "1787965204"
            return datetime.fromtimestamp(int(text), tz=timezone.utc)
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(default_tz))
    return dt


def next_tradable_session(
    ticker: str,
    ts: str | int | float | datetime,
    df: pd.DataFrame | None = None,
    *,
    default_tz: str = "UTC",
) -> date | None:
    """找出 ``ts`` 之後第一個「開盤時間仍在未來」的交易日。

    這是因果性的守門員。例如某人在美東時間 2026-06-03 09:45 發片,
    當天 09:30 已經開盤,那天就**不算**,進場日是下一個交易日。

    Args:
        ticker: 代號,用來決定交易所時區與開盤時間。
        ts: 預測發生的時間點。
        df: 已載入的日 K;``None`` 時自行載入。
        default_tz: ``ts`` 無時區資訊時套用的時區。

    Returns:
        進場交易日;若資料裡找不到任何符合條件的日期則回傳 ``None``。
    """
    ex = exchange_for(ticker)
    tz = ZoneInfo(ex.tz)
    pred = parse_ts(ts, default_tz).astimezone(tz)

    if df is None:
        df = load_ohlcv(ticker, start=pred.date() - timedelta(days=10))

    for session_date in df.index:
        session_open = datetime.combine(session_date, ex.open_time, tzinfo=tz)
        if session_open > pred:
            return session_date
    return None


# --------------------------------------------------------------------------
# 單筆評分
# --------------------------------------------------------------------------


@dataclass
class CallResult:
    """單一方向判斷的評分結果。

    Attributes:
        source: 判斷來源(頻道、作者代號等)。
        ticker: 標的代號。
        at: 判斷發生的時間(原樣保留輸入值)。
        direction: ``long`` / ``short`` / ``flat``。
        entry_date: 因果安全的進場日;失敗時為 ``None``。
        entry_price: 進場開盤價。
        raw_return: 各期間的原始報酬,鍵為 ``"5d"`` 這種字串。
        bench_return: 同期間的 benchmark 報酬。
        excess_return: 原始報酬減去 benchmark 報酬。
        correct: 各期間是否判斷正確。
        error: 評分失敗的原因;成功時為 ``None``。
        quote: 原話節錄,便於事後人工抽查。
        video: 出處連結。
    """

    source: str
    ticker: str
    at: str
    direction: str
    entry_date: str | None
    entry_price: float | None
    raw_return: dict[str, float | None] = field(default_factory=dict)
    bench_return: dict[str, float | None] = field(default_factory=dict)
    excess_return: dict[str, float | None] = field(default_factory=dict)
    correct: dict[str, bool | None] = field(default_factory=dict)
    error: str | None = None
    quote: str | None = None
    video: str | None = None


def _window_return(
    df: pd.DataFrame, entry_date: date, horizon: int
) -> tuple[float | None, float | None, date | None]:
    """由進場日開盤買進、持有 ``horizon`` 個交易日後以收盤賣出。

    Args:
        df: 該標的的日 K。
        entry_date: 進場日。
        horizon: 持有的交易日數。

    Returns:
        ``(進場價, 報酬率, 出場日)``。資料不足時三者皆為 ``None``。
    """
    idx = list(df.index)
    try:
        i = idx.index(entry_date)
    except ValueError:
        # 進場日不在該標的的交易日曆上(例如跨市場),取之後第一個交易日。
        after = [k for k, d in enumerate(idx) if d >= entry_date]
        if not after:
            return None, None, None
        i = after[0]

    j = i + horizon
    if j >= len(idx):
        return None, None, None

    entry = float(df.iloc[i]["Open"])
    exit_price = float(df.iloc[j]["Close"])
    if entry <= 0:
        return None, None, None
    return entry, exit_price / entry - 1.0, idx[j]


def _bench_return_over(bench_df: pd.DataFrame, entry_date: date, exit_date: date) -> float | None:
    """計算 benchmark 在同一段**日曆**窗口內的報酬。

    刻意用日曆窗口而非交易日數,避免兩個市場交易日數不同造成錯位。

    Args:
        bench_df: benchmark 的日 K。
        entry_date: 窗口起日。
        exit_date: 窗口迄日。

    Returns:
        報酬率;窗口內不足兩根 K 棒時回傳 ``None``。
    """
    sub = bench_df[(bench_df.index >= entry_date) & (bench_df.index <= exit_date)]
    if len(sub) < 2:
        return None
    entry = float(sub.iloc[0]["Open"])
    exit_price = float(sub.iloc[-1]["Close"])
    if entry <= 0:
        return None
    return exit_price / entry - 1.0


def evaluate_call(
    ticker: str,
    at: str | int | float | datetime,
    direction: str,
    *,
    source: str = "",
    benchmark: str | None = None,
    horizons: Sequence[int] = DEFAULT_HORIZONS,
    flat_band: float = 0.02,
    default_tz: str = "UTC",
    quote: str | None = None,
    video: str | None = None,
) -> CallResult:
    """評分單一個方向判斷。

    Args:
        ticker: 標的代號。
        at: 判斷發生的時間點,決定因果安全的進場日。
        direction: ``long`` 看多、``short`` 看空、``flat`` 看盤整。
        source: 判斷來源標籤,彙總時用來分組。
        benchmark: 用來計算超額報酬的基準代號;``None`` 表示不做基準比較。
        horizons: 要評估的持有交易日數。
        flat_band: ``flat`` 判斷的容忍區間,``|超額報酬|`` 小於此值即算正確。
        default_tz: ``at`` 無時區資訊時套用的時區。
        quote: 原話節錄。
        video: 出處連結。

    Returns:
        :class:`CallResult`。任何例外都會被收進 ``error`` 欄位而不向外拋,
        方便批次評分時單筆失敗不中斷整批。

    Raises:
        ValueError: ``direction`` 不在 :data:`DIRECTIONS` 之中。
    """
    direction = direction.lower().strip()
    if direction not in DIRECTIONS:
        raise ValueError(f"direction must be one of {sorted(DIRECTIONS)}, got {direction!r}")

    result = CallResult(
        source=source,
        ticker=ticker,
        at=str(at),
        direction=direction,
        entry_date=None,
        entry_price=None,
        quote=quote,
        video=video,
    )

    try:
        pred = parse_ts(at, default_tz)
        df = load_ohlcv(ticker, start=pred.date() - timedelta(days=15))
        entry_date = next_tradable_session(ticker, pred, df)
        if entry_date is None:
            result.error = "no tradable session after prediction timestamp"
            return result
        result.entry_date = entry_date.isoformat()

        bench_df = (
            load_ohlcv(benchmark, start=pred.date() - timedelta(days=15)) if benchmark else None
        )

        for horizon in horizons:
            key = f"{horizon}d"
            entry_price, ret, exit_date = _window_return(df, entry_date, horizon)
            if ret is None or exit_date is None:
                result.raw_return[key] = None
                result.bench_return[key] = None
                result.excess_return[key] = None
                result.correct[key] = None
                continue

            result.entry_price = entry_price
            result.raw_return[key] = ret

            bench = _bench_return_over(bench_df, entry_date, exit_date) if bench_df is not None else None
            result.bench_return[key] = bench
            excess = ret - bench if bench is not None else ret
            result.excess_return[key] = excess

            if direction == "long":
                result.correct[key] = excess > 0
            elif direction == "short":
                result.correct[key] = excess < 0
            else:
                result.correct[key] = abs(excess) < flat_band

    except Exception as exc:  # noqa: BLE001 - 單筆失敗不該打斷整批評分
        result.error = f"{type(exc).__name__}: {exc}"
    return result


# --------------------------------------------------------------------------
# 彙總與統計
# --------------------------------------------------------------------------


def _binom_two_sided(hits: int, n: int, p: float = 0.5) -> float:
    """二項檢定雙尾 p 值(不依賴 scipy)。

    Args:
        hits: 命中次數。
        n: 總次數。
        p: 虛無假設下的單次成功機率。

    Returns:
        雙尾 p 值;``n`` 為 0 時回傳 ``nan``。
    """
    if n == 0:
        return float("nan")
    from math import comb

    observed = comb(n, hits) * p**hits * (1 - p) ** (n - hits)
    total = 0.0
    for i in range(n + 1):
        prob = comb(n, i) * p**i * (1 - p) ** (n - i)
        if prob <= observed * (1 + 1e-9):  # 容忍浮點誤差
            total += prob
    return min(1.0, total)


def aggregate(
    results: Iterable[CallResult],
    horizon: str = "21d",
    *,
    bootstrap: int = 2000,
    seed: int = 0,
) -> dict:
    """把一批評分結果彙總成可比較的統計量。

    ``mean_edge`` 是**方向調整後**的超額報酬(long 取 +、short 取 −、
    flat 取 −|excess|)。直接平均帶號超額會讓「看空且看對」變成扣分,
    與 ``hit_rate`` 自相矛盾。

    Args:
        results: 一批 :class:`CallResult`。
        horizon: 要彙總的期間鍵,如 ``"21d"``。
        bootstrap: bootstrap 重抽次數,用來估信賴區間。
        seed: 亂數種子,確保結果可重現。

    Returns:
        含 ``n``、``hit_rate``、``mean_edge``、``t_stat``、``p_ttest``、
        ``p_binom``、``ci95``、``direction_mix`` 等鍵的字典。
        無有效樣本時各統計量為 ``None``。
    """

    def _usable(r: CallResult) -> bool:
        """只留下有數值的樣本 —— 價格缺值會產生 NaN,只濾 None 不夠。"""
        if r.error is not None:
            return False
        value = r.excess_return.get(horizon)
        return value is not None and value == value  # NaN != NaN

    rows = [r for r in results if _usable(r)]
    n = len(rows)
    out: dict = {"horizon": horizon, "n": n}
    if n == 0:
        out.update(hit_rate=None, mean_edge=None, t_stat=None, p_ttest=None, p_binom=None, ci95=None)
        return out

    excess = np.array([r.excess_return[horizon] for r in rows], dtype=float)
    hits = np.array([bool(r.correct[horizon]) for r in rows], dtype=bool)
    n_hits = int(hits.sum())

    sign = np.array([{"long": 1.0, "short": -1.0}.get(r.direction, 0.0) for r in rows])
    edge = np.where(sign != 0, sign * excess, -np.abs(excess))

    mean = float(edge.mean())
    sd = float(edge.std(ddof=1)) if n > 1 else 0.0
    t_stat = mean / (sd / math.sqrt(n)) if sd > 0 and n > 1 else float("nan")

    p_ttest = float("nan")
    if n > 1 and sd > 0:
        try:
            from scipy import stats

            p_ttest = float(2 * stats.t.sf(abs(t_stat), df=n - 1))
        except Exception:  # pragma: no cover - 沒裝 scipy 就跳過
            pass

    rng = np.random.default_rng(seed)
    boot = rng.choice(edge, size=(bootstrap, n), replace=True).mean(axis=1) if n > 1 else np.array([mean])

    out.update(
        hit_rate=n_hits / n,
        hits=n_hits,
        mean_edge=mean,
        median_edge=float(np.median(edge)),
        std_edge=sd,
        mean_excess_raw=float(excess.mean()),  # 未調整方向,僅供對照
        t_stat=t_stat,
        p_ttest=p_ttest,
        p_binom=_binom_two_sided(n_hits, n),
        ci95=(float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))),
        # 方向分布 —— 用來抓「只會喊多」的來源
        direction_mix={d: sum(1 for r in rows if r.direction == d) for d in sorted(DIRECTIONS)},
    )
    return out


def benjamini_hochberg(pvals: Sequence[float], alpha: float = 0.10) -> list[bool]:
    """Benjamini-Hochberg 多重比較校正,控制錯誤發現率。

    同時檢驗 10 個來源、取表現最好的那個,幾乎保證會找到「看起來很準」
    的人,即使所有人都只是在丟銅板。這個函式就是用來擋這件事的。

    Args:
        pvals: 各來源的 p 值。``nan`` 視為不顯著。
        alpha: 目標錯誤發現率。

    Returns:
        與輸入等長的布林清單,``True`` 表示在該 FDR 下仍顯著。
    """
    m = len(pvals)
    if m == 0:
        return []

    # nan 排到最後,確保不會佔用較嚴格的排名門檻
    order = sorted(range(m), key=lambda i: (float("inf") if pvals[i] != pvals[i] else pvals[i]))
    keep = [False] * m

    max_rank = -1
    for rank, i in enumerate(order, start=1):
        p = pvals[i]
        if p == p and p <= alpha * rank / m:
            max_rank = rank
    for rank, i in enumerate(order, start=1):
        if rank <= max_rank:
            keep[i] = True
    return keep


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _cmd_check(args: argparse.Namespace) -> int:
    """``check`` 子命令:評一筆判斷並印出完整 JSON。"""
    result = evaluate_call(
        args.ticker,
        args.at,
        args.direction,
        source=args.source or "",
        benchmark=args.benchmark,
        horizons=[int(h) for h in args.horizons.split(",")],
        default_tz=args.tz,
    )
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    return 0 if result.error is None else 1


def _cmd_score(args: argparse.Namespace) -> int:
    """``score`` 子命令:批次評分並依來源彙總,含 BH 校正。"""
    horizons = [int(h) for h in args.horizons.split(",")]

    calls: list[dict] = []
    with open(args.calls, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                calls.append(json.loads(line))

    results = [
        evaluate_call(
            c["ticker"],
            c["at"],
            c["direction"],
            source=c.get("source", ""),
            benchmark=c.get("benchmark", args.benchmark),
            horizons=horizons,
            default_tz=c.get("tz", args.tz),
            quote=c.get("quote"),
            video=c.get("video"),
        )
        for c in calls
    ]

    by_source: dict[str, list[CallResult]] = {}
    for r in results:
        by_source.setdefault(r.source or "(unnamed)", []).append(r)

    horizon_key = args.horizon or f"{horizons[-1]}d"
    summary = {src: aggregate(rs, horizon_key) for src, rs in by_source.items()}

    names = list(summary)
    pvals = [summary[s]["p_ttest"] if summary[s]["p_ttest"] is not None else float("nan") for s in names]
    for name, significant in zip(names, benjamini_hochberg(pvals, alpha=args.fdr)):
        summary[name]["significant_after_bh"] = significant

    Path(args.out).write_text(
        json.dumps(
            {
                "horizon": horizon_key,
                "n_calls": len(results),
                "n_errors": sum(1 for r in results if r.error),
                "fdr_alpha": args.fdr,
                "by_source": summary,
                "calls": [asdict(r) for r in results],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"{'source':<28}{'n':>5}{'hit':>8}{'mean_edge':>11}{'t':>8}{'p':>9}  BH")
    for name in sorted(names, key=lambda x: -(summary[x]["n"] or 0)):
        a = summary[name]
        hit = f"{a['hit_rate']:.1%}" if a["hit_rate"] is not None else "-"
        edge = f"{a['mean_edge']:+.2%}" if a["mean_edge"] is not None else "-"
        t = f"{a['t_stat']:.2f}" if a["t_stat"] == a["t_stat"] else "-"
        p = f"{a['p_ttest']:.3f}" if a["p_ttest"] == a["p_ttest"] else "-"
        flag = "YES" if a.get("significant_after_bh") else "."
        print(f"{name[:27]:<28}{a['n']:>5}{hit:>8}{edge:>11}{t:>8}{p:>9}  {flag}")
    print(f"\nwrote {args.out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """命令列進入點。

    Args:
        argv: 命令列參數;``None`` 時使用 ``sys.argv``。

    Returns:
        行程結束碼。
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    check = sub.add_parser("check", help="評一筆判斷")
    check.add_argument("--ticker", required=True)
    check.add_argument("--at", required=True, help="預測時間;ISO 8601 或 epoch 秒")
    check.add_argument("--direction", required=True, choices=sorted(DIRECTIONS))
    check.add_argument("--benchmark", default=None)
    check.add_argument("--source", default=None)
    check.add_argument("--horizons", default="1,5,21,63")
    check.add_argument("--tz", default="UTC", help="輸入時間無時區時套用的時區")
    check.set_defaults(func=_cmd_check)

    score = sub.add_parser("score", help="批次評分並依來源彙總")
    score.add_argument("--calls", required=True, help="JSONL,每行一個判斷")
    score.add_argument("--out", default="candlestick-report.json")
    score.add_argument("--benchmark", default=None, help="預設 benchmark,單筆可覆寫")
    score.add_argument("--horizons", default="1,5,21,63")
    score.add_argument("--horizon", default=None, help="彙總用的期間,如 21d")
    score.add_argument("--tz", default="UTC")
    score.add_argument("--fdr", type=float, default=0.10, help="BH 校正的目標錯誤發現率")
    score.set_defaults(func=_cmd_score)

    args = parser.parse_args(argv)
    _utf8_stdout()
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
