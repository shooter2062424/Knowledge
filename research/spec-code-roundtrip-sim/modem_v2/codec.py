"""MeasurementReport 編解碼(v2:Rel-20 與 Rel-21 並存;Rel-20 位元佈局凍結)。"""
from typing import Any

from .trace import trace

MEAS_ID_BITS = 6      # R-MR-01
MEAS_ID_MAX = 63      # R-MR-01
LEVEL_BITS = 7        # R-MR-02
LEVEL_MAX = 127       # R-MR-02
NEIGH_COUNT_BITS = 4  # R-MR-03
NEIGH_MAX = 16        # R-MR-03
NEIGH_BASE_MAX = 8    # R-MR-03
PCI_BITS = 10         # R-MR-03
PCI_MAX = 1007        # R-MR-03
EXT_LEN_BITS = 8      # R-MR-04
BEAM_MAX = 16         # R-MR-10
BEAM_BITS = 6         # R-MR-10
BEAM_COUNT_BITS = 5   # R-MR-10
EXTRA_NEIGH_COUNT_BITS = 4  # R-MR-11


class BitWriter:
    """逐位元寫入器。"""

    def __init__(self) -> None:
        self.bits: list[int] = []

    def write(self, value: int, nbits: int) -> None:
        if value < 0 or value >= (1 << nbits):
            raise ValueError(f"value {value} does not fit {nbits} bits")
        self.bits += [(value >> i) & 1 for i in range(nbits - 1, -1, -1)]

    def to_bytes(self) -> bytes:
        b = self.bits + [0] * (-len(self.bits) % 8)
        return bytes(int("".join(map(str, b[i:i + 8])), 2) for i in range(0, len(b), 8))


class BitReader:
    """逐位元讀取器。"""

    def __init__(self, data: bytes) -> None:
        self.bits = [(byte >> i) & 1 for byte in data for i in range(7, -1, -1)]
        self.pos = 0

    def read(self, nbits: int) -> int:
        if self.pos + nbits > len(self.bits):
            raise ValueError("truncated")
        v = 0
        for _ in range(nbits):
            v = (v << 1) | self.bits[self.pos]
            self.pos += 1
        return v


@trace("R-MR-01", "R-MR-02", "R-MR-03", "R-MR-04", "R-MR-10", "R-MR-11")
def encode_measurement_report(msg: dict[str, Any], release: int = 20) -> bytes:
    """編碼 MeasurementReport。

    Rel-20:最多 NEIGH_BASE_MAX 筆鄰區,無擴充(位元佈局與 v1 完全相同)。
    Rel-21:前 NEIGH_BASE_MAX 筆照舊;其餘鄰區與 beam 清單放進 v2100 擴充(R-MR-11)。
    """
    neighbors = msg.get("neighbors", [])
    beams = msg.get("beams", [])
    limit = NEIGH_MAX if release >= 21 else NEIGH_BASE_MAX
    if len(neighbors) > limit:
        raise ValueError("too many neighbors")
    if beams and release < 21:
        raise ValueError("beams require Rel-21")
    base, extra = neighbors[:NEIGH_BASE_MAX], neighbors[NEIGH_BASE_MAX:]
    w = BitWriter()
    w.write(msg["meas_id"], MEAS_ID_BITS)
    w.write(msg["rsrp"], LEVEL_BITS)
    w.write(msg["rsrq"], LEVEL_BITS)
    w.write(len(base), NEIGH_COUNT_BITS)
    for n in base:
        _write_neighbor(w, n)
    if release >= 21 and (beams or extra):
        if len(beams) > BEAM_MAX:
            raise ValueError("too many beams")
        x = BitWriter()  # v2100 擴充內容:先 beam 清單,再額外鄰區(R-MR-11)
        x.write(len(beams), BEAM_COUNT_BITS)
        for b in beams:
            x.write(b, BEAM_BITS)
        x.write(len(extra), EXTRA_NEIGH_COUNT_BITS)
        for n in extra:
            _write_neighbor(x, n)
        payload = x.to_bytes()
        w.write(1, 1)
        w.write(len(payload), EXT_LEN_BITS)
        for byte in payload:
            w.write(byte, 8)
    else:
        w.write(0, 1)
    return w.to_bytes()


def _write_neighbor(w: BitWriter, n: dict[str, int]) -> None:
    if n["pci"] > PCI_MAX:
        raise ValueError("pci out of range")
    w.write(n["pci"], PCI_BITS)
    w.write(n["rsrp"], LEVEL_BITS)


def _read_neighbor(r: BitReader) -> dict[str, int]:
    return {"pci": r.read(PCI_BITS), "rsrp": r.read(LEVEL_BITS)}


@trace("R-MR-01", "R-MR-02", "R-MR-03", "R-MR-04", "R-MR-10", "R-MR-11")
def decode_measurement_report(data: bytes, release: int = 20) -> dict[str, Any]:
    """解碼 MeasurementReport。release<21 時依 R-MR-04 靜默略過擴充。"""
    r = BitReader(data)
    msg: dict[str, Any] = {"meas_id": r.read(MEAS_ID_BITS), "rsrp": r.read(LEVEL_BITS),
                           "rsrq": r.read(LEVEL_BITS)}
    msg["neighbors"] = [_read_neighbor(r) for _ in range(r.read(NEIGH_COUNT_BITS))]
    if r.read(1):
        length = r.read(EXT_LEN_BITS)
        if release < 21:
            r.pos += 8 * length
            msg["ignored_ext_bytes"] = length
        else:
            x = BitReader(bytes(r.read(8) for _ in range(length)))
            beams = [x.read(BEAM_BITS) for _ in range(x.read(BEAM_COUNT_BITS))]
            msg["neighbors"] += [_read_neighbor(x) for _ in range(x.read(EXTRA_NEIGH_COUNT_BITS))]
            if beams:
                msg["beams"] = beams
    return msg
