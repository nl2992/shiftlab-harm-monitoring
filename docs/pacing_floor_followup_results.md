# Pacing floor follow-up: results

Protocol: [pacing_floor_followup_protocol.md](pacing_floor_followup_protocol.md). Exploratory.
100 fresh seeds per cell (62000000-62000099), CPU. Script `scripts/run_pacing_floor_followup.py`,
output `outputs/pacing_floor_followup/`. Floor 0.10 and fixed gating reproduce the sweep code's own
alarm times and horizons on every stream (asserted in the script). No pre-onset alarms in any cell.

| s | r | rule | detection | censored delay | horizon | labels |
|---|---|---|---:|---:|---:|---:|
| 0.75 | 0.05 | fixed | 0.13 | 1,480 | 1,195 | 120 |
| 0.75 | 0.05 | paced_0.10 | 0.09 | 1,591 | 2,148 | 119 |
| 0.75 | 0.05 | paced_0.25 | 0.07 | 1,573 | 1,680 | 120 |
| 0.75 | 0.05 | paced_0.40 | 0.09 | 1,542 | 1,372 | 119 |
| 0.75 | 0.10 | fixed | 0.60 | 917 | 1,325 | 240 |
| 0.75 | 0.10 | paced_0.10 | 0.55 | 1,352 | 2,313 | 236 |
| 0.75 | 0.10 | paced_0.25 | 0.55 | 1,352 | 2,312 | 236 |
| 0.75 | 0.10 | paced_0.40 | 0.56 | 1,226 | 2,029 | 239 |
| 0.75 | 0.20 | fixed | 1.00 | 552 | 2,042 | 479 |
| 0.75 | 0.20 | paced_0.10 | 1.00 | 788 | 2,400 | 409 |
| 0.75 | 0.20 | paced_0.25 | 1.00 | 788 | 2,400 | 409 |
| 0.75 | 0.20 | paced_0.40 | 1.00 | 788 | 2,400 | 409 |
| 1.00 | 0.05 | fixed | 0.19 | 1,390 | 1,115 | 120 |
| 1.00 | 0.05 | paced_0.10 | 0.14 | 1,560 | 2,118 | 119 |
| 1.00 | 0.05 | paced_0.25 | 0.15 | 1,487 | 1,505 | 119 |
| 1.00 | 0.05 | paced_0.40 | 0.16 | 1,448 | 1,256 | 119 |
| 1.00 | 0.10 | fixed | 0.67 | 769 | 1,220 | 240 |
| 1.00 | 0.10 | paced_0.10 | 0.79 | 1,194 | 2,300 | 237 |
| 1.00 | 0.10 | paced_0.25 | 0.79 | 1,157 | 2,243 | 238 |
| 1.00 | 0.10 | paced_0.40 | 0.77 | 945 | 1,785 | 240 |
| 1.00 | 0.20 | fixed | 1.00 | 401 | 1,797 | 480 |
| 1.00 | 0.20 | paced_0.10 | 1.00 | 638 | 2,400 | 415 |
| 1.00 | 0.20 | paced_0.25 | 1.00 | 638 | 2,400 | 415 |
| 1.00 | 0.20 | paced_0.40 | 1.00 | 638 | 2,400 | 415 |

## Reading

- At r = 0.10, raising the floor from 0.10 to 0.40 shortens censored delay by 9% (s = 0.75) and
  21% (s = 1.00), and the monitor still runs 1.5x as long as fixed gating, at similar detection.
- At r = 0.05 delay shortens by 3% and 7%; the horizon stays 1.13-1.15x that of fixed gating.
  Detection is low in these cells, so censored delay mostly reflects non-detections.
- At r = 0.20 the floor has no material effect.
- Fixed gating keeps the shortest delay wherever it detects often. The floor narrows the gap.
- Detection differences between rules are small relative to 100-seed noise except s = 1.00,
  r = 0.10, where fixed gating (0.67) is below the paced rules (0.77-0.79) on these seeds.
