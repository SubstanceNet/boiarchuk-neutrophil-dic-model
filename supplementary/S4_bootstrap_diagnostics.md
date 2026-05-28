# S4. Bootstrap diagnostic plots

*Part of the Supplementary Information for the manuscript "A mechanistic model of neutrophil-driven disseminated intravascular coagulation…" Main-text references to the bootstrap ensemble: Methods §2.4 (pipeline), Results §3.2 (XIII under-determination, Figure 2), Table 1 (well-identified parameter CIs), Table S2 (full ensemble). This section is the methodological appendix to the bootstrap: cost distribution, convergence diagnostic, mechanistic interpretation of the XIII basin classification, and normalization sensitivity.*

---

## S4.1 Bootstrap setup

The parametric bootstrap pipeline is fully specified in §S2.3. The specifics for this run:

- **Synthetic-data generator.** Each of the 100 iterations samples a synthetic dataset y_synth = y_baseline + ε, where y_baseline is the baseline-fit prediction at the real observation timepoints and ε is Gaussian noise with zero mean. The standard deviation σ is set per-observable per-group equal to the baseline RMSE on the real data (range-based normalisation; see §S4.5 for the sensitivity check under per-group standard deviations).
- **Iterations.** N = 100, seeds i = 1–1 to 100 (deterministic for reproducibility).
- **Computational profile.** Total wall-clock 23.4 hours on a single workstation using `workers=-1` (all CPU cores) in scipy.differential_evolution.
- **Failures.** Zero failed iterations: every refit converged to a finite cost and a non-NaN trajectory.

---

## S4.2 Cost distribution and convergence

Aggregated cost statistics across the 100 bootstrap iterations:

| Metric | Value |
|---|---|
| Mean cost | 0.8750 |
| Standard deviation | 0.0737 |
| 95% CI | [0.7554, 1.0204] |
| Minimum | 0.6906 |
| Maximum | 1.0888 |
| Baseline cost (real data) | 0.9590 |

The bootstrap mean (0.875) sits slightly below the baseline cost on real data (0.959). This is expected for parametric bootstrap: synthetic data are generated from the baseline predictions themselves, so the optimiser starts each iteration at near-zero residual on at least one trajectory and converges to costs systematically lower than the real-data fit. The standard deviation of 0.0737 (CV ≈ 8%) and the absence of failed iterations together indicate a stable pipeline; the multi-modal landscape described in §S4.3 manifests in *parameter-space* spread, not in cost-space outliers.

**Convergence check.** We compared 95% CI widths at N = 50 (first half of the ensemble) and N = 100 (full ensemble) to test whether the ensemble has converged for the well-identified parameters:

| Parameter | Δ width (N = 50 → N = 100) | Note |
|---|---|---|
| tp2 | +2.9% | converged |
| kd | −6.2% | converged |
| at | +5.1% | converged |
| tm | +8.8% | converged |
| s2 | +8.9% | converged |
| km | +26.4% | slightly under-converged |

Five of the six well-identified parameters show CI width changes below 10% between half-ensemble and full-ensemble, consistent with convergence. The exception is **km**, whose CI width changed by 26.4% across the doubling; the published interval [3.46, 5.73] may be slightly narrower than the true bootstrap CI, which is closer to [3.2, 6.0]. The difference does not affect any biological conclusion, but is reported here transparently. For sloppy parameters (§S3.2), the half-to-full-ensemble change is larger — e.g. df −47.7%, kx +27.2%, kr −23.8%, cr +19.7% — reflecting the wider intrinsic resample distribution of those parameters; this is expected and does not threaten the well-identified estimates. The aggregate mean of |Δ width| across all 26 parameters is 12.2%.

---

## S4.3 Factor XIII basin classification

The defining diagnostic from the bootstrap is the bimodal distribution of Group II XIII R² across the 100 iterations. The full breakdown:

| R²_G2 (XIII) range | Iterations | Fraction |
|---|---|---|
| < 0 | 41 | 41% |
| [0, 0.3) | 32 | 32% |
| [0.3, 0.6) | 19 | 19% |
| ≥ 0.6 | 8 | 8% |

The full ensemble median is R²_G2(XIII) = 0.075 with 95% CI [−1.019, 0.649], reflecting the bimodal shape rather than a unimodal central tendency (Figure 2, main-text panel b). For downstream analyses that depend on accurate XIII predictions, we define a **good-basin subset** by the criterion R²_G2(XIII) ≥ 0.3; this gives **n = 27 members** (the 19 + 8 from the table above). The same n = 27 criterion is used for the conservative confidence bands in the virtual experiments (main-text §3.5–3.8) and in Figures 4–6.

**Mechanism: the bx/kx ratio.** The bimodality is not arbitrary stochastic settling — it traces to a single parameter ratio that distinguishes the two basins. Comparing the 41 bad-basin iterations (R² < 0) with the 19 good-basin iterations (R² ≥ 0.3):

| Parameter | Bad-basin median | Good-basin median | Ratio (bad / good) |
|---|---|---|---|
| bx (XIII degradation rate) | 35.74 | 27.91 | 1.28 |
| ax (XIII production / inducer) | 47.78 | 42.21 | 1.13 |
| cx (XIII production / AP·Nr) | 575.1 | 507.3 | 1.13 |
| kx (XIII liver-modulated resynthesis) | 2.43 | 3.03 | 0.80 |

The mechanism is direct: high bx combined with low kx gives XIII degradation exceeding hepatic resynthesis, so the integrated XIII trajectory diverges from observation. Low bx with adequate kx gives degradation that resynthesis can compensate. The separation is continuous rather than discrete — the Pearson correlation between bootstrap-iteration bx/kx and R²_G2(XIII) is −0.33, moderate but not high — consistent with drift along the XIII sloppy direction identified in §S3.2 (ax, cx, bx, kx all classified as sloppy or grid-truncated). The XIII bimodality is therefore best described as the projection of a continuous sloppy manifold onto the binary fit-quality criterion, not as switching between two structurally distinct regimes.

By contrast, **the well-identified parameters are essentially identical between bad-basin and good-basin iterations** (ratios in [0.95, 1.03] for kd, tp2, km, tm). The mechanism split, the busulfan modifiers, and the inducer-pulse timing are robust to the XIII basin choice; the main biological conclusions of the manuscript are independent of which XIII basin a given iteration occupies.

---

## S4.4 Per-observable R² across the ensemble

Median R² with 95% CI across 100 iterations:

| Observable | Group I median [95% CI] | Group II median [95% CI] |
|---|---|---|
| recalc | 0.768 [0.703, 0.813] | 0.881 [0.768, 0.940] |
| thrombin | 0.850 [0.801, 0.883] | 0.935 [0.861, 0.966] |
| fib | 0.710 [0.644, 0.776] | 0.407 [0.038, 0.518] |
| xiii | 0.859 [0.779, 0.899] | 0.075 [−1.019, 0.649] |
| AP | 0.809 [0.724, 0.862] | 0.952 [0.754, 0.974] |
| D | 0.882 [0.807, 0.930] | 0.737 [0.590, 0.827] |

Group I fit quality is robust across the ensemble — every observable shows median R² > 0.70. Group II shows the expected XIII degradation; fibrinogen sits at median R² = 0.407 with a lower CI bound near zero, consistent with the fibrinogen-channel cancellation diagnostic discussed in main-text §4.6. Only 5 of 100 iterations achieve R²_G2 ≥ 0.4 across *all six* observables simultaneously, underscoring that the joint G2 fit is constrained by the XIII channel rather than by the data fit at large.

---

## S4.5 Normalization sensitivity (per-group standard deviations)

A colleague review raised the question of whether the XIII under-determination might be an artefact of the range-based per-observable scale factors. The range-based factor for XIII (SC[xiii] = 150) is set from the union of Group I and Group II value ranges. Per-group standard deviations differ sharply: σ(G1 xiii) = 48.6 vs σ(G2 xiii) = 6.36, so a per-group-std normalisation would up-weight the Group II XIII residual roughly 24-fold relative to the range-based default. A single-seed refit on real data under per-group-std lifted R²_G2(XIII) from 0.08 to 0.93 — superficially suggesting that the under-determination is a normalisation artefact.

**Bootstrap test (analysis 34).** We re-ran the parametric bootstrap (identical to S4.1 in every other respect) with the per-group-std normalisation. The R²_G2(XIII) < 0 fraction rose to **10 of 12 iterations (83%)**, *higher* than the 41% observed under range-based normalisation, not lower. The run was stopped at 12 of a planned 50 iterations because the 83% rate was already overwhelming relative to the 16% decision threshold and further iterations would not change the conclusion.

**Interpretation.** Up-weighting the Group II XIII residual by ~24× makes the cost surface in the XIII channel steeper, so the optimiser falls into the poor-bx/kx basin (§S4.3) *more often* under bootstrap noise, even though the good basin gives a better fit when reached on the real data. The range-based normalisation is too soft for G2 XIII (under-weighting by 24×); the per-group-std normalisation is too sharp (83% R² < 0). Both endpoints confirm the same structural property: the XIII under-determination is a property of the {ax, cx, bx, kx} parameter manifold, robust to the normalisation choice rather than an artefact of it.

We retain the range-based normalisation as the production setting (the N = 100 ensemble in §S4.1–S4.4 and Table S2) and report the per-group-std bootstrap as a sensitivity check. The full structural justification for the cx upper bound, the most identifiable single constraint on this manifold, is in §S9.
