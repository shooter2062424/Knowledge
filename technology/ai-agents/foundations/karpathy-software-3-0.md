# Karpathy 訪談:Software 3.0、Jagged Intelligence 與 Agentic Engineering

**主題分類:** AI / 代理工程 — 基礎概念
**來源:** YouTube〈AI 時代工程師怎麼重新定位自己:Andrej Karpathy 訪談解析〉(Gary Chen,2026-05-17,約 15 分;解析 Karpathy 在紅杉資本的訪談,依繁中逐字稿整理)
**整理日期:** 2026-05-30

---

## 0. 為什麼值得看

Andrej Karpathy(OpenAI 共同創辦人、前 Tesla AI 總監、發明「vibe coding」)幾個月前說「身為 programmer 從沒覺得自己這麼落後過」。這支影片把他的訪談整理成三個能重新定位自己的概念 + 一句貫穿全場的話。

> **「You can outsource your thinking, but you cannot outsource your understanding.」**
> 你可以外包你的思考,但你不能外包你的理解。

---

## 1. Software 3.0:你的程式設計變成「寫 prompt」

| 版本 | 你在做什麼 |
|---|---|
| **1.0** 傳統軟體 | 人寫 code,電腦按規則跑 |
| **2.0** 神經網路 | 不寫規則,設計資料集 + 目標函數,訓練出模型 |
| **3.0** LLM 時代 | 不寫 function,而是 **寫 prompt、管 context window、指揮 AI 助理** |

**MenuGen 故事:** Karpathy 用傳統思維做了一個「拍菜單→辨識→生圖→排版」的 app,做完才發現——在 Software 3.0 裡 **使用者直接把照片丟給 Gemini 就解決了,app 根本不該存在**。

> **可遷移的測試:** 你想做的東西,如果使用者能 **直接把原始輸入丟給前沿模型、三句話內拿到你 app 的輸出**,那它大概就不該存在。Software 3.0 不只是把舊東西做得更快,而是 **讓以前不可能的事現在變得可能**。

---

## 2. Jagged Intelligence:鋸齒狀的智力

AI 能解奧數,卻會建議你「去 50 公尺外的洗車場用走的」(忘了車本身要被洗)。能力分佈 **不是平滑曲線,有高峰也有斷崖**。原因:

1. **可驗證(verifiable)** 的領域才能丟進 RL 大量循環(數學能對答案、code 能跑測試)→ 能力飆升。
2. **實驗室有沒有把它當回事(labs care)**——把資料放進訓練分佈。例:GPT-3.5→4 西洋棋大躍進,是因為有人決定把棋譜加進預訓練,**不是模型自然變強**。

> 所以能力分佈是 **實驗室的產品決策 + 訓練資料** 決定的,不是均勻演化。Karpathy:「傳統電腦自動化你能 **specify** 的事;這代 LLM 自動化你能 **verify** 的事。」
>
> **個人應用:** 想用 AI 把某事做好,先問的不是「AI 能不能做」,而是「**我能不能驗證它做對了**」。能驗證→讓 AI 跑 100 次挑最好的;不能驗證→只能祈禱它這次運氣好。

---

## 3. Vibe Coding vs Agentic Engineering:你的下限 vs 上限

- **Vibe Coding = 提高所有人的下限**:不會寫 code 的人也能用自然語言做出能跑的小工具(消費者心態:「我有想法,AI 幫我做出來」)。
- **Agentic Engineering = 決定你的上限**:專業軟體的品質/安全/可維護性不能因為用了 AI 就掉(工程師心態:「我設計好 **邊界、驗證機制、回滾策略**,讓 100 個 agent 幫我跑」)。

**效率遠不只 10 倍:** 一個人指揮 100 個 agent 同時跑實驗,一晚產出 = 一個工程師數月的嘗試。實證就是 **Karpathy Loop / autoresearch**(見 [[karpathy-autoresearch]]):三個 constraint——**改一個檔、一個 metric、一個時間預算**——讓 agent 在乾淨的小盒子裡瘋狂試錯(2 天 700 次實驗、訓練時間 -11%、還抓到一個 bug)。SkyPilot 把它跑到 16 GPU(8 小時 910 次、成本 < $300);Shopify CEO 自己跑也拿到 19% 提升。

---

## 4. 阻力:世界的基礎建設還是「給人用的」

Karpathy 抱怨做完 app「寫 code 不痛苦,**部署才痛苦**」——Vercel 後台、串服務、配 DNS,每個介面都為人類設計。他要的是「一段能直接丟給 agent、它自己讀完去做」的東西。這就是 Codex / Perplexity 推 **computer use** 的原因:世界還沒為 agent 改造,那就讓 agent 假裝是人去操作滑鼠鍵盤。

---

## 5. 什麼該外包、什麼要自己留

- **email 配對 bug:** agent 想用「Google email == Stripe email」來綁定資金歸屬——語法跑得過、測試過得了,但 **系統設計是錯的**(正解是後端用 persistent user ID)。agent 不理解身份/支付/資金歸屬的風險。
- **概念不能外包:** Karpathy 不再記 PyTorch/pandas 的 API 細節(agent 記得更好),但 **tensor 是什麼、view vs storage、何時 copy memory 這些概念不能忘**。「細節可以外包,概念不能。」

> **時間重新分配:** 技術細節交給 agent;你的時間花在 **判斷值不值得做、寫好 spec、看 trace、檢查 agent 有沒有在 system level 犯根本性錯誤**。用 AI 不是變成更會打字的人,而是變成更會做 **頂層決策** 的人。

---

## 6. 應用案例:開新專案前先寫一份 30 分鐘的 spec

動手前回答三件事(寫不出第二題,代表任務還不夠 verifiable,先停下想清楚):
1. 你要 agent **做到什麼**?
2. 你 **怎麼知道它做對了**?(驗證方式)
3. 它出包時 **回滾到哪裡**?

這正是 [[long-running-agents-goal-evaluation]] 的 goal prompt 五要素的精神,也是 [[12-factor-agents]]「掌握控制流」的個人版。

> **一句帶走:** 別把 AI 當「讓你少想一點」的工具,要當「讓你想得更深」的槓桿。AI 把「願不願意深度思考」這件事的 ROI 放大了——過去差 2-3 倍,AI 時代會放大成幾十倍。

---

## 來源

- [YouTube:AI 時代工程師怎麼重新定位自己:Andrej Karpathy 訪談解析(Gary Chen)](https://youtu.be/_RD3iFDhuzs)
