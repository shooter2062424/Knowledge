# Claude Sonnet 5.5:價格不變、效率拉高,以及「檔位開最高反而更差」與五個會報 400 的遷移變更

**主題分類:** 科技 / AI 產業動態 — 模型發布、成本控制、API 遷移
**來源:** YouTube〈Sonnet 5.5 更新了什么?〉(Why QQ,2026-09-29,約 8.5 分;**依官方簡中字幕整理**)
**一手素材核實:** [Anthropic 官方公告](https://www.anthropic.com/claude-sonnet-5-5)(2026-09-28)、[官方遷移指南](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide)、[Simon Willison 部落格](https://simonwillison.net/2026/Sep/28/claude-sonnet-5-5/)
**整理日期:** 2026-09-30

> 📎 同家族的 **Opus 5.5**(2026-09-22)發布背景、價格與跑分,見本庫 [[rsi-recursive-self-improvement-anthropic]] §11;實際做事的差異見 [[opus-5-5-video-agent-tool-selection-self-check]]。

---

## TL;DR

1. ⭐ **定位:** Claude 5.5 家族第二個模型;**價格與 Sonnet 5 完全相同**(輸入 $2、輸出 $10、快取讀取 $0.20 / 百萬 token),**生成快 30% 以上、多數任務最多便宜 30%**。
2. ⭐⭐ **跑分大躍進:** Terminal-Bench 4.0 從 **10.3 → 70.6**(還高於 Opus 5.5 的 66.4);OSWorld 57.0 → 80.1;圖表辨識 15.6 → 61.6。但**開放式、長時程、需要持續判斷的編碼任務,Opus 5.5 仍明顯領先**(FrontierCode 54.4 vs 46.2)。
3. ⭐⭐⭐ **最反直覺的一點:effort 檔位是「成本旋鈕」,不是越高越好。** 官方 FrontierCode 圖上,**xhigh 52.1 分、max 反而掉到 46.2**,token 還多花好幾倍;Simon Willison 的鵜鶘測試,**max 檔燒光 128k 思考 token 還交不出圖**。
4. ⚠️⚠️ **五個會直接回 400 的破壞性變更**,外加幾個「不報錯但會咬人」的行為改變(見 §4)。
5. ⭐⭐ **選型一條線:** 「**你能不能替這個任務寫出自動化的驗收?**寫得出來,Sonnet 夠用;寫不出來,才輪到 Opus。」

---

## 1. 基本盤(✅ 官方公告核實)

| 項目 | 內容 |
|---|---|
| **發布** | 2026-09-28,Claude 5.5 家族第二個模型(排在 Opus 5.5 之後) |
| **價格** | 輸入 **$2**、輸出 **$10**、快取讀取 **$0.20**、快取寫入 $2.50(每百萬 token)——**與 Sonnet 5 相同** |
| **速度 / 成本** | 生成**快 30% 以上**;多數工作**每任務最多便宜 30%** |
| **平台** | Claude API、AWS、Google Cloud、Azure;claude.ai |
| **影片另外提到** | 知識截止 2026 年 6 月、上下文 100 萬、最大輸出 128k、**claude.ai 免費方案同步換成它**、Haiku 5.5 幾週內跟上(⚠️ 本文未逐項核實) |

---

## 2. 跑分:大幅進步,但塔尖仍是 Opus

| 基準 | Sonnet 5 | ⭐ Sonnet 5.5 | Opus 5.5 | 其他 |
|---|---|---|---|---|
| **Terminal-Bench 4.0**(終端多步任務) | 10.3 | ⭐ **70.6** | 66.4 | GPT-6 Astra 57.9(影片) |
| **OSWorld 2.1**(電腦操作) | 57.0 | **80.1** | 81.8 | |
| **Chartography**(圖表辨識) | 15.6 | **61.6** | 64.4 | GPT-6 Sol 53.6 |
| **GDPval-AA**(44 種職業的真實工作) | 1449 | **1844** | 1846 | |
| **CursorBench 4.0** | 34.1 | 55.5 | 57.8 | |
| ⚠️ **FrontierCode 1.1 Main**(Cognition 的編碼基準) | 42.4 | **46.2(max)** | **54.4** | GPT-6 Sol 49.3 |
| Humanity's Last Exam(有工具) | 54.9 | 64.5 | 67.7 | |

- ✅ 「**第一個只靠截圖打通《寶可夢 紅》的 Sonnet**」(官方公告)。
- 影片另提:SWE-Bench Pro 63.2 → 81.3(Opus 5.5 為 89.9)、AutomationBench 44.7 反超 Opus 5.5 的 42.5、HealthBench Professional 69.2 對 65.6 反超 Opus(⚠️ 這三項本文在官方公告頁未找到,未核實)。

> ⭐ Why QQ 的提問:「**Terminal-Bench 大半年從 10 分飆到 70 分,是模型真強了七倍,還是基準本身在通膨?**」——值得放在心上,本庫多篇筆記都提醒過「頭條數字要看條件」。

---

## 3. ⭐⭐⭐ 成本:單價沒變,省的錢全來自 token 效率

### 3.1 客戶實測

| 客戶 | ✅ 官方引述 |
|---|---|
| **Slack** | 沒改任何提示詞,離線評測「幾乎全面優於 Sonnet 5,**步驟更少、輸出 token 少約 14%**」 |
| **Epic Games** | 「在系統設計稽核上達到你預期**更高階模型**才有的品質」 |

影片補充:官方 Terminal-Bench 圖上,**medium 檔的 Sonnet 5.5 就超過 Sonnet 5 的最高分,單任務成本不到十分之一**;早期測試者注意到它會**把工具呼叫打包**,步驟更少。

### 3.2 ⚠️⚠️ effort 是成本旋鈕,不是越高越好

| 證據 | 內容 |
|---|---|
| **Artificial Analysis(影片引)** | low 檔單任務 **$0.41**、max 檔 **$7.60**,差 **18 倍**;智慧指數從 36 爬到 56 |
| ⭐ **官方 FrontierCode 圖(影片引系統卡)** | **xhigh 52.1 分 → max 掉到 46.2 分**,token 還多花好幾倍 |
| ✅ **Simon Willison 的鵜鶘測試** | **max 檔思考 15 分鐘、燒掉 128,000 個思考 token($1.28),把輸出上限用光,一張 SVG 都沒交出來**;同一個 prompt,xhigh 檔 5.7 美分、41 秒就畫好 |

📌 **本文補正:** 影片說鵜鶘測試「超時」;Simon Willison 原文的說法是 **token 用完**——**`max_tokens` 包含思考 token**,max 檔把 128k 上限全花在思考,沒有剩下任何額度寫答案。他也指出 **Opus 5.5 有同樣的問題**。

### 3.3 官方建議怎麼選檔

| 場景 | 建議 |
|---|---|
| Claude Code 預設 | **medium**(影片) |
| API 預設 | **high**(影片) |
| ⭐ agentic coding | **從 medium 起步**,任務變難再升 high |
| xhigh / max | **只留給評測證明真的有提升的場景** |
| ⚠️ 想讓模型少想一點 | **在系統提示裡叫它少思考不可靠,直接降檔才有效** |

---

## 4. ⚠️⚠️ 遷移:五個破壞性變更 + 幾個暗坑(✅ 官方遷移指南核實)

### 4.1 會直接回 400 的五件事

| # | 變更 | 怎麼改 |
|---|---|---|
| **①** | `thinking: {"type": "disabled"}` **回 400** | 改成 `{"type": "between_tools"}`(不做事前思考,只在工具之間思考) |
| **②** | `tool_choice` 的 **`any` 與 `tool` 不再支援** | 改用 `auto`,搭配 **strict 嚴格工具輸入**並自行驗證結果 |
| **③** | 舊版 computer use 工具 `computer_20251124` **在 Claude API 與 Google Cloud 上回 400** | 改用 **`computer_toolset_20260801`** |
| **④** | **advisor 工具**要搭配受支援的 advisor 模型(影片:不再接受 Sonnet 5 當顧問),且建議內容是加密的 | 換成受支援的 advisor |
| **⑤** | **思考區塊綁定模型與對話**:中途換模型,之前的推理就丟了;**2026-08-31 00:00 UTC 之後建立的帳號**,若**修改過歷史訊息再重放思考區塊,直接回 400** | ⭐ **對話保持「只追加、不改寫」** |

### 4.2 不報錯、但會咬人的變化

| 變化 | 影響 | 對策 |
|---|---|---|
| **思考文字預設不回傳**(`thinking` 欄位為空,只有 signature);工具呼叫之間的進度說明也放在 thinking 區塊 | ⚠️ **串流介面會在工具呼叫之間突然安靜**,不報錯 | 設 `display: "summarized"` 取回摘要 |
| **`max_tokens` 包含思考 token** | 預算給太少,答案會被截斷(鵜鶘事件) | agentic coding 建議 `max_tokens` 設到 **128000** 並開串流(影片) |
| **高解析度圖片檔位**:長邊最大 2576 px、每張最多 4,784 個視覺 token | ⚠️ **一張 2000×1500 的圖,token 約是 Sonnet 4.6 時代的 2.5 倍** | 不需要細節就先壓縮 |
| **安全分類器拒答** | 影片:分 cyber、bio 等五類;cyber 類可自動 fallback 到 Sonnet 5,**API 上要手動開啟** | 設定 fallback;正當資安工作可申請 Cyber Verification Program |
| **快取門檻從 1,024 降到 512 token** | ✅ 短系統提示也能快取,讀取只要輸入價的十分之一 | 善用 |

### 4.3 ⚠️ 關於「逐輪換檔」的補正

影片建議:「改頂層 effort 會讓快取失效,想單輪換檔用 per-message effort。」
✅ 官方文件補充了一個條件:**在 `between_tools` 模式下,effort 不能在對話中途改變**——per-message effort 與目前檔位不同會**回 400**。**要逐輪換檔,必須用 adaptive thinking**(不填 `thinking` 欄位或設 `{"type": "adaptive"}`)。

### 4.4 ⭐ 讓 Claude Code 幫你遷移

✅ 官方指南:在 Claude Code 裡執行
```text
/claude-api migrate this project to claude-sonnet-5-5
```
它會替換模型 ID、處理破壞性參數、取代 prefill、校準 effort,**動檔案前會先確認範圍**,最後產出一份要人工確認的清單。

---

## 5. ⭐⭐ 落地五條(影片)

| # | 動作 |
|---|---|
| **①** | 遷移交給 `/claude-api migrate` |
| **②** | **刪掉 Sonnet 5 時代的提示詞補丁**(「別偷懶」、重試 shim),刪完再跑評測 |
| **③** | ⚠️ **low 檔可能沒跑測試就回報完成**——官方給了一段系統提示,要求改動必須跑真實檢查,跑不了要說明原因 |
| **④** | 改頂層 effort 會讓快取失效;要逐輪換檔請用 adaptive thinking(見 §4.3) |
| **⑤** | agentic coding 把 `max_tokens` 設到 128000 並開串流 |

---

## 6. ⭐⭐⭐ 選型表:Sonnet 還是 Opus?

```mermaid
flowchart TB
    T["新任務"] --> Q{"能寫出自動化驗收嗎?<br/>測試、檢查腳本、明確規格"}
    Q -->|"能"| S["Sonnet 5.5<br/>修 bug、迭代功能<br/>寫文件、做簡報<br/>重複性 agent 任務"]
    Q -->|"不能"| O["Opus 5.5<br/>開放、長時程<br/>需要持續判斷"]
    S --> E{"effort 選哪檔?"}
    E --> M["從 medium 起步"]
    M -->|"評測證明有提升"| H["再升 high 或 xhigh"]
    H -.->|"⚠️ max 可能更差更貴"| X["max 只在證明有效時用"]
```

> ⭐⭐ Why QQ:「**規格和驗收,就是這條分工線。**這個標準,以後每次模型發布都能拿出來用。」
> 「**檔位跟著任務走,錢包跟著檔位走。**」

📎 這與 [[claude-code-hooks-complete-guide]] 用 hook 做驗收、[[shopify-helix-checkpoints-and-gates]] 把「完成」寫成關卡,是同一件事的另一面:**驗收寫得越清楚,越能放心用便宜的模型**。

---

## 7. 社群反應(HN 523 讚 / 353 則留言;自述性質)

| 話題 | 內容 |
|---|---|
| **免費方案之爭** | claude.ai 免費用 Sonnet 5.5,ChatGPT 免費用 GPT-6 Luna;Simon Willison 認為 **Anthropic 的免費方案明顯更強** |
| **中國模型價格壓力** | 多則高讚說:這個價位的中階智能,GLM、DeepSeek 只要零頭 |
| **token 需求會不會飽和** | 有人說 Opus 5.5 已吃滿他的工作量;有人回「**十個 agent 並發跑 worktree,燒起來快得很**」 |
| ⚠️ **教訓** | 讓模型自動 review 改動,**二十輪都在重寫同樣的註解** |
| 趣聞 | 一次生成的 Pac-Man 複製品近乎完美,僅次於 Opus |

---

## 8. 應用案例

### 案例一:團隊的 effort 預設值

| 用途 | 模型 | effort |
|---|---|---|
| CI 裡自動修 lint / 型別錯誤 | Sonnet 5.5 | **low 或 medium**(有測試兜底) |
| 日常功能開發 | Sonnet 5.5 | **medium**,卡住再 high |
| 架構設計、跨模組重構 | Opus 5.5 | high |
| 評測過確定有提升的困難題 | 依評測結果 | xhigh |

⚠️ 搭配一條系統提示:「**每次改動都必須實際執行測試;無法執行時,明確說明原因,不得回報完成。**」

### 案例二:遷移前的五分鐘自查

```bash
# 找出會回 400 的舊設定
grep -rn '"type": *"disabled"' src/          # thinking disabled
grep -rn 'tool_choice' src/ | grep -E '"(any|tool)"'
grep -rn 'computer_20251124' src/
# 有沒有「修改歷史訊息再重送」的程式碼(例如刪掉失敗的工具結果)
grep -rn 'messages\[.*\] *=' src/
```
然後在 Claude Code 跑 `/claude-api migrate`,最後逐項核對它產出的清單。

### 案例三:用「能不能寫驗收」做模型分派

把工作拆成兩類:
- **有驗收的**(單元測試、schema 驗證、截圖比對)→ 先丟 Sonnet 5.5,失敗再升級。
- **沒有驗收的**(「這個架構合不合理」「這段需求怎麼解讀」)→ 直接 Opus,或先花時間**把驗收寫出來**,再交給 Sonnet。

---

## 9. 核實總表

| 說法 | 結果 |
|---|---|
| 價格 $2 / $10 / 快取讀取 $0.20,與 Sonnet 5 相同 | ✅ 官方公告 |
| 快 30% 以上、每任務最多便宜 30% | ✅ 官方公告 |
| Terminal-Bench 10.3 → 70.6、Opus 5.5 66.4 | ✅ |
| OSWorld 80.1 / Opus 81.8、Chartography 61.6、GDPval 1844 vs 1846、FrontierCode 46.2 vs 54.4、CursorBench 55.5 vs 57.8 | ✅ |
| 寶可夢紅、Slack 少 14% 輸出 token、Epic Games 引述 | ✅ |
| 五個破壞性變更、2026-08-31 帳號規則、2.5 倍圖片 token、快取門檻 512、`/claude-api migrate` | ✅ 官方遷移指南 |
| Simon Willison 鵜鶘 max 檔失敗 | ✅ 屬實;📌 原因是 **token 用完**,影片說「超時」不精確 |
| 「單輪換檔用 per-message effort」 | 📌 補正:`between_tools` 下會回 400,需用 adaptive thinking |
| SWE-Bench Pro 81.3、AutomationBench 44.7、HealthBench 69.2、Artificial Analysis 的 18 倍 | ❓ 本文未在官方公告頁找到,未核實 |

---

## 10. 追加:四個模型怎麼選、額度怎麼燒,以及 Advisor Strategy(YAHA学堂,2026-08-31)

> 整理自 YouTube 頻道 **YAHA学堂**〈Anthropic 自己测的:Sonnet 配一个 Opus 顾问,分数更高、成本反而低 11.9%〉(2026-08-31,約 13.8 分)。**該片無官方字幕,逐字稿以 CPU 版 Whisper 轉錄,可能有同音字誤差**(Hikoo/Hikook = Haiku、OPIS/OPEX = Opus、Cursor Bench = CursorBench 等已還原)。
> ⏳ 影片發布時是 Sonnet 5 / Opus 5 / Fable 5 世代;**價格與方案規則今年多次改**(影片自己也這麼說),以下「影片數字」請以當下官方頁為準。

### 10.1 影片主張:「四個模型是四種任務形狀,不是好壞排序」

| 模型 | 影片給的定位 | 影片價格(每百萬 token 輸入) |
|---|---|---|
| Haiku | **要快**:快問快答、抓資訊、分類、簡單摘要 | $1 |
| Sonnet | **要穩**:日常主力(寫作、寫程式、除錯、多步驟);免費版與 Pro 預設 | $2(輸出 $10) |
| Opus | **要深**:多層依賴分析、大重構、需來回討論的協作 | $5 |
| Fable | **要長**:交代結果、自己規劃自查的長任務(例:Stripe 5,000 萬行 Ruby 遷移,一天跑完) | $10 |

- 頭尾差 **10 倍**(輸出端 5 / 10 / 25 / 50 美元);訂閱制不看美元,但額度是照這個成本在扣。
- **額度有兩道閘**:5 小時滾動窗口 + 每週上限。每則訊息扣多少取決於 **模型倍率**、**effort**(從 Low 到 Max;影片轉述官方部落格「同題開高 effort 比低 effort 多約 7 倍 token」)、以及 **每輪全量重送的對話歷史**。
- **降級順序**:活很常規 → 先換小模型(品質不掉還省錢);模型沒選錯但做得不夠細 → 才動 effort。「不夠細」的訊號:寫程式看 **跳過檔案、不跑測試、不複查**;純聊天看 **答得太籠統**。
- **預設 Sonnet,升級只有一個理由:小模型漏了你在乎的東西**。測法:拿一份你讀過的報告,讓 Haiku 摘成 5 點並標出一條想另外核對的說法,再開新對話讓 Sonnet 做同一件事;誰漏掉你自己會標的那條,就用誰。
- **Pro 用戶的 Fable 不在月費內**(需另開 usage credit);個人方案只有 Max 把 Fable 包進去,且免費包含部分最多到週額度一半。✅ 2026-11-07 已對照 Anthropic 官方說明頁核實(見 §10.5.5)。⚠️ 影片自己說這條規則夏天改過好幾次,**仍以觀看當下官方頁為準**。
- **Fable 的安全分類器**:碰到攻擊向資安、生物化學雙重用途等問題,會自動切給 Opus 回答;影片稱早期數據 **超過 95% 對話不觸發**。但一送出就被攔的整輪按 Opus 算、聊到一半才被攔的前半仍按 Fable 價——所以這類題**一開始就選 Opus** 較省。

### 10.2 ⭐ Advisor Strategy:貴模型只在拍板處出手

影片說 2026-04-09 Anthropic 發了〈Advisor Strategy〉一文。**對照官方原文([claude.com/blog/the-advisor-strategy](https://claude.com/blog/the-advisor-strategy),發布日 2026-04-09)核實:**

| 項目 | 官方原文 | 結果 |
|---|---|---|
| 機制 | Sonnet 或 Haiku 當 **executor**(自己呼叫工具、迭代);遇到無法合理解決的決策才問 **Opus advisor**。advisor 讀共享上下文,回傳計畫、修正或停止訊號;**不呼叫工具、也不直接回覆使用者** | ✅ 與影片一致 |
| API | 工具型別 `advisor_20260301`、beta header `anthropic-beta: advisor-tool-2026-03-01`、`max_uses` 限制單次請求的顧問呼叫數;整個交接在**同一個 `/v1/messages` 請求內** | 影片未提,補充 |
| 計費 | advisor 的 token 按 advisor 模型計價、executor 的按 executor 計價;advisor 通常只產出 **400–700 text tokens** 的短計畫 | 補充 |
| SWE-bench Multilingual | Sonnet + Opus advisor 比 Sonnet 單跑 **高 2.7 個百分點、每個 agentic 任務成本低 11.9%** | ✅ 影片數字正確 |
| BrowseComp(Haiku) | Haiku + Opus advisor **41.2%**,Haiku 單跑 **19.7%**;比 Sonnet 單跑**分數低 29%、成本低 85%** | ✅ 影片數字正確;影片說「比 Sonnet 單跑便宜 85%、分數還差一截」同義 |
| ⚠️ **模型世代** | 官方腳註:實驗用的是 **Sonnet 4.6 / Haiku 4.5 + Opus 4.6 advisor**;SWE-bench 為 5 次平均、300 題、9 種語言;BrowseComp 為 1,266 題、各一次 | 📌 影片語境像在談 5 代模型,**這組數字是 4.6 代的結果** |

- **不寫程式也能照做**:Claude app 同一個對話中途可換模型——想方向、拆步驟的那一兩輪切 Opus,定案後執行輪切回 Sonnet,上下文還在。
- **Claude Code**:輸入 `/model` 有 **Opus plan** 選項——計畫階段用 Opus、動手執行切回 Sonnet。✅ 官方文件中此選項的別名是 **`opusplan`**,定義為「plan mode 用 `opus`、執行時自動切 `sonnet`」;若管理員設了 `availableModels` 白名單,會以白名單中最新的 Opus 做規劃(見 §10.5.3)。
- **Claude Code 內建 `/advisor`(較新功能,需 v2.1.260 以上)**:不必靠自己切模型,直接設定顧問模型,由 Claude 在關鍵時刻自行呼叫(見 §10.5.2)。影片沒提到這個入口。
- 影片補的反轉(轉述 7 月部落格):複雜多步驟任務,大模型可能幾步做完,小模型卻一直磨、一直撞上限;**有些活 Opus / Sonnet 開到任何 effort 都做不完**。結論不是越便宜越好,而是按任務形狀配模型。

```mermaid
flowchart TD
    A["任務進來"] --> B{"任務形狀?"}
    B -->|"要快"| C["Haiku"]
    B -->|"要穩 預設"| D["Sonnet"]
    B -->|"要深"| E["Opus"]
    B -->|"要長 且 Opus 試過搞不定"| F["Fable"]
    D -->|"漏了你在乎的東西"| E
    D -.->|"卡在關鍵決策"| G["Opus 當 advisor<br/>只在拍板處"]
    G -.-> D
```

### 10.3 核實與疑點

| 說法 | 結果 |
|---|---|
| Advisor Strategy 發布日、2.7 pp、-11.9%、41.2 vs 19.7、-85% | ✅ 官方部落格 |
| Haiku $1 / Sonnet $2 / Opus $5 / Fable $10 | Sonnet $2/$10 與 Fable $10/$50 與本庫他篇一致;⚠️ **Haiku 已於 2026-10-07 由 Haiku 5.5 改為 $0.10/$0.50(見 [[claude-haiku-5-5-cheap-model-computer-use]]),影片的 $1 是 Haiku 4.5 時期** |
| Opus 5 離 Fable 峰值僅差 0.5%(CursorBench)、成本一半 | ⚠️ **部分核實**(2026-11-07):二手報導轉述 Anthropic 的主張——CursorBench 3.2 上 Opus 5 max 檔 70.1、Fable 5 為 70.4(差 0.3 分),**每任務成本約一半**;屬自報數字,且版本不同,不可與 CursorBench 4.0 比較(見 §10.5.6) |
| Opus 5 電腦操作反超 Fable、成本 1.3% 多一點 | ❓ 未能核實(未找到原始數字) |
| Opus 5 於 7/24 發布、Max 預設、Pro 最強 | ✅ 影片畫面字卡核對(字卡「7 / 24 才出的」、「MAX 預設」、「PRO 最強」);發布日本身未另行查證 |
| Pro 不含 Fable、Max 含至週額度一半 | ✅ Anthropic 官方說明頁(§10.5.5) |
| `opusplan` 在 plan 階段用 Opus、執行用 Sonnet | ✅ Claude Code 官方文件(§10.5.3) |
| Advisor 的 2.7 pp 與 11.9% 是「同條件」比較 | ⚠️ **條件不同**:Sonnet 單跑開 adaptive thinking,advisor 那組關閉 thinking(§10.5.4)。影片未提 |
| 「額度消耗大頭是每輪全量重發歷史」「高 effort 約 7 倍 token」 | ❓ 轉述其他影片/部落格,未核實 |
| 95% 對話不觸發 Fable 分類器 | ❓ 轉述發布時早期數據,未核實 |

### 10.4 應用案例

- **Pro 用戶的日常**:預設 Sonnet;整理會議記錄、改格式這種批量小活手動切 Haiku;若 Haiku 漏掉重點(用 10.1 的「摘 5 點 + 標一條」測),下次同類回 Sonnet。
- **寫大功能**:先在 Claude Code 用 `/model` → Opus plan 產生計畫與驗收條件,再切回 Sonnet 執行;對照 [[model-routing-compute-allocation]] 的「規劃用強模型、執行用便宜模型」成本實算。
- **自建 agent**:executor 用 Sonnet,在 API 加 `advisor_20260301` 工具並設 `max_uses`,只在「架構取捨、卡關」時叫 Opus;自己的評測集要同時跑 Sonnet 單跑 / Sonnet+advisor / Opus 單跑三組再決定(官方也這樣建議)。
- **資安/生物類題**:直接選 Opus,不要繞 Fable。

### 10.5 延伸閱讀與深度補充(2026-11-07 核實增補)

> 以下是逐一打開官方文件、部落格與說明頁後**真的讀到**的內容;影片沒講或講錯的地方一併標出。

#### 10.5.1 Advisor 工具的 API 細節(官方 API 文件)

- **工具定義**:`{"type": "advisor_20260301", "name": "advisor", "model": "claude-opus-5-5"}`;beta header `anthropic-beta: advisor-tool-2026-03-01`(仍屬 beta)。頂層 `model` 是 executor,工具內的 `model` 是 advisor,advisor 按自己的費率計價。
- **限制**:advisor 必須是 **Sonnet 4.6 或更強**,且**能力不低於 executor**。`max_uses` 限制單一 turn 的顧問呼叫次數,預設不限;超過上限會回 `advisor_tool_result_error`(`max_uses_exceeded`),**整個請求不會失敗**。`max_tokens`(最小 1024)可限制每次顧問輸出。
- **回傳形式(影響能不能讀)**:Opus 4.8 等 advisor 回 **明文** `advisor_result`;Sonnet 5.5、Opus 5、Opus 5.5、Fable 5 / 5.1、Mythos 5 / 5.1、Haiku 5.5 當 advisor 時回 **加密** `advisor_redacted_result`——客戶端讀不到建議內容,由伺服器在下一次請求解密後注入 executor 的提示。**做除錯或稽核時,要知道這點**。
- **計費**:`usage.iterations[]` 內 `type: "advisor_message"` 按 advisor 費率計;`type: "message"` 按 executor 費率計。**頂層 `usage` 只含 executor**,不會把 advisor 的 token 加進去——若只看頂層數字,會低估成本。
- **串流**:advisor 子推論**不串流**;executor 的串流會暫停,結果以單一事件送回。
- **快取**:executor 端快取照常;advisor 端快取是**選用**(`caching`),官方說「每段對話顧問呼叫少於或等於 2 次時,寫入快取的成本高於讀取省下的錢」。
- **強制呼叫**:`tool_choice: {"type": "tool", "name": "advisor"}` 不能與手動 extended thinking 併用(回 400);Opus 5.5、Sonnet 5.5、Fable 5.1 等 executor 不接受 `tool` / `any`,要改用提示詞引導。

#### 10.5.2 Claude Code 的 `/advisor`:配對規則(官方 Claude Code 文件)

- 設定方式三種:`/advisor opus`(互動選單或直接指定,會存入 `advisorModel`)、設定檔 `"advisorModel": "opus"`、啟動旗標 `claude --advisor opus`。
- **顧問必須不低於主模型**。Claude Code 內建配對表的重點列:

| 主模型 | 可接受的顧問 |
|---|---|
| Haiku 4.5 | Fable、Opus、Sonnet、Haiku 5.5 |
| Sonnet 5 或 Haiku 5.5 | Fable、Opus 4.7 以上、Sonnet 5 以上、Haiku 5.5 |
| Sonnet 5.5 | Fable、**Opus 5 以上**、Sonnet 5.5 |
| Opus 5 / Opus 5.5 | Fable、Opus 5 以上 |

- **Haiku 4.5 可以呼叫顧問,但不能當顧問**。影片的「Haiku 單跑 vs Haiku + Opus 顧問」實驗(BrowseComp)是在 **API** 上做的,與 Claude Code 這張表是不同層面的設定。
- 中途**開關** `/advisor` **不會**讓主模型的 prompt cache 失效(與切換主模型不同)。
- **只能用於 Anthropic 官方 API**:Amazon Bedrock、Google Cloud、Microsoft Foundry 都不支援;經 LLM gateway 轉送時看 gateway 是否原樣轉發。
- 功能標示為 **experimental**,行為、計價與可用性可能改變。

#### 10.5.3 `opusplan` 的官方定義

- `opusplan` 是別名:**plan mode 用 `opus` 做複雜推理與架構決策,執行模式自動切到 `sonnet`** 寫程式。
- context window:兩階段各自沿用 `opus` / `sonnet` 的設定;若要兩段都用 1M context,設 `opusplan[1m]`(例:`/model opusplan[1m]`)。
- 若管理員設了 `availableModels`,例如 `["sonnet", "claude-opus-4-6"]`,`opusplan` 會用白名單中**最新**的 Opus 規劃。
- 官方文件把它與 `/advisor` 區分:`opusplan` 是「依 plan mode 切換」;advisor 是「Claude 在任務中途自己決定何時問」。

#### 10.5.4 Advisor 基準的「條件表」(官方部落格腳註)

| 測試 | 執行者 | 顧問 | 條件 |
|---|---|---|---|
| SWE-bench Multilingual(+2.7 pp、成本 -11.9%) | Sonnet 4.6 | Opus 4.6 | **Sonnet 單跑開 adaptive thinking;advisor 組關閉 thinking**;5 次平均、300 題、9 種語言 |
| BrowseComp(Haiku 19.7% → 41.2%) | Haiku 4.5 | Opus 4.6 | 關閉 thinking;Sonnet 4.6 用 medium effort;1,266 題、各一次 |
| Terminal-Bench 2.0 | Sonnet 4.6 | Opus 4.6 | 關閉 thinking;Sonnet 用 medium;89 題、每題 5 次 |

- ⚠️ **影片沒講的重點**:2.7 pp 的兩組**thinking 設定不同**(單跑開、advisor 組關),所以它比較的不是「只多了一個顧問」這件事,而是「單跑 vs 顧問+關 thinking」。若要自己評估,應該讓兩組條件一致。
- 同一頁的客戶引述 Eve Legal:Haiku 4.5 + Opus 4.6 顧問,品質與前沿模型相當、成本約五分之一(單一客戶自述)。

#### 10.5.5 Fable 的方案規則(Anthropic 官方說明頁,2026-11-07 讀取)

- **Max、Ultra、高階 Team / Enterprise 席位**:Fable 5 與 5.1 是方案標準內容;最多可用**週額度的 50%**,超過後可改用 usage credits 或換模型。Fable 比其他模型更快消耗週額度。
- **Pro、標準 Team / Enterprise 席位**:Fable「不在方案用量內」,從第一個 token 起就按 pay-as-you-go usage credits 計費。
- **API**:按標準 API 費率。
- 前一波促銷只針對 **Fable 5**(2026-07-19 PT 結束),**Fable 5.1 從未包含在內**。
- ✅ 影片「Pro 要另開 credit、Max 只包到一半」的說法,與官方頁一致;影片也說規則會變,以頁面為準。

#### 10.5.6 Opus 5 與 Fable 5 的 CursorBench 數字(二手查證)

- 搜尋摘要轉述 Anthropic 的主張:**CursorBench 3.2** 上,Opus 5 max 檔 **70.1**、Fable 5 為 **70.4**,差 0.3 分(報導稱「0.5%」),**每任務成本約一半**;每 token 單價未變($5 / $25)。
- ⚠️ 這是 Anthropic 自報、且我**未讀到原始官方頁**,只看到多家報導的一致轉述,故標為「二手」。
- ⚠️ 後來 Cursor 文件表示 **Opus 5.5 取代了 Opus 5**;另一組 CursorBench 4.0 的數字(Opus 5.5 57.8、Opus 5 46.6)是**不同版本**,不要與 3.2 的 70.x 混比。

### 10.6 補充應用案例

- **Sonnet 主力 + 顧問**:在 `settings` 設 `"advisorModel": "opus"`,主模型用 Sonnet 5.5。注意 Sonnet 5.5 的顧問只能是 **Opus 5 以上**(Opus 4.x 不在配對表內),所以設 `opus` 別名會解析到當下的 Claude Code 內建預設版本;若要固定版本,寫完整模型 ID(如 `claude-opus-5-5`)。
- **多輪除錯的成本核算**:advisor 的 token 不會出現在頂層 `usage`;自建 agent 要從 `usage.iterations[]` 按 `type` 分開加總,否則帳單對不上。
- **想要可稽核的顧問意見**:選明文回傳的顧問(例如 Opus 4.8 系列)。Opus 5 / 5.5 或 Haiku 5.5 當顧問時,你在 API 回應中只能看到加密區塊,不能直接把建議寫進 log 或審查紀錄。

---

## 來源

- YouTube:[Sonnet 5.5 更新了什么?](https://www.youtube.com/watch?v=s87lkkWk9rQ)(Why QQ,2026-09-29;官方簡中字幕)
- Anthropic 官方:[Introducing Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5)
- 官方文件:[Migrating to Claude Sonnet 5.5](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide)、[What's new in Claude Sonnet 5.5](https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5)、[Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)
- Simon Willison:[Claude Sonnet 5.5](https://simonwillison.net/2026/Sep/28/claude-sonnet-5-5/)
- 討論:[Hacker News — Sonnet 5.5](https://news.ycombinator.com/item?id=49881850)
- 報導:[TechCrunch](https://techcrunch.com/2026/09/28/anthropic-releases-sonnet-5-5-which-it-calls-a-significantly-cheaper-faster-work-partner/)、[VentureBeat](https://venturebeat.com/technology/anthropic-launches-claude-sonnet-5-5-with-30-cost-reduction-per-task-due-to-faster-speeds-and-fewer-tool-calls)、[Help Net Security](https://www.helpnetsecurity.com/2026/09/29/anthropic-claude-sonnet-5-5/)
- YouTube:[Anthropic 自己测的:Sonnet 配一个 Opus 顾问…](https://www.youtube.com/watch?v=H4zIuJ4G1QY)(YAHA学堂,2026-08-31;**該片無官方字幕,逐字稿以 CPU 版 Whisper 轉錄,可能有同音字誤差**)——§10
- Anthropic 官方:[The advisor strategy: Give agents an intelligence boost](https://claude.com/blog/the-advisor-strategy)(2026-04-09)——§10
- Anthropic 官方 API 文件:[Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)——§10.5.1(2026-11-07 讀取)
- Claude Code 官方文件:[Escalate hard decisions with the advisor tool](https://code.claude.com/docs/en/advisor.md)(§10.5.2)、[Model configuration](https://code.claude.com/docs/en/model-config.md)(`opusplan`,§10.5.3)
- Anthropic 官方說明頁:[Claude Fable models on your plan](https://support.claude.com/articles/15424964-claude-fable-models-on-your-plan)——§10.5.5(頁面僅顯示「Updated over a week ago」,無精確日期)
- 二手報導(未讀原頁):Opus 5 的 CursorBench 3.2 數字,見 [implicator.ai](https://www.implicator.ai/anthropics-opus-5-cut-tokens-17-but-cost-more-to-benchmark-than-opus-4-8/)、[Opus 5 Does Fable 5's Job for Half the Price](https://ilikekillnerds.com/2026/07/25/opus-5-fable-capability-half-the-price/)——§10.5.6
