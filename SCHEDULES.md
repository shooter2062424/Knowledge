# 每日自動排程備份(session-only cron 的永久記錄)

> ⚠️ **為什麼需要這個檔案:** Claude Code 的 `CronCreate` 排程是 **session-only** 的——Claude 一關閉就消失,而且**每個排程 7 天後會自動到期**(靜默消失,不會通知)。過期期間累積的內容**不會自動補**。
> 本檔保存四個每日排程的**完整 prompt 原文**,新 session 或發現排程消失時,**直接複製下面的 prompt 給 `CronCreate` 即可重建**。

---

## 快速重建流程

1. **先確認現況:** 用 `CronList` 看四個排程還在不在(job id 每個 session 都會變,只能靠時間與內容辨識)。
2. **重建缺的:** 把下方對應章節的 prompt **原文複製**,用 `CronCreate` 建立(`recurring: true` + 對應的 cron 時間)。
3. **⚠️ 重建後立刻跑一次補檢**(不要等隔天),因為過期期間的新內容不會自動補上。
4. 建議**四個一起重建**讓到期日同步,之後好管理。

| # | 排程 | cron | 說明 |
|---|---|---|---|
| 1 | GitHub Weekly 週報 | `33 6 * * *`(每日 06:33) | 撈 itcoffee66/githubweekly 最新一期 |
| 2 | Gary Chen 頻道 | `10 7 * * *`(每日 07:10) | @garytalksstuff 新影片 |
| 3 | gooaye 記憶更新 | `33 7 * * *`(每日 07:33) | 更新 ai-grocery 的股癌 agent 記憶層 |
| 4 | 美投君 頻道 | `50 7 * * *`(每日 07:50) | @MeiTouJun 新影片(無字幕→Whisper) |

**最近一次重建:2026-08-21**。本 session job id:①`80eb1cba` ②`200075b5` ③`6de64cf1` ④`7682556f`(約 **08-28** 到期)。
(歷輪 job id:2026-07-26 建立的 `a2860f8e` / `c4193a54` / `0c987c21` / `803bb28d` → 08-02 重建為 `5d1c5a23` / `2a785098` / `cae3ee4f` / `ed2ef6c8` → 08-08 重建為 `c5b7e3de` / `bc3e9033` / `ee2f5bc3` / `912caf5c` → 08-12 重建為 `527ace5c` / `33f00fe0` / `695ccbb1` / `b82f9725` → 同日再重建為 `7bedd63f` / `0b7c8c41` / `932d52c3` / `3c3670ba` → 08-15 重建為 `7200afbe` / `32e17b91` / `d1ff4626` / `bff7377f`(**該輪把 CRLF、403 重試、pipe 遮蔽退出碼三個踩坑,以及重建來源索引的步驟寫進 prompt**)→ 08-21 重建為現行的四組(**本輪把 yt_dlp js_runtimes 需為 dict、gooaye pack 改根路徑兩個新踩坑寫進 prompt,並補上 lint_mermaid 與「比對官方文件核實」的步驟**)。每次都是**全刪後統一重建**,讓四個到期日同步。)

---

## 共通踩坑備忘(所有排程適用)

### ⚠️ 去重指令(最重要,踩過兩次)

用 video id 去重時**一律用**:

```bash
grep -rlF --include=*.md -- "<id>" .
```

- `-F` fixed-string、`--` 終止選項解析(**video id 可能以連字號開頭**,如 `-ih9NBMHiU8`,否則被當參數)。
- **`--include=*.md` 必須放在 `--` 之前!** 若寫成 `grep -rF -- "<id>" . --include=*.md`,`--include` 會被當成**檔名** → grep 回 **exit 2**(No such file)→ `if grep …` 走 else → **每支影片都誤報 NEW**,會白跑整批 Whisper。(2026-07-11 踩到,10 支全誤判。)
- 判斷用 exit code:**0=SEEN、非 0=NEW**。
- ⚠️⚠️⚠️ **若把 id 先寫進暫存檔再迴圈讀,寫檔務必指定 `newline='\n'`。** Python 在 Windows 文字模式預設寫 **CRLF**,行尾多出的 `\r` 會讓 `grep -F` 完全找不到 → **22 支全部誤報 NEW**。(2026-08-15 踩到。)正確寫法:
  ```python
  open(path, 'w', newline='\n').write('\n'.join(ids) + '\n')
  ```
  最穩的做法還是**逐支直接 grep**,不要繞暫存檔。

### ⚠️ git commit / push

- **用精準 `git add <檔案>`,不要用 `git add -A`** —— 曾誤把 `grep.exe.stackdump`(grep crash 的 core dump)commit 進 repo。
- commit 訊息用**無 BOM UTF-8 暫存檔**:`printf '%s' '訊息' > .git/COMMIT_MSG_TMP && git commit -q -F .git/COMMIT_MSG_TMP && rm -f .git/COMMIT_MSG_TMP`
- push 若遇 **git-lfs locksverify 錯誤**,改用:
  `git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push -q origin main`

### ⚠️ 新增筆記後要重建來源索引

```bash
python scripts/build_source_index.py
```

會覆寫根目錄的 `INDEX-SOURCES.md`(video id / arXiv 編號 → 筆記對照表)。之後查「這支整理過沒」可直接 `grep -F -- "<id>" INDEX-SOURCES.md`,比全庫掃快。**該檔為自動產生,不要手動編輯。**

### ⚠️ 中文亂碼

- `yt-dlp --print` 標題在終端機會 cp950 亂碼 → 改用 `yt_dlp` Python API 取 info,以 `encoding='utf-8'` 寫檔再 Read。
- 逐字稿一律**寫暫存 `.txt` 再用 Read 讀**。

### ⚠️ yt_dlp Python API 的 js_runtimes 要用 dict(2026-08-20 踩過)

命令列是 `--js-runtimes node`,但 **Python API 要傳 dict**:

```python
o = {'quiet': True, 'skip_download': True, 'js_runtimes': {'node': {}}}   # ✅
# o = {..., 'js_runtimes': ['node']}   # ❌ ValueError: Invalid js_runtimes format
```

> 只在需要拿標題/說明欄等 metadata(終端機會 cp950 亂碼)時才會用到 Python API;純列 id 用命令列即可。

---

### ⚠️ gooaye 的 pack 網址在根路徑(2026-08-20 踩過)

- ✅ `https://whatmkreallysaid.com/pack_manifest.json`
- ✅ `https://whatmkreallysaid.com/transcripts.json.br`(**要帶 `User-Agent` header**)
- ❌ `https://whatmkreallysaid.com/data/transcripts.json.br` —— 舊網址,現在 **404**

> `build_memory.py` 裡的 `PACK_URL` / `MANIFEST_URL` 常數是對的,**遇到 404 先去讀那兩個常數**,不要自己猜路徑。

---

### ⚠️⚠️ 連續 403 = 先檢查 yt-dlp 版本(2026-08-22 踩過)

**症狀**:`--remote-components ejs:github` 有加,但**每一支影片、每一次嘗試都 403**(當天 6 次全掛)。
log 的最後一段會露餡:

```
WARNING: [youtube] [jsc] Error solving n challenge ... found 0 n function possibilities
WARNING: n challenge solving failed: Some formats may be missing
ERROR: unable to download video data: HTTP Error 403: Forbidden
```

**根因**:yt-dlp 的 **n-challenge solver 跟不上當前的 YouTube player** ⇒ 拿到的下載網址沒簽名 ⇒ 403。
當時本機是 **2026.02.04(約半年前)**。

**修法**:

```bash
python -m pip install -U yt-dlp
```

更新到 2026.08.19 後,**第 1 次嘗試就下載成功**。

> ⭐ **判斷準則:**
> - **偶發 403、重試會過** ⇒ 是 SABR 實驗,照原本的「同參數重試 3 次」處理即可
> - ⚠️ **連續 3 次全 403、而且 log 有 `n challenge solving failed`** ⇒ **不是重試能解決的,是版本落後** ⇒ 先 `pip install -U yt-dlp` 再說
>
> ⚠️ 排程 prompt 裡的 `--no-update` 是避免執行中途自動更新,**不代表不該定期手動更新**。

---

### ⚠️ Whisper 轉錄配方

```python
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=6)
segs, info = m.transcribe(path, language='zh', vad_filter=True,
                          condition_on_previous_text=False,   # 防幻覺迴圈
                          no_repeat_ngram_size=3,             # 防幻覺迴圈
                          beam_size=5)
```

- 下載音訊:`yt-dlp --no-update --js-runtimes node --remote-components ejs:github -f "bestaudio/best"`(**`--remote-components` 解 403**)。
- **轉完務必掃結尾**有無「同句重複數十行」(幻覺迴圈)。
- 多支影片時**用單一背景進程串跑**,避免多進程 CPU 競爭。
- ⚠️ **遇 `HTTP Error 403: Forbidden` 就用「同參數重試」(最多 3 次)**,通常第 2~3 次會成功。**不要改 `--extractor-args player_client`** —— 改了會產生假的 `This video is DRM protected` 錯誤,更難查。
- ⚠️ **不要寫 `yt-dlp … | tail -1`** —— pipe 的退出碼是 `tail` 的,**yt-dlp 的失敗會被吞掉**,導致下一步拿不到檔案才報一個看不懂的錯。要看退出碼就用 `${PIPESTATUS[0]}`,或乾脆不接 pipe。

---

## 1. GitHub Weekly 週報整理(每日 06:33 / `33 6 * * *`)

```text
每日 GitHub Weekly 週報整理任務。步驟:
1. 用 WebFetch 撈 https://github.com/itcoffee66/githubweekly/tree/main/_weekly 找期數最大的 NNN.md,取 https://raw.githubusercontent.com/itcoffee66/githubweekly/main/_weekly/NNN.md 全文。(WebFetch 有快取,可另用 curl -s -o /dev/null -w "%{http_code}" 直接驗證下一期是否已發布。)
2. 去重:若 C:\Users\shoot\project\Knowledge\technology\github-weekly\issue-NNN.md 已存在就跳過、只回報、不 commit。
3. 未整理的:依 CLAUDE.md 規範(繁中、必要時 Mermaid、結尾附來源)整理成 technology/github-weekly/issue-NNN.md,逐一列出收錄專案的名稱/用途/亮點/連結。
4. 更新 README.md 的 github-weekly 索引與筆記數 badge,並跑 python scripts/build_source_index.py 重建來源索引。
5. 用無 BOM UTF-8 暫存檔(.git/COMMIT_MSG_TMP,printf '%s')git commit -q -F 提交(繁中訊息、[feat] 前綴)並 git push -q origin main。清暫存。⚠️ 用精準 git add <檔案> 而非 git add -A(避免誤入 grep.exe.stackdump 等垃圾檔)。push 若遇到 git-lfs locksverify 錯誤,改用 git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push -q origin main 重試。
沒有新一期就只回報、不空 commit。完成後回報期數與結果。
⚠️ 上游自 2026-08-03(第 124 期)起已長期無新期,連續空轉多日屬正常,不必特別排查。
(此為 session-only 每日排程,7 天後會自動到期,若仍需要請在到期前用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。)
```

---

## 2. Gary Chen 頻道(每日 07:10 / `10 7 * * *`)

```text
每日整理 Gary Chen YouTube 頻道(@garytalksstuff)新影片到 Knowledge。步驟:
1. 用 yt-dlp --no-update --js-runtimes node --flat-playlist --playlist-end 12 --print "%(id)s" "https://www.youtube.com/@garytalksstuff/videos" 列最新 12 部(標題在終端機會 cp950 亂碼,改用 yt_dlp Python API 取 info 再以 utf-8 寫檔)。
   ⚠️ yt_dlp Python API 的 js_runtimes 參數要用 **dict** 形式 {'node': {}},寫成 list ['node'] 會 ValueError: Invalid js_runtimes format(2026-08-20 踩過)。
2. 去重:用 Grep 在 C:\Users\shoot\project\Knowledge 搜每個 video id(youtu.be/<id> 或 watch?v=<id>),已在既有筆記來源 = 跳過。也可先查 INDEX-SOURCES.md(grep -F -- "<id>" INDEX-SOURCES.md)。
   ⚠️ video id 可能以連字號開頭(如 -ih9NBMHiU8),grep 會把它當參數而誤報 NEW → 一律用 `grep -rlF --include=*.md -- "<id>" .`(-F fixed-string、-- 終止選項解析)。
   ⚠️⚠️ `--include=*.md` 必須放在 `--` 之前!寫成 `grep -rF -- "<id>" . --include=*.md` 會被當成檔名 → exit 2 → 每支都誤報 NEW、白跑整篇(2026-07-11 踩過)。
   ⚠️⚠️⚠️ 若把 id 先寫進暫存檔再迴圈讀,**寫檔務必用 newline='\n'**(Python 在 Windows 預設寫 CRLF,行尾多一個 \r 會讓 grep 全部找不到 → 22 支全誤報 NEW,2026-08-15 踩過)。判斷用 exit code:0=SEEN、非0=NEW。
3. 未整理的:優先抓官方字幕(yt-dlp --write-subs --sub-langs zh-Hant/zh-TW/zh/zh-Hans/en),無官方字幕再抓自動字幕,都無則走 Whisper(下載音訊 --remote-components ejs:github + faster-whisper small/int8 zh,vad_filter=True、condition_on_previous_text=False、no_repeat_ngram_size=3)。⚠️ yt-dlp 遇 HTTP 403 就用同參數重試(最多 3 次),不要改 player_client。⚠️ 不要用 `yt-dlp … | tail -1`,pipe 會遮蔽退出碼讓失敗被吞掉。逐字稿寫暫存檔再用 Read 讀,避免終端機中文亂碼;轉完掃結尾有無同句重複數十行(幻覺迴圈)。
4. 依 CLAUDE.md 寫作規範整理繁中筆記(含應用案例、Mermaid、來源),歸到三層結構最貼切中類(多為 technology/ai-agents/{foundations,autonomy,memory-retrieval,applications,resources}、technology/claude-code 或 technology/ai-productivity;LLM 架構→llm-internals;設計工具→applied-ai/design)。
   ⭐ 影片若提到可查證的官方規格/價格/機制(如 Anthropic 文件、API 定價),務必比對官方來源核實,並在筆記中標出補正處——這是本倉庫的核心價值。
   ⭐ 產出 Mermaid 後跑 python scripts/lint_mermaid.py <檔案> 檢查語法。
5. 更新 README 對應表格、筆記數 badge、Gary Chen 作者索引篇數(主題表格與作者索引兩處都要),並跑 python scripts/build_source_index.py 重建來源索引。無 BOM UTF-8 檔 commit([feat] 前綴)、git push -q origin main。⚠️ 用精準 git add <檔案> 而非 git add -A;遇 git-lfs locksverify 錯誤改用 git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push 重試。清暫存。
無新片只回報、不空 commit。回報新增/略過哪些影片。(session-only 每日排程,7 天後自動到期,到期前若仍需要請用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。)
```

---

## 3. gooaye(股癌)agent 記憶更新(每日 07:33 / `33 7 * * *`)

> ⚠️ 這個排程動的是 **ai-grocery** repo(不是 Knowledge)。教育用途、非投資建議。

```text
每日更新 ai-grocery 的 gooaye(股癌模擬)agent 記憶層。位置:C:\Users\shoot\project\ai-grocery\plugins\investing-like-pro\gooaye\(build_memory.py 在 gooaye/scripts/、記憶檔在 gooaye/references/)。步驟:
1. cd C:\Users\shoot\project\ai-grocery 先 git pull。
2. 記憶來源 whatmkreallysaid.com 的 transcripts.json.br(brotli,需 pip install brotli);用 pack_manifest.json 的 episode_count 比對 references/mention-timeline.json 的 meta.built_at_ep,沒新集就只回報、不 commit。
   ⚠️ manifest 網址是**根路徑** https://whatmkreallysaid.com/pack_manifest.json,不是 /data/ 底下。
   ⚠️⚠️ pack 本身也在**根路徑**:https://whatmkreallysaid.com/transcripts.json.br —— /data/ 底下的舊網址已 404(2026-08-20 踩過)。下載要帶 User-Agent header(參考 build_memory.py 的 PACK_URL 常數,那裡是對的)。
3. 有新集:跑 gooaye/scripts/build_memory.py(會自動下載最新 pack)重算機器檔(mention-timeline.json、ranking.json、recency-ranking.md)→ 由 AI 依最近約 60 集逐字稿重寫 references/recent-stance.md(質化摘要,標非投資建議、集數越大越新)。取最新集逐字稿的方式:用 urllib 下載 transcripts.json.br → brotli.decompress → json.loads 得到 list,每筆有 n/t/d/dt/desc/tx 欄位;把 tx 寫暫存 .txt 再用 Read 讀(避免終端機中文亂碼)。
   ⭐ recent-stance.md 的維護方式:把舊的「🟢 最新進展」降級為「🟡 上一期進展」、再往前的降為「⚪ 更早」,新集數插在最前面;並同步更新第 1–6 節(近期熱度、族群傾向表、退燒項、操作心態、生活、一句話總結)與檔頭的涵蓋範圍與基準集數。
4. 無 BOM UTF-8 暫存檔 commit(繁中訊息)、git push(SSH origin main)。清暫存下載的 pack。
回報更新到第幾集。沒新集不空 commit。⚠️ 教育用途、非投資建議。(session-only 每日排程,7 天後自動到期,到期前若仍需要請用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。)
```

---

## 4. 美投君 / 美投讲美股 頻道(每日 07:50 / `50 7 * * *`)

> ⚠️ 該頻道影片**幾乎都無字幕**、多為 20+ 分鐘,基本上每支都要走 Whisper。

```text
每日整理美投君/美投讲美股(@MeiTouJun)YouTube 新影片到 Knowledge。⚠️ 此頻道影片幾乎都無字幕,多為 20+ 分鐘,需走 Whisper。步驟:
1. 用 yt-dlp --no-update --js-runtimes node --flat-playlist --playlist-end 10 --print "%(id)s|||%(title)s" "https://www.youtube.com/@MeiTouJun/videos" 列最新 10 部。
   ⚠️ 若改用 yt_dlp Python API,js_runtimes 參數要用 **dict** 形式 {'node': {}},寫成 list 會 ValueError(2026-08-20 踩過)。
2. 去重:用 Grep 在 C:\Users\shoot\project\Knowledge 搜每個 video id(youtu.be/<id> 或 watch?v=<id>),已整理過就跳過。也可先查 INDEX-SOURCES.md(grep -F -- "<id>" INDEX-SOURCES.md)。
   ⚠️ video id 可能以連字號開頭(如 -ih9NBMHiU8),grep 會把它當參數而誤報 NEW → 一律用 `grep -rlF --include=*.md -- "<id>" .`(-F fixed-string、-- 終止選項解析)。
   ⚠️⚠️ `--include=*.md` 必須放在 `--` 之前!寫成 `grep -rF -- "<id>" . --include=*.md` 會被當成檔名 → exit 2 → 每支都誤報 NEW、白跑 10 支 Whisper(2026-07-11 踩過)。
   ⚠️⚠️⚠️ 若把 id 先寫進暫存檔再迴圈讀,**寫檔務必用 newline='\n'**(Python 在 Windows 預設寫 CRLF,行尾多一個 \r 會讓 grep 全部找不到 → 全部誤報 NEW,2026-08-15 踩過)。判斷用 exit code:0=SEEN、非0=NEW。
3. 未整理的:先試官方/自動字幕;無則走 Whisper——下載音訊 yt-dlp --no-update --js-runtimes node --remote-components ejs:github -f "bestaudio/best"(--remote-components 解 403),再用 faster-whisper(WhisperModel small, device=cpu, compute_type=int8, cpu_threads=6, transcribe language=zh, vad_filter=True, condition_on_previous_text=False, no_repeat_ngram_size=3)。⚠️ 遇 HTTP 403 就用同參數重試(最多 3 次,間隔 20 秒),不要改 player_client(改了會誤報 DRM protected)。⚠️ 不要用 `yt-dlp … | tail -1`,pipe 會遮蔽退出碼讓失敗被吞掉;要判斷成敗用 ${PIPESTATUS[0]} 或乾脆不接 pipe。segment 寫暫存 .txt 再 Read。轉完掃結尾有無同句重複數十行(幻覺迴圈)。多支影片時用單一背景進程串跑,避免多進程 CPU 競爭。
4. 依 CLAUDE.md 整理繁中筆記(含應用案例、Mermaid、來源註明「該片無字幕,逐字稿以 CPU faster-whisper 轉錄、非官方字幕」、⚠️非投資建議)。歸 investing 中類:個股/產業→equity-research、心法/ETF/被動→strategy、AI 輔助→ai-assisted、選擇權→derivatives、技術分析→technical-analysis、房貸稅務繼承→personal-finance。
   ⭐ 產出 Mermaid 後跑 python scripts/lint_mermaid.py <檔案> 檢查語法。
5. 更新 README 表格、筆記數 badge、美投君作者索引篇數,並跑 python scripts/build_source_index.py 重建來源索引。無 BOM UTF-8 commit([feat] 前綴)、git push -q origin main。⚠️ 用精準 git add <檔案> 而非 git add -A;遇 git-lfs locksverify 錯誤改用 git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push 重試。清暫存(音訊數十 MB)。
無新片只回報、不空 commit。回報新增/略過哪些影片。(session-only 每日排程,7 天後自動到期,到期前若仍需要請用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。)
```

---

## 變更歷程

| 日期 | 事件 |
|---|---|
| 2026-06-06 | 四個排程從「每週日」改為**每天**檢查(有新內容才更新,沒有就略過、不空 commit) |
| 2026-07-11 | 發現 **grep 去重指令 bug**(`--include` 放在 `--` 之後 → 全部誤報 NEW),修正全部 prompt |
| 2026-07-15 | 三個排程到期消失,重建並補檢(補了 GitHub Weekly 第 121/122 期、Gary Chen 1 支) |
| 2026-07-19 | 美投君到期重建 |
| 2026-07-24 | 三個到期重建,prompt 補上 git-lfs locksverify fallback |
| 2026-07-26 | 四個統一重建、到期日同步;**建立本檔案作為永久備份** |
| 2026-08-02 | 到期前主動刪除四個舊排程並統一重建(新 id `5d1c5a23`/`2a785098`/`cae3ee4f`/`ed2ef6c8`),當日四個排程均已正常觸發過、無需補檢 |
| 2026-08-08 | 同樣到期前主動重建(新 id `c5b7e3de`/`bc3e9033`/`ee2f5bc3`/`912caf5c`,約 08-15 到期);當日四個排程均已跑過且皆無新內容,無需補檢 |
| 2026-08-12 | 兩輪重建(`527ace5c`… → `7bedd63f`…) |
| 2026-08-15 | 到期重建為 `7200afbe`/`32e17b91`/`d1ff4626`/`bff7377f`;**把 CRLF 寫檔、403 同參數重試、pipe 遮蔽退出碼三個踩坑寫進全部 prompt**,並加入重建 `INDEX-SOURCES.md` 的步驟 |
| 2026-08-20 | 踩到兩個新坑:**yt_dlp Python API 的 `js_runtimes` 需為 dict**、**gooaye pack 網址改到根路徑**(`/data/` 已 404);當日 Gary Chen 新增 1 篇、gooaye 更新至 EP689 |
| 2026-08-21 | 到期前主動全刪重建為 `80eb1cba`/`200075b5`/`6de64cf1`/`7682556f`(約 **08-28** 到期)。**本輪把上述兩個新踩坑寫進 prompt,並補上 `lint_mermaid.py` 檢查與「影片提到可查證的官方規格/價格時要比對官方文件核實並標出補正」的步驟。** 當日四個排程都已跑過且皆無新內容,無需補檢 |
