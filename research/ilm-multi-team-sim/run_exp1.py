"""實驗 1:大量隨機系統 × 隨機 producer 端變更,量測各閘門抓到「別的團隊會壞」的能力。

用法: python run_exp1.py <instances> <mutations_per_instance> <out.json> [stale=0.15 dyn=0.10 test=0.85 ...]
"""
from __future__ import annotations

import copy
import json
import random
import sys
from collections import defaultdict

import ilm_sim as S

GATES = ["G0_own", "G1_schema", "G2_manifest", "G2d_dataflow", "G3_contract", "G4_e2e", "FULL"]


def run(n_inst: int, n_mut: int, cfg: dict, seed0: int = 1000) -> list[dict]:
    """跑 n_inst 個系統、每個 n_mut 次變更,回傳逐次記錄。"""
    rows = []
    for i in range(n_inst):
        inst = S.Instance(seed0 + i, cfg)
        rng = random.Random(seed0 * 7 + i)
        for j in range(n_mut):
            for _ in range(20):
                op = rng.choice(S.OPS)
                reg = copy.deepcopy(inst.registry)
                if S.mutate(reg, rng, op):
                    break
            else:
                continue
            sd = rng.randint(1, 10**6)
            truth = S.truth_fails(inst, reg, sd)
            tm = {c for c, _, _ in truth}
            g1 = S.g1_schema_diff(inst, reg)
            g2 = S.g2_manifest(inst, reg, False)
            g2d = S.g2_manifest(inst, reg, True)
            g3 = S.g3_contract(inst, reg, sd)
            g4 = S.g4_e2e(inst, reg, sd)
            full = g2d | g3 | g4
            rows.append({"inst": i, "op": op, "broken": bool(truth), "truth_mods": sorted(tm),
                         "flag": {"G0_own": False, "G1_schema": g1, "G2_manifest": bool(g2),
                                  "G2d_dataflow": bool(g2d), "G3_contract": bool(g3),
                                  "G4_e2e": bool(g4), "FULL": bool(full)},
                         "mods": {"G2d_dataflow": sorted(g2d), "FULL": sorted(full)}})
    return rows


def summarize(rows: list[dict]) -> dict:
    """彙整:整體與分算子的 recall / 誤報率 / 模組層級通知精準度。"""
    out: dict = {"n": len(rows), "broken": sum(r["broken"] for r in rows), "gates": {}, "by_op": {}}
    broken = [r for r in rows if r["broken"]]
    safe = [r for r in rows if not r["broken"]]
    for g in GATES:
        tp = sum(r["flag"][g] for r in broken)
        fp = sum(r["flag"][g] for r in safe)
        out["gates"][g] = {"recall": tp / max(1, len(broken)), "tp": tp, "fn": len(broken) - tp,
                           "fp": fp, "fp_rate": fp / max(1, len(safe)), "safe_n": len(safe)}
    for g in ("G2d_dataflow", "FULL"):
        tp = fp = fn = 0
        for r in rows:
            t, f = set(r["truth_mods"]), set(r["mods"][g])
            tp += len(t & f)
            fp += len(f - t)
            fn += len(t - f)
        out["gates"][g].update(mod_precision=tp / max(1, tp + fp), mod_recall=tp / max(1, tp + fn))
    by = defaultdict(list)
    for r in rows:
        by[r["op"]].append(r)
    for op, rs in by.items():
        b = [r for r in rs if r["broken"]]
        d = {"n": len(rs), "broken": len(b)}
        for g in GATES:
            d[g + "_tp"] = sum(r["flag"][g] for r in b)
            d[g + "_fp"] = sum(r["flag"][g] for r in rs if not r["broken"])
        out["by_op"][op] = d
    return out


if __name__ == "__main__":
    n_inst, n_mut, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    cfg = dict(S.DEFAULT_CFG)
    for a in sys.argv[4:]:
        k, v = a.split("=")
        cfg[{"stale": "stale_rate", "dyn": "dyn_rate", "test": "test_rate", "strict": "strict_rate",
             "relay": "relay_rate", "ttest": "timing_test_rate"}[k]] = float(v)
    rows = run(n_inst, n_mut, cfg)
    summ = summarize(rows)
    summ["cfg"] = cfg
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"summary": summ, "rows": rows}, fh, ensure_ascii=False)
    print(f"mutations={summ['n']} truly_broken={summ['broken']} ({summ['broken'] / summ['n']:.0%})")
    for g in GATES:
        d = summ["gates"][g]
        extra = f" mod_prec={d['mod_precision']:.2f} mod_rec={d['mod_recall']:.2f}" if "mod_precision" in d else ""
        print(f"{g:14s} recall={d['recall']:.3f} ({d['tp']}/{d['tp'] + d['fn']})  FP={d['fp']}/{d['safe_n']} ({d['fp_rate']:.1%}){extra}")
