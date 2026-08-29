# 來源索引(video id / arXiv 編號 → 筆記)

貼連結前先在這裡查,就知道有沒有整理過。

> ⚠️ **本檔由 `scripts/build_source_index.py` 自動產生,請勿手動編輯。**
> 統計:**175 個 YouTube video id**、**22 個 arXiv 編號**,涵蓋 **181 篇**筆記。

---

## 快速查詢

```bash
# repo 根目錄執行(-F 固定字串、-- 終止選項解析,id 以連字號開頭也安全)
grep -F -- "<video-id 或 arXiv 編號>" INDEX-SOURCES.md
```

查不到 = 尚未整理。也可以直接對全庫查:

```bash
grep -rlF --include=*.md -- "<id>" .
```

⚠️ `--include=*.md` 必須放在 `--` **之前**,否則 grep 會把它當檔名而回 exit 2。

---

## YouTube(175 部,依 video id 排序)

| video id | 筆記 | 路徑 |
|---|---|---|
| `-_U4YHElE2k` | 特斯拉暴跌 20% 拆解:資本開支才是恐慌根源,以及「大跌後持有半年 9 成賺」的歷史規律(美投君) | [investing/equity-research/tesla-q2-2026-capex-shock-vs-narrative.md](./investing/equity-research/tesla-q2-2026-capex-shock-vs-narrative.md) |
| `-ih9NBMHiU8` | AI 應用層 4 大前瞻趨勢:從財報季挖出的下一輪機會(流量、Agent 管理、ROI、AI 原生) | [investing/equity-research/ai-application-layer-4-trends-earnings.md](./investing/equity-research/ai-application-layer-4-trends-earnings.md) |
| `-XLTrE5bjko` | 收入高卻存不住錢?7 個正在掏空你的隱形習慣 | [investing/strategy/hidden-money-draining-habits.md](./investing/strategy/hidden-money-draining-habits.md) |
| `0-Rr2iho6CI` | 未來一年的 6 個 AI Agent 趨勢:從「背提示詞」到「當 AI 管理者」 | [technology/ai-agents/foundations/six-ai-agent-trends-next-year.md](./technology/ai-agents/foundations/six-ai-agent-trends-next-year.md) |
| `0ANjSvoFq0g` | 用高階函式降低程式碼閱讀負擔:重點不是變短,是讀者的注意力放在哪 | [technology/software-engineering/higher-order-functions-readable-code.md](./technology/software-engineering/higher-order-functions-readable-code.md) |
| `0kvj3lbJqoY` | AI 像 100 年前的電力革命:真正的商機不在「AI 應用」,而在「AI 採納」(美投君) | [investing/equity-research/ai-adoption-electricity-revolution-analogy.md](./investing/equity-research/ai-adoption-electricity-revolution-analogy.md) |
| `18QEjrwaNVM` | Opus 5 系統提示詞公開之後:五條可直接抄的工程模式,與「提示詞債務」 | [technology/ai-agents/foundations/opus5-system-prompt-engineering-patterns.md](./technology/ai-agents/foundations/opus5-system-prompt-engineering-patterns.md) |
| `1a1VXDdIyrk` | Harness Engineering 的演進:從 Prompt → Context → Harness(與 loop 架構) | [technology/ai-agents/foundations/harness-engineering-evolution.md](./technology/ai-agents/foundations/harness-engineering-evolution.md) |
| `1SLbe0k6x4I` | 用 Claude Code + Jesse 做 AI 演算法交易:重點是「驗證流程」,不是那支策略 | [investing/ai-assisted/ai-algo-trading-claude-jesse.md](./investing/ai-assisted/ai-algo-trading-claude-jesse.md) |
| `1VqKUrxR2C8` | AI 編程的三個致命錯覺(OpenCode 創辦人 Dax Raad) | [technology/ai-productivity/ai-coding-three-illusions-opencode.md](./technology/ai-productivity/ai-coding-three-illusions-opencode.md) |
| `2UYRqQvagrk` | MCP 史上最大改版(2026-07-28):從「打電話」變成「寄信」,以及三個功能的退場公告 | [technology/ai-agents/foundations/mcp-2026-07-28-stateless-rewrite.md](./technology/ai-agents/foundations/mcp-2026-07-28-stateless-rewrite.md) |
| `3e_YTF3id_8` | Claude「降智」其實是算力危機:Opus 4.7 試玩與升級注意 | [technology/ai-productivity/claude-throttling-opus-4-7.md](./technology/ai-productivity/claude-throttling-opus-4-7.md) |
| `3ZVWhFI5bpw` | herdr:讓 Agent 互相指揮的終端 runtime —— 用 Claude Code 做計畫、Codex 審核、便宜模型執行 | [technology/ai-agents/applications/herdr-terminal-runtime-agent-to-agent.md](./technology/ai-agents/applications/herdr-terminal-runtime-agent-to-agent.md) |
| `41LR-NhwHfI` | 為什麼你該開始做產品給 AI 用:UX → AX → AXO 三層框架(從瑞幸開放 MCP 談起) | [technology/ai-agents/applications/products-for-ai-ax-axo-luckin-mcp.md](./technology/ai-agents/applications/products-for-ai-ax-axo-luckin-mcp.md) |
| `4fpZhuJuIls` | Claude Dynamic Workflows 解析:什麼時候該用、什麼時候別用? | [technology/ai-agents/foundations/claude-dynamic-workflows.md](./technology/ai-agents/foundations/claude-dynamic-workflows.md) |
| `4j1omjaRu0A` | 在瘋狂股市裡,你還該「持續買入」嗎?——Nick Maggiulli 訪談筆記 | [investing/strategy/just-keep-buying-nick-maggiulli.md](./investing/strategy/just-keep-buying-nick-maggiulli.md) |
| `4t8QcDdrL6Y` | AI 時代怎麼「讀」程式碼:6 個技巧(KodeKloud) | [technology/ai-productivity/reading-code-ai-era-6-techniques.md](./technology/ai-productivity/reading-code-ai-era-6-techniques.md) |
| `5XeVLt9WejM` | AI 時代最被低估的技能:語音輸入,以及「把世界看成一場 context 轉換遊戲」 | [technology/ai-productivity/voice-input-ai-context-transformation.md](./technology/ai-productivity/voice-input-ai-context-transformation.md) |
| `6OBtO9niT00` | 一張餐巾紙算完 LLM 訓練成本:Stanford CS336 前六講的三個判斷 | [technology/llm-internals/training/cs336-training-cost-napkin-math.md](./technology/llm-internals/training/cs336-training-cost-napkin-math.md) |
| `7pSZx9-VT3k` | 「Token 省 120 倍」該怎麼讀?Codebase-Memory-MCP vs CodeGraph:同一個痛點的兩條路線 | [technology/ai-agents/memory-retrieval/codebase-memory-vs-codegraph-two-routes.md](./technology/ai-agents/memory-retrieval/codebase-memory-vs-codegraph-two-routes.md) |
| `91yRxsdc0gA` | 這次半導體狂歡是 2000 泡沫重演嗎?五個相同、四個不同、兩個要盯的信號 | [investing/strategy/semiconductor-2000-bubble-vs-2026-ai.md](./investing/strategy/semiconductor-2000-bubble-vs-2026-ai.md) |
| `9tREtYASGbs` | 微軟財報大漲 15% 的真正原因:三大質疑逐一拆解,以及 AI 價值鏈的位移 | [investing/equity-research/microsoft-fy26q1-three-doubts-resolved.md](./investing/equity-research/microsoft-fy26q1-three-doubts-resolved.md) |
| `_oDISo3B3xw` | 美債史詩級拋售:真正的變量不是 40 兆債務,是新任聯準會主席的「溝通方式」 | [investing/strategy/us-treasury-selloff-warsh-communication-shift.md](./investing/strategy/us-treasury-selloff-warsh-communication-shift.md) |
| `_RD3iFDhuzs` | Karpathy 訪談:Software 3.0、Jagged Intelligence 與 Agentic Engineering | [technology/ai-agents/foundations/karpathy-software-3-0.md](./technology/ai-agents/foundations/karpathy-software-3-0.md) |
| `aR97E7aKEgg` | Matt Pocock 的 AI 開發 skills 全拆解:最紅的 skill 只有五行字,強在哪? | [technology/ai-agents/applications/matt-pocock-skills-teardown.md](./technology/ai-agents/applications/matt-pocock-skills-teardown.md) |
| `atqcAb7MFAM` | 給非技術人員的 Git / GitHub:Vibe Coding 必學的基礎技能 | [technology/ai-productivity/git-github-for-vibe-coders.md](./technology/ai-productivity/git-github-for-vibe-coders.md) |
| `aYfZN8t6AQs` | Mem0 記憶架構拆解:三個儲存、抽取管線,與那個「加起來再除以 2.5」的混合排序 | [technology/ai-agents/memory-retrieval/mem0-memory-architecture-teardown.md](./technology/ai-agents/memory-retrieval/mem0-memory-architecture-teardown.md) |
| `aZEmxJ9ivzg` | 學了那麼多 AI,為什麼還是沒加薪?——省下的時間 85% 被雜事吃掉,以及納許議價怎麼算你該開多少 | [career/mindset/ai-skills-no-raise-nash-bargaining.md](./career/mindset/ai-skills-no-raise-nash-bargaining.md) |
| `B91bZL8wcAI` | 什麼是 AI Harness?兩種「harness」的差別 | [technology/ai-agents/foundations/ai-harness-explained.md](./technology/ai-agents/foundations/ai-harness-explained.md) |
| `BAfRVpKIxZ4` | 交易的「贏家數學」:期望值、系統設計、變異數、風險,與一個改變交易的問題 | [investing/strategy/trading-math-expectancy-variance-risk.md](./investing/strategy/trading-math-expectancy-variance-risk.md) |
| `BhHMGRcbPkQ` | 為什麼 Anthropic 工程師棄 Markdown 改用 HTML:當「理解」變成真正的瓶頸 | [technology/ai-productivity/anthropic-html-work-pages.md](./technology/ai-productivity/anthropic-html-work-pages.md) |
| `bPWcSxkD6Uo` | WiFi 是怎麼傳遞資訊的?把資訊裝進電磁波的硬核原理 | [technology/telecom/wifi-how-it-works.md](./technology/telecom/wifi-how-it-works.md) |
| `BQveePDWavA` | Token 與 Embedding 的分工:為什麼 LLM 的 embedding 和 RAG 的 embedding 不是同一回事 | [technology/llm-internals/architecture/token-vs-embedding-llm-and-rag.md](./technology/llm-internals/architecture/token-vs-embedding-llm-and-rag.md) |
| `ByBLjNA3MvY` | 海鷗策略(Seagull):牛市中「不踏空又不怕跌」的三腿期權對沖 | [investing/derivatives/seagull-options-hedge.md](./investing/derivatives/seagull-options-hedge.md) |
| `CGd5zDUrWnw` | Agent 為什麼會長成 Runtime:DeepSeek Harness 的插件樹與事件日誌,以及底下那篇 Cordis 論文 | [technology/ai-agents/foundations/agent-runtime-deepseek-harness-cordis.md](./technology/ai-agents/foundations/agent-runtime-deepseek-harness-cordis.md) |
| `cgKUgAJE3cs` | AI 產業秘密轉向:大模型集體從 C 端轉 B 端、訂閱轉用量,而「算力」成了現階段的勝負手 | [investing/equity-research/ai-industry-shift-c-to-b-compute-decides.md](./investing/equity-research/ai-industry-shift-c-to-b-compute-decides.md) |
| `CKKJuFVMvXQ` | Graph Engineering:把腦袋裡的分工、路由與驗收畫出來,別再當人肉 routing system | [technology/ai-agents/foundations/graph-engineering-node-edge-state.md](./technology/ai-agents/foundations/graph-engineering-node-edge-state.md) |
| `CMs8YMU6_RM` | AI 改 code 一直「改 A 壞 B」?讓 AI 安全接手舊專案(Brownfield)的五個步驟 | [technology/ai-productivity/ai-brownfield-codebase-five-steps.md](./technology/ai-productivity/ai-brownfield-codebase-five-steps.md) |
| `d4329xvSDK4` | AI 額度老是不夠用?三招省 Token:丟掉、縮減、打折 | [technology/ai-productivity/token-saving-three-moves-context-control.md](./technology/ai-productivity/token-saving-three-moves-context-control.md) |
| `DcibeCh1aZ4` | 美股連漲 13 天還能追嗎?「真實通脹」數據、AI 情緒三大轉向信號,與「踏空風險 > 回調風險」 | [investing/strategy/us-stocks-ai-turning-point-fomo-over-pullback.md](./investing/strategy/us-stocks-ai-turning-point-fomo-over-pullback.md) |
| `dECosPI6SUc` | 「Loop 已死,Graph 當立」?從工程視角看透這場名詞之爭 | [technology/ai-agents/foundations/loop-vs-graph-debate-engineering-view.md](./technology/ai-agents/foundations/loop-vs-graph-debate-engineering-view.md) |
| `diU-Nbb1P_c` | 4 組頂級 Agent Skill:從「自我進化」到「工程／設計／內容」生產力套件 | [technology/ai-agents/applications/top-skills-for-agents.md](./technology/ai-agents/applications/top-skills-for-agents.md) |
| `dJc-h7ui8wc` | LeetCode 怎麼刷最有效(上):從 0 刷到 200 題的真實心路歷程與方法 | [career/interview-prep/leetcode-0-to-200-grinding-experience.md](./career/interview-prep/leetcode-0-to-200-grinding-experience.md) |
| `doc0NQas32U` | 雙底雙頂:看的不是形態像不像,而是動能有沒有衰減 | [investing/technical-analysis/double-top-bottom-momentum.md](./investing/technical-analysis/double-top-bottom-momentum.md) |
| `dVRFSzbLR7M` | C++ 演進史:複雜性詛咒、記憶體危機,與 AI 時代的絕地反擊 | [technology/dev-tools/cpp-evolution-complexity-ai-era.md](./technology/dev-tools/cpp-evolution-complexity-ai-era.md) |
| `E8Bx9OlpmdM` | Claude 不是變笨,是講話方式跟你對不上:用 output style 治好 AI 的囉嗦 | [technology/claude-code/output-style-communication-not-intelligence.md](./technology/claude-code/output-style-communication-not-intelligence.md) |
| `E8Mju53VB00` | 一張餐巾紙算完 LLM 訓練成本:Stanford CS336 前六講的三個判斷 | [technology/llm-internals/training/cs336-training-cost-napkin-math.md](./technology/llm-internals/training/cs336-training-cost-napkin-math.md) |
| `Ec1jRVQ_YZU` | 別再相信目標價:前外資分析師拆解法人到底在看什麼 | [investing/strategy/target-prices-institutional-secrets.md](./investing/strategy/target-prices-institutional-secrets.md) |
| `eiisw5N2U6w` | 用需求逼出 Agent 的五臟六腑:工作流 vs 智能體的分界,與 LangGraph 只做的三件事 | [technology/ai-agents/foundations/agent-five-cores-langgraph-trading-agent.md](./technology/ai-agents/foundations/agent-five-cores-langgraph-trading-agent.md) |
| `eKW9ITaltWw` | 一支影片看完 Stanford「Beyond LLM」:從 LLM 到 Multi-Agent 的技術地圖 | [technology/ai-agents/resources/stanford-beyond-llm-course.md](./technology/ai-agents/resources/stanford-beyond-llm-course.md) |
| `EmwW59QMadY` | Pi:只有 4 個工具的極簡 Agent —— 雙層循環、對話樹,以及「刻意不做沙箱」 | [technology/ai-agents/applications/pi-minimal-agent-harness-teardown.md](./technology/ai-agents/applications/pi-minimal-agent-harness-teardown.md) |
| `EOg4gY0Yln0` | 讓訊號自己交易:Man Group 用 Claude Skills 治理打通系統化交易 | [technology/ai-agents/applications/claude-skills-governance-man-group.md](./technology/ai-agents/applications/claude-skills-governance-man-group.md) |
| `eWkZlS5JMD4` | 駭客怎麼騙 AI:5.5 種 Prompt Injection 技巧與防禦實戰 | [technology/ai-safety/prompt-injection-5-techniques-defenses.md](./technology/ai-safety/prompt-injection-5-techniques-defenses.md) |
| `EyZEJPP2JNQ` | AI Operating System(AIOS):一套讓 AI 長期懂你、替你工作的系統 | [technology/ai-agents/applications/ai-operating-system-aios.md](./technology/ai-agents/applications/ai-operating-system-aios.md) |
| `f4mI3d-nTrI` | MCP 無狀態化的維運視角:砍掉 Redis、恢復 round robin、伺服器能縮到零 | [technology/ai-agents/foundations/mcp-stateless-deployment-ops-view.md](./technology/ai-agents/foundations/mcp-stateless-deployment-ops-view.md) |
| `F7oNfszczVc` | 再訪田淵棟:46.5 億美金估值的 RSI,押注「AI 自進化」與前沿實驗室的組織架構之爭 | [technology/ai-industry/tian-yuandong-rsi-recursive-self-improvement.md](./technology/ai-industry/tian-yuandong-rsi-recursive-self-improvement.md) |
| `FJxgz5pN4wU` | Pi Agent:用「留白」的極簡 harness,對沖 agent 框架的易變 | [technology/ai-agents/foundations/pi-agent-minimal-harness.md](./technology/ai-agents/foundations/pi-agent-minimal-harness.md) |
| `FmIUUT-TXHs` | 別跟單一模型「結婚」:Model Agnostic 才是槓桿位置 | [technology/ai-productivity/model-agnostic-ai-workflow.md](./technology/ai-productivity/model-agnostic-ai-workflow.md) |
| `FmzFqM-kf0A` | AI 算力與 Token 經濟學:當「省錢神話」撞上天價帳單 | [technology/ai-industry/ai-compute-token-economics.md](./technology/ai-industry/ai-compute-token-economics.md) |
| `FQ81w5UO9u8` | 你可能用錯 AI 了:Processing vs Thinking 與三層 token 效率陷阱 | [technology/ai-productivity/context-engineering-processing-vs-thinking.md](./technology/ai-productivity/context-engineering-processing-vs-thinking.md) |
| `FrAAxWbxSyE` | Claude 5 時代的 Context Engineering 新規則:Claude Code 刪掉 80% 系統提示詞,評測卻沒掉 | [technology/ai-agents/foundations/context-engineering-claude-5-unhobbling.md](./technology/ai-agents/foundations/context-engineering-claude-5-unhobbling.md) |
| `FvWfAgNyEWc` | 硬碟陣列 RAID 一次看懂:RAID 0/1/5/6 原理,以及 RAID 5 為什麼「不安全」的真相 | [technology/system-design/raid-explained-why-raid5-unsafe.md](./technology/system-design/raid-explained-why-raid5-unsafe.md) |
| `fX0Am0Rhnfg` | 4 隻「無論何時都能安心買入」的 ETF:靠機制賺錢,不靠預測 | [investing/strategy/four-buy-anytime-etfs.md](./investing/strategy/four-buy-anytime-etfs.md) |
| `gAUvadRNFNE` | 為什麼跟有些人聊天特別有趣:四個特質,而且都不是話術 | [life/communication/four-traits-interesting-conversation.md](./life/communication/four-traits-interesting-conversation.md) |
| `gC76aeibdFA` | DeepSeek V4 的瘋狂工程:用「不夠的資源」做出頂尖模型 | [technology/llm-internals/architecture/deepseek-v4-engineering.md](./technology/llm-internals/architecture/deepseek-v4-engineering.md) |
| `gcCTxeLA6Mg` | NVIDIA N1X 能撞開 x86 四十年的城牆嗎?三個變量決定成敗 | [technology/ai-industry/nvidia-n1x-vs-x86.md](./technology/ai-industry/nvidia-n1x-vs-x86.md) |
| `gD_so3Nc7Y0` | 當沖有技巧嗎?紐約證交所傳奇交易員 Peter Tuchman 的 40 年心法 | [investing/technical-analysis/peter-tuchman-day-trading.md](./investing/technical-analysis/peter-tuchman-day-trading.md) |
| `gM5wm2x7fi8` | 美股狂熱會終結嗎?三大短期風險與「市場需要一個觸發點來解毒」 | [investing/strategy/us-stocks-three-risks-detox-trigger.md](./investing/strategy/us-stocks-three-risks-detox-trigger.md) |
| `GrNbuWWJYiI` | 19 分鐘搞懂四個 AI Agent 熱詞:Harness、Loop、LLM Ops、Eval(一張圖串起記憶/RAG/Tracing) | [technology/ai-agents/foundations/agent-harness-loop-llmops-eval-explained.md](./technology/ai-agents/foundations/agent-harness-loop-llmops-eval-explained.md) |
| `GzHfE50N8x4` | Google 五天 AI 開發課程 Day 1:從 Vibe Coding 到 Agentic Engineering 的完整心智模型 | [technology/ai-agents/foundations/google-agentic-engineering-day1.md](./technology/ai-agents/foundations/google-agentic-engineering-day1.md) |
| `h0lDdWYreSw` | dbx:單一執行檔的跨平台資料庫客戶端(Rust 寫)+ 內建 MCP Server 讓 Agent 直接操作資料庫 | [technology/dev-tools/dbx-rust-database-client-mcp.md](./technology/dev-tools/dbx-rust-database-client-mcp.md) |
| `h7abDtqN9gs` | Google AI 課程 Day 4+5:怎麼放心讓 AI 上正式環境?三個動作 —— 講清楚、設邊界、做驗收 | [technology/ai-agents/foundations/google-agentic-engineering-day4-5.md](./technology/ai-agents/foundations/google-agentic-engineering-day4-5.md) |
| `h7RA7yyMBYY` | 量子計算:量子效應如何突破計算的邊界 | [technology/quantum-computing/quantum-computing-explained.md](./technology/quantum-computing/quantum-computing-explained.md) |
| `HcbjFO1mRIw` | Project Cairn:把「做過的事」沉澱成可複用知識的開源 Skill(高體感 × 低阻力) | [technology/ai-agents/memory-retrieval/project-cairn-experience-to-knowledge-skill.md](./technology/ai-agents/memory-retrieval/project-cairn-experience-to-knowledge-skill.md) |
| `hfgeEa-rg0A` | 怎麼確保結構化 JSON 輸出真的可靠:提示詞 → Tool Use → 校驗器 → 帶錯誤的重試 | [technology/ai-agents/foundations/reliable-structured-json-output-tool-use.md](./technology/ai-agents/foundations/reliable-structured-json-output-tool-use.md) |
| `HhZcnM9tR7s` | Pi:只有 4 個工具的極簡 Agent —— 雙層循環、對話樹,以及「刻意不做沙箱」 | [technology/ai-agents/applications/pi-minimal-agent-harness-teardown.md](./technology/ai-agents/applications/pi-minimal-agent-harness-teardown.md) |
| `Hnf1ExYg3M8` | SpaceX 為什麼這時間點上市?Musk 在 JP Morgan 投資人訪談說了什麼 | [investing/equity-research/spacex-ipo-musk-jpmorgan.md](./investing/equity-research/spacex-ipo-musk-jpmorgan.md) |
| `hR5ephowvLM` | AI Agent 工具調用一次講清:從 ReAct → Function Calling → MCP → CLI | [technology/ai-agents/foundations/function-calling-mcp-cli-tool-evolution.md](./technology/ai-agents/foundations/function-calling-mcp-cli-tool-evolution.md) |
| `HyHKizkVuVM` | Skill 不是能力,是能力的施工圖:Agent 交不出活的三層工程棧「跑 / 做 / 驗」 | [technology/ai-agents/foundations/agent-skill-three-layer-run-do-verify.md](./technology/ai-agents/foundations/agent-skill-three-layer-run-do-verify.md) |
| `I-PMiyYZkrs` | 你以為健康,其實天天慢性發炎:四個敵人與四個對策 | [health/wellness/chronic-inflammation-four-enemies.md](./health/wellness/chronic-inflammation-four-enemies.md) |
| `ib74sLgjIBM` | 用 Claude 蓋一個「會自我改進」的知識庫:三個資料夾 + 一個 CLAUDE.md + 五步驟 | [technology/ai-agents/memory-retrieval/self-improving-knowledge-base-claude-cowork.md](./technology/ai-agents/memory-retrieval/self-improving-knowledge-base-claude-cowork.md) |
| `ipvuIOaN5wA` | 用 Claude Code 零程式碼做網站:突破 AI 預設風格、捲動動畫、設計策略 | [technology/applied-ai/design/ai-website-building-claude-code.md](./technology/applied-ai/design/ai-website-building-claude-code.md) |
| `IqvnryFzZD4` | 用 Claude Code + TradingView 蓋一條「盤前交易計畫」流水線(Humbled Trader 實作) | [investing/ai-assisted/humbled-trader-claude-tradingview-pipeline.md](./investing/ai-assisted/humbled-trader-claude-tradingview-pipeline.md) |
| `IRNWXRFri2A` | 青安 3.0 上路:為什麼「最高 1500 萬」多半貸不滿?以及財政部繼承數據透露的性別轉變 | [investing/personal-finance/qingan-3-0-and-inheritance-gender-gap.md](./investing/personal-finance/qingan-3-0-and-inheritance-gender-gap.md) |
| `iw1VF8HOCrk` | Attention Residuals:把注意力「轉 90 度」用在網路深度上 | [technology/llm-internals/architecture/attention-residuals.md](./technology/llm-internals/architecture/attention-residuals.md) |
| `JPGo_5fczaA` | 模型越強,Superpowers 和 Matt Skills 該刪掉誰?兩套 AI 編程工作流的選擇框架 | [technology/ai-agents/applications/superpowers-vs-matt-skills-strong-model.md](./technology/ai-agents/applications/superpowers-vs-matt-skills-strong-model.md) |
| `KeRBNTOITEo` | 十大恐怖主管特質:從竹科裸辭看「只做向上管理」如何逼走一個好員工 | [career/workplace/ten-toxic-manager-traits.md](./career/workplace/ten-toxic-manager-traits.md) |
| `kGYFSDd-ZVY` | Loop Engineering 實務:怎麼設計、什麼任務值得、失控的三個坑(Gary Chen) | [technology/ai-agents/foundations/loop-engineering-when-and-how-gary-chen.md](./technology/ai-agents/foundations/loop-engineering-when-and-how-gary-chen.md) |
| `KNP9Mr1rUQY` | 你不是不會寫 Prompt,是不會「定義任務」:五個欄位把需求寫成 AI 接得住的 brief | [technology/ai-productivity/defining-tasks-not-prompts.md](./technology/ai-productivity/defining-tasks-not-prompts.md) |
| `kYkIdXwW2AE` | Yann LeCun 押 10 億美元賭 LLM 的另一條路:JEPA 與世界模型(上) | [technology/llm-internals/world-models/jepa-lecun-world-models.md](./technology/llm-internals/world-models/jepa-lecun-world-models.md) |
| `L5LLzXrKFIY` | 史上最強 AI 模型只活了 72 小時:Claude Fable 事件與「別把流程綁死在單一模型」 | [technology/ai-industry/claude-fable-72-hours-model-dependency.md](./technology/ai-industry/claude-fable-72-hours-model-dependency.md) |
| `ll-OBB-iswM` | 「Loop Engineering」是名詞詐騙嗎?一個反方吐槽視角 | [technology/ai-agents/foundations/loop-engineering-buzzword-critique.md](./technology/ai-agents/foundations/loop-engineering-buzzword-critique.md) |
| `LPv1KfUXLCo` | 一張餐巾紙算完 LLM 訓練成本:Stanford CS336 前六講的三個判斷 | [technology/llm-internals/training/cs336-training-cost-napkin-math.md](./technology/llm-internals/training/cs336-training-cost-napkin-math.md) |
| `LPZh9BOjkQs` | 大型語言模型,簡單講(3Blue1Brown) | [technology/llm-internals/architecture/llm-explained-3blue1brown.md](./technology/llm-internals/architecture/llm-explained-3blue1brown.md) |
| `luN-yydHpYY` | Graphify 實戰壓測:10 萬 Star 的程式碼知識圖譜,打不贏 grep?「找」與「看」的分水嶺 | [technology/ai-agents/memory-retrieval/graphify-code-knowledge-graph-real-world-test.md](./technology/ai-agents/memory-retrieval/graphify-code-knowledge-graph-real-world-test.md) |
| `m6U_TGf9Z_M` | 新版 Codex 全流程實戰:從資料夾、辦公文件、生圖,到 Skill / Hook / Worktree / 一鍵部署 | [technology/ai-agents/applications/codex-desktop-full-workflow-guide.md](./technology/ai-agents/applications/codex-desktop-full-workflow-guide.md) |
| `mBePcvqLX88` | Graph Engineering 八分鐘講清楚:從 1736 年的柯尼斯堡七橋,到 108 個 agent 的 DAG | [technology/ai-agents/foundations/graph-engineering-explained-euler-to-agents.md](./technology/ai-agents/foundations/graph-engineering-explained-euler-to-agents.md) |
| `MdZWB8eC83Q` | Bitter Lesson:模型變強後,你的舊 prompt 正在拖垮新模型 | [technology/ai-agents/foundations/bitter-lesson-cut-old-patterns.md](./technology/ai-agents/foundations/bitter-lesson-cut-old-patterns.md) |
| `Mhq6IS2vSQM` | ChatGPT 瀏覽器擴充功能:借用你「已經登入」的瀏覽器,在背景跨分頁做事 | [technology/ai-productivity/chatgpt-browser-extension-agent.md](./technology/ai-productivity/chatgpt-browser-extension-agent.md) |
| `MlhsoWmyEKE` | 落地競賽:OpenAI 與 Anthropic 同日進軍企業導入,承認「只有模型沒用」 | [technology/ai-agents/applications/enterprise-ai-adoption-race.md](./technology/ai-agents/applications/enterprise-ai-adoption-race.md) |
| `mnuk1GkJxDU` | 股癌選股心法:籌碼/技術都是工具,本質是「選對題材的好股」 | [investing/strategy/gooaye-stock-picking-philosophy.md](./investing/strategy/gooaye-stock-picking-philosophy.md) |
| `msHyYioAyNE` | 一張餐巾紙算完 LLM 訓練成本:Stanford CS336 前六講的三個判斷 | [technology/llm-internals/training/cs336-training-cost-napkin-math.md](./technology/llm-internals/training/cs336-training-cost-napkin-math.md) |
| `nlNDzop6tBw` | Claude 不是變笨,是講話方式跟你對不上:用 output style 治好 AI 的囉嗦 | [technology/claude-code/output-style-communication-not-intelligence.md](./technology/claude-code/output-style-communication-not-intelligence.md) |
| `nLZ-C7bbZzs` | PLTR 財報後大漲 30%:市場真正在交易的不是業績,是「增速見頂」風險的釋放 | [investing/equity-research/pltr-earnings-growth-ceiling-and-valuation-digestion.md](./investing/equity-research/pltr-earnings-growth-ceiling-and-valuation-digestion.md) |
| `oBy94l_48CQ` | 2026 年 Agent 開發工程師要什麼能力:從 Demo 到生產系統的四塊拼圖(附面試題與標準答案) | [technology/ai-agents/foundations/production-agent-engineer-skills-2026.md](./technology/ai-agents/foundations/production-agent-engineer-skills-2026.md) |
| `oW4hgB1vIoY` | 用 Python 做強化學習交易機器人:在 EUR/USD 外匯訓練 AI Agent | [investing/ai-assisted/rl-trading-bot-forex.md](./investing/ai-assisted/rl-trading-bot-forex.md) |
| `oW6MHjzxHpU` | 賣財報波動率:把 $1 萬變 $100 萬的選擇權策略(以及它真正的風險) | [investing/derivatives/selling-earnings-volatility.md](./investing/derivatives/selling-earnings-volatility.md) |
| `oZC00ImTJt8` | 存量邏輯下的四條投資原則:把握價值而非趨勢,以及該盯的那個訊號 | [investing/strategy/ai-investing-four-principles-stock-logic.md](./investing/strategy/ai-investing-four-principles-stock-logic.md) |
| `P6UWIA_bvt8` | 大模型 API「中轉站」起底:0.5 折的 GPT/Claude 到底摻了多少水? | [technology/ai-industry/llm-api-relay-stations.md](./technology/ai-industry/llm-api-relay-stations.md) |
| `pGYrWsNQ8A0` | Attention Residuals:把注意力「轉 90 度」用在網路深度上 | [technology/llm-internals/architecture/attention-residuals.md](./technology/llm-internals/architecture/attention-residuals.md) |
| `pJR6I9_06e4` | Codex 2.0 新功能實戰:懸停導航 + Fork、側邊對話/引導、Record & Replay、手機遠端操控 | [technology/ai-productivity/codex-2-record-replay-mobile-remote.md](./technology/ai-productivity/codex-2-record-replay-mobile-remote.md) |
| `pmWgyZM7mB8` | CLAUDE.md 砍掉 82% 反而更聽話:三個篩選問題、五項該留的、以及一個減號的坑 | [technology/claude-code/claude-md-cut-82-percent-and-maintain-it.md](./technology/claude-code/claude-md-cut-82-percent-and-maintain-it.md) |
| `PpeCur6fEXc` | 讓 AI agent 連續跑 27 小時:/goal 功能與「Evaluation 才是關鍵」 | [technology/ai-agents/autonomy/long-running-agents-goal-evaluation.md](./technology/ai-agents/autonomy/long-running-agents-goal-evaluation.md) |
| `pR7teM31_wI` | AI 學會了裝傻和欺騙:為什麼現有 Safety Evaluation 跟不上大模型 | [technology/ai-safety/safety-evaluation-crisis.md](./technology/ai-safety/safety-evaluation-crisis.md) |
| `ptFiH_bHnJw` | 一張餐巾紙算完 LLM 訓練成本:Stanford CS336 前六講的三個判斷 | [technology/llm-internals/training/cs336-training-cost-napkin-math.md](./technology/llm-internals/training/cs336-training-cost-napkin-math.md) |
| `PuqX3Kv2ino` | Skill 實戰:從製作到維護一份「agent 會自動觸發、產出穩定、人類維護得了」的 skill | [technology/ai-agents/applications/building-claude-skills.md](./technology/ai-agents/applications/building-claude-skills.md) |
| `px5M4ry8IO4` | 下半年美股前瞻:宏觀四變數 + AI 的「存量邏輯 vs 增量邏輯」 | [investing/strategy/us-stocks-h2-2026-outlook-stock-vs-flow-ai.md](./investing/strategy/us-stocks-h2-2026-outlook-stock-vs-flow-ai.md) |
| `PxPWaP7mXFM` | AI 時代怎麼創業?Anthropic 新創 Playbook 的四階段 workflow | [technology/ai-agents/applications/anthropic-startup-playbook.md](./technology/ai-agents/applications/anthropic-startup-playbook.md) |
| `PyctX9GQjXs` | AI Agent 三大核心技:Function Calling、MCP、A2A | [technology/ai-agents/foundations/function-calling-mcp-a2a.md](./technology/ai-agents/foundations/function-calling-mcp-a2a.md) |
| `pyqUiHyz_-c` | AI 時代真正拉開差距的三種能力 | [technology/ai-productivity/three-valuable-ai-skills.md](./technology/ai-productivity/three-valuable-ai-skills.md) |
| `QAhJRYua62k` | 把 Hermes 爆改成「主 Agent 中樞」:統一調度 SubAgent 與 Claude / Gemini / Codex | [technology/ai-agents/applications/hermes-main-agent-orchestration.md](./technology/ai-agents/applications/hermes-main-agent-orchestration.md) |
| `QHHTcYBEIEo` | 別追「最強 AI」:用一張分工地圖建立你的多工具工作流 | [technology/ai-productivity/multi-tool-ai-workflow.md](./technology/ai-productivity/multi-tool-ai-workflow.md) |
| `qnIlKvW00Sk` | AI Agent 最大的缺陷:它沒有「世界地圖」——用本體論給大模型套上邏輯護欄 | [technology/ai-agents/foundations/neuro-symbolic-ontology-guardrails-frank-coyle.md](./technology/ai-agents/foundations/neuro-symbolic-ontology-guardrails-frank-coyle.md) |
| `QwOUDPiBzfU` | 孫慶龍的「EPS × 本益比五檔價」估值法 + 護國群山、成長股複利 | [investing/equity-research/sun-qinglong-pe-band-valuation.md](./investing/equity-research/sun-qinglong-pe-band-valuation.md) |
| `R549oFP9uN8` | Pre-norm vs Post-norm:為什麼現在的大模型全都把 LayerNorm 搬到前面 | [technology/llm-internals/architecture/pre-norm-vs-post-norm-transformer.md](./technology/llm-internals/architecture/pre-norm-vs-post-norm-transformer.md) |
| `RAFQc6zHdXE` | Codex Multi-agent V2 與 Graph Engineering:主 agent 調度、多模型混用、動態派生 subagent | [technology/ai-agents/applications/codex-multi-agent-v2-graph-engineering.md](./technology/ai-agents/applications/codex-multi-agent-v2-graph-engineering.md) |
| `rKV5JcALQoQ` | J-Space:Claude 內心那層「說得出口的思考」——用全域工作空間理論解讀模型意識 | [technology/llm-internals/interpretability/j-space-global-workspace-claude.md](./technology/llm-internals/interpretability/j-space-global-workspace-claude.md) |
| `rLNGSDYkK-w` | Claude Code Hooks 完全指南:CLAUDE.md 是提醒紙條,Hook 才是自動門 | [technology/claude-code/claude-code-hooks-complete-guide.md](./technology/claude-code/claude-code-hooks-complete-guide.md) |
| `rv9aZRdtxsU` | MCP 無狀態化怎麼遷移:十分鐘自查、三個真正危險的點,與「狀態在哪裡,責任就在哪裡」 | [technology/ai-agents/foundations/mcp-stateless-migration-guide.md](./technology/ai-agents/foundations/mcp-stateless-migration-guide.md) |
| `s3yiXTxueoI` | Harness / Loop / Graph 三層排障地圖:把「Agent 又抽風了」翻譯成可執行的排查工單 | [technology/ai-agents/foundations/harness-loop-graph-troubleshooting-map.md](./technology/ai-agents/foundations/harness-loop-graph-troubleshooting-map.md) |
| `SPyXyB7lgWU` | 加息會引發美股大跌嗎?用 2000 泡沫「三階段」對照 AI 這輪革命(美投君) | [investing/strategy/us-stocks-rate-hike-three-stages-ai-vs-2000.md](./investing/strategy/us-stocks-rate-hike-three-stages-ai-vs-2000.md) |
| `SQ3fZ1sAqXI` | 一張餐巾紙算完 LLM 訓練成本:Stanford CS336 前六講的三個判斷 | [technology/llm-internals/training/cs336-training-cost-napkin-math.md](./technology/llm-internals/training/cs336-training-cost-napkin-math.md) |
| `t0ZWNh-UXDs` | 一兆筆紀錄的即時搜尋:從 36 小時延遲砍到 5 分鐘的去重管線 | [technology/system-design/trillion-record-realtime-search-kafka-dedup.md](./technology/system-design/trillion-record-realtime-search-kafka-dedup.md) |
| `T1k0MCmO-SA` | 《會想的人,先有錢》(Jonathan Clements):一整天看盤的人,沒有賺比較多 | [investing/strategy/thinkers-get-rich-jonathan-clements.md](./investing/strategy/thinkers-get-rich-jonathan-clements.md) |
| `T3R3CFtYUww` | 什麼是先進封裝?從有機基板到矽中介層、TSV、矽橋、玻璃基板一次看懂 | [technology/ai-industry/advanced-packaging-explained.md](./technology/ai-industry/advanced-packaging-explained.md) |
| `t4QF0t_Y2Bs` | Python 3.15 幾個值得關注的新特性:frozendict、Sentinel、lazy import | [technology/dev-tools/python-3-15-new-features.md](./technology/dev-tools/python-3-15-new-features.md) |
| `t5CtfUWJjm4` | 為什麼 AI 寫的網站一上線就掛?用手搖飲店看懂網站架構擴展 | [technology/system-design/scaling-web-architecture-bubble-tea.md](./technology/system-design/scaling-web-architecture-bubble-tea.md) |
| `t9WA-BkLUps` | 非技術者的資安入門:用五個問題做威脅建模,再交給 Codex Security 掃描 | [technology/ai-safety/vibe-coding-security-threat-modeling.md](./technology/ai-safety/vibe-coding-security-threat-modeling.md) |
| `TBVjqvueeCo` | qm(YC 開源):把個人 Agent 變成「多人可用」的 Agent Harness —— scope 隔離、權限審批與可換 harness | [technology/ai-agents/applications/qm-yc-multiplayer-agent-harness.md](./technology/ai-agents/applications/qm-yc-multiplayer-agent-harness.md) |
| `tGp6Ns9GtSU` | KV Cache:每個 LLM 背後那個看不見的把戲 | [technology/llm-internals/inference/kv-cache.md](./technology/llm-internals/inference/kv-cache.md) |
| `thIPYsSsuIs` | 推理成本腰斬的背後:GPT-5.6 Sol 讓模型自己重寫核心,與 Luna 降價 80% 的算盤 | [technology/ai-industry/gpt-5-6-sol-kernel-self-optimization-luna-pricing.md](./technology/ai-industry/gpt-5-6-sol-kernel-self-optimization-luna-pricing.md) |
| `TN3ZrSQ4DTc` | AI 旅遊規劃組合技:NotebookLM + Gemini + Google My Maps 從 0 到 100 | [technology/ai-productivity/ai-travel-planning-notebooklm-gemini.md](./technology/ai-productivity/ai-travel-planning-notebooklm-gemini.md) |
| `tUI3ITjo2Bw` | AI 是威脅還是機遇?軟體股多點開花的選股邏輯 | [investing/equity-research/ai-software-stocks-usage-based.md](./investing/equity-research/ai-software-stocks-usage-based.md) |
| `U9jFYSaalIc` | 7 種主流 Agent 架構選型:從單槍匹馬到工業流水線,以及「多加一層」的真實代價 | [technology/ai-agents/foundations/seven-agent-architectures-selection-guide.md](./technology/ai-agents/foundations/seven-agent-architectures-selection-guide.md) |
| `UPF9Ogid4N0` | 黃仁勳談生死與接班:不做「接班計畫」,而是不停傳遞知識 | [technology/ai-industry/jensen-huang-succession-and-vision.md](./technology/ai-industry/jensen-huang-succession-and-vision.md) |
| `us_rw9gZRYI` | 什麼樣的 Agent 專案才能給履歷加分:玩具 Demo 與企業級應用的分水嶺 | [technology/ai-agents/applications/agent-project-resume-enterprise-grade.md](./technology/ai-agents/applications/agent-project-resume-enterprise-grade.md) |
| `VD9zEKQEJxo` | Sutton 的「行動認知 AI(enactive AI)」:一張自相矛盾的反大模型藍圖 | [technology/llm-internals/world-models/sutton-enactive-ai.md](./technology/llm-internals/world-models/sutton-enactive-ai.md) |
| `vkpS7WztTMc` | 蘇姿丰 MIT 2026 畢業演講:如何創造自己的運氣,以及 AI 時代人類無可取代的價值 | [career/mindset/lisa-su-mit-commencement.md](./career/mindset/lisa-su-mit-commencement.md) |
| `W973FsTECa8` | to-tickets 深入實操:把 spec 拆成 agent「能穩定開工、單獨驗收、可並行」的工單 | [technology/ai-agents/applications/to-tickets-spec-to-agent-workunits.md](./technology/ai-agents/applications/to-tickets-spec-to-agent-workunits.md) |
| `Wah1vdFE92k` | Pi:只有 4 個工具的極簡 Agent —— 雙層循環、對話樹,以及「刻意不做沙箱」 | [technology/ai-agents/applications/pi-minimal-agent-harness-teardown.md](./technology/ai-agents/applications/pi-minimal-agent-harness-teardown.md) |
| `wexH7AueOeA` | NVIDIA RTX Spark(GB10 超級晶片)技術解析:最適合本地 AI 推理的 SoC 之一? | [technology/ai-industry/rtx-spark-gb10-soc.md](./technology/ai-industry/rtx-spark-gb10-soc.md) |
| `wj7mHCviMvs` | 15 分鐘學完 CLAUDE.md:三個位置、做減法的三問、做加法的五問、以及怎麼「修剪」 | [technology/claude-code/claude-md-from-zero-to-mastery.md](./technology/claude-code/claude-md-from-zero-to-mastery.md) |
| `WOMdoiy9Qas` | Opus 4.7 不是更強的 4.6,是另一種模型:四個該跟著升級的工作流 | [technology/ai-productivity/opus-4-7-workflow-upgrades.md](./technology/ai-productivity/opus-4-7-workflow-upgrades.md) |
| `WuMlsfKeWHc` | Loop Engineering(循環工程):從「寫提示詞驅動 agent」到「設計驅動 agent 的循環」 | [technology/ai-agents/foundations/loop-engineering.md](./technology/ai-agents/foundations/loop-engineering.md) |
| `x2meJPOn9ws` | SpaceX 崛起史:從被嘲笑的新創到航天巨頭,一套已跑起來的商業飛輪 | [investing/equity-research/spacex-rise-history.md](./investing/equity-research/spacex-rise-history.md) |
| `x3QOpcGit4Q` | 當 PR 變成 Prompt Request:Peter Steinberger 用 Agent 自製工具維護開源項目 | [technology/ai-agents/applications/agent-native-tooling-steinberger.md](./technology/ai-agents/applications/agent-native-tooling-steinberger.md) |
| `XDy8topNXcc` | 一張餐巾紙算完 LLM 訓練成本:Stanford CS336 前六講的三個判斷 | [technology/llm-internals/training/cs336-training-cost-napkin-math.md](./technology/llm-internals/training/cs336-training-cost-napkin-math.md) |
| `xEkNd6xG1qo` | 美股升息風險研判:哪三類股票該避、哪一類反而是機會(美投君) | [investing/strategy/us-stocks-rate-hike-risk-2026.md](./investing/strategy/us-stocks-rate-hike-risk-2026.md) |
| `xFPiU5sit7g` | Codex 新手指南:駕馭「會動你檔案的 AI Agent」的四個基本功 | [technology/ai-productivity/codex-beginner-guide-four-basics.md](./technology/ai-productivity/codex-beginner-guide-four-basics.md) |
| `XH1G58QqPIM` | CSS View Transitions:用純 CSS 讓「多頁網站」有單頁 App 般的轉場動畫 | [technology/web-dev/css-view-transitions.md](./technology/web-dev/css-view-transitions.md) |
| `xI3MCSTlCtA` | 為什麼你買什麼跌什麼?台股散戶虧錢的底層邏輯:不是運氣,是「沒有系統」 | [investing/strategy/retail-investor-losing-system-not-luck.md](./investing/strategy/retail-investor-losing-system-not-luck.md) |
| `XJUpuOBpT-4` | DeepSeek V4 的瘋狂工程:用「不夠的資源」做出頂尖模型 | [technology/llm-internals/architecture/deepseek-v4-engineering.md](./technology/llm-internals/architecture/deepseek-v4-engineering.md) |
| `XOyG9mE-6KY` | 特斯拉財報深挖:FSD 拐點、馬斯克造芯片、四象限投資邏輯與 SpaceX 合併的隱藏風險 | [investing/equity-research/tesla-earnings-fsd-chip-spacex-four-quadrant.md](./investing/equity-research/tesla-earnings-fsd-chip-spacex-four-quadrant.md) |
| `XTCP1qoa3cc` | Google Agentic Engineering 課程 Day 2+3:MCP、A2A、AP2 三協定,與 Skill 上線的四地雷四防線 | [technology/ai-agents/foundations/google-agentic-engineering-day2-3.md](./technology/ai-agents/foundations/google-agentic-engineering-day2-3.md) |
| `xzrvAERmvRk` | Cross-Model Review:用 stop hook + skill + marker 讓 Claude 跟 Codex 自動互審(自建 harness) | [technology/ai-agents/applications/cross-model-review-claude-codex-harness.md](./technology/ai-agents/applications/cross-model-review-claude-codex-harness.md) |
| `yF2BY8kQfyo` | HBM 高頻寬記憶體原理:矽中介層、TSV、堆疊鍵合一次看懂 | [technology/ai-industry/hbm-high-bandwidth-memory-principle.md](./technology/ai-industry/hbm-high-bandwidth-memory-principle.md) |
| `yLOtgJwjhZ8` | 打造「0 人 AI 公司」:用 Hermes Agent + Paperclip 讓 AI 互相協作 | [technology/ai-agents/applications/zero-person-ai-company.md](./technology/ai-agents/applications/zero-person-ai-company.md) |
| `Ynv_WYO_slw` | Understand-Anything vs Graphify:把 codebase 變成知識圖譜給 AI 查,實測對比 | [technology/dev-tools/understand-anything-vs-graphify.md](./technology/dev-tools/understand-anything-vs-graphify.md) |
| `yVvW0NaWe40` | 現在正在主導的 5 個程式設計概念 | [technology/system-design/dominating-programming-concepts.md](./technology/system-design/dominating-programming-concepts.md) |
| `Yzpx4Xaigms` | Task Decomposition:把「給人看的 SOP」拆成「agent 跑得動的工作流」 | [technology/ai-agents/foundations/task-decomposition-agentic-workflow.md](./technology/ai-agents/foundations/task-decomposition-agentic-workflow.md) |
| `z0IvtUIF65Y` | 股癌選股心法:籌碼/技術都是工具,本質是「選對題材的好股」 | [investing/strategy/gooaye-stock-picking-philosophy.md](./investing/strategy/gooaye-stock-picking-philosophy.md) |
| `z2GFDO4HrZY` | AI 編程的三個致命錯覺(OpenCode 創辦人 Dax Raad) | [technology/ai-productivity/ai-coding-three-illusions-opencode.md](./technology/ai-productivity/ai-coding-three-illusions-opencode.md) |
| `Z613KdxJpKg` | Claude Design 使用評測:AI 設計工具,以及設計師的核心競爭力往哪移動 | [technology/applied-ai/design/claude-design-review.md](./technology/applied-ai/design/claude-design-review.md) |
| `ZLM6Qy7pAHk` | Model Routing:同一份任務,Token 成本從 $21.7 降到 $9.15 —— 重點是「算力分配」不是「挑模型」 | [technology/ai-productivity/model-routing-compute-allocation.md](./technology/ai-productivity/model-routing-compute-allocation.md) |
| `ZWsZwX6nsV0` | 社交套利(Social Arbitrage):Chris Camillo 從日常生活挖出暴利機會的方法 | [investing/strategy/social-arbitrage-chris-camillo.md](./investing/strategy/social-arbitrage-chris-camillo.md) |

---

## arXiv(22 篇,依編號排序)

| arXiv | 筆記 | 路徑 |
|---|---|---|
| `2002.05202` | 一張餐巾紙算完 LLM 訓練成本:Stanford CS336 前六講的三個判斷 | [technology/llm-internals/training/cs336-training-cost-napkin-math.md](./technology/llm-internals/training/cs336-training-cost-napkin-math.md) |
| `2007.00072` | 一張餐巾紙算完 LLM 訓練成本:Stanford CS336 前六講的三個判斷 | [technology/llm-internals/training/cs336-training-cost-napkin-math.md](./technology/llm-internals/training/cs336-training-cost-napkin-math.md) |
| `2402.03300` | GRPO vs GEPA:同一條 rollout,兩種完全不同的「學習訊號」 | [technology/ai-agents/foundations/grpo-vs-gepa.md](./technology/ai-agents/foundations/grpo-vs-gepa.md) |
| `2406.04692` | Mixture-of-Agents(MoA):用「分層提議 + 聚合」讓多個 LLM 互相加成,純開源打贏 GPT-4o | [technology/ai-agents/foundations/mixture-of-agents-moa.md](./technology/ai-agents/foundations/mixture-of-agents-moa.md) |
| `2507.19457` | GRPO vs GEPA:同一條 rollout,兩種完全不同的「學習訊號」 | [technology/ai-agents/foundations/grpo-vs-gepa.md](./technology/ai-agents/foundations/grpo-vs-gepa.md) |
| `2509.03505` | LimiX:用「遮罩聯合分布」打造的結構化資料(表格)基礎模型 | [technology/machine-learning/limix-tabular-foundation-model.md](./technology/machine-learning/limix-tabular-foundation-model.md) |
| `2509.13351` | PDDL-Instruct:用「邏輯式 CoT + 外部驗證」教 LLM 做真正的符號規劃 | [technology/ai-agents/foundations/pddl-instruct-llm-planning.md](./technology/ai-agents/foundations/pddl-instruct-llm-planning.md) |
| `2511.00592` | COMPILOT:讓現成 LLM 當「優化 agent」,在與編譯器的閉環對話中把迴圈優化到 3.5 倍 | [technology/ai-agents/applications/compilot-llm-guided-loop-optimization.md](./technology/ai-agents/applications/compilot-llm-guided-loop-optimization.md) |
| `2512.13564` | Agent Memory 綜述:用「形式 / 功能 / 動態」三個切面收拾一個亂掉的領域 | [technology/ai-agents/memory-retrieval/agent-memory-survey-forms-functions-dynamics.md](./technology/ai-agents/memory-retrieval/agent-memory-survey-forms-functions-dynamics.md) |
| `2601.01554` | MOSS-Transcribe-Diarize 0.9B 評估:端到端「轉錄+分辨說話者」開源模型,對我們的管線是否值得換? | [technology/dev-tools/moss-transcribe-diarize-evaluation.md](./technology/dev-tools/moss-transcribe-diarize-evaluation.md) |
| `2603.24621` | ARC-AGI-3:人類 100%、前沿 AI 不到 1% —— 一個用「行動效率」而不是「對不對」計分的 agentic 基準 | [technology/ai-safety/arc-agi-3-agentic-benchmark.md](./technology/ai-safety/arc-agi-3-agentic-benchmark.md) |
| `2603.27277` | Codebase-Memory:把程式碼變成「可查詢的知識圖譜」,讓 LLM 探索程式碼省 10 倍 token | [technology/ai-agents/memory-retrieval/codebase-memory-treesitter-knowledge-graph-mcp.md](./technology/ai-agents/memory-retrieval/codebase-memory-treesitter-knowledge-graph-mcp.md) |
| `2604.25850` | Agentic Harness Engineering:讓 harness 自己演化自己,而瓶頸不是能力是「可觀測性」 | [technology/ai-agents/foundations/agentic-harness-engineering-observability-evolution.md](./technology/ai-agents/foundations/agentic-harness-engineering-observability-evolution.md) |
| `2605.15155` | SDAR:用「逐 token 門控」穩住多輪 Agent 的強化學習後訓練 | [technology/llm-internals/training/sdar-agentic-rl.md](./technology/llm-internals/training/sdar-agentic-rl.md) |
| `2605.15184` | Grep 就夠了嗎?Agent Harness 如何左右「代理式檢索」 | [technology/ai-agents/memory-retrieval/grep-vs-vector-agentic-search.md](./technology/ai-agents/memory-retrieval/grep-vs-vector-agentic-search.md) |
| `2606.09498` | Self-Harness:讓 Agent 自己改進「操作自己的那層 harness」 | [technology/ai-agents/foundations/self-harness.md](./technology/ai-agents/foundations/self-harness.md) |
| `2606.13643` | Recursive Agent Harness:遞迴的單位該是「一次模型呼叫」還是「一整個 harness」? | [technology/ai-agents/foundations/recursive-agent-harness-harness-recursion.md](./technology/ai-agents/foundations/recursive-agent-harness-harness-recursion.md) |
| `2606.25656` | 到底需不需要 GraphRAG?9 種 RAG 方案實測對照 + 脈絡優化省 19–53% token | [technology/ai-agents/memory-retrieval/is-graphrag-needed-rag-variants-comparison.md](./technology/ai-agents/memory-retrieval/is-graphrag-needed-rag-variants-comparison.md) |
| `2607.01232` | 一層就夠了?RL 後訓練的收益高度集中在單一「中間層」transformer | [technology/llm-internals/architecture/rl-gains-concentrate-single-middle-layer.md](./technology/llm-internals/architecture/rl-gains-concentrate-single-middle-layer.md) |
| `2607.28272` | MemHarness:記憶是「重建」出來的,不是「重播」——用 RL 讓 agent 學會批判自己的經驗 | [technology/ai-agents/memory-retrieval/memharness-memory-reconstructed-not-replayed.md](./technology/ai-agents/memory-retrieval/memharness-memory-reconstructed-not-replayed.md) |
| `2608.09867` | 加密的推理過程為什麼保不住:一個「全域金鑰 + 可攜載體」的架構教訓 | [technology/ai-safety/encrypted-reasoning-traces-portable-key-flaw.md](./technology/ai-safety/encrypted-reasoning-traces-portable-key-flaw.md) |
| `2608.17528` | Harnessed Agentic RL:當 harness 而不是訓練器擁有互動迴圈,RL 會壞在哪四個地方 | [technology/llm-internals/training/harnessed-agentic-rl-agent-lightning.md](./technology/llm-internals/training/harnessed-agentic-rl-agent-lightning.md) |

---

## 重建

```bash
python scripts/build_source_index.py
```

抓兩種樣式:

- YouTube:`youtu.be/<11 碼>` 或 `watch?v=<11 碼>`
- arXiv:`arxiv.org/{abs,pdf,html}/<編號>`

新增筆記後重跑即可覆蓋。**不要手動編輯**——手動加的內容會在下次重建時消失。

> 註:一篇筆記可能對應多個 id(同時引用影片與論文),一個 id 也可能出現在多篇筆記中(交叉引用)。
