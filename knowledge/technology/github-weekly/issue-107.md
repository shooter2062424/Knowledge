# GitHub Weekly 第 107 期:被 OpenAI 收購的 AI 安全工具、AI 代理事務所與 Agent 上下文資料庫

> **期數:** #107(2026/03/08–03/20)
> **本期主題:** 被 OpenAI 收購的 AI 安全/紅隊測試工具、AI 代理「人才事務所」、OpenClaw 技能精選庫、Claude Code 狀態列插件,以及為 Agent 設計的上下文資料庫。
> 來源:itcoffee66/githubweekly 第 107 期。以下為各收錄專案的名稱、用途、亮點與連結整理。

---

## 本期收錄專案一覽

| # | 專案 | 一句話 | 領域 |
|---|---|---|---|
| 1 | **promptfoo** | 評估與紅隊測試大模型應用的 CLI 工具,2026/3 被 OpenAI 收購 | AI 安全 |
| 2 | **agency-agents** | 一整套設計好人設的 AI 代理「事務所」,丟進 Claude Code 就能用 | Agent 角色資源 |
| 3 | **awesome-openclaw-skills** | 從 13000+ 技能篩到 5400+ 的 OpenClaw 高品質技能精選 | Agent 技能庫 |
| 4 | **claude-hud** | 在 Claude Code 狀態列顯示上下文用量、活躍工具與待辦進度 | Claude Code 插件 |
| 5 | **OpenViking** | 火山引擎開源、專為 Agent 設計的「上下文資料庫」 | Agent 記憶基礎設施 |

---

## 1. promptfoo — 評估與紅隊測試大模型應用,被 OpenAI 收購的 AI 安全工具

- **連結:** <https://github.com/promptfoo/promptfoo>
- **用途:** 用於 **評估(eval)** 與 **紅隊測試(red-teaming)** 大模型應用的 CLI 工具。在這波全球 OpenClaw 熱潮中,當 Agent 可能做出意料之外的操作時,安全與邊界變得格外重要;promptfoo 讓你告別反覆試錯,交付安全、可靠的 AI 應用。
- **亮點:**
  - 兩大核心功能:**自動化評估**(測試提示詞與模型、比較不同模型差異)與 **紅隊測試 / 漏洞掃描**。
  - 可在 **CI/CD 流程** 中做自動化檢查,提早發現程式碼中的安全性與合規問題。
  - 提供 **Web UI 與 CLI** 兩種使用方式,`npm` 即可安裝、依文件啟動。
  - 號稱已有數十萬使用者;**2026 年 3 月 9 日 OpenAI 正式官宣收購 promptfoo**,將其整合進 OpenAI Frontier(OpenAI 2026 年初推出的企業級「智能體協同」旗艦平台)。未來 promptfoo 將成為 OpenAI 安全方案的一部分。

> **應用案例:** 你做了一個客服 Agent,上線前想確認它不會被誘導洩漏系統提示或執行危險操作——
> 用 promptfoo 寫一組紅隊測試案例(prompt injection、越獄、敏感資料外洩),
> 把它掛進 GitHub Actions,每次改提示詞或換模型時自動跑一遍,
> 比較 GPT 與 Claude 在同一組測試下的安全表現再決定上線哪個。
> 這同時也是一個實打實的 AI 創業成功案例(被 OpenAI 收購)。

## 2. agency-agents — 一整套設計好人設的 AI 代理「事務所」

- **連結:** <https://github.com/msitarzewski/agency-agents>
- **用途:** 可以把它理解為一個 AI 代理的「人才市場」或「事務所」。它不是工具,而是一套精心設計的 **AI 代理人設集合**,每個代理都有自己的專業領域、性格特點與工作流程。
- **亮點:**
  - 目前分四個大部門:**工程部、設計部、銷售部、市場部**。光工程部就有前端、後端架構、行動端、AI 工程師、DevOps、安全工程師等二十多個角色。
  - 每個角色都有完整的定義文件:**身分定位、專業能力、工作流程、交付標準與溝通風格**。
  - 最推薦搭配 **Claude Code**,直接把 `agents` 資料夾複製到 `~/.claude/agents/` 即可;也支援 Cursor、Aider、Windsurf 等,並提供轉換腳本。
  - 思路在於:很多時候 AI 寫程式效果不好不是模型能力問題,而是 **上下文與角色定位不夠清晰**;這個專案把「AI 該怎麼工作」標準化了。

> **應用案例:** 你一個人接了案子但要同時當前端、後端跟設計——
> 把 agency-agents 複製到 `~/.claude/agents/` 後,需要寫 API 時 `@backend-architect` 出馬、
> 切版時 `@frontend-developer` 接手、想要文案時呼叫 `@market` 部門角色,
> 每個 sub-agent 都帶著明確的交付標準與溝通風格,等於替你的 AI 請了一群專業顧問來分工。

## 3. awesome-openclaw-skills — 從 13000+ 篩到 5400+ 的 OpenClaw 技能精選庫

- **連結:** <https://github.com/VoltAgent/awesome-openclaw-skills>
- **用途:** OpenClaw 生態已非常龐大,ClawHub 上有超過 **13000 個社群貢獻的 skills**,但品質參差不齊。這個專案做了件很實在的事:**篩掉 7000 多個低品質技能**,留下 **5400+ 經過篩選與分類的高品質技能**。
- **亮點:**
  - 過濾掉的包含 **垃圾帳號、重複內容、加密幣相關,甚至被安全審計標記為惡意** 的技能。
  - **整理清晰、按類別分好**:連接外部服務、開發工具、生產力工具、AI 相關等,基本能想到的需求都有對應 skill(ClawHub 原本只能關鍵字搜尋,體驗一般)。
  - 安裝 skill 可直接 `openclaw install`,或把連結丟給 OpenClaw 讓它自己裝。
  - 作者額外推薦搭配 **skill vett** 技能:讓 OpenClaw 在安裝任何 skill 前先做一次審查,發現高危問題就不裝,提升安全意識。

> ⚠️ **使用聲明:** 從第三方技能庫安裝 skill 等於把外部程式碼交給你的 Agent 執行,
> 即使經過篩選仍可能有風險。安裝前建議先用 skill vett 之類的工具審查,
> 不要無腦把陌生連結丟給 OpenClaw 自動安裝。

> **應用案例:** 你想讓 OpenClaw 自動把 Notion 內容同步到 Google Calendar,
> 與其在 ClawHub 用關鍵字海撈一堆品質不明的結果,
> 不如直接到這個精選庫的「連接外部服務」分類挑一個已被篩選過的 skill,
> 再用 skill vett 審一遍才安裝,省下大量篩選時間又降低踩雷機率。
>
> 註:作者也預期這類篩選功能很快會被 OpenClaw 官方(第一方)內建,效果會更好。

## 4. claude-hud — 在 Claude Code 狀態列顯示上下文用量與工具狀態

- **連結:** <https://github.com/jarrodwatts/claude-hud>
- **用途:** 一個實用的 **Claude Code 插件**,即時顯示「正在發生什麼」——例如 **上下文使用情況、活躍工具、運行中的子代理、待辦事項進度**,讓開發者更清楚 Claude Code 當前的狀態。
- **亮點:**
  - 解決痛點:Claude Code 很強,但開發過程中它「呼叫了什麼工具、讀了什麼檔案、開了哪些子任務、上下文還剩多少」常常看不清楚。
  - 採用 **Claude Code 原生狀態列(statusline)API**——無需單獨視窗、無需 tmux,**任何終端都能用**,上手容易。
  - 安裝三步:`​/plugin marketplace add jarrodwatts/claude-hud` → `​/plugin install claude-hud` → `​/claude-hud:setup` 設定狀態列,重啟後即可使用。

> **應用案例:** 你讓 Claude Code 跑一個橫跨多檔案的重構,跑到一半想知道它還有多少上下文額度、
> 此刻正在用哪個工具、有幾個子任務在跑——裝了 claude-hud 後,這些資訊直接顯示在終端底部狀態列,
> 不用一直往上捲訊息,就能判斷要不要先 `/compact` 或介入。

## 5. OpenViking — 火山引擎開源、專為 Agent 設計的上下文資料庫

- **連結:** <https://github.com/volcengine/OpenViking>
- **用途:** 位元組(字節)火山引擎開源的一項關鍵基礎設施:它不是模型,也不是 Agent 框架,而是一個 **專為 AI Agent 設計的上下文資料庫(context database)**。
- **亮點:**
  - 直指 AI 時代的痛點:資料雖豐富,**高品質上下文卻難取得**——上下文碎片化、需求激增、檢索效果不佳、記憶迭代有限。
  - 核心思路:把 Agent 的 **「記憶、資源、技能」統一管理**,全部放進一個統一的 Context 層,透過類似 `viking://` 的路徑存取,實現 **層級化載入與管理**。
  - 模型方面支援多種接入方式;最貼合近期熱點的場景是 **配置給 OpenClaw 當作記憶擴展**。
  - 官方測試數據:結合 OpenViking 後(即使仍開啟原生記憶),效果在原 OpenClaw 上 **提升 43%**,輸入 token 成本 **降低 91%**。

> **應用案例:** 你有一個長期協助你寫週報的 OpenClaw Agent,但它每次都「失憶」、
> 又因為把一堆歷史塞進上下文導致 token 爆表——
> 把 OpenViking 接成它的記憶層後,過往的專案脈絡、常用資源與技能用 `viking://` 路徑分層管理,
> Agent 需要時才精準載入對應上下文,既保留長期記憶又大幅壓低輸入 token 成本。
>
> 註:作者尚未完成與 OpenClaw 的實際配置體驗,等有結果會再分享。

---

## 額外資源(Bonus)

本期另分享兩份資料:

- **《The Complete Guide to Building Skills for Claude》** — Claude 官方出的 **33 頁 Claude skill 建構完全指南**,從概念到落地全部講透,適合想學「怎麼構建合適 skill」的人。
- **《OpenClaw 藍皮書》** — 近期出現許多各種「皮」的 OpenClaw 整理書(多為個人或 AI 整理),作者挑了兩份份量較大的供學習參考。

> 整期內容另有夸克網盤打包分享(連結見原文)。

---

## 一句話總結

> 本期主軸圍繞「**Agent 的安全、角色與記憶**」:promptfoo 替 Agent 把關安全(且被 OpenAI 收購)、
> agency-agents 給 Agent 標準化的角色人設、awesome-openclaw-skills 幫你篩出可靠的技能、
> claude-hud 讓你看清 Claude Code 的即時狀態,OpenViking 則為 Agent 補上統一的上下文/記憶層。

---

## 來源

- [GitHub Weekly 第 107 期原文](https://github.com/itcoffee66/githubweekly/blob/main/_weekly/107.md)
- [itcoffee66/githubweekly(週報倉庫)](https://github.com/itcoffee66/githubweekly)
- 各專案連結見上文各節。
