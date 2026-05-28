# Analysis 20 — Leave-One-Timepoint-Out Cross-Validation

## Question

Are the v13 baseline predictions robust to removal of any single
timepoint from the data? Which timepoints are critical structural
anchors for the model, and which are interpolated by the model
without information loss?

## Method

For each timepoint t in observed timelines (excluding t=0 anchor):
1. Remove all 6 observables for that timepoint from the corresponding
   group (G1 or G2).
2. Refit v13 model on reduced data (full quick-mode pipeline).
3. Predict the removed observables using the LOO-fitted model.
4. Compute PRESS statistic per observable, normalized by baseline RMSE^2.

Total: 15 G1 LOO fits + 8 G2 LOO fits = 23 LOO fits.
Quick-mode (popsize=15, maxiter=200) per fit, ~14 min each, ~5.4h total.

## PRESS metric

PRESS_k = sum_i (y_i_observed - y_i_predicted_when_left_out)^2 / RMSE_k_baseline^2

Interpretation per left-out timepoint:
- PRESS_k / 1 ≈ 1: prediction error similar to typical residuals (not overfit).
- PRESS_k / 1 >> 1: prediction error large vs typical (timepoint critical).
- PRESS_k / 1 << 1: prediction error smaller than typical (suspicious).

## Run

```bash
python -m analyses.20_loo_timepoint.run
```

## Outputs

- `results/loo_<group>_<t>.json` — per-LOO results
- `results/summary.json` — aggregated PRESS table
- `FINDINGS.md` — interpretation
