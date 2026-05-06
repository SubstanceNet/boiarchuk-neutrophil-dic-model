# Robustness analyses

Empty in Phase 0. Populated in Phase 1+ as analyses are written.

## Planned (Phase 1)

- `01_profile_likelihood/`         — per-parameter profile likelihood
- `02_local_sensitivity/`          — Fisher Information Matrix; eigenvalue analysis (sloppiness)
- `03_global_sensitivity/`         — Sobol indices for output observables
- `04_bootstrap_or_mcmc/`          — uncertainty quantification (parametric bootstrap or emcee)
- `05_mechanism_split_profile/`    — fit cost and parameters as function of W_split (issue I-3)

## Planned (Phase 2)

- `10_model_variants/`             — alternative structural forms; AIC/BIC comparison
- `11_g2_fib_channel/`             — investigation of issue I-4

## Planned (Phase 3)

- `20_loo_timepoint/`              — leave-one-timepoint-out cross-validation
- `21_perturbation/`               — robustness to perturbed N(t)
- `22_predictive_check/`           — posterior / bootstrap predictive intervals

## Planned (Phase 4.5: virtual experiments)

- `30_myelosan_dose/`              — variation in myelosan effect strength
- `31_intervention_timing/`        — late vs early myelosan
- `32_combination/`                — hypothetical combined interventions

Each subfolder contains: a runnable script, a README with the analysis question and method, and saved outputs (CSV / pickle / figures).
