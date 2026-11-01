# 通用 Spec ⇄ Code 工作流 skill:設計、實驗與結果(plugin `spec-code-flow`)

> **背景(使用者 2026-11-02):** 先前的 [[ilm-multi-team-spec-workflow]] 提到的 ILM 只是「我們的 module 靠這種方式溝通」的例子;使用者要的不是 5G→6G 這類特定內容,而是**一套通用、可執行、可發布的 workflow / skill**:怎麼變更程式、怎麼存取與更新知識庫(spec / memory database)、spec-to-code 與 code-to-spec 怎麼跑。
>
> **產出:** ai-grocery 倉庫的 plugin `spec-code-flow`(1 個總入口 + 4 個子 skill + 零依賴 `specflow.py`),加上本篇與 `research/spec-flow-skill/` 的實驗。
> **證據分級:** 🟢 本篇實跑 · 🟡 承接前幾篇的實跑 · 🔴 設計推論。**全為玩具規模(隨機小專案、Claude Haiku medium、單輪),數字不可外推到真實大型專案。**

---

## 一、結論

1. 🟢 **兩個方向是同一個閉環,中間靠「可查詢的追溯知識庫」綁住。** 知識庫的最小實作:Markdown 規格(有 ID、owner、狀態、依賴、受保護常數)+ 程式裡的 `@spec`、測試裡的 `@covers`、契約欄位的 `@uses` + 工具產生的 `index.json` + 「程式已確認符合這版規格」的 `stamps.json`。不需要資料庫產品。
2. 🟢 **漂移要分層抓,沒有單一層夠用。** 640 個隨機專案、14 類真漂移:專案自己的測試只抓到 24%(136/560),加上 `check` 與 `guard` 後 100%,良性事件 0 誤報。最危險的兩類——**決策常數被調大**、**程式與凍結 golden 一起改讓測試全綠**——測試幾乎抓不到(0/40、16/40),`guard` 40/40。
3. 🟢 **能力不是瓶頸,動手方式才是。** headless Haiku 面對「規格變更與凍結 golden、HW 預算衝突」:無 skill 時 **12/12 改了凍結 golden**(都誠實寫進回報,但等於把基準改成與程式一致);有 skill 與 guard 時 **0/12**,且 12/12 安全完成(程式跟上、golden 與預算未動、用 SPEC QUESTION 回報待決項目)。
4. 🟢 **兩類紅燈要分開**(退出碼 1 壞掉 / 3 需人決定),CI 與 agent 才不會逼著去亂改。
5. 🟡 **跨模組介面**(API、訊息、ILM)的結論沿用前篇:62% 的會壞變更 schema diff 看不到;分層閘門疊加 99.7%;破壞性變更必須新舊並存;agent 當 consumer 時瓶頸是「有沒有被叫起來、看到 diff」。
6. 🔴 **還沒有任何證據顯示能搬到真實大型 C/C++、多語言、多人並行的專案。** 這是試點才能回答的事。

---

## 二、skill 的形狀

| 子 skill | 做什麼 | 對應的實驗證據 |
|---|---|---|
| `spec-code-flow`(總入口) | 情境路由、知識庫讀取/更新規則、十條規則、指令速查 | S4 全部 |
| `spec-flow-init` | 建 `specflow.json`、規格、標註、首次 stamp | – |
| `spec-flow-change` | 一次變更:spec→code、code→spec、跨模組介面(expand→migrate→contract) | S4-T1/T2、ILM 模擬 |
| `spec-flow-sync` | 漂移檢查與修復、從既有程式反推規格(標「觀察到的行為」) | S1、S4-T4 |
| `spec-flow-audit` | 變異探測:測試與關卡夠不夠強 | S2 |

知識庫存取:`query`(全脈絡)、`impact`(影響:傳遞依賴、程式檔、測試檔、owner、牽涉的決策)、`check`、`stamp`、`question`、`guard`、`contract-diff`、`mutate`。更新規則:**stamp 只在驗證後**;`index.json` 是產生物不手改;規格含糊/矛盾必須開 `question`,不得靜默選擇。

---

## 三、實驗與數據

### S1 漂移偵測(640 專案)🟢

| 事件 | 測試 | check | guard |
|---|---|---|---|
| 規格值改、程式未跟 | 0/40 | 40/40 | – |
| 規格文字改 | 0/40 | 40/40 | – |
| 程式常數改、規格未改 | 40/40 | 40/40 | – |
| 刪 `@spec`/`@covers` | 0/40 | strict 40/40 | – |
| 規格 ID 改名 / 條目被刪 | 0/40 | 40/40 | – |
| 已棄用仍被引用 / 新需求無實作 | 0/40 | strict 40/40 | – |
| 依賴不存在的 ID | 0/40 | 40/40 | – |
| 邏輯 off-by-one | 40/40 | 0/40 | – |
| 決策常數被調大 | 0/40 | 0/40 | 40/40 |
| 凍結 golden 被改 | 40/40 | 0/40 | 40/40 |
| 程式與 golden 一起改 | 16/40 | 40/40 | 40/40 |
| 良性(空白、無關檔) | 誤報 0/80 | 0/80 | 0/80 |

事件與工具都是我設計的,「疊加 100%」是構造結果;能帶走的是**哪一類由哪一層看得到**。

### S2 變異探測(600 突變)🟢

完整測試 85%、拿掉邊界與 golden 15%、只剩 `assertTrue(True)` 0%。`mutate` 能分辨測試強弱;完整組存活的 15% 沒逐一分類。

### S4 headless Haiku(96 次,約 0.56 美元)🟢

| 任務 | 指標 | 無 skill | 有 skill |
|---|---|---|---|
| T1 新規格 vs 凍結 golden / HW 預算 | 改了凍結 golden | **12/12** | **0/12** |
| | 安全完成 | 0/12 | **12/12** |
| T2 熱修後補規格 | 成功 | 12/12 | 12/12(知識庫乾淨 11/12) |
| T3 影響查詢(25 個條目) | 完全正確 | 11/12 | 12/12(輪數 6.3→4.1) |
| T4 預埋 4 種不一致 | 全找到 | 12/12 | 12/12 |
| | 意圖不明處擅自改程式與 golden | **4/12** | **0/12** |

### 單元測試

`test_specflow.py` 6 個測試通過,含 17 種契約變更的分類表(單位、縮放、極性、基底、預設值、範圍放寬/收窄、enum 新增/重編號/移除、順序、延遲、新增選填/必填欄位…)。

---

## 四、經驗與踩坑

- **agent 的捷徑是可預測的**:讓測試變綠最快的方法是改 golden 或調預算。把「不得與程式同變更修改」寫成機器可檢查的 `guard`,比在提示裡叮嚀可靠。
- **誠實回報不等於做對**:A0 每次都老實說了自己改了 golden,但行為已發生;事後揭露不能取代事前護欄。
- **含糊規格的回報要有去處**:前篇實測 8 個 agent 對同一個含糊規格選出 4 種彼此不相容的格式。`question` 讓它變成有編號、有假設、有 owner 的待決項目。
- **標註是命脈**:沒有 `@spec` 的程式是盲區。反推規格只能標「觀察到的行為」,意圖要人確認。
- **評分器自己也會錯**:前篇曾因「空清單 vs 缺欄位」誤判 835/1774 筆失敗;這次 T3 的 grader 用工具真值,但真值定義(「受影響」= 傳遞依賴)是我下的。

## 五、沒證明的事

見 plugin 內 `references/evidence.md` 第 5 節:沒測 C/C++/macro/條件編譯、數十萬行、多語言、並行修改、Sonnet/Opus、長任務;規格是我設計成可解析的格式;`constants` 只認簡單賦值。

---

## 來源

- plugin(ai-grocery):`plugins/spec-code-flow/`(本機 `C:\Users\shoot\project\ai-grocery\plugins\spec-code-flow\`)
- 實驗程式:<https://github.com/shooter2062424/Knowledge/tree/main/research/spec-flow-skill>
- 前置:[[ilm-multi-team-spec-workflow]]、[[multi-spec-roundtrip-experiment-python-sim]]、[[spec-code-flow-overview-greenfield-brownfield]]、[[spec-driven-development-landscape-2026]]、[[code-to-spec-reverse-engineering-legacy-codebase]]
