# GitHub Weekly 第 110 期:史上最快爆紅的 Rust 版 Claude Code、端側 AI、記憶宮殿與自進化 Agent

> **期數:** #110(2026/04/05–04/11)
> **本期主題:** GitHub 歷史增長最快的專案(Rust 重寫的 Claude Code)、Google 的端側 AI 體驗 App、由《惡靈古堡》女主角發起的 AI 記憶系統、會自我進化的開源 Agent,以及一款免費的錄影神器。
> 來源:itcoffee66/githubweekly 第 110 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **claw-code + oh-my-codex** | Rust 重寫的 Claude Code(史上增長最快),加上 Codex CLI 的工作流強化層 | AI 程式工具 |
| 2 | **Google AI Edge Gallery** | Google 出的「手機端側 AI 模型體驗館」,離線跑開源模型 | 端側 AI |
| 3 | **MemPalace** | 用「記憶宮殿」架構組織 AI 對話記憶,基準測試刷出最高分 | AI 記憶系統 |
| 4 | **Hermes Agent** | 會自動長技能、自省沉澱知識的自進化開源 Agent | 自主 Agent |
| 5 | **OpenScreen** | MIT 授權、免費無浮水印的跨平台錄影軟體 | 工具/錄影 |

---

## 1. claw-code + oh-my-codex — Rust 版 Claude Code 與它背後的 Codex 工作流層

- **連結:** <https://github.com/ultraworkers/claw-code>
- **連結:** <https://github.com/Yeachan-Heo/oh-my-codex>
- **用途:** 本期用「1+1」的方式介紹兩個強相關專案。
  - **claw-code** 是用 **Rust 完全重寫的 Claude Code**,短短 2 週就衝上 **18 萬+ star**,號稱目前 GitHub 歷史上增長速度最快的專案。它源自上期提到的 Claude Code 原始碼外洩事件——有人拿到原始碼後立刻以 Python 與 Rust 重寫,專案介紹寫著「finally unlocked」(終於解禁)。
  - **oh-my-codex (OMX)** 是 claw-code 重寫過程中用到的工具:一個建構在 **OpenAI Codex** 之上的 **工作流層**,補強 Codex 在工作流管理上的弱項。
- **亮點:**
  - claw-code:Rust 重寫、效能取向,2 週累積 18 萬+ star,曾一度下架後又解禁。
  - oh-my-codex 的工作流組織方式:**team mode**(並行 review)、**ralph mode**(持久執行迴圈)、**architect 級驗證**、**codex 驅動實作**。
  - Codex 本身是不錯的程式執行引擎,但工作流管理較弱,OMX 正好補上這塊。
  - 安裝極簡:`npm install -g oh-my-codex`,再執行 `omx setup` 即可。
  - **注意:** OMX 是針對 **Codex CLI** 的強化;若使用的是 Codex App 請勿安裝,可能會出問題。

> **應用案例:** 一位習慣用 Codex CLI 的工程師,想把一個中型專案「整包重寫」成另一種語言。
> 他用 OMX 開 team mode 讓多個 agent 並行 review 現有程式碼,再用 ralph mode 持續跑實作迴圈、
> architect 層把關架構正確性——這正是 claw-code 把 Claude Code 重寫成 Rust 的同一套流程。

> ⚠️ **使用聲明:** claw-code 源自 Claude Code **原始碼外洩**事件的重寫版本,其來源與授權正當性具爭議。
> 學習其架構與重寫手法無妨,但商用、散布前請務必確認授權與法律風險,切勿直接挪用外洩程式碼。

## 2. Google AI Edge Gallery — Google 的手機端側 AI 體驗館

- **連結:** <https://github.com/google-ai-edge/gallery>
- **用途:** Google 推出的「**本地 AI 應用商店 + 模型跑分 / 演示平台**」。可離線在手機上運行最新開源模型(如 Gemma 4),完全使用手機本身的 GPU 資源,第一時間體驗 Google 最新的模型能力。
- **亮點:**
  - 不只聊天,還內建多個功能模組:**Agent Skills**(接維基百科做事實查核)、**Ask Image**(拍照辨識物體、解視覺謎題)、**Audio Scribe**(即時語音轉錄),甚至有 **Tiny Garden** 小遊戲(用自然語言種虛擬花園)。
  - 底層採 Google 的 **LiteRT** 推論引擎,支援從 **Hugging Face** 下載各種開源模型。
  - 可自己跑 **Benchmark**,看每個模型在你手機上的實際表現。
  - 直接從 Google Play 或 App Store 下載即可用(需切換到海外區,中國區目前無此 App)。
  - 目前主要為體驗與演示性質。

> **應用案例:** 想知道「大模型跑在手機上到底是什麼體驗」的入門者,下載 Gallery 後從 Hugging Face 拉一個量化版開源模型,
> 在飛航模式(完全離線)下跟它聊天、用 Ask Image 拍下路牌讓它翻譯,再開 Benchmark 比較不同模型在自己手機上的 token/秒,
> 一支 App 就摸清端側 AI 的能耐與極限。

## 3. MemPalace — 用「記憶宮殿」架構打造的 AI 記憶系統

- **連結:** <https://github.com/milla-jovovich/mempalace>
- **用途:** 解決「**你和 AI 聊的所有內容,每次會話結束就消失**」的痛點。MemPalace 把對話全部存下來,並用「記憶宮殿」的架構加以組織,而非一股腦堆積。4 月 5 日才建立,短短 4 天衝到近 3 萬 star;發起人正是演《惡靈古堡》的 **米拉·喬娃維琪(Milla Jovovich)**。
- **亮點:**
  - **記憶宮殿原理** 源自古希臘演說家的記憶術:把資訊放進想像建築的不同房間。MemPalace 把對話依專案、人物分成不同的「翼(wing)」,翼下分「廳」,廳下分「室」,形成可導航的記憶地圖。
  - 在 **LongMemEval** 基準上,raw mode 拿到 **96.6% R@5**,號稱迄今公開發布的最高分。
  - **零 API 呼叫、完全本地運行**;透過 **MCP 協定** 整合 Claude Code、Cursor、Gemini 等主流工具。
  - 安裝一行:`pip install mempalace`。
  - **誠信插曲:** 上線 48 小時內被社群「打假」——宣稱的「無損壓縮」其實有損(AAAK 模式在基準上比 raw mode 低約 12 個百分點);「+34% 宮殿提升」其實是 ChromaDB 標準功能的效果。發起人很快發公開信承認問題並承諾修復。

> **應用案例:** 一位用 Claude Code 開發、橫跨多個專案的工程師,常苦於「上週跟 AI 討論的架構決策,這週全忘了」。
> 接上 MemPalace 後,所有對話依「專案翼 → 模組廳 → 功能室」歸檔,需要時用 MCP 讓 AI 直接導航回相關「房間」取脈絡,
> 不必每次重貼背景;而且全程本地、不打外部 API。

## 4. Hermes Agent — 會自己進化的開源 AI Agent

- **連結:** <https://github.com/NousResearch/hermes-agent>
- **用途:** Nous Research 做的開源 AI Agent,核心賣點是「**會和你一起成長**」——不是每次對話完就失憶,而是內建學習迴圈。
- **亮點:**
  - **自動長技能:** 任務完成後自動建立 skill,日後遇到類似任務直接複用。
  - **持久記憶:** 用 **SQLite + FTS5** 全文搜尋跨會話檢索歷史對話。
  - **定期自省:** 主動把重要知識沉澱下來。
  - **多後端:** 支援本地、Docker、SSH、Daytona、Modal 等;Daytona 與 Modal 提供 **Serverless 持久化**(閒置自動休眠、有訊息時喚醒)。
  - **模型全支援:** OpenRouter 上 200 多個模型、OpenAI、Anthropic、Kimi、MiniMax 及私有模型,一條命令切換 `hermes model`。
  - **訊息平台全覆蓋:** Telegram、Discord、Slack、WhatsApp、Signal 及 CLI;支援用自然語言設定定時任務。
  - **搶用戶利器:** 提供 `hermes claw migrate`,可從 **OpenClaw** 自動匯入記憶、技能、設定與 API 金鑰。社群討論多拿它與 OpenClaw 比較,不少人認為更好。

> **應用案例:** 把 Hermes Agent 接上自己的 Telegram,讓它當長期助理。第一次教它「整理每週 GitHub 週報」的流程後,
> 它自動把這套步驟存成 skill;下週只要說「跑週報」,它就複用既有技能、從 SQLite 記憶裡撈出上週脈絡,
> 並透過 Modal 在閒置時休眠省成本、有新訊息再喚醒。

## 5. OpenScreen — 免費無浮水印的錄影神器

- **連結:** <https://github.com/siddharthvaddem/openscreen>
- **用途:** 開源免費的錄影軟體,鎖定「錄影」這個剛需品類,定位是更簡單版的 **Screen Studio**,覆蓋大多數人的核心需求。
- **亮點:**
  - 以 **Electron + PixiJS** 建構;支援錄製指定視窗或全螢幕。
  - 自動或手動加入 **縮放動畫**;可錄麥克風與系統音訊。
  - 支援裁剪、變速、標註(文字、箭頭、圖片),可自訂背景(桌布、純色、漸層)。
  - 匯出支援不同比例與解析度。
  - **MIT 授權**,個人與商業用途皆免費——錄影工具中少見(同類多半收費或帶浮水印)。
  - 支援 macOS、Windows、Linux;macOS 上可能需處理 Gatekeeper 攔截(給終端 Full Disk Access 後執行 `xattr` 命令)。

> **應用案例:** 一位獨立開發者要錄產品 Demo 上架到官網,但商用付費錄影軟體太貴、免費版又帶浮水印。
> 改用 OpenScreen 錄下操作畫面,加上自動縮放動畫聚焦關鍵步驟、用箭頭與文字標註重點,
> 再設一個漸層背景匯出成適合社群的比例——零成本、無浮水印、可商用。

---

## 額外資源(Bonus)

本期 one more thing 另分享兩份報告:

- **《具身智慧發展報告》** — 中國信通院出品。具身智慧(embodied intelligence)被視為 AI 未來的集大成者;適逢第二屆機器人馬拉松即將開跑,關注此領域者可先讀。
- **《2026 老年群體 AI 應用研究報告》** — 安永(EY)出品。探討 60 至 85 歲人群如何與 AI 互動及其影響,聚焦「確保老年人不被 AI 時代落下」的包容性挑戰。

(原文透過誇克網盤分享上述資料。)

---

## 一句話總結

> 本期主軸是「**Agent 與端側 AI 的爆發**」:claw-code 以驚人速度把 Claude Code 重寫成 Rust、
> MemPalace 與 Hermes Agent 分別從「記憶」與「自我進化」逼近長期可用的 Agent、
> Google AI Edge Gallery 把大模型搬進口袋;最後 OpenScreen 補上一個人人都用得到的免費錄影工具。

---

## 來源

- [GitHub Weekly 第 110 期原文](https://github.com/itcoffee66/githubweekly/blob/main/_weekly/110.md)
- [itcoffee66/githubweekly(週報倉庫)](https://github.com/itcoffee66/githubweekly)
- 各專案連結見上文各節。
