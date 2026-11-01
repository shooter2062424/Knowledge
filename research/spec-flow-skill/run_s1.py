"""實驗 S1:漂移偵測。對隨機玩具專案注入「spec 與 code 不同步」事件,比較各層偵測率。

偵測層:
  tests   : 專案自己的 unittest(含凍結 golden)
  check   : specflow check(只看 ERROR / NEEDS-HUMAN)
  check+w : specflow check --strict(警告也算偵測)
  union   : tests ∪ check+w
另含 2 種「良性」對照事件(不該被報):行尾空白、改無關檔案。

用法: python run_s1.py <每種事件的次數> <out.json>
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

import gen_repo as G

SF = Path(os.environ.get("SPECFLOW", r"C:\Users\shoot\project\ai-grocery\plugins\spec-code-flow\skills\spec-code-flow\scripts\specflow.py"))
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}


def sf(root: Path, *args: str) -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(SF), *args], cwd=root, capture_output=True, text=True, encoding="utf-8", env=ENV)
    return r.returncode, r.stdout + r.stderr


def tests_fail(root: Path) -> bool:
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"], cwd=root,
                       capture_output=True, text=True, env=ENV)
    return r.returncode != 0


def edit(p: Path, fn) -> bool:
    t = p.read_text(encoding="utf-8")
    n = fn(t)
    if n == t:
        return False
    p.write_text(n, encoding="utf-8")
    return True


def pick(rnd: random.Random, info: dict, decision: bool = False) -> dict:
    return rnd.choice([r for r in info["reqs"] if bool(r.get("decision")) == decision])


# 每個事件: (名稱, 是否真漂移, 注入函式(root, info, rnd) -> bool 是否成功注入)
def ev_spec_value(root, info, rnd):
    r = pick(rnd, info)
    return edit(root / "specs/requirements.md", lambda t: re.sub(rf"({r['const']}=)\d+", lambda m: m.group(1) + str(r["value"] * 2), t, count=1))


def ev_code_const(root, info, rnd):
    r = pick(rnd, info)
    return edit(root / "src" / f"{r['module']}.py", lambda t: re.sub(rf"^({r['const']} = )\d+", lambda m: m.group(1) + str(r["value"] + 1), t, count=1, flags=re.M))


def ev_spec_text(root, info, rnd):
    r = pick(rnd, info)
    return edit(root / "specs/requirements.md",
                lambda t: t.replace(f"最多接受 {r['const']} 筆 {r['word']};超過的請求 SHALL 被拒絕", f"最多接受 {r['const']} 筆 {r['word']};超過的請求 SHALL 被丟棄並記錄"))


def ev_drop_spec_tag(root, info, rnd):
    r = pick(rnd, info)
    return edit(root / "src" / f"{r['module']}.py", lambda t: t.replace(f"    # @spec {r['id']}\n", "", 1))


def ev_rename_id(root, info, rnd):
    r = pick(rnd, info)
    return edit(root / "specs/requirements.md", lambda t: t.replace(f"## {r['id']} ·", f"## {r['id']}X ·", 1))


def ev_delete_req(root, info, rnd):
    r = pick(rnd, info)
    def f(t):
        parts = re.split(r"(?m)^(?=## )", t)
        return "".join(p for p in parts if not p.startswith(f"## {r['id']} "))
    return edit(root / "specs/requirements.md", f)


def ev_drop_covers(root, info, rnd):
    r = pick(rnd, info)
    return edit(root / "tests" / f"test_{r['module']}.py", lambda t: t.replace(f"        # @covers {r['id']}\n", "", 1))


def ev_offbyone(root, info, rnd):
    r = pick(rnd, info)
    return edit(root / "src" / f"{r['module']}.py", lambda t: t.replace(f"count <= {r['const']}", f"count < {r['const']}", 1))


def ev_deprecate(root, info, rnd):
    r = pick(rnd, info)
    def f(t):
        i = t.index(f"## {r['id']} ·")
        j = t.index("- status: active", i)
        return t[:j] + "- status: deprecated" + t[j + len("- status: active"):]
    return edit(root / "specs/requirements.md", f)


def ev_new_req(root, info, rnd):
    return edit(root / "specs/requirements.md", lambda t: t + "\n## R-NEW-01 · 新需求\n- kind: external\n- owner: team-9\n- status: active\n\n系統 SHALL 支援新功能。\n")


def ev_bad_depends(root, info, rnd):
    r = pick(rnd, info)
    def f(t):
        i = t.index(f"## {r['id']} ·")
        j = t.index("- status: active", i)
        return t[:j] + "- depends: R-GHOST-99\n" + t[j:]
    return edit(root / "specs/requirements.md", f)


def ev_decision_const(root, info, rnd):
    r = pick(rnd, info, decision=True)
    return edit(root / "src" / f"{r['module']}.py", lambda t: re.sub(rf"^({r['const']} = )\d+", lambda m: m.group(1) + str(r["value"] + 20), t, count=1, flags=re.M))


def ev_golden(root, info, rnd):
    p = root / "tests/golden/vectors.json"
    d = json.loads(p.read_text())
    k = rnd.choice(sorted(d))
    d[k][-1][1] = (not d[k][-1][1]) if isinstance(d[k][-1][1], bool) else d[k][-1][1] + 1
    p.write_text(json.dumps(d, indent=1))
    return True


def ev_code_and_golden(root, info, rnd):
    """agent 常見捷徑:改程式常數,再把凍結 golden 改成與新程式一致,讓測試全綠。"""
    r = pick(rnd, info)
    ok = edit(root / "src" / f"{r['module']}.py", lambda t: re.sub(rf"^({r['const']} = )\d+", lambda m: m.group(1) + str(r["value"] + 1), t, count=1, flags=re.M))
    p = root / "tests/golden/vectors.json"
    d = json.loads(p.read_text())
    key = f"{r['module']}.{r['fn']}"
    for row in d[key]:
        if row[0] == r["value"] + 1:
            row[1] = True
    p.write_text(json.dumps(d, indent=1))
    return ok


def ev_benign_ws(root, info, rnd):
    return edit(root / "specs/requirements.md", lambda t: t.replace("SHALL", "SHALL  ", 0) + "   \n")


def ev_benign_other(root, info, rnd):
    (root / "README.txt").write_text("hello\n")
    return True


EVENTS = [
    ("spec_value_changed", True, ev_spec_value),
    ("code_const_changed", True, ev_code_const),
    ("spec_text_changed", True, ev_spec_text),
    ("spec_tag_dropped", True, ev_drop_spec_tag),
    ("spec_id_renamed", True, ev_rename_id),
    ("spec_req_deleted", True, ev_delete_req),
    ("covers_tag_dropped", True, ev_drop_covers),
    ("logic_offbyone", True, ev_offbyone),
    ("req_deprecated_still_used", True, ev_deprecate),
    ("new_req_no_code", True, ev_new_req),
    ("depends_on_ghost", True, ev_bad_depends),
    ("decision_const_changed", True, ev_decision_const),
    ("golden_tampered", True, ev_golden),
    ("code_and_golden_both_changed", True, ev_code_and_golden),
    ("benign_trailing_ws", False, ev_benign_ws),
    ("benign_unrelated_file", False, ev_benign_other),
]


def main() -> None:
    n = int(sys.argv[1])
    out = Path(sys.argv[2])
    rows = []
    rnd = random.Random(12345)
    for name, real, fn in EVENTS:
        for k in range(n):
            seed = rnd.randrange(10**6)
            mods, per = rnd.choice([(2, 2), (3, 3), (4, 4), (6, 4)])
            tmp = Path(tempfile.mkdtemp(prefix="s1-"))
            try:
                root = tmp / "r"
                info = G.gen(root, seed, mods, per)
                G.git_init(root)
                sf(root, "stamp", "--all")
                ok = fn(root, info, random.Random(seed))
                if not ok:
                    continue
                t = tests_fail(root)
                c_code, c_out = sf(root, "check")
                s_code, s_out = sf(root, "check", "--strict")
                g_code, g_out = sf(root, "guard") if name in ("decision_const_changed", "golden_tampered", "code_and_golden_both_changed") else (0, "")
                rows.append({"event": name, "real": real, "seed": seed, "n_items": len(info["reqs"]),
                             "tests": t, "check": c_code != 0, "check_strict": s_code != 0,
                             "guard": g_code != 0, "check_code": c_code, "guard_code": g_code,
                             "first_line": (s_out.splitlines() or [""])[0][:120]})
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
        print(name, "done", flush=True)
    out.write_text(json.dumps({"specflow_sha": hashlib.sha256(SF.read_bytes()).hexdigest()[:12], "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
