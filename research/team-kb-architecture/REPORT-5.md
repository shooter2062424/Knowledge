# 部門級 Knowledge Database 架構研究:第五輪(第一版 v1:實作 + 實驗)

> 延續 [REPORT-4](./REPORT-4.md)。本輪依使用者 2026-11-08 的指示「先實驗 + 完成研究,遇到問題先照你的建議,我們先有第一版」,把 REPORT 1–4 的結論與七項決策([REPORT-4 §7.1](./REPORT-4.md))合併成可上線的 **[`v1/`](./v1/)**:一個只用標準函式庫的 `kb.py` + `AGENTS.md`,並用實驗驗證。上線步驟看 [`v1/README.md`](./v1/README.md)。
> **全域限制(先看):** 虛構資料;agent 是 Haiku `--effort low`,每題單次取樣;題庫 43 題(離線)/ 17+4 題(agent)是我寫的;最大規模 1,530 條 claim,其中 1,500 條是模板產生的干擾;**任何差距小於 0.1(離線)或 2 題(agent)都視為噪聲**。

## 1. 一頁結論

1. **v1 做出來了,且行為測試 24/24 通過**(scope 解析、衝突、缺 scope 反問、gate、雙人規則、write-skew、折疊、lint、未找到清單)。測試過程抓到並修掉一個缺陷:已補明確 claim 的交集仍被 lint 報歧義。
2. **別名要「分欄加權」,不能直接併進全文**(本輪最重要的新發現)。同樣的別名,併進同一欄 hit@5 是 0.70(沒別名 0.72,等於沒用,英文題從 1.00 掉到 0.40);分成「主文 + 別名欄 × 0.5」是 **0.93**。原因:帶別名的同型干擾 claim 也有別名,別名詞頻會把字面完全吻合的結果擠下去。權重 0.3–0.5 都在平台(0.91–0.93),1.0 掉到 0.86。
3. **agent 實驗:v1 全對、更省。** 17 題(含 1 題「知識庫沒有」):對照組(只有 Grep/Glob/Read)與 v1 都是 17/17,但 v1 平均 **8.2 輪、US$0.116**,對照組 **13.6 輪、US$0.25**(輪數 −40%、成本 −54%);對照組還有 20 次權限拒絕(agent 試圖用被禁的指令),v1 為 0。**正確率沒有分出高下(兩邊都滿分,題目對 Haiku 太容易),差別只在效率。**
4. **兩項決策在 agent 層有效:** scope 4/4(缺 scope 反問、Vision/Linux/main 命中 deprecated 並講退場日、Windows LTS 用交集 claim、Audio/Windows/main 取 Windows 的 claim);「知識庫沒有」題 agent 回答找不到,且只在未找到清單留下 3 筆(2 筆自動 + 1 筆 agent 手動)。
5. **LLM 自己產的別名品質可用。** 8 段會議摘錄 → Haiku 提案,每條都有 6–8 個別名、全部含英文、沒有加入原文沒有的事實。對「換說法 / 英文」問句,有別名比無別名多命中約 1–2 題/8(三次重跑:換說法 5/8、3/8、4/8 對 3/8;英文 7/8、8/8、7/8 對 6/8、6/8、7/8),**但每次 LLM 產的別名不同,變動大**——這就是為什麼要有「未找到清單」回饋迴圈。
6. **寫入路徑可用但不是 100%。** 提案 7/8、8/8、7/8、7/8 成功;有記錄到原因的一次失敗是 Bash 權限拒絕(harness 的 allowlist;agent 自己也拒絕繞過 gate 手寫檔案),不是 gate 退回;其餘失敗當時沒存 agent 回覆,原因未查明。

## 2. v1 是什麼

詳見 [`v1/README.md`](./v1/README.md)。重點:

| 項目 | 做法 | 來源 |
|---|---|---|
| 檢索 | 兩欄 BM25(CJK 雙字 + ASCII 詞,極簡複數處理);別名欄 × 0.5 | REPORT-4 + 本輪 E1 |
| 過期 | 永遠顯示並標 SUPERSEDED,附取代鏈鄰居 | REPORT-4 P1–P3 |
| 折疊 | 同 concept、拿掉 scope 值後文字相同的 claim 只列一行並註明另有幾條 | REPORT-4 F 組 |
| 範圍 | `project/platform/branch` 三維;越具體越優先 | 決策 |
| 同具體度衝突 | `resolve` 回 CONFLICT、`lint` 報 AMBIGUOUS-INTERSECTION;有交集 claim 才算解決 | 決策 + REPORT-3 |
| 缺 scope | `resolve` 回 ASK;AGENTS.md 規定先反問 | 決策 |
| 未找到 | 無命中自動記 + `unfound` 手動記 + 每週 `--report` | 決策 |
| 寫入 | inbox;作者 ≠ 核准者;核准時重驗 gate;aliases ≥ 4 | 決策 |
| 彙整題 | `build` 產生 `topics/<subject>.md`,AGENTS.md 要求先讀 | REPORT-4 §1.6 |

## 3. 實驗

### E0 行為測試([`v1/tests/test_v1.py`](./v1/tests/test_v1.py))

24 項全過。涵蓋:同具體度重疊 → CONFLICT;補交集 claim → 唯一結論;缺 scope → ASK(且指出哪個維度會改變結論);deprecated 顯示退場日;未出現過的 project → 回全域;gate 擋(缺 retire_when、aliases 不足、取代時範圍變窄、同 scope 衝突無 supersedes);作者不能核准自己;write-skew(兩條衝突提案同時在 inbox,第二條核准時被重驗擋下);OVERDUE;別名命中;SUPERSEDED 不隱藏;未找到;折疊。
**抓到的缺陷:** 補了 Windows + LTS 的明確 claim 後,lint 仍報 Windows 與 LTS 的歧義 → 已改成「交集範圍已有明確 claim 就不再報」。

### E1 離線檢索(`v1/experiments/e1_retrieval.py`,1,530 條 claim,43 題)

| 設定 | hit@5 | 說明 |
|---|---|---|
| 無別名 | 0.72 | G(換說法)僅 0.25 |
| 別名併入同一欄 | 0.70 | G 升到 0.67,但 L 0.75、E 0.40 被擠下 |
| 兩欄,別名權重 0.3 / **0.5** / 1.0 | 0.91 / **0.93** / 0.86 | 0.5 採用 |
| 兩欄 0.5(最終版,加複數處理) | 0.93 | L 1.00、G 0.75、N 1.00、S 1.00、M 1.00、E 1.00、H 1.00 |

- **不能和 REPORT-4 的數字直接比。** 本輪索引只含 claim(1,530 條),REPORT-4 的單元還包含會議逐句與 1,500 條雜訊;v1 的做法是 claim 走 `kb.py`、原始紀錄由 agent 用 Grep 找。
- **權重是用同一批 43 題挑的,有過度擬合風險**;但 0.3–0.5 都在 0.91–0.93,看起來是平台而不是尖峰。
- 剩餘弱點:G 類 0.75(換說法題)、N 類「stale 排在現行前面」仍有 3/6——靠取代鏈鄰居補救,不是靠排序。
- 速度:1,530 條在行程內約 0.2 秒(讀檔 0.11、排序 0.02);每次查詢重讀所有檔案,上萬條時要改快取。

### E2 agent(`v1/experiments/e2_agents.py`;Haiku low)

| 條件 | 正確 | 平均輪數 | 成本 | 權限拒絕 |
|---|---|---|---|---|
| CTRL(Grep/Glob/Read,基本 AGENTS) | 17/17 | 13.6 | $0.250 | 20 |
| V1(v1 AGENTS.md + kb.py + Grep/Glob/Read)第一次 | 17/17 | 8.8 | $0.161 | 0 |
| V1 最終版重跑 | 17/17 | 8.2 | $0.116 | 0 |
| SCOPE(5 條 ipc claim,4 題) | 4/4 | 6.0 | $0.024 | 0 |

- 17 題 = REPORT-4 的 16 題(含過期前提題、彙整題 M1、英文題)+ 「知識庫沒有」X1。V1 的 M1 也過了(≥4/5 個禁止事項)。
- **天花板效應:** 兩邊都滿分,代表這批題對 Haiku 太容易;結論只能是「v1 不比對照差、而且更省」,不是「v1 更準」。要區分準確度需要更難的題或更大的語料。
- **第一次 V1 暴露一個設計缺陷(已修):** agent 常把整句問題當成 `resolve` 的 concept,每次都被記進未找到清單,污染了每週要看的清單。已改成 `resolve` 找不到 concept 時只記查詢紀錄、不進未找到清單,並回傳已有的 concept 列表。修後重跑,清單只剩 X1 的 3 筆。
- 另一個修正:agent 提案前的「重複檢查」搜尋也會被記為未找到;新增 `search --no-log`,AGENTS.md 寫入流程改用它。

### E3 寫入路徑(`v1/experiments/e3_write_path.py`)

8 段虛構摘錄 → 4 路平行 Haiku 提案 → 人核准 → 用刻意避開 claim 用字的換說法 / 英文問句檢索,對照「同批 claim 拿掉別名」。

- 4 次執行:提案成功 7/8、7/8、8/8、7/8。有存回覆的一次失敗是 Bash 權限拒絕(agent 明說不繞過 gate);第一次缺的「備份」單獨重跑即成功且無拒絕;其餘失敗原因未查明。
- 別名:6–8 個/條、全含英文、無新增事實(我逐條讀了第一次的 7 條)。
- 檢索 hit@3(有別名 vs 無別名;後三次執行,已含複數處理):換說法 5/8 vs 3/8、3/8 vs 3/8、4/8 vs 3/8;英文 7/8 vs 6/8、8/8 vs 6/8、7/8 vs 7/8。**效果為正但小且不穩定。**
- 仍然找不到的:「加密證書」(別名寫「憑證」,沒有「證書」)、「送審」(別名寫「審查」)。這就是未找到清單要補的那種詞。

## 4. 沒有解決 / 沒有測的

1. **lint 在粗 concept 上會爆量:** 合成干擾全放同一個 concept `ops`,lint 報出 9 萬多筆 CONFLICT。真實 KB 的 concept 必須夠細(一個 concept = 一件可以有唯一結論的事),否則 CONFLICT 失去意義。已加 `--limit` 限制輸出;但「concept 由誰命名、如何防止亂取」沒有機制,只能靠審核。
2. **concept 欄位本身是新負擔:** `resolve` 要 agent 知道 concept 名稱;實驗中 agent 會猜錯(上述污染問題)。目前靠 `search` 先找、`resolve` 的錯誤訊息列出 concept 清單,沒有實測更大的 concept 數量。
3. **沒測真實文件。** 沒有 PDF、投影片、長會議的切塊與抽取;claim 抽取品質(誰把會議變成 claim、錯抽怎麼辦)是 REPORT-1/2 的範圍,v1 只管 claim 之後的流程。
4. **沒測多人同時使用。** write-skew 只用兩個提案測;`next_id` 在核准時取號,併發核准同一秒可能撞號(沒有鎖)。
5. **沒測換 agent 平台**(決策是 Claude Code 類,本輪就是);也沒測 Sonnet 以上或地端模型。
6. **沒有向量。** 本輪沒有再比;REPORT-4 的結論(小嵌入模型沒贏 BM25)維持。
7. **權限設定是上線前要做的事:** 實驗中 4 次失敗都是 `Bash(python kb.py:*)` 白名單被拒;agent 若用 `;` `&&` 串接指令也會被拒。公司環境要先測一次 allowlist。
8. **規模:** 1,530 條;搜尋每次重讀全部檔案,上萬條要加快取索引(尚未實作)。

## 5. 上線檢查清單(明後天)

1. 複製 `v1/kb.py`、`AGENTS.md` 到新 repo(步驟見 [`v1/README.md`](./v1/README.md)),跑 `python tests/test_v1.py` 確認環境。
2. 先放 20–30 條**真實** claim(每條至少 6 個中英別名),concept 命名規則寫成一頁(一件事一個 concept,小寫英文短詞)。
3. 先確認 agent 的 Bash allowlist 允許 `python kb.py ...`(單一指令,不串接)。
4. 指定「未找到清單」的每週輪值人,第一週結束時看 `python kb.py unfound --report`。
5. 建 30–50 題自己的題庫(同事真的問過的),每週跑命中率(`v1/experiments/e1_retrieval.py` 可改寫)。
6. 還沒定的三項決策(例外 scope 負責人、共存期限、`deprecated` 是否改名)上線後再補。

## 6. 檔案

- [`v1/kb.py`](./v1/kb.py)、[`v1/AGENTS.md`](./v1/AGENTS.md)、[`v1/README.md`](./v1/README.md)、[`v1/tests/test_v1.py`](./v1/tests/test_v1.py)
- 實驗:[`v1/experiments/`](./v1/experiments/)(`build_l.py` 轉第四輪語料、`e1_retrieval.py`、`e2_agents.py`、`e3_write_path.py`)。路徑寫死沙盒 `data/sandbox/`(不進版控),重跑需先有第四輪的沙盒資料。
