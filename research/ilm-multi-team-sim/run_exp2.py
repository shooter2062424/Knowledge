"""實驗 2:會破壞相容的語意變更(單位/縮放/極性/索引基底/改名),比較四種做法。

  A naive      : producer 直接改(團隊只改自己的 spec)
  B expand/contract + AST manifest 找讀取者,manifest 顯示沒人讀了就移除舊欄位
  C B + 移除前再跑契約測試與端到端 replay,被擋就不移除
  D expand/contract + runtime access trace(執行期記錄誰讀了舊欄位,抓得到動態 key)

用法: python run_exp2.py <instances> <targets_per_instance> <out.json>
"""
from __future__ import annotations

import copy
import json
import random
import sys
from typing import Any

import ilm_sim as S


def rebuild(inst: S.Instance) -> None:
    """依 inst.mods 目前的 uses 重新產生所有 consumer 原始碼、handler 與 manifest。"""
    inst.sources.clear()
    inst.handlers.clear()
    for c, cm in inst.mods.items():
        for m, uses in cm["uses"].items():
            src = S.gen_source(inst, c, m, uses)
            inst.sources[(c, m)] = src
            ns: dict[str, Any] = {}
            exec(compile(src, f"<{c}.{m}>", "exec"), ns)
            inst.handlers[(c, m)] = ns["handle"]
    inst.manifest = S.extract_manifest(inst)


def make_use(u: dict[str, Any], f2: str, fs2: dict[str, Any], rng: random.Random) -> dict[str, Any]:
    """consumer 遷移:改讀新欄位 f2,常數依新規格重算。"""
    k = u["kind"]
    if k == "time":
        cs: dict[str, Any] = {"factor": S.UNIT_US[fs2["unit"]], "cap": fs2["hi"]}
    elif k == "index":
        cs = {"base": fs2["base"], "n": fs2["hi"] - fs2["base"] + 1}
    elif k == "enum":
        cs = {"map": {v: s for s, v in fs2["map"].items()}, "strict": u["consts"]["strict"]}
    elif k == "scaled":
        cs = {"scale": fs2["scale"], "cap": fs2["hi"]}
    else:
        cs = {"true_val": fs2["true_val"]}
    cs["default"] = fs2["default"]
    u2 = {"f": f2, "kind": k, "consts": cs, "relay_to": None, "dyn": u["dyn"]}
    u2["declared"] = S.declare(u2, fs2, rng, 0.0)
    return u2


def derive_new_spec(fs: dict[str, Any]) -> dict[str, Any]:
    """依欄位種類做『語意變更』,回傳新欄位規格;改名則語意不變。"""
    n = copy.deepcopy(fs)
    k = fs["kind"]
    if k == "time":
        n["unit"] = "us" if fs["unit"] != "us" else "ms"
        ratio = S.UNIT_US[fs["unit"]] // S.UNIT_US[n["unit"]] if S.UNIT_US[fs["unit"]] >= S.UNIT_US[n["unit"]] else 1
        if S.UNIT_US[fs["unit"]] >= S.UNIT_US[n["unit"]]:
            n["lo"], n["hi"], n["default"] = fs["lo"] * ratio, fs["hi"] * ratio, fs["default"] * ratio
        else:
            r2 = S.UNIT_US[n["unit"]] // S.UNIT_US[fs["unit"]]
            n["lo"], n["hi"], n["default"] = fs["lo"] // r2, max(1, fs["hi"] // r2), fs["default"] // r2
    elif k == "scaled":
        n["scale"], n["hi"] = fs["scale"] / 2, fs["hi"] * 2
    elif k == "flag":
        n["true_val"] = 1 - fs["true_val"]
    elif k == "index":
        d = 1 if fs["base"] == 0 else -1
        for key in ("base", "lo", "hi", "default"):
            n[key] += d
    return n


def trial(inst0: S.Instance, rng: random.Random) -> dict[str, Any] | None:
    """對一個系統隨機選目標欄位,跑 A/B/C/D 四種做法。"""
    cands = []
    for m, spec in inst0.registry.items():
        if spec["derived"] or spec["positional"]:
            continue
        for f in spec["fields"]:
            users = [(c, u) for c, cm in inst0.mods.items() for u in cm["uses"].get(m, []) if u["f"] == f]
            if users and not any(u["relay_to"] for _, u in users):
                cands.append((m, f))
    if not cands:
        return None
    m, f = rng.choice(cands)
    fs = inst0.registry[m]["fields"][f]
    f2 = f + "_n"
    rename = fs["kind"] == "enum" or rng.random() < 0.3  # enum 只示範改名;其餘 30% 改名、70% 語意變更
    fs2 = copy.deepcopy(fs) if rename else derive_new_spec(fs)
    sd = rng.randint(1, 10**6)
    res: dict[str, Any] = {"kind": fs["kind"], "op": "rename" if rename else "semantic", "readers": 0,
                           "strict_relaxed": 0}

    # A:直接改
    reg_a = copy.deepcopy(inst0.registry)
    if rename:
        reg_a[m]["fields"] = {(f2 if k == f else k): v for k, v in reg_a[m]["fields"].items()}
    else:
        reg_a[m]["fields"][f] = copy.deepcopy(fs2)
    res["A_broken"] = bool(S.truth_fails(inst0, reg_a, sd))

    # 共同前置:放寬 strict(tolerant reader)、expand
    base = copy.deepcopy(inst0)
    for c, cm in base.mods.items():
        if m in cm["uses"] and cm["strict"]:
            cm["strict"] = False
            res["strict_relaxed"] += 1
    rebuild(base)
    reg_e = copy.deepcopy(base.registry)
    reg_e[m]["fields"][f2] = copy.deepcopy(fs2)
    base.registry = copy.deepcopy(reg_e)  # 以 expand 後的規格為 baseline,供 known_syms 等使用
    res["expand_ok"] = not S.truth_fails(base, reg_e, sd)
    res["readers"] = sum(1 for cm in base.mods.values() for u in cm["uses"].get(m, []) if u["f"] == f)

    # runtime trace:誰在 expand 後的系統裡讀了 f(含動態 key)
    rec: list = []
    S.run_system(base, reg_e, "dense", 40, sd, recorder=rec)
    rt_readers = {c for c, mm, k in rec if mm == m and k == f}
    ast_readers = {c for (c, mm), mf in base.manifest.items() if mm == m and f in mf["reads"]}
    res["dyn_hidden"] = len(rt_readers - ast_readers)

    def migrate(who: set[str]) -> S.Instance:
        inst = copy.deepcopy(base)
        for c in who:
            uses = inst.mods[c]["uses"][m]
            inst.mods[c]["uses"][m] = [make_use(u, f2, fs2, rng) if u["f"] == f else u for u in uses]
        rebuild(inst)
        return inst

    reg_c = copy.deepcopy(reg_e)
    del reg_c[m]["fields"][f]
    for name, who in (("B", ast_readers), ("D", rt_readers)):
        inst = migrate(who)
        res[name + "_mid_ok"] = not S.truth_fails(inst, reg_e, sd)  # 兩欄並存期間必須無事
        visible_left = any(f in mf["reads"] for (c, mm), mf in inst.manifest.items() if mm == m)
        rec2: list = []
        S.run_system(inst, reg_e, "dense", 40, sd, recorder=rec2)
        runtime_left = any(mm == m and k == f for c, mm, k in rec2)
        broken = bool(S.truth_fails(inst, reg_c, sd))
        if name == "B":
            res["B_allowed"] = not visible_left
            res["B_broken"] = (not visible_left) and broken
            blocked = bool(S.g3_contract(inst, reg_c, sd) or S.g4_e2e(inst, reg_c, sd))
            res["C_broken"] = (not visible_left) and broken and not blocked
            res["C_blocked_safe"] = (not visible_left) and blocked and not broken
            res["C_blocked_any"] = (not visible_left) and blocked
        else:
            res["D_allowed"] = not runtime_left
            res["D_broken"] = (not runtime_left) and broken
    return res


if __name__ == "__main__":
    n_inst, n_t, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rows = []
    for i in range(n_inst):
        inst = S.Instance(5000 + i, S.DEFAULT_CFG)
        rng = random.Random(9000 + i)
        for _ in range(n_t):
            r = trial(inst, rng)
            if r:
                r["inst"] = i
                rows.append(r)
    n = len(rows)
    agg = {"n": n}
    for k in ("A_broken", "B_broken", "C_broken", "D_broken", "C_blocked_any", "expand_ok", "B_mid_ok", "D_mid_ok"):
        agg[k] = sum(bool(r.get(k)) for r in rows)
    agg["strict_relaxed_total"] = sum(r["strict_relaxed"] for r in rows)
    agg["dyn_hidden_cases"] = sum(1 for r in rows if r["dyn_hidden"] > 0)
    agg["readers_avg"] = sum(r["readers"] for r in rows) / max(1, n)
    by: dict[str, dict[str, int]] = {}
    for r in rows:
        d = by.setdefault(r["kind"], {"n": 0, "A": 0, "B": 0, "C": 0, "D": 0})
        d["n"] += 1
        d["A"] += r["A_broken"]
        d["B"] += r["B_broken"]
        d["C"] += r["C_broken"]
        d["D"] += r["D_broken"]
    agg["by_kind"] = by
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"summary": agg, "rows": rows}, fh, ensure_ascii=False)
    print(json.dumps(agg, ensure_ascii=False, indent=1))
