# Can the alarm time be predicted before any monitor run? Exploratory protocol

Written while the confirmation run of `gain_vs_disagreement_confirm_protocol.md` was in progress,
before any of its results were opened.

**Question.** The growth calculation predicts the gain. Can the same quantity say, from pilot
streams alone, when each arm will alarm, so that a label budget can be sized before deployment?

**Rule (no fitted parameter).** For each grid stake, let `g0` and `g1` be the expected per-event
log-growth before and after onset, query coin enumerated, with the arm's own support bound. The
predicted alarm is the first post-onset event `T` at which
`mean over stakes of exp(800 g0 + T g1) >= 20`. The first 800 monitored events are pre-onset.
Pre-onset and post-onset query rates are `min(1, max(0.10, r/rho))` with each period's mean
disagreement rate; the uniform arm queries at `r`.

**Pilot and test.** `g0`, `g1`, `rho` come only from the paths of seeds 63100000-63100099 (no
monitor output). The test is the monitor runs on seeds 63200000-63200099: settings A-E, four
budgets, `gated_ht_paced` and `uniform_ht`, 40 arm-cells.

**Pre-stated reading.**
- Predicted `T <= 800`: detection at least 0.8, and median censored delay within 25% of `T`.
- Predicted `T > 1600`: detection below 0.5.
- `800 < T <= 1600`: no claim; reported only.

All 40 arm-cells are reported with the count that meets the reading.
