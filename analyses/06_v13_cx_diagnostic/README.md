# Analysis 06 — v13 cx-bound diagnostic

## Question

Under v13 cost, how does the XIII-channel parameter cx respond to its upper
bound? Is there a unique optimum that the v12 prior (cx ≤ 600) was
constraining, or does the unconstrained problem still exhibit the multi-modal
"sacrifice XIII / preserve XIII" basin structure observed under v12 in
analysis 02?

This is a diagnostic, NOT a bound-selection exercise. We are not choosing
a new bound for v13. We are mapping the landscape to inform Phase 2 step 2
design.

This addresses an open methodological question after analysis 05 v13
baseline: cx fitted at 570.9 (seed 42) and 600.0 (seeds 7, 123) shows
mixed behaviour at the bound — was this seed luck, or genuine identifiability
issue under v13 cost?

## Method

Five quick-mode v13 fits at seed=42, varying cx upper bound:
- 500 (tighter than v12 prior)
- 600 (v12 prior)
- 700, 1000, 2000 (progressively expanded)

Lower bound stays at 10 throughout.

## Possible outcomes

| Pattern | Interpretation | Phase 2 step 2 implication |
|---------|----------------|-----------------------------|
| cx fitted converges to similar value (e.g. 550-650) at all bounds ≥ 700 | Data-determined optimum, v12 bound was unnecessary tightening | Phase 2 can proceed without cx prior; group-specific cx may not be the right intervention |
| cx fitted = upper bound always | Optimum lies at infinity in unconstrained problem; bound is necessary regularisation | Group-specific cx in Phase 2 step 2 is the right intervention |
| Multi-modal: bimodal split between "around 600" and "near upper bound" depending on bound | Same multi-modal landscape as v12 analysis 02 | Group-specific cx required, plus understanding of basin selection mechanism |
| xiii_G2 R² drops sharply at some specific cx bound | Threshold effect — abrupt transition between basins | Bound serves as basin selector; structural fix needed for stability |

## Run

```bash
python -m analyses.06_v13_cx_diagnostic.sweep
```

Wall-clock: ~60 min on 16-thread workstation (5 fits × ~12 min).

## Outputs

- `results/sweep.json` — all metrics, parameters per cx bound
- `results/_cache/*.pkl` — individual fit caches (hash-keyed, v13)
- `figures/cx_landscape.png` — visualisation of basin structure
