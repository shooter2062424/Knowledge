# GitHub Weekly 第 118 期:自託管 AI 工作空間、AI 求職系統、Obsidian 替代、檔案式持久規劃 Skill、大模型解禁工具

> **期數:** #118(2026/06/07–06/13)
> **本期主題:** PewDiePie 出品的自託管 AI 工作空間、反向篩選公司的 AI 求職系統、檔案優先的 Markdown 知識庫、把 Markdown 檔當 agent「工作記憶」的持久規劃 Skill、以及用「方向消融」永久移除模型審查的工具。
> 來源:itcoffee66/githubweekly 第 118 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **Odysseus** | 自託管、本地優先的 ChatGPT/Claude 替代(PewDiePie 出品) | 自託管 AI |
| 2 | **Career-Ops** | 基於 Claude Code 的 AI 求職「指揮中心」 | AI 求職 |
| 3 | **Tolaria** | 檔案/Git/離線優先的 Obsidian 替代、AI 友善 | 知識庫 |
| 4 | **Planning-with-Files** | 用 Markdown 檔當 agent 持久「工作記憶」 | Agent Skill |
| 5 | **Heretic** | 用 Abliteration 永久移除 LLM 拒答機制 | 模型工具 |

---

## 1. Odysseus — 自託管 AI 工作空間

- **連結:** <https://github.com/pewdiepie-archdaemon/odysseus>
- **用途:** 自託管的 ChatGPT/Claude 替代——跑在你自己的硬體、用你自己的資料,本地優先、隱私優先、不裝後門。
- **亮點:**
  - 功能全面:聊天、Agent、cookbook、深度研究、模型對比、文檔編輯器、郵件、筆記任務、持久記憶、日曆同步,支援移動端 PWA。Docker 一鍵部署,Apple Silicon 有專屬腳本。
  - **cookbook** 頗實用:掃描你的硬體(GPU/VRAM)→推薦合適模型→一鍵下載部署,免手動算顯存;**compare** 可做模型盲測。
  - 6.5 萬+ star,但爆紅主因是作者 **PewDiePie**(YouTube 史上最成功創作者之一,巔峰訂閱破 1.1 億)——**大部分代碼是 AI 寫的**,也有人質疑是靠網紅效應拿 star。

> **應用案例:** 想在自己機器上跑一個隱私優先、能挑本地模型的全功能 AI 工作台。也提醒所有開源作者:**運營開源要學會營銷,酒香也怕巷子深**。

## 2. Career-Ops — AI 驅動的求職指揮中心

- **連結:** <https://github.com/santifer/career-ops>
- **用途:** 基於 Claude Code 的 AI 求職系統。大公司用 AI 篩履歷,那求職者能不能用 AI **反向篩選公司**?把編程 agent 變成全功能求職指揮中心。
- **亮點:**
  - **A–F 評分系統**(10 維加權評估職位匹配度)、自動生成 ATS 優化履歷(針對每個崗位客製)、自動掃描(海外)招聘門戶、批量並行評估、面試故事庫。
  - 作者自述用它評估 **740+ 職位、生成 100+ 份客製履歷**,最終拿到 Head of Applied AI offer——實戰驗證過。
  - `npx @santifer/career-ops init` 啟動,對話引導配置。**它是「過濾器」不是海投工具**:評分低於 4.0 就別浪費時間。

> **應用案例:** 從幾百個機會裡篩出真正值得花時間的那些。呼應本庫 [[leetcode-0-to-200-grinding-experience]] 的面試準備主題——把時間花在值得的地方。

## 3. Tolaria — 檔案/Git/離線優先的 Obsidian 替代

- **連結:** <https://github.com/refactoringhq/tolaria>
- **用途:** 跨平台桌面 App,管理 Markdown 知識庫——**Obsidian 的替代**。核心理念:檔案優先、Git 優先、離線優先。筆記就是普通 Markdown、每個知識庫是一個 Git 倉庫,不需帳號/訂閱/雲端。
- **亮點:**
  - macOS/Windows/Linux;`brew install --cask tolaria`;用 **Tauri + React + TS**,體積比 Electron 輕很多。
  - **AI 友善**:筆記結構天然適合當 AI Agent 的上下文,官方提供 Claude Code / Codex CLI / Gemini CLI 整合——不只給人用,也是 agent 的知識庫。
  - 作者自己管理 10,000+ 筆記的工作空間,每天在用。但專案初期,換知識庫是大工程,建議先觀望。

> **應用案例:** 想要輕量、不綁生態、隨時能拿走、又對 AI 友善的筆記方案。**這正是本 Knowledge 倉庫的思路**(Markdown + Git + AI 可讀),對照 [[llm-wiki-karpathy]]、[[markdown-agent-memory]]。

## 4. Planning-with-Files — 用檔案做 agent 的持久工作記憶

- **連結:** <https://github.com/OthmanAdi/planning-with-files>
- **用途:** 一個 Skill,借鑑 **Manus** 的思路:用**持久化的 Markdown 檔**做任務規劃、進度追蹤與知識存儲。
- **亮點:**
  - Claude Code 做複雜任務、上下文窗口滿了時,傳統 `/clear` 會丟進度;它把規劃資訊存磁碟——**markdown 檔就是 agent 的「工作記憶」**,清了對話也能自動恢復進度。
  - 建 `task_plan.md` 記目標/步驟/進度;每次行動前自動重載計劃;完成時有**驗證門控**確保真做完才停。v3.0.0 加自治模式與門控模式,Benchmark 通過率 **96.7%**。
  - 支援 Claude Code、Cursor、Copilot、Gemini CLI、Codex、Hermes 等 17+ 平台。**注意與 Superpowers 有衝突,別同時開。**

> **應用案例:** 長時間運行的 agent 任務,用檔案系統當外部記憶對抗上下文限制。呼應本庫 [[markdown-agent-memory]]、[[loop-engineering-when-and-how-gary-chen]](Verifiable Goal 門控)。

## 5. Heretic — 用 Abliteration 移除模型審查

- **連結:** <https://github.com/p-e-w/heretic>
- **用途:** 全自動的大模型審查移除工具,快速解除 LLM 的拒答機制。
- **亮點:**
  - 核心技術 **Abliteration(方向消融)**:找到模型內部負責「拒絕回答」的方向向量,直接從權重「切掉」,**永久移除拒絕行為、不需重訓或微調**。
  - `pip install -U heretic-llm` 後一行命令跑(如 `heretic Qwen/Qwen3-4B-Instruct-2507`);幾十分鐘零人工,把拒絕率從 90%+ 降到接近 0、**基本不損智商**。
  - 支援多數 dense 模型(含多模態、MoE);HuggingFace 已有大量 Heretic 模型。

> ⚠️ **爭議性專案,僅供學術研究**。它也揭露一個安全事實:開源模型的「安全對齊」可以被低成本、機械式地移除——對照本庫 [[safety-evaluation-crisis]]、[[prompt-injection-5-techniques-defenses]]。

---

## One More Thing(本期附帶資料)

- **《2026 Vibe Coding 行業深度洞察》**:vibe coding 不只重塑「如何寫代碼」,也在改變「誰可以創造軟體」。
- **《2026 飛行汽車發展報告》**:飛行汽車逐漸從科幻走向產業(如小鵬概念車),但仍很早期、受政策等因素影響大。

---

## 來源

- itcoffee66/githubweekly 第 118 期:<https://github.com/itcoffee66/githubweekly/blob/main/_weekly/118.md>(2026/06/07–06/13)
