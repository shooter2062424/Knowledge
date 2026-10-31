"""規格與程式碼一致性檢查(drift gate)。

比對項目:
 1. 外部規格參數 vs 程式碼同名常數(值不同 = 偏離)。
 2. 外部規格條目沒有任何程式碼/測試追溯(未實作或未驗證)。
 3. 程式碼標註引用了不存在的規格 ID(殘留)。
 4. 公開函式完全沒標註(需人工歸類:外部/內部/基礎設施)。

用法:python tools/check_drift.py <pkg> <Release>   (有偏離則 exit 1)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from specutil import effective_params, load_json, param_owner  # noqa: E402


def check(pkg: str, release: str) -> dict[str, list[str]]:
    ext = load_json(ROOT / "specs" / "ext_spec.json")
    internal = load_json(ROOT / "specs" / "internal_spec.json")
    data = json.loads((ROOT / "out" / f"extracted_{pkg}.json").read_text(encoding="utf-8"))
    params, owner = effective_params(ext, release), param_owner(ext, release)
    code = {c["name"]: c for c in data["constants"]}
    problems: dict[str, list[str]] = {"mismatch": [], "missing_const": [], "uncovered_req": [], "stale_tag": [],
                                      "untraced_func": []}
    for name, want in params.items():
        c = code.get(name)
        if c is None:
            problems["missing_const"].append(f"{owner[name]}.{name} = {want}(程式碼沒有同名常數)")
        elif c["value"] != want:
            problems["mismatch"].append(f"{owner[name]}.{name}: 規格={want} 程式碼={c['value']}")
    traced = {t for c in data["constants"] for t in c["tags"]} | {t for f in data["functions"] for t in f["traces"]}
    tested = {i for t in data["tests"] for i in t["covers"]}
    known = {r["id"] for r in ext["requirements"]
             if any(__import__("specutil").rel_num(k) <= __import__("specutil").rel_num(release)
                    for k in r["by_release"])} | {d["id"] for d in internal["decisions"]}
    for rid in sorted(known):
        if rid.startswith("R-") and rid not in traced:
            problems["uncovered_req"].append(f"{rid} 無程式碼追溯")
        elif rid.startswith("R-") and rid not in tested:
            problems["uncovered_req"].append(f"{rid} 有程式碼但沒有任何測試 covers")
    all_ids = {r["id"] for r in ext["requirements"]} | {d["id"] for d in internal["decisions"]}
    for t in sorted(traced - all_ids):
        problems["stale_tag"].append(f"{t}(規格中不存在)")
    problems["untraced_func"] = [f"{f['module']}.{f['name']}" for f in data["functions"]
                                 if f["public"] and not f["traces"] and not f["infra"]]
    return problems


if __name__ == "__main__":
    pkg, release = sys.argv[1], sys.argv[2]
    p = check(pkg, release)
    labels = {"mismatch": "❌ 值偏離", "missing_const": "❌ 缺常數", "uncovered_req": "⚠️ 未覆蓋條目",
              "stale_tag": "⚠️ 殘留標註", "untraced_func": "⚠️ 未標註函式"}
    for k, items in p.items():
        for i in items:
            print(f"{labels[k]}: {i}")
    hard = len(p["mismatch"]) + len(p["missing_const"]) + len(p["uncovered_req"])
    print(f"drift 結果:硬性問題 {hard} 項,待人工 {len(p['stale_tag']) + len(p['untraced_func'])} 項")
    sys.exit(1 if hard else 0)
