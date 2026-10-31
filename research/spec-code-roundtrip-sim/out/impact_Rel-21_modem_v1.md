# Rel-21 影響分析(現行程式:modem_v1)

## 一、逐條變更影響

### MODIFY R-MR-03
- 內容:鄰區總數上限提高為 16;前 8 筆沿用原位置,第 9..16 筆 SHALL 放在 v2100 擴充內
- 相容性條款:Rel-20 位元佈局不變
- 受影響常數:NEIGH_COUNT_BITS, NEIGH_MAX, PCI_BITS, PCI_MAX
- 受影響函式:codec.encode_measurement_report, codec.decode_measurement_report, sched.admit
- 既有測試:test_golden_vectors_bit_exact, test_rel20_rejects_9_neighbors, test_roundtrip_16_neighbors_and_beams, test_rel21_base_prefix_equals_rel20_encoding, test_17_neighbors_rejected
- 🚨 編碼風險:此條目有位元寬度常數 ['NEIGH_COUNT_BITS', 'PCI_BITS'];不得更動,否則 Rel-20 golden vector 會破

### ADD R-MR-10
- 內容:新增可選 beam 清單,0..16 筆,每筆 6 位元;放在 v2100 擴充
- 相容性條款:(未載明)
- 既有程式:🆕 全新功能,需新增程式與測試

### ADD R-MR-11
- 內容:v2100 擴充內容順序:beam 清單,再來是額外鄰區(0..8 筆,計數 4 位元)
- 相容性條款:(未載明)
- 既有程式:🆕 全新功能,需新增程式與測試

### MODIFY R-FSM-01
- 內容:新增 SUSPENDED 狀態與轉移(僅 Rel-21)
- 相容性條款:Rel-20 轉移不變
- 受影響常數:TRANSITIONS
- 受影響函式:fsm.Rrc.step, fsm.Rrc.on_t300_expiry
- 既有測試:test_setup_retry, test_suspend_resume_only_in_rel21

### ADD R-FSM-05
- 內容:T_RESUME = 300 ms
- 相容性條款:(未載明)
- 既有程式:🆕 全新功能,需新增程式與測試

## 二、內部決定 vs 新外部規格

- ❌ 衝突 D-INT-01 鄰區處理上限:`code.sched.NEIGH_CAP >= ext['NEIGH_MAX']`(外部規格不可改 ⇒ 須重新協商此內部決定;負責:-)
- ❌ 衝突 D-INT-02 單份回報處理預算(微秒):`code.sched.cost_us(ext['NEIGH_MAX']) <= code.sched.BUDGET_US`(外部規格不可改 ⇒ 須重新協商此內部決定;負責:HW/時序小組)
- ✅ D-INT-03 setup 自動重試上限:`True`