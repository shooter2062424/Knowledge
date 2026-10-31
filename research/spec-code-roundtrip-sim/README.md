# spec-code-roundtrip-sim

模擬「外部公定規格(不可改)+ 內部規格(可協商)+ 既有程式碼」在新 Release 規格到來時的完整往返流程。
全為玩具規模、數值皆為模擬,不是真實 3GPP 內容。對應筆記:
`knowledge/technology/code-dev/spec-code-flow/multi-spec-roundtrip-experiment-python-sim.md`

```text
modem_v1/        改前程式(Rel-20),刻意埋了 3 個遺留問題:T304 偏離、殘留標註、未標註函式
modem_v2/        依 delta 改後的程式(Rel-20 + Rel-21 並存)
specs/           ext_spec.json(外部,by_release 保留舊版)、internal_spec.json(內部決定+可執行約束)、delta_rel21.json
tests/           test_modem.py(Rel-20 回歸)、test_rel21.py(由 delta 先寫的 spec-first 測試)
golden/          凍結的 Rel-20 golden vector(make_golden.py 只在 v1 跑一次)
tools/           extract_spec(code→spec)、merge_delta(合併+影響分析)、check_drift、run_gates、mutation_probe
```

重現(在本資料夾):
```bash
python golden/make_golden.py                          # 只需一次,且須在 v1 上
python tools/extract_spec.py modem_v1                 # code → spec
python tools/merge_delta.py modem_v1 specs/delta_rel21.json   # 影響分析(加 --write 才寫回 ext_spec.json)
python tools/run_gates.py modem_v2 Rel-21             # 四道關卡
python tools/mutation_probe.py                        # 關卡強度探測(10 種注入錯誤)
```

> 注意:`specs/ext_spec.json` 是已合併 Rel-21 的狀態(Rel-20 內容保留在 by_release)。重跑 `merge_delta.py` 不加 `--write` 只會印報告,不會改檔。
