<div align="center">

# 🧠 Knowledge

**個人知識庫 —— 把投資與 AI 的高品質內容,煉成可複用的繁體中文筆記**

把文章、論文、YouTube 逐字稿與開源程式碼,整理成「先框架、再細節、附應用案例」的筆記。

<br/>

![Notes](https://img.shields.io/badge/筆記-83_篇-4c8bf5?style=flat-square)
![Categories](https://img.shields.io/badge/大類-4-9b59b6?style=flat-square)
![Language](https://img.shields.io/badge/語言-繁體中文-e74c3c?style=flat-square)
![Updated](https://img.shields.io/badge/更新-每週-2ecc71?style=flat-square)
![Made with](https://img.shields.io/badge/協作-Claude_Code-d97757?style=flat-square)

</div>

---

## 🗺️ 分類地圖

採 **「大類 → 中類 → 主題」三層** 結構;每篇筆記都含 **應用案例**,程式類則先 clone 讀完整原始碼再整理。撰寫慣例見 [CLAUDE.md](./CLAUDE.md)。

```mermaid
flowchart LR
    K["🧠 Knowledge"] --> I["💰 investing"]
    K --> T["⚙️ technology"]
    K --> C["💼 career"]
    C --> C1["workplace"]
    K --> H["🩺 health"]
    H --> H1["wellness"]
    I --> I1["strategy"]
    I --> I2["derivatives"]
    I --> I3["technical-analysis"]
    I --> I4["ai-assisted"]
    I --> I5["equity-research"]
    T --> T1["🤖 ai-agents"]
    T --> T2["🧬 llm-internals"]
    T --> T14["📐 machine-learning"]
    T --> T3["🚀 ai-productivity"]
    T --> T4["🎨 applied-ai"]
    T --> T7["🛡️ ai-safety"]
    T --> T9["📊 ai-industry"]
    T --> T10["🏗️ system-design"]
    T --> T8["🖥️ claude-code"]
    T --> T11["🌲 dev-tools"]
    T --> T13["🎨 web-dev"]
    T --> T12["🗞️ github-weekly"]
    T --> T6["⚛️ quantum-computing"]
    T --> T5["📡 telecom"]
    T1 --> T1a["foundations · autonomy · memory-retrieval<br/>applications · resources"]
    T2 --> T2a["architecture · inference · world-models"]
    T4 --> T4a["design · forecasting · speech-synthesis"]
```

### 目錄
- [💰 investing(投資)](#-investing投資)
- [⚙️ technology(科技與技術研究)](#️-technology科技與技術研究)
  - [🤖 ai-agents(代理工程)](#-ai-agents代理工程)
  - [🧬 llm-internals(模型架構與推論)](#-llm-internals模型架構與推論)
  - [📐 machine-learning(機器學習模型與方法)](#-machine-learning機器學習模型與方法)
  - [🚀 ai-productivity(AI 生產力)](#-ai-productivityai-生產力)
  - [🎨 applied-ai(應用)](#-applied-ai應用)
  - [📊 ai-industry(AI 產業與算力經濟)](#-ai-industryai-產業與算力經濟)
  - [🏗️ system-design(系統設計與架構)](#️-system-design系統設計與架構)
  - [🖥️ claude-code(Claude Code 維運)](#️-claude-codeclaude-code-維運)
  - [🌲 dev-tools(開發者工具)](#-dev-tools開發者工具)
  - [🎨 web-dev(網頁前端開發)](#-web-dev網頁前端開發)
  - [🛡️ ai-safety(AI 安全與評測)](#️-ai-safetyai-安全與評測)
  - [⚛️ quantum-computing(量子計算)](#️-quantum-computing量子計算)
  - [📡 telecom(電信)](#-telecom電信)
  - [🗞️ github-weekly(GitHub 週報)](#️-github-weeklygithub-週報)
- [💼 career(職涯與職場)](#-career職涯與職場)
- [🩺 health(健康與身體)](#-health健康與身體)

---

## 💰 investing(投資)

> ⚠️ 投資相關筆記為觀念整理,**非投資建議**;內含風險聲明。

### 📈 strategy(心法與策略)
| 主題 | 一句話 |
|---|---|
| [《持續買進》(Nick Maggiulli)](./investing/strategy/just-keep-buying-nick-maggiulli.md) | 把「買不買、何時買」變成不需意志力的自動規則 |
| [別再相信目標價:前外資分析師拆解法人在看什麼](./investing/strategy/target-prices-institutional-secrets.md) | 法人不看目標價,看的是想法的改變與預期差 |
| [收入高卻存不住錢?7 個正在掏空你的隱形習慣](./investing/strategy/hidden-money-draining-habits.md) | 先付給自己、只背好債、抑制生活膨脹、用槓桿買龍頭 |
| [4 隻「無論何時都能安心買入」的 ETF](./investing/strategy/four-buy-anytime-etfs.md) | SGOV/JEPI/DGRO/ALLW;靠機制而非預測,長期增值+扛跌+低成本 |
| [《像冠軍一樣思考和交易》(Minervini)](./investing/strategy/minervini-think-trade-like-champion.md) | SEPA/Stage2/Trend Template 8條/VCP(2-6T)/停損3-8%/漸進建倉/賣出規則;核心是控風險 |
| [股癌選股心法:籌碼/技術都是工具,本質是選對題材的好股](./investing/strategy/gooaye-stock-picking-philosophy.md) | 籌碼太懸、技術只是工具;先選題材(看得懂有未來)再比估值;選股選得好要飯要到老 |
| [《會想的人,先有錢》(Jonathan Clements)](./investing/strategy/thinkers-get-rich-jonathan-clements.md) | 整天看盤沒賺比較多;依時間軸配置+指數+定期定額;投資是手段不是目的 |
| [美股升息風險研判:3 類股票該避、1 類反而是機會(美投君)](./investing/strategy/us-stocks-rate-hike-risk-2026.md) | 放鷹展示決心但行為按兵不動;擁擠 AI 半導體最危險、優質龍頭抗跌、埋伏應用層 |

### 🎲 derivatives(衍生性商品)
| 主題 | 一句話 |
|---|---|
| [賣財報波動率:選擇權策略與真正的風險](./investing/derivatives/selling-earnings-volatility.md) | 72,500 筆財報回測、Kelly 部位大小與尾端風險 |

### 📉 technical-analysis(技術分析)
| 主題 | 一句話 |
|---|---|
| [雙底雙頂:看的不是形態,而是動能衰減](./investing/technical-analysis/double-top-bottom-momentum.md) | 真假反轉的關鍵是第二隻腳/頭的動能有沒有衰減 |
| [短線交易七條核心法則(熊貓有財)](./investing/technical-analysis/short-term-trading-7-rules.md) | 順勢/強勢股/別被洗盤嚇走/追新;但通篇沒講停損,風控要自己補 |
| [當沖有技巧嗎?NYSE 傳奇交易員 Peter Tuchman 的 40 年心法](./investing/technical-analysis/peter-tuchman-day-trading.md) | 別靠財報/FOMO 當沖;最大敵人是恐懼;移動平均+RSI;自我重塑與感恩心態 |

### 🤝 ai-assisted(AI 輔助投資)
| 主題 | 一句話 |
|---|---|
| [用 AI 輔助股票分析:該怎麼問、有哪些工具](./investing/ai-assisted/using-ai-for-stock-analysis.md) | 盤前問「情報與計畫」而非「今天買哪支」 |
| [用 Claude Code + Jesse 做 AI 演算法交易](./investing/ai-assisted/ai-algo-trading-claude-jesse.md) | 重點是驗證流程(顯著性檢定→回測→Monte Carlo→樣本外),不是那支策略 |
| [用 Python 做強化學習交易機器人(EUR/USD 外匯)](./investing/ai-assisted/rl-trading-bot-forex.md) | RL 五要素+Gym/PPO 四檔架構;訓練漂亮、樣本外打回原形;市場噪音難抓信號 |

### 📊 equity-research(個股與產業研究)
| 主題 | 一句話 |
|---|---|
| [AI 是威脅還是機遇?軟體股多點開花的選股邏輯](./investing/equity-research/ai-software-stocks-usage-based.md) | 贏家三共性:2B + 按用量收費 + AI 帶來新增收入;基礎設施層最佳 |
| [孫慶龍 EPS×本益比五檔價估值法 + 護國群山](./investing/equity-research/sun-qinglong-pe-band-valuation.md) | 預估EPS×歷史PE分位→特價/便宜/合理/昂貴/瘋狂;便宜只賺一次、成長讓複利反覆工作 |
| [玻璃基板取代有機載板?欣興/群創/友達的技術門檻與量產時程](./investing/equity-research/glass-substrate-supply-chain.md) | TGV最難、永久GCS量產落2026底~2028後;Absolics領先、台廠相對落後;分清路線/進度/含金量 |

---

## ⚙️ technology(科技與技術研究)

### 🤖 ai-agents(代理工程)

**foundations — 基礎概念**
| 主題 | 一句話 |
|---|---|
| [什麼是 AI Harness?兩種 harness 的差別](./technology/ai-agents/foundations/ai-harness-explained.md) | harness = 模型權重以外的一切 |
| [Harness Engineering 的演進:Prompt → Context → Harness](./technology/ai-agents/foundations/harness-engineering-evolution.md) | context 撞牆在越摘要越失真;harness 用 loop+每輪乾淨 context 取代(Ralph) |
| [Pi Agent:用「留白」的極簡 harness 對沖框架易變](./technology/ai-agents/foundations/pi-agent-minimal-harness.md) | OpenClaw 的大腦;刻意不內建 MCP/sub-agent,能用 TS 擴展自己的 harness;build less |
| [五大 Agent 模式(2026 生產系統至少用一個)](./technology/ai-agents/foundations/five-agent-patterns.md) | Prompt Chaining/Routing/Parallelization/Orchestrator-Workers/Evaluator-Optimizer;工作流 vs 自主 |
| [12-Factor Agents:打造可上線、可靠的 LLM 代理](./technology/ai-agents/foundations/12-factor-agents.md) | 大量普通軟體 + 少量精心設計的 LLM 步驟 |
| [CLAUDE.md 12 條規則:把編碼錯誤率從 41% 壓到 3%](./technology/ai-agents/foundations/claude-md-12-rules.md) | 每條規則都對應一個你實際踩過的坑 |
| [AI Agent 三大核心技:Function Calling、MCP、A2A](./technology/ai-agents/foundations/function-calling-mcp-a2a.md) | 會用工具 → 即插即用生態 → agent 互相協作 |
| [Karpathy 訪談:Software 3.0、Jagged Intelligence、Agentic Engineering](./technology/ai-agents/foundations/karpathy-software-3-0.md) | 你可以外包思考,但不能外包理解 |
| [Bitter Lesson:模型變強後,舊 prompt 正在拖垮新模型](./technology/ai-agents/foundations/bitter-lesson-cut-old-patterns.md) | 該砍的 model rule vs 該留的 business rule |
| [GRPO vs GEPA:同一條 rollout,兩種學習訊號](./technology/ai-agents/foundations/grpo-vs-gepa.md) | RL 把 trace 壓成 1 bit 改權重;GEPA 讀完整 trace 反思改 prompt,省 35× rollouts |
| [Task Decomposition:把給人看的 SOP 拆成 agent 跑得動的工作流](./technology/ai-agents/foundations/task-decomposition-agentic-workflow.md) | 四步:標準化(MUST/SHOULD/MAY)→ 拆 pipeline 用 artifact 串 → 雙向開發挖默會知識 → 接 MCP + human-in-the-loop |
| [BDI(信念–欲望–意圖):經典 agent 架構,與 LLM agent 對照](./technology/ai-agents/foundations/bdi-belief-desire-intention.md) | 意圖=已承諾的欲望;現代 agent loop 是 BDI 續集,補上自己規劃與學習 |
| [PDDL-Instruct:用邏輯 CoT + 外部驗證教 LLM 做符號規劃](./technology/ai-agents/foundations/pddl-instruct-llm-planning.md) | 把規劃拆成可被 VAL 逐步驗證的原子步;不靠自我糾錯;Blocksworld 28%→94% |
| [Claude Dynamic Workflows 解析:何時該用、何時別用](./technology/ai-agents/foundations/claude-dynamic-workflows.md) | Claude 寫腳本指揮上百 agent;與 skill/subagent/agent team/goal 之別;任務能否切成獨立小塊 |
| [Self-Harness:讓 Agent 自己改進操作自己的 harness](./technology/ai-agents/foundations/self-harness.md) | 挖弱點→提最小修改→非退化驗證;權重不動只改 harness;三模型 held-out +33~60% |

**autonomy — 自主與長時間運行**
| 主題 | 一句話 |
|---|---|
| [Karpathy autoresearch:讓 AI agent 自主做 ML 研究的最小 harness](./technology/ai-agents/autonomy/karpathy-autoresearch.md) | 改一個檔、一個 metric、一個時間預算 |
| [讓 AI agent 連續跑 27 小時:/goal 與「Evaluation 才是關鍵」](./technology/ai-agents/autonomy/long-running-agents-goal-evaluation.md) | 對抗 context anxiety;rubric 把品味寫成文字 |

**memory-retrieval — 記憶與檢索**
| 主題 | 一句話 |
|---|---|
| [AI Agent 記憶管理:有時候 Markdown 檔案就夠了](./technology/ai-agents/memory-retrieval/markdown-agent-memory.md) | MEMORY.md + 日誌 + 漸進式上下文披露 |
| [Grep 就夠了嗎?Agent Harness 如何左右代理式檢索](./technology/ai-agents/memory-retrieval/grep-vs-vector-agentic-search.md) | inline grep 常勝向量,但換 harness 影響達 16pp |
| [SimpleRAG:給科學 PDF 的本地 RAG(OCR + 小-大多向量)](./technology/ai-agents/memory-retrieval/simplerag-pdf-rag.md) | MiniCPM OCR fallback + parent-child 多向量 + Ollama 忠實抽取 |
| [Vectorless RAG:不靠相似度,靠「結構導航」找對地方](./technology/ai-agents/memory-retrieval/vectorless-rag-structure-navigation.md) | LLM 在文件階層樹上推理導航(PageIndex);相似≠相關,FinanceBench 50%→98.7% |

**applications — 企業應用與實作**
| 主題 | 一句話 |
|---|---|
| [Skill 實戰:從製作到維護的完整指南](./technology/ai-agents/applications/building-claude-skills.md) | 給心法不給死步驟;references / scripts / subagent |
| [Man Group:用 Claude Skills 治理打通系統化交易](./technology/ai-agents/applications/claude-skills-governance-man-group.md) | 組織 context 是 IP;skill 治理解鎖企業級 |
| [落地競賽:OpenAI 與 Anthropic 同日進軍企業導入](./technology/ai-agents/applications/enterprise-ai-adoption-race.md) | 企業買的不是模型,是落地能力 |
| [打造「0 人 AI 公司」:Hermes Agent + Paperclip](./technology/ai-agents/applications/zero-person-ai-company.md) | 只對 CEO 下目標,agent 自動招募協作 |
| [把 Hermes 爆改成主 Agent 中樞:調度 SubAgent 與 Claude/Gemini/Codex](./technology/ai-agents/applications/hermes-main-agent-orchestration.md) | 單一入口路由多模型 CLI;gateway/ACP/任務監控/分層抓取 |
| [Agent Streaming 格式設計:串流是要設計的應用層介面](./technology/ai-agents/applications/agent-streaming-format-design.md) | 頻道×命名空間、快照/增量(JSON Patch)、存整段事件序列、斷線重連 |
| [用 AI 分析 Agent Traces:讓 agent 讀 trace,人類把持品味](./technology/ai-agents/applications/agent-trace-analysis-with-ai.md) | 三方案(自有 coding agent/執行時自診斷/批次掃描);agent 放大規模、人決定方向 |
| [AI 時代怎麼創業?Anthropic 新創 Playbook 四階段 workflow](./technology/ai-agents/applications/anthropic-startup-playbook.md) | 十人獨角獸;Idea/MVP/Launch/Scale 各用哪個 Claude;差距是誰把 AI 系統化得更好 |
| [AI Operating System(AIOS):讓 AI 長期懂你、替你工作的系統](./technology/ai-agents/applications/ai-operating-system-aios.md) | 四核心 Context/Connections/Capabilities/Cadence;progressive loading 省 context;從操作者變系統擁有者 |

**resources — 學習資源**
| 主題 | 一句話 |
|---|---|
| [awesome-agentic-ai-zh:中文學習路線圖](./technology/ai-agents/resources/awesome-agentic-ai-zh-roadmap.md) | 8 階段 + 2 條路徑,從 LLM 到多代理 |
| [一支影片看完 Stanford「Beyond LLM」](./technology/ai-agents/resources/stanford-beyond-llm-course.md) | Prompt/RAG/Agentic/Multi-Agent 技術地圖 |
| [AI System Design Guide(ombharatiya):生產級 AI 系統設計與面試活字典](./technology/ai-agents/resources/ai-system-design-guide.md) | 18 章 + 110 面試題 + 20 案例 + Eval 深入;基礎→建造→運維→治理→應用 |

### 🧬 llm-internals(模型架構與推論)
| 主題 | 一句話 |
|---|---|
| [Attention Residuals:把注意力「轉 90 度」用在網路深度上](./technology/llm-internals/architecture/attention-residuals.md) | Kimi 對「層」做注意力,緩解 pre-norm dilution |
| [DeepSeek V4 的瘋狂工程:用不夠的資源做出頂尖模型](./technology/llm-internals/architecture/deepseek-v4-engineering.md) | hybrid attention(CSA/HCA/滑窗)+ mHC 雙隨機約束防爆 + Muon + 通訊重疊;KV cache 砍 90% |
| [microGPT(Karpathy):200 行純 Python 講完整個 GPT 演算法](./technology/llm-internals/architecture/microgpt-karpathy.md) | autograd→架構→Adam→取樣全在眼前;KV cache 顯式;「其餘都只是效率」 |
| [大型語言模型,簡單講(3Blue1Brown)](./technology/llm-internals/architecture/llm-explained-3blue1brown.md) | LLM=下一字機率函式;參數/反向傳播/預訓練/RLHF/Transformer attention 白話入門 |
| [DiffusionGemma:把「擴散」搬進語言模型,並行生成可自我修正](./technology/llm-internals/architecture/diffusion-gemma.md) | 非自迴歸,256-token 畫布多輪去噪;瓶頸從記憶體頻寬轉計算;雙向注意力能改錯解數獨 |
| [KV Cache:每個 LLM 背後那個看不見的把戲](./technology/llm-internals/inference/kv-cache.md) | 穩定前綴 + 尾載查詢,推論便宜 10 倍 |
| [RTK(Rust Token Killer)深入研究](./technology/llm-internals/inference/rtk-rust-token-killer-report.md) | 在 I/O 邊界確定性壓縮工具輸出,省 60–90% token |
| [Yann LeCun 的 JEPA 與世界模型](./technology/llm-internals/world-models/jepa-lecun-world-models.md) | 非生成、聯合嵌入預測;反 LLM 的另一條路 |
| [Sutton 的 enactive AI:一張自相矛盾的反大模型藍圖](./technology/llm-internals/world-models/sutton-enactive-ai.md) | 行動認知≠生成式;兩根柱子撞自己的獎勵假設與苦澀教訓;三桌賭 2028/2030 |
| [SDAR:用逐 token 門控穩住多輪 Agent 的 RL 後訓練](./technology/llm-internals/training/sdar-agentic-rl.md) | RL 為主幹+門控蒸餾,避免多輪 OPSD 崩潰、技能內化 |

### 📐 machine-learning(機器學習模型與方法)
| 主題 | 一句話 |
|---|---|
| [LimiX:用「遮罩聯合分布」打造的結構化資料(表格)基礎模型](./technology/machine-learning/limix-tabular-foundation-model.md) | 一個模型四任務(分類/迴歸/填補/生成);CCMM+axis-wise attention;in-context 免訓練;勝 XGBoost/TabPFN |

### 🚀 ai-productivity(AI 生產力)
| 主題 | 一句話 |
|---|---|
| [AI 時代真正拉開差距的三種能力](./technology/ai-productivity/three-valuable-ai-skills.md) | AI 調度力 / 工作流設計力 / 獨立思考力 |
| [NotebookLM 三提問:把一學期壓縮到 48 小時](./technology/ai-productivity/notebooklm-rapid-learning.md) | 抽心智模型 → 畫爭議 → 用理解型問題自測 |
| [別追「最強 AI」:建立你的多工具工作流](./technology/ai-productivity/multi-tool-ai-workflow.md) | 任務需要什麼資料 → 在哪裡 → 哪個 AI 能操作 |
| [為什麼 Anthropic 工程師棄 Markdown 改用 HTML](./technology/ai-productivity/anthropic-html-work-pages.md) | 產出變便宜,理解變貴;用對的介面驗證 |
| [Opus 4.7 不是更強的 4.6,是另一種模型](./technology/ai-productivity/opus-4-7-workflow-upgrades.md) | prompt 補意圖、跨模型 review、分工、流程化 |
| [Claude「降智」其實是算力危機:Opus 4.7 試玩與升級注意](./technology/ai-productivity/claude-throttling-opus-4-7.md) | 降智=下修思考深度/配額;4.7 新設定、benchmark、tokenizer 變兇、指令字面化 |
| [你可能用錯 AI 了:Processing vs Thinking 與三層 token 效率陷阱](./technology/ai-productivity/context-engineering-processing-vs-thinking.md) | 別讓 AI 搬磚;讀檔/長對話/agent 檢索三層 context engineering |
| [AI 編程的三個致命錯覺(OpenCode Dax Raad)](./technology/ai-productivity/ai-coding-three-illusions-opencode.md) | 自動變快/執行就贏/在飛皆是幻覺;瓶頸是想清楚做什麼,慢下來打地基才最快 |
| [別跟單一模型結婚:Model Agnostic 才是槓桿位置](./technology/ai-productivity/model-agnostic-ai-workflow.md) | 沒有魔法模型;按任務選模型而非把任務塞進最強模型;擁有自有 infra 讓模型可替換 |
| [你不是不會寫 Prompt,是不會定義任務](./technology/ai-productivity/defining-tasks-not-prompts.md) | 目標/背景/素材/邊界/完成定義五欄位寫成 brief;AI 能幫你問不能替你想;本質是管理力 |
| [AI 時代怎麼「讀」程式碼:6 個技巧](./technology/ai-productivity/reading-code-ai-era-6-techniques.md) | 從進入點/先讀測試/跟著資料走/跳雜訊/讀一條失敗路徑/壓成一句話 |
| [AI 旅遊規劃組合技:NotebookLM + Gemini + My Maps](./technology/ai-productivity/ai-travel-planning-notebooklm-gemini.md) | 蒐集即時資料→整合零散素材→Canvas排程當裁判→CSV匯地圖→Live現場助理;分工是關鍵 |

### 🎨 applied-ai(應用)
| 主題 | 一句話 |
|---|---|
| [Claude Design 使用評測:AI 設計工具與設計師的品味](./technology/applied-ai/design/claude-design-review.md) | 執行被接管,人往「什麼該存在」的決策層移動 |
| [用 Claude Code 零程式碼做網站:風格突破/捲動動畫/設計策略](./technology/applied-ai/design/ai-website-building-claude-code.md) | 避免 AI 2014 風、逐幀捲動動畫、同品牌三種設計策略 |
| [Nexus:四代理分工的時間序列預測](./technology/applied-ai/forecasting/nexus-time-series.md) | 把「事件」帶進預測,而非只外推曲線 |
| [VoxCPM:無分詞器的開源 TTS](./technology/applied-ai/speech-synthesis/voxcpm-report.md) | 直接生成連續語音表示、可用文字描述設計聲音 |

### 📊 ai-industry(AI 產業與算力經濟)
| 主題 | 一句話 |
|---|---|
| [AI 算力與 Token 經濟學:省錢神話撞上天價帳單](./technology/ai-industry/ai-compute-token-economics.md) | 降本悖論、token maxing、從比智商到比划算、應用層替硬體打工 |
| [Google Cloud:AI Agent 趨勢 2026(五大轉變)](./technology/ai-industry/google-cloud-ai-agent-trends-2026.md) | 員工/工作流/客服/資安/規模五趨勢;A2A·MCP·AP2 三協定 |
| [黃仁勳談生死與接班:不做接班計畫,而是不停傳遞知識](./technology/ai-industry/jensen-huang-succession-and-vision.md) | 每場會議都是推理會議;組織韌性來自知識擴散非繼任者 |
| [NVIDIA N1X 能撞開 x86 四十年城牆嗎?三個變量定成敗](./technology/ai-industry/nvidia-n1x-vs-x86.md) | 換的不是速度是 CUDA;消費牆已破,但續航/需求/企業三牆未過;邊緣 vs 資料中心兩線作戰 |
| [NVIDIA RTX Spark(GB10 超級晶片)技術解析](./technology/ai-industry/rtx-spark-gb10-soc.md) | 10+10核Arm+近桌面5070 GPU+128G統一記憶體;最適合本地AI推理之一;隱憂是Win on ARM |
| [大模型 API 中轉站起底:0.5 折的 GPT/Claude 摻了多少水](./technology/ai-industry/llm-api-relay-stations.md) | 便宜來自薅大廠訂閱/免費羊毛(非換便宜模型);降質摻水+資安風險;灰色地帶 |

### 🏗️ system-design(系統設計與架構)
| 主題 | 一句話 |
|---|---|
| [為什麼 AI 寫的網站一上線就掛?用手搖飲店看懂架構擴展](./technology/system-design/scaling-web-architecture-bubble-tea.md) | 快取/Docker/CI-CD/負載平衡/Replica/微服務/CDN/Queue 是被問題逼出來的 |
| [現在正在主導的 5 個程式設計概念](./technology/system-design/dominating-programming-concepts.md) | 反應式/邊緣運算/資料導向設計/LLM 應用架構/本地優先;都是心智模型的轉變 |

### 🖥️ claude-code(Claude Code 維運)
| 主題 | 一句話 |
|---|---|
| [搬移專案目錄後如何保住 `--continue` 對話歷史](./technology/claude-code/continue-after-directory-move.md) | 歷史按路徑編碼存 ~/.claude/projects;搬目錄要同步改名 |

### 🌲 dev-tools(開發者工具)
| 主題 | 一句話 |
|---|---|
| [Tree-sitter:給程式工具用的「增量解析」引擎](./technology/dev-tools/tree-sitter.md) | 把原始碼變成可查詢、改一字不必重剖的語法樹;編輯器/GitHub/AI agent 的底層 |
| [Understand-Anything vs Graphify:codebase 變知識圖譜給 AI 查](./technology/dev-tools/understand-anything-vs-graphify.md) | 省 token vs 視覺化的取捨;Graphify 省一半 token+本地模型,Understand-Anything 圖更好 |
| [CodeGraph 原始碼深讀:架構與 shimmer TUI 怎麼做](./technology/dev-tools/codegraph-code-and-tui.md) | Tree-sitter→SQLite 圖譜→MCP 8 工具;TUI 用 worker 直寫 fd1 讓動畫不被 SQLite 凍住 |
| [C++ 演進史:複雜性詛咒、記憶體危機與 AI 時代絕地反擊](./technology/dev-tools/cpp-evolution-complexity-ai-era.md) | 三座冰山(複雜性/泛型反噬/Rust 圍剿);但 PyTorch/CUDA/llama.cpp 引擎全是 C++ |
| [ddddocr 原始碼深讀:離線驗證碼識別 SDK(OCR/檢測/滑塊/MCP)](./technology/dev-tools/ddddocr-captcha-ocr.md) | ONNX+CTC 解碼、YOLOX 檢測、OpenCV 滑塊;FastAPI+MCP 給 agent 用;雙面刃工具 |

### 🎨 web-dev(網頁前端開發)
| 主題 | 一句話 |
|---|---|
| [CSS View Transitions:純 CSS 讓多頁網站有 SPA 般轉場](./technology/web-dev/css-view-transitions.md) | 一行 @view-transition 啟用;old/new/group 三偽元素+共享圖 morph;progressive enhancement |

### 🛡️ ai-safety(AI 安全與評測)
| 主題 | 一句話 |
|---|---|
| [AI 學會裝傻和欺騙:為什麼 Safety Evaluation 跟不上大模型](./technology/ai-safety/safety-evaluation-crisis.md) | 湧現/情境覺察/Sleeper Agents/Sandbagging,benchmark 永遠落後 |
| [RSI(遞迴自我改進)是新的 AGI:Anthropic 為何呼籲暫停](./technology/ai-safety/rsi-recursive-self-improvement-anthropic.md) | AI 研發 AI 的飛輪;Claude 寫 >80% 生產 code、優化加速 ~52×;唯一護城河是研究品味 |

### ⚛️ quantum-computing(量子計算)
| 主題 | 一句話 |
|---|---|
| [量子計算:量子效應如何突破計算的邊界](./technology/quantum-computing/quantum-computing-explained.md) | 疊加+干涉操控機率向量,非「影分身試所有解」;Grover √n、Shor 威脅密碼 |

### 📡 telecom(電信)
| 主題 | 一句話 |
|---|---|
| [3GPP 懸疑小說《頻譜密典》](./technology/telecom/spectrum-codex-novel.md) | 用懸疑小說包裝 3GPP 協定知識 |
| [WiFi 是怎麼傳遞資訊的?把資訊裝進電磁波的硬核原理](./technology/telecom/wifi-how-it-works.md) | QAM 在振幅相位刻位元、OFDM 擠千條子載波、MIMO 開平行空間;WiFi4→7 提速之路 |

### 🗞️ github-weekly(GitHub 週報)
| 期數 | 主題 |
|---|---|
| [第 115 期:桌面 AI 助手、程式 Agent 知識系統與隱身瀏覽器](./technology/github-weekly/issue-115.md) | OpenHuman / CodeGraph / CloakBrowser / CLI-Anything / LingBot-Map |
| [第 114 期:DeepSeek V4 終端編程 Agent、金融 Agent 集合與開源電子簽](./technology/github-weekly/issue-114.md) | DeepSeek-TUI / financial-services / DocuSeal / easy-vibe / SuperSplat |
| [第 113 期:AI 終端機開源、駭客工具箱、Skill 生態與一句話生成影片](./technology/github-weekly/issue-113.md) | Warp / hackingtool / Skills / awesome-codex-skills / Pixelle-Video |
| [第 112 期:DeepSeek V4 開源、GPT-Image-2 玩法庫與開源金融終端](./technology/github-weekly/issue-112.md) | DeepSeek-V4-Pro / GPT-Image-2-prompts / FinceptTerminal / DeepTutor / Apollo-11 |
| [第 111 期:Karpathy 經驗的 Claude Code 設定、Agent 協作平台與新 TTS](./technology/github-weekly/issue-111.md) | karpathy-skills / Multica / VoxCPM2 / MarkItDown / QMD |
| [第 110 期:Rust 版 Claude Code、端側 AI、記憶宮殿與自進化 Agent](./technology/github-weekly/issue-110.md) | claw-code / AI Edge Gallery / MemPalace / Hermes Agent / OpenScreen |
| [第 109 期:被開源的 Claude Code、JS 排版引擎與瀏覽器端 3D 建模](./technology/github-weekly/issue-109.md) | Claude Code / Pretext / Claude How To / Gemma 4 / Pascal Editor |
| [第 108 期:Claude Code 終極優化、離線生存電腦與從零手搓 Agent](./technology/github-weekly/issue-108.md) | Everything Claude Code / N.O.M.A.D. / Learn Claude Code / Page Agent / OpenMAIC |
| [第 107 期:被 OpenAI 收購的 AI 安全工具、AI 代理事務所與上下文資料庫](./technology/github-weekly/issue-107.md) | promptfoo / agency-agents / awesome-openclaw-skills / claude-hud / OpenViking |
| [第 106 期:阿里 OpenClaw 替代、WiFi 人體感知與多代理深度研究](./technology/github-weekly/issue-106.md) | CoPaw / RuView / worldmonitor / GitNexus / deer-flow |
| [第 105 期:Rust 版 OpenClaw、本地語音克隆、Qwen3.5 與 AI 滲透測試](./technology/github-weekly/issue-105.md) | zeroclaw / voicebox / Qwen3.5 / pentagi / carbon |
| [第 104 期:智譜 GLM-5 旗艦模型、AI 編碼助手配置管理與金融研究 Agent](./technology/github-weekly/issue-104.md) | GLM-5 / cc-switch / shannon / monty / dexter |
| [第 103 期:超輕量 OpenClaw 復刻、程式 Agent 記憶與聊天記錄分析](./technology/github-weekly/issue-103.md) | NanoBot / Beads / ChatLab / Vision-Agents / KeyStats |
| [第 102 期:個人 AI 助理、React 生成影片與 Kimi K2.5 開源模型](./technology/github-weekly/issue-102.md) | OpenClaw / Remotion / Kimi K2.5 / PageIndex / LangExtract |
| [第 101 期:開源版 Cowork、資料工程實戰課、瀏覽器 MCP 與設計 Agent Skill](./technology/github-weekly/issue-101.md) | Eigent / data-engineering-zoomcamp / chrome-devtools-mcp / ui-ux-pro-max-skill / VoidNovelEngine |
| [第 100 期:開源程式 Agent、AI 技能框架與電腦操作 Agent](./technology/github-weekly/issue-100.md) | opencode / Superpowers / TARS / MiroThinker / icloud-downloader / wechat-exporter |
| [第 99 期:AI 程式代理編排、Claude Skills 與 Agent 生成 UI](./technology/github-weekly/issue-99.md) | vibe-kanban / skills / A2UI / Mole / fresh / rendercv |

---

## 💼 career(職涯與職場)

### 🧑‍💼 workplace(職場生存)
| 主題 | 一句話 |
|---|---|
| [十大恐怖主管特質:從竹科裸辭看「只做向上管理」如何逼走好員工](./career/workplace/ten-toxic-manager-traits.md) | 看主管做了什麼別聽他說什麼;光說不練/微觀管理/造假……中一點就是有毒信號 |

---

## 🩺 health(健康與身體)

> ⚠️ 健康相關筆記為衛教資訊整理,**非醫療建議**;診斷與治療請諮詢醫師。

### 🌱 wellness(健康保健)
| 主題 | 一句話 |
|---|---|
| [你以為健康,其實天天慢性發炎:四個敵人與四個對策](./health/wellness/chronic-inflammation-four-enemies.md) | 超加工食品/久坐/內臟脂肪/睡眠不足走四條路徑;只改一個或吞薑黃素沒用;驗 HS-CRP |

---

<div align="center">

<sub>📚 每篇筆記結尾皆附「來源」連結 · 🤖 內容由 Claude Code 協作整理 · 🗓️ 每週自動新增</sub>

</div>
