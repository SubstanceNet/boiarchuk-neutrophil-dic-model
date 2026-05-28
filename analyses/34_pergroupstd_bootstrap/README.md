# Analysis 34 — per-group-std normalization bootstrap (sensitivity)

## Question

Is the XIII-channel under-determination (41% of analysis-22 bootstrap
iterations have xiii_G2 R2 < 0) a real structural property, or an artifact
of the range-based scale-factor normalization?

The single range-based SC[xiii] = 150 under-weights the G2 XIII channel by
~24x relative to a per-group-std normalization (std(G2 xiii) = 6.36). A
single per-group-std fit on the real data lifts xiii_G2 R2 from 0.08 to 0.93,
which could mean the under-determination is a normalization artifact.

## Method

Re-run the analysis-22 parametric bootstrap with ONE change — per-group-std
normalization (each observable scaled by its own group's std) instead of the
single range-based cfg.SC. Synthetic data identical to analysis 22 (same
baseline predictions, same sigmas, same seeds). Decision by the R2<0
fraction:
- <= 6% -> Variant A (per-group-std resolves it; adopt as baseline)
- >= 16% -> Variant B (structural; retain range-SC, document as sensitivity)
- in between -> extend to N=100

## Run

```bash
python -m analyses.34_pergroupstd_bootstrap.run        # bootstrap (was N=50)
python -m analyses.34_pergroupstd_bootstrap.aggregate  # R2<0 fraction + verdict
```

Stopped at 12 iterations: 10/12 (83%) R2<0, far above the Variant-B
threshold, so the decision was unambiguous well before N=50.

## Result — Variant B

Per-group-std gives xiii_G2 R2<0 in **83% of iterations**, HIGHER than the
41% under range-based SC. The better normalization sharpens rather than
resolves the multi-modal XIII landscape. The structural under-determination
of the {ax, cx, bx, kx} manifold is robust to normalization choice. Baseline
remains range-based (analysis 22 ensemble); per-group-std reported as a
sensitivity check in §3.2.

See FINDINGS.md for the full argument and manuscript text.
