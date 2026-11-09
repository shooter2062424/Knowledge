# 在 Mac mini 上免費跑 MiniMax H3 影片生成:vpipe 實測、授權陷阱與買機建議(AI 策略室)

> **來源影片:** 〈24G 的 Mac mini 跑免費本地 AI 影片生成?MiniMax H3 真機實測加生成教學一次看完〉AI 策略室,2026-11-04 上傳,約 8 分 30 秒([VzO6PZeEkT8](https://youtu.be/VzO6PZeEkT8))。
> **整理方式:** 該片無字幕,逐字稿以 Whisper large-v3-turbo 轉錄(非官方字幕),時間點取自 `[m:ss]`,連結提前 10 秒。再讀了 MiniMax 官方部落格、Hugging Face 模型頁與授權全文、vpipe 與 h3.c 兩個 repo(已 clone 讀完,暫存已刪)、Apple 官方規格頁,逐項標「已核實 / 需修正 / 未能核實」。
> **利益揭露:** 說明欄只列官方連結與工具,沒有業配字樣;片尾導向自家頻道其他本地 AI 教學,屬頻道自家導流。影片以「公司剛買的」Mac mini 實測,數字為作者自測。

## 一、一句話結論

**MiniMax H3 的開源權重已可在 Apple Silicon Mac 上用 vpipe 免費跑,16GB 起跳、24GB 比較實用;但「免費」要付出 180GB 暫存硬碟、數小時準備、每支短片 5–11 分鐘等待,而且授權把美國、歐盟、英國、韓國排除在外。**畫質上限是 768p,官方 2K 那一段沒有開源。

```mermaid
flowchart LR
    A["Vpipe Manager<br/>下載並啟動伺服器"] --> B["瀏覽器介面<br/>匯入官方流程檔"]
    B --> C["按一次準備 H3<br/>下載並轉成 8 位元"]
    C --> D["第一支<br/>文字生影片"]
    D --> E["時裝廣告<br/>分兩段:文字生影片加圖生影片"]
    E --> F["合併流程接起來"]
    F --> G["後製:放大、剪輯字幕<br/>旁白、配樂"]
```

## 二、影片重點與逐項核實

### 1. MiniMax H3 是什麼([從 1:40 開始](https://youtu.be/VzO6PZeEkT8?t=100))

| 影片說法 | 查證 | 結論 |
|---|---|---|
| 2026 年 7 月底發表,畫面和聲音一次生成,立體聲([1:50]) | 官方部落格日期 2026-07-31,寫「native stereo sound」 | ✅ 已核實 |
| 官方 API 最高 2K、最長 15 秒([2:04]) | 部落格:「up to 15 seconds at 2K resolution」 | ✅ 已核實 |
| 2K 每秒價格不到主流模型的 1/3([2:08]) | 部落格寫「less than a third of mainstream models」,但**沒有給實際價格**;768p 對主流 720p 寫不到一半 | ⚠️ 廠商自述,無價格可驗 |
| 開源版畫質預設 768p,直橫式都能做([2:14]) | HF 模型頁:短邊預設 768,H3-Base 輸出 768p | ✅ 已核實 |
| 官方的幾種生成方式開源版都有,只有放大到 2K 的那一部沒開源([2:24]) | HF 頁列 T2VA、FL2VA(首尾幀)、Ref2VA(圖、影片、音訊參考);H3-Regenerate-2K 明寫 not yet open-sourced | ✅ 已核實 |
| 模型體量 | HF 頁:33B dense(影片沒講) | 補充 |

補充:部落格說 2K 是靠「H3-In-context Regeneration」讓基礎模型重生自己的低解析輸出,**不是傳統超解析度模組**,所以影片說的「放大到 2K 那一部」是口語簡化。

### 2. 授權:影片講了一半([從 2:27 開始](https://youtu.be/VzO6PZeEkT8?t=147))

影片說:台灣可用、小公司可商用、發佈要標示 AI 生成、美國歐盟英國韓國不在授權範圍([2:37]–[2:46])。讀授權全文(MiniMax H3 Community License Agreement):

- **地區:**「worldwide, excluding the Excluded Territories」,排除地為歐盟、英國、南韓、美國;範圍外使用「not authorized」,需另向 MiniMax 申請(逐案)。✅ 與影片一致。台灣不在排除清單,所以屬適用範圍;這是我對條文的讀法,不是法律意見。
- **商用門檻:** 商用產品與服務年營收**超過 2,000 萬美元**需另取得書面授權。影片只說「小公司可商用」,✅ 方向對,但沒給數字。
- **標示:** 授權鼓勵為檔案加 AI 生成識別碼;附件 A 第 12 項禁止在**公開傳播**時不清楚標明是機器生成。✅ 影片「發佈要標明」屬實。
- **⚠️ 影片沒提的一條:** 商用產品的使用者介面要**顯著標示「MiniMax H3」**(Section IV.2)。若你做的是對外產品而不只是自己發片,這條要注意。

### 3. 在 Mac 上用哪個 App([從 2:38 開始](https://youtu.be/VzO6PZeEkT8?t=158))

影片比較四種:ComfyUI(主要跑 Windows 加 NVIDIA,Mac 上跑 H3 很慢)、Draw Things(點按鈕)、h3.c(工程師寫的命令列)、vpipe([2:54]–[3:10]),最後選 vpipe。

- **vpipe:** 已核實是專為 Apple Silicon 寫的本地多模態推論,README 寫「custom Metal inference」,**forward 路徑不經第三方張量執行環境**,授權 Apache-2.0。✅ 與影片「繞過那一層直接叫 GPU」一致。
- **h3.c(antirez):** repo 名稱 `h3-metal`,README 寫 Apple Silicon 原生推論,支援文字生影片、首尾幀、Ref2VA,並有 `--ssd-streaming` 低記憶體模式(同時只放兩個 DiT 區塊在記憶體,從 SSD 讀下一塊)。✅ 影片說它是「命令列小程式」屬實。
- 「ComfyUI 在 Mac 上跑 H3 很慢」:**未能核實**,我沒有找到對照數據。
- 「Draw Things 點按鈕就能用」:**未逐項核實**(我沒有讀其官網內容)。

### 4. 要準備什麼([從 3:43 開始](https://youtu.be/VzO6PZeEkT8?t=223))

| 影片說法 | vpipe 文件 | 結論 |
|---|---|---|
| 記憶體 16GB 以上 | 「16 GB minimum」 | ✅ |
| 硬碟先空約 180GB,準備好後約 65GB([4:00]) | 準備峰值約 180GB、8 位元模型刪來源後約 65GB(來源 repack 約 115GB) | ✅ |
| 記憶體不夠時它會直接拒絕,不會硬跑到當機([3:32]) | 文件寫在 16GB 機器上會「refuse at that size rather than thrash」 | ✅ |
| 第一次準備下載加轉檔約 4 小時([4:10]) | 取決於網速,作者自述 | ⚠️ 自測,不具普遍性 |
| macOS 26 以上、Vpipe Manager 免費約 40MB | 我沒在文件中找到對應條文 | 未能核實 |

### 5. 動手做:兩支片([從 4:18 開始](https://youtu.be/VzO6PZeEkT8?t=258))

**第一支(橘貓翻鬆餅)**:提示詞依序寫主角、動作、鏡頭、聲音(音效與配樂寫在同一段),寬 544、高 960 直式,格數 192(24fps 即 8 秒),按開始,約 11 分鐘([4:48]–[5:08])。

**時裝廣告(重做官方 15 秒 8 鏡頭那支)**([從 5:10 開始](https://youtu.be/VzO6PZeEkT8?t=310)):切成兩段,在官方換鏡頭的 7.5 秒處分開。第一段文字生影片;第二段用第一段**兩位模特背影那一格**存成圖,當圖生影片的首幀,這樣衣服才會一致([6:13]–[6:24]);最後用 vpipe 合併流程接起來([6:44])。

**重點心得:** 長片不要一次生,**拆段、用上一段的畫面當下一段的首幀**,是在小記憶體機器上保持角色一致的做法。

### 6. 速度與買機建議([從 7:25 開始](https://youtu.be/VzO6PZeEkT8?t=445))

影片:同一段 5 秒的片,64G 的 M4 Pro 要 17 分多,24G 的 M5 Pro 筆電只要 5 分半,所以「錢先加在晶片,記憶體 24G 夠用」([7:43]–[7:52])。

- ✅ **數字對得上 vpipe 文件。** 同一個 960×544、124 格(約 5.2 秒)、6 步:M4 Pro Mac mini 64GB 總計 **17 分 43 秒**,M5 Pro MacBook Pro 16 吋 24GB **5 分 29 秒**。M5 Pro 峰值記憶體 18.2GB,所以 24GB 夠。
- 補充一點影片沒說的:文件的 M5 Pro 是 **MacBook Pro**,不是 Mac mini;風扇與散熱不同,**Mac mini M5 Pro 的同款對照文件沒有**。
- 影片說的「24G Mac mini 8 秒直式 11 分鐘」([0:25]):**自測,未能獨立核實**。文件對 5.2 秒版本給 5 分鐘(M5 Pro 筆電),8 秒約為 1.5 倍格數,11 分鐘不算離譜,但幀尺寸與設定不同,不能直接換算。
- 影片稱「Mac mini M5 Pro、18 核 CPU、20 核 GPU、24G」([1:33]–[1:38]):Apple 台灣規格頁確認 M5 Pro 款有「18 核心 CPU 與 20 核心 GPU」升級選項,基本記憶體 24GB。✅
- 「預算有限,入門 M6 也能跑,只是比較慢」([7:58]):Apple 頁確認入門款是 M6(12 核 CPU、12 核 GPU),基本 16GB。✅ 能跑與否看 16GB 夠不夠做你要的尺寸;文件在 16GB 機器上有測 3.75 秒到 5.2 秒短片(M5 Air:9 分 26 秒與 11 分 25 秒)。
- 「網路上有人說 Mac 跑 H3 五秒要等半小時」([0:18]):**未能核實**,影片沒指出來源。

### 7. 做完之後還要哪些工具([從 7:04 開始](https://youtu.be/VzO6PZeEkT8?t=424))

放大到 1080p(Flash V SR)、剪輯加字幕(FFmpeg 與 Whisper)、自己的聲音旁白(影片逐字稿寫「Twin 3TTS」)、配樂(「AC step」)。

這幾個名稱 Whisper 都轉得不準,下表為**推定**,沒有逐一核實:

| Whisper 寫法 | 推定 |
|---|---|
| Mii Max H3、Mac Pop H3 | MiniMax H3、Mac 跑 H3 |
| ConfUI、Convi UI | ComfyUI |
| DRADEX | Draw Things |
| V-Pipe、V-Pine | vpipe(說明欄寫 vpipe) |
| Flash V SR | FlashVSR(推定) |
| Twin 3TTS | Qwen3-TTS(推定) |
| AC step | ACE-Step(推定) |
| Fmpeg | FFmpeg |
| N4 Pro | M4 Pro(上下文與文件對得上) |
| 橘貓翻棕餅 | 橘貓翻鬆餅(推定) |

## 三、批判與限制

1. **「免費」是不含時間成本的免費。** 180GB 暫存、數小時準備,以及每支片 5–11 分鐘,只適合少量嘗試;要大量產出,官方 API 的付費版仍有速度與 2K 優勢。
2. **畫質上限 768p 以下,影片自己也承認「雖然不完美」**([0:59])。成品是否可用於商業用途,取決於觀眾對畫質的期待。
3. **效能數字多半來自 vpipe 作者自己的測試**,不是第三方,且 M5 Pro 欄位文件自述「風扇、時脈固定」較穩,M5 Air 欄位依冰袋位置會有波動。換機型請用自己的機器重測。
4. **授權不是「開源就能隨便用」。** 地區排除、營收門檻、標示義務都是真條款;台灣之外的讀者請先看自己所在地。

## 四、應用案例

- **自媒體小量產出:** 想為每集知識影片做 8 秒片頭動畫的創作者,可以在晚上睡前排隊跑 5–10 支(每支 11 分鐘),隔天挑最好的一支,再用 FFmpeg 加字幕;這樣不用付每秒計價的 API。
- **角色一致的長片:** 要做 15 秒廣告,不要一次生 15 秒,而是仿影片的做法在中段分開,第一段最後一幀當第二段首幀,兩段合併。
- **買機決策:** 預算有限、只想試試看,16GB 入門款能跑短片;打算長期做,預算優先放在晶片等級,而不是一次拉滿記憶體。

## 來源

- 〈24G 的 Mac mini 跑免費本地 AI 影片生成?MiniMax H3 真機實測加生成教學一次看完〉AI 策略室:[youtu.be/VzO6PZeEkT8](https://youtu.be/VzO6PZeEkT8)(該片無字幕,逐字稿以 Whisper large-v3-turbo 轉錄,非官方字幕)
- [MiniMax H3 發表(官方部落格)](https://www.minimax.io/blog/minimax-h3)
- [MiniMax-H3 模型頁(Hugging Face)](https://huggingface.co/MiniMaxAI/MiniMax-H3)與[授權全文](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE)
- [vpipe 原始碼](https://github.com/tgo-app-dev/vpipe)與其 [MiniMax H3 說明文件](https://github.com/tgo-app-dev/vpipe/blob/main/docs/MINIMAX-H3.md)
- [h3.c(antirez)](https://github.com/antirez/h3.c)
- [Apple Mac mini 規格(台灣)](https://www.apple.com/tw/mac-mini/specs/)
