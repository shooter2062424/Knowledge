#!/usr/bin/env python3
"""
extract_candidates.py — 從逐字稿撈出「可能是方向性判斷」的候選片段。

這一步刻意**重召回、輕精確**:機械過濾把 440 支逐字稿縮成可人工判讀的候選,
最終哪些算數、方向是什麼,由人(或 LLM)在下一步定案。過濾器自己不下結論。

三種候選,價值由高到低:
  self_action  本人動作揭露(「我今天進場買了…」)—— 有時間戳、有方向、自我承諾,最難賴帳
  directional  明確方向judgement(「我認為會漲到…」)
  mention      只提到標的,方向不明 —— 多半是背景敘述,留著讓人判讀

輸出
----
    calls/candidates_<handle>.json

用法
----
    python src/extract_candidates.py --handle NaNaShuoMeiGu
    python src/extract_candidates.py --all --min-score 2
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CALLS = ROOT / "calls"

# 方向詞典。權重只用來排序候選,不決定最終方向。
BULL = ["看多", "做多", "buy", "買進", "买进", "買入", "买入", "加倉", "加仓", "抄底",
        "上漲", "上涨", "反彈", "反弹", "突破", "新高", "看漲", "看涨", "漲上去", "涨上去",
        "可以進", "可以进", "值得買", "值得买", "低接", "撿", "捡", "布局", "續漲", "续涨"]
BEAR = ["看空", "做空", "sell", "賣出", "卖出", "減倉", "减仓", "清倉", "清仓", "出場", "出场",
        "下跌", "回檔", "回调", "回撤", "崩", "跌破", "新低", "看跌", "跌下去", "轉空", "转空",
        "獲利了結", "获利了结", "減碼", "减码", "風險很大", "风险很大", "泡沫"]
FLAT = ["盤整", "盘整", "橫盤", "横盘", "區間", "区间", "震盪", "震荡", "觀望", "观望"]

# 本人動作:第一人稱 + 交易動詞
# 第一人稱與動詞之間常夾副詞(「我今天『也』進場…」),固定詞表會漏掉,
# 改成允許中間隔最多 8 個非標點字元。
SELF = re.compile(
    r"(我|本人|自己)[^。,,、!?!?\s]{0,8}?"
    r"(進場|进场|加倉|加仓|減倉|减仓|清倉|清仓|買了|买了|買進|买进|賣了|卖了|賣出|卖出|"
    r"撿|捡|建倉|建仓|平倉|平仓|抄底|做多|做空|持有|重倉|重仓|空倉|空仓)"
)

# 條件句 / 不可證偽的措辭 —— 標記出來,下一步多半要剔除
HEDGE = ["可能", "也許", "也许", "或許", "或许", "不排除", "如果", "假如", "要看", "不一定",
         "未必", "有機會", "有机会", "說不定", "说不定", "個人看法", "个人看法"]

# ⚠️ self_action 的三種假陽性。抽驗實際命中過:
#   「雖然我不敢做空」→ 否定,當成看空會完全相反
#   「我本來想抄底的」→ 動作沒執行
#   「一堆人說…我這樣可以加倉」→ 在轉述別人
NEGATION = ["不敢", "沒有", "没有", "不會", "不会", "沒買", "没买", "沒賣", "没卖",
            "不打算", "還沒", "还没", "並未", "并未", "沒能", "没能", "不想"]
HYPOTHETICAL = ["本來想", "本来想", "如果", "假如", "要是", "的話", "的话", "應該會", "应该会",
                "打算", "考慮", "考虑", "會想", "会想", "早知道"]
REPORTED = ["他說", "他说", "有人說", "有人说", "一堆人", "大家都說", "大家都说",
            "市場說", "市场说", "網友", "网友", "粉絲", "粉丝", "密我"]

# 業配 / 導流段落。實測 @hackbearterry 有兩筆是投資平台推廣,裡面同時出現
# 「特斯拉」「做多還是做空」,不擋掉會被當成方向判斷收進樣本。
SPONSOR = ["贊助", "赞助", "業配", "业配", "合作夥伴", "合作伙伴", "折扣碼", "折扣码",
           "優惠碼", "优惠码", "推薦碼", "推荐码", "開戶", "开户", "註冊連結", "注册链接",
           "資訊欄", "资讯栏", "留言區連結", "我幫大家爭取", "我帮大家争取",
           "限時優惠", "限时优惠", "課程", "课程", "報名", "报名", "找助理", "加我微信",
           "私訊我", "私信我", "訂閱我的", "订阅我的"]

# 期間線索
HORIZON = {
    "今天": 1, "明天": 1, "隔天": 1, "短線": 5, "短线": 5, "本週": 5, "本周": 5, "這週": 5,
    "下週": 5, "下周": 5, "未來一週": 5, "两周": 10, "兩週": 10, "未來兩週": 10,
    "本月": 21, "這個月": 21, "下個月": 21, "月底": 21, "中線": 21, "中线": 21,
    "季度": 63, "這一季": 63, "下半年": 126, "年底": 126, "長線": 126, "长线": 126,
}


def _utf8_stdout() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def load_assets() -> list[tuple[str, str]]:
    raw = json.loads((Path(__file__).parent / "assets.json").read_text(encoding="utf-8"))
    pairs = [(k, v) for k, v in raw.items() if not k.startswith("_")]
    # 長別名優先,避免「美元」先吃掉「美元指數」
    return sorted(pairs, key=lambda kv: -len(kv[0]))


def _count(text: str, words: list[str]) -> int:
    return sum(1 for w in words if w in text)


def scan_video(text: str, assets: list[tuple[str, str]], window: int = 2) -> list[dict]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    hits: list[dict] = []
    for i, line in enumerate(lines):
        found: list[tuple[str, str]] = []
        for alias, ticker in assets:
            if alias in line and ticker not in {t for _, t in found}:
                found.append((alias, ticker))
        if not found:
            continue
        lo, hi = max(0, i - window), min(len(lines), i + window + 1)
        snippet = " ".join(lines[lo:hi])

        b, s, f = _count(snippet, BULL), _count(snippet, BEAR), _count(snippet, FLAT)
        raw_self = bool(SELF.search(snippet))
        hedge = _count(snippet, HEDGE)
        horizon = next((v for k, v in HORIZON.items() if k in snippet), None)

        neg = _count(snippet, NEGATION)
        hypo = _count(snippet, HYPOTHETICAL)
        rep = _count(snippet, REPORTED)
        spon = _count(snippet, SPONSOR)
        if spon:
            continue  # 業配段落整段不收
        # 命中任一旗標就不算「已執行的本人動作」,降級待判讀
        self_act = raw_self and not (neg or hypo or rep)

        if self_act:
            kind = "self_action"
        elif raw_self:
            kind = "self_action_suspect"
        elif b or s or f:
            kind = "directional"
        else:
            kind = "mention"

        score = (3 if self_act else 0) + min(b + s + f, 3) + (1 if horizon else 0) \
            - min(hedge, 2) - (2 if (raw_self and not self_act) else 0)

        for alias, ticker in found:
            hits.append({
                "line_no": i,
                "alias": alias,
                "ticker": ticker,
                "kind": kind,
                "score": score,
                "bull": b, "bear": s, "flat": f,
                "hedge": hedge,
                "self_action": self_act,
                "negated": neg, "hypothetical": hypo, "reported": rep,
                "horizon_hint": horizon,
                "snippet": snippet[:400],
            })
    return hits


def dedupe(hits: list[dict], per_ticker: int = 3) -> list[dict]:
    """同一支影片同一標的只留分數最高的幾段,避免整篇被同一個標的洗版。"""
    best: dict[str, list[dict]] = {}
    for h in sorted(hits, key=lambda x: (-x["score"], x["line_no"])):
        best.setdefault(h["ticker"], [])
        if len(best[h["ticker"]]) < per_ticker:
            best[h["ticker"]].append(h)
    out = [h for v in best.values() for h in v]
    return sorted(out, key=lambda x: x["line_no"])


def run_handle(handle: str, assets: list[tuple[str, str]], min_score: int, per_ticker: int) -> dict:
    base = DATA / handle
    meta_path = base / "videos.json"
    if not meta_path.exists():
        return {"handle": handle, "error": "no videos.json"}
    videos = {v["id"]: v for v in json.loads(meta_path.read_text(encoding="utf-8"))}

    out: list[dict] = []
    n_txt = 0
    for txt in sorted((base / "txt").glob("*.txt")) if (base / "txt").exists() else []:
        vid = txt.stem
        meta = videos.get(vid)
        if not meta or not meta.get("timestamp"):
            continue
        n_txt += 1
        hits = dedupe(scan_video(txt.read_text(encoding="utf-8"), assets), per_ticker)
        for h in hits:
            if h["score"] < min_score:
                continue
            h.update({
                "video_id": vid,
                "channel": meta.get("channel"),
                "handle": handle,
                "timestamp": meta["timestamp"],
                "upload_date": meta.get("upload_date"),
                "title": meta.get("title"),
                "url": meta.get("url"),
            })
            out.append(h)

    CALLS.mkdir(parents=True, exist_ok=True)
    dest = CALLS / f"candidates_{handle}.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

    kinds: dict[str, int] = {}
    for h in out:
        kinds[h["kind"]] = kinds.get(h["kind"], 0) + 1
    return {"handle": handle, "transcripts": n_txt, "candidates": len(out),
            "kinds": kinds, "file": str(dest)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--handle", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--min-score", type=int, default=1)
    ap.add_argument("--per-ticker", type=int, default=3)
    args = ap.parse_args(argv)
    _utf8_stdout()

    assets = load_assets()
    handles = ([d.name for d in sorted(DATA.iterdir()) if d.is_dir()]
               if args.all else [args.handle])
    if not handles or handles == [None]:
        ap.error("--handle 或 --all 擇一")

    print(f"{'handle':<24}{'txt':>6}{'cand':>7}   kinds")
    for h in handles:
        r = run_handle(h, assets, args.min_score, args.per_ticker)
        if r.get("error"):
            print(f"{h:<24}  {r['error']}")
            continue
        ks = " ".join(f"{k}={v}" for k, v in sorted(r["kinds"].items()))
        print(f"{h:<24}{r['transcripts']:>6}{r['candidates']:>7}   {ks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
