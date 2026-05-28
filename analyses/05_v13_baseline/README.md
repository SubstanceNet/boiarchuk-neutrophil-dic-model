# Analysis 05 — v13 baseline fit

## Question

What does the v13 cost yield in default configuration (W_SPLIT=2, default
cx bound, W_GROUP=(1,1), hard-coded uniform W_SURV)?

This is the v13 analogue of analysis 02 baseline. The only methodological
difference between v13 and the v12 baseline is uniform G1 timepoint
weighting (vs default `[1.0]*10 + [0.7]*3 + [0.3]*3`).

This addresses Phase 2 step 1: establish v13 baseline as the reference
point for subsequent group-specific architecture exploration (step 2)
and profile likelihood (step 3).

## Method

Single quick-mode fit, seed=42, all v13 defaults. No overrides.

## Expectations

Based on analysis 04 (uniform W_SURV with v12 cost):
- R²_G2 substantially higher (around +0.10) than v12 baseline (0.620)
- R²_G1 marginally lower (around -0.01)
- cost in different scale than v12 (~30 vs ~1, due to non-mean reduction);
  not directly comparable in absolute value
- parameters close to v12 baseline, modulo W_SURV effect

## Run

```bash
python -m analyses.05_v13_baseline.fit
```

Wall-clock: ~12 min on 16-thread workstation.
