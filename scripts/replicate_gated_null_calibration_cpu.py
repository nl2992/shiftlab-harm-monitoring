"""CPU replication of the registered null-calibration seeds, resumable in blocks.

See docs/gated_monitor_cpu_replication.md. As for the comparison, the CPU generator gives different
streams from the registered CUDA run's seeds, so this is a replication on new draws.
Run: PYTHONPATH=src:.:scripts OMP_NUM_THREADS=1 python scripts/replicate_gated_null_calibration_cpu.py
Finished blocks of 200 seeds are saved and skipped when the script is started again.
"""

from __future__ import annotations

import json
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from pathlib import Path

import pandas as pd
from analyze_gated_monitor_comparison import calibrate

from shiftlab.dive.gated_monitor_comparison import comparison_seed

OUT = Path(__file__).resolve().parents[1] / "outputs/gated_monitor_null_rerun"
SEEDS = range(58500000, 58502000)
CHUNK = 200


def one_task(task: tuple) -> list[dict]:
    return comparison_seed(*task)


def main() -> None:
    cells = OUT / "cells"
    cells.mkdir(parents=True, exist_ok=True)
    frames = []
    with ProcessPoolExecutor(8, mp_context=get_context("spawn")) as pool:
        for scenario in ("stationary", "benign_nuisance"):
            for budget in (0.02, 0.05, 0.1, 0.2):
                for first in range(SEEDS.start, SEEDS.stop, CHUNK):
                    path = cells / f"{scenario}_{budget}_{first}.parquet"
                    if not path.exists():
                        tasks = [
                            (scenario, seed, budget, "cpu") for seed in range(first, first + CHUNK)
                        ]
                        rows = [r for block in pool.map(one_task, tasks) for r in block]
                        partial = path.with_suffix(".partial")
                        pd.DataFrame(rows).to_parquet(partial, index=False)
                        partial.replace(path)
                        print("finished", path.name, flush=True)
                    frames.append(pd.read_parquet(path))
    summary, decision = calibrate(pd.concat(frames, ignore_index=True))
    summary.to_csv(OUT / "summary.csv", index=False)
    (OUT / "decision.json").write_text(json.dumps(decision, indent=2) + "\n", encoding="utf-8")
    print(summary[summary.arm.eq("gated_ht_paced")].to_string(index=False))
    print("largest upper bound:", summary.simultaneous_exact_upper.max())
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
