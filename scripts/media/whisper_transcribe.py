#!/usr/bin/env python3
"""語音轉文字的統一入口:固定使用 faster-whisper ``large-v3-turbo``(CPU、int8)。

**全倉庫(包含排程與其他 LLM / subagent)要轉錄影片或音訊,一律呼叫本腳本**,
不要自己 inline 寫 ``WhisperModel(...)``,也不要換成 ``small`` 或其他模型。
這樣引擎、參數、輸出格式只有一份,改進時只改這裡。

模型固定的理由(2026-11-07 實測,i7-1260P CPU):large-v3-turbo 比 small 只慢約 1.5 倍,
但明顯更準(Java、向量資料庫、云原生都聽對);專有名詞仍會錯,所以要搭配
``--prompt`` 的詞表(標題、說明欄、人名、工具名)與影片畫面校正。

輸入可以是:
    * 本機音訊/影片檔(``.webm`` ``.m4a`` ``.mp4`` ``.wav`` 等,PyAV 解碼,不需 ffmpeg)
    * YouTube 影片 ID 或網址(自動下載音訊到暫存資料夾,轉完刪除)

**詞表提示(``--prompt``)預設不要帶**(2026-11-08 十支影片基準:帶標題+說明欄詞表的 CER 6.9% 比不帶的 5.8% 更差,
術語召回幾乎沒提升,說明欄的推廣文字還會污染輸出)。正確流程:先不帶詞表轉錄 → 讀逐字稿,
**只有遇到語句不通順、疑似專有名詞聽錯的段落**,才用 ``--clip 起-迄 --prompt "正確詞表"`` 定點重轉那一小段並取代。

輸出為 ``[m:ss] 文字`` 逐行檔(與 ``scripts/youtube/transcript_tools.py find`` 相容),
最後一行印出 ``segments N``;成敗以這個數字為準(stderr 的 numpy 警告可忽略)。

用法:
    python scripts/media/whisper_transcribe.py oH0j8HYeMAM -o out.txt \
        --prompt "Claude Code、Anthropic、Projects、subagent"
    python scripts/media/whisper_transcribe.py audio.webm -o out.txt --prompt-file words.txt
    python scripts/media/whisper_transcribe.py a.webm b.webm --outdir transcripts/
    python scripts/media/whisper_transcribe.py talk.mp4 --language auto   # 自動偵測語言

注意:
    * 一律「前景」執行,不要 ``nohup … &``(背景 shell 環境不完整,torch/numpy 會失敗)。
      長片超過 10 分鐘會被轉成背景工作,等完成通知即可。
    * 轉完看結尾有無「同一句重複數十行」(幻覺迴圈);本腳本會偵測並警告。
    * VAD 會切掉非語音段;中文旁白與英文原聲交疊的影片可能有時間缺口,缺口處以畫面為準。
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Iterable, Iterator, NamedTuple

# 固定模型。不提供 --model 參數:要換模型代表要改這個常數並重做基準,而不是各處各自指定。
MODEL = "large-v3-turbo"

# 幻覺迴圈的判定門檻:結尾 N 行裡同一句出現超過 M 次即視為迴圈。
_LOOP_TAIL_LINES = 80
_LOOP_THRESHOLD = 25

_YOUTUBE_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")


class Segment(NamedTuple):
    """一段轉錄結果。

    Attributes:
        start: 起始秒數。
        end: 結束秒數。
        text: 該段文字(已去除前後空白)。
    """

    start: float
    end: float
    text: str


def _utf8_stdout() -> None:
    """把 stdout/stderr 切成 UTF-8(Windows 預設 cp950 會在印中文時中斷腳本)。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except Exception:  # pragma: no cover - 某些環境沒有 reconfigure
            pass


def format_timestamp(seconds: float) -> str:
    """把秒數格式化成 ``[m:ss]``(與 transcript_tools 相同,超過一小時仍以分鐘累計)。

    Args:
        seconds: 起始秒數。

    Returns:
        形如 ``[3:07]``、``[75:12]`` 的字串。
    """
    total = int(seconds)
    return f"[{total // 60}:{total % 60:02d}]"


def _parse_clip(spec: str) -> tuple[float, float]:
    """解析 ``--clip`` 參數(``起-迄``,各為秒數或 ``m:ss``)。

    Args:
        spec: 例如 ``"120-150"`` 或 ``"2:00-2:30"``。

    Returns:
        ``(起秒, 迄秒)``。

    Raises:
        ValueError: 格式錯誤或迄 <= 起。
    """
    def sec(t: str) -> float:
        parts = [float(x) for x in t.split(":")]
        return parts[0] * 60 + parts[1] if len(parts) == 2 else parts[0]

    a, b = spec.split("-", 1)
    start, end = sec(a), sec(b)
    if end <= start:
        raise ValueError(f"--clip 迄時間必須大於起時間:{spec}")
    return start, end


def is_youtube_ref(value: str) -> bool:
    """判斷輸入是不是 YouTube 影片 ID 或網址(且不是本機存在的檔案)。

    Args:
        value: 命令列輸入。

    Returns:
        是 YouTube 影片 ID(11 字元)或含 youtube.com / youtu.be 的網址時為 True。
    """
    if Path(value).exists():
        return False
    return bool(_YOUTUBE_ID.match(value)) or "youtube.com/" in value or "youtu.be/" in value


def download_audio(ref: str, out_dir: Path) -> Path:
    """用 yt-dlp 下載 YouTube 音訊(原始檔,不需 ffmpeg)。

    ``--remote-components ejs:github`` 是 JS challenge solver,少了它音訊下載常 HTTP 403。

    Args:
        ref: 影片 ID 或網址。
        out_dir: 下載資料夾。

    Returns:
        下載到的音訊檔路徑。

    Raises:
        RuntimeError: 下載失敗(連續三次 403 時先 ``python -m pip install -U yt-dlp``)。
    """
    import yt_dlp

    url = ref if "/" in ref else f"https://www.youtube.com/watch?v={ref}"
    opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        "outtmpl": str(out_dir / "audio.%(ext)s"),
        "js_runtimes": {"node": {}},
        "remote_components": ["ejs:github"],
    }
    last: Exception | None = None
    for _ in range(3):  # 403 用同參數重試,不要改 player_client
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            files = sorted(out_dir.glob("audio.*"))
            if files:
                return files[0]
        except Exception as exc:  # noqa: BLE001
            last = exc
    raise RuntimeError(f"音訊下載失敗:{ref}:{last}")


def transcribe(
    audio_path: str | Path,
    *,
    language: str | None = "zh",
    prompt: str | None = None,
    threads: int = 6,
    beam_size: int = 5,
    clip: tuple[float, float] | None = None,
) -> Iterator[Segment]:
    """轉錄單一音訊/影片檔,逐段產出結果(generator,可邊轉邊寫檔)。

    Args:
        audio_path: 音訊或影片檔路徑。
        language: 語言代碼;中文影片給 ``zh``。``None`` 表示自動偵測。若原音是英文,
            即使頻道是中文的,轉出來也會是英文。
        prompt: 提示詞(``initial_prompt``):放標題、說明欄、人名、工具名等專有名詞詞表,
            能補一部分專有名詞,但不能取代畫面核對。
        threads: CPU 執行緒數。與其他重運算並行時調低。
        beam_size: beam search 寬度。
        clip: ``(起秒, 迄秒)``,只轉錄這個範圍(輸出時間戳仍是整支影片的絕對時間);用於「讀到不通順處」
            的定點重轉,可搭配 ``prompt``。

    Yields:
        依時間排序的 :class:`Segment`。

    Raises:
        FileNotFoundError: ``audio_path`` 不存在。
        ImportError: 環境未安裝 ``faster-whisper``。
    """
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"找不到音訊檔:{path}")
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:  # pragma: no cover
        raise ImportError("需要 faster-whisper:pip install faster-whisper") from exc

    model = WhisperModel(MODEL, device="cpu", compute_type="int8", cpu_threads=threads)
    segments, _info = model.transcribe(
        str(path),
        language=language,
        vad_filter=True,                   # 切掉非語音段,防配樂觸發幻覺
        condition_on_previous_text=False,  # 不讓前文影響後文,避免錯誤滾雪球
        # ⚠️ 不要設 no_repeat_ngram_size:中文 token 很細,它會禁止重複的詞(第二次出現的「調查報告」
        # 被迫寫成「調察」「談查」),實測 CER 8% → 4%(2026-11-08 基準,fA7gNVUkkc8)。
        # 幻覺迴圈改靠 VAD + condition_on_previous_text=False,並由結尾偵測警告。
        beam_size=beam_size,
        initial_prompt=prompt or None,
        clip_timestamps=[clip[0], clip[1]] if clip else "0",
    )
    for seg in segments:
        text = seg.text.strip()
        if text:
            yield Segment(start=seg.start, end=seg.end, text=text)


def detect_hallucination_loop(
    lines: Iterable[str],
    *,
    tail_lines: int = _LOOP_TAIL_LINES,
    threshold: int = _LOOP_THRESHOLD,
) -> str | None:
    """偵測結尾是否出現幻覺迴圈(同一句重複數十行,整篇逐字稿會報廢)。

    Args:
        lines: 逐字稿的每一行(不含時間戳最準)。
        tail_lines: 只檢查最後幾行(迴圈幾乎都發生在尾端)。
        threshold: 同一行重複幾次以上就判定為迴圈。

    Returns:
        判定為迴圈時回傳那句重複的文字,否則 ``None``。
    """
    tail = [line.strip() for line in list(lines)[-tail_lines:] if line.strip()]
    if not tail:
        return None
    text, count = Counter(tail).most_common(1)[0]
    return text if count >= threshold else None


def transcribe_to_file(
    source: str | Path,
    output_path: str | Path,
    *,
    language: str | None = "zh",
    prompt: str | None = None,
    threads: int = 6,
    with_timestamps: bool = True,
    clip: tuple[float, float] | None = None,
) -> int:
    """轉錄(本機檔或 YouTube 參照)並寫入逐行文字檔;邊轉邊 flush。

    Args:
        source: 本機音訊/影片檔路徑,或 YouTube 影片 ID / 網址。
        output_path: 輸出 ``.txt``,UTF-8、LF 換行。
        language: 語言代碼,``None`` 自動偵測。
        prompt: 詞表提示。
        threads: CPU 執行緒數。
        with_timestamps: 是否加 ``[m:ss]`` 前綴。
        clip: 只轉錄 ``(起秒, 迄秒)``,見 :func:`transcribe`。

    Returns:
        實際寫出的行數(segments 數)。
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp: Path | None = None
    try:
        if isinstance(source, str) and is_youtube_ref(source):
            tmp = Path(tempfile.mkdtemp(prefix="stt_"))
            audio = download_audio(source, tmp)
        else:
            audio = Path(source)
        texts: list[str] = []
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            for seg in transcribe(audio, language=language, prompt=prompt, threads=threads, clip=clip):
                line = f"{format_timestamp(seg.start)} {seg.text}" if with_timestamps else seg.text
                fh.write(line + "\n")
                fh.flush()  # 中途中斷也保住已完成的部分
                texts.append(seg.text)
    finally:
        if tmp is not None:
            shutil.rmtree(tmp, ignore_errors=True)
    looped = detect_hallucination_loop(texts)
    if looped:
        print(f"  ⚠️ 疑似幻覺迴圈,結尾重複:{looped[:40]}", file=sys.stderr)
    return len(texts)


def main(argv: list[str] | None = None) -> int:
    """命令列進入點。

    Args:
        argv: 命令列參數;``None`` 時使用 ``sys.argv``。

    Returns:
        行程結束碼,0 表示全部成功。
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("inputs", nargs="+", help="音訊/影片檔,或 YouTube 影片 ID / 網址(可多個)")
    parser.add_argument("-o", "--output", default=None, help="輸出檔;僅單一輸入時有效")
    parser.add_argument("--outdir", default=None, help="輸出目錄;多輸入時使用")
    parser.add_argument("--language", default="zh", help="語言代碼(預設 zh;auto 自動偵測)")
    parser.add_argument("--prompt", default=None, help="詞表提示;預設不要帶(見模組說明),只在讀到不通順處、搭配 --clip 定點重轉時使用")
    parser.add_argument("--clip", default=None, help="只轉錄範圍 起-迄(秒或 m:ss),例:120-150 或 2:00-2:30")
    parser.add_argument("--prompt-file", default=None, help="從 UTF-8 檔讀詞表提示")
    parser.add_argument("--threads", type=int, default=6, help="CPU 執行緒數(預設 6)")
    parser.add_argument("--no-timestamps", action="store_true", help="不輸出時間戳")
    args = parser.parse_args(argv)
    _utf8_stdout()

    prompt = args.prompt
    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8").strip()
    language = None if args.language == "auto" else args.language
    clip = _parse_clip(args.clip) if args.clip else None

    failures = 0
    for raw in args.inputs:
        stem = raw if is_youtube_ref(raw) and "/" not in raw else Path(raw).stem
        if args.output and len(args.inputs) == 1:
            dest = Path(args.output)
        elif args.outdir:
            dest = Path(args.outdir) / f"{stem}.txt"
        else:
            dest = Path(f"{stem}.txt") if is_youtube_ref(raw) else Path(raw).with_suffix(".txt")
        print(f"轉錄 {raw} -> {dest}(模型 {MODEL})", flush=True)
        try:
            n = transcribe_to_file(
                raw, dest, language=language, prompt=prompt,
                threads=args.threads, with_timestamps=not args.no_timestamps, clip=clip,
            )
            print(f"segments {n}", flush=True)
        except Exception as exc:  # noqa: BLE001 - 單檔失敗不該中斷整批
            failures += 1
            print(f"  失敗:{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
