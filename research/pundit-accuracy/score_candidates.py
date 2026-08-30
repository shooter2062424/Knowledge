#!/usr/bin/env python3
"""
score_candidates.py — 把候選自動轉成方向判斷並回測,依頻道彙總。

專門回答:「哪個頻道點名個股之後,股票真的漲了?」
所以預設只留**個股**(排除指數、ETF、商品、加密貨幣)且**看多**的候選。

⚠️ 這一步的方向是用關鍵詞多寡自動推出來的,必然有雜訊。
   它的用途是**把 7000 多筆縮到值得人工檢查的前幾名**,不是最終結論。
   排名出來後務必用 --dump 逐筆抽查原話。

用法
----
    python src/score_candidates.py --horizon 5d --min-n 8
    python src/score_candidates.py --dump Josie技术分析 --horizon 5d
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from candlestick import CallResult, aggregate, benjamini_hochberg, evaluate_call  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CALLS = ROOT / "calls"
REPORTS = ROOT / "reports"

# 非個股:指數、寬基 ETF、商品、匯率、加密貨幣
NOT_A_STOCK = {
    "^GSPC", "^IXIC", "^DJI", "^RUT", "^VIX", "^TWII", "^HSI", "^TNX", "000001.SS",
    "SPY", "QQQ", "SOXX", "SMH", "ARKK", "GLD", "SLV", "GDX", "TLT",
    "BTC-USD", "ETH-USD", "CL=F", "NG=F", "DX-Y.NYB", "JPY=X",
}

BENCH = "^GSPC"


def _utf8_stdout() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def to_calls(cands: list[dict], stocks_only: bool, bullish_only: bool,
             min_margin: int, max_hedge: int) -> list[dict]:
    """把候選過成「方向夠明確」的判斷。方向由多空詞數差決定。"""
    out = []
    for c in cands:
        if stocks_only and c["ticker"] in NOT_A_STOCK:
            continue
        if c["kind"] not in ("directional", "self_action"):
            continue
        if c["hedge"] > max_hedge:
            continue
        margin = c["bull"] - c["bear"]
        if abs(margin) < min_margin:
            continue
        direction = "long" if margin > 0 else "short"
        if bullish_only and direction != "long":
            continue
        out.append({
            "source": c["handle"],
            "channel": c["channel"],
            "ticker": c["ticker"],
            "at": c["timestamp"],
            "direction": direction,
            "quote": c["snippet"][:200],
            "video": c["url"],
            "upload_date": c["upload_date"],
            "margin": margin,
            "kind": c["kind"],
        })
    return out


def dedupe_calls(calls: list[dict]) -> list[dict]:
    """同一支影片同一標的只留一筆,避免一支影片被重複計入好幾次。"""
    seen: dict[tuple, dict] = {}
    for c in calls:
        key = (c["source"], c["video"], c["ticker"])
        if key not in seen or abs(c["margin"]) > abs(seen[key]["margin"]):
            seen[key] = c
    return list(seen.values())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--horizon", default="5d")
    ap.add_argument("--horizons", default="1,5,21")
    ap.add_argument("--min-n", type=int, default=8, help="低於這個判斷數就不排名")
    ap.add_argument("--min-margin", type=int, default=1)
    ap.add_argument("--max-hedge", type=int, default=2)
    ap.add_argument("--all-tickers", action="store_true", help="不限個股")
    ap.add_argument("--both-directions", action="store_true", help="看空也算")
    ap.add_argument("--dump", default=None, help="印出某頻道的逐筆結果")
    ap.add_argument("--fdr", type=float, default=0.10)
    ap.add_argument("--benchmark", default=BENCH,
                    help="基準。半導體集中的頻道請改用 SOXX 檢驗是否只是產業曝險")
    args = ap.parse_args(argv)
    _utf8_stdout()

    horizons = [int(h) for h in args.horizons.split(",")]

    calls: list[dict] = []
    for f in sorted(CALLS.glob("candidates_*.json")):
        cands = json.loads(f.read_text(encoding="utf-8"))
        calls += to_calls(cands, not args.all_tickers, not args.both_directions,
                          args.min_margin, args.max_hedge)
    calls = dedupe_calls(calls)
    print(f"{len(calls)} calls after filtering\n", flush=True)

    results: list[CallResult] = []
    for c in calls:
        r = evaluate_call(c["ticker"], c["at"], c["direction"], source=c["source"],
                          benchmark=args.benchmark, horizons=horizons,
                          quote=c["quote"], video=c["video"])
        results.append(r)

    by_source: dict[str, list[CallResult]] = {}
    for r in results:
        by_source.setdefault(r.source, []).append(r)

    if args.dump:
        rs = [r for r in by_source.get(args.dump, []) if r.error is None]
        rs.sort(key=lambda r: -(r.excess_return.get(args.horizon) or -9))
        print(f"=== {args.dump} — {len(rs)} scored calls, best first ({args.horizon}) ===")
        for r in rs:
            ex = r.excess_return.get(args.horizon)
            raw = r.raw_return.get(args.horizon)
            if ex is None:
                continue
            print(f"\n[{r.at[:10] if isinstance(r.at,str) else r.at}] {r.ticker:6} "
                  f"entry={r.entry_date} raw={raw:+.2%} excess={ex:+.2%} "
                  f"{'HIT' if r.correct.get(args.horizon) else 'miss'}")
            print(f"   {r.video}")
            print(f"   {(r.quote or '')[:150]}")
        return 0

    summary = {s: aggregate(rs, args.horizon) for s, rs in by_source.items()}
    ranked = [s for s in summary if (summary[s]["n"] or 0) >= args.min_n]
    pvals = [summary[s]["p_ttest"] if summary[s]["p_ttest"] is not None else float("nan")
             for s in ranked]
    flags = benjamini_hochberg(pvals, alpha=args.fdr)
    for s, ok in zip(ranked, flags):
        summary[s]["significant_after_bh"] = ok

    ranked.sort(key=lambda s: -(summary[s]["mean_edge"] or -9))
    print(f"{'channel':<22}{'n':>5}{'hit':>8}{'mean_edge':>11}{'t':>7}{'p':>8}  BH")
    for s in ranked:
        a = summary[s]
        print(f"{s[:21]:<22}{a['n']:>5}{a['hit_rate']:>7.0%}"
              f"{a['mean_edge']:>+11.2%}{a['t_stat']:>7.2f}{a['p_ttest']:>8.3f}"
              f"  {'YES' if a.get('significant_after_bh') else '.'}")

    skipped = [(s, summary[s]["n"]) for s in summary if s not in ranked]
    if skipped:
        print(f"\nn < {args.min_n} 未排名: " + ", ".join(f"{s}({n})" for s, n in skipped))

    REPORTS.mkdir(parents=True, exist_ok=True)
    dest = REPORTS / f"stockpick_{args.horizon}_{args.benchmark.replace('^','')}.json"
    dest.write_text(json.dumps(
        {"horizon": args.horizon, "n_calls": len(results), "by_source": summary},
        ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(f"\nwrote {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
