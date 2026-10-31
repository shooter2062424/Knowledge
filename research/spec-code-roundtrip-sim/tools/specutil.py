"""共用:載入規格、計算指定 Release 的有效參數、評估內部約束。"""
import importlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def rel_num(release: str) -> int:
    """'Rel-21' -> 21。"""
    return int(release.split("-")[1])


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def effective_params(ext_spec: dict, release: str) -> dict[str, Any]:
    """合併 <= release 的所有版本參數(後版覆蓋前版)。

    Args:
        ext_spec: 外部規格(含 by_release)。
        release: 目標版本,如 "Rel-21"。

    Returns:
        參數名稱到值的字典。
    """
    out: dict[str, Any] = {}
    for req in ext_spec["requirements"]:
        for rel in sorted(req["by_release"], key=rel_num):
            if rel_num(rel) <= rel_num(release):
                out.update(req["by_release"][rel].get("params", {}))
    return out


def param_owner(ext_spec: dict, release: str) -> dict[str, str]:
    """參數名稱 -> 所屬需求 ID。"""
    owner: dict[str, str] = {}
    for req in ext_spec["requirements"]:
        for rel, body in req["by_release"].items():
            if rel_num(rel) <= rel_num(release):
                for p in body.get("params", {}):
                    owner[p] = req["id"]
    return owner


def eval_constraints(internal: dict, pkg: str, ext: dict[str, Any]) -> list[dict]:
    """對指定程式套件評估每條內部決定的約束。

    Args:
        internal: 內部規格。
        pkg: 套件名稱,如 "modem_v2"。
        ext: 有效的外部參數。

    Returns:
        每條決定的 {id, ok, detail}。
    """
    code = SimpleNamespace(**{m: importlib.import_module(f"{pkg}.{m}") for m in ("codec", "fsm", "sched")})
    results = []
    for d in internal["decisions"]:
        try:
            ok = bool(eval(d["constraint"], {"code": code, "ext": ext}))  # noqa: S307 (模擬實驗)
            detail = ""
        except Exception as e:  # noqa: BLE001
            ok, detail = False, f"約束無法求值:{e}"
        results.append({"id": d["id"], "title": d["title"], "ok": ok, "constraint": d["constraint"],
                        "owner": d.get("owner", "-"), "detail": detail})
    return results
