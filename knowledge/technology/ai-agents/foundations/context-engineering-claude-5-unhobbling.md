# Claude 5 時代的 Context Engineering 新規則:Claude Code 刪掉 80% 系統提示詞,評測卻沒掉

> 01Coder(小木頭)復盤 Anthropic Claude Code 團隊成員 **Thariq** 的文章《Claude 5 模型上下文工程的新規則》。最驚人的一條:他們把 **Claude Code 的系統提示詞刪掉了 80% 以上,編碼評測卻沒有任何可測的下降**。核心思路 Thariq 稱為 **unhobbling(給模型鬆綁)**。這與本庫 [[gpt-5-6-prompting-guide-openai]](先做減法)、[[bitter-lesson-cut-old-patterns]](模型變強後舊 prompt 拖垮新模型)是同一條線的 Anthropic 版本。

---

## 一、先分清:Prompt vs Context Engineering

你發給 Claude 的一條訊息(prompt),其實只是模型看到的**上下文裡很小的一塊**。真正的上下文是**系統提示詞 + Skills + CLAUDE.md + 記憶**拼裝在一起的結果。設計這些**通用指令**就叫 **上下文工程(Context Engineering)**。

| | **Prompt** | **Context Engineering** |
|---|---|---|
| 面對 | 一次具體任務 | 很多次請求(你甚至不知道用戶下一句問什麼) |
| 能否寫具體 | 可以 | **沒法寫太具體** |

**麻煩在於:模型的能力一直在變強。** Thariq 說他們翻自己團隊用 Claude Code 的對話記錄時發現,經常在**一個請求裡看到互相打架的指令**:

> 系統提示詞說「該寫文檔就寫文檔」,Skills 又說「絕對不要加註釋」,再疊上用戶自己的要求——模型大多數時候還是能猜對你想要什麼,**但它得先花力氣理解這些衝突的指令、推斷你的最終意圖,才能決定怎麼做。**

**這些約束當年是有用的**(老模型能力有限、寫出來常是錯的,只能接受這個取捨);**但新一代模型判斷力夠好,很多約束可以直接刪除**,讓它靠上下文和自己的判斷來決定——這就是 **unhobbling(鬆綁)**。

---

## 二、六組「過去 → 現在」的變化(同一個思路)

```mermaid
flowchart LR
    OLD["過去：模型弱<br/>拼命約束、堆規則/示例<br/>全塞進系統提示詞前面"] -->|unhobbling| NEW["現在：模型強<br/>該刪就刪、給判斷力<br/>設計接口 + 漸進式披露"]
    style NEW fill:#4c8bf5,color:#fff
    style OLD fill:#888,color:#fff
```

| # | 過去 | 現在 |
|---|---|---|
| **1. 給規則 → 給判斷力** | 怕模型闖禍(誤刪檔案),給強硬死規則;甚至在代碼裡寫死「一條註釋都別寫、絕不寫多行註釋塊」——但對愛寫文檔/複雜代碼的人這條就是錯的 | 換成一句話:「**寫出來的代碼要像它周圍的代碼**」——註釋密度、命名風格都跟著上下文走,交給模型判斷 |
| **2. 堆示例 → 設計接口** | 用工具的頭號鐵律是「給模型示例、一步步教它怎麼調」 | 發現**給示例反而把模型框死**;改為**打磨工具本身的設計**——參數取什麼名、枚舉值怎麼定,讓接口自己把用法說清楚。例:Todo 工具狀態只 3 值(`pending`/`in_progress`/`completed`)+ 一句「同時只保留一個 `in_progress`」,模型自然會用 |
| **3. 全塞前面 → 漸進式披露** | 系統提示詞塞一大堆「怎麼做代碼審查、怎麼驗證」的細節——不常用、但用時很關鍵 | **該用時再加載**:把代碼審查/驗證拆成獨立 Skills,模型需要時自己調;工具也**延遲加載**(先用 ToolSearch 搜完整定義才用),平時不佔上下文。**CLAUDE.md 和 Skills 同理——別堆進一個大文件,拆成一棵樹,該加載哪塊就加載哪塊** |
| **4. 反覆叮嚀 → 只說一遍** | 模型更容易聽上下文**末尾**的話、不太理開頭,所以系統提示詞重複提某個工具、工具描述又寫一遍 | 這些重複都刪了——**把怎麼用直接寫進工具描述,不在系統提示詞裡說第二遍** |
| **5. 手動記憶 → 自動記憶** | 鼓勵你用 `#` 快捷鍵把要記的東西寫進 CLAUDE.md | 現在 Claude **會自己把跟當前工作/跟你相關的東西存進記憶**,不用手動記 |
| **6. Markdown 計畫 → 富引用 + rubric** | plan 模式很依賴 Markdown 寫的計畫,長項目把規格存進代碼庫方便回查 | 模型能處理**複雜得多的引用**:不只 Markdown,可以是 artifacts 生成的 HTML、一段代碼、一套詳盡測試、甚至另一個代碼庫裡的某個函數。還有 **rubric(評分標準)**——幫模型摸清你在某領域的偏好(什麼才算好的 API 設計),再派**驗證 agent** 拿這套標準去核對 |

---

## 三、落到你每天要碰的幾個地方(Thariq 的實務建議)

| 對象 | 建議 |
|---|---|
| **系統提示詞** | 和產品強綁定(告訴模型它在哪個產品、在幹什麼)。用 Claude Code 你基本不用改;但**自建 agent 時值得下功夫** |
| **CLAUDE.md** | **保持輕量**:簡單說清楚倉庫是幹嘛的,篇幅主要花在**代碼庫的技術細節**(如「類型全放這個文件」);**別寫模型看一眼文件結構就知道的廢話**,細節交給漸進式披露、拆成 Skill 再引用 |
| **Skills** | 當成**輕量的向導**,讓模型需要時能找到信息,**別寫太死**(除非特別關鍵);長 Skill 拆成多個文件。**它最適合裝屬於你/你團隊/你產品的獨有經驗和判斷** |
| **References** | 用 `@` 引用文件,**盡量用代碼形式的引用**——因為代碼是模型最熟的語言;一個 HTML 設計稿通常比一段文字描述或一張截圖管用得多 |

---

## 四、實戰:拿一組開源 Skills 照新規則改兩處

01Coder 拿自己的開源項目 `boring-video-studio`(做影片用的一組 Skills,按 orchestration / building-blocks / assets 分三層,每個 Skill 是一個 `SKILL.md` + 一個 references 文件夾)示範:

**改法一:漸進式披露拆大文件**
- `blockframe-video` 的 `SKILL.md` 有 **300 多行**,從選定主題、項目格式、目錄結構到渲染、封面、章節化重建全塞在主文件。
- 按漸進式披露:**主文件只留「什麼時候用它、大致骨架、委託給誰」**;格式配置表、項目目錄結構、增量重建這些細節**下沉到 references,用到再加載**。(好在這套 Skills 本來就有 references 習慣,順著拆即可。)

**改法二:區分「該留的鐵律」與「該交給判斷的品味」**
> 文章重點是「Skills 別寫太死,**除非特別關鍵**」——關鍵就在這個「除非」:

| 該留的硬性規定(刪了會出事) | 該交給模型判斷的「品味層面硬話」 |
|---|---|
| 財經影片 Skill:「數字必須核對官方原件」 | 各種寫死的骨架、風格規定 |
| 封面設計 Skill:「codex 會謊報保存路徑」(避坑指南) | → 改成**占位符 + agent 判斷** |

> 作者最近一次提交就是把「平台文案」從寫死的骨架改成**占位符 + agent 判斷**,方向一致。

---

## 五、應用案例

1. **給自己的 CLAUDE.md / Skills 瘦身:** 照六組規則檢查——有沒有「一條註釋都別寫」這種對部分任務就是錯的死規則?有沒有把不常用的細節(代碼審查步驟)全塞前面?把它們改成「跟著上下文走」的判斷句 + 拆成 Skill 漸進加載。Anthropic 還上線了 **`/doctor` 命令**(Claude Code 裡敲 `/doctor`)自動幫 Skills 和 CLAUDE.md 瘦身。
2. **用「接口設計」取代「工具示例」:** 自建 agent 的工具,與其寫一堆調用示例,不如把參數名、枚舉值設計到「一看就懂」(如 Todo 的三狀態 + 一句約束)——讓接口自己說清用法。
3. **保留真正的鐵律、放掉品味規則:** 區分「刪了會出事的避坑指南」(核對官方數字、某工具會謊報路徑)和「品味層面的硬話」(命名/註釋風格)——前者留、後者交給模型。
4. **用富引用取代純文字規格:** 給 agent 的 reference 優先用**代碼/HTML** 而非文字描述或截圖(代碼是模型最熟的語言);設計偏好用 **rubric + 驗證 agent** 表達,而非在 prompt 裡反覆叮嚀。

> 🔎 **對照本庫:** 這與 [[gpt-5-6-prompting-guide-openai]] 的「先做減法、outcome-first、絕對規則只留安全」幾乎逐條對應(OpenAI 與 Anthropic 各自得出同一結論);漸進式披露見 [[markdown-agent-memory]];Skills 裝「獨有經驗判斷」見 [[building-claude-skills]]、[[matt-pocock-skills-teardown]];「模型變強該砍舊約束」是 [[bitter-lesson-cut-old-patterns]] 的主題。

---

## 六、重點回顧(TL;DR)

- **核心事件**:Claude Code 系統提示詞刪 80%+,編碼評測沒下降 → **unhobbling(給模型鬆綁)**。
- **為什麼**:老模型弱、靠約束防錯;新模型判斷力夠,衝突的死規則反而讓它花力氣消解、還可能框死它。
- **六組變化**:①給規則→給判斷力(「代碼要像周圍的代碼」)②堆示例→設計接口(Todo 三狀態)③全塞前面→漸進式披露(拆 Skill/延遲加載/ToolSearch)④反覆叮嚀→只說一遍(寫進工具描述)⑤手動記憶→自動記憶⑥Markdown 計畫→富引用(代碼/HTML/測試)+ rubric + 驗證 agent。
- **實務**:系統提示詞綁產品;CLAUDE.md 輕量講技術細節、別寫廢話;Skills 當輕量向導、裝獨有經驗、別寫太死(除非關鍵);References 優先代碼形式引用。
- **實戰**:300 行 SKILL.md 下沉細節到 references;死骨架 → 占位符+agent 判斷;保留「核對官方數字」這種真鐵律。
- **工具**:Claude Code `/doctor` 自動幫 Skills/CLAUDE.md 瘦身。

---

## 來源

- 影片:[Context Engineering 的全新规则:Claude 5 时代,Claude Code 删掉了 80% 系统提示词(01Coder,2026-07-26,官方 zh 字幕)](https://youtu.be/FrAAxWbxSyE)
- 原文:Thariq(@trq212)〈Claude 5 模型上下文工程的新規則〉(X:x.com/trq212/status/208071097122891806)
- 延伸(本庫):[OpenAI GPT-5.6 官方提示指南(先做減法)](./gpt-5-6-prompting-guide-openai.md)、[Bitter Lesson:模型變強後砍舊 prompt](./bitter-lesson-cut-old-patterns.md)、[AI Agent 記憶管理:Markdown + 漸進式上下文披露](../memory-retrieval/markdown-agent-memory.md)、[Skill 實戰:從製作到維護](../applications/building-claude-skills.md)、[Matt Pocock skills 全拆解(writing-great-skills 修剪)](../applications/matt-pocock-skills-teardown.md)
