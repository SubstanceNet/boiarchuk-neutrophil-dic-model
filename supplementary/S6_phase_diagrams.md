# S6. Phase Diagrams for Dose–Response Severity Metrics

*Part of the Supplementary Information for Boiarchuk & Onasenko (2026). Cross-references from the main text: §2.5 (dose–response protocol), §3.5 (± Figure 4 for three of four metrics; Figure 5 for the dose–response slice at observed timing). This appendix describes the dose–response setup with internal validation, each of the four valid severity metrics as a phase diagram on the $(k_m, t_m)$ grid, the reason why the fifth computed metric (time to $g_{Hn}$ peak) is not elevated to a figure, and documents the historical retraction of the sixth metric (liver\_collapse), recognised as invalid.*

---

## S6.1 Settings

The dose–response protocol is specified in §2.5 of the main text. Per cell: the Group II effective rate constants are redefined as $k_{r,G2} = k_r \cdot k_m$ and $t_{p2,G2} = t_{p2} \cdot t_m$; the Group II neutrophil profile $N(t)$ is preserved throughout (substitution of the Group I profile is a separate experiment, analysis 33, used for lethality validation in main text §3.4). For each of the 100 bootstrap ensemble members, the model is run on a $15 \times 15$ grid of $(k_m, t_m)$ values:

- $k_m \in [1.0, 10.0]$, 15 log-uniform values
- $t_m \in [0.2, 1.0]$, 15 log-uniform values

Total: 22,500 simulations, completed in approximately 2 minutes of wall-clock time with zero failed simulations.

Two reference points orient the phase diagrams. The point **$(k_m = 1, t_m = 1)$** corresponds to the no-kinetic-effect baseline: busulfan has not modified the rate constants relative to Group I. The point **$(k_m \approx 4.93, t_m \approx 0.43)$** is the Group II baseline — the fitted modifier values from the joint baseline (§S2.2, Table 1).

**Internal validation.** Before interpreting the phase diagrams, the model predictions at the Group II baseline cell were compared with the observed Group II values:

| **Metric** | **Observed** | **Model median** | **Model 95% CI** |
|---|---|---|---|
| max\_recalc (s) | 9.10 | 5.84 | [0.29, 13.04] |
| min\_xiii (%) | −9.30 | −11.80 | [−22.47, 0.00] |
| auc\_recalc | 70.55 | 82.78 | [66.91, 102.59] |

All three observed values fall within the model's 95% CI at the Group II baseline cell. The phase diagrams are therefore interpreted starting from a cell that the model reproduces correctly within bootstrap uncertainty.

These baseline-cell figures are produced by a dedicated, reproducible script (`analyses/30_myelosan_dose/g2_baseline_validation.py`): it computes the observed values (9.10, −9.30, 70.55) directly from the Group II data and the model predictions at the exact fitted dose $(k_m = 4.93, t_m = 0.43)$ through the ensemble, recovering the tabulated model median for max\_recalc (5.84 s on the good-basin subset) and the other two metrics to within grid resolution. (The somewhat higher Group II baseline value quoted in main-text Table 3, ≈ 6.6–7 s, is the corresponding median over the full 100-member ensemble; the small difference between the two reflects the good-basin-versus-full-ensemble distinction together with grid resolution.)

---

## S6.2 Four valid severity metrics

### S6.2.1 max\_recalc (peak hypocoagulation)

Shown in main text, Figure 4, panel (a). Across the $(k_m, t_m)$ grid, the median surface decreases monotonically both with increasing $k_m$ (stronger rate suppression) and with decreasing $t_m$ (compressed inflammatory peak time). At the no-kinetic-effect corner ($k_m = 1$, $t_m = 1$), the median is $\approx 41.6$ s; at the Group II baseline ($k_m \approx 4.93$, $t_m \approx 0.43$) — $\approx 5.8$ s, a 7-fold reduction. The 10-s contour marked on the figure defines the approximate boundary of the protected region; cells inside this contour yield outcomes comparable to Group II. Sensitivity to $t_m$ is highest at low $k_m$ (where rate suppression is weak and time compression is the main protective lever); at high $k_m$ the surface is dominated by the $k_m$ axis.

### S6.2.2 min\_xiii (factor XIII nadir)

Shown in main text, Figure 4, panel (b). Topology mirrors max\_recalc but with different scaling: at $k_m = 1$, $t_m = 1$, the median nadir is approximately $-52.5\%$, and at the Group II baseline $-11.8\%$ — a 4.5-fold reduction. The factor XIII channel is structurally under-determined in the bootstrap (§S4.3: 41% of iterations have $R^2_{\text{G2}}(\text{XIII}) < 0$), which widens per-cell CIs in the low-severity region, but the median surface itself is smooth and monotone across the grid.

### S6.2.3 max\_gHn (peak effective coagulation load)

Shown in main text, Figure 4, panel (c). $g_{Hn}$ is the nonlinear amplification of the neutrophil-derived coagulation pool (§S1.4); it sits between the state vector and the observable equations with no observable-specific coefficients in between. The phase diagram is therefore a direct proxy of the *cascade load* the model predicts in each $(k_m, t_m)$ cell, decoupled from the algebraic observable coefficients ($a_r, b_r, a_t, b_t, a_f, b_f, c_f, d_f, c_r$). Topology closely mirrors max\_recalc — unsurprisingly, since max\_recalc has $g_{Hn}$ as its dominant late-phase term — but the $g_{Hn}$ surface is structurally cleaner because fewer parameters mediate it.

### S6.2.4 auc\_recalc (integrated coagulation disturbance)

**Not shown in main text, Figure 4**; an additional metric completing the dose–response picture. auc\_recalc is the trapezoidal integral of $|\Delta\text{recalc}(t)|$ over the Group II evaluation grid $[0, 9]\;\text{d}$. At $k_m = 1$, $t_m = 1$, the median is $\approx 206$; at the Group II baseline $\approx 83$ — a 2.5-fold reduction, smaller than the 7-fold reduction in max\_recalc.

The smaller AUC reduction relative to the peak reduction is mechanistically informative. AUC integrates not only peak height but also episode duration, so a configuration that lowers the peak while prolonging recovery contributes less AUC reduction than peak reduction. The contrast between this 7-fold peak reduction and the 2.5-fold AUC reduction captures exactly this difference: busulfan compresses the peak more than it shortens the episode. (The main-text §3.5 headline of ≈**6-fold** for the peak refers to the 2×2 *kinetic* effect at the Group II profile, §S6.5; the 7-fold here is the full-grid corner ratio.) We include auc\_recalc here because it is clinically intuitive (total burden per episode) and complements the peak-based picture of Figure 4.

---

## S6.3 Methodological note on time\_to\_peak\_gHn

A fifth metric, time\_to\_peak\_gHn, is computed during the dose–response scan but is *not* elevated to a phase diagram in this appendix. The reason is a boundary artefact in the Group II setup: at $k_m = 1$ (no kinetic effect), Group II trajectories show a slow secondary rise of $g_{Hn}$ between $t = 7$ and $t = 8$, which marginally exceeds the first peak. This is attributed to the flat extrapolation of the neutrophil interpolator $N(t)$ beyond the last Group II observation ($t = 8$, with $N$ held at $3.73 \times 10^9\;\text{L}^{-1}$ thereafter on the $0$–$9\;\text{d}$ grid). The argmax operation then selects the boundary, giving a misleading time-to-peak of 8 d.

A clean treatment of the peak time requires a time-dependent $N(t)$ across the full 0–19 d horizon; this is the protocol of the *timing-of-intervention experiment* (analysis 31, §S5), whose temporal metrics supersede the dose–response time-to-peak values. The raw JSON `phase_diagram_time_to_peak_gHn` is preserved in the repository for reference but is not elevated to a figure.

---

## S6.4 Retraction of the liver\_collapse metric

An earlier version of analysis 30 reported a sixth metric, **liver\_collapse**, defined as a binary indicator of whether the ratio $H_n / H_m$ exceeded 0.99 anywhere on the trajectory. The reported result — liver\_collapse occurred in *0 of 22,500 simulations* — was then interpreted as evidence that the Group II neutrophil profile alone is structurally insufficient to drive fatal DIC.

This claim is retracted. Two independent reasons, both verified directly in analysis 33:

- **Code error.** The severity-computation routine read `o["Hm"]` from the `solve_group` output, but `solve_group` does not place `"Hm"` in its output dictionary. Hence `Hm` was `None`, the collapse branch (`if Hm is not None`) never executed, and `liver_collapse = False` was returned unconditionally for all 22,500 simulations — regardless of neutrophils, dose, or dynamics. The "0" was 0 by construction, not by result.

- **Conceptually empty even when corrected.** The 0.99 threshold is structurally unreachable in any tested model configuration. In the Group II baseline configuration with the preserved neutrophil profile — the one in which analysis 30 operates — $H_n/H_m$ reaches only $\approx 0.35$ (max across 100 bootstrap members), an order of magnitude below the threshold. In the pure Group I configuration (analysis 33), $H_n/H_m$ reaches $\approx 0.75$, but no ensemble member crosses 0.99. The retraction therefore stands even for the more severe Group I dynamics, where the $g_{Hn}$ nonlinearity is most active.

The metric has been removed from `analyses/30_myelosan_dose/run.py`. Lethality validation now rests on **hypocoagulation severity**, which is what the experimental endpoint actually measured (animals died at the peak of hypocoagulation, days 10–12, not at any abstract saturation threshold). Analysis 33 runs the joint model v13 in the pure Group I configuration (Group I neutrophil profile, no busulfan modifiers) through the same 100-member bootstrap ensemble and obtains max\_recalc $\approx 147$ s for Group I vs. $\approx 7$ s for the Group II baseline — a 21-fold separation, with the peak on day 11 (matching the observed lethality window) and factor XIII and fibrinogen nadirs reproduced to within 1–11% of observation. This validation is reported in main text §3.4 and Table 3.

We document the retraction transparently here, because it was discovered during internal methodological review rather than raised in peer review; readers encountering the earlier "0 of 22,500" claim in pre-archive drafts should treat it as retracted. The four severity metrics in §S6.2 are unaffected by the error and remain the production metrics for the dose–response experiment.

---

## S6.5 Decomposition of the protective effect: count versus kinetics

The dose–response phase diagrams above isolate the *kinetic* axis: the Group II neutrophil profile is preserved throughout, so the severity gradient reflects the $k_m, t_m$ modifiers only. To attribute the full Group I → Group II protection between its two routes — the reduction in neutrophil **count** (encoded in the profile $N(t)$) and the **kinetic** modification ($k_m, t_m$) — we evaluate all four cells of a $2 \times 2$ design, crossing the neutrophil profile (Group I vs. Group II) with the kinetic modifier (off, $k_m = t_m = 1$, vs. on, the fitted $k_m, t_m$ applied per ensemble member). The script is `decompose_2x2.py` (built on analysis 33). Values are median `max_recalc` (s) over the good-basin subset (consistent with §S6.1 and main-text §3.5):

| **Neutrophil profile** | **Kinetics off** ($k_m=t_m=1$) | **Kinetics on** (fitted) |
|---|---|---|
| **Group I** (high count) | [A] 150.8 | [B] 39.6 |
| **Group II** (low count) | [C] 44.5 | [D] 7.1 |

Each route is defined by varying one axis with the other held fixed, which gives two conditional values per route (the difference between them is the interaction):

| **Route** | **Conditional factor 1** | **Conditional factor 2** | **Main effect** (geom. mean) |
|---|---|---|---|
| Kinetic modification | $[A]/[B]=3.8\times$ (Group I profile) | $[C]/[D]=6.3\times$ (Group II profile) | $\approx 4.9\times$ |
| Count reduction | $[A]/[C]=3.4\times$ (kinetics off) | $[B]/[D]=5.6\times$ (kinetics on) | $\approx 4.3\times$ |

Three points follow. **(i)** Taken in isolation from the unsuppressed baseline [A], the two routes are of comparable magnitude: kinetic modification alone reaches cell [B] (3.8-fold) and count reduction alone reaches cell [C] (3.4-fold) — note that [B] and [C] are nearly equal. **(ii)** The two routes combine to the full $[A]/[D] \approx 21\times$ separation through a positive interaction: the route applied *second* contributes a larger factor (5.6–6.3×) than the same route applied first (3.4–3.8×), because the $g_{Hn}$ nonlinearity makes each route more effective once the other is in place. The decomposition is therefore path-dependent and approximately multiplicative ($3.8 \times 5.6 \approx 21$; $3.4 \times 6.3 \approx 21$). **(iii)** By the symmetric main-effect measure, the kinetic contribution ($\approx 4.9\times$) is marginally larger than the count contribution ($\approx 4.3\times$), but the two are comparable and **neither dominates**.

This is the quantitative basis for the statement in main-text §3.5 that busulfan acts through *both* routes. It also shows that the earlier informal reading of the $\approx 22\times$ contrast as "predominantly count" is not supported: the count reduction alone accounts for only $\approx 3.4\times$ of the separation. The full-ensemble run (100 members) gives the same qualitative picture (kinetic main effect $\approx 4.9\times$, count $\approx 4.4\times$). The earlier reading arose from comparing the pure Group I cell [A] directly with the Group II baseline [D], a single comparison that changes both axes at once and so cannot separate the two routes.
