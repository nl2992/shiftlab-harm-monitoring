# Alarm-time prediction: results

Protocol: `alarm_time_prediction_protocol.md`. Script: `scripts/predict_alarm_time.py`.
Predictions were saved 2026-11-28 11:23 EST, before any result of the test block was opened
(sha256 `81a9df29d6d548f7af9f8b2750de13474a8a9c1a8e85853f32833c668365297e`). Exploratory; not committed beforehand.

Pre-stated reading: 28 of 32 arm-cells with a claim (3 of 4 delay claims, 25 of 28 non-detection
claims). By arm: uniform 16 of 16, gated 12 of 16. The other 8 arm-cells had no claim.

| Setting | r | Arm | Predicted T | Detection | Median censored delay | Reading |
|---|---|---|---|---|---|---|
| A | 0.02 | gated_ht_paced | 2663 | 0.03 | 1600 | met |
| A | 0.02 | uniform_ht | 28908 | 0.00 | 1600 | met |
| A | 0.05 | gated_ht_paced | 1674 | 0.45 | 1600 | met |
| A | 0.05 | uniform_ht | 12410 | 0.00 | 1600 | met |
| A | 0.10 | gated_ht_paced | 1693 | 0.53 | 1579 | not met |
| A | 0.10 | uniform_ht | 6900 | 0.02 | 1600 | met |
| A | 0.20 | gated_ht_paced | 1693 | 0.53 | 1579 | not met |
| A | 0.20 | uniform_ht | 4123 | 0.04 | 1600 | met |
| B | 0.02 | gated_ht_paced | 928 | 0.94 | 854 | no claim |
| B | 0.02 | uniform_ht | 8196 | 0.00 | 1600 | met |
| B | 0.05 | gated_ht_paced | 520 | 1.00 | 482 | met |
| B | 0.05 | uniform_ht | 3442 | 0.07 | 1600 | met |
| B | 0.10 | gated_ht_paced | 403 | 1.00 | 372 | met |
| B | 0.10 | uniform_ht | 1857 | 0.44 | 1600 | met |
| B | 0.20 | gated_ht_paced | 403 | 1.00 | 371 | met |
| B | 0.20 | uniform_ht | 1063 | 0.87 | 1088 | no claim |
| C | 0.02 | gated_ht_paced | 5030 | 0.00 | 1600 | met |
| C | 0.02 | uniform_ht | 18834 | 0.00 | 1600 | met |
| C | 0.05 | gated_ht_paced | 3446 | 0.06 | 1600 | met |
| C | 0.05 | uniform_ht | 7899 | 0.01 | 1600 | met |
| C | 0.10 | gated_ht_paced | 2159 | 0.35 | 1600 | met |
| C | 0.10 | uniform_ht | 4250 | 0.08 | 1600 | met |
| C | 0.20 | gated_ht_paced | 1082 | 0.97 | 960 | no claim |
| C | 0.20 | uniform_ht | 2418 | 0.34 | 1600 | met |
| D | 0.02 | gated_ht_paced | 2695 | 0.01 | 1600 | met |
| D | 0.02 | uniform_ht | 9982 | 0.00 | 1600 | met |
| D | 0.05 | gated_ht_paced | 2531 | 0.10 | 1600 | met |
| D | 0.05 | uniform_ht | 4193 | 0.01 | 1600 | met |
| D | 0.10 | gated_ht_paced | 1641 | 0.66 | 1342 | not met |
| D | 0.10 | uniform_ht | 2262 | 0.28 | 1600 | met |
| D | 0.20 | gated_ht_paced | 822 | 1.00 | 708 | no claim |
| D | 0.20 | uniform_ht | 1294 | 0.68 | 1215 | no claim |
| E | 0.02 | gated_ht_paced | 1848 | 0.01 | 1600 | met |
| E | 0.02 | uniform_ht | 6828 | 0.00 | 1600 | met |
| E | 0.05 | gated_ht_paced | 2176 | 0.18 | 1600 | met |
| E | 0.05 | uniform_ht | 2869 | 0.05 | 1600 | met |
| E | 0.10 | gated_ht_paced | 1426 | 0.81 | 1176 | no claim |
| E | 0.10 | uniform_ht | 1549 | 0.59 | 1422 | no claim |
| E | 0.20 | gated_ht_paced | 714 | 1.00 | 528 | not met |
| E | 0.20 | uniform_ht | 887 | 0.96 | 884 | no claim |

The four that are not met all predicted a later alarm than observed, near a band edge:

- A, gated, r = 0.10 and 0.20: predicted 1693 against the 1600 cut-off, detection 0.53 against 0.5.
  The pacer queries every disagreement at both budgets, so these two are the same run.
- D, gated, r = 0.10: predicted 1641 against the 1600 cut-off, detection 0.66.
- E, gated, r = 0.20: predicted 714, median 528, 26% early against a 25% tolerance.

Observed afterwards: gated arm-cells with a median alarm inside the window alarmed 7-26% earlier
than predicted, and uniform ones landed within 9%. For a gated monitor the rule therefore errs
towards a later alarm, which over-provisions a budget.

Limits: the inputs come from labelled pilot streams that include the post-change distribution, as in
a power analysis, and the rule ignores the pacer's adjustment after a change in disagreement.
