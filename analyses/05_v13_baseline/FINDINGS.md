# Analysis 05 — v13 baseline Findings

**Status:** closed. Reference baseline for Phase 2 v13-cost analyses.

## Summary

Single quick-mode v13 fit at default configuration (W_GROUP=(1.0, 1.0), W_SPLIT=2.0, cx bound (10, 600), uniform W_SURV hard-coded), seed=42:
- cost = 0.9589
- R²_G1 avg = +0.8334
- R²_G2 avg = +0.6920

Vs analysis 02 v12 baseline (R²_G1=0.834, R²_G2=0.620): R²_G1 essentially unchanged (-0.0006), R²_G2 substantially improved (+0.0716).

5 of 6 G2 observables improved significantly. xiii_G2 R² collapsed from 0.728 (v12) to 0.077 (v13 seed=42).

## Per-observable G2 R² (vs analysis 02 v12 baseline)

| observable | v12 baseline | v13 baseline (seed 42) | Δ |
|------------|--------------|------------------------|---|
| recalc     | +0.6841 | +0.9068 | +0.2227 |
| thrombin   | +0.8347 | +0.9468 | +0.1121 |
| fib        | +0.2931 | +0.4977 | +0.2046 |
| xiii       | +0.7277 | +0.0772 | -0.6505 |
| AP         | +0.6777 | +0.9638 | +0.2861 |
| D          | +0.5051 | +0.7594 | +0.2543 |

## Seed stability (3 seeds: 42, 7, 123)

| seed | cost | R²_G1 | R²_G2 | xiii_G2 | cx fitted |
|------|------|-------|-------|---------|-----------|
| 42  | 0.9589 | +0.8334 | +0.6920 | +0.0772 | 570.9 |
|   7 | 0.9666 | +0.8342 | +0.7141 | +0.3581 | 600.0 |
| 123 | 0.9622 | +0.8275 | +0.7517 | +0.4307 | 599.9 |

**Spreads:** Δcost = 0.0077, ΔR²_G2 = 0.0597, Δxiii_G2 = 0.3535, Δcx = 29.1.

cost is highly stable (one order of magnitude tighter than v12 cost spreads in analysis 02). R²_G1 stable. R²_G2 varies modestly. xiii_G2 varies widely (0.077-0.431) — significant identifiability issue at default cx bound.

## Interpretation

v13 baseline is a strict improvement over v12 baseline on 5 of 6 G2 observables, with one (xiii_G2) showing identifiability problems. Phase 2 step 1 (cost redesign) is partially successful: the architectural penalty quantified in analysis 03 (~22 R² points) is largely recovered for most observables.

The xiii_G2 instability is a structural feature, not a v13-cost defect. Analysis 06 (companion diagnostic) confirms this: the v13 landscape under default cx bound is multi-modal in the XIII channel, with optimiser landing in different basins depending on seed. This is the same phenomenon observed in analysis 02 under v12, now visible because v13 cost reveals it more sharply (gradient elsewhere is smoother).

The xiii channel identifiability is the central finding for Phase 2 step 2: group-specific cx (or related XIII-channel parameter) is the natural intervention to resolve both identifiability and the residual G2 fit gap simultaneously.

## Run inventory

- `results/fit.json` — main fit result, seed=42
- `results/seed_check.json` — additional seeds 7, 123
- `results/_cache/*.pkl` — hash-keyed fit caches under v13
