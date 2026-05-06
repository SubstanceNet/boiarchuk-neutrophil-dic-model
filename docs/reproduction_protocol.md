# Reproduction protocol

This document describes how to reproduce all numerical results in this repository, end-to-end, on the reference workstation. Conditions for full reproducibility are: identical Python version, identical NumPy/SciPy versions, identical hardware-thread count for parallel optimisation (because differential evolution is order-sensitive).

## Reference environment

- Hardware: HP Omen 17 (AMD Ryzen 9 8945HS, 8 cores / 16 threads; 32 GB DDR5-5600; project SSD `/media/ssd2`)
- OS: Pop!_OS 22.04 LTS, kernel 6.12.10-76061203-generic
- Python: 3.10.12
- NumPy: 2.2.6
- SciPy: ≥ 1.13 (any version compatible with NumPy 2.x)
- Matplotlib: 3.10.3
- pytest: ≥ 8.0

## Setup

```bash
source ~/python_projects/my_env/bin/activate
cd /media/ssd2/ai_projects/research/boiarchuk_neutrophil_dic_model_final
pip install -e .
```

## Verify Phase 0 contract

Phase 0 is closed iff the reproducibility tests are green:

```bash
pytest -m "not slow"
```

Expected: all tests in `tests/test_smoke.py`, `tests/test_data_integrity.py`, `tests/test_reproducibility.py` pass. The contract is: cost values from `src.fit.joint_cost` are identical (atol=1e-12) to `archive/v12/model_v12.py:_cost_core`.

If a test fails, investigate before doing any further work. Possible causes:

- SciPy version drift changed the integrator output beyond 1e-12. Pin SciPy more tightly in `requirements.txt`.
- Refactoring inadvertently changed numerical behaviour. Bisect against the v12 archive.
- Hardware-level non-determinism (rare; would manifest as 1e-14 differences, not test failures).

## Run the joint fit

### Quick smoke run (~1–2 min on 16 threads)

```bash
python -m src.cli --quick
```

Uses 2 DE seeds, smaller population, shorter NM iterations. Best cost typically lands within 5% of the full-run optimum but is not the publishable result.

### Full run (~10–30 min on 16 threads)

```bash
python -m src.cli
```

Uses 5 DE seeds (42, 7, 123, 2024, 999), full population, full NM/Powell. Output:

- stdout: full per-observable R² and RMSE for both groups; myelosan modifier values; parameter table with bound flags; total time.
- pickle: `results/phase0_run.pkl` with full state trajectories, fit metrics, parameters.

### Custom output path

```bash
python -m src.cli --output results/run_$(date +%Y%m%d_%H%M%S).pkl
```

### Custom seed list (for reproducibility experiments)

```bash
python -m src.cli --seeds 42 7
```

## Determinism notes

The fit pipeline is deterministic given a fixed seed list and fixed thread count, modulo:

- **OS scheduler** non-determinism in `differential_evolution(workers=-1)`. To enforce strict bit-reproducibility, use `--workers 1` (much slower but bit-deterministic).
- **NumPy/SciPy version drift** can introduce sub-1e-10 differences. The reproducibility test uses 1e-12 tolerance, so minor SciPy patches may break it. Pin SciPy harder if needed.
- **BLAS backend** (OpenBLAS vs MKL) can introduce ~1e-15 differences. Negligible for cost evaluation; could matter at the optimum to the last few digits.

For publication, the recommended protocol is:

1. Pin SciPy to a single version in `requirements.txt`.
2. Run with `--seeds 42 7 123 2024 999` and `--workers -1`.
3. Record OS, kernel, Python, NumPy, SciPy versions in the manuscript.
4. Save `results/phase0_run.pkl` and ship as supplementary material.

The fit cost converges; minor variation in the parameter vector at the 5th–6th significant figure across thread counts is expected and biologically irrelevant.

## Phase 1+ reproduction

Phases 1+ will add their own scripts under `analyses/` with per-analysis reproduction notes. The expectation is: every figure in the manuscript can be regenerated from the data CSVs by running one command, with no manual intervention.
