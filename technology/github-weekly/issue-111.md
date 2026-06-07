# GitHub Weekly 第 111 期:Karpathy 經驗的 Claude Code 設定、AI Agent 協作平台與新一代 TTS

> **期數:** #111(2026/04/08–04/14)
> **本期主題:** Karpathy 踩坑經驗提煉的 Claude Code 設定檔、把 AI Agent 變成隊友的協作平台、Tokenizer-Free 的新一代 TTS 模型、微軟的萬能文件轉 Markdown 工具,以及 Shopify 創辦人做的輕量本地搜尋引擎。
> 來源:itcoffee66/githubweekly 第 111 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **andrej-karpathy-skills** | 從 Karpathy 用 LLM 寫程式的經驗提煉出的 Claude Code 設定檔 | AI 程式工具 |
| 2 | **Multica** | 把 AI Agent 當隊友派活、追蹤進度的開源託管平台 | AI Agent 編排 |
| 3 | **VoxCPM2** | "Tokenizer-Free" 直接在連續語音空間建模的新一代 TTS | 語音合成/TTS |
| 4 | **MarkItDown** | 微軟出品、把各種檔案轉成 Markdown 的萬能工具 | 文件處理 |
| 5 | **QMD** | Shopify 創辦人做的本地 CLI 搜尋引擎(BM25+向量+重排序) | 本地搜尋 |

---

## 1. andrej-karpathy-skills — Karpathy 經驗提煉的 Claude Code 設定

- **連結:** <https://github.com/forrestchang/andrej-karpathy-skills>
- **用途:** 說白了就是一個 `CLAUDE.md` 檔案,但它是從 **Andrej Karpathy** 長期用 LLM 寫程式的踩坑經驗提煉而來。Karpathy 曾任特斯拉 AI 總監、早期 OpenAI 成員,擅長把複雜 AI 技術講得通俗易懂。他曾吐槽 AI 編程助手最讓人頭疼的問題:模型擅自做假設、不問清楚就開幹、寫一堆不需要的「彈性」程式碼、還喜歡順手改你的其他程式碼。
- **亮點(四條核心原則):**
  - **先想再寫** — 不確定就問,有更簡單的方案就說出來。
  - **簡潔第一** — 不要亂寫沒用的東西。
  - **精準手術** — 只改該改的程式碼,別動其他地方。
  - **目標驅動** — 任務拆成可驗證的小步驟,每一步都有明確完成標準。
  - 可安裝成全域 skill,或只下載單獨的 `CLAUDE.md` 放到專案;專案特殊需求可加進 **Project-Specific** 區段。
  - 約 31.2k stars。雖然是寫給 Claude Code,但對所有 AI 編程助手都適用。

> **應用案例:** 你用 Claude Code 改一個 bug,模型卻順手「優化」了三個無關函式、還加了你沒要的設定選項。把這份 `CLAUDE.md` 複製到專案根目錄後,模型會先確認需求、只動該動的程式碼,行為品質明顯提升。可當作 superpowers 這類成熟 skill 的補充與思路參考。

## 2. Multica — 把 AI Agent 變成真正的隊友

- **連結:** <https://github.com/multica-ai/multica>
- **用途:** 開源的託管 agent 平台,slogan 是「你未來的 10 個新同事不會是人類」。目前大多數人用 Claude Code、Codex、OpenClaw 都是在那兒跟 Agent 對話、複製貼上 prompt、盯著輸出看;Multica 則讓你 **像給同事派活一樣給 Agent 分配任務**:透過統一看板調度,Agent 自己接活、寫程式、卡住主動回報 bug、完成後更新狀態。
- **亮點:**
  - 支援目前主流各種 Agent 工具。
  - 安裝簡單:macOS / Linux 直接 `brew install`,Windows 也有一鍵安裝腳本;裝完 `multica setup` 設定後即可在網頁使用。
  - **技能積累**:每次 Agent 解決一個問題,解決方案會變成可複用的技能,整個團隊都能用 — 你的 Agent 團隊越用越強(但目前階段尚未完全成熟)。
  - 類似專案有 Paperclip、vibekanban 等,專案內也列出對比。

> **應用案例:** 你是一人公司的獨立開發者,手上同時有「修登入 bug」「補測試」「更新文件」三件事。在 Multica 看板上把三張卡分別指派給不同 Agent,牠們各自開工、卡住自己回報,你只需看板上巡視進度,而不必同時開三個終端機輪流貼 prompt。對重度 AI 開發者很實用;若非重度使用者,這套方案可能暫時偏重。

## 3. VoxCPM2 — Tokenizer-Free 的新一代 TTS 模型

- **連結:** <https://github.com/OpenBMB/VoxCPM>
- **用途:** 面壁智能 × 清華大學聯合研發、OpenBMB 社群開源的新一代 **TTS(文字轉語音)模型**,主打關鍵詞 **"Tokenizer-Free"**:不再走傳統「文字 → token → 聲音」流程,而是直接在 **連續語音空間建模**,從根本解決語音合成的「機械感」與表達力不足。
- **亮點:**
  - 最新升級的 VoxCPM2 基於 [MiniCPM-4](https://github.com/OpenBMB/MiniCPM) 基座構建,總計 **20 億參數**,在超過 **200 萬小時** 多語種音訊上訓練,支援 **30 種全球語言**。
  - 具備 **上下文感知語音生成、零樣本語音克隆、連續語音建模** 能力;可用文字描述設計音色,並能在 **消費級顯卡** 上運行。
  - 在公開的零樣本與可控 TTS 基準測試取得 **SOTA** 結果,並公開技術資料。
  - 可直接在 Hugging Face demo 體驗;本地安裝相對簡單,專案附 web demo。目前尚未支援 Mac 推理加速(只能跑 CPU)。

> **應用案例:** 你要做一個有聲書或播客旁白,想要某位特定講者的音色又不想花錢請配音。用 VoxCPM2 的零樣本語音克隆,丟入幾秒參考音訊即可生成該音色的長段朗讀;若想要全新音色,直接用文字描述「沉穩、低沉、略帶磁性的男聲」也能合成,且整套能在自己的消費級顯卡上跑。

## 4. MarkItDown — 微軟的萬能文件轉 Markdown 工具

- **連結:** <https://github.com/microsoft/markitdown>
- **用途:** 來自微軟 **AutoGen 團隊** 的全能文件轉換工具,做的事情非常聚焦:**把各種檔案格式轉成 Markdown**。PDF、Word、Excel、PowerPoint、圖片、音訊、HTML、EPUB、YouTube 連結……基本上你想得到的格式都支援。
- **亮點:**
  - 為什麼要轉 Markdown?主流大模型都非常依賴 Markdown,用 Markdown 餵給它們效果最好、**token 消耗也最省**;這工具等於打通「你的檔案」與「AI 能理解的內容」之間的橋樑。
  - 安裝需 **Python 3.10 以上**,clone 專案後 `pip install -e` 裝依賴;一行命令即可用:`markitdown 檔名.pdf`,輸出乾淨的 Markdown。
  - 支援 **圖片 OCR、音訊轉文字、YouTube 字幕提取**。
  - 最近更新提供 **MCP Server**,可輕鬆和 Claude Code 等 AI 工具整合;另有 **VS Code 外掛**,右鍵點一下就能轉。
  - 約 10.8 萬 stars。

> **應用案例:** 你要做一個 RAG 知識庫,手上有上百份 PDF 合約與 PowerPoint 簡報。用 `markitdown` 批次把它們轉成乾淨 Markdown 再切塊嵌入,比直接塞 PDF 更省 token、檢索品質也更好;若再掛上 MCP Server,Claude Code 就能直接呼叫它把某份檔案轉文字後接著分析。

## 5. QMD — Shopify 創辦人做的輕量本地搜尋引擎

- **連結:** <https://github.com/tobi/qmd>
- **用途:** 一個 **完全在本地運行的 CLI 搜尋引擎**,專門用來搜尋你的 Markdown 文件、知識庫、會議記錄。它結合 **BM25 關鍵詞搜尋、向量語義搜尋與 LLM 重排序** 三路技術,全部跑在本地。
- **亮點:**
  - 作者是 **Tobi Lütke**(Shopify 創辦人兼 CEO):他平時用大量 Markdown 記筆記、會議紀要與文件,找不到東西時乾脆自己造了 QMD。
  - 最近爆紅的助推者是 **OpenClaw** — 其記憶模組預設的本地搜尋引擎就是 QMD(開啟進階搜尋會用到)。
  - 上手容易:`npm install` 安裝 → 加入要索引的目錄 → 生成 embeddings → 即可搜尋;支援關鍵詞、語義、以及混合 + 重排序的 query 模式。
  - 提供 **MCP Server**,可與 Claude Desktop、Claude Code 整合。約 2.1 萬 stars。

> **應用案例:** 你像本知識庫這樣累積了幾百篇 Markdown 筆記,想找「上週某場會議講到的某個決議」卻記不清關鍵詞。用 QMD 的混合模式做語義搜尋,即使下的詞和原文用字不同也能命中相關段落,再經 LLM 重排序把最相關的結果頂到最前面 — 體現了「AI 時代每個人都需要一個給自己的搜尋引擎」的理念。

---

## 額外資源(Bonus)

本期另分享兩份報告:

- **《具身智慧數據行業研究白皮書》** — 具身智慧是人工智慧與機器人技術交叉融合的前沿,被視為實現 AGI 的一種期許;看得到的是機械,看不到的背後則需大量數據訓練。
- **《2026 年輕人智慧家電消費洞察》** — B 站與益普索(Ipsos)合作出品,觀察年輕人更主動、更精明、追求品質與個性的消費結構變革,以及智慧家電的消費現況。

---

## 一句話總結

> 本期主軸圍繞「**讓 AI 更好用、更省、更能接活**」:andrej-karpathy-skills 用一份 `CLAUDE.md` 馴服編程助手、Multica 把 Agent 變成可派活的隊友;VoxCPM2 在語音合成端做 Tokenizer-Free 突破;MarkItDown 與 QMD 則分屬「把檔案餵給 AI」與「在本地把內容找回來」兩端的實用基礎建設。

---

## 來源

- [GitHub Weekly 第 111 期原文](https://github.com/itcoffee66/githubweekly/blob/main/_weekly/111.md)
- [itcoffee66/githubweekly(週報倉庫)](https://github.com/itcoffee66/githubweekly)
- 各專案連結見上文各節。
