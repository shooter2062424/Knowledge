"""Rel-20 行為回歸 + 規格導向測試。以環境變數 MODEM_PKG 指定受測套件。"""
import importlib
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
PKG = os.environ.get("MODEM_PKG", "modem_v1")
codec = importlib.import_module(f"{PKG}.codec")
fsm = importlib.import_module(f"{PKG}.fsm")
sched = importlib.import_module(f"{PKG}.sched")


def covers(*ids):
    def deco(fn):
        fn.__covers__ = ids
        return fn
    return deco


class Rel20(unittest.TestCase):
    @covers("R-MR-01", "R-MR-02", "R-MR-03")
    def test_golden_vectors_bit_exact(self):
        """凍結的 Rel-20 golden vector:編碼必須位元級一致。"""
        for case in json.loads((ROOT / "golden" / "rel20.json").read_text()):
            self.assertEqual(codec.encode_measurement_report(case["msg"], release=20).hex(), case["hex"])
            self.assertEqual(codec.decode_measurement_report(bytes.fromhex(case["hex"]), 20)["neighbors"],
                             case["msg"]["neighbors"])

    @covers("R-MR-03")
    def test_rel20_rejects_9_neighbors(self):
        msg = {"meas_id": 1, "rsrp": 1, "rsrq": 1, "neighbors": [{"pci": 1, "rsrp": 1}] * 9}
        with self.assertRaises(ValueError):
            codec.encode_measurement_report(msg, release=20)

    @covers("R-FSM-01", "R-FSM-02", "D-INT-03")
    def test_setup_retry(self):
        r = fsm.Rrc(20)
        r.step("setup_req")
        for _ in range(fsm.SETUP_RETRY_MAX):
            self.assertEqual(r.on_t300_expiry(), "SETUP_PENDING")
        self.assertEqual(r.on_t300_expiry(), "IDLE")

    @covers("R-FSM-03")
    def test_t304_timer_matches_spec(self):
        self.assertEqual(fsm.T304_MS, 200)

    @covers("D-INT-02")
    def test_budget_worst_case(self):
        ext_max = 8 if PKG == "modem_v1" else 16
        msg = {"neighbors": [{"pci": 1, "rsrp": 1}] * ext_max}
        ok, _ = sched.admit(msg)
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()
