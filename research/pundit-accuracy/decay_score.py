#!/usr/bin/env python3
"""
decay_score.py — 「介紹後多快漲」計分。

評分規則(使用者指定)
--------------------
1. 進場 = 影片發布後**第一個尚未開盤**的交易日開盤價(因果性,沿用 candlestick)
2. 對進場後第 d 個交易日(d = 1..window),取當日報酬 r_d,乘上時間衰減 w_d
3. score = Σ (r_d × w_d)
4. 超過 window(預設 10 個交易日 ≈ 兩週)權重為 0,直接不計 ——
   兩週後才漲太慢,可能只是碰巧
5. 每個「影片 × 個股」一個分數;頻道分數 = 全部配對分數的**平均**

r_d 的定義:d=1 是「進場開盤 → 當日收盤」,d≥2 是「前日收盤 → 當日收盤」。
用逐日報酬而非累積報酬,否則同一段漲幅會被重複計入多天。

衰減
----
    linear (預設)  w_d = 1 - (d-1)/window      d=1 → 1.0,d=10 → 0.1
    exp            w_d = exp(-(d-1)/halflife*ln2)
    flat           w_d = 1                      不衰減,用來對照

不做基準比較,直接用原始漲幅。

用法
----
    python src/decay_score.py
    python src/decay_score.py --decay exp --halflife 3
    python src/decay_score.py --dump Josie技术分析
    python src/decay_score.py --bullish-only
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from candlestick import load_ohlcv, next_tradable_session, parse_ts  # noqa: E402
from score_candidates import NOT_A_STOCK  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CALLS = ROOT / "calls"
REPORTS = ROOT / "reports"


def _utf8_stdout() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def weights(window: int, kind: str, halflife: float) -> list[float]:
    if kind == "flat":
        return [1.0] * window
    if kind == "exp":
        return [math.exp(-(d) / halflife * math.log(2)) for d in range(window)]
    return [1.0 - d / window for d in range(window)]     # linear


def score_one(ticker: str, ts, window: int, w: list[float]) -> dict:
    """回傳單一「影片 × 個股」的分數與明細。"""
    out: dict = {"ticker": ticker, "at": ts}
    try:
        pred = parse_ts(ts)
        df = load_ohlcv(ticker, start=pred.date() - timedelta(days=15))
        entry_d = next_tradable_session(ticker, ts, df)
        if entry_d is None:
            out["error"] = "no session after prediction"
            return out
        idx = list(df.index)
        i = idx.index(entry_d)
        if i + window >= len(idx):
            out["error"] = "not enough forward bars"
            return out

        entry_open = float(df.iloc[i]["Open"])
        if not (entry_open > 0):
            out["error"] = "bad entry price"
            return out

        prev = entry_open
        rets: list[float] = []
        for d in range(window):
            close = float(df.iloc[i + d]["Close"])
            if not (close > 0) or not (prev > 0):
                out["error"] = "bad price data"
                return out
            rets.append(close / prev - 1.0)
            prev = close

        score = sum(r * wt for r, wt in zip(rets, w))
        out.update(
            entry_date=entry_d.isoformat(),
            entry_open=entry_open,
            daily_returns=[round(r, 5) for r in rets],
            cum_return=round(prev / entry_open - 1.0, 5),
            score=score,
        )
    except Exception as e:  # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
    return out


def collect_pairs(bullish_only: bool) -> list[dict]:
    """每個「影片 × 個股」取一筆。同一支影片同一標的重複提及只算一次。"""
    pairs: dict[tuple, dict] = {}
    for f in sorted(CALLS.glob("candidates_*.json")):
        for c in json.loads(f.read_text(encoding="utf-8")):
            if c["ticker"] in NOT_A_STOCK:
                continue
            if bullish_only and (c["bull"] - c["bear"]) < 1:
                continue
            key = (c["handle"], c["video_id"], c["ticker"])
            if key in pairs:
                continue
            pairs[key] = {
                "source": c["handle"], "channel": c["channel"],
                "video_id": c["video_id"], "url": c["url"],
                "ticker": c["ticker"], "at": c["timestamp"],
                "upload_date": c["upload_date"], "title": c["title"],
                "quote": c["snippet"][:180],
            }
    return list(pairs.values())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--window", type=int, default=10, help="交易日數,預設 10 ≈ 兩週")
    ap.add_argument("--decay", choices=["linear", "exp", "flat"], default="linear")
    ap.add_argument("--halflife", type=float, default=3.0, help="--decay exp 用")
    ap.add_argument("--bullish-only", action="store_true",
                    help="只算多空詞數為正的提及(預設:所有個股提及)")
    ap.add_argument("--min-pairs", type=int, default=10)
    ap.add_argument("--rank", choices=["shrink", "lcb", "raw"], default="shrink",
                    help="shrink=向全體平均收縮(影片少者被拉回);lcb=95%% 信賴下界;raw=不校正")
    ap.add_argument("--min-videos", type=int, default=10,
                    help="低於這個影片數不進排名 —— n=2 的極端值連收縮都壓不住")
    ap.add_argument("--prior-k", type=float, default=10.0,
                    help="收縮強度,相當於「先驗值等於 k 支影片」")
    ap.add_argument("--dump", default=None)
    args = ap.parse_args(argv)
    _utf8_stdout()

    w = weights(args.window, args.decay, args.halflife)
    print(f"decay={args.decay} window={args.window}  weights="
          f"[{', '.join(f'{x:.2f}' for x in w)}]\n", flush=True)

    pairs = collect_pairs(args.bullish_only)
    print(f"{len(pairs)} (影片 × 個股) 配對", flush=True)

    scored: list[dict] = []
    for p in pairs:
        r = score_one(p["ticker"], p["at"], args.window, w)
        r.update({k: p[k] for k in ("source", "channel", "video_id", "url",
                                    "upload_date", "title", "quote")})
        scored.append(r)

    ok = [s for s in scored if s.get("error") is None]
    print(f"{len(ok)} 筆成功計分,{len(scored)-len(ok)} 筆略過(資料不足)\n", flush=True)

    by: dict[str, list[dict]] = {}
    for s in ok:
        by.setdefault(s["source"], []).append(s)

    if args.dump:
        rs = sorted(by.get(args.dump, []), key=lambda s: -s["score"])
        print(f"=== {args.dump} — {len(rs)} 個配對,分數高到低 ===")
        for s in rs[:25]:
            print(f"\n[{s['upload_date']}] {s['ticker']:6} entry={s['entry_date']} "
                  f"score={s['score']:+.4f}  兩週累積={s['cum_return']:+.2%}")
            print(f"   {s['url']}")
            print(f"   {s['quote'][:120]}")
        return 0

    # ── 兩層彙總 ──────────────────────────────────────────────────
    # 同一支影片裡的多支股票**不是獨立樣本**(同一天、同一個判斷情境)。
    # 先把每支影片的個股分數平均成「影片分數」,再用影片分數算頻道分數,
    # 有效樣本數才會等於影片數,而不是被一支多股影片灌水。
    # 實測:ChiefPaPa 12 個配對有 4 個來自同一支影片。
    per_video: dict[str, dict[str, list[float]]] = {}
    for s in ok:
        per_video.setdefault(s["source"], {}).setdefault(s["video_id"], []).append(s["score"])

    vid_scores = {src: [statistics.mean(v) for v in vids.values()]
                  for src, vids in per_video.items()}
    all_vid = [x for v in vid_scores.values() for x in v]
    global_mean = statistics.mean(all_vid) if all_vid else 0.0

    rows = []
    for src, ss in by.items():
        vs = vid_scores[src]
        n = len(vs)
        raw = statistics.mean(vs)
        sd = statistics.stdev(vs) if n > 1 else 0.0
        se = sd / math.sqrt(n) if n > 1 else float("inf")
        # 收縮:樣本越少,越被拉回全體平均 —— 影片數本身就是加分項
        shrunk = (n * raw + args.prior_k * global_mean) / (n + args.prior_k)
        # 單尾 95% 信賴下界:同時獎勵「分數高」與「樣本多、波動小」
        lcb = raw - 1.645 * se if n > 1 else float("-inf")
        rows.append({
            "source": src, "channel": ss[0]["channel"],
            "pairs": len(ss), "videos": n,
            "pairs_per_video": round(len(ss) / n, 2),
            "video_mean": raw,
            "shrunk": shrunk,
            "lcb": lcb,
            "median_score": statistics.median(vs),
            "pct_positive_videos": sum(1 for v in vs if v > 0) / n,
            "mean_cum_2w": statistics.mean(s["cum_return"] for s in ss),
        })
    key = {"shrink": "shrunk", "lcb": "lcb", "raw": "video_mean"}[args.rank]
    eligible = [r for r in rows if r["videos"] >= args.min_videos]
    benched = [r for r in rows if r["videos"] < args.min_videos]
    eligible.sort(key=lambda r: -r[key])
    benched.sort(key=lambda r: -r["videos"])
    rows = eligible

    print(f"排名依據 = {args.rank}"
          + (f" (prior_k={args.prior_k:g} 支影片)" if args.rank == "shrink" else "")
          + f",全體影片平均 = {global_mean:+.4f}\n")
    print(f"{'channel':<22}{'影片':>5}{'配對':>6}{'每片':>6}"
          f"{'原始':>10}{'收縮後':>10}{'信賴下界':>11}{'正片%':>8}{'兩週累積':>10}")
    for r in rows:
        lcb = f"{r['lcb']:+.4f}" if r["lcb"] != float("-inf") else "     -"
        print(f"{r['source'][:21]:<22}{r['videos']:>5}{r['pairs']:>6}"
              f"{r['pairs_per_video']:>6.1f}{r['video_mean']:>+10.4f}"
              f"{r['shrunk']:>+10.4f}{lcb:>11}{r['pct_positive_videos']:>7.0%}"
              f"{r['mean_cum_2w']:>+10.2%}")
    if benched:
        print(f"\n影片數 < {args.min_videos},不排名(樣本不足以區分實力與運氣):")
        for r in benched:
            print(f"  {r['source'][:21]:<22}影片={r['videos']:>3}  配對={r['pairs']:>3}  "
                  f"原始={r['video_mean']:+.4f}")

    REPORTS.mkdir(parents=True, exist_ok=True)
    tag = f"{args.decay}{args.window}" + ("_bull" if args.bullish_only else "_all")
    dest = REPORTS / f"decay_{tag}.json"
    dest.write_text(json.dumps({"config": vars(args), "channels": rows, "calls": ok},
                               ensure_ascii=False, indent=1),
                    encoding="utf-8", newline="\n")
    print(f"\nwrote {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
