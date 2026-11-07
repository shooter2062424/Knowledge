"""逐字稿時間校正工具:帶時間的字幕、片語定位、影片截圖。

三個子命令,專門解決「逐字稿可疑詞要讓使用者回到影片對的時間點確認」的問題:

* ``fetch``:下載 YouTube 字幕(官方優先,沒有就用自動字幕;含時間),輸出 ``[m:ss] 文字`` 逐行檔。
* ``find``:在帶時間的逐字稿中搜尋片語,印出精確時間與可點擊的連結(預設提前 10 秒)。
* ``frames``:下載低畫質影片並在指定秒數截圖,用來看燒錄字幕與投影片上的正確拼法。

⚠️ 時間規則:任何要給使用者看的時間點,都必須來自本工具印出的逐字稿時間,
**不可憑印象寫「約 X:XX」**。

用法範例::

    python scripts/youtube/transcript_tools.py fetch VIDEO_ID --out DIR
    python scripts/youtube/transcript_tools.py find DIR/VIDEO_ID.txt "Pinecone|Panco" --video VIDEO_ID
    python scripts/youtube/transcript_tools.py frames VIDEO_ID 281 284 --out DIR
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys
import time
from typing import Iterable

LEAD_IN_SECONDS = 10
TIME_LINE = re.compile(r"^\[(\d+):(\d{2})\]\s*(.*)$")


def fmt_time(seconds: int) -> str:
    """把秒數轉成 ``m:ss`` 字串。

    Args:
        seconds: 秒數(非負整數)。

    Returns:
        例如 ``281`` 轉成 ``"4:41"``。
    """
    return f"{seconds // 60}:{seconds % 60:02d}"


def video_url(video_id: str, seconds: int, lead_in: int = LEAD_IN_SECONDS) -> str:
    """產生可跳到指定時間點的 YouTube 連結(預設提前幾秒開始)。

    Args:
        video_id: YouTube 影片 ID。
        seconds: 目標句出現的秒數。
        lead_in: 提前播放的秒數,避免剛好錯過目標句。

    Returns:
        帶 ``&t=`` 參數的完整網址。
    """
    return f"https://www.youtube.com/watch?v={video_id}&t={max(0, seconds - lead_in)}s"


def parse_vtt(text: str) -> list[tuple[int, str]]:
    """把 WebVTT 字幕轉成 ``(起始秒, 文字)`` 清單並去除連續重複行。

    Args:
        text: ``.vtt`` 檔的全文。

    Returns:
        依時間排序的 ``(秒, 文字)`` 清單。
    """
    out: list[tuple[int, str]] = []
    prev = None
    for block in text.split("\n\n"):
        m = re.search(r"(\d+):(\d+):(\d+)\.\d+ -->", block)
        if not m:
            continue
        lines = [ln for ln in block.split("\n")[1:] if "-->" not in ln and not ln.startswith(("Kind", "Language"))]
        line = re.sub(r"<[^>]+>", "", " ".join(lines)).strip()
        if line and line != prev:
            out.append((int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]), line))
            prev = line
    return out


def fetch_timed_subs(video_id: str, out_dir: str, retries: int = 4) -> str | None:
    """下載帶時間的字幕並寫成 ``[m:ss] 文字`` 逐行檔。

    Args:
        video_id: YouTube 影片 ID。
        out_dir: 輸出資料夾,檔名為 ``<video_id>.txt``。
        retries: HTTP 429 等錯誤時的重試次數。

    Returns:
        輸出檔路徑;抓不到字幕時回傳 ``None``(此時請改走 Whisper,
        Whisper 輸出本身就帶時間)。
    """
    import yt_dlp

    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.join(out_dir, f"_vtt_{video_id}")
    files: list[str] = []
    for _ in range(retries):
        opts = {
            "quiet": True,
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,  # 無官方字幕時退而用自動字幕(橘鸦Juya 等頻道只有自動字幕)
            "subtitleslangs": ["zh-TW", "zh-Hant", "zh-Hans", "zh-Hans.*", "zh", "en"],
            "subtitlesformat": "vtt",
            "outtmpl": stem,
            "js_runtimes": {"node": {}},
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        except Exception as exc:  # noqa: BLE001 - 429 等暫時性錯誤;已寫出的字幕檔仍可用
            print(f"{video_id} retry: {str(exc)[:80]}", file=sys.stderr)
            if not glob.glob(f"{stem}*.vtt"):
                time.sleep(15)
                continue
        files = glob.glob(f"{stem}*.vtt")
        if files:
            break
        time.sleep(5)
    if not files:
        return None
    rows = parse_vtt(open(files[0], encoding="utf-8").read())
    dest = os.path.join(out_dir, f"{video_id}.txt")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write("\n".join(f"[{fmt_time(s)}] {t}" for s, t in rows))
    for f in files:
        os.remove(f)
    return dest


def find_phrase(path: str, pattern: str, video_id: str | None = None, context: int = 1) -> list[str]:
    """在帶時間的逐字稿中用正規表示式搜尋,回傳含精確時間與連結的結果行。

    Args:
        path: ``[m:ss] 文字`` 格式的逐字稿檔。
        pattern: 正規表示式(例如 ``"Pinecone|Panco"``)。
        video_id: 提供時會附上可點擊連結。
        context: 前後各附帶幾行上下文。

    Returns:
        可直接印出的文字行清單。

    Raises:
        ValueError: 檔案沒有 ``[m:ss]`` 時間標記(代表時間資訊已遺失,
            必須先用 ``fetch`` 或 Whisper 重做,不可猜時間)。
    """
    rows: list[tuple[int, str]] = []
    for ln in open(path, encoding="utf-8"):
        m = TIME_LINE.match(ln.rstrip("\n"))
        if m:
            rows.append((int(m[1]) * 60 + int(m[2]), m[3]))
    if not rows:
        raise ValueError(f"{path} 沒有時間標記,請先 fetch 帶時間字幕或用 Whisper 重轉")
    rx = re.compile(pattern, re.I)
    out: list[str] = []
    for i, (sec, txt) in enumerate(rows):
        if rx.search(txt):
            link = f"  {video_url(video_id, sec)}" if video_id else ""
            out.append(f"== [{fmt_time(sec)}] {txt}{link}")
            for j in range(max(0, i - context), min(len(rows), i + context + 1)):
                if j != i:
                    out.append(f"   [{fmt_time(rows[j][0])}] {rows[j][1]}")
    return out


def extract_frames(video_id: str, seconds: Iterable[int], out_dir: str) -> list[str]:
    """下載 480p 以下影片並在指定秒數截圖。

    Args:
        video_id: YouTube 影片 ID。
        seconds: 要截圖的秒數清單(請用 ``find`` 取得的秒數)。
        out_dir: 輸出資料夾,檔名 ``<video_id>_<秒>.png``。

    Returns:
        成功存檔的 PNG 路徑清單。
    """
    import av
    import yt_dlp

    os.makedirs(out_dir, exist_ok=True)
    opts = {
        "quiet": True,
        "js_runtimes": {"node": {}},
        "remote_components": ["ejs:github"],
        "format": "bestvideo[height<=480]/worst",
        "outtmpl": os.path.join(out_dir, f"{video_id}_v.%(ext)s"),
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
        video_path = ydl.prepare_filename(info)
    container = av.open(video_path)
    saved: list[str] = []
    for sec in seconds:
        container.seek(int(sec) * 1_000_000)
        for frame in container.decode(video=0):
            if frame.time >= sec:
                dest = os.path.join(out_dir, f"{video_id}_{sec}.png")
                frame.to_image().save(dest)
                saved.append(dest)
                break
    container.close()
    os.remove(video_path)
    return saved


def main() -> None:
    """命令列進入點。"""
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("fetch", help="下載帶時間字幕")
    p.add_argument("video_id")
    p.add_argument("--out", required=True)
    p = sub.add_parser("find", help="搜尋片語並印出時間與連結")
    p.add_argument("path")
    p.add_argument("pattern")
    p.add_argument("--video")
    p = sub.add_parser("frames", help="在指定秒數截圖")
    p.add_argument("video_id")
    p.add_argument("seconds", type=int, nargs="+")
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.cmd == "fetch":
        r = fetch_timed_subs(a.video_id, a.out)
        print(r or "NO_SUBS: 請改用 Whisper(輸出自帶時間)")
    elif a.cmd == "find":
        print("\n".join(find_phrase(a.path, a.pattern, a.video)) or "NO_MATCH")
    else:
        print("\n".join(extract_frames(a.video_id, a.seconds, a.out)))


if __name__ == "__main__":
    main()
