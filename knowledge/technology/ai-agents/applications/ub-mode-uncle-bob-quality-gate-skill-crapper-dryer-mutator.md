# ub-mode:Bob 大叔給 coding agent 的「工程質量門禁」技能(CRAP、dryer、mutator、UML)

> 整理自 YouTube 頻道 **Why QQ**〈[测试全绿也没有用:UB-Mode工程质量门禁](https://www.youtube.com/watch?v=Rfd6CzX7HLQ)〉(2026-10-30,約 10 分鐘,官方 zh-Hans 字幕)。
>
> ⭐ 已 `git clone --depth 1` 讀完 [unclebob/ub-mode](https://github.com/unclebob/ub-mode)(`SKILL.md`、`README.md`)與四個配套工具 [crapper](https://github.com/unclebob/crapper)、[dryer](https://github.com/unclebob/dryer)、[mutator](https://github.com/unclebob/mutator)、[uml-viewer](https://github.com/unclebob/uml-viewer) 的 README 與關鍵原始碼(2026-10-31 查詢;ub-mode 最後 commit 2026-10-25)。
>
> 立場:說明欄與片中沒有業配或聯盟連結。作者(Why QQ)說明內容依據 2026-10-29 抓取的文件。
>
> 相關:ub-mode 借鑑 poteto-mode / pstack 的部分規則(見 [[pstack-poteto-mode-cursor-plugin]]),這篇補的是「有確定性工具的門禁」那一半;「驗證先於規模」的討論見 [[agent-verification-before-scale-lauren-tan-reaction]]。

---

## 一句話總結

> **ub-mode 是一份很短的 `SKILL.md`(約 4 KB),把「先讓它跑、再把它做對、最後留下紀錄」三段式寫給 agent,並配四個確定性工具把「做對」變成可量測的門檻:CRAP < 10、結構重複相似度 < 0.8、變異測試存活者歸零、依賴方向不違規。** 影片的核心論點:測試全綠、覆蓋率高,不等於代碼好維護;AI 生成越快,未經檢查的改動越容易混進專案,所以約束要放在**執行過程**,而不是 review 時才補。

---

## 一、倉庫實況(clone 後核對)

| 倉庫 | 內容 | 星數(2026-10-31) | 授權 |
|---|---|---:|---|
| `unclebob/ub-mode` | 只有 `README.md` 與 `SKILL.md` | 約 5,400 | 無明示授權檔 |
| `unclebob/crapper` | CRAP 分數(Clojure、Java、Go、TypeScript、Rust、Python) | 約 150 | 0BSD |
| `unclebob/dryer` | 結構重複偵測 | 約 70 | 0BSD |
| `unclebob/mutator` | 變異測試 | 約 90 | 0BSD |
| `unclebob/uml-viewer` | Clojure 寫的動態 UML 檢視器 | 約 475 | 未標示 |

⚠️ **ub-mode 本身沒有授權檔**:引用或重新散布 `SKILL.md` 前要自己確認;三個工具為 0BSD(寬鬆)。

安裝:把 `SKILL.md` 放進 agent 技能目錄的 `ub-mode/SKILL.md`(README 舉例 `~/.claude/skills/`、`~/.cursor/skills/`、`~/.grok/skills/`),用 `/ub-mode` 呼叫。

---

## 二、三段式流程(SKILL.md 原文結構)

```mermaid
flowchart LR
    A["First Make it Work<br/>先得到可驗證的結果"] --> B["Then Make it Right<br/>處理原因、結構、測試、重複"]
    B --> C["Practice<br/>日誌、上下文、工作區、提交"]
```

### 1. First Make it Work

| 條目 | 規則(SKILL.md 精簡改寫) |
|---|---|
| Laziness Protocol | 一個決策只活在一處;**交付能解決問題的最小改動** |
| Foundational Thinking | 先把資料形狀弄對再寫邏輯;若並行寫入者會有影響,就不要共享狀態 |
| TDD | 改程式前先寫失敗的測試,**確認它因預期原因失敗**,再做最小改動讓它過;做不出誠實的測試就別寫永遠綠的擺設 |
| Redesign From First Principles | 別把新需求補丁式貼到舊設計;想「如果一開始就有這需求我會怎麼設計」,再分片交付 |
| Attack the Premise | 兩個共用同一前提的修法都過不了同一道門時,用一句話寫出那個前提,數出哪些角色承擔失衡,先移除前提再修 |
| Subtract Before You Add | 加東西前先拿掉複雜度 |
| Outcome-Oriented Execution | 瞄準可檢查的終態;中途可以有**事先規劃且可回退**的破壞 |
| Build the Lever | 工作不是一眼看懂的,就先做工具:先手動做一個單位,再讓工具貼合那個單位 |
| Architecture | 領域建模讓非法狀態無法表達;邊界檢查、內部信任、業務邏輯放純函式;型別系統別靜音編譯器;**操作冪等**;不需共享的可變狀態各自持有,確實共享則單一寫入者並由結構保證 |

### 2. Then Make it Right

| 條目 | 規則 |
|---|---|
| Fix Root Causes | 先重現、修原因;**只把崩潰點包起來的守衛不算修復** |
| Sequence work into verifiable units | 完成一小單位、驗證,才開始下一個 |
| Test Behavior, Not Implementation | 測試用使用者的方式呼叫、檢查使用者會看到的結果;**若每個函式都回傳空值測試仍會過,就該丟掉** |
| Crapper | 每個函式降到 **CRAP < 10**(拆分、補測試、或兩者);case/switch 要不要機械降低要判斷 |
| Dryer | 消除相似度 **0.8 以上**的重複 |
| Mutator | 補未覆蓋、殺死存活變異、刪死碼 |
| Refactoring | 先固定住行為、再改結構、證明行為沒變 |

### 3. Practice

記錄每個動作與原因並在完成時回報;主 context 保持小、大量素材丟到別處只留摘要;清理工作區前確認沒人在用、未提交的改動等待決定;小而有序地提交(每個 commit 寫為什麼、改了什麼、如何證明),最後推到主線。

---

## 三、四個工具實際怎麼運作(讀原始碼核對)

### crapper:複雜度 × 覆蓋率 = 一個分數

- 公式(`crap.py`):**`CRAP = CC² × (1 − coverage)³ + CC`**(CC 為圈複雜度,coverage 為 0–1)。覆蓋率缺值則不給分數,報表顯示 N/A。
- 影片例子驗算:CC=10 完全沒覆蓋 ⇒ 10²×1+10 = **110**;覆蓋 80% ⇒ 100×0.008+10 = **10.8**。✅ 即使 80% 覆蓋,CC=10 仍在 10 線上方,所以「覆蓋率高」不夠。
- 支援六種語言;單次執行偵測各檔語言。
- ⚠️ **容易誤判的細節(README 明載)**:缺少工具或測試執行失敗,該語言**按 0% 覆蓋計並仍寫出快照**;覆蓋報告沒提到的函式也算 0%。所以紅分可能來自環境沒裝好而非程式碼。`--no-coverage` 會讓覆蓋率與 CRAP 都留成 N/A,不能拿複雜度結果冒充完整評分。
- 閾值:SKILL.md 要求 < 10;工具另有 `--threshold`(超過則 exit 2),預設用法需自行設定。

### dryer:換名之後仍認得出的結構重複

- 做法:把區域變數、欄位名、字面量等附帶資訊**規範化**,再比對語法結構指紋集合;分數是 **Jaccard 相似度**(共有指紋 ÷ 兩者所有指紋)。1.0 = 規範化後結構指紋相同。
- ⚠️ **兩個口徑不要混**:ub-mode 要求處理 **≥ 0.8** 的重複;dryer **預設報告門檻是 0.82**(`--threshold`)。預設還會略過少於 **4 行**(`--min-lines`)或規範化節點少於 **20**(`--min-nodes`)的候選。
- 只是**審查線索**:共用抽象前要看兩段是否共享同一條業務規則;碰巧長得像的邏輯可以各自保留。

### mutator:故意下毒,看測試抓不抓得到

- 變異規則(原始碼):比較運算子互換(`>` ↔ `>=`、`<` ↔ `<=`)、`and` ↔ `or`、`true` ↔ `false` 等。
- 判定:測試失敗**或逾時**⇒ 變異體被殺死;測試仍全綠 ⇒ **存活**,表示斷言漏了一種行為差異。逾時為基準測試時間的 10 倍、至少 2 秒。
- **沒被覆蓋的位置不執行**(算 uncovered),所以覆蓋率與變異分數要一起看。分數 = killed ÷ (killed + survived)。
- **差分執行**:已有快照時,只重跑存活者與函式文字有變動的位置;未變動函式裡殺死的不重跑(`--mutate-all` 才全跑)。
- 結束碼:`0` 全殺死;`2` 基準測試失敗(且不改寫快照);`3` 有存活者。
- 用法:`./mutator src/demo/core.clj`、`./mutator --changed`、`./mutator --scan`(只列位置)。第一次全樹執行很耗時,影片也建議從手上那個檔案開始。

### uml-viewer:把依賴方向與品質疊在圖上

- Clojure 寫的 Quil 應用,需要 Clojure CLI 與 Java 21+。命名空間視為元件、其下模組為元素,可層層點進到原始碼,也能提出「what-if」架構提案,再請 agent 讓程式碼照提案改。
- **依 Clean Architecture 的依賴規則:由高層指向低層的依賴畫成紅色**。
- ⚠️ README 明載:**缺少 CRAP 或變異資料的模組也會是紅色**——紅不一定是壞,可能只是資料缺席。先確認快照齊全,再處理違規依賴。

---

## 四、應用案例

### 案例 1:訂單系統加「退款中」狀態

省事做法是沿著舊程式再補一個 `if`。ub-mode 要求先停下來:**訂單狀態該怎麼表達,非法組合能不能直接從型別消失**(例:用明確的 `已付款 / 已退款` 取代一串互相打架的布林欄位),並問「如果需求一開始就在,我會怎麼設計」,再**分片**交付,不做不可回退的大改。

### 案例 2:修 bug 的判空補丁算不算修復

只在崩潰點外面加 `if x is None: return`,資料可能仍是錯的。ub-mode 的做法:先寫能重現的使用者級測試 ⇒ 確認失敗 ⇒ 找出**原始錯誤發生在哪一步**再修;review 時多問一句「這個測試能抓到原始錯誤嗎」。

### 案例 3:一天能試的小循環(影片建議,對照原始碼可行)

1. 挑一個新發現的小 bug,先寫使用者行為測試並確認它失敗。
2. 最小修復。
3. 只針對本次改動跑覆蓋率與 `./mutator --changed`,看有沒有存活變異體(例如把 `>` 改 `>=` 測試仍全綠)。
4. 用 dryer 掃相關檔案。
5. commit 訊息寫上驗證命令,讓 reviewer 能重做。
6. 跑順之後再接 CRAP 閾值與 UML 依賴檢查。

### 案例 4:四張檢查卡(影片整理)

| 卡 | 問題 |
|---|---|
| 行為卡 | 有沒有能重現問題、且確實會失敗的使用者級測試? |
| 改動卡 | 這次只交付一個可驗證的小單位嗎?臨時破壞有計畫、能回退嗎? |
| 結構卡 | 入口邊界檢查、重複實作、依賴方向、函式複雜度過關嗎? |
| 證據卡 | 相關測試與變異檢查跑過了嗎?提交說明寫了改了什麼、怎麼證明嗎? |

遇到**紅燈**再加一個分類動作:先分清「環境失敗 / 指標缺失 / 程式碼問題」,再決定怎麼修。

### 案例 5:自己的 CI 要不要接

原型階段保留快速試驗;進入共享倉庫後,試驗程式碼也要過同一套。若團隊已有 PR、評審與分支保護,**服從專案流程**,不要拿技能檔繞過協作約定(影片原話精神)。

---

## 五、核實與保留

**✅ 已核實(原始碼 / README):**

- CRAP 公式與影片算例(110、10.8)正確;ub-mode 要求 CRAP < 10 與 dryer ≥ 0.8;dryer 預設門檻 0.82、最小 4 行與 20 節點;Jaccard 相似度。
- mutator:覆蓋不到的位置不執行、測試失敗或逾時算殺死、差分策略、`>`↔`>=`、`and`↔`or`、`true`↔`false` 變異;crapper 缺工具或測試失敗按 0% 計;uml-viewer 缺資料標紅、違反依賴規則的箭頭標紅。
- 影片說「crapper 支援 Clojure、Java、Go、TypeScript、Rust、Python」✅ 與 README 一致;ub-mode 借鑑 poteto-mode 與 pstack ✅ 與 README 一致。

**⚠️ 需補正或保留:**

- 影片說 ub-mode 的規則「必須」讓 agent 留下檢查證據。**SKILL.md 實際是原則清單(給 agent 的行為準則),沒有程式強制**;真正的強制力要靠把工具接進 CI 或 hook。技能被忽略時不會報錯。
- 影片把 CRAP「處理線是 10」說成每個函式的處理線;SKILL.md 寫 `CRAP 10`,而 crapper 的 `--threshold` 預設用法需自行指定,並未內建 10。
- 「Bob 大叔」即 Robert C. Martin(unclebob);影片稱「最近公開」——ub-mode 最後 commit 為 2026-10-25,屬最新。
- 影片沒給任何效果數據(例如導入後缺陷率),結論是**方法論推介**,不是實測。

**⭐ 影片沒講、值得補的:**

- 這些工具原生偏 **Clojure / JVM 生態**(uml-viewer 要 Clojure CLI;mutator 要把 crapper 放在 `../crapper` 取函式名稱),其他語言的接入成本要自己評估。
- 變異測試**很耗時**(首次全樹要執行每個覆蓋到的變異),實務上宜限定 `--changed` 或單檔,別一開始就放進每次 CI。
- 本庫 [[agent-skill-three-layer-run-do-verify]] 與 [[loop-engineering-when-and-how-gary-chen]] 可對照:ub-mode 的「別球員兼裁判」靠的是**確定性工具**當外部裁判。

---

## 相關筆記

- [[pstack-poteto-mode-cursor-plugin]]:ub-mode 借鑑的 poteto-mode / pstack 原始碼拆解。
- [[agent-verification-before-scale-lauren-tan-reaction]]:先給 agent 驗證,再談規模。
- [[agent-skill-three-layer-run-do-verify]]:技能的跑、做、驗三層。
- [[loop-engineering-when-and-how-gary-chen]]:可驗證目標與 hard stop。
- [[cross-model-review-claude-codex-harness]]:另一種外部裁判(跨模型互審)。

---

## 來源

- YouTube:Why QQ〈测试全绿也没有用:UB-Mode工程质量门禁〉 https://www.youtube.com/watch?v=Rfd6CzX7HLQ (2026-10-30;官方 zh-Hans 字幕)
- ub-mode: https://github.com/unclebob/ub-mode
- crapper: https://github.com/unclebob/crapper
- dryer: https://github.com/unclebob/dryer
- mutator: https://github.com/unclebob/mutator
- uml-viewer: https://github.com/unclebob/uml-viewer
