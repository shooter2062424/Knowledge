# Knowledge 倉庫慣例

## 寫作規範
- **所有知識筆記一律使用繁體中文撰寫 Markdown。**
- **每篇筆記都必須包含「應用案例 / 舉例」**:用具體的真實或情境化例子說明該知識怎麼用(可獨立一節「應用案例」,或在各重點處夾帶範例)。避免只有抽象論述。
- **若是程式 / 工具類且有 git repo:先 `git clone` 下載到本機暫存(如 `%TEMP%`),把原始碼讀完再整理**,而不是只看 README/網頁。整理後刪除暫存的 clone(別 commit 進本 repo)。重點放:實際架構、關鍵檔案與函式、真實程式碼片段、可跑的用法範例。
- 適當搭配 **Mermaid** 圖表(flowchart、pie 等)輔助說明。
- **每次產出 Mermaid 圖後,務必反覆檢查語法,確保能正確解析**:
  - 節點/邊標籤若含特殊字元(`( ) / % : , < >` 等),一律以雙引號包起來,例如 `A["約 4%"]`。
  - 換行使用 `<br/>`,且需在引號內。
  - 避免在標籤內直接使用 `>`;可改寫為「大於」等文字。

## 內容組織
- 採 **「大類 → 主題」兩層** 結構:先分大類資料夾,再於其下建主題資料夾,報告放主題資料夾內。
  - 大類示例:`investing/`(投資)、`technology/`(科技與技術研究)。
  - 路徑示例:`investing/just-keep-buying/...`、`technology/ai-token-saving/...`、`technology/telecom-3gpp/...`。
- 資料夾命名一律用 **小寫英文 + 連字號**,保持網址乾淨。
- 報告結尾附上「來源」區塊,以 Markdown 超連結列出參考來源。
- **預設分支為 `main`**;完成的筆記應整理到 `main`,讓 repo 首頁直接看到分類。

## 取得 YouTube 逐字稿的流程
1. 先用 `WebFetch` / `WebSearch` 取得標題與內容。
2. **若線上逐字稿服務失效(403/404/被擋),改用 Python 嘗試抓取**,例如:
   - `pip install youtube-transcript-api`,以 `YouTubeTranscriptApi().list(vid)` 與 `.fetch(vid, languages=[...])` 取得字幕。
   - 或 `yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs "zh-Hant,zh,en" <url>`。
3. **若被 IP 封鎖,可嘗試 free proxy 繞過**:抓取免費 proxy 清單(如 proxyscrape、TheSpeedX/PROXY-List),搭配 `youtube-transcript-api` 的 `http_client=requests.Session(proxies=...)` 逐一嘗試。
4. **本遠端環境的實測結論(2026-05):**
   - 直連:`youtube-transcript-api` 得到 `RequestBlocked`(資料中心 IP 被擋);`yt-dlp` 得到 `CERTIFICATE_VERIFY_FAILED`(環境 TLS 攔截代理用自簽憑證)。
   - free proxy:38 個免費 proxy 全數 `ProxyError`——本沙箱只允許走核可出口,無法透過任意第三方 proxy 連到 `youtube.com:443`。
   - **結論:在此遠端環境抓 YouTube 字幕目前不可行**;上述 Python 方法應於使用者本機可運作。退而求其次:以影片標題搜尋相關報導/逐字稿文章還原內容,並於筆記中明確標註「非逐字稿」。
5. **本機(使用者家中電腦)的實測結論(2026-05):**
   - `youtube-transcript-api` 與 `yt-dlp`(2026.02.04)皆已安裝,且本機有 `node` v24 可當 JS runtime,**沒有 IP 被擋或 TLS 問題**——遠端的封鎖在本機不存在。
   - 新版 yt-dlp 抓字幕需 JS runtime,務必加上 `--js-runtimes node`(否則會誤報「has no automatic captions」)。
   - **真正的卡點變成「影片本身有沒有字幕」**:若影片未提供字幕也無自動字幕(`TranscriptsDisabled` / `has no automatic captions`),則任何工具都拿不到逐字稿,此時才退而以標題 + 既有知識還原並標註「非逐字稿」。
