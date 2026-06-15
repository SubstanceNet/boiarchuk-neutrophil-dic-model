# S1. Full ODE Formulation and Observable Equations

*Part of the Supplementary Information for the manuscript "A mechanistic model of neutrophil-mediated disseminated intravascular coagulation predicts a narrow, biphasic therapeutic window for myelosuppressive intervention…". This appendix provides the complete mathematical specification of the model; parameter symbols are defined in Table S2 of Appendix S2, which also consolidates the numerical estimates (a selection of well-identified parameters is given in Table 1 of the main text). Cross-references from the main text: state-space definition (Methods, Mathematical model), $g_{Hn}$ nonlinearity (Discussion, limitations), initial-condition convention (Methods, Mathematical model), definition of group-specific modifiers $k_m$/$t_m$ (Methods, Mathematical model; quantitative application — Results, Virtual experiments).*

---

## S1.1 Notation and conventions

The model has five state variables, all initialised to zero (§S1.5):

| **Symbol** | **Range** | **Units** | **Meaning** |
|---|---|---|---|
| $D$ | $[0, 1]$ | dimensionless | Fraction of degranulated neutrophils |
| $AP$ | $\geq 0$ | Bodansky units (BO) | Plasma acid phosphatase activity ($\Delta$ from baseline) |
| $H_c$ | $\geq 0$ | arbitrary | Inducer-derived coagulation pool |
| $H_n$ | $[0, H_m]$ | arbitrary | Neutrophil-derived coagulation pool |
| $X$ | $\mathbb{R}$ | % | Factor XIII activity ($\Delta$ from baseline) |

Time $t$ is in days. The parameter vector $p_v$ has length 26; the mapping of symbols to indices follows `src/config.NAMES` and is given in Table S2.

The two pools $H_c$ and $H_n$ appear in the source dissertation under the term *hyaline microthrombi*, reflecting the historical association with fibrin clots in the microvascular bed characteristic of DIC. Within the ODE, they represent abstract coagulation pools rather than literal microthrombi; accordingly, the present text uses "inducer-derived coagulation pool" ($H_c$) and "neutrophil-derived coagulation pool" ($H_n$).

Group differences are encapsulated in two effective parameters:

$$\text{Group I:} \quad k_{r,\text{eff}} = k_r, \quad t_{p2,\text{eff}} = t_{p2}$$

$$\text{Group II:} \quad k_{r,\text{eff}} = k_r \cdot k_m, \quad t_{p2,\text{eff}} = t_{p2} \cdot t_m$$

All other 24 parameters are shared between groups. For the biological interpretation, see §S1.9.

---

## S1.2 Driving inputs

Three driving terms enter the ODE: a deterministic inducer toxicity impulse $V(t)$, the measured neutrophil signal $N(t)$, and a self-limiting inflammatory composite $S(t)$.

**Inducer toxicity impulse.** The impulse $V(t)$ has a gamma-like shape:

$$V(t) = \frac{t}{\tau_v} \exp\!\left(1 - \frac{t}{\tau_v}\right) \quad \text{for } t \geq 0, \qquad V(t) = 0 \quad \text{for } t < 0.$$

This is a $\text{Gamma}(2, 1)$ form, rescaled to a peak of $V(\tau_v) = 1$, with time scale $\tau_v$ held fixed (§S1.7). It reaches its maximum at $t = \tau_v$ and smoothly decays thereafter.

**Neutrophil signal.** The measured neutrophil count $N(t)$ is supplied as a linear interpolator for each group over the experimentally sampled time points. It is normalised by the Group I baseline count $N_{1,\text{BASE}}$ (§S1.7) to a relative form:

$$N_r(t) = N(t) \;/\; N_{1,\text{BASE}}.$$

**Gaussian shape.** An unnormalised Gaussian with peak 1 appears in the inflammatory composite:

$$g(t;\, \mu, \sigma) = \exp\!\left(-\tfrac{1}{2}\left(\frac{t - \mu}{\sigma}\right)^2\right).$$

**Inflammatory signal.** The self-limiting inflammatory drive combines the inducer impulse and a delayed neutrophil-mediated burst, modulated by the available (non-degranulated) fraction of the neutrophil pool:

$$S(t) = V(t) + a_2 \cdot g(t;\, t_{p2,\text{eff}},\, s_2) \cdot N_r(t) \cdot (1 - D).$$

The multiplier $(1 - D)$ ensures self-limitation: once neutrophils have degranulated, they cannot sustain further cytokine release. The Gaussian centred on $t_{p2,\text{eff}}$ with width $s_2$ represents the secondary inflammatory peak.

---

## S1.3 State equations

The five ordinary differential equations are given below. Each right-hand side is evaluated at clipped state values to keep biology and numerics consistent: $D \in [0, 1]$, $AP \geq 0$, $H_c \geq 0$, $H_n \in [0,\, H_m \cdot 0.999]$.

**Degranulation:**

$$\frac{dD}{dt} = k_d \cdot S(t) \cdot (1 - D) - k_{r,\text{eff}} \cdot D$$

The first term drives degranulation proportional to the inflammatory signal, saturating as $D \to 1$. The second term is first-order recovery/clearance of the degranulated state; in Group II its rate is amplified by $k_m$ (§S1.9).

**Acid phosphatase:**

$$\frac{dAP}{dt} = k_{rl} \cdot D - k_{cl} \cdot AP$$

First-order release from degranulated cells (proportional to $D$) and first-order plasma clearance.

**Inducer-derived coagulation pool:**

$$\frac{dH_c}{dt} = k_{ca} \cdot V(t) - k_{cd} \cdot H_c$$

The pool accumulates while the inducer is active and decays with rate constant $k_{cd}$, held fixed (§S1.7).

**Neutrophil-derived coagulation pool:**

$$\frac{dH_n}{dt} = k_{na} \cdot \min(AP^2,\, 10) \cdot \max\!\left(1 - \frac{H_n}{H_m},\, 0.005\right) - k_{nd} \cdot H_n$$

Production is driven by $AP^2$ (a phenomenological model of neutrophil burst amplification), capped at $AP^2 = 10$ to prevent unbounded growth during transient $AP$ excursions. The cap value is a conservative anti-blow-up guard rather than a fitted quantity: at the reported optimum $AP^2$ stays far below it (maximum $\approx 0.47$ in the Group I configuration and $\approx 0.09$ in Group II), so the cap is never active in the baseline fit and only bounds pathological trajectories that the global optimiser may probe transiently. The factor $\max(1 - H_n/H_m,\, 0.005)$ is a saturation floor: production wanes as $H_n$ approaches the limiting capacity $H_m$, with a numerical floor of 0.005 that prevents division by zero in the $g_{Hn}$ formula (§S1.4). The second term is first-order clearance.

**Factor XIII activity:**

$$\frac{dX}{dt} = a_x \cdot V(t) + c_x \cdot AP \cdot N_r(t) - b_x \cdot g_{Hn} - k_x \cdot \text{liver}(H_n) \cdot X,$$

where $\text{liver}(H_n) = \max(1 - H_n/H_m,\, 0)$.

$X$ is itself a state with its own dynamics, unlike recalcification time, thrombin time, and fibrinogen (which are algebraic functions of the state; §S1.6). The right-hand side has four terms: direct stimulation by the inducer ($a_x \cdot V$); neutrophil-mediated production proportional to acid phosphatase and to the relative neutrophil signal ($c_x \cdot AP \cdot N_r$; this models elastase-mediated activation of plasma factor XIII, where $AP$ serves as a marker of the degranulation that releases neutrophil elastase from the same azurophilic granules [Henriksson et al., 1980; Bagoly et al., 2008]; biological rationale — the Discussion, mechanism decomposition); $g_{Hn}$-mediated consumption ($b_x \cdot g_{Hn}$; see the $g_{Hn}$ nonlinearity in §S1.4); and liver-modulated resynthesis ($k_x \cdot \text{liver} \cdot X$). The resynthesis term is limited by liver function, modelled as $\max(1 - H_n/H_m, 0)$: when $H_n$ saturates the limiting capacity, hepatic resynthesis ceases.

---

## S1.4 The $g_{Hn}$ nonlinearity

Three of the observable equations (§S1.6) and the factor XIII state equation (§S1.3) depend on $H_n$ through the nonlinear quantity $g_{Hn}$:

$$g_{Hn}(H_n) = \frac{H_n}{\max\!\left(1 - H_n/H_m,\; 0.005\right)}.$$

The behaviour of $g_{Hn}$ changes character with the ratio $H_n / H_m$:

- **Linear regime** ($H_n \ll H_m$): the denominator is close to 1, so $g_{Hn} \approx H_n$. Coagulation effects scale linearly with the neutrophil-derived pool.

- **Accelerating regime** ($H_n \to H_m$): the denominator shrinks and $g_{Hn}$ rises faster than linearly (formally diverging only in the limit $H_n \to H_m$, which is never reached in practice; see below). In this regime each additional unit of $H_n$ contributes more to the observables and to factor XIII consumption — a phenomenological representation of accelerating coagulation-factor consumption as the neutrophil-derived pool approaches its limiting capacity. We read this as a qualitative amplification mechanism rather than as literal cascade collapse.

The two regimes are activated in different experimental configurations. In the Group II baseline configuration (preserved neutrophil profile with busulfan-modified rate constants), the ratio $H_n/H_m$ remains small — median 0.018 across 100 ensemble members, max 0.35 — and $g_{Hn}$ operates predominantly in the linear regime. In the pure Group I configuration (Group I neutrophil profile, no busulfan modifiers), $H_n/H_m$ grows substantially larger — median 0.090, $p_{97.5} = 0.62$, max $= 0.75$ across 100 ensemble members; 31 of 100 members exceed 0.30, and 11 exceed 0.50. In these members the denominator $1 - H_n/H_m$ falls to 0.25–0.40, giving a nonlinear $g_{Hn}/H_n$ lift of 2–4-fold. The accelerating regime is therefore active only in a minority of the most severe Group I members; the median Group I trajectory, with $H_n/H_m \approx 0.09$, still sits in the near-linear regime. Where active, it coincides with the deep-hypocoagulation mode (max $\Delta$recalcification 147 s) near the observed lethality window. Because the limiting capacity $H_m$ is among the least-identified parameters (relative profile depth $< 0.5\%$, §S3.2), the exact degree of this nonlinear lift is not well constrained by the data: the qualitative feature — mild faster-than-linear amplification in the most severe members — is robust, but its precise magnitude should not be over-interpreted.

The numerical floor 0.005 in the denominator bounds $g_{Hn} \leq 200 \cdot H_n$; this ceiling is never approached in practice — even in the most severe Group I members, max $H_n/H_m = 0.75$ gives only a ~4-fold lift, far from the 200-fold ceiling. The floor exists purely to keep the integrator well-defined at the saturation boundary.

$g_{Hn}$ enters the factor XIII channel twice: it appears (i) in the algebraic maps for recalcification, thrombin, and fibrinogen (§S1.6), and (ii) inside the factor XIII ODE itself as $-b_x \cdot g_{Hn}$ (§S1.3). This double dependence explains the structurally high sensitivity of the XIII channel to $H_n$ dynamics noted in the Results (Identifiability analysis) and the Discussion (limitations): phase mismatches between $AP$ and $g_{Hn}$ near the limiting capacity (the catastrophic-cancellation mode described in the Discussion, limitations) are amplified in the XIII fit.

---

## S1.5 Initial conditions

All five states are initialised to zero at $t = 0$:

$$\mathbf{y}(0) = \bigl[D(0),\; AP(0),\; H_c(0),\; H_n(0),\; X(0)\bigr] = (0, 0, 0, 0, 0).$$

These zeros are deltas, not absolute values. Measurements for each group are reported as changes from that group's own pre-induction baseline: Group I from the intact state, Group II from the post-busulfan state "M" (prior to inducer administration). The experimental rationale and note on the statistical significance of the shift from intact to M are given in the Methods (Mathematical model) — "all changes in Group II are measured relative to state M, not to the intact baseline."

In particular, $X(0) = 0$ does not mean "no factor XIII at $t = 0$"; it means "no change from baseline at $t = 0$." The absolute baseline activity (100% in Group I, 93.2% in Group II) is a property of the experimental groups, not of the ODE state.

---

## S1.6 Observable mappings

The six observables fall into three categories according to how they are linked to the state vector:

**Algebraic observables** are computed as linear combinations of the state at each evaluation time, with no separate ODE:

$$\text{recalc} = -a_r V(t) - c_r AP + b_r g_{Hn}$$

$$\text{thrombin} = -a_t V(t) + b_t g_{Hn}$$

$$\text{fib} = a_f V(t) + c_f AP - b_f g_{Hn} - d_f H_c$$

All coefficients ($a_r, c_r, b_r, a_t, b_t, a_f, c_f, b_f, d_f$) are constrained to be non-negative (Table S2). The signs in the formulas above encode the biological direction of each effect:

- $a_r \cdot V(t)$ shortens recalcification time (initial hypercoagulable phase); $c_r \cdot AP$ also shortens it; $b_r \cdot g_{Hn}$ prolongs it (the dominant late-phase hypocoagulation term).
- For thrombin time, the structure is analogous but with only two terms.
- For fibrinogen: $V$ and $AP$ raise concentration (acute-phase response); $g_{Hn}$ and $H_c$ deplete it (consumptive coagulopathy).

The opposing-sign structure of the fibrinogen channel is the source of the catastrophic-cancellation phenomenon discussed in the Discussion (limitations): in the window of days 5–7, $c_f \cdot AP$ and $-b_f \cdot g_{Hn}$ are each roughly fourfold larger in magnitude than their sum, so the observable is the difference of two large quantities.

**Dynamic-state observable** — the integrated ODE state:

$$\text{xiii} = X \quad \text{(defined in §S1.3)}.$$

The factor XIII channel is therefore architecturally distinct from recalc / thrombin / fib: its parameters ($a_x, c_x, b_x, k_x$) are *rate constants* in the ODE, not algebraic coefficients in the mapping.

**Direct-state observables** are read directly from the state vector without separate coefficients:

$$\text{acid\_phosphatase} = AP$$

$$\text{degranulation\_index} = D \times 100 \quad \text{(expressed in \%)}$$

These two observables therefore carry no contribution coefficients to estimate — they are identified up to the parameters governing the dynamics of $AP$ and $D$ (§S1.3).

This three-tier organisation (algebraic / dynamic-state / direct-state) refines the apparent "four haemostatic channels with contribution coefficients" (Methods, Mathematical model) into a more precise structure: only three (recalc, thrombin, fib) are algebraic maps with their own coefficients; the fourth nominally "haemostatic" observable (xiii) is an integrated dynamic-equation state.

---

## S1.7 Fixed (non-optimised) parameters

The following constants are specified outside of optimisation. Their values are from `src/config.py`:

| **Symbol** | **Value** | **Units** | **Role** |
|---|---|---|---|
| $\tau_v$ (TV\_FIX) | 1.5 | days | Time scale of the inducer toxicity impulse; biologically motivated by the peak acute systemic effect of ethylphenacin in rabbits at ~36 h after administration. |
| $k_{cd}$ (KCD\_FIX) | 0.2 | day$^{-1}$ | Clearance rate of the inducer-derived coagulation pool ($H_c$); held fixed at a diagnostic-phase value, an open candidate for future refitting with a prior. |
| $N_{1,\text{BASE}}$ | 7.3 | $10^9$/L | Baseline neutrophil count for normalisation $N_r(t) = N(t) / N_{1,\text{BASE}}$; corresponds to the intact Group I baseline. The same fixed scale normalises both cohorts, so the suppressed Group II profile (baseline $\approx 3.9$) enters as a reduced $N_r$ rather than rescaled to unity, preserving the absolute count difference used in the §S6.5 decomposition. |

These three constants and the 26 optimised parameters of Table S2 constitute the complete model parametrisation.

---

## S1.8 Numerical integration

The ODE is integrated using `scipy.integrate.odeint` (LSODA, switching between a non-stiff Adams method and stiff BDF as needed). Tolerances and bounds (from `src/config.py`):

$$\text{rtol} = 1 \times 10^{-5}, \quad \text{atol} = 1 \times 10^{-7}, \quad \text{mxstep} = 5000.$$

Integration is performed on group-specific fine time grids and then linearly interpolated to the evaluation grid for computing observables:

- **Group I fine grid:** 250 points uniformly on $[0, 20]$ days (covering the 19-day observation window).
- **Group II fine grid:** 200 points uniformly on $[0, 9]$ days (covering the 8-day observation window).

NaN-checking of integrator output guards against silent failure: any NaN in a trajectory raises a `RuntimeError`, ensuring that bootstrap or LOO iterations cannot silently drift into pathological regions of parameter space.

For the timing-of-intervention virtual experiment (Methods, Virtual experiments), the ODE is integrated in two segments with the state vector continuous across the intervention boundary; only the two effective rate constants ($k_{r,\text{eff}}$, $t_{p2,\text{eff}}$) change instantaneously at $t = t_{\text{intervention}}$. Full protocol in the Methods (Virtual experiments).

---

## S1.9 Group-specific structure

The shared model fits both groups with a common 24-parameter core plus two group-specific modifiers — $k_m$ and $t_m$ — that capture the busulfan effect on Group II:

$$\text{Group I:} \quad k_{r,\text{eff}} = k_r, \qquad t_{p2,\text{eff}} = t_{p2}$$

$$\text{Group II:} \quad k_{r,\text{eff}} = k_r \cdot k_m, \qquad t_{p2,\text{eff}} = t_{p2} \cdot t_m$$

Biologically, this means busulfan acts on the neutrophil compartment in two distinct ways. The rate modifier $k_m > 1$ represents accelerated clearance of activated neutrophils under reduced bone-marrow output (with $k_m \approx 4.9$ in the fitted Group II; see Table 1). The time modifier $t_m < 1$ represents an earlier inflammatory peak in the depleted Group II compartment (with $t_m \approx 0.43$ in the fitted Group II, shifting the peak from $t_{p2} \approx 9.2$ days in Group I to $\approx 3.9$ days in Group II).

Critically, all per-cell biochemistry (the free shared parameters $k_d, k_r, k_{rl}, k_{cl}, k_{na}, k_{nd}, a_x, c_x, b_x, k_x$, limiting capacity $H_m$, inducer parameters $k_{ca}, a_2, s_2, t_{p2}$, and all nine coefficients of the algebraic observables, alongside the explicitly fixed constants $k_{cd}$ and $\tau_v$) is held identical between groups. The two-modifier architecture therefore encodes the hypothesis that busulfan modifies the *kinetics and timing* of the neutrophil compartment without altering its *per-cell function*. The Results (Virtual experiments) quantify what fraction of the observed Group II protection is attributable to this kinetic modification alone, and what fraction to the reduction in neutrophil count encoded in $N(t)$.
