# Analysis 09 — Profile likelihood

## Question

Which v13 parameters are well-identified by the data, and which are sloppy
or unidentifiable? This addresses the open issues I-6 (τ_v, k_cd fixed
without justification), I-9 (XIII channel multi-modality), and provides
diagnostic basis for any future architectural changes.

## Method

For each parameter θ_i (i = 1..26):
1. Build grid of 11 values around v13 baseline best-fit (seed 42),
   ±50% span, logarithmic for rate constants, linear for modifiers.
2. For each grid point, fix θ_i and minimise cost over the remaining
   25 parameters via Nelder-Mead in 25-dim space.
3. Build profile C(θ_i) = min_{θ_{-i}} cost(θ_i, θ_{-i}).
4. Identify 95% CI where C - C_min < 1.92.
5. Classify: well-identified | weakly-identified | sloppy | unidentifiable.

Single-start (no multi-start) for cost reasons. Dry run on 3 parameters
{km, tm, cx} first to verify method and estimate full-sweep time.

## Run

```bash
# Dry run (3 params, ~5-15 min)
python -m analyses.09_profile_likelihood.dry_run

# Full sweep (26 params, ~3-4 h, only after dry run passes)
python -m analyses.09_profile_likelihood.full_sweep
```

## Outputs

- `results/profile_dry_<param>.json` — individual profile results (dry run)
- `results/dry_run_summary.json` — dry run summary table
- `results/profile_<param>.json` — individual profile results (full sweep)
- `results/full_summary.json` — aggregated 26-param table
- `figures/profile_<param>.png` — profile plot for each param
- `FINDINGS.md` — interpretation
