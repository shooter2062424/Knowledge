# GitHub Weekly 第 114 期:DeepSeek V4 終端編程 Agent、金融領域 Agent 集合與開源電子簽

> **期數:** #114(2026/05/10–05/16)
> **本期主題:** 為 DeepSeek V4 打造的終端編程 Agent、Anthropic 的金融領域 Agent 集合、開源版電子簽、給新手的 vibe coding 入門課,以及 3D 高斯 Splat 線上編輯器。
> 來源:itcoffee66/githubweekly 第 114 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **DeepSeek-TUI** | 為 DeepSeek V4 量身打造的終端編程 Agent | AI 程式工具 |
| 2 | **financial-services** | Anthropic 開放的金融領域 Agent 集合 | 金融 AI Agent |
| 3 | **DocuSeal** | 對標 DocuSign 的開源電子簽平台 | 文件/協作工具 |
| 4 | **easy-vibe** | 給新手的 vibe coding 入門課 | AI 學習資源 |
| 5 | **SuperSplat** | 瀏覽器內的 3D 高斯 Splat 線上編輯器 | 3D/電腦視覺 |

---

## 1. DeepSeek-TUI — 為 DeepSeek V4 量身打造的終端編程 Agent

- **連結:** <https://github.com/Hmbown/DeepSeek-TUI>
- **用途:** 一個專為 DeepSeek V4 打造的終端編程 Agent(coding agent)。注意它**不是 DeepSeek 官方產品**,而是個人開發者基於 DeepSeek V4 開發的第三方工具,填補了 DeepSeek 一直缺乏對應 coding agent 的空缺。
- **亮點:**
  - 開發者是一位叫 **Hunter Bown** 的美國人,宣傳時還特地把推文翻成中文向「鯨魚兄弟」(DeepSeek 社群)求助,因此爆紅。
  - 安裝方式多元:**npm、cargo、brew、docker** 都支援;會用 Claude Code 大致就能上手。
  - **Auto Mode 是最有意思的設計**:先用 `deepseek-v4-flash` 判斷任務該用哪個模型——簡單任務用 flash 省錢,複雜任務才調用更強的 `deepseek-v4-pro`。
  - 生態定位類比:GPT 有 Codex、Claude 有 Claude Code、國內也有 qwencode / kimicode / Kcode,DeepSeek 終於補上這塊。
  - 目前 issue 區仍有不少待解問題,屬中規中矩、尚需時間驗證的早期專案,不宜盲目追捧。

> **應用案例:** 你平常用 DeepSeek V4 寫程式但只能在網頁/聊天框複製貼上,效率低。裝上 DeepSeek-TUI 後,直接在終端機讓 Agent 讀 repo、改檔、跑指令;開啟 Auto Mode 後,問它「幫我重構這個函式」這種簡單任務自動走便宜的 flash 模型,遇到「跨多檔重構整個模組」才升級到 pro,兼顧成本與效果。

## 2. financial-services — Anthropic 開放的金融領域 Agent 集合

- **連結:** <https://github.com/anthropics/financial-services>
- **用途:** Anthropic 近期開放的金融領域 Agent 集合,涵蓋最常見的金融服務工作流程——**投資銀行、股票研究、私募股權、財富管理**。
- **亮點:**
  - 切入點明確:金融業有大量**可結構化的認知勞動**(需要理解上下文、但非創意工作),恰好落在 Agent 最擅長的區間。
  - 覆蓋場景典型:投行的推銷 Agent、會議準備 Agent;研究端的市場研究、財報評審;以及基金管理、財務對帳、KYC 審核。
  - 每個 agent 內含一份 **prompt、skill 和 connector**;可在 **Claude Cowork** 裡安裝,或走 **Claude Managed Agents API**。
  - 形象比喻:以前你買的是一個 Excel,現在 Anthropic 直接給你一整套投行分析師常用模板,還把資料連接器與工作流也接好了——代表 Anthropic 不再只做大模型,也開始下場做「行業工作方法」。
  - 門檻其實不低:很多價值建立在**真實金融數據與內部流程**之上,一般開發者拿來直接玩體驗未必好。

> **應用案例:** 一家私募基金想用 AI 加速盡職調查(due diligence)。直接套用集合裡的「財報評審」與「市場研究」agent,把目標公司的財報與產業資料接進 connector,讓 agent 產出初步分析草稿與重點提問清單,分析師再在此基礎上深入,而不必從零搭流程。

## 3. DocuSeal — 對標 DocuSign 的開源電子簽平台

- **連結:** <https://github.com/docusealco/docuseal>
- **用途:** 一個開源平台,提供安全高效的數位文件簽署與處理,**直接對標 DocuSign**。一句話:嫌 DocuSign 太貴、太重、太「企業味」,就可以看看它。
- **亮點:**
  - 核心很直接:線上建立、填寫、簽署 PDF 文件。
  - 支援**多提交人、Email 通知、儲存到 S3 / Azure / Google Cloud、API / Webhook 整合**,還能自部署。
  - 安裝可直接用官方 docker 映像檔,或先試用線上平台了解功能。
  - 專業功能齊全:公司徽標與白標(white-label)、使用者角色、自動提醒、透過簡訊邀請與身分驗證等。
  - 價值在於「簡化流程、保留關鍵能力」——很多公司真正需要的只是把「發合約、填欄位、簽字、歸檔」這件事順利跑完,對中小團隊已很夠用。

> **應用案例:** 一家 30 人的新創覺得 DocuSign 月費太貴,於是用 docker 自部署 DocuSeal。HR 把僱傭合約做成模板、設好待填欄位,系統自動發 Email 給新員工簽署,簽完歸檔並存到自家 S3;整條入職簽約流程不再依賴付費 SaaS,資料也留在自己手上。

## 4. easy-vibe — 給新手的 vibe coding 入門課

- **連結:** <https://github.com/datawhalechina/easy-vibe>
- **用途:** datawhale 社群出品的 **vibe coding 入門課程**。它不教你某個框架怎麼寫,而是教你**怎麼和 AI 一起把應用做出來**——更像一份「會說話就能開始做應用」的學習地圖。
- **亮點:**
  - 最強之處是把抽象概念做得**特別可視化**:step-by-step 教學、模擬 IDE 互動、RAG 流程演示、終端概念可視化,連 AI 生成圖片都做了動畫講解。
  - 可理解為「程式新手友善版的互動教材」,讓你邊看、邊點、邊試,而不是硬啃概念。
  - 切中痛點:很多人嘴上說 vibe coding,但真正的新手連環境、IDE、終端、Git、Prompt 都搞不定,一直卡在第一步。
  - 比起長篇大論的課程,更適合零基礎的人入門 AI 編程。

> **應用案例:** 一位完全不懂程式的設計師想試著用 AI 做個小工具,但連「終端機」「Git」是什麼都不懂。從 easy-vibe 的互動教材開始,先看終端概念可視化、再跟著模擬 IDE 一步步操作,搭配 RAG 流程演示理解 AI 怎麼讀資料,幾天後就能在 AI 協助下做出第一個能跑的小應用。

## 5. SuperSplat — 瀏覽器內的 3D 高斯 Splat 線上編輯器

- **連結:** <https://github.com/playcanvas/supersplat>
- **用途:** 一個 3D 高斯 Splat(Gaussian Splat)編輯器,讓你**在瀏覽器裡直接檢視、編輯、最佳化與發布 3D Gaussian Splats**,免下載安裝、打開網頁就能用。
- **亮點:**
  - Gaussian Splat 可理解為「把現實世界拍成一堆高品質光點、再拼成 3D 場景」的技術——看起來像點雲又像體素,但視覺更真實,成本又比傳統高模型低。
  - SuperSplat 就像這個領域的「線上 PS」,專門處理這些 3D splat 資產。
  - 由 **PlayCanvas 團隊**打造,走典型 Web 技術路線。
  - 優勢在於瀏覽器即開即用,適合**演示、迭代、分享與快速試錯**;不必是 3D 開發者也能進去玩。

> **應用案例:** 一個房仲團隊用手機把樣品屋拍成一段環繞影片,經由 Gaussian Splat 工具轉成 3D splat 後,丟進 SuperSplat 的網頁編輯器裁掉雜物、最佳化光點密度,再一鍵發布成可在瀏覽器旋轉檢視的 3D 看房場景連結,直接傳給客戶,全程不裝任何軟體。

---

## 額外資源(Bonus)

本期另分享兩份資料:

- **《AI Token 經濟學與推理利潤入門指南》** — 拆解 AI 的「Token 經濟學」:為何不同模型、不同模態的推理利潤差距巨大。重點分析 **Z.ai 與 Minimax** 的推理成本、Token 定價、KV Cache、GPU 利用率等。
- **《中國人工智慧系列白皮書:具身智慧》** — 適逢特斯拉 Optimus(擎天柱)準備量產,具身智慧(embodied AI)關注度持續升高,可先了解內容。

---

## 一句話總結

> 本期的主軸是「**讓 AI 落地各行各業**」:DeepSeek-TUI 補上 DeepSeek 的 coding agent 空缺、financial-services 把 Agent 帶進金融專業工作流;DocuSeal 與 easy-vibe 分別降低電子簽與 AI 編程的門檻,SuperSplat 則代表 3D 內容形態的 Web 化前沿。

---

## 來源

- [GitHub Weekly 第 114 期原文](https://github.com/itcoffee66/githubweekly/blob/main/_weekly/114.md)
- [itcoffee66/githubweekly(週報倉庫)](https://github.com/itcoffee66/githubweekly)
- 各專案連結見上文各節。
