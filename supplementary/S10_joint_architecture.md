# S10. Joint vs Group-II-only architecture

*Part of the Supplementary Information. Main-text reference: Methods §2.3 ("a separate Group-II-only fit attained roughly 22 percentage points higher mean Group II R² than the joint fit (Supplementary Methods), a gap that is largely architectural rather than attributable to overfitting"). Related sections: §S1.9 (the 24-shared + 2-modifier architecture), §S2.7 (architecture pointer in the parameter-estimation appendix), §S3.2 (parameter identifiability), §S9 (the cx ≤ 600 bound that already partially relieves the XIII channel).*

---

## S10.1 Setup

To quantify the architectural cost of the joint cost function (§S2.1, §S1.9), we ran a *separate* Group II-only fit and compared its per-observable Group II R² to the joint baseline.

The separate fit retains:

- All 26 parameters of the joint model.
- The same per-observable scale factors SC_k (range-based) for Group II residuals.
- The Hn-saturation penalty J_Hn as a numerical guard.

The separate fit removes:

- The Group I contribution to the cost (W_GROUP_G1 = 0).
- The mechanism-split penalty W_SPLIT · J_split, which constrains Group I day-2 fractions and is irrelevant when Group I is not being fit.

Other settings:

- Single seed (42), quick-mode pipeline (DE popsize 8, maxiter 120, plus the standard NM → Powell → NM polish from §S2.3).
- Source: `analyses/03_separate_g2_fit/`.
- Wall-clock: 510 s.

The separate fit has **54 Group II datapoints (9 timepoints × 6 observables) against 26 free parameters**, a data-to-parameter ratio of 2.08. This is low and raises a formal overfitting concern; the analysis below addresses it explicitly in S10.3.

---

## S10.2 Per-observable comparison

Per-observable Group II R² at the joint baseline (seed 42, §S2.5 / Table S2) and at the separate fit (analysis 03):

| Observable | Joint-fit R²_G2 | Separate-fit R²_G2 | Δ (sep − joint) |
|---|---|---|---|
| recalc | +0.6841 | +0.9013 | +0.2172 |
| thrombin | +0.8347 | +0.9936 | +0.1589 |
| fib | +0.2931 | +0.5778 | +0.2847 |
| xiii | +0.7277 | +0.7980 | +0.0703 |
| AP | +0.6777 | +0.9283 | +0.2506 |
| D | +0.5051 | +0.8191 | +0.3140 |
| **mean** | **+0.6204** | **+0.8363** | **+0.2160** |

The average improvement Δ ≈ 0.216 is the **≈22 percentage points** figure quoted in main-text §2.3. Reading the columns:

- All six observables improve under the separate fit; Δ is positive everywhere.
- The largest Δ are on **degranulation index (+0.314), fibrinogen (+0.285), and acid phosphatase (+0.251)**.
- The smallest Δ is on **factor XIII (+0.070)**, the channel that is already partially relieved at the joint baseline by the cx ≤ 600 structural prior (§S9).
- Recalcification and thrombin show intermediate Δ (+0.217 and +0.159).

---

## S10.3 Why architectural, not overfitting

The data-to-parameter ratio of 2.08 (S10.1) is low enough that the separate fit could in principle be exploiting the extra freedom to overfit the 54 Group II datapoints. Three independent observations argue against this and in favour of an *architectural* interpretation — namely, that the joint fit is genuinely too constrained to capture Group II dynamics, and the separate fit's advantage reflects the relief of that constraint rather than spurious wiggling.

**Argument 1 — uniformity across observables.** A pure-overfitting advantage would have a spiky per-observable signature: very high R² on a few channels where the 26 parameters happen to fit a particular sequence of timepoints, modest improvement elsewhere. The observed pattern is the opposite: all six observables improve together, with Δ spanning a narrow range [0.070, 0.314] around a mean of 0.216. Coherent improvement across all six channels is the signature of an architectural constraint being lifted, not of parameter wiggling.

**Argument 2 — the smallest gap is on the cx-constrained channel.** Factor XIII has the smallest Δ (+0.070), notably smaller than the others. This is exactly what the architectural interpretation predicts: the cx ≤ 600 prior (§S9) already relieves the joint architecture on the XIII channel — it gives the joint fit access to the same parameter subspace the separate fit explores. The other five channels have no such prior and remain fully constrained under joint fitting. The Δ pattern (large on uncontrained channels, small on the cx-relieved channel) is mechanism-consistent with architectural constraint relief; it has no natural reading under pure overfitting.

**Argument 3 — effective dimensionality is much lower than 26.** The 2.08 data-to-parameter ratio uses the nominal parameter count. The profile-likelihood analysis (§S3.2) classifies the 26 parameters as 6 well-identified, 5 weakly identified, 12 sloppy, and 3 grid-truncated. The 12 sloppy parameters and the 3 grid-truncated ones contribute very little to the effective fit dimensionality — cost varies by less than 2% across the entire ±50% grid for the 12 sloppy parameters, and the grid-truncated parameters cannot be assessed at all. The effective fit dimensionality is therefore substantially below 26, and the *effective* data-to-parameter ratio is correspondingly more comfortable. The reader who wants an exact effective count can read it off Table S2 and the §S3.2 classification; the qualitative argument is that nominal-26 overstates the model's flexibility.

Together, the three arguments support the architectural interpretation. The separate fit's advantage is genuine relief of a constraint imposed by joint fitting, not a parameter-fishing artefact.

---

## S10.4 What the gap means

The joint architecture forces both groups to share 24 of 26 parameters: the degranulation kinetics (kd, krl, kcl), the neutrophil-derived pool kinetics (kna, knd, Hm), the four XIII-channel parameters (ax, cx, bx, kx), the inducer-pulse parameters (kca, k_cd in S1.7 plus a2, s2, tp2), and all nine algebraic-observable coefficients (ar, br, cr, at, bt, af, bf, cf, df). Only two parameters — km and tm — are group-specific (§S1.9). This shared parameterisation encodes the biological hypothesis that busulfan modifies the *kinetics and timing* of the neutrophil compartment (km, tm) without altering its *per-cell biochemistry* (everything else shared).

The 22 pp R²_G2 gap is the cost of this hypothesis. The separate fit, with no shared parameters, would attain ≈0.84 mean R²_G2; the joint fit attains ≈0.62; the difference is the price paid for joint mechanistic interpretation. The price is accepted because the mechanistic claims that follow — in particular the busulfan-mechanism interpretation in main-text §3.5 and the dose-response in §S6, both of which rest on km and tm having the same meaning across groups — require a single shared per-cell biochemistry. A separate-fit parameterisation would give better G2 numbers but no comparable claim to make about *what changed* between the groups.

---

## S10.5 Failed single-parameter alternatives

It is natural to ask whether the gap could be narrowed by adding one or two group-specific parameters beyond km and tm — selectively relieving the joint constraint on the channels with the largest Δ (S10.2). Two such interventions were tested:

- **Group-specific cx** (`analyses/07_groupspec_cx/`): allow cx_G1 and cx_G2 to differ. This is the most natural candidate because the cx ≤ 600 prior already acts as an XIII-channel relief in the joint fit.
- **Group-specific cf** (`analyses/08_groupspec_cf/`): allow cf_G1 and cf_G2 to differ. This addresses the largest individual Δ outside the degranulation index, namely fibrinogen.

Both were rejected. The marginal R²_G2 improvement in each case was small (a few percentage points on average, sometimes concentrated in the XIII channel via regularisation rather than the targeted channel) and attributable to optimiser stabilisation — a side effect of adding a degree of freedom — rather than to genuine channel-specific relief. Neither extension closed the 22 pp gap; neither produced a coherent architectural improvement comparable to what the separate fit shows. The conclusion is that closing the gap would require an architectural redesign affecting most channels at once, not the addition of one or two group-specific parameters; that redesign is beyond the scope of the present work and would change the manuscript's central biological claim about shared per-cell biochemistry.

---

## S10.6 Conclusion

Three points close the case for accepting the 22 pp gap:

1. **The gap is quantified.** Mean R²_G2 = 0.6204 (joint) vs 0.8363 (separate); Δ_mean = +0.2160. All six observables improve under the separate fit, with Δ in [0.070, 0.314] (S10.2).

2. **The gap is architectural, not overfitting.** Three independent arguments support this reading: per-observable uniformity rather than spiky improvement; smallest Δ on the cx-constrained channel where the joint fit already has relief; effective parameter dimensionality much lower than the nominal 26 (S10.3, with cross-reference to §S3.2).

3. **The gap is accepted in exchange for joint mechanistic interpretation.** Joint fitting forces shared per-cell biochemistry, which is the basis for interpreting km, tm as the busulfan modifiers and for treating the joint baseline as a single mechanistic model rather than two parallel parameterisations (S10.4). Single-parameter group-specific extensions were tested as alternatives and rejected (S10.5).

This trade-off is the manuscript's deliberate methodological position: a model that fits less perfectly in Group II but supports a coherent mechanistic claim across both groups is preferred to a model that fits each group well in isolation but cannot speak to the differences between them.
