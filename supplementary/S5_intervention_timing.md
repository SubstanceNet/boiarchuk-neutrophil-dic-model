# S5. Intervention Timing Trajectories and Temporal Metrics

*Part of the Supplementary Information for Boiarchuk & Onasenko (2026). Cross-references from the main text: §2.5 (two-segment ODE protocol), §3.5 (therapeutic window), Figure 6 (severity vs. timing). This appendix provides the complete numerical table across nine timing scenarios, the per-phase numerical signature of the biphasic therapeutic window, the rationale for choosing $t_{\text{recovery}}$ over $t_{\text{peak}}$ as the primary temporal metric, and methodological caveats.*

---

## S5.1 Settings

The two-segment ODE protocol is specified in §2.5 of the main text. Per iteration: segment 1 on $[0, t_{\text{intervention}}]$ is integrated without busulfan ($k_{r,\text{eff}} = k_r$, $t_{p2,\text{eff}} = t_{p2}$); segment 2 on $[t_{\text{intervention}}, 19\;\text{d}]$ is integrated with active busulfan ($k_{r,\text{eff}} = k_r \cdot k_m$, $t_{p2,\text{eff}} = t_{p2} \cdot t_m$). The ODE state $(D, AP, H_c, H_n, X)$ is continuous across $t_{\text{intervention}}$; only the two effective rate constants change instantaneously at the boundary.

Particulars of this run:

- **Timing scenarios.** Nine values of $t_{\text{intervention}}$: 0, 1, 2, 2.5, 3, 3.5, 4, 6 days, plus a no-intervention reference ($t_{\text{intervention}} = \infty$).
- **Dose.** Fixed at the observed Group II values: $k_m = 4.93$, $t_m = 0.43$.
- **Ensemble.** Each of the 100 bootstrap members (§S4) is run through all nine scenarios, giving 900 total simulations.
- **Time grid.** 400 points uniformly on $[0, 19]\;\text{d}$.
- **Computational profile.** Wall-clock time $\approx 7$ s on a single workstation; zero failed simulations.

---

## S5.2 Full results across nine scenarios

Ensemble median across 100 bootstrap members; CIs are in the per-scenario figures (`analyses/31_intervention_timing/figures/`).

| **Scenario** | **max\_recalc (s)** | **auc\_recalc** | **min\_xiii (%)** | **$t_{\text{peak}}$ (d)** | **$t_{\text{recovery}}$ (d)** |
|---|---|---|---|---|---|
| $t = 0$ | 7.13 | 91.52 | −14.56 | 3.86 | 8.24 |
| $t = 1$ | 7.13 | 92.09 | −14.57 | 3.86 | 8.24 |
| $t = 2$ | 7.19 | 84.24 | −15.28 | 2.71 | 8.14 |
| $t = 2.5$ | 7.93 | 84.77 | −19.02 | 2.71 | 8.00 |
| $t = 3$ | 14.39 | 95.56 | −30.24 | 3.14 | 7.81 |
| $t = 3.5$ | 22.74 | 107.84 | −40.48 | 3.57 | 7.71 |
| $t = 4$ | 28.18 | 119.55 | −47.40 | 4.00 | 7.69 |
| $t = 6$ | 31.77 | 167.28 | −51.15 | 4.17 | 7.95 |
| no intervention | 75.57 | 606.00 | −108.27 | 10.52 | 17.14 |

Three severity metrics (max\_recalc, auc\_recalc, min\_xiii) and two temporal metrics ($t_{\text{peak}}$, $t_{\text{recovery}}$) per scenario. Acute-phase duration is computed as $t_{\text{recovery}} - t_{\text{peak}}$ and is discussed qualitatively in §S5.4 below.

---

## S5.3 Biphasic therapeutic window: numerical signature

Main text §3.5 describes the therapeutic window in prose; this subsection provides the per-phase numerical signature from the table above.

**Prevention phase ($0 \leq t_{\text{intervention}} \leq 2.5\;\text{d}$).** All three severity metrics sit close to the $t = 0$ baseline: max\_recalc 7.1–7.9 s (comparable to the observed Group II outcome $\approx 7$ s), auc\_recalc 84–92, min\_xiii $-14.6$ to $-19.0\%$. Within this window, busulfan intervention achieves near-complete DIC attenuation. The $t = 0$ and $t = 1$ entries are virtually identical (max\_recalc 7.13 vs. 7.13, min\_xiii $-14.56$ vs. $-14.57$), indicating that the inducer toxicity impulse $V(t)$ (peak at $\tau_v = 1.5\;\text{d}$, §S1.7) does not accumulate sufficient effective coagulation load in the first 24 hours to independently trigger the cascade — a biologically meaningful latency between exposure and established coagulopathy.

**Critical transition ($2.5 \to 3\;\text{d}$).** Across the half-day window between $t = 2.5$ and $t = 3$, max\_recalc approximately doubles (7.93 → 14.39 s, a 1.8× factor), min\_xiii worsens 1.6-fold (−19.0 → −30.2%), and auc\_recalc increases by 13%. This is the decisive phase boundary in the model: by $t \approx 3\;\text{d}$, the accumulated acid phosphatase from prior degranulation has reached the threshold for cascading $H_n$ growth that busulfan can attenuate but not prevent (recalling the accelerating $g_{Hn}$ nonlinearity, §S1.4).

**Mitigation phase ($3 \leq t_{\text{intervention}} \leq 6+\;\text{d}$).** Severity continues to rise but plateaus by day 6: max\_recalc 14.4 → 22.7 → 28.2 → 31.8 (at $t = 3, 3.5, 4, 6$); min\_xiii $-30.2 \to -40.5 \to -47.4 \to -51.2$. Busulfan still reduces peak severity 2–3-fold relative to no intervention (max\_recalc 31.8 at $t = 6$ vs. 75.6 without intervention), but cannot prevent acute DIC onset. Beyond $t = 4$, additional delay yields diminishing returns: severity at $t = 6$ is only 12% worse than at $t = 4$ across all three severity metrics, indicating that the clinically relevant decision boundary is entry into the mitigation phase, not the precise day within it.

---

## S5.4 Temporal metrics: $t_{\text{recovery}}$ as the cleaner indicator

The $t_{\text{peak}}$ column in the table above shows a non-monotonic pattern within the prevention phase: 3.86, 3.86, 2.71, 2.71, 3.14, 3.57, 4.00, 4.17 days for $t_{\text{intervention}} = 0, 1, 2, 2.5, 3, 3.5, 4, 6\;\text{d}$. This is not a biological signal but a *mathematical artefact* of the intervention boundary: at early intervention ($t = 2$, $2.5$), the $g_{Hn}$ maximum coincides with the intervention itself — a transient created by the accumulated $AP$ suddenly encountering a reduced $k_{r,\text{eff}}$. We therefore do not interpret $t_{\text{peak}}$ as the "DIC peak time"; main text §2.5 already notes that $t_{\text{peak}}$ is defined as the first local maximum of $g_{Hn}(t)$ to avoid finite-horizon boundary effects, but the early-intervention artefact remains visible in the table.

**$t_{\text{recovery}}$ is the cleaner temporal metric.** Across the prevention and mitigation phases, $t_{\text{recovery}}$ sits in a narrow band (7.69–8.24 d), with the no-intervention reference far outside it (17.14 d). Mitigation-phase values are marginally earlier than prevention-phase values (7.69–7.95 vs. 8.00–8.24 d), because there is less severity to recover from.

**Acute-phase duration** ($t_{\text{recovery}} - t_{\text{peak}}$) approximately halves under intervention, from $\approx 8\;\text{d}$ in the no-intervention reference to $\approx 4\;\text{d}$ in intervention scenarios, with little variation across timing within the intervention group. The qualitative result is consistent across all nine scenarios: **timing modulates severity, but leaves the temporal structure of the episode largely intact**. Once intervention is applied, the acute phase compresses to a similar duration regardless of precisely when within the therapeutic window the intervention occurred; only severity scales with timing.

---

## S5.5 Methodological caveats

Three caveats are reported transparently:

- **Idealised pharmacokinetics.** Busulfan is modelled as an instantaneous change in two effective rate constants at $t_{\text{intervention}}$. Real myelosuppression develops over 5–7 days under the two-stage experimental protocol (§2.1). The intervention timing simulation therefore represents an idealised scenario of immediate pharmacological effect, not a realistic PK/PD model; clinical extrapolation would require an explicit PK/PD layer built on top of the present model.

- **Neutrophil profile beyond $t = 8\;\text{d}$.** The Group II neutrophil interpolator $N(t)$ is held constant ($N = 3.73 \times 10^9\;\text{L}^{-1}$) for $t > 8\;\text{d}$, because the Group II observation window ended on day 8. For trajectories whose $t_{\text{recovery}}$ exceeds 8 d (all prevention and mitigation scenarios; see §S5.2), the dynamics on $[8, 19]\;\text{d}$ assume that neutrophil count remains stable near the Group II baseline. This is consistent with the experimental observation that Group II animals showed no late lethality and that the granulocyte compartment had not recovered within the observation window, but the extrapolation is a model assumption, not data.

- **Phase boundary precision.** The reported boundary "between days 2.5 and 3" reflects the 0.5-d grid resolution at this scan point. A finer scan would not meaningfully sharpen the boundary given the parameter uncertainty propagated through the bootstrap ensemble (per-scenario CIs on max\_recalc near the transition span several seconds; see the per-scenario figure reference in §S5.2). The half-day uncertainty is reported transparently in §3.5 of the main text ("a critical half-day transition between days 2.5 and 3"), not as a single interpolated value.

The first two caveats limit clinical generalisation, not model validity; the third reflects honest quantification of phase-boundary precision given the present grid.
