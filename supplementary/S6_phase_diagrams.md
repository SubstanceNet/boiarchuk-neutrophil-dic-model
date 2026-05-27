# S6. Phase diagrams for the dose-response severity metrics

*Part of the Supplementary Information for the manuscript "A mechanistic model of neutrophil-driven disseminated intravascular coagulation…" Main-text references: Methods §2.5 (dose-response protocol), Results §3.5 (± Figure 4 for three of the four metrics; Figure 5 for the dose-response slice at observed timing). This section gives the dose-response setup with internal validation, describes each of the four valid severity metrics as a phase diagram across the (km, tm) grid, explains why a fifth computed metric (time-to-peak gHn) was not promoted to a figure, and documents the historical retraction of a sixth metric (liver_collapse) that was later found to be invalid.*

---

## S6.1 Setup

The dose-response protocol is specified in main-text §2.5. Per-cell: the Group II effective rate constants are overridden as kr,G2 = kr · km and tp2,G2 = tp2 · tm; the Group II neutrophil profile N(t) is retained throughout (the substitution of the Group I profile is a separate experiment, analysis 33, used for the mortality validation in main-text §3.8). For each of 100 bootstrap ensemble members the model is run across a 15 × 15 grid of (km, tm) values:

- km ∈ [1.0, 10.0], log-spaced 15 values
- tm ∈ [0.2, 1.0], log-spaced 15 values

The total is 22,500 simulations, completed in approximately 2 minutes of wall-clock time with zero failed simulations.

Two reference points orient the phase diagrams. The point **(km = 1, tm = 1)** corresponds to the no-kinetic-effect baseline: busulfan has not modified the rate constants relative to Group I. The point **(km ≈ 4.93, tm ≈ 0.43)** is the Group II baseline — the fitted modifier values from the joint baseline (§S2.2, Table 1).

**Internal validation.** Before interpreting the phase diagrams, the model's prediction at the Group II baseline cell was compared with the observed Group II values:

| Metric | Observed | Model median | Model CI95 |
|---|---|---|---|
| max_recalc (s) | 9.10 | 5.84 | [0.29, 13.04] |
| min_xiii (%) | −9.30 | −11.80 | [−22.47, 0.00] |
| auc_recalc | 70.55 | 82.78 | [66.91, 102.59] |

All three observed values lie within the model CI95 at the Group II baseline cell. The phase diagrams are therefore interpreted starting from a cell that the model reproduces correctly within bootstrap uncertainty.

---

## S6.2 The four valid severity metrics

### S6.2.1 max_recalc (peak hypocoagulation)

Shown in main-text Figure 4 panel (a). Across the (km, tm) grid the median surface decreases monotonically with both increasing km (stronger rate suppression) and decreasing tm (compressed timing of the inflammatory peak). At the no-kinetic-effect corner (km = 1, tm = 1) the median is ≈41.6 s; at the Group II baseline (km ≈ 4.93, tm ≈ 0.43) it is ≈5.8 s — a 7-fold reduction. The 10-s contour, marked on the figure, defines the rough boundary of the protected region; cells inside this contour produce Group-II-like outcomes. Sensitivity to tm is highest at low km (where rate suppression is weak and timing compression is the main protective lever); at high km the surface is dominated by the km axis.

### S6.2.2 min_xiii (factor XIII nadir)

Shown in main-text Figure 4 panel (b). The topology mirrors max_recalc but with different scaling: at km = 1, tm = 1 the median nadir is approximately −52.5%, and at the Group II baseline −11.8% — a 4.5-fold reduction. The XIII channel is structurally under-determined under bootstrap (§S4.3: 41% of iterations have R²_G2(XIII) < 0), which widens the per-cell CIs in the low-severity region, but the median surface itself is smooth and monotonic across the grid.

### S6.2.3 max_gHn (peak effective coagulation load)

Shown in main-text Figure 4 panel (c). gHn is the nonlinear amplification of the neutrophil-derived coagulation pool (§S1.4); it sits between the state vector and the observable equations, with no observable-specific coefficients between it and the metric. The phase diagram therefore reads as a direct proxy for the *cascade load* the model predicts at each (km, tm) cell, decoupled from the algebraic observable coefficients (ar, br, at, bt, af, bf, cf, df, cr). The topology matches max_recalc closely — unsurprising, since max_recalc has gHn as its dominant late-phase term — but the gHn surface is structurally cleaner because fewer parameters mediate it.

### S6.2.4 auc_recalc (integrated coagulation disruption)

**Not shown in main-text Figure 4**; this is the additional metric S6 brings to the dose-response picture. auc_recalc is the trapezoidal integral of |Δrecalc(t)| over the Group II evaluation grid [0, 9] d. At km = 1, tm = 1 the median is ≈206; at the Group II baseline ≈83 — a 2.5-fold reduction, smaller than the 7-fold reduction in max_recalc.

The smaller AUC reduction relative to the peak reduction is mechanistically informative. AUC integrates not only the peak height but also the duration of disturbance, so a configuration that lowers the peak but lengthens the recovery contributes less reduction in AUC than in peak. The contrast between the 7-fold and 2.5-fold figures (main text §3.5) captures exactly this difference: busulfan compresses the peak more than it shortens the episode. We include auc_recalc here because it is clinically intuitive (total burden over the episode) and complements the peak-based view of Figure 4.

---

## S6.3 Methodological note on time_to_peak_gHn

A fifth metric, time_to_peak_gHn, was computed during the dose-response sweep but is *not* promoted to a phase diagram in this section. The reason is an edge artefact in the Group II setting: at km = 1 (no kinetic effect), Group II trajectories show a slow secondary rise of gHn between t = 7 and t = 8, slightly exceeding the first peak. This is attributable to constant extrapolation of the neutrophil interpolator N(t) beyond the last Group II observation (t = 8, with N held at 3.73 × 10⁹ L⁻¹ thereafter on the 0-9 d grid). The argmax operation then selects the boundary, producing a misleading time-to-peak of 8 d.

A clean treatment of intervention timing requires a time-dependent N(t) over the full 0-19 d horizon; this is the protocol of the *intervention-timing* experiment (analysis 31, §S5), whose temporal metrics supersede the analysis-30 time-to-peak values. The raw JSON of phase_diagram_time_to_peak_gHn is retained in the repository for reference but is not promoted to a figure.

---

## S6.4 Retraction of the liver_collapse metric

An earlier version of analysis 30 reported a sixth metric, **liver_collapse**, defined as a binary indicator of whether the Hn / Hm ratio exceeded 0.99 anywhere on the trajectory. The reported result was that liver_collapse occurred in *0 of 22,500 simulations*, which was interpreted at the time as evidence that the Group II neutrophil profile alone is structurally insufficient to drive fatal DIC.

That claim is retracted. Two independent reasons, both verified directly in analysis 33:

1. **Code bug.** The severity-computation routine read `o["Hm"]` from the `solve_group` output, but `solve_group` does not place `"Hm"` in its output dict. So `Hm` was `None`, the collapse branch (`if Hm is not None`) never executed, and `liver_collapse = False` was produced unconditionally for all 22,500 simulations — independent of neutrophils, dose, or dynamics. The "0" was 0 by construction, not a result.

2. **Conceptually empty even if fixed.** With Hm taken correctly from pv[7], Hn reaches only ≈1.15% of Hm across the realistic parameter range (max Hn ≈10.5 vs Hm ≈ 908 for a representative ensemble member). The 0.99 threshold is structurally unreachable, so even a correctly-coded liver_collapse metric would detect nothing.

The metric has been removed from `analyses/30_myelosan_dose/run.py`. The mortality validation now rests on **hypocoagulation severity**, which is what the experimental endpoint actually measured (animals died at the hypocoagulation peak, days 10-12, not at any abstract saturation threshold). Analysis 33 runs the joint v13 model in pure Group I configuration (Group I neutrophil profile, no busulfan modifiers) through the same 100-member bootstrap ensemble and obtains max_recalc ≈147 s for Group I versus ≈7 s for the Group II baseline — a 22-fold separation, with the peak occurring at day 11 (matching the observed mortality window) and the XIII and fibrinogen nadirs reproduced within 1-11% of observation. This validation is reported in main-text §3.8 and Table 4.

We document the retraction transparently here because it was discovered during internal methodological audit rather than raised in review; readers who encounter the earlier "0 of 22,500" statement in pre-archival drafts should treat it as withdrawn. The four severity metrics in §S6.2 are unaffected by the bug and remain the production metrics for the dose-response experiment.
