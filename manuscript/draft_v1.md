---
title: "[WORKING TITLE] A mechanistic model of neutrophil-driven disseminated intravascular coagulation reveals a narrow therapeutic window for myelosuppressive intervention"
authors:
  - name: "Olena Boiarchuk"
    affiliation: "[institution placeholder]"
    role: "experimental design, biological interpretation, manuscript drafting"
  - name: "Oleksiy Onasenko"
    affiliation: "[institution placeholder]"
    role: "mathematical model, numerical analysis, manuscript drafting"
journal: "Journal of Theoretical Biology (working format)"
status: "skeleton v1 — 12 May 2026"
---

# Abstract

**[PLACEHOLDER — fill last, ~250 words]**

Skeleton scope:
- 1-2 sentences: context (neutrophil role in DIC, myelosan in the neutrophil compartment; Efa-2 / ethylphenacin anticoagulant-rodenticide DIC model)
- 1 sentence: gap (no mechanistic model decomposing neutrophil vs vessel contributions)
- 2-3 sentences: approach (mechanistic ODE model fit to two experimental groups; identifiability + bootstrap + LOO-CV + N(t) perturbation robustness checks; three virtual experiments)
- 3-4 sentences: key findings (prior-regularized mechanism split quantifying neutrophil contribution, consistent with the neutrophil hypothesis; myelosan kinetic effect 2.5-7× DIC reduction; therapeutic window 0-2.5 days; dose-timing thresholds)
- 1 sentence: clinical implication (narrow window requires both adequate dose AND early administration)

---

# 1. Introduction

*[Team-drafted from the source documents; to be reviewed by O.B. for
biological accuracy and reference completeness.]*

Disseminated intravascular coagulation (DIC) is a systemic, acquired
disorder of hemostasis in which widespread activation of coagulation leads
first to microvascular thrombosis and consumption of clotting factors, and
subsequently to a bleeding tendency as those factors are exhausted. DIC is
not a primary disease but a complication of shock, sepsis, trauma, burns,
obstetric emergencies, and envenomation, and it remains a major contributor
to mortality in these settings [ref: Pavlovsky 1988; Chervyovy 1990]. Its
laboratory hallmark is a characteristic temporal sequence: an initial
hypercoagulable phase, a transitional consumption coagulopathy, and a
terminal hypocoagulable phase in which clotting may fail almost completely.

Neutrophilic granulocytes are classically regarded as effectors of innate
immunity and as participants in the inflammatory response that accompanies
DIC. A body of experimental work, however, has argued that neutrophils are
not merely bystanders but active participants in the coagulopathy itself,
acting through their lysosomal apparatus. The lysosomal enzymes of
neutrophils are markedly more active than the corresponding enzymes of liver
and brain, and they exert a potent activating effect on Hageman factor
(factor XII), the contact-phase initiator of the intrinsic coagulation
cascade [ref: Bakhov 1988; Baluda; Kuznik 1989]. Upon neutrophil
degranulation, these enzymes — for which acid phosphatase serves as a
convenient marker — are released into the circulation, where they can
activate factor XII, promote the conversion of plasminogen to plasmin, and
thereby amplify fibrinolytic activity. This places neutrophil degranulation
mechanistically upstream of the fibrinolytic, hypocoagulable phase of DIC.

The experimental model underlying the present study tests this hypothesis
directly. DIC was induced in rabbits by a standardized inducer (the
preparation "Efa-2", 8330 mg/kg orally), which reproduces the classical
three-phase DIC time course — hypercoagulation (days 1-4), a transitional
consumption phase, and deep hypocoagulation (days ~6-11, with possible
complete incoagulability), resolving by days 19-20 [ref: Boiarchuk 1998].
Two groups were compared: a control DIC group (Group I), and a group in
which granulocytopoiesis was pharmacologically suppressed by myelosan prior
to induction (Group II). The central experimental finding is that
suppression of the neutrophil lineage largely prevents the deep
hypocoagulable phase: in Group II the clinically significant DIC stage
contracts from ~14-15 days to ~6 days, peak acid phosphatase activity is
roughly 2.5-fold lower, and the 30% mortality observed in Group I (days
10-12, at the hypocoagulation peak) is essentially absent. Together these
observations provide a causal, not merely correlative, argument for the
pathogenetic role of activated neutrophils in the hypocoagulable phase of
DIC [ref: Boiarchuk 2008].

This causal picture nonetheless leaves two questions unresolved, both of
which are quantitative rather than qualitative. First, the observable
coagulation defects (prolonged recalcification time, fibrinogen depletion,
factor XIII loss) presumably reflect a combination of a direct,
inducer-driven (vessel-mediated) contribution and an indirect,
neutrophil-mediated contribution; the relative size of these two
contributions in each observable has not been quantified. Second, myelosan
attenuates DIC, but the mechanism of that protection is ambiguous: it could
act by reducing the number of neutrophils available to degranulate, by
altering the kinetics of the neutrophil-driven processes, or both — and the
existing data describe the protective effect without decomposing it. The
prior literature characterizes neutrophil involvement qualitatively and
through stage-averaged comparisons; it does not provide a mechanistic model
that resolves these two questions.

We therefore develop a mechanistic ordinary-differential-equation model of
neutrophil-driven DIC, fit jointly to both experimental groups, with three
aims: (i) to build and validate a dynamical model that reproduces the
six measured hemostatic and neutrophil-activity observables in both groups;
(ii) to quantify, with uncertainty, the decomposition of each observable
into vessel-mediated and neutrophil-mediated contributions, and to test it
against the held-out suppressed-granulopoiesis group; and (iii) to use the
validated model to predict the dose-response and the timing dependence of
myelosuppressive intervention, with a view to the therapeutic window such
intervention would imply.

---

# 2. Methods

## 2.1 Experimental data and protocols

*[Team-drafted from the experimental protocol; to be reviewed by O.B. for
accuracy and ethics/approval details.]*

**Animals and design.** Experiments were performed on 40 sexually mature
rabbits of both sexes, body mass 2.5-3.0 kg, housed under standard vivarium
conditions with free access to water and maintained according to accepted
bioethical principles for laboratory animals. Two groups were studied. In
Group I (control DIC), disseminated intravascular coagulation was modeled by
a single oral dose of the inducer "Efa-2" (8330 mg/kg, administered fasting). Efa-2 is a commercial anticoagulant-rodenticide bait based on ethylphenacin, a first-generation 1,3-indandione vitamin-K antagonist; the 8330 mg/kg figure is the dose of the ready bait (approximately 0.015% active substance), not of a purified compound. Mechanistically it inhibits vitamin-K-epoxide reductase, which depletes the vitamin-K-dependent coagulation factors (II, VII, IX, X) and proteins C and S and damages vascular endothelium, triggering a secondary disseminated intravascular coagulation that progresses through the classic three-phase cycle reproduced here
without prior intervention in the granulocyte lineage. In Group II
(suppressed granulocytopoiesis), the identical inducer and dose were
administered after pharmacological suppression of granulocytopoiesis.

**Granulocytopoiesis suppression (Group II).** Suppression was achieved by
oral myelosan (busulfan, an alkylating agent — 1,4-butanediol dimethanesulfonate; marketed elsewhere as Myleran or Busulfex — which at low doses selectively depresses granulocytopoiesis) in a two-stage schedule. In the first stage, myelosan was given
at 10 mg/day for 5-7 days, continued until the absolute peripheral neutrophil
count fell by 40-50% from the intact level. In the second stage, a
maintenance dose of 4 mg/day was given for approximately 8 days to stabilize
the reduced neutrophil count without deepening the cytopenia. The inducer was
then administered immediately, without interval. This protocol establishes a
distinct pre-induction state, denoted "M" (post-myelosan), at which the
absolute neutrophil count is reduced (from ~8.0 to ~3.9 x10^9/L) and
hemostatic parameters are minimally shifted relative to intact; differences
between intact and M are statistically significant for factor XIII
(P < 0.001). For Group II, the effects of Efa-2 are therefore referenced to
state M rather than to the intact state.

**Sampling and observables.** Group I was sampled at 16 timepoints over 19
days (including the baseline anchor at t=0); Group II at 9 timepoints over 8
days (the DIC process in Group II essentially resolves by day 8, whereas in
Group I it extends to day 19). At each timepoint, six observables were
recorded: plasma recalcification time, thrombin time, fibrinogen
concentration, factor XIII (fibrinase) activity, serum acid phosphatase
activity, and the hyaline-degranulation index of circulating neutrophils.
Recalcification time, thrombin time, fibrinogen, and factor XIII were
determined by standard hemostasis methods; ethanol and protamine-sulfate
tests were used to detect soluble fibrin-monomer complexes. The neutrophil
lysosomal formula was determined by the Pigarevsky method with
May-Grunwald staining, classifying cells into three categories by granule
content (>30, up to 10, and <10 granules); acid phosphatase, the marker
lysosomal enzyme, was assayed by the Bodansky method and expressed in
Bodansky units (BU). Statistical significance was assessed by the method of
direct differences (Monceviciute-Eringene).

**Mortality.** In Group I, partial mortality of 30% (12 of 40 animals) was
observed on days 10-12 post-induction, coinciding with the phase of maximal
hypocoagulation; subsequent timepoints (days 13, 14, 19) therefore derive
from a reduced surviving cohort (n ~ 28). No mortality occurred in Group II.

**Data representation and availability.** All hemostatic and
neutrophil-activity values are expressed as deltas from each group's baseline
(Group I from the intact state; Group II from state M); neutrophil counts are
absolute. The experimental tables are reproduced in `data/csv/` with
per-table source mapping in `data/csv/PROVENANCE.md`. The data derive from
the Boiarchuk dissertation (1998) and associated publications; a substantial
portion of the Group II dynamics is reported here for the first time.

## 2.2 Mathematical model

The model comprises a 5-state ODE system tracking degranulation dynamics (D), acid phosphatase activity (AP), hyaline form (Hc), neutrophil count (Hn), and factor XIII activity (X). Six measured observables — recalcification time, thrombin time, fibrinogen, factor XIII, acid phosphatase, hyaline-degranulation index — are computed as algebraic functions of the ODE state vector.

The model contains 26 parameters: rate constants for degranulation and recovery (kr, krl, kcl, kca, kna, knd, Hm, kd), peak-timing parameters of the inducer toxicity pulse (tp2, s2), and observable-specific contribution coefficients for the four hemostatic channels (recalcification time, thrombin time, fibrinogen, factor XIII). The remaining two observables — acid phosphatase and the hyaline-degranulation index — are read directly from the model states (AP and D respectively) and so carry no separate contribution coefficients; the six observables are thus four coefficient-mapped hemostatic channels plus two directly-observed states. The G1 and G2 groups share all parameters except for group-specific modifiers (km, tm) that scale the effective rate constants in G2 to represent the myelosan effect.

Two structural priors are imposed to resolve identifiability. First, a mechanism-split constraint (penalty weight W_SPLIT = 2.0) targets the day-2 neutrophil-attributable fractions of the recalcification, fibrinogen, and factor XIII channels; the target values (0.24, 0.76, 0.82) are derived independently from the day-1 (ΔG1−ΔG2)/ΔG1 ratios in the experimental data (see §3.3). Without this prior the decomposition is non-identifiable across optimizer seeds. Second, an upper bound on the factor XIII production parameter (cx ≤ 600) constrains the XIII channel to a biologically interpretable subspace; relaxing it unlocks a multi-modal landscape in which the XIII fit trades off against the other G2 observables. Both priors are validated post-hoc by superior held-out (G2) fit relative to unconstrained alternatives (Supplementary, Analyses 01-02).

**Full ODE formulation, parameter definitions, and observable formulas are provided in Supplementary Methods S1.**

The neutrophil count time course N(t) is provided as experimental input (one interpolator per group) rather than as a model variable; this design choice is justified by the fact that N(t) is directly measured at all sampling timepoints.

## 2.3 Parameter estimation

Joint cost function minimizes weighted sum of squared residuals across all six observables and both groups. Parameter estimation pipeline: differential evolution (popsize=15, maxiter=200, Sobol initialization) for global search, followed by sequential Nelder-Mead → Powell → Nelder-Mead polishing.

Numerical implementation details: scipy 1.15, numpy 2.2, Python 3.10. Code and reproducibility tests at [repository URL placeholder].

The joint architecture (24 shared parameters + 2 group-specific modifiers) trades some per-group fit quality for cross-group consistency: a separate G2-only fit attains ~22 percentage points higher mean G2 R² than the joint fit (Supplementary, Analysis 03), a gap that is largely architectural rather than attributable to overfitting. This penalty is accepted in exchange for a single shared mechanistic parameterization across both groups.

## 2.4 Robustness analysis

We assessed model robustness through three complementary protocols.

**Profile likelihood analysis** for all 26 parameters identified well-identified parameters (depth_rel > 5%; 6 parameters: tp2, km, tm, kd, s2, at), weakly identified (5 parameters), and sloppy (12 parameters with depth_rel < 2%).

**Parametric bootstrap (N=100):** synthetic datasets generated from baseline predictions with Gaussian noise (σ = per-observable per-group baseline RMSE); full estimation pipeline repeated per iteration. Yields marginal CIs on all parameters and on prediction trajectories.

**Leave-one-out cross-validation:** for each of 23 non-anchor timepoints (15 G1 + 8 G2), removed all six observables at that timepoint, refit the model, computed PRESS statistic for predictions at the held-out point.

**Neutrophil count perturbation:** tested model sensitivity to N(t) measurement uncertainty via deterministic scaling (α ∈ {0.8, 0.9, 1.0, 1.1, 1.2}) and stochastic lognormal noise (CV=10%, CV=20%, N=20 each).

## 2.5 Virtual experiments

Three virtual experiments used the 100-member bootstrap parameter ensemble to propagate uncertainty through prediction tasks.

**Myelosan dose-response (Experiment 1):** 15×15 log-spaced grid in (km, tm) parameter space, with G2 effective rate constants overridden as kr_g2 = kr × km, tp2_g2 = tp2 × tm. G2 neutrophil profile retained throughout. 22,500 total simulations.

**Intervention timing (Experiment 2):** myelosan effect applied starting at t_intervention via two-segment ODE integration. ODE state (D, AP, Hc, Hn, X) is continuous across the intervention boundary; only rate constants change instantaneously. Nine timing scenarios from t=0 to t=∞ (no intervention), at fixed G2-observed dose. 900 total simulations.

**Dose × timing combinations (Experiment 3):** two specific scenarios — high dose at late timing, half dose at early timing — to test the dose-timing trade-off hypothesis directly. 200 simulations.

**Severity metrics.** For each trajectory: peak hypocoagulation (max Δrecalc), integrated coagulation disruption (AUC |Δrecalc|), XIII depletion nadir (min Δxiii), and peak hyaline-degranulation accumulation (max gHn).

**Temporal metrics** (Experiment 2 only): time of peak gHn (t_peak), time to recovery (gHn falling below 10% of peak after the peak; t_recovery), acute phase duration (Δt = t_recovery − t_peak).

Severity metrics were computed on the native G2 timeline (0-9 days) for Experiment 1 and on an extended timeline (0-19 days) for Experiments 2 and 3. Time-to-peak was defined as the first local maximum of gHn(t) to avoid boundary artifacts in finite-horizon simulations.

---

# 3. Results

## 3.1 Model captures both experimental groups

Fitted jointly to both groups, the model reproduces the measured dynamics of
all six observables. For Group I (15 non-anchor timepoints over 19 days) the
mean coefficient of determination across observables is R² = 0.83; for the
myelosan-suppressed Group II (8 timepoints over 8 days) it is R² = 0.69. Most
channels are captured well in both groups; the lower Group II mean is driven
by the factor XIII channel, which is structurally under-determined (§3.2)
rather than poorly fit by chance.

The agreement is strongest in the deep-hypocoagulation phase: the late-phase
nadirs of factor XIII and fibrinogen are reproduced within 1–11% (§3.8). The
principal discrepancy is in the early, hypercoagulation phase, where the
amplitude of the two vessel-driven channels — recalcification time and
fibrinogen — is underestimated; the fibrinogen channel additionally shows a
non-monotonic intermediate profile arising from near-cancellation of two
large opposing terms (§4.6). These discrepancies are confined to the early
phase of the vessel-driven channels and do not affect the peak timing or the
group separation that underlie the main findings.

The baseline fits are shown in Figure 1.

**Figure 1.** Baseline model fits versus experimental data for both groups. Six panels, one per observable: (a) recalcification time, (b) thrombin time, (c) fibrinogen, (d) factor XIII activity, (e) acid phosphatase, (f) hyaline-degranulation index. Group I (blue circles, solid line) and Group II (red triangles, dashed line); points are group means with SEM error bars (M±m from the dissertation tables), curves are the baseline fit (lowest-cost parameter vector across seeds). All quantities are deltas from each group's baseline (Group I from intact, Group II from state M); model curves are drawn only within each group's observed range (no Group II extrapolation). The gray band (days 10-12) marks the Group I mortality / deep-hypocoagulation window. Mean R² = 0.83 (Group I) and 0.69 (Group II). The early hypercoagulation amplitude in the recalcification and fibrinogen channels is underestimated, and the fibrinogen curve shows a non-monotonic intermediate profile (§4.6); the late-phase nadirs are reproduced within 1-11% (§3.8).

## 3.2 Parameter identifiability and uncertainty

Profile-likelihood analysis of all 26 parameters identifies six as
well-identified (relative depth > 5%: tp2, km, tm, kd, s2, at), with the
remaining parameters weakly identified or sloppy — the universal sloppiness
pattern typical of mechanistic systems-biology models. The parametric
bootstrap (N = 100) yields marginal confidence intervals that are consistent
with the profile-likelihood classification: tight for the well-identified
parameters and wide for the sloppy ones, as expected.

The exception is the factor XIII channel in Group II, which is structurally
under-determined rather than merely sloppy: 41 of the 100 bootstrap members
(41%) yield a negative Group II XIII R², and the ensemble distribution is
bimodal (Figure 2b), reflecting the optimizer settling in different basins
across resamples. This is a limitation of the information content of the
available Group II data, not a failure of the estimation pipeline — the cost
is otherwise stable across members. For downstream predictions we therefore
report full-ensemble CI bands; where a conservative XIII interpretation is
needed, a good-basin subset (n = 27 members with Group II XIII R² ≥ 0.3,
the same criterion used in the virtual experiments) provides a tighter band.

We tested sensitivity to the per-observable normalization by replacing the range-based scale factors with per-group standard deviations (which upweights G2 XIII by ~24x). At the baseline parameter point this lifts XIII G2 R² from 0.08 to 0.93 (single seed). However, under parametric bootstrap, the fraction of iterations with XIII G2 R² < 0 increases from 41% (range-based) to ~83% (per-group-std), indicating that the improved normalization sharpens rather than resolves the multi-modal landscape in the XIII channel. The structural under-determination of the {ax, cx, bx, kx} manifold is therefore robust to normalization choice (Supplementary, Analysis 34).

The identifiability results are shown in Figure 2.

**Figure 2.** Parameter identifiability and uncertainty from the 100-member bootstrap ensemble. (a) Coefficient of determination R² for all six observables in both groups (median, 95% CI). Eleven of the twelve intervals are tight and high; factor XIII in Group II is the sole wide interval, spanning negative values — the signature of its structural under-determination. (b) Distribution of the factor XIII (Group II) R² across the ensemble; 41% of members fall below zero (computed from the same 100 members). The bimodal shape reflects optimizer basin-switching in the XIII channel. R² is computed identically to the ensemble aggregation, so the two panels share one source of truth.
**Table 1.** Estimates and 95% bootstrap confidence intervals for the six well-identified parameters (profile-likelihood relative depth > 5%). Median and CI are from the 100-member ensemble. “Well-identified” refers to profile-likelihood depth (local curvature of the cost surface); the bootstrap CIs for kd and s2 are wider, reflecting a long right tail in the global resample distribution (the multi-scale cost-surface structure). Estimates for all 26 parameters are given in Supplementary Table S2.

| Parameter | Median [95% CI] | Role |
|---|---|---|
| tp2 | 9.217 [8.889, 10.034] | Peak time of the inflammatory pulse (days) |
| km | 4.918 [3.462, 5.734] | Group II rate modifier (myelosan effect on rate constants) |
| tm | 0.427 [0.392, 0.467] | Group II timing modifier (myelosan effect on pulse timing) |
| kd | 0.264 [0.218, 1.054] | Degranulation recovery rate |
| s2 | 1.757 [1.513, 2.712] | Width of the inflammatory pulse |
| at | 5.659 [4.893, 6.437] | Thrombin / inducer-pulse coefficient |

## 3.3 Mechanism split — neutrophil vs vessel contributions

The coagulation dynamics were decomposed into vessel-mediated and neutrophil-mediated contributions using a biologically-derived prior on the day-2 (G1) neutrophil share. The prior targets were estimated independently from the day-1 neutrophil-attributable fraction (ΔG1−ΔG2)/ΔG1 (recalc 0.24, fibrinogen 0.76, factor XIII 0.82); the derivation is well-posed because the two groups have near-identical hemostatic baselines (recalcification 78.7 vs 78.0 s; fibrinogen 58.2 vs 58.3 mg%; factor XIII 100.0 vs 93.2%), so myelosan altered neutrophil numbers without shifting baseline hemostasis. Imposing this prior (W_SPLIT = 2.0) yields fitted day-2 fractions of 0.240 [0.225, 0.249] for recalcification (vessel-dominant), 0.759 [0.738, 0.777] for fibrinogen, and 0.806 [0.777, 0.844] for factor XIII (both neutrophil-dominant). The prior is required for identifiability: without it, the recalcification fraction is non-identifiable across optimizer seeds (0.34–0.48) and the decomposition is not unique (Supplementary, W-sweep). The decomposition is validated post-hoc by superior held-out (G2) fit relative to unconstrained alternatives (+2–7 percentage points R²_G2). We therefore present these fractions as a prior-regularized, held-out-validated decomposition that quantifies and is consistent with the neutrophil hypothesis, rather than as a prior-free inference. We note one transparency caveat: for fibrinogen, an unconstrained fit places the neutrophil fraction near 0.05; the 0.76 value is the imposed day-1-derived prior target, not a feature independently reproduced by the day-2 fibrinogen dynamics.

The strong neutrophil contribution to factor XIII (~80%) is consistent with the azurophilic-granule storage hypothesis: degranulating neutrophils release pre-stored F.XIII into circulation, where it is rapidly consumed in the coagulation cascade. The vessel-dominant contribution to recalcification (~76% vessel) is consistent with the rapid onset of hypocoagulation following inducer administration, before neutrophil-mediated effects have time to develop.

The decomposition is shown in Figure 3.

**Figure 3.** Mechanism-split decomposition: neutrophil-attributable fraction of each coagulation channel at Group I day 2. Median and 95% CI from the 100-member bootstrap ensemble. The decomposition is prior-regularized (W_SPLIT = 2.0): target fractions (recalcification 0.24, fibrinogen 0.76, factor XIII 0.82) were derived independently from the day-1 (ΔG1−ΔG2)/ΔG1 ratios and imposed as soft constraints. Narrow CIs reflect both data consistency and prior strength. For fibrinogen, an unconstrained fit (W = 0) places the neutrophil fraction near 0.05; the 0.76 value is the imposed prior target, validated by the superior held-out Group II fit. Dashed vertical lines (full plot height) mark the prior targets for reference; each channel's CI sits on its target, with factor XIII pulled marginally below (median 0.806 vs target 0.82).

**Table 2.** Mechanism-split decomposition: neutrophil-attributable fraction of each coagulation channel at Group I day 2. Prior targets are the day-1 (ΔG1−ΔG2)/ΔG1 ratios imposed as soft constraints (W_SPLIT = 2.0); fitted values are the median and 95% CI across the 100-member bootstrap ensemble.

| Channel | Prior target | Fitted median [95% CI] | Interpretation |
|---|---|---|---|
| Recalcification time | 0.24 | 0.240 [0.225, 0.249] | Vessel-dominant |
| Fibrinogen | 0.76 | 0.759 [0.738, 0.777] | Neutrophil-dominant |
| Factor XIII | 0.82 | 0.806 [0.777, 0.844] | Neutrophil-dominant |

## 3.4 Robustness validation

Leave-one-out cross-validation reveals that Group I predictions are robust to removal of any single timepoint (median PRESS = 6.5 across 6 observables; worst case t=11, PRESS = 24.5, reflecting the critical role of peak DIC observation). Group II predictions are more sensitive to individual timepoint removal (median PRESS = 21.5), consistent with the smaller sample size (8 informative timepoints vs 15 in Group I). The high PRESS at G2 t=1 (76.6, dominated by AP channel) identifies early AP dynamics as the least constrained aspect of the G2 fit — a direct consequence of having only one observation (t=1) between AP onset and the first post-onset measurement (t=2). These results characterize the information content of the experimental design, not model overfitting: all LOO refits converge to costs within 10% of baseline (range 0.94-1.06), indicating stable parameter identification.

Model sensitivity to neutrophil count input was assessed using three perturbation protocols: deterministic scaling (α ∈ {0.8, 0.9, 1.0, 1.1, 1.2}), and stochastic per-timepoint lognormal noise at CV=10% and CV=20% (N=20 each). Aggregate G1 fit quality remained stable across all perturbations (R² ∈ [0.78, 0.83]). G2 fit quality showed sensitivity to XIII channel parameters as expected from their profile likelihood classification (§3.2), but stochastic perturbation did not produce systematic shifts in well-identified parameters (km, tm, cf, kd). The non-monotonic α-scan pattern (R²_G2 = 0.65, 0.68, 0.65, 0.74, 0.77 at α = 0.8, 0.9, 1.0, 1.1, 1.2) reflects the multi-modal optimization landscape characterized in earlier analyses, not biological signal about neutrophil count accuracy. Doubling the noise level from CV=10% to 20% produced only marginally wider cost CIs (0.140 vs 0.139), demonstrating sub-linear sensitivity for well-identified parameters.

## 3.5 Myelosan dose-response

Virtual experiments using the 100-member bootstrap ensemble show that myelosan-induced kinetic modification of neutrophil-derived rate constants reduces peak hypocoagulation by 7-fold and integrated coagulation disruption by 2.5-fold, relative to the same neutrophil profile without kinetic modification (phase diagram in (km, tm) space). The observed experimental dose (km=4.93, tm=0.43) lies on the dose-response curve at intermediate severity. The kinetic modification alone, applied to the G2 neutrophil profile, does not reproduce G1-level hypocoagulation severity: substituting the G1 neutrophil profile into the model (§3.8) yields an ~22-fold greater peak hypocoagulation. This indicates that the protective effect of myelosan operates substantially through the reduction of neutrophil abundance, not through kinetic modification alone.

The dose-response phase diagrams are shown in Figure 4.

**Figure 4.** Myelosan dose-response phase diagrams across the (km, tm) parameter space. Each cell: median across the 100-member bootstrap ensemble. (a) Peak hypocoagulation (max Δrecalcification, s); contour lines at 10, 20, 30, 40 s. (b) Factor XIII nadir (min ΔXIII activity, %). (c) Peak neutrophil load (max gHn), the mechanistic driver of DIC severity. Circle: no kinetic myelosan effect (km=1, tm=1); star: observed G2 dose (km=4.93, tm=0.43). The G2 neutrophil profile is retained throughout; severity reflects kinetic modification only. All three metrics decrease monotonically with increasing km (verified: 15/15 timing-columns monotonic for each metric), confirming that rate-constant suppression is the primary determinant of DIC attenuation within the G2 neutrophil context.
A dose-response slice at the observed timing is shown in Figure 5.

**Figure 5.** Dose-response slice: peak hypocoagulation (max Δrecalcification) versus the rate modifier km at fixed timing modifier tm ≈ 0.45 (the nearest grid value to the observed G2 timing modifier tm = 0.43). Median (blue line) and 95% CI (band) across the 100-member bootstrap ensemble. The dotted line marks the no-myelosan severity (km = 1, median 92 s); the dashed line and triangle mark the observed G2 operating point (km = 4.93), where the median peak hypocoagulation is 7.4 s, consistent with the observed Group II outcome (§3.6). The CI band narrows with increasing km — from [65, 110] s at km = 1 to [1, 14] s near km = 5 — indicating that the predicted attenuation is more certain at higher kinetic suppression. This is the dose-axis detail that the Figure 4 heatmaps cannot resolve.

## 3.6 Therapeutic window

Myelosan intervention provides near-complete DIC attenuation when administered within 2.5 days post-injury (max Δrecalcification 7-8 s, comparable to the observed G2 outcome). A critical half-day transition occurs between days 2.5 and 3, during which severity doubles (max Δrecalcification 7.9 → 14.4 s). Beyond day 3, myelosan retains partial protective effect — reducing peak severity 2-3-fold relative to no intervention — but cannot prevent acute DIC onset. The therapeutic window thus comprises a prevention phase (0-2.5 days) and a mitigation phase (2.5-6+ days).

Notably, intervention at t=0 and t=1 produce indistinguishable outcomes, indicating that the inducer toxicity pulse V(t) (peaking at τ_v=1.5 days, reflecting the time to peak ethylphenacin effect) does not produce sufficient hyaline accumulation in the first 24 hours to trigger the DIC cascade independently. This is consistent with the expected latency between anticoagulant exposure and onset of measurable coagulopathy.

The therapeutic window is shown in Figure 6.

**Figure 6.** Therapeutic window: DIC severity versus myelosan intervention time, from the 100-member bootstrap ensemble (median, 95% CI band). (a) Peak hypocoagulation (max Δrecalcification), (b) factor XIII nadir (min ΔXIII), (c) peak neutrophil load (max gHn). The shaded band (days 2.5-3) marks the critical transition, across which peak hypocoagulation roughly doubles (median 7.9 → 14.4 s). The dotted line on each panel is the no-intervention reference. All three metrics share the same window: a prevention phase (0-2.5 days, where early timings give near-identical low severity — reflecting the latency of the inducer pulse V(t)) and a mitigation phase (2.5-6+ days), where intervention still reduces severity 2-3-fold relative to no intervention but cannot prevent acute onset. The transition is reported as occurring between days 2.5 and 3 (the sampled timings) rather than at a single interpolated value.
Temporal metrics (time to peak gHn, time to recovery, acute-phase duration) vary within the bootstrap CI across all intervention timings, indicating that myelosan timing modulates the severity of the DIC episode but not its temporal structure (Supplementary Figure S5).

## 3.7 Dose × timing thresholds

A focused virtual experiment tested whether dose × timing operate as continuous trade-offs or as independent thresholds. Doubling the myelosan dose at late intervention (t=4 days, km=10 instead of 4.93) produced no measurable improvement in peak severity (28.0 vs 28.2), indicating a dose ceiling once the DIC cascade is established. Conversely, halving the dose at optimal timing (t=0, km=2.5) produced markedly worse outcome (34.0 vs 7.1), exceeding even the severity of late full-dose intervention. The protective effect of myelosan thus requires both adequate dose (above the kr-suppression threshold) AND timely administration (before cascade lock-in), not either alone.

**Table 3.** Dose × timing combinations, testing whether dose and timing trade off continuously or act as independent thresholds. Peak hypocoagulation (max Δrecalc, s) is median [95% CI] from the 100-member ensemble. Each combination is compared with its full-dose reference at the same timing.

| Scenario | Dose (km) | Timing (d) | Max Δrecalc [95% CI] | Reference (full dose, same timing) | Outcome |
|---|---|---|---|---|---|
| Double dose, late | 10.0 | 4 | 28.0 [0.0, 38.9] | 28.2 (full dose, t=4) | No improvement (dose ceiling) |
| Half dose, early | 2.5 | 0 | 34.0 [22.7, 44.0] | 7.1 (full dose, t=0) | Markedly worse (dose floor) |
| _Full dose, early (ref)_ | 4.93 | 0 | 7.1 [0.6, 14.7] | — | Prevention |
| _Full dose, late (ref)_ | 4.93 | 4 | 28.2 [1.5, 39.0] | — | Mitigation |
| _No intervention (ref)_ | — | — | 75.6 [60.5, 92.0] | — | Untreated |

---

## 3.8 External validation against the observed mortality pattern

The model was validated against the experimentally observed mortality
contrast (30% in Group I, days 10-12; 0% in Group II) by simulating pure
Group I dynamics (G1 neutrophil profile, no myelosan) through the bootstrap
ensemble. The model reproduces severe hypocoagulation in Group I (peak
Δrecalcification 147 s [CI95 122-176], factor XIII nadir -77%, fibrinogen
nadir -58 mg%) versus near-absent hypocoagulation in the myelosan-modified
Group II baseline (peak Δrecalcification ~7 s), a 22-fold separation
consistent with the observed mortality difference. The peak occurs at
day 11, matching the observed timing of both the hypocoagulation maximum
and the mortality window (days 10-12).

Channel-level agreement is differential: the factor XIII nadir matches
observation within 1% (model -77.1% vs observed -76.7%) and the fibrinogen
nadir within 11% (model -58.3 vs observed -52.6 mg%; the early
fibrinogen rise is underestimated more strongly, see §4.6), while the
recalcification peak is
underestimated by ~29% (147 vs 207 s). The amplitude underestimation is
confined to the vessel-driven channels (recalcification peak and the early
fibrinogen rise) rather than being systemic — the XIII and AP nadirs and
the peak timing are reproduced accurately; it is consistent with the
joint-fit architecture penalty (§2.3) and is reported as a known
limitation (§4.6). The validation is therefore qualitative and
directional — the model reproduces the timing and the group separation
underlying the observed mortality — rather than a quantitative mortality
model.

**Table 4.** Group I versus Group II severity and validation against the observed Group I values. Modeled values are median [95% CI] from the 100-member ensemble (pure Group I dynamics: G1 neutrophil profile, no myelosan; and the myelosan-modified G2 baseline). Observed Group I values are from the dissertation tables. Agreement is reported as the model/observed relation.

| Metric | G1 model [95% CI] | G1 observed | Agreement | G2 model [95% CI] |
|---|---|---|---|---|
| Peak hypocoagulation (max Δrecalc) (s) | 147 [122, 176] | 207 | model 29% below obs | 7 [3, 11] |
| Factor XIII nadir (min ΔXIII) (%) | -77.1 [-94.4, -61.4] | -76.7 | within 1% | -13.8 [-19.7, -7.3] |
| Fibrinogen nadir (min Δfib) (mg%) | -58.3 [-69.1, -46.4] | -52.6 | within 11% | -1.4 [-8.1, 0.0] |
| Time of peak (t_max recalc) (d) | 11 [10, 11] | 11 | exact | 5 [5, 6] |
| **G1/G2 separation (max Δrecalc)** | **22.2×** | — | — | — |

# 4. Discussion

**[OLENA — to be drafted; Oleksiy provides bullet points below as scaffolding]**

Suggested structure:

4.1. **Summary of findings.** Restate four-pillar narrative: (i) a prior-regularized mechanism split that quantifies and is consistent with (not independently confirms) the neutrophil contribution; (ii) quantified myelosan kinetic effect 2.5-7×; (iii) narrow therapeutic window with sharp 2.5-3 day transition; (iv) dose-timing thresholds requiring both.

4.2. **Biological interpretation of mechanism split.** Vessel-dominant recalcification + neutrophil-dominant fib/XIII — discuss in light of known DIC pathogenesis. Connection to azurophilic-granule F.XIII storage (Boiarchuk 2008).

4.3. **Implications for myelosan therapy.** Translation of dose-response findings to clinical/veterinary practice. The G2-observed dose is near the plateau of efficacy — additional dose escalation unlikely to help. The therapeutic window concept: timing matters as much as dose. Practical guidance for anticoagulant-rodenticide intoxication presented at different times post-exposure. The vitamin-K-antagonist mechanism of ethylphenacin suggests clinical parallels with warfarin reversal therapy [OLENA — expand clinical context: ethylphenacin vs warfarin half-life, tissue selectivity, and limits of the analogy].

4.4. **The two-phase nature of the therapeutic window.** Discuss biological mechanism: prevention phase (0-2.5 days) = before cascade lock-in; mitigation phase (2.5-6+) = limiting damage extent. Half-day transition reflects sharp threshold in AP/Hn accumulation.

4.5. **Count reduction vs. kinetic modification.** Pure-G1 simulation (§3.8) produces ~22-fold greater hypocoagulation severity than the G2 kinetic scenario, indicating that myelosan protection operates substantially through reduction of neutrophil abundance rather than kinetic modification alone. Discuss in light of the observed mortality pattern (30% G1 vs 0% G2). Note the model limitation: the recalcification amplitude is underestimated ~30% relative to observation, though peak timing and the XIII/fibrinogen nadirs are reproduced within 1-11% (§3.8).

4.6. **Limitations.** XIII channel structural under-determination (robust to normalization, §3.2); idealized myelosan pharmacokinetics (instantaneous effect); neutrophil interpolator extrapolation; veterinary translation caveats. Two vessel-driven channels (recalcification, fibrinogen) underestimate the early hypercoagulation-phase amplitude while reproducing the late nadir well. For fibrinogen the cause is explicit in the channel decomposition (Supplementary, fib channel decomposition at baseline): the fibrinogen output is a small difference of two large opposing terms, the acid-phosphatase contribution (cf·AP) and the neutrophil-dependent contribution (−bf·gHn), each roughly four-fold larger in magnitude than their sum near days 5-7. Minor phase mismatches between AP and gHn in that window therefore produce a non-monotonic intermediate profile, and the fast-rising −bf·gHn term suppresses the early fibrinogen rise relative to observation (model +16 vs +28 mg% at day 1). This is a consequence of the fixed, jointly-estimated parameterization and does not affect the channels carrying the main findings.

4.7. **Future directions.** Additional G2 timepoints to constrain XIII; explicit PK/PD layer for myelosan; combined intervention exploration.

---

# 5. Conclusions

**[PLACEHOLDER — 1 paragraph fill last]**

Brief restatement of:
- Model successfully decomposes neutrophil vs vessel contributions to DIC.
- Myelosan kinetic effect quantified and bracketed.
- Therapeutic window characterized: two-phase, sharp half-day transition at 2.5-3 days.
- Both dose AND timing thresholds required for protection.

---

# References

*Intermediate format (author, year, title, journal, volume:pages, DOI).
Final styling to JTB at submission. Entries marked [TO FIND] still need a
verified source — not yet confirmed, deliberately not fabricated.*

**Primary experimental sources (Boiarchuk series)**

1. Boiarchuk OD (1998) Experimental model of DIC syndrome. Visnyk Problem Biolohii i Medytsyny (7):132–138. [dissertation basis; full protocol tables]
2. Boiarchuk OD, Koval SB, Lunina NV (2000) Changes in the lysosomal apparatus of neutrophilic leukocytes in disseminated intravascular coagulation syndrome. Fiziolohichnyi Zhurnal 46(3):72–77.
3. Boiarchuk OD (2008) Changes in neutrophil activity during formation of disseminated intravascular coagulation syndrome. Naukovyi Visnyk Mykolaivskoho Derzhavnoho Universytetu im. V.O. Sukhomlynskoho 23(3):14–17.
4. Boiarchuk OD, Lunina NV (2012) Histochemical features of neutrophils in DIC syndrome. Visnyk LNU imeni Tarasa Shevchenka 17(252):[pages TO FIND].
5. Boiarchuk OD (2013) Dynamics of granulocyte acid phosphatase in DIC syndrome. Visnyk LNU imeni Tarasa Shevchenka 19(278), Part I:[pages TO FIND].
6. Boiarchuk OD (2023) Features of neutrophils in DIC syndrome. InterConf (Orléans). doi:10.51582/interconf.19-20.04.2023.042

**Methods (hemostasis, lysosomal apparatus)**

7. Pigarevsky VE (1975) The lysosomal-cationic test. Patologicheskaya Fiziologiya i Eksperimentalnaya Terapiya (3):86–88.
8. Baluda VP, Barkagan ZS, Goldberg ED (eds., 1980) Laboratory methods for studying the hemostatic system. Tomsk, 314 pp.
9. Myelosan (busulfan) pharmacology — granulocytopoiesis suppression protocol. [TO FIND: primary pharmacology reference; protocol details from author commentary, Cherstvoy/AO Oktyabr source to confirm]

**Identifiability and uncertainty methodology**

10. Raue A, Kreutz C, Maiwald T, Bachmann J, Schilling M, Klingmüller U, Timmer J (2009) Structural and practical identifiability analysis of partially observed dynamical models by exploiting the profile likelihood. Bioinformatics 25(15):1923–1929. doi:10.1093/bioinformatics/btp358
11. Kreutz C, Raue A, Kaschek D, Timmer J (2013) Profile likelihood in systems biology. FEBS Journal 280(11):2564–2571. doi:10.1111/febs.12276
12. Gutenkunst RN, Waterfall JJ, Casey FP, Brown KS, Myers CR, Sethna JP (2007) Universally sloppy parameter sensitivities in systems biology models. PLoS Computational Biology 3(10):e189. doi:10.1371/journal.pcbi.0030189
13. Bootstrap confidence intervals for dynamical-model parameters. [TO FIND: Efron & Tibshirani 1993, An Introduction to the Bootstrap, or a systems-biology bootstrap-CI reference]
14. Cross-validation / PRESS for model assessment. [TO FIND: Stone 1974, J. R. Stat. Soc. B 36(2):111–147, to verify]

**Inducer toxicology (anticoagulant rodenticides)**

15. Watt BE, Proudfoot AT, Bradberry SM, Vale JA (2005) Anticoagulant rodenticides. Toxicological Reviews 24(4):259–269.
16. Hadler MR, Buckle AP (1992) Forty-five years of anticoagulant rodenticides — past, present and future trends. Proceedings of the Fifteenth Vertebrate Pest Conference, Paper 36. University of California, Davis.

**DIC pathogenesis**

17. DIC pathogenesis review(s). [TO FIND: a current authoritative DIC review, e.g. Levi & ten Cate NEJM 1999 or a recent ISTH consensus, to verify]
18. Barkagan ZS, Momot AP — DIC pathogenesis/diagnosis/therapy. [TO FIND: full citation; cited in Boiarchuk 2012 ref list as Vestn. Gematol. 2005;1(2):5–14, to verify]

---

# Supplementary Information

## S1. Full ODE formulation and observable equations

Will be auto-generated from `src/model.py` source.

## S2. Parameter estimation pipeline and full estimates

DE settings, polish sequence, convergence criteria. Reference `src/fit.py`.

**Table S2.** Estimates and 95% bootstrap confidence intervals for all 26 model parameters (100-member ensemble), sorted by relative CI width (an identifiability spectrum: tightest first). Parameters flagged † are the six classified as well-identified by profile likelihood (relative depth > 5%). Relative width is (CI upper − lower) / |median|; entries with median near zero (width reported as —) are unconstrained in sign.

| Parameter | Median [95% CI] | Rel. width | Well-id. |
|---|---|---|---|
| tp2 | 9.217 [8.889, 10.03] | 0.12× | † |
| tm | 0.4267 [0.3918, 0.4675] | 0.18× | † |
| at | 5.659 [4.893, 6.437] | 0.27× | † |
| ar | 34.74 [28, 40.01] | 0.35× |  |
| km | 4.918 [3.462, 5.734] | 0.46× | † |
| cr | 35.61 [27.55, 45.11] | 0.49× |  |
| cx | 545.8 [294.8, 600] | 0.56× |  |
| s2 | 1.757 [1.513, 2.712] | 0.68× | † |
| ax | 47.21 [25.63, 67.73] | 0.89× |  |
| bf | 6.219 [2.335, 7.999] | 0.91× |  |
| cf | 99.68 [59.87, 154.7] | 0.95× |  |
| af | 9.949 [5.527, 15.03] | 0.96× |  |
| kx | 2.604 [1.408, 4.047] | 1.01× |  |
| bx | 34.07 [11.77, 49.01] | 1.09× |  |
| br | 8.876 [3.043, 13.49] | 1.18× |  |
| bt | 0.5546 [0.1854, 0.8652] | 1.23× |  |
| kcl | 12.01 [3.372, 18.25] | 1.24× |  |
| krl | 12.69 [4.001, 19.97] | 1.26× |  |
| knd | 6.167 [1.94, 9.999] | 1.31× |  |
| a2 | 3.423 [2.654, 8.312] | 1.65× |  |
| kna | 257.4 [80.92, 644.6] | 2.19× |  |
| kd | 0.2635 [0.2179, 1.054] | 3.17× | † |
| Hm | 290.5 [11.11, 999.8] | 3.40× |  |
| kca | 3.834 [0.1334, 33.34] | 8.66× |  |
| kr | 0.247 [0.1802, 2.693] | 10.17× |  |
| df | 1.037 [0.1221, 13.01] | 12.43× |  |

## S3. Profile likelihood plots — all 26 parameters

26-panel figure. Reference `analyses/09_profile_likelihood/`.

## S4. Bootstrap diagnostic plots

Per-iteration cost distribution, parameter CI shrinkage with N, basin classification of XIII channel. Reference `analyses/22_predictive_check/`. The per-group-std normalization sensitivity bootstrap (§3.2) is reported in `analyses/34_pergroupstd_bootstrap/`: under per-group std the XIII G2 R² < 0 fraction rises to ~83% (vs 41% range-based), confirming the XIII under-determination is robust to normalization choice rather than an artifact of it.

## S5. Intervention-timing trajectories and temporal metrics

Per-scenario gHn trajectories and the temporal metrics (time to peak gHn, time to recovery, acute-phase duration) versus intervention timing. The temporal metrics vary within the bootstrap CI across all timings (median ranges below the mean CI widths), i.e. timing modulates severity (§3.6, Figure 6) but not the temporal structure of the episode. Reference `analyses/31_intervention_timing/` (figures/fig3_trajectories.png and results/summary_by_timing.json).

## S6. Phase diagrams for all six severity metrics

Including auc_recalc and max_gHn variants not in main text. Reference `analyses/30_myelosan_dose/results/phase_diagram_*.json`.

## S7. Reproducibility

Code repository, commit hashes for tagged phases, environment specification (`environment.yml`).

---

**Document log:**
- 2026-05-12: skeleton v1 created. Methods and Results sections populated with manuscript-ready paragraphs from FINDINGS files (analyses 22, 20, 21, 30, 31, 32). Introduction, Discussion, Conclusions left as placeholders for Olena. Figure/table placeholders marked.
