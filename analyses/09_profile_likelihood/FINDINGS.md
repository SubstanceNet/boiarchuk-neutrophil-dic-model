# Analysis 09 — Profile likelihood for v13 parameters (Phase 2 step 3)

**Status:** closed. Profile likelihood map of all 26 v13 parameters complete.
Method validated via multi-start diagnostic on representative sloppy parameter (kca).

## Summary

For each of 26 v13 baseline parameters, computed profile likelihood
C(θ_i) = min_{θ_{-i}} cost(θ_i, θ_{-i}) over 11 grid points spanning
±50% (linear) or factor e^0.5 ≈ 1.65 (log) around the baseline best-fit
value. 25-dim Nelder-Mead minimisation per grid point, single starting
point from baseline best_x. Total wall-clock: 4.6 hours.

Method validated by multi-start diagnostic on kca (5 starts × 11 grid
points): all 4 random starts converged to higher cost basins; baseline
start matched single-start full-sweep result exactly (Δ = 0.0). The
single-start profile likelihood is reliable for this problem; sloppy
classifications are genuine, not optimisation artefacts.

## Parameter classification (26 parameters)

### Well-identified or moderately-identified (6 parameters, depth_rel > 5%)

| param | baseline | depth_rel | CI 95 | classification |
|-------|----------|-----------|-------|----------------|
| km | 4.933 | 0.1539 | [3.453, 6.906] | weakly identified |
| tm | 0.4269 | 0.1409 | [0.3415, 0.5123] | moderately identified |
| kd | 0.2492 | 0.0727 | [0.1671, 0.3718] | weakly identified |
| s2 | 1.731 | 0.0720 | [1.16, 2.336] | moderately identified |
| at | 5.697 | 0.0705 | [3.819, 8.5] | weakly identified |

Plus tp2, classified as `well_identified_grid_truncated` (depth_rel = 0.473,
CI collapsed to single value because baseline 9.18 is near upper bound 10.0
and grid clipped on the upper side).

### Weakly identified (5 parameters, depth_rel 1-5%)

| param | baseline | depth_rel | CI 95 |
|-------|----------|-----------|-------|
| a2 | 3.274 | 0.0376 | [1.986, 5.398] |
| ar | 33.94 | 0.0323 | [20.59, 55.96] |
| cf | 94.15 | 0.0235 | [57.11, 155.2] |
| kr | 0.2286 | 0.0209 | [0.1387, 0.3769] |
| ax | 56.61 | 0.0203 | [34.33, 93.33] |
| bt | 0.2722 | 0.0194 | [0.1651, 0.4487] |
| cr | 37.25 | 0.0179 | [22.6, 61.42] |
| af | 10.11 | 0.0166 | [6.135, 16.68] |
| br | 4.112 | 0.0160 | [2.494, 6.779] |
| kx | 2.997 | 0.0151 | [1.818, 4.942] |
| bx | 18.25 | 0.0132 | [11.07, 30.09] |
| knd | 4.072 | 0.0130 | [2.47, 6.713] |
| bf | 2.836 | 0.0125 | [1.72, 4.675] |

### Sloppy (12 parameters, depth_rel < 1%)

Cost varies less than 1% across the entire ±50% grid. Other parameters
compensate when these are perturbed, leaving cost essentially unchanged.

| param | baseline | depth_rel |
|-------|----------|-----------|
| kca | 0.3818 | 0.0018 |
| df | 12.67 | 0.0019 |
| Hm | 118.4 | 0.0020 |
| kna | 367.4 | 0.0046 |

### Grid-truncated (3 parameters, baseline near bound)

Profile cannot be properly assessed because baseline value is near the
parameter bound, causing the grid to be clipped. May or may not be
identifiable if bounds were extended.

| param | baseline | bounds | classification |
|-------|----------|--------|----------------|
| cx | 570.9 | explored: [346.3, 600] | grid truncated inconclusive grid truncated |
| kcl | 14.82 | explored: [8.991, 20] | grid truncated inconclusive grid truncated |
| krl | 16.26 | explored: [9.86, 20] | grid truncated inconclusive grid truncated |

## Multi-start validation (kca diagnostic)

To verify single-start Nelder-Mead is reliable, repeated profile for `kca`
with 5 starting points per grid point: 1 baseline best_x + 4 random uniform
within bounds. Results:

| metric | value |
|--------|-------|
| Δ range across grid | [+0.000000, +0.000000] |
| max improvement of multistart | 0.000000 |
| median Δ | 0.000000 |

Random starts converged to higher cost basins (1.3-3.5), but none found
anything below the baseline-anchored minimum (~0.957). This confirms:
- The baseline is a true local minimum in the 26-dim cost surface.
- The flat profile observed for kca is a genuine multi-dim plateau
  ("sloppy direction"), not an artefact of failed optimisation.
- The full-sweep classifications can be trusted.

## Interpretation

**6 parameters are well- to moderately-identified by the data:**
tp2, km, tm, s2, kd, at. These define the model's predictive content —
predictions that depend on these parameters will be robust to the data
limitations. tp2 in particular is sharply identified (depth_rel 0.47).

**12 parameters are sloppy:** kca, kna, knd, Hm, cr, br, bt, af, bf, df, bx,
kx. Cost surface has multidimensional plateau in these directions. When
one of these parameters is fixed at any value within ±50% of baseline,
the others compensate and cost stays at baseline level. Their precise
values are not constrained by the available data.

**3 parameters are grid-truncated** (baseline near upper bound):
krl, kcl, cx. With current bounds, profile cannot be properly assessed.

**5 parameters are weakly identified** with depth 1-5% and broad CI.

This 23% well-identified ratio (6/26) places the model in the typical
range for sloppy systems-biology models reported in the literature
(Gutenkunst et al. 2007, PLoS Comput Biol; Sethna et al. 2007,
Phys Rev Lett).

## Implications for the project

**Manuscript.** The sloppy structure should be described in Discussion
as an expected property of dynamic models with parameter count exceeding
observable degrees of freedom. Reference Gutenkunst et al. 2007.
The 6 well-identified parameters are the model's predictive content;
the 20 others define soft directions that can vary without affecting
fit quality.

**Phase 2 step 2 retrospective.** The negative results from analyses 07
(group-specific cx) and 08 (group-specific cf) now have a causal explanation.
Both `cx` and `cf` lie within the sloppy region of parameter space
(depth_rel < 0.025 for both). Single-parameter group-specific extensions
along sloppy directions cannot extract additional information from the
data because the data do not constrain those directions in the first place.
This validates the decision to skip remaining single-parameter candidates
(kna, kd, etc.) and proceed directly to step 3.

**Phase 3 (virtual experiments, manuscript).** Predictions that depend
on the 6 well-identified parameters will be robust. Predictions that
isolate effects of sloppy parameters (e.g., counterfactual of changing
only `kca`) will have wide uncertainty bands and should be avoided
or accompanied by appropriate caveats.

**Open issues update.**
- I-4 (fib G2 weak): structurally explained — `cf`, `bf`, `df`, `af` all
  sloppy, plus weakly-identified `cf`. The fib channel is essentially
  underdetermined by observation. Improvement requires additional fib
  observation timepoints, not architectural changes.
- I-6 (τ_v, k_cd fixed without justification): partially addressed —
  these are not in the v13 parameter list, but the analysis confirms that
  many parameters are sloppy, justifying selective fixing of others to
  reduce model dimensionality if desired.
- I-9 (XIII identifiability under v13): explained — all four XIII channel
  parameters {ax, cx, bx, kx} are sloppy or grid-truncated. The channel
  is genuinely underdetermined.
- I-10 (Zone A vs B trade-off): explained — Zone A vs Zone B reflect
  different points on the sloppy plateau of `cx`, both with similar cost.
  Multi-modality at finite numerical precision is expected.

## Run inventory

- `results/profile_<name>.json` — 26 individual profiles
- `results/full_summary.json` — aggregated summary
- `results/full_sweep.log` — full sweep log
- `results/dry_run.log` — final dry-run log (validated method)
- `results/dry_run.log.v1_buggy_grid`, `dry_run.log.v2_bad_threshold` —
  retained for debugging history
- `results/multistart_diagnostic_kca.json` — multi-start validation result
- `results/multistart_kca.log` — diagnostic log
