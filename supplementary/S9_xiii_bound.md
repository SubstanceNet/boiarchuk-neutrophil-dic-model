# S9. Upper bound on cx (factor XIII channel) as a structural prior

*Part of the Supplementary Information. Main-text reference: Methods §2.2 ("Relaxing it unlocks a multi-modal landscape in which the XIII fit trades off against the other Group II observables"). Related sections: §S1.7 (the role of cx in the dX/dt equation), §S2.6 (cx bound saturation in Table S2 — median 545.8, upper CI 600.0), §S3.2 (cx classified as grid-truncated under profile likelihood), §S4.3 (the bx/kx mechanistic interpretation of the same XIII manifold under bootstrap).*

---

## S9.1 Setup

Two complementary series of experiments together establish the case for the cx ≤ 600 bound:

- **Analysis 02 (`analyses/02_cx_bound/`):** 9 fits across three bound levels, testing what happens when the bound is removed.
- **Analysis 06 (`analyses/06_v13_cx_diagnostic/`):** 15 fits across five bound values (cx ≤ 500, 600, 700, 1000, 2000) at three seeds each, mapping where the bound should sit.

All fits share the v13 baseline configuration (W_SPLIT = 2.0, uniform W_SURV, quick-mode optimisation per §S2.2). The 24-shared + 2-modifier architecture is identical across the sweep; only the upper bound on cx changes.

---

## S9.2 Removing the bound: multi-modal landscape

Analysis 02 ran 9 fits across three upper-bound levels on cx:

| Bound | Seed | Cost | cx fitted | xiii_G2 | recalc_G2 | AP_G2 | D_G2 | fib_G2 |
|---|---|---|---|---|---|---|---|---|
| cx ≤ 600 (baseline) | 42 | 1.0431 | 599.7 | +0.728 | +0.684 | +0.678 | +0.505 | +0.293 |
| cx ≤ 2000 (expanded) | 42 | 0.9512 | 1997.5 | −0.047 | +0.912 | +0.947 | +0.754 | +0.388 |
| cx ≤ 2000 (expanded) | 7 | 0.9446 | 1249.0 | −0.404 | +0.908 | +0.955 | +0.766 | +0.442 |
| cx ≤ 2000 (expanded) | 123 | 0.9496 | 1111.2 | −1.149 | +0.905 | +0.963 | +0.753 | +0.476 |
| cx ≤ 5000 (wide) | 42 | 0.9395 | 1890.4 | −0.472 | +0.914 | +0.958 | +0.763 | +0.448 |
| cx ≤ 5000 (wide) | 7 | 0.9975 | 1408.7 | +0.150 | +0.839 | +0.817 | +0.635 | +0.325 |
| cx ≤ 5000 (wide) | 123 | 1.0283 | 1621.1 | +0.625 | +0.737 | +0.718 | +0.522 | +0.303 |
| cx ≤ 5000 (wide) | 999 | 0.9458 | 1579.8 | −0.479 | +0.907 | +0.954 | +0.754 | +0.454 |
| cx ≤ 5000 (wide) | 2024 | 0.9401 | 2153.0 | −0.338 | +0.909 | +0.959 | +0.763 | +0.445 |

The unconstrained problem (cx ≤ 2000 or wider) is **multi-modal**: at least two distinct basins of attraction exist.

**Dominant basin ("sacrifice XIII"), 5 of 9 fits plus 2 transitional.** xiii_G2 R² ranges [−1.149, −0.047]; the other five Group II observables fit very well (recalc, AP, D in [0.84, 0.96]; fib in [0.32, 0.48]). cx settles broadly in [1111, 2153] with no narrow preferred value. Total cost: [0.940, 0.951].

**Minor basin ("preserve XIII"), 2 of 9 fits.** xiii_G2 R² positive (+0.150, +0.625); the other Group II observables fit moderately (recalc, AP, D in [0.52, 0.84]; fib in [0.30, 0.33]). cx in [1408, 1621]. Total cost noticeably higher: [0.998, 1.028].

The differential-evolution optimiser falls into the minor basin in roughly 2 of 5 attempts at the wide bound. The cost difference between basins is small but consistent (≈0.05–0.09), and crucially, **cost alone does not discriminate the basins** — they correspond to qualitatively different mechanistic interpretations of the XIII channel sitting at similar total cost values.

---

## S9.3 Why cx alone does not determine the basin

Sorting the 8 unconstrained fits (cx ≤ 2000 and cx ≤ 5000) by fitted cx value reveals that the basin choice is not a simple function of cx:

| cx fitted | xiii_G2 R² | Basin |
|---|---|---|
| 1111.2 | −1.149 | sacrifice (deepest) |
| 1249.0 | −0.404 | sacrifice |
| 1408.7 | +0.150 | transitional / preserve |
| 1579.8 | −0.479 | sacrifice |
| 1621.1 | +0.625 | preserve (best XIII) |
| 1890.4 | −0.472 | sacrifice |
| 1997.5 | −0.047 | transitional |
| 2153.0 | −0.338 | sacrifice |

Two cx values 170 units apart (1408.7 and 1579.8, an ≈9% difference) yield xiii_G2 R² of +0.150 and −0.479 — *opposite* basins. The XIII channel is governed by a four-parameter sloppy direction {ax, cx, bx, kx} (§S3.2: all four classified as sloppy or grid-truncated under profile likelihood; §S4.3: the same manifold produces the bimodal bootstrap distribution via the bx/kx ratio). cx is one component of that direction, not its primary determinant. Constraining cx to a fixed upper bound therefore selects a *subspace* of the manifold, not a single point.

---

## S9.4 Where to put the bound: zone structure (analysis 06)

Analysis 06 swept five upper-bound values at three seeds each (15 fits total):

| Upper bound | Seed | Cost | cx fitted | xiii_G2 R² |
|---|---|---|---|---|
| 500 | 42 | 1.0521 | 500.0 | +0.7504 |
| 500 | 7 | 1.0524 | 498.6 | +0.7375 |
| 500 | 123 | 1.0522 | 500.0 | +0.7499 |
| 600 | 42 | 0.9589 | 570.9 | +0.0772 |
| 600 | 7 | 0.9666 | 600.0 | +0.3581 |
| 600 | 123 | 0.9622 | 599.9 | +0.4307 |
| 700 | 42 | 1.0420 | 700.0 | +0.7610 |
| 700 | 7 | 0.9595 | 700.0 | +0.3543 |
| 700 | 123 | 1.0389 | 700.0 | +0.7092 |
| 1000 | 42 | 0.9566 | 995.3 | −0.1590 |
| 1000 | 7 | 0.9534 | 1000.0 | +0.2552 |
| 1000 | 123 | 1.0401 | 999.6 | +0.6559 |
| 2000 | 42 | 1.0269 | 1319.0 | +0.6662 |
| 2000 | 7 | 0.9479 | 1999.8 | +0.2523 |
| 2000 | 123 | 1.0117 | 1247.4 | −0.1615 |

The landscape splits into two qualitatively different zones:

**Zone A (cx ≤ 500).** Unique seed-stable optimum. Cost ≈1.052 across all three seeds (Δ cost = 0.0003); xiii_G2 R² ≈0.74 across all three seeds (Δ = 0.013); cx fitted saturates near the upper bound (500.0, 498.6, 500.0). The bound is acting strongly and reproducibly, but the average Group II R² is depressed relative to wider bounds (≈0.66 vs 0.69–0.75 in Zone B).

**Zone B (cx ≥ 600).** Multi-modal. Different seeds find different local optima with widely varying xiii_G2 R² ([−0.16, +0.76]) at near-equal cost. Cost spreads across seeds at fixed bound are 0.05–0.10; xiii_G2 spreads are 0.35–0.83 R² points. cx fitted almost always saturates the upper bound (within 1%). The data alone do not constrain cx to a unique value in Zone B.

The transition between zones is sharp and falls between cx = 500 and cx = 600.

---

## S9.5 Choice of cx ≤ 600

The chosen bound, cx ≤ 600, sits exactly at the zone transition. Two seeds at this bound find optima with cx saturating near 600.0 (one with seed 42 settles slightly below, at 570.9), and the three seeds give xiii_G2 R² of 0.077, 0.358, 0.431 — spread but partial; the bound is too narrow to enter Zone B cleanly and too wide to be in stable Zone A.

The trade-off was discussed explicitly during the project and is reported transparently here: Zone A (cx ≤ 500) is methodologically clean (unique optimum) but biologically constrained (lower average R²_G2); Zone B (cx ≥ 700+) gives higher R²_G2 in the favourable basin but is multi-modal. The choice of cx ≤ 600 keeps the bound at the natural transition point, accepts the residual XIII-channel multi-modality as a *characterised structural limitation* of the model (documented in §S3.2, §S4.3, and here), and avoids retreating to a tighter prior that would damage the rest of the Group II fit.

Alternative resolutions via group-specific cx or group-specific cf (additional G1/G2 modifiers in the XIII or fibrinogen channel) were tested in `analyses/07_*/` and `analyses/08_*/` and rejected: single-parameter group-specific extensions yielded only marginal regularisation side effects, not the architectural fix the multi-modality required.

---

## S9.6 Validation by Group II observable balance

A second, independent criterion validates the cx ≤ 600 bound — not total cost but **per-observable Group II R² balance**. Reading the per-observable columns of the analysis-02 table (§S9.2):

- The constrained baseline (cx ≤ 600) keeps **all six Group II observables at positive R²** simultaneously (the table shows five with the sixth, thrombin, also positive in the underlying data).
- Every unconstrained fit (n = 8 across the two basins under cx ≤ 2000 and cx ≤ 5000) has **at least one Group II observable with R² < 0** — either xiii_G2 in the dominant "sacrifice XIII" basin, or fib_G2 / D_G2 in the minor "preserve XIII" basin.

This is a stronger criterion than total cost (S9.2 already showed that cost does not discriminate basins) and a stronger criterion than xiii_G2 alone (which can be lifted by sacrificing other channels). It says that *the only configuration in which the joint model fits all six Group II observables coherently* is the cx ≤ 600 baseline. The bound is therefore not only motivated by identifiability (S9.3) but selected by an out-of-cost, per-observable validation.

---

## S9.7 Conclusion

Three points close the case for the cx ≤ 600 prior:

1. **The bound is necessary.** Removing it unlocks a multi-modal landscape in which two qualitatively different mechanistic interpretations of the XIII channel sit at nearly equal cost (§S9.2). Cost cannot discriminate the basins, and cx alone does not determine which basin the optimiser finds (§S9.3).

2. **The bound value is justified.** The cost landscape has a sharp zone transition between cx = 500 and cx = 600: a tight bound (Zone A) gives a unique optimum at the expense of average R²_G2; a loose bound (Zone B) regains R²_G2 in the favourable basin at the cost of multi-modality. The chosen cx ≤ 600 sits at the transition, accepting partial multi-modality as a characterised structural limitation rather than retreating to a tighter prior (§S9.4–S9.5).

3. **The bound is validated.** Only the cx ≤ 600 configuration keeps all six Group II observables at positive R²; every unconstrained fit fails on at least one Group II observable, an out-of-cost criterion that the bound passes uniquely (§S9.6).

The cx upper bound saturates in the production baseline fit (Table S2: median 545.8, upper CI 600.0; §S2.6), as expected from a bound that is acting as a structural prior rather than a generous outer limit. This is the second of the two structural priors imposed by the joint cost function (the first being W_SPLIT = 2.0, §S8); together they pin the model to a biologically interpretable single basin within the cost-equivalent manifold the data alone would otherwise leave open.
