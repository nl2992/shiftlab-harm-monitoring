# Gated-vs-ungated comparison: CPU replication

Script `scripts/replicate_gated_comparison_cpu.py`; output `outputs/gated_monitor_compare_rerun/`.
1,600 tasks: the registered scenarios, budgets and seeds 58400000-58400099, analysed with the
registered `compare` function. The registered run generated streams on CUDA. The CPU generator gives
different streams from the same seeds, so this is a replication on new draws, run after the
registered results were known. It does not replace them.

| Quantity | Registered run (CUDA) | CPU replication |
|---|---|---|
| P1 growth ratio, r = 0.20 (95% interval) | 7.20 (6.88-7.55) | 7.77 (7.38-8.20), passes |
| P2 discordant wins/losses, r = 0.05 | 100/0 | 100/0, passes |
| Measured growth ratio, r = 0.02/0.05/0.10/0.20 | 17.5/20.6/14.7/7.2 | 21.4/19.1/15.2/7.8 |
| gated HT paced, r = 0.05: detection, delay, labels | 1.00, 496, 118 | 1.00, 501, 119 |
| gated HT paced + GRAPA | 1.00, 469, 118 | 1.00, 480, 119 |
| PPE gated | 0.99, 451, 118 | 1.00, 432, 119 |
| uniform PPI | 0.00, 1,616, 114 | 0.00, 1,608, 115 |
| uniform PPI + GRAPA | 0.01, 1,611, 114 | 0.03, 1,597, 115 |
| Xu active | 0.00, 1,616, 115 | 0.00, 1,608, 115 |
| harmful adaptation, r = 0.10, fixed vs paced detection (GRAPA) | 0.86 vs 0.76 | 0.90 vs 0.87 |

- Against the registered prediction (18/18/15/7.5) the CPU ratios differ by 19%, 6%, 1% and 4%.
  Against the registered-grid growth calculation (20.0/19.7/15.5/7.6) they differ by at most 7%.
- Boundary harm at r <= 0.05: registered ungated arms detect at most 0.03. Gated HT arms detect 0.80-1.00,
  gated PPI arms 0.71 or more, and the gated empirical-Bernstein arm 0.36 at r = 0.02 (the
  registered run reported 0.82-1.00 for all gated arms).
- No harm monitor alarmed in the stationary or benign-nuisance cells.

## Null calibration

Script `scripts/replicate_gated_null_calibration_cpu.py`; output `outputs/gated_monitor_null_rerun/`.
The registered seeds 58500000-58501999, 2,000 streams per null scenario and budget, analysed with the
registered `calibrate` function. New draws on the CPU generator, as above.

| Quantity | Registered run (CUDA) | CPU replication |
|---|---|---|
| gated HT paced, alarms per 2,000 by cell | 0-6 | 1-5 |
| gated HT paced, largest simultaneous exact upper bound | 0.764% | 0.689% |
| Largest upper bound in the panel (PPE gated) | 1.953% (24/2,000) | 2.139% (27/2,000) |
| Arms passing the 5% bound | all | all |
