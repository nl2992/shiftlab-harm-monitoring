# Pacing floor follow-up: protocol

Exploratory follow-up, chosen after the R7 sweep results were known. It is not part of the frozen
registration and does not replace any registered result. Written before the runs below.

**Question.** The registered paced arm clips its query rate to [0.10, 1] and detects later than fixed
gating. Does a higher floor shorten the delay while keeping a longer horizon than fixed gating?

**Design.** `harmful_adaptation`, strengths 0.75 and 1.00, budgets 0.05, 0.10 and 0.20, 100 fresh seeds
62000000-62000099. Floors 0.10 (registered), 0.25 and 0.40 for the paced gated-HT arm, plus fixed
gating, all on the same streams and query coins. Registered betting engine, no other change.

**Endpoints per cell.** Detection, censored delay, events processed (horizon), labels, pre-onset alarms.
All floors and cells are reported.
