# 別跟單一模型「結婚」:Model Agnostic 才是槓桿位置

> 來源:Elijah Bricker(AI drivers 創辦人)〈I Tried Every AI Model, This is What Works in 2026〉。Opus 4.8、Gemini 3.5、Codex GPT-5.5 全出了,每個都有人說最強。這支影片切穿噪音,給一個核心結論:**別跟任何一家公司/模型「結婚」——保持 model agnostic(模型無關),把模型當可替換的零件,穿過你自己擁有的 infrastructure。**

> ⚠️ 影片中的模型版本名(Opus 4.8、Gemini 3.5、Codex GPT-5.5 等)為影片說法,僅作情境參考。

---

## 一句話總結

**沒有魔法模型、沒有明確贏家**——一個領先、另一個追上,來回循環。所以正確的姿勢不是「找出最強模型、把所有任務塞進去」,而是「**看任務本身,再選最適合這個任務的模型/工具**」。要做到這點,你得擁有**自己的 infrastructure / operating system**,讓模型只是「穿過去」的東西;升級或替換模型時,一行設定的事,而不是回去手改一堆硬編碼。

---

## 核心:Model Agnostic = 槓桿位置

跟單一公司「結婚」的兩個壞處:
1. **被那家公司綁架**(無論是 OpenAI、Anthropic 還是誰)——它降智、漲價、出事,你只能跟著。
2. **學得更慢**——只用一種工具,就少了跨模型比較的視野。

> **歷史類比:** PC 出現、網路出現時,**擁抱新工具的人贏了,把眼睛閉起來推到一邊的人輸了**。就像當年死守 Android 不碰 iPhone 的人,一旦用了就回不去。**對某家公司有 pride、跟另一家結仇,都是公司用來綁住你的心理操控**——Claude 有好東西就用、OpenAI/Gemini/Hermes 有好東西也用,你才會得到「從自身經驗出發、中立而有機」的判斷。

**80/20 原則:** 看 Twitter、看 YouTube(像這支影片)只佔你判斷的 **20%**,且只是強化你已有的看法;真正的 **80%——你的信心與理解——來自每天親自用這些模型**。別人說「Opus 對我做 UI 很好」,你自己用可能覺得 Gemini 更好;每個人的業務有 nuance,所以你必須親自用過,才知道何時該用哪個。

---

## 範例:一個實作者怎麼「按任務派模型」

作者經營 AI drivers(幫企業導入 agentic AI 基礎設施),他的分工:

| 任務 | 用哪個 |
|---|---|
| 基礎建設、實際的 nuts and bolts | **Codex** |
| 文案生成(copy) | **Sonnet** |
| 腦力激盪、高層次/策略性長任務、UI/UX 與儀表板 | **Opus** |
| 研究 | **Gemini** |
| 簡單重複的工作:cron jobs、watchdog、Hermes gateway 掛掉的告警 | **DeepSeek** |

> **關鍵對比:**
> - ❌ 「**最強模型是哪個?** Opus 4.8 → 把所有任務塞進去」——完全依賴那家公司,而它不會永遠最強,甚至現在是不是最強都難說。
> - ✅ 「**這是任務,有了任務的 context,最適合它的模型/工具是哪個?**」——這才是槓桿位置。

---

## 為什麼要「擁有自己的 infrastructure」

- 如果你把整個業務都跑在 Claude 上、到處**硬編碼** Opus 4.6/4.7,當 Opus 4.8 出來(或 Codex 突然遠勝),你得**手動翻遍 codebase、所有函式工具去改版本**,甚至整個重構——痛苦、費時、不是槓桿位置。
- 正解:**建一套完全屬於你、跑在自己電腦上的獨立 operating system / 內部 infrastructure**,從頭就設計成「模型可穿過」。要從 Opus 4.7 換 4.8、或從 Opus 換 GPT-5.5,都是輕鬆切換。
- **Hermes、OpenClaw 是 operators(管理 agent 的操作者),不是 AI 模型**——它們是讓你「把模型當可替換零件」的那一層。(怎麼搭這層,見 [[ai-operating-system-aios]]、[[hermes-main-agent-orchestration]]。)

---

## 應用案例 / 怎麼開始

- **服務型企業/一人公司**:把「找客戶、交付、營運」拆成任務,各自配最划算的模型(研究用 Gemini、寫程式用 Codex、策略用 Opus、雜事用便宜模型),而不是全押一個訂閱。
- **別被「升級」綁架**:把模型名稱集中在設定/環境變數,別硬編碼進每個檔案,新版一出一鍵切換。
- **不會建 infrastructure 也別焦慮**:別想著「現在就要把全部建好」。最簡單的起手式——**如果你只用過 Claude Code,就去玩玩 Codex、玩玩 Gemini**,自然會長出「model agnostic」的直覺。
- **核心心法**:不要被任何東西綁定——不只是公司、模型、工具,而是「任何東西」;對客戶、對業務、對一切,都要站在**可替換、可切換的槓桿位置**。

> 這與本庫 [[multi-tool-ai-workflow]](別追最強 AI、建你的多工具工作流)是同一條主軸的兩種講法:前者談「任務需要什麼資料→在哪→哪個 AI 能操作」,本篇補上「**擁有自己的 infrastructure、讓模型可替換**」這層槓桿視角。亦可對照 [[opus-4-7-workflow-upgrades]](跨模型 review)、[[three-valuable-ai-skills]](AI 調度力)。

---

## 來源

- Elijah Bricker(AI drivers),〈I Tried Every AI Model, This is What Works in 2026〉,YouTube:<https://youtu.be/FmIUUT-TXHs>(2026-06-07)
