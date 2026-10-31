# 由程式碼反推的規格書:modem_v2

## 外部規格條目(R-*)

### R-FSM-01 — RRC 狀態轉移表；新增 SUSPENDED 狀態與轉移(僅 Rel-21)

- 常數:TRANSITIONS={'IDLE|setup_req': 'SETUP_PENDING', 'SETUP_PENDING|setup_ok': 'CONNECTED', 'SETUP_PENDING|t300_expiry': 'IDLE', 'CONNECTED|release': 'IDLE', 'CONNECTED|handover_cmd': 'HO_EXEC', 'HO_EXEC|ho_ok': 'CONNECTED', 'HO_EXEC|t304_expiry': 'IDLE'}, TRANSITIONS_ADD={'CONNECTED|suspend': 'SUSPENDED', 'SUSPENDED|resume_fast': 'CONNECTED', 'SUSPENDED|t_resume_expiry': 'IDLE'}
- 實作:fsm.Rrc.step, fsm.Rrc.on_t300_expiry
- 測試:test_setup_retry, test_suspend_resume_only_in_rel21

### R-FSM-02 — T300 = 1000 ms

- 常數:T300_MS=1000
- 實作:fsm.Rrc.on_t300_expiry
- 測試:test_setup_retry

### R-FSM-03 — T304 = 200 ms

- 常數:T304_MS=200
- 實作:(無)
- 測試:test_t304_timer_matches_spec

### R-FSM-05 — T_RESUME = 300 ms

- 常數:T_RESUME_MS=300
- 實作:fsm.Rrc.step
- 測試:test_suspend_resume_only_in_rel21

### R-MR-01 — meas_id 為 0..63

- 常數:MEAS_ID_BITS=6, MEAS_ID_MAX=63
- 實作:codec.encode_measurement_report, codec.decode_measurement_report
- 測試:test_golden_vectors_bit_exact

### R-MR-02 — rsrp、rsrq 為 0..127

- 常數:LEVEL_BITS=7, LEVEL_MAX=127
- 實作:codec.encode_measurement_report, codec.decode_measurement_report
- 測試:test_golden_vectors_bit_exact

### R-MR-03 — 鄰區清單最多 8 筆;pci 0..1007；鄰區總數上限提高為 16;前 8 筆沿用原位置,第 9..16 筆 SHALL 放在 v2100 擴充內

- 常數:NEIGH_COUNT_BITS=4, NEIGH_MAX=16, NEIGH_BASE_MAX=8, PCI_BITS=10, PCI_MAX=1007
- 實作:codec.encode_measurement_report, codec.decode_measurement_report, sched.admit
- 測試:test_golden_vectors_bit_exact, test_rel20_rejects_9_neighbors, test_roundtrip_16_neighbors_and_beams, test_rel21_base_prefix_equals_rel20_encoding, test_17_neighbors_rejected

### R-MR-04 — 尾端 1 位元擴充旗標;旗標為 1 時接 8 位元長度與內容;不認得的接收端 SHALL 略過

- 常數:EXT_LEN_BITS=8
- 實作:codec.encode_measurement_report, codec.decode_measurement_report
- 測試:test_rel20_decoder_ignores_rel21_extension

### R-MR-10 — 新增可選 beam 清單,0..16 筆,每筆 6 位元;放在 v2100 擴充

- 常數:BEAM_MAX=16, BEAM_BITS=6, BEAM_COUNT_BITS=5
- 實作:codec.encode_measurement_report, codec.decode_measurement_report
- 測試:test_roundtrip_16_neighbors_and_beams, test_boundary_16_beams_and_6bit_max

### R-MR-11 — v2100 擴充內容順序:beam 清單,再來是額外鄰區(0..8 筆,計數 4 位元)

- 常數:EXTRA_NEIGH_COUNT_BITS=4
- 實作:codec.encode_measurement_report, codec.decode_measurement_report
- 測試:test_roundtrip_16_neighbors_and_beams, test_rel20_decoder_ignores_rel21_extension

## 內部決定(D-*)

### D-INT-01 — 鄰區處理上限
- 理由:與外部上限對齊,不得少於外部 NEIGH_MAX
- 常數:NEIGH_CAP=16
- 實作:sched.admit

### D-INT-02 — 單份回報處理預算(微秒)
- 理由:由硬體 slot 時序推得;最壞情況(外部最大鄰區數)成本必須落在預算內
- 常數:BUDGET_US=50, COST_BASE_US=5, COST_PER_NEIGH_US=3, BATCH_THRESHOLD=8, COST_PER_NEIGH_BATCH_US=2
- 實作:sched.cost_us, sched.admit

### D-INT-03 — setup 自動重試上限
- 理由:產品體驗決定,外部規格未規定
- 常數:SETUP_RETRY_MAX=3
- 實作:fsm.Rrc.on_t300_expiry

## ⚠️ 待人工判斷

- 無任何追溯標註的公開函式:無
