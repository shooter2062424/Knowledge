# GitHub Weekly 第 99 期:AI 程式代理編排、Claude Skills 與 Agent 生成 UI

> **期數:** #99(2025/12/29–2026/01/03)
> **本期主題:** AI 編碼代理的編排平台、Claude skill、Agent 生成 UI、macOS 系統清理工具、終端文字編輯器與履歷產生器。
> 來源:itcoffee66/githubweekly 第 99 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **vibe-kanban** | 指揮多個 AI 編碼代理幹活的中央調度看板 | AI 程式工具 |
| 2 | **skills** | Anthropic 官方 50+ 個可定制 Claude skill 範本庫 | Claude/Agent |
| 3 | **A2UI** | 讓 AI Agent 生成可渲染 UI 的開源協定 | Agent/前端 |
| 4 | **Mole** | 把多款付費工具整合成一個的 macOS 清理工具 | 系統工具 |
| 5 | **fresh** | 非模式、效能導向的終端文字編輯器 | 開發工具 |
| 6 | **rendercv** | 用 YAML 寫、一行指令產生排版漂亮 PDF 的履歷產生器 | 生產力 |

---

## 1. vibe-kanban — 指揮多個 AI 編碼代理的中央調度台

- **連結:** <https://github.com/BloopAI/vibe-kanban>
- **用途:** 號稱能讓你的 Claude Code / Codex 等工具效率提升 10 倍。它不是傳統手動拖拽任務的看板軟體,而是一個能真正「指揮 AI 幹活」的中央調度台:幫開發者規劃、審查並安全地執行 AI 輔助的編碼任務。
- **亮點:**
  - **每個任務都在獨立的 Git 工作樹(worktree)中執行**,讓你在充分利用 AI 助手的同時,仍完全掌控程式碼庫,避免多個 agent 同時改檔互相干擾。
  - 支援主流編程 agent;本地裝好支援的 agent 後,以 `npx` 一行指令即可安裝啟動。
  - 可配置 **GitHub 整合** 與 **MCP 整合**。
  - 解決「AI 一執行任務,人就只能盯著它閃爍的執行過程、又不敢同步改檔」的痛點。

> **應用案例:** 你同時有三項工作要交給 AI——修一個 bug、寫一份新功能、重構一個模組。與其開三個終端機輪流盯著 Claude Code 跑、深怕同時動到同一份檔案搞衝突,不如在 vibe-kanban 建三張任務卡,各自跑在獨立 Git 工作樹裡,你只需在看板上審查、合併它們的成果。

## 2. skills — Anthropic 官方的 Claude skill 範本庫

- **連結:** <https://github.com/anthropics/skills>
- **用途:** Claude skill 是近期非常熱門的概念。它本質上不是「新模型」,而是一種「結構化能力模組」的抽象方式,定義一組可複用、可呼叫、可組合的能力單元。本倉庫收錄 50 多個可隨時定制的 Claude skill。
- **亮點:**
  - 涵蓋:文件處理(Word、PDF、PowerPoint)、開發工具(Playwright、AWS、Git)、數據分析、商業與行銷、溝通、創意媒體、生產力、專案管理與安全。
  - 每個類別都有自己的資料夾,內含清晰的 `SKILL.md`,詳列提示詞與邏輯。
  - **skill 與 MCP 的關係是互補而非重疊**:MCP 連接讓 Claude 能存取各種工具,skill 則教會 Claude 如何有效地「使用」這些工具,兩者可組合使用。
  - 即使部分 skill 偏雞肋,整個倉庫仍是極佳的 sample——想做自己定制的 skill 時,拿它當基礎很好用。

> **應用案例:** 你想讓 Claude 自動把一批會議逐字稿整理成 PowerPoint 簡報。與其從零摸索提示詞,直接從這個倉庫複製 PowerPoint 處理相關的 `SKILL.md`,改寫成符合你公司模板的版本,就能快速擁有一個專屬的「簡報產生 skill」。

## 3. A2UI — 讓 AI Agent 生成可渲染 UI 的開源協定

- **連結:** <https://github.com/google/A2UI>
- **用途:** 由 Google 及社群聯合維護的開源協定加函式庫集合,用來讓 AI Agent 生成富互動的使用者介面,並能在 Web、行動、桌面等不同平台上原生渲染,而不只靠純文字互動。
- **亮點:**
  - 傳統聊天式互動只靠自然語言來回,面對「預訂餐廳」「填寫表單」這類操作會產生大量「來回問答加結果推理」。
  - A2UI 的思路是讓 agent 輸出一組可渲染的介面結構描述(JSON),前端客戶端再依自己的元件庫渲染成真實 UI 元件,讓使用者直接操作。
  - 換句話說,agent 不再只回答「什麼時候預訂?」,而能直接給你一套帶日期選擇器、時間選擇器與確認按鈕的完整介面,互動更直觀自然。
  - 正在構建一個面向 AI 驅動 UI 互動的新標準。

> **應用案例:** 以前做簡單 agent demo,你可能用 streamlit 手刻表單。現在做一個「訂餐助理」,可直接讓 agent 透過 A2UI 輸出一份含餐廳清單、日期/時間選擇器與確認按鈕的 JSON,前端自動渲染成可點選的真實介面,使用者三秒完成預訂,不必再打字來回問答。

## 4. Mole — 把多款付費工具整合成一個的 macOS 清理工具

- **連結:** <https://github.com/tw93/Mole>
- **用途:** 用 Go 加 Shell 打造的開源 macOS 系統清理與優化工具,透過終端介面實現「深度清理、卸載應用、分析磁碟、系統優化」等功能。
- **亮點:**
  - 目標是把多個付費工具(CleanMyMac、AppCleaner、DaisyDisk、Sensei、iStat)整合到一個開源命令列體驗裡。
  - 可用 brew 快速安裝,執行指令 `mo` 即可使用;啟動後顯示互動式選單,用方向鍵選擇不同操作。
  - 主要功能:清理占空間的「隱形垃圾」、徹底刪除應用程式、磁碟可視化分析、系統優化、顯示即時系統狀態。
  - 擔心誤刪可先用 `--dry-run` 看一遍清理計畫,避免刪到重要檔案。

> **應用案例:** 你的 MacBook 只剩幾 GB 空間,但又不想花錢買 CleanMyMac。直接 `brew` 裝 Mole,執行 `mo` 後先用 `--dry-run` 確認清理清單,確認沒誤刪重要快取後,一次清掉 Xcode、Docker 殘留的數十 GB 隱形垃圾。

## 5. fresh — 非模式、效能導向的終端文字編輯器

- **連結:** <https://github.com/sinelaw/fresh>
- **用途:** 一個終端裡的文字編輯器,主打「像 VS Code / Sublime 那樣直覺、非模式(non-modal)」的互動,不要求你先背一套 Vim / Emacs 快捷鍵。
- **亮點:**
  - 有完整選單、命令面板、滑鼠支援,盡量開箱即用。
  - **強調效能**:設計目標是能高效處理多 GB 級大檔或慢速網路串流,並保持很低的記憶體開銷,避免傳統編輯器在大檔上卡成 PPT。
  - 功能完整:檔案管理、分屏、搜尋取代、多游標、Markdown 預覽、LSP(跳轉定義/補全/診斷/重新命名等)、git 相關能力都覆蓋。
  - **外掛用 TypeScript 寫,並在沙箱化的 Deno 環境裡執行**,既能用現代 JS 生態,又不至於把編輯器穩定性當盲盒。
  - 提供一鍵安裝腳本,也支援 brew、npm 等多種方式。

> **應用案例:** 你 SSH 連到伺服器要編輯一個 5 GB 的 log 檔,用 Vim 開到卡死、又不想臨時背一堆模式指令。改用 fresh,滑鼠點選、Ctrl+F 搜尋都跟桌面編輯器一樣,還能在低記憶體下流暢捲動這份巨檔。

## 6. rendercv — 用 YAML 寫、一行指令產生 PDF 的履歷產生器

- **連結:** <https://github.com/rendercv/rendercv>
- **用途:** 面向學術與工程人群的履歷產生器:用 YAML 寫履歷內容,然後一條指令 `rendercv render xxx.yaml` 就能生成排版穩定、間距一致、字體排印講究的 PDF。
- **亮點:**
  - 可把履歷當純文字進 Git 版本管理。
  - 提供多種主題範例與非常細的設計選項(頁面尺寸、邊距、配色、字體、行距、對齊方式等)。
  - 附 **JSON Schema**,編輯 YAML 時可獲得自動補全與內聯說明;同時做嚴格校驗,填錯欄位會明確告訴你哪裡錯,避免「渲染出來才發現炸版」。
  - 安裝:`pip install "rendercv[full]"`。

> **應用案例:** 你要投不同職缺,需要好幾個版本的履歷。用 rendercv 把內容寫成 YAML 後丟進 Git,每個版本開一個分支只改幾行、一行指令重新 `render` 成 PDF,版控清楚又能保證每次排版一致,不會像 Word 那樣調一處就跑版。

---

## 額外資源(Bonus)

本期另分享兩份報告:

- **《AI agent trends 2026》(Google Cloud)** — 在 Meta 收購 Manus 之後,眾人都看到 AI agent 市場的巨大潛力,這份最新報告值得一看。
- **《全球通用 agent 趨勢洞察》** — 深度分析 8 款代表性通用 agent 產品(ChatGPT、Claude、Manus、Genspark、Lindy、Flowith、Gumloop、Relay),並結合數據做分析。

> 原作者以夸克網盤分享「一週熱點 99 期」資料:<https://pan.quark.cn/s/d092e17f4058>

---

## 一句話總結

> 本期主軸圍繞「**讓 AI Agent 從寫程式到生介面都更好用**」:vibe-kanban 編排多個編碼代理、skills 提供官方能力模組範本、A2UI 讓 agent 直接吐出可操作的 UI;另外三個則是實用工具——Mole 清理 macOS、fresh 處理大檔的終端編輯器、rendercv 工程化管理履歷。

---

## 來源

- [GitHub Weekly 第 99 期原文](https://github.com/itcoffee66/githubweekly/blob/main/_weekly/99.md)
- [itcoffee66/githubweekly(週報倉庫)](https://github.com/itcoffee66/githubweekly)
- 各專案連結見上文各節。
