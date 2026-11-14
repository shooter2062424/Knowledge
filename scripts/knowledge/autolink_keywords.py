"""
Insert Obsidian wikilinks for per-note keywords inside note bodies.

Reads a keyword map ``{slug: [keyword, ...]}`` and turns the first body
occurrence of each keyword, in every *other* note, into ``[[slug|keyword]]``.
Code fences, inline code, headings, tables, existing links, URLs, frontmatter
and the 來源 / 相關筆記 sections are never modified.

Usage:
    python scripts/knowledge/autolink_keywords.py KEYWORDS.json [--apply]
        [--max-docs 60] [--sample 30]

Without ``--apply`` it only reports statistics and sample contexts.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import sys
from pathlib import Path

NOTES_ROOT   = Path("knowledge")
GENERIC      = {
    "ai", "agent", "llm", "模型", "投資", "分析", "策略", "週報", "影片", "筆記",
    "claude", "openai", "github", "python", "chatgpt", "google", "nvidia",
    # words whose meaning differs per note, found by reviewing a dry run
    "compaction", "dispatch", "agent skills", "azure", "prompt engineering",
    "human-in-the-loop", "keep awake", "殘差流", "統一調度", "指令遵循", "五個欄位",
}
SECTION_SKIP = re.compile(r"^##\s*(來源|相關筆記|參考|延伸閱讀)")
LINK_PAT     = re.compile(
    r"\[\[[^\]]*\]\]"          # existing wikilinks
    r"|!\[[^\]]*\]\([^)]*\)"   # images
    r"|\[[^\]]*\]\([^)]*\)"    # markdown links
    r"|`[^`]*`"                # inline code
    r"|https?://\S+"           # bare urls
    r"|<[^>]+>"                # html tags
)


def load_notes() -> dict[str, Path]:
    """
    Map slug to path for every markdown note under ``knowledge/``.

    Returns:
        Dict of note slug (file name without ``.md``) to its path.
    """
    notes: dict[str, Path] = {}
    for root, _dirs, files in os.walk(NOTES_ROOT):
        for name in files:
            if name.endswith(".md"):
                notes[name[:-3]] = Path(root) / name
    return notes


def keyword_regex(keyword: str) -> re.Pattern[str]:
    """
    Build a regex matching ``keyword`` without splitting a longer ASCII word.

    Args:
        keyword: The literal keyword text.

    Returns:
        Compiled pattern; case-insensitive when the keyword is pure ASCII.
    """
    body = re.escape(keyword)
    if re.match(r"[A-Za-z0-9]", keyword[0]):
        body = r"(?<![A-Za-z0-9])" + body
    if re.match(r"[A-Za-z0-9]", keyword[-1]):
        body = body + r"(?![A-Za-z0-9])"
    flags = re.IGNORECASE if keyword.isascii() else 0
    return re.compile(body, flags)


def linkable_spans(text: str) -> list[tuple[int, int]]:
    """
    Return character spans of ``text`` where a link may be inserted.

    Args:
        text: Full markdown text with LF line endings.

    Returns:
        List of (start, end) spans outside code, headings, tables, links,
        frontmatter and the skipped sections.
    """
    spans: list[tuple[int, int]] = []
    pos = 0
    in_fence = False
    in_front = text.startswith("---\n")
    skip_section = False
    first = True
    for line in text.split("\n"):
        start, end = pos, pos + len(line)
        pos = end + 1
        stripped = line.strip()
        if in_front:
            if not first and stripped == "---":
                in_front = False
            first = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("#"):
            skip_section = bool(SECTION_SKIP.match(line))
            continue
        if skip_section or stripped.startswith("|"):
            continue
        cursor = start
        for m in LINK_PAT.finditer(line):
            if start + m.start() > cursor:
                spans.append((cursor, start + m.start()))
            cursor = start + m.end()
        if cursor < end:
            spans.append((cursor, end))
    return spans


def build_keywords(raw: dict[str, list[str]], notes: dict[str, Path],
                   max_docs: int) -> tuple[dict[str, str], list[str]]:
    """
    Validate keywords and map each surviving keyword to one slug.

    Args:
        raw: Proposed ``{slug: [keyword, ...]}``.
        notes: Slug to path map.
        max_docs: Drop keywords found in more than this many other notes.

    Returns:
        ``({keyword: slug}, drop_report_lines)``.
    """
    texts = {s: p.read_text(encoding="utf-8") for s, p in notes.items()}
    report: list[str] = []
    claim: dict[str, set[str]] = collections.defaultdict(set)
    for slug, kws in raw.items():
        if slug not in notes:
            continue
        for kw in kws:
            kw = kw.strip()
            if not kw or kw.lower() in GENERIC:
                report.append(f"generic: {kw}")
                continue
            if (kw.isascii() and len(kw) < 5) or (not kw.isascii() and len(kw) < 3):
                report.append(f"short: {kw}")
                continue
            if not keyword_regex(kw).search(texts[slug]):
                report.append(f"not-in-own-note: {slug}:{kw}")
                continue
            # The keyword must name the note's own topic, i.e. show up in a heading.
            heads = "\n".join(re.findall(r"(?m)^#{1,3}\s+.+$", texts[slug]))
            if not keyword_regex(kw).search(heads):
                report.append(f"not-in-heading: {slug}:{kw}")
                continue
            claim[kw.lower() if kw.isascii() else kw].add(slug)
    final: dict[str, str] = {}
    for kw, slugs in claim.items():
        if len(slugs) > 1:
            report.append(f"ambiguous: {kw} -> {sorted(slugs)}")
            continue
        slug = next(iter(slugs))
        pat = keyword_regex(kw)
        docs = sum(1 for s, t in texts.items() if s != slug and pat.search(t))
        if docs > max_docs:
            report.append(f"too-common({docs}): {kw}")
            continue
        final[kw] = slug
    return final, report


def link_note(slug: str, text: str,
              kw_map: dict[str, str]) -> tuple[str, list[tuple[str, str, str]]]:
    """
    Insert links for the first occurrence of each keyword.

    Args:
        slug: Slug of the note being edited (never linked to itself).
        text: Note text with LF line endings.
        kw_map: ``{keyword: target_slug}``.

    Returns:
        ``(new_text, [(shown_text, target_slug, context), ...])``.
    """
    done_targets = {
        m.split("|")[0].split("#")[0].strip()
        for m in re.findall(r"\[\[([^\]]+)\]\]", text)
    }
    spans = linkable_spans(text)
    taken: list[tuple[int, int, str, str]] = []
    for kw in sorted(kw_map, key=len, reverse=True):
        target = kw_map[kw]
        if target == slug or target in done_targets:
            continue
        pat = keyword_regex(kw)
        hit = None
        for s, e in spans:
            for m in pat.finditer(text, s, e):
                if all(m.end() <= a or m.start() >= b for a, b, _, _ in taken):
                    hit = m
                    break
            if hit:
                break
        if hit:
            taken.append((hit.start(), hit.end(), target, hit.group(0)))
            done_targets.add(target)
    out = text
    ins: list[tuple[str, str, str]] = []
    for a, b, target, shown in sorted(taken, reverse=True):
        ctx = text[max(0, a - 18):b + 18].replace("\n", " ")
        ins.append((shown, target, ctx))
        out = out[:a] + f"[[{target}|{shown}]]" + out[b:]
    return out, ins


def main() -> int:
    """
    CLI entry point.

    Returns:
        Process exit code.
    """
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("keywords")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--max-docs", type=int, default=15)
    ap.add_argument("--sample", type=int, default=30)
    args = ap.parse_args()
    raw = json.loads(Path(args.keywords).read_text(encoding="utf-8"))
    notes = load_notes()
    kw_map, report = build_keywords(raw, notes, args.max_docs)
    cats = collections.Counter(r.split(":")[0].split("(")[0] for r in report)
    print(f"keywords kept {len(kw_map)}; dropped {len(report)} {dict(cats)}")
    total, changed = 0, 0
    allins: list[tuple[str, str, str, str]] = []
    for slug, path in notes.items():
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        new, ins = link_note(slug, text, kw_map)
        if ins:
            changed += 1
            total += len(ins)
            allins += [(slug, *i) for i in ins]
            if args.apply:
                path.write_text(new, encoding="utf-8", newline="\n")
    print(f"notes changed {changed}, links inserted {total}")
    per = collections.Counter(t for _, _, t, _ in allins)
    print("top targets", per.most_common(8))
    random.seed(7)
    for slug, shown, target, ctx in random.sample(allins, min(args.sample, len(allins))):
        line = f"{slug[:26]} | {shown} -> {target[:32]} | ...{ctx}...\n"
        sys.stdout.buffer.write(line.encode("utf-8"))
    Path(args.keywords).with_suffix(".drop.txt").write_text("\n".join(report), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
