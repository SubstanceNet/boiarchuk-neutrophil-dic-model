# S10. Shared Architecture Versus Group-II-Only

*Part of the Supplementary Information for Boiarchuk & Onasenko (2026). Cross-references from the main text: §2.3 ("separate fitting of Group II alone achieves approximately 22 percentage points higher average $R^2$ for Group II than joint fitting (Supplementary Methods), a gap that is predominantly architectural rather than due to overfitting"). Related appendices: §S1.9 (24-shared + 2-modifier architecture), §S2.7 (architecture pointer in the estimation appendix), §S3.2 (parameter identifiability), §S9 ($c_x \leq 600$ bound, which already partially alleviates the factor XIII channel).*

---

## S10.1 Settings

To quantify the architectural cost of the joint cost function (§S2.1, §S1.9), we ran a *separate* fit for Group II only and compared its per-observable Group II $R^2$ against the joint baseline.

The separate fit retains:

- All 26 parameters of the shared model.
- The same per-observable scale factors $SC_k$ (range-based) for Group II residuals.
- The $H_n$ saturation guard $J_{Hn}$ as a numerical safeguard.

The separate fit removes:

- The Group I contribution to the cost ($W_{\text{GROUP,G1}} = 0$).
- The mechanism-decomposition penalty $W_{\text{SPLIT}} \cdot J_{\text{split}}$, which constrains Group I day-2 fractions and is irrelevant when Group I is not being fitted.

Other settings:

- One seed (42), fast-mode pipeline (DE popsize 8, maxiter 120, plus standard NM → Powell → NM refinement from §S2.3).
- Source: `analyses/03_separate_g2_fit/`.
- Wall-clock time: 510 s.

The separate fit has **54 Group II data points (9 time points $\times$ 6 observables) versus 26 free parameters**, a data-to-parameter ratio of 2.08. This is low and raises a formal overfitting concern; the analysis below addresses it explicitly in S10.3.

---

## S10.2 Per-observable comparison

Per-observable Group II $R^2$ at the joint baseline (seed 42, §S2.5 / Table S2) and at the separate fit (analysis 03):

| **Observable** | **$R^2_{\text{G2}}$ joint** | **$R^2_{\text{G2}}$ separate** | **$\Delta$ (separate $-$ joint)** |
|---|---|---|---|
| recalc | +0.6841 | +0.9013 | +0.2172 |
| thrombin | +0.8347 | +0.9936 | +0.1589 |
| fib | +0.2931 | +0.5778 | +0.2847 |
| xiii | +0.7277 | +0.7980 | +0.0703 |
| AP | +0.6777 | +0.9283 | +0.2506 |
| D | +0.5051 | +0.8191 | +0.3140 |
| **mean** | **+0.6204** | **+0.8363** | **+0.2160** |

The mean improvement $\Delta \approx 0.216$ is the **$\approx 22$ percentage points** figure reported in main text §2.3. Reading the columns:

- All six observables improve under separate fitting; $\Delta$ is positive everywhere.
- The largest $\Delta$: **degranulation index (+0.314), fibrinogen (+0.285), and acid phosphatase (+0.251)**.
- The smallest $\Delta$: **factor XIII (+0.070)**, the channel already partially alleviated in the joint baseline by the structural prior $c_x \leq 600$ (§S9).
- Recalcification and thrombin show intermediate $\Delta$ (+0.217 and +0.159).

---

## S10.3 Why architectural, not overfitting

The data-to-parameter ratio of 2.08 (S10.1) is low enough that the separate fit could in principle exploit additional freedom to overfit the 54 Group II data points. Three independent observations argue against this and in favour of the *architectural* interpretation — that the joint fit is genuinely over-constrained to capture Group II dynamics, and the separate-fit advantage reflects relief of this constraint rather than spurious parameter oscillation.

**Argument 1 — uniformity across observables.** Pure overfitting would have a spiky per-observable signature: very high $R^2$ on a few channels where 26 parameters happen to fit a particular time-point sequence, moderate improvement elsewhere. The observed pattern is the opposite: all six observables improve together, with $\Delta$ spanning the narrow range $[0.070, 0.314]$ around the mean 0.216. Uniform improvement across all six channels is the signature of architectural-constraint relief, not of parameter fishing.

**Argument 2 — smallest gap on the $c_x$-constrained channel.** Factor XIII has the smallest $\Delta$ (+0.070), noticeably smaller than the others. This is precisely what the architectural interpretation predicts: the $c_x \leq 600$ prior (§S9) already partially alleviates the shared architecture in the factor XIII channel — it gives the joint fit access to the same parameter subspace that the separate fit explores. The remaining five channels have no such prior and remain fully constrained under joint fitting. The $\Delta$ pattern (large on unconstrained channels, small on the $c_x$-alleviated channel) is mechanistically consistent with constraint-relief; it has no natural reading under pure overfitting.

**Argument 3 — effective dimensionality far below 26.** The data-to-parameter ratio of 2.08 uses the nominal parameter count. Profile likelihood analysis (§S3.2) classifies the 26 parameters as 6 well-identified, 5 weakly identified, 12 sloppy, and 3 grid-truncated. The sloppy and grid-truncated categories contribute very little to the effective fitting dimensionality: for the 12 sloppy parameters, cost changes less than 2% across the full $\pm 50\%$ grid, and the 3 grid-truncated simply cannot be assessed. The effective fitting dimensionality is therefore substantially below 26, and the *effective* data-to-parameter ratio is correspondingly more comfortable. A reader wanting the precise effective count can read it from Table S2 and the §S3.2 classification; the qualitative point is that the nominal-26 overstates the model's flexibility.

Together the three arguments support the architectural interpretation. The separate-fit advantage is genuine constraint relief, not a parameter-fishing artefact.

---

## S10.4 What the gap means

The shared architecture forces both groups to share 24 of 26 parameters: degranulation kinetics ($k_d, k_{rl}, k_{cl}$), neutrophil-derived pool kinetics ($k_{na}, k_{nd}, H_m$), four factor XIII channel parameters ($a_x, c_x, b_x, k_x$), inducer impulse parameters ($k_{ca}, k_{cd}$ in S1.7 plus $a_2, s_2, t_{p2}$), and all nine algebraic observable coefficients ($a_r, b_r, c_r, a_t, b_t, a_f, b_f, c_f, d_f$). Only two parameters — $k_m$ and $t_m$ — are group-specific (§S1.9). This shared parametrisation encodes the biological hypothesis that busulfan modifies the *kinetics and timing* of the neutrophil compartment ($k_m$, $t_m$) without altering its *per-cell biochemistry* (everything else shared).

The 22 pp $R^2_{\text{G2}}$ gap is the cost of this hypothesis. Separate fitting, without shared parameters, would achieve $\approx 0.84$ mean $R^2_{\text{G2}}$; joint fitting achieves $\approx 0.62$; the difference is the price paid for a single shared mechanistic parametrisation for both groups. This price is accepted because the mechanistic claims that follow — in particular the busulfan mechanism interpretation in §3.5 of the main text and the dose–response dependence in §S6, both of which rely on $k_m$ and $t_m$ meaning the same thing across groups — require a single shared per-cell biochemistry. A separate-fit parametrisation would give better Group II numbers but would not support a comparable claim about what *changed* between groups.

---

## S10.5 Failed single-parameter alternatives

It is natural to ask whether the gap could be narrowed by adding one or two group-specific parameters beyond $k_m$ and $t_m$ — selectively relieving the shared constraint on channels with the largest $\Delta$ (S10.2). Two such extensions were tested:

- **Group-specific $c_x$** (`analyses/07_groupspec_cx/`): allow $c_{x,\text{G1}}$ and $c_{x,\text{G2}}$ to differ. This is the most natural candidate, because the $c_x \leq 600$ prior already acts as a constraint relief for the factor XIII channel in joint fitting.

- **Group-specific $c_f$** (`analyses/08_groupspec_cf/`): allow $c_{f,\text{G1}}$ and $c_{f,\text{G2}}$ to differ. This addresses the largest single $\Delta$ outside the degranulation index, namely fibrinogen.

Both were rejected. The marginal improvement in $R^2_{\text{G2}}$ in each case was small (a few percentage points on average, sometimes concentrated in the factor XIII channel via regularisation rather than the target channel) and attributable to optimiser stabilisation — a side-effect of adding a degree of freedom — rather than genuine channel-specific relief. Neither extension closed the 22 pp gap; neither gave a consistent architectural improvement comparable to what the separate fit shows. The conclusion is that closing the gap would require an architectural redesign touching most channels simultaneously, not adding one or two group-specific parameters; such a redesign is beyond the scope of the present work and would change the central biological claim of the manuscript about shared per-cell biochemistry.

---

## S10.6 Conclusion

Three points close the justification for accepting the 22 pp gap:

- **The gap is quantified.** Mean $R^2_{\text{G2}} = 0.6204$ (joint) vs. 0.8363 (separate); $\Delta_{\text{mean}} = +0.2160$. All six observables improve under separate fitting, with $\Delta \in [0.070, 0.314]$ (S10.2).

- **The gap is architectural, not overfitting.** Three independent arguments support this reading: per-observable uniformity rather than spiky improvement; the smallest $\Delta$ on the $c_x$-constrained channel where joint fitting already has relief; and effective parameter dimensionality far below the nominal 26 (S10.3, cross-referenced to §S3.2).

- **The gap is accepted in exchange for a shared mechanistic interpretation.** Joint fitting enforces shared per-cell biochemistry, which is the foundation for interpreting $k_m$ and $t_m$ as busulfan modifiers and for treating the joint baseline as a single mechanistic model rather than two parallel parametrisations (S10.4). Single-parameter group-specific extensions were tested as alternatives and rejected (S10.5).

This trade-off is a deliberate methodological position of the manuscript: a model that fits less perfectly in Group II but supports a consistent mechanistic claim for both groups is preferred over a model that fits each group in isolation but cannot say what changed between them.
