# Knowledge 倉庫慣例

## 寫作規範
- **所有知識筆記一律使用繁體中文撰寫 Markdown。**
- 適當搭配 **Mermaid** 圖表(flowchart、pie 等)輔助說明。
- **每次產出 Mermaid 圖後,務必反覆檢查語法,確保能正確解析**:
  - 節點/邊標籤若含特殊字元(`( ) / % : , < >` 等),一律以雙引號包起來,例如 `A["約 4%"]`。
  - 換行使用 `<br/>`,且需在引號內。
  - 避免在標籤內直接使用 `>`;可改寫為「大於」等文字。

## 內容組織
- 每個研究主題建立 **獨立的主題資料夾**(例如 `investing/`、`ai-token-save/`),報告放在該資料夾內。
- 報告結尾附上「來源」區塊,以 Markdown 超連結列出參考來源。

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
