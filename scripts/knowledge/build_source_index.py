#!/usr/bin/env python3
"""重建 INDEX-SOURCES.md:掃描全庫筆記,建立 video id / arXiv 編號 → 筆記的對照表。

用法(在 repo 根目錄執行):
    python scripts/knowledge/build_source_index.py

會覆寫根目錄的 INDEX-SOURCES.md。唯讀掃描,不會動到任何筆記。
"""
import io
import json
import os
import re
import sys

SKIP_TOP = {'README.md', 'SCHEDULES.md', 'CLAUDE.md', 'INDEX-SOURCES.md'}

# 只索引知識筆記。research/ 的研究產出與 scripts/ 的說明不屬於「來源 → 筆記」對照表。
SKIP_DIRS = {'research', 'scripts', 'quests', 'rawdata'}

YT_RE = re.compile(r'(?:youtu\.be/|watch\?v=)([A-Za-z0-9_-]{11})')
ARXIV_RE = re.compile(r'arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})')


def collect(root_dir):
    rows = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d != '.git' and not d.startswith('.')]
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, root_dir).replace(os.sep, '/')
            if rel in SKIP_TOP:
                continue
            if rel.split('/')[0] in SKIP_DIRS:
                continue
            try:
                s = open(full, encoding='utf-8').read()
            except OSError:
                continue
            title = ''
            for line in s.split('\n'):
                if line.startswith('# '):
                    title = line[2:].strip()
                    break
            yt = sorted(set(YT_RE.findall(s)))
            ax = sorted(set(ARXIV_RE.findall(s)))
            if yt or ax:
                rows.append({'path': rel, 'title': title, 'yt': yt, 'arxiv': ax})
    return rows


def render(rows):
    yt, ax = [], []
    for r in rows:
        for v in r['yt']:
            yt.append((v, r['title'], r['path']))
        for a in r['arxiv']:
            ax.append((a, r['title'], r['path']))
    yt.sort(key=lambda x: x[0].lower())
    ax.sort(key=lambda x: x[0])

    def esc(t):
        return t.replace('|', '\\|')

    out = io.StringIO()
    w = out.write
    w('# 來源索引(video id / arXiv 編號 → 筆記)\n\n')
    w('貼連結前先在這裡查,就知道有沒有整理過。\n\n')
    w('> ⚠️ **本檔由 `scripts/knowledge/build_source_index.py` 自動產生,請勿手動編輯。**\n')
    w('> 統計:**%d 個 YouTube video id**、**%d 個 arXiv 編號**,涵蓋 **%d 篇**筆記。\n\n'
      % (len(yt), len(ax), len(rows)))
    w('---\n\n## 快速查詢\n\n```bash\n')
    w('# repo 根目錄執行(-F 固定字串、-- 終止選項解析,id 以連字號開頭也安全)\n')
    w('grep -F -- "<video-id 或 arXiv 編號>" INDEX-SOURCES.md\n```\n\n')
    w('查不到 = 尚未整理。也可以直接對全庫查:\n\n```bash\n')
    w('grep -rlF --include=*.md -- "<id>" .\n```\n\n')
    w('⚠️ `--include=*.md` 必須放在 `--` **之前**,否則 grep 會把它當檔名而回 exit 2。\n\n')
    w('---\n\n## YouTube(%d 部,依 video id 排序)\n\n' % len(yt))
    w('| video id | 筆記 | 路徑 |\n|---|---|---|\n')
    for v, t, p in yt:
        w('| `%s` | %s | [%s](./%s) |\n' % (v, esc(t), p, p))
    w('\n---\n\n## arXiv(%d 篇,依編號排序)\n\n' % len(ax))
    w('| arXiv | 筆記 | 路徑 |\n|---|---|---|\n')
    for a, t, p in ax:
        w('| `%s` | %s | [%s](./%s) |\n' % (a, esc(t), p, p))
    w('\n---\n\n## 重建\n\n```bash\npython scripts/knowledge/build_source_index.py\n```\n\n')
    w('抓兩種樣式:\n\n')
    w('- YouTube:`youtu.be/<11 碼>` 或 `watch?v=<11 碼>`\n')
    w('- arXiv:`arxiv.org/{abs,pdf,html}/<編號>`\n\n')
    w('新增筆記後重跑即可覆蓋。**不要手動編輯**——手動加的內容會在下次重建時消失。\n\n')
    w('> 註:一篇筆記可能對應多個 id(同時引用影片與論文),一個 id 也可能出現在多篇筆記中(交叉引用)。\n')
    return out.getvalue()


def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    rows = collect(root_dir)
    text = render(rows)
    target = os.path.join(root_dir, 'INDEX-SOURCES.md')
    open(target, 'w', encoding='utf-8', newline='\n').write(text)
    n_yt = sum(len(r['yt']) for r in rows)
    n_ax = sum(len(r['arxiv']) for r in rows)
    print('wrote %s — %d notes, %d youtube ids, %d arxiv ids' % (target, len(rows), n_yt, n_ax))


if __name__ == '__main__':
    main()
