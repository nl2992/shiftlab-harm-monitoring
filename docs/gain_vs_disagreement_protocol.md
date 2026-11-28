# Does the gating gain follow `min(1/rho, 1/r)` at other disagreement rates? Exploratory protocol

Written before any monitor run on these settings. Chosen after the registered results, so it is
exploratory and replaces none of them.

**Question.** The paper measures the gain over uniform labelling at one disagreement rate (about
0.085). Does it follow the prediction when the disagreement rate changes?

**Settings.** Seeds 63100000-63100099 for every setting, budgets 0.02/0.05/0.10/0.20.

| Setting | Scenario | Change | Post-onset rho |
|---|---|---|---|
| A | `boundary_local_harm` | deployed threshold 0.35 | about 0.05 |
| B | `boundary_local_harm` | registered pair (threshold 0.5) | about 0.085 |
| C, D, E | `harmful_adaptation` | intervention strength 0.50, 0.75, 1.00 | about 0.25, 0.33, 0.41 |
| N | `stationary` | deployed threshold 0.35 | null check |

**Choice of thresholds.** A pre-check with no monitors (20 streams, seeds 63000000-63000019) required
the expected excess cost to be at most the tolerance 0.1 without harm and above it after harm.
Threshold 0.35 passes (0.027, 0.211). Thresholds of 0.25 and below give too little harm (at most
0.089). Thresholds of 0.65 and above exceed the tolerance without harm (at least 0.165).

**Arms.** `gated_ht_paced` against `uniform_ht` (no proxy, bound `5/r + 0.1`, as in
`uniform_ht_followup_protocol.md`).

**Prediction.** Ratio of post-onset growth `= q/r`, with `q = min(1, max(0.10, r/rho))` and `rho` the
mean post-onset disagreement rate. This equals `min(1/rho, 1/r)` unless the pacer's floor of 0.10
binds; floor-bound cells spend above budget and are marked. Tolerance: within 15% of the prediction.

**Reported.** Every cell: growth ratio with the registered bootstrap, prediction, relative error,
detection and delay for both arms, and alarms in setting N and before onset. Cells outside the
tolerance are reported as such.
