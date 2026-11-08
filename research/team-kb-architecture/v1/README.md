# Team KB v1(第一版:一天內可上線)

整合 REPORT 1–4 的結論與使用者 2026-11-08 的七項決策。**一個檔案 `kb.py`(只用 Python 標準函式庫)+ 一份 `AGENTS.md`**,不需要資料庫、不需要向量庫。
實驗與限制見 [`../REPORT-5.md`](../REPORT-5.md)。

## 十分鐘上線

```bash
mkdir team-kb && cd team-kb
cp <本資料夾>/kb.py <本資料夾>/AGENTS.md .
git init                                  # 版本控制 = 免費的稽核紀錄
mkdir -p claims raw inbox state topics    # raw/ 放不可變的原始紀錄(會議逐字稿等)
python kb.py template                     # 看 claim 欄位
python tests/test_v1.py                   # (選用)跑 24 項行為測試,確認你的 Python 沒問題
```

把 `AGENTS.md` 放在 KB 根目錄,AI(Claude Code 之類)開在這個目錄時會先讀它。

## 日常流程

| 誰 | 做什麼 | 指令 |
|---|---|---|
| 任何人 / AI | 查 | `python kb.py search "關鍵字"`;範圍相關用 `python kb.py resolve <concept> --project X --platform Y --branch Z` |
| 任何人 / AI | 提案 | `python kb.py propose --subject … --statement … --valid-from … --source … --author … --aliases "a, b, c, d"` |
| 另一個人 | 審核 | `python kb.py review` → `python kb.py approve <P-id> --by 名字`(作者不能核准自己的) |
| 輪值者(每週) | 維護 | `python kb.py unfound --report` + `python kb.py lint` |

## 設計決策(已拍板)

| 項目 | v1 做法 |
|---|---|
| 檢索 | 兩欄 BM25(雙字詞):主文 + 別名欄 × 0.5;不用向量 |
| 別名 | LLM 提案時自己產(AGENTS.md 要求 ≥4 個、建議 6–12 個、中英都要),審核者順手看;gate 擋 <4 個 |
| 過期 claim | 搜尋**永遠顯示**並標 SUPERSEDED,自動附取代鏈鄰居;不隱藏 |
| 範圍 | 維度固定三個 `project / platform / branch`(改 `kb.py` 的 `DIMS` 一行即可);越具體越優先 |
| 同具體度衝突 | `resolve` 回 `CONFLICT`、`lint` 報 AMBIGUOUS-INTERSECTION;要有人寫一條「交集範圍」的明確 claim 並 supersedes 其一 |
| 缺 scope | `resolve` 回 `ASK`,列出各情境;AGENTS.md 規定 agent 必須先反問使用者 |
| 「找不到」 | `search` 無命中自動記、agent 用 `unfound` 手動記;每週輪值者 `unfound --report` |
| 寫入 | 只能走 inbox;作者 ≠ 核准者;核准當下重驗 gate(防 write-skew) |
| 彙整類問題 | `build` 自動產生 `topics/<subject>.md`,AGENTS.md 要求這類問題先讀它 |

## 檔案

```
claims/CL-0001.md   已核准、不可變(只有 build 會改 status / superseded_by 兩個衍生欄位)
inbox/ inbox/rejected/   待審 / 退回
topics/             build 產生的主題現況頁(勿手改)
state/              unfound.jsonl、queries.jsonl、ledger.jsonl(核准紀錄)
raw/                不可變原始紀錄
kb.py  AGENTS.md  tests/  experiments/(實驗腳本,上線不需要)
```

## 還沒做 / 之後再說

- 例外 scope 的負責人共同核可(目前只有「另一人核准」)
- 共存最長期限的強制(目前只有 `lint` 對逾期退場日報警)
- `deprecated` 與 Wikidata 的 deprecated rank 撞名,要不要改叫 `sunsetting`
- 向量索引:只有在「別名補完仍有大量落差題」時才加,而且要先在你們自己的語料上測
- 規模:實驗只到約 1,500 條 claim;每次 `search` 都重讀所有檔案,上萬條時要改成快取索引
