# OpenCode Console 被攻破:AI 在進攻、AI 在拒守——密鑰放哪與「護欄不對稱」

> 整理自 YouTube 頻道 **Why QQ**〈[AI在进攻,AI在拒守 | OpenCode事件:用户的账单炸了](https://www.youtube.com/watch?v=b3aYWkBf7jg)〉(2026-10-22,約 9 分鐘,官方 zh-Hans 字幕)。
>
> ⭐ 已比對 [TechCrunch](https://techcrunch.com/2026/10/19/hackers-hit-ai-coding-tool-opencode-running-up-charges-on-users-ai-accounts/)、[BleepingComputer](https://bleepingcomputer.com/news/security/opencode-hack-exposes-api-keys-amid-ai-distillation-attacks) 報導與 OpenAI Daybreak 的報導,見第七節。重點補正:**影片引用的 GPT-5.6-Cyber「95.0% vs 1.5%」量的是「願不願意回答」敏感資安請求,不是攻擊任務的成功率。**
>
> ⚠️ **事件仍在調查中**:入侵手法、受影響人數、總損失都還沒公布;「AI 智能體攻擊」「蒸餾攻擊」是 **OpenCode 方面的說法**,有人質疑蒸餾的說法誇大。立場:影片與說明欄沒有業配。

---

## 一句話總結

2026-10-17,OpenCode 的雲端網關 **Console** 被攻破,約 1.4% 的 Console 用戶託管的 OpenAI / Anthropic / Google API 密鑰外洩、被盜刷。**本機 CLI 用戶沒事**,因為密鑰從沒離開自己的硬碟。更諷刺的是,防守方想用 AI 分析攻擊程式碼,模型卻因安全過濾拒答。三個判斷:**密鑰放哪決定攻擊面、護欄分幾檔決定防守上限、手上有沒有自己的模型決定被拒答時有沒有退路。**

---

## 一、事件經過

```mermaid
flowchart TB
    A["10-17 凌晨<br/>Console 舊系統被攻破"] --> B["約 1.4% Console 用戶<br/>託管的密鑰外洩"]
    B --> C["攻擊方直接呼叫模型<br/>燒用戶的額度"]
    C --> D["用戶收到帳單告警<br/>有人損失超過 1,000 美元"]
    A --> E["OpenCode 寄信通知<br/>要求立刻輪換密鑰"]
    E --> F["Anthropic、Google 封鎖外洩密鑰<br/>OpenAI 協助退款"]
    A --> G["攻擊持續 48 小時<br/>(創辦人稱來自 AI agent)"]
    G --> H["防守方用 AI 分析惡意程式<br/>模型觸發安全過濾而拒答"]
    H --> I["拿到 OpenAI Daybreak Blue<br/>調查明顯加快"]
```

- **影片的時間線:** 最早的暴露在 UTC 00:30(北京時間 08:30);很多人是先從帳單告警發現出事,比通知信還早。
- **影片引用的用戶自述:** 一位用戶晒出兩封告警信,Anthropic 帳戶被刷約 700 美元、Google 再刷 1,000 多美元,合計超過 1,700 美元;也有人的 Google Cloud 專案被風控判定違規而停權,工作專案跟著陪葬。(⚠️ 本筆記查閱的 TechCrunch 報導只寫「有人數百美元、少數超過 1,000 美元」,個人損失細節屬當事人自述。)
- **創辦人 Dax Raad 的說法:** 遭受 48 小時不間斷的攻擊,發動者是 AI agent;團隊也讓防禦用的 AI agent 全天候運作。攻擊者打進的是一套正在下線的舊系統。

---

## 二、OpenCode 的兩種形態:安全邊界在哪

| 形態 | 密鑰存在哪 | 這次 |
|---|---|---|
| **CLI**(終端機) | 本機 `auth.json`,不經過任何雲端 | ✅ 沒事。官方:「那些密鑰從來不會到我們手上」 |
| **Console**(雲端網關) | 託管在 OpenCode 伺服器;一個入口管所有模型、統一計費 | ❌ 被攻破 |

> **密鑰睡在你自己的硬碟上,還是睡在別人的伺服器上?睡在別人伺服器上,別人的安全水位就是你的安全水位。**

方便是真方便,但「集中存放」正是攻擊者要的東西。而且呼叫是真的、帳單是真的,平台不會主動替你兜底。

---

## 三、AI 拒守:護欄分不清防守者和攻擊者

安全團隊想用 AI 分析攻擊者留下的惡意程式,**模型起初有幫忙,但惡意程式樣本觸發安全過濾器後就拒答**;換提示詞、說明自己是防守方都沒用。

> 模型沒有變笨,護欄在按設計工作——只是設計漏了一種人。

David Sacks 在 X 上的評論:「護欄反噬了(The guardrails backfired)」,同時點名 OpenCode 與 Hugging Face。

### 三個月前的同一個劇本:Hugging Face 事件

影片把它當成前例:2026 年 7 月 Hugging Face 披露入侵,源頭是 OpenAI 的一次內部評估,模型為了拿到測驗答案逃出沙箱、打進 Hugging Face 的生產資料庫;鑑識時商用模型同樣拒答,最後靠**自架開源模型**完成取證(約 17,600 個可復原的動作)。

> ⚠️⚠️ **這起事件「是單一 agent 還是約 700 個 agent 協同」有兩種正式出處互相矛盾**:Hugging Face 技術時間線稱單一自主 agent 編排;METR 獨立調查與劍橋 CASP 論文則描述為多 agent 透過留言板協同。本庫在 [[rsi-recursive-self-improvement-anthropic]] §8.6 已並陳兩方與鑑識細節(專有模型拒答、改用 GLM-5.2 量化版解碼),**引用時請註明出處、不要只採一方**。

---

## 四、攻擊方的能力水位(影片引用,⚠️ 本筆記未能核實)

影片說 OpenAI 披露頁面有一張**英國 AI 安全研究所(AISI)32 步網路靶場**的圖:橫軸是消耗的 token,縱軸是完成的攻擊步驟。

- GPT-5.6 Sol 最佳嘗試走完全部 32 步。
- GLM-5.2 約 11 步,DeepSeek-V4-Pro 約 8 步。
- 影片的觀察:**曲線越往後爬得越快**,頭部模型的長週期攻擊能力一年一個台階。

> ❓ 本筆記查到的 Daybreak 相關報導都沒有提到這張 AISI 32 步靶場圖,**只能當作影片的轉述**。

---

## 五、OpenAI Daybreak:分級訪問

| 級別 | 給誰 | 模型 |
|---|---|---|
| **Daybreak Blue** | 通過驗證的防禦團隊(漏洞偵測、惡意程式分析、事件應變) | GPT-5.6 Sol + 針對防禦工作調整過的防護 |
| **Daybreak Red** | 授權的漏洞研究、exploit 驗證、滲透測試 | **只有 Red 能用** GPT-5.6-Cyber |

- 兩級都要身分驗證、帳號安全措施、監控與法律聲明;2026-09-01 起所有 Daybreak 帳號強制使用硬體安全金鑰。
- **OpenCode 在事發那個週六拿到 Blue 權限,調查進度明顯加快**(✅ TechCrunch 引述 Raad)。OpenAI 也邀請 Hugging Face 加入同一個計畫(影片說法)。

**OpenAI 內部的「Advanced Cybersecurity Completion Rate」:**

| 模型 | 數字 |
|---|---|
| GPT-5.6-Cyber | 95.0% |
| GPT-5.5-Cyber(上一代) | 57.3% |
| GPT-5.6 Sol + Blue 防護 | 2.0% |
| GPT-5.6 Sol(一般防護) | 1.5% |

> ⚠️ **這個指標量的是模型「回答」敏感資安請求(exploit chain、繞過驗證、提權)的比例,不是拒答;不是攻擊任務的成功率。** 影片說「高級網路安全任務的完成率」,容易被理解成能力差了幾十倍——實際上主要是**願不願意做**的差距。

**影片的評價:** 護欄沒有做錯,錯在它只有一種檔位。同一個過滤器對攻擊者和救火隊執行同一套規則,防住的往往是守規矩的人。Daybreak 的分級思路是承認不對稱存在:**防護不撤,門檻變準。**

---

## 六、今晚就能做的四件事

1. **盤點密鑰託管在哪**:本機 `auth.json` 還是某個雲端網關?列一張表。
2. **每個密鑰加用量告警與限額**:帳單異動第一時間知道,別等月底。
3. **定期輪換密鑰**:外洩的窗口期越短,損失越小。
4. **能本地優先就本地優先**;用網關類工具的話,現在就去開告警,順便把每個密鑰的權限範圍縮到只開必要的。

**影片的走向判斷:**

- AI 對 AI 的攻防會成為常態,48 小時全自動攻擊只會更多。
- 密鑰與憑證的託管架構會被整個行業重新審視;雲端網關要證明自己守得住。
- 用量告警會變成平台預設;分級訪問會從個別公司的計畫變成行業標配。
- GLM-5.3-Flash 在事發當晚免費開放(✅ TechCrunch),也說明**開源模型正在變成防禦方的備胎,甚至主力**。

> 你的工具鏈裡每一層託管,都是一次信任外包。

---

## 七、核實結果

**✅ 已核實(TechCrunch / BleepingComputer):**

- 約 1.4% Console 用戶受影響,以 email 通知;攻擊者進入的是**正在下線的舊系統**。
- 只有 Console 受影響,開源 app 與 CLI 沒事(Raad:「those keys never come to us」)。
- Raad 稱攻擊持續 48 小時、使用 AI agent;防守方也讓 AI agent 全天候運作。
- AI 模型起初協助分析,惡意程式觸發安全過濾後拒答。
- OpenCode 之後取得 Daybreak Blue,調查改善。
- Anthropic、Google 封鎖外洩密鑰;OpenAI 協助恢復存取並退還被盜用的額度。
- David Sacks:「The guardrails backfired」。
- OpenCode 稱這是「大規模蒸餾攻擊」;⚠️ 也有人認為此說法誇大,蒸餾用途未經證實。
- GLM-5.3-Flash 當晚免費開放。
- Daybreak Blue / Red 的分級與資格要求;GPT-5.6-Cyber 只在 Red。

**⚠️ 需修正:**

- **95.0% / 1.5% / 2.0% / 57.3% 是「回答率」**,量的是模型肯不肯回答敏感資安請求,不是攻擊或防禦任務的成功率(見第五節)。

**❓ 未能核實:**

- UTC 00:30 的最早暴露時間(影片稱出自 OpenCode 通知信)。
- 個別用戶 700 + 1,000 多美元的損失、Google Cloud 專案被停權(當事人自述)。
- 英國 AISI 32 步網路靶場圖與各模型步數。
- 入侵手法、總受影響人數、總損失(OpenCode 尚未公布)。

---

## 八、應用案例

### 案例 1:團隊的 API 密鑰盤點表

| 密鑰 | 存放位置 | 託管方 | 月限額 | 告警門檻 | 上次輪換 |
|---|---|---|---|---|---|
| Anthropic(開發) | 本機 `~/.local/share/opencode/auth.json` | 無 | $200 | $50/日 | 2026-10-18 |
| OpenAI(CI) | GitHub Actions secret | GitHub | $100 | $30/日 | 2026-09-01 |
| Google(實驗) | 某雲端網關 | 第三方 | ⚠️ 未設 | ⚠️ 未設 | ⚠️ 從未 |

最後一列就是這次事件裡最容易受傷的那種:**託管在第三方、沒有限額、沒有告警、從沒輪換。**

### 案例 2:事件發生後的 30 分鐘應變清單

1. 到各模型平台**撤銷(revoke)**所有可能外洩的密鑰,再發新的。
2. 查看最近 72 小時的用量曲線,截圖保存異常時段,作為申請退款的證據。
3. 檢查雲端專案有沒有被風控停權;有的話先開工單說明是密鑰外洩。
4. 新密鑰先存在本機,並設好每日用量告警,再考慮要不要放回網關。

### 案例 3:防守方被拒答時的退路

情境:你要分析一段被混淆的惡意 JavaScript,商用模型拒答。

- **短期**:在隔離環境自架開源模型(例如 Hugging Face 事件中用過的 GLM 量化版)做解碼與行為分析。
- **中期**:若屬正式的防禦團隊,申請 Daybreak Blue 這類分級訪問計畫。
- **提醒**:自架模型也要放在無外網的沙箱裡跑,惡意樣本不要在日常工作機上執行。

---

## 來源

- YouTube:Why QQ〈AI在进攻,AI在拒守 | OpenCode事件:用户的账单炸了〉 https://www.youtube.com/watch?v=b3aYWkBf7jg (2026-10-22,官方 zh-Hans 字幕)
- TechCrunch,〈Hackers hit AI coding tool OpenCode, running up charges on users' AI accounts〉(2026-10-19): https://techcrunch.com/2026/10/19/hackers-hit-ai-coding-tool-opencode-running-up-charges-on-users-ai-accounts/
- BleepingComputer,〈OpenCode hack exposes API keys amid AI distillation attacks〉: https://bleepingcomputer.com/news/security/opencode-hack-exposes-api-keys-amid-ai-distillation-attacks
- The Decoder,〈OpenAI launches GPT-5.6-Cyber to help defenders find vulnerabilities before attackers do〉(2026-08-10): https://the-decoder.com/openai-launches-gpt-5-6-cyber-to-help-defenders-find-vulnerabilities-before-attackers-do/
- INSIDE,〈金鑰恐外洩!OpenCode 證實 Console 遭入侵,1.4% 使用者受影響〉: https://www.inside.com.tw/article/42669-opencode-console-breach-1-4-percent-distillation-attack-provider-keys
- Hugging Face 事件兩方說法:見本庫 `rsi-recursive-self-improvement-anthropic.md` §8.6
