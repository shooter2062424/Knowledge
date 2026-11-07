# `new/` 收件匣批次帳本

> 規則:`new/` 底下**一個子資料夾 = 一批素材 = 一個 task**,整批處理完才改名 `done-<名稱>`。素材本身不進版控(`new/` 已在 `.gitignore`),這份帳本只記「哪一批、何時收、產出哪些筆記」,方便日後回溯。
> 每篇筆記的「來源」區塊也會寫明批次資料夾名。

| 收件日 | 批次資料夾 | 檔案 | 產出 / 增補的筆記 | 備註 |
|---|---|---|---|---|
| 2026-09-29 | `done-karpathy_8years_conclusion` | 1 個 mp4(約 129 分鐘) | `knowledge/technology/ai-productivity/karpathy-how-i-use-llms.md` | 「上週發布」說法有誤,實為 2025-02-27 〈How I use LLMs〉 |
| 2026-11-07 | `done-ai-guide` | 28 個 PDF(約 17 個有文字層、11 個無文字層輪播)+ 2 個 zip 原始碼(約 48 MB;作者 Anjana「AI & Tech」@aiwithanju,社群引流型素材) | 新建 15 篇:`career/ai-transition/ai-ml-engineer-learning-roadmaps-anjana`、`career/data-analyst/{data-analyst-roadmap-2027-and-7-day-plan,data-analyst-10-projects-code-review,free-courses-and-job-search-resources-checked}`、`technology/ai-agents/applications/ai-engineering-seven-projects-source-review`、`technology/ai-agents/foundations/{agentic-ai-ten-concepts-interview-map,ai-architectures-twelve-patterns-practical-examples,ai-engineering-twenty-concepts-serving-rag-ops}`、`technology/llm-internals/architecture/ai-essential-13-concepts-beginner-map`、`technology/machine-learning/{supervised,unsupervised}-ml-algorithms-guide`、`model-evaluation-techniques-guide`、`ml-ten-core-concepts-guide`、`ml-practice-projects-fifteen`、`technology/system-design/cloud-engineering-fifteen-concepts`;增補 2 篇:`career/ai-transition/{fde-and-ordinary-people-ai-entry-guide §3,ai-app-dev-learning-roadmap-four-tiers §6}`。嵌入原稿圖表 67 張(`assets/<slug>/`) | 6 個 Sonnet 子 agent 分群處理;全部檔案都讀了文字層或看圖轉寫,但長篇 PDF(2027 路線 90 頁、資料分析 98 頁)內的程式碼與逐行輸出只讀說明與重點,詳見各筆記「未能核實」。P6 LoRA 專案未實跑;AutoGen 已封存、多個課程連結失效等修正已寫入筆記 |
