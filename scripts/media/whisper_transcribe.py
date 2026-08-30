#!/usr/bin/env python3
"""用 CPU 版 faster-whisper 把影片或音訊轉成逐字稿。

適用情境:YouTube 影片沒有官方字幕也沒有自動字幕時的最後手段。
可直接吃 `.webm` / `.m4a` / `.mp4` 原始檔 —— faster-whisper 透過 PyAV 解碼,
**不需要系統安裝 ffmpeg**。

預設參數是踩過坑之後定下來的:
    * ``vad_filter=True``      先切掉非語音段,避免片頭配樂造成幻覺
    * ``condition_on_previous_text=False`` 與 ``no_repeat_ngram_size=3``
      兩者合力壓制「同一句重複數十行」的迴圈

用法:
    python scripts/media/whisper_transcribe.py audio.webm
    python scripts/media/whisper_transcribe.py audio.webm -o out.txt --model medium
    python scripts/media/whisper_transcribe.py *.webm --outdir transcripts/

注意:
    轉完務必掃一眼結尾。若出現同一句重複數十行,那是幻覺迴圈,
    本模組的 :func:`detect_hallucination_loop` 會偵測並警告。
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, Iterator, NamedTuple

# 預設模型。small 在中文口播上準確度與速度的平衡點最好;
# 品質不足時可換 medium(約慢一倍),但換模型救不了 small 的同音錯字問題。
DEFAULT_MODEL = "small"

# 幻覺迴圈的判定門檻:結尾 N 行裡同一句出現超過 M 次即視為迴圈。
_LOOP_TAIL_LINES = 80
_LOOP_THRESHOLD = 25


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
    """把 stdout/stderr 切成 UTF-8。

    Windows 終端機預設 cp950,印出中文檔名或逐字稿會直接
    ``UnicodeEncodeError`` 並中斷整支腳本(不只是亂碼而已)。
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except Exception:  # pragma: no cover - 某些環境沒有 reconfigure
            pass


def format_timestamp(seconds: float) -> str:
    """把秒數格式化成 ``[MM:SS]``。

    Args:
        seconds: 起始秒數。

    Returns:
        形如 ``[03:07]`` 的字串;超過一小時仍以分鐘累計(例如 ``[75:12]``)。
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"[{minutes:02d}:{secs:02d}]"


def transcribe(
    audio_path: str | Path,
    *,
    model_size: str = DEFAULT_MODEL,
    language: str = "zh",
    threads: int = 6,
    beam_size: int = 5,
) -> Iterator[Segment]:
    """轉錄單一音訊/影片檔,逐段產出結果。

    以 generator 回傳,呼叫端可以邊轉邊寫檔,不必等整支跑完才有輸出。

    Args:
        audio_path: 音訊或影片檔路徑。可直接給 ``.webm``/``.m4a``/``.mp4``,
            不需要事先轉檔。
        model_size: faster-whisper 模型代號,如 ``small``、``medium``。
            首次使用會自動下載。
        language: 語音的語言代碼。中文影片給 ``zh``;若原音是英文,
            即使頻道是中文的,轉出來也會是英文。
        threads: CPU 執行緒數。與其他重運算工作並行時建議調低,避免互搶。
        beam_size: beam search 寬度。調大略微提升準確度、代價是變慢。

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
    except ImportError as exc:  # pragma: no cover - 取決於執行環境
        raise ImportError("需要 faster-whisper:pip install faster-whisper") from exc

    # int8 量化在 CPU 上是速度與記憶體的最佳解,對中文口播的準確度影響很小。
    model = WhisperModel(model_size, device="cpu", compute_type="int8", cpu_threads=threads)

    segments, _info = model.transcribe(
        str(path),
        language=language,
        vad_filter=True,                 # 切掉非語音段,防配樂觸發幻覺
        condition_on_previous_text=False,  # 不讓前文影響後文,避免錯誤滾雪球
        no_repeat_ngram_size=3,          # 壓制重複片語
        beam_size=beam_size,
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
    """偵測結尾是否出現幻覺迴圈。

    Whisper 在長靜音或背景音樂處可能陷入「同一句重複數十行」的迴圈,
    整篇逐字稿會因此報廢。這個檢查只看結尾,因為迴圈幾乎都發生在尾端。

    Args:
        lines: 逐字稿的每一行(可含時間戳前綴,比較時不影響結果)。
        tail_lines: 只檢查最後幾行。
        threshold: 同一行重複幾次以上就判定為迴圈。

    Returns:
        判定為迴圈時回傳那句重複的文字,否則回傳 ``None``。
    """
    tail = [line.strip() for line in list(lines)[-tail_lines:] if line.strip()]
    if not tail:
        return None
    text, count = Counter(tail).most_common(1)[0]
    return text if count >= threshold else None


def transcribe_to_file(
    audio_path: str | Path,
    output_path: str | Path,
    *,
    model_size: str = DEFAULT_MODEL,
    language: str = "zh",
    threads: int = 6,
    with_timestamps: bool = True,
) -> int:
    """轉錄並寫入純文字檔。

    邊轉邊 flush,長影片中途中斷時已完成的部分仍會留在檔案裡。

    Args:
        audio_path: 音訊或影片檔路徑。
        output_path: 輸出的 ``.txt`` 路徑,以 UTF-8、LF 換行寫入。
        model_size: 模型代號。
        language: 語言代碼。
        threads: CPU 執行緒數。
        with_timestamps: 是否在每行前面加 ``[MM:SS]`` 時間戳。

    Returns:
        實際寫出的行數。
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        for seg in transcribe(
            audio_path, model_size=model_size, language=language, threads=threads
        ):
            line = f"{format_timestamp(seg.start)} {seg.text}" if with_timestamps else seg.text
            fh.write(line + "\n")
            fh.flush()  # 中途中斷也保住已完成的部分
            lines.append(seg.text)

    looped = detect_hallucination_loop(lines)
    if looped:
        print(f"  ⚠️ 疑似幻覺迴圈,結尾重複:{looped[:40]}", file=sys.stderr)
    return len(lines)


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
    parser.add_argument("inputs", nargs="+", help="音訊或影片檔(可多個)")
    parser.add_argument("-o", "--output", default=None, help="輸出檔;僅單一輸入時有效")
    parser.add_argument("--outdir", default=None, help="輸出目錄;多檔輸入時使用")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"模型代號(預設 {DEFAULT_MODEL})")
    parser.add_argument("--language", default="zh", help="語言代碼(預設 zh)")
    parser.add_argument("--threads", type=int, default=6, help="CPU 執行緒數(預設 6)")
    parser.add_argument("--no-timestamps", action="store_true", help="不輸出時間戳")
    args = parser.parse_args(argv)
    _utf8_stdout()

    failures = 0
    for raw in args.inputs:
        src = Path(raw)
        if args.output and len(args.inputs) == 1:
            dest = Path(args.output)
        elif args.outdir:
            dest = Path(args.outdir) / f"{src.stem}.txt"
        else:
            dest = src.with_suffix(".txt")

        print(f"轉錄 {src.name} -> {dest}", flush=True)
        try:
            n = transcribe_to_file(
                src,
                dest,
                model_size=args.model,
                language=args.language,
                threads=args.threads,
                with_timestamps=not args.no_timestamps,
            )
            print(f"  完成,{n} 行", flush=True)
        except Exception as exc:  # noqa: BLE001 - 單檔失敗不該中斷整批
            failures += 1
            print(f"  失敗:{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
