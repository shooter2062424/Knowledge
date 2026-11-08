"""第四輪檢索實驗題庫:(qid, 類型, 問句, gold claim 集合, 過期 claim 集合)。

類型:L 字面詞、G 詞彙落差(改說法、不含 claim 關鍵詞)、N 現況(新舊同詞)、S 舊前提(問句字面只對到過期 claim)、
M 多條彙整(算 recall)、E 英文/中英混用、H 歷史/原因。gold 與 stale 皆在執行前寫定。
"""
Q = [
    # L 字面
    ("L1", "L", "RT thread 數目前是多少", {"CL-0030"}, set()),
    ("L2", "L", "plugin 初始化完成後可以 dlopen 嗎", {"CL-0013", "CL-0014"}, set()),
    ("L3", "L", "tier-1 支援哪個平台", {"CL-0019"}, set()),
    ("L4", "L", "toolchain 的 gcc 版本", {"CL-0024"}, set()),
    ("L5", "L", "ARM64 Linux 支援等級", {"CL-0020"}, set()),
    ("L6", "L", "RT 路徑可以使用 shared_ptr 嗎", {"CL-0018"}, set()),
    ("L7", "L", "monitoring 用 lock-free counter 取樣", {"CL-0027"}, set()),
    ("L8", "L", "所有 team 必須使用 framework 的 logging API 嗎", {"CL-0022"}, set()),
    # G 詞彙落差
    ("G1", "G", "即時執行緒裡面可以動態要記憶體嗎", {"CL-0006"}, set()),
    ("G2", "G", "實時路徑可以用引用計數的智慧指標嗎", {"CL-0018"}, set()),
    ("G3", "G", "外掛什麼時候可以載入動態函式庫", {"CL-0013", "CL-0014"}, set()),
    ("G4", "G", "即時路徑可以丟異常嗎", {"CL-0016"}, set()),
    ("G5", "G", "在時間敏感的路徑上可以用互斥鎖嗎", {"CL-0007"}, set()),
    ("G6", "G", "每個週期可以花多少時間", {"CL-0026"}, {"CL-0005"}),
    ("G7", "G", "新版跨程序通訊在視窗系統上做不做", {"CL-0021"}, {"CL-0004"}),
    ("G8", "G", "舊的同步呼叫什麼時候移除", {"CL-0025"}, {"CL-0003"}),
    ("G9", "G", "別組可以自己開即時執行緒嗎", {"CL-0023"}, set()),
    ("G10", "G", "編譯器版本多新", {"CL-0024"}, set()),
    ("G11", "G", "為什麼不先做無鎖日誌", {"CL-0010"}, set()),
    ("G12", "G", "監控資料彙整放哪個執行緒", {"CL-0028"}, set()),
    # N 現況(新舊同詞)
    ("N1", "N", "RT 路徑可以使用 mutex logger 嗎", {"CL-0011"}, {"CL-0009"}),
    ("N2", "N", "framework 每個 cycle 預算是多少", {"CL-0026"}, {"CL-0005"}),
    ("N3", "N", "v1 ipc_call 還能用嗎", {"CL-0025"}, {"CL-0003"}),
    ("N4", "N", "IPC v2 的 Windows 版本現在狀態", {"CL-0021"}, {"CL-0004"}),
    ("N5", "N", "memory pool allocator 現在狀態", {"CL-0029"}, {"CL-0008"}),
    ("N6", "N", "RT 路徑 logger 現在怎麼處理", {"CL-0011", "CL-0012"}, {"CL-0009"}),
    # S 舊前提
    ("S1", "S", "framework 每個 cycle 預算是 200µs 對嗎", {"CL-0026"}, {"CL-0005"}),
    ("S2", "S", "RT 路徑的 logger 採 mutex 保護的 logger 對嗎", {"CL-0011", "CL-0012"}, {"CL-0009"}),
    ("S3", "S", "IPC v2 先支援 Linux,Windows 版本之後再做,對嗎", {"CL-0021"}, {"CL-0004"}),
    ("S4", "S", "v1 同步 ipc_call 暫時保留以維持相容,對嗎", {"CL-0025"}, {"CL-0003"}),
    ("S5", "S", "framework 暫不提供 memory pool allocator,對嗎", {"CL-0029"}, {"CL-0008"}),
    # M 多條彙整
    ("M1", "M", "RT 路徑有哪些禁止事項", {"CL-0006", "CL-0007", "CL-0016", "CL-0018", "CL-0011"}, set()),
    ("M2", "M", "初始化階段與 RT 階段的規則差異", {"CL-0013", "CL-0014", "CL-0015", "CL-0016", "CL-0017", "CL-0018"}, set()),
    ("M3", "M", "各平台的支援與限制", {"CL-0019", "CL-0020", "CL-0021"}, set()),
    ("M4", "M", "跟 IPC 相關的所有決定", {"CL-0001", "CL-0002", "CL-0003", "CL-0004", "CL-0021", "CL-0025"}, set()),
    # E 英文/中英混用
    ("E1", "E", "can real-time code throw exceptions", {"CL-0016"}, set()),
    ("E2", "E", "is mutex allowed in RT path", {"CL-0007"}, set()),
    ("E3", "E", "what is the per-cycle budget", {"CL-0026"}, {"CL-0005"}),
    ("E4", "E", "when will v1 IPC be removed", {"CL-0025"}, {"CL-0003"}),
    ("E5", "E", "does Windows get IPC v2", {"CL-0021"}, {"CL-0004"}),
    # H 歷史/原因
    ("H1", "H", "為什麼 mutex logger 被作廢", {"CL-0011"}, set()),
    ("H2", "H", "lock-free ring buffer logger 當初為什麼被棄", {"CL-0010"}, set()),
    ("H3", "H", "memory pool allocator 為什麼延後", {"CL-0008", "CL-0029"}, set()),
]
