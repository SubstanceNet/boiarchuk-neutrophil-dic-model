# Analysis 07 — Group-specific cx Findings (negative result)

**Status:** closed. Group-specific cx does NOT resolve I-9 / I-10. Hypothesis rejected.

## Summary

Three v13_gs quick-mode fits at seeds {42, 7, 123} with `cx_g1` and `cx_g2` as separate parameters (both bounded 10-600). Plus one extended test at seed=42 with bounds widened to (10, 2000) for both cx parameters.

**Result.** Across all four fits, the optimiser converges to `cx_g1 ≈ cx_g2`:
- cx_ratio ∈ {0.999, 0.998, 1.000} (3 seeds, bounds 600)
- cx_ratio = 0.987 (1 seed, bounds 2000)

The data do not require group-specific cx. The extra parameter contributes degree of freedom but is not used by optimisation.

## Evidence (4 fits)

### Default bounds (10, 600)

| seed | cost | R²_G1 | R²_G2 | cx_g1 | cx_g2 | ratio | xiii_G2 |
|------|------|-------|-------|-------|-------|-------|---------|
|  42 | 1.0449 | +0.8276 | +0.6556 | 600.0 | 599.6 | 0.999 | +0.7549 |
|   7 | 1.0462 | +0.8260 | +0.6609 | 600.0 | 599.0 | 0.998 | +0.7604 |
| 123 | 1.0452 | +0.8264 | +0.6596 | 600.0 | 599.9 | 1.000 | +0.7217 |

### Extended bounds (10, 2000), seed=42

| cost | R²_G1 | R²_G2 | cx_g1 | cx_g2 | ratio | xiii_G2 |
|------|-------|-------|-------|-------|-------|---------|
| 1.0378 | +0.8317 | +0.6485 | 1003.2 | 990.5 | 0.987 | +0.7695 |

cx_g1 and cx_g2 settled at 1003 and 990 (far from bound). The optimiser found the same Zone B solution (cx ≈ 1000) regardless of the extra degree of freedom.

## Comparison to v13 baseline (analysis 05, cx shared)

| metric | v13 baseline (best seed) | v13_gs (default bounds, seed=42) | v13_gs (extended bounds, seed=42) |
|--------|--------------------------|-----------------------------------|------------------------------------|
| cost | 0.959 | 1.0449 | 1.0378 |
| R²_G1 avg | 0.834 | 0.8276 | 0.8317 |
| R²_G2 avg | 0.692 | 0.6556 | 0.6485 |
| xiii_G2 R² | 0.077 | 0.7549 | 0.7695 |

R²_G2 average is **lower** under v13_gs than v13 baseline. Group-specific cx does not improve aggregate G2 fit.

## Spread analysis under default bounds (3 seeds)

| metric | v13 baseline (analysis 05) | v13_gs (analysis 07) |
|--------|----------------------------|----------------------|
| Δcost | 0.0077 | 0.0013 |
| ΔR²_G2 | 0.0597 | 0.0053 |
| Δxiii_G2 | 0.354 | 0.0387 |
| Δcx_g1 | (n/a) | 0.0 |
| Δcx_g2 | (n/a) | 0.9 |

**Seed-stability dramatically improved under v13_gs.** All spreads tighten by an order of magnitude.

## Interpretation

The result has two facets:

**1. cx is NOT group-specific in the data.** Both default and extended bounds yield `cx_g1 ≈ cx_g2`. Myelosan does not change the rate constant for neutrophil-mediated XIII production. Biologically: neutrophil suppression reduces neutrophil COUNT (already captured by km, tm modifiers on kr, tp2) but does not alter the per-neutrophil rate of XIII production.

**2. v13_gs has a regularization side effect.** The extra parameter (cx_g2) does not contribute biological information, but its presence stabilises the optimisation: all three seeds converge to the same point, escaping the multi-modal landscape of v13 baseline. This is a stabilisation through redundancy, not architectural fix. It is also why R²_G2 under v13_gs equals Zone A quality from analysis 06: the optimiser settles into the regularised symmetric solution (Zone A region) rather than seed-dependent Zone B variants.

## Implications for Phase 2

- **Reject group-specific cx as architectural intervention.** Hypothesis falsified.
- **I-9 / I-10 remain open.** Multi-modal landscape and Zone A/B trade-off persist under v13 baseline. v13_gs achieves seed-stability artificially (regularisation) but does not improve fit quality.
- **Next candidate: c_f (fibrinogen / AP coefficient).** Analysis 03 showed largest separate-fit improvement for fib (Δ +0.285). Biologically, IL-6-mediated hepatic fib synthesis could plausibly differ between groups under neutrophil suppression (different neutrophil-driven IL-6 production). Group-specific c_f addresses both I-4 (fib G2 structurally weak) and possibly I-9/I-10.
- **Architecturally**, leaving v13 baseline (cx shared) untouched. analysis 08 (c_f group-specific) will use a parallel implementation `src/cost_v13_groupspec_cf.py` analogous to `cost_v13_groupspec.py` from this analysis.

## Run inventory

- `results/summary.json` — main 3-seed sweep
- `results/fit_seed_42.json`, `fit_seed_7.json`, `fit_seed_123.json` — individual full results
- `results/extended_test_seed_42.json` — extended bounds (10, 2000) sanity check
- `results/_cache/*.pkl` — 4 hash-keyed v13_gs fit caches
- `src/cost_v13_groupspec.py` and `run_with_overrides_v13_gs` in `src/fit_runner.py` retained for potential reuse (template for analysis 08+)
