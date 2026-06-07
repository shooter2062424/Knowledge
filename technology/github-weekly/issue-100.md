# GitHub Weekly 第 100 期:開源程式 Agent、AI 技能框架與電腦操作 Agent

> **期數:** #100(2025/12/29–2026/01/03)
> **本期主題:** 開源 AI 編程代理、AI 開發技能框架、自動操作電腦的 GUI Agent、深度研究 Agent,以及 iCloud 照片下載與微信公眾號文章導出兩款內容備份工具。
> 來源:itcoffee66/githubweekly 第 100 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **opencode** | 不綁定單一模型廠商的開源 AI 編程代理 | AI 程式工具 |
| 2 | **Superpowers** | 給程式 Agent 植入「資深工程師工作流」的技能框架 | AI 開發工作流 |
| 3 | **TARS** | 字節跳動開源、用 VLM 操作電腦的多模態 GUI Agent | 電腦操作 Agent |
| 4 | **MiroThinker** | 主打「深度交互 Scaling」的開源深度研究 Agent | 深度研究 Agent |
| 5 | **icloud_photos_downloader** | 跨平台批次下載 iCloud 照片影片的 CLI | 備份/下載工具 |
| 6 | **wechat-article-exporter** | 把微信公眾號文章導出成 Markdown/HTML/PDF | 內容導出工具 |

---

## 1. opencode — 不被單一廠商鎖定的開源 AI 編程代理

- **連結:** <https://github.com/anomalyco/opencode>
- **用途:** 開源的 AI 編程代理,產品定位直接對標 Claude Code,但走「完全開放」路線——**不綁定任何一家大模型供應商**,可同時接 Claude、OpenAI、Google 模型甚至本地模型。
- **亮點:**
  - 支援 **75+ 個模型來源**,對不想被單一 API 或閉源服務鎖定的使用者非常友善。
  - 除了終端機 TUI,還有 **Desktop 應用(Beta)** 與 **IDE 插件**(如 VS Code 整合)。
  - 可為同一個專案 **同時啟動多個 Agent 並行執行任務**。
  - 熱度暴漲與「Claude 封號事件」有關:Claude 封掉一批透過 OpenCode 等第三方調用 Claude Code 訂閱套餐的通道,反而把 opencode 推上風口;OpenAI 的 Codex 隨即宣布支援 OpenCode,opencode 也光速推出 ChatGPT Plus 接入——「敵人的敵人就是朋友」的一波商戰。

> **應用案例:** 假設你同時訂閱了 Claude、ChatGPT Plus 與 Google 的模型,想避免被任一家鎖死。
> 用 opencode 搭配 `oh-my-opencode` 之類的插件,就能把「御三家」的模型組合在一起完成開發:
> 例如用某家模型負責規劃、另一家負責寫程式碼、第三家負責 code review,任一通道被封還能立刻切換。

## 2. Superpowers — 給 AI 編程代理植入「資深工程師工作流」

- **連結:** <https://github.com/obra/superpowers>
- **用途:** 一套 **AI 編程代理的擴展工作流系統**,為 Claude Code / Codex / OpenCode 等智能編程助手提供完整的軟體工程實時技能庫與工作流程,強行讓 AI「按規矩辦事」。
- **亮點:**
  - 主要是為 **Claude Code 設計的插件**,可直接透過 marketplace 安裝;Codex / OpenCode 需手動安裝,但現在直接叫 AI「取得並依指令安裝」即可。
  - 內建可見指令:**brainstorm、write-plan、execute-plan**。
  - 底層由 **多個 agent skill** 組成,正好是當前最火的 skill 概念的優質學習範例。
  - 解決大型專案中 AI 表現不穩定的痛點——先對齊需求、再產出開發基準文件、最後才實作。

> **應用案例:** 在一個大型專案中丟出新需求後,Superpowers 會自動觸發 brainstorm 技能,
> 像一位經驗豐富的架構師先透過多輪問答與你對齊需求,接著生成一份盡量詳細的開發基準文件,
> 最後才開始寫程式碼——避免 AI 一聽到需求就埋頭亂寫、半路才發現方向錯誤。

## 3. TARS — 字節跳動開源的多模態電腦操作 Agent

- **連結:** <https://github.com/bytedance/UI-TARS-desktop>
- **用途:** 字節跳動開源的 **多模態 AI Agent Stack**,讓 AI 用視覺語言模型(VLM)理解並操作電腦圖形介面(GUI)。
- **亮點:**
  - 實際包含 **兩個專案**:**Agent TARS** 提供基本能力,把 GUI Agent 與 Vision 能力帶進終端、電腦、瀏覽器與產品,提供命令列與網頁兩種介面。
  - **UI-TARS Desktop** 則是由 UI-TARS 與 **Seed-1.5-VL / 1.6 系列模型** 驅動的原生 GUI agent。
  - 可用 **自然語言命令(中文/英文)** 讓 AI 模擬滑鼠/鍵盤操作,在桌面應用、瀏覽器等環境完成任務。
  - 被視為 2026 年各大廠商的重點發力方向,目前主要瓶頸仍在操作的速度、準確性與穩定性。

> **應用案例:** 想讓 AI 自動完成「打開瀏覽器 → 登入某網站 → 填表單 → 截圖存檔」這種沒有 API 的純 GUI 流程,
> 只要用中文下指令,UI-TARS Desktop 就能靠視覺辨識界面元素並模擬點擊與輸入,
> 類似豆包電腦/豆包手機那種「AI 自主操作裝置」的體驗,但是開源、可自部署。

## 4. MiroThinker — 主打「深度交互 Scaling」的開源深度研究 Agent

- **連結:** <https://github.com/MiroMindAI/MiroThinker>
- **用途:** 由 MiroMindAI 維護的 **開源深度研究代理(open-source search agent model)**,目標是打造能做「工具增強推理 + 複雜現實世界資訊檢索」的 AI 模型,在類似 Deep Research 的任務上表現更強。
- **亮點:**
  - **MiroThinker 1.5** 提出 **「深度交互 Scaling」** 概念:不再卷參數,而是讓代理在環境中「試錯 + 反思」,模擬人類處理複雜問題的方式。
  - 隨著與環境互動的深度與頻率提升,效能在多個 benchmark 上呈可預測的提升,刷新開源代理紀錄。
  - **235B 規模** 跑出全球第一梯隊表現;**30B 版本** 以 **1/20 的推理成本** 對標萬億參數模型。
  - 官方宣稱曾成功預測 Polymarket 題目、A 股漲停板與 GTA 6 發布趨勢。

> **應用案例:** 給它一個開放式研究題目,例如「整理某新技術近一年的關鍵進展與爭議」,
> 它不會只做一次檢索就交差,而是反覆「搜尋 → 讀取 → 反思 → 再搜尋」,
> 在多輪與環境互動中逐步逼近答案——適合需要跨來源交叉驗證的深度調研任務。

## 5. icloud_photos_downloader — 跨平台 iCloud 照片下載工具

- **連結:** <https://github.com/icloud-photos-downloader/icloud_photos_downloader>
- **用途:** 社群維護的 **跨平台命令列工具**,把 iCloud 照片庫裡的全部照片與影片下載到本地(支援 Linux、Windows、macOS,甚至 NAS),適合做 **備份、遷移或定期同步**。
- **亮點:**
  - 直接透過 Apple 雲端介面取檔,而非靠 iCloud Drive 同步。
  - 支援 **Copy、sync、move** 多種操作模式,並提供 **自動去重** 與 **斷點檢查** 能力。
  - 以 Python 撰寫,可在 release 頁下載安裝包,或透過 **pip、Docker、Homebrew** 安裝。
  - 使用前需在 iPhone/iPad 開啟「Access iCloud Data on the Web」,並關閉「高級數據保護(Advanced Data Protection)」,否則可能存取被拒。

> ⚠️ **使用聲明:** 此工具僅供下載 **你自己帳號** 的照片做備份/遷移使用;
> 請勿用於存取他人 iCloud 內容,並注意關閉「高級數據保護」會降低帳號安全等級,操作前評估風險。

> **應用案例:** 想把多年累積的數萬張 iCloud 照片完整備份到家裡的 NAS,
> 用 Docker 跑 sync 模式排程,每天自動把新照片增量同步下來、自動去重,
> 中途斷線也能靠斷點檢查續傳,不必手動在網頁版一張張下載。

## 6. wechat-article-exporter — 微信公眾號文章導出工具

- **連結:** <https://github.com/wechat-article/wechat-article-exporter>
- **用途:** 專注於 **導出微信公眾號文章** 的開源工具,把文章抓取下來並轉成 **Markdown、HTML 或 PDF**,適合歸檔、備份、離線閱讀、筆記整理。
- **亮點:**
  - 因官方沒有公開的文章提取 API,改用 **解析瀏覽器端文章資料** 的方式提取內容。
  - 掃碼登入一個公眾號後,可透過搜尋新增公眾號,自動抓取 **標題、作者、正文、圖片** 等並依所選格式輸出。
  - 可 **線上直接使用**,也能 **本地部署**(Docker 或原始碼),部署都相當容易。

> ⚠️ **使用聲明:** 此工具屬於抓取他人發布內容的雙面刃工具,僅供 **個人歸檔/離線閱讀** 等合理使用;
> 線上版需掃碼登入公眾號(等於把帳號授權給第三方服務),不放心請改本地部署;
> 導出後再次傳播他人文章可能涉及著作權,請自行確認授權與合規。

> **應用案例:** 你長期追蹤幾個技術公眾號,想把其中的乾貨文章保存成 Markdown 進自己的知識庫。
> 本地部署這個工具、掃碼登入後搜尋目標公眾號,批次導出成 Markdown,
> 再丟給 AI 做摘要或自動分類,把零散的公眾號內容沉澱成可檢索的個人筆記。

---

## 額外資源(Bonus)

本期另分享兩份報告:

- **《2025 抖音科技內容生態報告》** — 回顧這一年從年初 DeepSeek、到 Manus、Gemini 3 的科技浪潮,以前所未有的速度與規模席捲而來。
- **《開發者技術及生態發展 2030》** — InfoQ 的報告,探討開發者在 AI 浪潮中的不同心態(擔憂被取代 vs. 乘風而上)與整體技術生態的發展趨勢。

> 作者另以夸克網盤分享「一周熱點 100 期」彙整內容:<https://pan.quark.cn/s/32a4e4b816fe>

---

## 一句話總結

> 第 100 期的主軸圍繞「**讓 AI Agent 更能寫程式、更能動手、更會研究**」:opencode 讓你不被模型廠商鎖定、
> Superpowers 給 agent 一套資深工程師工作流、TARS 讓 AI 直接操作電腦 GUI、MiroThinker 用深度交互把研究做深;
> 另兩個 icloud_photos_downloader 與 wechat-article-exporter 則是把照片與公眾號內容備份到本地的實用工具。

---

## 來源

- [GitHub Weekly 第 100 期原文](https://github.com/itcoffee66/githubweekly/blob/main/_weekly/100.md)
- [itcoffee66/githubweekly(週報倉庫)](https://github.com/itcoffee66/githubweekly)
- 各專案連結見上文各節。
