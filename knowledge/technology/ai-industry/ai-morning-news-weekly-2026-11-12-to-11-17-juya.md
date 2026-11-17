# AI 早報週報(2026-11-12 至 11-17):Gemini Decision 1、Gemini 4 Hydrogen、DeepSeek 應用 API、llama.cpp v1.0、Kitesurf、Cursor 資安事件(橘鸦 Juya + 一手來源核實)

> **來源頻道:** 橘鸦 Juya(`@imjuya`,每日「AI 早報」短影片)。本篇併整 6 支:`n9o9Tv2s0HQ`(11/12)、`-xCz5oneKZ0`(11/13)、`5Q89lUEYDWI`(11/14)、`-v0xqIfR8Kw`(11/15)、`eyxGH3TCUuY`(11/16)、`67rZTbZnFqM`(11/17)。
> **讀了什麼 / 沒讀什麼:** 六支我**只讀了說明欄**(逐條標題、章節時間與來源連結),**沒有讀逐字稿,也沒有看畫面**;所以本篇**沒有影片內的時間點引用**,只能引用說明欄的章節時間。條目只是頻道的新聞標題,**未標「已核實」的一律不代表我查過**。核實的做法是直接去讀說明欄附的官方原文。
> **立場:** 說明欄沒有業配或聯盟連結;資訊型頻道。
> **形式:** 早報本來就是每天十幾二十條標題,不逐日一篇;本篇挑「有官方原文可讀、且對工程選型有意義」的七條,其餘只留標題索引。上一份週報見 [[ai-morning-news-weekly-2026-11-05-to-11-10-juya]]。
> ⚠️ 11/11 那一期不在本篇範圍(上一份的最後一支是 11/10);本篇從 11/12 起算。

## TL;DR

1. **Gemini Decision 1**(11/12):Google 官方 Decisions API:一次最多 1,000 個是非/單選/評分題,不產生輸出文字,150–250 ms、$0.10/百萬輸入 token、輸出 token 不計費。**它的三種題型 `noul`、`choice`、`score` 與本庫 [[system-one-models-jev-calibrated-decisions]] 裡 Jev 的型態一模一樣**。
2. **Gemini 4 Hydrogen**(11/13):官方定價 $1.50 / $7.50 每百萬 token(1M 上下文不分段);Antigravity 新增 Orchestrator 在同一 session 切換模型。數字全是 Google 自報。
3. **DeepSeek 開放應用 API**(11/14):官方定價頁屬實:TTS、ASR、OCR 都有價目,語音目前五折。
4. **llama.cpp v1.0.0**(11/14):官方部落格屬實:`libllama` 與 `libggml` 同時 1.0.0,之後有破壞性 API/ABI 變更會升主版本。
5. **Cloudflare Kitesurf 開源**(11/15):Apache 2.0、跑在 Workers、不含瀏覽器容器、支援 CDP。
6. **Cursor 資安事件完整說明**(11/15):源頭在 **Fireworks 外洩的存取金鑰**,與上一份週報的 Fireworks 事件接上。
7. **Anthropic 安全評測建議**(11/15):原文讀了前半與數個小節,「十項」的計數我沒有逐項點算。

## 1. 核實過的七條

### 1.1 Gemini Decision 1 / Decisions API(11/12 早報,Google 11/11 發布)

讀了 Google 官方文章全文(`blog.google/.../gemini-decisions-api/`):

| 項目 | 官方內容 | 判定 |
|---|---|---|
| 是什麼 | 新端點 Decisions API,模型 `gemini-decision-1`,做「封閉集合決策」(選工具、策略檢查、模型路由、情境分級) | ✅ |
| 輸入 | 單一多模態輸入(文字、圖像、音訊、影片、PDF,最多 256K token)搭配最多 **1,000 個**獨立問題 | ✅ |
| 運作 | **不逐 token 生成答案文字**,在單次前向傳遞給出各選項機率與信心分數;端到端 **150–250 ms**(模型運算約 50–100 ms),問題數從 1 到 100 延遲幾乎持平 | ✅(官方自述) |
| 價格 | **$0.10 / 百萬輸入 token,輸出 token 計 $0**;共用輸入只計一次;沒有思考 token 費用、也沒有另計語音轉寫或 OCR | ✅ |
| 與 Gemini 3.5 Flash-Lite 比 | 官方稱在共同基準套件上「近 5 倍便宜」 | 官方自述,**基準細節沒讀到** |
| 三種題型 | `noul`(是/否機率)、`choice`(2–255 個選項、回傳歸一化機率)、`score`(有序量表、回傳連續加權分數與各級機率) | ✅ |
| 內部使用 | Gemini Notebook 用它做即時模型路由(最多降 40% 延遲)、Stitch 的 rapid canvas、CC 的 emoji 挑選(200 多個選項)、Google 搜尋用它偵測針對 MCP 工具的對抗行為 | ✅(官方說法,**「40%」未獨立量測**) |

⭐ **跟本庫既有筆記的關係:** Jev(TypeSafe AI 的 System One 模型)當初的賣點就是「不會打字、只回傳列舉值與機率」,本庫還特別更正過那個型態名稱就叫 `noul`。**Google 官方 API 現在用了完全相同的三種型態名稱**(`noul`、`choice`、`score`),概念上是同一類「把做決定從生成式呼叫中拆下來」的東西。我只讀了 Google 的文章,**沒有查兩者是否同源或誰先採用**,不下結論;但已可以說這個形態不再只是一家新創的產品。

> 實務解讀:路由、守門、分級這類「要結果不要文字」的呼叫,現在有了官方的低延遲選項;但**準確度與「領先、最低校準誤差」的基準數字都是官方自述**,上線前要用自己的標註集測,別只信文章。

### 1.2 Gemini 4 Hydrogen(11/13 早報,Google 11/12 發布,頁面 11/16 更新)

讀了 Google 官方文章全文:

| 項目 | 官方內容 | 判定 |
|---|---|---|
| 定位 | 速度與效率型模型;旗艦是 Carbon 與 Argon,Hydrogen 主打快速執行與多代理場景 | ✅ |
| 價格 | **$1.50 / 百萬輸入、$7.50 / 百萬輸出,1M 上下文全程單一價格** | ✅ |
| 上下文與輸出 | 原生 1M 輸入、最多 1M 輸出;四個思考層級 low / medium / high(預設)/ 新增 xhigh | ✅ |
| 智能指數 | 預設 high 時 Artificial Analysis Intelligence Index **51 對 Argon 的 50**,xhigh 54 | 官方引用第三方指數,**我沒讀該指數頁**,標未能核實 |
| 對 Gemini 3.8 Flash | 預設設定下完成任務快 2.5 倍;Terminal-Bench 4.1 **57% 對 18.2%**;虛構陳述少 5 倍以上 | 官方自述,**基準未獨立量測** |
| Antigravity Orchestrator | 同一 session 內動態在 Carbon、Hydrogen 間切換;Terminal-Bench 4.0 上接近 Carbon 成功率,平均少用 24% 額度、快 19% | 官方自述 |
| 其他基準 | HLE-Diamond 58.8%、Vals Tax Agent Bench 52.3%(稱第一)、Vals Legal Research 55.8%(並列第一)、Agent Arena 第 5 | 官方自述,第三方榜單我沒查 |

> 重點不在排名,在**定價結構**:長上下文不分段加價,對「大 repo 一次餵進去」的用法友善;但要和本庫 [[gemini-4-argon-release-benchmarks-pricing]] 並讀,Argon 與 Hydrogen 的分工是官方畫的線。

### 1.3 DeepSeek 開放應用 API(11/14 早報)

讀了 DeepSeek API 官方「Models & Pricing」頁:

| 項目 | 官方內容 | 判定 |
|---|---|---|
| 頁首公告 | 完整應用 API 已上線:網頁搜尋、檔案輸入、URL 讀取、模型安全、ASR、TTS 等 | ✅ |
| 語音價 | **TTS 每萬字元 $0.45**,限時五折 $0.225;**ASR 每小時音訊 $0.116**,限時五折 $0.058 | ✅ |
| 文件解析與 OCR | 每千頁 $0.225 | ✅ |
| 搜尋與抓取 | 每千次 $0.75(文字與圖片搜尋、web fetch) | ✅(與 [[deepseek-search-fetch-api-agent-evidence]] 吻合) |
| 模型與時段 | `deepseek-flash`(DeepSeek-V4.1-Flash-1017)與 `deepseek-v4-pro`(V4-Pro-0813);尖峰/離峰兩套價,**離峰半價**,尖峰為 UTC 週一至五 01–04 與 06–10 | ✅ |
| 舊名稱 | `deepseek-v4-flash` 等舊名仍可用但已由新版服務,以 Flash 價計費 | ✅ |

> ⚠️ 頁面上寫的是「限時五折」,**到期日我沒看到**,別把五折價當長期成本估算。

### 1.4 llama.cpp v1.0.0(11/14 早報,HF 部落格 11/13)

讀了 ggml-org 的 Hugging Face 官方部落格:

- **`libllama`(llama.cpp)與 `libggml`(ggml)同日發 v1.0.0**;公共標頭分別在 `llama.cpp/include/` 與 `ggml/include/`。
- **版本規則:** 對公共 C API 的破壞性變更升 MAJOR;向後相容的功能、後端更新、模型支援或 API 新增升 MINOR;無 API 變更的修正升 PATCH。今後 llama.cpp 與 ggml 的 API/ABI 不相容都會用主版本號標出。
- 發行管道:預發行檔(Linux、macOS、Windows、Android、iOS)、Docker、Debian、Homebrew、conda-forge、MacPorts、Winget、XCFramework。
- 部落格自述專案成立約 3.5 年,下游應用依賴日增。

> 這是 **「API 穩定性承諾」** 而不是新功能發布:自己包 llama.cpp 做產品的人,現在可以對 `1.x` 釘版本;之前追 master 的人要開始看 MAJOR 變動。⚠️ 我讀的是部落格,**沒有讀 GitHub release 頁的變更清單**。量化格式背景見 [[llm-quantization-q4-q8-gguf-qat-explained-mia]]。

### 1.5 Cloudflare Kitesurf 開源(11/15 早報)

讀了 Cloudflare 官方部落格:

- Kitesurf 是**跑在 Workers 上的「無狀態瀏覽器」**(8 月發布、9 月加 WebMCP),**Apache 2.0** 開源;能解析 HTML、套 CSS、執行頁面 JavaScript、渲染截圖,**不需要瀏覽器容器**,支援 Chrome DevTools Protocol,可接 Puppeteer。
- 技術組成:Blitz(HTML 解析、DOM、版面、繪製)、Stylo(CSS)、Boa(在 WebAssembly 內跑 JavaScript,僅在 Dynamic Workers 跑不了時當最後手段)、Linebender 與 Krilla(文字、2D 圖形、PDF)。
- 倉庫三部分:Engine(session 與連線)、PageScript(跑頁面與 JS)、PageRenderer(繪製);自架:`git clone`、`pnpm install --frozen-lockfile`、`pnpm run dev`。

> ⚠️ 我**沒有 clone 倉庫讀原始碼**(本篇只是週報條目),也沒有實測它和 Chromium 的相容度;部落格自己說 JavaScript 執行有「最後手段」的路徑,代表相容性不是 100%。要選型的人應該先 clone 再評估。

### 1.6 Cursor 資安事件完整說明(11/15 早報)

讀了 Cursor 官方部落格〈An update on our recent security incident〉:

| 項目 | 官方內容 |
|---|---|
| 起點 | **Fireworks**:攻擊者取得 Cursor 發給 Fireworks 的存取金鑰(該金鑰被 Fireworks 外洩),用它複製了一個唯讀儲存桶裡的資料 |
| 桶內資料 | 有限的 coding agent 追蹤紀錄,多為 2025 年、**非 Privacy Mode** 的會話;**少數追蹤含未遮蔽的憑證,API 憑證外洩的客戶不到 0.01%** |
| 橫向擴散 | 用那些憑證進入選定的 SaaS 工具,取得封存的非生產程式碼倉庫、客服資料、使用量指標、部分 agent 對話摘要、使用者寄給客服的部分憑證 |
| 惡意擴充 | 10/29 攻擊者在服務 VS Code 擴充市集的**快取**上放了假的 Claude Code 擴充(**Anthropic.claude-code 2.1.312 / 2.1.313**);**最多 5,000 名使用者可能收到,約 11 小時後移除**;Open VSX 本身沒有惡意程式;官方說這不是 Anthropic 產品的漏洞 |
| 未受影響 | Privacy Mode 使用者的提示與程式碼;生產系統;簽署金鑰;客戶程式碼倉庫(官方列出) |
| 處置 | 把所有推論流量移出 Fireworks 並停用其金鑰;輪換全部內部憑證;重建市集並驗證其他擴充;加強機密掃描;最後一次攻擊活動為 11/1 並被擋下 |
| 影響範圍口徑 | 追蹤資料外洩使用者「不到 0.05%」、API 憑證外洩「不到 0.01%」,兩個比例不同,是不同層次的集合 |

> ⭐ **與前一份週報連起來:** 上週早報記錄了 Fireworks 11/09 的更新(帳務資訊、少數客戶密鑰、資料集與未完成模型受影響);Cursor 這篇補上**同一事件在客戶端的鏈條**:供應商外洩金鑰 → 共享資料桶 → 追蹤內含憑證 → SaaS → 假擴充。教訓和本庫 [[claude-code-dont-ask-again-secrets-leak-checklist-why-qq]] 一致:**機密別進追蹤/對話,且要假設供應商會外洩**。官方的數字是公司自述,我沒有第三方核實。

### 1.7 Anthropic 安全評測建議(11/15 早報:「10 項安全評測建議」)

讀了 Anthropic 研究文〈Building strong safety evaluations〉的開頭與多個小節(全文約三萬字元,我讀到的是主要段落,**沒有逐項點算「十項」**):

- 主張:安全評測測的是**模型造成或助長傷害的傾向**而不是能力;「更安全」這句話只等於「在某組評測上分數更好」,所以評測本身的品質決定了結論。
- 借鏡心理學的可重複性改革:預先註冊假設與分析計畫、更好的測量、更嚴謹的統計。
- 我讀到的具體建議:組隊要有領域專家與技術人員;LLM 評分員的指令要簡單清楚、像寫給「一位稱職同事」;**避免資料污染**(用晚於模型訓練截止日的資料或自行合成);別把題目做得太易或太難;提防模型走你沒預期的捷徑。

> 這和本庫 [[llm-evals-how-to-know-ai-works]]、[[skill-evaluation-four-layer-checklist-google-qq]] 同一條線:**先確認評測量到的是你以為的東西**。「十項」是早報的說法,**我只確認文章確實是建議清單,不確認剛好十項**。

## 2. 其餘條目索引(**僅頻道標題,未核實**)

- **11/12:** 通義千問預告 Qwen4 預覽版;AlphaGenome 2;Nex-N2.6 開源;ERNIE 5.5 Flash Preview;Runway Praxis-1 權重;dots.tts.edit;DeepL Aure;Qwen Code 1.0 Preview;Antigravity Browser use;Gemini API Managed Agents 接自架 Linux 沙箱;Grok Bot 1.0;ChatGPT 桌面版 Finances;Gemini 上 CarPlay;Tabletop。
- **11/13:** Antigravity Orchestrator;**Jensen Huang 辭任 CEO(官方連結:NVIDIA 新聞稿)**;ChatGPT dot 自訂規則;Seedance 2.5 flash;豆包工作接第三方模型;**Claude Meetings**;Grok Bot Mac 版接七類 app;Inkling 2 Small 權重;**IBM LLMON 標記語言防提示注入**;OpenAI 兩款網路防禦工具;**Claude API 對話中途調 effort 的 Beta**;**Managed Agents 企業自架私測**;A2UI 1.0;Gemini 智慧眼鏡預購;五款 Flow 工具。
- **11/14:** ChatGPT Wallet(**官方頁 HTTP 403,未能讀,細節未核實**);混元 Hy Realtime;DeepSeek Harness 會話匯入插件;Antigravity Dynamic Workflows 與 Pro 開放 Orchestrator;AI Studio 領 Cloud 額度;Claude Code Projects 更新;Cognition 免費 SWE-2;GLM-5.3 額度;**Vercel Token Pass 月費 30 美元含 150 美元額度**;Claude Duet 研究預覽;Gemini 接 Wallet 理財洞察。
- **11/15:** Grok Bot 優化;**Claude Code 桌面版 mods 自訂主題**;Google 300 美元贈金不再覆蓋 Gemini 調用;**Claude always-on agents 指南**;**FBI 警告開源 AI 滲透工具 ARTEX 被武器化(說明欄無連結,未核實)**。
- **11/16:** 華為雲 openPangu-2.1-Pro;Agnes 2.5 Pro Theta 187.8B 多模態 MoE 開源;OpenCode Go 支援微信支付;OpenAI science blog 與 Standard Model 研究(arXiv 2610.09093);⭐ **「報道稱黃仁勳考慮重返 NVIDIA 擔任 CEO」**(出處 wccftech 與 Yahoo,我**抓不到原文**〔憑證驗證失敗〕,視為傳聞,見下)。
- **11/17:** ⭐ **阿里 Qwen4-Max「官方稱成本降 58%」**(qwen.ai 部落格是動態頁面,我用 curl 取不到內文,**58% 與其比較基準未能核實**,Mia 11/17 日報也講同一則,見存量);混元 Hy4 flash;Antigravity 上下文翻倍;**OpenAI 嵌入式評估**(外部機構審查安全);Seedance 2.5 4K API;書生-S2.1 Flash;Claude Code 適配 iPhone Duo 模擬器;Perplexity Monitor API;Google Ultra 5X 土耳其區漲價;DeepSeek 算力不足限流傳聞;ChatGPT for Healthcare;Gemini Notebook 變網站;Gemini 66 種地區語音;Hugging Face 與 OpenRouter;豆包工作台;**Claude Code 團隊談 AI 編程驗證方法**。

## 3. 這週的三條主線(我的整理,非頻道觀點)

1. **「做決定」從生成式呼叫裡被拆出來**:Gemini Decision 1 與前述 Jev 同型;Google 內部先拿去做路由、守門、挑 emoji,說明這類呼叫量大、延遲敏感。
2. **供應鏈與基礎設施在同一週出事故或穩定化**:Cursor/Fireworks 的外洩鏈、llama.cpp 與 ggml 宣告 API 穩定、Kitesurf 把瀏覽器拆成可自架的 Workers 元件。
3. **模型價格結構變細**:Hydrogen 的長上下文不分段單價、DeepSeek 的離峰半價與語音五折,都讓「成本估算」要看時段與限時活動。

## 4. 應用案例

1. **把低風險的「是非與分級」交給 Decisions 類 API:** 客服工單先過一個 `noul`(「是否提到退款」)再決定是否進 LLM;用 `confidence < 0.7` 轉人工。要先拿自己的 200 筆標註集測準確度與校準。
2. **用 llama.cpp 做桌面產品的人:** 現在可以把依賴釘在 `1.x`,升級時看 MAJOR;不再被 master 的 API 變動打斷。
3. **供應商外洩的防禦清單:** 追蹤與對話紀錄預設視為會外洩;給供應商的金鑰要限權限、限網路來源;客服信件不要貼憑證(Cursor 這次就有「使用者寄給客服的憑證」被取走)。
4. **成本估算:** DeepSeek 要分尖峰與離峰、語音限時價要在到期後重算;Hydrogen 的 1M 不加價適合整個 repo 一次餵,但輸出 token 單價($7.50)仍是大頭。

## 5. 核實總表

| 條目 | 結果 |
|---|---|
| Gemini Decision 1 的機制、價格、三題型、1,000 題、256K 輸入 | ✅ 官方文章 |
| 「近 5 倍便宜」、「領先且最低校準誤差」、Notebook「40% 低延遲」 | 官方自述,基準未讀、未獨立量測 |
| Gemini 4 Hydrogen 價格與 1M 單價、四個思考層級 | ✅ 官方文章 |
| AA 指數 51/50/54、Terminal-Bench 57% 對 18.2%、5 倍少虛構、Orchestrator 24%/19% | 官方自述,**未能核實** |
| DeepSeek 語音、OCR、搜尋價與離峰規則 | ✅ 官方定價頁 |
| 語音五折到期日 | 頁面沒寫,**未知** |
| llama.cpp v1.0.0 版本規則與發行管道 | ✅ 官方部落格;GitHub release 清單未讀 |
| Kitesurf 開源、Apache 2.0、Workers、CDP、元件 | ✅ 官方部落格;倉庫未 clone |
| Cursor 事件鏈、5,000 人、11 小時、0.01%/0.05% | ✅ 官方部落格(公司自述,無第三方核實) |
| Anthropic「10 項」建議 | 文章屬實,**「十項」計數未核實** |
| Qwen4-Max 成本降 58% | **未能核實**(頁面動態渲染) |
| ChatGPT Wallet | **未能核實**(官方頁 403) |
| 黃仁勳考慮重返 | **傳聞,未能核實**(原文抓不到);官方 11/17 財報稿由 Kress 以 interim CEO 署名,見 [[nvidia-ceo-exit-ecosystem-commitments-three-scenarios-why-qq]] |

## 相關筆記

- [[ai-morning-news-weekly-2026-11-05-to-11-10-juya]] — 上一份早報週報(含 Fireworks 事件的前半)
- [[system-one-models-jev-calibrated-decisions]] — Jev 的 noul / choice / score,與 Gemini Decision 1 同型
- [[gemini-4-argon-release-benchmarks-pricing]] — Gemini 4 Argon,與 Hydrogen 同代
- [[deepseek-search-fetch-api-agent-evidence]] — DeepSeek 搜尋與抓取 API
- [[claude-code-dont-ask-again-secrets-leak-checklist-why-qq]] — 機密外洩的排查清單,對照 Cursor 事件

## 來源

- 橘鸦 Juya 六支早報:`n9o9Tv2s0HQ`、`-xCz5oneKZ0`、`5Q89lUEYDWI`、`-v0xqIfR8Kw`、`eyxGH3TCUuY`、`67rZTbZnFqM`(只讀說明欄;範例:https://www.youtube.com/watch?v=n9o9Tv2s0HQ )
- Google〈Gemini Decisions API〉:https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/
- Google〈Introducing Gemini 4 Hydrogen〉:https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/
- DeepSeek API 定價:https://api-docs.deepseek.com/quick_start/pricing/
- ggml-org〈llama.cpp v1.0.0〉:https://huggingface.co/blog/ggml-org/llama-cpp-v1
- Cloudflare〈Kitesurf is now open source〉:https://blog.cloudflare.com/kitesurf-open-source/
- Cursor〈An update on our recent security incident〉:https://cursor.com/blog/security-incident-update
- Anthropic〈Building strong safety evaluations〉:https://anthropic.com/research/building-strong-safety-evaluations
- 未能讀到:OpenAI ChatGPT Wallet(403)、qwen.ai Qwen4-Max(動態頁)、wccftech 黃仁勳重返報導(憑證錯誤)
