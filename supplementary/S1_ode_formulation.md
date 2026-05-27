# S1. Full ODE formulation and observable equations

*Part of the Supplementary Information for the manuscript "A mechanistic model of neutrophil-driven disseminated intravascular coagulation…" This section is the complete mathematical specification of the model; parameter symbols are defined in Table S2 (Supplementary S2), and the numerical estimates appear in Table 1 (main text) and Table S2. Cross-references in main text point here for: state-space definition (§2.2), gHn nonlinearity (§4.6), initial-condition convention (§2.1), and group-specific structure (§3.5).*

---

## S1.1 Notation and conventions

The model has five state variables, all initialised to zero (§S1.5):

| Symbol | Range | Units | Meaning |
|---|---|---|---|
| D | [0, 1] | dimensionless | Fraction of degranulated neutrophils |
| AP | ≥ 0 | Bodansky units (BO) | Acid phosphatase activity in plasma (Δ from baseline) |
| Hc | ≥ 0 | arbitrary | Inducer-derived coagulation pool |
| Hn | [0, Hm] | arbitrary | Neutrophil-derived coagulation pool |
| X | ℝ | % | Factor XIII activity (Δ from baseline) |

Time t is in days. The parameter vector pv has length 26; symbol-to-index mapping follows `src/config.NAMES` and is given in Table S2.

The two pools Hc and Hn appear in the source dissertation under the term *hyaline microthrombi*, reflecting the historical association with fibrin clots in the microvasculature characteristic of DIC. In the ODE these are abstract coagulation pools rather than literal microthrombi; the present text uses "inducer-derived coagulation pool" (Hc) and "neutrophil-derived coagulation pool" (Hn) accordingly.

Group differences are encapsulated in two effective parameters:

- Group I:  kr_eff = kr,  tp2_eff = tp2
- Group II: kr_eff = kr · km,  tp2_eff = tp2 · tm

All other 24 parameters are shared between groups. See §S1.9 for the biological interpretation.

---

## S1.2 Driving inputs

Three driving terms enter the ODE: a deterministic inducer-toxicity pulse V(t), a measured neutrophil signal N(t), and a self-limiting inflammatory composite S(t).

**Inducer-toxicity pulse.** The pulse V(t) has a gamma-like shape:

> V(t) = (t/τv) · exp(1 − t/τv) for t ≥ 0, and V(t) = 0 for t < 0.

This is a Gamma(2, 1) shape rescaled to peak at V(τv) = 1, with the timescale τv held fixed (§S1.7). It reaches its maximum at t = τv and decays smoothly thereafter.

**Neutrophil signal.** The measured neutrophil count N(t) is supplied as a per-group linear interpolator over the experimentally sampled timepoints. It is normalised by the Group I baseline count N1_BASE (§S1.7) to a relative form:

> Nr(t) = N(t) / N1_BASE.

**Gaussian shape.** An unnormalised peak-1 Gaussian appears in the inflammatory composite:

> g(t; μ, σ) = exp(−½ ((t − μ) / σ)²).

**Inflammatory signal.** The self-limiting inflammatory drive combines the inducer pulse and a delayed neutrophil-mediated burst, modulated by the available (non-degranulated) fraction of the neutrophil pool:

> S(t) = V(t) + a2 · g(t; tp2_eff, s2) · Nr(t) · (1 − D).

The factor (1 − D) enforces self-limitation: once neutrophils have degranulated, they cannot sustain further cytokine output. The Gaussian centred at tp2_eff with width s2 represents the secondary inflammatory peak.

---

## S1.3 State equations

The five ordinary differential equations are given below. Each right-hand side is evaluated against clipped state values to keep biology and numerics consistent: D ∈ [0, 1], AP ≥ 0, Hc ≥ 0, Hn ∈ [0, Hm · 0.999].

**Degranulation:**

> dD/dt = kd · S(t) · (1 − D) − kr_eff · D

The first term drives degranulation in proportion to the inflammatory signal, saturating as D → 1. The second term is first-order recovery / clearance of the degranulated state; in Group II its rate is amplified by km (§S1.9).

**Acid phosphatase:**

> dAP/dt = krl · D − kcl · AP

First-order release from degranulated cells (proportional to D) and first-order plasma clearance.

**Inducer-derived coagulation pool:**

> dHc/dt = kca · V(t) − k_cd · Hc

The pool accumulates while the inducer is active and decays with rate constant k_cd held fixed (§S1.7).

**Neutrophil-derived coagulation pool:**

> dHn/dt = kna · min(AP², 10) · max(1 − Hn/Hm, 0.005) − knd · Hn

Production is driven by AP² (a phenomenological model of neutrophil-burst amplification), capped at AP² = 10 to prevent runaway during transient AP excursions. The factor max(1 − Hn/Hm, 0.005) is a saturation-with-floor: production tapers off as Hn approaches the carrying capacity Hm, with a numerical floor of 0.005 preventing division-by-zero in the gHn formula (§S1.4). The second term is first-order clearance.

**Factor XIII activity:**

> dX/dt = ax · V(t) + cx · AP · Nr(t) − bx · gHn − kx · liver(Hn) · X,
> with liver(Hn) = max(1 − Hn/Hm, 0).

X is itself a state with its own dynamics, in contrast to recalcification, thrombin time, and fibrinogen (which are algebraic functions of the state; §S1.6). The right-hand side has four terms: direct inducer stimulation (ax · V), neutrophil-mediated production proportional to acid phosphatase and to the relative neutrophil signal (cx · AP · Nr; this models release of azurophilic-granule-stored XIII into circulation), gHn-mediated consumption (bx · gHn; see §S1.4 for the gHn nonlinearity), and liver-modulated resynthesis (kx · liver · X). The resynthesis term is gated by liver function, modelled as max(1 − Hn/Hm, 0): when Hn saturates the carrying capacity, hepatic resynthesis halts.

---

## S1.4 The gHn nonlinearity

Three of the observable equations (§S1.6) and the XIII state equation (§S1.3) depend on Hn through the nonlinear quantity gHn:

> gHn(Hn) = Hn / max(1 − Hn/Hm, 0.005).

The behaviour of gHn changes character with the ratio Hn / Hm:

- **Linear regime** (Hn ≪ Hm): the denominator is close to 1, so gHn ≈ Hn. Coagulation effects scale linearly with the neutrophil-derived pool.
- **Accelerating regime** (Hn → Hm): the denominator approaches zero and gHn diverges. Each additional unit of Hn contributes progressively more to the observables and to XIII consumption. This models a *cascading collapse* of coagulation as the neutrophil-derived pool saturates its carrying capacity — the mechanism by which neutrophil burden translates into the deep-hypocoagulation phase observed clinically.

The numerical floor 0.005 in the denominator bounds gHn ≤ 200 · Hn; this ceiling is never approached in practice (across all 100 bootstrap ensemble members and 22,500 dose-response simulations, Hn never exceeds approximately 1% of Hm). The floor exists purely to keep the integrator well-defined at the saturation boundary.

gHn enters the XIII channel doubly: it appears (i) in the algebraic recalcification, thrombin, and fibrinogen maps (§S1.6) and (ii) inside the XIII ODE itself as −bx · gHn (§S1.3). This double dependency explains the structurally high sensitivity of the XIII channel to Hn dynamics noted in main-text §3.2 and §4.6: phase mismatches between AP and gHn near the carrying capacity (the catastrophic-cancellation regime described in §4.6) amplify into the XIII fit.

---

## S1.5 Initial conditions

All five states are initialised to zero at t = 0:

> y(0) = [D(0), AP(0), Hc(0), Hn(0), X(0)] = (0, 0, 0, 0, 0).

These zeros are deltas, not absolute values. Each group's measurements are reported as changes from its own pre-induction baseline: Group I from the intact state, Group II from state M (the post-busulfan, pre-inducer state). See main-text §2.1 — "all Group II changes were therefore measured relative to state M rather than to the intact baseline" — for the experimental rationale and the statistical-significance footnote on the intact-to-M shift.

In particular, X(0) = 0 does not mean "no factor XIII at t = 0"; it means "no change from baseline at t = 0". Absolute baseline activity (100% in Group I, 93.2% in Group II) is a property of the experimental groups, not of the ODE state.

---

## S1.6 Observable maps

The six observables fall into three categories by how they relate to the state vector:

**Algebraic observables** are computed as linear combinations of the state at each evaluation time, with no separate ODE:

> recalc = −ar · V(t) − cr · AP + br · gHn
> thrombin = −at · V(t) + bt · gHn
> fib = +af · V(t) + cf · AP − bf · gHn − df · Hc

All coefficients (ar, cr, br, at, bt, af, cf, bf, df) are constrained to be non-negative (Table S2). The signs in the formulas above encode the biological direction of each effect:

- ar · V(t) shortens recalcification (initial hypercoagulation phase); cr · AP also shortens it; br · gHn lengthens it (the dominant hypocoagulation term in the late phase).
- For thrombin time the structure is similar but with only two terms.
- For fibrinogen: V and AP raise the concentration (acute-phase response); gHn and Hc deplete it (consumption coagulopathy).

The opposing-signs structure of the fibrinogen channel is the origin of the catastrophic-cancellation phenomenon discussed in main-text §4.6: in the days 5–7 window, cf · AP and −bf · gHn are each roughly four-fold larger in magnitude than their sum, so the observable is the difference of two large quantities.

**Dynamic-state observable** is the integrated state of an ODE:

> xiii = X (defined by §S1.3).

The XIII channel is therefore architecturally different from recalc / thrombin / fib: its parameters (ax, cx, bx, kx) are *rate constants* in an ODE, not algebraic coefficients in a map.

**Direct-state observables** are read straight from the state vector with no separate coefficients:

> acid_phosphatase = AP
> degranulation_index = D · 100  (presented as %)

These two observables therefore have no contribution coefficients to estimate — they are identifiable up to the parameters governing the AP and D dynamics (§S1.3).

The three-tier organisation of the six observables (algebraic / dynamic-state / direct-state) is what reduces the apparent "four contribution coefficient" channels of main-text §2.2 to a more nuanced structure: only three (recalc, thrombin, fib) are algebraic maps with their own coefficients; the fourth nominally "hemostatic" observable (xiii) is the integrated state of a dynamical equation.

---

## S1.7 Fixed (non-optimised) parameters

The following constants are set outside the optimisation. Their values are from `src/config.py`:

| Symbol | Value | Units | Role |
|---|---|---|---|
| τv (TV_FIX) | 1.5 | days | Inducer-toxicity pulse time-scale; biologically motivated by the peak of acute systemic ethylphenacin effect in rabbit at ~36 hours post-administration. |
| k_cd (KCD_FIX) | 0.2 | day⁻¹ | Inducer-derived coagulation pool (Hc) clearance rate; held fixed at the diagnostic-phase value, an open candidate for a future refit with prior. |
| N1_BASE | 7.3 | 10⁹/L | Baseline neutrophil count used to normalise Nr(t) = N(t) / N1_BASE; matches the Group I intact baseline. |

These three constants and the 26 optimised parameters in Table S2 are the complete parameterisation of the model.

---

## S1.8 Numerical integration

The ODE is integrated with `scipy.integrate.odeint` (LSODA, switching between non-stiff Adams and stiff BDF methods as needed). Tolerances and limits (from `src/config.py`):

> rtol = 1 × 10⁻⁵,  atol = 1 × 10⁻⁷,  mxstep = 5000.

Integration is performed on group-specific fine time grids and then linearly interpolated onto the evaluation grid for observable computation:

- Group I fine grid: 250 points uniformly over [0, 20] days (covers the 19-day observation window).
- Group II fine grid: 200 points uniformly over [0, 9] days (covers the 8-day observation window).

A NaN check on the integrator output guards against silent failure: any NaN in the trajectory raises a `RuntimeError`, ensuring that bootstrap or LOO iterations cannot drift unnoticed into pathological regions of parameter space.

For the intervention-timing virtual experiment (main-text §2.5), the ODE is integrated in two segments with the state vector continuous across the intervention boundary; only the two effective rate constants (kr_eff, tp2_eff) change instantaneously at t = t_intervention. See main-text §2.5 for the full protocol.

---

## S1.9 Group-specific structure

The joint model fits both groups with a shared 24-parameter core plus two group-specific modifiers — km and tm — that capture the effect of busulfan on Group II:

> Group I:  kr_eff = kr,        tp2_eff = tp2
> Group II: kr_eff = kr · km,   tp2_eff = tp2 · tm

The biological interpretation is that busulfan acts on the neutrophil compartment in two distinct ways. The rate modifier km > 1 represents accelerated clearance of activated neutrophils under reduced bone-marrow output (with km ≈ 4.9 in the fitted Group II, see Table 1). The timing modifier tm < 1 represents an earlier inflammatory peak in the depleted Group II compartment (with tm ≈ 0.43 in the fitted Group II, shifting the peak from tp2 ≈ 9.2 days in Group I to ≈ 3.9 days in Group II).

Critically, all per-cell biochemistry (kd, krl, kcl, kna, knd, ax, cx, bx, kx, the carrying capacity Hm, the inducer parameters kca, k_cd, τv, the pulse-width s2 and amplitude a2, and all nine algebraic-observable coefficients) is held identical between groups. The two-modifier architecture therefore encodes the hypothesis that busulfan modifies the *kinetics and timing* of the neutrophil compartment without altering its *per-cell function*. Main-text §3.5 quantifies how much of the observed Group II protection is attributable to this kinetic modification alone versus the reduction in neutrophil abundance encoded in N(t).
