"""MeasurementReport 編解碼(模擬 ASN.1 UPER 風格的位元打包)。"""
from typing import Any

from .trace import trace

MEAS_ID_BITS = 6      # R-MR-01
MEAS_ID_MAX = 63      # R-MR-01
LEVEL_BITS = 7        # R-MR-02
LEVEL_MAX = 127       # R-MR-02
NEIGH_COUNT_BITS = 4  # R-MR-03
NEIGH_MAX = 8         # R-MR-03
PCI_BITS = 10         # R-MR-03
PCI_MAX = 1007        # R-MR-03
EXT_LEN_BITS = 8      # R-MR-04


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


@trace("R-MR-01", "R-MR-02", "R-MR-03", "R-MR-04")
def encode_measurement_report(msg: dict[str, Any], release: int = 20) -> bytes:
    """編碼 MeasurementReport。"""
    neighbors = msg.get("neighbors", [])
    if len(neighbors) > NEIGH_MAX:
        raise ValueError("too many neighbors")
    w = BitWriter()
    w.write(msg["meas_id"], MEAS_ID_BITS)
    w.write(msg["rsrp"], LEVEL_BITS)
    w.write(msg["rsrq"], LEVEL_BITS)
    w.write(len(neighbors), NEIGH_COUNT_BITS)
    for n in neighbors:
        if n["pci"] > PCI_MAX:
            raise ValueError("pci out of range")
        w.write(n["pci"], PCI_BITS)
        w.write(n["rsrp"], LEVEL_BITS)
    w.write(0, 1)  # 擴充旗標:v1 永遠無擴充
    return w.to_bytes()


@trace("R-MR-01", "R-MR-02", "R-MR-03", "R-MR-04")
def decode_measurement_report(data: bytes, release: int = 20) -> dict[str, Any]:
    """解碼 MeasurementReport;遇到未知擴充依 R-MR-04 靜默略過。"""
    r = BitReader(data)
    msg: dict[str, Any] = {"meas_id": r.read(MEAS_ID_BITS), "rsrp": r.read(LEVEL_BITS),
                           "rsrq": r.read(LEVEL_BITS)}
    count = r.read(NEIGH_COUNT_BITS)
    msg["neighbors"] = [{"pci": r.read(PCI_BITS), "rsrp": r.read(LEVEL_BITS)} for _ in range(count)]
    if r.read(1):
        length = r.read(EXT_LEN_BITS)
        r.pos += 8 * length
        msg["ignored_ext_bytes"] = length
    return msg


def pack_bits_debug(data: bytes) -> str:
    """除錯用:位元字串(歷史遺留,無規格標註)。"""
    return "".join(f"{b:08b}" for b in data)


@trace("R-MR-99")
def legacy_filter(msg: dict[str, Any]) -> bool:
    """舊需求殘留的標註(R-MR-99 已不存在於外部規格)。"""
    return msg.get("rsrp", 0) > 0
