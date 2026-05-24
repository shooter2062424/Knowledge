# VoxCPM:無分詞器、可「用文字描述設計聲音」的開源 TTS

**主題分類:** AI / 語音合成(TTS)
**研究對象:** [OpenBMB/VoxCPM](https://github.com/OpenBMB/VoxCPM)
**整理日期:** 2026-05-25

---

## 1. 是什麼

OpenBMB 開源的文字轉語音(TTS)系統。最新版 **VoxCPM2 為 2B 參數模型**,特點是 **直接生成連續語音表示、繞過離散分詞(tokenizer-free)**,以追求更自然的表達。Apache-2.0 授權,**商用免費**,HuggingFace 與 ModelScope 皆可下載。

---

## 2. 技術架構

無分詞器的 **擴散自迴歸(diffusion autoregressive)** 架構,在 AudioVAE V2 潛空間運作,四階段管線:

```mermaid
flowchart LR
    A["LocEnc<br/>區域編碼"] --> B["TSLM"] --> C["RALM"] --> D["LocDiT<br/>區域擴散"] --> E["48kHz 高品質音頻"]
```

---

## 3. 四大能力

| 能力 | 說明 |
|---|---|
| **文字轉語音** | 標準 TTS,支援用自然語言描述風格。 |
| **語音設計** | 從文字描述「無中生有」造出全新聲音,**不需參考音頻**,可指定性別、年齡、音色、情感。 |
| **可控克隆** | 從短音頻克隆聲音,並用風格指導調整情感、語速、表現力。 |
| **終極克隆** | 結合參考音頻 + 其文本,保留每個聲學細節。 |

**多語言:** 支援 30 種語言,含中文方言(四川話、粵語、吳語等)。

---

## 4. 效能指標

- **Seed-TTS-eval:** 英文 WER 1.84%、中文 CER 0.97%。
- **多語言 ASR:** 30 語言平均 WER/CER 1.68%。
- **推理速度:** RTX 4090 上 RTF ≈ 0.3;以 Nano-vLLM 加速可至 ≈ 0.13。

---

## 5. 使用方式

- **Python API:** `VoxCPM.from_pretrained()` → `generate()`。
- **CLI:** 支援設計、克隆、批次處理等指令。
- **Web UI:** `python app.py --port 8808`。
- **生產部署:** Nano-vLLM 或 vLLM-Omni 提供高吞吐量服務。

---

## 來源

- [OpenBMB/VoxCPM (GitHub)](https://github.com/OpenBMB/VoxCPM)
