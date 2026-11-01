"""ILN 變更影響檢查器(試點版):registry 語意 diff + 從原始碼抽 consumer manifest + 影響通知。

拿真實模組做試點用。不依賴外部套件。流程:
  1. 把兩個以上模組的 ILN 訊息整理成 registry JSON(格式見 example/registry.json)
  2. `manifest`  掃各模組原始碼,抽出「這個模組讀了哪些訊息的哪些欄位」
  3. `diff`      比較新舊 registry,把每項變更分類(靜默破壞 / 結構破壞 / 相容)
  4. `impact`    diff + manifest => 每個模組要收到什麼通知
  5. `inject`    對 registry 逐一注入變更算子,印出每個算子會通知到誰(找哪一層漏接用)

欄位讀取的辨識規則放在 config JSON(`read_patterns`):每條是一個 regex,
必須含兩個 named group `msg`(訊息名)與 `field`(欄位名),或只含 `field`(此時訊息名取檔案內
出現的第一個已知訊息名)。Python 檔另外用 ast 精確抽取 msg["x"] / msg.get("x")。

用法:
  python iln_check.py manifest <config.json> > manifest.json
  python iln_check.py diff <old_registry.json> <new_registry.json>
  python iln_check.py impact <old_registry.json> <new_registry.json> <manifest.json>
  python iln_check.py inject <registry.json> <manifest.json>
"""
from __future__ import annotations

import ast
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any

SEMANTIC_KEYS = ("kind", "unit", "base", "scale", "true_val", "map", "default", "optional", "lo", "hi")


# ───────────────────────── registry 語意 diff ─────────────────────────
def classify(old_f: dict[str, Any], new_f: dict[str, Any]) -> list[tuple[str, str]]:
    """比較同一欄位新舊規格,回傳 [(類別, 說明)]。類別: silent(型別不變但語意變)/ loud(結構破壞)/ compat。"""
    out: list[tuple[str, str]] = []
    if old_f.get("kind") != new_f.get("kind"):
        return [("loud", f"kind {old_f.get('kind')} -> {new_f.get('kind')}")]
    for k in ("unit", "base", "scale", "true_val", "default"):
        if old_f.get(k) != new_f.get(k):
            out.append(("silent", f"{k} {old_f.get(k)!r} -> {new_f.get(k)!r}"))
    if old_f.get("kind") == "enum":
        om, nm = old_f.get("map", {}), new_f.get("map", {})
        for s, v in om.items():
            if s not in nm:
                out.append(("loud", f"enum 符號 {s} 移除"))
            elif nm[s] != v:
                out.append(("silent", f"enum {s}: {v} -> {nm[s]}"))
        for s in nm:
            if s not in om:
                out.append(("silent", f"enum 新增符號 {s}(舊 consumer 的 UNKNOWN/strict 處理可能不對)"))
    for k in ("lo", "hi"):
        if old_f.get(k) != new_f.get(k):
            out.append(("silent", f"{k} {old_f.get(k)} -> {new_f.get(k)}(consumer 的上限/陣列大小可能不夠)"))
    if old_f.get("optional") != new_f.get("optional"):
        out.append(("compat" if new_f.get("optional") else "loud", f"optional -> {new_f.get('optional')}"))
    return out


def diff_registry(old: dict[str, Any], new: dict[str, Any]) -> list[dict[str, Any]]:
    """回傳變更清單 [{msg, field, cls, note}]。msg 層級的 latency/seq/positional 變更用 field='*'。"""
    items: list[dict[str, Any]] = []
    for m, om in old.items():
        nm = new.get(m)
        if nm is None:
            items.append({"msg": m, "field": "*", "cls": "loud", "note": "整個訊息被移除"})
            continue
        for key in ("latency_us", "seq"):
            if om.get(key) != nm.get(key):
                items.append({"msg": m, "field": "*", "cls": "silent", "note": f"{key} {om.get(key)} -> {nm.get(key)}"})
        if om.get("positional") and list(om["fields"]) != list(nm["fields"])[:len(om["fields"])]:
            items.append({"msg": m, "field": "*", "cls": "loud", "note": "positional 訊息欄位順序/刪除"})
        for f, of in om["fields"].items():
            if f not in nm["fields"]:
                items.append({"msg": m, "field": f, "cls": "loud", "note": "欄位移除或改名"})
                continue
            for cls, note in classify(of, nm["fields"][f]):
                items.append({"msg": m, "field": f, "cls": cls, "note": note})
        for f, nf in nm["fields"].items():
            if f not in om["fields"]:
                items.append({"msg": m, "field": f, "cls": "compat" if nf.get("optional") else "loud",
                              "note": "新增欄位" + ("(optional)" if nf.get("optional") else "(required,舊 producer/consumer 皆受影響)")})
    return items


# ───────────────────────── 從原始碼抽 manifest ─────────────────────────
def py_reads(src: str) -> set[str]:
    """Python:用 ast 抓 x["f"] 與 x.get("f"),不限變數名(試點用,寬鬆)。"""
    reads: set[str] = set()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return reads
    for n in ast.walk(tree):
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, str):
            reads.add(n.slice.value)
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get" \
                and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
            reads.add(n.args[0].value)
    return reads


def build_manifest(cfg: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    """依 config 掃各模組檔案,輸出 {module: {msg: [fields]}}。無法判定訊息的讀取歸 '?'。"""
    pats = [re.compile(p) for p in cfg.get("read_patterns", [])]
    msg_names = set(registry)
    out: dict[str, dict[str, set[str]]] = {}
    for mod, spec in cfg["modules"].items():
        root = Path(cfg.get("root", ".")) / spec["path"]
        files = [p for p in root.rglob("*") if p.is_file() and p.suffix in tuple(spec.get("suffixes", [".c", ".h", ".cpp", ".hpp", ".py"]))]
        mm: dict[str, set[str]] = {}
        for p in files:
            src = p.read_text(encoding="utf-8", errors="replace")
            mentioned = [m for m in msg_names if re.search(rf"\b{re.escape(m)}\b", src)]
            fields: set[tuple[str, str]] = set()
            # 變數型別表: `const ILN_X *g` / `ILN_X &cfg` => g/cfg 屬於 ILN_X(讓 g->field 能判出訊息)
            names_rx = "|".join(re.escape(m) for m in sorted(msg_names, key=len, reverse=True))
            var2msg = {g.group("var"): g.group("msg") for g in
                       re.finditer(rf"\b(?P<msg>{names_rx})\b\s*(?:const\s*)?[&*]*\s*(?P<var>[A-Za-z_]\w*)", src)} if names_rx else {}
            for rx in pats:
                for g in rx.finditer(src):
                    gd = g.groupdict()
                    msg_of = (gd.get("msg") or var2msg.get(gd.get("var") or "")
                              or (mentioned[0] if len(mentioned) == 1 else "?"))
                    fields.add((msg_of, gd["field"]))
            if p.suffix == ".py":
                fields |= {((mentioned[0] if len(mentioned) == 1 else "?"), f) for f in py_reads(src)}
            for m, f in fields:
                # 只收 registry 裡確實有的欄位名(過濾掉 ->next 之類的雜訊);訊息判不出來的歸 '?'
                known = {x for s_ in registry.values() for x in s_["fields"]} if m == "?" else set(registry.get(m, {}).get("fields", {}))
                if f in known:
                    mm.setdefault(m, set()).add(f)
        out[mod] = mm
    # 只保留 registry 認得的訊息;'?' 保留供人工檢視
    return {mod: {m: sorted(fs) for m, fs in mm.items() if m in registry or m == "?"} for mod, mm in out.items()}


# ───────────────────────── 影響通知 ─────────────────────────
def impact(changes: list[dict[str, Any]], manifest: dict[str, Any], registry: dict[str, Any]) -> dict[str, list[str]]:
    """每個模組該收到的通知。

    規則: msg 層級變更通知所有消費該訊息的模組;欄位層級只通知讀到該欄位的模組;
    manifest 中訊息為 '?' 的模組(無法判定)保守地全部通知。
    """
    notes: dict[str, list[str]] = {}
    for ch in changes:
        if ch["cls"] == "compat":
            continue
        for mod, mm in manifest.items():
            reads = mm.get(ch["msg"])
            hit = reads is not None and (ch["field"] == "*" or ch["field"] in reads)
            unsure = "?" in mm and not hit
            if hit or unsure:
                tag = "" if hit else "(manifest 無法判定訊息,保守通知)"
                notes.setdefault(mod, []).append(f"[{ch['cls']}] {ch['msg']}.{ch['field']}: {ch['note']}{tag}")
    return notes


# ───────────────────────── 變更注入(找漏接) ─────────────────────────
def inject_ops(reg: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """對 registry 的每個欄位套用可套用的變更算子,回傳 [(說明, 新 registry)]。"""
    out: list[tuple[str, dict[str, Any]]] = []
    for m, spec in reg.items():
        for f, fs in spec["fields"].items():
            k = fs.get("kind")
            cands: list[tuple[str, Any]] = []
            if k == "time" and fs.get("unit") in ("ms", "us", "s"):
                new_unit = "us" if fs["unit"] != "us" else "ms"
                cands.append((f"unit {fs['unit']}->{new_unit}", lambda x, u=new_unit: x.update(unit=u)))
            if k == "scaled":
                cands.append(("scale/2", lambda x: x.update(scale=x["scale"] / 2, hi=x.get("hi", 0) * 2)))
            if k == "flag":
                cands.append(("flag 極性反轉", lambda x: x.update(true_val=1 - x["true_val"])))
            if k == "index":
                cands.append(("index base 0<->1", lambda x: x.update(base=1 - x["base"], lo=x.get("lo", 0) + (1 - 2 * x["base"]), hi=x.get("hi", 0) + (1 - 2 * x["base"]))))
            if k == "enum" and fs.get("map"):
                cands.append(("enum 新增符號", lambda x: x["map"].update({"NEW_SYM": max(x["map"].values()) + 1})))
                if len(fs["map"]) >= 2:
                    cands.append(("enum 兩值互換", lambda x: _swap_enum(x)))
            if k in ("time", "index", "scaled") and "hi" in fs:
                cands.append(("範圍上限放寬 x2+1", lambda x: x.update(hi=x["hi"] * 2 + 1)))
            if fs.get("optional") and "default" in fs:
                cands.append(("default +1", lambda x: x.update(default=(x["default"] + 1) if isinstance(x["default"], (int, float)) else x["default"])))
            for label, fn in cands:
                new = copy.deepcopy(reg)
                fn(new[m]["fields"][f])
                out.append((f"{m}.{f}: {label}", new))
        out.append((f"{m}: latency x3", _with(reg, m, latency_us=spec.get("latency_us", 100) * 3)))
    return out


def _swap_enum(x: dict[str, Any]) -> None:
    a, b = list(x["map"])[:2]
    x["map"][a], x["map"][b] = x["map"][b], x["map"][a]


def _with(reg: dict[str, Any], m: str, **kw: Any) -> dict[str, Any]:
    new = copy.deepcopy(reg)
    new[m].update(kw)
    return new


# ───────────────────────── CLI ─────────────────────────
def _load(p: str) -> Any:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "manifest":
        cfg = _load(argv[2])
        cfg["root"] = (Path(argv[2]).resolve().parent / cfg.get("root", ".")).as_posix()  # root 相對於 config 檔
        reg = _load((Path(cfg["root"]) / cfg["registry"]).as_posix())
        print(json.dumps(build_manifest(cfg, reg), ensure_ascii=False, indent=1))
    elif cmd == "diff":
        for ch in diff_registry(_load(argv[2]), _load(argv[3])):
            print(f"{ch['cls']:7s} {ch['msg']}.{ch['field']}: {ch['note']}")
    elif cmd == "impact":
        old, new, man = _load(argv[2]), _load(argv[3]), _load(argv[4])
        notes = impact(diff_registry(old, new), man, old)
        for mod, ls in sorted(notes.items()):
            print(f"== {mod}")
            for line in ls:
                print("  " + line)
        if not notes:
            print("沒有模組需要通知")
    elif cmd == "inject":
        reg, man = _load(argv[2]), _load(argv[3])
        print(f"{'注入的變更':44s} 通知到的模組")
        for label, new in inject_ops(reg):
            notes = impact(diff_registry(reg, new), man, reg)
            print(f"{label:44s} {', '.join(sorted(notes)) or '(沒人被通知)'}")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
