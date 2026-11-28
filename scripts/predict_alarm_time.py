"""Alarm-time prediction from pilot paths (docs/alarm_time_prediction_protocol.md).

Run before reading the test results: PYTHONPATH=src:.:scripts python scripts/predict_alarm_time.py
Then, once the confirmation run has finished, add --compare.
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
from g1_kelly_check import EPS, STAKES
from gain_vs_disagreement_calculation import path
from run_gain_vs_disagreement import BUDGETS, CONFIRM_OUT, FLOOR, OUT, SEEDS, SETTINGS
from scipy.special import logsumexp

PRE, WINDOW = 800, 1600
PREDICTIONS = OUT.with_name("alarm_time_prediction")


def stake_growth(active, cost, q, bound):
    """Expected log-growth of each grid stake; the query coin is enumerated."""
    stakes = np.asarray(STAKES)[:, None]
    queried = np.log1p(stakes * (-EPS + cost / q) / bound)
    skipped = np.log1p(stakes * -EPS / bound)
    rate = np.where(active, q, 0.0)
    return (rate * queried + (1 - rate) * skipped).mean(axis=1)


def alarm_time(g0, g1, horizon=100_000):
    """First post-onset event at which the expected log-path mixture reaches 1/alpha."""
    times = np.arange(1, horizon + 1)
    log_e = logsumexp(PRE * g0[:, None] + np.outer(g1, times), axis=0) - np.log(len(g0))
    hits = np.flatnonzero(log_e >= np.log(20))
    return int(times[hits[0]]) if len(hits) else np.inf


def predict() -> pd.DataFrame:
    rows = []
    for setting, (scenario, strength, threshold) in SETTINGS.items():
        if setting == "N":
            continue
        paths = [path(scenario, strength, threshold, seed, start=PRE) for seed in SEEDS]
        periods = [slice(0, PRE), slice(PRE, None)]
        rho = [np.mean([a[p].mean() for a, _ in paths]) for p in periods]
        for budget in BUDGETS:
            for arm in ("gated_ht_paced", "uniform_ht"):
                growth = []
                for p, share in zip(periods, rho, strict=True):
                    gated = arm == "gated_ht_paced"
                    q = min(1.0, max(FLOOR, budget / share)) if gated else budget
                    growth.append(
                        np.mean(
                            [
                                stake_growth(
                                    a[p] if gated else np.ones_like(a[p]), c[p], q, 5 / q + EPS
                                )
                                for a, c in paths
                            ],
                            axis=0,
                        )
                    )
                rows.append(
                    {
                        "setting": setting,
                        "budget_rate": budget,
                        "arm": arm,
                        "predicted_delay": alarm_time(*growth),
                    }
                )
    return pd.DataFrame(rows)


def compare(table: pd.DataFrame) -> pd.DataFrame:
    out = []
    for row in table.itertuples():
        cell = pd.read_parquet(CONFIRM_OUT / "cells" / f"{row.setting}_{row.budget_rate}.parquet")
        cell = cell[cell.arm.eq("uniform_ht")]
        gated = row.arm == "gated_ht_paced"
        detected = cell["gated_detected" if gated else "detected"].astype(float).mean()
        delay = cell["gated_delay" if gated else "censored_delay"].astype(float).median()
        t = row.predicted_delay
        met = None
        if t <= WINDOW / 2:
            met = bool(detected >= 0.8 and abs(delay / t - 1) <= 0.25)
        elif t > WINDOW:
            met = bool(detected < 0.5)
        out.append({**row._asdict(), "detection": detected, "median_delay": delay, "met": met})
    return pd.DataFrame(out).drop(columns="Index")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", action="store_true")
    PREDICTIONS.mkdir(parents=True, exist_ok=True)
    saved = PREDICTIONS / "predictions.csv"
    if parser.parse_args().compare:
        table = compare(pd.read_csv(saved))
        table.to_csv(PREDICTIONS / "comparison.csv", index=False)
        print(table.to_string(index=False))
        print("met:", int(table.met.eq(True).sum()), "of", int(table.met.notna().sum()))
    else:
        if saved.exists():
            raise FileExistsError(f"refusing to overwrite {saved}")
        table = predict()
        table.to_csv(saved, index=False)
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
