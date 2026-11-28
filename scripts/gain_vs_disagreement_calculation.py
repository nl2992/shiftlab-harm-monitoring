"""Growth calculation for the gain-versus-disagreement settings (computed after the run).

The method of scripts/g1_kelly_check.py: each arm's registered stake grid and support bound, query
coin enumerated exactly on the realised post-onset paths. No monitor output is used.
Run: PYTHONPATH=src:.:scripts python scripts/gain_vs_disagreement_calculation.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from g1_kelly_check import EPS, growth
from run_gain_vs_disagreement import BUDGETS, FLOOR, OUT, SEEDS, SETTINGS
from scipy.special import ndtr

from shiftlab.decision_harm_experiment import (
    SCENARIOS,
    ExperimentConfig,
    _generate,
    _source_action,
)
from shiftlab.dive.experiment import _binary_cost


def path(scenario_name: str, strength: float, threshold: float, seed: int):
    """Post-onset disagreements and paired costs, built as in comparison_seed."""
    scenario = next(s for s in SCENARIOS if s.name == scenario_name)
    config = ExperimentConfig(
        n=3200, d=16, evaluation_seeds=1, calibration_seeds=2, calibration_start=800, window=64,
        stride=32, alpha=0.05, eprocess_epsilon=EPS, seed_offset=seed, change_fraction=0.5,
        device="cpu",
    )  # fmt: skip
    _, frame, _, _ = _generate(scenario, seed, config)
    x = np.stack(frame.features.to_numpy()).astype(float)
    y = frame.target.to_numpy(dtype=float) > 0
    deployed = (ndtr((x[:, 0] - 0.9 * x[:, 1]) / 0.3) >= threshold).astype(int)
    if scenario.harmful_adaptation:
        if strength >= 1:
            deployed[1600:] = 1
        else:
            forced = np.random.default_rng(seed + 31_337).random(1600) < strength
            deployed[1600:][forced] = 1
    reference = _source_action(x, scenario)
    fn, fp = scenario.fn_cost, scenario.fp_cost
    cost = _binary_cost(deployed, y, fn, fp) - _binary_cost(reference, y, fn, fp)
    return (deployed != reference)[1600:], cost[1600:]


def main() -> None:
    measured = pd.read_csv(OUT / "summary.csv")
    rows = []
    for setting, (scenario, strength, threshold) in SETTINGS.items():
        if setting == "N":
            continue
        paths = [path(scenario, strength, threshold, seed) for seed in SEEDS]
        for budget in BUDGETS:
            cell = measured[measured.setting.eq(setting) & measured.budget_rate.eq(budget)].iloc[0]
            np.testing.assert_allclose(np.mean([a.mean() for a, _ in paths]), cell.rho_post)
            q = min(1.0, max(FLOOR, budget / cell.rho_post))
            gated, uniform = [], []
            for active, cost in paths:
                idle = np.full(len(cost), -EPS)
                gated.append(
                    growth(np.where(active, -EPS + cost / q, -EPS), np.where(active, q, 0.0), idle,
                           5 / q + EPS)
                )  # fmt: skip
                uniform.append(
                    growth(-EPS + cost / budget, np.full(len(cost), budget), idle, 5 / budget + EPS)
                )
            ratio = float(np.mean(gated) / np.mean(uniform))
            rows.append(
                {
                    "setting": setting,
                    "budget_rate": budget,
                    "calculation": ratio,
                    "small_signal": cell.predicted,
                    "measured": cell.measured,
                    "relative_error": cell.measured / ratio - 1,
                }
            )
    table = pd.DataFrame(rows)
    table.to_csv(OUT / "calculation.csv", index=False)
    print(table.to_string(index=False))
    print("within 15%:", int((table.relative_error.abs() <= 0.15).sum()), "of", len(table))


if __name__ == "__main__":
    main()
