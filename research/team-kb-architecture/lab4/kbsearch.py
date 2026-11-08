"""KB 檢索 CLI(實驗用):BM25(雙字)+ bge-small-zh 向量,RRF 融合;標示 status;附 supersedes 鄰居。

用法:python kbsearch.py "查詢" [--k 8]。環境變數 KBX_MODE=file 時結果寫到 results.txt、只印路徑。
需要:fastembed(PYTHONPATH)、FASTEMBED_CACHE_PATH。
"""
import math, os, re, sys, json
from collections import Counter
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
if os.environ.get("KBX_PYLIB"):
    sys.path.insert(0, os.environ["KBX_PYLIB"])


def tok(s: str):
    s = s.lower()
    out = re.findall(r"[a-z0-9_.+]+", s)
    for seg in re.findall(r"[一-鿿]+", s):
        out += [seg[i:i + 2] for i in range(len(seg) - 1)]
    return out


def load():
    docs = {}
    for f in sorted((HERE / "claims").glob("*.md")):
        t = f.read_text(encoding="utf-8")
        fm = dict(re.findall(r"^(\w+): (.*)$", t, re.M))
        docs[fm["id"]] = fm
    return docs


def main():
    args = sys.argv[1:]
    k = 8
    if "--k" in args:
        i = args.index("--k")
        k = int(args[i + 1])
        del args[i:i + 2]
    q = " ".join(args)
    docs = load()
    z = np.load(HERE / ".index.npz")
    ids = list(z["ids"])
    E = z["E"]
    texts = [docs[i]["statement"] + " " + docs[i].get("aliases", "") for i in ids]
    toks = [Counter(tok(t)) for t in texts]
    L = np.array([sum(c.values()) for c in toks], float)
    df = Counter(t for c in toks for t in c)
    N = len(ids)
    s_b = np.zeros(N)
    for t in set(tok(q)):
        if t in df:
            idf = math.log(1 + (N - df[t] + .5) / (df[t] + .5))
            for i, c in enumerate(toks):
                if t in c:
                    s_b[i] += idf * c[t] * 2.5 / (c[t] + 1.5 * (0.25 + 0.75 * L[i] / L.mean()))
    from fastembed import TextEmbedding
    m = TextEmbedding("BAAI/bge-small-zh-v1.5")
    qv = np.array(list(m.embed([q])))[0]
    qv /= np.linalg.norm(qv)
    s_v = E @ qv
    fused = np.zeros(N)
    for s in (s_b, s_v):
        for r, i in enumerate(np.argsort(-s)[:100]):
            if s[i] > 0:
                fused[i] += 1 / (60 + r + 1)
    ranked = [ids[i] for i in np.argsort(-fused)[:100] if fused[i] > 0]
    groups = {}
    if os.environ.get("KBX_COLLAPSE") == "1":
        MODS = "net storage ui telemetry build security sensor codec sched diag update crypto".split()
        def norm(t):
            for m in MODS:
                t = re.sub("(?<![A-Za-z])" + m + "(?![A-Za-z])", "<MOD>", t)
            return t
        top = []
        for cid in ranked:
            key = norm(docs[cid]["statement"]) if cid.startswith("HN") else cid
            if key not in groups:
                groups[key] = [cid]
                top.append(cid)
            else:
                groups[key].append(cid)
            if len(top) >= k:
                break
    else:
        top = ranked[:k]
    lines, seen = [], set(top)
    for cid in top:
        d = docs[cid]
        more = ""
        if groups:
            g = next((v for v in groups.values() if v[0] == cid), [])
            if len(g) > 1:
                more = f" | (另有 {len(g)-1} 條同型 claim 只差模組名: {', '.join(g[1:6])}{'…' if len(g) > 6 else ''})"
        lines.append(f"[{cid}] ({d['status']}) {d['statement']} | source={d.get('source','-')}" + (f" | superseded_by={d['superseded_by']}" if d.get("superseded_by") else "") + more)
    extra = []
    for cid in top:
        for key in ("superseded_by", "supersedes"):
            for n in [x.strip() for x in docs[cid].get(key, "").split(",") if x.strip()]:
                if n in docs and n not in seen:
                    seen.add(n)
                    extra.append(f"  +[{n}] ({docs[n]['status']}) {docs[n]['statement']} | source={docs[n].get('source','-')} (取代鏈鄰居 of {cid})")
    out = "\n".join(lines + (["-- 取代鏈鄰居 --"] + extra if extra else []))
    if os.environ.get("KBX_MODE") == "file":
        import hashlib; p = HERE / f"results-{hashlib.md5(q.encode()).hexdigest()[:8]}.txt"
        p.write_text(out, encoding="utf-8")
        print(f"已寫入 {len(top)} 筆結果(另有 {len(extra)} 筆鄰居)到 {p}。請用 Read 讀取。")
    else:
        print(out)


if __name__ == "__main__":
    main()
