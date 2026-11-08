"""用 headless Haiku 產生:①ingest 階段的 claim aliases(doc-side expansion)②查詢擴充(query-side expansion)。

用法:python gen_llm.py alias | qexp
"""
import json, os, re, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import corpus, queries

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)
EMPTY = Path(tempfile.mkdtemp(prefix="kbx_empty_"))


def ask(prompt: str) -> tuple[str, float]:
    cmd = ["claude", "-p", "--model", "claude-haiku-5-5", "--effort", "low", "--output-format", "json", "--no-session-persistence",
           "--setting-sources", "project", "--disable-slash-commands", "--permission-mode", "dontAsk", "--allowedTools", "Read"]
    p = subprocess.run(cmd, input=prompt, cwd=str(EMPTY), capture_output=True, text=True, encoding="utf-8", timeout=300,
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    j = json.loads(p.stdout)
    return j.get("result", ""), j.get("total_cost_usd", 0.0)


def jload(s: str):
    m = re.search(r"\{[\s\S]*\}", s)
    return json.loads(m.group(0))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "alias":
        cl = [u for u in corpus.seed_units() if u["kind"] == "claim"]
        lines = "\n".join(f"{u['uid']}: {u['text']}" for u in cl)
        prompt = ("你在替團隊知識庫的每條 claim 加上『檢索別名』,讓別人用不同說法也找得到。對下列每條 claim,輸出 6–12 個別名詞或短語,空白分隔:"
                  "口語說法、同義詞、中文與英文互換(例如 mutex 與 互斥鎖)、常見的換字問法。不要重複 claim 原有的詞,不要加入原文沒有的事實。"
                  "只輸出一個 JSON 物件:{\"CL-0001\": \"別名 別名 ...\", ...},不要其他文字。\n\n" + lines)
        ans, cost = ask(prompt)
        d = jload(ans)
        (OUT / "aliases.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(len(d), "aliases, cost", cost)
    elif mode == "qexp":
        def one(q):
            qid, _, text, _, _ = q
            prompt = ("你是團隊知識庫的檢索助手。把下列問句改寫成一組檢索關鍵詞,涵蓋同義詞、口語說法、中英對照與可能出現在文件裡的專有詞,"
                      "8–15 個詞,空白分隔,只輸出關鍵詞一行,不要其他文字。\n問句:" + text)
            ans, cost = ask(prompt)
            return qid, ans.strip().splitlines()[0] if ans.strip() else "", cost
        with ThreadPoolExecutor(5) as ex:
            res = list(ex.map(one, queries.Q))
        (OUT / "qexp.json").write_text(json.dumps({r[0]: r[1] for r in res}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(len(res), "qexp, cost", round(sum(r[2] for r in res), 3))
