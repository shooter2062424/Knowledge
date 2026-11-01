# iln-multi-team-sim

模擬「多個團隊各守一個 module、模組之間用 ILN(Inter-Layer Message)溝通」時,某團隊只改自己的 spec,別人會不會壞、哪一層檢查抓得到。
全為玩具規模、數值皆為模擬值,不是任何公司的真實格式。對應筆記:
`knowledge/technology/code-dev/spec-code-flow/iln-multi-team-spec-workflow.md`

```text
iln_sim.py     隨機系統產生(4–8 模組、每系統 7–27 個 ILN 訊息,中位數 16)、consumer 原始碼模板、ast 抽取 manifest、
               18 種 producer 端變更算子、閘門 G1/G2/G2d/G3/G4、ground truth
run_exp1.py    實驗 1:N 個隨機系統 × M 次隨機變更,量各閘門 recall / 誤報
run_exp2.py    實驗 2:語意破壞變更下,naive vs expand/contract(AST / 加閘門 / runtime trace)
out/*.txt      終端輸出;out/*.summary.json 彙整(逐筆資料可由固定 seed 重現,未入版控)
```

重現(約 4 分鐘 + 7 分鐘 + 5 分鐘):
```bash
python run_exp1.py 80 150 out/exp1_main.json                 # 12000 次變更
python run_exp1.py 40 120 out/x.json stale=0 dyn=0 test=1 ttest=1   # 理想條件
python run_exp1.py 40 120 out/x.json stale=0.3 dyn=0.25 test=0.6 ttest=0.2   # 差條件
python run_exp2.py 60 30 out/exp2_main.json                  # 1800 次遷移
```
