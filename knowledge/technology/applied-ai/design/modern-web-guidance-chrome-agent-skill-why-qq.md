# Modern Web Guidance 1.0:Chrome 為 AI 編程工具做的「現代前端知識庫」,官方評測通過率 56% → 88%(Why QQ)

> 影片:Why QQ「AI写前端却停留在2019年?详解 Modern Web Guidance」(2026-11-14,約 8 分鐘,官方 zh-Hans 字幕)。
> ⭐ **2026-11-19 增補 YAHA學堂**〈13 次實測〉(2026-11-18,自動字幕),見〈增補:YAHA學堂 13 次對照實測〉:自測顯示常見特性差距小、冷門特性 63% → 100%、成本約 2.3 倍;核實 Node 22+、遙測會收搜尋字串、上下文成本 repo 寫約 205 token(影片說 700)。
> 專案:<https://github.com/GoogleChrome/modern-web-guidance>(分發用倉庫)與 <https://github.com/GoogleChrome/modern-web-guidance-src>(原始碼、評測與規則)。
>
> ⚠️ 立場:說明欄與片尾只有一般訂閱呼籲,無業配;本篇的數字多為 **Google/Chrome 官方自報的評測結果**,不是獨立第三方實驗,見「邊界」一節。

---

## 它在解決什麼問題

模型寫前端常停在舊寫法:訓練資料裡有大量遺留程式碼,生成時又會模仿專案裡已有的風格(影片引 Chrome 官方說法:AI 會把 2015 年形成的慣例一起複製)。同時瀏覽器已內建很多過去要靠 JavaScript 或第三方函式庫的能力:CSS 的容器查詢、`:has()`、滾動驅動動畫、現代色彩函式;HTML 的 `dialog`、`popover`、原生表單驗證;還有任務排程、圖片優先級、新的安全 API。模型可能知道某個 API 存在,卻不知道適用場景、相容性處理與要補的無障礙細節(`[1:00]`–`[1:25]`)。

> 影片標題的「停在 2019 年」是**修辭**,不是 Google 給模型劃定的知識截止年份——影片自己在 `[0:52]` 就說明了。

---

## 運作方式(已讀原始碼與 SKILL.md)

```mermaid
flowchart LR
    U["使用者提出前端需求"] --> S["Skill 啟動<br/>要求先查指南再寫 HTML CSS JS"]
    S --> Q["CLI search<br/>本地語意向量 加 BM25"]
    Q --> R["合併排名<br/>Reciprocal Rank Fusion"]
    R --> G["Agent 選指南 ID"]
    G --> T["CLI retrieve<br/>程式碼模式 陷阱 相容性 降級"]
    T --> C["寫入當前上下文"]
    C --> V["寫完對照指南檢查<br/>並在回覆末尾揭露用了哪些指南"]
```

| 影片說法 | 一手來源(clone 兩個 repo 讀過) | 結論 |
|---|---|---|
| Chrome 發起;Chrome、Edge、Firefox、MDN 與標準和無障礙專家共同參與 | README:「由 Google Chrome、Microsoft Edge、Mozilla Firefox、MDN 團隊與 Web 開發社群共同管理(Stewarded by…)」 | ✅ 已核實 |
| 1.0 於 2026 年 11 月 10 日正式發布 | GitHub Releases:`v1.0.0` 發布於 2026-11-10;`package.json` 版本 1.0.0;此前是 `v0.0.19x` 每週發版 | ✅ 已核實 |
| 倉庫列 250 項現代 Web 特性 | README 摺疊清單:CSS 與版面 140 + HTML 與 DOM 36 + JavaScript 與 API 74 = **250** | ✅ 已核實 |
| 指南覆蓋兩百多個場景 | `skills/modern-web-guidance/guides/` 下有 209 個 `.md`(分 accessibility、css、forms、html、js、performance、security、ui-components、webmcp 等 17 個資料夾);**「場景」與「檔案數」未必一對一**,但數量級吻合 | ✅ 大致核實 |
| 流程是 search → 選 ID → retrieve | README「How It Works」:Agent 跑 `modern-web-guidance search "<query>"`,再 `retrieve <guide-id>` | ✅ 已核實 |
| 本地混合檢索:語意向量 + BM25,再用 RRF 合併 | README:「離線、零依賴的 embedding 模型加 BM25,無網路呼叫、無 API key」;`src/rag/bm25.ts` 匯出 `reciprocalRankFusion`;`src/cli/modern-web.ts` 動態載入 BM25 | ✅ 已核實 |
| 蒸餾過的輕量 Embedding 查找表,取代沉重的模型執行環境 | `src/rag/benchmarks/` 的 README 與測試提到 **word tables 的蒸餾**與 static embedder;**具體蒸餾方法與尺寸我只看到存在、未逐行讀** | ⚠️ 大致核實,細節未讀 |
| 不必為每次查詢再叫遠端大模型 | README:CLI 全程離線、無網路呼叫、無 API key | ✅ 已核實 |
| 預設以 Baseline Widely available 為準;可在 AGENTS.md 或 CLAUDE.md 宣告目標;新特性要漸進增強、特性偵測或輕量 fallback | `SKILL.md`「Interpreting Browser Support & Fallbacks」:預設假設 **Baseline Widely available** 可無 fallback 使用,其餘特性「必須」依指南的 fallback 建議;使用者可自訂支援範圍;並建議把政策寫進 `AGENTS.md` 或 `CLAUDE.md`(例:允許 Newly Available,但自訂 fallback 限 ≤20 行且不加外部依賴) | ✅ 已核實 |
| 1.0 新增遺留程式碼掃描,本地用 AST 與 HTML/CSS 解析器,不用 LLM 也不耗 Token | CLI 有 `legacy-scan` 指令;`SKILL.md` 寫它只掃「精選子集(約 20% 的指南語料)」 | ✅ 已核實(影片說「約五分之一」正確) |
| 規則在約 4.5 萬個開源倉庫上校準、未見程式碼上靜態匹配精度 ≥80%、上下文複核精度 ≥90% | `src/analyzing/rules/index.ts` 註解寫**規則升級的門檻**:Post-Verifier 精度 ≥90%,且靜態匹配精度 ≥80%(n ≥ 10),或稀有模式 ≥90%(n ≥ 5);**「4.5 萬個倉庫」我沒在原始碼或文件找到** | ⚠️ 門檻已核實;**4.5 萬倉庫校準未能核實**(影片轉述自官方說法,出處不明) |
| 沒有一鍵 `--fix`;Agent 要檢查周邊程式碼排除誤報,再檢索指南、重構、重跑掃描與專案測試 | `SKILL.md`「Alternative flow: Modernize an existing codebase」是多步流程,`legacy-scan` 旗標只有 `json`、`guide`、`include-docs-and-tests`,**沒有 fix** | ✅ 已核實 |

---

## 影片舉的程式碼案例(對照官方指南)

1. **自動長高的輸入框:** 舊作法監聽 `input`、設 `height: auto`、讀 `scrollHeight` 再寫回,每敲一字可能觸發版面計算;現代作法是 CSS `field-sizing: content` 搭配 `min-block-size` / `max-block-size`(`[1:27]`–`[1:53]`)。→ ✅ 指南 `forms/form-fields-automatically-fit-contents.md` 的 textarea 範例正是 `field-sizing: content; min-block-size: 3lh; max-block-size: 10lh;`,並提醒「明確的 `width` / `height` 會覆蓋 `field-sizing`」(例:全域 `width: 100%` 要覆寫)。
2. **彈出層:** AI 常寫按鈕加 click 事件再呼叫 `showPopover`,自己維護開關狀態、點外面關閉與焦點;現代作法用 HTML `popover` / `popovertarget` 宣告式控制,對話框用原生 `dialog` 搭配 top layer、`@starting-style`、`transition-behavior` 做進出場動畫(`[1:56]`–`[2:22]`)。
3. **無障礙、動效、表單的常漏細節:** 開啟 modal 時焦點要進入、關閉後回到觸發鈕、背景要從鍵盤路徑移除,不能只加 `aria-modal`;使用 View Transitions、平滑捲動、滾動驅動動畫要尊重 `prefers-reduced-motion`;表單要處理 `autocomplete`、`aria-invalid` 與常駐格式提示(`[2:24]`–`[2:51]`)。
4. **效能:** 模型常把大迴圈丟 Web Worker,卻忽略主執行緒上零碎任務自己用 `setTimeout` 排隊;可考慮 `scheduler.postTask` / `scheduler.yield`;長清單可評估 `content-visibility` 與 `contain-intrinsic-size`;媒體要明確尺寸避免跳動(`[2:53]`–`[3:20]`)。→ 倉庫指南中 `performance/break-up-long-tasks.md` 涵蓋 `scheduler.yield`。
5. **安全:** Google 的評測發現模型通常不會主動補 CSP 或跨來源隔離;處理不可信 HTML 時可能手寫 DOMParser 白名單、或用過鬆的 Trusted Types 策略;指南引導優先用瀏覽器原生 Sanitizer,不支援時用經驗證的函式庫並正確設 CSP;Passkey 涉及序列化、能力偵測與憑證生命週期,「只記住 WebAuthn 名稱遠遠不夠」(`[3:22]`–`[3:51]`)。→ 這段是**評測者的觀察與指南的設計取向**,**我沒有逐一讀完 security 指南對應條目**,標為「未逐項核實」。

---

## 官方評測:56% → 88% 怎麼來的

**影片說法**(`[6:28]`–`[7:33]`):配對 A/B 方法,同一個開發任務分別交給沒裝與已裝指南的 Agent;任務描述不直接告訴模型該用哪個 API;再用 Playwright 在真實瀏覽器檢查 DOM、計算樣式、執行期行為與無障礙;Dashboard 彙總約 5,300 項檢查、三個 Agent 家族;11 月 8 日模型明細 Claude Code 57% → 88%、Codex 54% → 82%、Antigravity 58% → 94%。

**核實:** `modern-web-guidance-src` README 的「Recent eval results snapshot」:

| 日期 | Agent + 模型(依 repo 表格寫法) | 任務 / 檢查數 | 未引導 → 引導(提升) |
|---|---|---|---|
| Nov 8 | claude_code(opus-5-5) | 215 / 1801 | 57% → 88%(+31pp) |
| Nov 8 | codex_cli(gpt-6.1-sol) | 215 / 1795 | 54% → 82%(+28pp) |
| Nov 8 | antigravity_cli(gemini-4-argon) | 214 / 1673 | 58% → 94%(+36pp) |

- ✅ 三個明細數字與影片一致;三者檢查數相加 1,801 + 1,795 + 1,673 = **5,269**,與影片說的「約 5,300 項」吻合。
- ✅ 影片標題數字「56% → 88%、+32 個百分點」是官方首頁的**彙總值**;repo 表格只列單一 Agent 的日期明細,**彙總值本身我沒在 repo 讀到**(可能在線上 Dashboard),標為「彙總值未能核實,明細已核實」。
- ✅ 評測方法 README 寫得更細:任務以完整基底應用(如 `daily-grind`、`devtools-times`)模擬真實請求、**提示不點名 API 或特性**;Playwright 評分器驗證來源模式、計算樣式、執行期 DOM 與無障礙狀態;評分器以多 Agent「黃金解」(目標 100% 通過)與未修改基底應用(目標 0%)**自我校正**;衡量指標是「機會(100% − 未引導通過率)」與「提升(引導 − 未引導)」,單位是**百分點 pp,不是相對百分比**。

### 邊界(影片也自己講了)

- 任務集只覆蓋專案選擇的開發場景;自動化檢查不等於完整人工 code review;無障礙檢查只涵蓋部分基礎機制,**不等於完整 WCAG 稽核**;引導後也沒到 100%(可能沒檢索到指南、漏 fallback、沒落實每一條);結果會隨模型、任務、提示與專案要求變化(`[7:02]`–`[7:33]`)。
- **本庫補充:** 評測由專案方自己設計與執行,**非獨立第三方複現**;模型名稱是 repo 表格的寫法,本庫未另外驗證;三個 Agent 之間的差異(+28 到 +36 pp)與未引導基準(54%–58%)也提醒你:**幫助最大的是「原本就不夠現代的實作」**。

---

## 怎麼安裝與使用

- **一行安裝(互動式精靈):** `npx modern-web-guidance@latest install`;支援 Claude Code、Codex、GitHub Copilot、Antigravity 等,也有 `npx skills add GoogleChrome/modern-web-guidance` 與 `gh skill install GoogleChrome/modern-web-guidance`。
- **不安裝先試用:** `npx modern-web-guidance@latest search "animate a dialog modal backdrop"`、`retrieve "animate-to-from-top-layer"`、`legacy-scan .`。
- **技能包:** `modern-web-guidance`(README 標約 205 tokens 的啟動成本)與 `chrome-extensions`(約 175 tokens;Manifest V3 等)。
- **實驗性特性預設不開:** Origin Trial 與 volatile(單一引擎、近三個月內出貨或仍不穩定)特性的指南仍可被搜到,但預設閘住,要用 `set-allow-origin-trials`、`set-allow-volatile-features` 開啟。
- 影片提到 Google 也推薦搭配 **Chrome DevTools for agents**:前者供現代 Web 知識,後者讓 Agent 在真 Chrome 互動、除錯、跑 Lighthouse,形成「生成 → 指導 → 驗證」閉環(`[7:48]`–`[7:57]`)。本篇**未讀 Chrome DevTools for agents 本身**。
- **隱私:** README 有「Telemetry & Privacy」一節,**本篇未讀其內容**,導入前請自行確認。

---

## 應用案例

1. **接手一個 2018 年的 jQuery 後台:** 先跑 `legacy-scan .` 找高信心的舊模式(手寫彈窗、捲動監聽),再讓 Agent 逐項依指南重構、重跑掃描與專案測試。注意它只涵蓋約 20% 的指南,**掃不到不代表沒有舊寫法**。
2. **新專案要求「支援過去兩年的瀏覽器」:** 在 `AGENTS.md` 寫 `Browser Support: Baseline 2024` 之類的政策(依 SKILL.md 的範例格式),讓 Agent 對尚未廣泛支援的特性自動採用漸進增強與特性偵測,而不是無條件追新。
3. **用 Claude Code 寫表單與彈窗元件:** 裝好後,Agent 在寫 HTML/CSS 前會先 `search`、`retrieve`;回覆末尾會附「### Modern Web Guidance」一節,條列套用了哪些指南與避開了什麼坑(`SKILL.md` Step 4 的要求),**可當 code review 的檢查清單**。
4. **評估要不要導入團隊標準流程:** 先在一個內部小專案跑相同任務兩次(裝/不裝),用自己的 lint、Lighthouse 與人工 review 比較,**別直接引用官方 +32 個百分點當承諾**。

## 增補:YAHA學堂 13 次對照實測(2026-11-19 增補)

> 影片:YAHA學堂〈[Claude Code 真需要 Google 這個技能?Modern Web Guidance 教學|13 次實測,效果與代價一次看](https://www.youtube.com/watch?v=vLTHW_MHWFM)〉(2026-11-18,約 8.6 分鐘)。**字幕為 YouTube 自動字幕,看得出是機翻再轉繁(例如把 Claude Code 寫成「CloudCode」、「Claude 程式碼」),下列時間點可靠、字句僅供對照,數字以說明欄與官方資料為準。** 說明欄附官方文件連結與指令,無業配字樣。

### 影片重點

| 時間 | 重點 |
|---|---|
| [0:21](https://www.youtube.com/watch?v=vLTHW_MHWFM&t=11s) | 範例是 2019 年風格的小型麵包店網站:jQuery 切換 FAQ、手動 JS 調整輸入框高度、動畫硬寫高度到 9000px |
| [2:02](https://www.youtube.com/watch?v=vLTHW_MHWFM&t=112s) | `legacy-scan` 兩秒掃出 9 項與指南對應的舊寫法,附檔名與行號,無 AI、無 API;限制是**只有約 20% 的指南有掃描規則**,他的下拉選單就漏掉,仍需 Agent 補查 |
| [2:42](https://www.youtube.com/watch?v=vLTHW_MHWFM&t=152s) | Claude Code 安裝兩個指令:加 Google 外掛來源、安裝外掛;提醒 Anthropic 官方市集也列了此外掛但版本停在 0.0.194、缺掃描流程,要改裝 Google 來源並開自動更新 |
| [3:12](https://www.youtube.com/watch?v=vLTHW_MHWFM&t=182s) | 即使不用也會佔上下文,影片說每次對話約 700 token;匿名使用統計可用環境變數關閉 |
| [3:34](https://www.youtube.com/watch?v=vLTHW_MHWFM&t=214s) | 改寫流程:先掃描 → 驗證結果 → 提三階段計畫並問「支援哪些瀏覽器、可否移除 jQuery」→ 一次檢索 8 份指南,約 2 分 20 秒改 3 個檔 |
| [4:33](https://www.youtube.com/watch?v=vLTHW_MHWFM&t=263s) | 結果:jQuery 移除;瀏覽器檢查前後 8/10 → 10/10;意外修好「選單關不掉」(一行 CSS 覆蓋屬性)與 Esc 關閉 |
| [5:03](https://www.youtube.com/watch?v=vLTHW_MHWFM&t=293s) | 建新頁面,用純文字提五個需求,Agent 自行把每個需求轉成指南搜尋(工具提示用 CSS 錨點定位、對話框開啟時背景不捲動) |
| [5:54](https://www.youtube.com/watch?v=vLTHW_MHWFM&t=344s) | Baseline 目標預設「廣泛可用」(影片說主流瀏覽器支援至少 30 個月);可在 `CLAUDE.md` 加一行改成如 2024,Agent 逐特性判斷:`light-dark` 不需 polyfill、`field-sizing` 較新所以保留原腳本當備援 |
| [6:36](https://www.youtube.com/watch?v=vLTHW_MHWFM&t=396s) | **13 次自測**(同提示同模型,開/關各 2–3 次,檢查項先寫好):建新頁面兩邊都全過;舊站改造兩邊都修好 9 項;冷門特性頁面**開 100%(影片後來說依原標準為 88%)vs 關 63%**,且總漏同一項;成本約 2.3 倍 |
| [8:16](https://www.youtube.com/watch?v=vLTHW_MHWFM&t=486s) | 建議:先跑免費的 `legacy-scan`;有用較新瀏覽器特性才裝外掛;價值主要在冷門特性 |

### 核實(讀 `GoogleChrome/modern-web-guidance` repo 原始碼與 web.dev)

- ✅ **Node 22+**:`package.json` 的 `engines.node` 為 `>=22.0.0`。影片說「文件沒提」,本文只確認 repo 有此限制,**官方文件是否漏寫未能核實**。
- ✅ **遙測**:README「Telemetry & Privacy」寫明收集安裝次數、呼叫的 Agent 名稱、指南檢索 ID 與 **Agent 產生的搜尋字串**(例如 "dark mode scrollbar color-scheme"),**不收原始使用者提示**;關閉方式是環境變數 **`DISABLE_TELEMETRY=1`**。影片說「匿名使用統計」屬實,但漏了「搜尋字串會被收」這點,對隱私敏感專案要注意。
- ⚠️ **上下文成本影片偏高?** README 標註 `modern-web-guidance` 技能約 **205 token**、`chrome-extensions` 約 175 token(兩者合計約 380)。影片說「約 700 token」,**差距原因不明**(可能含外掛其他註冊內容或不同統計方式),本文標「需補充」,不判斷誰對。
- ✅ **Baseline 預設**:`SKILL.md` 寫「All guides assume **Baseline Widely available** features are safe to use without fallbacks…」,非 widely available 的特性要照指南做備援,除非使用者指定自訂支援政策,與影片一致。web.dev:「Widely available」= 成為 Newly available 後滿 **30 個月**,影片的 30 個月說法 ✅。
- ✅ **版本**:repo `plugin.json` / `package.json` 版本 `1.0.1`,最後一次 commit 為 2026-11-16,與影片說 1.0 於 11 月 10 日發布後仍持續更新相容。**1.0 發布日與「下載量四倍」** 未能核實(未讀官方公告)。
- ✅ **官方評測 57% → 88%**:與本文上方 repo 表格(claude_code + opus-5-5,Nov 8)一致;影片引的是同一個數字。
- ❓ **未能核實**:`legacy-scan` 規則涵蓋「約 20% 指南」(repo 有 210 份指南,但我沒逐一數有規則者)、Anthropic 官方市集版本停在 0.0.194、13 次自測的原始資料與 2.3 倍成本(作者自測,單一模型、每組 2–3 次,樣本極小)。

### 我的判讀

1. **這片補的是「值不值得裝」的反面證據**:Why QQ 版引官方評測(+31pp),YAHA 版的自測顯示**常見特性 Claude 本來就會寫,差距只出現在冷門特性**,和官方「引導後大幅提升」不矛盾,而是說明提升集中在長尾。
2. **成本 2.3 倍 + 小樣本**:是作者自己的數字、不是第三方。與其全裝,更務實的是先跑免費的 `legacy-scan` 當體檢,再決定要不要常駐。
3. **「先寫檢查項再測」是這支片最值得學的做法**,和本庫[[agent-verification-before-scale-lauren-tan-reaction]]的「先定義驗證再放大」同一精神;驗收要在瀏覽器實測,而不是看 Agent 自述。

### 應用案例(增補)

- **接手舊官網前的體檢**:`npx -y modern-web-guidance@latest legacy-scan .` 兩秒給出「檔案:行號 + 指南名」清單,先看有幾項再決定要不要裝外掛、花 2.3 倍成本做改寫。
- **在 `CLAUDE.md` 寫瀏覽器目標**:加一行 Baseline 年份,Agent 便逐特性決定要不要 polyfill,避免舊站為了 IE 殘影一律保守寫法。
- **隱私受限的客戶專案**:先 `export DISABLE_TELEMETRY=1` 再用,搜尋字串可能帶出專案功能描述。

## 影片未細講、值得追的延伸

- 官方線上評測 Dashboard 與彙總值的計算方式:<https://googlechrome.github.io/modern-web-guidance-src/>
- `legacy-scan` 的規則與「4.5 萬倉庫校準」出處:`modern-web-guidance-src/src/analyzing/` 與 `docs/EVALS.md`。
- 官方文件:<https://developer.chrome.com/docs/modern-web-guidance>。

---

## 來源

- 增補影片:YAHA學堂〈Claude Code 真需要 Google 這個技能?Modern Web Guidance 教學|13 次實測〉(2026-11-18):https://www.youtube.com/watch?v=vLTHW_MHWFM(YouTube 自動字幕 zh-Hans,機翻痕跡明顯,非人工字幕)
- 增補核實:`git clone --depth 1 https://github.com/GoogleChrome/modern-web-guidance`(2026-11-19 讀 package.json、plugin.json、README、SKILL.md,clone 已刪除);Baseline 定義 https://web.dev/baseline

- 影片:Why QQ「AI写前端却停留在2019年?详解 Modern Web Guidance」(2026-11-14):<https://www.youtube.com/watch?v=ta5sXjdQ0sA>(官方 zh-Hans 字幕,含時間)
- 專案(2026-11-15 `git clone --depth 1` 讀 README、SKILL.md、指南與原始碼,clone 已刪除;GitHub API:⭐ 約 1.51 萬、Apache-2.0、2026-03-23 建立):
  - <https://github.com/GoogleChrome/modern-web-guidance>
  - <https://github.com/GoogleChrome/modern-web-guidance-src>
- 官方文件:<https://developer.chrome.com/docs/modern-web-guidance>(本次未讀,僅 README 引用)

## 相關筆記

- [[agent-verification-before-scale-lauren-tan-reaction]] — 先定義驗證再放大;本篇增補的「先寫檢查項再測」同精神
- [[claude-web-design-skills-benchmark-pnh]] — 網站類 Claude Code Skill 的實測對照
- [[impeccable-frontend-design-skill-ai-slop]] — 另一個讓 AI 前端不走樣的設計 Skill
- [[chenxing-github-top5-2026-11-14-graphify-hallmark-anthropic-skills-pocock-t3code]] — 同期的 Hallmark 與 Skills 倉庫介紹
- [[issue-138]] — 同日週報中 Meta Astryx:給 Agent 查詢元件的設計系統
