# GitHub Weekly 第 116 期:Agent 記憶 OS、超省錢 DeepSeek 編程 agent、HTML 出片、repo 轉知識圖譜、學術研究 Skill 包

> **期數:** #116(2026/05/24–05/30)
> **本期主題:** AI Agent 的記憶作業系統、圍繞 DeepSeek prefix cache 打造的省錢終端編程 agent、用 HTML 生成影片、把 code repo 變互動知識圖譜、以及涵蓋論文全流程的學術研究 Skill 包。
> 來源:itcoffee66/githubweekly 第 116 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **EverOS** | AI Agent 的長期記憶作業系統(受人腦四層架構啟發) | Agent 記憶 |
| 2 | **DeepSeek-Reasonix** | 圍繞 DeepSeek prefix cache 的超省錢終端編程 agent | AI 程式工具 |
| 3 | **HyperFrames** | 寫 HTML 就能出確定性 MP4,專為 AI Agent 設計 | AI 影片生成 |
| 4 | **Understand-Anything** | 把 code repo 變成「會教你」的互動知識圖譜 | 程式理解 |
| 5 | **academic-research-skills** | 論文研究→寫作→審稿→定稿的 Claude Code 技能包 | 學術/Agent |

---

## 1. EverOS — AI Agent 的記憶作業系統

- **連結:** <https://github.com/EverMind-AI/EverOS>
- **用途:** EverMind AI 團隊開發的開源「長期記憶作業系統」,為「自進化智能體」提供記憶基礎設施。解決 agent 一超出上下文窗口就「像金魚一樣失憶」、每次從零開始的痛點——讓 agent 能記住、積累、複用經驗。
- **亮點:**
  - 核心組件 **EverCore**,架構受人腦資訊處理啟發分四層(基礎設施/業務/記憶/智能體層);agent 跑完任務後會「復盤」,把經驗沉澱成下次可直接用的技能——**不只存資料,是真的在學習**。
  - 是一個 **Umbrella Project**:含 Architecture Methods、完整 Benchmarks、25+ Use Cases(蜂群智能體、有記憶的 Live2D 角色等)。
  - Benchmark 在 **LoCoMo、LongMemEval** 上勝 mem0 等同類一截;`docker compose` 兩條命令上手,或用 EverOS Cloud。
  - 團隊為盛大集團(陳天橋)全資孵化;超圖記憶架構 **HyperMem** 入選 ACL 2026。

> **應用案例:** 想給自己的 agent 加一層「跨對話會累積經驗」的記憶時,挑一個貼近需求的 Use Case + Architecture Method,用 Benchmark 做對比落地。呼應本庫 [[markdown-agent-memory]] 與 [[agent-harness-loop-llmops-eval-explained]] 的記憶系統討論。

## 2. DeepSeek-Reasonix — 圍繞 prefix cache 的省錢編程 agent

- **連結:** <https://github.com/esengine/DeepSeek-Reasonix>
- **用途:** 專為 DeepSeek 模型打造的終端編程 agent,核心賣點「便宜好用」。整個架構圍繞 DeepSeek 的 **prefix cache 穩定性**構建,讓快取命中率盡量高。
- **亮點:**
  - 實測快取命中率 **99.82%**,同樣 API 成本比通用工具低 **5 倍**——可以放心開著跑不心疼。
  - TypeScript、MIT;支援 MCP、計劃模式、自動工具調用修復;直連 `api.deepseek.com` 無中間轉換層(對國內用戶友善)。一條命令安裝。
  - 代價:功能全面性尚不足,看你的場景取捨。

> **應用案例:** 主力用 DeepSeek 做編程、又怕 token 燒太快的人,值得一試——「省錢就是賺錢」。呼應本庫 [[ai-compute-token-economics]] 的成本優化主題。

## 3. HyperFrames — 寫 HTML 出影片,專為 Agent 設計

- **連結:** <https://github.com/heygen-com/hyperframes>
- **用途:** 影片 AI 頭部玩家 **HeyGen** 出品,思路巧妙:與其教 AI 學複雜的剪輯軟體,不如讓它用最熟的 **HTML/CSS/JS「寫」影片**。把 HTML 轉成影片的開源框架。
- **亮點:**
  - Apache 2.0、20K+ stars;用 HTML+CSS+**GSAP** 寫動畫,本地渲染出**確定性 MP4**(同輸入永遠同輸出,對自動化產線關鍵)。
  - 支援 GSAP/WebGL shader/Lottie;CLI 自帶網站 capture(Gemini 驅動設計系統提取);附 7 步製作 Skill 模板。
  - Codex、Claude Code、豆包等可直接用其 Skill。

> **應用案例:** 把影片製作「降維成前端開發」——批量生產基礎/動畫向短視頻、動態內容生成。與本庫 [[claude-fable-72-hours-model-dependency]] 提到的 Hyperframe 同源。

## 4. Understand-Anything — 把 repo 變成「會教你」的知識圖譜

- **連結:** <https://github.com/Lum1104/Understand-Anything>
- **用途:** Claude Code 插件,把任何 code repo / 知識庫 / 文檔轉成**可互動的知識圖譜**。接到幾十萬行的新專案時——「別看代碼了,先看圖」。
- **亮點:**
  - 用多 Agent 管道做靜態分析 + LLM 處理,自動建含每個檔案/函式/類/依賴的知識圖譜,給互動式儀表盤。
  - 特色是「**教而不只是炫**」(Graphs that teach):AI 生成的引導導覽、每個節點摘要、語意標籤、任兩節點的依賴路徑查找。輸出便攜的 `knowledge-graph.json`。
  - 一週 5K+ stars、MIT,對 Claude Code 幾乎即插即用。

> **應用案例:** 這是「給人看、幫人快速理解」的版本;若要「給 Agent 查、省 token」則看本庫 [[codebase-memory-treesitter-knowledge-graph-mcp]](同期 120 期的 codebase-memory-mcp),兩者是同一條「結構化理解程式碼」路線的人/機兩端。

## 5. academic-research-skills — 論文全流程 Skill 包

- **連結:** <https://github.com/Imbad0202/academic-research-skills>
- **用途:** 一套完整的學術研究 Claude Code 技能包,涵蓋研究→寫作→審稿→定稿全流程。兩行命令安裝(`/plugin marketplace add` + `/plugin install`)。
- **亮點(4 個 Agent 團隊):**
  - **Deep Research**(13 Agent):文獻調研、研究問題構建、方法論設計,能寫 PRISMA 系統性綜述。
  - **Academic Paper**(12 Agent):大綱→論證→草稿→雙語摘要→圖表→引用格式。
  - **Academic Paper Reviewer**(7 Agent):從方法論、學科視角、跨學科價值多維打分。
  - **Academic Pipeline**:把前三個團隊串成 10 階段流水線。

> **應用案例:** 讀研寫論文一條龍;也是「多 Agent 分工完成專業工作」的實例,對照本庫 [[mixture-of-agents-moa]]。

---

## One More Thing(本期附帶資料)

- **《How OpenAI Uses Codex》**:OpenAI 給內部成員的 PDF,分享如何用 Codex——場景不限編程,含筆記整理、原型設計、時間管理等。
- **《人工智能時代的組織變革》**:世界經濟論壇 × 埃森哲白皮書,談企業如何從「局部試點」走向「組織級重構」,把 AI 深度嵌入客戶體驗/運營/研發/戰略/人才體系。

---

## 來源

- itcoffee66/githubweekly 第 116 期:<https://github.com/itcoffee66/githubweekly/blob/main/_weekly/116.md>(2026/05/24–05/30)
