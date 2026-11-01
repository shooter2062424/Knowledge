# ILM 試點工具(pilot)

拿**真實模組**驗證模擬結論用的最小工具,`ilm_check.py` 單檔、無外部相依。
`example/` 是玩具範例(RRC 用 C、MAC 用 C++、CTL 用 Python,兩則訊息),**不是任何公司的真實格式**。

## 試點步驟(兩個模組、各挑 2–3 則真實 ILM)

1. **建 registry**:照 `example/registry.json` 的欄位格式,把兩個模組之間的 ILM 訊息寫進去。
   每個欄位至少填 `kind`(time/index/enum/scaled/flag)、單位或縮放、範圍 `lo/hi`、`default`、`optional`。
   ⚠️ 這一步本身就是試點的第一個產出:填不出來的欄位 = 規格裡根本沒寫的隱含假設。
2. **調 config**:`example/config.json` 的 `read_patterns` 改成貴公司存取欄位的寫法
   (例如 `GET_FIELD(msg, name)`、`msg->name`、`msg.name`、巨集);每條 regex 要有 `field` group,
   可有 `var`(變數名,工具會用變數宣告 `const ILM_X *g` 反查訊息)或 `msg` group。
3. **抽 manifest**:`python ilm_check.py manifest config.json > manifest.json`。
   人工抽查 10 個欄位,算「抽到 / 實際有讀」的比例;`?` 表示判不出是哪則訊息。
4. **注入變更找漏接**:`python ilm_check.py inject registry.json manifest.json`。
   每一行是一個假設的 producer 端變更,右邊是會被通知的模組。
   對照 consumer 程式碼人工判斷:**真的會壞但沒被通知的 = 漏接**(例如動態欄位名、宏展開、讀取被包在 helper 函式)。
5. **再挑 5 個歷史上真的出過事的 ILM 變更**(commit log / 缺陷單),把當時的變更套在 registry 上跑
   `diff` 與 `impact`,看這套當時能不能提前通知到後來出事的模組。這比任何模擬都有說服力。

## 試點要記錄的三個數字

| 指標 | 怎麼量 | 模擬值(僅參考) |
|---|---|---|
| manifest 抽取召回 | 人工抽查的欄位中,工具抽到的比例 | 模擬設定 90% 的讀取是靜態可見(動態 key 占 10%,是設定值不是量測) |
| 注入變更的漏接率 | 步驟 4 人工判定「會壞卻沒通知」的比例 | G2 約 5%、疊加三層約 0.3% |
| 歷史缺陷回放命中 | 步驟 5 當時有被通知到的比例 | 無模擬對照 |

## 已知限制

- 欄位辨識是 regex + 變數宣告反查,不是真的 C/C++ 解析。巨集、模板、經 helper 函式轉手的讀取抓不到。
  真要做好,下一步是 libclang(C/C++)抽 AST,工具介面(manifest 格式)不用變。
- `inject` 的算子是通用的幾種(單位、縮放、極性、base、enum、範圍、default、延遲),不含領域專屬變更。
- 這個工具只做「通知誰」,不做契約測試與端到端 replay(那兩層要接貴公司既有的測試環境)。
