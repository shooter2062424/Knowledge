"""關卡強度探測:對 modem_v2 手工注入 10 種典型錯誤,看測試/drift 能抓到幾個。

另外做大量差分:modem_v2(release=20) 對凍結的 modem_v1 隨機比對 5000 筆。
用法:python tools/mutation_probe.py
"""
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MUTATIONS = [
    ("codec.py", "x.write(len(beams), BEAM_COUNT_BITS)", "x.write(len(beams), BEAM_COUNT_BITS + 0) if False else x.write(len(beams) % 16, BEAM_COUNT_BITS)", "beam 計數被取模(超過 15 筆失真)"),
    ("codec.py", "NEIGH_BASE_MAX = 8 ", "NEIGH_BASE_MAX = 7 ", "base 邊界少一(第 8 筆被推到擴充)"),
    ("codec.py", "PCI_MAX = 1007", "PCI_MAX = 1023", "PCI 上限放寬到位元寬度極限"),
    ("codec.py", "if release < 21:\n            r.pos += 8 * length", "if release < 20:\n            r.pos += 8 * length", "舊版解碼器不再略過擴充"),
    ("codec.py", "base, extra = neighbors[:NEIGH_BASE_MAX], neighbors[NEIGH_BASE_MAX:]", "base, extra = neighbors[:NEIGH_BASE_MAX], neighbors[NEIGH_BASE_MAX + 1:]", "額外鄰區漏掉第 9 筆(off-by-one)"),
    ("fsm.py", "T300_MS = 1000", "T300_MS = 100", "T300 數值錯"),
    ("fsm.py", "if nxt is None and self.release >= 21:", "if nxt is None:", "Rel-21 轉移洩漏到 Rel-20"),
    ("sched.py", "COST_PER_NEIGH_BATCH_US = 2", "COST_PER_NEIGH_BATCH_US = 5", "批次成本偏高,最壞情況超預算"),
    ("sched.py", "NEIGH_CAP = 16", "NEIGH_CAP = 12", "內部上限小於外部上限"),
    ("fsm.py", "self.retries += 1\n            return self.step(\"setup_req\")", "self.retries += 2\n            return self.step(\"setup_req\")", "重試計數錯(內部行為)"),
]


def gates(pkg: str) -> list[str]:
    env = {**os.environ, "MODEM_PKG": pkg, "PYTHONIOENCODING": "utf-8"}
    fails = []
    for name, mod in (("G1", "tests.test_modem"), ("G2", "tests.test_rel21")):
        if subprocess.run([sys.executable, "-m", "unittest", mod, "-q"], cwd=ROOT, env=env,
                          capture_output=True).returncode:
            fails.append(name)
    subprocess.run([sys.executable, "tools/extract_spec.py", pkg], cwd=ROOT, env=env, capture_output=True)
    if subprocess.run([sys.executable, "tools/check_drift.py", pkg, "Rel-21"], cwd=ROOT, env=env,
                      capture_output=True).returncode:
        fails.append("G3")
    r = subprocess.run([sys.executable, "tools/run_gates.py", pkg, "Rel-21"], cwd=ROOT, env=env,
                       capture_output=True, text=True, encoding="utf-8")
    if "FAIL  G4" in r.stdout:
        fails.append("G4")
    return fails


def differential() -> str:
    from modem_v1 import codec as c1
    from modem_v2 import codec as c2
    rng = random.Random(7)
    bad = 0
    for _ in range(5000):
        n = rng.randint(0, 8)
        m = {"meas_id": rng.randint(0, 63), "rsrp": rng.randint(0, 127), "rsrq": rng.randint(0, 127),
             "neighbors": [{"pci": rng.randint(0, 1007), "rsrp": rng.randint(0, 127)} for _ in range(n)]}
        if c1.encode_measurement_report(m, 20) != c2.encode_measurement_report(m, 20):
            bad += 1
    rt_bad = 0
    for _ in range(5000):
        n = rng.randint(0, 16)
        m = {"meas_id": rng.randint(0, 63), "rsrp": rng.randint(0, 127), "rsrq": rng.randint(0, 127),
             "neighbors": [{"pci": rng.randint(0, 1007), "rsrp": rng.randint(0, 127)} for _ in range(n)]}
        if rng.random() < 0.5:
            m["beams"] = [rng.randint(0, 63) for _ in range(rng.randint(1, 16))]
        if c2.decode_measurement_report(c2.encode_measurement_report(m, 21), 21) != m:
            rt_bad += 1
        old = c2.decode_measurement_report(c2.encode_measurement_report(m, 21), 20)
        if old["neighbors"] != m["neighbors"][:8]:
            rt_bad += 1
    return f"差分(v2@Rel-20 vs 凍結 v1,5000 筆):不一致 {bad};Rel-21 往返 + 舊解碼器相容(5000 筆):失敗 {rt_bad}"


def main() -> None:
    print(differential())
    killed = 0
    for i, (f, old, new, desc) in enumerate(MUTATIONS, 1):
        pkg = f"mut_{i}"
        shutil.rmtree(ROOT / pkg, ignore_errors=True)
        shutil.copytree(ROOT / "modem_v2", ROOT / pkg, ignore=shutil.ignore_patterns("__pycache__"))
        p = ROOT / pkg / f
        s = p.read_text(encoding="utf-8")
        if old not in s:
            print(f"M{i:02d} 無法套用:{desc}")
            shutil.rmtree(ROOT / pkg)
            continue
        p.write_text(s.replace(old, new, 1), encoding="utf-8")
        caught = gates(pkg)
        killed += bool(caught)
        print(f"M{i:02d} {'抓到 ' + '+'.join(caught) if caught else '⚠️ 漏網':<14} {desc}")
        shutil.rmtree(ROOT / pkg)
    print(f"結果:{killed}/{len(MUTATIONS)} 被關卡抓到")


if __name__ == "__main__":
    main()
