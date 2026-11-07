# Claude Code 30 個藏得最深的快捷鍵與功能:暫存、插隊、回退與 Agent 視圖

> 整理自 YouTube 頻道 **YAHA學堂**〈Claude Code 教程:30个隐藏最深功能,有些你一次都没用过〉(2026-10-17,約 16 分鐘)。作者錄影時用的是 Claude Code v2.1.296。
>
> **立場揭露:** 說明欄寫這支影片是作者「用 Opus 製作」的。作者在片尾說自己的 Claude 帳號被封,之後會轉向 Codex 等其他工具。說明欄沒有聯盟連結。
>
> **核對方式:** 本文每個按鍵都已逐一對照官方文件:[Interactive mode](https://code.claude.com/docs/en/interactive-mode)、[Keybindings](https://code.claude.com/docs/en/keybindings)、[Model config](https://code.claude.com/docs/en/model-config)、[Fullscreen](https://code.claude.com/docs/en/fullscreen)、[Agent view](https://code.claude.com/docs/en/agent-view),2026-10-18 查核。補正與平台差異以 📌 標出。
>
> **整理日期:** 2026-10-18

---

## TL;DR

1. **prompt 寫到一半被打斷:** `Ctrl+S` 暫存、`Ctrl+G` 用編輯器改長 prompt、`Ctrl+J` 換行不送出。
2. **Claude 在忙時不用乾等:**
   - `Ctrl+B` 把工作丟到背景。
   - 直接 `Enter` 會排隊;`Ctrl+X Enter` 在有自動完成候選時也能排隊。
   - `Ctrl+Enter` 或 `Ctrl+X Ctrl+S` 立刻插隊。
   - `Ctrl+X Ctrl+K` 一次停掉所有背景子 agent。
3. **輸入框是 readline 那一套:** `Ctrl+W` 刪到前一個空白、`Ctrl+Y` 貼回、`Ctrl+_` 復原、`Esc Esc` 清空(會存進歷史)。
4. **只對這次 session 生效:** `/model`、`/effort` 裡按小寫 `s`,不會改到預設值。
5. **很多功能要先開全螢幕渲染**(`/tui fullscreen`):transcript 裡的 `?` 說明、`{` `}` 跳 prompt、`Ctrl+R` 切搜尋範圍、diff 面板、`PgUp` 捲動。
6. **最實用的是 Agent 視圖:** 空輸入框按 `←`,所有 session 依狀態排好,可以分組、置頂、搜尋、改名。

```mermaid
flowchart TD
    A["30 個功能"] --> B["寫 prompt<br/>暫存、編輯器、換行"]
    A --> C["Claude 在忙<br/>背景、排隊、插隊、全停"]
    A --> D["彈窗裡<br/>權限加註解、/btw"]
    A --> E["輸入框編輯<br/>刪、貼回、復原、清空"]
    A --> F["輸入框入口<br/>emoji、問號、斜線、驚嘆號、建議"]
    A --> G["模型與力度<br/>s 只套用這次"]
    A --> H["回顧與管理<br/>回退、transcript、搜尋、diff、Agent 視圖"]
    H --> I["多數要全螢幕渲染<br/>/tui fullscreen"]
```

---

## 1. prompt 寫到一半被打斷(1–3)

| # | 按鍵 | 作用 | 📌 對照官方文件 |
|---|---|---|---|
| 1 | `Ctrl+S` | **暫存**目前輸入、清空輸入框,右下角出現 stash 提示 | 官方寫法是「在空輸入框**再按一次** `Ctrl+S` 還原」,而且連游標位置、貼上的內容、輸入模式都一起還原,例如暫存的 `!` 指令會回到 shell 模式。影片示範的是送出問題後暫存內容**自動回填**,官方文件沒有寫這個行為,以實測為準 |
| 2 | `Ctrl+G` 或 `Ctrl+X Ctrl+E` | 用外部編輯器(讀 `$EDITOR`)開啟 prompt,存檔離開後內容填回輸入框 | ✅ `Ctrl+X Ctrl+E` 是 readline 原生按法。`/config` 開 **Show last response in external editor**,會把 Claude 上一則回覆以 `#` 註解放在 prompt 上方 |
| 3 | `Ctrl+J`,或行尾 `\` 加 `Enter` | 換行不送出 | ✅ 兩種都是「任何終端機免設定」。Shift+Enter 要看終端機設定 |

> 編輯器小提醒:Nano 用 `Ctrl+X`、`Y`、`Enter` 存檔離開;Vim 用 `Esc` 加 `:wq`。

---

## 2. Claude 在忙時不用乾等(4–9)

| # | 按鍵 | 作用 | 📌 對照官方文件 |
|---|---|---|---|
| 4 | `Ctrl+B` | 把正在跑的 Bash 指令或 agent 轉到背景,輸入框馬上空出來;跑完 Claude 會收到通知再告訴你 | ✅ **tmux 使用者要按兩次**,因為 `Ctrl+B` 是 tmux 前綴鍵。也可用 `Ctrl+X Ctrl+B` |
| 5 | 忙碌中直接 `Enter` | 訊息**排隊**,不打斷目前這輪 | ✅ 若 Claude 正在跑工具,排隊的訊息會在工具跑完後、**同一輪內**就交給 Claude |
| 6 | `Ctrl+X` 放開,再按 `Enter` | 有自動完成候選彈出時,`Enter` 會先選中候選;這個和弦**照樣把整句排進隊列** | ✅ 官方 action 是 `chat:queueSubmit`,需 v2.1.247 以上。和弦每一鍵要在**前一鍵 3 秒內**按下 |
| 7 | 排隊後按 `↑` | 把排隊中的訊息收回輸入框,改完再排 | ✅ 要從輸入框**第一行**按 |
| 8 | `Ctrl+Enter` 或 `Ctrl+X Ctrl+S` | **插隊**:立刻送出排隊的訊息。能轉背景的工作(測試、子 agent)會自動轉背景繼續跑,Claude 先回答你 | ✅ 需 v2.1.275 以上。不支援擴充按鍵的終端機會把 `Ctrl+Enter` 當成一般 `Enter`(變成排隊),所以 **`Ctrl+X Ctrl+S` 是哪裡都能用的保底按法** |
| 9 | `Ctrl+X Ctrl+K` | **緊急煞車**:停掉這個 session 所有背景子 agent。第一次按會問確定嗎,3 秒內再按一次執行 | 📌 官方補充:它同時會**關掉這個 session 剩下時間的 artifact 自動回覆** |

**`Ctrl+Z` 暫停整個 Claude Code(第 10 個):** 回到一般 shell,用完打 `fg` 回來,畫面原樣恢復。
- 📌 **只有 macOS 與 Linux(Unix)能用**,Windows 沒有。
- 習慣按 `Ctrl+Z` 復原的人要改用 `Ctrl+_`(見第 12 個)。

---

## 3. 彈窗裡藏的鍵(11 與 /btw)

**第 11 個:權限提示框上按 `Tab` 加註解**
- Claude 要動檔案前會問你同不同意。在 **Yes** 或 **No** 上按 `Tab`,會開一個註解欄,可以補一句修改意見。影片示範的是先照原計畫建檔,再依意見修改,省掉重新描述需求那一輪。
- 開著 **auto** 等自動模式時不會跳這個框,先用 `Shift+Tab` 切回手動(`default`)。
- 📌 Windows 上若 Node 或 Bun 沒開 VT 輸入模式,切換模式的鍵是 `Alt+M`。

**`/btw` 順便問一句:**
- 答案顯示在浮層,不寫進對話紀錄。它只根據已有的對話內容回答,**沒有工具**,不會讀檔或跑指令。Claude 正在工作時也能用,不會打斷主流程。
- 浮層裡的鍵:

| 鍵 | 作用 |
|---|---|
| `c` | 把答案以原始 Markdown 複製到剪貼簿,比滑鼠選取乾淨 |
| `f` | 把這組問答**分岔成背景子 agent**,帶著完整對話繼續做,而且可以用工具 |
| `Shift+←` / `Shift+→` | 在之前的 `/btw` 答案間切換 |
| `x` | 清掉之前的 `/btw` 列表 |

---

## 4. 輸入框編輯(12–19)

| # | 按鍵 | 作用 | 📌 對照官方文件 |
|---|---|---|---|
| 12 | `Ctrl+_`(實際按 `Ctrl+Shift+-`) | **復原**上一次輸入編輯,游標也回原位 | ✅ 兩種寫法都是官方預設 |
| 13 | `Ctrl+W` | 往回刪到**上一個空白**,所以 `src/utils/foo.ts` 一次刪光 | ✅ 只想刪一個字,macOS 用 `Option+Delete`、Windows 用 `Ctrl+Backspace`(標點會切字) |
| 14 | `Ctrl+Y` | 貼回剛才用 `Ctrl+W`、`Ctrl+U`、`Ctrl+K` 刪掉的文字 | ✅ 接著按 `Alt+Y` 可以輪替更早刪掉的內容。📌 **macOS 要先把終端機的 Option 設成 Meta** |
| 15 | `Ctrl+U` / `Ctrl+K` | 刪到行首 / 刪到行尾,刪掉的內容都會先存起來 | 📌 影片字幕這段聽不清,依官方是這兩個鍵。macOS 的 iTerm2 與 Terminal.app 把 `Cmd+Backspace` 對應到 `Ctrl+U` |
| 16 | `Esc` `Esc`(有字時) | 連按兩下清空輸入框,**草稿存進歷史**,用 `↑` 叫得回來 | ✅ 兩下要連著按 |
| 17 | `Ctrl+C`(沒在跑東西時) | 清空輸入框;在空輸入框按 `↑` 找回草稿 | ✅ 找回功能需 v2.1.288 以上。⚠️ **再按一次 `Ctrl+C` 會直接退出 Claude Code** |
| 18 | `:rocket:` | 打完整 shortcode 自動變成 🚀;打 `:` 加兩個字母會跳候選,`Tab` 插入 | ✅ 需 v2.1.217 以上。shortcode 必須在開頭或空白之後,所以網址裡的 `:` 不會觸發。整段貼上不會轉換。可用 `emojiCompletionEnabled: false` 關掉 |

> 📌 readline 這套按鍵自 **v2.1.261** 起是預設行為,舊的 `keybindingFlavor` 設定已失效。

---

## 5. 輸入框裡的入口(19–22)

| # | 操作 | 作用 | 📌 對照官方文件 |
|---|---|---|---|
| 19 | 空輸入框按 `?` | 列出快捷鍵清單 | ✅ 輸入框有字時,`?` 就只是打出問號 |
| 20 | 句子中間打 `空白` 加 `/` | 一樣會跳斜線指令補全,`Tab` 補上 | ✅ 官方:在單獨的句中 `/` 按 `Tab` 會列出所有指令。**只有放在開頭才會真的執行**,放中間只是文字,Claude 看得到你提了它 |
| 21 | 開頭打 `!` | **Shell 模式**:直接跑終端機指令,輸出進對話,Claude 會順手看結果 | ✅ shell 模式下按 `Tab` 會從**這個專案跑過的 `!` 指令**補全;路徑含 `/` 時會跳檔案補全。Windows 也用 `/`。空輸入框按 `Esc`、`Backspace` 或 `Ctrl+U` 離開 |
| 22 | 灰字建議按 `Tab` 或 `→` | Claude 回完後猜你下一步要說什麼,接受後再 `Enter` 送出;直接打字就消失 | 📌 官方補充:每個建議都是**用同一模型發的背景請求,會計入用量**。快到用量上限時會自動不出,也可能預設關閉 |

---

## 6. 模型與思考力度(23–25)

| # | 操作 | 作用 | 📌 對照官方文件 |
|---|---|---|---|
| 23 | `Option+P`(macOS)/ `Alt+P`(Windows、Linux) | prompt 寫到一半直接跳模型選擇器,輸入框的字不會被清掉 | 📌 **macOS 要把終端機的 Option 設成 Meta 才有效**(官方 terminal-config 有各終端機設定方式) |
| 24 | 選擇器裡 `←` `→` 調思考力度;`Enter` 或 **`s`** | `Enter` 會**存成以後所有新 session 的預設**;小寫 `s` **只套用這次 session** | ✅ `/model <名稱>` 直接打等同 `Enter`。`s` 需 v2.1.257 以上 |
| 25 | `/effort` 不帶參數 | 跳出力度滑桿,`s` 只套用這次;**`Tab` 切換 Ultracode** | ✅ Ultracode 是設定而非力度檔位,切換時力度不變。滑桿的 Tab 開關需 v2.1.284 以上。影片說開了之後每個任務會自動安排多個 agent 一起做、用量多很多,與官方「讓 Claude 自己決定要不要開工作流」的說法一致 |

---

## 7. 翻舊帳、找東西、管 session(26–30)

| # | 操作 | 作用 | 📌 對照官方文件 |
|---|---|---|---|
| 26 | 空輸入框 `Esc` `Esc` | 打開**回退選單**:列出你送過的每則訊息,選一則就把對話與程式碼還原到那之前 | ✅ 官方叫 rewind,還能選「摘要」 |
| 27 | `Ctrl+O` | transcript 詳細紀錄:每個工具呼叫、指令、每則回覆用的模型與時間 | 📌 在裡面按 `?` 看說明、`{` `}` 跳到上一個或下一個 prompt、`v` 用編輯器開整段對話、`[` 把整段寫進終端機原生捲動區,**這些都要全螢幕渲染**。`/` 搜尋也在這裡 |
| 28 | `Ctrl+R` | 搜尋以前送過的 prompt,`Enter` 填回輸入框可再修改 | 📌 **`Ctrl+S` 切換範圍(這個 session、這個專案、所有專案)只在全螢幕渲染有效**;一般渲染器的行內搜尋固定搜所有專案 |
| 29 | `PgUp` / `PgDn`,MacBook 用 `Fn+↑` / `Fn+↓` | 一次捲半屏。捲上去後新輸出不會把你拉回底部,底部出現 `Jump to bottom` | 📌 外接鍵盤 `Ctrl+Home` / `Ctrl+End` 跳到開頭或最新。⚠️ **Mac 鍵盤的 `Ctrl+End` 傳不到 Claude Code**,官方建議點按鈕、滾到底或自行改綁 `scroll:bottom` |
| 29b | `/diff` 加 `Ctrl+X B` | 旁邊打開改動面板,列出改了哪些檔、加減幾行;`Ctrl+X B` 切換比較基準:這個 session、所有未提交改動、整條分支 | 📌 面板需要**全螢幕渲染、git repo、終端機至少 110 欄、v2.1.287 以上**;會記住每個 repo 選的基準 |
| 30 | 空輸入框按 `←` | 進入 **Agent 視圖**:所有 session 依狀態排好,哪個在等你、哪個在跑、哪個跑完一眼可見;原本的 session 轉背景繼續跑 | ✅ 視圖裡:`Ctrl+S` 切換依狀態或依目錄分組、`Ctrl+T` 置頂、`Ctrl+F` 依名稱找、`Ctrl+R` 改名(後兩者需 v2.1.288)。📌 置頂也會讓該 session 閒置時**繼續保持執行**;在視圖裡按 `Ctrl+X` 是停止 session,兩秒內再按會刪除,要小心 |

> 📌 **全螢幕渲染怎麼開:** 執行 `/tui fullscreen`,會在保留對話的情況下重啟;`/tui default` 切回。2026-05-06 之後才開始用 Claude Code 的人多半預設已是全螢幕。它還在 research preview 階段。

---

## 8. 應用案例

### 案例一:長任務跑測試時順便問問題

你叫 Claude 跑一組 30 秒的整合測試,同時想問「這個 API 的 timeout 預設多少」:

1. 正在寫的長需求先按 `Ctrl+S` 暫存。
2. 打問題後按 `Ctrl+Enter`;終端機不支援就按 `Ctrl+X Ctrl+S`。測試自動轉背景,Claude 先回答你。
3. 回答完,在空輸入框再按 `Ctrl+S` 把剛才的長需求叫回來。

如果只是想確認對話裡講過的東西,例如「剛剛那個設定檔叫什麼」,改用 `/btw`,不佔主對話的 context。

### 案例二:Claude 改壞了,要倒回去

Claude 連改三個檔後測試全紅:

1. 在空輸入框按 `Esc` `Esc` 打開回退選單,選「請它重構 auth」那則訊息之前,對話與程式碼一起還原。
2. 如果開了一堆背景子 agent 而方向錯了,先按兩次 `Ctrl+X Ctrl+K` 全部停掉,再回退。

### 案例三:同時開五個 session 做不同 repo

1. 每個 session 開工後,空輸入框按 `←` 進 Agent 視圖。
2. `Ctrl+S` 改成依目錄分組;用 `Ctrl+R` 把 session 改名成「前端-登入頁」「後端-計費」這類好記的名字。
3. 最常回來看的那個用 `Ctrl+T` 置頂。
4. 「Needs input」那一組有東西時才切過去處理,其他讓它們在背景跑。

### 案例四:Windows 使用者的對照

照著 Mac 影片學時,要換成這樣:

| 影片(macOS) | Windows |
|---|---|
| `Option+P` | `Alt+P` |
| `Ctrl+Z` 加 `fg` | 沒有這個功能,另開一個終端機分頁 |
| `Option+Delete` 刪一個字 | `Ctrl+Backspace` |
| `Shift+Tab` 切模式 | 一樣;若沒反應,改用 `Alt+M` |

其餘 `Ctrl` 開頭的鍵、`Ctrl+X` 和弦兩邊都一樣。安裝相關的坑見 [[claude-code-windows-native-install-troubleshooting]]。

### 案例五:把常用鍵改成自己的習慣

執行 `/keybindings` 開啟 `~/.claude/keybindings.json`,存檔後免重啟生效。例如不想讓 `Ctrl+S` 被暫存佔走:

```json
{
  "bindings": [
    { "context": "Chat", "bindings": { "ctrl+s": null, "ctrl+e": "chat:externalEditor" } }
  ]
}
```

`Ctrl+C`、`Ctrl+D` 等是保留鍵,不能改。

---

## 9. 補充:AI LABS 整理的隱藏「設定」與指令,逐項對官方文件(2026-11-06 增補)

> 來源影片:〈Claude Code Features That 90% Don't Know Exist〉(**AI LABS**,2026-10-05,約 16.4 分鐘;無官方字幕,逐字稿以 CPU 版 Whisper 轉錄,可能有同音字誤差;「Claude API prompt audit」「hill climb」等已依官方指令名還原)。
>
> **立場揭露:** 片中 Scrimba「Explain」(把程式碼轉成旁白影片的 AI 工具)為業配,**不轉述**;另宣傳其付費社群 AI Labs Pro。
>
> 本篇前八節偏**按鍵**;這支影片偏**設定檔與斜線指令**,兩者重疊的按鍵(`Ctrl+S` 暫存、`Ctrl+Y` 取回、`Ctrl+_` 復原)不再重複。2026-11-06 對照 [Commands](https://code.claude.com/docs/en/commands)、[Settings](https://code.claude.com/docs/en/settings)、[Model config](https://code.claude.com/docs/en/model-config)、[Env vars](https://code.claude.com/docs/en/env-vars) 查核。

### 9.1 專案設定與「清垃圾」

| 影片的功能 | 官方文件核實 | 備註 |
|---|---|---|
| `CLAUDE_CODE_NEW_INIT=1` 後 `/init` 先問問題、擬計畫、再寫 `CLAUDE.md`、skills、hooks | ✅ 環境變數存在,「互動流程,詢問要產生哪些檔案(CLAUDE.md、skills、hooks),再探索程式碼並寫入」 | 影片說**要在輸入 `claude` 之前設**,正確(環境變數)。不設則直接自動產生 `CLAUDE.md` |
| `/import <agent>` 從別的 agent 搬設定 | ✅ `/import [codex\|gemini\|cursor] [--dry-run] [--yes]`,搬指令檔、MCP、commands、subagents、skills | `/init` 偵測到 Codex 或 Gemini CLI 設定時也會主動提議 |
| `/claude-api prompt-audit`:用 subagent 稽核 `CLAUDE.md` 與 skills 有無過期指令 | ✅ `/claude-api` 子命令清單有 `prompt-audit`;另有 `/doctor prompt-audit [path]`(v2.1.283+) | 新模型剛出時最該跑——舊指令最容易過期。可對照本庫 [[claude-md-cut-82-percent-and-maintain-it]] |
| `/skill-doctor`:看每個 skill 的使用頻率、最後使用時間、佔用 context | ✅ 存在,需 v2.1.252+ 與功能旗標抓取 | 見 [[skill-doctor-self-improving-agent-loop]] |
| `/skills` 後按 `T` 依 token 排序 | ✅ 官方 [Commands](https://code.claude.com/docs/en/commands) 寫的是**小寫 `t`** 依 token 數排序(影片字幕寫大寫 `T`,以官方為準);排序方向(影片說遞增)文件未載,未核實 | 按 `Space`/`Enter` 可切換技能對 Claude 與 `/` 選單的可見度 |

### 9.2 權限與 context 預算

| 影片的功能 | 官方文件核實 | 備註 |
|---|---|---|
| `/auto-mode setup`:讀專案與過往 session,草擬 Auto mode 規則,審閱後存入使用者設定 | ✅ 指令實名為 **`/auto-mode-setup`**(草擬 `autoMode.environment` 項目,存到 user settings;v2.1.228+) | 影片的「從 Auto mode 啟動」呼應本篇姊妹篇 [[claude-code-2026-feature-timeline]] §8.5(Auto mode 成為預設) |
| `/fewer-permission-prompts`:掃過往 transcripts,只挑**唯讀**的 Bash / MCP 呼叫,寫入 allow list | ✅ 官方描述幾乎同句,寫入**專案** `.claude/settings.json` | 與 auto mode 設定是兩條互補路徑:前者改分類器規則,後者加白名單 |
| `disableClaudeAiConnectors: true`:不載入 Claude 網頁版連接器(Notion、Slack 等)進 Claude Code,省 context | ✅ 設定鍵存在;**任何範圍設 true 都生效,連 managed 設 false 也擋不住** | 連接器被載入卻沒用,白占 token(對應本篇姊妹 [[token-saving-three-moves-context-control]] 的「丟掉用不到的」) |
| `enableArtifact: false`:關掉 Artifact 工具 | ✅ 鍵存在;「任何檔案設 false,沒有檔案能再打開」,需 v2.1.242+ | 影片說設在 `~/.claude/settings.json`;注意**一旦被關,低層級無法再開** |
| `/claude-api build-eval`、`hillclimb`:建一組測試、反覆改 app 並只保留分數更高的變更 | ✅ `build-eval`、`hillclimb` 為官方子命令(影片寫 hill climb) | 影片警告:**每次執行都呼叫模型,會花 API 費用**;若你的 app 不呼叫模型,`build-eval` 仍可產出測試計畫而不耗 API(影片說法,我未實測) |

### 9.3 計畫模式與輸出

| 影片的功能 | 官方文件核實 | 備註 |
|---|---|---|
| `showClearContextOnPlanAccept: true`:接受計畫時恢復「先清 context 再實作」選項 | ✅ 設定鍵存在(索引列:Show a "clear context" option on the plan accept screen) | 清掉對話後計畫不會消失 |
| `plansDirectory`:把計畫存到專案內指定資料夾 | ✅ 設定鍵存在(Choose where plan mode writes plan files) | 預設存在使用者 `.claude/plans`,設到專案內才能與團隊共享 |
| `/output-style [style]` 五種風格:default、proactive、concise、explanatory、learning | ✅ 指令存在(v2.1.269+)。官方 [Output styles](https://code.claude.com/docs/en/output-styles) 確認五種:Default(預設)加 Proactive、Concise(v2.1.237+)、Explanatory、Learning 四個內建風格 | ⚠️ 設定檔 `outputStyle` 的值**區分大小寫**(要寫 `Explanatory`,寫 `explanatory` 會退回 Default);`/output-style` 指令則不分大小寫。與 [[output-style-communication-not-intelligence]] 並讀 |
| `showThinkingSummaries: true` 後 `Ctrl+O` 看思考摘要 | ✅ 預設 `false`;未設時 API 會遮蔽思考區塊,只顯示摺疊占位 | 官方註明遮蔽只影響**你看到的**,不影響模型實際產生量 |
| `/tui fullscreen` + `/focus`:只顯示最後的 prompt、一行工具摘要、最終回覆 | ✅ 兩者皆存在;focus 設定會跨 session 保存 | 影片說「focus 只在全螢幕可用」,與文件的 `/tui fullscreen` 搭配一致 |

### 9.4 平行與多 session

| 影片的功能 | 官方文件核實 | 備註 |
|---|---|---|
| `/branch`:複製目前對話開新分支,可用 `/resume` 回原本 | ✅ | 會切進分支 |
| `/fork [prompt]`:把對話複製成**背景 session**,有 prompt 就立刻開工 | ✅ 官方 [Commands](https://code.claude.com/docs/en/commands) 與 [Agent view](https://code.claude.com/docs/en/agent-view) 確認 | 📌 **需修正**:影片說「完成後背景 session 自己結束」。官方寫的是任務完成後 session 留在 agent view 的 `Completed` 群組,閒置約一小時後程序可能被停止、對話保留,直到你再回覆或 attach 才續跑;需刪除才會消失。另,關掉 agent view 時 `/fork` 改為啟動 forked subagent。詳見 §9.7 |
| `/subtask <task>`:起一個繼承**完整對話**的 forked subagent,結果回到本對話 | ✅ | 一般 subagent 從乾淨 context 開始,只拿到主 agent 給的 prompt;`/subtask` 是例外 |
| `/list-agents`:列出可傳訊的 subagent、teammates 與其他 session,可請一個 session 傳話給另一個 | ✅ 別名 `/peers`;需 v2.1.224+ | 見 [[claude-code-2026-feature-timeline]] §8.1 跨 session 訊息 |
| `askUserQuestionTimeout`:Claude 提問閒置到時自動採用建議答案繼續 | ✅ 設定鍵存在,範圍**僅使用者或 managed** | 影片說「只在不阻塞時才自動選」——細節我**未核實** |
| `/config` → 本機通知 → terminal bell | ❓ 未逐項核實 | |

### 9.5 模型分工與省額度

- **`/model opusplan`**:✅ 官方 [Model configuration](https://code.claude.com/docs/en/model-config):plan mode 用 `opus` 做複雜推理與架構決策,執行階段自動切到 `sonnet`;兩階段的脈絡視窗各依對應模型。用 `/model` 設定需 Claude Code v2.1.265+。「要 1M 可用 `opusplan[1m]`」一句,官方段落未見此寫法,**未核實**。注意**換模型會讓該模型的 prompt cache 重算**(Settings 文件的提醒)。
- **`CLAUDE_CODE_SUBAGENT_MODEL` + `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`**:✅ 官方 [Sub-agents](https://code.claude.com/docs/en/sub-agents) 的模型優先序(v2.1.251 起):①呼叫時傳入的 `model` 參數 → ②subagent 定義檔的 `model` frontmatter → ③`CLAUDE_CODE_SUBAGENT_MODEL` → ④主對話的模型。也就是環境變數只是**預設值**,不會蓋過①②。要讓所有 subagent 都用同一個模型,要再設 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`(需 v2.1.257+),此時會忽略定義檔的 `model` 欄位。官方範例放在 settings.json 的 `env` 區塊。影片說「不設 FORCE,subagent 自己的檔案仍可選別的模型」與上述一致。
- **`/powerup`**:✅ 官方指令名是 `/powerup`(不是 power up 兩個字),互動式小課程附動畫示範。

### 9.6 應用案例

**案例 1|新模型上線當天的 15 分鐘保養**:①`/doctor prompt-audit`(或 `/claude-api prompt-audit`)掃出對新模型多餘的規則 ②`/skill-doctor` 刪掉久未使用且 token 重的 skill ③`disableClaudeAiConnectors` 關掉沒用的連接器 ④再看一次 `/context`。目的:**把每輪都要重送的固定成本降下來**。

**案例 2|讓一個晚上跑的長任務不被一個問題卡住**:`askUserQuestionTimeout` 設 60 秒(僅能放使用者或 managed 設定)+ `/config` 開本機通知 + `/fewer-permission-prompts` 預先把唯讀指令放行。**注意**:真正需要你決定的問題它還是會等,不要期待它替你做重要選擇。

**案例 3|計畫與實作分檔、分模型**:`plansDirectory` 指到專案內 `docs/plans`(進版控、給同事看)、`showClearContextOnPlanAccept` 打開讓實作從乾淨 context 開始、`/model opusplan` 讓規劃用 Opus、實作用 Sonnet;subagent 用 `CLAUDE_CODE_SUBAGENT_MODEL=haiku` + `_FORCE=1` 做大量搜尋。

**案例 4|試另一種做法又不丟現場**:`/branch` 試新方向、需要側任務用 `/subtask`(要完整上下文)或 `/fork <prompt>`(要獨立背景 session)。

**核實狀態(2026-11-07 更新):** ✅ 大多數設定鍵與指令皆有官方文件依據(多項僅核到「索引列」描述,型別與預設值未逐一核)。已由 ❓ 改為 ✅:`/skills` 排序鍵(官方為小寫 `t`)、output style 五種名稱。📌 需修正:`/fork` 完成後**不會**自己結束(留在 agent view)。❓ 仍未核實:`/skills` 排序方向、`askUserQuestionTimeout` 的「僅在不阻塞時」(官方只寫「閒置後讓未回答的問題自動繼續」)、`opusplan[1m]` 寫法、terminal bell 路徑。⚠️ 指令名稱修正:`/auto-mode-setup`、`/powerup`、`hillclimb`(`/claude-api` 的子命令)。

### 9.7 延伸閱讀與深度補充(2026-11-07 核實增補)

影片 [i6Q7bXnWGlM](https://www.youtube.com/watch?v=i6Q7bXnWGlM)(約 16 分鐘)是**無官方字幕**的自動轉錄,已依官方文件查核設定鍵與指令;畫面部分見下方「畫面核對」。以下只列**真的讀過官方頁面**後比影片多出或更正的內容。時間點皆來自 `transcript_tools.py find` 的精確時間。

**A. 設定鍵的「作用範圍」與「單向開關」(官方 [Settings](https://code.claude.com/docs/en/settings) 的 Exceptions 表)**

| 鍵 | 官方規則 | 對使用者的意義 |
|---|---|---|
| `disableClaudeAiConnectors` | `true` 從任何範圍都生效,**即使 managed 設 `false` 也擋不住** | 專案檔設 `true` 也會生效,不必動使用者檔 |
| `enableArtifact` | `false` 從任何範圍都生效;**沒有任何檔案能再把它打開**;需 v2.1.242+ | 設過後,低層級的檔案無法再開;[6:21](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=371s) 影片說法正確 |
| `askUserQuestionTimeout` | 範圍僅 **user 或 managed**,專案檔無效(與影片「寫在 `settings.json`」一致,但不可放專案檔) | [13:08](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=778s) 影片說的「寫在 main .claude 資料夾」即使用者層級 |
| `showClearContextOnPlanAccept`、`plansDirectory`、`showThinkingSummaries` | 任何檔案皆可;`showThinkingSummaries` 預設 `false`,未開時 API 會遮蔽思考區塊,官方註明只影響**你看到的**內容 | 影片 [7:49](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=459s)、[8:26](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=496s)、[10:22](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=612s) 的設定鍵名正確 |

**B. 四種「岔開」方式的差別(官方 [Commands](https://code.claude.com/docs/en/commands) 與 [Agent view](https://code.claude.com/docs/en/agent-view))**

| 指令 | 結果 | 回報去向 |
|---|---|---|
| `/branch [name]` | 複製對話並**切進去**,原對話用 `/resume` 回得去 | 你自己接手 |
| `/fork [prompt]` | 複製成**背景 session**,在 agent view 裡跑;兩邊獨立。除非選擇原地編輯,否則 Claude 會指示它先建立自己的 git worktree(`.claude/worktrees/`) 再改檔 | 完成後留在 `Completed` 群組,官方未寫會自動刪除 |
| `/subtask <task>` | 背景 forked subagent,繼承完整對話 | **結果回到目前對話** |
| 一般 subagent | 乾淨 context,只拿到主 agent 給的 prompt | 結果回到目前對話 |

影片把 `/fork` 說成「完成後自己結束」([11:49](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=699s)),**需修正**如上。`/branch` 與 `/fork` 的差別([11:21](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=671s)、[11:36](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=686s))則與官方一致。

**C. 模型分工的兩個細節**
- `opusplan` 只控制**主對話**的 plan / 執行切換;subagent 的模型依 §9.5 所列四層順序決定,與 `opusplan` 無關。
- `CLAUDE_CODE_SUBAGENT_MODEL` 單獨設定時,**不會改變內建 Explore、Plan 兩個 subagent 的模型**(官方明寫)。影片 [14:38](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=868s) 未提這點。兩個變數都設時,subagent 跑 `CLAUDE_CODE_SUBAGENT_MODEL` 指定的模型;只設 `_FORCE` 時,subagent 跑主對話的模型,但內建 Explore 仍跑它自己列出的模型(官方明寫)。

**D. 輸出風格的大小寫陷阱**:見 §9.3 表格。影片把五種風格都列出來,正確;但它沒提設定檔值區分大小寫。

**畫面核對(已截圖 5 格,截圖秒數 180、333、459、778、868 s)**:[3:00](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=180s)、[5:33](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=333s)、[7:39](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=459s)、[12:58](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=778s)、[14:28](https://www.youtube.com/watch?v=i6Q7bXnWGlM&t=868s) 的畫面是**示意動畫與卡片**,無可讀的設定鍵名或指令拼法;因此**設定鍵與指令名稱的正確性全部以官方文件為準,未以畫面核對**。

**E. 未能核實清單**
- `askUserQuestionTimeout` 是否「只在不會阻塞時才自動選」:官方索引只寫「閒置後讓未回答的問題自動繼續」,未能核實。
- `/fork` 的「任務完成後自動結束」:官方不是這樣寫,已改為需修正。
- `opusplan[1m]`:未能核實。
- `/skills` 的 `t` 排序方向(遞增或遞減):未能核實。
- `/doctor prompt-audit`(v2.1.283+)與 `/claude-api prompt-audit` 功能重疊:官方兩者皆列出,未比較輸出差異。

**來源(9.7 新增)**
- [Commands](https://code.claude.com/docs/en/commands)、[Settings](https://code.claude.com/docs/en/settings)、[Settings reference](https://code.claude.com/docs/en/settings-reference)、[Model configuration](https://code.claude.com/docs/en/model-config)、[Sub-agents](https://code.claude.com/docs/en/sub-agents)、[Agent view](https://code.claude.com/docs/en/agent-view)、[Output styles](https://code.claude.com/docs/en/output-styles)(2026-11-07 查核)

來源:[AI LABS〈Claude Code Features That 90% Don't Know Exist〉](https://www.youtube.com/watch?v=i6Q7bXnWGlM)(2026-10-05)—— **該片無官方字幕,逐字稿以 CPU 版 Whisper 轉錄,可能有同音字誤差**;[Commands](https://code.claude.com/docs/en/commands)、[Settings](https://code.claude.com/docs/en/settings)、[Settings reference](https://code.claude.com/docs/en/settings-reference)、[Env vars](https://code.claude.com/docs/en/env-vars)、[Model config](https://code.claude.com/docs/en/model-config)。

---

## 延伸閱讀(本庫)

- [[claude-code-mods-explained]]:Claude Code 的 mod 機制;diff 面板就是內建 mod `cc-plugin-diff` 畫的。
- [[claude-code-2026-feature-timeline]]:2026 年各功能上線時間軸。
- [[claude-code-windows-native-install-troubleshooting]]:Windows 原生安裝的坑(同為 YAHA學堂)。

---

## 來源

- YouTube:[Claude Code 教程:30个隐藏最深功能,有些你一次都没用过](https://www.youtube.com/watch?v=Lx22N9R_0As)(YAHA學堂,2026-10-17)
  - 該片只有自動字幕;自動字幕連續 3 次 HTTP 429,改以 CPU 版 Whisper(faster-whisper)轉錄,非官方字幕,可能有少量聽寫誤差。按鍵名稱一律以官方文件為準。
- 官方文件(2026-10-18 查核):
  - [Interactive mode](https://code.claude.com/docs/en/interactive-mode)
  - [Customize keyboard shortcuts](https://code.claude.com/docs/en/keybindings)
  - [Model configuration](https://code.claude.com/docs/en/model-config)
  - [Fullscreen rendering](https://code.claude.com/docs/en/fullscreen)
  - [Agent view](https://code.claude.com/docs/en/agent-view)
  - [Setup](https://code.claude.com/docs/en/setup)
- Claude Code 官方 repo:<https://github.com/anthropics/claude-code>
