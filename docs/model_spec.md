# Model specification

> **Status (Phase 0):** placeholder. The mathematical content here will be expanded into a publication-ready specification during Phase 4. For now, this document records the v12 model as migrated, sufficient for any reader of the code to reconstruct the equations.

## State variables

| Symbol | Domain | Meaning |
|--------|--------|---------|
| D      | [0, 1] (fraction) | Fraction of degranulated neutrophils |
| AP     | ℝ⁺, BO units      | Acid phosphatase activity in plasma (delta from baseline) |
| Hc     | ℝ⁺, arbitrary     | Venom-driven coagulation reservoir |
| Hn     | [0, Hm]           | Neutrophil-driven coagulation reservoir |
| X      | ℝ, %              | Δ Factor XIII activity |

## Driving inputs

- **Venom pulse** (gamma-shape, peak at t = τ_v):
  V(t) = (t/τ_v) · exp(1 − t/τ_v) for t ≥ 0, else 0.  τ_v = 1.5 d (fixed).

- **Neutrophil count** N(t): linear interpolation of measured values from `data/csv/group{1,2}.csv`, normalised as Nr(t) = N(t) / N0 with N0 = 7.3 × 10⁹/L (G1 baseline).

- **Self-limiting inflammatory signal**:
  S(t) = V(t) + a₂ · exp(−½ · ((t − τ_p2) / σ₂)²) · Nr(t) · (1 − D(t)).
  The (1 − D) factor models the fact that already-degranulated cells cannot sustain cytokine output.

## ODE system

dD/dt  = k_d · S(t) · (1 − D)  −  k_r,eff · D
dAP/dt = k_rl · D  −  k_cl · AP
dHc/dt = k_ca · V(t)  −  k_cd · Hc                  (k_cd = 0.2, fixed)
dHn/dt = k_na · min(AP², 10) · max(1 − Hn/Hm, 0.005) · 1  −  k_nd · Hn
dX/dt  = a_x · V(t)  +  c_x · AP · Nr  −  b_x · gHn  −  k_x · max(1 − Hn/Hm, 0) · X

with auxiliary quantity gHn(t) = Hn / max(1 − Hn/Hm, 0.005).

**Group differences** enter only through k_r,eff and τ_p2:
- G1: k_r,eff = k_r,            τ_p2 = τ_p2
- G2: k_r,eff = k_r · k_m,       τ_p2 = τ_p2 · t_m

## Observation equations

Δ Recalcification time = − a_r · V  − c_r · AP  + b_r · gHn
Δ Thrombin time         = − a_t · V             + b_t · gHn
Δ Fibrinogen            = + a_f · V  + c_f · AP − b_f · gHn − d_f · Hc
Δ F. XIII activity      = X (state variable)

## Parameters

26 parameters total, listed in `src/config.py` with bounds. See `docs/parameter_glossary.md` for biological interpretation, units, and source.

## Cost function

Joint cost = (G1 survivor-weighted normalised RMSE over 6 observables) + (G2 uniform normalised RMSE over 6 observables) + Hn-saturation penalty + W_split · mechanism-split residual at G1 day 2.

Mechanism-split fixes pro-coagulant fractions on G1 day 2:
- recalc: 24% neutrophil-mediated
- fib:    76% neutrophil-mediated
- xiii:   82% neutrophil-mediated

These targets are derived from G2/G1 day-1 ratios in the dissertation tables. The use of these as a hard prior on the same data is a methodological concern flagged in `notes/known_issues.md` and will be addressed in Phase 1 by sensitivity to W_split and Phase 2 by potential reformulation.

## Numerical integration

`scipy.integrate.odeint` with rtol=1e-5, atol=1e-7, mxstep=5000. Fine integration grids: 250 points on [0, 20] d for G1; 200 points on [0, 9] d for G2. State trajectories are linearly interpolated to observation times.

## Open structural questions (Phase 2)

1. Is the (1 − D) self-limiting factor sufficient to capture G2 dynamics, or does fibrinogen-G2 require an additional channel? (current G2 fib R² = 0.26 — see v12 report §7.5)
2. Should the W_split mechanism-split constraint be replaced by an external prior derived independently of the fitted dataset, or relaxed and treated as a soft target across a profile of W values?
3. Is k_cd = 0.2 (Hc clearance) a defensible biological constant, or should it be fitted with a narrow prior?
4. Does the joint architecture (24 shared + 2 modifiers) have a principled extension that recovers the per-group separate-fit R² without overfitting?
