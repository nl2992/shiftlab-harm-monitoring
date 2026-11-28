"""Post-hoc diagnostic: what does the per-stream best-stake estimator read when growth is known?

Draws the query coins repeatedly on the same post-onset paths and applies the estimator used for
measured growth (best fixed stake per stream, then the ratio of means over streams). No monitor is
run. Run: PYTHONPATH=src:.:scripts python scripts/gain_vs_disagreement_estimator.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from g1_kelly_check import EPS, STAKES
from gain_vs_disagreement_calculation import path
from run_gain_vs_disagreement import BUDGETS, FLOOR, OUT, SEEDS, SETTINGS

DRAWS = 50


def best_stake(queried, cost, q, bound):
    """Per-draw best fixed-stake mean log-growth; queried is [draws, events]."""
    values = np.where(queried, -EPS + cost / q, -EPS)
    return np.max([np.log1p(s * values / bound).mean(axis=1) for s in STAKES], axis=0)


def main() -> None:
    table = pd.read_csv(OUT / "calculation.csv")
    rng = np.random.default_rng(63_200_000)
    simulated = {}
    for setting, (scenario, strength, threshold) in SETTINGS.items():
        if setting == "N":
            continue
        paths = [path(scenario, strength, threshold, seed) for seed in SEEDS]
        rho = np.mean([a.mean() for a, _ in paths])
        for budget in BUDGETS:
            q = min(1.0, max(FLOOR, budget / rho))
            gated = np.zeros(DRAWS)
            uniform = np.zeros(DRAWS)
            for active, cost in paths:
                coins = rng.random((DRAWS, len(cost)))
                gated += best_stake(active & (coins < q), cost, q, 5 / q + EPS)
                coins = rng.random((DRAWS, len(cost)))
                uniform += best_stake(coins < budget, cost, budget, 5 / budget + EPS)
            simulated[setting, budget] = float(gated.sum() / uniform.sum())
    table["estimator_on_simulated_coins"] = [
        simulated[row.setting, row.budget_rate] for row in table.itertuples()
    ]
    table.to_csv(OUT / "estimator.csv", index=False)
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
