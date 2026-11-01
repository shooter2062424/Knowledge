# CTL: 消費 ILN_MeasCfg(只看 carrier 與 handover 旗標)
def handle_ILN_MeasCfg(msg):
    idx = msg["carrier_idx"]
    ho = msg.get("ho_enable", 0) == 1
    return idx, ho
