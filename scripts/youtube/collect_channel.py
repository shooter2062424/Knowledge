#!/usr/bin/env python3
"""抓取 YouTube 頻道的影片清單與逐字稿。

會為每支影片記錄 yt-dlp 的 ``timestamp``(epoch 秒,精確到秒),而不是只有
日期的 ``upload_date`` —— 需要判斷「發言在行情之前」時,秒級時間戳是必要的。

字幕優先順序:官方字幕 → 自動字幕 → 都沒有就標記 ``needs_whisper``,
之後交給 ``scripts/media/whisper_transcribe.py`` 補。

用法:
    python scripts/youtube/collect_channel.py --channel @SomeHandle --since 2026-03-01
    python scripts/youtube/collect_channel.py --channel @SomeHandle --since 2026-03-01 --list-only

輸出:
    <outdir>/<handle>/videos.json         影片 metadata(含 timestamp)
    <outdir>/<handle>/txt/<video_id>.txt  逐字稿純文字
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yt_dlp

# 字幕語言的偏好順序,由前往後試。
SUB_LANGS: list[str] = ["zh-Hant", "zh-TW", "zh", "zh-Hans", "zh-CN", "yue", "en"]

# yt-dlp 共用選項。js_runtimes 必須是 dict,寫成 list 會 ValueError。
_YDL_BASE: dict = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
    "noprogress": True,
    "js_runtimes": {"node": {}},
}

# VTT 的時間軸行,轉純文字時要濾掉。
_TS_LINE = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s+-->")


def _utf8_stdout() -> None:
    """把 stdout/stderr 切成 UTF-8。

    Windows 終端機預設 cp950,印出中文影片標題會直接 ``UnicodeEncodeError``
    並中斷整支腳本 —— 不只是顯示成亂碼而已。
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except Exception:  # pragma: no cover
            pass


def epoch_of(day: str) -> int:
    """把 ``YYYY-MM-DD`` 轉成 UTC epoch 秒。

    Args:
        day: 日期字串,格式 ``YYYY-MM-DD``。

    Returns:
        該日 00:00:00 UTC 的 epoch 秒。

    Raises:
        ValueError: 格式不符。
    """
    return int(datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())


def list_video_ids(channel: str, limit: int = 400) -> list[str]:
    """列出頻道的影片 id(新到舊)。

    只做 flat 擷取,不取每支影片的完整 metadata,所以很快。

    Args:
        channel: ``@handle`` 或完整頻道網址。
        limit: 最多列出幾支。

    Returns:
        影片 id 清單,由新到舊。
    """
    opts = dict(_YDL_BASE, extract_flat=True, playlistend=limit)
    url = channel if channel.startswith("http") else f"https://www.youtube.com/{channel}"
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url.rstrip("/") + "/videos", download=False)
    return [e["id"] for e in (info.get("entries") or []) if e.get("id")]


def fetch_meta(video_id: str) -> dict:
    """取得單支影片的 metadata。

    Args:
        video_id: 11 碼影片 id。

    Returns:
        含 ``id`` / ``title`` / ``timestamp`` / ``duration`` /
        ``official_subs`` / ``auto_subs`` 等鍵的字典。

    Raises:
        yt_dlp.utils.DownloadError: 影片為會員限定、已刪除或私人。
    """
    with yt_dlp.YoutubeDL(_YDL_BASE) as ydl:
        info = ydl.extract_info(f"https://youtu.be/{video_id}", download=False)

    subs = [k for k in (info.get("subtitles") or {}) if k != "live_chat"]
    auto = list(info.get("automatic_captions") or {})
    return {
        "id": video_id,
        "title": info.get("title"),
        "channel": info.get("channel"),
        "handle": info.get("uploader_id"),
        "timestamp": info.get("timestamp"),  # ← 秒級,判斷時序靠這個
        "upload_date": info.get("upload_date"),
        "duration": info.get("duration"),
        "official_subs": sorted(subs),
        "auto_subs": sorted(auto),
        "url": f"https://www.youtube.com/watch?v={video_id}",
    }


def vtt_to_text(vtt: str) -> str:
    """把 VTT 字幕轉成純文字。

    去掉時間軸、內嵌標記,並移除 YouTube 自動字幕特有的捲動重複行
    (前一行的內容會再出現在下一行開頭)。

    Args:
        vtt: VTT 檔的完整內容。

    Returns:
        一行一句的純文字。
    """
    out: list[str] = []
    for raw in vtt.splitlines():
        line = raw.strip()
        if not line or line == "WEBVTT" or _TS_LINE.match(line):
            continue
        if line.startswith(("Kind:", "Language:", "NOTE")) or line.isdigit():
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        if not line:
            continue
        if out and (line == out[-1] or line in out[-1]):  # 捲動字幕的重複
            continue
        out.append(line)
    return "\n".join(out)


def fetch_transcript(video_id: str, outdir: Path) -> str | None:
    """下載字幕並轉存成純文字。

    Args:
        video_id: 影片 id。
        outdir: 頻道的輸出目錄;文字會寫到 ``outdir/txt/<video_id>.txt``。

    Returns:
        實際採用的字幕語言代碼;完全沒有字幕時回傳 ``None``。
    """
    tmp = outdir / "_sub"
    tmp.mkdir(parents=True, exist_ok=True)

    opts = dict(
        _YDL_BASE,
        writesubtitles=True,
        writeautomaticsub=True,
        subtitleslangs=SUB_LANGS,
        subtitlesformat="vtt",
        outtmpl=str(tmp / "%(id)s.%(ext)s"),
    )
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([f"https://youtu.be/{video_id}"])

    try:
        for lang in SUB_LANGS:  # 依偏好順序挑第一個有內容的
            for candidate in tmp.glob(f"{video_id}.{lang}*.vtt"):
                text = vtt_to_text(candidate.read_text(encoding="utf-8", errors="replace"))
                if text.strip():
                    dest = outdir / "txt" / f"{video_id}.txt"
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_text(text, encoding="utf-8", newline="\n")
                    return lang
        return None
    finally:
        for leftover in tmp.glob(f"{video_id}.*"):
            leftover.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    """命令列進入點。

    Args:
        argv: 命令列參數;``None`` 時使用 ``sys.argv``。

    Returns:
        行程結束碼;區間內沒有任何影片時回傳 1。
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--channel", required=True, help="@handle 或完整頻道網址")
    parser.add_argument("--since", required=True, help="起始日 YYYY-MM-DD")
    parser.add_argument("--until", default=None, help="結束日 YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=400, help="最多掃描幾支(新到舊)")
    parser.add_argument("--outdir", default="data", help="輸出根目錄(預設 data)")
    parser.add_argument("--list-only", action="store_true", help="只抓 metadata,不下載字幕")
    parser.add_argument(
        "--stop-after",
        type=int,
        default=25,
        help="連續幾支早於 --since 才視為掃完。直播型頻道的 /videos 排序不嚴格,設太小會提早中斷",
    )
    args = parser.parse_args(argv)
    _utf8_stdout()

    since = epoch_of(args.since)
    until = epoch_of(args.until) if args.until else None

    ids = list_video_ids(args.channel, args.limit)
    print(f"listed {len(ids)} videos from {args.channel}", flush=True)

    metas: list[dict] = []
    outdir: Path | None = None
    consecutive_old = 0
    n_failed = 0
    reached_since = False
    scanned = 0

    for n, vid in enumerate(ids, 1):
        scanned = n
        try:
            meta = fetch_meta(vid)
        except Exception as exc:  # noqa: BLE001 - 多為會員限定,記錄後繼續
            n_failed += 1
            print(f"  [{n}] {vid} meta FAILED: {type(exc).__name__}", flush=True)
            continue

        ts = meta.get("timestamp")
        if ts is None:
            continue
        if until and ts > until:
            continue
        if ts < since:
            # /videos 分頁對直播型頻道並非嚴格新到舊(排程時間 vs 實際開播),
            # 所以要連續多支早於區間才算真的掃完。
            consecutive_old += 1
            if consecutive_old >= args.stop_after:
                reached_since = True
                print(f"  reached {args.since} ({consecutive_old} consecutive older)", flush=True)
                break
            continue
        consecutive_old = 0

        if outdir is None:
            handle = (meta.get("handle") or args.channel).lstrip("@")
            outdir = Path(args.outdir) / handle
            outdir.mkdir(parents=True, exist_ok=True)

        if not args.list_only:
            try:
                lang = fetch_transcript(vid, outdir)
            except Exception as exc:  # noqa: BLE001
                lang = None
                print(f"  [{n}] {vid} sub FAILED: {type(exc).__name__}", flush=True)
            meta["transcript_lang"] = lang
            meta["needs_whisper"] = lang is None

        metas.append(meta)
        mark = "" if args.list_only else f"  sub={meta.get('transcript_lang')}"
        print(f"  [{n}] {meta['upload_date']} {vid}{mark}  {(meta['title'] or '')[:40]}", flush=True)

    if outdir is None:
        print("no videos in range")
        return 1

    dest = outdir / "videos.json"
    dest.write_text(json.dumps(metas, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

    if not reached_since:
        earliest = min(m["upload_date"] for m in metas)
        print(
            f"  ⚠️ 掃完 {scanned} 支仍未回溯到 {args.since},樣本被 --limit 截斷,"
            f"實際只涵蓋到 {earliest}。請調高 --limit 重跑。",
            flush=True,
        )
    if n_failed:
        print(f"  ⚠️ {n_failed} 支取不到 metadata(多為會員限定),已排除 —— 屬選樣偏誤", flush=True)

    if args.list_only:
        print(f"\nwrote {dest} — {len(metas)} videos(僅 metadata,未檢查字幕)")
    else:
        need = sum(1 for m in metas if m.get("needs_whisper"))
        print(f"\nwrote {dest} — {len(metas)} videos, {need} need whisper")
    return 0


if __name__ == "__main__":
    sys.exit(main())
