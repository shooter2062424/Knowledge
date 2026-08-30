# GitHub Weekly 第 120 期:Agent 影片生產系統、用戶名情報搜索、Agent 聯網能力層、代碼庫記憶 MCP、開源剪輯工具

> **期數:** #120(2026/06/21–06/27)
> **本期主題:** 把編程 agent 變影片工作室的生產系統、跨 3000 站的用戶名 OSINT 工具、給 agent 一鍵裝上聯網能力的「工具箱管理器」、把 repo 建成本地知識圖譜的記憶 MCP、以及走向 AI 化的開源剪輯器。
> 來源:itcoffee66/githubweekly 第 120 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **OpenMontage** | 把編程 agent 變成完整影片製作工作室 | AI 影片 |
| 2 | **Maigret** | 輸入用戶名跨 3000+ 網站查公開帳號的 OSINT | 情報/安全 |
| 3 | **Agent-Reach** | 給 agent 一鍵裝上互聯網能力的「工具箱管理器」 | Agent 工具 |
| 4 | **codebase-memory-mcp** | 把 repo 索引成本地知識圖譜、經 MCP 給 agent 查 | 程式記憶 |
| 5 | **OpenCut** | 走向 AI 化的開源剪輯器(CapCut 替代) | 影片剪輯 |

---

## 1. OpenMontage — Agent 影片生產系統

- **連結:** <https://github.com/calesthio/OpenMontage>
- **用途:** 自稱「全球首個開源智能體影片製作系統」,把 AI 編程 agent 變成完整影片工作室。用自然語言描述(如「做一個 60 秒神經網路科普動畫」),agent 就去做選題研究、腳本、素材、配音、字幕、音樂、剪輯與最終合成——把影片生產拆成一套 **pipeline** 按流程執行。
- **亮點:**
  - 內建 **12 條製作流水線**(動畫解說、紀錄片剪輯、虛擬人播報、電影預告、螢幕錄製、播客切片、多語言本地化等)、52 個製作工具、500+ Skill;支援免費資源(免 API Key 也能做)。
  - 給 Claude Code/Cursor/Codex 用的**影片生產工程框架**(需 Python/Node.js/FFmpeg;效果好還是要配 OpenAI/Pexels/ElevenLabs/Runway 等)。**上限取決於你給它多少能力。**
  - 可**復刻爆款**:給它一個參考影片,分析字幕/節奏/場景/關鍵幀/風格,生成新製作方案。

> **應用案例:** 短視頻創作者做「人提要求、Agent 拆流程、工具鏈自動執行」的批量生產。與本庫 [[hyperframes(issue-116)]]、[[claude-fable-72-hours-model-dependency]] 的 AI 影片路線呼應。

## 2. Maigret — 用戶名情報搜索(OSINT)

- **連結:** <https://github.com/soxoj/maigret>
- **用途:** OSINT 工具,輸入一個用戶名,在 **3000+ 網站**查找對應公開帳號並整理成報告。免 API Key,`pip install maigret` 後 `maigret 用戶名`(預設查流量最高的 500 站)。
- **亮點:**
  - 不只查「有沒有帳號」,還盡量從公開頁面提取可用資訊(個人主頁、關聯帳號、其他 ID),可遞歸搜索;有 Web 界面(圖形瀏覽結果)、可導出 HTML/PDF/XMind;新增 AI analysis 模式整理成調查摘要。
  - 對中國大陸平台(抖音/小紅書/B 站)支援有限(風控強),更適合查跨平台、偏海外的用戶名足跡。

> **應用案例:** 資安/盡職調查的公開情報蒐集。也給普通人一個提醒:**別在所有平台用同一個用戶名**——工作/生活/投資/遊戲/社交混用,很容易被串成一張圖。

## 3. Agent-Reach — 給 Agent 一鍵裝上互聯網能力

- **連結:** <https://github.com/Panniantong/Agent-Reach>
- **用途:** 給 AI Agent 一鍵裝上聯網能力。解決「agent 寫代碼很強、但一上網找東西就麻煩」(讀網頁要處理 HTML、Twitter 要登入、Reddit 匿名 403、小紅書要瀏覽器登入態……)。
- **亮點:**
  - 做法不是重寫所有平台,而是做一個**能力層**:幫你選當前最穩的上游工具、裝好配好,`agent-reach doctor` 體檢;真正讀取時 agent 直接調用對應上游工具。
  - 核心設計「**每個平台 = 首選 + 備選的有序後端列表**」:網頁用 Jina Reader、GitHub 用 `gh` CLI、YouTube 字幕/搜索用 **yt-dlp**、B 站 bili-cli、Twitter twitter-cli(備選 OpenCLI)、Reddit OpenCLI/rdt-cli、小紅書 OpenCLI/xiaohongshu-mcp。
  - 像給 agent 裝一個「聯網工具箱管理器」。⚠️ 需 Cookie 的平台(Twitter/小紅書)**別用主帳號**,有封號風險。

> **應用案例:** 想讓自己的 agent 穩定抓各平台內容,又不想逐一折騰認證。與本庫 CLAUDE.md 的 YouTube 抓取流程(yt-dlp)同源。

## 4. codebase-memory-mcp — 代碼庫記憶 MCP

- **連結:** <https://github.com/DeusData/codebase-memory-mcp>
- **用途:** 面向 AI 編程 agent 的代碼庫記憶與代碼智能引擎。把 repo 索引成**本地知識圖譜**,經 **MCP** 給 Claude Code/Codex CLI/Gemini CLI/OpenCode/OpenClaw 查詢——解決「agent 每次 grep→讀檔→再 grep,token 燒飛、還漏掉調用關係」。
- **亮點:**
  - 把函式/類/調用鏈/HTTP 路由/跨服務關係/基礎設施配置都變成圖上節點與邊。**普通 repo 毫秒級索引,Linux kernel(2800 萬行/7.5 萬檔)3 分鐘索引完**;用 **tree-sitter 支援 158 種語言** + Hybrid LSP 語義類型解析。
  - 全程本地、代碼不出機器、單一靜態二進位檔、支援 3D 圖譜可視化(隱私敏感企業重要)。
  - 與 118/116 期的人看向工具不同,它是**給 agent 建可查詢的代碼知識圖譜**(結構化、持續記憶、精準查詢);小專案 agent 自己 grep 反而最好,幾十萬行以上多語言大專案才有價值。

> **應用案例:** 大型多語言 repo 上跑 agent 想省 token。**本庫已有這篇論文的完整深度筆記** → [[codebase-memory-treesitter-knowledge-graph-mcp]](arXiv 論文整理),兩者對照可看實作與論文兩面。

## 5. OpenCut — 走向 AI 化的開源剪輯器

- **連結:** <https://github.com/OpenCut-app/OpenCut>
- **用途:** 開源影片剪輯工具,支援 Web/桌面/移動端,定位 **CapCut(剪映國際版)的開源替代**。目前官網跑 classic 版,新版正在從零重寫。
- **亮點:**
  - 新版方向都指向 **AI**:Editor API、插件優先架構、一套代碼覆蓋三端、**MCP server、headless mode、編輯器內 scripting tab**。
  - 有了穩定 Editor API + 插件 + 無頭模式 + MCP,agent 就能參與:自動粗剪、批量加字幕、依腳本生成時間線、替換素材、輸出多比例版本,甚至依評論回饋自動改一版。
  - 現階段別期待馬上取代達芬奇/PR/剪映,更適合關注它面向自動化的架構方向。

> **應用案例:** 期待「人和 agent 一起操作專案檔」的剪輯未來時,可關注可腳本化/可插件化/可 MCP 的開源剪輯器。

---

## One More Thing(本期附帶資料)

- **《2026 全球人工智能 OPC 模式商業洞察報告》**:系統梳理 **OPC(One Person Company,一人公司)** 的商業模式、發展路徑、案例與趨勢,對 AI 原生公司、一人獨角獸、Agent 驅動創業有完整介紹。呼應本庫 [[zero-person-ai-company]]、[[anthropic-startup-playbook]]。
- **《2026 中國 AI 應用全景圖譜報告》**(量子位智庫):從 To C、To B 到底層開發工具,梳理國內主流 AI 產品與方向,含 AI 五大趨勢與大量產品數據/生態圖譜。

---

## 來源

- itcoffee66/githubweekly 第 120 期:<https://github.com/itcoffee66/githubweekly/blob/main/_weekly/120.md>(2026/06/21–06/27)
