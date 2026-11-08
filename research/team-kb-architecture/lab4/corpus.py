"""第四輪(檢索實驗)語料:真實 seed(30 claim + 12 場會議逐句)+ 合成「同詞彙」干擾 + 真實文字雜訊。

單元(unit)欄位:uid, kind(claim|meeting|noise_hard|noise_easy), text, status(current|superseded|raw), alias
"""
from __future__ import annotations
import glob, json, random, re, sys
from pathlib import Path

SB = Path(r"C:\Users\shoot\project\Knowledge\research\team-kb-architecture\data\sandbox")
sys.path.insert(0, str(SB / "kb" / "scripts"))
import kb  # noqa: E402

REPO = Path(r"C:\Users\shoot\project\Knowledge")

MODS = ["net", "storage", "ui", "telemetry", "build", "security", "sensor", "codec", "sched", "diag", "update", "crypto"]
THINGS = ["mutex", "shared_ptr", "malloc", "exceptions", "dlopen", "logger", "memcpy", "std::function", "RTTI", "virtual dispatch", "thread_local", "spinlock"]
PLAT = ["Linux", "Windows", "ARM64 Linux", "macOS", "QNX"]
STRAT = ["ring buffer", "mutex 保護", "per-thread 緩衝", "直接丟棄", "非同步批次寫入"]
# 規則式同義詞(干擾 claim 也帶 alias,避免 alias 只幫到 seed)
SYN = {"mutex": "鎖 互斥鎖 lock", "shared_ptr": "共享指標 智慧指標 引用計數", "malloc": "動態配置 記憶體分配", "exceptions": "例外 異常 throw",
       "dlopen": "動態載入 動態函式庫 插件載入", "logger": "日誌 記錄 log", "預算": "時間限制 週期預算 budget", "cycle": "週期 tick", "deprecated": "棄用 淘汰 移除",
       "Windows": "視窗 微軟平台", "ARM64": "ARM 架構", "gcc": "編譯器 toolchain", "IPC": "行程間通訊 跨程序呼叫"}


def hard_noise(n: int, rng: random.Random) -> list[dict]:
    T = [
        lambda: f"{rng.choice(MODS)} 模組每個 cycle 預算 {rng.choice([80,120,150,300,400,600])}µs",
        lambda: f"{rng.choice(MODS)} 不得在 RT 路徑使用 {rng.choice(THINGS)}",
        lambda: f"{rng.choice(MODS)} 的 {rng.choice(THINGS)} 已 deprecated,預計 {rng.choice(['2027-03','2027-06','2027-09','2028-01'])} 移除",
        lambda: f"{rng.choice(MODS)} 在 {rng.choice(PLAT)} 為 tier-{rng.choice([1,2,3])} 支援",
        lambda: f"{rng.choice(MODS)} 採用 {rng.choice(THINGS)} 取代 {rng.choice(THINGS)}",
        lambda: f"{rng.choice(MODS)} 的 logger 採 {rng.choice(STRAT)}",
        lambda: f"{rng.choice(MODS)} 可以在初始化階段使用 {rng.choice(THINGS)},RT 路徑不行",
        lambda: f"{rng.choice(MODS)} 的 IPC 走 v{rng.choice([1,2])},{rng.choice(PLAT)} 版本之後再做",
        lambda: f"{rng.choice(MODS)} 要求 gcc {rng.choice([9,11,12,13])} 以上,C++{rng.choice([17,20])}",
        lambda: f"{rng.choice(MODS)} 暫不提供 {rng.choice(['pool allocator','plugin 熱載入','RT logger','lock-free queue'])},因人力延後",
        lambda: f"{rng.choice(MODS)} 的 RT thread 數目前為 {rng.choice([2,3,4,5,8])}",
        lambda: f"{rng.choice(MODS)} 的 {rng.choice(THINGS)} 在 {rng.choice(PLAT)} 上被棄用,改用 {rng.choice(THINGS)}",
    ]
    out, seen = [], set()
    while len(out) < n:
        t = rng.choice(T)()
        if t in seen:
            continue
        seen.add(t)
        alias = " ".join(v for k, v in SYN.items() if k.lower() in t.lower())
        out.append(dict(uid=f"HN{len(out):04d}", kind="noise_hard", text=t, status=rng.choice(["current"] * 4 + ["superseded"]), alias=alias))
    return out


def easy_noise(n: int, rng: random.Random) -> list[dict]:
    lines = []
    for f in glob.glob(str(REPO / "knowledge" / "**" / "*.md"), recursive=True):
        for ln in Path(f).read_text(encoding="utf-8", errors="ignore").splitlines():
            ln = ln.strip("-*> #|").strip()
            if 25 <= len(ln) <= 110 and not ln.startswith(("http", "![", "```", "[")):
                lines.append(ln)
    rng.shuffle(lines)
    return [dict(uid=f"EN{i:04d}", kind="noise_easy", text=t, status="current", alias="") for i, t in enumerate(lines[:n])]


def seed_units() -> list[dict]:
    claims = kb.load_claims(kb.CLAIMS)
    d = kb.derive(claims)
    out = []
    for c in claims.values():
        out.append(dict(uid=c["id"], kind="claim", text=c["statement"], status="current" if d["status"][c["id"]] == "current" else "superseded",
                        alias="", source=c["source"], subject=c["subject"], sup_by=d["sup"].get(c["id"], []), sup=list(c.get("supersedes") or [])))
    for mid, (p, _) in kb.meeting_index().items():
        for ln in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\[(\d{1,3}:\d{2})\]\s*(.*)", ln)
            if m:
                out.append(dict(uid=f"{mid}@{m.group(1)}", kind="meeting", text=m.group(2), status="raw", alias=""))
    return out


def build(scale: str, seed_aliases: dict[str, str] | None = None) -> list[dict]:
    """scale: S(僅 seed)、M(+300 hard)、L(+1500 hard +1500 easy)。"""
    rng = random.Random(7)
    units = seed_units()
    if seed_aliases:
        for u in units:
            u["alias"] = seed_aliases.get(u["uid"], "")
    nh, ne = {"S": (0, 0), "M": (300, 0), "L": (1500, 1500)}[scale]
    allu = units + hard_noise(nh, rng) + easy_noise(ne, rng)
    random.Random(99).shuffle(allu)  # 打散順序:避免同分時穩定排序偏袒排在前面的 seed
    return allu


if __name__ == "__main__":
    for s in "SML":
        u = build(s)
        print(s, len(u), {k: sum(1 for x in u if x["kind"] == k) for k in ("claim", "meeting", "noise_hard", "noise_easy")})
