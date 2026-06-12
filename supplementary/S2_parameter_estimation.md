# S2. Parameter Estimation Pipeline and Full Estimates

*Part of the Supplementary Information for Boiarchuk & Onasenko (2026). The high-level pipeline is described in the main text (§2.3 — base; §2.4 — ensemble); this appendix provides the full technical specification: the cost function, stage-by-stage settings for both pipelines, and full parameter estimates. Related appendices: the $W_{\text{SPLIT}}$ prior is justified in S8; the shared-vs.-Group-II-only architecture trade-off in S10; bootstrap diagnostics in S4.*

---

## S2.1 Cost function

The model is fitted by minimising a joint cost function with three additive terms:

$$J(p_v) = J_{\text{data}}(p_v) + W_{\text{SPLIT}} \cdot J_{\text{split}}(p_v) + J_{Hn}(p_v).$$

**$J_{\text{data}}$ — sum of per-channel normalised RMSE.** This is the data-fitting term. For each group $g$ and observable $k$ it is the root-mean-square standardised residual over that group's time points; these per-channel values are summed over the six observables (S1.6) and over both groups:

$$J_{\text{data}} = \sum_{g \in \{G_1, G_2\}} W_{\text{GROUP},g} \sum_{k=1}^{6} \sqrt{\frac{1}{|T_g|} \sum_{t \in T_g} \left[\frac{y_{\text{obs}}(g, k, t) - y_{\text{model}}(g, k, t)}{SC_k}\right]^2}.$$

Here $T_g$ is the set of time points for group $g$ and $|T_g|$ its size; the inner root-mean-square puts each observable on a comparable footing regardless of how many time points it has, and the square root means a single poorly fitted channel is penalised sub-linearly rather than quadratically (this is what distinguishes the metric from a plain sum of squared residuals). The scale factor for each observable $SC_k$ is by default range-based (to make residuals across observables of different units commensurate); the sensitivity analysis using per-group standard deviations is described in S4. $W_{\text{GROUP}} = (1.0, 1.0)$ gives equal weight to both groups, and the time-average within each channel is uniform. (An earlier formulation, cost v12, applied a non-uniform survivor weight $W_{\text{SURV}}$ that downweighted late Group I time points to compensate for the 30% lethality between days 10–12; this proved empirically harmful — removing it improved mean Group II $R^2$ by approximately 10 percentage points at negligible cost to Group I, analysis 04 — and was discarded. The production v13 cost contains no survivor-weighting term.)

**$W_{\text{SPLIT}} \cdot J_{\text{split}}$ — mechanism-decomposition prior.** The model is structurally unable to identify the neutrophil-attributed fraction of day 2 for each coagulation channel from the data alone (different optimiser seeds find equicost solutions with recalcification fractions ranging from 0.34 to 0.48). A soft penalty attracts the three fractions toward biologically derived targets:

$$J_{\text{split}} = \sum_{k \in \{\text{recalc, fib, xiii}\}} \mathbb{1}\!\left[(v_k + n_k) > 1\right] \cdot \left(\frac{n_k}{v_k + n_k} - f_k^{\text{target}}\right)^2,$$

where, for each channel, $v_k$ and $n_k$ are the vascular- and neutrophil-attributed *production* contributions on day 2 of Group I (the positive terms of the corresponding observable equation, S1.6), $n_k/(v_k+n_k)$ is the neutrophil-attributed fraction, and the targets are $f^{\text{target}} = (0.24,\, 0.76,\, 0.82)$ for recalcification, fibrinogen, and factor XIII. The indicator $\mathbb{1}[(v_k+n_k)>1]$ gates the penalty: a channel enters $J_{\text{split}}$ only when the combined day-2 amplitude is large enough for the fraction to be well defined, and is excluded below that threshold. $W_{\text{SPLIT}} = 2.0$ was chosen via sensitivity analysis (full justification with scan of $W \in \{0, 0.3, 1.0, 2.0, 5.0\}$ is given in S8). The targets are derived independently from the day-1 ratios $(\Delta G_1 - \Delta G_2)/\Delta G_1$ in the experimental tables, not from the day-2 fit; the derivation is described in main text §3.3. Because the fraction is built from the *production* terms, it quantifies the neutrophil contribution to the early (day-1/day-2) rise of each channel, not to its later depletion (see main text §4.2 for the fibrinogen case).

**$J_{Hn}$ — saturation guard.** A soft penalty discourages trajectories in which the neutrophil-derived coagulation pool $H_n$ approaches its limiting capacity $H_m$ too closely (where the $g_{Hn}$ nonlinearity, S1.4, would become numerically unstable). This is a numerical safeguard rather than a biological constraint; across all 100 bootstrap members and 22,500 dose–response simulations the guard never triggers.

---

## S2.2 Base fitting pipeline

The baseline parameter vector reported in Table 1 (main text) and Table S2 below is obtained from the multi-seed global-search plus local-refinement pipeline implemented in `src/fit.py`.

**Differential evolution.** `scipy.optimize.differential_evolution` with `popsize=12`, `maxiter=300`, `tol=1e-7`, `mutation=(0.5, 1.5)`, `recombination=0.85`, default scipy initialisation (Latin hypercube), and `polish=False` (internal DE refinement disabled, since we run our own multi-stage refinement).

**Multi-seed.** DE is launched five times independently, with seeds $[42, 7, 123, 2024, 999]$. Each run yields a candidate optimum.

**Local refinement.** Each candidate is refined by a three-stage sequence using `scipy.optimize.minimize`:

1. Nelder–Mead, `maxiter=10000`, `xatol=1e-9`, `fatol=1e-10`.
2. Powell, `maxiter=8000`, `ftol=1e-10`.
3. Nelder–Mead, `maxiter=10000`, `xatol=1e-10`, `fatol=1e-11` (tighter than stage 1, to sharpen the Powell result).

**Selection.** The result with the lowest cost among the five refined seeds is retained as the joint baseline. Costs across seeds typically span a range of 0.02–0.05 around the best (seed 42 minimises in the documented baseline, with a final cost of 0.959).

This pipeline is run **once** to obtain the baseline parameter vector. The ensemble pipeline below (S2.3) is run repeatedly for uncertainty characterisation.

---

## S2.3 Ensemble fitting pipeline

The three robustness analyses in main text §2.4 (bootstrap, leave-one-out, neutrophil-count perturbation) share a common lightweight re-fitting pipeline, distinct from S2.2 due to computational cost: 168 total re-fits across three analyses (100 bootstrap + 23 LOO + 5 $\alpha$-scan + 20 + 20 stochastic perturbation re-fits) would be impractical under the full multi-seed base settings.

**Differential evolution.** The same `scipy` call as in S2.2, but with `popsize=15`, `maxiter=200`, `init='sobol'`, and one seed per iteration (the iteration number). Other DE settings (`tol=1e-7`, `mutation=(0.5, 1.5)`, `recombination=0.85`, `polish=False`) are unchanged.

**Local refinement.** The same NM → Powell → NM structure as in S2.2, but with looser per-stage iteration limits (NM `maxiter=3000`, Powell `maxiter=2000`, final NM `maxiter=3000`) and slightly looser NM stage-1 tolerances (`xatol=1e-8`, `fatol=1e-10` vs. `1e-9`, `1e-10` in S2.2); final NM tolerances (`xatol=1e-9`, `fatol=1e-11`) are one decade looser than the base-pipeline final stage.

This pipeline is called identically in `analyses/22_predictive_check/run.py` (bootstrap), `analyses/20_loo_timepoint/run.py` (LOO), and `analyses/21_perturbation/run_alpha_scan.py` plus `run_stochastic.py` (perturbation), guaranteeing that ensemble members across the three analyses are produced under identical optimisation conditions.

---

## S2.4 Hyperparameters at a glance

Both pipelines side by side, to make differences visible in one place:

| **Setting** | **Base (S2.2)** | **Ensemble (S2.3)** |
|---|---|---|
| DE popsize | 12 | 15 |
| DE maxiter | 300 | 200 |
| DE init | default (LHS) | Sobol |
| DE seeds | 5 multi-seed (42, 7, 123, 2024, 999) | 1 per iteration |
| DE polish (internal) | False | False |
| DE tol | $1\times10^{-7}$ | $1\times10^{-7}$ |
| DE mutation | (0.5, 1.5) | (0.5, 1.5) |
| DE recombination | 0.85 | 0.85 |
| Refinement stage 1 (NM) maxiter | 10000 | 3000 |
| Refinement stage 1 (NM) xatol, fatol | $1\times10^{-9}$, $1\times10^{-10}$ | $1\times10^{-8}$, $1\times10^{-10}$ |
| Refinement stage 2 (Powell) maxiter | 8000 | 2000 |
| Refinement stage 2 (Powell) ftol | $1\times10^{-10}$ | $1\times10^{-10}$ |
| Refinement stage 3 (NM) maxiter | 10000 | 3000 |
| Refinement stage 3 (NM) xatol, fatol | $1\times10^{-10}$, $1\times10^{-11}$ | $1\times10^{-9}$, $1\times10^{-11}$ |
| Total calls | 1 (base) | 168 (100+23+5+20+20) |

---

## S2.5 Full parameter estimates

**Table S2.** Estimates and 95% bootstrap confidence intervals for all 26 parameters (100-member ensemble), sorted by relative CI width (identifiability spectrum, tightest first). Parameters marked † are the six classified as well-identified by profile likelihood (relative depth > 5%). Relative width is (upper − lower) / |median|.

| **Parameter** | **Description** | **Median [95% CI]** | **Rel. width** | **Well-id.** |
|---|---|---|---|---|
| $t_{p2}$ | Time to peak of inducer toxicity impulse (Group I) | 9.217 [8.889, 10.03] | 0.12× | † |
| $t_m$ | Group II busulfan modifier on $t_{p2}$ (timing) | 0.4267 [0.3918, 0.4675] | 0.18× | † |
| $a_t$ | Thrombin / inducer impulse coefficient | 5.659 [4.893, 6.437] | 0.27× | † |
| $a_r$ | Recalcification / inducer impulse coefficient | 34.74 [28, 40.01] | 0.35× | |
| $k_m$ | Group II busulfan modifier on $k_r$ (rate) | 4.918 [3.462, 5.734] | 0.46× | † |
| $c_r$ | Recalcification / $AP$ coefficient | 35.61 [27.55, 45.11] | 0.49× | |
| $c_x$ | Factor XIII production / $AP \cdot N_r$ (elastase-mediated plasma XIII activation) | 545.8 [294.8, 600] | 0.56× | |
| $s_2$ | Width of inducer toxicity impulse | 1.757 [1.513, 2.712] | 0.68× | † |
| $a_x$ | Factor XIII production / inducer impulse | 47.21 [25.63, 67.73] | 0.89× | |
| $b_f$ | Fibrinogen / $g_{Hn}$ coefficient (consumption) | 6.219 [2.335, 7.999] | 0.91× | |
| $c_f$ | Fibrinogen / $AP$ coefficient (neutrophil-secretion driven) | 99.68 [59.87, 154.7] | 0.95× | |
| $a_f$ | Fibrinogen / inducer impulse coefficient | 9.949 [5.527, 15.03] | 0.96× | |
| $k_x$ | Liver-modulated factor XIII resynthesis | 2.604 [1.408, 4.047] | 1.01× | |
| $b_x$ | Factor XIII degradation / $g_{Hn}$ | 34.07 [11.77, 49.01] | 1.09× | |
| $b_r$ | Recalcification / $g_{Hn}$ coefficient | 8.876 [3.043, 13.49] | 1.18× | |
| $b_t$ | Thrombin / $g_{Hn}$ coefficient | 0.5546 [0.1854, 0.8652] | 1.23× | |
| $k_{cl}$ | $AP$ clearance rate | 12.01 [3.372, 18.25] | 1.24× | |
| $k_{rl}$ | $AP$ release rate from degranulated cells | 12.69 [4.001, 19.97] | 1.26× | |
| $k_{nd}$ | $H_n$ decay rate | 6.167 [1.94, 9.999] | 1.31× | |
| $a_2$ | Inducer toxicity impulse amplitude | 3.423 [2.654, 8.312] | 1.65× | |
| $k_{na}$ | $H_n$ formation rate (from $AP^2$) | 257.4 [80.92, 644.6] | 2.19× | |
| $k_d$ | Degranulation rate constant | 0.2635 [0.2179, 1.054] | 3.17× | † |
| $H_m$ | $H_n$ limiting capacity | 290.5 [11.11, 999.8] | 3.40× | |
| $k_{ca}$ | $H_c$ accumulation from inducer | 3.834 [0.1334, 33.34] | 8.66× | |
| $k_r$ | Recovery/clearance of degranulated state (Group I) | 0.247 [0.1802, 2.693] | 10.17× | |
| $d_f$ | Fibrinogen / $H_c$ coefficient (inducer pathway) | 1.037 [0.1221, 13.01] | 12.43× | |

---

## S2.6 Reading Table S2: the identifiability spectrum and the well-identified flag

The 26 parameters in Table S2 are sorted by relative bootstrap CI width (upper − lower) / |median|, from tightest ($t_{p2}$, 0.12×) to widest ($d_f$, 12.43×). This ordering reflects the *re-sampling-determined* identifiability spectrum: how narrowly each parameter is determined when the data are perturbed by Gaussian noise (S4).

The dagger (†) marks six parameters classified as well-identified under a separate criterion: relative profile likelihood depth greater than 5%. Profile depth measures the local curvature of the cost surface at the optimum; bootstrap CI width measures the global scatter across re-samples. The two criteria generally agree (a sharp local minimum corresponds to a narrow re-sampling distribution), but they can diverge. The most striking example is **$k_d$**: flagged as well-identified by profile likelihood (sharp local minimum, depth > 5%), yet carrying a wide bootstrap CI (3.17×) caused by a heavy right tail in the re-sampling distribution. Interpretation: the optimum is locally sharp, but a minority of bootstrap iterations find alternative equicost solutions at larger $k_d$ values. **$s_2$** shows a milder manifestation of the same pattern (CI width 0.68×, wider than the other four well-identified parameters but not as extreme as $k_d$).

Parameter bounds are defined in `src/config.py` and reproduced in the code repository (S7); the upper bound on $c_x$ ($\leq 600$) is the only bound that saturates in the baseline fit (Table S2: median $c_x$ 545.8, upper CI 600.0). The biological and methodological justification for the $c_x$ bound is documented in S9.

---

## S2.7 Shared architecture versus Group-II-only

The pipelines above fit the joint cost across both groups, with 24 shared parameters plus two group-specific modifiers ($k_m$, $t_m$; definitions in S1.9). This architecture trades shared connectivity for some Group II fit quality: separate fitting of Group II alone achieves approximately 14 percentage points higher average Group II $R^2$ than joint fitting. The gap is concentrated almost entirely in the structurally under-determined factor XIII channel—the remaining five observables fit comparably under joint and separate fitting. This channel-specific localisation, rather than a diffuse improvement, is what establishes the gap as *architectural* (relief of a known structural constraint on factor XIII; §S4, §S9), not *overfitting* (which would improve channels indiscriminately). Full evidence and per-observable breakdown are given in S10.
