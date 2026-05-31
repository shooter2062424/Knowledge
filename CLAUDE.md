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
- 採 **「大類 → 中類 → 主題」三層** 結構:大類資料夾下分中類(子領域)資料夾,報告放在中類資料夾內(同一中類可放多篇相關報告)。
  - 大類示例:`investing/`(投資)、`technology/`(科技與技術研究)。
  - 現有中類:
    - `investing/`:`strategy`、`derivatives`、`technical-analysis`、`ai-assisted`。
    - `technology/`:`ai-agents`(再分 `foundations`/`autonomy`/`memory-retrieval`/`applications`/`resources`)、`llm-internals`(`architecture`/`inference`/`world-models`)、`ai-productivity`、`applied-ai`(`design`/`forecasting`/`speech-synthesis`)、`telecom`、`github-weekly`(週報 cron 落點)。
  - 路徑示例:`technology/ai-agents/foundations/12-factor-agents.md`、`investing/strategy/just-keep-buying-nick-maggiulli.md`。
  - 新筆記歸到最貼切的中類;若不屬於任何現有中類,可新增中類資料夾並更新 README 索引。
- 資料夾命名一律用 **小寫英文 + 連字號**,保持網址乾淨。
- **筆記檔名一旦建立盡量不要改**(筆記內以 `[[檔名slug]]` 互相連結,改名會讓連結失效)。
- 報告結尾附上「來源」區塊,以 Markdown 超連結列出參考來源。
- **預設分支為 `main`**;完成的筆記應整理到 `main`,讓 repo 首頁直接看到分類。

## 兩個倉庫的分工(重要)
- **本倉庫(Knowledge / knowledgedb)** 只放 **知識整理 report**(繁中筆記)。
- **給 Claude 用的 skill / hook / command / agent** 一律放到另一個倉庫:
  - **ai-grocery**(舊名 claude_marketplace,2026-05-31 改名)— `git@github.com:shooter2062424/ai-grocery.git`(HTTPS: `https://github.com/shooter2062424/ai-grocery.git`)。本機 clone 在 `C:\Users\shoot\project\ai-grocery`。
  - 它是一個 **multi-plugin marketplace**:`.claude-plugin/marketplace.json` 列出所有 plugin;各 plugin 放在 `plugins/<name>/`,內含 `.claude-plugin/plugin.json` 與 `skills/ hooks/ commands/ agents/`。
  - 新增 skill 時:歸到對應類別的 plugin(目前知識/學習類為 `knowledge-tools`);沒有對應類別就新增一個 plugin 並更新 `marketplace.json`。
  - 使用者安裝:`/plugin marketplace add shooter2062424/ai-grocery`(GitHub repo 路徑)→ `/plugin install <plugin>@ai-grocery`(`@` 後用 **marketplace 名稱**,定義在 `marketplace.json` 的 `name`)。repo 名與 marketplace 名稱已統一為 `ai-grocery`。
  - ⚠️ **marketplace 名稱不可含 "claude"**:會觸發 Claude Code 的「仿冒官方 marketplace」防衛而被擋(`marketplace add` 失敗)。這是當初從 `claude_marketplace` 改名的原因。
- **慣例:** 日後若需求同時產生「知識」與「給 Claude 的能力」,report 進本倉庫、skill/plugin 進 ai-grocery,兩邊各自 commit。

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
   - **真正的卡點變成「影片本身有沒有字幕」**:若影片未提供字幕也無自動字幕(`TranscriptsDisabled` / `has no automatic captions`),**先走第 6 步用 Whisper 轉錄**,不要直接退回「非逐字稿」。
6. **影片完全沒有字幕時:下載音訊 + 跑 CPU 版 Whisper 轉錄(使用者指定的首選 fallback,2026-05 實測可行):**
   - 本機已裝 `faster-whisper`(1.2.1)與 `PyAV`(av 16.x);**faster-whisper 透過 PyAV 解碼,可直接吃原始 `.mp4/.m4a/.webm`,不需系統 ffmpeg**(本機 ffmpeg 缺也沒關係)。
   - **下載音訊**:`yt-dlp --no-update --js-runtimes node --remote-components ejs:github -f "bestaudio/best" -o "audio.%(ext)s" <url>`。
     - **關鍵:`--remote-components ejs:github`**(JS challenge solver)。少了它,音訊資料下載常 `HTTP 403 Forbidden`(SABR-only 串流實驗)。
     - **不要**加 `-x --audio-format mp3`(那會需要系統 ffmpeg);直接抓原始檔給 whisper 即可。
   - **轉錄(CPU)**:`WhisperModel('small', device='cpu', compute_type='int8')` → `.transcribe(path, language='zh', vad_filter=True, beam_size=5)`,把 segment 文字寫進暫存 `.txt` 再用 Read 讀(終端機中文會亂碼)。3 分鐘音訊用 small 約數十秒;品質不足可換 `medium`(較慢)。
   - 取得逐字稿後正常整理筆記;**在「來源」標註「該片無字幕,逐字稿以 CPU 版 faster-whisper 轉錄取得,非官方字幕」**(可能有少量聽寫誤差)。
   - **只有當 Whisper 也拿不到**(影片無音訊/下載失敗)才退回「標題 + 說明欄 + 既有知識」並標註「非逐字稿」。
   - 取 metadata(標題/說明欄)時若 `yt-dlp --print > file` 出現亂碼,改用 `yt_dlp` Python API 取 `info` 再用 `open(...,encoding='utf-8')` 寫檔。
