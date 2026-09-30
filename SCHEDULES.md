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
| 2 | Gary Chen 頻道 | `10 7 * * *`(每日 07:10) | Gary Chen 新影片(**用 channel ID,不用 handle**) |
| 3 | gooaye 記憶更新 | `33 7 * * *`(每日 07:33) | 更新 ai-grocery 的股癌 agent 記憶層 |
| 4 | 美投君 頻道 | `50 7 * * *`(每日 07:50) | @MeiTouJun 新影片(無字幕→Whisper) |
| 5 | 未涵蓋頻道巡檢 | `12 8 * * *`(每日 08:12) | Why QQ / Caleb / YAHA學堂 / 白白说大模型 / 小Lin说 / Redknot-乔红 |
| 6 | ⭐ `new/` 收件匣 | `37 8 * * *`(每日 08:37) | 使用者丟進 `new/` 的大檔素材,整理完改名 `done-`(2026-09-29 新增) |

**最近一次重建:2026-09-28(使用者要求「續排」,五個全刪重建、到期日對齊至約 10-05)。**
本 session job id:①`ce8e9c59`(GitHub Weekly 06:33) ②`a4206b99`(Gary Chen 07:10) ③`59bd5619`(gooaye 07:33) ④`c8f16d37`(美投君 07:50) ⑤`f8529c0d`(巡檢 08:12)。
⚠️ **本輪發現各節 prompt 備份落後於實際運作版本**(部分停在 08-26 版),已用對話中實際觸發的 prompt 全文覆蓋第 1–4 節,並在第 5 節補上巡檢 prompt 原文;同時更新 GitHub Weekly 空轉天數(56 天)、gooaye 上游停更天數(23 天)、Gary Chen 會員限定 `roUfF8nUYNo`。

**前一次重建:2026-09-24(使用者要求「延伸一下排程」,五個全刪重建、到期日對齊至約 10-01)。**
本 session job id:①`96b0538a`(GitHub Weekly 06:33) ②`4324537b`(Gary Chen 07:10) ③`9f269651`(gooaye 07:33) ④`d2e99ecd`(美投君 07:50) ⑤`3437e688`(巡檢 08:12)。
本輪寫進 prompt 的新經驗:**① 巡檢只評估存量清單外新冒出的 id**(已知存量不必每天重查 metadata);**② 頭條數字要檢查兩邊條件是否相同**(09-23 Dream-RSI「差 162 倍」實為換模型 + 換策略混算、同模型約 1.7 倍;09-24 各家都挑對自己有利的基準);**③ 說明欄常附指令與官方文件連結,Whisper 聽錯的指令直接取說明欄原文**;**④ RSI / Pace the Frontier 後續一律併入 RSI 筆記(已到 §11)**;**⑤「智能體群攻擊 HF」說法 09-19/20/24 三度出現,遇到直接引用 §8.6 補正**。

**前一次重建:2026-09-23**(`07daefe0` / `d4266504` / `98575f73` / `7ec086d3` / `b69c9365`)。

**更早一次重建:2026-09-23(使用者要求「請展延 schedule task」,五個全刪重建、到期日對齊至約 09-30)。**
本 session job id:①`07daefe0`(GitHub Weekly 06:33) ②`d4266504`(Gary Chen 07:10) ③`98575f73`(gooaye 07:33) ④`7ec086d3`(美投君 07:50) ⑤`b69c9365`(巡檢 08:12)。
⚠️ **本輪同時修正 commit 署名**:模型已更新,prompt 內的 trailer 由 `Claude Opus 5` 改為 **`Claude Opus 5.5 (1M context)`**。
本輪新寫進 prompt 的經驗:**① 巡檢動筆前先 `grep` 主題關鍵字確認撞題**(09-22 一支 localhost 教學轉錄完才發現與既有部署筆記高度重疊,白花一支 Whisper);**② 技術架構類影片要確認版本時效性**(09-21 Milvus 那支講的是 2.5 舊架構);**③ 本庫自己也會寫錯,寫「更正」前先對官方來源核實**(09-21 Jev 的 `noul` 事件);**④ 美投君個股類要同時查法說會與分析師報導**(09-21 Viking 枯水規模不在新聞稿);**⑤ Gary Chen 常與 Why QQ / YAHA學堂 撞題**。

**前一次重建:2026-09-20**(`f9c7b0cd` / `84be8194` / `fd79e25f` / `c4679a67` / `bd1da4d6`)。

**更早一次重建:2026-09-20(使用者要求「延長排程」,五個全刪重建、到期日對齊至約 09-27)。**
本 session job id:①`f9c7b0cd`(GitHub Weekly 06:33) ②`84be8194`(Gary Chen 07:10) ③`fd79e25f`(gooaye 07:33) ④`c4679a67`(美投君 07:50) ⑤`bd1da4d6`(巡檢 08:12)。
本輪新寫進 prompt 的經驗:**① Whisper 前景跑時 stderr 仍會印 `Failed to initialize NumPy: _ARRAY_API not found` 的 UserWarning,那只是警告、轉錄會正常完成**(別誤判為失敗,看有沒有印出 segment 行數為準);**② Gary Chen `BbofEyeE2Ek` 為會員限定影片,永久跳過**;**③ 影片若在講開源 repo,務必 clone 讀原始碼再整理**(09-19/20 兩次實測各抓到 3–4 處補正);**④「700 個 agent 協同攻破 Hugging Face」與官方技術時間軸不符,遇到直接引用 RSI 筆記 §8.6 補正,不要照抄**;**⑤ 寫 `[[wikilink]]` 前先 `find` 確認目標存在**;**⑥ 新增 `applied-ai/language-learning` 中類**;**⑦ 已知業配/聯盟連結清單寫進巡檢 prompt**。

**前一次重建:2026-09-16**(五個全刪重建:`2b9ad1dd` / `0cd78bf8` / `a4b03c19` / `51de569e` / `f99874c1`)。

**更早一次重建:2026-09-08(使用者要求「續排」,五個全刪重建、到期日對齊至約 09-15)。**
本 session job id:①`090d60c6`(GitHub Weekly 06:33) ②`29732111`(Gary Chen 07:10) ③`97c35683`(gooaye 07:33) ④`e9197bcb`(美投君 07:50) ⑤`6fe38538`(巡檢 08:12)。
本輪同時把三條經驗寫進 prompt:**長影片 Whisper 要用背景進程 + 輪詢**(前景會逾時)、**影片提到開源專案或官方文件時盡量直接讀一手素材**(如 SKILL.md、部落格原文)、**社群討論串要標明性質**(自述而非研究、無樣本代表性)。

**Gary Chen 排程於 2026-09-06 因 handle 改名單獨重建為 `121696df`(改用 channel ID),已於本輪併入統一重建。**

**最近一次重建:2026-09-04**(使用者要求「恢復 cron task」時順手做的全刪重建)。本 session job id:①`f9a9b1f3` ②`5cb4b8b4` ③`cc2882c1` ④`de16b6ea` ⑤`4446ffdd`(巡檢,約 **09-11** 到期)。
**本輪重點:把 2026-09-03 發現的「去重範圍必須限定 `knowledge/`」修正寫進全部五個 prompt**(先前只有巡檢排程修掉,四個固定排程仍留著 `.` 的潛在誤報),並在全部 prompt 加上 commit 訊息的 Co-Authored-By / Claude-Session trailer 要求。
(歷輪 job id:2026-07-26 建立的 `a2860f8e` / `c4193a54` / `0c987c21` / `803bb28d` → 08-02 重建為 `5d1c5a23` / `2a785098` / `cae3ee4f` / `ed2ef6c8` → 08-08 重建為 `c5b7e3de` / `bc3e9033` / `ee2f5bc3` / `912caf5c` → 08-12 重建為 `527ace5c` / `33f00fe0` / `695ccbb1` / `b82f9725` → 同日再重建為 `7bedd63f` / `0b7c8c41` / `932d52c3` / `3c3670ba` → 08-15 重建為 `7200afbe` / `32e17b91` / `d1ff4626` / `bff7377f`(**該輪把 CRLF、403 重試、pipe 遮蔽退出碼三個踩坑,以及重建來源索引的步驟寫進 prompt**)→ 08-21 重建為 `80eb1cba` / `200075b5` / `6de64cf1` / `7682556f`(**該輪把 yt_dlp js_runtimes 需為 dict、gooaye pack 改根路徑兩個踩坑寫進 prompt,並補上 lint_mermaid 與「比對官方文件核實」的步驟**)→ 08-26 重建為現行的四組(**本輪把 yt-dlp 版本落後的持續性 403、`grep | head` 遮蔽退出碼、來源只寫標題會漏收索引三個新踩坑,以及「同主題優先增補既有筆記而非新開」的慣例寫進 prompt**)。每次都是**全刪後統一重建**,讓四個到期日同步。)

---

## 共通踩坑備忘(所有排程適用)

### ⚠️ 去重指令(最重要,踩過兩次)

> ⚠️⚠️⚠️ **2026-09-03 新增、而且是最陰險的一次:去重範圍必須限定 `knowledge/`。**
>
> ```bash
> grep -rlF --include=*.md -- "<id>" knowledge/     # ✅ 正確
> grep -rlF --include=*.md -- "<id>" .              # ❌ 會誤報
> ```
>
> 原因:本檔(`SCHEDULES.md`)第 5 節存了**巡檢排程的存量清單,裡面就是一堆待處理的 video id**。
> 對整個 repo 搜尋會匹配到那份清單,使**每一支存量都誤報 SEEN**。
>
> **這個 bug 最糟的地方是它不報錯** —— 巡檢會回報「全部 SEEN、無新片」,
> 看起來像順利完成,實際上從此永遠跳過所有存量。實測當天 18 支全數誤報。


用 video id 去重時**一律用**:

```bash
grep -rlF --include=*.md -- "<id>" knowledge/
```

- `-F` fixed-string、`--` 終止選項解析(**video id 可能以連字號開頭**,如 `-ih9NBMHiU8`,否則被當參數)。
- **`--include=*.md` 必須放在 `--` 之前!** 若寫成 `grep -rF -- "<id>" . --include=*.md`,`--include` 會被當成**檔名** → grep 回 **exit 2**(No such file)→ `if grep …` 走 else → **每支影片都誤報 NEW**,會白跑整批 Whisper。(2026-07-11 踩到,10 支全誤判。)
- 判斷用 exit code:**0=SEEN、非 0=NEW**。
- ⚠️⚠️⚠️ **若把 id 先寫進暫存檔再迴圈讀,寫檔務必指定 `newline='\n'`。** Python 在 Windows 文字模式預設寫 **CRLF**,行尾多出的 `\r` 會讓 `grep -F` 完全找不到 → **22 支全部誤報 NEW**。(2026-08-15 踩到。)正確寫法:
  ```python
  open(path, 'w', newline='\n').write('\n'.join(ids) + '\n')
  ```
  最穩的做法還是**逐支直接 grep**,不要繞暫存檔。

### ⚠️⚠️ 頻道 handle 會改,列表一律用 channel ID(2026-09-06 踩到)

**症狀:**`yt-dlp … "https://www.youtube.com/@garytalksstuff/videos"` 突然全數 404:

```
WARNING: [youtube:tab] YouTube said: ERROR - Requested entity was not found.
ERROR: [youtube:tab] @garytalksstuff/videos: Unable to download API page: HTTP Error 404
```

**根因:作者把 handle 從 `@garytalksstuff` 改成了 `@garychenai`。** 頻道本身沒消失,channel ID 也沒變。

**怎麼查出新 handle:**拿任何一支既有筆記裡的 video id 反查 —— 

```python
i = y.extract_info('https://www.youtube.com/watch?v=<既有影片id>', download=False)
print(i['uploader'], i['uploader_id'], i['channel_id'], i['channel_url'])
```

⭐ **修法(治本):列表一律改用 channel ID,不要用 handle** ——
`https://www.youtube.com/channel/<UC…>/videos`。**channel ID 不會因改名而變。**

**全部排程頻道的 channel ID(2026-09-06 逐一實際解析驗證):**

| 頻道(中文名) | channel ID | 當時 handle | 用在哪個排程 |
|---|---|---|---|
| **Gary Chen** | `UC9C3t-3ocL0LiwGRD0gBJ8A` | @garychenai(原 @garytalksstuff) | 排程 2 |
| **美投君 / 美投讲美股** | `UCBUH38E0ngqvmTqdchWunwQ` | @MeiTouJun | 排程 4 |
| **Why QQ** | `UClkMmnf9yOKbYRMfOv1HvwA` | @whycallqq | 排程 5(巡檢) |
| **Caleb Writes Code** | `UCuU9jE4MHHEIyYMbDfUPSew` | @CalebWritesCode | 排程 5 |
| **YAHA學堂** | `UC7ynDhvkWzAxctvxKrkwtsg` | @YAHAClass | 排程 5 |
| **白白说大模型** | `UCHrUrG5wJR1rjKkINFxm8yQ` | @白白说大模型 | 排程 5 |
| **小Lin说** | `UCilwQlk62k1z7aUEZPOB6yw` | @xiao_lin_shuo | 排程 5 |
| **Redknot-乔红** | `UCAf2Y9FGJlE_ByXYF7BXv5g` | @redknot-miaomiao | 排程 5 |

> ⭐ **handle 欄只是給人看的備忘,排程一律用 channel ID。**
> ⭐ **回報時請寫頻道中文名稱,不要只寫 channel ID。**

> ⚠️ 這個坑的嚴重性在於:**404 會讓排程當天直接失敗,而如果沒人看回報,之後每天都失敗** ——
> 與 09-03 那個「靜默誤報 SEEN」不同,這個至少會報錯,但一樣會讓該頻道永遠停更。

---

### ⚠️ git commit / push

- **用精準 `git add <檔案>`,不要用 `git add -A`** —— 曾誤把 `grep.exe.stackdump`(grep crash 的 core dump)commit 進 repo。
- commit 訊息用**無 BOM UTF-8 暫存檔**:`printf '%s' '訊息' > .git/COMMIT_MSG_TMP && git commit -q -F .git/COMMIT_MSG_TMP && rm -f .git/COMMIT_MSG_TMP`
- push 若遇 **git-lfs locksverify 錯誤**,改用:
  `git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push -q origin main`

### ⚠️ 新增筆記後要重建來源索引

```bash
python scripts/knowledge/build_source_index.py
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
每日 GitHub Weekly 週報整理任務。⚠️ Knowledge repo 已於 2026-08-30 重整:筆記在 knowledge/、腳本在 scripts/。步驟:
1. 用 curl -s -o /dev/null -w "%{http_code}" https://raw.githubusercontent.com/itcoffee66/githubweekly/main/_weekly/NNN.md 驗證下一期是否已發布(WebFetch 有快取,用 curl 較準)。找到最大期數後取全文。
2. 去重:若 C:\Users\shoot\project\Knowledge\knowledge\technology\github-weekly\issue-NNN.md 已存在就跳過、只回報、不 commit。
3. 未整理的:依 CLAUDE.md 規範(繁中、必要時 Mermaid、結尾附完整網址來源)整理成 knowledge/technology/github-weekly/issue-NNN.md,逐一列出收錄專案的名稱/用途/亮點/連結。產出 Mermaid 後跑 python scripts/knowledge/lint_mermaid.py <檔案>。
4. 更新 README.md 的 github-weekly 索引與筆記數 badge,並跑 python scripts/knowledge/build_source_index.py 重建來源索引。
5. 用無 BOM UTF-8 暫存檔(.git/COMMIT_MSG_TMP,printf '%s')git commit -q -F 提交(繁中訊息、[type] 前綴)並 git push -q origin main。清暫存。
⚠️ 用精準 git add <檔案> 而非 git add -A(避免誤入 grep.exe.stackdump 等垃圾檔)。
⚠️ push 遇 git-lfs locksverify 錯誤,改用 git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push -q origin main 重試。
⚠️ 不要用 `git push … | grep …; echo $?` 判斷成敗(拿到的是 grep 的退出碼),改用 git rev-parse HEAD 與 origin/main 比對。
⚠️ commit 訊息結尾要加:
Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CjznW7K3y5MRDg2y2UcAKV
沒有新一期就只回報、不空 commit。完成後回報期數與結果。
⚠️ 上游自 2026-08-03(第 124 期)起已長期無新期(截至 2026-09-28 已 56 天),連續空轉多日屬正常,不必特別排查。
(此為 session-only 每日排程,7 天後會自動到期,若仍需要請在到期前用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。)
```

---

## 2. Gary Chen 頻道(每日 07:10 / `10 7 * * *`)

> ⚠️⚠️ **2026-09-06:handle 從 `@garytalksstuff` 改成 `@garychenai`,舊 handle 直接 404。**
> **本排程已改用 channel ID `UC9C3t-3ocL0LiwGRD0gBJ8A`**,不受日後再改名影響。詳見共通踩坑。

```text
每日整理 Gary Chen YouTube 頻道新影片到 Knowledge。⚠️ Knowledge repo 已於 2026-08-30 重整:筆記在 knowledge/、腳本在 scripts/。步驟:
1. 列最新 12 部:
   yt-dlp --no-update --js-runtimes node --flat-playlist --playlist-end 12 --print "%(id)s" "https://www.youtube.com/channel/UC9C3t-3ocL0LiwGRD0gBJ8A/videos"
   ⚠️⚠️ **一定要用 channel ID,不要用 handle** —— 2026-09-06 該頻道把 handle 從 `@garytalksstuff` 改成 `@garychenai`,舊 handle 直接回 404 讓排程整個失敗。**channel ID `UC9C3t-3ocL0LiwGRD0gBJ8A` 不會因改名而變。**
   ⚠️ 若哪天 channel ID 也拉不到,用既有筆記裡任一 video id 反查:extract_info 後看 `uploader`/`uploader_id`/`channel_id`。
   ⚠️ 標題在終端機會 cp950 亂碼,改用 yt_dlp Python API 取 info 再以 utf-8 寫檔;js_runtimes 要用 **dict** {'node': {}},list 會 ValueError。
   ⚠️ Python 印中文/emoji 前先 sys.stdout.reconfigure(encoding='utf-8', errors='replace')。
2. 去重:一律用
   grep -rlF --include=*.md -- "<id>" knowledge/
   ⚠️⚠️⚠️ **範圍必須是 knowledge/,不可用 `.`** —— SCHEDULES.md 存有待處理 video id 清單,對整個 repo 搜尋會讓每一支都誤報 SEEN 且完全不報錯(2026-09-03 踩過,18 支全誤報)。
   ⚠️ -F fixed-string、-- 終止選項解析;--include 必須放在 -- 之前。判斷用 exit code:0=SEEN、非0=NEW。不要用 `grep … | head -1`。逐支直接 grep,不要繞暫存檔。
   ⚠️⚠️ **`BbofEyeE2Ek` 是頻道會員限定影片**(level: Gary AI 實戰營),`extract_info` 直接報 members-only、拿不到 metadata 或字幕,**永久跳過不要重試**。⚠️ `roUfF8nUYNo`(2026-09-27)、`JctGH-SOYBA`(2026-09-29)同為會員限定,永久跳過;該頻道新片常搭配一支會員專屬片。日後若再遇到 members-only 就同樣跳過並記錄。
3. 未整理的:優先抓官方字幕(yt-dlp --write-subs --sub-langs zh-Hant/zh-TW/zh/zh-Hans/en),無官方字幕再抓自動字幕,都無則走 Whisper(下載音訊 --remote-components ejs:github + faster-whisper small/int8 zh,vad_filter=True、condition_on_previous_text=False、no_repeat_ngram_size=3、beam_size=5)。⚠️ 遇 HTTP 403 用同參數重試(最多 3 次),不要改 player_client;連續 3 次全 403 且 log 有 `n challenge solving failed` ⇒ 先 python -m pip install -U yt-dlp。⚠️ 字幕下載遇 HTTP 429 就重試(通常第 2–3 次會過)。⚠️ 不要用 `yt-dlp … | tail -1`。逐字稿寫暫存 .txt 再 Read;轉完掃結尾有無同句重複數十行(幻覺迴圈)。
   ⚠️⚠️ **Whisper 一律用「前景」跑,不要用 `nohup ... &` 背景跑** —— 2026-09-13/14 連續兩天踩到:背景 shell 環境變數不完整,torch/numpy import 會失敗(`_ARRAY_API not found` 後直接 Traceback)。前景執行若超過 600s 會自動轉背景,再用 TaskOutput 等它完成即可。
   ⭐ **前景跑時 stderr 仍會印 `Failed to initialize NumPy: _ARRAY_API not found` 的 UserWarning,那只是警告、轉錄會正常完成**(2026-09-19 確認)。看到它不要以為失敗,看最後有沒有印出 segment 行數為準。
4. 依 CLAUDE.md 寫作規範整理繁中筆記(含應用案例、Mermaid、結尾**完整網址**來源),歸三層結構最貼切中類(ai-agents/{foundations,autonomy,memory-retrieval,applications,resources}、claude-code、ai-productivity;LLM 架構→llm-internals;軟體工程→software-engineering;系統設計→system-design;設計工具→applied-ai/design;AI 安全→ai-safety;產業動態→ai-industry;職涯心態→knowledge/career/*)。
   ⭐ 影片若提到可查證的官方規格/價格/機制,務必比對官方來源核實並在筆記標出補正處。⭐ 實測很有效:2026-09-20 查 OpenAI 官方文件補出該片沒提的三個門檻;2026-09-21 查官方 API 文件發現影片把 `score` 的級距上限講錯。
   ⭐⭐ **同主題已有既有筆記時,優先「增補既有筆記」而非新開**;檔名不動,檔頭與來源區塊同時列出兩支影片。⭐ 此頻道與 Why QQ、YAHA學堂 常撞題(Jev 已累積五個來源全部併入同一篇;部署教學 YAHA 也出了一支高度重疊的),**動筆前先 `grep -rl "<關鍵字>" knowledge/` 確認**。
   ⭐ **作者常推廣自家 Patreon / Skool 社群與付費內容,務必在檔頭標明立場,且不要轉述付費素材。**
   ⭐ 產出 Mermaid 後跑 python scripts/knowledge/lint_mermaid.py <檔案>。⚠️ Mermaid 節點避免用圓形語法 `(("文字"))`,lint 會報 UNQUOTED-SPECIAL;一律用方括號 `["文字"]`。
   ⭐ 寫 `[[wikilink]]` 前先 `find knowledge -name "<slug>.md"` 確認目標存在。
5. 更新 README 主題表格、筆記數 badge、Gary Chen 作者索引篇數(兩處都要;⚠️ 索引標題已於 09-06 改為 `@garychenai`),跑 python scripts/knowledge/build_source_index.py。無 BOM UTF-8 檔 commit([feat] 前綴)、git push -q origin main。⚠️ 精準 git add <檔案>,不要 git add -A;遇 git-lfs locksverify 錯誤改用 git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push 重試;不要用 pipe 判斷 push 成敗,改用 git rev-parse 比對。清暫存。
⚠️ commit 訊息結尾要加:
Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CjznW7K3y5MRDg2y2UcAKV
無新片只回報、不空 commit。回報新增/略過哪些影片。(session-only 每日排程,7 天後自動到期,到期前若仍需要請用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。)
```

---

## 3. gooaye(股癌)agent 記憶更新(每日 07:33 / `33 7 * * *`)

> ⚠️ 這個排程動的是 **ai-grocery** repo(不是 Knowledge)。教育用途、非投資建議。

```text
每日更新 ai-grocery 的 gooaye(股癌模擬)agent 記憶層。⚠️ 這個排程動的是 ai-grocery repo(不是 Knowledge)。教育用途、非投資建議。位置:C:\Users\shoot\project\ai-grocery\plugins\investing-like-pro\gooaye\(build_memory.py 在 gooaye/scripts/、記憶檔在 gooaye/references/)。步驟:
1. cd C:\Users\shoot\project\ai-grocery 先 git pull。
2. 記憶來源 whatmkreallysaid.com 的 transcripts.json.br(brotli,需 pip install brotli);用 pack_manifest.json 的 episode_count 比對 references/mention-timeline.json 的 meta.built_at_ep,沒新集就只回報、不 commit。
   ⭐ 順手看一下 manifest 的 `built_at` 欄位:若它也停在舊日期,代表**上游抓取站本身停止重建**(而非股癌沒更新)——截至 2026-09-27 查證,`built_at` 仍停在 `2026-09-04T06:33:28Z`,episode_count 已連續 23 天停在 693,連 `version` 雜湊 `79bd90a9ca0b` 都沒變。回報時可一併說明。
   ⚠️ 讀 mention-timeline.json 要用 io.open(..., encoding='utf-8'),直接 open 會 cp950 UnicodeDecodeError。
   ⚠️ manifest 網址是**根路徑** https://whatmkreallysaid.com/pack_manifest.json,不是 /data/ 底下。
   ⚠️⚠️ pack 本身也在**根路徑**:https://whatmkreallysaid.com/transcripts.json.br —— /data/ 底下的舊網址已 404(2026-08-20 踩過)。下載要帶 User-Agent header(參考 build_memory.py 的 PACK_URL 常數,那裡是對的)。
3. 有新集:跑 gooaye/scripts/build_memory.py(會自動下載最新 pack)重算機器檔(mention-timeline.json、ranking.json、recency-ranking.md)→ 由 AI 依最近約 60 集逐字稿重寫 references/recent-stance.md(質化摘要,標非投資建議、集數越大越新)。取最新集逐字稿:urllib 下載 transcripts.json.br → brotli.decompress → json.loads 得到 list,每筆有 n/t/d/dt/desc/tx 欄位;把 tx 寫暫存 .txt 再用 Read 讀(避免終端機中文亂碼;檔案大時先切半)。
   ⚠️ Python 印中文/emoji 前先 sys.stdout.reconfigure(encoding='utf-8', errors='replace'),否則 cp950 UnicodeEncodeError 會殺掉腳本。
   ⭐ recent-stance.md 的維護方式:把舊的「🟢 最新進展」降級為「🟡 上一期進展」、再往前降為「⚪ 更早」,新集數插在最前面;並同步更新第 1–6 節(近期熱度、族群傾向表、退燒項、操作心態、生活、一句話總結)與檔頭的涵蓋範圍與基準集數。
   ⭐ 實作建議:用 Python 腳本做「精準字串替換 + 插入」(每次 replace 都 assert count==1),比整檔重寫安全;寫檔一律 encoding='utf-8', newline=''。
4. 無 BOM UTF-8 暫存檔 commit(繁中訊息)、git push(SSH origin main)。清暫存下載的 pack。⚠️ 不要用 pipe 判斷 push 成敗,改用 git rev-parse 比對。
⚠️ commit 訊息結尾要加:
Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CjznW7K3y5MRDg2y2UcAKV
回報更新到第幾集。沒新集不空 commit。⚠️ 教育用途、非投資建議。(session-only 每日排程,7 天後自動到期,到期前若仍需要請用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。)
```

---

## 4. 美投君 / 美投讲美股 頻道(每日 07:50 / `50 7 * * *`)

> ⚠️ 該頻道影片**幾乎都無字幕**、多為 20+ 分鐘,基本上每支都要走 Whisper。

```text
每日整理**美投君 / 美投讲美股**(頻道中文名,回報時請用它)YouTube 新影片到 Knowledge。⚠️ 此頻道影片幾乎都無字幕、多為 20+ 分鐘,基本上每支都要走 Whisper。⚠️ Knowledge repo 已於 2026-08-30 重整:筆記在 knowledge/、腳本在 scripts/。步驟:
1. 列最新 10 部:
   yt-dlp --no-update --js-runtimes node --flat-playlist --playlist-end 10 --print "%(id)s" "https://www.youtube.com/channel/UCBUH38E0ngqvmTqdchWunwQ/videos"
   ⚠️⚠️ **一定要用 channel ID `UCBUH38E0ngqvmTqdchWunwQ`(頻道:美投讲美股,當時 handle 為 @MeiTouJun),不要用 handle** —— 2026-09-06 Gary Chen 把 handle 改掉導致排程整個 404 失敗,**channel ID 不會因改名而變**。
   ⚠️ 若哪天連 channel ID 也拉不到,用既有筆記裡任一該頻道的 video id 反查:extract_info 後看 `uploader`/`uploader_id`/`channel_id`。
   ⚠️ yt_dlp Python API 的 js_runtimes 要用 **dict** {'node': {}},list 會 ValueError。
   ⚠️ Python 印中文/emoji 前先 sys.stdout.reconfigure(encoding='utf-8', errors='replace')。
2. 去重:一律用
   grep -rlF --include=*.md -- "<id>" knowledge/
   ⚠️⚠️⚠️ **範圍必須是 knowledge/,不可用 `.`** —— SCHEDULES.md 存有待處理 video id 清單,對整個 repo 搜尋會讓每一支都誤報 SEEN 且完全不報錯(2026-09-03 踩過,18 支全誤報)。
   ⚠️ -F fixed-string、-- 終止選項解析(id 可能以連字號開頭如 -ih9NBMHiU8);--include 必須放在 -- 之前。判斷用 exit code:0=SEEN、非0=NEW。不要用 `grep … | head -1`。逐支直接 grep,不要繞暫存檔。
3. 未整理的:先試官方/自動字幕;無則走 Whisper——下載音訊 yt-dlp --no-update --js-runtimes node --remote-components ejs:github -f "bestaudio/best"(--remote-components 解 403),再用 faster-whisper(WhisperModel small, device=cpu, compute_type=int8, cpu_threads=6, transcribe language=zh, vad_filter=True, condition_on_previous_text=False, no_repeat_ngram_size=3, beam_size=5)。⚠️ 遇 HTTP 403 用同參數重試(最多 3 次,間隔 20 秒),不要改 player_client(會誤報 DRM protected);連續 3 次全 403 且 log 有 `n challenge solving failed` ⇒ 先 python -m pip install -U yt-dlp。⚠️ 字幕下載遇 HTTP 429 就重試。⚠️ 不要用 `yt-dlp … | tail -1`;要判斷成敗用 ${PIPESTATUS[0]} 或不接 pipe。
   ⚠️⚠️ **Whisper 一律用「前景」跑,不要用 `nohup ... &` 背景跑** —— 2026-09-13/14 連續兩天踩到:背景 shell 環境變數不完整,torch/numpy import 會失敗(`_ARRAY_API not found` 後直接 Traceback)。20+ 分鐘的影片約需 8–12 分鐘,前景超過 600s 會自動轉背景,再用 TaskOutput 等它完成即可。segment 寫暫存 .txt 再 Read(大檔先切半)。轉完掃有無同句重複數十行(幻覺迴圈)。多支影片串著跑,避免 CPU 競爭。
   ⭐ **前景跑時 stderr 仍會印 `Failed to initialize NumPy: _ARRAY_API not found` 的 UserWarning,那只是警告、轉錄會正常完成**(2026-09-19 確認)。看到它不要以為失敗,看最後有沒有印出 segment 行數為準。
4. 依 CLAUDE.md 整理繁中筆記(含應用案例、Mermaid、來源註明「該片無字幕,逐字稿以 CPU faster-whisper 轉錄、非官方字幕」、⚠️非投資建議)。歸 knowledge/investing/ 中類:個股/產業→equity-research、心法/ETF/被動/宏觀市場研判→strategy、AI 輔助→ai-assisted、選擇權→derivatives、技術分析→technical-analysis、房貸稅務繼承→personal-finance。
   ⭐ Whisper 對人名與數字容易出錯,在來源區塊列出已還原的專有名詞對照(如「卧石」→沃什)。此頻道常見誤轉:「美肤/美肱/美肯」→美股、「美戛/美倔/美借」→美債、「美職儲/美聀儲」→聯準會、「風陷/風陰」→風險、「導火鎖」→導火線。
   ⭐ **數字務必逐項核實**:財報類比對 SEC/官方 IR、股價與漲跌幅比對公開資料,並在筆記中列出「已核實 / 需修正 / 未能核實」三類。未獨立查證的要明講。文末重申非投資建議。
   ⭐⭐ **新聞稿不會寫的風險細節通常在法說會 Q&A 裡**(2026-09-21 Viking 那篇實測:枯水規模完全不在財報新聞稿,是查法說會與分析師報導才挖到的,而影片把它講小了)。個股類務必同時查法說會與分析師報導。
   ⭐⭐ **核心 CPI 與核心 PCE 不可混用**(2026-09-14 踩過):核心 CPI 與聯準會偏好的核心 PCE 是兩個指標、數字差距明顯,引用時要講清楚是哪一個。
   ⭐ 此頻道常為「美投 Pro」付費訂閱做推廣,**務必在檔頭標明立場,不轉述付費素材**。
   ⭐ 產出 Mermaid 後跑 python scripts/knowledge/lint_mermaid.py <檔案>。⚠️ Mermaid 節點避免用圓形語法 `(("文字"))`,lint 會報 UNQUOTED-SPECIAL;一律用方括號 `["文字"]`。
5. 更新 README 表格、筆記數 badge、美投君作者索引篇數,跑 python scripts/knowledge/build_source_index.py(⚠️ 來源要放**完整網址**,只寫標題會漏收)。無 BOM UTF-8 commit([feat] 前綴)、git push -q origin main。⚠️ 精準 git add <檔案>,不要 git add -A;遇 git-lfs locksverify 錯誤改用 git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push 重試;不要用 pipe 判斷 push 成敗,改用 git rev-parse 比對。清暫存(音訊數十 MB)。
⚠️ commit 訊息結尾要加:
Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CjznW7K3y5MRDg2y2UcAKV
無新片只回報、不空 commit。**回報時用頻道中文名稱「美投君 / 美投讲美股」**,列出新增/略過哪些影片。(session-only 每日排程,7 天後自動到期,到期前若仍需要請用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。)
```

---

## 5. 未涵蓋頻道每日巡檢(每日 08:12 / `12 8 * * *`)

> 2026-09-01 新增,同日首次執行後依實測結果修訂。緣由:盤點發現 README 作者索引共 **49 位,
> 先前僅 3 位有排程涵蓋**,pi agent / MCP / Codex / CS336 等內容都得靠手動丟連結補。

### prompt 原文(2026-09-28 同步自實際運作版本)

```text
每日巡檢六個「有累積但沒有專屬排程」的頻道,把新影片整理進 Knowledge。⚠️ Knowledge repo 已於 2026-08-30 重整:筆記在 knowledge/、腳本在 scripts/。

⚠️⚠️ **頻道一律用 channel ID,不要用 handle** —— 2026-09-06 Gary Chen 把 handle 從 `@garytalksstuff` 改成 `@garychenai`,舊 handle 直接 404 讓當天排程整個失敗。**channel ID 不會因改名而變。**
若哪天連 channel ID 也拉不到,用既有筆記裡任一該頻道的 video id 反查:extract_info 後看 `uploader`/`uploader_id`/`channel_id`。

頻道清單(channel ID 均已於 2026-09-06 實際解析驗證):

| 頻道 | channel ID | 當時 handle | 字幕 |
|---|---|---|---|
| Why QQ | `UClkMmnf9yOKbYRMfOv1HvwA` | @whycallqq | 官方 zh-Hans |
| Caleb Writes Code | `UCuU9jE4MHHEIyYMbDfUPSew` | @CalebWritesCode | 自動(英文) |
| YAHA學堂 | `UC7ynDhvkWzAxctvxKrkwtsg` | @YAHAClass | 時有時無 |
| 白白说大模型 | `UCHrUrG5wJR1rjKkINFxm8yQ` | @白白说大模型 | 無(需 Whisper) |
| 小Lin说 | `UCilwQlk62k1z7aUEZPOB6yw` | @xiao_lin_shuo | 官方中文 |
| Redknot-乔红 | `UCAf2Y9FGJlE_ByXYF7BXv5g` | @redknot-miaomiao | 多數無(⚠️ `rQR_0WZzjV4` 實測無官方字幕,只有自動英文 ASR) |

步驟:
1. 逐個頻道列最新 6 部:
   yt-dlp --no-update --js-runtimes node --flat-playlist --playlist-end 6 --print "%(id)s" "https://www.youtube.com/channel/<channel ID>/videos"
   ⚠️ 回報時請寫出**頻道中文名稱**(如「Why QQ」「小Lin说」),不要只寫 channel ID,方便使用者閱讀。
2. 去重:一律用
   grep -rlF --include=*.md -- "<id>" knowledge/
   ⚠️⚠️⚠️ **範圍必須是 knowledge/,不可用 `.`** —— SCHEDULES.md 第 5 節存有本排程的存量清單(裡面就是一堆待處理 video id),對整個 repo 搜尋會讓**每一支存量都誤報 SEEN**,而且**完全不報錯**(2026-09-03 踩過,18 支全誤報)。
   ⚠️ -F fixed-string、-- 終止選項解析;--include 放在 -- 之前。exit code:0=SEEN、非0=NEW。不要用 `grep … | head -1`。逐支直接 grep,不要繞暫存檔。
   ⭐ **區分「真正的新片」與「已知存量」**:SCHEDULES.md 第 5 節已列的存量不必每天重新評估,只看清單外新冒出的 id(2026-09-23/24 實測可省下大量 metadata 查詢)。
3. ⚠️⚠️ **產出上限:每次執行最多產出 2–3 篇,其中需 Whisper 者最多 1 支。**(本倉庫每篇都要比對一手來源核實,一次灌一堆等於灌水。)
   ⭐ 挑選優先序:① **能增補既有筆記的優先**(同一工具/同一論文/同一事件的後續)→ ② 有官方或自動字幕的(成本低)→ ③ 其餘依新到舊。
   ⭐⭐ **動筆前先用 `grep -rl "<主題關鍵字>" knowledge/` 確認有無同主題筆記** —— 2026-09-22 實測:YAHA學堂一支 localhost 教學轉錄完才發現與既有部署筆記內容高度重疊,白花一支 Whisper。**能先看標題判斷撞題就先查**。
4. 取逐字稿:優先官方字幕(--write-subs --sub-langs zh-Hant/zh-TW/zh/zh-Hans/en),次之自動字幕(--write-auto-subs),都無才走 Whisper(下載音訊 --remote-components ejs:github + faster-whisper small/int8,vad_filter=True、condition_on_previous_text=False、no_repeat_ngram_size=3、beam_size=5)。⚠️ 403 用同參數重試最多 3 次,不要改 player_client;連續 3 次全 403 且 log 有 `n challenge solving failed` ⇒ 先 python -m pip install -U yt-dlp。⚠️ 字幕下載遇 **HTTP 429 Too Many Requests** 就重試(通常第 2–3 次會過;⚠️ 但 `--write-auto-subs` 被限流較兇,曾連續 7 次全 429,遇到就順延別死磕)。⚠️ 不要用 `yt-dlp … | tail -1`。
   ⚠️⚠️ **Whisper 一律用「前景」跑,不要用 `nohup ... &` 背景跑** —— 2026-09-13/14 連續兩天踩到:背景 shell 環境變數不完整,torch/numpy import 會失敗(`_ARRAY_API not found` 後直接 Traceback)。前景超過 600s 會自動轉背景,再用 TaskOutput 等它完成即可。逐字稿寫暫存 .txt 再 Read。轉完掃結尾有無同句重複數十行(幻覺迴圈)。
   ⭐ **前景跑時 stderr 仍會印 `Failed to initialize NumPy: _ARRAY_API not found` 的 UserWarning,那只是警告、轉錄會正常完成**(2026-09-19 確認)。看到它不要以為失敗,看最後有沒有印出 segment 行數為準。
   ⭐ **影片說明欄常附指令與官方文件連結**(2026-09-23 YAHA 那支 Windows 安裝教學就是),Whisper 容易聽錯的指令直接從說明欄取原文。
   ⚠️ 遇影片被設為私人/會員限定就跳過並記錄,不要重試到底。
   ⚠️ Python 印中文/emoji 前先 sys.stdout.reconfigure(encoding='utf-8', errors='replace')。
5. 依 CLAUDE.md 寫作規範整理繁中筆記(含應用案例、Mermaid、結尾**完整網址**來源),歸三層結構最貼切中類(AI agent→knowledge/technology/ai-agents/*;LLM 架構/推論→knowledge/technology/llm-internals/*;Claude Code→knowledge/technology/claude-code;產業動態→knowledge/technology/ai-industry;AI 安全→knowledge/technology/ai-safety;軟體工程→knowledge/technology/software-engineering;系統設計/密碼學/資料庫→knowledge/technology/system-design;影像/設計工具→knowledge/technology/applied-ai/design;語言學習工具→knowledge/technology/applied-ai/language-learning;職涯與心態→knowledge/career/*;財經/個股→knowledge/investing/* 並標⚠️非投資建議)。
   ⭐⭐ **可查證的官方規格/價格/機制務必比對官方來源核實並標出補正處。影片若提到某個開源專案、官方報告或部落格原文,盡量直接讀那份一手素材** —— 實測這一步經常挖到影片沒講、但更重要的內容(例:讀 Anthropic 威脅情報報告原文才發現有預載台灣 12 個軍事目標的案例;讀 arXiv 2609.11873 才發現影片把 HCI 的高低方向講反了;讀 Milvus 2.6 官方說明才發現影片講的是舊架構,IndexNode 已移除;讀 Dream-RSI 論文才發現「差 162 倍」混了換模型與換策略兩個效果,同模型下約 1.7 倍)。
   ⭐⭐ **頭條數字要檢查「兩邊條件是否相同」** —— 2026-09-23 Dream-RSI 與 09-24 Opus 5.5 vs Sol 兩次實測,影片的對比常把不同模型、不同基準、不同廠商自報的數字放在一起比。
   ⭐⭐ **技術架構類影片要特別確認「版本時效性」** —— 2026-09-21 Milvus 那支講的是 2.5 及更早的元件拆法,照做會白架一套已不需要的 Kafka。
   ⭐⭐⭐ **影片若在講某個開源 repo,務必依 CLAUDE.md 先 `git clone --depth 1` 到暫存讀原始碼再整理,整理完刪除 clone(別 commit 進 repo)** —— 2026-09-19/20/22/23 四次實測,讀 repo 各抓到 2–4 處影片講錯或漏掉的關鍵資訊(09-23 Dream-RSI 影片說「直接給出代碼」,clone 後發現程式碼都還是「準備中」)。
   ⭐ **本庫自己也會寫錯**:2026-09-21 發現 Jev 筆記 §12.7 的「勘誤」本身是錯的(型態名稱確實是 `noul`)。**寫「更正」之前先對官方來源核實,別只憑直覺。**
   ⚠️⚠️ **「700 個 agent / 智能體群協同攻破 Hugging Face」這個說法在多支影片裡反覆出現(09-19、09-20、09-24 都有),但與 Hugging Face 官方技術時間軸不符**(官方:「單一自主 agent 編排整場行動,作為整合系統而非協同蜂群」)。本庫 `rsi-recursive-self-improvement-anthropic.md` §8.6 已查證,**遇到就直接引用該節補正,不要照抄影片說法**。
   ⭐ 同主題已有筆記優先增補、檔名不動,檔頭與來源區塊同時列出兩支影片。⭐ RSI / Pace the Frontier 相關的後續一律併入 `rsi-recursive-self-improvement-anthropic.md`(已到 §11)。
   ⭐ **作者若推廣自家產品、業配或聯盟連結,務必在檔頭標明立場。**(⚠️ YAHA學堂 `CV7HX6qFglc` 說明欄含 `?via=yahaclass` 聯盟連結;Redknot `EsJKkDbHsec` 片中明示「與 ASML 合作出品」= 業配;Caleb 近期影片常夾 JetBrains 等業配段落;小Lin说 常夾 eSIM 等業配。)
   ⭐ **社群討論串、論壇熱帖這類材料要標明性質**(是自述不是研究、無樣本代表性)。
   ⭐ **涉及對特定公司/個人的指控時,務必標明是誰的單方陳述、對方是否回應,並並陳質疑動機的聲音,不做真偽判斷。**(⭐ 兩支影片內容高度重疊時也一樣:只記錄可觀察的重疊事實,不對成因做判斷。)
   ⭐ 產出 Mermaid 後跑 python scripts/knowledge/lint_mermaid.py <檔案>。⚠️ Mermaid 節點避免用圓形語法 `(("文字"))`,lint 會報 UNQUOTED-SPECIAL;一律用方括號 `["文字"]`。
   ⭐ 寫 `[[wikilink]]` 前先 `find knowledge -name "<slug>.md"` 確認目標存在,避免留下死連結。
6. 更新 README 主題表格、筆記數 badge、對應作者索引篇數(兩處都要),跑 python scripts/knowledge/build_source_index.py。無 BOM UTF-8 commit([feat] 前綴,訊息標作者名)、git push -q origin main。⚠️ 精準 git add <檔案>,不要 git add -A;遇 git-lfs locksverify 錯誤改用 git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push 重試;不要用 pipe 判斷 push 成敗,改用 git rev-parse 比對。清暫存(含 clone 與音訊)。
7. 完成後把 SCHEDULES.md 第 5 節的存量清單更新(移除已完成者、加入新片),並在「變更歷程」表最上方插入當日一列。
⚠️ commit 訊息結尾要加:
Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CjznW7K3y5MRDg2y2UcAKV
無新片只回報、不空 commit。**回報時請用頻道中文名稱**,並列出本次新增哪幾篇、各頻道剩餘存量。(session-only 每日排程,7 天後自動到期,到期前若仍需要請用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md。)
```

### 頻道清單(⚠️ 2026-09-06 起一律用 channel ID,handle 只是給人看的備忘)

| 頻道(中文名) | channel ID | 當時 handle | 字幕 | 片長 |
|---|---|---|---|---|
| **Why QQ** | `UClkMmnf9yOKbYRMfOv1HvwA` | @whycallqq | 官方 zh-Hans | 10–18 分 |
| **Caleb Writes Code** | `UCuU9jE4MHHEIyYMbDfUPSew` | @CalebWritesCode | 自動(英文) | 8–11 分 |
| **YAHA學堂** | `UC7ynDhvkWzAxctvxKrkwtsg` | @YAHAClass | 時有時無 | 8–14 分 |
| **白白说大模型** | `UCHrUrG5wJR1rjKkINFxm8yQ` | @白白说大模型 | **無** | 8–19 分 |
| **小Lin说** | `UCilwQlk62k1z7aUEZPOB6yw` | @xiao_lin_shuo | **官方中文** | 15–29 分 |
| **Redknot-乔红** | `UCAf2Y9FGJlE_ByXYF7BXv5g` | @redknot-miaomiao | 多數**無** | 14–19 分 |

> ⭐ 列表網址一律寫成 `https://www.youtube.com/channel/<channel ID>/videos`。

**已移除:`@TheStormMedia`(風傳媒 下班經濟學)** —— 首次巡檢實測六支裡**三支會員限定抓不到**,
免費部分偏健康與政論(還有一支 56 分鐘政論),與本倉庫主題距離遠、成本效益不佳。

### ⚠️⚠️ 產出上限(這個排程最重要的設計)

**每次執行最多產出 2–3 篇,其中需 Whisper 者最多 1 支。**

首次巡檢(2026-09-01)發現當時五個頻道有 **32 支存量未整理**(2026-09-02 加入小Lin说後約 39 支) ——
原本 prompt 寫「有字幕者數量不限」,照字面執行會一次寫出 15 篇。
**本倉庫每篇都要比對一手來源核實,一次灌一堆等於灌水。** 故改為限量慢慢消,約兩週消化完。

挑選優先序:①**能增補既有筆記的優先**(不製造重複主題,價值最高)→ ②有字幕的(成本低)→ ③新到舊。

### 存量清單(2026-09-01 首次巡檢盤點,已完成 1 支)

- ✅ 已完成:Why QQ `j2I2TIvhs0c`(Jalapeño 首測拆解)→ `knowledge/technology/llm-internals/inference/jalapeno-inference-benchmark-boundaries.md`
- ✅ 已完成:Why QQ `bNMBbrplILM`(Fable 5.1)、Why QQ `jgy1A0Mrx7g`(Omarchy 4)、Caleb `yHNp_rT6uEo`(Jalapeño,增補跑分邊界筆記 §10)
- **Why QQ 剩 1**:`nScMXSWz9aE` vgpu(09-05~09-17 已完成 `BkoCVZJcRHY` Dario 降速長文、 `9uq4FRJ0oEE` 陶哲軒聯名聲明、`6Ly6wZUsESA` Anthropic 威脅情報報告、 `Ea1XvVD7GTY` DeepSeek V4.1-Flash、`98Mz0a1wJag` Voice Spec Loop、 GPT-6 Astra、DHH 16 條並行、RSA-260、AI 原生 SDLC、可塑軟體、Skill Doctor、HN 熱帖、`-XBnFO6FweQ` 刪提示詞、`0AvqP_WRVVM` 刪完之後寫什麼、`zFSWbN7VKB8` Coxon 辭職信、`479-FVtko2c` 29 個邏輯閘玩馬里奧、`pEMIF2Cu1mA` Jev/System One 決策模型、09-19 完成 `h9fLB0aS2AM` RSI 75 頁論文、`yOExQX0j19g` 小米 MiMo RL 儀表盤、09-20 完成 `bhfBWHPYC-I` Cloudflare 安全審計 Skill、09-21 完成 `Y31OgSV-S8k` Jev 實操指南、09-22 完成 `SHRkOI0yO4Q` Supermemory、09-23 完成 `t96q8onLu90` Dream-RSI、09-24 完成 `F22wTQzVkI8` 呼籲放緩後三家齊發新模型、09-25 完成 `I3bnBM4vNnY` LLMentalist 效應、09-26 完成 `ou9SC0Z_CtI` 給 Coding Agent 加決策層、09-27 完成 `bLWJmz_uAco` Anthropic ART 酶系統科研 harness、09-28 完成 `hmrXnBvaFaI` 荷蘭政府 DAWO / NixOS、09-29 完成 `zxxAl7Wc2g0` DHH Rails World 2026 → 併入 DHH 筆記 §13、09-30 完成 `s87lkkWk9rQ` Sonnet 5.5)
- **Caleb 剩 7**(⚠️ 09-25 新增 `gQmPD4I62rU`〈Opus 5.5 vs GPT-6 is racing to the bottom〉:**自動字幕連續 3 次 HTTP 429 順延**;⚠️ 含 Hyperagent 業配(`hyperagent.com/caleb` 導購);主題與 RSI 筆記 §11 相同,只有新資訊才增補)(09-20 完成 `vj7hysh0mOI` Jev 七分鐘版 → 增補 Jev 筆記 §13)(09-14 完成 `7DncQnIjZmA` Navier-Stokes、09-17 完成 `PTubnGrHdmM` V4.1-Flash 架構深潛):`noPuRPDiY6k` AGI, are we there yet(09-09 新片,⚠️ 含 Micro Center 業配;09-10 三度嘗試抓自動字幕全數 **HTTP 429**,順延)、`3WbXyUolFA0`、`ZxBRtRjMU88` HBF、`Cx-pVoBR7C0`、`8ji5vURIllM` Why harness is SO expensive、`O1JMZvgFxKE`(09-04 完成 `dGHLg9NfvEo` Fable 5.1 質疑;09-05 完成 `XvmixEXPT3Q` GPT-6 Astra,與 Why QQ 版合併為同一篇)
- **白白说大模型 剩 9**(全需 Whisper):`Uz7K757psEU` 高階 RAG 架構(09-07 新片)、`Wf2PZN-Ep2M` AI 應用開發學習路線(09-04 新片)、`4CZiE0Y0FFQ`、`Pio4SrsPHCY`、`acvK103404s` Agent Skills、`x-s1Dbp4BE4` Agent 架構十連問、`whdEwyY9A78` 單體 Loop→分散式 Graph(⭐可增補 graph-engineering-node-edge-state)、`wiQgPk8BnhM`、`XQXMSc0L5DA` 向量庫+RAG
- ⭐ **2026-09-30 巡檢新發現(順延)**:YAHA學堂 `o1EQ5wezMyA`(AI 改崩程式碼用 Git 留退路,約 13.7 分鐘,**僅自動字幕,連續 3 次 HTTP 429 順延**;⚠️ 與 Gary Chen 既有 git-github-for-vibe-coders.md 主題高度重疊,只在有新內容時增補);白白说大模型 `0gtzVKkg3L0`(後端轉 AI 應用開發學習路線,約 17 分鐘,需 Whisper;⚠️ 說明欄以「公眾號回覆關鍵詞領資料」導流,屬通用路線圖,優先度低)。
- ⭐ **2026-09-28 巡檢新發現(順延)**:YAHA學堂 `sX6n9lL_9F8`(Jev 決策模型教程,約 29.7 分鐘,**僅自動字幕,連續 3 次 HTTP 429 順延**)。⚠️ Jev 筆記已有 6 個來源(76 KB),**只在它有新東西時才增補**:說明欄提到官方列出的失敗模式(數數、日期、多跳推理、提示注入、非英語)、64K 上下文與上下文腐爛、技能選擇 16.8%→7.3%(Jev 筆記 §15 目前標為未核實,若此片指出官方出處可一併解決)。
- **YAHA學堂 剩 7**(09-12 完成 `zK2TjT17b8U` Claude Cowork、09-14 完成 `Q4hTr67ECLg` 付費 API 成本護欄、09-16 完成 `Y2yElMkwH_A` Hooks 實戰):`A2i8D66J83U`(09-12 新片,shadcn registry 把 Claude Code 介面搬進網頁,無字幕需 Whisper)、`rq4EHbqaaAk` diagram-design skill(09-03 新片,無字幕)、`9leHSMk-9nY`、`H4zIuJ4G1QY`、`ahb8kfsZmIk`、`yrnGrdPZx_U`(以上無字幕)、`Wq1icAZYr4E` Claude 隱藏設定(官方字幕)。09-07 完成 `X2A6fANij9Q` workload creep。⭐ **09-19 完成 `mAoXktiOhWY` Astra vs Fable 找/修 bug 實測(Whisper)**;⚠️ **仍順延 `huGHec7mpm8`(Cowork vs Chat)、`CV7HX6qFglc`(Topview,說明欄含 `?via=yahaclass` 聯盟連結,收之前要先判定是否業配)**。 ⭐ **09-22 完成 `8unONuKIaPs` localhost/部署 → 併入既有部署筆記 §9**;⭐ **09-23 完成 `iHVpk9IM1Uk` Windows 原生安裝 Claude Code → 新篇 claude-code-windows-native-install-troubleshooting.md**;⭐ **09-26 完成 `9Be7ALZBv0Q` Graft → 併入 codebase-memory-vs-codegraph-two-routes.md §七**(⚠️ 該片內容與 Gary Chen `6bvEcpm72W0` 高度重疊,僅記錄事實不做判斷)。
  ⚠️ **`9O4IueW_n1k`(09-08「60 秒開好 AI agent」)判定為不整理** —— 該片說明欄第一行即 Hostinger 聯盟連結與優惠碼,通篇是特定託管商的 UI 操作導覽,可轉移的知識薄;唯一有價值的「一次任務燒多少額度」也綁定該平台的積分制。**若日後想收,建議只擷取成本量測那一段併入既有 agent 筆記,不要單獨開篇。**
- **小Lin说 剩 5**(⭐ 09-23 完成 `R1-j8TFlqCo` 俄烏戰爭誰在買單 → 新篇 russia-ukraine-war-economy-who-pays.md)(2026-09-02 加入,全有官方字幕;09-10 完成 `T7z71yENz94` 川普關稅、`8BN8p5xDkzw` 日圓 40 年新低、`l38ceFOWOAE` 萬達):`fKoWrF49Qo8` 川普收入、`OcKl98ZQbMQ` AI 巨頭資本混戰(⭐可增補 nvda-fy27q2-guidance-and-circular-financing)、`wpb-DrbhEiY` SpaceX 上市(⭐可增補 spacex-ipo-musk-jpmorgan / spacex-rise-history)、`7oF-JqEtWDU`、`mcTAHffEkIw`、`7qWH7e_AEDs`
- **白白说大模型 剩 12**(09-21 完成 `-hKHbHA0KKI` Milvus 架構解析 → 新篇 milvus-architecture-vector-database.md)(09-16 完成 `MWNuu9m93dk` 多 Agent 資料一致性):`Zez7CMkSZsI`(09-11 新片,職場人專屬選型指南,需 Whisper)、`wt2kiCU6sA0`(09-10 新片,面向普通人的 AI 時代入局指南,需 Whisper)、`dThNVDU64ew`(09-09 新片,需 Whisper)
- ⚠️ **2026-09-23 判定不整理**:白白说 `ITniwzQy9uc`(Jev 3 分鐘入門,需 Whisper)—— **Jev 已累積 5 個來源、筆記 64 KB,3 分鐘入門片不可能有新內容,依「先判斷撞題」規則直接跳過,不花 Whisper**。
- ⭐ **2026-09-22 巡檢新發現(尚未處理)**:白白说 `Ru_YVdveirY`(30+ 程式設計師轉行的四個 AI 方向,約 13.6 分鐘,需 Whisper)。
- ⭐ **2026-09-19 巡檢新發現(尚未處理)**:白白说 `JNVK-fd2pH4`(09-18 新片,從 Token 到 Agent 底層技術全拆解,約 19 分鐘,需 Whisper)、小Lin说 `fKoWrF49Qo8`(⚠️ **2026-07-23 舊片**,川普收入曝光,有官方繁中字幕)、Redknot `N3o8AcflmO4`(⚠️ **2026-05-12 舊片**,磁軸鍵盤原理,無字幕需 Whisper)。
- ⚠️⚠️ **Gary Chen `JctGH-SOYBA` 同為會員限定(2026-09-29 發現),永久跳過。**
- ⚠️⚠️ **Gary Chen `roUfF8nUYNo` 同為會員限定(2026-09-27 發現,level: Gary AI 實戰營),永久跳過**;該頻道新片常搭配一支會員專屬片,遇到 members-only 一律跳過。
- ⚠️⚠️ **Gary Chen `BbofEyeE2Ek` 判定為不可處理** —— 該片為**頻道會員限定**(level: Gary AI 實戰營),`extract_info` 直接報 members-only,**無法取得 metadata 或字幕,永久跳過**。
- **Redknot 剩 4**:⚠️ `EsJKkDbHsec`(09-16 新片,ASML 控光藝術/衍射極限,**片中明確標示「本期視頻與 ASML 合作出品」= 業配**,無字幕需 Whisper;技術內容看來紮實,若要收務必於檔頭標明業配立場)
- **Redknot 原有 3**:`eOcyZqtw0Fg` 玄戒 O100 堆疊、`BUHHheaKlDY` 光刻機光源(無字幕)、`rQR_0WZzjV4` SSD 原理(⚠️ 09-10 實測**無官方字幕**,只有自動英文 ASR,先前記錄有誤;要收得走 Whisper)

⚠️ 實測遇過**來源影片後來被設為私人**(白白说大模型的 `diU-Nbb1P_c`,是既有筆記的來源),
取不到就跳過記錄、不要重試到底。

---

## 6. `new/` 收件匣巡檢(每日 08:37 / `37 8 * * *`,2026-09-29 新增)

> 緣由:使用者要求「建立 `new/` 資料夾,有新東西(例如太大的檔案)就放這裡,定時來搜尋;整理完把資料夾加上 `done-` 前綴,下次就不會再處理」。
> - `new/` 已加入 `.gitignore`,**素材本身永不進版控**,只有整理出的筆記進 repo。
> - 首個素材 `karpathy_8years_conclusion/`(1.1 GB、129 分鐘 mp4)於建立當日手動處理。
> - 本 session job id:`6e7a39b5`。

```text
每日巡檢 Knowledge repo 的 `new/` 收件匣資料夾,把使用者丟進來的素材整理成筆記。⚠️ Knowledge repo 已於 2026-08-30 重整:筆記在 knowledge/、腳本在 scripts/。
背景:使用者會把「太大、不方便直接貼」的素材(影片、音檔、PDF、簡報、圖片、文字檔等)各放一個子資料夾到 C:\Users\shoot\project\Knowledge\new\ 底下。**處理完的子資料夾要改名加上 `done-` 前綴,下次就不再處理。**
步驟:
1. 列出 new/ 底下**名稱不以 `done-` 開頭**的子資料夾:`ls -1 new/ | grep -v '^done-'`。沒有就只回報「收件匣無新素材」,不 commit。
2. 逐一檢查每個子資料夾的檔案(類型、大小、長度):影片/音檔用 PyAV 看長度與音軌;PDF 用 Read(pages 參數,每次最多 20 頁);圖片直接 Read;文字/Markdown 直接讀。⚠️ 檔名常含原作者與標題線索(例如 `Callan_-_Andrej_Karpathy_...`),據此用 WebSearch 找出原始出處網址,放進筆記「來源」。
3. 影片/音檔轉錄:faster-whisper(WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=6),transcribe(path, language=None 自動偵測, vad_filter=True, condition_on_previous_text=False, no_repeat_ngram_size=3, beam_size=5)),**可直接吃 mp4/m4a/webm,不需 ffmpeg**。segment 逐行寫暫存 .txt(帶 [分:秒] 時間戳、每行 flush)再 Read(大檔分段讀)。
   ⚠️⚠️ **Whisper 一律用「前景」跑,不要用 `nohup ... &` 背景跑**(背景 shell 環境不完整,torch/numpy import 會失敗)。長片前景超過 600s 會自動轉背景,等完成通知即可;期間可 Read 暫存 .txt 看進度。stderr 的 `_ARRAY_API not found` UserWarning 只是警告。轉完掃結尾有無同句重複數十行(幻覺迴圈)。實測參考:129 分鐘英文影片約 40 分鐘轉完。
4. 依 CLAUDE.md 寫作規範整理繁中筆記(含應用案例、Mermaid、結尾**完整網址**來源),歸三層結構最貼切中類;同主題已有筆記就優先增補(先 `grep -rl "<關鍵字>" knowledge/` 確認)。⭐ 可查證的規格/數字/論文/repo 一律比對一手來源核實並標出補正;講到開源 repo 就 `git clone --depth 1` 到暫存讀原始碼(讀完刪除)。來源區塊標註「使用者提供的本機檔案 `new/<資料夾>/<檔名>`」,若為轉錄則註明「逐字稿以 CPU faster-whisper 轉錄、非官方字幕」。投資類加⚠️非投資建議;作者推廣自家產品/業配要在檔頭標明立場。產出 Mermaid 後跑 python scripts/knowledge/lint_mermaid.py <檔案>(節點一律方括號 `["文字"]`)。寫 `[[wikilink]]` 前先 `find knowledge -name "<slug>.md"` 確認存在。
5. ⚠️⚠️ **`new/` 已列入 .gitignore,素材本身絕對不進版控**;不要把大檔複製到 knowledge/ 或任何被追蹤的路徑。
6. 更新 README 主題表格、筆記數 badge、對應作者索引(兩處都要),跑 python scripts/knowledge/build_source_index.py。無 BOM UTF-8 暫存檔(.git/COMMIT_MSG_TMP,printf '%s')commit([feat] 前綴,訊息寫明來源為 new/ 收件匣)、git push -q origin main。⚠️ 精準 git add <檔案>,不要 git add -A;遇 git-lfs locksverify 錯誤改用 git -c lfs.https://github.com/shooter2062424/Knowledge.git/info/lfs.locksverify=false push 重試;用 git rev-parse HEAD 與 origin/main 比對判斷 push 成敗。
7. **筆記 commit 並 push 成功後**,才把該子資料夾改名:`mv "new/<名稱>" "new/done-<名稱>"`。處理失敗(轉錄失敗、檔案損毀、看不懂格式)就**不要改名**,在回報中說明原因,留待下次或請使用者協助。
8. 清暫存(逐字稿 .txt、clone)。在 SCHEDULES.md「變更歷程」表最上方插入當日一列(記錄處理了哪個資料夾、產出哪篇筆記),與筆記同一個 commit。
⚠️ commit 訊息結尾要加:
Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CjznW7K3y5MRDg2y2UcAKV
沒有新素材就只回報、不空 commit。回報處理了哪些資料夾、產出哪些筆記、改名結果。(session-only 每日排程,7 天後自動到期,到期前若仍需要請用 CronCreate 續排;完整 prompt 備份在 Knowledge repo 的 SCHEDULES.md 第 6 節。)
```

---

## 變更歷程

| 日期 | 事件 |
|---|---|
| 2026-09-30 | 巡檢產出 1 篇(官方字幕,零 Whisper):**Why QQ** `s87lkkWk9rQ` → 新篇 ai-industry/claude-sonnet-5-5-release-effort-migration.md。✅ **已讀 Anthropic 官方公告、遷移指南與 Simon Willison 原文核實**:價格、速度、Terminal-Bench/OSWorld/Chartography/GDPval/FrontierCode/CursorBench、五個 400 破壞性變更、2026-08-31 帳號規則、圖片 token 2.5 倍、快取門檻 512 全部屬實。📌 **兩處補正**:①鵜鶘 max 檔失敗是**輸出 token 用完**(`max_tokens` 含思考),不是「超時」;②`between_tools` 模式下 per-message effort 與現行檔位不同會回 400,**逐輪換檔要用 adaptive thinking**。❓ SWE-Bench Pro、AutomationBench、HealthBench 數字未在官方頁找到。⚠️ **順延 2 支**:YAHA學堂 `o1EQ5wezMyA`(自動字幕 429)、白白说 `0gtzVKkg3L0`(通用路線圖、導流)。同日 Gary Chen 新增 Opus 5.5 做宣傳片筆記。其餘頻道無新片 |
| 2026-09-29 | 巡檢產出 1 篇增補(官方字幕,零 Whisper):**Why QQ** `zxxAl7Wc2g0` DHH Rails World 2026 開幕演講 → 併入 dhh-16-threads-bottleneck-migration.md §13。⭐⭐ **抓 DHH 官方演講英文字幕逐句核實**:退休宣告、現場約 5 人舉手、每年 3 萬行 vs 8 月 15 萬行、HEY Rust 後端 CPU −99%/記憶體 −95%/樹莓派、CLI 下週五、Omarchy 3:33→35 秒→實驗室 9 秒皆屬實;⚠️⚠️ **DHH 自己引用的 ATM 數字是錯的**——他說 1950 年代 3 萬櫃員→2010 年 4 萬,Bessen 研究是 1980 年代起約 50 萬→近 60 萬,且 ATM 大規模部署在 1970 年代後。⭐ 同意 Why QQ 的補充:HEY 省下的資源**主要來自架構改變(算繪移到客戶端)而非換成 Rust**。同日 Gary Chen 新增會員限定 `JctGH-SOYBA`(跳過)。其餘五頻道無新片 |
| 2026-09-29 | ⭐ **新增第 6 個排程 `new/` 收件匣(`6e7a39b5`,每日 08:37)**,並手動處理首個素材 `new/karpathy_8years_conclusion/`(1.1 GB、129 分鐘 mp4,faster-whisper 英文轉錄約 40 分鐘)→ 新篇 ai-productivity/karpathy-how-i-use-llms.md;資料夾已改名 `done-karpathy_8years_conclusion`。⚠️ 素材來自 X 爆紅貼文,**「上週發布、Agents→Loops→Graphs」說法有誤**,實為 2025-02-27〈How I use LLMs〉。同日另依使用者連結新增邦妮區塊鏈 John D'Agostino 筆記 |
| 2026-09-28 | 巡檢產出 1 篇(官方字幕,零 Whisper):**Why QQ** `hmrXnBvaFaI` → 新篇 system-design/dawo-nixos-laptop-as-code-dutch-government.md。⭐⭐⭐ **clone 荷蘭政府自架 Forgejo 上的 DAWO / DAWO-NixOS / DAWO-Sextant 三個 repo**,抓到影片把**強制安全基線講多了**:`architecture.md` 自己更正——**usbguard 刻意改為選配**(開箱拒絕 USB 會被使用者視為壞掉)、**auditd 因 nixpkgs 26.05 上游 bug 延後**,強制層實際只有 ssh/sysctl/chrony/PAM;DAWO-NixOS **已到 0.1.3**(影片說 0.1.2 為 8 月時點);另補 Sextant 支援遠端「意圖」(鎖定、診斷、加密抹除)而非遠端控制。✅ nixpkgs 核心團隊 2026-08-07 解散已核實。⚠️ 試點市政府數「四個」vs 部分媒體「八個」未能以官方確認。⚠️ **YAHA學堂 `sX6n9lL_9F8`(Jev 教程)自動字幕連續 3 次 429 順延**。同日美投君新增記憶體週期筆記。其餘四頻道無新片 |
| 2026-09-28 | **使用者要求「續排」,五個排程全刪重建**(`ce8e9c59` / `a4206b99` / `59bd5619` / `c8f16d37` / `f8529c0d`,約 **10-05** 到期)。補檢確認:09-27 五個排程全數有跑(GitHub Weekly 125 仍 404、Gary Chen 新增 Impeccable、gooaye 仍 EP693、美投君無新片、巡檢新增 ART),**無漏跑**;09-28 各排程觸發時間未到。⚠️ **SCHEDULES.md 各節 prompt 備份已落後實際版本,本輪以實際運作 prompt 全文覆蓋同步** |
| 2026-09-27 | 巡檢產出 1 篇(官方字幕,零 Whisper):**Why QQ** `bLWJmz_uAco` → 新篇 anthropic-art-enzyme-discovery-research-harness.md。⭐⭐⭐ **已讀 [Anthropic 公告](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system) 與 40 頁技術報告預印本全文**,影片的規模、漏斗、10 次重跑、3,500 次對照數字**全部核實一致**;⭐ **補上影片沒講的三件事**:①跑這場的是 **Claude Mythos 5**;②**2.156 億 token 裡 1.895 億是寫入快取、輸出只有 1,490 萬**;③摘要明寫模型內部有**對重複 DNA 反應的可解釋訊號**(與 Evo 2、gLM2 對照)。⚠️ 影片的「339 萬候選序列」報告中未找到;VirBench 加檢索層後官方是「超過 92%」而非 90%。同日 Gary Chen 排程另新增 Impeccable 筆記、`roUfF8nUYNo` 會員限定跳過。其餘五頻道無新片(存量不變) |
| 2026-09-26 | 巡檢產出 2 篇增補(Whisper 1 支):**Why QQ** `ou9SC0Z_CtI` → Jev 筆記 §16(64→76 KB);**YAHA學堂** `9Be7ALZBv0Q` → 程式碼圖譜筆記 §七。⭐⭐⭐ **兩篇都靠 clone repo 挖到比影片更重要的內容**:① [hermes-jev-skills](https://github.com/kerpopule/hermes-jev-skills) 的 CHANGELOG 記錄了**影子模式中 89% 回合被送往最貴檔**的失敗(**不確定的 score 平均值會落在門檻上**,改讀各級機率後降到 4.5%),以及交接實驗完整數據(**「留原文 + 能搜一次」勝過任何摘要**);② [Graft](https://github.com/trailhq/Graft) README 頂端表格**混了兩組不同測試**、**按需查詢(pull)準確率最高達 98%**、SWE-bench 33 對 27 是**廠商自跑**而非說明欄說的第三方口徑。⚠️ Why QQ 影片把 hermes 的 0.00006 美元誤掛在 LangChain 名下。其餘四頻道無新片 |
| 2026-09-25 | 巡檢產出 1 篇(官方字幕,零 Whisper):**Why QQ** `I3bnBM4vNnY` → 新篇 llmentalist-effect-cold-reading-and-verifiers.md。⭐ **已讀 [Bjarnason 原文](https://softwarecrisis.dev/letters/llmentalist/) 核實**六步驟、RLHF 論點、占星師故事;⚠️ **補正:影片說「心理學研究發現自認聰明的人更易上當」,原文沒有引用任何研究,屬作者論點**。⚠️ **Caleb `gQmPD4I62rU` 自動字幕連續 3 次 HTTP 429,依規則順延**(含 Hyperagent 業配,主題同 RSI §11)。其餘四頻道無新片 |
| 2026-09-24 | 巡檢產出 1 篇增補(官方字幕,零 Whisper):**Why QQ** `F22wTQzVkI8` → 併入 rsi-recursive-self-improvement-anthropic.md §11(84→96 KB),接續 §7 的「Pace the Frontier」宣言:十天後 xAI / Anthropic / OpenAI 在 48 小時內全部發了新模型。✅ **已核實**:Opus 5.5 $4/$20、快取讀取 $0.20、思考無法關閉、Terminal-Bench 4.0 66.4% vs Astra 57.9%、沙箱邊界嘗試少 85%;GPT-6 Sol $2/$10、Luna $0.10/$0.50、AutomationBench 33.2% vs Opus 5 26.9%。⚠️ **補上影片沒提的:Sol 在 OSWorld 2.0 反而退步**(60.5% vs 前代 65.7%)。⚠️ **一則報導標題寫 Opus 5.5「取消」五小時上限,與其他來源不符** —— 較完整的報導是「上調 20% + 一次性重置」,與影片一致。⚠️ 影片再次沿用「智能體**群**攻擊 HF」說法,已引用 §8.6 補正。其餘五頻道無新片(存量不變) |
| 2026-09-23(當日第二輪) | 巡檢產出 1 篇(Whisper 1 支):**YAHA學堂** `iHVpk9IM1Uk` → 新篇 claude-code-windows-native-install-troubleshooting.md(動筆前先 grep 確認本庫**沒有**安裝教學筆記,才花 Whisper)。⭐⭐ **五個報錯的訊息原文與修法全部對 [官方 setup](https://code.claude.com/docs/en/setup) 與 [troubleshoot-install](https://code.claude.com/docs/en/troubleshoot-install) 核實屬實**;另補上影片沒講的五件事:不需系統管理員、支援 ARM64、**WinGet 可用 `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1` 開自動更新**、`CLAUDE_CODE_GIT_BASH_PATH` 不能指向 `git-bash.exe`、公司 EDR 白名單。⭐ 影片標題「別碰 WSL」讀成「一般情況不需要」:**原生 Windows 不支援沙箱,只有 WSL 2 支援**。其餘頻道無新片(存量不變) |
| 2026-09-23 | ⭐ **使用者要求展延排程,五個全刪重建**(新 id 見檔頭;**同時把 commit 署名由 `Claude Opus 5` 更正為 `Claude Opus 5.5 (1M context)`**)。巡檢產出 2 篇,**皆官方字幕、零 Whisper**:**Why QQ** `t96q8onLu90` → 增補 rsi-recursive-self-improvement-anthropic.md §10(68→84 KB);**小Lin说** `R1-j8TFlqCo` → 新篇 russia-ukraine-war-economy-who-pays.md。⚠️⚠️ **Dream-RSI 兩處補正**:①頭條「317 對 51,200、差 162 倍」**混了換模型(GPT-OSS-120B → Gemini-3.1-Pro)與換策略兩個效果**,論文內同模型公平比較是 **317 vs 550,約 1.7 倍**;②影片說論文「直接給出代碼」,但 **clone 官方 repo 確認程式碼、發現的程式、重現腳本都還是「準備中」,且無授權檔**。⭐ 小Lin说那篇核實了 Rosstat 修訂 GDP 與 IMF 81 億美元方案,**並補上 IMF 官方寫明它屬於 1,365 億美元國際總包** —— 正好佐證影片「IMF 是其他援助的鑰匙」論點。⚠️ **小Lin说該片含 Saily eSIM 業配,已標註**。⚠️ **白白说 `ITniwzQy9uc`(Jev 3 分鐘入門)依新規則先判斷撞題後直接跳過**。GitHub Weekly(125 仍 404,已 51 天)/ gooaye(`built_at` 仍停在 09-04,已 19 天)/ Gary Chen / 美投君 當輪均無新內容 |
| 2026-09-22 | 巡檢產出 2 篇(Whisper 1 支):**Why QQ** `SHRkOI0yO4Q` → 新篇 supermemory-memory-layer.md(⭐⭐ **已 clone [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory) 讀 README 與 monorepo**,跑分/port/MCP 工具/本地部署全部核實;⚠️ **兩處補正**:monorepo 裡沒有 LangChain/LangGraph/Mastra 套件目錄、**Mem0 有 65,790 star 是它兩倍多而影片沒給對手數字**;⭐ 另補上影片沒給的分項召回率,**最弱的 Temporal 91% / Preference 90% 正是它主打要解決的**);**YAHA學堂** `8unONuKIaPs` → ⚠️ **不新開,併入既有 deployment-for-vibe-coders-platform-selection.md §9** —— **該片內容與 Gary Chen `6bvEcpm72W0` 高度重疊**(同樣的餐廳比喻、三個決定、平台推薦、後台四個地方、結尾資安提醒),**本文只記錄此事實、不對成因做任何判斷**,並摘出該片三句更凝練的說法。⭐ **順延** 白白说 `Ru_YVdveirY`(轉行四個 AI 方向)。Caleb / 小Lin说 / Redknot-乔红 當輪無新片 |
| 2026-09-21 | 巡檢產出 2 篇(Whisper 1 支):**Why QQ** `Y31OgSV-S8k` → 增補 Jev 筆記 §14(實操指南,36→52 KB);**白白说大模型** `-hKHbHA0KKI` → 新篇 milvus-architecture-vector-database.md(無字幕,faster-whisper)。⭐⭐⭐ **兩篇都靠讀官方文件抓到重要補正**:①**Milvus 那篇發現影片講的是 2.5 及更早的架構** —— **IndexNode 已在 2.6 移除**、**Woodpecker 零磁碟 WAL 取代 Pulsar/Kafka**、**新增 StreamingNode 而 QueryNode 只剩歷史段批次查詢**;②**Jev 那篇更正了本庫自己先前寫錯的一處** —— 第三種型態名稱**確實是 `noul` 不是 `bool`**(已對官方 API 請求範例核實,原影片沒講錯,是本庫 §12.7 的「勘誤」搞錯了,已於 §14.1 更正並同步修正 §二與 README);另把 §12.4「OpenRouter 已上架」從未核實更正為屬實。⚠️ **白白说該片下載首次 403,同參數重試第 2 次成功**(符合既有 SABR 重試規則)。⚠️ **Why QQ 該片作者在片中介紹自己的專案 BLUFF,已於檔頭標註**。Caleb / YAHA學堂 / 小Lin说 / Redknot-乔红 當輪無新片 |
| 2026-09-20 | 巡檢產出 2 篇,**皆官方/自動字幕、零 Whisper**:**Why QQ** `bhfBWHPYC-I` → 新篇 cloudflare-security-audit-skill-pipeline.md(⭐⭐ **已 clone [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) 讀完 15 份 Markdown 與 schema,並讀 [官方部落格](https://blog.cloudflare.com/build-your-own-vulnerability-harness/) 核實全部漏斗數字**);**Caleb Writes Code** `vj7hysh0mOI` → 增補 Jev 筆記 §13。⚠️⚠️ **三處補正**:①影片開場的「700 個 agent 協同攻破 Hugging Face」與 HF 官方技術時間軸不符(本庫 RSI 筆記 §8.6 已查證);②開源版是 **6 階段**、官方部落格描述的內部原版是 **7 階段**;③「上下文窗口超過 1/4 就開始幻覺」**倉庫全文查無此句**。⭐ 另補上影片沒提的「高完整度發現 35%→58%」與校驗器硬上限。⚠️ **Caleb 該片中段含 JetBrains Juni CLI 業配,已於檔頭標註**。其餘四頻道(YAHA學堂 / 白白说大模型 / 小Lin说 / Redknot-乔红)當輪無新片 |
| 2026-09-19 | 巡檢產出 3 篇(達上限),Whisper 1 支:**Why QQ** `h9fLB0aS2AM` → 增補 rsi-recursive-self-improvement-anthropic.md §9(56→68 KB);**Why QQ** `yOExQX0j19g` → 新篇 xiaomi-mimo-v26-rl-live-dashboard-scaling.md;**YAHA學堂** `mAoXktiOhWY` → 新篇 astra-vs-fable-find-bugs-vs-fix-bugs.md(無字幕,faster-whisper)。⭐⭐ **兩處一手素材補正**:①讀 [arXiv 2609.11873](https://arxiv.org/abs/2609.11873) 原文發現**影片把 HCI 講反了** —— 論文是 **Headroom-Closed Index(已關閉空間指數)**,數值越高代表剩餘空間**越少**,影片說成「剩餘提升空間指數」;②小米那篇比對第三方報導補了三件影片沒講的事 —— **DeepSWE 65.97 其實低於 GPT-6 Astra/Fable 5/Kimi K3/Grok 4.6 全部四家**(但較 V2.5 的 19% 躍升 47 點)、**儀表盤上 `Claude Distill Requests` 是 `hidden`**(所以「開放過程」並沒有回答蒸餾質疑)、這是 1T 級模型。⚠️ **`mimo.xiaomi.com/rl` 是 WebSocket 即時頁,HTTP 抓取只會得到 `reconnecting…` 外殼,無法取數**。⚠️⚠️ **Gary Chen `BbofEyeE2Ek` 為會員限定影片,永久跳過**。GitHub Weekly(125 仍 404)/ gooaye(`built_at` 仍停在 2026-09-04,已 15 天)/ 美投君 當輪均無新內容 |
| 2026-09-18 | 巡檢產出 2 篇,**皆為官方字幕、零 Whisper**:**Why QQ** `pEMIF2Cu1mA` Jev/System One 決策模型 → 新篇 system-one-models-jev-calibrated-decisions.md;**Why QQ** `oCNhFF5wBE0` 群體智能長文 → 增補 rsi-recursive-self-improvement-anthropic.md §8(39.8→55.7 KB)。⭐⭐ **兩篇都靠讀一手素材抓到補正**:①[TypeSafe 官方部落格](https://typesafe.ai/blog/introducing-system-one-models-and-jev)確認「零幻覺」**不是實測而是 schema 匹配的數學保證**,且官方自承評測工作流由自家團隊設計、參考答案取 GPT-6 Astra 與 Fable 5.1 平均;②**Hugging Face 官方技術時間軸推翻了廣傳的「700 個 agent 協同攻擊」說法**——原文是「a single autonomous AI agent orchestrated the entire campaign... as an integrated system rather than a coordinated swarm」。⚠️ **順延 3 支**:YAHA `huGHec7mpm8`(Cowork vs Chat)、YAHA `CV7HX6qFglc`(Topview,⚠️ 說明欄含 `?via=yahaclass` 聯盟連結,收之前要先判定是否業配)、白白说 `aGpyWKtgjoU`(企業 RAG 權限,需 Whisper)。GitHub Weekly(404)/ gooaye(`built_at` 仍停在 2026-09-04,已 14 天)/ Gary Chen / 美投君 當輪均無新內容 |
| 2026-09-17 | Gary Chen 排程新增 1 篇(`6bvEcpm72W0` 給非技術人員的部署教學 → 新篇 deployment-for-vibe-coders-platform-selection.md,補正 Render 定價與 Cloudflare 動態請求上限兩處)。巡檢產出 2 篇增補,**皆為既有筆記的直接後續**:**Why QQ** `BkoCVZJcRHY` Dario《We Must Pace the Frontier》→ rsi-recursive-self-improvement-anthropic.md §7(24.9→39.8 KB,**原文已逐句核實**,含「狂熱效忠的集體」「試圖攻破自己的評分器」「6–12 個月可能接管網際網路」等逐字引述);**Caleb** `PTubnGrHdmM` V4.1-Flash 架構深潛 → deepseek-v4-engineering.md V15(30.3→41.4 KB,補上 V1–V14 沒有的 **Engram 完整機制、CED 相對 YOCO 的取捨、single-pass mHC 的 GPU 記憶體階層問題**)。⚠️ Redknot 新片 `EsJKkDbHsec` 為 **ASML 合作出品的業配**,已記入存量並標明 |
| 2026-09-16(當日第二輪) | 巡檢產出 1 篇增補:**YAHA學堂** `Y2yElMkwH_A` Claude Code Hooks 實戰 → 增補 claude-code-hooks-complete-guide.md §10(21.5→36.3 KB)。⭐⭐ **本輪實際 clone 了 obra/superpowers 原始碼量測 + 讀官方 hooks 文件**,成果:①**抓到影片一處近一倍的數字誤差**(注入量實測 718 token vs 影片說的 1,300)②**修正 matcher 描述**(`startup\|clear\|compact`,不含 `resume`)③**補上影片沒提的官方 Stop Hook 保險**(連續阻止 8 次自動覆蓋、腳本應解析 `stop_hook_active`、可用 `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` 調整)。⭐ 再次印證「直接讀一手素材」這條 prompt 規則的價值 |
| 2026-09-16 | **五個排程到期前全刪重建**(`2b9ad1dd` GitHub Weekly / `a4b03c19` gooaye / `0cd78bf8` Gary Chen / `51de569e` 美投君 / `f99874c1` 巡檢,約 **09-22** 到期)。本輪把近日踩坑寫進 prompt:**① Whisper 一律前景跑**(nohup 背景跑 torch import 會失敗,09-13/14 連兩天踩到)**② Mermaid 節點不用圓形語法 `(("字"))`**(lint 報 UNQUOTED-SPECIAL)**③ 核心 CPI 與核心 PCE 不可混用 ④ 直接讀一手素材經常挖到影片沒講的重點**(舉威脅情報報告與 Clay 研究所為例)**⑤ `--write-auto-subs` 被限流較兇,連續 429 就順延**。巡檢產出 2 篇:**Why QQ** `9uq4FRJ0oEE` 陶哲軒與 25 位菲爾茲獎得主聯名《數學中 AI 的嚴重錯位》→ 增補 openai-navier-stokes-agent-swarm-and-attribution.md §8(**聲明全文已直接讀原文逐句核實**);**白白说大模型** `MWNuu9m93dk` 多 Agent 資料一致性 → 新篇 multi-agent-data-consistency-reliability.md(⚠️ 該片無任何可查證來源,已標明屬工程主張並補上影片沒談的適用邊界) |
| 2026-09-15 | 巡檢產出 1 篇:**Why QQ** `6Ly6wZUsESA` Anthropic 第四份威脅情報報告 → 新篇 anthropic-threat-intelligence-2026-09.md。⭐ **直接讀了 154 頁官方報告原文核實**,並補上影片完全未提、對台灣讀者最相關的三個案例(GTG-17002 預載台灣 12 個軍事目標的電子戰系統、GTG-14020 針對台灣基督長老教會含「施壓點」的情蒐、GTG-27005 全自主 FPV 自殺無人機蜂群)。⚠️ 全篇已標明對特定公司的指控均為 Anthropic 單方陳述,並並陳社群對「IPO 前點名競爭對手」的動機質疑。GitHub Weekly / gooaye / Gary Chen / 美投君 均無新內容。⭐ **順手查出 gooaye 停更原因:上游 whatmkreallysaid.com 的 `pack_manifest.json` `built_at` 停在 2026-09-04,是抓取站本身停止重建,不是股癌沒更新** |
| 2026-09-14 | 美投君排程新增 1 篇(`KG9M-8mvq7Q` 五大風險分級 → 新篇 us-stocks-five-risks-2026q4-hike-treasury-midterm.md)。巡檢產出 2 篇:**Caleb Writes Code** `7DncQnIjZmA` Navier-Stokes(OpenAI 一萬個 agent 與抄襲爭議,⚠️ 補正 Clay 研究所並未認定已解、陶哲軒「答案與理解脫鉤」)→ 新篇 openai-navier-stokes-agent-swarm-and-attribution.md;**YAHA學堂** `Q4hTr67ECLg` 付費 API 成本護欄(硬上限在扣費前攔截 ⇒ 失敗是免費的)→ 新篇 agent-paid-api-cost-guardrails-mcp.md。⚠️⚠️ **踩到的坑:Whisper 用 `nohup &` 背景跑時 torch/numpy import 連續失敗,改前景跑(超時自動轉背景)才成功** —— 已連續兩天出現,判定為背景 shell 環境變數不完整所致,今後一律前景跑 |
| 2026-09-13 | Gary Chen 排程新增 1 篇增補(`dwGn39M5oX8` Claude Code 近期更新 → 功能時間軸 §8,含 **Auto mode 變預設的 13.6% vs 89% 對照數據**,並補正「週上限永久 +25% 實為相對現況 −17%」)。巡檢再產出 2 篇增補,皆為 **Why QQ**:`Ea1XvVD7GTY` DeepSeek V4.1-Flash(890 位元組 KV 快取、CED 不對稱架構、成本主戰場從算力搬到儲存)→ 併入 deepseek-v4-engineering.md;`98Mz0a1wJag` Voice Spec Loop 六步(HIVE 研究 55 萬次評分、Anthropic 40 萬次會話)→ 併入 voice-input-ai-context-transformation.md。⚠️ 兩支 Why QQ 新片皆有官方字幕、零 Whisper。當輪另有 Caleb `7DncQnIjZmA` 與 YAHA `A2i8D66J83U` 兩支新片順延 |
| 2026-09-12 | 巡檢產出 2 篇:**Why QQ**〈29 个开关玩转马里奥〉→ 新篇 differentiable-logic-gate-networks-mario-29-gates.md(邏輯閘神經網路 vs Transformer 的物種之辨、2014 年 Koch/Tononi 進化演算法祖先、2022 年 DDLGN 可求導邏輯閘、複雜度預算);**YAHA學堂**〈Claude Cowork 加班費對帳〉→ 新篇 claude-cowork-overtime-pay-audit-prompt.md(五工具串聯、台灣加班費三個算法漏洞、可泛化的稽核模板)。GitHub Weekly / gooaye / Gary Chen / 美投君 均無新內容 |
| 2026-09-11 | 巡檢產出 1 篇增補:**Why QQ**〈Anthropic 研究员辞职〉→ 增補 rsi-recursive-self-improvement-anthropic.md §6(Jacob Coxon 辭職信、Hugging Face 與 Anthropic 自家模型的兩起真實入侵、Pachocki《An Alien Mind》、安全立場判斷框架)。當輪新出現 YAHA學堂 `zK2TjT17b8U`(Claude Cowork 示範)與白白说大模型 `wt2kiCU6sA0` 皆無字幕待走 Whisper,依上限本輪只做 1 支 Whisper,順延到下次。GitHub Weekly / gooaye / Gary Chen / 美投君 均無新內容 |
| 2026-09-10(當日第二輪) | 巡檢再產出 2 篇,皆為 **小Lin说**:日圓創 40 年新低(主導因素從利差換成財政風險、Takaichi Trade、美日 15 年來首次聯手、FIMA 回購便利)與萬達(兩份對賭、四次遞表失敗、太盟危機套利)。⚠️ **Caleb `noPuRPDiY6k` 又連續 3 次 HTTP 429**(累計 7 次),自動字幕似乎被特別限流,再順延。⚠️ **修正存量清單一處錯誤**:Redknot `rQR_0WZzjV4` 實測**沒有官方字幕**,只有自動英文 ASR,要收得走 Whisper。GitHub Weekly / gooaye / Gary Chen / 美投君 當輪均無新內容 |
| 2026-09-10 | **五個排程到期前全刪重建**(`345bebe3` GitHub Weekly / `1c8eb572` gooaye / `64e10797` Gary Chen / `fb24ebba` 美投君 / `4eef56e5` 巡檢,約 **09-17** 到期)。當日巡檢產出 3 篇:**小Lin说**川普關稅被判違法(新篇,已對最高法院判決、CBP CAPE、122/301 條款逐項核實)、**Why QQ**「刪完之後寫什麼」拆成兩處增補(CLAUDE.md 筆記 §11 提示詞八模組 + Astra 筆記 §12 成本配置,後者已對 OpenAI 官方模型頁核實 272K 倍率與各 Tier TPM)。⚠️ **Caleb `noPuRPDiY6k` 三次抓字幕全數 HTTP 429,順延到下次**。gooaye 仍為 EP693(一週無新集)、GitHub Weekly 仍停在第 124 期(38 天)、Gary Chen 與美投君皆無新片 |
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
| 2026-08-22 | 踩到 **yt-dlp 版本落後導致「持續性 403」** —— 三支影片 6 次嘗試全掛,log 顯示 `n challenge solving failed`;本機版本停在 2026.02.04(約半年前),更新到 2026.08.19 後第 1 次就成功。**與偶發性 403 的區分準則已寫入共通踩坑** |
| 2026-08-23 | 自己踩到 **`grep … | head -1` 遮蔽退出碼**(找不到也回 0),連帶暴露另一個問題:**筆記檔頭只寫影片標題、沒放網址,導致 `build_source_index.py` 漏收該來源**。兩者都已寫進 prompt |
| 2026-09-06(當日第二次) | 依使用者指示,**把巡檢(排程 5)與美投君(排程 4)也全部改用 channel ID**,八個頻道的 ID 已逐一解析驗證並列表於共通踩坑;兩支排程重建為 `004b3a7a`(巡檢 08:12)與 `bdb6be2c`(美投君 07:50)。**並在 prompt 中要求回報時使用頻道中文名稱**(先前只寫 handle / ID 不好讀)。另加入「字幕下載遇 HTTP 429 要重試」與「作者若有業配或推薦連結須標明立場」兩條 |
| 2026-09-06 | ⚠️⚠️ **Gary Chen 的 handle 從 `@garytalksstuff` 改成 `@garychenai`,舊 handle 回 404**,排程當天列表整個失敗。用既有筆記的 video id 反查出新 handle 與 channel ID(`UC9C3t-3ocL0LiwGRD0gBJ8A`),**全部改用 channel ID URL(不受日後改名影響)**,並把這個坑寫進共通踩坑。當日補上新片 1 篇 |
| 2026-09-04 | 使用者要求「恢復 cron task」。`CronList` 顯示五個都還在(未到期),但**四個固定排程的 prompt 仍寫著 `.` 去重範圍**——就是 09-03 那個靜默誤報 bug 的殘留。故全刪重建為 `f9a9b1f3`/`5cb4b8b4`/`cc2882c1`/`de16b6ea`/`4446ffdd`(約 **09-11** 到期),五個 prompt 一律改為 `knowledge/`,並加上 commit 訊息的 Co-Authored-By / Claude-Session trailer 要求 |
| 2026-09-03 | ⚠️ **修掉一個自己造成的靜默 bug**:昨天把存量清單(含所有待處理 video id)寫進本檔後,去重指令對整個 repo 搜尋會匹配到該清單,**使每一支存量都誤報 SEEN 且完全不報錯**。已將去重範圍限定 `knowledge/`,排程重建為 `f115eb43`,並把這條寫進共通踩坑 |
| 2026-09-02 | 第 5 排程加入 **小Lin说 `@xiao_lin_shuo`**(282 萬訂閱、財經商業解說、**官方中文字幕不需 Whisper**、約兩週一支),重建為 `c579118a`。該頻道 8 支全未整理,存量由 31 增至約 39;其中 AI 資本混戰與 SpaceX 上市兩支可增補既有筆記 |
| 2026-09-01 | **第 5 排程首次執行後修訂為 `28e85f8c`** —— 實測發現五個頻道有 **32 支存量**,原本「有字幕者數量不限」會一次寫 15 篇,改為**每次上限 2–3 篇(Whisper 至多 1 支)**、並加入「優先增補既有筆記」的挑選序;**移除 `@TheStormMedia`**(半數會員限定、題材偏離)。當日完成 Why QQ 的 Jalapeño 拆解一篇 |
| 2026-09-01 | **新增第 5 個排程 `9fe20ecd`(未涵蓋頻道每日巡檢 08:12)** —— 盤點發現作者索引 49 位僅 3 位有排程,六個已累積 3 篇以上的頻道全靠手動補;handle 已逐一解析驗證,並對無字幕頻道設「每次最多 1 支」的 Whisper 上限 |
| 2026-09-01 | 到期前主動全刪重建為 `ae5bf239`(GitHub Weekly)/ `881dd1ea`(Gary Chen)/ `8949d7df`(gooaye)/ `fb30e2ee`(美投君),約 **09-08** 到期。**本輪重點:同步 2026-08-30 的 repo 重整** —— 筆記路徑一律改為 `knowledge/...`、腳本改為 `scripts/knowledge/`;另新增三條踩坑(`git push … | grep …; echo $?` 會拿到 grep 的退出碼故改用 rev-parse 比對、印中文或 emoji 需先 reconfigure stdout 否則 cp950 崩潰、`wc -c` 位元組 vs `len(s)` 字元差約 3 倍別誤判內容遺失)與兩條慣例(財報類影片須比對 SEC/官方 IR 並列核實表、作者推廣自家產品時要標明立場)。⚠️ 已知缺口:README 作者索引 49 位,**僅 3 位有排程涵蓋**,詳見下節 |
| 2026-08-26 | 到期前主動全刪重建為 `1b469bda`/`b3478479`/`e88151b9`/`07b52878`(約 **09-02** 到期)。**本輪新增三條踩坑(持續性 403 判準、pipe 遮蔽退出碼、來源需放完整網址)與一條慣例(同主題優先增補既有筆記、檔名不動),並補上 `technology/software-engineering` 這個新中類。** 當日四個排程都已跑過且皆無新內容,無需補檢 |
