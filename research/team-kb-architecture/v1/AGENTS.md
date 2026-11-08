# 團隊知識庫使用說明(給 AI 與人;放在 KB 根目錄)

## 結構
- `claims/CL-*.md`:一條一檔的 claim(單一事實),已核准且不可改。欄位是單行 `key: value`,可以直接 grep。
  `status: current | superseded | retired` 與 `superseded_by` 由工具自動維護,不要手改。
- `topics/<subject>.md`:自動產生的「該主題現況頁」(現行 + 歷史)。**彙整類問題(「有哪些…」「所有…」)先讀這裡**,不要期待搜尋湊齊清單。
- `raw/`:不可變的原始紀錄(會議逐字稿等)。`notes/`:雜項。`inbox/`:待審,不算正式結論。
- 範圍欄位:`project` / `platform` / `branch`。`*` = 全部;越具體的 claim 在它的範圍內優先。

## 查詢(照這個順序)
1. `python kb.py search "關鍵字"`:會標 current / SUPERSEDED / DEPRECATED,並自動附上取代鏈鄰居。
   - **至少用 3 種說法查**(中文、英文、口語/同義詞);第一次沒找到,換說法再查,不要立刻放棄。
   - 結果裡標 SUPERSEDED 的是過期結論:**不要當答案**,改用它的取代者;若使用者的前提是過期內容,要明講「這個已經改了」。
2. 同一件事在不同範圍結論不同時(例如依平台、分支、專案),用 `python kb.py resolve <concept> --project X --platform Y --branch Z`。
   - 輸出 `ASK`:**先反問使用者缺哪個條件並列出各情境,不要自己猜**。
   - 輸出 `CONFLICT`:兩條同等具體的 claim 互相矛盾,**回答「尚有衝突待裁決」並列出兩條 id**,不要自己挑。
3. 需要整體現況或「有哪些」:讀 `topics/<subject>.md`;需要原始脈絡:用 Grep 搜 `raw/`、`notes/`,再 Read。
4. **找不到**:換過說法仍找不到時,執行 `python kb.py unfound "你查的問題"` 記錄,然後回答「知識庫目前沒有這項資料」。不要用常識或猜測補。

## 回答格式
- 附 claim id 與生效日期;說明是否仍有效(current / 已被取代 / deprecated 及退場日)。
- 有 deprecated:一定要講退場日。
- 否定句(不得、不支援)與肯定句是不同 claim,看清楚適用範圍(例如 RT 路徑 vs 初始化)。

## 寫入(只能走 inbox,禁止直接改 `claims/`、`topics/`)
1. 先 `python kb.py search --no-log "…"` 確認沒有同義 claim(`--no-log` 不會把這次查詢記成未找到);沒有新資訊就不要提案。
2. `python kb.py template` 看欄位;用 `python kb.py propose --subject ... --statement ... --valid-from ... --source ... --author ... --aliases "a, b, c, d, ..."`。
3. **aliases 必填至少 4 個,建議 6–12 個**:口語說法、同義詞、中英互換(例如 mutex 與 互斥鎖)、常見的換字問法;不要加原文沒有的事實。
4. 取代舊 claim 用 `--supersedes <舊id>`,新範圍不得比舊的更窄;範圍的例外請另寫一條帶範圍的 claim。
5. `deprecated` 必須帶 `--retire-when`。
6. 提案後等**另一個人**用 `python kb.py review` / `approve` 核准(作者不能核准自己的)。

## 每週維護(指定一人輪值)
`python kb.py unfound --report` 看大家找不到什麼 → 補 aliases / 補詞彙 / 補缺的 claim;`python kb.py lint` 清掉 ERROR。
