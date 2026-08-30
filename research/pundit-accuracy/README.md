# pundit-backtest

用**因果安全**的方式,檢驗財經 YouTuber 到底準不準。

核心約束只有一條:

> **進場價 = 講話時間點之後,第一個「尚未開盤」的交易日開盤價。**

講話當下已經開出來的那根 K 棒不算數。所有時間比較一律在**交易所當地時區**進行,
不用 UTC 日期硬切 —— 一支美東時間 09:45 發布的影片,當天不算,進場日是下一個交易日。

> ⚠️ **教育與研究用途,非投資建議。** 本專案的結論是「某人過去的發言與後續價格的統計關係」,
> 不代表未來表現,也不構成任何買賣建議。

---

## 目錄結構

```
pundit-backtest/
├── src/candlestick.py   # K 線回測工具(因果性守門 + 統計彙總)
├── calls/               # 抽取出來的判斷,JSONL,一行一筆
├── reports/             # 評分報告輸出
├── data/                # 暫存(逐字稿等),不進版控
└── requirements.txt
```

行情快取預設放在 `~/.cache/candlestick/`,可用環境變數 `CANDLESTICK_CACHE` 改。

---

## 安裝

```bash
pip install -r requirements.txt
```

---

## 用法

### 單筆檢查

```bash
python src/candlestick.py check \
  --ticker NVDA \
  --at 2026-06-03T21:30:00+00:00 \
  --direction long \
  --benchmark ^GSPC
```

輸出含各期間的 `raw_return`(原始報酬)、`bench_return`(同期大盤)、
`excess_return`(超額)與 `correct`(對錯)。

### 批次評分

`calls/*.jsonl`,每行一個判斷:

```json
{"source":"某頻道","ticker":"2330.TW","at":"2026-03-01T20:00:00+08:00","direction":"long","quote":"原話節錄","video":"https://youtu.be/..."}
```

```bash
python src/candlestick.py score \
  --calls calls/all.jsonl \
  --out reports/2026-08.json \
  --benchmark ^GSPC \
  --horizon 21d
```

終端機印出各來源的 n / 命中率 / 平均超額 / t 值 / p 值 / BH 校正結果,
完整明細寫進 `--out`。

---

## 方法論上的三個坑(以及本工具怎麼處理)

### 1. 因果性

**坑:** 用「影片日期」當進場日,會把當天早盤已經走完的行情算進預測。

**處理:** `next_tradable_session()` 只接受**開盤時間仍在未來**的交易日。
影片時間戳用 yt-dlp 的 `timestamp`(epoch,精確到秒),不是只有日期的 `upload_date`。

### 2. 大盤本身會漲

**坑:** 長期而言市場多頭居多,所以「看多」這個動作本身就有五成以上的裸命中率。
只看「漲了沒」,會讓所有只會喊多的人自動及格。

**處理:** 預設用**超額報酬**(相對 benchmark)判定對錯,並在彙總裡輸出
`direction_mix` —— 一個只喊多、從不喊空的頻道,一眼就看得出來。

### 3. 多重比較

**坑:** 同時測 10 個頻道、挑出最準的那個,幾乎保證會找到「看起來很準」的人,
即使所有人都只是在丟銅板。

**處理:** `benjamini_hochberg()` 控制錯誤發現率;`score` 子命令會自動對所有來源的
p 值做 BH 校正,輸出 `significant_after_bh` 欄位。**沒過 BH 的頻道,不要當成「準」。**

另外:`aggregate()` 一律回傳 `n`。**n 小於 30 時 hit_rate 沒有討論價值**,
請看 `ci95`(bootstrap 95% 信賴區間)的寬度。

---

## 還沒解決的問題

- **判斷的抽取本身是主觀的。** 多數財經內容用的是不可證偽的措辭
  (「可能會回檔」「要注意風險」)。抽取時必須把這類語句標為 non-falsifiable 並排除,
  否則等於在評分自己的閱讀理解。
- **只評「說了什麼」,沒評「說了多重」。** 沒有部位大小,就沒有真正的績效。
- **倖存者偏誤。** 刪片、改標題、停更的頻道不會出現在樣本裡。
