# Knowledge 倉庫慣例

## ⏰ 每日自動排程(session 恢復時必看)
- 本倉庫有 **2 個每日 cron 排程**(2026-11-07 合併):**A「YouTube 來源總巡檢」07:03**(GitHub Weekly、Gary Chen、美投君 + 十個巡檢頻道,共 13 個來源)與 **B「`new/` 收件匣」08:37**。⛔ gooaye 已於 2026-10-20 停用,重建時跳過。
- **`new/` 收件匣**:使用者把同一批素材放進一個子資料夾(**一個資料夾 = 一批 = 一個 task**,資料夾內可混多種檔案);整批一起整理(依內容分門別類、先比對既有筆記,相近就增補),完成後資料夾改名加 `done-` 前綴,並在 [`INBOX-LOG.md`](./INBOX-LOG.md) 記一列(批次→筆記),筆記「來源」也寫明批次。`new/` 已列入 `.gitignore`,素材不進版控。
- ⚠️ 這些排程是 **session-only**:Claude 一關就消失,而且**每個 7 天後會自動到期(靜默消失、不通知)**,過期期間的新內容**不會自動補**。
- **完整 prompt 原文與重建流程都存在 [`SCHEDULES.md`](./SCHEDULES.md)** —— 新 session 開始、或發現排程沒觸發時,先用 `CronList` 檢查,缺的就照 `SCHEDULES.md` 複製 prompt 用 `CronCreate` 重建,**並立刻跑一次補檢**(不要等隔天)。
- ⭐ **排程紀錄一律推上 GitHub**(使用者 2026-10-24 要求,方便換電腦恢復):凡是新增/停用/改 prompt/重建排程,`SCHEDULES.md` 要在同一輪 commit 並 `git push origin main`,不可只留本機。換電腦的恢復步驟見 `SCHEDULES.md`「在另一台電腦恢復排程」。
- 該檔也記錄了共通踩坑(去重 grep 指令、git add 精準、LFS push fallback、Whisper 配方)。

## 寫作規範
- ⭐ **素材含圖片:要看、要用,但不貼整頁文字圖**(2026-11-07 使用者要求):筆記 = **可複製的文字內容 + 你的延伸閱讀/查證 + 原稿已做好的精美圖表**。用 `python scripts/media/extract_images.py`:`text` 取可複製文字、`figures` 列內嵌圖(自動標頭像/logo/重複)、`embedded` 取圖表、`crop` 從無文字層頁面裁出圖表區塊、`shrink` 壓縮既有圖;輸出寬 ≤1100px、單檔 ≤220KB,存筆記同層 `assets/<筆記 slug>/`,以 `![說明](assets/<slug>/<檔名>)` 嵌入並解說。⛔ 不要把整頁文字投影片轉成一張大圖。無文字層的輪播式 PDF 由你看圖轉寫成文字。原始大檔仍不進版控,只 `git add` 壓縮後的配圖。
- **所有知識筆記一律使用繁體中文撰寫 Markdown。**
- **每篇筆記都必須包含「應用案例 / 舉例」**:用具體的真實或情境化例子說明該知識怎麼用(可獨立一節「應用案例」,或在各重點處夾帶範例)。避免只有抽象論述。
- **若是程式 / 工具類且有 git repo:先 `git clone` 下載到本機暫存(如 `%TEMP%`),把原始碼讀完再整理**,而不是只看 README/網頁。整理後刪除暫存的 clone(別 commit 進本 repo)。重點放:實際架構、關鍵檔案與函式、真實程式碼片段、可跑的用法範例。
- 適當搭配 **Mermaid** 圖表(flowchart、pie 等)輔助說明。
- **每次產出 Mermaid 圖後,務必反覆檢查語法,確保能正確解析**:
  - 節點/邊標籤若含特殊字元(`( ) / % : , < >` 等),一律以雙引號包起來,例如 `A["約 4%"]`。
  - 換行使用 `<br/>`,且需在引號內。
  - 避免在標籤內直接使用 `>`;可改寫為「大於」等文字。

## 📂 Repo 佈局(2026-08-30 重整)

單一 repo,三個並列的頂層資料夾:

```
knowledge/    知識筆記,維持既有的 大類 → 中類 → 主題 三層結構
research/     研究專案,一個題目一個資料夾(如 pundit-accuracy/)
scripts/      通用腳本,按功能分類
  ├── knowledge/  本庫維護(build_source_index、lint_mermaid)
  ├── youtube/    頻道與影片擷取(collect_channel、discover_channels)
  ├── media/      音訊處理(whisper_transcribe 語音轉文字統一入口、extract_images 配圖)
  └── market/     行情與回測(candlestick)
```

- **筆記路徑一律以 `knowledge/` 開頭**;README 內部連結同樣是 `./knowledge/...`。
- **`scripts/` 底下的腳本必須有完整的 Google style docstring**(brief 與參數說明可用中文)、
  必要處加註解、並標註 type hint。
- `research/` 底下的產出不進來源索引(`build_source_index.py` 會跳過)。
- 研究用的原始資料(逐字稿等第三方內容)放 `research/<題目>/data/`,**不進版控**。

## 內容組織
- 採 **「大類 → 中類 → 主題」三層** 結構:大類資料夾下分中類(子領域)資料夾,報告放在中類資料夾內(同一中類可放多篇相關報告)。
  - 大類示例:`knowledge/investing/`(投資)、`knowledge/technology/`(科技與技術研究)。
  - 現有中類:
    - `knowledge/investing/`:`strategy`、`derivatives`、`technical-analysis`、`ai-assisted`、`equity-research`、`personal-finance`(房貸/稅務/繼承等個人理財與政策)。
    - `knowledge/technology/`:`ai-agents`(再分 `foundations`/`autonomy`/`memory-retrieval`/`applications`/`resources`)、`llm-internals`(`architecture`/`inference`/`world-models`)、`ai-productivity`、`applied-ai`(`design`/`forecasting`/`speech-synthesis`)、`telecom`、`github-weekly`(週報 cron 落點)、`code-dev`(大型程式開發;`spec-code-flow` 放 spec-to-code / code-to-spec 流程,`c-cpp` 放 C/C++ 工具鏈)。
  - 路徑示例:`knowledge/technology/ai-agents/foundations/12-factor-agents.md`、`knowledge/investing/strategy/just-keep-buying-nick-maggiulli.md`。
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
   - ⭐⭐ **語音轉文字一律呼叫 `python scripts/media/whisper_transcribe.py <影片ID、網址或檔案> -o <輸出.txt> [--clip 起-迄 --prompt "詞表"(僅「定點重轉不通順處」時用)]`**(2026-11-08 使用者決定):引擎固定 faster-whisper `large-v3-turbo` int8、參數與 `[m:ss]` 輸出格式都在腳本裡,YouTube ID 會自動下載音訊並清暫存。**不要自己 inline 寫 `WhisperModel(...)`、不要換 `small`**;成敗看最後一行 `segments N`,一律前景執行。下文各處殘留的 inline 轉錄參數僅是歷史說明,以本腳本為準。 ⚠️ **不要自己加 `no_repeat_ngram_size`**(2026-11-08 基準:中文會讓 turbo 的 CER 由約 4% 變 8%,重複詞被迫換字,例如「調查報告」→「調察報告」);腳本已移除,舊文件中提到此參數的配方一律作廢。 ⚠️ **不要預設帶 `--prompt` 詞表**(2026-11-08 十支影片基準:帶詞表 CER 6.9% 比不帶 5.8% 更差、術語召回沒提升;SenseVoice 整體 7.3% 也沒有比 turbo 好,中英夾雜尤其差,故固定 turbo)。流程:先不帶詞表轉錄 → 讀逐字稿 → **只有語句不通順、疑似專有名詞聽錯處**,才用 `--clip 起-迄 --prompt "正確詞表"` 定點重轉並取代;不通順靠讀稿與影片畫面判斷,不能靠 `avg_logprob`(分佈太窄抓不到)。
   - 本機已裝 `faster-whisper`(1.2.1)與 `PyAV`(av 16.x);**faster-whisper 透過 PyAV 解碼,可直接吃原始 `.mp4/.m4a/.webm`,不需系統 ffmpeg**(本機 ffmpeg 缺也沒關係)。
   - **下載音訊**:`yt-dlp --no-update --js-runtimes node --remote-components ejs:github -f "bestaudio/best" -o "audio.%(ext)s" <url>`。
     - **關鍵:`--remote-components ejs:github`**(JS challenge solver)。少了它,音訊資料下載常 `HTTP 403 Forbidden`(SABR-only 串流實驗)。
     - **不要**加 `-x --audio-format mp3`(那會需要系統 ffmpeg);直接抓原始檔給 whisper 即可。
   - **轉錄引擎(2026-06-13 benchmark + 踩雷後:按素材分流):** 詳見 `knowledge/technology/dev-tools/whisper-cpp-vs-faster-whisper-benchmark.md`。**whisper.cpp 比 faster-whisper 快 1.4–1.9×、準確度相同,但無內建 VAD ⇒ 遇背景音樂/長靜音會幻覺迴圈(同句重複數百行)整篇報廢。** 所以:
     - **預設走 faster-whisper(穩):**`WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=6).transcribe(path, language='zh', vad_filter=True, beam_size=5)`——`vad_filter=True` 先切掉非語音段,可直接吃 mp4、不需轉 wav。**只要影片有片頭/轉場配樂/旁白配樂/雜訊(多數 YouTube 影片),一律用這個。**
     - **確定是乾淨單人人聲(演講/純口播、無配樂)才切 whisper.cpp 賺速度:**①用 PyAV 把音訊轉 16kHz mono wav(免 ffmpeg,約 0.5s):`av.open` → `AudioResampler(format='s16',layout='mono',rate=16000)` → 寫 `wave`;②`from pywhispercpp.model import Model; Model('small', n_threads=8, language='zh', print_realtime=False, print_progress=False).transcribe('audio.wav')`。首次自動下載 `ggml-small`。
     - **轉完務必掃一眼結尾有無「同一句重複數十/數百行」**——是 whisper.cpp 幻覺迴圈的徵兆,改用 faster-whisper 重轉。
     - segment 文字寫暫存 `.txt` 再 Read(終端機中文亂碼)。品質不足兩者都可換 `medium`(較慢);換引擎救不了 small 的同音錯字。
   - 取得逐字稿後正常整理筆記;**在「來源」標註「該片無字幕,逐字稿以 CPU 版 Whisper(whisper.cpp / faster-whisper)轉錄取得,非官方字幕」**(可能有少量聽寫誤差);中文影片若原音是英文,轉出來會是英文逐字稿。
   - **只有當 Whisper 也拿不到**(影片無音訊/下載失敗)才退回「標題 + 說明欄 + 既有知識」並標註「非逐字稿」。
   - 取 metadata(標題/說明欄)時若 `yt-dlp --print > file` 出現亂碼,改用 `yt_dlp` Python API 取 `info` 再用 `open(...,encoding='utf-8')` 寫檔。

## 股票 / 交易影片的字幕術語校正(2026-10-27 使用者指正)
- **字幕(官方或 Whisper)常把技術分析術語聽成同音字。整理股票、策略、技術分析內容時,遇到看不懂或語意怪的詞,先用艾略特波浪理論與常見技術分析術語去對,不要望文生義硬翻。**
- ⚠️ 實際踩過:黃培碩 2026-10-27 那集字幕「西坡 / 稀坡 / 稀薄」被誤譯成「下坡」,**正確是 ABC 修正中的「C 波」**(使用者指正)。
- 常見對照(持續補充):

  | 字幕常見寫法 | 正確術語 |
  |---|---|
  | 西坡、稀坡、稀薄 | **C 波** |
  | 一浪 / 二浪…、1234 5 波、五小坡 | 第一波…第五波、五小波(推動浪) |
  | 序尾波、細微波 | 細微波(小級數波浪) |
  | 擴延、擴沿 | 延伸(Extension) |
  | 恆台、橫台 | 橫盤 |
  | 中繼形態、反轉形態 | 中繼型態 / 反轉型態 |
  | 金X、精差、金沙 / 死X、時差、史插 | 金叉 / 死叉 |
  | 當充、撥斷 | 當沖、波段 |
  | 停搎、停搟 / 停歷、停力、挺立 | 停損 / 停利 |
  | 乖理率、怪力 | 乖離率 |
  | 嘎、嘎爆 | 軋(軋空) |
  | 廢半 | 費半(費城半導體指數) |
  | 站在賣房 | 站在賣方 |

- 確定不了的詞,在筆記「字幕還原」列出原字幕與推定術語,標明「推定」,不要當成確定事實。

### 股票名稱校正流程(2026-10-27 使用者要求)
- **字幕裡的股票名稱一律先查表確認存在**,不要照字幕直接寫:
  `python scripts/market/tw_stock_lookup.py query <字幕寫法或代號> ...`
  - 會依序比對:代號、名稱完全相符、已確認別名表 `scripts/market/stock_name_aliases.csv`、去聲調拼音同音、拼音相似度。
  - 清單快取在 `scripts/market/data/`(不進版控);過期或缺檔時跑 `python scripts/market/tw_stock_lookup.py update`。
- **有唸代號** ⇒ 以代號為準。**沒唸代號、只有一個同音候選** ⇒ 仍要問。**候選不止一個或都不像** ⇒ 一定要問。
- ⭐⭐ **只要不確定,務必用 `AskUserQuestion` 把候選列給使用者判斷**,不要自己猜了就寫進筆記。Whisper 對同音字特別容易錯,所以更要校正。
- 使用者確認後,把結果**追加到 `stock_name_aliases.csv`**(確認方式寫「使用者確認」;代號比對寫「字幕同時唸出代號比對」),讓對照表逐步累積。技術分析術語的誤聽則補進上面的術語對照表。

### Whisper 逐字稿一律檢查不合理字眼(2026-10-27 使用者要求,適用所有主題)
- **凡是 Whisper 轉出的逐字稿(以及品質可疑的自動字幕),整理前都要逐段檢查有沒有不合理的字眼**:人名、公司名、產品名、股票名、技術術語、數字、不通順或前後矛盾的句子。Whisper 對同音字特別容易錯。
- 判斷為不合理、又無法用一手來源(官方文件、repo、說明欄、上面的對照表與 `tw_stock_lookup.py`)確定時:
  1. ⭐⭐ **優先用 `AskUserQuestion` 問使用者**,把原字幕、上下文和候選答案列出來讓使用者選。
  2. 使用者沒空回答(例如排程在無人時執行)時,**先記錄到 `TRANSCRIPT-PENDING.md`**(影片、時間點、原字幕、候選、目前筆記寫法),筆記裡標「推定」,之後再問。
- 使用者確認後:股票名寫進 `scripts/market/stock_name_aliases.csv`,術語補進上面的對照表,並把 `TRANSCRIPT-PENDING.md` 對應項目移除、更新筆記。

### 影片筆記的「時間、畫面、延伸」校正流程(2026-11-07 使用者要求,之後一律照做)
完整流程見 skill `video-transcript-verify`(ai-grocery 倉庫,`plugins/knowledge-tools/skills/video-transcript-verify/SKILL.md`);工具是 `scripts/youtube/transcript_tools.py`(`fetch` 帶時間字幕、`find` 精確時間與連結、`frames` 影片截圖)。重點:
1. ⏱️ **時間絕對不可錯**:給使用者的時間點只能來自帶時間逐字稿的 `[m:ss]`(用 `find` 查),禁止「約 X:XX」;逐字稿一律保留時間(官方字幕存 VTT 時間,不要存成無時間純文字);連結提前 10 秒;找不到詞就寫找不到。
2. 👁️ **看影片畫面,不只看字幕**:專有名詞、數字、圖表、論文/repo 畫面處截圖讀圖(白白说大模型、Why QQ 等有燒錄字幕與投影片,可直接讀到正確拼法)。
3. 📚 **依字幕與畫面中的論文/技術/工具 keyword 查一手資料延伸**(arXiv、官方文件、GitHub、官方部落格,有 repo 就 clone 讀),把真的讀到的內容寫進「延伸閱讀與深度補充」,並標「已核實/需修正/未能核實」。
4. 🙋 **需要使用者判斷的題目集中成一頁 Artifact**(每題附「從 X:XX 開始、目標句 Y:YY」連結、`db` 存選擇),不要在對話裡一題一題問;使用者填完後用 `ArtifactData` 讀回、更新筆記並清掉 `TRANSCRIPT-PENDING.md`。
5. 🎙️ 語音辨識:**一律呼叫 `scripts/media/whisper_transcribe.py`(固定 faster-whisper `large-v3-turbo` int8,`--prompt` 帶標題/說明欄/詞表)**,專有名詞仍要畫面校正;SenseVoice-Small 只作純中文口播的備選實驗(未納入腳本),`small` 不再使用。
