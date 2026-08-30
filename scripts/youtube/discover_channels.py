#!/usr/bin/env python3
"""從 YouTube 搜尋反向挖出候選頻道,並自動篩掉不能用的。

從文章或 AI 回答裡猜 ``@handle`` 很容易猜錯(實測連猜三個全 404)。
改成用 yt-dlp 的 ``ytsearch`` 直接搜影片、再把出現的頻道聚合起來 ——
搜得到的必然存在,而且必然還在更新。

三種模式:
    * ``--queries-file`` 依查詢搜尋並聚合頻道,再對前 N 名做可用性篩選
    * ``--screen`` 直接對指定 handle 做可用性篩選
    * ``--profile`` 對指定 handle 做題材剖析與更新頻率估算

可用性篩選會回報四個決定「能不能用」的指標:

===============  ==========================================================
 指標             意義
===============  ==========================================================
 members_rate     會員限定比率。太高代表免費樣本被系統性挑選過
 caption_rate     有字幕比率。決定要不要花 Whisper 時間
 median_len       影片長度中位數。太短多半是切片,太長多半是直播
 recent_in_range  抽樣影片中落在指定區間內的比例
===============  ==========================================================

用法:
    python scripts/youtube/discover_channels.py --queries-file queries.txt --per-query 25
    python scripts/youtube/discover_channels.py --screen @HandleA @HandleB
    python scripts/youtube/discover_channels.py --profile @HandleA
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import yt_dlp

_YDL_BASE: dict = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
    "noprogress": True,
    "js_runtimes": {"node": {}},
}

# yt-dlp 對會員限定影片拋出的錯誤訊息裡會包含這段文字。
MEMBERS_MARK = "available to this channel's members"

# 題材關鍵字。機械篩選只看得出「片長正常、有字幕」,看不出講的是什麼。
TOPIC_WORDS: dict[str, list[str]] = {
    "us": ["美股", "標普", "标普", "納斯達克", "纳斯达克", "納指", "纳指", "道瓊", "道琼",
           "輝達", "英偉達", "英伟达", "NVDA", "特斯拉", "TSLA", "蘋果", "苹果", "AAPL",
           "聯準會", "联准会", "美聯儲", "美联储", "Fed", "降息", "升息", "美債", "美债"],
    "tw": ["台股", "加權", "加权", "櫃買", "柜买", "台積電", "台积电", "鴻海", "鸿海",
           "聯發科", "联发科", "投信", "外資買超", "外资买超", "當沖", "当冲", "存股"],
    "crypto": ["比特幣", "比特币", "以太", "BTC", "ETH", "幣圈", "币圈", "加密"],
    "metal": ["黃金", "黄金", "白銀", "白银", "金價", "金价"],
    "politics": ["時政", "时政", "政局", "選舉", "选举"],
}


def _utf8_stdout() -> None:
    """把 stdout/stderr 切成 UTF-8,避免 Windows cp950 印中文頻道名時中斷。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except Exception:  # pragma: no cover
            pass


def _to_url(handle_or_url: str) -> str:
    """把 ``@handle`` 補成完整頻道網址;已是網址則原樣回傳。

    Args:
        handle_or_url: ``@handle`` 或完整網址。

    Returns:
        完整的頻道網址。
    """
    return handle_or_url if handle_or_url.startswith("http") else f"https://www.youtube.com/{handle_or_url}"


def search_channels(queries: list[str], per_query: int) -> dict[str, dict]:
    """依查詢搜尋影片,並把出現過的頻道聚合起來。

    Args:
        queries: 查詢字串清單。混合不同角度的查詢,避免只撈到同一類頻道。
        per_query: 每個查詢取幾筆結果。

    Returns:
        以 channel_id 為鍵的字典,值含 ``hits``(命中次數)、``channel``、
        ``channel_url``、``titles``(取樣標題)與 ``queries``(命中的查詢)。
    """
    opts = dict(_YDL_BASE, extract_flat=True)
    agg: dict[str, dict] = defaultdict(lambda: {"hits": 0, "titles": [], "queries": []})

    with yt_dlp.YoutubeDL(opts) as ydl:
        for query in queries:
            try:
                info = ydl.extract_info(f"ytsearch{per_query}:{query}", download=False)
            except Exception as exc:  # noqa: BLE001 - 單一查詢失敗不中斷
                print(f"  query FAILED {query!r}: {type(exc).__name__}", flush=True)
                continue

            for entry in info.get("entries") or []:
                cid = entry.get("channel_id") or entry.get("uploader_id")
                if not cid:
                    continue
                rec = agg[cid]
                rec["hits"] += 1
                rec["channel"] = entry.get("channel") or entry.get("uploader")
                rec["channel_url"] = entry.get("channel_url") or entry.get("uploader_url")
                if len(rec["titles"]) < 3:
                    rec["titles"].append(entry.get("title"))
                if query not in rec["queries"]:
                    rec["queries"].append(query)
            print(f"  searched {query!r} -> {len(agg)} channels so far", flush=True)

    return dict(agg)


def screen_channel(url: str, since_epoch: int, *, probe: int = 8, scan: int = 80) -> dict:
    """對單一頻道取樣,回報可用性指標。

    Args:
        url: 頻道網址。
        since_epoch: 判斷「近期」的起始時間(epoch 秒)。
        probe: 實際抓完整 metadata 的影片數。越多越準,但越慢。
        scan: flat 列出幾支影片。

    Returns:
        含 ``channel`` / ``handle`` / ``subs`` / ``members_rate`` /
        ``caption_rate`` / ``median_len_min`` / ``recent_in_range`` 的字典;
        整個頻道抓不到時含 ``error`` 鍵。
    """
    out: dict = {"url": url}
    flat = dict(_YDL_BASE, extract_flat=True, playlistend=scan)

    try:
        with yt_dlp.YoutubeDL(flat) as ydl:
            info = ydl.extract_info(url.rstrip("/") + "/videos", download=False)
    except Exception as exc:  # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {str(exc)[:90]}"
        return out

    out["channel"] = info.get("channel") or info.get("title")
    out["handle"] = info.get("uploader_id")
    out["subs"] = info.get("channel_follower_count")
    entries = [e for e in (info.get("entries") or []) if e.get("id")]
    out["listed"] = len(entries)

    members = captioned = ok = in_range = 0
    lengths: list[int] = []

    with yt_dlp.YoutubeDL(_YDL_BASE) as ydl:
        for entry in entries[:probe]:
            try:
                info_v = ydl.extract_info(f"https://youtu.be/{entry['id']}", download=False)
            except Exception as exc:  # noqa: BLE001
                if MEMBERS_MARK in str(exc):
                    members += 1
                continue

            ok += 1
            if info_v.get("duration"):
                lengths.append(info_v["duration"])
            if (info_v.get("timestamp") or 0) >= since_epoch:
                in_range += 1
            subs = [k for k in (info_v.get("subtitles") or {}) if k != "live_chat"]
            if subs or info_v.get("automatic_captions"):
                captioned += 1

    probed = min(probe, len(entries))
    out["probed"] = probed
    out["members_rate"] = round(members / probed, 2) if probed else None
    out["caption_rate"] = round(captioned / ok, 2) if ok else None
    out["median_len_min"] = round(statistics.median(lengths) / 60, 1) if lengths else None
    out["recent_in_range"] = f"{in_range}/{ok}" if ok else "0/0"
    return out


def profile_channel(url: str, *, scan: int = 60, probe: int = 6) -> dict:
    """由標題判斷頻道題材,並用少量抽樣估算更新頻率。

    Args:
        url: 頻道網址。
        scan: 取幾則標題做題材判斷。
        probe: 抓幾支影片的時間戳來估頻率。

    Returns:
        含 ``topic``(各題材佔比)、``primary_topic``、``days_per_video``、
        ``est_6m_videos`` 的字典。

    Note:
        ``est_6m_videos`` 由少量抽樣外推,遇到發片有爆量期會嚴重高估
        (實測曾把實際 45 支估成 225 支)。只可當粗略排序用,
        真實數量請以 ``collect_channel.py`` 的實際收集結果為準。
    """
    out: dict = {"url": url}
    flat = dict(_YDL_BASE, extract_flat=True, playlistend=scan)

    try:
        with yt_dlp.YoutubeDL(flat) as ydl:
            info = ydl.extract_info(url.rstrip("/") + "/videos", download=False)
    except Exception as exc:  # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {str(exc)[:80]}"
        return out

    out["channel"] = info.get("channel") or info.get("title")
    out["handle"] = info.get("uploader_id")
    out["subs"] = info.get("channel_follower_count")
    entries = [e for e in (info.get("entries") or []) if e.get("id")]
    titles = [(e.get("title") or "") for e in entries]
    out["titles_scanned"] = len(titles)

    scores = {
        topic: round(sum(1 for t in titles if any(w in t for w in words)) / max(len(titles), 1), 2)
        for topic, words in TOPIC_WORDS.items()
    }
    out["topic"] = scores
    out["primary_topic"] = max(scores, key=lambda k: scores[k]) if titles else None

    stamps: list[int] = []
    with yt_dlp.YoutubeDL(_YDL_BASE) as ydl:
        for entry in entries[:probe]:
            try:
                info_v = ydl.extract_info(f"https://youtu.be/{entry['id']}", download=False)
            except Exception:  # noqa: BLE001
                continue
            if info_v.get("timestamp"):
                stamps.append(info_v["timestamp"])

    if len(stamps) >= 2:
        span_days = (max(stamps) - min(stamps)) / 86400
        per_day = (len(stamps) - 1) / span_days if span_days > 0 else None
        out["days_per_video"] = round(1 / per_day, 1) if per_day else None
        out["est_6m_videos"] = int(per_day * 180) if per_day else None

    out["sample_titles"] = titles[:3]
    return out


def verdict(stats: dict) -> str:
    """依可用性指標給出「能不能用」的結論。

    門檻刻意寫死在這裡,方便日後檢討。

    Args:
        stats: :func:`screen_channel` 的回傳值。

    Returns:
        ``KEEP`` / ``KEEP (whisper needed)`` / ``SKIP ...`` / ``ERROR``。
    """
    if stats.get("error"):
        return "ERROR"
    if (stats.get("members_rate") or 0) >= 0.5:
        return "SKIP members-only"
    median_len = stats.get("median_len_min") or 0
    if median_len < 4:
        return "SKIP too-short/clips"
    if median_len > 90:
        return "SKIP livestream"
    if stats.get("caption_rate") is None:
        return "SKIP no-data"
    return "KEEP" if stats["caption_rate"] >= 0.5 else "KEEP (whisper needed)"


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
    parser.add_argument("--queries-file", default=None, help="每行一個查詢的文字檔")
    parser.add_argument("--per-query", type=int, default=25, help="每個查詢取幾筆結果")
    parser.add_argument("--top", type=int, default=25, help="依命中數取前 N 個頻道做篩選")
    parser.add_argument("--screen", nargs="*", default=None, help="直接篩選指定 @handle")
    parser.add_argument("--profile", nargs="*", default=None, help="對指定 @handle 做題材剖析")
    parser.add_argument("--since", default="2026-03-01", help="判斷「近期」的起始日")
    parser.add_argument("--outdir", default="reports", help="輸出目錄")
    args = parser.parse_args(argv)
    _utf8_stdout()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    since_epoch = int(
        datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()
    )

    # ---- profile 模式 ----
    if args.profile:
        rows = [profile_channel(_to_url(h)) for h in args.profile]
        print(f"{'channel':<22}{'handle':<24}{'subs':>9}{'d/vid':>7}{'6m':>6}  topic mix")
        for row in rows:
            if row.get("error"):
                print(f"{row['url']:<22}  {row['error']}")
                continue
            mix = " ".join(
                f"{k}={v}" for k, v in sorted(row["topic"].items(), key=lambda kv: -kv[1]) if v > 0
            )
            print(
                f"{(row.get('channel') or '')[:21]:<22}{str(row.get('handle') or '')[:23]:<24}"
                f"{str(row.get('subs') or '?'):>9}{str(row.get('days_per_video') or '?'):>7}"
                f"{str(row.get('est_6m_videos') or '?'):>6}  {mix}"
            )
        dest = outdir / "profiles.json"
        dest.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        print(f"\nwrote {dest}")
        return 0

    # ---- screen / search 模式 ----
    if args.screen:
        targets = [{"channel_url": _to_url(h), "hits": 0} for h in args.screen]
    else:
        if not args.queries_file:
            parser.error("--queries-file / --screen / --profile 三者擇一")
        queries = [
            line.strip()
            for line in Path(args.queries_file).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        ]
        print(f"searching {len(queries)} queries x {args.per_query}")
        agg = search_channels(queries, args.per_query)
        targets = sorted(agg.values(), key=lambda r: -r["hits"])[: args.top]
        print(f"\nfound {len(agg)} channels, screening top {len(targets)}\n")

    rows: list[dict] = []
    for target in targets:
        url = target.get("channel_url")
        if not url:
            continue
        stats = screen_channel(url, since_epoch)
        stats["search_hits"] = target.get("hits", 0)
        stats["verdict"] = verdict(stats)
        rows.append(stats)
        print(
            f"{(stats.get('channel') or url)[:22]:<24}"
            f"{str(stats.get('handle') or '')[:22]:<24}"
            f"subs={str(stats.get('subs') or '?'):>8}  "
            f"mem={stats.get('members_rate')}  cap={stats.get('caption_rate')}  "
            f"len={stats.get('median_len_min')}m  {stats['verdict']}",
            flush=True,
        )

    dest = outdir / "discovery.json"
    dest.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    usable = sum(1 for r in rows if r["verdict"].startswith("KEEP"))
    print(f"\nwrote {dest} — {usable}/{len(rows)} usable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
