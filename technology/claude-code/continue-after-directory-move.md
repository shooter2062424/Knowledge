# Claude Code:搬移專案目錄後,如何保住 `--continue` 對話歷史

**主題分類:** 科技 / Claude Code 維運技巧
**來源:** GitHub gist〈Claude Code Continue Functionality: Directory Migration Guide〉(作者 gwpl)
**整理日期:** 2026-05-30

> 重點問題:**Claude Code 目前沒有內建的「目錄搬移」功能**。每個專案目錄各自維護獨立的對話 session,**`mv` 搬走資料夾後歷史不會自動跟著走**。本筆記講機制 + 修復步驟。

---

## 1. 運作機制:`--continue` 怎麼找到歷史

對話歷史以 **JSONL** 存在 `~/.claude/projects/<把路徑編碼後的目錄名>/`。Claude Code 用「**工作目錄絕對路徑**」當 key——`--continue` 時:

```mermaid
flowchart LR
    A["pwd 取當前目錄"] --> B["把路徑編碼<br/>(/ → -)"]
    B --> C["找 ~/.claude/projects/<編碼路徑>/"]
    C --> D["讀該目錄所有 .jsonl"]
    D --> E["從最近的 session 重建對話"]
```

- **路徑編碼規則:** 取絕對路徑,把所有 `/` 換成 `-`。例:`/home/alice/code/project` → `-home-alice-code-project`。
- **檔案結構:**
  ```
  ~/.claude/
  ├── projects/<編碼路徑>/
  │   ├── <session-uuid>.jsonl    # 完整對話(含工具呼叫與結果)
  │   └── <summary-uuid>.jsonl    # 對話摘要(session 變長時用)
  ├── settings.json   .credentials.json   statsig/
  ```
  每行一個事件,含 `sessionId`、`parentUuid`(串接訊息)、`cwd`(當時工作目錄)、`version`、`timestamp`。
- **專案內檔案**(會跟著專案一起搬):`./.claude/`(settings、commands)、`CLAUDE.md`、`.mcp.json`。

> 💡 **Windows 實機驗證(本筆記補充):** Windows 上 **連磁碟機代號的 `:` 也會被換成 `-`**。例:本機 `C:\Users\shoot\project\Knowledge` 的歷史目錄就是 `~/.claude/projects/C--Users-shoot-project-Knowledge/`(`C:` → `C-`、各 `\` → `-`,於是開頭出現 `C--`)。所以 gist 的「`/ → -`」在 Windows 要理解成「**路徑分隔字元與 `:` 都換成 `-`**」。

---

## 2. 快速修復:搬完目錄後讓歷史接回來

```bash
# 假設從 /home/user/old-location/project 搬到 /home/user/new-location/project
cd ~/.claude/projects/
mv -- -home-user-old-location-project -home-user-new-location-project
#      ^^ 用 -- 避免 mv 把開頭的連字號當成參數
# 然後到新目錄驗證
cd /home/user/new-location/project && claude --continue
```

**完整搬遷(連設定一起):**
```bash
# 1) 搬專案內的 Claude 檔
cp -r ~/path/foo/.claude ~/path/bar/ ; cp ~/path/foo/CLAUDE.md ~/path/bar/ ; cp ~/path/foo/.mcp.json ~/path/bar/
# 更新設定檔裡的絕對路徑
sed -i 's|/path/foo|/path/bar|g' ~/path/bar/.claude/settings.json ~/path/bar/.mcp.json
# 2) 搬對話歷史目錄
OLD=$(echo "/path/foo" | sed 's/\//-/g'); NEW=$(echo "/path/bar" | sed 's/\//-/g')
mv ~/.claude/projects/$OLD ~/.claude/projects/$NEW
```

---

## 3. 替代做法

- **Symlink 固定位置:** 常搬就把編碼目錄做成穩定 symlink,搬移時只更新連結(`ln -sfn`)。
- **Git Worktrees(最乾淨):** 同一個 codebase 要 **平行、各自獨立的 session**,用 worktree——`git worktree add ~/path/bar feature-branch`,每個 worktree 各自有獨立 Claude session,避免共用對話狀態的複雜。

---

## 4. session 管理指令

| 指令 | 作用 |
|---|---|
| `claude --continue` | 接續當前目錄 **最近一個** 對話 |
| `claude --resume` | 跳出選單,從過往 session 挑一個 |
| `claude --continue --print "prompt"` | 帶指定 prompt 接續 |
| `/compact` | 壓縮對話歷史以省 context window |
| `claude -p "continue our previous work" --output-format stream-json` | headless 自動化接續 |

---

## 5. 應用案例

- **把專案從 `~/tmp/poc` 正式搬到 `~/work/myapp` 但想留下幾天累積的對話:** 先 `pwd | sed 's/\//-/g'` 查舊編碼名、`ls ~/.claude/projects/` 確認 → `mv -- <舊編碼> <新編碼>` → `claude --continue` 接回。
- **同一 repo 要同時開兩條互不干擾的 Claude session(例:一條做 feature、一條做 review):** 用 `git worktree add` 開第二個工作目錄,各自 `claude`,歷史天然分流。
- **備份/稽核對話:** `cd ~/.claude/projects && git init && git add . && git commit -m backup`;分析某 session 用 `grep '"type":"user"' *.jsonl | jq -r '.message.content'` 抽出所有使用者訊息。
- **清理:** `find ~/.claude/projects/ -name "*.jsonl" -mtime +30 -delete`(刪 30 天前)+ `find ~/.claude/projects/ -type d -empty -delete`。

---

## 6. 注意事項與限制

- **安全:** JSONL **含完整對話(連程式碼片段)**,可能有敏感資訊 → `chmod -R 700 ~/.claude/`,必要時加密或排除備份。
- **目前限制:** 無自動 session 遷移、各目錄歷史 **完全獨立**、無內建匯出/匯入、無跨目錄接續——搬專案得手動處理設定與歷史。
- **故障排除:** 接不回多半是 **編碼路徑不符**(`echo "Current encoded: $(pwd | sed 's/\//-/g')"` 比對 `ls ~/.claude/projects/`);JSONL 疑似損壞用 `jq empty <file>` 驗證。

> ⚠️ 這些是社群整理的內部機制與技巧,**未必是官方保證的行為**;不同 Claude Code 版本的存放路徑/格式可能變動,操作前先備份 `~/.claude/`。

---

## 來源

- [gist:Claude Code Continue Functionality — Directory Migration Guide(gwpl)](https://gist.github.com/gwpl/e0b78a711b4a6b2fc4b594c9b9fa2c4c)
- [Claude Code 官方文件](https://docs.anthropic.com/en/docs/claude-code) · [JSONL 格式](https://jsonlines.org/)
