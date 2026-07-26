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

**最近一次重建:2026-07-26**。本 session job id:①`a2860f8e` ②`c4193a54` ③`0c987c21` ④`803bb28d`(約 08-02 到期)。

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

### ⚠️ git commit / push

- **用精準 `git add <檔案>`,不要用 `git add -A`** —— 曾誤把 `grep.exe.stackdump`(grep crash 的 core dump)commit 進 repo。
- commit 訊息用**無 BOM UTF-8 暫存檔**:`printf '%s' '訊息' > .git/COMMIT_MSG_TMP && git commit -q -F .git/COMMIT_MSG_TMP && rm -f .git/COMMIT_MSG_TMP`
- push 若遇 **git-lfs locksverify 錯誤**,改用:
  `git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push -q origin main`

### ⚠️ 中文亂碼

- `yt-dlp --print` 標題在終端機會 cp950 亂碼 → 改用 `yt_dlp` Python API 取 info,以 `encoding='utf-8'` 寫檔再 Read。
- 逐字稿一律**寫暫存 `.txt` 再用 Read 讀**。

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

---

## 1. GitHub Weekly 週報整理(每日 06:33 / `33 6 * * *`)

```text
每日 GitHub Weekly 週報整理任務。步驟:
1. 用 WebFetch 撈 https://github.com/itcoffee66/githubweekly/tree/main/_weekly 找期數最大的 NNN.md,取 https://raw.githubusercontent.com/itcoffee66/githubweekly/main/_weekly/NNN.md 全文。(WebFetch 有快取,可另用 curl -s -o /dev/null -w "%{http_code}" 直接驗證下一期是否已發布。)
2. 去重:若 C:\Users\shoot\project\Knowledge\technology\github-weekly\issue-NNN.md 已存在就跳過、只回報、不 commit。
3. 未整理的:依 CLAUDE.md 規範(繁中、必要時 Mermaid、結尾附來源)整理成 technology/github-weekly/issue-NNN.md,逐一列出收錄專案的名稱/用途/亮點/連結。
4. 更新 README.md 的 github-weekly 索引與筆記數 badge。
5. 用無 BOM UTF-8 暫存檔(.git/COMMIT_MSG_TMP,printf '%s')git commit -q -F 提交(繁中訊息、[feat] 前綴)並 git push -q origin main。清暫存。⚠️ 用精準 git add <檔案> 而非 git add -A(避免誤入 grep.exe.stackdump 等垃圾檔)。push 若遇到 git-lfs locksverify 錯誤,改用 git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push -q origin main 重試。
沒有新一期就只回報、不空 commit。完成後回報期數與結果。（此為 session-only 每日排程,7 天後會自動到期,若仍需要請在到期前用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。）
```

---

## 2. Gary Chen 頻道(每日 07:10 / `10 7 * * *`)

```text
每日整理 Gary Chen YouTube 頻道(@garytalksstuff)新影片到 Knowledge。步驟:
1. 用 yt-dlp --no-update --js-runtimes node --flat-playlist --playlist-end 12 --print "%(id)s" "https://www.youtube.com/@garytalksstuff/videos" 列最新 12 部(標題在終端機會 cp950 亂碼,改用 yt_dlp Python API 取 info 再以 utf-8 寫檔)。
2. 去重:用 Grep 在 C:\Users\shoot\project\Knowledge 搜每個 video id(youtu.be/<id> 或 watch?v=<id>),已在既有筆記來源 = 跳過。⚠️ video id 可能以連字號開頭(如 -ih9NBMHiU8),grep 會把它當參數而誤報 NEW → 一律用 `grep -rlF --include=*.md -- "<id>" .`(-F fixed-string、-- 終止選項解析)。⚠️⚠️ 重點:`--include=*.md` 必須放在 `--` 之前!若寫成 `grep -rF -- "<id>" . --include=*.md`,`--include` 會被當成檔名 → grep 回 exit 2(No such file)→ `if grep …` 走 else → 每支影片都誤報 NEW、白跑整篇(2026-07-11 踩過這坑)。判斷用 exit code:0=SEEN、非0=NEW。
3. 未整理的:優先抓官方字幕(yt-dlp --write-subs --sub-langs zh-Hant/zh-TW/zh/zh-Hans/en),無官方字幕再抓自動字幕,都無則走 Whisper(下載音訊 --remote-components ejs:github + faster-whisper small/int8 zh,vad_filter=True、condition_on_previous_text=False、no_repeat_ngram_size=3)。逐字稿寫暫存檔再用 Read 讀,避免終端機中文亂碼。
4. 依 CLAUDE.md 寫作規範整理繁中筆記(含應用案例、Mermaid、來源),歸到三層結構最貼切中類(多為 technology/ai-agents/{foundations,autonomy,memory-retrieval,applications,resources} 或 technology/ai-productivity;LLM 架構→llm-internals;設計工具→applied-ai/design)。
5. 更新 README 對應表格、筆記數 badge、Gary Chen 作者索引篇數(主題表格與作者索引兩處都要)。無 BOM UTF-8 檔 commit([feat] 前綴)、git push -q origin main。⚠️ 用精準 git add <檔案> 而非 git add -A;遇 git-lfs locksverify 錯誤改用 git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push 重試。清暫存。
無新片只回報、不空 commit。回報新增/略過哪些影片。（session-only 每日排程,7 天後自動到期,到期前若仍需要請用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。）
```

---

## 3. gooaye(股癌)agent 記憶更新(每日 07:33 / `33 7 * * *`)

> ⚠️ 這個排程動的是 **ai-grocery** repo(不是 Knowledge)。教育用途、非投資建議。

```text
每日更新 ai-grocery 的 gooaye(股癌模擬)agent 記憶層。位置:C:\Users\shoot\project\ai-grocery\plugins\investing-like-pro\gooaye\(build_memory.py 在 gooaye/scripts/、記憶檔在 gooaye/references/)。步驟:
1. cd C:\Users\shoot\project\ai-grocery 先 git pull。
2. 記憶來源 whatmkreallysaid.com 的 transcripts.json.br(brotli,需 pip install brotli);用 pack_manifest.json 的 episode_count 比對 references/mention-timeline.json 的 meta.built_at_ep,沒新集就只回報、不 commit。
3. 有新集:跑 gooaye/scripts/build_memory.py(會自動下載最新 pack)重算機器檔(mention-timeline.json、ranking.json、recency-ranking.md)→ 由 AI 依最近約 60 集逐字稿重寫 references/recent-stance.md(質化摘要,標非投資建議、集數越大越新)。取最新集逐字稿的方式:用 urllib 下載 transcripts.json.br → brotli.decompress → json.loads 得到 list,每筆有 n/t/d/dt/desc/tx 欄位;把 tx 寫暫存 .txt 再用 Read 讀(避免終端機中文亂碼)。
4. 無 BOM UTF-8 暫存檔 commit(繁中訊息)、git push(SSH origin main)。清暫存下載的 pack。
回報更新到第幾集。沒新集不空 commit。⚠️ 教育用途、非投資建議。（session-only 每日排程,7 天後自動到期,到期前若仍需要請用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。）
```

---

## 4. 美投君 / 美投讲美股 頻道(每日 07:50 / `50 7 * * *`)

> ⚠️ 該頻道影片**幾乎都無字幕**、多為 20+ 分鐘,基本上每支都要走 Whisper。

```text
每日整理美投君/美投讲美股(@MeiTouJun)YouTube 新影片到 Knowledge。⚠️ 此頻道影片幾乎都無字幕,多為 20+ 分鐘,需走 Whisper。步驟:
1. 用 yt-dlp --no-update --js-runtimes node --flat-playlist --playlist-end 10 --print "%(id)s|||%(title)s" "https://www.youtube.com/@MeiTouJun/videos" 列最新 10 部。
2. 去重:用 Grep 在 C:\Users\shoot\project\Knowledge 搜每個 video id(youtu.be/<id> 或 watch?v=<id>),已整理過就跳過。⚠️ video id 可能以連字號開頭(如 -ih9NBMHiU8),grep 會把它當參數而誤報 NEW → 一律用 `grep -rlF --include=*.md -- "<id>" .`(-F fixed-string、-- 終止選項解析)。⚠️⚠️ 重點:`--include=*.md` 必須放在 `--` 之前!若寫成 `grep -rF -- "<id>" . --include=*.md`,`--include` 會被當成檔名 → grep 回 exit 2(No such file)→ `if grep …` 走 else → 每支影片都誤報 NEW,會白跑 10 支 Whisper(2026-07-11 踩過這坑)。判斷用 exit code:0=SEEN、非0=NEW。
3. 未整理的:先試官方/自動字幕;無則走 Whisper——下載音訊 yt-dlp --no-update --js-runtimes node --remote-components ejs:github -f "bestaudio/best"(--remote-components 解 403),再用 faster-whisper(WhisperModel small, device=cpu, compute_type=int8, cpu_threads=6, transcribe language=zh, vad_filter=True, condition_on_previous_text=False, no_repeat_ngram_size=3)。segment 寫暫存 .txt 再 Read。轉完掃結尾有無同句重複數十行(幻覺迴圈)。多支影片時用單一背景進程串跑,避免多進程 CPU 競爭。
4. 依 CLAUDE.md 整理繁中筆記(含應用案例、Mermaid、來源註明「該片無字幕,逐字稿以 CPU faster-whisper 轉錄、非官方字幕」、⚠️非投資建議)。歸 investing 中類:個股/產業→equity-research、心法/ETF/被動→strategy、AI 輔助→ai-assisted、選擇權→derivatives、技術分析→technical-analysis。
5. 更新 README 表格、筆記數 badge、美投君作者索引篇數。無 BOM UTF-8 commit([feat] 前綴)、git push -q origin main。⚠️ 用精準 git add <檔案> 而非 git add -A;遇 git-lfs locksverify 錯誤改用 git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push 重試。清暫存(音訊數十 MB)。
無新片只回報、不空 commit。回報新增/略過哪些影片。（session-only 每日排程,7 天後自動到期,到期前若仍需要請用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。）
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
