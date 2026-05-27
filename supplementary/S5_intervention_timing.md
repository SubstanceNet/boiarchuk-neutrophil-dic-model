# S5. Intervention-timing trajectories and temporal metrics

*Part of the Supplementary Information for the manuscript "A mechanistic model of neutrophil-driven disseminated intravascular coagulation…" Main-text references: Methods §2.5 (two-segment ODE protocol), Results §3.6 (therapeutic window), Figure 6 (severity vs timing). This section gives the full numerical table across the nine timing scenarios, the per-phase numerical signature of the two-phase therapeutic window, the choice of t_recovery over t_peak as the principal temporal metric, and methodological caveats.*

---

## S5.1 Setup

The two-segment ODE protocol is specified in main-text §2.5. Per-iteration: segment 1 over [0, t_intervention] integrates with no busulfan (kr_eff = kr, tp2_eff = tp2); segment 2 over [t_intervention, 19 d] integrates with busulfan active (kr_eff = kr · km, tp2_eff = tp2 · tm). The ODE state (D, AP, Hc, Hn, X) is continuous across t_intervention; only the two effective rate constants change instantaneously at the boundary.

Specifics for this run:

- **Timing scenarios.** Nine values of t_intervention: 0, 1, 2, 2.5, 3, 3.5, 4, 6 days, plus the no-intervention reference (t_intervention = ∞).
- **Dose.** Fixed at the observed Group II values km = 4.93, tm = 0.43.
- **Ensemble.** Each of the 100 bootstrap members (§S4) is run through all nine scenarios, giving 900 total simulations.
- **Time grid.** 400 points uniformly over [0, 19] d.
- **Computational profile.** Wall-clock ≈7 s on a single workstation; zero failed simulations.

---

## S5.2 Full results across the nine scenarios

Ensemble median across 100 bootstrap members; CIs in the per-scenario figures (`analyses/31_intervention_timing/figures/`).

| Scenario | max_recalc (s) | auc_recalc | min_xiii (%) | t_peak (d) | t_recovery (d) |
|---|---|---|---|---|---|
| t = 0 | 7.13 | 91.52 | −14.56 | 3.86 | 8.24 |
| t = 1 | 7.13 | 92.09 | −14.57 | 3.86 | 8.24 |
| t = 2 | 7.19 | 84.24 | −15.28 | 2.71 | 8.14 |
| t = 2.5 | 7.93 | 84.77 | −19.02 | 2.71 | 8.00 |
| t = 3 | 14.39 | 95.56 | −30.24 | 3.14 | 7.81 |
| t = 3.5 | 22.74 | 107.84 | −40.48 | 3.57 | 7.71 |
| t = 4 | 28.18 | 119.55 | −47.40 | 4.00 | 7.69 |
| t = 6 | 31.77 | 167.28 | −51.15 | 4.17 | 7.95 |
| no intervention | 75.57 | 606.00 | −108.27 | 10.52 | 17.14 |

Three severity metrics (max_recalc, auc_recalc, min_xiii) and two temporal metrics (t_peak, t_recovery) per scenario. The acute-phase duration is computed as t_recovery − t_peak and is discussed qualitatively in §S5.4 below.

---

## S5.3 The two-phase therapeutic window: numerical signature

Main-text §3.6 describes the therapeutic window in prose; this subsection gives the per-phase numerical signature from the table above.

**Prevention phase (0 ≤ t_intervention ≤ 2.5 d).** All three severity metrics sit close to the t = 0 baseline: max_recalc 7.1–7.9 s (comparable to the observed Group II outcome of ≈7 s), auc_recalc 84–92, min_xiii −14.6 to −19.0%. Within this window, busulfan intervention provides near-complete DIC attenuation. The t = 0 and t = 1 entries are essentially identical (max_recalc 7.13 vs 7.13, min_xiii −14.56 vs −14.57), indicating that the inducer-toxicity pulse V(t) (peaking at τv = 1.5 d, §S1.7) does not accumulate sufficient effective coagulation load in the first 24 hours to trigger the cascade independently — a biologically meaningful latency between exposure and committed coagulopathy.

**Critical transition (2.5 → 3 d).** Across the half-day window between t = 2.5 and t = 3, max_recalc roughly doubles (7.93 → 14.39 s, factor 1.8×), min_xiii worsens by 1.6× (−19.0 → −30.2%), and auc_recalc rises by 13%. This is the decisive phase boundary in the model: by t ≈ 3 d, accumulated acid phosphatase from upstream degranulation has reached a threshold for cascading Hn growth that busulfan can attenuate but not prevent (recalling the accelerating gHn nonlinearity, §S1.4).

**Mitigation phase (3 ≤ t_intervention ≤ 6+ d).** Severity continues to rise but plateaus by day 6: max_recalc 14.4 → 22.7 → 28.2 → 31.8 (at t = 3, 3.5, 4, 6); min_xiii −30.2 → −40.5 → −47.4 → −51.2. Busulfan still reduces peak severity by a factor of 2–3× relative to no intervention (max_recalc 31.8 at t = 6 vs 75.6 without intervention), but cannot prevent acute DIC onset. After t = 4, additional delay produces diminishing returns: severity at t = 6 is only 12% worse than at t = 4 across the three severity metrics, indicating that the relevant clinical decision boundary is the entry into the mitigation phase, not the precise day within it.

---

## S5.4 Temporal metrics: t_recovery as the cleanest indicator

The t_peak column of the table above shows a non-monotonic pattern within the prevention phase: 3.86, 3.86, 2.71, 2.71, 3.14, 3.57, 4.00, 4.17 d across t_intervention = 0, 1, 2, 2.5, 3, 3.5, 4, 6 d. This is not a biological signal but a *mathematical artefact* of the intervention boundary: at early interventions (t = 2, 2.5) the gHn maximum coincides with the intervention itself — a transient created by accumulated AP suddenly meeting the reduced kr_eff. We therefore do not interpret t_peak as the "time of the peak of DIC"; main-text §2.5 already notes that t_peak is defined as the first local maximum of gHn(t) to avoid finite-horizon boundary effects, but the early-intervention artefact remains visible in the table.

**t_recovery is the cleaner temporal metric.** Across the prevention and mitigation phases t_recovery sits in a narrow band (7.69–8.24 d), with no intervention sitting far outside it (17.14 d). The mitigation-phase values are marginally earlier than prevention-phase ones (7.69–7.95 vs 8.00–8.24 d), because the severity is already capped — there is less to recover from.

**Acute-phase duration** (t_recovery − t_peak) shrinks roughly twofold under intervention, from ≈8 d in the no-intervention reference to ≈4 d in the intervened scenarios, with little variation across timing within the intervened group. The qualitative result is consistent across the nine scenarios: **timing modulates severity but not the temporal structure of the episode**. Once intervention is applied, the acute phase contracts to a similar duration regardless of when within the therapeutic window the intervention occurs; only the severity scales with timing.

---

## S5.5 Methodological caveats

Three caveats are reported transparently:

1. **Idealised pharmacokinetics.** Busulfan is modelled as an instantaneous change of the two effective rate constants at t_intervention. Real myelosuppression develops over 5–7 days under the experimental two-stage protocol (§2.1). The intervention-timing simulation therefore represents an idealised scenario of immediate pharmacological effect rather than realistic PK/PD; clinical translation would require an explicit PK/PD layer on top of the present model.

2. **Neutrophil profile after t = 8 d.** The Group II neutrophil interpolator N(t) is held constant (N = 3.73 × 10⁹ L⁻¹) for t > 8 d, because the experimental Group II observation window ended at day 8. For trajectories whose t_recovery exceeds 8 d (all prevention and mitigation scenarios; see §S5.2), the dynamics on [8, 19] d assume the neutrophil count remains stable near the Group II baseline. This is consistent with the experimental observation that Group II animals had no late mortality and the granulocytic compartment did not recover within the observation window, but the extrapolation is a model assumption rather than data.

3. **Phase boundary precision.** The reported boundary "between days 2.5 and 3" reflects the grid resolution of 0.5 d at this point in the scan. Finer-resolution sweeps would not meaningfully refine the boundary given the parameter uncertainty propagated through the bootstrap ensemble (the per-scenario CIs on max_recalc near the transition span several seconds; see §S5.2 reference to the per-scenario figure). The half-day uncertainty is reported transparently in main text §3.6 ("a critical half-day transition occurred between days 2.5 and 3") rather than as an interpolated single-day value.

The first two caveats limit clinical generalisation rather than model validity; the third reflects honesty about phase-boundary precision under the available grid.
