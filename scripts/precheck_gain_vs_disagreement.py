"""Threshold pre-check for docs/gain_vs_disagreement_protocol.md (no monitors, seeds 63000000-19).

Run: PYTHONPATH=src:. python scripts/precheck_gain_vs_disagreement.py
"""

import numpy as np
from scipy.special import ndtr

from shiftlab.decision_harm_experiment import (
    SCENARIOS,
    ExperimentConfig,
    _generate,
    _source_action,
)

out = {}
for name in ("stationary", "boundary_local_harm"):
    sc = next(s for s in SCENARIOS if s.name == name)
    for seed in range(63000000, 63000020):
        base = ExperimentConfig(
            n=3200,
            d=16,
            evaluation_seeds=1,
            calibration_seeds=2,
            calibration_start=800,
            window=64,
            stride=32,
            alpha=0.05,
            eprocess_epsilon=0.1,
            seed_offset=seed,
            change_fraction=0.5,
            device="cpu",
        )
        _, frame, oracle, timing = _generate(sc, seed, base)
        x = np.stack(frame.features.to_numpy()).astype(float)
        p = oracle.probability_positive.to_numpy(float)
        ref = _source_action(x, sc)
        sp = ndtr((x[:, 0] - 0.9 * x[:, 1]) / 0.3)
        for t in (0.2, 0.25, 0.35, 0.5, 0.65, 0.8, 0.95, 0.999):
            dep = (sp >= t).astype(int)
            e = np.where(dep == 1, 1 - p, 5 * p) - np.where(ref == 1, 1 - p, 5 * p)
            A = dep != ref
            out.setdefault((name, t), []).append(
                (
                    A[400:800].mean(),
                    A[1600:].mean(),
                    e[800:1600].mean(),
                    e[1600:].mean(),
                )
            )
for k, v in out.items():
    rho_val, rho_post, pre, post = np.mean(v, 0)
    print(k, f"{rho_val=:.3f} {rho_post=:.3f} excess_pre={pre:.3f} excess_post={post:.3f}")
