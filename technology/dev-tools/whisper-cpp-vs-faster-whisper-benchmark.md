# whisper.cpp vs faster-whisper:本機 CPU 轉錄 Benchmark(中英文速度與準確度)

> 自製 benchmark:兩個都宣稱「比原版 OpenAI Whisper 快」的推論實作——**whisper.cpp**(C/C++,經 `pywhispercpp` 綁定)與 **faster-whisper**(CTranslate2 後端,我們原本在用的)——在**本機 CPU** 上對同一批中/英文音訊做轉錄,比較**速度**與**準確度**,決定未來用哪個當預設 transcribe 引擎。

---

## 一句話結論

**同樣 small 模型下,兩者準確度幾乎相同(都受 small 模型限制、錯誤模式一致),但 whisper.cpp 明顯更快——中文 1.9×、英文 1.4×。** 即使 whisper.cpp 需要先把音訊轉成 16kHz wav(本機無系統 ffmpeg,用已裝的 **PyAV** 轉,開銷僅 **0.5 秒**可忽略),端到端仍大幅勝出。

> ⚠️ **但有一個會毀掉整份逐字稿的致命前提(實戰踩雷後補充,見下方「重大踩雷」):whisper.cpp 沒有內建 VAD,遇到背景音樂/長靜音/純配樂段會陷入「幻覺迴圈」——同一句話重複幾百行,整篇報廢。** 所以**不是無腦換 whisper.cpp**,而是:**乾淨人聲(演講/單人解說)→ whisper.cpp(快);有背景音樂/旁白配樂/雜訊的影片 → faster-whisper(`vad_filter=True`,穩)。**

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

## 重大踩雷:whisper.cpp 無 VAD → 背景音樂/靜音段「幻覺迴圈」

benchmark 用的是**乾淨人聲**素材,所以沒暴露這個問題;但在一支**帶背景配樂的財經敘事影片**(社交套利,~39 分鐘)實測時踩了大雷:

- **現象**:whisper.cpp 從某個轉場配樂段開始,**把同一句話「我剛剛在中國爆發的那個時候…」連續重複了數百行**(line 280 一路壞到結尾),整份逐字稿從中段全毀、無法使用。
- **根因**:**whisper.cpp(pywhispercpp)沒有內建 VAD(語音活動偵測)**。當某段沒有語音(純配樂、長靜音、雜訊)時,Whisper 模型仍被迫「解碼出文字」,就會吐出上一段的殘留並陷入自我重複的**幻覺迴圈(hallucination loop)**。
- **faster-whisper 為何沒事**:它的 `vad_filter=True` 會**先用 Silero VAD 把非語音段切掉**,根本不丟給模型解碼,從源頭杜絕了這種迴圈。用 faster-whisper 重轉同一支影片即乾淨正常。
- **教訓**:速度數字漂亮 ≠ 可直接上線。**「會不會在無語音段崩掉」對真實 YouTube 影片(幾乎都有片頭/轉場配樂)比「快 1.9×」更關鍵。**

> 結論不是推翻 whisper.cpp,而是**按素材分流**:單人乾淨講話用 whisper.cpp 賺速度;只要影片有配樂/旁白/雜訊就走 faster-whisper 的 VAD。不確定時,**預設走 faster-whisper(穩),確定是乾淨人聲再切 whisper.cpp(快)**。

---

## 實用性對比(決定預設的關鍵)

| 面向 | faster-whisper | whisper.cpp(pywhispercpp) |
|---|---|---|
| 速度 | 基準 | **快 1.4–1.9×** |
| 準確度(同模型) | 基準 | **相當** |
| 輸入格式 | **直接吃 mp4/m4a/webm(PyAV 內建)** | 需 16kHz wav → 用 PyAV 轉(僅 0.5s) |
| 系統 ffmpeg | 不需要 | 不需要(PyAV 轉 wav 繞過) |
| 內建 VAD | **有(`vad_filter`,防幻覺迴圈)** | **無 → 背景音樂/靜音段會幻覺迴圈報廢** |
| 安裝 | 已裝 | `pip install pywhispercpp`(有預編譯 wheel,免 cmake) |
| 適用素材 | **任何影片(含配樂/雜訊)都穩** | **僅限乾淨人聲** |

> faster-whisper 的 VAD **不是可有可無的便利,而是真實 YouTube 影片的剛需**——大多數影片都有片頭/轉場配樂,whisper.cpp 無 VAD 會在那些段落幻覺迴圈。VAD 只對「全程乾淨人聲」的素材才可省略。

---

## 結論與決策

- **按素材分流,不要無腦二選一**:
  - **乾淨人聲(單人演講/解說、無配樂)→ whisper.cpp(`pywhispercpp` + `ggml-small`)+ PyAV 轉 16kHz wav**,賺 1.4–1.9× 速度。
  - **有背景音樂/旁白配樂/雜訊的影片(多數 YouTube 影片)→ faster-whisper + `vad_filter=True`**,避免無 VAD 的幻覺迴圈。
  - **拿不準時預設走 faster-whisper(穩),確定乾淨人聲再切 whisper.cpp(快)。**
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
