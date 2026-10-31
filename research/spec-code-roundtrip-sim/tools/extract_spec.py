"""code-to-spec:用 ast 從程式碼套件靜態抽出「規格現況」(常數、轉移表、追溯標註、測試覆蓋)。

用法:python tools/extract_spec.py modem_v1
輸出:out/extracted_<pkg>.json 與 out/spec_<pkg>.md
"""
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TAG_RE = re.compile(r"#\s*((?:R|D)-[A-Z]+-\d+)")


def _trace_ids(dec: ast.expr) -> list[str]:
    if isinstance(dec, ast.Call) and getattr(dec.func, "id", "") == "trace":
        return [a.value for a in dec.args if isinstance(a, ast.Constant)]
    return []


def _norm(v: Any) -> Any:
    """tuple 鍵轉成 'a|b' 字串,方便 JSON 與規格比對。"""
    if isinstance(v, dict):
        return {("|".join(k) if isinstance(k, tuple) else k): _norm(x) for k, x in v.items()}
    return v


def extract_module(path: Path, pkg: str) -> dict[str, list]:
    src = path.read_text(encoding="utf-8")
    lines = src.splitlines()
    tree = ast.parse(src)
    consts, funcs = [], []
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name.isupper():
                try:
                    value = _norm(ast.literal_eval(node.value))
                except ValueError:
                    continue
                tags = TAG_RE.findall(lines[node.lineno - 1])
                consts.append({"module": path.stem, "name": name, "value": value, "tags": tags})
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            items = [(node.name, node)] if isinstance(node, ast.FunctionDef) else \
                [(f"{node.name}.{n.name}", n) for n in node.body if isinstance(n, ast.FunctionDef)]
            class_traced = isinstance(node, ast.ClassDef) and any(
                _trace_ids(d) for _, n in items for d in n.decorator_list)
            for qn, fn in items:
                traces = [t for d in fn.decorator_list for t in _trace_ids(d)]
                is_class = isinstance(node, ast.ClassDef)
                funcs.append({
                    "module": path.stem, "name": qn, "traces": traces,
                    "public": not fn.name.startswith("_"),
                    "infra": is_class and not class_traced,
                    "doc": (ast.get_docstring(fn) or "").splitlines()[0] if ast.get_docstring(fn) else "",
                })
    return {"constants": consts, "functions": funcs}


def extract_tests(tests_dir: Path) -> list[dict]:
    out = []
    for path in sorted(tests_dir.glob("test_*.py")):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                ids = [a.value for d in node.decorator_list if isinstance(d, ast.Call)
                       and getattr(d.func, "id", "") == "covers" for a in d.args if isinstance(a, ast.Constant)]
                out.append({"file": path.name, "name": node.name, "covers": ids})
    return out


def extract(pkg: str) -> dict[str, Any]:
    data: dict[str, Any] = {"pkg": pkg, "constants": [], "functions": []}
    for path in sorted((ROOT / pkg).glob("*.py")):
        if path.stem in ("__init__", "trace"):
            continue
        part = extract_module(path, pkg)
        data["constants"] += part["constants"]
        data["functions"] += part["functions"]
    data["tests"] = extract_tests(ROOT / "tests")
    return data


def render_md(data: dict[str, Any], ext: dict, internal: dict) -> str:
    """把抽取結果與規格 ID 排成人類可讀的「反推規格書」。"""
    ids: dict[str, dict] = {r["id"]: r for r in ext["requirements"]}
    idx: dict[str, dict[str, list]] = {}
    for c in data["constants"]:
        for t in c["tags"]:
            idx.setdefault(t, {}).setdefault("consts", []).append(f"{c['name']}={c['value']}")
    for f in data["functions"]:
        for t in f["traces"]:
            idx.setdefault(t, {}).setdefault("funcs", []).append(f"{f['module']}.{f['name']}")
    for t in data["tests"]:
        for i in t["covers"]:
            idx.setdefault(i, {}).setdefault("tests", []).append(t["name"])
    out = [f"# 由程式碼反推的規格書:{data['pkg']}", "", "## 外部規格條目(R-*)", ""]
    for rid in sorted(k for k in idx if k.startswith("R-")):
        meta = ids.get(rid)
        title = "；".join(b["text"] for b in meta["by_release"].values()) if meta else "⚠️ 外部規格中查無此 ID(殘留標註)"
        out += [f"### {rid} — {title}", ""]
        for k, label in (("consts", "常數"), ("funcs", "實作"), ("tests", "測試")):
            out.append(f"- {label}:{', '.join(idx[rid].get(k, [])) or '(無)'}")
        out.append("")
    out += ["## 內部決定(D-*)", ""]
    dmap = {d["id"]: d for d in internal["decisions"]}
    for did in sorted(k for k in idx if k.startswith("D-")):
        d = dmap.get(did, {})
        out += [f"### {did} — {d.get('title', '⚠️ 內部規格查無此 ID')}", f"- 理由:{d.get('rationale', '-')}",
                f"- 常數:{', '.join(idx[did].get('consts', [])) or '(無)'}",
                f"- 實作:{', '.join(idx[did].get('funcs', [])) or '(無)'}", ""]
    untraced = [f"{f['module']}.{f['name']}" for f in data["functions"]
                if f["public"] and not f["traces"] and not f["infra"]]
    out += ["## ⚠️ 待人工判斷", "", f"- 無任何追溯標註的公開函式:{', '.join(untraced) or '無'}", ""]
    return "\n".join(out)


if __name__ == "__main__":
    pkg = sys.argv[1]
    sys.path.insert(0, str(ROOT / "tools"))
    from specutil import load_json  # noqa: E402
    d = extract(pkg)
    (ROOT / "out").mkdir(exist_ok=True)
    (ROOT / "out" / f"extracted_{pkg}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    md = render_md(d, load_json(ROOT / "specs" / "ext_spec.json"), load_json(ROOT / "specs" / "internal_spec.json"))
    (ROOT / "out" / f"spec_{pkg}.md").write_text(md, encoding="utf-8")
    print(f"extracted {pkg}: {len(d['constants'])} constants, {len(d['functions'])} functions, {len(d['tests'])} tests")
