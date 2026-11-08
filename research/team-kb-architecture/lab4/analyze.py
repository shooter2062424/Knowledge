"""從 out/res.pkl 彙整表格,並測試「過期 claim 處理策略」(P0 原排序 / P1 隱藏 / P2 降權 / P3 原排序+展開 supersedes 鄰居)。"""
import pickle, sys, os
from collections import defaultdict
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
import corpus, queries, evalret as ev

OUT = Path(__file__).parent / "out"
res = pickle.load(open(OUT / "res.pkl", "rb"))  # 本機自己產生的結果檔,非外部資料
NAME = {(m, a, x): f"{m}{'+alias' if a else ''}{'+qx' if x else ''}" for (_, m, a, x, _) in res}


def agg(sc, m, a, x, types=None, key="h5"):
    v = [r[1][key] for (s, mm, aa, xx, qid), r in res.items() if (s, mm, aa, xx) == (sc, m, a, x) and (types is None or r[0] in types)]
    return float(np.mean(v)) if v else float("nan"), len(v)


lines = []
P = lines.append
for sc in "SML":
    P(f"\n### 規模 {sc}")
    P("| 方法 | 全部 hit@5 | MRR | L 字面 | G 落差 | E 英文 | N+S 現況 | M recall@8 | H 歷史 | stale-first(N+S+G6~8) |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    keys = sorted({(m, a, x) for (s, m, a, x, _) in res if s == sc}, key=lambda k: (k[0], k[1], k[2]))
    for (m, a, x) in keys:
        allv, _ = agg(sc, m, a, x)
        mrr, _ = agg(sc, m, a, x, key="mrr")
        cells = [agg(sc, m, a, x, t)[0] for t in (["L"], ["G"], ["E"], ["N", "S"])]
        rec = agg(sc, m, a, x, ["M"], key="rec8")[0]
        h = agg(sc, m, a, x, ["H"])[0]
        sf = agg(sc, m, a, x, ["N", "S"], key="stale_first")[0]
        P(f"| {NAME[(m,a,x)]} | {allv:.2f} | {mrr:.2f} | " + " | ".join(f"{c:.2f}" for c in cells) + f" | {rec:.2f} | {h:.2f} | {sf:.2f} |")

# 配對比較:L 規模,每題 hit@5
def per_q(sc, cfg, key="h5"):
    return {qid: r[1][key] for (s, m, a, x, qid), r in res.items() if (s, m, a, x) == (sc,) + cfg}
P("\n### 配對比較(規模 L,43 題,hit@5;只列 A 贏、B 贏的題數)")
pairs = [(("bm25", 0, 0), ("bm25b", 0, 0)), (("bm25b", 0, 0), ("grep", 0, 0)), (("hyb", 0, 0), ("bm25", 0, 0)), (("hyb", 1, 1), ("hyb", 0, 0)),
         (("hyb", 1, 0), ("hyb", 0, 1)), (("hybb", 1, 1), ("bm25b", 1, 1)), (("hybb", 1, 0), ("bm25b", 1, 0)), (("vec", 1, 0), ("vec", 0, 0))]
for A, B in pairs:
    a, b = per_q("L", A), per_q("L", B)
    aw = [q for q in a if a[q] > b[q]]
    bw = [q for q in a if b[q] > a[q]]
    P(f"- {NAME[A]} vs {NAME[B]}:A 贏 {len(aw)}({','.join(aw)}),B 贏 {len(bw)}({','.join(bw)})")

# 過期策略
P("\n### 過期 claim 策略(規模 L;N+S 共 11 題;method=hybb+alias,top5 顯示)")
ALIAS = ev.ALIAS
units = corpus.build("L", ALIAS)
idx = ev.Index(units, True)
byid = {u["uid"]: u for u in units}
fused_cfg = lambda q: idx.scores("hybb", q)
pol = defaultdict(lambda: defaultdict(list))
for qid, qt, qtext, gold, stale in queries.Q:
    if qt not in ("N", "S", "H", "G") or not stale and qt != "H":
        continue
    sc = fused_cfg(qtext)
    rk = ev.ranks(idx, sc)
    def cur_in(lst):
        return int(any(u in gold for u in lst))
    # P0 原排序
    p0 = rk[:5]
    # P1 隱藏 superseded
    p1 = [u for u in rk if byid[u]["status"] != "superseded"][:5]
    # P2 降權(superseded 分數 *0.5)
    order = sorted(rk, key=lambda u: -(sc[units.index(byid[u])] * (0.5 if byid[u]["status"] == "superseded" else 1)))
    p2 = order[:5]
    # P3 原排序 + 展開鄰居(supersedes 雙向),鄰居附在後面
    p3 = list(p0)
    for u in p0:
        for n in (byid[u].get("sup_by") or []) + (byid[u].get("sup") or []):
            if n not in p3:
                p3.append(n)
    # 是否同時看到過期的(歷史題需要)
    for name, lst in (("P0 原排序", p0), ("P1 隱藏過期", p1), ("P2 降權", p2), ("P3 原排序+展開", p3)):
        pol[name][qt].append((cur_in(lst), int(any(u in stale for u in lst)) if stale else None, qid))
for name, d in pol.items():
    ns = d["N"] + d["S"]
    P(f"- {name}:N+S 取得現行 claim {sum(x[0] for x in ns)}/{len(ns)};其中 N {sum(x[0] for x in d['N'])}/{len(d['N'])}、S {sum(x[0] for x in d['S'])}/{len(d['S'])};"
      f"G6-G8 取得現行 {sum(x[0] for x in d['G'] if x[2] in ('G6','G7','G8'))}/3;同時看到被取代版本(可警示)N+S {sum(x[1] for x in ns)}/{len(ns)}")
    miss = [x[2] for x in ns if not x[0]]
    P(f"  - 沒取得現行的題:{miss}")
(OUT / "summary.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
