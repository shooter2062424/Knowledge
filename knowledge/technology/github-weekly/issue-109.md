# GitHub Weekly 第 109 期:被開源的 Claude Code、JS 排版引擎與瀏覽器端 3D 建模

> **期數:** #109(2026/03/28–04/03)
> **本期主題:** 因設定失誤而「被開源」的 Claude Code、純 JS 的多行文字測量與排版引擎、Claude Code 從入門到精通的視覺化指南、Google 最新開源模型 Gemma 4,以及完全跑在瀏覽器裡的 3D 建築編輯器。
> 來源:itcoffee66/githubweekly 第 109 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **Claude Code** | 因 npm 設定失誤而意外「被開源」的官方 CLI | AI 程式工具 |
| 2 | **Pretext** | 純 JS 的多行文字測量與排版引擎,比 DOM 快數百倍 | 前端/效能 |
| 3 | **Claude How To** | Claude Code 從入門到精通的視覺化指南 | AI 程式工具 |
| 4 | **Gemma 4** | Google 最新一代開源模型,主打端側與推理 | 開源模型 |
| 5 | **Pascal Editor** | 完全跑在瀏覽器裡的開源 3D 建築編輯器 | 3D/前端 |

---

## 1. Claude Code — 因設定失誤而「被開源」的官方 CLI

- **連結:** <https://github.com/anthropics/claude-code>
- **用途:** Anthropic 官方的命令列 AI 程式助手。本期的看點不在它本身,而在於一樁業界大新聞:**Claude Code 因一個低級的 npm 設定錯誤「意外開源」了。**
- **亮點:**
  - 在 Claude Code 的公開 npm 套件裡,除了常規檔案外,竟然夾帶了一個高達 **59.8 MB 的 `cli.js.map`** 檔案。
  - 有了這個 **Source Map**,就能把壓縮混淆後的程式碼反向映射回原始原始碼——等於把整套實作攤在陽光下。
  - 一時之間 GitHub 冒出無數個 Claude Code 鏡像倉庫,其中最知名的那個 star 光速暴增,甚至出現 **fork 比 star 還多** 的奇景。
  - Anthropic 迅速以 **DMCA 版權投訴** 封殺所有分享原始碼的連結。洩漏者為了避免被起訴,在極短時間內完成罕見的「換殼手術」:把龐大的 TypeScript 全量改寫為 **Python**,接著又用 **Rust** 重構一遍;但換過殼的專案最終仍被下架。
  - 這件事的提醒意義大於技術意義:再大的 AI 巨頭也會犯把敏感檔案、金鑰一不小心提交出去的低級錯誤。

> ⚠️ **使用聲明:** 透過外洩 Source Map 取得、傳播他人專有原始碼可能侵犯版權並違反授權條款(Anthropic 已實際以 DMCA 下架相關倉庫)。本節僅作為事件記錄與安全警示,**請勿散布或商用洩漏的原始碼**;一般使用者直接透過官方管道安裝使用即可。
>
> **應用案例:** 對團隊而言,這是一堂活生生的供應鏈/發佈安全課——例如在 CI 發佈流程加上「打包產物白名單檢查」,確認 npm publish 前不會誤帶 `.map`、`.env`、金鑰等檔案;以及示範了 Source Map 上線可能造成原始碼外洩,生產環境應關閉或不隨套件發佈 Source Map。

## 2. Pretext — 純 JS 的多行文字測量與排版引擎

- **連結:** <https://github.com/chenglou/pretext>
- **用途:** 一個純 TypeScript 函式庫,專門做 **多行文字的測量與排版(layout)**,用來繞開傳統前端「要量文字就得渲染進 DOM」的痛點。
- **亮點:**
  - 約 **31,487 stars / 1,613 forks**,是本週 GitHub 上的熱門專案。
  - 解決長年困擾前端的問題:傳統上要知道一段文字的高度或行數,唯一可靠方式是把它渲染進 DOM 再讀 `getBoundingClientRect` / `offsetHeight`,但這會觸發昂貴的 **layout reflow(重排)**,在大量元件同時測量時效能急遽惡化。
  - Pretext 的做法是 **繞過 DOM**,改用瀏覽器自帶字型引擎(Canvas 的 `measureText`)做一次性文字分析並快取結果;之後不管怎麼改寬度、換版面,`layout()` 階段都只是純數學運算。
  - Benchmark 上約 **0.09ms 處理 500 條文字,比 DOM 測量快 300–600 倍**。
  - 屬於較底層的工具,適合對文字渲染效能有極致要求的場景;一般頁面用現成 CSS 方案就夠。

> **應用案例:** 在做大型虛擬列表(virtual list)或聊天訊息流時,每筆訊息高度不一,需要先算出每列高度才能正確估算捲動位置。若用 DOM 逐一測量會嚴重卡頓;改用 Pretext 在記憶體中一次算好數百條訊息的行數與高度,捲動就能維持順暢。

## 3. Claude How To — Claude Code 從入門到精通的視覺化指南

- **連結:** <https://github.com/luongnv89/claude-howto>
- **用途:** 一份直觀、範例驅動的 Claude Code 使用指南,專治「裝了 Claude Code、跑了幾條 prompt 之後就不知道還能幹嘛」的常見窘境。
- **亮點:**
  - 把官方文件有提、卻沒教你「怎麼組合起來幹活」的能力串成完整路線:commands、hooks、memory、subagents、MCP servers、skills、plugins。
  - 以 **視覺化教學 + 開箱即用的 Mermaid 圖表 + 10 個模組 + 可複製的設定範本** 組成引導式學習路徑。
  - 學習路徑分三階段:**入門**(slash commands + memory,約 2.5 小時)→ **進階**(skills + hooks + MCP,約 4 小時)→ **高級**(subagents + plugins + advanced,約 5 小時)。
  - 每個模組內建自測,可在 Claude Code 裡直接執行 `/self-assessment` 找出自己的弱點。
  - 最大價值在實用性:每個模組最後都附上可直接 `cp` 進專案的設定檔;熱度也反映出「既教怎麼用、也教為什麼」的專案很受歡迎。

> **應用案例:** 一位剛上手 Claude Code 的工程師想讓它真正接管日常開發流程,卻不知如何起步。照著 Claude How To 的入門→進階→高級路徑走,先用 memory 與 slash commands,再逐步加上 hooks(例如存檔自動跑 lint)、自訂 subagents 與 MCP server,最後把模組附的設定範本複製進自己的專案,兩三天內就能把 Claude Code 從「玩具」變成生產力工具。

## 4. Gemma 4 — Google 最新一代開源模型

- **連結:** <https://huggingface.co/blog/gemma4>
- **用途:** Google 最新開源的模型系列,自稱「迄今為止最智能的開放模型系列」,面向 **複雜推理與代理(agent)工作流** 設計,以商業友善的 **Apache 2.0** 授權開源。
- **亮點:**
  - 約 **17,435 stars / 1,408 forks**。
  - 提供四種規格:**Effective 2B(E2B)**、**Effective 4B(E4B)**、**26B 混合專家模型(MoE)** 與 **31B 稠密模型(Dense)**。
  - 最受矚目的是端側模型:**E2B 與 E4B 針對行動與物聯網裝置最佳化**,推理時分別只激活約 20 億、40 億參數,以降低記憶體與耗電;官方並列出各尺寸所需的 GPU / TPU 記憶體估算。
  - 相較上一代:推理更強、上下文視窗更大、編碼與代理能力增強、多模態進一步擴展;**31B Dense 版本在業界標準榜單的開源模型中排名第三**。
  - 開箱支援 **NVIDIA、AMD GPU 以及 Google Cloud TPU**;Mac 使用者需稍等社群更新 MLX 版本。

> **應用案例:** 想在手機或邊緣裝置上跑離線 AI 助手而不想連雲端時,可選 E2B / E4B——只激活約 20–40 億參數,在記憶體與電量受限的環境下仍能做基本推理與工具呼叫;若是在伺服器端要兼顧品質與成本,則可用排名前段的 31B Dense 版本,且 Apache 2.0 授權讓商業落地沒有授權顧慮。

## 5. Pascal Editor — 瀏覽器裡的 3D 建築編輯器

- **連結:** <https://github.com/pascalorg/editor>
- **線上體驗:** <https://editor.pascal.app>
- **用途:** 一個開源的 **3D 建築編輯器**,完全跑在瀏覽器裡,不需安裝任何軟體,就能畫牆體、樓層、屋頂、門窗,還能做空間分區與室內布局。
- **亮點:**
  - 約 **9,127 stars / 1,176 forks**。
  - 基於 **React Three Fiber + WebGPU** 構建,完全瀏覽器端執行。
  - 架構切成三個套件:核心邏輯(`@pascal-app/core`)、3D 渲染(`@pascal-app/viewer`)、編輯器 UI(`apps/editor`)。
  - 狀態管理用 **Zustand**,支援 **IndexedDB 持久化** 與 **50 步 undo/redo**;渲染管線用一個 **Scene Registry** 管理節點到 Three.js 物件的映射,避免遍歷整個場景圖的開銷。
  - 定位偏向建築師與室內設計師的「快速原型工具」,而非取代 AutoCAD 或 SketchUp;**完全免費、MIT 授權**,對 Mac 友善。

> **應用案例:** 室內設計師在跟客戶開會時,不必開沉重的桌面軟體——直接在瀏覽器打開 Pascal Editor,當場拉出房間隔間、擺上門窗、調整樓層配置,客戶即時看到 3D 效果並提意見;因為資料存在 IndexedDB,關掉分頁下次再開也還在,並可靠 50 步 undo/redo 快速試錯。

---

## 額外資源(Bonus)

本期 one more thing 另分享兩份資料:

- **《AI 醫學影像行業發展現狀與未來趨勢藍皮書》** — 由沙利文(Frost & Sullivan)與相關組委會聯合出品。作者看好 AI 在醫療領域的巨大潛力,而中國醫療影像發展仍有不足,值得關注。
- **《OpenClaw(龍蝦)全維度安全實戰指南》** — OpenClaw 存在安全隱患已逐漸成為共識(連官媒都已強調),但多數人難具體說清是什麼隱患;這份較專業的內容可用來了解相關安全問題。

> 資料透過夸克網盤分享:<https://pan.quark.cn/s/2b3982ac3613>

---

## 一句話總結

> 本期主軸落在「**AI 程式工具的熱潮與翻車**」:Claude Code 因設定失誤被迫上演開源與下架的攻防戲、Claude How To 教你把它用滿;另外三個則分屬前端效能(Pretext)、開源模型(Gemma 4)與瀏覽器端 3D(Pascal Editor)的前沿。

---

## 來源

- [GitHub Weekly 第 109 期原文](https://github.com/itcoffee66/githubweekly/blob/main/_weekly/109.md)
- [itcoffee66/githubweekly(週報倉庫)](https://github.com/itcoffee66/githubweekly)
- 各專案連結見上文各節。
