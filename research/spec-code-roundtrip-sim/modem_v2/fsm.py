"""RRC 連線狀態機(模擬)。"""
from .trace import trace

T300_MS = 1000       # R-FSM-02
T304_MS = 200        # R-FSM-03(v1 為 150,偏離規格,見變更紀錄)
T_RESUME_MS = 300    # R-FSM-05
SETUP_RETRY_MAX = 3  # D-INT-03

TRANSITIONS = {      # R-FSM-01
    ("IDLE", "setup_req"): "SETUP_PENDING",
    ("SETUP_PENDING", "setup_ok"): "CONNECTED",
    ("SETUP_PENDING", "t300_expiry"): "IDLE",
    ("CONNECTED", "release"): "IDLE",
    ("CONNECTED", "handover_cmd"): "HO_EXEC",
    ("HO_EXEC", "ho_ok"): "CONNECTED",
    ("HO_EXEC", "t304_expiry"): "IDLE",
}

TRANSITIONS_ADD = {  # R-FSM-01(僅 Rel-21 生效)
    ("CONNECTED", "suspend"): "SUSPENDED",
    ("SUSPENDED", "resume_fast"): "CONNECTED",
    ("SUSPENDED", "t_resume_expiry"): "IDLE",
}


class Rrc:
    """RRC 狀態機;內部重試邏輯疊在規格轉移表之上。"""

    def __init__(self, release: int = 20) -> None:
        self.release = release
        self.state = "IDLE"
        self.retries = 0

    @trace("R-FSM-01", "R-FSM-05")
    def step(self, event: str) -> str:
        nxt = TRANSITIONS.get((self.state, event))
        if nxt is None and self.release >= 21:
            nxt = TRANSITIONS_ADD.get((self.state, event))
        if nxt is None:
            raise ValueError(f"illegal event {event} in {self.state}")
        self.state = nxt
        return nxt

    @trace("R-FSM-01", "R-FSM-02", "D-INT-03")
    def on_t300_expiry(self) -> str:
        """T300 逾時:規格要求回 IDLE;內部決定在上限內自動重發 setup_req。"""
        self.step("t300_expiry")
        if self.retries < SETUP_RETRY_MAX:
            self.retries += 1
            return self.step("setup_req")
        self.retries = 0
        return self.state
