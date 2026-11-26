"""Exploratory pacing-floor follow-up (docs/pacing_floor_followup_protocol.md)."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from pathlib import Path

import numpy as np
import pandas as pd

import shiftlab.dive.gated_monitor_comparison as gmc

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/pacing_floor_followup"
FLOORS = (0.10, 0.25, 0.40)
STRENGTHS = (0.75, 1.00)
BUDGETS = (0.05, 0.10, 0.20)
SEEDS = range(62000000, 62000100)

_replay = gmc.replay_gated
_Pacer = gmc.DisagreementPacer


def floored_pacer(floor: float) -> type:
    class Floored(_Pacer):
        @property
        def propensity(self) -> float:
            return float(np.clip(self.target / max(float(np.mean(self.window)), 1e-6), floor, 1))

    return Floored


def one_task(task: tuple) -> list[dict]:
    seed, budget, strength = task
    inputs = {}

    def capture(**kwargs):
        inputs[kwargs["arm"]] = kwargs
        return _replay(**kwargs)

    gmc.replay_gated = capture
    try:
        records = gmc.comparison_seed("harmful_adaptation", seed, budget, "cpu", strength)
    finally:
        gmc.replay_gated = _replay
    base = {r["arm"]: r for r in records if r["engine"] == "fixed08"}
    onset = base["gated_ht_fixed"]["onset"]
    if onset is None:
        return []
    rows = []
    for label, arm, floor in [("fixed", "gated_ht_fixed", 0.10)] + [
        (f"paced_{f:.2f}", "gated_ht_paced", f) for f in FLOORS
    ]:
        gmc.DisagreementPacer = floored_pacer(floor)
        try:
            result = _replay(**inputs[arm])
        finally:
            gmc.DisagreementPacer = _Pacer
        alarm, processed = result.first_alarm, len(result.increments)
        detected = alarm is not None and alarm >= onset
        row = dict(
            seed=seed, budget_rate=budget, strength=strength, rule=label,
            detected=detected,
            false_alarm=alarm is not None and alarm < onset,
            censored_delay=alarm - onset if detected else max(0, 2400 - onset),
            processed=processed,
            labels=int(result.queried.sum()),
        )
        # The registered floor and fixed gating must reproduce the sweep's own arms.
        if floor == 0.10:
            assert alarm == base[arm]["first_alarm"] and processed == base[arm]["processed"]
        rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    if OUT.exists() and any(OUT.iterdir()):
        raise FileExistsError(f"refusing to overwrite {OUT}")
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = [(seed, b, s) for s in STRENGTHS for b in BUDGETS for seed in SEEDS]
    with ProcessPoolExecutor(args.workers, mp_context=get_context("spawn")) as pool:
        rows = [row for block in pool.map(one_task, tasks, chunksize=4) for row in block]
    data = pd.DataFrame(rows)
    data.to_parquet(OUT / "streams.parquet", index=False)
    table = data.groupby(["strength", "budget_rate", "rule"]).agg(
        n=("seed", "size"), detect=("detected", "mean"), delay=("censored_delay", "mean"),
        horizon=("processed", "mean"), labels=("labels", "mean"), false_alarms=("false_alarm", "sum"),
    )
    table.to_csv(OUT / "by_cell.csv")
    print(table.round(2).to_string())


if __name__ == "__main__":
    main()
