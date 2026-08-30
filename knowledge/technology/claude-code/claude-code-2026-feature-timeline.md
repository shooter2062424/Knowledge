# Claude Code 2026 功能演進:從「權限提示」到「agent 艦隊」的半年軌跡

> 整理自 **Claude Code 官方 What's New**(週更摘要,涵蓋 **Week 13 / 2026-03-23 ~ Week 34 / 2026-08-21**,版本 v2.1.83 – v2.1.239)。
> **本文不是逐條轉錄,而是把半年的更新重新按主題歸類,並標出與本倉庫既有筆記的對應。**

> 相關筆記:[[output-style-communication-not-intelligence]]、[[claude-dynamic-workflows]]、[[long-running-agents-goal-evaluation]]、[[claude-code-hooks-complete-guide]]、[[claude-md-cut-82-percent-and-maintain-it]]、[[continue-after-directory-move]]、[[claude-code-architecture-deep-dive]]

---

## 一句話總結

**把半年的更新排在一起看,一條主線非常清楚:Claude Code 正在從「一個會聽話的終端工具」變成「一個你要管理的 agent 艦隊」。**

⭐ 而權限模型的演變是這條線的縮影:**3 月引入 auto mode(分類器代你按核准)→ 8 月它成為 Pro / Max / Team 新 session 的預設。**

---

## 一、⭐ 最新一則:`/design`(Week 34,2026-08-17~21)

| 項目 | 內容 |
|---|---|
| **狀態** | **research preview** |
| **做什麼** | ⭐ **把 Claude Design 的 artboard 工作流帶進 CLI 與 Claude Code Desktop** |
| **建立在什麼上** | ⭐ **artifacts** |
| **流程** | **Claude 為你的 UI 起草「可編輯的 artboard」,你挑一個,它就把那個實作出來** |

⭐⭐ **這一項的意義不只是多一個指令** —— 它把「設計」與「實作」接在同一條 session 裡。以往是:在別的工具畫 → 描述給 Claude → 它猜你要什麼。現在是:**它畫幾個版本 → 你指一個 → 它照那個做。**

> 📎 對照 [[claude-design-review]] —— 那篇評測的是 Claude Design 這個獨立產品,**這裡是它被收進 Claude Code 的動作**。

**同週還有三項:**

| 功能 | 說明 |
|---|---|
| ⭐ **Concise 內建輸出風格** | **讓 Claude 先給結果、跳過開場白** |
| **Device card** | 任何跑著 `claude remote-control` 的機器,**會以裝置卡片出現在你手機上**,可從 Code 分頁直接在那台機器上開 session |
| **`ANTHROPIC_DEFAULT_MODEL`** | 設定新 session 預設從哪個模型開始 |

> ⭐ **Concise 這一項正好印證了 [[output-style-communication-not-intelligence]] 那篇的補正** —— 兩支談 output style 的影片都沒提到它,但它才是「治囉嗦」最直接的內建答案。

---

## 二、⭐⭐ 主線一:權限模型的半年演變

**這是全期最清楚的一條演進線,值得單獨拉出來看:**

```mermaid
flowchart TB
    W13["Week 13(3 月)<br/>⭐ auto mode 進入 research preview<br/>分類器代你處理權限提示:<br/>安全的直接跑、有風險的擋下"] --> W19
    W19["Week 19(5 月)<br/>hard deny 規則<br/>⭐ 無條件封鎖,不受 allow 例外影響"] --> W21
    W21["Week 21(5 月)<br/>auto mode 上 Pro 方案"] --> W23
    W23["Week 23(6 月)<br/>上 Bedrock / Google Agent Platform / Microsoft Foundry"] --> W25
    W25["Week 25(6 月)<br/>⭐ 擋下破壞性 git 指令<br/>(當你沒要求丟棄本地變更時)"] --> W28
    W28["Week 28(7 月)<br/>⭐ 擋轉錄稿竄改<br/>對「變數未解析的 rm -rf」先問"] --> W32
    W32["Week 32(8 月)<br/>⭐⭐ 8/14 起成為 Pro / Max / Team<br/>新 session 的「預設」權限模式"]
```

⭐⭐ **這條線的定位講得很精準:auto mode 是「全部核准」與 `--dangerously-skip-permissions` 之間的中間地帶。**

⚠️ **而每一次補強都是針對一個具體的破壞面**:破壞性 git 指令、轉錄稿竄改、變數沒解析的 `rm -rf`。**這不是通用的安全論述,是一份實際踩過的清單。**

> 📎 對照 [[pi-minimal-agent-harness-teardown]] 的相反取捨(刻意不做權限系統)與 [[codex-as-a-platform-open-agent-harness]] 把審批做成協定原語 —— **三家對「該不該內建安全機制」給了三個不同答案。**

---

## 三、⭐⭐ 主線二:從「一個 session」到「一支艦隊」

**這條線的密度最高,幾乎每個月都有進展:**

| 週次 | 功能 | 意義 |
|---|---|---|
| **W20**(5 月) | ⭐ **Agent view(`claude agents`)** | **一個畫面看所有 session:什麼在跑、什麼卡在你身上、什麼做完了** |
| **W21** | 背景 session 出現在 `/resume`,釘選後保持存活 | |
| **W22**(5 月) | ⭐⭐ **Dynamic workflows** | **從 Claude 自己寫的腳本編排「數十到數百個」subagent** |
| **W24**(6 月) | ⭐ **Subagent 可以再生自己的 subagent** | **背景鏈上限五層深** |
| **W26** | 背景 subagent 的權限提示**改為浮到主 session**,不再自動拒絕 | |
| **W27**(7 月) | ⭐ **Subagent 預設在背景執行** | 讓 Claude 在它們跑的時候繼續工作 |
| **W28** | Agent view 每列顯示**帶顏色的狀態字** + **分類器寫的標題** | |
| **W29** | ⭐ **`/fork`** 把對話複製到新的背景 session,你繼續原本的工作 | |
| **W32**(8 月) | ⭐⭐ **跨 session 訊息傳遞**(macOS / Linux) | **session 之間可以互相傳話 —— Claude 把一個發現或決定從一個 session 傳到另一個,而不用你重講一遍** |
| **W33** | ⭐ **Fork mode 在互動 session 中預設開啟**;打 **`@`** 可以按名稱提及另一個 session | |

⭐⭐ **把 W32 的「跨 session 訊息」跟 W20 的「Agent view」放在一起,就是這條線的終點形狀:你不再是「跟一個 AI 對話」,而是「管一組正在各自工作的 agent」。**

> 📎 這正好呼應 [[graph-engineering-node-edge-state]] 講的「別把自己變成人肉 routing system」—— **而 W32 的跨 session 訊息,就是把 routing 從你手上拿走的一步。**
> 也對照 [[recursive-agent-harness-harness-recursion]]:W22 的 dynamic workflows 正是那篇論文說的「同一種 code-first 生成模式的生產版」。

---

## 四、主線三:讓長時間工作真的能跑完

| 週次 | 功能 |
|---|---|
| **W15**(4 月) | ⭐ **Monitor 工具** —— 把背景事件串進對話,讓 Claude 能 tail log 並即時反應;**`/loop` 在你省略間隔時會自我調節節奏** |
| **W20**(5 月) | ⭐⭐ **`/goal`** —— **讓 Claude 跨多輪持續工作,直到某個完成條件成立** |
| **W20** | Rewind 選單可用「Summarize up to here」**壓縮較早的上下文** |
| **W26**(6 月) | ⭐ **`/rewind` 可以從「`/clear` 執行之前」恢復對話** |
| **W33**(8 月) | **Desktop 上額度用完可自動續跑** —— 勾選後,額度重置時自動重試被中斷的那一輪 |

> 📎 `/goal` 對應 [[long-running-agents-goal-evaluation]];而「完成條件」正是 [[loop-engineering-when-and-how-gary-chen]] 講的 **Verifiable Goal**。

---

## 五、主線四:離開終端 —— 桌面、雲端、手機

| 週次 | 功能 |
|---|---|
| **W13–14**(3–4 月) | ⭐ **Computer use** 進入 research preview(先 Desktop 後 CLI)—— **Claude 可以開原生 app、點 UI、驗證改動**。定位很明確:**適合收尾那些「只有 GUI 才驗得了」的事** |
| **W16**(4 月) | ⭐ **Routines**(web)—— **從排程、GitHub 事件或 API 呼叫觸發模板化的雲端 agent**;**手機推播**;CLI 改為原生二進位檔 |
| **W17** | ⭐ **`/ultrareview`** 公開研究預覽 —— **一支在雲端跑的抓蟲 agent 艦隊**,結果自動回到你的 CLI 或 Desktop |
| **W25**(6 月) | ⭐⭐ **Artifacts** —— **把 session 的產出變成 claude.ai 上一個「會隨 session 進行而就地更新」的可分享頁面** |
| **W28**(7 月) | ⭐ **Desktop 內建瀏覽器** —— Claude 可以叫出文件、設計稿或任何網站並互動 |
| **W29** | ⭐⭐ **Artifacts 可以呼叫「觀看者自己的」MCP connector** —— 已發布的 artifact 能在別人打開時,透過那個人的 connector 拉即時資料、執行動作 |
| **W30**(7 月) | **Desktop 開 iOS 模擬器分頁**(公開測試)—— Claude 能跑你的 app 並點過去給你看 |
| **W32**(8 月) | ⭐ **自架環境** —— 在你組織自己的基礎設施上跑 Claude Code 雲端 session(Team / Enterprise 公開測試) |
| **W34**(8 月) | **Device card** —— 跑著 remote-control 的機器出現在手機上 |

⭐⭐ **W29 的 artifacts + 觀看者 MCP 是這條線裡最特別的一項** —— 它把「分享一個結果」變成「分享一個會用『對方的』資料源活起來的東西」。

---

## 六、⭐ 主線五:模型與成本

| 週次 | 內容 |
|---|---|
| **W16**(4 月) | **Opus 4.7** 成為 Max / Team Premium 預設;⭐ **新增 `xhigh` effort 等級,且被推薦為多數 coding 工作的設定**;`/effort` 互動滑桿;**`/usage` 顯示什麼在吃額度** |
| **W21**(5 月) | ⭐ **`/usage` 細分到 skill、subagent、plugin、MCP server 層級** |
| **W22**(5 月) | **Opus 4.8** 成為 Max / Team Premium / Enterprise 隨用隨付 / API 預設,**預設 high effort**,`/effort xhigh` 給最難的任務;**fast mode $10/$50 per MTok** |
| **W24**(6 月) | ⭐ **`fallbackModel`** —— 可設定最多三個依序嘗試的後備模型 |
| **W27**(7 月) | **Sonnet 5** 成為 Pro / Team Standard / Enterprise 訂閱席次預設 —— **原生 1M token 上下文、adaptive thinking 預設開啟** |
| **W30**(7 月) | ⭐ **Opus 5** 成為 Claude Code 預設 Opus,**1M token 上下文**,fast mode **$10/$50 per MTok** |
| **W34**(8 月) | **`ANTHROPIC_DEFAULT_MODEL`** |

> ⭐ **`/usage` 從「顯示額度」進化到「細分到 skill / subagent / plugin / MCP server」,是很值得注意的一步** —— 它承認了一件事:**當你裝了一堆東西之後,你其實不知道錢花在哪。**
> 📎 這跟 [[token-saving-three-moves-context-control]] 講的「每個 MCP 的說明都被打包進 context」是同一個問題的兩面 —— 一個講成因,一個給了量測工具。

---

## 七、其他值得記的單項

| 週次 | 功能 | 為什麼值得記 |
|---|---|---|
| **W18**(4–5 月) | ⭐⭐ **Windows 不再需要 Git Bash** —— Bash 不存在時 Claude Code **改用 PowerShell 當 shell 工具** | 這對 Windows 使用者是結構性改變 |
| **W18** | `claude project purge` 清理專案的本機狀態;把 **PR URL 貼進 `/resume`** 會找到建立它的那個 session | |
| **W19**(5 月) | ⭐ **Plugin 可從 `.zip` 與 URL 載入**(`--plugin-dir` 吃 zip、`--plugin-url` 抓封存檔);**hook 可以看到當前 effort 等級**(`effort.level` / `$CLAUDE_EFFORT`) | 📎 hook 那條可補進 [[claude-code-hooks-complete-guide]] |
| **W24**(6 月) | ⭐ **`/cd`** —— **在對話中途換工作目錄,而且不會重建 prompt 快取** | 📎 正是 [[continue-after-directory-move]] 的官方解法 |
| **W24** | **`--safe-mode`** 停用所有自訂設定以排查問題 | |
| **W25** | ⭐ **deny / ask 規則可以比對工具參數** —— `Tool(param:value)`,例如 `Agent(model:opus)`;**`/config key=value`** 可從 prompt、`-p` 模式與 Remote Control 設定任何設定 | |
| **W26** | ⭐ **`claude mcp login` / `logout`** —— 從 shell 認證 MCP server,不用進互動選單;**shell 模式會對指令輸出作出回應**(`! npm test` 不用再問第二次就給解釋) | |
| **W28**(7 月) | ⭐ **`/doctor`(別名 `/checkup`)** —— 完整的環境檢查,**能診斷也能修** | 📎 [[claude-md-cut-82-percent-and-maintain-it]] 提過 |
| **W29** | ⭐ **Screen reader 模式** —— 用純線性文字取代視覺化終端介面,支援 VoiceOver / NVDA | 無障礙 |
| **W30**(7 月) | ⭐ **Claude Security plugin** —— 對程式庫做**多 agent 漏洞掃描**,把你挑中的發現變成**你自己套用**的修補;**`/code-review` 改為背景 subagent** | ⚠️ 注意「你自己套用」這個設計 |
| **W17**(4 月) | **Session recap** —— 終端沒被聚焦時發生了什麼;**自訂主題** | |
| **W14**(4 月) | **`/powerup` 互動課程**;每工具的 MCP 結果大小上限可覆寫到 **500K**;plugin 執行檔進 Bash 工具的 `PATH` | |
| **W15**(4 月) | ⭐ **Ultraplan 早期預覽** —— 從 CLI 在雲端草擬計畫、在網頁編輯器審閱評論,再遠端執行或拉回本機;**`/team-onboarding`** 把你的設定打包成可重播的指南 | |
| **W13**(3 月) | **轉錄稿搜尋(`/`)**;**Windows 原生 PowerShell 工具**;⭐ **條件式 `if` hook** | 📎 hook 那條可補進 hooks 筆記 |

---

## 應用案例

### 案例 1|⭐⭐ 從權限模型的演變讀出一條產品哲學

把 auto mode 半年的軌跡排開,會看到一個很清楚的模式:

```
① 先做成 research preview(3 月)—— 不預設開啟
② 逐步補「具體破壞面」的防護
   破壞性 git → 轉錄稿竄改 → 未解析變數的 rm -rf
③ 逐步擴大方案覆蓋(Pro → 第三方雲)
④ ⭐ 五個月後才變成預設(8/14)
```

⭐ **值得學的是第 ② 步的性質**:每一條防護都對應一個**具體的、可命名的破壞方式**,而不是抽象的「安全性提升」。**這代表它們是從實際事故裡長出來的。**

⚠️ **而「五個月才變預設」也是個訊號** —— 把預設從「每次問」改成「分類器決定」,是把風險從使用者身上移到系統身上,這種改動應該慢。

### 案例 2|⭐ 用這條時間軸檢查自己的用法有沒有過時

半年裡有好幾個功能取代了原本要繞路的做法:

| 你如果還在… | 現在有 |
|---|---|
| 為了換目錄而重開 session | ⭐ **`/cd`**(不重建 prompt 快取) |
| `/clear` 之後才想起有東西要用 | ⭐ **`/rewind` 可以回到 `/clear` 之前** |
| 手動開好幾個終端管平行工作 | ⭐ **`claude agents` + 背景 subagent + 跨 session 訊息** |
| 自己寫腳本編排多個 agent | ⭐ **Dynamic workflows** |
| 用 `--dangerously-skip-permissions` 圖方便 | ⚠️ **auto mode** —— 現在已是預設 |
| 抱怨回覆太囉嗦、自己寫 output style | ⭐ **內建 `Concise`** |
| 在別的工具畫 UI 再描述給 Claude | ⭐ **`/design`** |

### 案例 3|⚠️ 注意兩個「刻意不自動」的設計

在一片自動化裡,有兩處官方刻意留了手動:

1. ⭐ **Claude Security plugin 的修補是「你自己套用」** —— 它掃描、它產生修補,**但不替你套用**
2. ⭐ **`/design` 是「它畫幾個、你挑一個」** —— 不是它直接決定

⭐ **共同點:在「有品味成分」或「有安全成分」的決策點上,把最後一步留給人。** 📎 這跟 [[graph-engineering-node-edge-state]] 講的「human approval 處理的是價值判斷而非邏輯判斷」是同一條原則。

### 案例 4|⭐ Artifacts + 觀看者 MCP:一個值得想清楚的能力

W29 那項的含意比表面大:

```
傳統分享:我把結果匯出成一份靜態文件給你
Artifacts:我分享一個頁面,它在我的 session 進行時就地更新
⭐ W29:我分享的頁面,會用「你自己的」MCP connector 拉即時資料、執行動作
```

⚠️ **第三層要特別小心**:那個頁面在別人的環境裡、用別人的憑證做事。**分享之前要想清楚頁面裡的程式碼會做什麼** —— 這跟 [[pi-minimal-agent-harness-teardown]] 提到的「裝第三方 extension 等於執行別人的程式碼」是同一類風險,只是方向相反(這次是你把東西送出去)。

---

## 重點回顧(TL;DR)

1. ⭐⭐ **半年主線:Claude Code 從「會聽話的終端工具」變成「你要管理的 agent 艦隊」。**
2. **最新(Week 34,8/17–21):`/design` research preview** —— **把 Claude Design 的 artboard 工作流帶進 CLI 與 Desktop,建立在 artifacts 上;Claude 起草可編輯 artboard,你挑一個它就實作。** 同週另有 **Concise 輸出風格**、**device card**(remote-control 機器出現在手機上)、**`ANTHROPIC_DEFAULT_MODEL`**。
3. ⭐⭐ **權限模型是全期最清楚的演進線**:3 月 auto mode 進 research preview(**定位是「全部核准」與 `--dangerously-skip-permissions` 之間的中間地帶**)→ 逐步補防護(**hard deny 無條件封鎖、擋破壞性 git、擋轉錄稿竄改、對未解析變數的 `rm -rf` 先問**)→ 擴大到 Pro 與三家雲 → **8/14 起成為 Pro/Max/Team 新 session 的預設**。⭐ **每條防護都對應一個具體可命名的破壞方式,不是抽象的安全論述。**
4. ⭐⭐ **艦隊化那條線**:`claude agents` 一畫面看全部 → **dynamic workflows 編排數十到數百個 subagent** → **subagent 可再生 subagent(上限五層)** → subagent 預設背景執行 → `/fork` → ⭐ **跨 session 訊息傳遞(Claude 把發現從一個 session 傳到另一個,不用你重講)** → fork mode 預設開啟、`@` 提及其他 session。
5. **長時間工作**:**Monitor**(串背景事件、能 tail log 即時反應)、**`/goal`**(跨輪持續工作直到完成條件成立)、**「Summarize up to here」壓縮早期上下文**、⭐ **`/rewind` 能回到 `/clear` 之前**、Desktop 額度重置後自動續跑。
6. **離開終端**:**computer use**(定位是「收尾那些只有 GUI 才驗得了的事」)、**Routines**(排程/GitHub 事件/API 觸發雲端 agent)、**`/ultrareview`**(雲端抓蟲 agent 艦隊)、**Artifacts**(會就地更新的可分享頁面)、Desktop 內建瀏覽器與 iOS 模擬器、**自架環境**。
7. ⭐⭐ **W29 的 Artifacts + 觀看者 MCP 最特別**:已發布的 artifact 能在別人打開時,**透過「那個人的」connector 拉即時資料、執行動作**。⚠️ 分享前要想清楚頁面裡的程式碼會做什麼。
8. **模型線**:Opus 4.7(**新增 `xhigh` 且被推薦為多數 coding 工作的設定**)→ Opus 4.8(**預設 high effort**)→ Sonnet 5(**原生 1M 上下文、adaptive thinking 預設開**)→ **Opus 5(1M 上下文、fast mode $10/$50 per MTok)**;另有 **`fallbackModel`(最多三個依序嘗試)**。
9. ⭐ **`/usage` 從「顯示額度」進化到「細分到 skill / subagent / plugin / MCP server」** —— 等於承認「裝了一堆東西之後你不知道錢花在哪」。
10. ⭐⭐ **Windows 不再需要 Git Bash** —— Bash 不存在時改用 **PowerShell** 當 shell 工具。
11. **其他實用單項**:⭐ **`/cd`(中途換目錄且不重建 prompt 快取)**、`--safe-mode`、⭐ **deny/ask 規則可比對工具參數 `Tool(param:value)`**、`/config key=value`、⭐ **`claude mcp login`/`logout`**、shell 模式會對指令輸出直接回應、⭐ **`/doctor`(別名 `/checkup`,能診斷也能修)**、**screen reader 模式**、plugin 可從 `.zip` 與 URL 載入、**hook 看得到 effort 等級**、**條件式 `if` hook**、MCP 結果大小可覆寫到 500K。
12. ⭐ **兩個刻意不自動的設計值得注意**:**Claude Security plugin 產生修補但「你自己套用」**;**`/design` 是「它畫幾個、你挑一個」**。⭐ **共同原則:在有品味或有安全成分的決策點,把最後一步留給人。**

---

## 來源

- [What's new — Claude Code Docs](https://code.claude.com/docs/en/whats-new)(週更摘要;本文涵蓋 **Week 13 / 2026-03-23 至 Week 34 / 2026-08-21**,版本 v2.1.83 – v2.1.239)
- 官方另有逐條的 [changelog](https://code.claude.com/docs/en/changelog) 記錄每個 bug fix 與小改進
- 本倉庫相關筆記:[[output-style-communication-not-intelligence]]、[[claude-dynamic-workflows]]、[[long-running-agents-goal-evaluation]]、[[claude-code-hooks-complete-guide]]、[[claude-md-cut-82-percent-and-maintain-it]]、[[continue-after-directory-move]]、[[claude-code-architecture-deep-dive]]、[[claude-design-review]]、[[graph-engineering-node-edge-state]]、[[token-saving-three-moves-context-control]]、[[loop-engineering-when-and-how-gary-chen]]、[[pi-minimal-agent-harness-teardown]]、[[codex-as-a-platform-open-agent-harness]]

> ⚠️ **Claude Code 迭代極快(半年跨了 v2.1.83 → v2.1.239)**,本文是特定時點的快照。功能可能已改名、改預設值或移除(例如 `/output-style` 就在 v2.1.73 棄用、v2.1.91 移除)。**實際可用項目請以你當下版本的 `/help` 與官方文件為準。**
