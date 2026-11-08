"""v1 行為測試:scope 解析(含兩個使用者決策)、gate、雙人規則、lint、未找到清單、折疊。
用法:python tests/test_v1.py   (在臨時目錄建 KB,不動真實資料)
"""
import os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

KB = Path(__file__).resolve().parent.parent / "kb.py"
FAILS = []


def run(root, *args, today="2026-11-08", user="alice"):
    p = subprocess.run([sys.executable, "-X", "utf8", str(KB), *args], capture_output=True, text=True, encoding="utf-8",
                       env=dict(os.environ, KB_ROOT=str(root), KB_TODAY=today, KB_USER=user, PYTHONIOENCODING="utf-8"))
    return p.returncode, p.stdout + p.stderr


def check(name, cond, info=""):
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else "\n     " + info.replace("\n", "\n     ")))
    if not cond:
        FAILS.append(name)


def claim(root, cid, **kw):
    f = {"id": cid, "concept": "ipc", "subject": "ipc", "lifecycle": "active", "valid_from": "2026-06-01", "source": "M01@01:00",
         "author": "seed", "aliases": "行程間通訊, 跨程序呼叫, IPC protocol, inter-process", **kw}
    (root / "claims").mkdir(parents=True, exist_ok=True)
    (root / "claims" / f"{cid}.md").write_text("---\n" + "\n".join(f"{k}: {v}" for k, v in f.items()) + "\n---\n", encoding="utf-8")


def main():
    root = Path(tempfile.mkdtemp(prefix="kbv1_"))
    try:
        claim(root, "CL-0001", statement="IPC 使用 v2")
        claim(root, "CL-0002", statement="Vision 在 Linux main 仍使用 IPC v1", lifecycle="deprecated", retire_when="2027-09-30", project="vision", platform="linux", branch="main")
        claim(root, "CL-0003", statement="Windows 上 IPC v2 尚未提供,使用 v1", platform="windows")
        claim(root, "CL-0004", statement="LTS 分支維持 IPC v1 不升級", branch="lts")
        run(root, "build")

        # --- 決策 2:同具體度衝突 → 不自動挑,要求寫明確 claim ---
        rc, out = run(root, "resolve", "ipc", "--platform", "windows", "--branch", "lts")
        check("同具體度重疊 → CONFLICT (exit 3)", rc == 3 and "CONFLICT" in out, out)
        rc, out = run(root, "lint")
        check("lint 抓到 AMBIGUOUS-INTERSECTION", "AMBIGUOUS-INTERSECTION" in out and rc == 1, out)

        # 補明確 claim(Windows + LTS)後 → 唯一結論
        claim(root, "CL-0005", statement="Windows LTS 使用 IPC v1,只做安全修補", platform="windows", branch="lts")
        rc, out = run(root, "resolve", "ipc", "--platform", "windows", "--branch", "lts")
        check("補明確 claim 後 → 唯一結論 CL-0005 (exit 0)", rc == 0 and "[CL-0005]" in out, out)
        rc, out = run(root, "lint")
        check("補完後 lint 無 AMBIGUOUS", "AMBIGUOUS-INTERSECTION" not in out, out)

        # --- 決策 6:缺 scope → 反問 ---
        rc, out = run(root, "resolve", "ipc")
        check("完全沒給 scope → ASK (exit 2) 並列出情境", rc == 2 and "ASK" in out and "platform" in out, out)
        rc, out = run(root, "resolve", "ipc", "--platform", "linux", "--branch", "main")
        check("缺 project 且 project 會改變結論 → ASK project", rc == 2 and "project" in out.split("ASK")[-1], out)
        rc, out = run(root, "resolve", "ipc", "--project", "vision", "--platform", "linux", "--branch", "main")
        check("Vision/Linux/main → CL-0002 且標 deprecated 與退場日", rc == 0 and "[CL-0002]" in out and "2027-09-30" in out, out)
        rc, out = run(root, "resolve", "ipc", "--project", "audio", "--platform", "linux", "--branch", "main")
        check("未出現過的 project 值 → 回全域 CL-0001", rc == 0 and "[CL-0001]" in out, out)
        rc, out = run(root, "resolve", "nothing-here")
        check("不存在的 concept → exit 4 並列出已有 concept(不污染未找到清單)", rc == 4 and "ipc" in out, out)

        # --- gate ---
        base = ["propose", "--subject", "ipc", "--statement", "新結論", "--valid-from", "2026-11-08", "--source", "M09@01:00", "--author", "alice",
                "--aliases", "a1, a2, new conclusion, 新說法"]
        rc, out = run(root, *base, "--platform", "windows")
        check("同 concept 同 scope 結論不同且沒 supersedes → 退回", rc == 1 and "supersedes" in out, out)
        rc, out = run(root, *base, "--platform", "windows", "--supersedes", "CL-0003")
        check("明確 supersedes → 進 inbox", rc == 0 and "inbox" in out, out)
        pid = re.search(r"P-\d+-\w+", out).group(0)
        rc, out = run(root, "approve", pid, "--by", "alice")
        check("作者不能核准自己的 claim", rc != 0 and "雙人" in out, out)
        rc, out = run(root, "approve", pid, "--by", "bob")
        check("另一人核准成功並產生 CL-0006", rc == 0 and "CL-0006" in out, out)
        rc, out = run(root, "show", "CL-0003")
        check("被取代的 CL-0003 衍生欄位 status: superseded", "status: superseded" in out and "superseded_by: CL-0006" in out, out)
        rc, out = run(root, *base[:-2], "--aliases", "a1, a2", "--platform", "macos")
        check("aliases 少於 4 個 → 退回", rc == 1 and "aliases" in out, out)
        rc, out = run(root, "propose", "--subject", "ipc", "--statement", "x", "--valid-from", "2026-11-08", "--source", "s", "--author", "a",
                      "--aliases", "a, b, c, d", "--project", "vision", "--supersedes", "CL-0001")
        check("取代較寬的舊 claim 時 scope 變窄 → 退回", rc == 1 and "更窄" in out, out)
        rc, out = run(root, "propose", "--subject", "ipc", "--statement", "x2", "--valid-from", "2026-11-08", "--source", "s", "--author", "a",
                      "--aliases", "a, b, c, d", "--lifecycle", "deprecated")
        check("deprecated 沒 retire_when → 退回", rc == 1 and "retire_when" in out, out)

        # --- write-skew:兩條互相衝突的提案同時在 inbox,先核准的贏,後者核准時重驗被擋 ---
        r1 = run(root, *base[:-2], "--aliases", "a1, a2, b1, b2", "--platform", "qnx", "--statement", "QNX 用 v1")
        r2 = run(root, *base[:-2], "--aliases", "a1, a2, b1, b2", "--platform", "qnx", "--statement", "QNX 用 v2", "--author", "carol")
        p1 = re.search(r"P-\d+-\w+", r1[1]).group(0); p2 = re.search(r"P-\d+-\w+", r2[1]).group(0)
        run(root, "approve", p1, "--by", "bob")
        rc, out = run(root, "approve", p2, "--by", "bob")
        check("write-skew:第二條同 scope 衝突提案核准時重驗被擋", rc != 0 and "重驗未過" in out, out)

        # --- lint 時間類 ---
        rc, out = run(root, "lint", today="2027-10-01")
        check("退場日已過 → OVERDUE", "OVERDUE" in out and "CL-0002" in out, out)

        # --- 搜尋:別名、狀態、取代鏈、未找到 ---
        rc, out = run(root, "search", "跨程序呼叫")
        check("別名能命中", "CL-0001" in out, out)
        rc, out = run(root, "search", "Windows IPC v2")
        check("搜尋顯示 SUPERSEDED 並附新者(不隱藏)", "SUPERSEDED" in out and "CL-0006" in out, out)
        rc, out = run(root, "search", "完全無關的火星殖民")
        check("無命中 → 記入未找到", "未找到" in out, out)
        rc, out = run(root, "unfound", "--report")
        check("unfound --report 列出該查詢", "火星殖民" in out, out)

        # --- 折疊同型 ---
        for m in ["net", "ui", "codec", "sensor"]:
            claim(root, f"CL-1{m[:2]}", concept="budget", subject="budget", statement=f"{m} 模組每個 cycle 預算 150µs", project=m)
        run(root, "build")
        rc, out = run(root, "search", "cycle 預算")
        check("同型 claim 折疊成一列並註明另有幾條", "另有 3 條同型" in out, out)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print(f"\n{'全部通過' if not FAILS else '失敗 ' + str(len(FAILS)) + ' 項: ' + ', '.join(FAILS)}")
    sys.exit(1 if FAILS else 0)


main()
