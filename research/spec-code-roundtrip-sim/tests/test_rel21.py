"""由 delta_rel21.json 先寫好的規格導向測試(spec-first,v1 上必紅)。"""
import importlib
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
PKG = os.environ.get("MODEM_PKG", "modem_v1")
codec = importlib.import_module(f"{PKG}.codec")
fsm = importlib.import_module(f"{PKG}.fsm")


def covers(*ids):
    def deco(fn):
        fn.__covers__ = ids
        return fn
    return deco


def msg16():
    return {"meas_id": 5, "rsrp": 100, "rsrq": 90,
            "neighbors": [{"pci": 100 + i, "rsrp": 10 + i} for i in range(16)],
            "beams": [3, 9, 63]}


class Rel21(unittest.TestCase):
    @covers("R-MR-03", "R-MR-10", "R-MR-11")
    def test_roundtrip_16_neighbors_and_beams(self):
        data = codec.encode_measurement_report(msg16(), release=21)
        self.assertEqual(codec.decode_measurement_report(data, release=21), msg16())

    @covers("R-MR-04", "R-MR-11")
    def test_rel20_decoder_ignores_rel21_extension(self):
        """向下相容:Rel-20 接收端解 Rel-21 訊息,前 8 筆鄰區正確、擴充被略過。"""
        data = codec.encode_measurement_report(msg16(), release=21)
        old = codec.decode_measurement_report(data, release=20)
        self.assertEqual(old["neighbors"], msg16()["neighbors"][:8])
        self.assertGreater(old["ignored_ext_bytes"], 0)

    @covers("R-MR-03")
    def test_rel21_base_prefix_equals_rel20_encoding(self):
        """前 8 筆沿用原佈局:只含 8 筆的訊息,Rel-21 編碼 == Rel-20 編碼。"""
        m = msg16()
        m["neighbors"] = m["neighbors"][:8]
        m.pop("beams")
        self.assertEqual(codec.encode_measurement_report(m, 21), codec.encode_measurement_report(m, 20))

    @covers("R-MR-10")
    def test_boundary_16_beams_and_6bit_max(self):
        """邊界值:beam 計數 = 上限、beam 值 = 6 位元最大。(變異探測 M01 漏網後補)"""
        m = msg16()
        m["beams"] = [63] * 16
        data = codec.encode_measurement_report(m, release=21)
        self.assertEqual(codec.decode_measurement_report(data, release=21), m)

    @covers("R-MR-03")
    def test_17_neighbors_rejected(self):
        m = msg16()
        m["neighbors"] = m["neighbors"] + [{"pci": 1, "rsrp": 1}]
        with self.assertRaises(ValueError):
            codec.encode_measurement_report(m, release=21)

    @covers("R-FSM-01", "R-FSM-05")
    def test_suspend_resume_only_in_rel21(self):
        r = fsm.Rrc(21)
        r.step("setup_req")
        r.step("setup_ok")
        self.assertEqual(r.step("suspend"), "SUSPENDED")
        self.assertEqual(r.step("resume_fast"), "CONNECTED")
        self.assertEqual(fsm.T_RESUME_MS, 300)
        old = fsm.Rrc(20)
        old.step("setup_req")
        old.step("setup_ok")
        with self.assertRaises(ValueError):
            old.step("suspend")


if __name__ == "__main__":
    unittest.main()
