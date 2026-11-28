# Gating gain across disagreement rates: results

Protocol `docs/gain_vs_disagreement_protocol.md`; pre-check `scripts/precheck_gain_vs_disagreement.py`;
run `scripts/run_gain_vs_disagreement.py`; output `outputs/gain_vs_disagreement/`. Exploratory,
seeds 63100000-63100099, CPU generator. 2,400 streams.

## Growth ratio, gated HT paced against uniform HT without a proxy

Prediction (from the protocol): `q/r`. Tolerance 15%.

| Setting | rho | r | Predicted | Measured (95% interval) | Error | Detection gated / uniform |
|---|---|---|---|---|---|---|
| A | 0.050 | 0.02 | 19.9 | 10.4 (8.3-13.6) | -48% **miss** | 0.08 / 0.00 |
| A | 0.050 | 0.05 | 19.9 | 14.8 (12.1-18.4) | -26% **miss** | 0.42 / 0.00 |
| A | 0.050 | 0.10 | 10.0 | 9.8 (8.1-12.1) | -2% | 0.46 / 0.04 |
| A | 0.050 | 0.20 | 5.0 | 5.0 (4.3-5.7) | -1% | 0.46 / 0.07 |
| B | 0.084 | 0.02 | 11.9 | 9.1 (7.9-10.8) | -23% **miss** | 0.92 / 0.01 |
| B | 0.084 | 0.05 | 11.9 | 12.3 (11.0-14.0) | +3% | 0.99 / 0.04 |
| B | 0.084 | 0.10 | 10.0 | 10.0 (9.1-11.0) | -0% | 0.99 / 0.31 |
| B | 0.084 | 0.20 | 5.0 | 5.1 (4.8-5.4) | +2% | 0.99 / 0.79 |
| C | 0.251 | 0.02* | 5.0 | 3.5 (3.0-4.3) | -29% **miss** | 0.00 / 0.00 |
| C | 0.251 | 0.05 | 4.0 | 3.3 (2.9-3.8) | -16% **miss** | 0.06 / 0.00 |
| C | 0.251 | 0.10 | 4.0 | 3.8 (3.4-4.4) | -4% | 0.36 / 0.03 |
| C | 0.251 | 0.20 | 4.0 | 3.9 (3.5-4.3) | -3% | 0.92 / 0.27 |
| D | 0.336 | 0.02* | 5.0 | 4.4 (3.8-5.1) | -12% | 0.03 / 0.00 |
| D | 0.336 | 0.05 | 3.0 | 3.1 (2.8-3.4) | +3% | 0.13 / 0.00 |
| D | 0.336 | 0.10 | 3.0 | 3.1 (2.9-3.5) | +6% | 0.64 / 0.26 |
| D | 0.336 | 0.20 | 3.0 | 3.1 (2.9-3.3) | +4% | 0.99 / 0.76 |
| E | 0.418 | 0.02* | 5.0 | 4.5 (4.0-5.1) | -9% | 0.05 / 0.00 |
| E | 0.418 | 0.05 | 2.4 | 2.5 (2.4-2.7) | +6% | 0.14 / 0.07 |
| E | 0.418 | 0.10 | 2.4 | 2.7 (2.5-2.9) | +12% | 0.78 / 0.60 |
| E | 0.418 | 0.20 | 2.4 | 2.5 (2.4-2.7) | +7% | 0.99 / 0.97 |

`*` pacer floor of 0.10 binds, so the gated arm spends above budget.

15 of 20 cells are within 15%, including all 10 cells at r >= 0.10 (within 12%). Gated detection is
at least uniform detection in every cell. The five misses are at r <= 0.05 and fall below the
prediction.

`rho` is the realised post-onset disagreement rate. It needs no labels, but in C-E it is known only
once the intervention has happened.

## Null checks

- Setting N (stationary, threshold 0.35): no alarm by either arm in any cell.
- Before onset, the gated arm alarmed on one stream (seed 63100061) in settings B-E at r >= 0.05:
  1/100 per cell (exact 95% upper bound 4.7%). The uniform arm never did.

## Why the five cells miss (post-hoc diagnostics)

- The exact growth calculation with each arm's stake grid and bound
  (`scripts/gain_vs_disagreement_calculation.py`) agrees with `q/r` within 1.5% in every cell, so the
  stake cap is not the reason.
- Measured growth takes the best fixed stake separately on each stream, after the path is seen. In
  the miss cells the uniform arm's measured growth exceeds its exact expectation more than the gated
  arm's does, which lowers the ratio.
- `scripts/gain_vs_disagreement_estimator.py` applies that estimator to 50 simulated sets of query
  coins on the same paths. It gives:

| Miss cell | A 0.02 | A 0.05 | B 0.02 | C 0.02 | C 0.05 |
|---|---|---|---|---|---|
| Calculation | 20.0 | 20.2 | 11.9 | 5.0 | 4.0 |
| Estimator on simulated coins | 13.0 | 15.8 | 11.1 | 4.0 | 3.4 |
| Measured | 10.4 | 14.8 | 9.1 | 3.5 | 3.3 |

  The estimator accounts for most of the shortfall in four cells, whose simulated values lie inside
  the measured intervals. In B at 0.02 it accounts for less (11.1 against 9.1). The simulation holds
  `q` constant and uses the whole post-onset path, so it only approximates the measured run.
- The same setting B at r = 0.02 measured 12.8 on seeds 58400000-58400099
  (`uniform_ht_followup_results.md`) and 9.1 here, so this cell varies between seed blocks.
- At r = 0.20 the estimator reads 4.7-5.0 where the calculation gives 5.0-5.1 (A, B).
