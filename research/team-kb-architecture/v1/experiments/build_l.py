"""把第四輪的 L 規模語料(30 條 seed claim + 1,500 合成同詞彙干擾 + 1,500 雜訊 + 12 場會議)轉成 v1 格式。

產出到 data/sandbox/v1kb/(不進版控):claims/*.md(v1 格式)、notes/(雜項,可 grep)、raw/meetings/、AGENTS.md、kb.py。
用法:python experiments/build_l.py [--no-alias]   (--no-alias 產生沒有別名的對照版 v1kb_noalias)
"""
import json, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE.parent
TK = V1.parent
sys.path.insert(0, str(TK / "lab4"))
import corpus  # noqa: E402
import yaml  # noqa: E402

ALIAS = json.loads((TK / "data/sandbox/sim4/out/aliases.json").read_text(encoding="utf-8"))
SEED_DIR = TK / "data/sandbox/kb/claims"
MODS = set(corpus.MODS)


def main(alias: bool = True):
    out = TK / "data" / "sandbox" / ("v1kb" if alias else "v1kb_noalias")
    if out.exists():
        shutil.rmtree(out)
    (out / "claims").mkdir(parents=True)
    seeds = {}
    for f in SEED_DIR.glob("CL-*.md"):
        seeds[f.stem] = yaml.safe_load(f.read_text(encoding="utf-8").split("---")[1])
    units = corpus.build("L", ALIAS if alias else None)
    easy = []
    for u in units:
        if u["kind"] == "claim":
            s = seeds[u["uid"]]
            al = ALIAS.get(u["uid"], "").split() if alias else []
            # 別名在第四輪是空白分隔;v1 用逗號分隔(英文片語不被切碎)
            fm = {"id": u["uid"], "concept": s["subject"], "subject": s["subject"], "statement": u["text"], "lifecycle": "active",
                  "valid_from": str(s["valid_from"]), "supersedes": ", ".join(s.get("supersedes") or []), "aliases": ", ".join(al),
                  "source": s["source"], "author": "seed"}
        elif u["kind"] == "noise_hard":
            m = re.match(r"(\w+) ", u["text"])
            proj = m.group(1) if m and m.group(1) in MODS else "*"
            al = u["alias"].split() if alias else []
            fm = {"id": u["uid"], "concept": "ops", "subject": "ops", "statement": u["text"], "lifecycle": "active", "project": proj,
                  "valid_from": "2026-05-01", "aliases": ", ".join(al), "source": "synthetic", "author": "seed"}
        elif u["kind"] == "noise_easy":
            easy.append(u["text"])
            continue
        else:
            continue
        lines = [f"{k}: {v}" for k, v in fm.items() if v not in ("", None)]
        (out / "claims" / f"{fm['id']}.md").write_text("---\n" + "\n".join(lines) + "\n---\n", encoding="utf-8")
    (out / "notes").mkdir()
    for i in range(0, len(easy), 50):
        (out / "notes" / f"note-{i // 50:03d}.md").write_text("# 雜項筆記\n" + "\n".join("- " + t for t in easy[i:i + 50]) + "\n", encoding="utf-8")
    shutil.copytree(corpus.SB / "kb" / "raw" / "meetings", out / "raw" / "meetings")
    shutil.copy(V1 / "kb.py", out / "kb.py")
    shutil.copy(V1 / "AGENTS.md", out / "AGENTS.md") if (V1 / "AGENTS.md").exists() else None
    import subprocess, os
    subprocess.run([sys.executable, "-X", "utf8", str(out / "kb.py"), "build"], env=dict(os.environ, KB_ROOT=str(out), PYTHONIOENCODING="utf-8"), check=True)
    print("built", out, len(list((out / "claims").glob("*.md"))), "claims")


if __name__ == "__main__":
    main("--no-alias" not in sys.argv)
