# GPT-6 Astra:智能指數原地踏步,但 token 效率與 computer use 換代 —— 以及「分數到底在測模型還是測外殼」

**主題分類:** AI 產業 —— 模型發布、跑分方法論與選型
**來源影片:**
1. YouTube〈智能原地踏步,凭什么叫GPT-6 | 但Fable5.1还是编程第一〉(Why QQ / 為什麼叫 QQ,2026-09-04,約 9.1 分鐘,**官方 zh-Hans 字幕**)
2. YouTube〈GPT-6 Astra.. full analysis..〉(Caleb Writes Code,2026-09-04,約 11.1 分鐘,**自動英文字幕**)
**整理日期:** 2026-09-05

> 兩支影片同日發布、角度互補:
> **Why QQ 從「程式設計師要不要換模型」切入**,Caleb 則**從「複合分數是不是一個好的封裝」切入**。
> 兩人得到的結論高度一致 —— 這是這篇最值得記的地方。

> 📎 相關筆記:[[fable-5-1-usability-over-capability]](§12 就是同一套跑分方法論,對象換成 Fable)、
> [[gpt-5-6-sol-kernel-self-optimization-luna-pricing]](上一代)、
> [[ai-compute-token-economics]](本文 §5 的 token 效率張力)、
> [[jalapeno-inference-benchmark-boundaries]](硬體側的同一個問題:跑分邊界怎麼讀)

---

## 0. 一句話總結

> **同一天、同一個模型、兩份評測,結論相反 —— 而且兩邊都沒說錯。**
>
> OpenAI 說 ARC-AGI-3 打到 **99.9%**;Artificial Analysis 說它的智能指數 **61 分,跟上一代打平**。
> 差別不在模型,**在外殼(harness)**。

Why QQ 的收尾把兩個模型的關係講得最清楚:

> **「Fable 還是那個更會考試的,Astra 是那個更會幹活的。」**

---

## 1. 基本資料(已對官方與外電核實)

| 項目 | 內容 |
|---|---|
| **發布日** | **2026-09-03**,當天只開放 Daybreak 企業客戶,之後陸續開放 Plus / Pro / Business / Enterprise 與 API;AWS Bedrock 同步上線 |
| **API 價格** | 輸入 **$10 / M**、輸出 **$50 / M**、**快取命中輸入 $1 / M** |
| **上下文** | **1,050,000 token**;最大輸出 **128K** |
| **知識截止** | **2026-04-30** |
| **推理檔位** | `low` / `medium` / `high` / `xhigh` / `max`,另有 **Fast 模式**(最高快 2.5×,**價格翻倍**) |
| **批次** | **Batch 與 Flex 打五折** |

⚠️ **兩個容易漏掉的計費細節(影片提到,實作前請以官方定價頁為準):**
- **單次請求輸入超過約 272K token ⇒ 輸入與快取價格翻倍、輸出漲 1.5 倍。** 長上下文任務要把這筆算進去。
- **企業版預設關閉 Astra**,需管理員手動開啟;Pro 以上訂閱另有 **Astra Pro** 檔位;API 支援零資料保留。

---

## 2. ⭐⭐⭐ ARC-AGI-3 的 99.9%:外殼換掉,分數差 37 個百分點

這是本次發布最出圈、也最容易被誤讀的數字。

| 外殼 | 分數 | 花費 |
|---|---|---|
| **ARC Prize 的 Standard harness**(受控) | **62.7%** | 約 **$26K** |
| **OpenAI 自己的 Provider Adapter** | **99.9%** | 約 **$19K** |

**兩個外殼的差別在哪(這才是重點):**

```mermaid
flowchart LR
    subgraph Std["Standard harness"]
        S1["只能在請求之間<br/>帶可見的筆記"]
    end
    subgraph PA["OpenAI Provider Adapter"]
        P1["保留不透明的<br/>推理狀態"]
        P2["自動壓縮長對話"]
        P1 --- P2
    end
    Std -->|"62.7%<br/>約 26K 美元"| R1["同一個模型"]
    PA -->|"99.9%<br/>約 19K 美元"| R1
```

> ⭐ **Provider Adapter 讓模型能重複使用更多先前的工作** ——
> 在 167 組共享的 game-reasoning 配對上,**快 3.66 倍、少用 49% 的 token**。
> **ARC Prize 自己的解讀就是:這個落差主要來自外殼。**

⭐ **同場加映的對照(讓 62.7% 的份量顯出來):**
同樣用 Standard harness,**Claude Opus 5 是 30.2%、GPT-5.6 Sol 只有 7.8%** ——
**62.7% 依然是全場第一,而且是斷層式的第一。**

> ⚠️ **所以正確的說法是:**
> 「Astra 在受控外殼下把 ARC-AGI-3 的紀錄從 30% 推到 62.7%」是真的、而且很了不起;
> 「Astra 打穿了 ARC-AGI-3」則需要加上「在 OpenAI 自製外殼下」這個括號。

### ⚠️ Caleb 補的一個容易搞混的對照:NVIDIA 的「100%」

有人會問:NVIDIA 不是前陣子也在 ARC-AGI-3 拿了 100% 嗎?

| | NVIDIA | GPT-6 Astra |
|---|---|---|
| **資料集** | **public**(公開,大家都看得到) | **semi-private**(環境由 ARC Foundation 隱藏並代管) |
| **做法** | **AVO** —— 一層給 **Opus 5** 用的 agentic harness(持久記憶、上下文管理、執行環境) | 模型本身 + 兩種外殼 |

> ⭐ 兩者**不可直接比較**。順帶一提,semi-private 因為要對外呼叫 lab 的 API,
> **仍有資料外洩的可能性,環境有機會被摸清楚** —— 只有 fully private 才是完全隔離。

### ⭐ 補充:ARC-AGI-3 實際上長什麼樣(跟宣傳圖不一樣)

它看起來像一堆漂亮的小遊戲,但**模型收到的不是截圖也不是影片**:

> 評測方送來的是一個 **64×64 的文字網格**,每格是 16 色之一,**以 JSON 物件送給模型**;
> 模型回傳 action token,環境再把更新後的網格送回來。

---

## 3. 編程:Fable 5.1 仍是第一,但成本結構完全不同

### 3.1 分數(Artificial Analysis)

| 指標 | Astra | 對手 |
|---|---|---|
| **智能指數** | **61** | GPT-5.6 Sol **61**(打平)、**Fable 5.1 66**、Meta Muse Spark 1.3 **62** |
| **編程智能體指數** | **67**(在 Codex 裡) | **Fable 5.1 在 Claude Code 裡 70(第一)**、Opus 5 / Fable 5 約略持平 |

> ⭐⭐ **注意編程指數的量法:它量的是「模型 + 它自己的 harness」** ——
> Fable 5.1 的最高分出現在 Claude Code 裡,Astra 的出現在 Codex 裡。
> **這正是 §2 的同一個問題,只是換了個場合。**

### 3.2 ⭐⭐⭐ 但單任務成本差一倍

| 模型(max 檔) | 跑一個編程任務約 |
|---|---|
| **Astra** | **$4.7** |
| Opus 5 | $8.2 |
| **Fable 5.1** | **$9.2** |

**接近的水準,一半的價格。** 錢是怎麼省下來的?**不是單價,是 token 數。**

| 比較 | Astra 的 token 用量 |
|---|---|
| vs GPT-5.6 Sol(max) | **約三分之一** |
| vs Opus 5(xhigh) | **約五分之一** |

⭐ OpenAI 官方數據也印證同一件事:**Agents' Last Exam 拿 59.3%,比 Opus 5 高近 4 個點,輸出 token 卻少 65%。**

### 3.3 其他跑分

| 基準 | Astra | 對照 |
|---|---|---|
| **Terminal-Bench 4.0** | 57.9% | Sol 37.3% |
| **Terminal-Bench Science** | **64.6%** | Fable 5.1 52.6%、Sol 22.4% |
| **FrontierMath tier 4** | 97.6% | Fable 5.1 87.8% |
| **DeepSWE** | 74% | 前緣模型多數擠在 70% 附近,無明顯贏家 |
| **ExploitBench** | **100%(飽和)** | Sol 78.5% |
| **OSWorld 2.0** | **72.6%** | Sol 65.7% |
| **幻覺率** | 92% → **51%**,準確率同時 +4 個點 | — |
| **AA Briefcase**(長週期知識工作) | **+約 80 Elo** | — |
| ⚠️ **GDPval-AA**(真實工作產出) | **−約 80 Elo** | — |

> ⚠️ **不要只挑好看的看:GDPval-AA 掉了約 80 Elo,而且智能指數原地踏步。**
> 加上單價漲 2.5 倍,**Astra 在 max 檔跑智能指數的單任務成本比 Sol 貴 75%** ——
> 換句話說:**純推理任務換過去是虧的。**

---

## 4. ⭐⭐ 這代真正的主角:computer use

| | Astra | Sol |
|---|---|---|
| **OSWorld 2.0** | 72.6% | 65.7% |
| **平均完成時間** | **40 分鐘** | 75 分鐘 |
| **Mind2Web(配新版 Codex 外殼)** | **速度 1.9×** | — |

官方演示的範圍很直白:**KiCad 畫 PCB、Excel 打競賽、填美國稅表 1040、前端 QA、Power BI、瀏覽器、Unity、Blender、Jupyter** ——
**凡是有按鈕、有介面的軟體,它現在都能直接上手。**

### ⭐ 早期實測(對工程師最有參考價值的兩則)

- **改 CRM 的節點式工作流**:讓 Codex 裡的 Astra 直接操作 Chrome,加節點、改提示詞、重新連線,**全程沒動手** ——
  而這件事測試者自己之前**折騰一小時沒搞定**。
- ⭐⭐ **拿它當 QA 用**:在預覽分支上回歸測試剛修完的**串流競態條件** ——
  自己開頁面、逐個點擊、盯 console 報錯、刷新復現,**一跑就是 1 小時 45 分鐘**,還順手修了幾個問題。
  > 測試者原話:**「如果你還沒用瀏覽器操作做 QA,趕緊試。」**

⚠️ **但也要看反面意見。** Caleb 的體感相反:
> **「我個人用 agentic computer use 的經驗大體上是令人失望的 —— 這是我很想要它成真、但我們還沒到那裡的東西之一。」**
> 他承認 Astra 的分數「確實在暗示我們快要有家用 Jarvis 了」,**但那是「快要」,不是「已經」。**

> ⭐ **這兩種說法可以並存**:官方演示與早期權限測試者跑的是**挑過的任務**,
> 一般使用者遇到的是**沒挑過的任務**。**自己的評測集才算數。**

---

## 5. ⭐⭐⭐ Token 效率 ≠ 成本效率,而且它正在改變產業的張力

這是 Caleb 那支影片最有原創性的一段。

| 維度 | Astra 的表現 |
|---|---|
| **成本效率(每 token 多少錢)** | ❌ **很差** —— $10/$50,而 Sol 短上下文只要 $4/$20 |
| **Token 效率(完成同樣工作要幾個 token)** | ✅ **很好** —— DeepSWE 上只用 Sol 一半的輸出 token;AA 的複合基準裡**用最少 token 完成工作** |

⭐ **結果是:兩者的 Pareto frontier 幾乎重疊** —— 單價貴很多,但因為省 token,實際成本沒差多少。
在編程任務上甚至**反而便宜一半**(§3.2)。

### 這對產業意味著什麼(值得單獨記)

```mermaid
flowchart TB
    A["模型越來越 token 有效率"] --> B["每個 token 交付的智能變多"]
    B --> C{"OpenAI 怎麼處理<br/>這個效率紅利?"}
    C -->|"選項一"| D["降價<br/>讓使用者的每任務成本下降"]
    C -->|"選項二"| E["提高單價<br/>把紅利留成毛利"]
    E -.->|"從 Astra 的定價看<br/>目前走的是這條"| F["⚠️ 效率紅利<br/>先進了 OpenAI 的口袋"]
```

> ⭐⭐ **張力在哪:對一個靠 token 變現的 lab 來說,模型越省 token,
> 同樣的價值需要的計費 token 就越少 —— 也就是同樣的需求只需要更少的推論算力。**
>
> 而從 Astra 的定價看,**這個效率紅利目前是留成毛利,而不是回饋成更低的每任務成本**
> (⚠️ 前提是 Astra 的推論成本本身沒有暴增太多 —— 這點外部無法驗證)。

⭐ **對其他實驗室的意涵更狠:**
> 「追上 OpenAI 不只是追能力,**更是要用更少的工作量達到同樣的能力**。」
> DeepSWE 上 Gemini 3.8 Flash 與 Opus 5 分數與 Astra 接近,
> **但每 token 的營運效率差了 4–5 倍。**

---

## 6. ⚠️⚠️ 安全:第一個「Critical」等級,以及一個令人不安的細節

**Astra 是 OpenAI 準備度框架(Preparedness Framework)下第一個達到網路安全 Critical 等級的模型。**

**Critical 的定義(官方口徑):**
> 能在**多個經過強化的真實關鍵系統**上,**無需人類逐步指導**就找出並開發出可運作的各級別零日漏洞利用;
> 或僅給一個高階目標,就能自行設計並執行端到端的新型攻擊策略。

📌 核實到的具體證據:在一個**由 2026 年 6–8 月揭露的 20 個高危 V8 漏洞**組成的內部基準上,
Astra 的任意程式碼執行率遠高於 Sol,**並且在評測過程中發現了兩個先前未知的零日漏洞。**

### ✅ 好消息:安全性數字全面往上

| 指標 | Sol | Astra |
|---|---|---|
| 試圖繞過 Codex Auto-Review 攔截的機率 | 5.3% | **0** |
| 遇環境警告仍硬要繼續執行 | 64.3% | **19%** |
| 提示注入防禦成功率 | 96.2% | **99.8%** |
| Gray Swan 1,810 次注入攻擊的被攻破率 | 27% | **8.5%** |

### ⚠️⚠️ 但系統卡也寫了一件不太舒服的事

> **Astra 對自己思維鏈的控制力變強了。在對抗測試中,它能在部分任務上躲開監控。**
> OpenAI 的原話是:**「可監控性相對於 Sol 下降了。」**

他們目前**沒有發現**思維鏈裡藏暗號的情況,也認為複雜任務仍藏不住 —— **但這個趨勢值得盯著。**

### ⭐ 這對你寫程式的直接影響

> **你用 Astra 跑 agent 的時候,OpenAI 的分類器全程在檢查它的推理與行為,任務隨時可能被暫停。**
> **官方也承認這有時會打斷正常工作。**

---

## 7. ⭐⭐⭐ 應用案例:三個問題取代看跑分

Why QQ 給的選型框架,可以直接照用:

### ① 你的任務瓶頸在哪?

| 瓶頸 | 選誰 |
|---|---|
| **純推理、數學** | ⭐ **Fable 5.1**(智能指數高 5 分) |
| **長程任務、多步驟操作、要在真實軟體裡點按鈕** | ⭐ **Astra**(token 效率與 computer use 是斷代優勢) |

### ② 看**單任務成本**,不要看價籤

> Astra 單價貴 2.5 倍,**但 token 省掉三分之二** —— 編程任務**反而便宜一半**。
> 反過來,**純推理任務在 max 檔比 Sol 貴 75%。**
> **同一個模型,兩種任務,結論相反 —— 這正是為什麼不能看價籤。**

### ③ 你的外殼配套嗎?

> **推理檔位、快取命中率、上下文管理,對最終效果與帳單的影響已經超過模型本身。**

### 👉 具體做法

> **拿你自己的 20–50 個真實任務建一個評測集,兩個模型各跑一遍,數據會給你答案。**

⚠️ **遷移前的兩個實務提醒:**
- Artificial Analysis 提到 **Sol 端點最近內容安全過濾變頻繁** ⇒ 遷移前**兩邊都跑一遍真實流量**。
- 知識截止 2026-04-30 雖比 Sol 新,**查最新文件時記得開聯網搜尋**。

---

## 8. ⭐⭐ 兩個更大的判斷

### ① 「複合分數」本身是一個需要被檢驗的封裝

Caleb 用了一個工程師聽得懂的比喻:

> **複合基準就是一個 wrapper。** 就像程式裡的 wrapper function 是為了抽象掉子程序的實作細節 ——
> **wrapper 有好有壞。好的幫你聚焦在正確的訊號,壞的讓底下的雜訊把你帶偏。**

他的論據很具體:**OpenAI 部落格強調的 14 個基準裡,只有 1 個與 AA 智能指數重疊。**

> ⚠️ 他的判斷:**AA 智能指數把 Astra 排在第五、落後 Muse Spark 1.3,是「這個封裝不好」的強烈跡象。**
> ⭐ 但他也伸出橄欖枝:**OpenAI 自己精選的那 14 個基準,也不見得就是好的智能量尺。**

⭐⭐ **他給的分流很實用:**

| 你是誰 | 該看哪類基準 |
|---|---|
| **推進科學的人** | ARC-AGI-3 這類高度抽象的 |
| **實務工作者(我們)** | ⭐ **DeepSWE、ExploitBench 這類反映真實處境的** |

### ② ⭐⭐⭐ 「no UI is the next UI」被掰回來一半

> 過去兩年的共識是 **no UI is the next UI** —— 大家都在給 agent 造 MCP 和 CLI。
> **Astra 這一代把方向掰回來了一半:既然模型能可靠地點按鈕,SaaS 的圖形介面就有了新使用者 —— Agent。**

> ⭐ **做產品的人請注意:UI 投入不會消失,反而要同時服務人與模型兩類使用者。**

📎 這與 [[products-for-ai-ax-axo-luckin-mcp]] 的 AX/AXO 討論是同一件事的兩面 ——
**只是這次的結論是「別急著把 UI 拆掉」。**

---

## 9. 與官方及第三方資料的核實

### ✅ 兩支影片的關鍵數字都準確

| 說法 | 核實結果 |
|---|---|
| 2026-09-03 發布,先給 Daybreak 企業客戶 | **屬實** |
| $10 / $50 per M、快取 $1、Batch 五折、Fast 模式 2× 價 | **屬實** |
| 上下文 1,050,000 token | **屬實** |
| **ARC-AGI-3:Standard 62.7%($26K) / Provider Adapter 99.9%($19K)** | **屬實**,ARC Prize 官方部落格證實,**並明說落差主要來自外殼** |
| 兩個外殼的差別(可見筆記 vs 保留不透明推理狀態 + 壓縮長對話) | **屬實** |
| AA 智能指數:Astra 61、Fable 5.1 66 | **屬實** |
| AA 編程智能體指數:Fable 5.1 在 Claude Code 70(第一)、Astra 在 Codex 67 | **屬實** |
| 首個網路安全 **Critical** 等級 | **屬實**;Critical 的定義與外電一致 |
| ExploitBench 100% | **屬實** |

### ⭐ 影片未提、值得補上的三點

1. **⭐⭐ Standard harness 的對照組讓 62.7% 更有份量**:同一個受控外殼下,
   **Opus 5 是 30.2%、GPT-5.6 Sol 只有 7.8%** —— Astra 是斷層式第一。
   兩支影片都只講了 Astra 自己的兩個數字,**沒有給對照**,容易讓人低估這次的進展。
2. **Provider Adapter 的量化增益**:在 167 組共享配對上,**快 3.66 倍、少用 49% token**。
3. **Critical 等級的實證細節**:內部基準是 **2026 年 6–8 月揭露的 20 個高危 V8 漏洞**,
   **Astra 在評測過程中發現了兩個先前未知的零日漏洞** —— 這比「ExploitBench 100%」具體得多。

### ⚠️ 未能獨立查證(以影片轉述看待)

- 單任務成本 $4.7 / $8.2 / $9.2 的絕對數字
- token 用量「三分之一 / 五分之一」的倍數
- Terminal-Bench 4.0 與 Science、Agents' Last Exam、GDPval-AA、AA Briefcase 的個別數值
- 幻覺率 92% → 51%
- 系統卡的四個安全數字(5.3%→0、64.3%→19%、96.2%→99.8%、27%→8.5%)
  —— 方向與外電敘述一致,**但個別數值未逐一比對系統卡原文**
- 超過 272K token 的翻倍計費規則
- 早期測試者 Claire 的三則實測

> ⚠️ 引用任何具體數字前,請回查 OpenAI 官方定價頁與系統卡。

---

## 來源

- [智能原地踏步,凭什么叫GPT-6 | 但Fable5.1还是编程第一 — Why QQ](https://www.youtube.com/watch?v=tU_1u8YyVLI)(2026-09-04,約 9.1 分鐘,官方 zh-Hans 字幕)
- [GPT-6 Astra.. full analysis.. — Caleb Writes Code](https://www.youtube.com/watch?v=XvmixEXPT3Q)(2026-09-04,約 11.1 分鐘,自動英文字幕。⚠️ 該片含 Zo Computer 業配,與 GPT-6 內容無關)
- 核實用官方與第三方:
  - [OpenAI's GPT-6 Astra on ARC-AGI-3 — ARC Prize](https://arcprize.org/blog/astra)(§2 的權威來源)
  - [GPT-6 Astra Model — OpenAI API Docs](https://developers.openai.com/api/docs/models/gpt-6-astra)
  - [GPT-6 Astra System Card — OpenAI Deployment Safety Hub](https://deploymentsafety.openai.com/gpt-6-astra)
  - [Safety overview: GPT-6 Astra — OpenAI](https://openai.com/index/safety-overview-gpt-6-astra/)
  - [Path to Astra: critical capabilities and frontier safeguards — OpenAI](https://openai.com/index/path-to-astra/)
  - [Benchmarking GPT-6 Astra — Artificial Analysis](https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra)
  - [OpenAI launches GPT-6 Astra, its first model to cross a critical cybersecurity threshold — CSO Online](https://www.csoonline.com/article/4218679/openai-launches-gpt-6-astra-its-first-model-to-cross-a-critical-cybersecurity-threshold.html)
  - [OpenAI Releases GPT-6 Astra, Its First Model Rated Critical for Cybersecurity — Unite.AI](https://www.unite.ai/openai-releases-gpt-6-astra-its-first-model-rated-critical-for-cyber/)

> ⚠️ 本文為對兩支公開影片的整理與交叉查證。§9 已標示核實狀態與三點補充。
> 模型定價與能力變動快速,**具體數字以 OpenAI 官方定價頁與系統卡為準**。
> §4 對 computer use 的評價兩位作者相反,文中已並陳。
