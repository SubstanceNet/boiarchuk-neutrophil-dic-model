# S3. Profile Likelihood Plots — All 26 Parameters

*Part of the Supplementary Information for Boiarchuk & Onasenko (2026). The parameter classification (§2.4: well-identified, weakly identified, sloppy) used in the main text for interpreting bootstrap intervals (§3.2, Table 1, Table S2). This appendix describes the profiling method, presents full per-parameter results, and provides multi-start validation of the sloppy classification.*

---

## S3.1 Method

For each of the 26 parameters $\theta_i$, the profile likelihood is

$$C(\theta_i) = \min_{\theta_{-i}}\; \text{cost}(\theta_i,\, \theta_{-i}),$$

computed on a grid of 11 values of $\theta_i$. The grid spans $\pm 50\%$ (linearly) or $e^{\pm 0.5} \approx \times 1.65$ (logarithmically) around the baseline best value, with a logarithmic step for parameters whose bounds span more than two orders of magnitude. At each grid point, the remaining 25 parameters are minimised by Nelder–Mead, with a single start from the baseline best vector $\mathbf{x}_{\text{best}}$. Total wall-clock time for the full scan: 4.6 hours.

The **relative profile depth** for parameter $\theta_i$ is defined as

$$\text{depth\_rel} = \frac{C_{\text{edge}} - C_{\text{baseline}}}{C_{\text{baseline}}},$$

where $C_{\text{edge}}$ is the smaller of the two grid-edge cost values. A sharp local minimum gives $\text{depth\_rel} \gg 0$; a flat profile gives $\text{depth\_rel} \approx 0$. Classification thresholds used throughout (aligned with main text §3.2):

- **Well-identified or moderately identified:** $\text{depth\_rel} > 5\%$
- **Weakly identified:** $2\% \leq \text{depth\_rel} \leq 5\%$
- **Sloppy:** $\text{depth\_rel} < 2\%$

The 95% confidence interval is read from the profile as the connected range of $\theta_i$ for which $C(\theta_i)$ remains within the $\chi^2$-based statistical threshold of $C_{\text{baseline}}$; this CI is reported for each parameter in Table S2 (derived from bootstrap) and is also recoverable from the per-panel figures referenced in S3.5.

---

## S3.2 Classification of all 26 parameters

Twenty-three parameters fall cleanly into the three depth-rel categories above; three additional parameters reach the grid boundary before a clearly defined minimum is found and are reported separately as *grid-truncated*. In total: 6 + 5 + 12 + 3 = 26.

**Well-identified or moderately identified (6 parameters, depth\_rel $> 5\%$).** These parameters carry the model's predictive content: their values are constrained by the data above the statistical threshold.

**Weakly identified (5 parameters, $2\% \leq$ depth\_rel $\leq 5\%$).** Constrained by the data, but with wide confidence intervals; predictions depending solely on them will carry visible uncertainty.

**Sloppy (12 parameters, depth\_rel $< 2\%$).** The cost changes by less than 2% across the full $\pm 50\%$ grid. When such a parameter is fixed at any value in this range, the others compensate and overall fit quality is preserved. Four of these twelve are particularly flat: **$k_{ca}$, $d_f$, $H_m$, $k_{na}$** all show depth\_rel $< 0.5\%$, meaning the cost changes by less than 0.5% across the full $\pm 50\%$ grid — the parameter is effectively unconstrained by the available data.

**Grid-truncated (3 parameters).** For $c_x$, $k_{rl}$, and $k_{cl}$, the baseline value sits near the parameter's upper bound, so the profile cannot be assessed symmetrically and the depth\_rel statistic is inconclusive. The main text subsumes them into the sloppy/weakly-identified categories for brevity; this distinction matters in particular for **$c_x$**, whose upper bound ($\leq 600$) is an active structural constraint motivated by identifiability collapse on the manifold $\{a_x, c_x, b_x, k_x\}$, not by data fitting (role in the model: §S1.3; full bound justification: §S9).

The full per-parameter table follows. depth\_rel values are from `analyses/09_profile_likelihood/results/`.

| **Parameter** | **depth\_rel** | **Category** |
|---|---|---|
| $t_{p2}$ | 0.473 †‡ | well-identified |
| $k_m$ | 0.154 | well-identified |
| $t_m$ | 0.141 | well-identified |
| $k_d$ | 0.073 | well-identified |
| $s_2$ | 0.072 | well-identified |
| $a_t$ | 0.071 | well-identified |
| $a_2$ | 0.038 | weakly identified |
| $a_r$ | 0.032 | weakly identified |
| $c_f$ | 0.024 | weakly identified |
| $k_r$ | 0.021 | weakly identified |
| $a_x$ | 0.020 | weakly identified |
| $b_t$ | 0.019 | sloppy |
| $c_r$ | 0.018 | sloppy |
| $a_f$ | 0.017 | sloppy |
| $b_r$ | 0.016 | sloppy |
| $k_x$ | 0.015 | sloppy |
| $b_x$ | 0.013 | sloppy |
| $k_{nd}$ | 0.013 | sloppy |
| $b_f$ | 0.013 | sloppy |
| $k_{na}$ | 0.0046 | sloppy (flattest) |
| $H_m$ | 0.0020 | sloppy (flattest) |
| $d_f$ | 0.0019 | sloppy (flattest) |
| $k_{ca}$ | 0.0018 | sloppy (flattest) |
| $c_x$ | — | grid-truncated |
| $k_{rl}$ | — | grid-truncated |
| $k_{cl}$ | — | grid-truncated |

† $t_{p2}$ (depth\_rel 0.473) has grid truncation at the upper end because its baseline value (9.22 d) sits near the parameter's upper bound (10 d); the well-identified classification is unaffected because the depth is large, but the bootstrap CI in Table S2 ([8.89, 10.03] d) is a more reliable uncertainty estimate for this parameter.

The sorting in this table — by depth\_rel (profile likelihood spectrum) — complements the sorting in Table S2 by relative bootstrap CI width (re-sampling spectrum). The two orderings are similar but not identical; the most informative divergence is **$k_d$** (well-identified by depth, wide bootstrap CI; interpretation in §S2.6).

---

## S3.3 Sloppiness as a structural property

The well-identified ratio $6/26 \approx 23\%$ places this model squarely within the typical range for mechanistic systems-biology models. Gutenkunst et al. (2007, PLoS Comput. Biol.) demonstrated across seventeen published biological models that *universal sloppiness* — the coexistence of a few stiff parametric directions with many soft ones — is a structural property of ODE models whose parameter count exceeds the effective dimensionality of the available data, not a defect of any particular fit.

The consequence is two-sided. **Predictions depending on well-identified parameters** — inducer impulse time $t_{p2}$, busulfan modifiers $k_m$ and $t_m$, degranulation rate constant $k_d$, impulse width $s_2$, and thrombin–inducer coefficient $a_t$ — are robust to data limitations and propagate narrow uncertainty bands. **Predictions isolating effects of sloppy parameters** (e.g. a counterfactual that varies only $k_{ca}$ with everything else held fixed) are not data-constrained and will carry wide uncertainty bands; we therefore do not present such isolated counterfactuals as results.

---

## S3.4 Multi-start validation: $k_{ca}$ diagnostic

The classifications above rely on single-start Nelder–Mead minimisation at each grid point. To verify that the *sloppy* classifications are genuine — rather than artefacts of the inner optimiser settling in a local minimum and missing a deeper basin elsewhere — we re-ran the profile for $k_{ca}$ (Table: depth\_rel 0.0018, second-flattest parameter) with five starting points at each grid value: the baseline best vector $\mathbf{x}_{\text{best}}$ plus four random points sampled uniformly within parameter bounds.

The result was unambiguous. At each of the 11 grid points, the lowest cost among the five starts matched the single-start result anchored to the baseline exactly ($\Delta$ across the grid: 0.000000 at every grid point; maximum multi-start improvement over single-start: 0.000000). The four random starts each converged to higher-cost basins (final cost 1.3–3.5 vs. $\approx 0.957$ anchored to the baseline). The baseline $\mathbf{x}_{\text{best}}$ is therefore a genuine local minimum of the 26-dimensional cost surface; the flat $k_{ca}$ profile is a multidimensional plateau (a sloppy direction in parameter space), not a failed optimisation. By extension, single-start profile likelihood is reliable for the other sloppy classifications as well.

---

## S3.5 Reading the per-parameter figure (26 panels)

The accompanying figure (in `analyses/09_profile_likelihood/figures/`) shows one panel per parameter. Each panel plots the relative cost increase $(C(\theta_i) - C_{\text{baseline}})/C_{\text{baseline}}$ on the vertical axis against parameter value on the horizontal axis. The axis is linear or logarithmic depending on the grid step (S3.1). The horizontal reference line corresponds to the 5% depth threshold; the vertical line marks the baseline best value; the shaded interval (where present) shows the 95% confidence range read from the profile.

Panels are ordered by classification: well-identified at the top, then weakly identified, then sloppy in descending depth\_rel, with the three grid-truncated parameters at the bottom. For the four deepest-sloppy parameters, the curve is effectively flat across the entire grid — visually confirming the depth\_rel $< 0.5\%$ conclusion from S3.2.

---

## S3.6 Relationship to bootstrap intervals

Profile likelihood (this appendix) measures the *local curvature of the cost surface* at the baseline optimum: how cost responds to perturbation of one parameter at a time, with all others free to compensate. Parametric bootstrap (§S4 and Table S2) measures the *global scatter under re-sampling of the data*: how the optimum shifts when synthetic data are drawn from the baseline predictions with noise. The two criteria are complementary and generally agree.

Main text §3.2 cites the profile likelihood depth criterion as the source of the well-identified classification. Bootstrap confidence intervals in Table S2 use a different criterion (re-sampling percentile) and produce a different parameter ordering by uncertainty; the key divergence is $k_d$, well-identified by depth (0.073) but wide by bootstrap (CI width 3.17×). The interpretation of this divergence — a sharp local minimum with a heavy re-sampling right tail — is given in §S2.6.
