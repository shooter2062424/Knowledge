"""E3:寫入路徑。Haiku 依 AGENTS.md 把 8 段(虛構)會議摘錄提案成 claim(自己產 aliases),人核准後,
用「刻意不含 claim 關鍵詞」的換說法問句與英文問句檢索,對照「把 aliases 拿掉」的同一批 claim。
用法:python experiments/e3_write_path.py
"""
import json, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE.parent
SB = V1.parent / "data" / "sandbox"
SRC, DST = SB / "v1kb", SB / "v1kb_write"

ITEMS = [  # (摘錄, 換說法問句, 英文問句)
    ("【週會 M20】結論:遙測資料每 30 秒批次上傳一次;上傳失敗時本地最多暫存 200MB,超過就丟掉最舊的。", "資料送不出去的時候會先存多少在本機?", "how much data is buffered when upload fails"),
    ("【週會 M20】結論:TLS 憑證有效期縮短為 90 天,由資安組在到期前 14 天自動更新。", "加密證書多久要換一次?", "certificate rotation interval"),
    ("【週會 M20】結論:CI 規定合併前單元測試覆蓋率必須達 80% 以上,低於者 PR 不可合併。", "程式碼被測試涵蓋的比例不夠可以送出嗎?", "minimum test coverage to merge"),
    ("【週會 M21】結論:韌體升級採 A/B 雙分區;升級失敗自動回滾到舊分區,回滾須在 60 秒內完成。", "更新壞掉的話怎麼退回去、要多久?", "firmware update rollback time limit"),
    ("【週會 M21】結論:資料庫每日 02:00 做增量備份、每週日做完整備份,備份保留 35 天。", "存檔副本要留多久?", "database backup retention period"),
    ("【週會 M21】結論:API 請求逾時預設 5 秒,失敗最多重試 3 次,採指數退避。", "請求等不到回應會重打幾次?", "api retry policy"),
    ("【週會 M22】結論:程式碼審查至少需要 2 位 reviewer,其中 1 位必須是該模組的 owner。", "改動送審要幾個人看過才行?", "required reviewers for a change"),
    ("【週會 M22】結論:感測器校正週期為 6 個月,逾期未校正的裝置不得出貨。", "設備多久要重新校準一次?", "sensor calibration interval"),
]


def kbcmd(root, *args, user="human"):
    return subprocess.run([sys.executable, "-X", "utf8", str(root / "kb.py"), *args], capture_output=True, text=True, encoding="utf-8",
                          env=dict(os.environ, KB_ROOT=str(root), KB_USER=user, PYTHONIOENCODING="utf-8"))


def propose(i, item):
    prompt = ("先讀 AGENTS.md。下面是一段會議摘錄,請依 AGENTS.md 的寫入規則,用 kb.py propose 把其中的結論提案到知識庫(只提一條,subject 請用貼切的英文小寫短詞)。"
              "source 請寫 M2X@00:00 格式(摘錄標題的會議編號)、valid-from 用 2026-11-08、author 用 ai:haiku。若被 gate 退回,依訊息修正後再提一次。\n摘錄:" + item[0])
    cmd = ["claude", "-p", "--model", "claude-haiku-5-5", "--effort", "low", "--output-format", "json", "--no-session-persistence",
           "--setting-sources", "project", "--disable-slash-commands", "--permission-mode", "dontAsk", "--allowedTools", "Bash(python kb.py search:*)", "Bash(python kb.py propose:*)", "Bash(python kb.py template:*)", "Read", "Grep"]
    p = subprocess.run(cmd, input=prompt, cwd=str(DST), capture_output=True, text=True, encoding="utf-8", timeout=600,
                       env=dict(os.environ, PYTHONIOENCODING="utf-8", KB_USER="ai:haiku"))
    try:
        j = json.loads(p.stdout)
        (SB / "logs_v1").mkdir(exist_ok=True)
        (SB / "logs_v1" / f"e3_{i}.txt").write_text(j.get("result", "") + chr(10) + json.dumps(j.get("permission_denials", []), ensure_ascii=False), encoding="utf-8")
        return i, j.get("num_turns"), j.get("total_cost_usd", 0), len(j.get("permission_denials", []))
    except Exception:  # noqa: BLE001
        return i, None, 0, 0


def main():
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("state"))
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda a: propose(*a), enumerate(ITEMS)))
    print("agent turns/cost/denials:", [(r[1], round(r[2], 3), r[3]) for r in res], "total cost", round(sum(r[2] for r in res), 3))
    inbox = sorted((DST / "inbox").glob("P-*.md"))
    print("inbox 提案數:", len(inbox), "/ 8")
    for f in inbox:
        r = kbcmd(DST, "approve", f.stem, user="human")
        if r.returncode:
            print("approve 失敗", f.stem, r.stdout.strip()[:120], r.stderr.strip()[:120])
    sys.path.insert(0, str(V1))
    os.environ["KB_ROOT"] = str(DST)
    import kb
    claims = kb.load_claims()
    new = [c for c in claims.values() if c.get("author") == "ai:haiku"]
    print("核准後新 claim 數:", len(new))
    for c in new:
        has_en = any(re.search(r"[A-Za-z]{3,}", a) for a in c["aliases"])
        print(f"- {c['id']} subject={c['subject']} aliases={len(c['aliases'])} 含英文={has_en} :: {c['statement'][:50]} :: {', '.join(c['aliases'])[:150]}")
    # 檢索:對每條新 claim 找到它對應的摘錄(用最相近的結論詞匹配 id),再比較有/無別名
    def rank_of(claims_, target, q):
        ids = list(claims_)
        r = kb.rank_claims(claims_, ids, q)
        order = [ids[i] for i, _ in r]
        return order.index(target) + 1 if target in order else 999
    import copy
    stripped = copy.deepcopy(claims)
    for c in stripped.values():
        if c.get("author") == "ai:haiku":
            c["aliases"] = []
    tot = {"paraphrase": [0, 0], "english": [0, 0]}
    key_terms = ["遙測|上傳", "憑證|TLS", "覆蓋率", "韌體|回滾", "備份", "逾時|重試", "reviewer|審查", "校正"]
    for (txt, qp, qe), kt in zip(ITEMS, key_terms):
        tgt = next((c["id"] for c in new if re.search(kt, c["statement"])), None)
        if not tgt:
            print("找不到對應 claim:", kt)
            continue
        for kind, q in (("paraphrase", qp), ("english", qe)):
            ra_, rb_ = rank_of(claims, tgt, q), rank_of(stripped, tgt, q)
            tot[kind][0] += ra_ <= 3
            tot[kind][1] += rb_ <= 3
            print(f"  {kind:10} {q[:28]:28} 有別名名次={ra_:>3} 無別名名次={rb_:>3}")
    print("hit@3 有別名/無別名:", {k: f"{v[0]}/8 vs {v[1]}/8" for k, v in tot.items()})
    r = kbcmd(DST, "lint")
    print("lint(新增部分摘要):", [ln for ln in r.stdout.splitlines() if "ALIASES" in ln or "SHADOW" in ln][:5], r.stdout.splitlines()[-1])


if __name__ == "__main__":
    main()
