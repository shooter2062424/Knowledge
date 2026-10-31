"""以凍結的 v1 產生 Rel-20 golden vector(只在 v1 上跑一次,之後不得重產)。"""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modem_v1 import codec  # noqa: E402

rng = random.Random(2026)
cases = []
for _ in range(40):
    n = rng.randint(0, 8)
    msg = {"meas_id": rng.randint(0, 63), "rsrp": rng.randint(0, 127), "rsrq": rng.randint(0, 127),
           "neighbors": [{"pci": rng.randint(0, 1007), "rsrp": rng.randint(0, 127)} for _ in range(n)]}
    cases.append({"msg": msg, "hex": codec.encode_measurement_report(msg, 20).hex()})
(Path(__file__).parent / "rel20.json").write_text(json.dumps(cases), encoding="utf-8")
print(len(cases), "golden vectors")
