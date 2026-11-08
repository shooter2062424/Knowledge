#!/usr/bin/env python3
"""Team KB v1:一條一檔的 claim、別名檢索、取代鏈、scope 解析、lint、未找到清單。只用標準函式庫。

目錄(以本檔所在的上一層為根):
  claims/    已核准、不可變的 claim(只有 build 會改 status / superseded_by 兩個衍生欄位)
  inbox/     待審 claim(propose 寫入)   inbox/rejected/ 被退回
  topics/    build 產生的主題現況頁(勿手改)
  state/     unfound.jsonl(找不到清單)、queries.jsonl(查詢紀錄)、ledger.jsonl(核准紀錄)
  raw/       不可變原始紀錄(會議逐字稿等)

指令:propose / review / approve / reject / build / search / resolve / unfound / lint / show / template
環境變數:KB_USER(操作者)、KB_TODAY(模擬日期,測試用)
"""
from __future__ import annotations

import argparse
import datetime as dt
import itertools
import json
import math
import os
import re
import secrets
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:  # Windows 主控台預設 cp950,強制 UTF-8 輸出
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

ROOT = Path(os.environ.get("KB_ROOT", Path(__file__).resolve().parent))
CLAIMS, INBOX, REJECTED, TOPICS, STATE = (ROOT / "claims", ROOT / "inbox", ROOT / "inbox" / "rejected", ROOT / "topics", ROOT / "state")
TODAY = os.environ.get("KB_TODAY", str(dt.date.today()))
DIMS = ["project", "platform", "branch"]  # 決策:維持三個維度;要加維度只改這一行
LIFECYCLES = ("active", "deprecated", "retired")
LIST_FIELDS = {"supersedes", "aliases", "superseded_by"}
REQUIRED = ["subject", "statement", "valid_from", "source", "author", "aliases"]
MIN_ALIASES = 4
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")  # subject / concept:會成為 topics/<subject>.md 的檔名,不得含路徑字元


def identity() -> str:
    """操作者身分:只認環境(KB_USER,由 harness / 登入帳號設定)或作業系統帳號,不接受命令列自報。
    注意:同一個 OS 帳號下的程序仍可改環境變數;真正的強制要靠 agent 的工具白名單不含 approve/reject(見 README)。"""
    return os.environ.get("KB_USER") or __import__("getpass").getuser()



# ---------- 讀寫 ----------
def parse(text: str) -> dict:
    """解析 `---` 之間的單行 `key: value` frontmatter(刻意不用 YAML,維持 grep 友善)。"""
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    out: dict = {}
    for ln in (m.group(1) if m else "").splitlines():
        k, sep, v = ln.partition(":")
        if sep:
            out[k.strip()] = v.strip()
    return out


def split_list(v: str) -> list[str]:
    if not v:
        return []
    parts = [p.strip() for p in re.split(r"[,，、;；]", v) if p.strip()]
    if len(parts) == 1 and re.search(r"\s", parts[0]):
        parts = parts[0].split()
    return parts


def dump(c: dict) -> str:
    order = ["id", "concept", "subject", "statement", "lifecycle", *DIMS, "valid_from", "retire_when", "review_by",
             "supersedes", "aliases", "source", "author", "proposer", "reviewer", "status", "superseded_by"]
    lines = []
    for k in order + [k for k in c if k not in order and not k.startswith("_")]:
        v = c.get(k)
        if v in (None, "", []):
            continue
        lines.append(f"{k}: {', '.join(v) if isinstance(v, list) else v}")
    return "---\n" + "\n".join(lines) + "\n---\n"


def load_dir(d: Path) -> dict[str, dict]:
    out = {}
    for f in sorted(d.glob("*.md")) if d.exists() else []:
        c = parse(f.read_text(encoding="utf-8"))
        if "id" not in c:
            c["id"] = f.stem
        c["_path"] = f
        for k in LIST_FIELDS:
            c[k] = split_list(c.get(k, "")) if not isinstance(c.get(k), list) else c[k]
        c.setdefault("lifecycle", "active")
        c.setdefault("concept", c.get("subject", ""))
        for d_ in DIMS:
            c[d_] = (c.get(d_) or "*").strip().lower()
        out[c["id"]] = c
    return out


def load_claims() -> dict[str, dict]:
    return load_dir(CLAIMS)


def derive(claims: dict[str, dict]) -> tuple[dict[str, list[str]], set[str]]:
    """回傳 (被誰取代, 被取代集合)。只有指向存在的 claim 的 supersedes 才算。"""
    by: dict[str, list[str]] = defaultdict(list)
    for c in claims.values():
        for o in c["supersedes"]:
            if o in claims:
                by[o].append(c["id"])
    return by, set(by)


def spec(c: dict) -> int:
    return sum(1 for d in DIMS if c[d] != "*")


def scope_str(c: dict) -> str:
    return " ".join(f"{d}={c[d]}" for d in DIMS if c[d] != "*") or "全域"


def log(name: str, rec: dict) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    rec = {"ts": dt.datetime.now().isoformat(timespec="seconds"), "user": os.environ.get("KB_USER", "?"), **rec}
    with open(STATE / name, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ---------- gate / propose / approve ----------
def gate(c: dict, claims: dict[str, dict]) -> tuple[list[str], list[str]]:
    """回傳 (錯誤, 警告)。錯誤擋下,警告只提示。"""
    err, warn = [], []
    for k, v in c.items():
        vals = v if isinstance(v, list) else [v]
        if any(isinstance(x, str) and re.search(r"[\r\n]", x) for x in vals):
            err.append(f"欄位 {k} 不得含換行字元")
    for k in ("subject", "concept"):
        if c.get(k) and not SLUG_RE.match(c[k]):
            err.append(f"{k} 只能是小寫英文、數字、- 或 _(開頭須為英數,最長 64):目前 {c[k]!r}")
    for k in REQUIRED:
        if not c.get(k):
            err.append(f"缺必填欄位 {k}")
    if c.get("valid_from") and not DATE_RE.match(c["valid_from"]):
        err.append("valid_from 必須是 YYYY-MM-DD")
    if c["lifecycle"] not in LIFECYCLES:
        err.append(f"lifecycle 必須是 {'/'.join(LIFECYCLES)}")
    if c["lifecycle"] == "deprecated" and not c.get("retire_when"):
        err.append("deprecated 必須有 retire_when(退場日只存在這一處)")
    for k in ("retire_when", "review_by"):
        if c.get(k) and not DATE_RE.match(c[k]):
            err.append(f"{k} 必須是 YYYY-MM-DD")
    if len(c["aliases"]) < MIN_ALIASES:
        err.append(f"aliases 至少 {MIN_ALIASES} 個(口語、同義、中英互換);目前 {len(c['aliases'])}")
    elif re.search(r"[一-鿿]", c.get("statement", "")) and not any(re.search(r"[A-Za-z]{3,}", a) for a in c["aliases"]):
        warn.append("aliases 沒有英文詞;英文提問會找不到(建議中英都補)")
    for o in c["supersedes"]:
        if o not in claims:
            err.append(f"supersedes 指向不存在的 {o}")
            continue
        old = claims[o]
        for d in DIMS:
            if c[d] != "*" and c[d] != old[d]:
                err.append(f"取代 {o} 時 {d} 不得比舊的更窄(新={c[d]},舊={old[d]});範圍變窄請另寫例外 claim,不要用 supersedes")
    same = [x for x in claims.values() if x["concept"] == c["concept"] and all(x[d] == c[d] for d in DIMS)
            and x["id"] not in c["supersedes"] and x["lifecycle"] != "retired" and x["statement"].strip() != c["statement"].strip()]
    _, sup = derive(claims)
    same = [x for x in same if x["id"] not in sup]
    if same:
        err.append(f"同 concept、同 scope 已有現行 claim {', '.join(x['id'] for x in same)} 且結論不同;要改請加 --supersedes,否則請寫成不同 scope")
    return err, warn


def cmd_template(a):
    print("""---
concept: ipc                 # 同一件事的名字(resolve 用它分組)
subject: ipc                 # 主題(產生 topics/<subject>.md)
statement: 一句話的結論,單一事實。
lifecycle: active            # active / deprecated / retired
project: *                   # 範圍;不寫或 * = 全部
platform: *
branch: *
valid_from: 2026-11-08
retire_when:                 # deprecated 時必填,日期只存在這一處
supersedes:                  # 例:CL-0003(明確取代同 scope 或更寬 scope 的舊 claim)
aliases: 口語說法, 同義詞, English term, 中英互換   # 至少 4 個,中英都要
source: M05@05:10            # 來源(會議時間戳、文件、連結)
author: 你的名字
---""")


def cmd_propose(a):
    c = {k: v for k, v in vars(a).items() if v is not None and k not in ("fn", "cmd")}
    for k in LIST_FIELDS:
        c[k] = split_list(c.get(k, "")) if not isinstance(c.get(k), list) else c[k]
    c.setdefault("lifecycle", "active")
    c.setdefault("concept", c.get("subject", ""))
    for d in DIMS:
        c[d] = (c.get(d) or "*").lower()
    claims = load_claims()
    err, warn = gate(c, claims)
    for w in warn:
        print("警告:", w)
    if err:
        print("退回(未寫入 inbox):")
        for e in err:
            print(" -", e)
        sys.exit(1)
    INBOX.mkdir(parents=True, exist_ok=True)
    pid = f"P-{dt.datetime.now():%Y%m%d%H%M%S}-{secrets.token_hex(2)}"
    c["id"] = pid
    c["proposer"] = identity()  # 信任來源的提案者身分;author 欄只是顯示用的自報名稱
    (INBOX / f"{pid}.md").write_text(dump(c), encoding="utf-8")
    print(f"已放入 inbox:{pid}(等另一人 review / approve)")


def cmd_review(a):
    claims = load_claims()
    items = load_dir(INBOX)
    if not items:
        print("inbox 是空的")
        return
    _, sup = derive(claims)
    for pid, c in items.items():
        print(f"\n## {pid}  by {c.get('author')}\n{c['statement']}\n範圍:{scope_str(c)}  concept={c['concept']}  lifecycle={c['lifecycle']}")
        err, warn = gate(c, claims)
        for e in err:
            print("  [擋] " + e)
        for w in warn:
            print("  [警告] " + w)
        for o in c["supersedes"]:
            if o in claims:
                print(f"  核可後 {o} 會變成 SUPERSEDED:{claims[o]['statement']}")
        # 受影響的格子:同 concept 現行 claim 與其範圍重疊者
        for x in claims.values():
            if x["concept"] == c["concept"] and x["id"] not in sup and x["id"] not in c["supersedes"] and overlaps(x, c):
                print(f"  與現行 {x['id']} 範圍重疊({scope_str(x)}):{x['statement']}")


def overlaps(x: dict, y: dict) -> bool:
    return all(x[d] == "*" or y[d] == "*" or x[d] == y[d] for d in DIMS)


def next_id(claims):
    n = max([int(m.group(1)) for k in claims if (m := re.match(r"CL-(\d+)$", k))] or [0])
    return f"CL-{n + 1:04d}"


def cmd_approve(a):
    items = load_dir(INBOX)
    if a.pid not in items:
        sys.exit(f"inbox 沒有 {a.pid}")
    c = items[a.pid]
    by = identity()
    if by in (c.get("proposer"), c.get("author")):
        sys.exit("核准者不可以是提案者本人(雙人規則;身分取自 KB_USER / 作業系統帳號,不接受 --by 自報)")
    claims = load_claims()
    err, _ = gate(c, claims)  # 核准當下重驗一次(等待期間可能有別的 claim 先進來:write-skew)
    if err:
        sys.exit("重驗未過:\n - " + "\n - ".join(err))
    cid = next_id(claims)
    c["id"], c["reviewer"] = cid, by
    CLAIMS.mkdir(parents=True, exist_ok=True)
    (CLAIMS / f"{cid}.md").write_text(dump(c), encoding="utf-8")
    items[a.pid]["_path"].unlink()
    log("ledger.jsonl", {"op": "approve", "claim": cid, "from": a.pid, "author": c.get("author"), "reviewer": by})
    build()
    print(f"已核准:{cid}")


def cmd_reject(a):
    items = load_dir(INBOX)
    if a.pid not in items:
        sys.exit(f"inbox 沒有 {a.pid}")
    REJECTED.mkdir(parents=True, exist_ok=True)
    p = items[a.pid]["_path"]
    p.rename(REJECTED / p.name)
    log("ledger.jsonl", {"op": "reject", "from": a.pid, "reason": a.reason})
    print("已退回:", a.pid)


# ---------- build ----------
def build() -> None:
    """寫回衍生欄位 status / superseded_by,並產生 topics/<subject>.md。"""
    claims = load_claims()
    by, sup = derive(claims)
    for c in claims.values():
        want_status = "superseded" if c["id"] in sup else ("retired" if c["lifecycle"] == "retired" else "current")
        want_by = ", ".join(sorted(by.get(c["id"], [])))
        if c.get("status") != want_status or c.get("superseded_by", "") != want_by:
            c["status"], c["superseded_by"] = want_status, [x for x in sorted(by.get(c["id"], []))]
            c["_path"].write_text(dump(c), encoding="utf-8")
    TOPICS.mkdir(parents=True, exist_ok=True)
    subjects = defaultdict(list)
    for c in claims.values():
        subjects[c["subject"]].append(c)
    for s, cs in subjects.items():
        if not SLUG_RE.match(s):  # 手改過的壞檔:不寫檔,交給 lint 報
            continue
        L = [f"# {s}(自動產生,請勿手改)\n", f"更新:{TODAY}\n", "## 現行\n"]
        for c in sorted(cs, key=lambda x: x["id"]):
            if c["id"] not in sup and c["lifecycle"] != "retired":
                tag = f" ⚠️ deprecated,退場 {c.get('retire_when', '?')}" if c["lifecycle"] == "deprecated" else ""
                L.append(f"- [{c['id']}] {c['statement']} (範圍:{scope_str(c)}; 生效 {c['valid_from']}; 來源 {c['source']}){tag}")
        old = [c for c in cs if c["id"] in sup or c["lifecycle"] == "retired"]
        if old:
            L.append("\n## 已被取代 / 已退場(歷史)\n")
            for c in sorted(old, key=lambda x: x["id"]):
                L.append(f"- [{c['id']}] {c['statement']} → 被 {', '.join(by.get(c['id'], [])) or '(退場)'} 取代")
        (TOPICS / f"{s}.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def cmd_build(a):
    build()
    print("build 完成:", len(load_claims()), "條 claim")


# ---------- search ----------
def tok(s: str) -> list[str]:
    s = s.lower()
    out = [w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w for w in re.findall(r"[a-z0-9_.+]+", s)]  # 極簡複數處理:reviewers=reviewer
    for seg in re.findall(r"[一-鿿]+", s):
        out += [seg[i:i + 2] for i in range(len(seg) - 1)]
    return [t for t in out if len(t) >= 2 or re.match(r"[a-z0-9]", t)]


ALIAS_W = float(os.environ.get("KB_ALIAS_W", "0.5"))  # 別名欄的權重(E1 實驗:1.0 會讓帶別名的同型 claim 擠掉英文字面查詢)


def doc_main(c: dict) -> str:
    return " ".join([c["statement"], c["concept"], c["subject"], *(c[d] for d in DIMS if c[d] != "*")])


def doc_text(c: dict) -> str:
    return doc_main(c) + " " + " ".join(c["aliases"])


def rank_claims(claims: dict[str, dict], ids: list[str], q: str) -> list[tuple[int, float]]:
    """兩欄 BM25:主文(statement/concept/subject/scope)+ 別名欄 × ALIAS_W。"""
    main = bm25_rank([doc_main(claims[i]) for i in ids], q)
    sc: dict[int, float] = {i: s for i, s in main}
    if ALIAS_W > 0:
        for i, s in bm25_rank([" ".join(claims[i]["aliases"]) for i in ids], q):
            sc[i] = sc.get(i, 0.0) + ALIAS_W * s
    return sorted(sc.items(), key=lambda x: -x[1])


def bm25_rank(texts: list[str], q: str, k1=1.5, b=0.75) -> list[tuple[int, float]]:
    toks = [Counter(tok(t)) for t in texts]
    n = len(toks)
    if not n:
        return []
    ln = [sum(t.values()) for t in toks]
    avg = sum(ln) / n or 1
    df = Counter(t for c in toks for t in c)
    sc = [0.0] * n
    for t in set(tok(q)):
        if t not in df:
            continue
        idf = math.log(1 + (n - df[t] + .5) / (df[t] + .5))
        for i, c in enumerate(toks):
            if t in c:
                sc[i] += idf * c[t] * (k1 + 1) / (c[t] + k1 * (1 - b + b * ln[i] / avg))
    return sorted([(i, s) for i, s in enumerate(sc) if s > 0], key=lambda x: -x[1])


def norm_template(c: dict) -> str:
    """折疊用:拿掉 scope 值(例如模組名)與數字後相同的 statement 視為同型。"""
    t = c["statement"].lower()
    for d in DIMS:
        if c[d] != "*":
            t = re.sub(r"(?<![a-z0-9])" + re.escape(c[d]) + r"(?![a-z0-9])", "<S>", t)
    return c["concept"] + "|" + t


def cmd_search(a):
    claims = load_claims()
    ids = list(claims)
    q = " ".join(a.query)
    ranked = rank_claims(claims, ids, q)
    if not a.no_log:
        log("queries.jsonl", {"q": q, "hits": len(ranked)})
    if not ranked:
        if not a.no_log:
            log("unfound.jsonl", {"q": q, "why": "no-hit"})
        print(f"沒有任何命中。已記入未找到清單。請換說法(中文/英文/口語)再試至少一次;仍找不到就回答「知識庫沒有」。")
        return
    by, sup = derive(claims)
    top, groups = [], {}
    for i, _ in ranked:
        c = claims[ids[i]]
        key = norm_template(c) if spec(c) else c["id"]
        if key in groups:
            groups[key].append(c["id"])
            continue
        groups[key] = [c["id"]]
        top.append(c["id"])
        if len(top) >= a.k:
            break
    seen = set(top)
    for cid in top:
        c = claims[cid]
        st = "SUPERSEDED" if cid in sup else ("RETIRED" if c["lifecycle"] == "retired" else ("DEPRECATED" if c["lifecycle"] == "deprecated" else "current"))
        extra = []
        if cid in sup:
            extra.append("被 " + ", ".join(by[cid]) + " 取代")
        if c["lifecycle"] == "deprecated":
            extra.append(f"退場 {c.get('retire_when', '?')}")
        g = groups[norm_template(c) if spec(c) else cid]
        if len(g) > 1:
            extra.append(f"另有 {len(g) - 1} 條同型 claim 只差範圍: {', '.join(g[1:6])}{'…' if len(g) > 6 else ''}")
        print(f"[{cid}] ({st}) {c['statement']} | 範圍:{scope_str(c)} | 生效 {c['valid_from']} | 來源 {c['source']}" + (" | " + "; ".join(extra) if extra else ""))
    nb = []
    for cid in top:  # 取代鏈鄰居:永遠附上,不隱藏過期
        c = claims[cid]
        for n in c["supersedes"] + by.get(cid, []):
            if n in claims and n not in seen:
                seen.add(n)
                x = claims[n]
                nb.append(f"  +[{n}] ({'SUPERSEDED' if n in sup else 'current'}) {x['statement']} | 範圍:{scope_str(x)} | 來源 {x['source']} (取代鏈鄰居 of {cid})")
    if nb:
        print("-- 取代鏈鄰居 --")
        print("\n".join(nb))
    if len(ranked) < 2 and not a.no_log:
        log("unfound.jsonl", {"q": q, "why": "weak"})


def cmd_unfound(a):
    if a.report:
        p = STATE / "unfound.jsonl"
        if not p.exists():
            print("未找到清單是空的")
            return
        cnt, last = Counter(), {}
        for ln in p.read_text(encoding="utf-8").splitlines():
            r = json.loads(ln)
            cnt[r["q"]] += 1
            last[r["q"]] = r
        print(f"# 未找到清單({len(cnt)} 個不同查詢) — 每週補 aliases / 詞彙表 / 缺的 claim\n")
        for q, n in cnt.most_common():
            print(f"- ×{n} 「{q}」 ({last[q]['why']}, {last[q]['ts'][:10]}, {last[q]['user']})")
        return
    q = " ".join(a.query)
    log("unfound.jsonl", {"q": q, "why": a.why})
    print("已記入未找到清單:", q)


# ---------- resolve ----------
def cmd_resolve(a):
    claims = load_claims()
    _, sup = derive(claims)
    pool = [c for c in claims.values() if c["concept"] == a.concept and c["id"] not in sup and c["lifecycle"] != "retired"]
    if not pool:
        log("queries.jsonl", {"q": f"resolve {a.concept}", "hits": 0})  # 不進 unfound:agent 常把一句話當 concept 用,會污染清單
        known = sorted({c["concept"] for c in claims.values()})
        print(f"沒有 concept={a.concept} 的現行 claim。concept 是主題代號,不是問句;已有的 concept:{', '.join(known[:40])}{'…' if len(known) > 40 else ''}。要查內容請用 search。")
        sys.exit(4)
    given = {d: getattr(a, d).lower() for d in DIMS if getattr(a, d)}
    vals = {}
    for d in DIMS:
        known = sorted({c[d] for c in pool if c[d] != "*"})
        vals[d] = [given[d]] if d in given else known + ["(其他)"]
    cells = list(itertools.product(*[vals[d] for d in DIMS]))
    outcome: dict[tuple, str] = {}
    detail: dict[str, str] = {}
    conflict = False
    for cell in cells:
        m = [c for c in pool if all(c[d] == "*" or (cell[i] != "(其他)" and c[d] == cell[i]) for i, d in enumerate(DIMS))]
        if not m:
            outcome[cell] = "無適用 claim"
            continue
        top = max(spec(c) for c in m)
        w = [c for c in m if spec(c) == top]
        if len({c["statement"].strip() for c in w}) > 1:
            conflict = True
            outcome[cell] = "CONFLICT:" + ",".join(sorted(c["id"] for c in w))
        else:
            c = sorted(w, key=lambda x: x["valid_from"])[-1]
            outcome[cell] = c["id"]
            detail[c["id"]] = f"[{c['id']}] {c['statement']}" + (f" ⚠️ deprecated,退場 {c.get('retire_when', '?')}" if c["lifecycle"] == "deprecated" else "") + f"(範圍:{scope_str(c)};來源 {c['source']})"
    groups: dict[str, list[str]] = defaultdict(list)
    for cell, o in outcome.items():
        groups[o].append(" ".join(f"{d}={cell[i]}" for i, d in enumerate(DIMS) if d not in given) or "(已指定的範圍)")
    # 哪些未指定維度會改變結論
    matter = []
    for i, d in enumerate(DIMS):
        if d in given:
            continue
        for cell in cells:
            for other in vals[d]:
                c2 = cell[:i] + (other,) + cell[i + 1:]
                if outcome[cell] != outcome[c2]:
                    matter.append(d)
                    break
            else:
                continue
            break
    print(f"# resolve {a.concept}  已指定:{given or '無'}")
    for o, cs in groups.items():
        print(f"\n結論 {detail.get(o, o)}\n  適用情境:{'; '.join(cs[:12])}{'…' if len(cs) > 12 else ''}")
    if conflict:
        print("\nCONFLICT:同具體度的 claim 在某些情境重疊且結論不同,需要有人寫一條明確 claim(含兩者交集的 scope)並用 supersedes 取代其一。不要自行挑一個回答。")
        sys.exit(3)
    if matter:
        print(f"\nASK:結論會依 {', '.join(sorted(set(matter)))} 而不同,請先反問使用者這個條件,不要猜。")
        sys.exit(2)
    print("\n結論唯一,可直接回答。")


# ---------- lint ----------
def cmd_lint(a):
    claims = load_claims()
    by, sup = derive(claims)
    act = [c for c in claims.values() if c["id"] not in sup and c["lifecycle"] != "retired"]
    issues: list[tuple[str, str, str]] = []  # (級別, 代碼, 說明)
    for c in claims.values():
        i = c["id"]
        if not SLUG_RE.match(c["subject"]) or not SLUG_RE.match(c["concept"]):
            issues.append(("ERROR", "BAD-SLUG", f"{i} subject/concept 格式不合法({c['subject']!r}/{c['concept']!r}),topics 頁不會產生"))
        if c["lifecycle"] == "deprecated" and not c.get("retire_when"):
            issues.append(("ERROR", "NO-EXIT", f"{i} deprecated 但沒有 retire_when"))
        if c.get("retire_when") and c["retire_when"] < TODAY and c["lifecycle"] != "retired":
            issues.append(("ERROR", "OVERDUE", f"{i} 退場日 {c['retire_when']} 已過但 lifecycle={c['lifecycle']}"))
        if c.get("review_by") and c["review_by"] < TODAY and i not in sup:
            issues.append(("WARN", "REVIEW-DUE", f"{i} review_by {c['review_by']} 已過"))
        for o in c["supersedes"]:
            if o not in claims:
                issues.append(("ERROR", "DEAD-REF", f"{i} supersedes 不存在的 {o}"))
        if len(c["aliases"]) < MIN_ALIASES:
            issues.append(("WARN", "ALIASES-FEW", f"{i} aliases 只有 {len(c['aliases'])} 個"))
        elif re.search(r"[一-鿿]", c["statement"]) and not any(re.search(r"[A-Za-z]{3,}", x) for x in c["aliases"]):
            issues.append(("WARN", "ALIASES-NO-EN", f"{i} aliases 沒有英文詞"))
    for x, y in itertools.combinations(act, 2):
        if x["concept"] != y["concept"] or not overlaps(x, y) or x["statement"].strip() == y["statement"].strip():
            continue
        if spec(x) == spec(y):
            same = all(x[d] == y[d] for d in DIMS)
            inter = {d: (x[d] if x[d] != "*" else y[d]) for d in DIMS}
            if not same and any(all(r[d] == inter[d] for d in DIMS) for r in act if r["concept"] == x["concept"] and r["id"] not in (x["id"], y["id"])):
                continue  # 交集已有明確 claim 負責,不再算歧義
            issues.append(("ERROR", "CONFLICT" if same else "AMBIGUOUS-INTERSECTION",
                           f"{x['id']}({scope_str(x)}) 與 {y['id']}({scope_str(y)}) 同具體度、範圍" + ("相同" if same else "重疊") + "且結論不同;請寫一條明確 claim 並 supersedes 其一"))
    seen_t = defaultdict(list)
    for c in act:
        seen_t[(c["concept"], tuple(c[d] for d in DIMS), re.sub(r"\s+", "", c["statement"]))].append(c["id"])
    for k, v in seen_t.items():
        if len(v) > 1:
            issues.append(("WARN", "DUP-CANDIDATE", f"{', '.join(v)} 同 concept、同範圍、同文字"))
    # SHADOWED:在任何格子都不是勝出者
    for concept in {c["concept"] for c in act}:
        pool = [c for c in act if c["concept"] == concept]
        known = [sorted({c[d] for c in pool if c[d] != "*"}) + ["(其他)"] for d in DIMS]
        won = set()
        for cell in itertools.product(*known):
            m = [c for c in pool if all(c[d] == "*" or (cell[i] != "(其他)" and c[d] == cell[i]) for i, d in enumerate(DIMS))]
            if m:
                t = max(spec(c) for c in m)
                won |= {c["id"] for c in m if spec(c) == t}
        for c in pool:
            if c["id"] not in won:
                issues.append(("WARN", "SHADOWED", f"{c['id']} 在任何情境都不是勝出者(被更具體的 claim 完全蓋住)"))
    p = STATE / "unfound.jsonl"
    if p.exists():
        n = len({json.loads(x)["q"] for x in p.read_text(encoding="utf-8").splitlines()})
        if n:
            issues.append(("INFO", "UNFOUND", f"未找到清單有 {n} 個不同查詢待處理:python kb.py unfound --report"))
    shown = Counter()
    for lv, code, msg in issues:
        shown[code] += 1
        if shown[code] <= a.limit:
            print(f"[{lv}] {code}: {msg}")
    for code, n in shown.items():
        if n > a.limit:
            print(f"      … {code} 還有 {n - a.limit} 筆未顯示(--limit 調整)")
    errs = sum(1 for i in issues if i[0] == "ERROR")
    print(f"\nclaims={len(claims)} 現行={len(act)} 錯誤={errs} 警告={sum(1 for i in issues if i[0] == 'WARN')}")
    sys.exit(1 if errs else 0)


def cmd_show(a):
    claims = load_claims()
    if a.id not in claims:
        sys.exit("找不到 " + a.id)
    print(claims[a.id]["_path"].read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("template").set_defaults(fn=cmd_template)
    p = sp.add_parser("propose")
    for k in ["concept", "subject", "statement", "lifecycle", "valid_from", "retire_when", "review_by", "supersedes", "aliases", "source", "author", *DIMS]:
        p.add_argument("--" + k.replace("_", "-"), dest=k)
    p.set_defaults(fn=cmd_propose)
    sp.add_parser("review").set_defaults(fn=cmd_review)
    p = sp.add_parser("approve"); p.add_argument("pid"); p.set_defaults(fn=cmd_approve)
    p = sp.add_parser("reject"); p.add_argument("pid"); p.add_argument("--reason", default=""); p.set_defaults(fn=cmd_reject)
    sp.add_parser("build").set_defaults(fn=cmd_build)
    p = sp.add_parser("search"); p.add_argument("query", nargs="+"); p.add_argument("--k", type=int, default=8); p.add_argument("--no-log", action="store_true", help="提案前的重複檢查用,不記入查詢/未找到清單"); p.set_defaults(fn=cmd_search)
    p = sp.add_parser("resolve"); p.add_argument("concept")
    for d in DIMS:
        p.add_argument("--" + d)
    p.set_defaults(fn=cmd_resolve)
    p = sp.add_parser("unfound"); p.add_argument("query", nargs="*"); p.add_argument("--report", action="store_true"); p.add_argument("--why", default="agent-gave-up"); p.set_defaults(fn=cmd_unfound)
    p = sp.add_parser("lint"); p.add_argument("--limit", type=int, default=15); p.set_defaults(fn=cmd_lint)
    p = sp.add_parser("show"); p.add_argument("id"); p.set_defaults(fn=cmd_show)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
