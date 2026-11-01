#include "ilm.h"
/* RRC: 產生 ILM_MeasCfg,並消費 ILM_SchedGrant */
void on_sched_grant(const ILM_SchedGrant *g) {
    int pwr_half_db = g->tx_power;      /* 0.5 dB 單位 */
    int h = g->harq_id;
    apply_power(pwr_half_db, h);
}
