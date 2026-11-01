# spec-flow-skill

通用 spec ⇄ code 工作流(plugin `spec-code-flow`,放在 ai-grocery 倉庫)的實驗資料。全為玩具規模,數字不可外推。對應筆記:`knowledge/technology/code-dev/spec-code-flow/spec-code-flow-skill-experiments.md`。

```text
gen_repo.py   產生隨機玩具專案(規格、程式、測試、凍結 golden、契約),seed 可重現
run_s1.py     S1 漂移偵測:16 種事件 × N 次,比較 測試 / check / guard 各層
run_s2.py     S2 變異探測:三種測試強度下 specflow mutate 的抓取率
run_s4.py     S4 headless Haiku:4 任務 × (無 skill / 有 skill) × N 次
out/          結果 JSON(s4 含逐列 LLM 回報,不可重現)
```

工具與 skill 本體在 ai-grocery:`plugins/spec-code-flow/skills/spec-code-flow/scripts/specflow.py`。路徑用環境變數覆寫:`SPECFLOW`(s1、s2)、`SKILL_DIR`(s4)。

```bash
PYTHONIOENCODING=utf-8 python run_s1.py 40 out/s1_results.json     # 約 20 分鐘
PYTHONIOENCODING=utf-8 python run_s2.py 10 20 out/s2_results.json
PYTHONIOENCODING=utf-8 python run_s4.py 12 out/s4_results.json 4   # 96 次呼叫,約 0.56 美元,耗訂閱額度
```

結果檔記錄 `specflow_sha` / `skill_sha`,用來確認跑的是哪一版。S4 的 `--tools` 加 `--allowedTools` 只放行讀寫檔、`python -m unittest`、git 唯讀指令與(A1)`.sf/specflow.py`;工作目錄在專案外暫存資料夾,不載入使用者設定。
