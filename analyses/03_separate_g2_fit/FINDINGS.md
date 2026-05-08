# Analysis 03 — Findings

**Status:** closed. Result feeds back into `notes/known_issues.md` issue I-2.

## Summary

Separate-G2 fit gives R²_G2 avg = 0.8363. Joint-fit baseline (analysis 02): 0.6204. Δ = +0.2160 (Case C, Δ > 0.15). Joint architecture systematically sacrifices ~22 percentage points of G2 fit quality for G1 compatibility.

## Method

Separate G2-only fit, no constraint on joint behaviour with G1.
- 54 datapoints (9 timepoints × 6 observables)
- 26 free parameters
- Data/parameter ratio: 2.08
- Single seed (42), quick mode (DE 8×120 + NM + Powell + NM)
- Cost: same per-observable normalisation as joint cost, but G1 contribution
  and mechanism-split constraint set to zero
- Hn-saturation penalty preserved as numerical guard

Wall time: 510 s.

## Results (per-observable G2 R²)

| observable | separate-fit R² | joint-fit R² (analysis 02 baseline) | Δ |
|------------|------------------|--------------------------------------|---|
| recalc     | +0.9013 | +0.6841 | +0.2172 |
| thrombin   | +0.9936 | +0.8347 | +0.1589 |
| fib        | +0.5778 | +0.2931 | +0.2847 |
| xiii       | +0.7980 | +0.7277 | +0.0703 |
| AP         | +0.9283 | +0.6777 | +0.2506 |
| D          | +0.8191 | +0.5051 | +0.3140 |
| **avg**    | +0.8363 | +0.6204 | +0.2160 |


## Interpretation

**Case C confirmed (Δavg > 0.15).** The joint fit systematically constrains parameters toward G1-optimal regions, costing ~22 percentage points of G2 R² average. The deficit is largest for D (+0.314) and fib (+0.285), and smallest for XIII (+0.070, partly because XIII G2 is already supported by the cx ≤ 600 structural prior).

Note that the data/parameter ratio for separate G2 fit is 2.08, which raises overfitting concerns. However, the **systematic, uniform improvement across all 6 observables** (rather than spiky over-fits on individual observables) suggests the gap is largely architectural, not pure overfitting. If this were pure overfitting, we would expect very high R² on a few observables and modest improvement on others; instead, all six rise together.

## Implications for Phase 2

The current joint architecture (24 shared + 2 modifiers {km, tm}) is too constrained for the data. The v13 cost redesign cannot resolve this gap by changing per-observable normalisation alone — it requires architectural change.

Likely candidates for additional group-specific parameters:
- **c_f** (fib production / AP) — fib has the largest Δ (+0.285) and is the channel where IL-6-mediated hepatic synthesis could plausibly differ between groups under neutrophil suppression.
- **kna** (Hn formation rate) — neutrophil-driven coagulation pool; suppression of neutrophils may reduce this rate non-proportionally.
- **kx** (XIII liver resynthesis) — XIII has the smallest Δ but liver function may be differentially affected.

Quantitative assessment of which parameters most need group-specificity is to be done via Phase 2 step 1: profile likelihood with per-group residual decomposition.

## Run inventory

- `results/fit.json` — full fit result (params, metrics, cost, wall_time)
