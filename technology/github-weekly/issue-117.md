# GitHub Weekly 第 117 期:開源 Claude Design、上下文壓縮省 token、給 AI「培養審美」、英語學習指南、從零手搓 AI 課程

> **期數:** #117(2026/05/31–06/06)
> **本期主題:** 開源的 Claude Design 替代、AI 上下文壓縮(token 省錢神器)、給編程 agent 注入「設計品味」的 Skill、寫了近十年的英語進階指南、以及從零手搓 AI 工程的免費課程。
> 來源:itcoffee66/githubweekly 第 117 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **Open Design** | 本地優先、開源的 Claude Design 替代(Agent 時代設計工具) | AI 設計 |
| 2 | **Headroom** | 送進 LLM 前先幫 prompt/上下文「瘦身」,省 token | Token 優化 |
| 3 | **Taste Skill** | 給 AI 注入「設計品味規則」的反垃圾前端 Skill | 前端/Skill |
| 4 | **English-level-up-tips** | 寫近十年、5 萬星的英語進階指南(含 AI 輔助章) | 學習資源 |
| 5 | **ai-engineering-from-scratch** | 503 節、從數學到多智能體的免費 AI 工程課 | 學習資源 |

---

## 1. Open Design — 開源的 Claude Design 替代

- **連結:** <https://github.com/nexu-io/open-design>
- **用途:** 本地優先、完全開源的 Claude Design 替代。定位「Agent 時代的設計工具」——不是在畫布拖像素,而是讓 AI 編碼代理從零生成網頁原型、儀表盤、PPT、甚至影片。
- **亮點:**
  - Apache 2.0;支援 Claude Code、Codex、Cursor、OpenClaw、Gemini、Kimi 等 **21 種**編碼代理,一條命令接入。
  - 內建 **259+ Skills、142+ 設計系統**;選 Skill + 風格 + 需求 → 自動生成單頁 HTML 原型、沙盒即時預覽,可導出 HTML/PDF/PPTX/MP4。0.9.0 內建 Model Router 免配 API Key。
  - `od mcp install claude` 一條命令接入常用編碼代理。

> **應用案例:** 獨立開發者做產品官網/活動頁/簡報/行銷素材,直接複用設計規範快速完成。它也展現趨勢:**設計能力會像代碼能力一樣被封裝成標準化、可調用、可共享的 Agent 能力**。對照本庫 [[claude-design-review]]。

## 2. Headroom — 上下文壓縮,Token 省錢神器

- **連結:** <https://github.com/chopratejas/headroom>
- **用途:** 專給 AI Agent 的上下文壓縮工具。在請求送給 LLM **之前**,對 prompt 與上下文中的 token「瘦身」,刪除大量冗餘(估計目前送給模型的 token 最高有 **90%** 是重複/無意義的)。
- **亮點:**
  - 據稱已累計幫用戶省約 **70 萬美元**、釋放 **2000 億+ token** 配額。
  - `pip install "headroom-ai[all]"` → `headroom wrap claude` 零配置壓縮 Claude Code;另有 Python/TS 庫、HTTP 代理、MCP Server 三種接法。
  - 三套壓縮算法:**SmartCrusher**(壓 JSON)、**CodeCompressor**(用 AST 壓代碼)、自訓模型;**壓縮可逆**(原始資料不刪、需要時自動取回)。

> **應用案例:** vibe coding 時 token 耗太快、5 小時額度轉眼見底的解法之一。呼應本庫 [[context-engineering-processing-vs-thinking]]、[[is-graphrag-needed-rag-variants-comparison]] 的脈絡成本主題。

## 3. Taste Skill — 給 AI「培養審美」的反垃圾前端 Skill

- **連結:** <https://github.com/Leonxlnx/taste-skill>(⭐ 32.6k)
- **用途:** 一組能裝進編碼 agent 的 `SKILL.md`,注入「設計品味規則」約束 AI 輸出,讓界面**布局更有層次、排版更講究、動效更自然**——解決 AI 生成前端「一眼就很 AI」(藍紫漸層、免費模板感)的問題。
- **亮點:**
  - 13 個 Skill,涵蓋極簡風(Notion/Linear)、高端柔和、工業粗野主義等;另有「先生成設計參考圖再讓代理照做」的工作流。
  - `npx skills add ...` 一條命令裝進 Codex/Cursor/Claude Code。
  - 三個可調變數:**DESIGN_VARIANCE**(布局實驗性)、**MOTION_INTENSITY**(動畫深度)、**VISUAL_DENSITY**(資訊密度),1–10 自由調。

> **應用案例:** 用 AI 生成前端頁面又不想要「模板感」時,選一個風格 Skill 並微調三變數。與本庫 [[top-skills-for-agents]] 的設計類 Skill 同源。

## 4. English-level-up-tips — 近十年的英語進階指南

- **連結:** <https://github.com/byoungd/English-level-up-tips>(⭐ 51.5k)
- **用途:** 中文網路流傳很廣的英語學習指南(2017 寫到 2026,近十年持續更新)。涵蓋理解/詞彙/聽力/閱讀/口語/寫作全鏈條,朋友聊天式風格。
- **亮點:**
  - 2026 新增 **AI 輔助學習章**:推薦 **Gemini** 當主引擎(把 Live、Guided Learning、Canvas、Quiz、Flashcards 串成訓練流程),並說明 ChatGPT/Claude/Perplexity/DeepL Write 各自分工。

> **應用案例:** 想系統提升英語、又想用 AI 當練習引擎的人的路線圖。提醒:AI 能幫很多事,但**自主學習能力還是要有**。

## 5. ai-engineering-from-scratch — 從零手搓 AI 工程

- **連結:** <https://github.com/rohitg00/ai-engineering-from-scratch>(⭐ 28k)
- **用途:** 免費開源的 AI 工程學習課程(彌合「84% 學生在用 AI 工具、但只 18% 覺得能專業使用」的落差)。
- **亮點:**
  - **503 節課、20 階段、約 320 小時**,涵蓋 Python/TypeScript/Rust/Julia;從線性代數與數學基礎,一路到多智能體系統與自主集群,每步從公式推導到代碼實現。
  - 特別處:每節課都產出一個「**可複用的產出物**」——一個 prompt/skill/agent/MCP Server。底層是數學、頂層是 Agent 與生產部署。
  - 可在 aiengineeringfromscratch.com 讀,或 clone 跟著寫;支援 Claude/Cursor/Codex 的 Skill 直接學。

> **應用案例:** 想從數學底層一路打到 agent 生產部署、且邊學邊產出可用工件的自學者。對照本庫 [[awesome-agentic-ai-zh-roadmap]]、[[stanford-beyond-llm-course]]。

---

## One More Thing(本期附帶資料)

- **《全球大模型數據市場白皮書》**:算力紅利見頂,**數據**成為決定模型能力上限的核心生產要素;公開網路語料接近枯竭,高品質專家數據/RLHF/合成數據價值快速提升。
- **《2026 AI 重構下的社交媒體營銷趨勢報告》**:AI 重構整個社媒營銷鏈路,從「流量驅動」轉向「智能驅動」,品牌需構建 AI 原生的內容與運營能力。

---

## 來源

- itcoffee66/githubweekly 第 117 期:<https://github.com/itcoffee66/githubweekly/blob/main/_weekly/117.md>(2026/05/31–06/06)
