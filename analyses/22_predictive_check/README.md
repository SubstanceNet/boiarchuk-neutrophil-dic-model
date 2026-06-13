# Analysis 22 — Parametric bootstrap (predictive check)

## Question

What are the confidence intervals on v13 baseline parameters and on
predictions (R^2 per observable, mechanism split fractions, observable
trajectories) given the empirical residuals as estimate of measurement
noise?

## Method

Parametric Gaussian bootstrap, N=100 iterations:

1. Compute baseline RMSE per group (G1, G2) per observable from the
   v13 baseline best_x (analysis 05, seed 42). 12 sigma values total.
2. For each bootstrap iteration i ∈ 1..100, with seed = i:
   a. Sample synthetic data: y_synth(t) = baseline_pred(t) + N(0, sigma)
      independently per observable per group per timepoint. No clipping.
      G1 generated on 16 timepoints, G2 on 9 timepoints.
   b. Fit v13 model to synthetic data using full quick-mode pipeline
      (DE with popsize=15, maxiter=200, workers=-1; then Nelder-Mead;
      then Powell). Single seed per iter (seed=i).
   c. Save best_x, best_cost, per-iter metrics.
3. Aggregate ensemble of 100 best_x into:
   - Per-parameter CI: 2.5 and 97.5 percentiles
   - Per-prediction CI: ensemble of model predictions, 2.5/97.5 percentiles
     on R^2 per observable, mechanism split fractions, etc.

## Run

```bash
python -m analyses.22_predictive_check.run --run
```

The `--run` flag is required: without it the script prints a notice and exits
without computing (this is a long run). Wall-clock: 23.4 hours (actual, 100
members, zero failed).

## Outputs

- `results/iter_<seed>.json` — individual fit results
- `results/_cache/*.pkl` — fit caches
- `results/ensemble.json` — aggregated CI on parameters and predictions
- `results/sigmas.json` — sigma values used for noise generation
- `FINDINGS.md` — interpretation
