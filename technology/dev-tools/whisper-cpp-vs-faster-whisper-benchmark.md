# whisper.cpp vs faster-whisper:本機 CPU 轉錄 Benchmark(中英文速度與準確度)

> 自製 benchmark:兩個都宣稱「比原版 OpenAI Whisper 快」的推論實作——**whisper.cpp**(C/C++,經 `pywhispercpp` 綁定)與 **faster-whisper**(CTranslate2 後端,我們原本在用的)——在**本機 CPU** 上對同一批中/英文音訊做轉錄,比較**速度**與**準確度**,決定未來用哪個當預設 transcribe 引擎。

---

## 一句話結論

**同樣 small 模型下,兩者準確度幾乎相同(都受 small 模型限制、錯誤模式一致),但 whisper.cpp 明顯更快——中文 1.9×、英文 1.4×。** 即使 whisper.cpp 需要先把音訊轉成 16kHz wav(本機無系統 ffmpeg,用已裝的 **PyAV** 轉,開銷僅 **0.5 秒**可忽略),端到端仍大幅勝出。→ **未來預設改用 whisper.cpp(pywhispercpp)+ PyAV 轉 wav;faster-whisper 留作 fallback。**

---

## 測試設置(力求公平)

| 項目 | 設定 |
|---|---|
| 機器 | Windows 11、16 核 CPU、**無 GPU**、**無系統 ffmpeg** |
| 模型 | **small**(兩邊對等);faster-whisper=`int8` 量化、whisper.cpp=`ggml-small.bin`(fp16) |
| 執行緒 | 兩邊都 **8 threads** |
| 解碼 | 都 beam(faster `beam_size=5`);關閉 VAD 以單純比引擎 |
| 素材 | **中文 5 分鐘**(科技解說,含中英混雜術語)+ **英文 5 分鐘**(蘇姿丰 MIT 演講),各截前 300 秒、轉 16kHz mono wav |
| 計時 | 只計 `transcribe()` wall time;模型載入/下載不計;**單一引擎獨佔 CPU**(等其他背景任務跑完才計時) |

> 註:faster-whisper 是 `int8`、whisper.cpp 是 `fp16`,不是完全對等的量化——理論上 whisper.cpp(fp16)精度應**略高**、速度應**略慢**,但實測 whisper.cpp **又快又不輸準確度**,優勢更明確。

---

## 結果一:速度(whisper.cpp 完勝)

| 引擎 | 中文 5 分(300s) | 英文 5 分(300s) |
|---|---|---|
| **faster-whisper**(small int8) | 136.7s(2.2× 即時) | 89.4s(3.4× 即時) |
| **whisper.cpp**(pywhispercpp, ggml-small) | **72.5s(4.1×)** | **62.3s(4.8×)** |
| **whisper.cpp 加速倍率** | **1.89×** | **1.43×** |

- **PyAV 把 mp4 轉 16kHz wav 的開銷:0.5 秒 / 5 分鐘音訊** → 對 whisper.cpp 的端到端時間幾乎無影響(中文 73.0s vs faster 136.7s,仍快近一倍)。
- 中文加速幅度比英文大(中文解碼較吃力,whisper.cpp 的 C++ 實作優勢更明顯)。
- **對長影片放大優勢**:一支 32 分鐘音訊,faster-whisper 約需十幾分鐘,whisper.cpp 可省下接近一半時間。

## 結果二:準確度(幾乎相同,各有微小勝負)

兩者都是 small 模型,**主要錯誤是 small 模型本身的限制,兩引擎一致**(非引擎差異)。

**中文**(同音/術語):
- 兩者共有的 small 模型錯誤(同樣出現):賦能→「負能」、井然有序→「謹然/僅然」、對講機→「破對獎勢」、毫秒級→「豪妙期」、引以為傲→「擬有惟傲」。
- 差異點打平:`電焊`(whisper.cpp ✅ / faster ❌「電汗」);`零星火花`(faster ✅ / whisper.cpp ❌「靈星」);**英文術語 `issue`**(faster ✅ 保留英文 / whisper.cpp ❌「一宿」)。
- → 中文兩者品質相當;faster 在「中英混雜時保留英文詞」略好,whisper.cpp 在部分中文詞略好。

**英文**(蘇姿丰演講,本就好轉):
- 兩者幾乎逐字相同、都很準。
- 人名:`Anantha`(faster ✅ 接近正確 / whisper.cpp「Ananda」);`Gorenberg`/`Gorinberg`(難分);兩者都把 MIT 的 `UROP` 聽錯(faster「Europe」/ whisper.cpp「year up」)。
- whisper.cpp **會標 `[APPLAUSE]`** 等非語音事件(視需求是優點或雜訊)。
- → 英文兩者準確度無實質差異。

**小結**:**準確度打平**;要更準的唯一辦法是兩者都換 `medium` 模型(代價是更慢),而非換引擎。

---

## 實用性對比(決定預設的關鍵)

| 面向 | faster-whisper | whisper.cpp(pywhispercpp) |
|---|---|---|
| 速度 | 基準 | **快 1.4–1.9×** |
| 準確度(同模型) | 基準 | **相當** |
| 輸入格式 | **直接吃 mp4/m4a/webm(PyAV 內建)** | 需 16kHz wav → 用 PyAV 轉(僅 0.5s) |
| 系統 ffmpeg | 不需要 | 不需要(PyAV 轉 wav 繞過) |
| 內建 VAD | **有(`vad_filter`)** | 無(需自理或不用) |
| 安裝 | 已裝 | `pip install pywhispercpp`(有預編譯 wheel,免 cmake) |

> faster-whisper 唯二的便利(直接吃原始檔、內建 VAD)在「PyAV 轉 wav 只要 0.5 秒」面前不構成障礙;VAD 對乾淨的演講/解說音訊影響不大。

---

## 結論與決策

- **未來預設轉錄引擎改為 whisper.cpp(`pywhispercpp` + `ggml-small`)**,搭配 **PyAV 把音訊轉 16kHz mono wav** 的前處理。理由:**速度快近 2 倍、準確度相同、轉 wav 開銷可忽略**。
- **faster-whisper 保留為 fallback**(若某環境 `pywhispercpp` 跑不動,或需要內建 VAD)。
- **要更高準確度** → 兩者都升 `medium` 模型(換引擎救不了 small 的同音錯字)。
- 已同步更新 Knowledge `CLAUDE.md` 的 YouTube 轉錄流程與記憶 [[youtube-whisper-fallback]]。

---

## 複現方式

```python
# 1) 用 PyAV 把任意音訊轉 16kHz mono wav(免系統 ffmpeg)
import av, numpy as np, wave
cont = av.open('audio.mp4'); st = cont.streams.audio[0]
rs = av.AudioResampler(format='s16', layout='mono', rate=16000)
frames = [rf.to_ndarray().reshape(-1) for f in cont.decode(st) for rf in rs.resample(f)]
data = np.concatenate(frames).astype(np.int16)
with wave.open('audio.wav','wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000); w.writeframes(data.tobytes())

# 2) whisper.cpp 轉錄(pywhispercpp,首次會自動下載 ggml-small)
from pywhispercpp.model import Model
m = Model('small', n_threads=8, language='zh', print_realtime=False, print_progress=False)
text = ' '.join(s.text.strip() for s in m.transcribe('audio.wav'))
```

---

## 來源 / 工具

- whisper.cpp(ggerganov):<https://github.com/ggml-org/whisper.cpp>;Python 綁定 `pywhispercpp` 1.5.0(預編譯 wheel)。
- faster-whisper(SYSTRAN,CTranslate2 後端):<https://github.com/SYSTRAN/faster-whisper>。
- 測試音訊:本機既有的兩支 YouTube 影片音訊(中文科技解說 + 蘇姿丰 MIT 演講英文原音)各前 5 分鐘;benchmark 為單機單次量測,數字會隨機器/負載浮動,但兩引擎相對差距穩定。
