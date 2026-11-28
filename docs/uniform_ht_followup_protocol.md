# Uniform labelling without a proxy: exploratory follow-up

Written before the run. Chosen after the registered comparison and its CPU replication were known,
so it is exploratory and replaces no registered result.

**Question.** The registered uniform comparator carries a ridge proxy, whose support bound
`5.1(2/r - 1)` is nearly twice the no-proxy bound `5/r + 0.1`. How large is the gating gain against
uniform labelling without a proxy?

**Arm.** `uniform_ht`: the same query decisions, labels, spend and stopping time as `uniform_ppi`,
with increment `-0.1 + L c / r`, bound `5/r + 0.1`, the registered stake mixture, and a Timans GRAPA
variant.

**Streams.** The CPU replication streams: four scenarios, budgets 0.02/0.05/0.10/0.20, seeds
58400000-58400099.

**Reported.** Ratio of post-onset growth of `gated_ht_paced` to `uniform_ht` on
`boundary_local_harm` (bootstrap as in the registered analysis), detection and delay per cell, and
alarms in the null scenarios. All cells are reported whatever the outcome.

**Estimate seen beforehand.** The growth calculation with `h = 0` on 20 streams gave about
12/12/10/5 across the four budgets.
