"""實驗 S2:`specflow mutate` 能不能分辨強弱不同的測試套件(關卡品質探測是否有鑑別力)。

三種測試強度(同一批隨機專案):
  full    : 原測試(每個需求都測 上限 與 上限+1)
  no_edge : 拿掉「上限+1 必須被拒絕」的斷言(弱邊界)
  smoke   : 每個測試只剩 assertTrue(True)(幾乎不驗證)
各跑 N 個突變,看 gates(unittest)抓到率。

用法: python run_s2.py <專案數> <每專案突變數> <out.json>
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import gen_repo as G

SF = Path(os.environ.get("SPECFLOW", r"C:\Users\shoot\project\ai-grocery\plugins\spec-code-flow\skills\spec-code-flow\scripts\specflow.py"))
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}


def weaken(root: Path, mode: str) -> None:
    for p in (root / "tests").glob("test_mod_*.py"):
        t = p.read_text(encoding="utf-8")
        if mode == "no_edge":
            t = re.sub(r"\n\s+self\.assertFalse\(M\.accept_\w+\(M\.\w+ \+ 1\)\)", "", t)
            t = re.sub(r"(    def test_golden_[\s\S]*?)(?=\n\nif __name__)", "    def test_golden_skip(self):\n        pass\n", t)
        elif mode == "smoke":
            t = re.sub(r"(def test_\w+\(self\):\n)(?:(?:        .*\n)+)", r"\1        self.assertTrue(True)\n", t)
        p.write_text(t, encoding="utf-8")


def main() -> None:
    n_proj, n_mut = int(sys.argv[1]), int(sys.argv[2])
    rows = []
    for mode in ("full", "no_edge", "smoke"):
        for k in range(n_proj):
            tmp = Path(tempfile.mkdtemp(prefix="s2-"))
            try:
                root = tmp / "r"
                G.gen(root, 500 + k, 3, 3)
                weaken(root, mode)
                r = subprocess.run([sys.executable, str(SF), "--path", str(root), "mutate", "-n", str(n_mut), "--seed", str(k), "--json"],
                                   capture_output=True, text=True, encoding="utf-8", env=ENV)
                m = re.search(r"mutation: (\d+)/(\d+)", r.stdout)
                rows.append({"mode": mode, "proj": k, "killed": int(m.group(1)) if m else None, "total": int(m.group(2)) if m else None,
                             "rc": r.returncode, "err": r.stderr[-120:] if not m else ""})
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
        print(mode, "done", flush=True)
    Path(sys.argv[3]).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
