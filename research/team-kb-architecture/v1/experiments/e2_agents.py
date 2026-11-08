"""E2:Haiku(low) 當查詢者,測 v1 的 AGENTS.md + kb.py 在 L 規模(1,530 條 claim)與 scope 小 KB 的實際表現。

條件:
  CTRL  只有 Grep/Glob/Read + 第四輪的基本 AGENTS(對照,等同 REPORT-4 的 A/B)
  V1    v1 AGENTS.md + kb.py(search / resolve / unfound)+ Grep/Glob/Read
  SCOPE v1 + 5 條帶範圍的 ipc claim(含同具體度衝突的修補),4 題 scope 問題
另外 X1 是「知識庫沒有」的題目,檢查會不會亂答、有沒有寫進未找到清單。
用法:python experiments/e2_agents.py setup|run [CTRL|V1|SCOPE ...]
"""
import json, os, re, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE.parent
TK = V1.parent
SB = TK / "data" / "sandbox"
sys.path.insert(0, str(TK / "lab4"))
import queries  # noqa: E402
import run_agents as ra  # noqa: E402  (只取 MUST / M1_GOLD / QIDS / BASE)

LOG = SB / "logs_v1"
KBS = {"CTRL": SB / "v1kb_ctrl", "V1": SB / "v1kb", "SCOPE": SB / "v1kb_scope"}
CTRL_AGENTS = """# 知識庫使用說明
這是 framework 團隊的知識庫(虛構)。
- claims/CL-*.md、claims/HN*.md:一條一檔的 claim。frontmatter 的 status 為 current 表示現行;superseded 表示已被新 claim 取代(superseded_by 指向取代者)。
- raw/meetings/:會議逐字稿(不可變原始紀錄)。notes/:雜項筆記。
- 回答時請引用 claim id,並說明日期與是否仍然有效。
"""
X1 = ("X1", "公司的差旅報銷上限是多少?")
SQ = [  # (id, 問題, 評分函式名)
    ("SQ1", "我們的 IPC 要用 v1 還是 v2?"),
    ("SQ2", "Vision 專案在 Linux 的 main 分支上,IPC 用哪一版?有沒有要退場?"),
    ("SQ3", "Windows 的 LTS 分支上 IPC 用哪一版?"),
    ("SQ4", "Audio 專案在 Windows 的 main 分支,IPC 用哪一版?"),
]


def claim(root, cid, **kw):
    f = {"id": cid, "concept": "ipc", "subject": "ipc", "lifecycle": "active", "valid_from": "2026-06-01", "source": "M01@01:00",
         "author": "seed", "aliases": "行程間通訊, 跨程序呼叫, IPC protocol, inter-process", **kw}
    (root / "claims").mkdir(parents=True, exist_ok=True)
    (root / "claims" / f"{cid}.md").write_text("---\n" + "\n".join(f"{k}: {v}" for k, v in f.items()) + "\n---\n", encoding="utf-8")


def setup():
    # V1 先重建(讓 AGENTS.md 進去)
    subprocess.run([sys.executable, "-X", "utf8", str(HERE / "build_l.py")], check=True)
    for n in ("CTRL", "SCOPE"):
        if KBS[n].exists():
            shutil.rmtree(KBS[n])
    shutil.copytree(KBS["V1"], KBS["CTRL"], ignore=shutil.ignore_patterns("kb.py", "state", "topics", "AGENTS.md"))
    (KBS["CTRL"] / "AGENTS.md").write_text(CTRL_AGENTS, encoding="utf-8")
    r = KBS["SCOPE"]
    r.mkdir()
    claim(r, "CL-0001", statement="IPC 使用 v2")
    claim(r, "CL-0002", statement="Vision 在 Linux main 仍使用 IPC v1,預計 2027-09-30 退場", lifecycle="deprecated", retire_when="2027-09-30", project="vision", platform="linux", branch="main")
    claim(r, "CL-0003", statement="Windows 上 IPC v2 尚未提供,使用 v1", platform="windows")
    claim(r, "CL-0004", statement="LTS 分支維持 IPC v1 不升級", branch="lts")
    claim(r, "CL-0005", statement="Windows LTS 使用 IPC v1,只做安全修補", platform="windows", branch="lts")
    shutil.copy(V1 / "kb.py", r / "kb.py")
    shutil.copy(V1 / "AGENTS.md", r / "AGENTS.md")
    subprocess.run([sys.executable, "-X", "utf8", str(r / "kb.py"), "build"], env=dict(os.environ, KB_ROOT=str(r), PYTHONIOENCODING="utf-8"), check=True)
    for n in ("V1", "SCOPE"):  # 清空 state,避免殘留
        shutil.rmtree(KBS[n] / "state", ignore_errors=True)
    print("setup ok")


def score_scope(qid, ans):
    ask = bool(re.search("請問|請告訴|請提供|需要知道|需要確認|想確認|哪個專案|哪個平台|哪個分支|[?？]", ans))
    dims = sum(1 for k in (r"專案|project", r"平台|platform", r"分支|branch") if re.search(k, ans, re.I))
    if qid == "SQ1":  # 缺 scope:應反問,或至少列出多種情境而不是只答 v2
        return ask and dims >= 2 and "v1" in ans and "v2" in ans
    if qid == "SQ2":
        return "CL-0002" in ans and "v1" in ans and "2027-09-30" in ans
    if qid == "SQ3":
        return "CL-0005" in ans and "v1" in ans
    if qid == "SQ4":  # audio/windows/main:project 與 branch 不影響 → CL-0003 勝出 v1
        return "CL-0003" in ans and "v1" in ans
    return False


def run_one(cond, qid, text):
    kb = KBS["SCOPE" if cond == "SCOPE" else cond]
    tools = ["Grep", "Glob", "Read"] if cond == "CTRL" else [f"Bash(python kb.py {sub}:*)" for sub in ("search", "resolve", "unfound")] + ["Grep", "Glob", "Read"]  # 不含 approve / reject / build / lint
    cmd = ["claude", "-p", "--model", "claude-haiku-5-5", "--effort", "low", "--output-format", "json", "--no-session-persistence",
           "--setting-sources", "project", "--disable-slash-commands", "--permission-mode", "dontAsk", "--allowedTools", *tools]
    env = dict(os.environ, PYTHONIOENCODING="utf-8", KB_USER="agent")
    prompt = ("【工具規則】Bash 一次只執行單一 `python kb.py ...` 指令,不要用 ; && | 串接。\n" if cond != "CTRL" else "") + ra.BASE + text
    t0 = time.time()
    try:
        p = subprocess.run(cmd, input=prompt, cwd=str(kb), env=env, capture_output=True, text=True, encoding="utf-8", timeout=600)
        out = p.stdout
    except subprocess.TimeoutExpired:
        out = ""
    wall = time.time() - t0
    LOG.mkdir(exist_ok=True)
    (LOG / f"{cond}_{qid}.json").write_text(out, encoding="utf-8")
    try:
        j = json.loads(out)
        ans, turns, cost, den = j.get("result", ""), j.get("num_turns"), j.get("total_cost_usd", 0), len(j.get("permission_denials", []))
    except Exception:  # noqa: BLE001
        ans, turns, cost, den = "PARSE-ERROR", None, 0, 0
    (LOG / f"{cond}_{qid}.answer.txt").write_text(ans, encoding="utf-8")
    if qid == "X1":
        ok = bool(re.search(r"沒有|找不到|未收錄|無相關|不在", ans)) and not re.search(r"\d{3,}\s*(元|NT|美)", ans)
    elif qid.startswith("SQ"):
        ok = score_scope(qid, ans)
    elif qid == "M1":
        ok = len(set(re.findall(r"CL-\d{4}", ans)) & ra.M1_GOLD) >= 4
    else:
        ok = all(re.search(r, ans) for r in ra.MUST[qid])
    return dict(cond=cond, qid=qid, ok=bool(ok), turns=turns, cost=round(cost, 4), wall=round(wall, 1), denials=den)


def main():
    conds = sys.argv[2:] or ["CTRL", "V1", "SCOPE"]
    qmap = {q[0]: q[2] for q in queries.Q}
    jobs = []
    for c in conds:
        if c == "SCOPE":
            jobs += [(c, q, t) for q, t in SQ]
        else:
            jobs += [(c, q, qmap[q]) for q in ra.QIDS] + [(c, X1[0], X1[1])]
    with ThreadPoolExecutor(5) as ex:
        res = list(ex.map(lambda a: run_one(*a), jobs))
    LOG.mkdir(exist_ok=True)
    with open(LOG / "summary.jsonl", "a", encoding="utf-8") as fh:
        for r in res:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    for c in conds:
        rs = [r for r in res if r["cond"] == c]
        print(c, f"{sum(r['ok'] for r in rs)}/{len(rs)}", f"avg turns {sum((r['turns'] or 0) for r in rs) / len(rs):.1f}", f"cost {sum(r['cost'] for r in rs):.3f}",
              "failed:", [r["qid"] for r in rs if not r["ok"]], "denials", sum(r["denials"] for r in rs))


if __name__ == "__main__":
    setup() if sys.argv[1] == "setup" else main()
