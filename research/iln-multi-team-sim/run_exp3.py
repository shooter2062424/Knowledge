"""實驗 3:讓 headless Claude(Haiku)當「consumer 團隊成員」,看收到不同程度的通知時能否正確跟上 producer 的變更。

三種通知程度(同一批變更、同一份 consumer 原始碼):
  N0 silent : 只給最新 registry 條目,沒說有變更(團隊只改自己的 spec、沒人通知)
  N1 notify : 加一句「你吃的訊息 Mx 更新了」(manifest 比對後的自動通知,不含細節)
  N2 diff   : N1 + registry 條目的 old→new diff(ICR 內容)
另有「安全變更」對照組(consumer 其實不會壞),量測 agent 會不會把本來好的碼改壞。

評分:把 agent 改好的 handle 換進系統,用稠密取樣(含邊界)只跑該 consumer,物理真值全對才算過。
另記錄 ASSUME(consumer 宣告的假設)是否也同步到新規格(spec↔code 一致性)。

用法: python run_exp3.py <broken_trials_per_op> <safe_trials> <out.json> [workers=4] [model=haiku] [task=check|unrelated]
"""
from __future__ import annotations

import ast
import copy
import difflib
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import iln_sim as S

OPS3 = ["unit_change", "scale_change", "range_widen", "range_narrow", "enum_add", "enum_renumber",
        "enum_remove", "flag_polarity", "index_base", "reorder_fields", "rename_field", "default_change"]

LEGEND = """\
ILN 欄位語意(registry 的 kind):
- time  : 線上原始值 raw,實際時間(微秒 us) = raw * unit 對應的微秒數(us=1, ms=1000, s=1000000);範圍 lo..hi(raw 單位)
- index : 實際索引 = raw - base(輸出為從 0 起算);raw 範圍 lo..hi
- enum  : map 為 符號->raw;handler 輸出符號字串;raw 不在 map 時輸出 "UNKNOWN"(除非該模組設定 strict,strict 則可拋例外)
- scaled: 實際值 = raw * scale;raw 範圍 lo..hi
- flag  : 實際值 = (raw == true_val),輸出 bool
- optional 欄位可能缺席,缺席時 raw 取 default
- positional=true 的訊息是 list,依 fields 順序取位置;否則是 dict,依欄位名稱取
handler 規則:r[欄位名] 必須等於上述『實際值』;對規格範圍內的所有 raw 值都不可拋例外;上限檢查(cap)必須涵蓋規格範圍。"""

PROMPT = """你是模組 {c} 的維護者。你的模組用下面的 Python 檔處理 ILN 訊息 {m}。
{legend}

【目前 registry 中訊息 {m} 的規格(JSON,最新版)】
{spec}
{notice}
【你的模組原始碼 {c}.py】
```python
{src}
```

任務:確保 handle(msg) 對最新 registry 規格正確。若需要修改就修改(包含檔頭的 ASSUME 宣告也要和程式實際假設一致);若不需修改就原樣輸出。
只輸出一個 ```python 區塊,內容是完整的 {c}.py,不要其他文字。"""


PROMPT_U = """你是模組 {c} 的維護者。現在的任務是一個和 ILN 無關的小功能:
在 handle(msg) 的回傳 r 中,新增一個鍵 "_cnt",值為本模組處理的欄位數量(len 現有的 r 項目即可,不要改變其他欄位的輸出)。
{legend}

【參考:目前 registry 中訊息 {m} 的規格(JSON,最新版)】
{spec}
{notice}
【你的模組原始碼 {c}.py】
```python
{src}
```

只輸出一個 ```python 區塊,內容是完整的 {c}.py,不要其他文字。"""

TASK = "check"  # check: 明確要求對齊最新規格; unrelated: 做無關小功能(規格只當參考,測 agent 會不會順手發現漂移)


def spec_json(reg: dict[str, Any], m: str) -> str:
    s = {k: v for k, v in reg[m].items() if k in ("name", "producer", "positional", "fields")}
    return json.dumps(s, ensure_ascii=False, indent=1, sort_keys=False)


def make_trials(n_per_op: int, n_safe: int) -> list[dict[str, Any]]:
    """從隨機系統中挑出『會壞』與『不會壞』的 (consumer, message, mutation) 目標,各算子平均。"""
    broken_cnt = {op: 0 for op in OPS3}
    trials: list[dict[str, Any]] = []
    safe: list[dict[str, Any]] = []
    for i in range(400):
        if all(v >= n_per_op for v in broken_cnt.values()) and len(safe) >= n_safe:
            break
        inst = S.Instance(2000 + i, S.DEFAULT_CFG)
        rng = random.Random(7000 + i)
        for op in rng.sample(OPS3, len(OPS3)):
            reg = copy.deepcopy(inst.registry)
            if not S.mutate(reg, rng, op):
                continue
            changed = [m for m in reg if not reg[m]["derived"] and reg[m] != inst.registry[m]]
            if not changed:
                continue
            sd = rng.randint(1, 10**6)
            for m in changed:
                for c, cm in inst.mods.items():
                    uses = cm["uses"].get(m)
                    if not uses or any(u["relay_to"] for u in uses):
                        continue
                    fails = S.run_system(inst, reg, "dense", 150, sd, relay=False, only={(c, m)}, with_timing=False)
                    item = {"inst_seed": 2000 + i, "op": op, "c": c, "m": m, "sd": sd,
                            "rng_seed": 7000 + i, "reg": reg}
                    if fails and broken_cnt[op] < n_per_op:
                        broken_cnt[op] += 1
                        trials.append(dict(item, broken=True))
                    elif not fails and len(safe) < n_safe and op not in ("rename_field",):
                        safe.append(dict(item, broken=False))
                    break
                else:
                    continue
                break
    return trials + safe


def rebuild_case(t: dict[str, Any]) -> tuple[S.Instance, dict[str, Any]]:
    """重建 instance(seed 決定性),變更後 registry 直接取自 trial。"""
    return S.Instance(t["inst_seed"], S.DEFAULT_CFG), t["reg"]


def build_notice(cond: str, t: dict[str, Any], inst: S.Instance, reg: dict[str, Any]) -> str:
    if cond == "N0":
        return ""
    m = t["m"]
    txt = f"\n【通知】ILN 訊息 {m}(producer: {inst.registry[m]['producer']})在 registry 有更新,你的模組有讀取它。\n"
    if cond == "N2":
        a = spec_json(inst.registry, m).splitlines()
        b = spec_json(reg, m).splitlines()
        diff = "\n".join(difflib.unified_diff(a, b, "old", "new", lineterm="", n=2))
        txt += f"【registry 變更 diff(old→new)】\n{diff}\n"
    return txt


def call_claude(prompt: str, model: str, timeout: int = 300) -> dict[str, Any]:
    cmd = ["claude", "-p", "--model", model, "--effort", "medium", "--output-format", "json",
           "--tools", "", "--no-session-persistence", "--system-prompt", "You are a careful Python maintainer.",
           "--strict-mcp-config", "--disable-slash-commands", "--setting-sources", "", "--max-budget-usd", "0.5"]
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    env["CLAUDE_CODE_SUBPROCESS_ENV_SCRUB"] = "1"
    t0 = time.time()
    with tempfile.TemporaryDirectory() as d:
        try:
            r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=timeout, env=env, cwd=d)
            out, err = r.stdout, r.stderr
        except subprocess.TimeoutExpired:
            out, err = "", "timeout"
    try:
        j = json.loads(out)
    except ValueError:
        j = {}
    return {"text": j.get("result") or err[-300:], "cost": j.get("total_cost_usd"),
            "sec": round(time.time() - t0)}


def extract_code(text: str) -> str | None:
    blocks = re.findall(r"```(?:python)?\n(.*?)```", text, re.S)
    return blocks[-1] if blocks else None


def grade(t: dict[str, Any], inst: S.Instance, reg: dict[str, Any], code: str | None) -> dict[str, Any]:
    c, m = t["c"], t["m"]
    if code is None:
        return {"ok": False, "why": "no_code"}
    try:
        ns: dict[str, Any] = {}
        exec(compile(code, f"<{c}.{m}>", "exec"), ns)
        handler = ns["handle"]
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "why": f"load:{type(e).__name__}"}
    inst2 = copy.copy(inst)
    inst2.handlers = dict(inst.handlers)
    inst2.handlers[(c, m)] = handler
    fails = S.run_system(inst2, reg, "dense", 150, t["sd"], relay=False, only={(c, m)}, with_timing=False)
    res = {"ok": not fails, "why": "" if not fails else sorted({f[2] for f in fails})[:3]}
    # ASSUME 一致性
    try:
        tree = ast.parse(code)
        assume = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "ASSUME":
                assume = ast.literal_eval(node.value)
        res["assume_synced"] = not any(S._decl_flag(a, f, reg[m]) for f, a in assume.items())
    except Exception:  # noqa: BLE001
        res["assume_synced"] = False
    return res


def run_one(args: tuple[dict[str, Any], str, str]) -> dict[str, Any]:
    t, cond, model = args
    inst, reg = rebuild_case(t)
    src = inst.sources[(t["c"], t["m"])]
    prompt = (PROMPT_U if TASK == "unrelated" else PROMPT).format(c=t["c"], m=t["m"], legend=LEGEND, spec=spec_json(reg, t["m"]),
                           notice=build_notice(cond, t, inst, reg), src=src)
    r = call_claude(prompt, model)
    code = extract_code(r["text"])
    g = grade(t, inst, reg, code)
    return {"op": t["op"], "broken": t["broken"], "cond": cond, "inst_seed": t["inst_seed"],
            "c": t["c"], "m": t["m"], "changed_code": bool(code and code.strip() != src.strip()),
            "cost": r["cost"], "sec": r["sec"], **g}


if __name__ == "__main__":
    per_op, n_safe, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    workers = int(next((a.split("=")[1] for a in sys.argv[4:] if a.startswith("workers=")), 4))
    model = next((a.split("=")[1] for a in sys.argv[4:] if a.startswith("model=")), "haiku")
    TASK = next((a.split("=")[1] for a in sys.argv[4:] if a.startswith("task=")), "check")
    trials = make_trials(per_op, n_safe)
    jobs = []
    for t in trials:
        for cond in (("N0", "N1", "N2") if t["broken"] and TASK == "check" else ("N0", "N2")):
            jobs.append((t, cond, model))
    print(f"trials={len(trials)} (broken={sum(t['broken'] for t in trials)}) jobs={len(jobs)} model={model}", flush=True)
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(workers) as ex:
        for k, row in enumerate(ex.map(run_one, jobs), 1):
            rows.append(row)
            if k % 10 == 0:
                print(f"  done {k}/{len(jobs)}", flush=True)
                with open(path, "w", encoding="utf-8") as fh:
                    json.dump(rows, fh, ensure_ascii=False)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False)
    for broken in (True, False):
        for cond in ("N0", "N1", "N2"):
            rs = [r for r in rows if r["broken"] == broken and r["cond"] == cond]
            if rs:
                ok = sum(r["ok"] for r in rs)
                sy = sum(bool(r.get("assume_synced")) for r in rs)
                print(f"{'broken' if broken else 'safe  '} {cond}: ok {ok}/{len(rs)}  assume_synced {sy}/{len(rs)}  "
                      f"cost ${sum(r['cost'] or 0 for r in rs):.2f}")
