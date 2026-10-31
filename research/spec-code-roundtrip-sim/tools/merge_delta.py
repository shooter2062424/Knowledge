"""把外部規格 delta 合併進規格書,並產出影響分析報告。

做的事:
 1. 把 delta 的 ADD/MODIFY 合併成 by_release 結構(舊版內容完整保留,可隨時查 Rel-20)。
 2. 用既有程式的追溯索引(extract_spec 輸出)列出每條變更影響的常數/函式/測試。
 3. 偵測編碼風險:被 MODIFY 的條目若帶有 *_BITS 常數,代表位元佈局可能被誤改。
 4. 用「內部規格約束」對合併後的外部參數求值,列出與既有程式衝突的內部決定。

用法:python tools/merge_delta.py <現行程式套件> <delta.json> [--write]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from specutil import eval_constraints, effective_params, load_json  # noqa: E402


def merge(ext: dict, delta: dict) -> dict:
    rel = delta["release"]
    by_id = {r["id"]: r for r in ext["requirements"]}
    for ch in delta["changes"]:
        body = {"text": ch["text"], "params": ch["params"]}
        if "compat" in ch:
            body["compat"] = ch["compat"]
        if ch["op"] == "ADD":
            ext["requirements"].append({"id": ch["id"], "section": ch["section"], "kind": ch["kind"],
                                        "by_release": {rel: body}})
        else:
            by_id[ch["id"]]["by_release"][rel] = body
    return ext


def impact(data: dict, delta: dict) -> list[dict]:
    rows = []
    for ch in delta["changes"]:
        rid = ch["id"]
        consts = [c for c in data["constants"] if rid in c["tags"]]
        funcs = [f"{f['module']}.{f['name']}" for f in data["functions"] if rid in f["traces"]]
        tests = [t["name"] for t in data["tests"] if rid in t["covers"]]
        bits = [c["name"] for c in consts if c["name"].endswith("_BITS")]
        rows.append({"op": ch["op"], "id": rid, "text": ch["text"], "compat": ch.get("compat", ""),
                     "consts": [c["name"] for c in consts], "funcs": funcs, "tests": tests,
                     "encoding_risk": bits if ch["op"] == "MODIFY" else []})
    return rows


def main() -> None:
    pkg, delta_path = sys.argv[1], Path(sys.argv[2])
    delta = load_json(delta_path)
    ext = load_json(ROOT / "specs" / "ext_spec.json")
    internal = load_json(ROOT / "specs" / "internal_spec.json")
    data = json.loads((ROOT / "out" / f"extracted_{pkg}.json").read_text(encoding="utf-8"))
    merged = merge(ext, delta)
    params = effective_params(merged, delta["release"])
    rows = impact(data, delta)
    cons = eval_constraints(internal, pkg, params)

    md = [f"# {delta['release']} 影響分析(現行程式:{pkg})", "", "## 一、逐條變更影響", ""]
    for r in rows:
        md += [f"### {r['op']} {r['id']}", f"- 內容:{r['text']}", f"- 相容性條款:{r['compat'] or '(未載明)'}"]
        if r["op"] == "ADD":
            md.append("- 既有程式:🆕 全新功能,需新增程式與測試")
        else:
            md += [f"- 受影響常數:{', '.join(r['consts']) or '(無)'}",
                   f"- 受影響函式:{', '.join(r['funcs']) or '(無)'}",
                   f"- 既有測試:{', '.join(r['tests']) or '(無)'}"]
        if r["encoding_risk"]:
            md.append(f"- 🚨 編碼風險:此條目有位元寬度常數 {r['encoding_risk']};不得更動,"
                      "否則 Rel-20 golden vector 會破")
        md.append("")
    md += ["## 二、內部決定 vs 新外部規格", ""]
    for c in cons:
        md.append(f"- {'✅' if c['ok'] else '❌ 衝突'} {c['id']} {c['title']}:`{c['constraint']}`"
                  + ("" if c["ok"] else f"(外部規格不可改 ⇒ 須重新協商此內部決定;負責:{c['owner']})"))
    out = ROOT / "out" / f"impact_{delta['release']}_{pkg}.md"
    out.write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    if "--write" in sys.argv:
        (ROOT / "specs" / "ext_spec.json").write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
        print("\n已寫回 specs/ext_spec.json(Rel-20 內容保留於 by_release)")


if __name__ == "__main__":
    main()
