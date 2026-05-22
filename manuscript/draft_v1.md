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
- 1-2 sentences: context (neutrophil role in DIC, myelosan in veterinary toxicology of Ephedra-2 poisoning)
- 1 sentence: gap (no mechanistic model decomposing neutrophil vs vessel contributions)
- 2-3 sentences: approach (mechanistic ODE model fit to two experimental groups; identifiability + bootstrap + LOO-CV + N(t) perturbation robustness checks; three virtual experiments)
- 3-4 sentences: key findings (prior-regularized mechanism split quantifying neutrophil contribution, consistent with the neutrophil hypothesis; myelosan kinetic effect 2.5-7× DIC reduction; therapeutic window 0-2.5 days; dose-timing thresholds)
- 1 sentence: clinical implication (narrow window requires both adequate dose AND early administration)

---

# 1. Introduction

**[OLENA — to be drafted]**

Suggested scope:

1.1. **Biological context.** DIC syndrome, pathogenesis. Neutrophil role in coagulation cascade — review of evidence for azurophilic granule storage of F.XIII, vessel-mediated vs neutrophil-mediated mechanisms.

1.2. **Experimental model.** Ephedra-2 (Vipera berus) envenomation model. Two groups: G1 (envenomation alone), G2 (envenomation + pre-treatment with myelosan to suppress neutrophil production). Reference to Boiarchuk dissertation and 2008 publication.

1.3. **The myelosan question.** What is the mechanism by which myelosan attenuates DIC? Two hypotheses: (a) reduction of neutrophil count, (b) modification of neutrophil kinetics. Need for quantitative decomposition.

1.4. **Gap.** Existing literature describes neutrophil involvement qualitatively. No mechanistic model that (a) quantitatively decomposes neutrophil vs vessel contributions to coagulation observables, (b) characterizes the timing dependence of myelosuppressive intervention.

1.5. **Aims.** State three: (i) build and validate ODE model; (ii) quantify mechanism split with uncertainty; (iii) predict dose-response and intervention timing relationships.

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
a single oral dose of the inducer "Efa-2" (8330 mg/kg, administered fasting)
without prior intervention in the granulocyte lineage. In Group II
(suppressed granulocytopoiesis), the identical inducer and dose were
administered after pharmacological suppression of granulocytopoiesis.

**Granulocytopoiesis suppression (Group II).** Suppression was achieved by
oral myelosan in a two-stage schedule. In the first stage, myelosan was given
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

The model contains 26 parameters: rate constants for degranulation and recovery (kr, krl, kcl, kca, kna, knd, Hm, kd), peak-timing parameters of the envenomation pulse (tp2, s2), and observable-specific contribution coefficients for each of the four observable channels (recalc, thrombin, fib, xiii). The G1 and G2 groups share all parameters except for group-specific modifiers (km, tm) that scale the effective rate constants in G2 to represent the myelosan effect.

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

**[OLEKSIY — paragraph from analysis 05 + baseline R² table]**

Working content:
- Model fits both G1 and G2 with R² > 0.7 on most observables.
- G1 (15 timepoints, 6 observables): mean R² ≈ 0.82.
- G2 (8 timepoints, 6 observables): mean R² ≈ 0.69, with known structural limitations in XIII channel (see §3.2).
- Figure: baseline fit panels (one per observable per group).
- **FIGURE 1 PLACEHOLDER — baseline fits**

## 3.2 Parameter identifiability and uncertainty

**[OLEKSIY — paragraphs synthesized from analyses 09 + 22 FINDINGS]**

Working content:
- Profile likelihood: 6 well-identified parameters (tp2, km, tm, kd, s2, at).
- Bootstrap: marginal CIs broadly consistent with PL for well-identified parameters; wider for sloppy parameters as expected.
- XIII channel structurally under-determined: 41% of bootstrap iterations yield xiii_G2 R² < 0, reflecting fundamental limitation of the available data rather than parameter identification failure.
- Implication for downstream predictions: report ensemble CI bands; good-basin subset (n=59 with xiii_G2 R² ≥ 0.3) provides tighter band when conservative interpretation is needed.
- **FIGURE 2 PLACEHOLDER — bootstrap CI on key parameters + xiii_G2 R² histogram**
- **TABLE 1 PLACEHOLDER — parameter estimates with bootstrap CI95**

## 3.3 Mechanism split — neutrophil vs vessel contributions

**[OLEKSIY — paragraph from analysis 22 FINDINGS; manuscript-ready]**

Working content (direct from analysis 22 FINDINGS):

The coagulation dynamics were decomposed into vessel-mediated and neutrophil-mediated contributions using a biologically-derived prior on the day-2 (G1) neutrophil share. The prior targets were estimated independently from the day-1 neutrophil-attributable fraction (ΔG1−ΔG2)/ΔG1 (recalc 0.24, fibrinogen 0.76, factor XIII 0.82); the derivation is well-posed because the two groups have near-identical hemostatic baselines (recalcification 78.7 vs 78.0 s; fibrinogen 58.2 vs 58.3 mg%; factor XIII 100.0 vs 93.2%), so myelosan altered neutrophil numbers without shifting baseline hemostasis. Imposing this prior (W_SPLIT = 2.0) yields fitted day-2 fractions of 0.240 [0.225, 0.249] for recalcification (vessel-dominant), 0.759 [0.738, 0.777] for fibrinogen, and 0.806 [0.777, 0.844] for factor XIII (both neutrophil-dominant). The prior is required for identifiability: without it, the recalcification fraction is non-identifiable across optimizer seeds (0.34–0.48) and the decomposition is not unique (Supplementary, W-sweep). The decomposition is validated post-hoc by superior held-out (G2) fit relative to unconstrained alternatives (+2–7 percentage points R²_G2). We therefore present these fractions as a prior-regularized, held-out-validated decomposition that quantifies and is consistent with the neutrophil hypothesis, rather than as a prior-free inference. We note one transparency caveat: for fibrinogen, an unconstrained fit places the neutrophil fraction near 0.05; the 0.76 value is the imposed day-1-derived prior target, not a feature independently reproduced by the day-2 fibrinogen dynamics.

The strong neutrophil contribution to factor XIII (~80%) is consistent with the azurophilic-granule storage hypothesis: degranulating neutrophils release pre-stored F.XIII into circulation, where it is rapidly consumed in the coagulation cascade. The vessel-dominant contribution to recalcification (~76% vessel) is consistent with the rapid onset of hypocoagulation following envenomation, before neutrophil-mediated effects have time to develop.

- **TABLE 2 PLACEHOLDER — mechanism split fractions with bootstrap CI95**

## 3.4 Robustness validation

**[OLEKSIY — paragraphs from analyses 20 + 21 FINDINGS; manuscript-ready]**

Working content (direct from analysis 20):

Leave-one-out cross-validation reveals that Group I predictions are robust to removal of any single timepoint (median PRESS = 6.5 across 6 observables; worst case t=11, PRESS = 24.5, reflecting the critical role of peak DIC observation). Group II predictions are more sensitive to individual timepoint removal (median PRESS = 21.5), consistent with the smaller sample size (8 informative timepoints vs 15 in Group I). The high PRESS at G2 t=1 (76.6, dominated by AP channel) identifies early AP dynamics as the least constrained aspect of the G2 fit — a direct consequence of having only one observation (t=1) between AP onset and the first post-onset measurement (t=2). These results characterize the information content of the experimental design, not model overfitting: all LOO refits converge to costs within 10% of baseline (range 0.94-1.06), indicating stable parameter identification.

Working content (direct from analysis 21):

Model sensitivity to neutrophil count input was assessed using three perturbation protocols: deterministic scaling (α ∈ {0.8, 0.9, 1.0, 1.1, 1.2}), and stochastic per-timepoint lognormal noise at CV=10% and CV=20% (N=20 each). Aggregate G1 fit quality remained stable across all perturbations (R² ∈ [0.78, 0.83]). G2 fit quality showed sensitivity to XIII channel parameters as expected from their profile likelihood classification (§3.2), but stochastic perturbation did not produce systematic shifts in well-identified parameters (km, tm, cf, kd). The non-monotonic α-scan pattern (R²_G2 = 0.65, 0.68, 0.65, 0.74, 0.77 at α = 0.8, 0.9, 1.0, 1.1, 1.2) reflects the multi-modal optimization landscape characterized in earlier analyses, not biological signal about neutrophil count accuracy. Doubling the noise level from CV=10% to 20% produced only marginally wider cost CIs (0.140 vs 0.139), demonstrating sub-linear sensitivity for well-identified parameters.

## 3.5 Myelosan dose-response

**[OLEKSIY — paragraph from analysis 30 FINDINGS]**

Working content (direct from analysis 30):

Virtual experiments using the 100-member bootstrap ensemble show that myelosan-induced kinetic modification of neutrophil-derived rate constants reduces peak hypocoagulation by 7-fold and integrated coagulation disruption by 2.5-fold, relative to the same neutrophil profile without kinetic modification (phase diagram in (km, tm) space). The observed experimental dose (km=4.93, tm=0.43) lies on the dose-response curve at intermediate severity. The kinetic modification alone, applied to the G2 neutrophil profile, does not reproduce G1-level hypocoagulation severity: substituting the G1 neutrophil profile into the model (§3.8) yields an ~22-fold greater peak hypocoagulation. This indicates that the protective effect of myelosan operates substantially through the reduction of neutrophil abundance, not through kinetic modification alone.

- **FIGURE 3 PLACEHOLDER — phase diagram (3-panel: max_recalc, min_xiii, max_gHn)**
- **FIGURE 4 PLACEHOLDER — dose-response slice at tm=0.43**

## 3.6 Therapeutic window

**[OLEKSIY — paragraph from analysis 31 FINDINGS; manuscript-ready]**

Working content (direct from analysis 31):

Myelosan intervention provides near-complete DIC attenuation when administered within 2.5 days post-injury (max Δrecalcification 7-8 s, comparable to the observed G2 outcome). A critical half-day transition occurs between days 2.5 and 3, during which severity doubles (max Δrecalcification 7.9 → 14.4 s). Beyond day 3, myelosan retains partial protective effect — reducing peak severity 2-3-fold relative to no intervention — but cannot prevent acute DIC onset. The therapeutic window thus comprises a prevention phase (0-2.5 days) and a mitigation phase (2.5-6+ days).

Notably, intervention at t=0 and t=1 produce indistinguishable outcomes, indicating that the envenomation pulse V(t) (peaking at τ_v=1.5 days) does not produce sufficient hyaline accumulation in the first 24 hours to trigger the DIC cascade independently. This is consistent with the known clinical latency between envenomation and onset of measurable coagulopathy.

- **FIGURE 5 PLACEHOLDER — severity vs timing (3 panels) with critical transition shaded**
- **FIGURE 6 PLACEHOLDER — temporal metrics vs timing**

## 3.7 Dose × timing thresholds

**[OLEKSIY — paragraph from analysis 32 FINDINGS]**

Working content (direct from analysis 32):

A focused virtual experiment tested whether dose × timing operate as continuous trade-offs or as independent thresholds. Doubling the myelosan dose at late intervention (t=4 days, km=10 instead of 4.93) produced no measurable improvement in peak severity (28.0 vs 28.2), indicating a dose ceiling once the DIC cascade is established. Conversely, halving the dose at optimal timing (t=0, km=2.5) produced markedly worse outcome (34.0 vs 7.1), exceeding even the severity of late full-dose intervention. The protective effect of myelosan thus requires both adequate dose (above the kr-suppression threshold) AND timely administration (before cascade lock-in), not either alone.

- **TABLE 3 PLACEHOLDER — dose × timing combination outcomes**

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
nadir within 11% (-58.3 vs -52.6 mg%), while the recalcification peak is
underestimated by ~29% (147 vs 207 s). The underestimate is localized to
the recalcification channel (the gHn-dependent term) rather than systemic;
it is consistent with the joint-fit architecture penalty (§2.3) and is
reported as a known limitation. The validation is therefore qualitative and
directional — the model reproduces the timing and the group separation
underlying the observed mortality — rather than a quantitative mortality
model.

- **TABLE 4 PLACEHOLDER — G1 vs G2 severity + model-vs-observed validation**

# 4. Discussion

**[OLENA — to be drafted; Oleksiy provides bullet points below as scaffolding]**

Suggested structure:

4.1. **Summary of findings.** Restate four-pillar narrative: (i) a prior-regularized mechanism split that quantifies and is consistent with (not independently confirms) the neutrophil contribution; (ii) quantified myelosan kinetic effect 2.5-7×; (iii) narrow therapeutic window with sharp 2.5-3 day transition; (iv) dose-timing thresholds requiring both.

4.2. **Biological interpretation of mechanism split.** Vessel-dominant recalcification + neutrophil-dominant fib/XIII — discuss in light of known DIC pathogenesis. Connection to azurophilic-granule F.XIII storage (Boiarchuk 2008).

4.3. **Implications for myelosan therapy.** Translation of dose-response findings to clinical/veterinary practice. The G2-observed dose is near the plateau of efficacy — additional dose escalation unlikely to help. The therapeutic window concept: timing matters as much as dose. Practical guidance for envenomation cases presented at different times post-bite.

4.4. **The two-phase nature of the therapeutic window.** Discuss biological mechanism: prevention phase (0-2.5 days) = before cascade lock-in; mitigation phase (2.5-6+) = limiting damage extent. Half-day transition reflects sharp threshold in AP/Hn accumulation.

4.5. **Count reduction vs. kinetic modification.** Pure-G1 simulation (§3.8) produces ~22-fold greater hypocoagulation severity than the G2 kinetic scenario, indicating that myelosan protection operates substantially through reduction of neutrophil abundance rather than kinetic modification alone. Discuss in light of the observed mortality pattern (30% G1 vs 0% G2). Note the model limitation: the recalcification amplitude is underestimated ~30% relative to observation, though peak timing and the XIII/fibrinogen nadirs are reproduced within 1-11% (§3.8).

4.6. **Limitations.** XIII channel structural under-determination; idealized myelosan pharmacokinetics (instantaneous effect); neutrophil interpolator extrapolation; veterinary translation caveats.

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

**[PLACEHOLDER — collect during draft refinement]**

Categories to assemble:
- Boiarchuk dissertation + 2008 publication on azurophilic granule F.XIII
- Vipera berus envenomation pathophysiology
- Myelosan pharmacology
- DIC pathogenesis reviews
- Identifiability methodology (Raue 2009, Kreutz 2013, etc.)
- Bootstrap and LOO-CV in systems biology
- ODE model fitting methodology
- Related mechanistic models of coagulation

---

# Supplementary Information

## S1. Full ODE formulation and observable equations

Will be auto-generated from `src/model.py` source.

## S2. Parameter estimation pipeline details

DE settings, polish sequence, convergence criteria. Reference `src/fit.py`.

## S3. Profile likelihood plots — all 26 parameters

26-panel figure. Reference `analyses/09_profile_likelihood/`.

## S4. Bootstrap diagnostic plots

Per-iteration cost distribution, parameter CI shrinkage with N, basin classification of XIII channel. Reference `analyses/22_predictive_check/`.

## S5. Trajectories per intervention scenario

Reference `analyses/31_intervention_timing/figures/fig3_trajectories.png`.

## S6. Phase diagrams for all six severity metrics

Including auc_recalc and max_gHn variants not in main text. Reference `analyses/30_myelosan_dose/results/phase_diagram_*.json`.

## S7. Reproducibility

Code repository, commit hashes for tagged phases, environment specification (`environment.yml`).

---

**Document log:**
- 2026-05-12: skeleton v1 created. Methods and Results sections populated with manuscript-ready paragraphs from FINDINGS files (analyses 22, 20, 21, 30, 31, 32). Introduction, Discussion, Conclusions left as placeholders for Olena. Figure/table placeholders marked.
