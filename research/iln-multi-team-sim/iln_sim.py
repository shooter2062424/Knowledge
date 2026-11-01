"""多團隊 ILN(Inter-Layer Message)規格往返模擬:隨機系統產生、變異算子、閘門。

玩具規模、全為模擬值,不是真實 3GPP 或任何公司的內部格式。用途是回答:
一個團隊只改自己模組的 ILN 規格時,哪一層檢查能抓到「其他團隊會壞掉」。

結構:
  registry   : ILN 訊息規格(單一真相來源,每個欄位帶 kind/unit/range/enum/default)
  consumer   : 每個模組的處理程式(由模板產生 Python 原始碼再 exec,所以可用 ast 抽取)
  mutation   : 18 種 producer 端變更算子
  gates      : G1 schema diff / G2 manifest 語意 diff / G2d 含 dataflow / G3 契約測試 / G4 端到端 replay
  truth      : 用稠密取樣跑整個系統當 ground truth
"""
from __future__ import annotations

import ast
import copy
import random
from typing import Any

UNIT_US = {"us": 1, "ms": 1000, "s": 1_000_000}
KINDS = ["time", "index", "enum", "scaled", "flag"]
SYMS = ["SETUP", "RELEASE", "REEST", "SUSPEND", "RESUME", "FAIL", "IDLE", "ACTIVE"]


# ───────────────────────── 欄位與訊息規格 ─────────────────────────
def new_field(rng: random.Random, kind: str | None = None) -> dict[str, Any]:
    """產生一個隨機欄位規格。

    Args:
        rng: 亂數來源。
        kind: 指定欄位種類;None 則隨機。

    Returns:
        欄位規格 dict。
    """
    kind = kind or rng.choice(KINDS)
    fs: dict[str, Any] = {"kind": kind, "optional": rng.random() < 0.25}
    if kind == "time":
        fs.update(unit=rng.choice(["ms", "us", "s"]), lo=rng.choice([0, 1, 10]),
                  hi=rng.choice([20, 100, 640, 1000]))
        fs["default"] = fs["lo"]
    elif kind == "index":
        base = rng.choice([0, 0, 1])
        fs.update(base=base, lo=base, hi=base + rng.randint(3, 15))
        fs["default"] = base
    elif kind == "enum":
        n = rng.randint(2, 5)
        fs["map"] = {s: i for i, s in enumerate(rng.sample(SYMS, n))}
        fs["default"] = 0
    elif kind == "scaled":
        fs.update(scale=rng.choice([0.5, 0.25, 2, 4]), lo=0, hi=rng.choice([60, 120, 255]))
        fs["default"] = 0
    else:
        fs.update(true_val=rng.choice([1, 1, 0]), default=0)
    return fs


def phys_of_raw(fs: dict[str, Any], raw: int) -> Any:
    """依「producer 的規格」把線上原始值轉成物理意義(ground truth 用)。"""
    k = fs["kind"]
    if k == "time":
        return raw * UNIT_US[fs["unit"]]
    if k == "index":
        return raw - fs["base"]
    if k == "enum":
        inv = {v: s for s, v in fs["map"].items()}
        return inv.get(raw, "UNKNOWN")
    if k == "scaled":
        return raw * fs["scale"]
    return raw == fs["true_val"]


def sample_raw(fs: dict[str, Any], rng: random.Random, policy: str,
               base_syms: set[str] | None = None) -> int:
    """依取樣策略抽一個原始值。

    policy: dense / contract(含邊界)、typical(只取中段、只用舊有 enum 符號)。
    """
    k = fs["kind"]
    if k == "enum":
        syms = list(fs["map"])
        if policy == "typical" and base_syms:
            keep = [s for s in syms if s in base_syms]
            syms = keep or syms
        return fs["map"][rng.choice(syms)]
    if k == "flag":
        return rng.choice([0, 1])
    lo, hi = fs["lo"], fs["hi"]
    if policy == "typical":
        a = lo + int((hi - lo) * 0.3)
        b = lo + int((hi - lo) * 0.7)
        return rng.randint(a, max(a, b))
    if rng.random() < 0.3:
        return rng.choice([lo, hi, hi - 1 if hi - 1 >= lo else hi])
    return rng.randint(lo, hi)


def sample_message(spec: dict[str, Any], base_spec: dict[str, Any], rng: random.Random,
                   policy: str) -> tuple[Any, dict[str, Any]]:
    """依(變更後的)producer 規格產生一則訊息與其物理真值。"""
    truth: dict[str, Any] = {}
    named: dict[str, Any] = {}
    for f, fs in spec["fields"].items():
        is_new = f not in base_spec["fields"]
        omit = False
        if fs["optional"] and not spec["positional"] and policy != "typical":
            omit = rng.random() < (0.5 if is_new else 0.3)
        if omit:
            raw = fs["default"]
        else:
            base_syms = None
            if not is_new and fs["kind"] == "enum" and base_spec["fields"][f]["kind"] == "enum":
                base_syms = set(base_spec["fields"][f]["map"])
            raw = sample_raw(fs, rng, policy, base_syms)
            named[f] = raw
        truth[f] = phys_of_raw(fs, raw)
    if spec["positional"]:
        return [named[f] for f in spec["fields"]], truth
    return named, truth


# ───────────────────────── 系統產生 ─────────────────────────
class Instance:
    """一個隨機產生的多模組系統(baseline 正確,所有 consumer 與規格一致)。"""

    def __init__(self, seed: int, cfg: dict[str, Any]):
        self.seed = seed
        self.cfg = cfg
        self.rng = random.Random(seed)
        self.registry: dict[str, dict[str, Any]] = {}
        self.mods: dict[str, dict[str, Any]] = {}
        self.handlers: dict[tuple[str, str], Any] = {}
        self.sources: dict[tuple[str, str], str] = {}
        self.relay_msgs: dict[tuple[str, str], tuple[str, dict[str, str]]] = {}
        self._build()
        self.manifest = extract_manifest(self)

    def known_syms(self, msg: str, f: str) -> set[str]:
        """baseline 規格中該 enum 欄位的符號集合(consumer 認得的符號)。"""
        base = self.registry[msg]["fields"].get(f)
        return set(base["map"]) if base and base["kind"] == "enum" else set()

    def _build(self) -> None:
        r, cfg = self.rng, self.cfg
        n_mod = r.randint(4, 8)
        names = [f"mod{i}" for i in range(n_mod)]
        for m in names:
            self.mods[m] = {"strict": r.random() < cfg["strict_rate"], "uses": {}, "deadline": {},
                            "orders": [], "timing_test": r.random() < cfg["timing_test_rate"],
                            "tested": {}}
        idx = 0
        for p in names:
            for seq in range(r.randint(1, 3)):
                idx += 1
                pos = r.random() < 0.3
                fields = {}
                for j in range(r.randint(2, 6)):
                    fs = new_field(r)
                    if pos:
                        fs["optional"] = False
                    fields[f"f{j}"] = fs
                self.registry[f"M{idx}"] = {"name": f"M{idx}", "producer": p, "seq": seq,
                                            "latency_us": r.choice([50, 100, 200]),
                                            "positional": pos, "fields": fields, "derived": {}}
        sources = list(self.registry)
        for msg in sources:
            spec = self.registry[msg]
            others = [m for m in names if m != spec["producer"]]
            for c in r.sample(others, r.randint(1, min(3, len(others)))):
                self._add_consumer_uses(c, msg, spec)
        # relay:consumer 把某欄位原樣轉發到自己的下游訊息
        pairs = [(c, m) for c, cm in self.mods.items() for m in list(cm["uses"])]
        for c, msg in pairs:
            spec = self.registry[msg]
            if spec["derived"]:
                continue
            relayed: dict[str, str] = {}
            for u in self.mods[c]["uses"][msg]:
                fs = spec["fields"][u["f"]]
                if not fs["optional"] and not spec["positional"] and r.random() < cfg["relay_rate"]:
                    relayed[u["f"]] = f"{u['f']}_r"
                    u["relay_to"] = relayed[u["f"]]
            if relayed:
                idx += 1
                rm = f"M{idx}"
                self.registry[rm] = {"name": rm, "producer": c, "seq": 0, "latency_us": 100,
                                     "positional": False, "derived": {},
                                     "fields": {g: copy.deepcopy(spec["fields"][f]) for f, g in relayed.items()}}
                for f, g in relayed.items():
                    self.registry[rm]["derived"][g] = (msg, f)
                self.relay_msgs[(c, msg)] = (rm, relayed)
                downs = [m for m in names if m != c]
                for d in r.sample(downs, r.randint(1, min(2, len(downs)))):
                    self._add_consumer_uses(d, rm, self.registry[rm], force_all=True)
        # 順序/期限需求
        for p in names:
            mine = sorted([m for m, s in self.registry.items() if s["producer"] == p and not s["derived"]],
                          key=lambda x: self.registry[x]["seq"])
            for c, cm in self.mods.items():
                got = [m for m in mine if m in cm["uses"]]
                if len(got) >= 2 and r.random() < cfg["order_rate"]:
                    cm["orders"].append((got[0], got[1]))
        for c, cm in self.mods.items():
            for m in cm["uses"]:
                s = self.registry[m]
                if r.random() < cfg["deadline_rate"]:
                    cm["deadline"][m] = int(s["latency_us"] * r.choice([1.0, 1.5, 2.0]))
                cm["tested"][m] = r.random() < cfg["test_rate"]
        for c, cm in self.mods.items():
            for m, uses in cm["uses"].items():
                src = gen_source(self, c, m, uses)
                self.sources[(c, m)] = src
                ns: dict[str, Any] = {}
                exec(compile(src, f"<{c}.{m}>", "exec"), ns)
                self.handlers[(c, m)] = ns["handle"]

    def _add_consumer_uses(self, c: str, msg: str, spec: dict[str, Any], force_all: bool = False) -> None:
        r = self.rng
        fields = list(spec["fields"])
        pick = fields if force_all else r.sample(fields, r.randint(1, len(fields)))
        uses = []
        for f in pick:
            fs = spec["fields"][f]
            k = fs["kind"]
            cap_m = r.choice([1, 1, 2])
            if k == "time":
                consts: dict[str, Any] = {"factor": UNIT_US[fs["unit"]], "cap": int(fs["hi"] * cap_m)}
            elif k == "index":
                consts = {"base": fs["base"], "n": fs["hi"] - fs["base"] + 1 + r.choice([0, 0, 2])}
            elif k == "enum":
                consts = {"map": {v: s for s, v in fs["map"].items()}, "strict": r.random() < 0.5}
            elif k == "scaled":
                consts = {"scale": fs["scale"], "cap": int(fs["hi"] * cap_m)}
            else:
                consts = {"true_val": fs["true_val"]}
            consts["default"] = fs["default"]
            u = {"f": f, "kind": k, "consts": consts, "relay_to": None,
                 "dyn": (not spec["positional"]) and r.random() < self.cfg["dyn_rate"]}
            u["declared"] = declare(u, fs, r, self.cfg["stale_rate"])
            uses.append(u)
        self.mods[c]["uses"].setdefault(msg, []).extend(uses)


def declare(u: dict[str, Any], fs: dict[str, Any], rng: random.Random, stale: float) -> dict[str, Any]:
    """產生 consumer 對該欄位『文件宣告的假設』;以 stale 機率讓宣告與程式實際常數不一致。"""
    k, c = u["kind"], u["consts"]
    d: dict[str, Any] = {"kind": k, "optional": fs["optional"], "default": c["default"]}
    if k == "time":
        d.update(unit=[n for n, v in UNIT_US.items() if v == c["factor"]][0], cap=c["cap"])
    elif k == "index":
        d.update(base=c["base"], n=c["n"])
    elif k == "enum":
        d.update(map={s: v for v, s in c["map"].items()}, strict=c["strict"])
    elif k == "scaled":
        d.update(scale=c["scale"], cap=c["cap"])
    else:
        d.update(true_val=c["true_val"])
    if rng.random() < stale:
        # 只模擬「宣告比程式實際更寬鬆」的過期(單位/極性等寫錯在 baseline 就會被發現,不屬於靜默過期)
        if k in ("time", "scaled"):
            d["cap"] = d["cap"] * 4
        elif k == "index":
            d["n"] = d["n"] + 100
        elif k == "enum":
            d["strict"] = False
    return d


def gen_source(inst: Instance, c: str, msg: str, uses: list[dict[str, Any]]) -> str:
    """為 consumer c 處理訊息 msg 產生 Python 原始碼(可被 ast 抽取)。"""
    spec = inst.registry[msg]
    cm = inst.mods[c]
    known = list(spec["fields"])
    assume: dict[str, Any] = {}
    keys: list[str] = []
    lines = ["def handle(msg):", "    r = {}", "    out = {}"]
    if cm["strict"]:
        if spec["positional"]:
            lines.append(f"    if len(msg) > {len(known)}: raise ValueError('extra')")
        else:
            lines.append(f"    if set(msg) - {set(known)!r}: raise ValueError('extra')")
    for u in uses:
        f, k, cs = u["f"], u["kind"], u["consts"]
        pos = known.index(f) if f in known else -1
        if not u["dyn"]:
            assume[f] = dict(u["declared"], pos=pos)
        if spec["positional"]:
            acc = f"msg[{pos}]"
        elif u["dyn"]:
            keys.append(f)
            acc = (f"msg.get(KEYS[{len(keys) - 1}], {cs['default']})" if spec["fields"][f]["optional"]
                   else f"msg[KEYS[{len(keys) - 1}]]")
        else:
            acc = (f'msg.get("{f}", {cs["default"]})' if spec["fields"][f]["optional"] else f'msg["{f}"]')
        if u["relay_to"]:
            lines.append(f'    out["{u["relay_to"]}"] = {acc}')
            continue
        if k == "time":
            lines += [f"    v = {acc}", f'    if v > {cs["cap"]}: raise ValueError("cap")',
                      f'    r["{f}"] = v * {cs["factor"]}']
        elif k == "index":
            lines += [f'    v = {acc} - {cs["base"]}', f'    if v < 0 or v >= {cs["n"]}: raise IndexError("idx")',
                      f'    r["{f}"] = v']
        elif k == "enum":
            lines.append(f'    r["{f}"] = {cs["map"]!r}[{acc}]' if cs["strict"]
                         else f'    r["{f}"] = {cs["map"]!r}.get({acc}, "UNKNOWN")')
        elif k == "scaled":
            lines += [f"    v = {acc}", f'    if v > {cs["cap"]}: raise ValueError("cap")',
                      f'    r["{f}"] = v * {cs["scale"]}']
        else:
            lines.append(f'    r["{f}"] = ({acc} == {cs["true_val"]})')
    lines.append("    return r, out")
    meta = {"strict": cm["strict"], "known": known, "deadline_us": cm["deadline"].get(msg),
            "orders": [list(o) for o in cm["orders"] if msg in o]}
    head = [f"ASSUME = {assume!r}", f"META = {meta!r}"]
    if keys:
        head.append(f"KEYS = {keys!r}")
    return "\n".join(head + [""] + lines) + "\n"


# ───────────────────────── code → spec:抽取 manifest ─────────────────────────
def _msg_read(n: ast.AST) -> Any:
    """若節點是 msg["x"] / msg.get("x", ..) / msg[3] 回傳常數 key,否則 None。"""
    if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == "msg" \
            and isinstance(n.slice, ast.Constant):
        return n.slice.value
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get" \
            and isinstance(n.func.value, ast.Name) and n.func.value.id == "msg" \
            and n.args and isinstance(n.args[0], ast.Constant):
        return n.args[0].value
    return None


def extract_manifest(inst: Instance) -> dict[tuple[str, str], dict[str, Any]]:
    """用 ast 從 consumer 原始碼抽出:讀了哪些欄位/位置、relay 邊、宣告的假設與 META。

    動態 key(msg[KEYS[i]])抽不到,這是刻意保留的盲點。
    """
    out = {}
    for key, src in inst.sources.items():
        tree = ast.parse(src)
        assume: dict[str, Any] = {}
        meta: dict[str, Any] = {}
        reads: set[Any] = set()
        edges: list[tuple[Any, str]] = []
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                if node.targets[0].id == "ASSUME":
                    assume = ast.literal_eval(node.value)
                elif node.targets[0].id == "META":
                    meta = ast.literal_eval(node.value)
        for n in ast.walk(tree):
            v = _msg_read(n)
            if v is not None:
                reads.add(v)
            if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Subscript):
                t = n.targets[0]
                if isinstance(t.value, ast.Name) and t.value.id == "out" and isinstance(t.slice, ast.Constant):
                    src_f = _msg_read(n.value)
                    if src_f is not None:
                        edges.append((src_f, t.slice.value))
        names: set[str] = set()
        for r_ in reads:
            if isinstance(r_, int):
                names |= {f for f, a in assume.items() if a.get("pos") == r_}
            else:
                names.add(r_)
        out[key] = {"assume": assume, "meta": meta, "reads": names, "edges": edges}
    return out


# ───────────────────────── 變更算子 ─────────────────────────
def _src_msgs(reg: dict[str, Any]) -> list[str]:
    return [m for m, s in reg.items() if not s["derived"]]


def _pick_field(reg: dict[str, Any], rng: random.Random, pred=lambda fs, s: True):
    cands = [(m, f) for m in _src_msgs(reg) for f, fs in reg[m]["fields"].items() if pred(fs, reg[m])]
    return rng.choice(cands) if cands else None


def mutate(reg: dict[str, Any], rng: random.Random, op: str) -> bool:
    """在 registry 上原地套用一個 producer 端變更。回傳是否套用成功。"""
    if op == "noop_doc":
        return True
    if op in ("add_optional", "add_required"):
        m = rng.choice(_src_msgs(reg))
        fs = new_field(rng)
        fs["optional"] = (op == "add_optional") and not reg[m]["positional"]
        reg[m]["fields"][f"x{rng.randint(100, 999)}"] = fs
        return True
    if op == "remove_field":
        t = _pick_field(reg, rng)
        if not t or len(reg[t[0]]["fields"]) < 2:
            return False
        del reg[t[0]]["fields"][t[1]]
        return True
    if op == "rename_field":
        t = _pick_field(reg, rng)
        if not t:
            return False
        m, f = t
        reg[m]["fields"] = {(f + "_v2" if k == f else k): v for k, v in reg[m]["fields"].items()}
        return True
    if op == "unit_change":
        t = _pick_field(reg, rng, lambda fs, s: fs["kind"] == "time")
        if not t:
            return False
        fs = reg[t[0]]["fields"][t[1]]
        new = rng.choice([u for u in UNIT_US if u != fs["unit"]])
        old_f, new_f = UNIT_US[fs["unit"]], UNIT_US[new]
        if new_f < old_f:
            ratio = old_f // new_f
            fs["lo"], fs["hi"], fs["default"] = fs["lo"] * ratio, fs["hi"] * ratio, fs["default"] * ratio
        else:
            ratio = new_f // old_f
            fs["lo"], fs["hi"], fs["default"] = fs["lo"] // ratio, max(1, fs["hi"] // ratio), fs["default"] // ratio
        fs["unit"] = new
        return True
    if op == "scale_change":
        t = _pick_field(reg, rng, lambda fs, s: fs["kind"] == "scaled")
        if not t:
            return False
        fs = reg[t[0]]["fields"][t[1]]
        fs["scale"] = fs["scale"] / 2
        fs["hi"] *= 2
        return True
    if op == "range_widen":
        t = _pick_field(reg, rng, lambda fs, s: fs["kind"] in ("time", "index", "scaled"))
        if not t:
            return False
        fs = reg[t[0]]["fields"][t[1]]
        fs["hi"] = fs["hi"] * 2 + 1
        return True
    if op == "range_narrow":
        t = _pick_field(reg, rng, lambda fs, s: fs["kind"] in ("time", "index", "scaled") and fs["hi"] > fs["lo"] + 1)
        if not t:
            return False
        fs = reg[t[0]]["fields"][t[1]]
        fs["hi"] = fs["lo"] + max(1, (fs["hi"] - fs["lo"]) // 2)
        return True
    if op == "enum_add":
        t = _pick_field(reg, rng, lambda fs, s: fs["kind"] == "enum")
        if not t:
            return False
        fs = reg[t[0]]["fields"][t[1]]
        fs["map"][f"NEW{rng.randint(1, 99)}"] = max(fs["map"].values()) + 1
        return True
    if op == "enum_renumber":
        t = _pick_field(reg, rng, lambda fs, s: fs["kind"] == "enum" and len(fs["map"]) >= 2)
        if not t:
            return False
        fs = reg[t[0]]["fields"][t[1]]
        a, b = rng.sample(list(fs["map"]), 2)
        fs["map"][a], fs["map"][b] = fs["map"][b], fs["map"][a]
        return True
    if op == "enum_remove":
        t = _pick_field(reg, rng, lambda fs, s: fs["kind"] == "enum" and len(fs["map"]) >= 2)
        if not t:
            return False
        fs = reg[t[0]]["fields"][t[1]]
        del fs["map"][rng.choice(list(fs["map"]))]
        return True
    if op == "flag_polarity":
        t = _pick_field(reg, rng, lambda fs, s: fs["kind"] == "flag")
        if not t:
            return False
        fs = reg[t[0]]["fields"][t[1]]
        fs["true_val"] = 1 - fs["true_val"]
        return True
    if op == "index_base":
        t = _pick_field(reg, rng, lambda fs, s: fs["kind"] == "index")
        if not t:
            return False
        fs = reg[t[0]]["fields"][t[1]]
        d = 1 if fs["base"] == 0 else -1
        fs["base"] += d
        fs["lo"] += d
        fs["hi"] += d
        fs["default"] += d
        return True
    if op == "reorder_fields":
        cands = [m for m in _src_msgs(reg) if reg[m]["positional"] and len(reg[m]["fields"]) >= 2]
        if not cands:
            return False
        m = rng.choice(cands)
        items = list(reg[m]["fields"].items())
        for _ in range(10):
            rng.shuffle(items)
            if [k for k, _ in items] != list(reg[m]["fields"]):
                reg[m]["fields"] = dict(items)
                return True
        return False
    if op == "seq_swap":
        by: dict[str, list[str]] = {}
        for m in _src_msgs(reg):
            by.setdefault(reg[m]["producer"], []).append(m)
        cands = [v for v in by.values() if len(v) >= 2]
        if not cands:
            return False
        a, b = rng.sample(rng.choice(cands), 2)
        reg[a]["seq"], reg[b]["seq"] = reg[b]["seq"], reg[a]["seq"]
        return True
    if op == "latency_up":
        m = rng.choice(_src_msgs(reg))
        reg[m]["latency_us"] *= 3
        return True
    if op == "default_change":
        t = _pick_field(reg, rng, lambda fs, s: fs["optional"] and fs["kind"] != "enum")
        if not t:
            return False
        fs = reg[t[0]]["fields"][t[1]]
        fs["default"] = fs["default"] + 1 if fs["kind"] != "flag" else 1 - fs["default"]
        return True
    raise ValueError(op)


OPS = ["noop_doc", "add_optional", "add_required", "remove_field", "rename_field", "unit_change",
       "scale_change", "range_widen", "range_narrow", "enum_add", "enum_renumber", "enum_remove",
       "flag_polarity", "index_base", "reorder_fields", "seq_swap", "latency_up", "default_change"]


# ───────────────────────── 系統執行(truth / G3 / G4 共用) ─────────────────────────
class RecDict(dict):
    """記錄被讀取欄位的 dict(runtime access trace,抓得到動態 key)。"""

    def __init__(self, d: dict, rec: list, mod: str, msg: str):
        super().__init__(d)
        self._rec, self._mod, self._msg = rec, mod, msg

    def __getitem__(self, k):
        self._rec.append((self._mod, self._msg, k))
        return super().__getitem__(k)

    def get(self, k, default=None):
        self._rec.append((self._mod, self._msg, k))
        return super().get(k, default)


def _check(u: dict[str, Any], decoded: Any, truth: Any, known: set[str]) -> bool:
    if truth is None:  # producer 已無此欄位,consumer 卻解出值 = 讀到別欄位的資料
        return False
    if u["kind"] == "scaled":
        return abs(decoded - truth) < 1e-9
    if u["kind"] == "enum":
        return decoded == truth or (decoded == "UNKNOWN" and truth not in known)
    return decoded == truth


def feed(inst: Instance, msg: str, body: Any, truth: dict[str, Any], fails: set,
         relay: bool, recorder: list | None = None, only: set | None = None) -> None:
    """把一則訊息交給該訊息的所有 consumer 處理,比對物理真值,必要時下游 relay。"""
    for c, cm in inst.mods.items():
        if only is not None and (c, msg) not in only:
            continue
        uses = cm["uses"].get(msg)
        if not uses:
            continue
        b = body
        if recorder is not None and isinstance(body, dict):
            b = RecDict(body, recorder, c, msg)
        try:
            r, out = inst.handlers[(c, msg)](b)
        except Exception as e:  # noqa: BLE001  任何例外都算失敗
            fails.add((c, msg, f"exc:{type(e).__name__}"))
            continue
        for u in uses:
            if u["relay_to"] or u["f"] not in r:
                continue
            if not _check(u, r[u["f"]], truth.get(u["f"]), inst.known_syms(msg, u["f"])):
                fails.add((c, msg, f"mismatch:{u['f']}"))
        rm = inst.relay_msgs.get((c, msg))
        if rm and relay and out:
            rmsg, mapping = rm
            t2 = {g: truth.get(f) for f, g in mapping.items()}
            feed(inst, rmsg, out, t2, fails, relay, recorder)


def timing_fails(inst: Instance, reg: dict[str, Any], only_mods: set[str] | None = None) -> set:
    """延遲期限與到達順序是否被違反。"""
    fails = set()
    for c, cm in inst.mods.items():
        if only_mods is not None and c not in only_mods:
            continue
        for m, dl in cm["deadline"].items():
            if m in reg and reg[m]["latency_us"] > dl:
                fails.add((c, m, "latency"))
        for x, y in cm["orders"]:
            if x in reg and y in reg and reg[x]["seq"] > reg[y]["seq"]:
                fails.add((c, x, "order"))
    return fails


def run_system(inst: Instance, reg: dict[str, Any], policy: str, n: int, seed: int,
               relay: bool = True, only: set | None = None, with_timing: bool = True,
               recorder: list | None = None) -> set:
    """跑整個系統(或只跑部分 consumer),回傳失敗集合。"""
    rng = random.Random(seed)
    fails: set = set()
    for m in _src_msgs(inst.registry):
        if m not in reg:
            continue
        for _ in range(n):
            body, truth = sample_message(reg[m], inst.registry[m], rng, policy)
            feed(inst, m, body, truth, fails, relay, recorder, only)
    if with_timing:
        fails |= timing_fails(inst, reg)
    return fails


# ───────────────────────── 閘門 ─────────────────────────
def g1_schema_diff(inst: Instance, new: dict[str, Any]) -> bool:
    """純結構 diff(類似 protobuf breaking 規則):看不到 unit、範圍、default、時序,也不知道誰在用。"""
    for m, old in inst.registry.items():
        if old["derived"] or m not in new:
            continue
        nw = new[m]
        for f, fs in old["fields"].items():
            if f not in nw["fields"]:
                return True
            nf = nw["fields"][f]
            if nf["kind"] != fs["kind"]:
                return True
            if fs["kind"] == "enum":
                for s, v in fs["map"].items():
                    if s not in nf["map"] or nf["map"][s] != v:
                        return True
        for f, nf in nw["fields"].items():
            if f not in old["fields"] and not nf["optional"]:
                return True
        if old["positional"] and list(old["fields"]) != list(nw["fields"])[:len(old["fields"])]:
            return True
    return False


def _decl_flag(a: dict[str, Any], f: str, spec: dict[str, Any]) -> bool:
    """consumer 宣告的假設與新 producer 規格是否衝突。"""
    if f not in spec["fields"]:
        return True
    fs = spec["fields"][f]
    if fs["kind"] != a["kind"]:
        return True
    k = a["kind"]
    if spec["positional"] and list(spec["fields"]).index(f) != a["pos"]:
        return True
    if k == "time":
        if fs["unit"] != a["unit"] or fs["hi"] > a["cap"]:
            return True
    elif k == "index":
        if fs["base"] != a["base"] or fs["hi"] - a["base"] >= a["n"] or fs["lo"] - a["base"] < 0:
            return True
    elif k == "enum":
        inv_decl = {v: s for s, v in a["map"].items()}
        for s, v in fs["map"].items():
            if s in a["map"] and a["map"][s] != v:
                return True
            if s not in a["map"] and v in inv_decl:
                return True
            if s not in a["map"] and a["strict"]:
                return True
    elif k == "scaled":
        if fs["scale"] != a["scale"] or fs["hi"] > a["cap"]:
            return True
    elif fs["true_val"] != a["true_val"]:
        return True
    return bool(fs["optional"] and a["optional"] and fs["default"] != a["default"])


def g2_manifest(inst: Instance, new: dict[str, Any], dataflow: bool) -> set[str]:
    """用 AST 抽出的 manifest(讀了哪些欄位 + 宣告的假設)對新規格做語意比對。

    Args:
        inst: 系統。
        new: 變更後的 registry。
        dataflow: True 時沿 relay 邊把上游新規格傳遞給下游訊息再比對。

    Returns:
        被判定受影響的模組集合。
    """
    eff = new
    if dataflow:
        eff = copy.deepcopy(new)
        for (c, msg), mf in inst.manifest.items():
            rm = inst.relay_msgs.get((c, msg))
            if not rm or msg not in eff:
                continue
            for f_in, g in mf["edges"]:
                if isinstance(f_in, int):
                    f_in = next((f for f, a in mf["assume"].items() if a.get("pos") == f_in), None)
                if f_in in eff[msg]["fields"] and g in eff[rm[0]]["fields"]:
                    eff[rm[0]]["fields"][g] = copy.deepcopy(eff[msg]["fields"][f_in])
    flagged: set[str] = set()
    for (c, msg), mf in inst.manifest.items():
        if msg not in eff:
            continue
        spec, meta = eff[msg], mf["meta"]
        if any(f not in spec["fields"] for f in mf["reads"]):
            flagged.add(c)
        if any(_decl_flag(a, f, spec) for f, a in mf["assume"].items()):
            flagged.add(c)
        if meta["strict"] and (set(spec["fields"]) - set(meta["known"])):
            flagged.add(c)
        if meta["deadline_us"] is not None and spec["latency_us"] > meta["deadline_us"]:
            flagged.add(c)
        if any(x in eff and y in eff and eff[x]["seq"] > eff[y]["seq"] for x, y in meta["orders"]):
            flagged.add(c)
    return flagged


def g3_contract(inst: Instance, new: dict[str, Any], seed: int) -> set[str]:
    """consumer 自備的契約測試:用『新規格』產生含邊界的樣本,只跑自己(不含下游),可能缺測試。"""
    only = {(c, m) for c, cm in inst.mods.items() for m in cm["uses"] if cm["tested"].get(m)}
    fails = run_system(inst, new, "contract", 40, seed, relay=False, only=only, with_timing=False)
    for c, cm in inst.mods.items():
        if cm["timing_test"]:
            fails |= timing_fails(inst, new, {c})
    return {c for c, _, _ in fails}


def g4_e2e(inst: Instance, new: dict[str, Any], seed: int) -> set[str]:
    """端到端 replay:少量典型刺激(只取範圍中段、舊有 enum 符號),含下游,時序一定檢查。"""
    return {c for c, _, _ in run_system(inst, new, "typical", 8, seed)}


def truth_fails(inst: Instance, new: dict[str, Any], seed: int) -> set:
    """ground truth:稠密取樣(含邊界)的整個系統。"""
    return run_system(inst, new, "dense", 150, seed)


DEFAULT_CFG = {"strict_rate": 0.2, "relay_rate": 0.2, "order_rate": 0.4, "deadline_rate": 0.5,
               "test_rate": 0.85, "timing_test_rate": 0.5, "dyn_rate": 0.10, "stale_rate": 0.15}
