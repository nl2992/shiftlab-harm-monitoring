"""Gating gain across disagreement rates (docs/gain_vs_disagreement_protocol.md).

Run: PYTHONPATH=src:.:scripts OMP_NUM_THREADS=1 python scripts/run_gain_vs_disagreement.py
Finished cells are saved and skipped when the script is started again.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from pathlib import Path

import numpy as np
import pandas as pd
from analyze_gated_monitor_comparison import paired_bootstrap
from run_uniform_ht_followup import one_task

OUT = Path(__file__).resolve().parents[1] / "outputs/gain_vs_disagreement"
# setting: (scenario, adaptation strength, deployed threshold)
SETTINGS = {
    "A": ("boundary_local_harm", 1.0, 0.35),
    "B": ("boundary_local_harm", 1.0, 0.5),
    "C": ("harmful_adaptation", 0.5, 0.5),
    "D": ("harmful_adaptation", 0.75, 0.5),
    "E": ("harmful_adaptation", 1.0, 0.5),
    "N": ("stationary", 1.0, 0.35),
}
BUDGETS = (0.02, 0.05, 0.1, 0.2)
SEEDS = range(63100000, 63100100)
FLOOR = 0.10


def summarise(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (setting, budget), cell in frame[frame.arm.eq("uniform_ht")].groupby(
        ["setting", "budget_rate"]
    ):
        rho = float(cell.disagreement_post.mean())
        q = min(1.0, max(FLOOR, budget / rho))
        row = {
            "setting": setting,
            "budget_rate": budget,
            "streams": len(cell),
            "rho_post": rho,
            "predicted": q / budget,
            "floor_bound": budget / rho < FLOOR,
            "gated_detection": cell.gated_detected.mean(),
            "uniform_detection": cell.detected.mean(),
            "gated_delay": cell.gated_delay.mean(),
            "uniform_delay": cell.censored_delay.mean(),
            "gated_labels": cell.gated_labels.mean(),
            "uniform_labels": cell.labels.mean(),
            "gated_false_alarms": int(cell.gated_false_alarm.sum()),
            "uniform_false_alarms": int(cell.false_alarm.sum()),
        }
        if setting != "N":
            ratio = paired_bootstrap(cell.gated_growth, cell.uniform_growth, ratio=True)
            row["measured"] = ratio["estimate"]
            row["lower"], row["upper"] = (
                ratio["lower_95_two_sided"],
                ratio["upper_95_two_sided"],
            )
            if ratio["estimate"] is not None:
                row["relative_error"] = ratio["estimate"] / row["predicted"] - 1
                row["within_15pct"] = bool(np.abs(row["relative_error"]) <= 0.15)
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    cells = OUT / "cells"
    cells.mkdir(parents=True, exist_ok=True)
    frames = []
    with ProcessPoolExecutor(8, mp_context=get_context("spawn")) as pool:
        for setting, (scenario, strength, threshold) in SETTINGS.items():
            for budget in BUDGETS:
                path = cells / f"{setting}_{budget}.parquet"
                if not path.exists():
                    tasks = [
                        (scenario, budget, seed, strength, threshold) for seed in SEEDS
                    ]
                    rows = [r for block in pool.map(one_task, tasks) for r in block]
                    partial = path.with_suffix(".partial")
                    pd.DataFrame(rows).assign(setting=setting).to_parquet(
                        partial, index=False
                    )
                    partial.replace(path)
                    print("finished", path.name, flush=True)
                frames.append(pd.read_parquet(path))
    summary = summarise(pd.concat(frames, ignore_index=True))
    summary.to_csv(OUT / "summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
