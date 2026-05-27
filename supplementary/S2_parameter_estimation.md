# S2. Parameter estimation pipeline and full estimates

*Part of the Supplementary Information for the manuscript "A mechanistic model of neutrophil-driven disseminated intravascular coagulation…" Main-text references give the high-level pipeline (Methods §2.3 baseline; §2.4 ensemble); this section is the complete technical specification — cost function, per-stage settings for both pipelines, and full parameter estimates. Pointers to related sections: the W_SPLIT prior is justified in S8; the joint-vs-Group-II-only architecture trade-off is documented in S10; bootstrap diagnostics are in S4.*

---

## S2.1 Cost function

The model was fit by minimising a joint cost function of three additive terms:

> J(pv) = J_SSR(pv) + W_SPLIT · J_split(pv) + J_Hn(pv).

**J_SSR — weighted sum of squared residuals.** This is the data-fit term, summed over both groups (G1, G2), the six observables defined in S1.6, and all observation timepoints:

> J_SSR = Σ_g Σ_k Σ_t W_GROUP_g · W_SURV_{g,t} · [(y_obs(g, k, t) − y_model(g, k, t)) / SC_k]².

The six observables (three algebraic, one dynamic-state, two direct-state; see S1.6 for the formulas) enter through the standardised residual (y_obs − y_model)/SC_k. The per-observable scale factor SC_k is range-based by default (so that residuals across observables of different units are comparable); a sensitivity analysis using per-group standard deviations is described in S4. W_GROUP = (1.0, 1.0) gives both groups equal weight. W_SURV weights timepoints within each group; in the v13 baseline this is uniform across all timepoints. An earlier v12 cost down-weighted late Group I timepoints to compensate for the 30% mortality between days 10–12, but that weighting was found to be empirically harmful — removing it improved mean Group II R² by approximately 10 percentage points at negligible Group I cost (analysis 04 in the code repository), so v13 uses uniform weighting.

**W_SPLIT · J_split — mechanism-split prior.** The model is structurally unable to identify the day-2 neutrophil-attributable fraction of each coagulation channel from data alone (different optimiser seeds find cost-equivalent solutions with recalcification fractions ranging from 0.34 to 0.48). A soft penalty pulls the three fractions toward biologically-derived targets:

> J_split = (f_recalc − 0.24)² + (f_fib − 0.76)² + (f_xiii − 0.82)²,

with W_SPLIT = 2.0 selected by sensitivity analysis (full justification, with the W ∈ {0, 0.3, 1.0, 2.0, 5.0} sweep, is in S8). The targets are derived independently from the day-1 (ΔG1 − ΔG2)/ΔG1 ratios in the experimental tables, not from the day-2 fit; the derivation is described in main text §3.3.

**J_Hn — saturation guard.** A soft penalty discourages trajectories in which the neutrophil-derived coagulation pool Hn approaches its carrying capacity Hm too closely (where the gHn nonlinearity, S1.4, would become numerically unstable). This is a numerical guard rather than a biological constraint; under all 100 bootstrap members and 22,500 dose-response simulations the guard never binds.

---

## S2.2 Baseline-fit pipeline

The baseline parameter vector reported in Table 1 (main text) and in Table S2 below is obtained from a multi-seed global-search-plus-local-polish pipeline implemented in `src/fit.py`.

**Differential evolution.** scipy.optimize.differential_evolution with `popsize=12`, `maxiter=300`, `tol=1e-7`, `mutation=(0.5, 1.5)`, `recombination=0.85`, scipy default initialisation (Latin Hypercube), and `polish=False` (the DE-internal polish is disabled because we run our own multi-stage polish next).

**Multi-seed.** DE is run five times independently, with seeds [42, 7, 123, 2024, 999]. Each run produces a candidate optimum.

**Local polish.** Each candidate is refined by a three-stage sequence using scipy.optimize.minimize:

1. Nelder–Mead, `maxiter=10000`, `xatol=1e-9`, `fatol=1e-10`.
2. Powell, `maxiter=8000`, `ftol=1e-10`.
3. Nelder–Mead, `maxiter=10000`, `xatol=1e-10`, `fatol=1e-11` (tighter than stage 1, to refine the Powell result).

**Selection.** The lowest-cost result across the five polished seeds is retained as the joint baseline. Per-seed costs typically span a range of 0.02–0.05 around the best (seed 42 minimises in the published baseline, with final cost 0.959).

This pipeline is run **once** to produce the baseline parameter vector. The ensemble pipeline below (S2.3) is run repeatedly to characterise uncertainty.

---

## S2.3 Ensemble-fit pipeline

The three robustness analyses in main text §2.4 (bootstrap, leave-one-out, neutrophil-count perturbation) share a common lighter pipeline, distinct from S2.2 because of computational cost: 168 total refits across the three analyses (100 bootstrap + 23 LOO + 5 α-scan + 20 + 20 stochastic perturbation refits) would be infeasible at the multi-seed baseline settings.

**Differential evolution.** Same scipy call as S2.2 but with `popsize=15`, `maxiter=200`, `init='sobol'`, and a single seed per iteration (the iteration number). Other DE settings (`tol=1e-7`, `mutation=(0.5, 1.5)`, `recombination=0.85`, `polish=False`) are unchanged.

**Local polish.** Same NM → Powell → NM structure as S2.2 but with looser per-stage iteration limits (NM `maxiter=3000`, Powell `maxiter=2000`, final NM `maxiter=3000`) and slightly looser stage-1 NM tolerances (`xatol=1e-8`, `fatol=1e-10` vs `1e-9, 1e-10` in S2.2); the final NM tolerances (`xatol=1e-9`, `fatol=1e-11`) are one decade looser than the baseline-pipeline final stage.

This pipeline is invoked identically by `analyses/22_predictive_check/run.py` (bootstrap), `analyses/20_loo_timepoint/run.py` (LOO), and `analyses/21_perturbation/run_alpha_scan.py` plus `run_stochastic.py` (perturbation), ensuring that ensemble members across the three analyses are produced under identical optimisation conditions.

---

## S2.4 Hyperparameters at a glance

The two pipelines side-by-side, so that the differences are visible in one place:

| Setting | Baseline (S2.2) | Ensemble (S2.3) |
|---|---|---|
| DE popsize | 12 | 15 |
| DE maxiter | 300 | 200 |
| DE init | default (LHS) | Sobol |
| DE seeds | 5 multi-seed (42, 7, 123, 2024, 999) | 1 per iteration |
| DE polish (internal) | False | False |
| DE tol | 1×10⁻⁷ | 1×10⁻⁷ |
| DE mutation | (0.5, 1.5) | (0.5, 1.5) |
| DE recombination | 0.85 | 0.85 |
| Polish stage 1 (NM) maxiter | 10000 | 3000 |
| Polish stage 1 (NM) xatol, fatol | 1×10⁻⁹, 1×10⁻¹⁰ | 1×10⁻⁸, 1×10⁻¹⁰ |
| Polish stage 2 (Powell) maxiter | 8000 | 2000 |
| Polish stage 2 (Powell) ftol | 1×10⁻¹⁰ | 1×10⁻¹⁰ |
| Polish stage 3 (NM) maxiter | 10000 | 3000 |
| Polish stage 3 (NM) xatol, fatol | 1×10⁻¹⁰, 1×10⁻¹¹ | 1×10⁻⁹, 1×10⁻¹¹ |
| Total invocations | 1 (baseline) | 168 (100+23+5+20+20) |

---

## S2.5 Full parameter estimates

**Table S2.** Estimates and 95% bootstrap confidence intervals for all 26 parameters (100-member ensemble), sorted by relative CI width (an identifiability spectrum, tightest first). Parameters flagged † are the six classified as well-identified by profile likelihood (relative depth > 5%). Relative width is (upper − lower)/|median|.

| Parameter | Description | Median [95% CI] | Rel. width | Well-id. |
| --- | --- | --- | --- | --- |
| tp2 | Inducer-toxicity pulse peak time (Group I) | 9.217 [8.889, 10.03] | 0.12× | † |
| tm | Group II busulfan modifier on τp2 (timing) | 0.4267 [0.3918, 0.4675] | 0.18× | † |
| at | Thrombin / inducer-pulse coefficient | 5.659 [4.893, 6.437] | 0.27× | † |
| ar | Recalcification / inducer-pulse coefficient | 34.74 [28, 40.01] | 0.35× | |
| km | Group II busulfan modifier on kr (rate) | 4.918 [3.462, 5.734] | 0.46× | † |
| cr | Recalcification / AP coefficient | 35.61 [27.55, 45.11] | 0.49× | |
| cx | XIII production / AP·Nr (azurophil-granule store) | 545.8 [294.8, 600] | 0.56× | |
| s2 | Inducer-toxicity pulse width | 1.757 [1.513, 2.712] | 0.68× | † |
| ax | XIII production / inducer-pulse | 47.21 [25.63, 67.73] | 0.89× | |
| bf | Fibrinogen / gHn coefficient (consumption) | 6.219 [2.335, 7.999] | 0.91× | |
| cf | Fibrinogen / AP coefficient (neutrophil-secretion-driven) | 99.68 [59.87, 154.7] | 0.95× | |
| af | Fibrinogen / inducer-pulse coefficient | 9.949 [5.527, 15.03] | 0.96× | |
| kx | XIII liver-modulated resynthesis | 2.604 [1.408, 4.047] | 1.01× | |
| bx | XIII degradation / gHn | 34.07 [11.77, 49.01] | 1.09× | |
| br | Recalcification / gHn coefficient | 8.876 [3.043, 13.49] | 1.18× | |
| bt | Thrombin / gHn coefficient | 0.5546 [0.1854, 0.8652] | 1.23× | |
| kcl | AP clearance rate | 12.01 [3.372, 18.25] | 1.24× | |
| krl | AP release rate from degranulated cells | 12.69 [4.001, 19.97] | 1.26× | |
| knd | Hn decay rate | 6.167 [1.94, 9.999] | 1.31× | |
| a2 | Inducer-toxicity pulse amplitude | 3.423 [2.654, 8.312] | 1.65× | |
| kna | Hn formation rate (from AP²) | 257.4 [80.92, 644.6] | 2.19× | |
| kd | Degranulation rate constant | 0.2635 [0.2179, 1.054] | 3.17× | † |
| Hm | Hn carrying capacity | 290.5 [11.11, 999.8] | 3.40× | |
| kca | Hc accumulation from inducer | 3.834 [0.1334, 33.34] | 8.66× | |
| kr | Recovery/clearance of degranulated state (Group I) | 0.247 [0.1802, 2.693] | 10.17× | |
| df | Fibrinogen / Hc coefficient (inducer pathway) | 1.037 [0.1221, 13.01] | 12.43× | |

---

## S2.6 Reading Table S2: identifiability spectrum and the well-identified flag

The 26 parameters in Table S2 are sorted by relative bootstrap CI width (upper − lower)/|median|, from the tightest (tp2, 0.12×) to the widest (df, 12.43×). This ordering reflects a *resampling-defined* identifiability spectrum: how narrowly each parameter is determined when the data are perturbed by Gaussian noise (S4).

The dagger flag (†) marks the six parameters classified as well-identified by a different criterion: profile-likelihood relative depth greater than 5%. Profile-likelihood depth measures local curvature of the cost surface at the optimum; bootstrap CI width measures global spread across resamples. The two criteria usually agree (a sharp local minimum corresponds to a narrow resample distribution), but they can diverge. The clearest example is **kd**: it is flagged as well-identified by profile likelihood (sharp local minimum, depth > 5%) yet has a wide bootstrap CI (3.17×), driven by a long right tail in the resample distribution. Interpretation: the optimum is locally sharp, but a minority of bootstrap iterations find alternative cost-equivalent solutions at larger kd values. **s2** shows a milder instance of the same pattern (CI width 0.68×, wider than the other four well-identified parameters but not as extreme as kd).

Parameter bounds are defined in `src/config.py` and are reproduced in the code repository (S7); the upper bound on cx (≤ 600) is the only bound that saturates in the baseline fit (Table S2: cx median 545.8, upper CI 600.0). The biological and methodological justification for the cx bound is documented in S9.

---

## S2.7 Joint vs Group-II-only architecture

The pipelines above fit a joint cost across both groups, with 24 shared parameters plus two group-specific modifiers (km, tm; see S1.9 for definitions). This architecture trades joint coherence for some Group II fit quality: a separate Group-II-only fit attains approximately 22 percentage points higher mean Group II R² than the joint fit, with a uniform improvement across all six observables. The uniformity is the key methodological observation — it argues that the gap is *architectural* (an unavoidable cost of fitting two groups with one mechanistic parameterisation) rather than *overfitting* (which would manifest as spiky improvements on a few observables). The full evidence and the per-observable breakdown are in S10.
