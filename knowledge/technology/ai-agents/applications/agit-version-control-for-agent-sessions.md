# Agit:把 Git 那套用在「和 agent 的對話」上,以及影片沒講的兩個坑

> 整理自 YouTube 頻道 **AI LABS**〈[This New Open Source Tool Just Fixed Your Claude Code Workflow](https://www.youtube.com/watch?v=CHHEjuNBxoQ)〉(2026-09-22,約 12.4 分鐘)。
> **該片自動字幕下載連續遇到 HTTP 429,逐字稿改以 CPU faster-whisper 轉錄英文原音取得,非官方字幕。**
>
> ⚠️⚠️ **立場揭露:該片有 Runable 業配段落;片中做的「密碼登記 skill」與示範用的專案範本需加入付費社群 AI Labs Pro 才能取得。**
>
> ⭐⭐⭐ **本文已 `git clone` [Einsia/agent-git](https://github.com/Einsia/agent-git) 讀過 README 與 `docs/`**,
> ⚠️⚠️ **抓到兩件影片沒講、但會影響使用的事**(見 §五):
> **① 影片說 Agit 會漏掉密碼、要靠他們的 skill 解決 —— 其實 Agit 內建 `agit secrets add` 專門處理這件事;**
> **② 影片教的「revert 之後 resume」,在同一台電腦上 revert 可能不會生效。**

---

## 一句話總結

> ⭐⭐⭐ **官方 README 的定位:「對每一個 agent session 做無損的版本控制:可以發布、可以接續。」**
>
> ⭐⭐ **它要解決的問題影片講得很實際:把對話內容整理成交接文件給別人或另一個 agent 時,
> 「寫出來的檔案只留下重點,細節都不見了」。Agit 讓你直接交出整段對話。**

---

## 一、⭐ 基本資料(✅ 本文實查,2026-09-25)

| 項目 | 內容 |
|---|---|
| **倉庫** | `Einsia/agent-git` |
| **star** | **362**(⚠️ **2026-09-01 才建立**,還很新) |
| **授權** | **MIT** |
| **語言** | **Rust** |
| **支援的 agent** | **Claude Code、Codex、OpenCode、Cursor** |
| **官方標語** | **「Code is cheap, show me the talk」**(把 Linus 那句話倒過來) |

> ⭐ **為什麼需要它(✅ README 原文):
> 「在磁碟上,session 只是一堆 JSONL 檔,隨時可能被覆寫、壓縮、清掉。
> `agit` 在上面加上快照與版本,讓『上週三那段終於抓到 bug 的對話』變成可以找到、接續、交給隊友的東西。」**

---

## 二、⭐⭐ 概念對照:Git 管程式碼,Agit 管對話

| Git | ⭐ **Agit** |
|---|---|
| **repo 存程式碼與歷史** | **repo 存 agent 的對話,加上記憶與 skill** |
| **branch** | ⭐ **每個 session 一條 branch,同一個專案可以有多段互不干擾的對話** |
| **commit** | **存下訊息與 agent 做了什麼(一個「回合」)** |
| **push** | **上傳到 Hub,出現在你的個人頁** |
| **revert** | ⚠️ **只改對話,不動你的程式碼**(見 §五.2) |

> ⭐⭐ **影片強調的一點:「回到對話的早期,不會把你的 App 退回去。App 不變,只有 agent 看到的對話變了。」**

### ⭐ 兩個名詞(✅ 官方文件)

| 名詞 | 意思 |
|---|---|
| **settle** | **把「上次紀錄之後新增的對話」切成回合 commit**,指令是 `agit commit` |
| ⭐ **VIEW** | **agent 下次 resume 時實際看到的 context。它是推導出來的 —— `agit revert` 從 VIEW 拿掉東西時,原始紀錄(log)一個位元組都不會動** |

---

## 三、⭐⭐ 常用操作

### 3.1 安裝與設定

```sh
npx -y create-agit                   # 一次裝好 agit,並設定 skill / hook / MCP
# 或
npm install -g @einsia/agent-git     # 裝成全域套件
agit --version
```

⚠️ **官方特別提醒:不要裝 `@einsia/agentgit`(沒有連字號)** —— 那是改寫前的舊版,協定不相容。

⭐ **影片提到第一種安裝方式在他們那邊失敗,改用 npm 才成功。**

**登入與初始化:**

```sh
agit login        # 選瀏覽器登入
agit whoami       # 確認登入的帳號
agit init         # 在專案資料夾執行,設定 repo 名稱、是否自動 push、要寫進 AGENTS.md 還是 CLAUDE.md
```

> ⭐ **影片的做法:同時用 Codex 與 Claude Code,所以兩個檔案都寫。**

**✅ 官方文件:安裝時會設定這些東西**

| 項目 | 位置 | 作用 |
|---|---|---|
| **hooks** | `~/.claude/settings.json`、`$CODEX_HOME/hooks.json` | **SessionStart 登記 session,Stop 自動把一個回合存下來** |
| **skill** | `~/.claude/skills/agit/` 等 | **教 agent 用 `agit commit --milestone`** |

> 📎 **這裡用的正是 Stop hook —— 跟本庫 [[shopify-helix-checkpoints-and-gates]] 用來擋 agent 收工的是同一種事件,只是這裡拿來「存檔」。**

### 3.2 ⭐⭐ 查看與回退

```sh
agit log                         # 選一個 session,看它的每個回合
agit revert @#12.4 -m "這個結論是錯的"   # 把某些回合從 VIEW 拿掉
agit resume <branch>             # 繼續這段對話
agit push                        # 更新到 Hub
```

⚠️ **回退之後直接 resume,請先看 §五.2。**

### 3.3 ⭐⭐⭐ 把另一段對話的內容搬過來:cherry-pick

```sh
agit cherry-pick try-ratelimit#3..#4 -m "把 uid 改名那段拿過來"
```

> ⭐ **訊息和 agent 的回應(含它做過什麼)會一起加到目前 session 的最後。**
> ⚠️ **只複製對話紀錄,不會套用那些訊息裡做過或描述的程式改動。**

### 3.4 ⭐⭐⭐ 跨 agent 接續:從 Claude Code 換到 Codex

> **影片:「我們常常同時用 Codex 和 Claude Code。平常要叫 Claude 先寫一份交接文件,再叫 Codex 讀 ——
> Agit 讓你直接把對話帶進 Codex,不用自己寫交接。」**

```sh
agit resume ratelimit --as codex     # 換 runtime(它會先列出哪些東西會遺失)
```

**✅ 官方文件:換 runtime 是**有損**的,指令會先列出遺失清單。**
⭐ **影片說帶得過去的是訊息與工具紀錄,帶不過去的是模型的思考過程** —— ✅ 官方的 session 儲存文件也寫明回合雜湊**排除思考區塊與加密推理**。

> ⭐ **影片的小提醒:可以請 agent 幫你寫這條指令,但要**自己在終端機執行**,才能在另一個終端機接著對話。**

### 3.5 分享

| 方式 | 內容 |
|---|---|
| **加協作者** | **對方可以接續,再用 pull request 把他的部分送回你的 repo** |
| **唯讀連結** | **可以設定能開啟幾次,用完就失效** |
| **公開 repo** | ⚠️⚠️ **一旦公開就不能改回私人**(別人可能已經複製了歷史) |

⚠️ **影片說私人 repo 總共只有 1 GB 空間、公開 repo 沒有上限 —— 這是 Hub 服務的方案規定,本文無法從原始碼核實。**

---

## 四、⭐⭐ 密鑰保護:它自動擋得住哪些

> ⚠️ **agent 常常會讀到 API key 和密碼,一旦讀到就成了對話的一部分;把對話推上去,就等於把密鑰也分享出去。**

**✅ 官方文件:Agit 用 gitleaks 規則認出**已知格式**與**高熵值**的憑證,存檔時換成佔位符,推送前再檢查一次。**

> ⭐ **影片實測:用假的 API key 測試,存下來的歷史裡確實都被換成佔位符。**

### ⚠️ 自動偵測的盲點(影片說對了)

> **「API key 通常有可辨識的樣式,例如固定開頭與長度;但由普通單字組成的密碼沒有這些特徵。」**
>
> ✅ **官方文件也承認這點:「它刻意不把 `password = short` 或一句好記的通關語當成密鑰 ——
> 光看文字,無法分辨一般句子和使用者自己的密碼。」**

---

## 五、⚠️⚠️ 影片沒講的兩件事(本文讀原始碼文件後補上)

### 5.1 ⚠️⚠️⚠️ 密碼的問題,Agit 本身就有解法:`agit secrets add`

**影片說這是「工具本身的一個問題,以及我們怎麼解決它」,並介紹他們做的付費 skill。**

> ⭐⭐⭐ **但 Agit 本身就內建了一套「在這台裝置上手動登記密鑰」的機制,專門處理低熵密碼(✅ 官方文件,狀態:已實作):**

```sh
agit secrets add <名稱>            # 在終端機會用不回顯的方式讓你輸入
agit secrets add <名稱> --stdin    # 非互動環境用
agit secrets list
agit secrets remove <id 或名稱>
agit secrets status
```

| 規則 | 內容 |
|---|---|
| **比對方式** | ⭐ **任何 UTF-8 字串的子字串比對,不看格式、不看熵值** |
| **長度** | **預設至少 8 位元組;4–7 位元組要加 `--allow-short`;4 以下拒絕;上限 512** |
| ⭐ **安全設計** | **密鑰不能當指令參數傳入(避免留在 shell 歷史與行程列表);存放在加密保險庫,主金鑰放在作業系統的憑證管理(Windows 是認證管理員)** |
| **作用範圍** | **推送前的檢查、`agit share` 分享前檢查、匯出的遮蔽副本,都用同一套比對** |

**⭐ 另外還有「repository 層級的可還原佔位符」(✅ 官方文件,已實作):**

> **登記過的值與啟發式偵測到的候選值,會進入 repository 字典:
> **本機繼續看到真實值,Git 與 Hub 只看到佔位符**。**

> ⭐⭐ **所以影片的 skill 做的事,本質上是**提醒 agent 在對話中遇到密碼時,先幫你登記進去** ——
> 這個自動化有價值,但底層機制是 Agit 本來就有的,不是額外補上的漏洞修補。**
> ⭐ **不想用他們的 skill,可以自己在開始 session 前手動 `agit secrets add` 你專案會用到的密碼。**

### ⚠️ 關於「事後才登記」

**影片說:「一旦 Agit 已經把密碼存進歷史,之後再加 skill 也不會把它移除;就算刪掉那則訊息,密碼仍會留在歷史裡。」**

> ✅ **這點屬實**:官方文件寫明「保護新的快照,不會移除舊的明文物件」。
> ⭐⭐ **但文件同時寫了影片沒提的另一半:「push 會檢查**整個**要送出的歷史,而且不會改寫它。」**
> **也就是說,事後登記的密碼雖然留在本機歷史裡,**推送時會被擋下來**,不會悄悄傳上去。**

### 5.2 ⚠️⚠️⚠️ 在同一台電腦上 revert 之後 resume,revert 可能沒生效

**影片教的流程是:`log` 找到回合 → `revert` 拿掉 → `resume` 繼續。**

> ⚠️⚠️ **官方文件寫了一個關鍵例外:**
> **「如果原生 session 還在這台電腦上,resume 會走零複製路徑(直接 `claude --resume <id>`),
> 這條路徑**重用原生 transcript、繞過 VIEW** —— 所以 `agit revert` 剛從 VIEW 拿掉的東西,
> 在這台電腦上零複製 resume 的 session 裡**仍然看得到**。」**
>
> ⭐ **要讓 revert 生效,必須走「重新產生」的路徑:**換一台電腦、merge、`--as`、`--cwd` 都會觸發**。**

```sh
# 在同一台電腦上,想讓 revert 真的生效:
agit resume <branch> --cwd <同一個專案路徑>   # --cwd 會觸發重新產生
```

⚠️ **上面這個寫法是本文依文件推論,**未實測**;官方文件只說 `--cwd` 會觸發重新產生路徑。**

> ⚠️⚠️ **這個坑很容易讓人以為 revert 壞掉了 —— 你以為拿掉的錯誤結論,agent 其實還看得到。**

### ⭐ 另一個相關的設計

> ✅ **官方:`resume` 只接受 branch;tag、歷史 commit、`#n` 都會被拒絕,要改用 `fork`。
> 理由是「歷史不改寫 —— 想回到舊狀態,就長出一條新的線,而不是把舊線彎回去」。**

```sh
agit fork 21d8a51 -b ratelimit-retry --resume   # 從某個歷史點開一條新 branch 並直接啟動
```

---

## 應用案例

### 案例 1|⭐⭐⭐ 把「交接文件」換成「整段對話」

| 以前 | 用 Agit |
|---|---|
| **叫 Claude 寫一份交接摘要 → 給 Codex 讀** | **`agit resume <branch> --as codex`** |
| ⚠️ **摘要只留重點,細節不見** | ⭐ **訊息與工具紀錄都帶過去(思考過程除外)** |

### 案例 2|⭐⭐ 開工前先登記密碼

```sh
agit secrets add staging-db-password
agit secrets add admin-passphrase
```

> ⭐⭐ **只要專案裡有「普通單字組成的密碼」,就在開始 session 之前登記。
> 事後才登記,舊歷史裡的明文不會消失(但推送時會被擋)。**

### 案例 3|⭐⭐ 從一段失敗的嘗試裡,只撿有用的部分

```sh
agit log                                  # 找到那段對話裡有用的回合
agit cherry-pick try-ratelimit#3..#4 -m "只拿 uid 改名的結論"
```

> ⭐ **比整段 resume 乾淨:只把那幾個回合的結論帶進目前 session。記得它不會套用程式改動。**

---

## 重點回顧(TL;DR)

1. ⭐⭐ **Agit 把 Git 的概念套在 agent 對話上**:一個 session 一條 branch、一個回合一個 commit、push 到 Hub 分享。支援 Claude Code、Codex、OpenCode、Cursor。
2. ⭐ **它解決的問題**:交接文件只留重點、細節流失;Agit 讓你直接交出整段對話。
3. ⭐ **revert 只改對話(VIEW),不動程式碼,原始 log 也一個位元組都不變。**
4. ⭐⭐ **cherry-pick** 可以把另一段對話的某幾個回合搬過來,**只搬對話,不套用程式改動**。
5. ⭐⭐⭐ **跨 agent**:`agit resume <branch> --as codex`,換 runtime 是有損的,會先列遺失清單;**思考過程帶不過去**。
6. ⭐ **分享**:協作者 + pull request、可限次數的唯讀連結;⚠️ **公開後不能改回私人**。
7. ⭐ **自動密鑰遮蔽**用 gitleaks 規則,認得出有格式的 API key,**認不出普通單字組成的密碼**(官方也承認)。
8. ⚠️⚠️⚠️ **補正一:密碼問題 Agit 本身就有解法 —— `agit secrets add`**,不看格式、做子字串比對,存在加密保險庫。**影片的付費 skill 只是自動提醒 agent 去登記。**
9. ⭐ **事後才登記**:舊歷史裡的明文不會被移除(影片說對了),**但 push 會檢查整個歷史並擋下**(影片沒說)。
10. ⚠️⚠️⚠️ **補正二:同一台電腦上 revert 後直接 resume,revert 可能沒生效** —— 零複製路徑會繞過 VIEW;換電腦、merge、`--as`、`--cwd` 才會重新產生。
11. ⚠️ **很新的專案**:2026-09-01 建立、362 star;**不要裝沒有連字號的 `@einsia/agentgit`(舊版)**。

---

## 核實狀態

### ✅ 已核實(clone 後讀 README 與 `docs/`)

| 項目 | 來源 |
|---|---|
| **定位、支援的 agent、JSONL 會被覆寫的問題** | ✅ README |
| **兩種安裝方式、舊套件名警告** | ✅ README |
| **hooks 與 skill 的安裝位置、Stop hook 自動存回合** | ✅ `docs/00_usage.md` |
| **settle / VIEW 的定義、revert 不動原始 log** | ✅ `docs/00_usage.md` |
| ⭐⭐ **零複製 resume 會繞過 VIEW,revert 不生效** | ✅ `docs/00_usage.md` |
| **`--as codex` 換 runtime 會先列遺失清單** | ✅ `docs/00_usage.md` |
| **思考區塊不進回合雜湊** | ✅ `docs/02_session_store.md` |
| ⭐⭐ **`agit secrets add/list/remove/status` 與長度規則、加密保險庫** | ✅ `docs/05_global_secret_filter.md`(狀態:已實作) |
| **repository 字典:本機真實值、遠端佔位符** | ✅ `docs/06_repository_secret_dictionary.md`(狀態:已實作) |
| **「保護新快照不移除舊明文;push 檢查整個歷史」** | ✅ `docs/06_repository_secret_dictionary.md` |

### ⚠️ 未能核實

- ⚠️ **私人 repo 1 GB、公開 repo 無上限** —— Hub 服務的方案規定,不在原始碼裡。
- ⚠️ **影片的付費 skill 實際做了什麼** —— 無法取得,本文依影片描述推斷它是在呼叫登記機制。
- ⚠️ **§五.2 用 `--cwd` 讓 revert 生效的寫法** —— 依文件推論,**未實測**。
- ⚠️ **本文未實際安裝或執行 Agit。**

> 📌 **⭐ 依本庫慣例,clone 已在整理完成後刪除,未進版控。**

---

## 來源

- [This New Open Source Tool Just Fixed Your Claude Code Workflow — AI LABS](https://www.youtube.com/watch?v=CHHEjuNBxoQ)(2026-09-22,約 12.4 分鐘;**自動字幕連續 HTTP 429,逐字稿以 CPU faster-whisper 轉錄英文原音取得**)
- ⚠️ **立場**:該片含 Runable 業配;密碼登記 skill 與專案範本在付費社群 AI Labs Pro。
- ⭐⭐⭐ **一手素材(已 clone 讀過)**:[Einsia/agent-git — GitHub](https://github.com/Einsia/agent-git)(MIT,Rust,本文查詢時 362 star)
  - `docs/00_usage.md`(指令與 VIEW / 零複製 resume 的例外)
  - `docs/05_global_secret_filter.md`(`agit secrets add`)
  - `docs/06_repository_secret_dictionary.md`(可還原佔位符)
- 延伸:本庫 [[shopify-helix-checkpoints-and-gates]](同一頻道;Stop hook 的另一種用法)、[[supermemory-memory-layer]](跨 session 的記憶層,與「對話版本控制」互補)、[[claude-code-hooks-complete-guide]]。
