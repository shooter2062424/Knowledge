# diagram-design:Claude Code 畫圖 Skill 為什麼沒有「AI 味」——答案在規則,不在模型

**主題分類:** 應用 AI / 設計 —— Agent Skill 的規則設計
**來源影片:** YouTube〈GitHub 冲榜第一的 Claude Code 画图 Skill,翻开源码才知道它凭什么没有AI味〉(YAHA学堂,2026-09-03,約 8 分 20 秒)
**核實對象:** [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)(MIT,已 `git clone --depth 1` 讀 `SKILL.md`、`commands/`,最新 commit 2026-11-03)
**整理日期:** 2026-11-06

> **立場揭露:** 說明欄只有開源 repo、官方安裝指令與 Claude Code / Playwright 連結,**無聯盟連結、無業配聲明**。結尾請求「Hype」為 YouTube 曝光機制。
> **字幕品質:** 自動字幕(簡體),術語如「Scale / Skill」「珊琬色=珊瑚色」「指底=紙底(paper)」「Taste Gate」已校正。

---

## 0. 一句話總結

> **同一個模型,裝了這個 Skill 畫出來就不一樣;差別不在模型,而在 `SKILL.md` 裡寫死的「不可談判」規則與一份出圖前的檢查清單。**
> 影片最有價值的是第 5 分鐘那段:拿來檢視自己寫的 Skill 有沒有任何一條「不可談判」規則。

## 1. 它是什麼(以 repo 現況為準)

- 一個 Agent Skill,輸出是**單一自含的 HTML + inline SVG**(可再匯出 SVG / PNG)。README 自述「45 diagram types. No shadows. No Mermaid slop.」(影片錄製時的星數約 2.6 萬;**我讀到時 GitHub API 顯示 65,290**,影片的數字已過時)。
- 兩種安裝:`npx skills add cathrynlavery/diagram-design`(多宿主),或 Claude Code 內 `/plugin marketplace add cathrynlavery/diagram-design` → `/plugin install diagram-design@diagram-design`(含斜線指令)。
- 斜線指令在 `commands/`:`import-mermaid`、`import-drawio`、`import-excalidraw`、`export-diagram`、`profile`、`doctor`(影片所說「Diagram Design 開頭的命令」)。
- 影片示範的五種情境:讀專案程式碼畫架構圖、從網址抽品牌色、Mermaid 整批翻新、產品經理用的四象限圖、PNG 匯出進 PPT。

```mermaid
flowchart TD
    A["使用者一句話<br/>或 Mermaid 檔"] --> B["先檢查 profile<br/>是否仍為預設配色"]
    B --> C["預設則暫停詢問<br/>先用預設 / 從網站抽取 / 手動給 token"]
    C --> D["選圖型並宣告計畫"]
    D --> E["依規則畫 SVG<br/>刪除原則 4px 網格 連線六規則"]
    E --> F["Taste Gate 檢查清單"]
    F --> G["輸出 HTML<br/>要 PNG 時才匯出"]
```

## 2. 影片的關鍵操作(實用層)

| 步驟 | 內容 | repo 對照 |
|---|---|---|
| 品牌化 | 給一個公開網址,抓首頁 CSS 變數,映射成 5 個角色(紙底、墨色、次要文字、強調、連結),做 WCAG 對比檢查 | `SKILL.md §0` 與 `references/onboarding.md`;語義 token 為 `paper / ink / muted / accent / link` |
| 存檔 | 配色寫在**外掛目錄內**,更新外掛可能被覆蓋 → 另存成 **profile**;專案根目錄放 `.diagram-design` 單行檔,自動切換 | `commands/profile.md`、`references/profiles.md`(第一步先解析 `.diagram-design` marker) |
| Mermaid 翻新 | 先跑**解析腳本**把 Mermaid 拆成表(節點數、邊數、入口、終點、最多連線節點),不渲染、不連網、不執行內容;再畫 | `commands/import-mermaid.md`(支援 `.mmd` 與 Markdown 內 fenced mermaid;預設 `--detail=balanced`) |
| 批次 | 直接說「整個目錄」,流程圖 / 時序圖 / 狀態機自動辨識 | 同上 |
| PNG 匯出 | 沒裝 Playwright 時**貼出安裝指令但不自動安裝** | `export-diagram.md` 第 4 條:「PNG requested but Playwright not installed → surface the install instruction verbatim and stop. Do **not** auto-install.」**已核實** |
| 倍率 | 1000x640 的 viewBox 輸出 2000x1280(2x) | 影片實測,未重現 |

## 3. 「規則」才是主角:影片點名的五條,逐一對原始碼

| 影片說法 | `SKILL.md` 原文 / 位置 | 結果 |
|---|---|---|
| 最高質量的動作通常是**刪除**;永遠一起出現的兩個節點就是一個節點;版面已看得出的關係把線刪掉 | 「The highest-quality move is usually deletion.」「Two nodes that always travel together are one node.」「If the relationship is obvious from layout, remove the line.」(§1) | 已核實 |
| 超過 9 個節點大概是兩張圖;目標密度 4 成 | 「Target density: 4/10…Above 9 nodes, it's probably two diagrams.」 | 已核實 |
| 任何元素不准有陰影 | 反模式表:「Shadow on any element — Shadows are out. Borders are in.」 | 已核實 |
| 圓角有上限 | 「`rounded-2xl` on boxes — Max radius 6–10px or none」 | 已核實 |
| 強調色一張圖最多 2 個元素 | 「accent 1–2 focal elements per diagram」「if you're tempted to accent 4 things, you haven't decided what's focal yet」 | 已核實 |
| 連線 6 條規則「不可談判」,斜線直接不合格 | §6「Non-negotiable」:orthogonal only(圓角直角彎 r=8,r=6 為緊湊下限)、標籤間隙、不重疊、扇出連接點、不穿過非端點方塊、標籤遮罩在節點之前。**「Any breach of the six §6 connector rules → Automatic fail」** | 已核實 |
| 座標 / 字號 / 間距必須是 4 的倍數 | 「Structural geometry sits on a 4px grid」——但注意:**字型大小依角色階梯,不是 4px 網格**(影片說「字號」也是 4 的倍數,**不精確**) | 需修正 |
| Taste Gate「30 幾條」勾完才准交圖 | §9 Pre-Output Checklist,我數到 **38 個勾選項**(`- [ ]`) | 已核實(影片的「30 幾」成立) |

> **影片沒講、但值得知道的設計:** repo 還附了可執行的檢查腳本(`scripts/verify-geometry.py`、`verify-contrast.py`、`lint-render.py` 等,以及許多圖型專屬 `verify-*.py`),也就是把「不可談判」做成**可機器驗證**,而不只是寫在提示詞裡。這才是「規則」真正硬的地方。

## 4. 對寫自己 Skill 的啟示

1. **把審美寫成可判定的規則**:「別太花」無法執行;「強調色最多 2 個」「斜線直接 fail」可以。
2. **用刪除當第一原則**:給模型的不是「加什麼」,而是「還能刪什麼」。
3. **出圖前有檢查清單**(Taste Gate),並盡量配**腳本驗證**。
4. **邊界感**:缺依賴時只提示、不擅自安裝(Playwright 例)。
5. **品牌狀態要抽離到可存檔的 profile**,避免外掛更新蓋掉。

可對照:[[impeccable-frontend-design-skill-ai-slop]](前端設計 Skill 反 AI 味)、[[claude-design-25-tricks-design-rules-skill]](Claude Design 的規則型 Skill)、[[anatomy-skill-object-is-the-explanation]](Skill 本身就是說明)、[[building-claude-skills]](Skill 製作基礎)。

## 5. 應用案例

1. **舊專案的 README 圖更新**:資料夾有 20 張 Mermaid 流程圖,看起來全是預設紫色方塊。裝好 Skill 後說「把 docs/ 裡所有 Mermaid 重畫」,它先逐檔解析節點與邊,再依規則畫;超過 9 個節點的圖會被建議拆成兩張(總覽 + 細節)。
2. **替客戶出架構圖**:每個客戶存一個 profile(配色、字型),各專案根目錄放 `.diagram-design` 指向對應 profile,同一句話「畫出這個專案的架構圖」就自動套客戶品牌。
3. **PM 的優先級四象限**:提供七個功能與大概位置,加一句「焦點放最值得先做的」;依「強調色只用 1–2 處」的規則,整張只有一個珊瑚色象限,避免所有象限都在喊「重要」。
4. **簡報用圖**:`/export-diagram` 匯出透明背景 PNG(2x 像素),沒裝 Playwright 時它會停下來貼安裝指令,由你決定是否裝。

## 核實狀態

- **已核實:** 安裝指令、斜線指令清單、刪除原則、密度與 9 節點規則、無陰影、圓角上限、強調色 1–2、連線六規則、不自動安裝 Playwright、Taste Gate 條數、授權、星數現況。
- **需修正:** 「字號也必須是 4 的倍數」(字型大小依角色階梯)。
- **未能核實:** 影片中的耗時比較(Figma 30 分鐘 vs 1 分多鐘)、倍率輸出與三項渲染修正(CSS 撐寬、位移多兩行、紙色底)為作者實測,我未重跑。

## 來源

- 〈GitHub 冲榜第一的 Claude Code 画图 Skill…〉YAHA学堂,2026-09-03:https://www.youtube.com/watch?v=rq4EHbqaaAk (自動字幕,簡體,非官方人工字幕)
- cathrynlavery/diagram-design(MIT):https://github.com/cathrynlavery/diagram-design
