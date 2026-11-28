# Gain across disagreement rates: confirmation on fresh seeds

Written before this run. It follows `gain_vs_disagreement_protocol.md` and was chosen after its
results were seen, so it stays exploratory; the second estimator below was prompted by the five
low-budget misses there.

**Unchanged.** Settings A-E and N, budgets 0.02/0.05/0.10/0.20, arms `gated_ht_paced` and
`uniform_ht`, prediction `q/r` with `q = min(1, max(0.10, r/rho))`, tolerance 15%.

**New seeds.** 63200000-63200099 for every setting.

**Two growth estimators, both reported for every cell.**

1. *Per-stream stake* (as before): the best fixed grid stake of each stream on the common post-onset
   prefix, averaged over streams; ratio of the averages.
2. *One stake per cell*: average each grid stake's post-onset growth over the 100 streams, then take
   the best stake of that average, separately for each arm; ratio of the two. Interval from a
   bootstrap over streams that repeats the stake choice in every resample.

**Reading.** Estimator 2 picks one stake from 100 streams instead of one per stream, so hindsight
selection has much less room to inflate a small growth rate. If it is within 15% in the low-budget
cells where estimator 1 is not, the shortfall is a property of how growth was measured. Counts for
both estimators are reported whatever they show.

**Also reported.** Detection and delay for both arms, alarms in setting N and before onset.
