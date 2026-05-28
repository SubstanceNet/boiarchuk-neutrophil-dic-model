# Reproduction protocol

This document describes how to reproduce the numerical results at three levels
of effort, from a seconds-long verification to a full multi-day re-run.

## Reference environment

Results were produced on a workstation with an 8-core / 16-thread x86-64 CPU,
32 GB RAM, running Linux (kernel 6.x), Python 3.10.12, with the pinned
dependencies in `requirements.txt` (NumPy 2.2.6, SciPy ≥ 1.13, Matplotlib
3.10.3). Wall-clock times below assume 16 threads; they scale roughly with
core count.

Full bit-level reproducibility additionally requires the same Python, NumPy and
SciPy versions and the same thread count, because the global optimizer
(`scipy.optimize.differential_evolution`) is order-sensitive across parallel
workers.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Level 1 — Verify (seconds)

Confirms that the package is structurally sound and that the published
conclusions still hold, without re-running any fit:

```bash
pytest -m "not slow"
```

This runs four test groups: structural smoke tests; data-integrity tests
(CSV values match the source dissertation literals); reproducibility tests; and
scientific-invariant tests (`tests/test_invariants.py`), which read the tracked
result artifacts and assert the manuscript's conclusions — the ~22× Group I vs
Group II hypocoagulation separation, the factor XIII nadir near −77 %, the day-11
peak, the mechanism-split fractions, the two-phase therapeutic window, the
good-basin count (n = 27), and the dose/timing thresholds. A green run is the
fastest meaningful confirmation that the repository is intact.

## Level 2 — Reproduce a key result (hours)

Re-run a single analysis from scratch and compare against the stored artifact.
The bootstrap ensemble is the natural target, since the virtual experiments
depend on it:

```bash
python -m analyses.05_v13_baseline.fit          # baseline fit (~12 min)
python -m analyses.22_predictive_check.run       # bootstrap, N=100 (~20 h)
python -m analyses.22_predictive_check.aggregate # writes ensemble.json + ensemble_members.json
```

Each bootstrap member is fit from a fixed per-member seed (`seed = i`), so the
ensemble is deterministic up to optimizer thread-ordering. Compare the
regenerated `ensemble.json` (parameter CIs, mechanism split) against the stored
values; they should agree within the reported confidence intervals.

A cheaper Level-2 target is the dose-response phase diagram, which reuses the
existing ensemble:

```bash
python -m analyses.30_myelosan_dose.run          # 22,500 simulations (~2 h)
python -m analyses.30_myelosan_dose.make_fig4
```

## Level 3 — Reproduce everything (tens of hours)

The full pipeline from scratch. Approximate wall-clock on 16 threads:

| Stage | Analysis | Time |
|-------|----------|------|
| Baseline fit | 05 | ~12 min |
| Bootstrap ensemble | 22 | ~20 h |
| Leave-one-out CV | 20 | ~5 h |
| N(t) perturbation | 21 | ~11 h |
| Dose-response | 30 | ~2 h |
| Intervention timing | 31 | ~3 min |
| Combinations | 32 | minutes |
| G1 severity validation | 33 | minutes |

Total is roughly 1.5–2 days of compute. Long fits should be run detached
(e.g. with `nohup`) and monitored by their process ID. The order matters only
in that analysis 22 must precede the virtual experiments (30–33), which consume
its ensemble.

## Determinism notes

- **Optimizer parallelism.** `differential_evolution(workers=-1)` is sensitive
  to OS thread scheduling; for strict bit-reproducibility use `workers=1` (much
  slower). With `workers=-1`, the fit cost converges reliably, while individual
  parameters in sloppy directions may vary at the 5th–6th significant figure —
  a variation that is within the reported confidence intervals and does not
  affect the scientific conclusions.
- **Version drift.** Minor NumPy/SciPy patch differences can shift integrator
  output below 1e-10. Pin the versions in `requirements.txt` for exact matching.
- **Stochastic conclusions.** Because the ensemble is a bootstrap, exact CI
  bounds shift slightly between full re-runs; the qualitative findings (group
  separation, mechanism split, therapeutic window, dose/timing thresholds) are
  stable, and the Level-1 invariant tests enforce exactly this stability.
