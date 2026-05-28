# Analysis 06 — v13 cx-bound diagnostic Findings

**Status:** closed. Identifies multi-modal landscape structure in XIII channel under v13 cost.

## Summary

Five-point cx-bound sweep (cx upper ∈ {500, 600, 700, 1000, 2000}) at seed=42, plus seed-stability check at seeds {7, 123} for all five bounds (15 fits total). Landscape is qualitatively divided into two zones:

**Zone A (cx ≤ 500):** unique seed-stable optimum. cost ≈ 1.052, xiii_G2 R² ≈ 0.74 across all seeds. cx fitted ≈ 500 (saturates bound).

**Zone B (cx ≥ 600):** multi-modal landscape. Different seeds find different local optima with widely varying xiii_G2 R² ([-0.16, +0.76]) at near-equal cost.

The transition between zones is sharp at cx ≈ 500-600. Within Zone B, increasing the bound does not improve fit quality — it instead increases the variance between seeds.

## Evidence (15 fits)

### Zone A — bound = 500 (seed-stable)

| seed | cost | cx fitted | xiii_G2 |
|------|------|-----------|---------|
| 42  | 1.0521 | 500.0 | +0.7504 |
|   7 | 1.0524 | 498.6 | +0.7375 |
| 123 | 1.0522 | 500.0 | +0.7499 |

Δcost = 0.0003, Δxiii_G2 = 0.0130. **Unique optimum.**

### Zone B — bounds {600, 700, 1000, 2000} (multi-modal)

| bound | seed | cost | cx fitted | xiii_G2 |
|-------|------|------|-----------|---------|
| 600 | 42 | 0.9589 | 570.9 | +0.0772 |
| 600 |   7 | 0.9666 | 600.0 | +0.3581 |
| 600 | 123 | 0.9622 | 599.9 | +0.4307 |
| 700 | 42 | 1.0420 | 700.0 | +0.7610 |
| 700 |   7 | 0.9595 | 700.0 | +0.3543 |
| 700 | 123 | 1.0389 | 700.0 | +0.7092 |
| 1000 | 42 | 0.9566 | 995.3 | -0.1590 |
| 1000 |   7 | 0.9534 | 1000.0 | +0.2552 |
| 1000 | 123 | 1.0401 | 999.6 | +0.6559 |
| 2000 | 42 | 1.0269 | 1319.0 | +0.6662 |
| 2000 |   7 | 0.9479 | 1999.8 | +0.2523 |
| 2000 | 123 | 1.0117 | 1247.4 | -0.1615 |

Cost spreads across seeds at fixed bound: 0.05-0.10. xiii_G2 spreads: 0.35-0.83 R² points. **Cost does not discriminate basins** — small cost differences correspond to large differences in the mechanistic interpretation of xiii dynamics.

cx fitted almost always saturates the upper bound (within 1%). The data alone do not constrain cx to a unique value in Zone B.

## Interpretation

The v13 cost landscape has a strict zone structure in the XIII channel. Zone A (cx ≤ 500) is the only region where the optimum is unique and seed-stable. However, Zone A trades off mean G2 fit quality: avg R²_G2 ≈ 0.66 vs ≈ 0.69-0.75 in Zone B (depending on basin). Zone A is methodologically clean but biologically constrained.

Zone B contains higher-quality fits (higher R²_G2 avg in the favourable basin), but is multi-modal: which basin DE finds depends on seed. Cost cannot prefer one basin over another — they are cost-equivalent.

The v12 prior (cx ≤ 600) sits **at the transition** between zones, which explains why analysis 05 v13 baseline (bound=600, seed=42) showed xiii_G2 = 0.077 while seeds {7, 123} showed xiii_G2 ∈ [0.358, 0.431]: bound=600 is too narrow to clearly enter Zone B but too wide to be in stable Zone A.

## Implications for Phase 2 step 2

The analysis confirms — and quantifies — the central architectural problem identified in analysis 03 (joint architecture costs ~22 R² points G2). The fix is structural: introducing group-specific parameter(s) in the XIII channel.

Candidate intervention: make `cx` group-specific (analogous to existing `km, tm` modifiers for `kr, tp2`). This adds 1-2 parameters but should:
- Resolve the G1-vs-G2 XIII trade-off that drives Zone B multi-modality.
- Permit unique optimum at biologically reasonable cx values.
- Recover R²_G2 quality without sacrificing R²_G1.

If group-specific cx is insufficient, related XIII-channel parameters {ax, bx, kx} can be made group-specific in turn.

The choice between Zone A (constrain bound to 500) and Zone B (group-specific cx) was discussed in detail. Decision: **proceed to Phase 2 step 2 with current bound (10, 600), seek architectural resolution rather than fall back to tighter prior**. Tighter prior remains as fallback if architectural intervention is unsuccessful.

## Run inventory

- `results/sweep.json` — 5-point sweep, seed 42
- `results/seed_check.json` — 10 fits (5 bounds × seeds {7, 123})
- `results/_cache/*.pkl` — 15 hash-keyed fit caches under v13
