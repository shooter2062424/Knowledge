# Claude Artifact「Install as app」:小工具一鍵裝成桌面 App、權限分級,與「個人軟體時代」的說法核實

**主題分類:** 科技 / AI 生產力 — Claude Artifact 桌面安裝、權限與個人化軟體
**來源:** YouTube〈Major Claude Artifacts Update: Anthropic Strikes SaaS Again〉(Gary Chen @garychenai,2026-11-26,11 分 28 秒;**依自動字幕整理**(無官方字幕,影片為中文口述,術語已對照畫面外的官方文件),時間點取自帶時間字幕)
**整理日期:** 2026-11-27

> ⚠️ **立場揭露:** 作者在說明欄與片尾(約 [10:50](https://www.youtube.com/watch?v=tE-ahWIDFIs&t=650s))推廣自己的 Skool 付費社群與「AI 實戰營」,並說影片附三套提示詞放在付費文章內。**本文不轉述付費內容**。作者也自述「不太喜歡被 Claude 生態系綁住」,立場並非全面吹捧。
> 📎 同為 Anthropic 把工作成品做成網頁/App 的脈絡見 [[anthropic-html-work-pages]];Artifact 的設計向應用見 [[claude-design-review]]。

---

## 1. 一句話

Anthropic 在 2026-11-24 讓 Claude 做出的 Artifact 可以 **直接安裝成 Mac / Windows 桌面 App**:有自己的圖示與獨立視窗、和原 Artifact 是同一份(改了會自動更新),需要時還能向使用者要通知、全域快捷鍵、選單列、甚至「完整電腦存取」。作者的判斷是:這把軟體最貴的「上線並交到使用者手上」那一段也變便宜了。

```mermaid
flowchart LR
    A["對 Claude 描述<br/>要做的小工具"] --> B["Artifact<br/>預覽與分享"]
    B --> C["Install as app<br/>標題選單或右鍵"]
    C --> D["獨立視窗與圖示<br/>Mac Claude Apps 資料夾"]
    D --> E["按需求授權<br/>通知、快捷鍵、選單列"]
    E --> F["最高級:完整電腦存取<br/>讀寫刪檔案、執行程式"]
```

## 2. 影片脈絡(時間連結已提前 10 秒)

| 時間 | 內容 | 連結 |
|---|---|---|
| 0:00 | 開場:YouTube 之於電視台,類比軟體產業 | [前往](https://www.youtube.com/watch?v=tE-ahWIDFIs&t=0s) |
| 0:48 | Artifact 是什麼:能存資料、呼叫 Claude、接連接器 | [前往](https://www.youtube.com/watch?v=tE-ahWIDFIs&t=38s) |
| 2:37 | 11/24 推出 Install as app,beta、各方案陸續開放 | [前往](https://www.youtube.com/watch?v=tE-ahWIDFIs&t=147s) |
| 3:05 | 安裝步驟(標題或右鍵 → Install as app → Install) | [前往](https://www.youtube.com/watch?v=tE-ahWIDFIs&t=175s) |
| 3:41 | 與原 Artifact 是同一個、改了自動更新 | [前往](https://www.youtube.com/watch?v=tE-ahWIDFIs&t=211s) |
| 4:20 | 官方五個示範 App + Felix 的合集 | [前往](https://www.youtube.com/watch?v=tE-ahWIDFIs&t=250s) |
| 5:09 | 權限:通知、快捷鍵、完整電腦存取 | [前往](https://www.youtube.com/watch?v=tE-ahWIDFIs&t=299s) |
| 5:46 | 為何是打 SaaS 的一拳 | [前往](https://www.youtube.com/watch?v=tE-ahWIDFIs&t=336s) |
| 6:28 | 「這是 2015 年就有的 PWA」的反駁與回應 | [前往](https://www.youtube.com/watch?v=tE-ahWIDFIs&t=378s) |
| 8:33 | 三個缺點:綁生態系、手機不能裝、無人審查 | [前往](https://www.youtube.com/watch?v=tE-ahWIDFIs&t=503s) |
| 10:22 | 結論:個人化軟體時代,半年內成預設做法 | [前往](https://www.youtube.com/watch?v=tE-ahWIDFIs&t=612s) |

## 3. 怎麼裝、裝在哪(已對官方教學核實)

- **步驟:** 在 Claude 桌面版打開 Artifact → 點標題或按右鍵 → **Install as app** → 確認 **Install**。官方另說也可在 Share 選單找到,或 Artifact 自帶安裝鈕。
- **最低版本:** Claude for Mac / Windows **6.28899.0 以上**;找不到選項先更新桌面版。
- **位置:** Mac 在「應用程式」下 **Claude Apps** 資料夾(Spotlight 找得到、可釘 Dock);Windows 在開始功能表的 Claude Apps 資料夾或桌面捷徑。桌面版內也可從 **File > Apps** 開啟、解除安裝。
- **試手題(官方範例,影片 2:57 引用):** 對 Claude 說「幫我做一個住在選單列的番茄鐘」,做完再安裝。
- **選單列/系統匣類 App** 關掉視窗後仍在背景執行,要從 Dock(Mac)或系統匣選單(Windows)結束——影片沒提。

## 4. 官方五個示範 App(核實:名稱與用途與官方一致)

| App | 用途 |
|---|---|
| Linnet | 可分圖層的圖片編輯器 |
| Phosphor | 電影感介面的檔案管理器 |
| Sift | 設規則後用 Claude 自動整理資料夾 |
| Tern | 旁邊有 Claude 解釋指令的終端機 |
| Vitals | 選單列/系統匣的電腦效能監控 |

Felix 的「影片編輯器、桌面寵物」合集:說明欄給了 claude.ai 分享連結,**我沒有打開這些 App,未能核實其內容**。

## 5. 權限分級與風險(影片講對大方向,官方補了更多細節)

官方公告把能力分成三級:**預設**(等同瀏覽器)、**App 權限**(視窗置頂、全域快捷鍵、通知、選單列)、**完整電腦存取**(執行程式、讀寫刪檔案,不必每次詢問)。

| 項目 | 影片說法 | 官方說明 | 核實 |
|---|---|---|---|
| 更新後重新詢問 | 有更新(含自己改)就再問 | 「Allow」只對單一版本有效,更新後再問 | ✅ |
| 完整存取限自己/公司內部做的 | 原則上只開放給自己或內部成員 | 若有組織外的人寫了其中一部分、或無法確認作者,通常不讓 App 申請;免費/Pro/Max/Ultra 方案「組織外」= 你以外的任何人 | ✅(官方更精確) |
| 無人審查 | 「安裝之前不會審查」 | 原文 "Anthropic doesn't review apps before you install them" | ✅ |
| 必須上線且登入 | 沒網路、沒登入打不開 | 原文:必須上線並登入 Claude Desktop 才能開啟 | ✅ |
| 分享者取消分享 → App 失效 | 對方刪除或取消分享,你的也不能用 | 失去存取權時其程式也會停止,可能最多約 20 分鐘,離線或換組織時更久;開啟時 Claude 通常會提議解除安裝 | ✅ |
| 只支援 Mac/Windows 桌面版 | 網頁、手機、Linux 不行 | 原文:不支援 Linux、網頁、行動裝置 | ✅ |
| 免費方案也陸續開放 | 所有方案陸續開放 | Free、Pro、Max、Ultra、Team、Enterprise 皆 beta | ✅(但見下一列) |

**影片沒講、使用前該知道的官方細節:**

- **Team:** 功能預設開,但「完整電腦存取」要管理員開;**Enterprise:** 整個功能預設關,要 owner 在 Organization settings > Artifacts 開。
- 「Don't allow」會一直生效直到你改;若 App **從其他網站載入程式碼,那段程式碼可在沒有新提示下改變**——所以「每次更新重問」不能保證內容不變。
- 打開 App 與 App 對 Claude 的請求 **計入方案用量上限**。
- 以 Docs、Slides、Sheets 範本做的 Artifact 與 Cowork 的 live artifact **不能安裝**;HIPAA-ready 組織不可用。
- 關閉完整存取會停止 App 啟動的程式,**但不會還原已做的修改**。

## 6. 影片的論點與我的核實

| 論點 | 核實 |
|---|---|
| 「裝好不用處理打包與簽章、也不用另設 API key 或重新登入」(3:51) | ⚠️ **部分未能核實**:官方教學沒寫簽章/打包;「不用重新登入」與官方「須登入 Claude Desktop」並不矛盾(沿用桌面版登入),但「不用 API key」只是 App 沿用你的 Claude 身分,**用量仍計入方案額度** |
| 「把網頁裝成桌面 App 是 2015 年的 PWA」(6:28) | ⚠️ 未能核實(我沒有查 PWA 年份;官方也說瀏覽器的「Add to Dock」只是捷徑,缺少桌面權限這層) |
| 「最先被打到的是小工具型軟體(進度表、報表、檢查清單)」 | 作者判斷,非可核實事實;但與官方定位「個人/組織內部小 App」吻合 |
| 「半年內會變成做小工具的預設方式」(10:38) | 作者預測,**無法核實** |
| 「大型系統(CRM、會計)短期不會被換掉」 | 作者經驗判斷,合理但屬意見 |

**判讀:** 技術上新的不是「安裝」,而是 **「描述→生成→分享→存資料→管權限→安裝」同一個平台走完**(作者自己也這樣說,6:38)。真正的代價是三個:綁生態系(離線與未登入不能用)、手機不能裝、**無人審查卻可能握有刪檔權限**。

## 7. 應用案例

- **自己做的小工具(適合授權):** 對 Claude 說「做一個只服務我們五人團隊的新人報到檢查清單,資料要存起來」,先用預設權限安裝。需要桌面提醒再單獨允許「通知」,不要一開始就給完整存取。
- **別人傳來的 App(先別給完整存取):** 官方立場是完整存取原則上只給自己或組織內部做的;若同事傳來檔案整理類 App,先只用預設權限,並確認它是否從外站載入程式碼(外站內容可改,不會再問你)。
- **團隊用量管控:** Team 管理員可關閉「完整電腦存取」;Enterprise 預設整個功能關閉,要導入前先確認管理後台。

## 8. 相關筆記

- [[anthropic-html-work-pages]] — Anthropic 內部把工作成品做成 HTML 頁面的脈絡
- [[claude-design-review]] — Claude Design 評測,同樣是「對話生成可用成品」
- [[claude-cowork-vs-chat-four-questions]] — Cowork 與 Chat 的分工,對照 Artifact 的定位
- [[claude-app-nine-hidden-settings-memory-skills-dispatch]] — Claude 訂閱裡其他沒打開的設定
- [[claude-code-2026-feature-timeline]] — Claude 近期功能時間軸

## 來源

- [YouTube:Major Claude Artifacts Update: Anthropic Strikes SaaS Again(Gary Chen,2026-11-26)](https://youtu.be/tE-ahWIDFIs)(僅自動字幕,非官方字幕、非逐字稿)
- [Anthropic:Install as app(2026-11-24 公告)](https://claude.com/resources/articles/install-as-app)(已讀全文)
- [Claude 說明中心:Install an artifact as an app](https://support.claude.com/en/articles/18516354-install-an-artifact-as-an-app)(已讀全文)
