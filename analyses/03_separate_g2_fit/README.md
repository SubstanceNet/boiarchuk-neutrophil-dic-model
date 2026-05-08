# Analysis 03 — Separate G2 fit

## Question

In v12 development, separate G2 fits (R²_G2 = 0.868, 25 free parameters)
gave a much higher R² than the joint fit (R²_G2 = 0.598, 24 shared + 2
modifiers). Was the higher separate-fit R² overfitting (54 datapoints,
25 parameters → 2.16 ratio), or does the joint architecture systematically
sacrifice G2 fit quality for G1 fit quality?

This addresses **I-2** in `notes/known_issues.md`.

## Method

Run a quick-mode fit using only G2 data, all 26 parameters free
(no constraint that they match G1). Compare per-observable R² for G2
to the joint-fit values from analyses/02_cx_bound (baseline run).

## Decision rule

| Observation | Conclusion |
|-------------|------------|
| Separate-fit R²_G2 close to joint-fit R²_G2 (Δ < 0.05 avg) | Joint architecture not biased; v11.2 separate-fit value of 0.868 was overfitting. |
| Separate-fit R²_G2 substantially higher (Δ > 0.10 avg) | Joint architecture loses fit quality on G2 to maintain G1. v13 cost redesign should consider per-group balance. |
| Separate-fit R²_G2 similar but with different parameter values | Joint constraints push parameters off G2-optimal. Document for Phase 2. |

## Run

```bash
python -m analyses.03_separate_g2_fit.fit
```

Wall-clock: ~12 min on 16-thread workstation.
