# GitHub Weekly 第 101 期:開源版 Cowork、資料工程實戰課、瀏覽器 MCP 與專業設計 Agent Skill

> **期數:** #101(2026/01/18–01/24)
> **本期主題:** 開源版 Cowork 多代理桌面應用、資料工程實戰訓練營、瀏覽器 MCP、專業 UI/UX 設計 Agent Skill,以及無程式碼的 galgame 引擎。
> 來源:itcoffee66/githubweekly 第 101 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **Githubweekly** | IT 咖啡館自家的「一週熱點」文字版倉庫 | 開源資源/週報 |
| 2 | **Eigent** | 自稱全球首個多代理工作流的桌面 App"(開源版 Cowork)" | 多代理桌面應用 |
| 3 | **data-engineering-zoomcamp** | DataTalks 社群維護的資料工程實戰訓練營 | 資料工程/教學 |
| 4 | **chrome-devtools-mcp** | 讓 AI 助手控制真實 Chrome 的瀏覽器 MCP server | MCP/自動化 |
| 5 | **ui-ux-pro-max-skill** | 替 AI 注入專業 UI/UX 設計知識的 Agent Skill | Agent Skill/設計 |
| 6 | **VoidNovelEngine** | 流程圖節點式、無程式碼的視覺小說"(galgame)"引擎 | 遊戲引擎 |

---

## 1. Githubweekly — IT 咖啡館自家的「一週熱點」文字版倉庫

- **連結:** <https://github.com/itcoffee66/githubweekly>
- **用途:** 把「GitHub 一週熱點」每一期的 **文字版內容** 集中發布到一個 GitHub 倉庫,方便想看文字版(而非只看影片)的讀者閱讀與檢索。
- **亮點:**
  - 作者(IT 咖啡館)自己的專案,每期文字內容會陸續補齊放進倉庫。
  - 放在 GitHub 的額外好處:想 **提建議或投稿專案** 的人可以直接開 Issue。
  - 製作流程正在嘗試用 **AI 工作流** 自動化,後續規劃靜態頁等延伸內容。

> **應用案例:** 你在通勤時用影片看過某一期週報,事後想找回某個專案的連結或名稱——直接到這個倉庫用關鍵字搜尋對應期數的 Markdown,比在影片裡來回拖拉快得多;若你自己做了不錯的開源專案,也能直接在這裡開 Issue 投稿給作者。

## 2. Eigent — 自稱全球首個多代理工作流的桌面 App(開源版 Cowork)

- **連結:** <https://github.com/eigent-ai/eigent>
- **用途:** 一款 **多代理(multi-agent)工作流桌面應用**,定位為「開源版 Cowork」,幫你建立、管理並部署客製化的 AI 工作團隊,把最複雜的工作流程轉成自動化任務。
- **亮點:**
  - 基於 **CAMEL-AI 多代理框架** 構建,透過並行調度多個專責 agent 協同完成跨步驟任務。
  - 內建多個現成代理:**開發代理**(寫並執行程式碼、跑終端機指令)、**搜尋代理**(搜網頁並擷取內容)、**文件代理**(建立與管理文件)、**多模態代理**(處理影像與音訊)。
  - 提供 **可自託管部署版、雲端版與企業版**(企業版應是為後續變現鋪路)。
  - 模型可用 **線上 API**,也可用 **本地模型**。
  - 同類「開源 Cowork」中熱度較高的還有 openwork、AionUI,而 Eigent 的 star 數最多。

> **應用案例:** 你要做一份競品調查報告——讓搜尋代理上網蒐集資料、文件代理整理成 Markdown、開發代理順手寫個小腳本把數據畫成圖表,多個 agent 並行跑完整條流程,而不必自己在不同工具間手動搬運。

## 3. data-engineering-zoomcamp — DataTalks 社群的資料工程實戰訓練營

- **連結:** <https://github.com/DataTalksClub/data-engineering-zoomcamp>
- **用途:** 由 **DataTalks 社群** 維護的開源資料工程訓練營,是一套完整的「學習專案 + 線上課程教材」,內容涵蓋 **從基礎工具到生產級資料管道設計** 的全流程教學、程式碼範例與實作任務。
- **亮點:**
  - 課程共 **9 週**,分為 **6 大模組 + 1 個 final project**,每個模組都有大量影片。
  - 目標是讓你掌握打造真實世界資料工程系統所需的核心技能。
  - 先備條件:具備基本程式設計經驗(最好是 **Python**),並熟悉 **SQL**。
  - 適合想進入資料工程領域的初學者。

> **應用案例:** 一位會寫一點 Python、也懂基本 SQL 的後端工程師想轉資料工程——照著這套訓練營從 Docker、資料倉儲、批次/串流管道一路做到 final project,九週下來就有一個能放進作品集的端到端資料管道專案。

## 4. chrome-devtools-mcp — 讓 AI 助手控制真實 Chrome 的瀏覽器 MCP

- **連結:** <https://github.com/ChromeDevTools/chrome-devtools-mcp>
- **用途:** 一個開源的 **MCP server**,專為支援 MCP 的 AI 編程助手(Claude、Cursor、Copilot、Gemini CLI、Cline 等)提供 **對真實 Chrome 瀏覽器實例的存取與控制能力**。
- **亮點:**
  - 讓 agent 不只會產生程式碼,還能 **啟動 Chrome、導航頁面、除錯、抓取效能數據、分析網路/主控台資訊**,達成更可靠的自動化、除錯與效能優化。
  - 相較於 Playwright MCP,**可以很方便地保留登入資訊**,在許多除錯與 AI 自動化場景中省事很多。
  - 支援的功能也較為齊全。
  - 適合 **前端開發者、效能工程師、程式碼/測試自動化以及 CI/CD**。

> **應用案例:** 你叫 AI 助手「打數登入後台、量測首頁載入效能、把 Lighthouse 報告整理出來」——透過此 MCP,agent 能沿用既有登入狀態打開真實 Chrome,跑完導航與效能擷取,直接回報哪幾個資源拖慢了 LCP,而不必你手動操作 DevTools。

## 5. ui-ux-pro-max-skill — 替 AI 注入專業 UI/UX 設計知識的 Agent Skill

- **連結:** <https://github.com/nextlevelbuilder/ui-ux-pro-max-skill>
- **用途:** 一個面向 AI 編程助手(Claude Code、Cursor、Windsurf、Copilot、OpenCode 等)的開源 **設計智慧庫(Agent Skill)**,本質是「結構化設計知識庫 + 設計系統生成引擎」,在 AI 接到 UI/UX 任務時 **自動注入背景知識與規範**,讓產出的介面更專業、更符合 UI/UX 實務標準。
- **亮點:**
  - 內含大量設計資產:**67 個 UI 樣式、96 種配色方案、56 種字體搭配、100 條產業特定推理規則** 等。
  - 安裝彈性:可用自帶的 CLI 工具,或手動安裝。
  - 使用時只要說「開發什麼內容」(例如做寵物食品的 landing page),它會自動推理、搜尋方案資訊、挑選合適設計方案,最終給出 **一整套系統化的風格設計**。
  - 若安裝的 skill 較多、擔心衝突,可 **指定使用此技能** 來完成任務。
  - 對解決「AI 寫出來的 UI 太有 AI 味」很有幫助,也適合對設計不熟的人藉此理解 vibe coding。

> **應用案例:** 你想做一個寵物食品品牌的 landing page,但對配色與排版毫無頭緒——讓 AI 助手帶上這個 skill,它會自動挑出契合品牌調性的配色、字體與版面規則,輸出一份成系統的設計與程式碼建議,而不是隨手堆一些樣式。

## 6. VoidNovelEngine — 流程圖節點式、無程式碼的視覺小說(galgame)引擎

- **連結:** <https://github.com/VoidmatrixHeathcliff/VoidNovelEngine>
- **用途:** 一款專為現代 **視覺小說與敘事遊戲** 開發者打造的開源引擎,可用來開發 galgame 等作品。
- **亮點:**
  - 採 **無程式碼開發範式**:用 **流程圖式的節點編輯**,以拖拽、連接節點來建構完整的遊戲邏輯、分支對話與演出流程,開發過程像畫心智圖一樣自然。
  - 設計思路與 galgame 創作邏輯高度契合。
  - 提供大量開箱即用的 **專用節點**(對話、選項、轉場、角色控制等)。
  - 可直接從 release 下載打包好的 **二進位版本**,並附有相對詳細的文件。
  - 搭配 AI 生成素材已大幅便利,可讓 galgame 開發更容易上手。

> **應用案例:** 一位不會寫程式的同人作者想做一款帶分支結局的戀愛 galgame——用 VoidNovelEngine 拖拉節點就能排好「對話 → 選項 → 不同好感度走向不同結局」的劇情流程,素材用 AI 生成,不必去硬啃晦澀的腳本語言。

---

## 額外資源(Bonus)

本期另分享兩份報告:

- **《「情緒療癒」消費市場趨勢盤點》** — 從市場角度分析情緒療癒消費,呼應「現代人隱性情緒問題」這個值得關注的方向(作者先前也聊過情緒問題與 AI 結合的思考)。
- **《AI 智慧體聖經》** — CB Insights 發布,分析超過 **500 家以上的 AI agent 新創公司**,給出 2026 年的趨勢分析與洞察,協助企業制定自己的 AI agent 策略。

> 作者另以夸克網盤分享「一週熱點 101 期」打包資料:<https://pan.quark.cn/s/015fd96302ba>

---

## 一句話總結

> 本期主軸是「**讓 AI agent 更會做事、也讓人更好上手**」:Eigent 把多代理工作流搬上桌面、chrome-devtools-mcp 讓 agent 操控真實瀏覽器、ui-ux-pro-max-skill 替 AI 補上專業設計知識;另有資料工程訓練營(data-engineering-zoomcamp)、無程式碼遊戲引擎(VoidNovelEngine),以及 IT 咖啡館自家的文字版週報倉庫(Githubweekly)。

---

## 來源

- [GitHub Weekly 第 101 期原文](https://github.com/itcoffee66/githubweekly/blob/main/_weekly/101.md)
- [itcoffee66/githubweekly(週報倉庫)](https://github.com/itcoffee66/githubweekly)
- 各專案連結見上文各節。
