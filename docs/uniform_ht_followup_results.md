# Uniform labelling without a proxy: results

Protocol `docs/uniform_ht_followup_protocol.md`; script `scripts/run_uniform_ht_followup.py`; output
`outputs/uniform_ht_followup/`. Exploratory, on the CPU replication streams (seeds
58400000-58400099), run after the registered results were known.

## Growth (`boundary_local_harm`, gated HT paced)

| r | 0.02 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| vs uniform HT, no proxy | 12.8 | 11.5 | 9.5 | 5.1 |
| 95% interval | 10.6-15.9 | 10.1-13.4 | 8.7-10.5 | 4.85-5.43 |
| Small-signal `min(1/rho, 1/r)` | 11.9 | 11.9 | 10.0 | 5.0 |
| Seeds with gated growth higher (of 100) | 99 | 100 | 100 | 100 |
| Uniform HT growth / uniform PPI growth, same streams | 1.67 | 1.65 | 1.59 | 1.52 |

The ratio against no-proxy uniform labelling is within 8% of the small-signal value at every budget.
The registered comparator (ridge proxy, wider bound) grows 1.5-1.7 times more slowly than the
no-proxy arm, which accounts for the larger ratio against it. The follow-up's gated growth equals the
CPU replication's on the same seeds.

## Detection (GT = gated HT paced, GF = gated HT fixed, U = uniform HT, +G = Timans GRAPA)

Paired wins/losses on the same seeds, with two-sided exact McNemar p-values.

| Scenario | r | GT / GF / U | GT vs U | GF vs U | GT+G / U+G | wins/losses (p) |
|---|---|---|---|---|---|---|
| boundary_local_harm | 0.02 | 0.91 / 0.89 / 0.00 | 91/0 | 89/0 | 0.93 / 0.00 | 93/0 (2e-28) |
| boundary_local_harm | 0.05 | 1.00 / 1.00 / 0.06 | 94/0 | 94/0 | 1.00 / 0.16 | 84/0 (1e-25) |
| boundary_local_harm | 0.10 | 1.00 / 1.00 / 0.32 | 68/0 | 68/0 | 1.00 / 0.51 | 49/0 (4e-15) |
| boundary_local_harm | 0.20 | 1.00 / 1.00 / 0.84 | 16/0 | 16/0 | 1.00 / 0.88 | 12/0 (5e-4) |
| harmful_adaptation | 0.02 | 0.00 / 0.02 / 0.00 | 0/0 | 2/0 | 0.02 / 0.01 | 2/1 (1.0) |
| harmful_adaptation | 0.05 | 0.20 / 0.24 / 0.05 | 19/4 | 23/4 | 0.23 / 0.28 | 11/16 (0.44) |
| harmful_adaptation | 0.10 | 0.80 / 0.79 / 0.46 | 37/3 | 40/7 | 0.87 / 0.53 | 36/2 (5e-9) |
| harmful_adaptation | 0.20 | 1.00 / 1.00 / 0.95 | 5/0 | 5/0 | 1.00 / 0.93 | 7/0 (0.016) |

- Under `harmful_adaptation` at r = 0.05, gated and no-proxy uniform labelling with GRAPA are not
  distinguishable on 100 streams (0.23 and 0.28). After the intervention the disagreement rate is
  about 0.41, where `min(1/rho, 1/r)` is about 2.4, so a small gating gain is expected there.
- Uniform PPI detects 0.00 in that cell. "Uniform detects nothing at r <= 0.05" holds for uniform
  PPI only, and the manuscript now says so.
- Mean censored delay and labels per cell are in `outputs/uniform_ht_followup/summary.csv`.
- Neither uniform HT arm alarmed in any `stationary` or `benign_nuisance` cell (100 streams each).
