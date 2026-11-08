"""Haiku(low) 當查詢者,在四種 KB/工具條件下回答同一批問題並自動評分。用法:python run_agents.py [條件字母...]"""
import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import queries

LOG = HERE / "logs_agents"
LOG.mkdir(exist_ok=True)
QIDS = ["G1", "G2", "G5", "G6", "G7", "G8", "G11", "N1", "N2", "N5", "S1", "S2", "S4", "M1", "E1", "E4"]
TOOLS = {"A": ["Grep", "Glob", "Read"], "B": ["Grep", "Glob", "Read"],
         "C": ["Bash(python kbsearch.py:*)", "Read"], "D": ["Bash(python kbsearch.py:*)", "Read"],
         "E": ["Bash(python kbsearch.py:*)", "Grep", "Glob", "Read"], "F": ["Bash(python kbsearch.py:*)", "Grep", "Glob", "Read"]}
BASE = ("你是 framework 以外部門的工程師,不熟內部細節。cwd 是 framework 團隊的知識庫,先讀 AGENTS.md。請用知識庫查證後,用白話回答下面的問題;"
        "答案要附出處(claim id),並說明該結論是否仍然有效(claim 可能已被取代)。資料找不到就明說找不到,不要猜。\n問題:")
# 評分:must 全部命中才算對(regex,對答案全文);M1 另算引用 id 數
MUST = {
    "G1": [r"CL-0006"], "G2": [r"CL-0018"], "G5": [r"CL-0007"], "G6": [r"250"], "G7": [r"CL-0021", r"取消|不支援|不做"],
    "G8": [r"CL-0025", r"2027"], "G11": [r"CL-0010"], "N1": [r"CL-0011", r"不得|不可|不能|作廢"], "N2": [r"250"],
    "N5": [r"CL-0029", r"2027", r"尚未|未決|評估"], "S1": [r"250", r"調整|不再|已改|修正|不對|不是|過期|取代"],
    "S2": [r"CL-0011|作廢", r"不得|不可|不能|關閉|作廢"], "S4": [r"CL-0025|deprecated|棄用", r"不得|不可|不能|移除"],
    "E1": [r"CL-0016"], "E4": [r"CL-0025", r"2027"],
}
M1_GOLD = {"CL-0006", "CL-0007", "CL-0016", "CL-0018", "CL-0011"}


def run(cond, qid, text):
    kb = HERE / "kbs" / cond
    name = f"{cond}_{qid}"
    cmd = ["claude", "-p", "--model", "claude-haiku-5-5", "--effort", "low", "--output-format", "json", "--no-session-persistence",
           "--setting-sources", "project", "--disable-slash-commands", "--permission-mode", "dontAsk", "--allowedTools", *TOOLS[cond]]
    env = dict(os.environ, PYTHONIOENCODING="utf-8", KBX_MODE="file" if cond == "D" else "inline", KBX_COLLAPSE="1" if cond == "F" else "0",
               KBX_PYLIB=os.environ["KBX_PYLIB"], FASTEMBED_CACHE_PATH=os.environ["FASTEMBED_CACHE_PATH"])
    prompt = ("【工具規則】Bash 一次只執行單一 `python kbsearch.py ...` 指令,不要用 ; && | 串接。\n" if cond in "CDEF" else "") + BASE + text
    t0 = time.time()
    try:
        p = subprocess.run(cmd, input=prompt, cwd=str(kb), env=env, capture_output=True, text=True, encoding="utf-8", timeout=600)
        out = p.stdout
    except subprocess.TimeoutExpired:
        out = ""
    wall = time.time() - t0
    (LOG / f"{name}.json").write_text(out, encoding="utf-8")
    try:
        j = json.loads(out)
        ans, turns, cost = j.get("result", ""), j.get("num_turns"), j.get("total_cost_usd", 0)
        den = len(j.get("permission_denials", []))
    except Exception:  # noqa: BLE001
        ans, turns, cost, den = "PARSE-ERROR", None, 0, 0
    (LOG / f"{name}.answer.txt").write_text(ans, encoding="utf-8")
    if qid == "M1":
        ids = set(re.findall(r"CL-\d{4}", ans)) & M1_GOLD
        ok = len(ids) >= 4
    else:
        ok = all(re.search(r, ans) for r in MUST[qid])
    return dict(cond=cond, qid=qid, ok=bool(ok), turns=turns, cost=round(cost, 4), wall=round(wall, 1), denials=den)


if __name__ == "__main__":
    conds = sys.argv[1:] or list("ABCD")
    qmap = {q[0]: q[2] for q in queries.Q}
    jobs = [(c, q, qmap[q]) for c in conds for q in QIDS]
    with ThreadPoolExecutor(5) as ex:
        res = list(ex.map(lambda a: run(*a), jobs))
    f = LOG / "summary.jsonl"
    with open(f, "a", encoding="utf-8") as fh:
        for r in res:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    for c in conds:
        rs = [r for r in res if r["cond"] == c]
        print(c, f"{sum(r['ok'] for r in rs)}/{len(rs)}", f"avg turns {sum((r['turns'] or 0) for r in rs)/len(rs):.1f}", f"cost {sum(r['cost'] for r in rs):.3f}")
