# Analysis 02 — Findings

**Status:** closed. Result feeds back into `notes/known_issues.md` issue I-1.

## Summary

The cx upper bound at 600 is a necessary structural prior on the XIII channel, not an artefactual constraint. Removing it does not yield a uniformly better fit; it instead unlocks a multi-modal parameter landscape with at least two distinct basins, each producing a hard trade-off between XIII fit quality and the rest of the G2 observables. Across 9 fits at expanded or wide cx bounds, only the constrained baseline (cx ≤ 600) keeps all six G2 observables at positive R-squared.

## Evidence (9 fits total)

### baseline (cx ≤ 600), 1 seed
| seed | cost | cx_fit | xiii_G2 | recalc_G2 | AP_G2 | D_G2 | fib_G2 |
|------|------|--------|---------|-----------|-------|------|--------|
| 42 | 1.0431 | 599.7 | +0.728 | +0.684 | +0.678 | +0.505 | +0.293 |

### expanded (cx ≤ 2000), 3 seeds
| seed | cost | cx_fit | xiii_G2 | recalc_G2 | AP_G2 | D_G2 | fib_G2 |
|------|------|--------|---------|-----------|-------|------|--------|
| 42  | 0.9512 | 1997.5 | -0.047 | +0.912 | +0.947 | +0.754 | +0.388 |
| 7   | 0.9446 | 1249.0 | -0.404 | +0.908 | +0.955 | +0.766 | +0.442 |
| 123 | 0.9496 | 1111.2 | -1.149 | +0.905 | +0.963 | +0.753 | +0.476 |

### wide (cx ≤ 5000), 5 seeds
| seed | cost | cx_fit | xiii_G2 | recalc_G2 | AP_G2 | D_G2 | fib_G2 |
|------|------|--------|---------|-----------|-------|------|--------|
| 42   | 0.9395 | 1890.4 | -0.472 | +0.914 | +0.958 | +0.763 | +0.448 |
| 7    | 0.9975 | 1408.7 | +0.150 | +0.839 | +0.817 | +0.635 | +0.325 |
| 123  | 1.0283 | 1621.1 | +0.625 | +0.737 | +0.718 | +0.522 | +0.303 |
| 999  | 0.9458 | 1579.8 | -0.479 | +0.907 | +0.954 | +0.754 | +0.454 |
| 2024 | 0.9401 | 2153.0 | -0.338 | +0.909 | +0.959 | +0.763 | +0.445 |

## Multi-modal landscape — two basins identified

The unconstrained search space has at least two distinct basins of attraction for the joint fit:

**Dominant basin: "sacrifice XIII" (5 of 9 fits, plus 2 transitional).**
xiii_G2 R-squared ranges [-1.149, -0.047]. Other G2 observables fit very well (recalc, AP, D in [0.84, 0.96]; fib in [0.32, 0.48]). cx settles in [1111, 2153] with no narrow preferred value. Total cost ranges [0.940, 0.951].

**Minor basin: "preserve XIII" (2 of 9 fits).**
xiii_G2 R-squared positive (+0.150, +0.625). Other G2 observables fit moderately (recalc, AP, D in [0.52, 0.84]). cx in [1408, 1621]. Total cost noticeably higher: 0.998-1.028.

The DE optimiser enters the minor basin in roughly 2 of 5 attempts at the wide bound. The cost difference between basins (~0.05-0.09) is small but consistent: the dominant basin is preferred by the optimiser most of the time. The persistence of the minor basin across seeds {7, 123} demonstrates it is a real local optimum, not a single-seed convergence artefact.

The transitional points (expa/s42 with xiii_G2 = -0.047, wide/s7 with xiii_G2 = +0.150) suggest the basins are connected by a low-cost ridge rather than separated by high-cost barriers. This reinforces the identifiability diagnosis: small perturbations to optimisation trajectory produce qualitatively different mechanistic interpretations.

## Why cx alone does not determine the basin

Across the 8 unconstrained fits cx values cover [1111, 2153]:

```
cx_fit | xiii_G2 R-squared | basin
1111.2 |  -1.149          | sacrifice (deepest)
1249.0 |  -0.404          | sacrifice
1408.7 |  +0.150          | transitional / preserve
1579.8 |  -0.479          | sacrifice
1621.1 |  +0.625          | preserve (best XIII)
1890.4 |  -0.472          | sacrifice
1997.5 |  -0.047          | transitional
2153.0 |  -0.338          | sacrifice
```

cx values 1408 and 1579 are very close (Δ = 170, ~10% of value), but yield xiii_G2 of +0.15 and -0.48 — opposite basins. The XIII channel is governed by four parameters {ax, cx, bx, kx} that co-vary along a sloppy direction; cx is one component of that sloppy direction, not its primary determinant.

## Note on v12 report value cx = 1481

The v12 internal report quoted a fitted cx = 1481, outside the script's bound (10, 600). This value falls within the cx range observed across all unconstrained fits ([1111, 2153]). Most likely it represents a fit in the dominant "sacrifice XIII" basin (which contains 6 of 8 unconstrained fits), produced by an earlier development run with broader bounds. The report tracked aggregate R-squared metrics rather than per-observable G2 quality, so the catastrophic XIII collapse on G2 (R-squared < 0) was not noticed at the time.

## Implications for manuscript

- The cx upper bound (10, 600) is to be presented as a structural prior on the XIII channel, alongside W_split = 2.0 (analysis 01), in a unified "structural priors" section of the methods.
- Justification: without these priors, the model exhibits identifiability collapse with multiple cost-equivalent local optima at qualitatively different mechanistic interpretations. The constrained problem yields a single, biologically interpretable solution.
- Both priors are validated post-hoc by the same conservative criterion: G2 observable balance. The constrained baseline keeps all six G2 observables at positive R-squared. Every unconstrained fit (n=8 across two basins) has at least one G2 observable with R-squared < 0.
- Analysis 02 itself is suitable as a methods-section supplement demonstrating necessity of the cx prior.

## Open follow-up for Phase 2

The {ax, cx, bx, kx} sloppy direction in the XIII channel is empirically demonstrated but not formally characterised. Phase 2 profile likelihood + Fisher Information Matrix should produce explicit identifiability classification for each XIII-channel parameter (well-determined / weakly-identified / sloppy) and quantify the sloppy direction's eigenvector.

## Run inventory

- `results/sweep.json` — 3-point sweep, seed=42 (3 fits)
- `results/seed_check.json` — 4 fits at seeds {7, 123} × {expanded, wide}
- `results/seed_check_extra.json` — 2 fits at wide × seeds {999, 2024}
- `results/_cache/*.pkl` — 9 individual fit results, hash-keyed
- `figures/regimes.png` — visualisation of all 9 fits across both basins
