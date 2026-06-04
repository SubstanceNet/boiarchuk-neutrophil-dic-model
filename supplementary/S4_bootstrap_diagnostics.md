# S4. Bootstrap Diagnostic Plots

*Part of the Supplementary Information for Boiarchuk & Onasenko (2026). Bootstrap ensemble in the main text: §2.4 (pipeline), §3.2 (factor XIII under-determination, Figure 2), Table 1 (CIs for well-identified parameters), Table S2 (full ensemble). This appendix provides the methodological supplement: cost distribution, convergence diagnostics, mechanistic interpretation of the factor XIII basin classification, and sensitivity to normalisation.*

---

## S4.1 Bootstrap settings

The parametric bootstrap pipeline is fully specified in §S2.3. Particulars of this run:

- **Synthetic data generator.** Each of the 100 iterations samples a synthetic dataset $y_{\text{synth}} = y_{\text{baseline}} + \varepsilon$, where $y_{\text{baseline}}$ is the baseline fitted prediction at the real observation time points and $\varepsilon$ is zero-mean Gaussian noise. The standard deviation $\sigma$ is set for each observable in each group equal to the baseline RMSE on real data (range-based normalisation; sensitivity analysis with per-group standard deviations is described in subsection S4.5 below).

- **Iterations.** $N = 100$, seeds $i = 1$ to $100$ (deterministic for reproducibility).

- **Computational profile.** Total wall-clock time 23.4 hours on a single workstation using `workers=-1` (all CPU cores) in `scipy.differential_evolution`.

- **Failures.** Zero failed iterations: every re-fit converged to a finite cost and NaN-free trajectory.

---

## S4.2 Cost distribution and convergence

Aggregate cost statistics across 100 bootstrap iterations:

| **Metric** | **Value** |
|---|---|
| Mean cost | 0.8750 |
| Standard deviation | 0.0737 |
| 95% CI | [0.7554, 1.0204] |
| Minimum | 0.6906 |
| Maximum | 1.0888 |
| Baseline cost (real data) | 0.9590 |

The bootstrap mean (0.875) sits slightly below the baseline cost on real data (0.959). This is expected for parametric bootstrap: synthetic data are generated from the baseline predictions themselves, so the optimiser starts each iteration near zero residual on at least one trajectory and converges to costs systematically lower than the real-data fit. Standard deviation 0.0737 (CV $\approx$ 8%) and the absence of failed iterations together indicate a stable pipeline; the multimodal landscape described in S4.3 manifests in *parameter-space* scatter, not in cost-space outliers.

**Convergence check.** We compared 95% CI widths at $N = 50$ (first half of the ensemble) versus $N = 100$ (full ensemble) to verify whether the ensemble had converged for the well-identified parameters:

| **Parameter** | **$\Delta$ width ($N = 50 \to N = 100$)** | **Note** |
|---|---|---|
| $t_{p2}$ | +2.9% | converged |
| $k_d$ | −6.2% | converged |
| $a_t$ | +5.1% | converged |
| $t_m$ | +8.8% | converged |
| $s_2$ | +8.9% | converged |
| $k_m$ | +26.4% | slightly under-converged |

Five of the six well-identified parameters show CI width changes below 10% between the half and full ensembles, consistent with convergence. The exception is **$k_m$**, whose CI width changed by 26.4% upon doubling; the reported interval [3.46, 5.73] may be slightly narrower than the true bootstrap CI, which is closer to [3.2, 6.0]. This difference does not affect any biological conclusion, but is reported here for transparency. For sloppy parameters (§S3.2), the change from half to full ensemble is larger — for example, $d_f$ −47.7%, $k_x$ +27.2%, $k_r$ −23.8%, $c_r$ +19.7% — reflecting the wider internal re-sampling distribution of these parameters; this is expected and does not threaten the well-identified estimates. The aggregate mean $|\Delta\text{width}|$ across all 26 parameters is 12.2%.

---

## S4.3 Factor XIII basin classification

The defining diagnostic from the bootstrap is the bimodal distribution of $R^2$ for Group II factor XIII across 100 iterations. Full breakdown:

| **$R^2_{\text{G2}}(\text{XIII})$ range** | **Iterations** | **Fraction** |
|---|---|---|
| $< 0$ | 41 | 41% |
| $[0, 0.3)$ | 32 | 32% |
| $[0.3, 0.6)$ | 19 | 19% |
| $\geq 0.6$ | 8 | 8% |

The full-ensemble median is $R^2_{\text{G2}}(\text{XIII}) = 0.075$ with 95% CI $[-1.019, 0.649]$, reflecting the bimodal shape rather than a unimodal central tendency (Figure 2, panel b, main text). For subsequent analyses depending on accurate factor XIII predictions, we define a **"good-basin" subset** by the criterion $R^2_{\text{G2}}(\text{XIII}) \geq 0.3$; this yields **$n = 27$ members** (19 + 8 from the table above). The same $n = 27$ criterion is used for conservative confidence bands in the virtual experiments (main text §3.5) and in Figures 4–6.

**Mechanism: the $b_x/k_x$ ratio.** The bimodality is not arbitrary stochastic settling — it traces to a single parameter ratio that distinguishes the two basins. Comparison of 41 poor-basin iterations ($R^2 < 0$) with 19 good-basin iterations ($R^2 \geq 0.3$):

| **Parameter** | **Poor-basin median** | **Good-basin median** | **Ratio (poor/good)** |
|---|---|---|---|
| $b_x$ (factor XIII degradation rate) | 35.74 | 27.91 | 1.28 |
| $a_x$ (factor XIII production / inducer) | 47.78 | 42.21 | 1.13 |
| $c_x$ (factor XIII production / $AP \cdot N_r$) | 575.1 | 507.3 | 1.13 |
| $k_x$ (liver-modulated factor XIII resynthesis) | 2.43 | 3.03 | 0.80 |

The mechanism is straightforward: high $b_x$ combined with low $k_x$ gives degradation of factor XIII that exceeds hepatic resynthesis, so the integrated factor XIII trajectory diverges from the observation. Low $b_x$ with sufficient $k_x$ gives degradation that resynthesis can compensate. The separation is rather continuous than discrete — the Pearson correlation between a bootstrap iteration's $b_x/k_x$ ratio and its $R^2_{\text{G2}}(\text{XIII})$ is −0.33, moderate but not high — consistent with drift along the sloppy factor XIII direction identified in §S3.2 ($a_x$, $c_x$, $b_x$, $k_x$ are all classified as sloppy or grid-truncated). The factor XIII bimodality is therefore best described as the projection of a continuous sloppy manifold onto a binary fit-quality criterion, not as a switch between two structurally distinct regimes.

In contrast, **well-identified parameters are virtually identical between poor- and good-basin iterations** (ratio in [0.95, 1.03] for $k_d$, $t_{p2}$, $k_m$, $t_m$). The mechanism decomposition, busulfan modifiers, and inducer impulse timing are robust to which basin the factor XIII channel occupies; the main biological conclusions of the manuscript do not depend on which basin a given iteration occupies.

---

## S4.4 Per-observable $R^2$ across the ensemble

Median $R^2$ with 95% CI across 100 iterations:

| **Observable** | **Group I median [95% CI]** | **Group II median [95% CI]** |
|---|---|---|
| recalc | 0.768 [0.703, 0.813] | 0.881 [0.768, 0.940] |
| thrombin | 0.850 [0.801, 0.883] | 0.935 [0.861, 0.966] |
| fib | 0.710 [0.644, 0.776] | 0.407 [0.038, 0.518] |
| xiii | 0.859 [0.779, 0.899] | 0.075 [−1.019, 0.649] |
| AP | 0.809 [0.724, 0.862] | 0.952 [0.754, 0.974] |
| D | 0.882 [0.807, 0.930] | 0.737 [0.590, 0.827] |

Group I fit quality is robust across the ensemble — each observable shows median $R^2 > 0.70$. Group II shows the expected degradation in factor XIII; fibrinogen sits at median $R^2 = 0.407$ with the CI lower bound near zero, consistent with the fibrinogen channel cancellation diagnostic discussed in main text §4.4. Only 5 of 100 iterations achieve $R^2_{\text{G2}} \geq 0.4$ across *all six* observables simultaneously, highlighting that the joint Group II fit is constrained by the factor XIII channel, not by the data fit overall.

---

## S4.5 Sensitivity to normalisation (per-group standard deviations)

A peer-review query raised whether the factor XIII under-determination could be an artefact of the range-based scale factors for each observable. The range-based multiplier for factor XIII ($SC[\text{xiii}] = 150$) is set from the pooled value range of Group I and Group II. Per-group standard deviations differ sharply: $\sigma(\text{G1 xiii}) = 48.6$ vs. $\sigma(\text{G2 xiii}) = 6.36$, so normalising by per-group standard deviation would raise the weight of the Group II factor XIII residual approximately 24-fold relative to the default range-based multiplier. A single-seed re-fit on real data under per-group standard deviation normalisation raised $R^2_{\text{G2}}(\text{XIII})$ from 0.08 to 0.93 — superficially suggesting that the under-determination is a normalisation artefact.

**Bootstrap test (analysis 34).** We re-ran the parametric bootstrap (identical to S4.1 in all other respects) with per-group standard deviation normalisation. The fraction of $R^2_{\text{G2}}(\text{XIII}) < 0$ rose to **10 of 12 iterations (83%)**, *higher* than the 41% observed under range normalisation, not lower. The run was stopped at 12 of the planned 50 iterations because the 83% fraction was already decisive relative to the 16% decision threshold, and further iterations would not have changed the conclusion.

**Interpretation.** Raising the weight of the Group II factor XIII residual approximately 24-fold makes the cost surface steeper in the factor XIII channel, so the optimiser falls into the poor $b_x/k_x$ basin (subsection S4.3) *more often* under bootstrap noise, even though the good basin gives a better fit when reached on real data. Range-based normalisation is too soft for Group II factor XIII (under-weighted by 24×); per-group standard-deviation normalisation is too harsh (83% $R^2 < 0$). Both extremes confirm the same structural property: factor XIII under-determination is a property of the parameter manifold $\{a_x, c_x, b_x, k_x\}$, robust to the normalisation choice, not an artefact of it.

We retain range-based normalisation as the production setting (subsections S4.1–S4.4 and Table S2) and report the per-group standard deviation bootstrap as a sensitivity check. The full structural justification for the $c_x$ upper bound — the single most identifiable individual constraint on this manifold — is given in §S9.
