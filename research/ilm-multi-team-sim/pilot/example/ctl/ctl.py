# CTL: 消費 ILM_MeasCfg(只看 carrier 與 handover 旗標)
def handle_ILM_MeasCfg(msg):
    idx = msg["carrier_idx"]
    ho = msg.get("ho_enable", 0) == 1
    return idx, ho
