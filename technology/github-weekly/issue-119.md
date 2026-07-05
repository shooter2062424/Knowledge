# GitHub Weekly 第 119 期:生產級 Agent 技能包、蘋果官方容器、NVIDIA 物理 AI 世界模型、開源客服平台、公開 IPTV 清單

> **期數:** #119(2026/06/14–06/20)
> **本期主題:** Addy Osmani 的生產級工程 Agent 技能包、蘋果第一方容器工具、NVIDIA 物理 AI 世界模型 Cosmos、開源全渠道客服平台、以及世界盃期間爆紅的公開 IPTV 播放清單。
> 來源:itcoffee66/githubweekly 第 119 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **agent-skills** | Addy Osmani 的生產級工程 Agent 技能包(反偷懶) | Agent Skill |
| 2 | **container** | 蘋果官方、為 Apple Silicon 優化的 Linux 容器工具 | 開發環境 |
| 3 | **cosmos** | NVIDIA 開源的物理 AI 世界模型平台 | 世界模型 |
| 4 | **Chatwoot** | 開源全渠道客服平台(對標 Zendesk) | 客服/SaaS |
| 5 | **IPTV** | 全球公開 IPTV 頻道播放清單(12 萬星) | 資源目錄 |

---

## 1. agent-skills — 生產級工程 Agent 技能包

- **連結:** <https://github.com/addyosmani/agent-skills>
- **用途:** Google Gemini 團隊主管 **Addy Osmani** 開源的 AI 編程 Agent 技能包。把一個資深工程師做開發會用到的流程,拆成可被 Agent **穩定執行**的技能——解決「模型越強、越愛走捷徑、拿到任務就一股腦往前衝」的毛病。
- **亮點:**
  - **24 個技能**(23 個開發生命週期 + 1 個元技能判斷該用哪個);7 個 Slash 命令、3 個 Agent 人設。主線分階段:**Define → Plan → Build → Verify → Review → Ship**——把檢查點、質量門禁、反偷懶規則都寫進 skill。
  - 對 Claude Code 支援最完整,也支援 Cursor/Gemini CLI/OpenCode/Codex。
  - 與 **Superpowers**(強調完整工程流程)常被拿來搭配;社群都想把兩者結合。

> **應用案例:** 每天和 agent 一起開發、想從「讓 AI 幫我寫代碼」升級到「讓 AI 專業地完成工程」的重度用戶。這位 Addy Osmani 正是本庫 [[loop-engineering-when-and-how-gary-chen]]、[[loop-engineering-buzzword-critique]] 裡把 Loop Engineering 寫成框架的人。

## 2. container — 蘋果官方容器工具

- **連結:** <https://github.com/apple/container>
- **用途:** 蘋果第一方工具,在 Mac 上用**輕量虛擬機**創建與運行 Linux 容器,專為 Apple Silicon 優化。用 Swift 寫,底層依賴蘋果的虛擬化與網路能力。
- **亮點:**
  - 支援 OCI 相容鏡像(可從標準倉庫拉、也能推回),接進現有容器生態。
  - 最受關注的是它是**蘋果親兒子**——過去 Mac 上跑容器繞不開 Docker Desktop / OrbStack,現在官方下場,說明蘋果越來越重視本地開發與容器體驗。
  - 門檻不低:需 **Apple Silicon + macOS 26**;仍在活躍開發、小版本間才相對穩定,不急著替換。

> **應用案例:** Apple Silicon + 新系統的開發者,想試官方原生的容器方案。

## 3. cosmos — NVIDIA 物理 AI 世界模型

- **連結:** <https://github.com/NVIDIA/cosmos>
- **用途:** NVIDIA 開源的**物理 AI 世界模型平台**,面向機器人、自動駕駛、智慧基礎設施。給物理世界的 AI 系統提供世界模型、資料集與工具——讓 AI 不只看圖回答,而是**理解物理世界會怎麼變化、下一步可能發生什麼**。
- **亮點:**
  - 重點是 **Cosmos 3**:一組 **omnimodal** 世界模型,統一處理與生成語言/圖像/影片/音頻/動作序列,把視覺語言理解、影片生成、世界模擬、動作預測、機器人訓練放在同一框架。
  - 兩個使用面:**Reasoner**(理解推理——判斷時序事件、物理合理性、下一步動作)與 **Generator**(生成模擬——生成未來畫面/聲音/動作軌跡)。
  - 機器人/自駕最缺的不是會聊天的模型,而是**能理解現實世界**的模型(機器人拿杯子要知道杯子會不會倒)。對算力與環境要求不低,偏研究與產業基礎設施。

> **應用案例:** 做機器人/自駕、需要世界模型當「物理直覺」的團隊。對照本庫 world-models 類筆記([[sutton-enactive-ai]] 等)。

## 4. Chatwoot — 開源全渠道客服平台

- **連結:** <https://github.com/chatwoot/chatwoot>
- **用途:** 開源客服平台,對標 Zendesk、Salesforce Service Cloud。把散在官網聊天/郵件/FB/IG/Twitter/WhatsApp/Telegram/簡訊的對話,收進**統一的 inbox**。
- **亮點:**
  - 全渠道客服、團隊協作、標籤、快捷回覆、自動分配、多語言、幫助中心(FAQ/知識庫)。
  - 在加 AI Agent **Captain**:自動回答常見問題減輕人工壓力——**客服是最適合 AI 落地的場景之一**(問題重複、流程明確、知識庫可控、效果易衡量)。
  - 最大價值是**開源與自部署**:適合覺得 Intercom/Zendesk 貴、重、資料不想放別人那裡的中小團隊/獨立產品/SaaS。

> **應用案例:** 中小團隊要一個可控、可自部署、能接 AI 的全渠道客服系統。

## 5. IPTV — 全球公開 IPTV 播放清單

- **連結:** <https://github.com/iptv-org/iptv>(12 萬+ star)
- **用途:** 把全球公開可訪問的 IPTV 頻道整理成 **M3U 播放清單**。把清單連結貼進 VLC 這類支援串流的播放器即可開。(世界盃期間爆紅。)
- **亮點:**
  - 主清單 `https://iptv-org.github.io/iptv/index.m3u`,另按國家/語言/分類整理;還有配套 **EPG 節目單、頻道資料庫與 API**——已是一套開源電視直播資源目錄。
  - ⚠️ **世界盃這類強版權節目看不到**(版權賣到幾億)。

> **應用案例:** 有電視盒/NAS/家庭影院,或想在電腦上集中管理公開直播源時很方便。

---

## One More Thing(本期附帶資料)

- **《2026 創作者經濟報告》**:匯總 TikTok/YouTube/Instagram 數據,分析創作者收入結構與 AI 對內容業的影響;AI 推動創作者從「內容生產者」轉型為「個人媒體公司」。
- **《智能體安全研究報告》**(80 頁):agent 從聊天機器人進化成能執行任務的行動系統,系統梳理權限管理、工具調用、MCP、沙箱隔離、審計追蹤等核心安全問題,提出企業級 Agent 控制平面思路。呼應本庫 [[prompt-injection-5-techniques-defenses]]。

---

## 來源

- itcoffee66/githubweekly 第 119 期:<https://github.com/itcoffee66/githubweekly/blob/main/_weekly/119.md>(2026/06/14–06/20)
