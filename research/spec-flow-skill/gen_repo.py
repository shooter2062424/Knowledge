"""產生玩具專案(規格 + 程式 + 測試 + 凍結 golden + 契約),供 specflow 工具與 agent 實驗使用。

專案內容全是隨機玩具,不代表任何真實系統。結構:
    specs/requirements.md   R-*(外部需求,帶常數)與 D-*(內部決策,帶 owner 與受保護常數)
    specs/contracts.json    模組間介面契約(欄位含單位/縮放等語意屬性)
    src/mod_*.py            每個需求一個常數與一個函式,帶 @spec;契約欄位用 @uses
    tests/test_mod_*.py     每個需求的邊界測試,帶 @covers
    tests/golden/vectors.json  凍結的輸出基準(受保護)
    specflow.json
所有輸出由 seed 決定,可重現。標準函式庫 unittest 即可執行,不需 pytest。
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
from pathlib import Path

WORDS = ["neighbor", "retry", "window", "burst", "queue", "beam", "timer", "slot", "cell", "grant", "frame", "paging"]


def gen(root: Path, seed: int, n_mod: int = 3, per_mod: int = 3) -> dict:
    """在 ``root`` 產生專案並回傳描述(需求清單、常數、契約),供實驗評分用。"""
    rnd = random.Random(seed)
    for d in ["specs", "src", "tests/golden"]:
        (root / d).mkdir(parents=True, exist_ok=True)
    reqs: list[dict] = []
    spec_lines = ["# 需求與決策\n"]
    golden: dict[str, list] = {}
    prev_id = None
    for m in range(1, n_mod + 1):
        mod = f"mod_{m}"
        code = [f'"""模組 {mod}(玩具)。"""\n']
        tests = ["import json\nimport unittest\nfrom pathlib import Path\n", f"import sys\nsys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))\n",
                 f"import {mod} as M\n\nGOLD = json.loads((Path(__file__).parent / 'golden' / 'vectors.json').read_text())\n\n\nclass T(unittest.TestCase):\n"]
        for j in range(1, per_mod + 1):
            rid = f"R-M{m}-{j:02d}"
            word = rnd.choice(WORDS)
            limit = rnd.choice([4, 8, 12, 16, 20, 32])
            cname = f"M{m}_{word.upper()}_{j}_LIMIT"
            fn = f"accept_{word}_{j}"
            dep = f"depends: {prev_id}\n" if prev_id and rnd.random() < 0.5 else ""
            spec_lines.append(f"## {rid} · {word} 上限\n- kind: external\n- owner: team-{m}\n- status: active\n"
                              f"- constants: {cname}={limit}\n" + (f"- {dep}" if dep else "") +
                              f"\n系統 SHALL 最多接受 {cname} 筆 {word};超過的請求 SHALL 被拒絕。\n")
            code.append(f"{cname} = {limit}\n\n\ndef {fn}(count):\n    # @spec {rid}\n    return 0 <= count <= {cname}\n")
            tests.append(f"    def test_{rid.replace('-', '_').lower()}(self):\n        # @covers {rid}\n"
                         f"        self.assertTrue(M.{fn}(M.{cname}))\n        self.assertFalse(M.{fn}(M.{cname} + 1))\n")
            gold_in = [0, limit - 1, limit, limit + 1]
            golden[f"{mod}.{fn}"] = [[x, 0 <= x <= limit] for x in gold_in]
            reqs.append({"id": rid, "module": mod, "const": cname, "value": limit, "fn": fn, "word": word})
            prev_id = rid
        # 決策:每模組一個預算
        did = f"D-M{m}"
        base, per = rnd.choice([3, 5]), rnd.choice([1, 2, 3])
        top = max(r["value"] for r in reqs if r["module"] == mod)
        budget = base + per * top + rnd.choice([0, 3])
        bname = f"M{m}_BUDGET_US"
        spec_lines.append(f"## {did} · 處理預算\n- kind: decision\n- owner: team-hw\n- status: active\n"
                          f"- depends: {', '.join(r['id'] for r in reqs if r['module'] == mod)}\n- constants: {bname}\n\n"
                          f"最壞情況處理成本 = {base} + {per}×(最大筆數) µs 必須 ≤ {bname}。{bname} 由硬體小組擁有,"
                          f"不得為了讓測試通過自行調整。\n")
        code.append(f"{bname} = {budget}\nBASE_US = {base}\nPER_US = {per}\n\n\n"
                    f"def worst_cost():\n    # @spec {did}\n    cap = max({', '.join(r['const'] for r in reqs if r['module'] == mod)})\n"
                    f"    return BASE_US + PER_US * cap\n")
        tests.append(f"    def test_{did.replace('-', '_').lower()}(self):\n        # @covers {did}\n"
                     f"        self.assertLessEqual(M.worst_cost(), M.{bname})\n")
        golden[f"{mod}.worst_cost"] = [[None, base + per * top]]
        reqs.append({"id": did, "module": mod, "const": bname, "value": budget, "decision": True})
        (root / "src" / f"{mod}.py").write_text("\n".join(code), encoding="utf-8")
        gold_tests = (f"    def test_golden_{mod}(self):\n        for key, rows in GOLD.items():\n"
                      f"            if not key.startswith('{mod}.'):\n                continue\n"
                      f"            fn = getattr(M, key.split('.')[1])\n            for x, exp in rows:\n"
                      f"                got = fn() if x is None else fn(x)\n                self.assertEqual(got, exp, (key, x))\n")
        tests.append(gold_tests)
        (root / "tests" / f"test_{mod}.py").write_text("\n".join(tests) + "\n\nif __name__ == '__main__':\n    unittest.main()\n",
                                                        encoding="utf-8")
    (root / "specs" / "requirements.md").write_text("\n".join(spec_lines), encoding="utf-8")
    (root / "tests" / "golden" / "vectors.json").write_text(json.dumps(golden, indent=1), encoding="utf-8")
    # 契約:mod_1 產生,其他模組讀
    contracts = {"contracts": {"Report": {"owner": "team-1", "order": ["id", "delay", "power", "flag"], "latency_ms": 10,
                  "fields": {"id": {"type": "int", "range": [0, 255]},
                             "delay": {"type": "int", "unit": "ms", "range": [0, 1000]},
                             "power": {"type": "int", "scale": 0.5, "range": [0, 127]},
                             "flag": {"type": "int", "polarity": "1=on", "enum": {"OFF": 0, "ON": 1}}}}}}
    (root / "specs" / "contracts.json").write_text(json.dumps(contracts, indent=1), encoding="utf-8")
    consumer = ["\"\"\"consumer(玩具):讀 Report 契約。\"\"\"\n",
                "# @uses Report.delay\ndef delay_us(msg):\n    return msg['delay'] * 1000  # 單位 ms -> us\n",
                "# @uses Report.power\ndef power_db(msg):\n    return msg['power'] * 0.5\n",
                "# @uses Report.flag\ndef is_on(msg):\n    return msg['flag'] == 1\n"]
    (root / "src" / "consumer_a.py").write_text("\n".join(consumer), encoding="utf-8")
    (root / "specflow.json").write_text(json.dumps({
        "spec_dirs": ["specs"], "code_dirs": ["src"], "test_dirs": ["tests"], "protected": ["tests/golden/**"],
        "contracts": "specs/contracts.json", "gates": ["python -m unittest discover -s tests -q"]}, indent=2), encoding="utf-8")
    return {"reqs": reqs, "n_mod": n_mod, "per_mod": per_mod, "seed": seed}


def git_init(root: Path) -> None:
    """初始化 git 並做第一個 commit(guard 需要)。"""
    def g(*a: str) -> None:
        subprocess.run(["git", *a], cwd=root, check=True, capture_output=True)
    g("init", "-q")
    g("config", "user.email", "t@example.com")
    g("config", "user.name", "t")
    g("config", "core.autocrlf", "false")
    (root / ".gitignore").write_text(".specflow/index.json\n__pycache__/\n", encoding="utf-8")
    g("add", "-A")
    g("commit", "-qm", "init")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--mods", type=int, default=3)
    ap.add_argument("--per", type=int, default=3)
    a = ap.parse_args()
    out = Path(a.out)
    info = gen(out, a.seed, a.mods, a.per)
    git_init(out)
    print(json.dumps({"reqs": len(info["reqs"])}))
    sys.exit(0)
