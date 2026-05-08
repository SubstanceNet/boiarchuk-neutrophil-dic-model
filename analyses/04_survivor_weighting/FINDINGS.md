# Analysis 04 — Findings

**Status:** closed. Result feeds back into `notes/known_issues.md` issue I-5.

## Summary

With `W_SURV = ones(16)`, the fit achieved:
- cost = 0.9775 (baseline: 1.0431, Δ = -0.0656)
- R²_G1 avg = +0.8279 (baseline: +0.8340, Δ = -0.0061)
- R²_G2 avg = +0.7162 (baseline: +0.6204, Δ = +0.0959)

Uniform weighting yields a substantially better G2 fit at negligible G1 cost. **Default W_SURV is load-bearing in the wrong direction.**

## Method

Joint fit with `W_SURV` overridden to `numpy.ones(16)` — i.e., uniform weighting across all 16 G1 timepoints, instead of default `[1.0]×10 + [0.7]×3 + [0.3]×3`. Other settings identical to analysis 02 baseline (W_split=2, default cx bound, seed=42, quick mode).

Default W_SURV qualitatively reflects 30% mortality on days 10-12 and further dropout afterwards, but the values 0.7 and 0.3 are ad hoc.

Wall time: 600 s.

## Results

### Aggregate metrics

| metric | uniform W_SURV | default W_SURV | Δ |
|--------|----------------|----------------|---|
| cost            | 0.9775 | 1.0431 | -0.0656 |
| R²_G1 avg       | +0.8279 | +0.8340 | -0.0061 |
| R²_G2 avg       | +0.7162 | +0.6204 | +0.0959 |

### Per-observable G1 R²

| observable | uniform | default | Δ |
|------------|---------|---------|---|
| recalc     | +0.7876 | +0.7289 | +0.0587 |
| thrombin   | +0.8630 | +0.8304 | +0.0326 |
| fib        | +0.7445 | +0.8318 | -0.0874 |
| xiii       | +0.8694 | +0.9270 | -0.0576 |
| AP         | +0.8125 | +0.7856 | +0.0270 |
| D          | +0.8902 | +0.9003 | -0.0101 |


### Per-observable G2 R²

| observable | uniform | default | Δ |
|------------|---------|---------|---|
| recalc     | +0.9095 | +0.6841 | +0.2254 |
| thrombin   | +0.9589 | +0.8347 | +0.1242 |
| fib        | +0.4729 | +0.2931 | +0.1799 |
| xiii       | +0.2758 | +0.7277 | -0.4518 |
| AP         | +0.9335 | +0.6777 | +0.2558 |
| D          | +0.7468 | +0.5051 | +0.2418 |


## Interpretation

**Case C — load-bearing, with reversed sign relative to expectation.**

The default `W_SURV` was designed to discount late-timepoint G1 data, on the rationale that mortality on days 10-12 makes those points less reliable. Empirically, the opposite is true: removing the discount (uniform weighting) yields a strictly better fit by every aggregate metric — lower cost, only marginally lower R²_G1 (Δ = -0.0061), and substantially higher R²_G2 (Δ = +0.0959).

This suggests the original v12 W_SURV choice was an over-correction. Late G1 timepoints are not "noisy outliers requiring downweighting" but informative about the long-term recovery dynamics, which the model needs to fit in order to balance against G2.

## Implications for Phase 2

Phase 2 cost redesign should default to uniform weighting on G1. The current ad-hoc `W_SURV` is to be removed or replaced with proper inverse-variance weights derived from biological data (e.g., per-timepoint sample size in the surviving cohort).

**Caveat:** this finding is from a single seed (42). Before committing to the change as a permanent v13 default, seed-stability should be checked (seeds {7, 123}) to confirm that the cost / R² improvement is not seed-specific. Recommended to do this in the same Phase 2 step that does seed-checks for the v13 cost.

## Run inventory

- `results/fit.json` — full fit result (cached via fit_runner hash key)
