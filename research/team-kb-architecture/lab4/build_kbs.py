"""建立四個 agent 實驗用的 KB 目錄(規模 L:約 3,000 單元)。

A:純檔案(claim 檔、無 aliases),只給 Grep/Glob/Read
B:同 A,但 claim frontmatter 加 aliases(入庫端擴充)
C:同 B + kbsearch.py(BM25雙字+向量 RRF,含 supersedes 鄰居展開),結果直接印出(inline)
D:同 C,但結果寫檔、只印路徑(file-based)
"""
import json, shutil, sys, os
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
import corpus, evalret as ev

ROOT = Path(__file__).parent / "kbs"
SRC_MEET = corpus.SB / "kb" / "raw" / "meetings"

AGENTS = """# 知識庫使用說明
這是 framework 團隊的知識庫(虛構)。
- claims/CL-*.md、claims/HN*.md:一條一檔的 claim。frontmatter 的 status 為 current 表示現行;superseded 表示已被新 claim 取代(superseded_by 指向取代者)。
- raw/meetings/:會議逐字稿(不可變原始紀錄)。notes/:雜項筆記。
- 回答時請引用 claim id,並說明日期與是否仍然有效。
"""


def write_claims(kbdir: Path, units, with_alias: bool):
    cd = kbdir / "claims"
    cd.mkdir(parents=True, exist_ok=True)
    easy = []
    for u in units:
        if u["kind"] in ("claim", "noise_hard"):
            fm = [f"id: {u['uid']}", f"statement: {u['text']}", f"status: {'superseded' if u['status']=='superseded' else 'current'}"]
            if u.get("sup_by"):
                fm.append(f"superseded_by: {', '.join(u['sup_by'])}")
            if u.get("sup"):
                fm.append(f"supersedes: {', '.join(u['sup'])}")
            if u.get("source"):
                fm.append(f"source: {u['source']}")
            if with_alias and u.get("alias"):
                fm.append(f"aliases: {u['alias']}")
            (cd / f"{u['uid']}.md").write_text("---\n" + "\n".join(fm) + "\n---\n", encoding="utf-8")
        elif u["kind"] == "noise_easy":
            easy.append(u["text"])
    nd = kbdir / "notes"
    nd.mkdir(exist_ok=True)
    for i in range(0, len(easy), 50):
        (nd / f"note-{i//50:03d}.md").write_text("# 雜項筆記\n" + "\n".join("- " + t for t in easy[i:i + 50]) + "\n", encoding="utf-8")
    md = kbdir / "raw" / "meetings"
    md.mkdir(parents=True, exist_ok=True)
    for f in SRC_MEET.glob("*.md"):
        shutil.copy(f, md / f.name)
    (kbdir / "AGENTS.md").write_text(AGENTS, encoding="utf-8")


def main():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    units_a = corpus.build("L", None)
    units_b = corpus.build("L", ev.ALIAS)
    # 合成干擾也要有 alias(corpus.hard_noise 已帶);A 版移除所有 alias
    for u in units_a:
        u["alias"] = ""
    for name, units, al in (("A", units_a, False), ("B", units_b, True), ("C", units_b, True), ("D", units_b, True)):
        write_claims(ROOT / name, units, al)
    # C/D:建立索引(BM25 在 CLI 內即時建;嵌入預先算好存 npz)
    claim_units = [u for u in units_b if u["kind"] in ("claim", "noise_hard")]
    texts = [u["text"] + (" " + u["alias"] if u["alias"] else "") for u in claim_units]
    E = ev.embed(texts)
    for name in ("C", "D"):
        np.savez(ROOT / name / ".index.npz", E=E, ids=np.array([u["uid"] for u in claim_units]))
        shutil.copy(Path(__file__).parent / "kbsearch.py", ROOT / name / "kbsearch.py")
        (ROOT / name / "AGENTS.md").write_text(AGENTS + (
            "\n## 檢索工具\n`python kbsearch.py \"查詢\"`:混合檢索(關鍵字+語意),會標示 status 並附上取代鏈鄰居。查詢可多試幾種說法。\n"
            + ("結果直接印在輸出。\n" if name == "C" else "結果會寫入檔案,指令只印出檔案路徑,請用 Read 讀取該檔。\n")), encoding="utf-8")
    print("built", {n: sum(1 for _ in (ROOT / n / "claims").glob("*.md")) for n in "ABCD"})


if __name__ == "__main__":
    main()
