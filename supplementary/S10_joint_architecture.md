# S10. Shared Architecture Versus Group-II-Only

*Part of the Supplementary Information for Boiarchuk & Onasenko (2026). Cross-references from the main text: §2.3 (the architectural penalty on Group II fit quality; quantified in §S2.7 as an $\approx 14$ percentage-point gap concentrated almost entirely in the structurally under-determined factor XIII channel, architectural rather than due to overfitting). Related appendices: §S1.9 (24-shared + 2-modifier architecture), §S2.7 (architecture pointer in the estimation appendix), §S3.2 (parameter identifiability), §S9 ($c_x \leq 600$ bound on the factor XIII sloppy direction).*

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
| recalc | +0.9068 | +0.9013 | −0.0055 |
| thrombin | +0.9468 | +0.9936 | +0.0468 |
| fib | +0.4977 | +0.5778 | +0.0801 |
| xiii | +0.0772 | +0.7980 | +0.7208 |
| AP | +0.9638 | +0.9283 | −0.0355 |
| D | +0.7594 | +0.8191 | +0.0597 |
| **mean** | **+0.6920** | **+0.8363** | **+0.1444** |

The mean improvement $\Delta \approx 0.144$ is the **$\approx 14$ percentage points** figure quantified in §S2.7 (referenced from main text §2.3). Reading the columns:

- The gap is dominated by a single channel: **factor XIII** ($\Delta = +0.72$), where joint fitting reaches only $R^2 = 0.077$ — consistent with the bootstrap median $R^2_{\text{G2}}(\text{XIII}) = 0.075$ (§S4.3).
- Across the other five observables the mean $\Delta$ is only **+0.03**; two of them (**recalcification** and **acid phosphatase**) are fit marginally better under joint fitting ($\Delta < 0$).
- The separate-fit advantage is therefore not a diffuse, multi-channel improvement, but rather a nearly isolated recovery of the factor XIII channel.

---

## S10.3 Why architectural, not overfitting

The data-to-parameter ratio of 2.08 (S10.1) is low enough that the separate fit could in principle exploit additional freedom to overfit the 54 Group II data points. Three independent observations argue against this and in favour of the *architectural* interpretation — that the joint fit is genuinely over-constrained to capture Group II dynamics, and the separate-fit advantage reflects relief of this constraint rather than spurious parameter oscillation.

**Argument 1 — the gap is isolated to a single, independently under-determined channel.** Across five of the six observables, joint and separate fitting are comparable: the mean $\Delta$ over {recalcification, thrombin, fibrinogen, acid phosphatase, degranulation} is only +0.03, and two of these channels (recalcification, acid phosphatase) are fit marginally better under joint fitting. The 14 pp mean gap is carried almost entirely by factor XIII ($\Delta = +0.72$), where joint fitting reaches only $R^2 = 0.077$ — consistent with the bootstrap median $R^2_{\text{G2}}(\text{XIII}) = 0.075$ (§S4.3). Overfitting would relieve the joint constraint diffusely, or on whichever channels offered the most free residual; instead the separate fit recovers exactly the one channel that joint fitting structurally cannot pin down, leaving the other five essentially unchanged.

**Argument 2 — the factor XIII deficit is structural, and decomposes into two verified sources.** The factor XIII channel is governed by a four-parameter sloppy direction $\{a_x, c_x, b_x, k_x\}$ (§S3.2, §S9), and the gap on it decomposes cleanly between the separate fit ($R^2_{\text{G2}} = 0.80$) and the production joint baseline (0.077). Removing the mechanism-split prior alone recovers the channel only to 0.276 — a $-0.20$ contribution from $W_{\text{SPLIT}} = 2.0$ — while the larger $-0.52$ drop is the cost of architecture-sharing itself: the shared parameters $\{a_x, c_x, b_x, k_x\}$ are dominated by the strong Group I factor XIII signal and lie poorly on the near-flat Group II trajectory. That this under-determination is structural rather than a scale-factor artefact is confirmed directly — under per-group standard-deviation normalisation the fraction of negative $R^2_{\text{G2}}(\text{XIII})$ rises to 83%, not falls (§S4, analysis 34). The separate fit's recovery of this channel therefore reflects genuine relief of a structural constraint, not parameter fishing.

**Argument 3 — effective dimensionality far below 26.** The data-to-parameter ratio of 2.08 uses the nominal parameter count. Profile likelihood analysis (§S3.2) classifies the 26 parameters as 6 well-identified, 5 weakly identified, 12 sloppy, and 3 grid-truncated. The sloppy and grid-truncated categories contribute very little to the effective fitting dimensionality: for the 12 sloppy parameters, cost changes less than 2% across the full $\pm 50\%$ grid, and the 3 grid-truncated simply cannot be assessed. The effective fitting dimensionality is therefore substantially below 26, and the *effective* data-to-parameter ratio is correspondingly more comfortable. A reader wanting the precise effective count can read it from Table S2 and the §S3.2 classification; the qualitative point is that the nominal-26 overstates the model's flexibility.

Together the three arguments support the architectural interpretation. The separate-fit advantage is genuine constraint relief, not a parameter-fishing artefact.

---

## S10.4 What the gap means

The shared architecture forces both groups to share 24 of 26 parameters: degranulation kinetics ($k_d, k_{rl}, k_{cl}$), neutrophil-derived pool kinetics ($k_{na}, k_{nd}, H_m$), four factor XIII channel parameters ($a_x, c_x, b_x, k_x$), inducer impulse parameters ($k_{ca}, k_{cd}$ in S1.7 plus $a_2, s_2, t_{p2}$), and all nine algebraic observable coefficients ($a_r, b_r, c_r, a_t, b_t, a_f, b_f, c_f, d_f$). Only two parameters — $k_m$ and $t_m$ — are group-specific (§S1.9). This shared parametrisation encodes the biological hypothesis that busulfan modifies the *kinetics and timing* of the neutrophil compartment ($k_m$, $t_m$) without altering its *per-cell biochemistry* (everything else shared).

The 14 pp $R^2_{\text{G2}}$ gap is the cost of this hypothesis. Separate fitting, without shared parameters, achieves $\approx 0.84$ mean $R^2_{\text{G2}}$; the joint baseline achieves $\approx 0.69$. The difference is concentrated almost entirely in factor XIII (S10.3) and decomposes into a dominant architecture-sharing term ($\approx 0.52$ on that channel) and a smaller mechanism-prior term ($\approx 0.20$); it is the price paid for a single shared mechanistic parametrisation for both groups. This price is accepted because the mechanistic claims that follow — in particular the busulfan mechanism interpretation in §3.5 of the main text and the dose–response dependence in §S6, both of which rely on $k_m$ and $t_m$ meaning the same thing across groups — require a single shared per-cell biochemistry. A separate-fit parametrisation would give better Group II numbers but would not support a comparable claim about what *changed* between groups.

---

## S10.5 Failed single-parameter alternatives

It is natural to ask whether the gap could be narrowed by adding one or two group-specific parameters beyond $k_m$ and $t_m$ — selectively relieving the shared constraint on channels with the largest $\Delta$ (S10.2). Two such extensions were tested:

- **Group-specific $c_x$** (`analyses/07_groupspec_cx/`): allow $c_{x,\text{G1}}$ and $c_{x,\text{G2}}$ to differ. This is the most natural candidate, because the $c_x \leq 600$ prior already acts as a constraint relief for the factor XIII channel in joint fitting.

- **Group-specific $c_f$** (`analyses/08_groupspec_cf/`): allow $c_{f,\text{G1}}$ and $c_{f,\text{G2}}$ to differ. This addresses the fibrinogen channel, the largest of the small residual gaps outside factor XIII.

Both were rejected. The marginal improvement in $R^2_{\text{G2}}$ in each case was small (a few percentage points on average, sometimes concentrated in the factor XIII channel via regularisation rather than the target channel) and attributable to optimiser stabilisation — a side-effect of adding a degree of freedom — rather than genuine channel-specific relief. Neither extension closed the 14 pp gap; neither gave a consistent architectural improvement comparable to what the separate fit shows. The conclusion is that closing the gap would require an architectural redesign touching most channels simultaneously, not adding one or two group-specific parameters; such a redesign is beyond the scope of the present work and would change the central biological claim of the manuscript about shared per-cell biochemistry.

---

## S10.6 Conclusion

Three points close the justification for accepting the 14 pp gap:

- **The gap is quantified.** Mean $R^2_{\text{G2}} = 0.6920$ (joint) vs. 0.8363 (separate); $\Delta_{\text{mean}} = +0.1444$. The gap is concentrated almost entirely in factor XIII ($\Delta = +0.72$); across the other five observables the mean $\Delta$ is +0.03, two of them slightly favouring joint fitting (S10.2).

- **The gap is architectural, not overfitting.** Three independent arguments support this reading: the gap is isolated to a single channel (factor XIII) rather than diffuse across observables; that channel's under-determination is structural — decomposing into architecture-sharing ($\approx 0.52$) and the mechanism prior ($\approx 0.20$), and worsening rather than improving under per-group normalisation (§S4, analysis 34); and effective parameter dimensionality far below the nominal 26 (S10.3, cross-referenced to §S3.2).

- **The gap is accepted in exchange for a shared mechanistic interpretation.** Joint fitting enforces shared per-cell biochemistry, which is the foundation for interpreting $k_m$ and $t_m$ as busulfan modifiers and for treating the joint baseline as a single mechanistic model rather than two parallel parametrisations (S10.4). Single-parameter group-specific extensions were tested as alternatives and rejected (S10.5).

This trade-off is a deliberate methodological position of the manuscript: a model that fits less perfectly in Group II but supports a consistent mechanistic claim for both groups is preferred over a model that fits each group in isolation but cannot say what changed between them.
