"""E1:v1 搜尋(BM25 雙字 + 別名 + 取代鏈鄰居 + 折疊)在 L 規模(約 1,530 條 claim)的離線檢索成績。

對照第四輪同一批 43 題。指標:hit@5(前 5 名含任一 gold 現行 claim)、hit@5+鄰居(前 5 名加上取代鏈鄰居)、
M 類 recall@8。stale 類(N/S/G6-8/E3-5):另算「前 8 名裡 stale claim 排在現行 claim 前面」的比例(誤導風險)。
用法:KB_ROOT 指向 build_l.py 的輸出;python experiments/e1_retrieval.py <kb_root>
"""
import os, sys
from collections import defaultdict
from pathlib import Path

root = Path(sys.argv[1])
os.environ["KB_ROOT"] = str(root)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent.parent / "lab4"))
import kb  # noqa: E402
import queries  # noqa: E402

claims = kb.load_claims()
ids = list(claims)
by, sup = kb.derive(claims)


def search(q, k):
    ranked = kb.rank_claims(claims, ids, q)
    top, groups = [], {}
    for i, _ in ranked:
        c = claims[ids[i]]
        key = kb.norm_template(c) if kb.spec(c) else c["id"]
        if key in groups:
            groups[key].append(c["id"])
            continue
        groups[key] = [c["id"]]
        top.append(c["id"])
        if len(top) >= k:
            break
    nb = []
    for cid in top:
        c = claims[cid]
        for n in c["supersedes"] + by.get(cid, []):
            if n in claims and n not in top and n not in nb:
                nb.append(n)
    return top, nb


rows = defaultdict(list)
for qid, typ, text, gold, stale in queries.Q:
    top5, nb5 = search(text, 5)
    top8, nb8 = search(text, 8)
    hit5 = bool(set(top5) & gold)
    hit5n = bool((set(top5) | set(nb5)) & gold)
    rec8 = len((set(top8) | set(nb8)) & gold) / len(gold)
    misl = None
    if stale:  # 前 8 名中第一個 gold 或 stale 是 stale 嗎?
        for cid in top8:
            if cid in gold:
                misl = False
                break
            if cid in stale:
                misl = True
                break
    rows[typ].append((hit5, hit5n, rec8, misl))

print(f"KB={root.name} claims={len(claims)}")
print(f"{'type':4} {'n':>2} {'hit@5':>6} {'hit@5+nb':>9} {'recall@8+nb':>12} {'stale先於現行':>12}")
tot = [0, 0, 0, 0]
for t in "LGNSMEH":
    r = rows[t]
    n = len(r)
    ms = [x[3] for x in r if x[3] is not None]
    print(f"{t:4} {n:>2} {sum(x[0] for x in r) / n:6.2f} {sum(x[1] for x in r) / n:9.2f} {sum(x[2] for x in r) / n:12.2f} " + (f"{sum(ms)}/{len(ms)}" if ms else "-"))
    tot[0] += sum(x[0] for x in r); tot[1] += sum(x[1] for x in r); tot[2] += n
print(f"ALL  {tot[2]:>2} {tot[0] / tot[2]:6.2f} {tot[1] / tot[2]:9.2f}")
