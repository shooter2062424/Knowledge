"""台股代號/名稱查詢,用來校正字幕(Whisper)把股票名稱聽成同音字的錯誤。

資料來源是證交所 ISIN 公開清單(上市、上櫃、興櫃),快取在本機 JSON。
查詢時同時比對:代號、名稱完全相符、已確認的字幕別名表,以及去聲調拼音的相似度。

用法:
    python scripts/market/tw_stock_lookup.py update
    python scripts/market/tw_stock_lookup.py query 華晶 6148 聯帽
"""

from __future__ import annotations

import argparse
import csv
import difflib
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

from pypinyin import lazy_pinyin

HERE = Path(__file__).resolve().parent
CACHE = HERE / "data" / "tw_stocks.json"
ALIASES = HERE / "stock_name_aliases.csv"

# strMode:2 = 上市、4 = 上櫃、5 = 興櫃
MARKETS: dict[str, str] = {"2": "上市", "4": "上櫃", "5": "興櫃"}
ISIN_URL = "https://isin.twse.com.tw/isin/C_public.jsp?strMode={mode}"


def fetch_market(mode: str) -> list[dict[str, str]]:
    """抓取證交所 ISIN 清單中的股票列。

    Args:
        mode: ISIN 頁面的 strMode(2 上市、4 上櫃、5 興櫃)。

    Returns:
        每檔股票一個 dict,含 code、name、market、industry。
        只保留 CFICode 以 ``ES`` 開頭的普通股/特別股,排除權證、ETF、債券等。
    """
    req = urllib.request.Request(ISIN_URL.format(mode=mode), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        text = resp.read().decode("big5", errors="replace")
    rows: list[dict[str, str]] = []
    for tr in re.findall(r"<tr>(.*?)</tr>", text, flags=re.S):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)]
        if len(cells) < 6 or "　" not in cells[0]:
            continue
        code, name = cells[0].split("　", 1)
        if not cells[5].startswith("ES"):
            continue
        rows.append({"code": code.strip(), "name": name.strip(), "market": MARKETS[mode], "industry": cells[4]})
    return rows


def update() -> None:
    """下載上市、上櫃、興櫃清單並寫入本機快取。"""
    stocks: list[dict[str, str]] = []
    for mode in MARKETS:
        stocks.extend(fetch_market(mode))
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(stocks, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"wrote {CACHE} ({len(stocks)} stocks)")


def load_stocks() -> list[dict[str, str]]:
    """讀取快取;沒有快取就先下載。

    Returns:
        股票清單。
    """
    if not CACHE.exists():
        update()
    return json.loads(CACHE.read_text(encoding="utf-8"))


def load_aliases() -> list[dict[str, str]]:
    """讀取已確認的字幕別名表(使用者確認或代號比對過的對照)。

    Returns:
        別名列,欄位為 字幕寫法、正確名稱、代號、確認方式、日期。
    """
    if not ALIASES.exists():
        return []
    with ALIASES.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def toneless(text: str) -> str:
    """把中文轉成去聲調、以空白分隔的拼音,用來比對同音字。

    Args:
        text: 中文字串。

    Returns:
        例如「華晶」→ ``"hua jing"``。
    """
    return " ".join(lazy_pinyin(text))


def query(term: str, stocks: list[dict[str, str]], aliases: list[dict[str, str]], top: int = 8) -> None:
    """查詢一個字幕詞,印出最可能的股票。

    依序檢查:代號完全相符、名稱完全相符、別名表、拼音完全相同、拼音相似度。

    Args:
        term: 字幕中的寫法(名稱或代號)。
        stocks: 股票清單。
        aliases: 已確認別名表。
        top: 拼音相似度最多列出幾筆。
    """
    print(f"== {term}")
    by_code = [s for s in stocks if s["code"] == term]
    for s in by_code:
        print(f"  [代號] {s['code']} {s['name']}({s['market']},{s['industry']})")
    for a in aliases:
        if a["字幕寫法"] == term:
            print(f"  [別名表] {term} → {a['正確名稱']} {a['代號']}({a['確認方式']},{a['日期']})")
    exact = [s for s in stocks if s["name"] == term]
    for s in exact:
        print(f"  [名稱相符] {s['code']} {s['name']}({s['market']},{s['industry']})")
    if by_code or exact:
        return
    target = toneless(term)
    scored: list[tuple[float, dict[str, str]]] = []
    for s in stocks:
        py = toneless(s["name"])
        ratio = difflib.SequenceMatcher(None, target, py).ratio()
        if py == target:
            ratio = 2.0  # 同音完全相同排最前
        scored.append((ratio, s))
    scored.sort(key=lambda x: -x[0])
    for ratio, s in scored[:top]:
        tag = "同音" if ratio == 2.0 else f"{ratio:.2f}"
        print(f"  [{tag}] {s['code']} {s['name']}({s['market']},{s['industry']})  {toneless(s['name'])}")


def main(argv: list[str] | None = None) -> None:
    """命令列進入點。

    Args:
        argv: 命令列參數;預設讀 ``sys.argv``。
    """
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("update", help="下載最新股票清單")
    q = sub.add_parser("query", help="查詢字幕中的股票名稱或代號")
    q.add_argument("terms", nargs="+")
    args = parser.parse_args(argv)
    if args.cmd == "update":
        update()
        return
    stocks, aliases = load_stocks(), load_aliases()
    for t in args.terms:
        query(t, stocks, aliases)


if __name__ == "__main__":
    main()
