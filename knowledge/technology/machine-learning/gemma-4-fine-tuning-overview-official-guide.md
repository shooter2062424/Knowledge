# Gemma 4 微調總覽:RAG、LoRA 還是全量?顯存要多少(官方文件導讀)

> 來源是 Google DeepMind 官方 Gemma 文件站的〈Fine-tuning overview〉頁(2026,由使用者貼連結)。頁面本身是中性技術指南,但含推廣:`gemma-trainer` skill、Google Cloud(Vertex AI / GKE / Gemini API)、Unsloth。**我只讀了這一頁,沒讀各子指南,也沒實際訓練**,數字皆為官方頁所述,**未能獨立核實**。

## TL;DR

- 多數團隊從**指令微調版(`-it`)**起手,不需要走完預訓練、續訓、SFT、RL 四階段。
- 事實常變 → **RAG**;新格式/新任務 → **SFT(LoRA/QLoRA)**;新語言或大領域 → **續訓**;嚴格正確性 → **強化學習(GRPO)**。LoRA 可與 RAG 併用。
- LoRA 只訓練約 1–2% 參數;QLoRA 再把凍結權重存成 4-bit。
- 顯存是主要門檻:QLoRA 12B 約 11 GB,全量微調 12B 約 80 GB。

## 1. 四階段訓練

| 階段 | 做什麼 | 官方頁指南 |
|---|---|---|
| 1 基底模型 | 續訓、自訂聊天模板(ChatML) | 從 pre-trained 檢查點開始,算力需求大 |
| 2 監督微調 | (Q)LoRA、全量、MoE(僅 26B A4B)、視覺、音訊(僅 E2B/E4B/12B) | 最常用 |
| 3 強化學習 | 偏好最佳化、可驗證獎勵(GRPO) | 要求嚴格正確時 |
| 4 部署 | FSDP2/QAT、匯出(vLLM、GGUF、Ollama、LiteRT-LM) | |

## 2. 方法選擇

| 目標 | 建議 |
|---|---|
| 知識常更新 | RAG(權重不動,檢索文件塞進提示) |
| 新格式、新任務 | SFT,LoRA 為主 |
| 新語言、大領域 | 續訓 |
| 嚴格正確 | RL(GRPO) |

LoRA 原理見 [[lora-fine-tuning-explained]]。

## 3. 顯存需求(官方頁,序列長度 2,048)

| 模型 | 參數 | QLoRA | 全量 |
|---|---|---|---|
| Gemma 4 E2B | 2B 有效 | 約 7 GB | 約 32 GB |
| Gemma 4 E4B | 4B 有效 | 約 9 GB | 約 42 GB |
| Gemma 4 12B | 12B | 約 11 GB | 約 80 GB |
| Gemma 4 26B A4B | 26B(4B 啟用) | 約 21 GB | 約 160 GB |
| Gemma 4 31B | 31B | 約 22 GB | 約 200 GB |

顯存 = 權重 + 梯度 + 優化器狀態 + 激活值,所以全量遠大於 QLoRA。

## 4. 工具

TRL(SFT/DPO/GRPO、多 GPU)、Unsloth(單卡加速、GGUF 匯出)、Axolotl(YAML 設定)、Vertex AI(託管微調)、GKE(多 GPU)。

## 應用案例

- **客服機器人要有公司口吻**:拿 `-it` 12B,用數百到數千筆對話做 QLoRA,約 11 GB 顯存,一張消費級卡可跑;產品價格另用 RAG 查,避免價格改了就得重訓。
- **內部資料常變的問答**:不要微調,直接 RAG。
- **要輸出固定 JSON 格式**:SFT 教格式,再用 GRPO 以「JSON 可解析」當可驗證獎勵。

## 相關筆記

- [[lora-fine-tuning-explained]]:LoRA 為何省顯存
- [[diffusion-gemma]]:Gemma 系列的另一條路線
- [[llm-slm-lrm-vlm-model-routing-guide]]:模型選型
- [[cs336-training-cost-napkin-math]]:訓練成本估算

## 來源

- Google DeepMind,Gemma 文件〈Fine-tuning overview〉:<https://gemma.ai/tuning/>(使用者提供的連結帶有 fbclid 追蹤參數,已略去)。只讀本頁。
