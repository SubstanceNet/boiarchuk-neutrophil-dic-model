# Analysis 08 — Group-specific cf Findings (negative result)

**Status:** closed. Group-specific cf does NOT resolve I-4. Hypothesis rejected.

## Summary

Three v13_gs[cf] quick-mode fits at seeds {42, 7, 123} with `cf_g1` and `cf_g2` as separate parameters (both bounded 5-350).

**Result.** Group-specific cf does not improve fib_G2 R² and the cf_g2/cf_g1 ratio is inconsistent across seeds (0.86, 0.86, 1.04 — split direction). The marginal +0.01 improvement in R²_G2 average comes from xiii_G2 (a side effect through regularisation), not from fib improvement.

## Evidence (3 fits)

| seed | cost | R²_G1 | R²_G2 | cf_g1 | cf_g2 | ratio | fib_G2 | xiii_G2 |
|------|------|-------|-------|-------|-------|-------|--------|---------|
|  42 | 0.9617 | +0.8284 | +0.7507 | 103.9 | 93.0 | 0.895 | +0.4845 | +0.4336 |
|   7 | 0.9594 | +0.8302 | +0.7344 | 97.2 | 83.7 | 0.861 | +0.4845 | +0.3359 |
| 123 | 0.9699 | +0.8307 | +0.7102 | 102.0 | 106.4 | 1.043 | +0.4317 | +0.2949 |

## Comparison to v13 baseline (analysis 05, cf shared)

| metric | v13 baseline (3-seed avg) | v13_gs[cf] (3-seed avg) | Δ |
|--------|---------------------------|--------------------------|---|
| R²_G2 avg | 0.7193 | 0.7318 | +0.0125 |
| fib_G2 R² | 0.4771 | 0.4669 | -0.0102 |

R²_G2 average marginally improved (+0.01); fib_G2 R² actually **decreased**. The R²_G2 gain comes primarily from xiii_G2, which is unrelated to the cf parameter being made group-specific.

## Spread analysis (3 seeds)

| metric | value |
|--------|-------|
| Δcost | 0.0104 |
| ΔR²_G2 avg | 0.0405 |
| Δfib_G2 | 0.0528 |
| Δxiii_G2 | 0.1387 |
| Δcf_g1 | 6.7 |
| Δcf_g2 | 22.8 |
| Δratio | 0.183 |

Seed-stability moderate (Δcost 0.010 vs 0.008 baseline; Δxiii_G2 0.14 vs 0.35 baseline — improved but not as dramatic as analysis 07).

## Interpretation

Three substantive findings:

**1. Direction of cf_g1/cf_g2 ratio is inconsistent.** Two seeds show cf_g2 < cf_g1 (consistent with hypothesis "myelosan reduces neutrophil-driven fib production"); one seed shows the opposite. If the data carried real group-specific information about cf, all three seeds should agree on direction. They don't. This rules out a clear biological signal in cf.

**2. Hypothesis specifically about fib falsified.** The premise was that `cf` group-specific would resolve I-4 (fib G2 weak). It does not — fib_G2 R² is essentially unchanged (Δ ≈ -0.01). I-4 remains structural and unaddressed by single-parameter group-specific extension.

**3. Marginal R²_G2 gain is regularisation side effect.** The +0.01 R²_G2 avg improvement comes from xiii_G2 increase (+0.07 across seeds), not from fib. Adding cf_g2 as extra degree of freedom slightly stabilises the optimisation and lets the XIII channel parameters {ax, bx, kx} reach a better basin. This mirrors the regularisation effect observed in analysis 07 but is weaker.

## Implications for Phase 2

- **Reject group-specific cf as architectural intervention.** Hypothesis falsified.
- **I-4 (fib G2 weak) remains open.** Single-parameter group-specific extension does not address it.
- **I-9 / I-10 remain open.** Marginal improvement insufficient to claim resolution.
- **Phase 2 step 2 outcome: 2 of 2 candidates (cx, cf) rejected.** Pattern emerging: single-parameter group-specific extensions yield regularisation side effects but not architectural fixes.
- **Decision: skip remaining candidates (kna, kd, etc.) and proceed to Phase 2 step 3 (profile likelihood).** Rationale: profile likelihood will give a formal map of identifiability for all 26 parameters, providing diagnostic basis rather than continued single-parameter guessing.

## Run inventory

- `results/summary.json` — 3-seed sweep
- `results/fit_seed_42.json`, `fit_seed_7.json`, `fit_seed_123.json` — individual full results
- `results/_cache/*.pkl` — 3 hash-keyed v13_gs[cf] fit caches
