# Understand-Anything vs Graphify:把 codebase 變成知識圖譜給 AI 查,實測對比

> 兩個 Claude Code 工具,都能把整個 codebase 轉成可探索的**程式知識圖譜/知識庫**,
> 讓 AI 做程式研究時**省 token**(不必每次把整包檔案塞進 context)。
> 一位前 Amazon/Microsoft 資深 AI 工程師(Eric Tech)在自己的 production SaaS 上實測兩者的差異。
>
> 整理自 Eric Tech 影片(英文)。這和本庫 [[tree-sitter]](程式結構化)、GitHub Weekly #115 的 CodeGraph、
> [[context-engineering-processing-vs-thinking]](省 token / 索引)是同一條「**結構化理解程式碼以省 token**」的路線。

---

## 它們在解決什麼

agent 對大型 codebase 做研究時,若每次都讓它 grep/讀整包檔案,**token 燒很兇且容易 lost in the middle**。
解法:**先把 codebase 建成一份知識圖譜/知識庫(節點=檔案/元件,邊=依賴關係)**,之後 AI 查圖定位、只讀需要的部分。
Understand-Anything 與 Graphify(Graphy AI)就是兩個這樣的工具。

| | 安裝方式 |
|---|---|
| **Graphify** | 用 `uv tool` 安裝,把 skill 裝進 `CLAUDE.md` |
| **Understand-Anything** | 透過 **Claude Code marketplace plugin** 安裝(`/plugin marketplace add` → install,可選 project 層級) |

> 操作上都很簡單:`/understand` 或 `/graph` 掃描整個 codebase 產生圖;用 `understand ignore` 排除 tests/fixtures/migrations/mock 等不相關檔案(把候選 2,000 檔縮到 1,500),由 sub-agents 分批處理。

---

## 六個維度實測對比

| 維度 | 贏家 | 說明 |
|---|---|---|
| **Token 消耗** | 🟢 **Graphify** | 同一個 codebase,Understand-Anything 約耗 **200K token**,是 Graphify 的**約 2 倍**;Graphify 只用約一半 → 預算吃緊時關鍵 |
| **Dashboard 視覺化** | 🟢 **Understand-Anything** | 能顯示**父/子節點關係**、元件摘要、往下 trace 依賴、抓出**沒被引用的 dead file**;Graphify 的圖只顯示「鄰居節點」,**分不出父子** |
| **AI 查詢回應** | 🟢 **Understand-Anything**(token 兩者相近) | 同一問題兩者答案一致、token 差不多;但 Understand-Anything 回應更結構化(檔案位置、流程圖、step-by-step 演算法),Graphify 多為純文字 |
| **Onboarding 產出** | 🤝 平手(看偏好) | Graphify → 一份 **wiki**(含 77 篇文章);Understand-Anything → 一份**摘要 MD**(專案總覽、架構分層)。要 wiki 選 Graphify、要摘要選 Understand-Anything |
| **過時資料/自動更新** | 🤝 兩者都有 | 都能在 **git commit / 切 branch** 時自動跑 update,依最新變更刷新圖 |
| **隱私/本地模型** | 🟢 **Graphify** | Graphify 支援**本地模型**(Ollama、AWS Bedrock 後端,設環境變數即可);Understand-Anything **預設不支援**,程式碼會送到你 IDE 接的那個 provider |

---

## 結論與作者建議

- **Understand-Anything**:**視覺化更好、AI 查詢回應更易讀**(父子節點、流程圖、dead file 偵測),適合「人要看懂、做研究、重構」;但 **token 約 2 倍、不支援本地模型**。
- **Graphify**:**省 token(約一半)、支援本地模型/隱私**;圖的層級資訊較弱。
- **作者建議:兩個一起用、在同一個 repo 各維護一份圖** —— 要**好視覺化**用 Understand-Anything,要**低 token / 本地模型**用 Graphify。

---

## 為什麼這類工具重要(放回脈絡)

- **省 token = 省錢 + 更準**:把「結構」先抽出來當索引,AI 查圖定位再讀局部,避免把整包檔案塞進 context(對照 [[context-engineering-processing-vs-thinking]] 的「索引系統 / progressive disclosure」)。
- **結構化理解程式碼**:和 [[tree-sitter]](語法樹)、CodeGraph(GitHub Weekly #115)同屬「給 agent 一張 code map」這條路線——差別在這兩個工具更偏「**用 LLM 產生語意層知識庫/wiki**」,而 Tree-sitter 偏「**確定性的語法結構**」。實務上兩層可互補。
- **自動更新**是關鍵:程式天天在改,知識圖譜若不能跟著 commit 自動刷新就會很快過時——兩者都用 git hook 解決。

---

## 應用案例

- **大型 repo 上跑 coding agent 一直燒 token:** 先用 Graphify 建知識圖譜(省一半 token、可走本地模型保隱私),讓 agent 查圖定位再讀局部,而非每次 grep 整包。
- **接手陌生 codebase / 要重構:** 用 Understand-Anything 的 dashboard 看父子依賴、元件摘要、揪出 dead file,比硬讀程式快很多。
- **要給新人/agent 一份專案總覽:** 兩者的 onboarding 各擅場——想要可瀏覽 wiki 用 Graphify,想要一份精簡 MD 摘要用 Understand-Anything。
- **既要視覺化又要省 token:** 照作者建議**兩個都裝**,各取所長,git commit 時都會自動更新。

---

## 一句話總結

> 兩個工具都把 codebase 變成「給 AI 查的程式知識圖譜」以省 token:
> **Graphify 省 token、支援本地模型**;**Understand-Anything 視覺化與回應更好、但 token 約 2 倍、不支援本地模型**。
> 與其二選一,不如兩個一起用——這正是「**把程式結構抽成索引、讓 AI 查圖而非吞整包**」這條省 token 路線的最新一站。

---

## 來源

- YouTube:[Understand-Anything vs Graphify: I Tested Both on My SaaS(Eric Tech)](https://www.youtube.com/watch?v=Ynv_WYO_slw)
- 延伸:本庫 [[tree-sitter]]、[[context-engineering-processing-vs-thinking]];GitHub Weekly 第 115 期的 CodeGraph(程式 Agent 知識圖譜)。
