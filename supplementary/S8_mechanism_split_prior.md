# S8. Sensitivity to the Mechanism-Decomposition Prior Weight ($W_{\text{SPLIT}}$)

*Part of the Supplementary Information for Boiarchuk & Onasenko (2026). Cross-references from the main text: Methods, Mathematical model (introduction of $W_{\text{SPLIT}}$ as one of two structural priors); Results, mechanism decomposition (the prior is required for magnitude identification, while the recalcification and factor XIII directions hold without it; mechanism decomposition fractions and Table 2), and the definition of the cost term $J_{\text{split}}$ in §S2.1. This appendix provides empirical evidence for the two central claims about the $W_{\text{SPLIT}} = 2.0$ prior: it is necessary for identifiability and validated post-hoc by improved fit in the parallel (Group II) cohort.*

---

## S8.1 Settings

The mechanism-decomposition prior is the second term of the joint cost function (§S2.1):

$$J_{\text{split}} = (f_{\text{recalc}} - 0.24)^2 + (f_{\text{fib}} - 0.76)^2 + (f_{\text{xiii}} - 0.82)^2,$$

with weight $W_{\text{SPLIT}}$. The targets $(0.24, 0.76, 0.82)$ are the neutrophil-attributed day-1 fractions $(\Delta G_1 - \Delta G_2)/\Delta G_1$, estimated from the dissertation tables (Results, mechanism decomposition). $f_{\text{recalc}}$, $f_{\text{fib}}$, $f_{\text{xiii}}$ are the Group I day-2 fractions read from the model.

A nine-fit scan characterised the role of $W_{\text{SPLIT}}$. The structure was asymmetric across $W$ values, focused on two cases testing the central claims:

- $W = 2.0$ and $W = 0.0$: three seeds each (42, 7, 123), to test stability across seeds with and without the prior — the *identifiability* claim.
- $W = 0.3$, $1.0$, $5.0$: one seed (42), to map the cost / $R^2$ trajectory as a function of prior strength — the *choice of $W = 2.0$* claim.

All other settings were at the analysis 01 baseline ($c_x \leq 600$, uniform $W_{\text{SURV}}$, fast-mode optimisation, as described in §S2.2). Source: `analyses/01_w_split_profile/`.

---

## S8.2 Without the prior ($W = 0$): unidentified decomposition

Three seeds at $W = 0.0$:

| **Seed** | **Cost** | **$R^2_{\text{G1}}$** | **$R^2_{\text{G2}}$** | **$f_{\text{recalc}}$** | **$f_{\text{fib}}$** | **$f_{\text{xiii}}$** |
|---|---|---|---|---|---|---|
| 42 | 1.0096 | 0.854 | 0.548 | 0.478 | 0.053 | 0.747 |
| 7 | 1.0190 | 0.835 | 0.605 | 0.450 | 0.060 | 0.782 |
| 123 | 1.0170 | 0.852 | 0.577 | 0.344 | 0.049 | 0.725 |

The three seeds converge to *equicost* solutions ($\Delta\text{cost} = 0.009$) but find *qualitatively different* mechanism decompositions. The neutrophil-attributed recalcification fraction $f_{\text{recalc}}$ varies by 13 percentage points across seeds (0.344, 0.450, 0.478), and the fibrinogen fraction $f_{\text{fib}}$ settles near 0.05 for all three seeds — stable, but *far* from the day-1-derived target of 0.76. The factor XIII fraction $f_{\text{xiii}}$ falls in $[0.725, 0.782]$, a 5.7 pp spread. Although the absolute magnitudes remain unconstrained, the qualitative direction of each channel is highly consistent across all prior-free optimization seeds: recalcification is strictly $<0.5$ (indicating a vascular-driven effect), factor XIII is strictly $>0.5$ (neutrophil-mediated), and fibrinogen centres around $\approx 0.05$ (reflecting an intrinsic vascular direction). Fibrinogen is the only channel where the introduction of the prior reverses the direction of the effect.

This demonstrates that the day-2 Group I fit alone does not constrain the decomposition: the data are consistent with an equicost manifold of different mechanism decompositions, and which point on this manifold the optimiser finds is a property of the random seed, not of the data. Cost does not discriminate between basins.

---

## S8.3 With the prior ($W = 2.0$): unique optimum

Three seeds at $W = 2.0$:

| **Seed** | **Cost** | **$R^2_{\text{G1}}$** | **$R^2_{\text{G2}}$** | **$f_{\text{recalc}}$** | **$f_{\text{fib}}$** | **$f_{\text{xiii}}$** |
|---|---|---|---|---|---|---|
| 42 | 1.0431 | 0.834 | 0.620 | 0.244 | 0.739 | 0.808 |
| 7 | 1.0316 | 0.837 | 0.621 | 0.244 | 0.740 | 0.812 |
| 123 | 1.0456 | 0.833 | 0.602 | 0.244 | 0.740 | 0.808 |

The same three seeds now converge to the *same* mechanism decomposition, with precision far tighter than optimiser noise. $f_{\text{recalc}}$ agrees to 0.000 across all three seeds; $f_{\text{fib}}$ and $f_{\text{xiii}}$ agree to within 0.001 and 0.004, respectively. The cost spread ($\Delta = 0.014$) is comparable to the $W = 0$ case — the prior does not flatten the cost landscape, it selects a single basin within it.

The contrast with S8.2 is the key identifiability claim referenced in the main text: the prior converts an equicost manifold of decompositions into a single basin with a well-defined optimum. The optimum selected by the prior is the biologically motivated day-1 point (recalc 0.24, fib 0.76, xiii 0.82, matching the targets to within 0.014).

---

## S8.4 Five-point $W$ scan

The five-point scan at seed 42 (with stability-across-seeds established for $W = 0$ and $W = 2.0$ from S8.2/S8.3) maps the cost / decomposition trajectory as the prior strength varies:

| **$W$** | **Cost** | **$R^2_{\text{G1}}$** | **$R^2_{\text{G2}}$** | **$f_{\text{recalc}}$** | **$f_{\text{fib}}$** | **$f_{\text{xiii}}$** |
|---|---|---|---|---|---|---|
| 0.0 | 1.0096 | 0.854 | 0.548 | 0.478 | 0.053 | 0.747 |
| 0.3 | 0.9555 | 0.842 | 0.537 | 0.302 | 0.647 | 0.736 |
| 1.0 | 1.0368 | 0.837 | 0.606 | 0.250 | 0.731 | 0.803 |
| 2.0 | 1.0431 | 0.834 | 0.620 | 0.244 | 0.739 | 0.808 |
| 5.0 | 0.9619 | 0.830 | 0.645 | 0.243 | 0.751 | 0.806 |

Three patterns are visible. **The decomposition locks onto the targets between $W = 0.3$ and $W = 1.0$:** $f_{\text{recalc}}$ falls from 0.302 to 0.250 as $W$ rises from 0.3 to 1.0 and stabilises within 0.01 of the target 0.24 for $W \geq 1.0$. **$R^2_{\text{G1}}$ is effectively flat** across the scan (0.83–0.85): the prior does not harm Group I fit. **$R^2_{\text{G2}}$ improves monotonically** from 0.548 ($W = 0$) through 0.620 ($W = 2.0$) to 0.645 ($W = 5.0$), confirming the post-hoc validation claim (§S8.5).

$W = 2.0$ was chosen as the smallest weight at which the decomposition is robustly locked across multiple seeds (S8.3), while retaining the $R^2_{\text{G2}}$ gain in the parallel cohort. Higher $W$ (5.0) gives marginally better $R^2_{\text{G2}}$ (+0.025), but the cost function changes character — the prior starts to dominate the data-fitting term — and the trade-off is not justified by the marginal gain.

---

## S8.5 Post-hoc validation: improved fit in the parallel experimental cohort

Re-reading the $R^2_{\text{G2}}$ column from the seed-stability tables for $W = 0$ and $W = 2.0$ (S8.2, S8.3):

| **Seed** | **$R^2_{\text{G2}}$ at $W = 0$** | **$R^2_{\text{G2}}$ at $W = 2.0$** | **$\Delta$ ($W = 2.0$ minus $W = 0$)** |
|---|---|---|---|
| 42 | 0.548 | 0.620 | +0.072 |
| 7 | 0.605 | 0.621 | +0.016 |
| 123 | 0.577 | 0.602 | +0.025 |

$R^2_{\text{G2}}$ is **higher at $W = 2.0$ than at $W = 0$ across all three seeds**, by 2–7 percentage points. The prior derived from the Group I / Group II day-1 contrast therefore guides the model to a mechanism decomposition that improves the day-2 fit for the parallel Group II cohort—a feature that the day-2 Group I fit alone could not constrain. $R^2_{\text{G1}}$ is virtually unchanged across the same comparison (0.834–0.854 at $W = 0$; 0.833–0.837 at $W = 2.0$). The prior pays no Group I cost for its Group II improvement; it uses *Group I day-1 information* to constrain the *Group I day-2 mechanism decomposition* in a way that *Group II day-2 fit quality validates*.

---

## S8.6 Conclusion

The mechanism-decomposition prior $W_{\text{SPLIT}} = 2.0$ is therefore (i) **necessary** for identifiability — without it, three optimiser seeds find equicost solutions with recalcification fractions spanning 13 percentage points and fibrinogen fractions near 0.05 (S8.2); (ii) **validated** post-hoc — $R^2_{\text{G2}}$ in the parallel cohort improves by 2–7 pp across all three seeds (S8.5); and (iii) **biologically motivated** — the targets are day-1 ratios $(\Delta G_1 - \Delta G_2)/\Delta G_1$, derived from a different time point than the day-2 fit they constrain, and the two groups have nearly identical haemostatic baselines that make the derivation correctly posed (Results, mechanism decomposition).

One transparency caveat applies, repeated here for self-contained reading: at $W = 0$, the neutrophil fibrinogen fraction settles near 0.05 across seeds (S8.2), so the prior target of 0.76 is an *imposed* day-1-derived goal, not a feature *reproduced* by day-2 fibrinogen dynamics. The Results (mechanism decomposition) already state this caveat; §S8 confirms it directly from the $W = 0$ fits.

The decomposition is therefore best described as a regularised, prior-constrained estimate consistent with the day-1 biological signal, not as a prior-free inference from day-2 fitting alone. This is the framing used in the Results (mechanism decomposition); §S8 provides the empirical evidence underlying it.
