"""檢索模式 × 規模 × 題型的離線評測(不呼叫 LLM;別名與查詢擴充已由 gen_llm.py 預先產生)。

方法:grep(單次字面,以 token 命中數排序)、bm25(kb.tok 單字+雙字)、bm25j(jieba)、vec(bge-small-zh)、hyb(RRF)。
變體:+alias(入庫端擴充)、+qx(查詢端擴充)。
"""
from __future__ import annotations
import json, math, re, sys, pickle, os
from collections import Counter
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / ".." / ".." / ".." / ".." / ".." / ".." / "Temp"))
import corpus, queries
import jieba
jieba.setLogLevel(60)

OUT = Path(__file__).parent / "out"
ALIAS = json.loads((OUT / "aliases.json").read_text(encoding="utf-8"))
QX = json.loads((OUT / "qexp.json").read_text(encoding="utf-8"))
PYLIB = os.environ.get("KBX_PYLIB")
if PYLIB:
    sys.path.insert(0, PYLIB)


def tok_kb(s: str) -> list[str]:
    return corpus.kb.tok(s)


def tok_b(s: str) -> list[str]:
    """ASCII 詞 + CJK 雙字(去掉單字,避免「的、不、路」之類高頻單字灌分)。"""
    return [t for t in corpus.kb.tok(s) if len(t) >= 2 or re.match(r"[a-z0-9]", t)]


def tok_j(s: str) -> list[str]:
    s = s.lower()
    out = re.findall(r"[a-z0-9_.+]+", s)
    out += [w for w in jieba.cut_for_search(re.sub(r"[a-z0-9_.+\s]+", " ", s)) if w.strip() and re.search(r"[一-鿿]", w)]
    return out


class BM25:
    def __init__(self, texts, tokf, k1=1.5, b=0.75):
        self.tokf, self.k1, self.b = tokf, k1, b
        self.toks = [Counter(tokf(t)) for t in texts]
        self.len = np.array([sum(c.values()) for c in self.toks], float)
        self.avg = self.len.mean()
        df = Counter(t for c in self.toks for t in c)
        N = len(texts)
        self.idf = {t: math.log(1 + (N - n + .5) / (n + .5)) for t, n in df.items()}
        self.inv = {}
        for i, c in enumerate(self.toks):
            for t in c:
                self.inv.setdefault(t, []).append(i)

    def coverage(self, q: str) -> np.ndarray:
        """每份文件命中的不同 query token 佔比(coordination factor)。"""
        qt = set(self.tokf(q))
        c = np.zeros(len(self.toks))
        for t in qt:
            for i in self.inv.get(t, ()):
                c[i] += 1
        return c / max(1, len(qt))

    def score(self, q: str) -> np.ndarray:
        s = np.zeros(len(self.toks))
        for t in set(self.tokf(q)):
            for i in self.inv.get(t, ()):
                tf = self.toks[i][t]
                s[i] += self.idf[t] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg))
        return s


def grep_scores(texts, q):
    """單次字面 grep:query 的 ASCII 詞與 CJK 雙字(>=2)是否出現在文字裡,命中不同 token 數排序(無 idf、無長度正規化)。"""
    qt = {t for t in tok_kb(q) if len(t) >= 2}
    low = [t.lower() for t in texts]
    return np.array([sum(1 for t in qt if t in x) for x in low], float)


# 注意:pickle 只用於本機自己寫出的嵌入快取(非外部資料),無反序列化風險。
_emb_cache_f = OUT / "emb_cache.pkl"
_emb_cache = pickle.loads(_emb_cache_f.read_bytes()) if _emb_cache_f.exists() else {}
_model = None


def embed(texts):
    global _model
    miss = [t for t in dict.fromkeys(texts) if t not in _emb_cache]
    if miss:
        if _model is None:
            from fastembed import TextEmbedding
            _model = TextEmbedding("BAAI/bge-small-zh-v1.5")
        v = np.array(list(_model.embed(miss)))
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        for t, x in zip(miss, v):
            _emb_cache[t] = x
        _emb_cache_f.write_bytes(pickle.dumps(_emb_cache))
    return np.array([_emb_cache[t] for t in texts])


def rrf(*score_arrays, k=60, depth=100):
    """Reciprocal Rank Fusion:每個排序只取前 depth 名且分數>0 者貢獻 1/(k+rank)。"""
    fused = np.zeros(len(score_arrays[0]))
    for s in score_arrays:
        order = np.argsort(-s, kind="stable")[:depth]
        for r, i in enumerate(order):
            if s[i] > 0:
                fused[i] += 1.0 / (k + r + 1)
    return fused


class Index:
    def __init__(self, units, with_alias: bool):
        self.units = units
        texts = [u["text"] + (" " + u["alias"] if with_alias and u["alias"] else "") for u in units]
        self.texts = texts
        self.bm = BM25(texts, tok_kb)
        self.bj = BM25(texts, tok_j)
        self.bb = BM25(texts, tok_b)
        self.E = embed(texts)

    def scores(self, method: str, q: str, qx: str | None = None):
        qq = q + (" " + qx if qx else "")
        if method == "grep":
            return grep_scores(self.texts, qq)
        if method == "bm25":
            return self.bm.score(qq)
        if method == "bm25c":
            return self.bb.score(qq) * self.bb.coverage(qq)
        if method == "hybc":
            return rrf(self.bb.score(qq) * self.bb.coverage(qq), self.E @ embed([qq])[0])
        if method == "bm25b":
            return self.bb.score(qq)
        if method == "hybb":
            return rrf(self.bb.score(qq), self.E @ embed([qq])[0])
        if method == "bm25j":
            return self.bj.score(qq)
        if method == "vec":
            return self.E @ embed([qq])[0]
        if method == "hyb":
            return rrf(self.bm.score(qq), self.E @ embed([qq])[0])
        if method == "hybj":
            return rrf(self.bj.score(qq), self.E @ embed([qq])[0])
        raise ValueError(method)


def gold_expand(units, gold):
    srcs = {u["uid"]: u.get("source") for u in units if u["kind"] == "claim"}
    g = set(gold) | {srcs[c] for c in gold if srcs.get(c)}
    return g


def ranks(idx: Index, sc: np.ndarray):
    order = np.argsort(-sc, kind="stable")
    return [idx.units[i]["uid"] for i in order if sc[i] > 0]


def metrics(rk, gold_units, gold_claims, stale):
    def first(S):
        for i, u in enumerate(rk):
            if u in S:
                return i + 1
        return None
    f = first(gold_units)
    top5 = rk[:5]
    return dict(h1=int(f == 1), h5=int(f is not None and f <= 5), mrr=(1 / f if f else 0.0),
                rec8=len(set(rk[:8]) & set(gold_claims)) / len(gold_claims), stale_first=int(bool(stale) and first(stale) == 1 and (f is None or f > 1)))


def run(scales=("S", "M", "L"), configs=None):
    configs = configs or [(m, a, x) for m in ("grep", "bm25", "bm25b", "bm25j", "vec", "hyb", "hybb", "hybj") for a in (0, 1) for x in (0, 1)
                          if not (m == "grep" and (a or x)) and not (m == "vec" and x)]
    res = {}
    for sc in scales:
        u0 = corpus.build(sc, ALIAS)
        idx = {0: Index(u0, False), 1: Index(u0, True)}
        for (m, al, qx) in configs:
            for qid, qt, qtext, gold, stale in queries.Q:
                s = idx[al].scores(m, qtext, QX[qid] if qx else None)
                rk = ranks(idx[al], s)
                met = metrics(rk, gold_expand(u0, gold), gold, stale)
                res[(sc, m, al, qx, qid)] = (qt, met, rk[:8])
        print("done scale", sc, len(u0), flush=True)
    return res


def table(res):
    import collections
    agg = collections.defaultdict(lambda: collections.defaultdict(list))
    for (sc, m, al, qx, qid), (qt, met, _) in res.items():
        agg[(sc, m, al, qx)][qt].append(met)
        agg[(sc, m, al, qx)]["ALL"].append(met)
    return agg


if __name__ == "__main__":
    res = run()
    pickle.dump(res, open(OUT / "res.pkl", "wb"))
    agg = table(res)
    types = ["L", "G", "N", "S", "M", "E", "H", "ALL"]
    for key in sorted(agg):
        row = []
        for t in types:
            ms = agg[key].get(t, [])
            if ms:
                row.append(f"{t}:{np.mean([x['h5'] for x in ms]):.2f}")
        print(key, " ".join(row), f"MRR={np.mean([x['mrr'] for x in agg[key]['ALL']]):.2f}")
