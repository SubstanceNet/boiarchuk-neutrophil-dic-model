# Analysis 21 — Perturbation of N(t) (Phase 3)

## Question

How robust are v13 model predictions to perturbations of the neutrophil
count input N(t)? Two complementary perturbation modes:

1. **Deterministic scaling** (α): systematic bias on N(t) measurements.
2. **Stochastic noise**: random per-timepoint multiplicative noise on N(t).

This addresses reviewer concern: "How sensitive are predictions to
neutrophil count measurement precision?"

## Method

### Sub-analysis 21a — α scan (deterministic)

Multiply N1(t), N2(t) by α ∈ {0.8, 0.9, 1.0, 1.1, 1.2}. Rebuild
interpolators. Refit v13 model. Compare costs and per-observable R²
across α values.

5 fits × ~14 min = ~1.2 hours.

### Sub-analysis 21b — stochastic σ=10%

Apply lognormal noise to N(t) per timepoint, CV=10%:
N_perturbed(t) = N(t) × exp(z), z ~ N(0, ln(1.10)).
N=20 realisations. Refit each. Compute parameter spread, prediction CI.

20 fits × ~14 min = ~4.7 hours.

### Sub-analysis 21c — stochastic σ=20% (sensitivity check)

As 21b but with CV=20%: z ~ N(0, ln(1.20)).
N=20 realisations.

20 fits × ~14 min = ~4.7 hours.

### Total compute

45 fits, ~10.6 hours wall-clock. Two nights overnight.

## Run

```bash
# Sub-analysis 21a (~1 hour)
python -m analyses.21_perturbation.run_alpha_scan

# Sub-analysis 21b (~5 hours, one night)
python -m analyses.21_perturbation.run_stochastic --sigma 10

# Sub-analysis 21c (~5 hours, one night)
python -m analyses.21_perturbation.run_stochastic --sigma 20
```

## Outputs

- `results/alpha_scan/fit_alpha_<α>.json` — 5 deterministic fits
- `results/stochastic_10/iter_<seed>.json` — 20 σ=10% fits
- `results/stochastic_20/iter_<seed>.json` — 20 σ=20% fits
- `results/_cache/*.pkl` — fit caches
- `results/summary.json` — aggregated analysis
- `FINDINGS.md` — interpretation
