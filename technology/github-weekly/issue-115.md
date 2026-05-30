# GitHub Weekly 第 115 期:桌面 AI 助手、程式 Agent 知識系統與隱身瀏覽器

> **期數:** #115(2026/05/17–05/23)
> **本期主題:** 桌面 AI 助手、程式設計 Agent 的知識系統、反偵測隱身瀏覽器、把 GUI 軟體變成 CLI 的自動化,以及即時 3D 場景重建。
> 來源:itcoffee66/githubweekly 第 115 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **OpenHuman** | 重隱私、有「持久記憶」的開源桌面 AI 助手 | 桌面 AI 助手 |
| 2 | **CodeGraph** | 給程式 Agent 用的知識圖譜,省 token、加速 repo 分析 | AI 程式工具 |
| 3 | **CloakBrowser** | 通過 30+ 反爬偵測的反偵測 Chromium | 自動化/爬蟲 |
| 4 | **CLI-Anything** | 把 GUI 軟體自動變成 AI 可用的命令列介面 | Agent 工具化 |
| 5 | **LingBot-Map** | 從影片串流即時重建 3D 場景(~20 FPS) | 3D/電腦視覺 |

---

## 1. OpenHuman — 重隱私、有持久記憶的桌面 AI 助手

- **連結:** <https://github.com/tinyhumansai/openhuman>
- **用途:** 開源的桌面 AI 助手,強調 **本地運行(local-first)** 與 **持久記憶**,把助手變成「會記得你」的長期夥伴,而非每次對話都失憶。
- **亮點:**
  - **118+ 第三方整合**,且能自動抓取資料(約每 20 分鐘刷新一次)。
  - **雙系統架構**:把「Memory Tree(記憶樹)」與「Obsidian Wiki 工作流」結合,兼顧結構化記憶與可瀏覽筆記。
  - **TokenJuice 壓縮層**:宣稱可把成本/延遲最多壓低 **80%**。
  - 支援本地模型;macOS / Linux 可用 `curl` 一鍵安裝。

> **應用案例:** 想要一個不把對話上傳雲端、又能跨天記住「我在做什麼專案、偏好什麼」的個人助理——
> 例如每天問它「昨天我們討論到哪」,靠 Memory Tree 接續脈絡,而非重貼背景。

## 2. CodeGraph — 給程式 Agent 的知識圖譜,專治「燒 token」

- **連結:** <https://github.com/colbymchenry/codegraph>
- **用途:** 一個 **知識圖譜引擎**,讓程式設計 Agent 在分析整個 code repo 時,不必把大量檔案塞進 context,
  而是查圖譜定位,藉此 **大幅降低 token 消耗**。
- **亮點:**
  - 官方數據:**成本 ↓35%、token ↓59%、速度 ↑49%**。
  - 支援 **19+ 種程式語言**,並有「框架專屬」的 URL→handler 對應(能理解路由到處理函式的關係)。
  - 相容 **Claude Code、Cursor、Hermes Agent** 等。
  - **100% 本地執行**,不呼叫任何外部 API。

> **應用案例:** 在大型 codebase 上跑 coding agent 時,與其每次 grep/讀檔把 context 撐爆,
> 不如先建一份程式知識圖譜,讓 agent「查圖找入口」再精準讀檔——和本庫 dev-tools 的 [Tree-sitter](../dev-tools/tree-sitter.md)
> 屬於同一條「結構化理解程式碼以省 token」的路線。

## 3. CloakBrowser — 通過 30+ 反爬偵測的反偵測瀏覽器

- **連結:** <https://github.com/CloakHQ/CloakBrowser>
- **用途:** 一個 **反偵測(anti-detection)的 Chromium**,用來繞過各種 bot 防護系統。
- **亮點:**
  - 通過 **30+ 種反爬偵測** 測試。
  - reCAPTCHA v3 拿到 **0.9 的人類等級分數**;可繞過 Cloudflare Turnstile。
  - 在 C++ 原始碼層做了 **58 處修補**,覆蓋指紋向量(canvas、WebGL、audio、GPU、WebRTC)。

> ⚠️ **使用聲明:** 此類工具屬雙面刃,僅供 **合法授權的自動化測試/研究** 使用;
> 繞過網站防護可能違反對方服務條款或當地法律,請自行確認授權與合規。

## 4. CLI-Anything — 把 GUI 軟體自動變成 AI 可用的 CLI

- **連結:** <https://github.com/HKUDS/CLI-Anything>
- **用途:** 自動把 **圖形介面軟體** 轉成「AI 能呼叫」的命令列介面,讓 Agent 也能操作原本只有 GUI 的工具。
- **亮點:**
  - 從原始碼 / GitHub repo **自動生成 JSON-first 的 CLI**。
  - 已有 **18+ 個社群貢獻的應用 adapter**:Blender、GIMP、LibreOffice、Zoom、Kdenlive、Godot 等。
  - 內建 **CLI-Hub 套件管理器**,可一鍵安裝各 adapter。
  - **2269+ 測試案例** 覆蓋。

> **應用案例:** 想讓 agent 自動化 Blender 建模或 GIMP 批次修圖,但這些工具沒有好用的 API——
> 用 CLI-Anything 生出一層 CLI,agent 就能用「下指令」的方式驅動它們。

## 5. LingBot-Map — 從影片即時重建 3D 場景

- **連結:** <https://github.com/Robbyant/lingbot-map>
- **用途:** 用 **transformer 幾何** 從影片串流做 **即時(streaming)3D 場景重建**。
- **亮點:**
  - **即時重建,約 20 FPS**。
  - 能處理 **超過 25,000 幀(13+ 分鐘)** 的長序列。
  - 支援室內 / 室外場景。
  - **Apache 2.0 授權**;模型已上架 HuggingFace 與 ModelScope。

> **應用案例:** 機器人/無人機邊走邊建環境地圖,或把一段巡檢影片直接轉成可量測的 3D 場景,
> 不必離線跑數小時的 SfM 重建。

---

## 額外資源(Bonus)

本期另分享兩份報告:

- **《OpenClaw 時代:中國 Agent 生態報告》** — 探討協定、模型與基礎設施。
- **《2025 人形機器人市場研究報告》** — 分析全球市場發展。

---

## 一句話總結

> 本期的主軸圍繞「**讓 AI Agent 更省、更能動手**」:OpenHuman 給它記憶、CodeGraph 給它省 token 的程式知識、
> CLI-Anything 讓它能操作 GUI 軟體;另兩個則分屬自動化(CloakBrowser)與電腦視覺(LingBot-Map)前沿。

---

## 來源

- [GitHub Weekly 第 115 期原文](https://github.com/itcoffee66/githubweekly/blob/main/_weekly/115.md)
- [itcoffee66/githubweekly(週報倉庫)](https://github.com/itcoffee66/githubweekly)
- 各專案連結見上文各節。
