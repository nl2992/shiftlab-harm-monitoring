# When Does Paired Disagreement Gating Pay? Selective-Label Harm Monitoring

A deployed model is replaced or adapted, and the team wants to know, as labels arrive, whether its decisions cost more than a reference policy's. The study compares anytime-valid betting e-processes that query labels only on disagreements (gated) against uniform labelling at matched label spend: evidence growth, detection delay, behaviour when an intervention shifts the disagreement rate, null calibration, and a real-data check on electricity-demand paths. The repository holds the pre-registered protocols, results, implementation and the TMLR manuscript.

**Status.** Manuscript prepared for TMLR.

## Layout

- `papers/`: paper records and manuscript
- `docs/`: protocols, results and notes
- `src/shiftlab/`: implementation
- `scripts/`: experiment, analysis and audit scripts
- `tests/`: unit and regression tests
- `configs/`: experiment configuration

The manuscript sources are in `papers/paper1_decision_drift/manuscript`. The main implementation is `src/shiftlab/dive/gated_monitor_comparison.py`; scripts are under `scripts`. Protocols and result notes are under `docs/` (`gated_*`, `eia_*`, `r7_*`).

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

Large raw data and run outputs are not tracked. Scripts regenerate them, and each protocol or results note under `docs/` states the seeds and commands it used.

## Related repositories

The Python package `shiftlab` started as one shared codebase and is now split by paper. Each repository carries the part of it that the paper needs.

## License

MIT. See `LICENSE`.
