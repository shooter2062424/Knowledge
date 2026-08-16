#!/usr/bin/env python3
"""檢查 Markdown 裡的 Mermaid 區塊是否符合本倉庫的語法慣例。

用法:
    python scripts/lint_mermaid.py <檔案.md> [更多檔案...]
    python scripts/lint_mermaid.py            # 不給參數 = 掃全庫

檢查兩件事(對應 CLAUDE.md 的規範):
  1. 節點/邊標籤含特殊字元 ( ) / : , < > 時必須用雙引號包起來
  2. <br/> 必須出現在雙引號內

唯讀,不會修改任何檔案。退出碼:0 = 沒問題,1 = 有問題。
"""
import os
import re
import sys

BAD_CHARS = set('()/:,<>')
LABEL_RE = re.compile(r'(?:\[\(|\[|\{\{|\{|\()(.*?)(?:\)\]|\]|\}\}|\}|\))')
SKIP_PREFIX = ('%%', 'subgraph', 'direction', 'flowchart', 'graph',
               'sequenceDiagram', 'stateDiagram', 'note', 'end', 'participant',
               'pie', 'gantt', 'classDiagram', 'erDiagram', 'title')


def check_file(path):
    try:
        text = open(path, encoding='utf-8').read()
    except OSError:
        return []
    problems = []
    for idx, block in enumerate(re.findall(r'```mermaid\n(.*?)```', text, re.S), 1):
        head = block.strip().split('\n')[0].strip()
        # these diagram types use a different label syntax entirely
        if head.startswith(('stateDiagram', 'sequenceDiagram', 'quadrantChart',
                            'pie', 'gantt', 'classDiagram', 'erDiagram',
                            'timeline', 'mindmap', 'journey')):
            continue
        for line in block.split('\n'):
            t = line.strip()
            if not t or t.startswith(SKIP_PREFIX):
                continue
            # blank out every properly double-quoted span
            stripped = re.sub(r'"[^"]*"', '""', t)
            for m in LABEL_RE.finditer(stripped):
                lab = m.group(1).strip()
                if not lab or lab == '""':
                    continue
                if any(c in BAD_CHARS for c in lab):
                    problems.append((idx, 'UNQUOTED-SPECIAL', t))
                    break
            if '<br/>' in stripped:
                problems.append((idx, 'BR-OUTSIDE-QUOTES', t))
    return problems


def iter_md(root='.'):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != '.git' and not d.startswith('.')]
        for f in sorted(filenames):
            if f.endswith('.md'):
                yield os.path.join(dirpath, f)


def main():
    targets = sys.argv[1:] or list(iter_md('.'))
    total = 0
    checked = 0
    for path in targets:
        problems = check_file(path)
        checked += 1
        if problems:
            rel = os.path.relpath(path, '.').replace(os.sep, '/')
            print(rel)
            for blk, kind, line in problems:
                print('  block %d %s: %s' % (blk, kind, line))
            total += len(problems)
    print('checked %d file(s), %d problem(s)' % (checked, total))
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
