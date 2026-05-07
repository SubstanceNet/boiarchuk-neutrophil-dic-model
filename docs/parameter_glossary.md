# Parameter glossary

> **Status (Phase 0):** structural skeleton. Biological-interpretation column to be expanded with literature citations during Phase 4. For now, this captures the parameter inventory and the source of bounds, sufficient for code review.

## Convention

- Index = position in `src.config.NAMES` (0-based)
- Type: **shared** = same value for both groups; **G2-mod** = G2-specific modifier on a shared parameter
- Source: where the bound came from (diagnostic = inherited from v11.x diagnostic exploration; v12 = set in v12 prototype; biology = constrained by independent biological knowledge)

| # | Symbol | Bounds | Type | Role | Biological interpretation | Source |
|---|--------|--------|------|------|--------------------------|--------|
| 0 | k_d   | 0.1–5.0    | shared | Degranulation rate constant | Per-unit-signal degranulation kinetics; sets how fast the inflammatory signal converts resting → degranulated neutrophils | v12 |
| 1 | k_r   | 0.1–5.0    | shared | Recovery / clearance of degranulated state (G1) | Rate of return from degranulated state — combines true clearance and replenishment | v12 (expanded from 3.0 in v11.x) |
| 2 | k_rl  | 0.3–20     | shared | AP release rate from degranulated cells | Rate of acid-phosphatase appearance in plasma per unit D | v12 |
| 3 | k_cl  | 0.3–20     | shared | AP clearance rate | Plasma half-life of free AP | v12 |
| 4 | k_ca  | 0.1–100    | shared | Hc accumulation from venom | Rate of venom-driven coagulation-reservoir build-up | v12 |
| 5 | k_na  | 1–1500     | shared | Hn formation rate | Saturable Hn production from AP² | v12 (expanded from 800) |
| 6 | k_nd  | 0.01–10    | shared | Hn decay rate | First-order decay of neutrophil-driven reservoir | v12 |
| 7 | H_m   | 3–1000     | shared | Hn carrying capacity | Saturation level of neutrophil pro-coagulant pool | v12 |
| 8 | τ_p2  | 6–12       | shared | Inflammatory peak time (G1) | Days post-induction when secondary inflammatory pulse peaks | v12 (narrowed from wide; diagnostic showed 9–10 d) |
| 9 | σ₂    | 0.8–6.0    | shared | Inflammatory pulse width | Standard deviation of secondary inflammatory pulse | v12 |
| 10 | a₂   | 0.1–10     | shared | Inflammatory pulse amplitude | Multiplier on neutrophil-driven inflammatory drive | v12 |
| 11 | a_r  | 1–200      | shared | Recalc / V coefficient | Direct contribution of venom pulse to recalcification | v12 |
| 12 | c_r  | 5–600      | shared | Recalc / AP coefficient | Contribution of AP-mediated activity to recalcification | v12 |
| 13 | b_r  | 0.005–15   | shared | Recalc / gHn coefficient | Contribution of Hn-driven coagulation block to prolonged recalcification | v12 |
| 14 | a_t  | 0.5–25     | shared | Thrombin / V coefficient | Direct effect of venom on thrombin time | v12 |
| 15 | b_t  | 0.001–1.5  | shared | Thrombin / gHn coefficient | Hn-driven prolongation of thrombin time | v12 |
| 16 | a_f  | 1–120      | shared | Fib / V coefficient | Direct contribution of venom to fibrinogen change | v12 |
| 17 | c_f  | 5–350      | shared | Fib / AP coefficient | AP-driven (i.e. neutrophil-secretion-driven) contribution to fibrinogen — large c_f indicates IL-6-mediated hepatic stimulation by activated neutrophils | v12 |
| 18 | b_f  | 0.001–8    | shared | Fib / gHn coefficient | Consumption of fibrinogen via Hn pathway | v12 (expanded from 5) |
| 19 | d_f  | 0.1–30     | shared | Fib / Hc coefficient | Consumption of fibrinogen via venom pathway | v12 |
| 20 | a_x  | 1–250      | shared | XIII production / V | Direct stimulation of XIII activity by venom | v12 |
| 21 | c_x  | 10–600     | shared | XIII production / AP·Nr | Neutrophil-mediated XIII contribution (XIII is stored in azurophil granules). **Upper bound is a structural prior** validated by analysis 02 — without it, XIII-channel parameter manifold {ax, cx, bx, kx} becomes non-identifiable and at least one G2 observable collapses to R-squared < 0. See FINDINGS in `analyses/02_cx_bound/`. | v12 + analysis 02 (Phase 1) |
| 22 | b_x  | 0.001–50   | shared | XIII degradation / gHn | Consumption of XIII via neutrophil pathway | v12 |
| 23 | k_x  | 0.05–15    | shared | XIII liver-modulated resynthesis | Rate of hepatic XIII resynthesis, gated by liver function (1 − Hn/Hm) | v12 |
| 24 | k_m  | 1.5–15     | G2-mod | Myelosan modifier on k_r | Multiplier (G2: k_r,eff = k_r · k_m). Reflects accelerated clearance of activated neutrophils under myelosuppression | v12 |
| 25 | t_m  | 0.2–0.8    | G2-mod | Myelosan modifier on τ_p2 | Multiplier (G2: τ_p2,eff = τ_p2 · t_m). Reflects shortened inflammatory peak with reduced neutrophil pool | v12 |

## Fixed (not optimised)

- τ_v = 1.5 d — venom-pulse time-scale. Set by biological reasoning: peak of acute systemic effect of Эфа-2 venom in rabbit at ~36 hours post-administration.
- k_cd = 0.2 — Hc clearance rate. Set during diagnostic phase. Open question (Phase 2): refit with prior?

## Notes on bound rationale

For Phase 1 we will produce profile-likelihood plots of each parameter; bounds that are hit at the optimum (`<-- LOW` / `<-- HIGH` in CLI output) need either re-justification (biology forbids further extension) or expansion (purely numerical bound). At present, the v12 fit hits no bounds — but this should be re-verified after migration, and tracked across all alternative model variants.

## To be added in Phase 4

- Literature citations for each biological interpretation (e.g. azurophil granule storage of XIII: Schroeder et al. 2007).
- Independent biological-prior values for parameters where they exist (e.g. neutrophil-pool half-life from labelled-cell studies).
- Identifiability classification per parameter (Phase 1 output): well-identified / weakly-identified / sloppy.
