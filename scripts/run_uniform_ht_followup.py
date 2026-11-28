"""Exploratory no-proxy uniform arm (docs/uniform_ht_followup_protocol.md).

Run: PYTHONPATH=src:.:scripts OMP_NUM_THREADS=1 python scripts/run_uniform_ht_followup.py
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from pathlib import Path

import numpy as np
import pandas as pd
from analyze_gated_monitor_comparison import paired_bootstrap

import shiftlab.dive.gated_monitor_comparison as gmc

OUT = Path(__file__).resolve().parents[1] / "outputs/uniform_ht_followup"
SCENARIOS = ("stationary", "benign_nuisance", "boundary_local_harm", "harmful_adaptation")
BUDGETS = (0.02, 0.05, 0.1, 0.2)
SEEDS = range(58400000, 58400100)
EPSILON = 0.1

_replay = gmc.replay_gated
_one = gmc._one_method


def one_task(task: tuple) -> list[dict]:
    scenario, budget, seed, *variant = task  # variant: adaptation strength, deployed threshold
    gated, traces = {}, []

    def capture_gated(**kwargs):
        result = _replay(**kwargs)
        gated[kwargs["arm"]] = result
        return result

    def capture_uniform(**kwargs):
        result = _one(**kwargs)
        if kwargs["method"] == "uniform_proxy" and not kwargs["config"].common_eprocess_bound:
            traces.extend(kwargs["event_trace_rows"])
        return result

    gmc.replay_gated, gmc._one_method = capture_gated, capture_uniform
    try:
        records = gmc.comparison_seed(scenario, seed, budget, "cpu", *variant)
    finally:
        gmc.replay_gated, gmc._one_method = _replay, _one
    base = {r["arm"]: r for r in records}
    onset = base["uniform_ppi"]["onset"]

    queried = np.array([bool(t["queried"]) for t in traces])
    q = np.array([float(t["propensity"]) for t in traces])
    centered = np.array(
        [float(t["learner_observed_excess_cost"]) if t["queried"] else 0.0 for t in traces]
    )
    h = np.array([float(t["proxy_prediction"]) for t in traces])
    # The traces must rebuild the registered proxy arm before they are reused without the proxy.
    np.testing.assert_allclose(
        h + queried * (centered - h) / q,
        [t["monitor_increment"] for t in traces],
        rtol=0,
        atol=1e-9,
    )
    np.testing.assert_allclose(q, budget, rtol=0, atol=1e-12)
    values = -EPSILON + queried * (centered + EPSILON) / q
    bounds = np.full(len(values), 5 / budget + EPSILON)
    assert np.all(np.abs(values) <= bounds * (1 + 1e-9))
    values = np.clip(values, -bounds, bounds)
    gains = np.log1p(values[:, None] * np.asarray(gmc.DEFAULT_STAKES) / bounds[:, None])
    pair = gmc.paired_growth(gated["gated_ht_paced"].component_log_gains, gains, onset)

    logs = {
        "uniform_ht": gmc.replay_mixture_log_e(values, float(bounds[0]), alpha=0.05),
        "uniform_ht__timans_grapa": gmc.replay_engine(values, bounds, "timans_grapa"),
    }
    rows = []
    for arm, log_e in logs.items():
        hits = np.flatnonzero(log_e >= -np.log(0.05))
        alarm = int(hits[0]) if len(hits) else None
        detected = alarm is not None and onset is not None and alarm >= onset
        rows.append(
            {
                "scenario": scenario,
                "budget_rate": budget,
                "seed": seed,
                "arm": arm,
                "detected": detected,
                "false_alarm": alarm is not None and (onset is None or alarm < onset),
                "censored_delay": None
                if onset is None
                else (alarm - onset if detected else max(0, 2400 - onset)),
                "labels": int(queried.sum()),
                "processed": len(values),
                "disagreement_post": base["gated_ht_paced"]["disagreement_post"],
                "gated_detected": base["gated_ht_paced"]["detected"],
                "gated_false_alarm": base["gated_ht_paced"]["false_alarm"],
                "gated_delay": base["gated_ht_paced"]["censored_delay"],
                "gated_labels": base["gated_ht_paced"]["labels"],
                "gated_growth": pair["first"],
                "uniform_growth": pair["second"],
            }
        )
        assert rows[-1]["labels"] == base["uniform_ppi"]["labels"]
        assert rows[-1]["processed"] == base["uniform_ppi"]["processed"]
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    if OUT.exists() and any(OUT.iterdir()):
        raise FileExistsError(f"refusing to overwrite {OUT}")
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = [(s, b, seed) for s in SCENARIOS for b in BUDGETS for seed in SEEDS]
    with ProcessPoolExecutor(args.workers, mp_context=get_context("spawn")) as pool:
        rows = [row for block in pool.map(one_task, tasks, chunksize=4) for row in block]
    frame = pd.DataFrame(rows)
    frame.to_parquet(OUT / "streams.parquet", index=False)
    table = frame.groupby(["scenario", "budget_rate", "arm"]).agg(
        detection=("detected", "mean"),
        false_alarms=("false_alarm", "sum"),
        censored_delay=("censored_delay", "mean"),
        labels=("labels", "mean"),
        streams=("seed", "nunique"),
    )
    table.to_csv(OUT / "summary.csv")
    primary = frame[frame.scenario.eq("boundary_local_harm") & frame.arm.eq("uniform_ht")]
    ratios = {
        str(b): paired_bootstrap(
            primary[primary.budget_rate.eq(b)].gated_growth,
            primary[primary.budget_rate.eq(b)].uniform_growth,
            ratio=True,
        )
        for b in BUDGETS
    }
    (OUT / "growth_ratios.json").write_text(json.dumps(ratios, indent=2) + "\n", encoding="utf-8")
    print(table.to_string())
    print(json.dumps(ratios, indent=2))


if __name__ == "__main__":
    main()
