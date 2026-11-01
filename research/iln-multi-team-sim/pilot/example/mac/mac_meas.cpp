#include "iln.h"
// MAC: 消費 ILN_MeasCfg
void on_meas_cfg(const ILN_MeasCfg &cfg) {
    uint32_t period_us = cfg.meas_period * 1000;   // ms -> us
    if (cfg.report_mode == REPORT_EVENT) arm_event();
    cell_table[cfg.carrier_idx].period = period_us;
    if (cfg.ho_enable) enable_ho();
}
