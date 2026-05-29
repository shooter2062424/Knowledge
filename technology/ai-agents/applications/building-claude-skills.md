# Skill 實戰:從製作到維護一份「agent 會自動觸發、產出穩定、人類維護得了」的 skill

**主題分類:** AI / 代理工程 — 應用與實作
**來源:** YouTube〈Skill 實戰教學,從製作到維護的完整指南〉(Gary Chen,2026-04-25,約 20 分;講者自述替各公司做過上百個 skill,依繁中逐字稿整理)
**整理日期:** 2026-05-30

> 📌 本筆記的方法已用在使用者自己的 [claude_marketplace](https://github.com/shooter2062424/claude_marketplace) 上(`knowledge-tools` plugin 的 `rapid-learning` skill 即按此寫法)。

---

## 1. Skill 結構與漸進式披露

一個 skill 就是一個資料夾,通常三種東西:
- **`SKILL.md`** — 最上面 frontmatter(`name` + `description`),下面是傳授給 agent 的 **方法論**。
- **`references/`** — 參考資料(不是每次都要載入的內容)。
- **`scripts/`** — 讓 agent 直接執行的腳本(固定流程交給確定性腳本)。

**漸進式披露(progressive disclosure)三層**——這是能掛很多 skill 卻不爆 context 的關鍵:
1. 啟動時每個 skill 只載入 name+description(約 100 token)。
2. 對話觸發到才載入完整 `SKILL.md`。
3. `references`/`scripts` 真的需要時才載入。

---

## 2. 什麼時候該做 skill?三個信號

1. **重複性高、步驟固定**(一直在不同對話重複同樣指令)。
2. **你的 domain knowledge 是 AI 不知道的**(專案路徑規範、公司文件格式)。
3. **出錯成本高、需要標準化品質**(要對外交付)。

> 不用精算「只符合一個要不要做」——製作成本極低,**與其想不如直接做,用不到再刪**。

---

## 3. 兩種製作方法

- **① 逆向工程(新手友善):** 先實際跟 agent 協作完成一次任務(例:連 Google Drive 撈工作日誌 + 翻 GitHub commit → 彙整週報),滿意後 **千萬別關 session**(這是你最值錢的 context)→ 用 Claude 官方 **skill-creator** skill(marketplace 安裝)說「把剛剛的對話轉成可重複使用的 skill」。(非 Claude 也行:先叫它上網查 skill best practice。)
- **② 主動發起(brain dump):** 還沒實作過時,把「想達成什麼目的 + 想像中的流程 + 可能難點」丟給 AI,請它做成 skill,並要求「開始前有不清楚的先跟我釐清」。

> **心態:你是在當 AI 的 PM。** 別一直問「AI 能為我做什麼」,反過來想「我有沒有把 context、約束、方法、目標準備到足夠讓 AI 成功交付」。
>
> **進階:Evaluation-Driven Development**——做 skill 前先讓 AI 裸做一次(什麼方法論都不給),看它卡在哪,**那些卡點才是你該人為填補的空白**(而非腦補的規則)。優化也一樣:不是「再試一次」,而是問「缺工具?缺規則?缺文件?缺驗收標準?」——補系統缺口,不是抽籤式重跑。

---

## 4. 三個最常見的坑

### 坑一:agent 根本不觸發這份 skill
`description` 是 agent 判斷是否觸發的 **唯一根據**(因為漸進式披露)。三規則:
1. **同時包含「做什麼 + 何時用」**(只有其一 agent 不知道何時觸發/能做什麼)。
2. **用第三人稱**(別寫「I can help you...」會跟系統視角衝突)。
3. **包含使用者自然會說的觸發詞**(不是技術名詞——你都說「做週報」,description 卻寫「整理文件」,AI 要多一層推理)。

命名:**小寫 + 連字號 + 動名詞/名詞**(`weekly-report-drafting`、`pdf-processing`)。範例 description:
> `Drafts weekly status updates for managers, aggregating data from Google Drive and GitHub. Use when user mentions weekly reports, team updates, status summaries, or weekly reviews.`

也要避免 **過度觸發**(描述太廣,看 CSV 前三行也觸發處理 CSV 的 skill)。

### 坑二:產出品質不穩
**模型越強,人類要學會放手。** 窄 SOP 假設模型不會判斷,但推理模型基本吊打多數人類。Anthropic best practice:**給原則,不過度限縮做法**。好 SKILL 的核心是 **執行心法** 三要素:**為什麼這樣做 / agent 該抱什麼心態 / 執行時的 guiding principle**。

> 週報範例心法:「週報是寫給主管看的,整理資訊的標準不是『我做了什麼』,而是『主管需要知道嗎』;以卡點與下一步為優先。」——這不是步驟,是哲學/優先順序,agent 就能處理各種變體。
>
> **判準:這件事對錯有沒有客觀標準?有(表單欄位驗證)→ 寫窄一點/寫步驟;沒有(週報好壞)→ 寫原則。**

### 坑三:skill 太長(context rot)
載入 token 越多,召回精度越差。官方建議 **超過 500 行就該拆**(講者自己傾向 **200 行內**,因為太長自己都不想維護、出問題難回溯是哪份 skill 帶歪)。怎麼拆:
- **references** = 把細節/變體外掛(>100 行的 output format、公司術語表、只在特定情境用的範例如「進度落後的寫法」)。
- **scripts** = 把 **確定性操作**(排序、格式驗證、API 呼叫、計算)外包。例:固定撈過去 5 天 commit 寫成腳本,agent 從「自己去抓(可能 freestyle 抓 7 天)」變成「跑腳本讀結果」。**腳本程式碼永遠不進 context,只有執行結果餵給 AI** → 更穩又省 context。
- **subagent** = 容錯率低時當最後一層品管(separation of concerns:給它乾淨 context + checklist 驗收,避免主 agent 球員兼裁判)。

---

## 5. 應用案例:維護一份週報 skill(複利效應)

Skill 最有價值的是 **複利**:做一版、用一次修一次,一個月後已不是原本那份。但多數人做完就放著 → references 一堆沒用資料、200 行膨脹到 1000 行。**不維護的 skill 會越來越差**(錯誤觸發、燒多餘 token、產出不穩)。兩種維護時機:

1. **新模型出來時:** 拿既有 skill 跑一次,檢查「哪些是為補舊模型弱點加的」→ 新模型能自己處理就拿掉(呼應 [[bitter-lesson-cut-old-patterns]])。
2. **每次 workflow 跑完復盤:** 請 agent「盤點剛剛犯了哪些錯、背後原因、能否融入既有 skill 避免再犯」。

維護三動作:**刪冗餘 / 重整結構(整份重讀能不能快速抓骨架,不能就重構)/ references 萃取**。⚠️ agent 自己改 skill 會把結構搞亂、寫出人類難維護的東西——**寫入前一定 double check,別完全放手**。

**測試小技巧:** 開兩個 session。A 先查 skill best practice;B 觸發要優化的 skill 執行,把失敗處記錄丟給 A 提優化方向,你審核,持續跑。

---

## 6. Skill 的真正意義

> Skill 是 **個人知識轉移給 agent 的載體**——你要花很久教會新人的事,打包成 skill 後 agent 立刻學會。模型會自己越來越聰明,**你真正要做的是把你的「判斷/思考方式」交給它**。
>
> 回扣 **harness engineering**(見 [[ai-harness-explained]]):人類掌舵、agent 執行;skill 把你腦中的執行 logic 告訴 agent——這也是為什麼「執行心法」才是真正有獨特價值的東西。它是你、團隊、與 agent 之間 **協作的新介面**(對照 [[claude-skills-governance-man-group]] 的企業級 skill 治理)。

---

## 來源

- [YouTube:Skill 實戰教學,從製作到維護的完整指南(Gary Chen)](https://youtu.be/PuqX3Kv2ino)
