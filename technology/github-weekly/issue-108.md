# GitHub Weekly 第 108 期:Claude Code 終極優化、離線生存電腦與從零手搓 Agent

> **期數:** #108(2026/03/21–03/27)
> **本期主題:** Claude Code 的終極優化配置、完全離線的「生存電腦」、從零手搓一個 Claude Code、住在網頁裡的 GUI 代理,以及清華的多代理互動課堂。
> 來源:itcoffee66/githubweekly 第 108 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **Everything Claude Code** | 黑客松冠軍實戰打磨的 Claude Code 配置合集 | AI 程式工具 |
| 2 | **Project N.O.M.A.D.** | 一台完全離線運行的「生存電腦」知識中心 | 離線/應急 |
| 3 | **Learn Claude Code** | 從零手搓一個類 Claude Code 的程式代理 | AI 學習/教材 |
| 4 | **Page Agent** | 住在網頁裡、純文字解析 DOM 的 GUI 代理 | 網頁自動化 |
| 5 | **OpenMAIC** | 一鍵把任何主題變成 AI 多代理互動課堂 | AI 教育 |

---

## 1. Everything Claude Code — 黑客松冠軍實戰打磨的 Claude Code 配置合集

- **連結:** <https://github.com/affaan-m/everything-claude-code>
- **用途:** 不是獨立工具,而是一套經 **10 個月高強度實戰打磨** 的完整 Claude Code 配置合集,涵蓋 Agent、Skill、Hook、快捷命令、規則、MCP 等一整套「Agent Harness 工程化」方案。出自 Anthropic 黑客松冠軍,11 萬 star、6 千 fork。
- **亮點:**
  - 核心思路:與其讓模型每次從零開始,不如給它預裝好「肌肉記憶」——透過精心設計的 Hooks、Rules 與 MCP 配置,讓 Claude Code 編碼時自動載入最佳實踐,**減少 token 浪費、提升輸出品質**。
  - 以 **插件市場(plugin marketplace)** 方式安裝:把此倉庫加為插件市場再安裝,即可一次取得所有 commands / agents / skills / hooks,開箱即用。
  - 內建安全模組 **AgentShield**:針對 Agent 場景做沙箱隔離、輸入過濾與權限管控。
  - 附有快速上手(shorthand)、長篇與安全等多份指南,建議先看 shorthand 快速入門。

> **應用案例:** 你是 Claude Code 重度使用者,常覺得每次新開專案都要重新交代規範、且 token 燒得快——把這個倉庫加為插件市場後,coding agent 立刻擁有預設好的 Hook(例如自動跑測試、自動套用程式風格)與規則,等於把資深工程師的「肌肉記憶」一次裝好。它同時也是理解「Agent Harness 工程化」的絕佳教材。

## 2. Project N.O.M.A.D. — 一台完全離線運行的「生存電腦」

- **連結:** <https://github.com/Crosstalk-Solutions/project-nomad>
- **用途:** N.O.M.A.D. 全稱為 *Node for Offline Media, Archives, and Data*——把一台電腦變成 **完全離線** 的知識中心。想像全球網際網路突然消失、雲端全面癱瘓時,這台電腦仍能運作。
- **亮點:**
  - 打包了:離線 Wikipedia、醫學參考資料、可汗學院課程系統、離線地圖、基於 **Ollama** 的 AI 聊天助手、CyberChef 數據工具、筆記系統等。
  - 所有工具以 **Docker 容器** 編排,單一瀏覽器介面統一管理。
  - 部署門檻低:一台 Ubuntu 機器、一條安裝指令即可跑起。
  - 硬體需求彈性:跑本地大模型至少需 **32GB 記憶體 + 一張像樣顯卡**;若只用離線百科與課程,**4GB 記憶體** 的設備也能跑。
- **適用情境:** 末日生存愛好者之外,在 **災難應急、野外作業、網路受限地區**,或單純想要一台不依賴網際網路的知識終端時都很有價值。

> **應用案例:** 你帶隊到通訊不穩的偏遠山區做工程或醫療志工,沒有穩定網路——把一台筆電裝上 N.O.M.A.D.,隊員就能離線查 Wikipedia、看離線地圖定位、用本地 AI 助手問醫療參考資料,完全不靠基地台或雲端。

## 3. Learn Claude Code — 從零手搓一個程式代理

- **連結:** <https://github.com/shareAI-lab/learn-claude-code>
- **用途:** 名字像「學用 Claude Code」,實際更硬核——它帶你 **從零手撸一個類似 Claude Code 的 AI 程式設計代理**,逐步反向工程 Claude Code 的各個 Harness 機制。
- **亮點:**
  - 核心觀念:所有 AI 程式設計 Agent 共享同一個循環——**呼叫模型、執行工具、回傳結果**;生產級系統只是在其上疊加策略、權限與生命週期層。
  - 把複雜的 Agent 架構拆成 **12 個 Session**,每個 Session 反向工程一個機制:工具系統、上下文壓縮、子 Agent 編排、權限管控、任務系統等。
  - 程式碼從 **84 行一路長到 694 行**,每次只加一個機制,清楚看到每一步解決了什麼問題。
  - 提出 Harness 工程思維不只適用於程式設計,也適用於 **農業、酒店運營、醫療研究、教育** 等任何需要 AI 處理複雜任務的領域。

> **應用案例:** 你會用 Claude Code 但對它「黑盒子」般的運作好奇——跟著 12 個 Session 一行行寫,當你親手實作「上下文壓縮」那一節時,就會真正理解為什麼長對話會自動摘要、token 又是怎麼被省下來的,把對 Agent 的認知從「使用者」提升到「能造輪子」。

## 4. Page Agent — 住在網頁裡的純文字 GUI 代理

- **連結:** <https://github.com/alibaba/page-agent>
- **用途:** 一個「住在網頁裡的 GUI 代理」——**不需要瀏覽器插件、不需要 Python、不需要無頭瀏覽器**,只要一段 JavaScript,就能讓網頁聽懂自然語言指令。阿里通義出品,1.4 萬 star,以 TypeScript 編寫。
- **亮點:**
  - 核心走 **純文字解析 DOM** 路線,而非「截圖 + 視覺模型」:不需多模態大模型、不需特殊瀏覽器權限,**對效能更友善、整合更簡單**。
  - 接入極輕量:一行 `<script>` 標籤即可,也可用 npm 安裝。
  - 支援 **SaaS AI Copilot 整合**,幾行程式碼就能為產品加上 AI 助手、無需重寫後端;另有智慧表單填寫、無障礙訪問等情境。
  - 提供可選的 **Chrome 擴充** 與 **MCP Server**,用於跨頁面任務。
  - 測試推薦搭配 **Qwen** 自家模型(本地運行方便)。
- **定位差異:** 專為「客戶端網頁增強」設計,不是服務端自動化工具;相比需要 Python 後端的方案,更適合 **嵌入產品作為內建功能**。

> **應用案例:** 你的 SaaS 後台想加一個「AI 助手」讓使用者用講的就能操作介面(例如「幫我把這張表單填好並送出」)——只要在頁面塞一段 Page Agent 的 script,它直接解析現有 DOM 操作元件,不必另外架後端服務或裝瀏覽器外掛。

> ⚠️ **使用聲明:** 這類能自動操作網頁、自動填表的代理屬雙面刃,僅供 **合法授權的網站/自家產品** 使用;用於繞過驗證、大量自動操作他人網站可能違反服務條款或當地法律,請自行確認授權與合規。

## 5. OpenMAIC — 一鍵把任何主題變成 AI 多代理互動課堂

- **連結:** <https://github.com/THU-MAIC/OpenMAIC>
- **用途:** 清華大學 MAIC 實驗室出品,全稱 *Open Multi-Agent Interactive Classroom*——**一鍵把任何主題或文件變成沉浸式的 AI 互動課堂**。發布兩週即拿下 1.2 萬 star。
- **亮點:**
  - 自動搭好完整課堂結構:有串聯全程的 **AI 老師**、隨時補充細節的 **技術助教**,以及像「阿強」「木木」這類代表不同基礎、不同關注點的 **AI 同學**。
  - 輸入一個學習主題,系統自動生成 **PPT 課件、測驗題、互動模擬實驗**,再由 AI 老師講課、AI 同學陪你討論;AI 老師還能在白板上畫圖、寫公式、用語音講解。課後可導出可編輯的 **PPTX 或互動 HTML**。
  - 技術上基於 **Next.js + LangGraph**,支援 OpenAI、Anthropic、Google Gemini、DeepSeek、Grok 等多家模型;推薦用 **Gemini 3 Flash**(性價比最高)。
  - 部署方便:支援 **Vercel 一鍵部署** 與 Docker。
  - 內建 **OpenClaw 整合**:可直接在飛書、Slack、Telegram 等聊天工具裡生成課堂,零本地配置。
  - 目前為剛發布的 **v0.1.0**,功能仍在快速迭代。

> **應用案例:** 你想做一門「給高中生的量子力學入門」線上課但沒時間做投影片——丟一份講義給 OpenMAIC,它自動生成 PPT、測驗與模擬實驗,由 AI 老師開講、AI 同學「阿強」幫你問出新手最容易卡的問題,你還能把成果導出成 PPTX 微調後直接拿去上課。

---

## 額外資源(Bonus)

本期另分享兩份資料:

- **《OpenClaw 未來可能方向研究報告》** — 結合 OpenClaw 官方資料、論文等內容做出的方向性研究。
- **《2026 中國企業 AI 應用場景報告》** — 極客時間出品,聚焦 AI 在企業級市場落地的困境與應用場景。

> 原文以夸克網盤分享(連結見下方「來源」原文)。

---

## 一句話總結

> 本期主軸圍繞「**把 Claude Code 與 Agent 玩到極致**」:Everything Claude Code 給你冠軍級的工程化配置、Learn Claude Code 教你親手造一個;Page Agent 與 OpenMAIC 分別把 Agent 能力包進「網頁」與「課堂」;Project N.O.M.A.D. 則提醒我們——當雲端消失時,知識仍要能離線運轉。

---

## 來源

- [GitHub Weekly 第 108 期原文](https://github.com/itcoffee66/githubweekly/blob/main/_weekly/108.md)
- [itcoffee66/githubweekly(週報倉庫)](https://github.com/itcoffee66/githubweekly)
- 各專案連結見上文各節。
