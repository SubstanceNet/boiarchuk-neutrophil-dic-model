# S3. Profile-likelihood plots — all 26 parameters

*Part of the Supplementary Information for the manuscript "A mechanistic model of neutrophil-driven disseminated intravascular coagulation…" Main-text references give the classification (Methods §2.4: well-identified, weakly identified, sloppy) and use it to interpret bootstrap intervals (Results §3.2, Table 1, Table S2). This section gives the method, the full per-parameter results, and a multi-start validation of the sloppy classification.*

---

## S3.1 Method

For each of the 26 parameters θ_i, the profile likelihood is

> C(θ_i) = min_{θ_{−i}} · cost(θ_i, θ_{−i}),

computed on a grid of 11 values of θ_i. The grid spans ±50% (linear) or e^{±0.5} ≈ ×1.65 (logarithmic) around the baseline best-fit value, with log spacing used for parameters whose bounds span more than two orders of magnitude. At each grid point the remaining 25 parameters are minimised by Nelder–Mead, single-started from the baseline best_x vector. Total wall-clock for the full sweep: 4.6 hours.

The **relative profile depth** for parameter θ_i is defined as

> depth_rel = (C_edge − C_baseline) / C_baseline,

where C_edge is the smaller of the two grid-edge cost values. A sharp local minimum gives depth_rel ≫ 0; a flat profile gives depth_rel ≈ 0. Classification thresholds used throughout (consistent with main-text §3.2):

- **well- or moderately-identified**: depth_rel > 5%
- **weakly identified**: 2% ≤ depth_rel ≤ 5%
- **sloppy**: depth_rel < 2%

A 95% confidence interval is read from the profile as the connected range of θ_i for which C(θ_i) remains within a χ²-based statistical threshold of C_baseline; this CI is reported per parameter in Table S2 (bootstrap-derived) and is also recoverable from the per-panel figures referenced in S3.5.

---

## S3.2 Classification of all 26 parameters

Twenty-three parameters fall cleanly into the three depth-rel categories above; three additional parameters reach a grid boundary before a well-defined minimum is found, and are reported separately as *grid-truncated*. The total is 6 + 5 + 12 + 3 = 26.

**Well- or moderately-identified (6 parameters, depth_rel > 5%).** These are the parameters that drive the model's predictive content: their values are constrained by the data above the statistical threshold.

**Weakly identified (5 parameters, 2% ≤ depth_rel ≤ 5%).** Constrained by the data but with broad confidence intervals; predictions depending only on these will carry visible uncertainty.

**Sloppy (12 parameters, depth_rel < 2%).** Cost varies less than 2% across the entire ±50% grid. When such a parameter is fixed at any value within this range, the others compensate and the overall fit quality is preserved. Four of these twelve are particularly flat: **kca, df, Hm, kna** all show depth_rel < 0.5%, meaning cost varies by less than 0.5% across the entire ±50% grid — the parameter is essentially unconstrained by the available data.

**Grid-truncated (3 parameters).** For cx, krl, and kcl the baseline value sits near the upper parameter bound, so the profile cannot be evaluated symmetrically and the depth_rel statistic is inconclusive. Main text subsumes these under the sloppy / weakly-identified categories for brevity; the distinction matters specifically for **cx**, whose upper bound (≤ 600) is an active structural constraint motivated by identifiability collapse on the {ax, cx, bx, kx} manifold rather than by data fit (see §S1.7 for the model role and §S9 for the full justification of the bound).

The full per-parameter table follows. depth_rel values are from `analyses/09_profile_likelihood/results/`.

| Parameter | depth_rel | Category |
|---|---|---|
| tp2 | 0.473 † | well-identified |
| km | 0.154 | well-identified |
| tm | 0.141 | well-identified |
| kd | 0.073 | well-identified |
| s2 | 0.072 | well-identified |
| at | 0.071 | well-identified |
| a2 | 0.038 | weakly identified |
| ar | 0.032 | weakly identified |
| cf | 0.024 | weakly identified |
| kr | 0.021 | weakly identified |
| ax | 0.020 | weakly identified |
| bt | 0.019 | sloppy |
| cr | 0.018 | sloppy |
| af | 0.017 | sloppy |
| br | 0.016 | sloppy |
| kx | 0.015 | sloppy |
| bx | 0.013 | sloppy |
| knd | 0.013 | sloppy |
| bf | 0.013 | sloppy |
| kna | 0.0046 | sloppy (deepest) |
| Hm | 0.0020 | sloppy (deepest) |
| df | 0.0019 | sloppy (deepest) |
| kca | 0.0018 | sloppy (deepest) |
| cx | — | grid-truncated |
| krl | — | grid-truncated |
| kcl | — | grid-truncated |

† tp2 (depth_rel 0.473) has a high-end grid truncation as its baseline (9.22 d) sits near the upper parameter bound (10 d); the classification as well-identified is unaffected because the depth is large, but the bootstrap CI in Table S2 ([8.89, 10.03] d) is the more reliable uncertainty estimate for this parameter.

Sorting in this table is by depth_rel (profile-likelihood spectrum) and complements the sorting in Table S2 by relative bootstrap CI width (resample spectrum). The two orderings are similar but not identical — the most informative divergence is **kd** (well-identified by depth, wide bootstrap CI; see §S2.6 for interpretation).

---

## S3.3 Sloppiness as a structural property

A well-identified ratio of 6/26 ≈ 23% places this model squarely in the typical range for mechanistic systems-biology models. Gutenkunst et al. (2007, PLoS Comput Biol) demonstrated, across seventeen published biological models, that *universal sloppiness* — the coexistence of a few stiff parameter directions with many soft ones — is a structural property of ODE models whose parameter count exceeds the effective dimensionality of the available data, rather than a fault of any individual fit.

The implication is two-sided. **Predictions that depend on the well-identified parameters** — the inducer-pulse timing tp2, the busulfan modifiers km and tm, the degranulation rate constant kd, the pulse width s2, and the thrombin–inducer coefficient at — are robust to the data limitations and propagate narrow uncertainty bands. **Predictions that isolate effects of sloppy parameters** (e.g. a counterfactual changing only kca with all else fixed) are not constrained by the data and would carry wide uncertainty bands; we accordingly do not present such isolated counterfactuals as findings.

---

## S3.4 Multi-start validation: the kca diagnostic

The classifications above rest on single-start Nelder–Mead minimisation at each grid point. To verify that the *sloppy* classifications are genuine — not artefacts of the inner optimiser settling in a local minimum and missing a deeper basin elsewhere — we re-ran the profile for kca (Table: depth_rel 0.0018, the second-flattest parameter) with five starting points at each grid value: the baseline best_x vector plus four random uniform within the parameter bounds.

The result was unambiguous. At every one of the 11 grid points the lowest cost across the five starts coincided exactly with the single-start result anchored at baseline (Δ across the grid: 0.000000 in every grid point; maximum improvement of multi-start over single-start: 0.000000). The four random starts each converged to higher-cost basins (final cost 1.3–3.5 vs the baseline-anchored ≈0.957). The baseline best_x is therefore a true local minimum of the 26-dimensional cost surface; the flat profile of kca is a multi-dimensional plateau (a sloppy direction in parameter space) rather than a failed optimisation. By extension, single-start profile likelihood is reliable for the other sloppy classifications too.

---

## S3.5 Reading the per-parameter figure (26 panels)

The accompanying figure (`analyses/09_profile_likelihood/figures/`) shows one panel per parameter. Each panel plots the relative cost increment (C(θ_i) − C_baseline) / C_baseline on the vertical axis against the parameter value on the horizontal axis. The axis is linear or logarithmic depending on the grid spacing (S3.1). A horizontal reference line marks the 5% depth threshold; a vertical reference line marks the baseline best-fit value; the shaded interval, where present, marks the 95% confidence range read from the profile.

Panels are arranged by classification: well-identified at the top, then weakly identified, then sloppy by descending depth_rel, with the three grid-truncated parameters at the bottom. For the four deepest-sloppy parameters the curve is essentially flat across the entire grid — visually confirming the depth_rel < 0.5% finding from S3.2.

---

## S3.6 Relation to bootstrap intervals

Profile likelihood (this section) measures *local curvature of the cost surface* at the baseline optimum: how the cost responds to one-parameter-at-a-time perturbations, with all other parameters allowed to compensate. The parametric bootstrap (§S4 and Table S2) measures *global spread under data resampling*: how the optimum shifts when synthetic data are drawn from the baseline predictions with noise. The two criteria are complementary, and they usually agree.

Main text §3.2 cites the profile-likelihood depth criterion as the source of the "well-identified" classification. The bootstrap confidence intervals in Table S2 use a different criterion (resample percentile) and produce a different ordering of the parameters by uncertainty; the principal divergence is kd, well-identified by depth (0.073) but wide under bootstrap (CI width 3.17×). The interpretation of this divergence — a sharp local minimum with a long resample right tail — is given in §S2.6.
