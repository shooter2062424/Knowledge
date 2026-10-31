"""一次跑完所有關卡:單元/golden/Rel-21 測試、drift、內部約束。

用法:python tools/run_gates.py <pkg> <Release>
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from specutil import effective_params, eval_constraints, load_json  # noqa: E402


def run(cmd: list[str], env_extra: dict[str, str]) -> tuple[int, str]:
    env = {**os.environ, **env_extra, "PYTHONIOENCODING": "utf-8"}
    p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr


def main() -> int:
    pkg, release = sys.argv[1], sys.argv[2]
    env = {"MODEM_PKG": pkg}
    rows = []
    rc, _ = run([sys.executable, "-m", "unittest", "tests.test_modem", "-q"], env)
    rows.append(("G1 Rel-20 回歸(含 golden 位元級、timer、重試)", rc == 0))
    if release != "Rel-20":
        rc, _ = run([sys.executable, "-m", "unittest", "tests.test_rel21", "-q"], env)
        rows.append(("G2 Rel-21 規格導向測試(含向下相容解碼)", rc == 0))
    run([sys.executable, "tools/extract_spec.py", pkg], env)
    rc, out = run([sys.executable, "tools/check_drift.py", pkg, release], env)
    rows.append((f"G3 drift gate(規格 {release} vs 程式碼)", rc == 0))
    ext = load_json(ROOT / "specs" / "ext_spec.json")
    internal = load_json(ROOT / "specs" / "internal_spec.json")
    cons = eval_constraints(internal, pkg, effective_params(ext, release))
    rows.append(("G4 內部決定約束 vs 外部規格", all(c["ok"] for c in cons)))
    for name, ok in rows:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    for c in cons:
        if not c["ok"]:
            print(f"      ↳ 衝突 {c['id']} {c['title']}: {c['constraint']}")
    print("---- drift 明細 ----")
    print(out.strip())
    return 0 if all(ok for _, ok in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
