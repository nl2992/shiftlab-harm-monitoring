"""CPU replication of the registered gated-vs-ungated comparison seeds.

See docs/gated_monitor_cpu_replication.md. The registered run generated its streams on CUDA; the CPU
generator gives different streams from the same seeds, so this is a replication, not a replay.
Run: PYTHONPATH=src:.:scripts python scripts/replicate_gated_comparison_cpu.py
"""

from __future__ import annotations

import json
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from pathlib import Path

import pandas as pd
from analyze_gated_monitor_comparison import compare

from shiftlab.dive.gated_monitor_comparison import comparison_seed

OUT = Path(__file__).resolve().parents[1] / "outputs/gated_monitor_compare_rerun"
SCENARIOS = ("stationary", "benign_nuisance", "boundary_local_harm", "harmful_adaptation")


def one_task(task: tuple) -> list[dict]:
    return comparison_seed(*task)


def main() -> None:
    if OUT.exists() and any(OUT.iterdir()):
        raise FileExistsError(f"refusing to overwrite {OUT}")
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = [
        (scenario, seed, budget, "cpu")
        for scenario in SCENARIOS
        for budget in (0.02, 0.05, 0.1, 0.2)
        for seed in range(58400000, 58400100)
    ]
    with ProcessPoolExecutor(8, mp_context=get_context("spawn")) as pool:
        rows = [row for block in pool.map(one_task, tasks, chunksize=4) for row in block]
    frame = pd.DataFrame(rows)
    frame.to_parquet(OUT / "streams.parquet", index=False)
    summary, decision = compare(frame)
    summary.to_csv(OUT / "summary.csv", index=False)
    print(json.dumps({k: decision[k] for k in ("p1", "p2", "growth_prediction_table")}, indent=2))


if __name__ == "__main__":
    main()
