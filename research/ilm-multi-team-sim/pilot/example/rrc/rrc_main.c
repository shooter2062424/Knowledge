#include "iln.h"
/* RRC: 產生 ILN_MeasCfg,並消費 ILN_SchedGrant */
void on_sched_grant(const ILN_SchedGrant *g) {
    int pwr_half_db = g->tx_power;      /* 0.5 dB 單位 */
    int h = g->harq_id;
    apply_power(pwr_half_db, h);
}
