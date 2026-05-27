*[Working title]* A mechanistic model of neutrophil-driven disseminated intravascular coagulation reveals a narrow therapeutic window for myelosuppressive intervention

# Abstract

**[PLACEHOLDER — to be written last, ~250 words.]**
Scope: context (neutrophil role in DIC; busulfan acting on the neutrophil compartment; the ethylphenacin anticoagulant-rodenticide DIC model) → gap (no mechanistic model decomposing neutrophil vs vessel contributions) → approach (a mechanistic ODE model fit jointly to two experimental groups; identifiability, bootstrap, leave-one-out and N(t)-perturbation robustness checks; three virtual experiments) → key findings (a prior-regularized mechanism split that quantifies and is consistent with the neutrophil contribution; a 2.5–7-fold kinetic attenuation of DIC by busulfan; a therapeutic window of 0–2.5 days; independent dose and timing thresholds) → clinical implication (the narrow window requires both adequate dose and early administration).

# 1. Introduction

Disseminated intravascular coagulation (DIC) is a systemic, acquired disorder of hemostasis in which widespread activation of coagulation leads first to microvascular thrombosis and consumption of clotting factors, and subsequently to a bleeding tendency as those factors are exhausted. DIC is not a primary disease but a complication of shock, sepsis, trauma, burns, obstetric emergencies, and envenomation, and it remains a major contributor to mortality in these settings [ref: Levi & ten Cate 1999]. Its laboratory hallmark is a characteristic temporal sequence: an initial hypercoagulable phase, a transitional consumption coagulopathy, and a terminal hypocoagulable phase in which clotting may fail almost completely.

Neutrophilic granulocytes are classically regarded as effectors of innate immunity and as participants in the inflammatory response that accompanies DIC. A body of experimental work, however, has argued that neutrophils are not merely bystanders but active participants in the coagulopathy itself, acting through their lysosomal apparatus. The lysosomal enzymes of neutrophils are markedly more active than the corresponding enzymes of liver and brain, and they exert a potent activating effect on Hageman factor (factor XII), the contact-phase initiator of the intrinsic coagulation cascade [ref: Bakhov 1988; Baluda 1980; Kuznik 1989]. Upon neutrophil degranulation these enzymes — for which acid phosphatase serves as a convenient marker — are released into the circulation, where they can activate factor XII, promote the conversion of plasminogen to plasmin, and thereby amplify fibrinolytic activity. This places neutrophil degranulation mechanistically upstream of the fibrinolytic, hypocoagulable phase of DIC.

The experimental model underlying the present study tests this hypothesis directly. DIC was induced in rabbits by a standardized inducer (the preparation "Efa-2", based on ethylphenacin, 8330 mg/kg orally), which reproduces the classical three-phase DIC time course — hypercoagulation (days 1–4), a transitional consumption phase, and deep hypocoagulation (days ~6–11, with possible complete incoagulability), resolving by days 19–20 [ref: Boiarchuk 1998]. Two groups were compared: a control DIC group (Group I) and a group in which granulocytopoiesis was pharmacologically suppressed (with the alkylating agent busulfan) before induction (Group II). The central experimental finding is that suppression of the neutrophil lineage largely prevents the deep hypocoagulable phase: in Group II the clinically significant DIC stage contracts from ~14–15 days to ~6 days, peak acid phosphatase activity is roughly 2.5-fold lower, and the 30% mortality observed in Group I (days 10–12, at the hypocoagulation peak) is essentially absent. Together these observations provide a causal, not merely correlative, argument for the pathogenetic role of activated neutrophils in the hypocoagulable phase of DIC [ref: Boiarchuk 2008].

This causal picture nonetheless leaves two questions unresolved, both quantitative rather than qualitative. First, the observable coagulation defects (prolonged recalcification time, fibrinogen depletion, factor XIII loss) presumably reflect a combination of a direct, inducer-driven (vessel-mediated) contribution and an indirect, neutrophil-mediated contribution; the relative size of these two contributions in each observable has not been quantified. Second, busulfan attenuates DIC, but the mechanism of that protection is ambiguous: it could act by reducing the number of neutrophils available to degranulate, by altering the kinetics of the neutrophil-driven processes, or both — and the existing data describe the protective effect without decomposing it. The prior literature characterizes neutrophil involvement qualitatively and through stage-averaged comparisons; it does not provide a mechanistic model that resolves these two questions.

We therefore develop a mechanistic ordinary-differential-equation model of neutrophil-driven DIC, fit jointly to both experimental groups, with three aims: (i) to build and validate a dynamical model that reproduces the six measured hemostatic and neutrophil-activity observables in both groups; (ii) to quantify, with uncertainty, the decomposition of each observable into vessel-mediated and neutrophil-mediated contributions, and to test it against the held-out suppressed-granulopoiesis group; and (iii) to use the validated model to predict the dose-response and the timing dependence of myelosuppressive intervention, with a view to the therapeutic window such intervention would imply.

# 2. Methods

## 2.1 Experimental data and protocols

**Animals and design.** Experiments were performed on 40 sexually mature rabbits of both sexes, body mass 2.5–3.0 kg, housed under standard vivarium conditions with free access to water and maintained according to accepted bioethical principles for laboratory animals. Two groups were studied. In Group I (control DIC), disseminated intravascular coagulation was modeled by a single oral dose of the inducer "Efa-2" (8330 mg/kg, administered fasting). Efa-2 is a commercial anticoagulant-rodenticide bait based on ethylphenacin, a first-generation 1,3-indandione vitamin-K antagonist; the 8330 mg/kg figure is the dose of the ready bait (approximately 0.015% active substance), not of a purified compound. Mechanistically, ethylphenacin inhibits vitamin-K-epoxide reductase, which depletes the vitamin-K-dependent coagulation factors (II, VII, IX, X) and proteins C and S and damages vascular endothelium, triggering a secondary disseminated intravascular coagulation that progresses through the classic three-phase cycle. In Group II (suppressed granulocytopoiesis), the identical inducer and dose were administered after pharmacological suppression of granulocytopoiesis.

**Granulocytopoiesis suppression (Group II).** Suppression was achieved with oral busulfan — an alkylating agent (1,4-butanediol dimethanesulfonate) that at low doses selectively depresses granulocytopoiesis — administered as the preparation Myelosan (AO Oktyabr, St. Petersburg) on a two-stage schedule. In the first stage busulfan was given at 10 mg/day for 5–7 days, continued until the absolute peripheral neutrophil count had fallen by 40–50% from the intact level. In the second stage a maintenance dose of 4 mg/day was given for approximately 8 days to stabilize the reduced neutrophil count without deepening the cytopenia. The inducer was then administered immediately, without interval. This protocol established a distinct pre-induction state, denoted "M" (post-busulfan), at which the absolute neutrophil count was reduced (from ~8.0 to ~3.9 ×10⁹/L) and hemostatic parameters were minimally but significantly shifted relative to intact (for factor XIII, P < 0.001); all Group II changes were therefore measured relative to state M rather than to the intact baseline.

**Observables and measurements.** Six observables were measured. Four characterize the hemostatic system: plasma recalcification time (s), thrombin time (s), fibrinogen (mg%¹), and factor XIII activity (%). Two characterize the neutrophil compartment: serum acid phosphatase activity (the lysosomal-enzyme marker) and a degranulation index derived from the lysosomal granule formula (the fraction of neutrophils showing pronounced degranulation, i.e. fewer than ten lysosomal granules). Group I was sampled at 16 timepoints over 19 days; Group II at 8 timepoints over 8 days, after which its dynamics had essentially resolved. The data derive from the Boiarchuk dissertation (1998) and the associated publications; a substantial portion of the Group II dynamics is reported here for the first time. Full provenance is documented in Supplementary §S7.

> ¹ Fibrinogen is reported in mg% (numerically equivalent to mg/dL), the unit used throughout the primary dataset.

## 2.2 Mathematical model

The model is a five-state ODE system tracking degranulation (D), acid phosphatase activity (AP), an inducer-derived coagulation pool (Hc), a neutrophil-derived coagulation pool (Hn), and factor XIII activity (X). Hc and Hn represent, respectively, the vessel-mediated (inducer-driven) and neutrophil-mediated pools of consumed coagulation activity; Hn has a carrying capacity Hm. The neutrophil-mediated effect entering the observable equations is the *effective coagulation load* gHn = Hn / (1 − Hn / Hm), a nonlinear amplification of Hn that reflects accelerating consumption as the pool approaches saturation. The measured neutrophil count is not a state variable: its time course N(t) is supplied as a per-group experimental input (one interpolator per group), a choice justified by N(t) being directly measured at every sampling timepoint.

The six observables are computed as algebraic functions of the state vector. Four hemostatic observables (recalcification time, thrombin time, fibrinogen, factor XIII) are mapped from the states through observable-specific contribution coefficients; the remaining two (acid phosphatase and the degranulation index) are read directly from the states AP and D and carry no separate coefficients. The model contains 26 parameters: rate constants governing degranulation (kd) and recovery/clearance of the degranulated state (kr), acid-phosphatase turnover (krl, kcl), the coagulation-pool kinetics (kca, kna, knd, Hm), the timing and width of the inducer-toxicity pulse (tp2, s2), and the contribution coefficients of the four hemostatic channels. Group I and Group II share all parameters except two group-specific modifiers (km, tm) that scale the effective rate constants in Group II to represent the busulfan effect; biologically, busulfan reduces neutrophil number and pulse timing rather than the per-cell production rates.

Two structural priors were imposed to resolve identifiability. First, a mechanism-split constraint (penalty weight W_SPLIT = 2.0) targets the day-2 neutrophil-attributable fractions of the recalcification, fibrinogen, and factor XIII channels; the target values (0.24, 0.76, 0.82) were derived independently from the day-1 (ΔG1 − ΔG2)/ΔG1 ratios in the experimental data (§3.3). Without this prior the decomposition is non-identifiable across optimizer seeds. Second, an upper bound on the factor XIII production parameter (cx ≤ 600) constrains the XIII channel to a biologically interpretable subspace; relaxing it unlocks a multi-modal landscape in which the XIII fit trades off against the other Group II observables. Both priors were validated post-hoc by a superior held-out (Group II) fit relative to unconstrained alternatives (Supplementary Methods). The full ODE formulation, parameter definitions, and observable formulas are given in Supplementary §S1.

## 2.3 Parameter estimation

The model was fit by minimizing a joint cost function — a weighted sum of squared residuals over all six observables in both groups — using a multi-seed differential evolution / local polishing pipeline. Differential evolution (scipy.optimize.differential_evolution: population size 12, maxiter 300, tol 1e-7, mutation (0.5, 1.5), recombination 0.85, polish disabled) was run independently from five random seeds (42, 7, 123, 2024, 999); each global solution was then polished by a Nelder-Mead → Powell → Nelder-Mead sequence (scipy.optimize.minimize). The lowest-cost result across the five seeds was retained as the joint baseline. The implementation used scipy 1.15, numpy 2.2, and Python 3.10; code and reproducibility tests are described under Code availability (Supplementary §S7).

The joint architecture (24 shared parameters plus two group-specific modifiers) trades some per-group fit quality for cross-group consistency: a separate Group-II-only fit attained roughly 22 percentage points higher mean Group II R² than the joint fit (Supplementary Methods), a gap that is largely architectural rather than attributable to overfitting. This penalty was accepted in exchange for a single shared mechanistic parameterization across both groups.

## 2.4 Robustness analysis

Model robustness was assessed through four complementary protocols. The three ensemble-based protocols among them — the parametric bootstrap, the leave-one-out cross-validation, and the neutrophil-count perturbation — share a common refit pipeline, distinct from and intentionally lighter than the §2.3 baseline pipeline: differential evolution (maxiter 200, popsize 15, single seed per iteration, tol 1e-7, mutation (0.5, 1.5), recombination 0.85, polish disabled, init='sobol'), followed by a Nelder–Mead → Powell → Nelder–Mead local polish. This choice reflects the total refit count across the three analyses — 100 bootstrap members, 23 leave-one-out timepoints, 5 deterministic α-scan and 40 stochastic perturbation refits, 168 in all — at which the full multi-seed §2.3 procedure would not have been practical.

A profile-likelihood analysis of all 26 parameters classified each as well-identified (relative profile depth > 5%; six parameters: tp2, km, tm, kd, s2, at), weakly identified (five parameters), or sloppy (twelve parameters with relative depth < 2%). A parametric bootstrap (N = 100) generated synthetic datasets from the baseline predictions with Gaussian noise (σ equal to the per-observable, per-group baseline RMSE) and refit the model on each, yielding marginal confidence intervals on all parameters and on the prediction trajectories. A leave-one-out cross-validation removed all six observables at each of the 23 non-anchor timepoints (15 in Group I, 8 in Group II) in turn, refit the model, and computed the PRESS statistic for the held-out point. Finally, sensitivity to neutrophil-count input was tested by perturbing N(t) deterministically (scaling factor α ∈ {0.8, 0.9, 1.0, 1.1, 1.2}) and stochastically (per-timepoint lognormal noise at CV = 10% and CV = 20%, N = 20 each).

## 2.5 Virtual experiments

Three virtual experiments propagated parameter uncertainty by running the 100-member bootstrap ensemble through prediction tasks. In the dose-response experiment, the Group II effective rate constants were overridden as kr,G2 = kr × km and tp2,G2 = tp2 × tm across a 15 × 15 log-spaced grid in (km, tm), with the Group II neutrophil profile retained throughout (22,500 simulations in total). In the intervention-timing experiment, the busulfan effect was switched on at a variable time t_intervention by two-segment ODE integration in which the state (D, AP, Hc, Hn, X) was continuous across the boundary and only the rate constants changed instantaneously; nine timing scenarios from t = 0 to no intervention were run at the observed Group II dose (900 simulations). In the dose-by-timing experiment, two scenarios — high dose at late timing, half dose at early timing — were run to test the dose–timing trade-off directly (200 simulations).

For each trajectory four severity metrics were computed: peak hypocoagulation (the maximum change in recalcification time), integrated coagulation disruption (the area under |Δrecalcification|), the factor XIII depletion nadir (the minimum change in XIII activity), and the peak effective coagulation load (max gHn). For the intervention-timing experiment three temporal metrics were additionally computed: the time of peak gHn, the time to recovery (gHn falling below 10% of its peak), and the acute-phase duration (the interval between the two). Severity metrics were evaluated on the native Group II timeline (0–9 days) for the dose-response experiment and on an extended timeline (0–19 days) for the timing and dose-by-timing experiments; time-to-peak was defined as the first local maximum of gHn(t) to avoid finite-horizon boundary artifacts.

# 3. Results

## 3.1 The model captures both experimental groups

Fitted jointly to both groups, the model reproduced the measured dynamics of all six observables. For Group I (15 non-anchor timepoints over 19 days) the mean coefficient of determination across observables was R² = 0.83; for the busulfan-suppressed Group II (8 timepoints over 8 days) it was R² = 0.69. Most channels were captured well in both groups; the lower Group II mean is attributable to the factor XIII channel, which is structurally under-determined (§3.2).

Agreement was strongest in the deep-hypocoagulation phase, where the late-phase nadirs of factor XIII and fibrinogen were reproduced within 1–11% (§3.8). The principal discrepancy was in the early, hypercoagulation phase, where the amplitude of the two vessel-driven channels — recalcification time and fibrinogen — was underestimated; the fibrinogen channel additionally showed a non-monotonic intermediate profile arising from the near-cancellation of two large opposing terms (§4.6). These discrepancies are confined to the early phase of the vessel-driven channels and do not affect the peak timing or the group separation that underlie the main findings. The baseline fits are shown in Figure 1.

**Figure 1.** Baseline model fits and experimental data for both groups, one panel per observable: (a) recalcification time, (b) thrombin time, (c) fibrinogen, (d) factor XIII activity, (e) acid phosphatase, (f) degranulation index. Group I in blue (circles, solid line), Group II in red (triangles, dashed line); points are group means ± SEM, curves are the lowest-cost baseline fit. All quantities are changes from each group's baseline (Group I from intact, Group II from state M); model curves are drawn only within each group's observed range. The gray band (days 10–12) marks the Group I deep-hypocoagulation and mortality window.

## 3.2 Parameter identifiability and uncertainty

The profile-likelihood analysis identified six well-identified parameters (relative profile depth > 5%: tp2, km, tm, kd, s2, at); the remaining twenty were weakly identified or sloppy — the universal sloppiness pattern typical of mechanistic systems-biology models. The parametric bootstrap (N = 100) yielded marginal confidence intervals consistent with this classification: tight for the well-identified parameters and wide for the sloppy ones. Median estimates and confidence intervals for the well-identified parameters are given in Table 1; estimates for all 26 parameters appear in Supplementary Table S2.

The one exception is the factor XIII channel in Group II, which is structurally under-determined rather than merely sloppy. Across the 100 bootstrap members, 41 yielded a negative Group II XIII R², and the ensemble distribution was bimodal (Figure 2), reflecting the optimizer settling in different basins across resamples. This is a limitation of the information content of the available Group II data, not of the estimation pipeline; the cost was otherwise stable across members. For downstream predictions we therefore report full-ensemble confidence bands, and, where a conservative XIII interpretation is required, a good-basin subset (the n = 27 members with Group II XIII R² ≥ 0.3, the criterion also used in the virtual experiments) provides a tighter band.

Sensitivity to the per-observable normalization was tested by replacing the range-based scale factors with per-group standard deviations (which upweights the Group II XIII channel ~24-fold). At the baseline parameter point this raised the Group II XIII R² from 0.08 to 0.93 (single seed); however, under the parametric bootstrap the fraction of iterations with negative Group II XIII R² rose from 41% to ~83%. The improved normalization therefore sharpens rather than resolves the multi-modal landscape, confirming that the XIII under-determination is a structural property of the {ax, cx, bx, kx} manifold rather than an artifact of the normalization choice (Supplementary §S4).

**Table 1.** Well-identified parameters (relative profile depth > 5%): median and 95% confidence interval from the 100-member bootstrap ensemble. "Well-identified" refers to profile-likelihood depth (local curvature of the cost surface); the bootstrap intervals for kd and s2 are wider, reflecting a long right tail in the global resample distribution.

| Parameter | Median [95% CI] | Role |
| --- | --- | --- |
| tp2 | 9.217 [8.889, 10.034] | Peak time of the inducer-toxicity pulse (days) |
| km | 4.918 [3.462, 5.734] | Group II rate modifier (busulfan effect on rate constants) |
| tm | 0.427 [0.392, 0.467] | Group II timing modifier (busulfan effect on pulse timing) |
| kd | 0.264 [0.218, 1.054] | Degranulation rate constant |
| s2 | 1.757 [1.513, 2.712] | Width of the inducer-toxicity pulse |
| at | 5.659 [4.893, 6.437] | Thrombin / inducer-pulse coefficient |

## 3.3 Mechanism split: neutrophil vs vessel contributions

The coagulation dynamics were decomposed into vessel-mediated and neutrophil-mediated contributions using a biologically derived prior on the day-2 (Group I) neutrophil share. The prior targets were estimated independently from the day-1 neutrophil-attributable fraction (ΔG1 − ΔG2)/ΔG1 — recalcification 0.24, fibrinogen 0.76, factor XIII 0.82 — a derivation that is well-posed because the two groups have near-identical hemostatic baselines (recalcification 78.7 vs 78.0 s; fibrinogen 58.2 vs 58.3 mg%; factor XIII 100.0 vs 93.2%), so busulfan altered neutrophil numbers without shifting baseline hemostasis. Imposing this prior (W_SPLIT = 2.0) yielded fitted day-2 fractions of 0.240 [0.225, 0.249] for recalcification (vessel-dominant) and 0.759 [0.738, 0.777] and 0.806 [0.777, 0.844] for fibrinogen and factor XIII (both neutrophil-dominant).

The prior is required for identifiability: without it the recalcification fraction is non-identifiable across optimizer seeds (0.34–0.48) and the decomposition is not unique (Supplementary Methods). The decomposition was validated post-hoc by a superior held-out (Group II) fit relative to unconstrained alternatives (+2–7 percentage points of Group II R²). We therefore present these fractions as a prior-regularized, held-out-validated decomposition that quantifies and is consistent with the neutrophil hypothesis, rather than as a prior-free inference. One transparency caveat applies: for fibrinogen, an unconstrained fit places the neutrophil fraction near 0.05, so the 0.76 value is the imposed day-1-derived prior target, not a feature independently reproduced by the day-2 fibrinogen dynamics. The decomposition is shown in Figure 3.

The strong neutrophil contribution to factor XIII (~80%) is consistent with the azurophilic-granule storage hypothesis, under which degranulating neutrophils release pre-stored factor XIII into the circulation, where it is rapidly consumed; the vessel-dominant contribution to recalcification is consistent with the rapid onset of hypocoagulation after inducer administration, before neutrophil-mediated effects have developed.

**Figure 3.** Mechanism-split decomposition: the neutrophil-attributable fraction of each coagulation channel at Group I day 2 (median and 95% CI, 100-member ensemble). Dashed vertical lines mark the day-1-derived prior targets (recalcification 0.24, fibrinogen 0.76, factor XIII 0.82) imposed as soft constraints (W_SPLIT = 2.0).

**Table 2.** Mechanism-split decomposition: neutrophil-attributable fraction of each coagulation channel at Group I day 2. Prior targets are the day-1 (ΔG1 − ΔG2)/ΔG1 ratios; fitted values are the median and 95% CI across the 100-member ensemble.

| Channel | Prior target | Fitted median [95% CI] | Interpretation |
| --- | --- | --- | --- |
| Recalcification time | 0.24 | 0.240 [0.225, 0.249] | Vessel-dominant |
| Fibrinogen | 0.76 | 0.759 [0.738, 0.777] | Neutrophil-dominant |
| Factor XIII | 0.82 | 0.806 [0.777, 0.844] | Neutrophil-dominant |

## 3.4 Robustness validation

Leave-one-out cross-validation showed that Group I predictions were robust to removal of any single timepoint (median PRESS = 6.5 across the six observables; worst case t = 11, PRESS = 24.5, reflecting the role of the peak-DIC observation). Group II predictions were more sensitive to timepoint removal (median PRESS = 21.5), consistent with the smaller sample size (8 informative timepoints vs 15 in Group I). The highest single value, at Group II t = 1 (PRESS = 76.6, dominated by the acid phosphatase channel), identifies early acid-phosphatase dynamics as the least-constrained aspect of the Group II fit — a direct consequence of there being only one observation (t = 1) between acid-phosphatase onset and the first post-onset measurement (t = 2). These results characterize the information content of the experimental design rather than overfitting: all refits converged to costs within 10% of baseline (range 0.94–1.06), indicating stable parameter identification.

Sensitivity to the neutrophil-count input was likewise limited. Aggregate Group I fit quality remained stable across all perturbations (R² ∈ [0.78, 0.83]), and stochastic perturbation produced no systematic shift in the well-identified parameters (km, tm, cf, kd). The non-monotonic α-scan pattern (Group II R² = 0.65, 0.68, 0.65, 0.74, 0.77 at α = 0.8–1.2) reflects the multi-modal optimization landscape rather than a biological signal about neutrophil-count accuracy; doubling the noise level from CV = 10% to CV = 20% widened the cost confidence interval only marginally (0.140 vs 0.139), indicating sub-linear sensitivity for the well-identified parameters.

## 3.5 Busulfan dose-response

The dose-response experiment showed that the busulfan-induced kinetic modification of the neutrophil-derived rate constants reduced peak hypocoagulation about 7-fold and integrated coagulation disruption about 2.5-fold, relative to the same neutrophil profile without kinetic modification. The observed experimental dose (km = 4.93, tm = 0.43) lies on the dose-response curve at intermediate severity. Kinetic modification alone, applied to the Group II neutrophil profile, did not reproduce Group-I-level hypocoagulation: substituting the Group I neutrophil profile into the model (§3.8) produced ~22-fold greater peak hypocoagulation, indicating that the protective effect of busulfan operates substantially through the reduction of neutrophil abundance, not through kinetic modification alone. The phase diagrams are shown in Figure 4, and a dose-response slice at the observed timing in Figure 5.

**Figure 4.** Busulfan dose-response phase diagrams over the (km, tm) parameter space (per-cell median, 100-member ensemble): (a) peak hypocoagulation (max Δrecalcification, s; contours at 10, 20, 30, 40 s), (b) factor XIII nadir (min ΔXIII, %), (c) peak effective coagulation load (max gHn). The circle marks no kinetic effect (km = 1, tm = 1); the star marks the observed Group II dose (km = 4.93, tm = 0.43). The Group II neutrophil profile is retained throughout, so severity reflects kinetic modification only. All four severity metrics are mapped in Supplementary §S6.

**Figure 5.** Dose-response slice: peak hypocoagulation versus the rate modifier km at fixed timing modifier tm ≈ 0.45 (median and 95% CI band, 100-member ensemble). The dotted line marks the no-busulfan severity (km = 1); the dashed line and triangle mark the observed Group II operating point (km = 4.93). The confidence band narrows with increasing km, indicating that the predicted attenuation is more certain at higher kinetic suppression.

## 3.6 Therapeutic window

Busulfan intervention provided near-complete DIC attenuation when applied within 2.5 days of injury (peak change in recalcification time 7–8 s, comparable to the observed Group II outcome). A critical half-day transition occurred between days 2.5 and 3, across which peak severity roughly doubled (7.9 → 14.4 s). Beyond day 3 busulfan retained a partial protective effect — reducing peak severity 2–3-fold relative to no intervention — but could not prevent acute DIC onset. The therapeutic window thus comprises a prevention phase (0–2.5 days) and a mitigation phase (2.5–6+ days).

Intervention at t = 0 and t = 1 produced indistinguishable outcomes, indicating that the inducer-toxicity pulse V(t) (peaking at τv = 1.5 days, reflecting the time to peak ethylphenacin effect) does not accumulate sufficient effective coagulation load in the first 24 hours to trigger the cascade independently — consistent with the expected latency between anticoagulant exposure and measurable coagulopathy. The therapeutic window is shown in Figure 6.

**Figure 6.** Therapeutic window: DIC severity versus busulfan intervention time (median and 95% CI band, 100-member ensemble): (a) peak hypocoagulation, (b) factor XIII nadir, (c) peak effective coagulation load. The shaded band (days 2.5–3) marks the critical transition; the dotted line on each panel is the no-intervention reference. The transition is reported as occurring between the sampled timings (days 2.5 and 3) rather than at a single interpolated value. The temporal metrics are shown in Supplementary §S5.

## 3.7 Dose × timing thresholds

A focused experiment tested whether dose and timing operate as a continuous trade-off or as independent thresholds. Doubling the dose at late intervention (t = 4 days, km = 10 instead of 4.93) produced no measurable improvement in peak severity (28.0 vs 28.2 s), indicating a dose ceiling once the cascade is established. Conversely, halving the dose at optimal timing (t = 0, km = 2.5) produced a markedly worse outcome (34.0 vs 7.1 s), exceeding even the severity of late full-dose intervention. The protective effect of busulfan thus requires both an adequate dose (above the rate-suppression threshold) and timely administration (before cascade lock-in), not either alone (Table 3).

**Table 3.** Dose × timing combinations testing whether dose and timing trade off continuously or act as independent thresholds. Peak hypocoagulation (max Δrecalcification, s) is the median [95% CI] from the 100-member ensemble; each combination is compared with its full-dose reference at the same timing.

| Scenario | Dose (km) | Timing (d) | Peak Δrecalc [95% CI] | Reference (full dose, same timing) | Outcome |
| --- | --- | --- | --- | --- | --- |
| Double dose, late | 10.0 | 4 | 28.0 [0.0, 38.9] | 28.2 (full dose, t = 4) | No improvement (dose ceiling) |
| Half dose, early | 2.5 | 0 | 34.0 [22.7, 44.0] | 7.1 (full dose, t = 0) | Markedly worse (dose floor) |
| *Full dose, early (ref)* | 4.93 | 0 | 7.1 [0.6, 14.7] | — | Prevention |
| *Full dose, late (ref)* | 4.93 | 4 | 28.2 [1.5, 39.0] | — | Mitigation |
| *No intervention (ref)* | — | — | 75.6 [60.5, 92.0] | — | Untreated |

## 3.8 External validation against the observed mortality pattern

The model was validated against the observed mortality contrast (30% in Group I, days 10–12; 0% in Group II) by simulating pure Group I dynamics (Group I neutrophil profile, no busulfan) through the bootstrap ensemble. The model reproduced severe hypocoagulation in Group I (peak Δrecalcification 147 s, factor XIII nadir −77%, fibrinogen nadir −58 mg%) versus near-absent hypocoagulation in the busulfan-modified Group II baseline (peak Δrecalcification ~7 s) — a 22-fold separation consistent with the observed mortality difference. The peak occurred at day 11, matching the observed timing of both the hypocoagulation maximum and the mortality window (days 10–12).

Channel-level agreement was differential: the factor XIII nadir matched observation within 1% (−77.1 vs −76.7%) and the fibrinogen nadir within 11% (−58.3 vs −52.6 mg%), while the recalcification peak was underestimated by ~29% (147 vs 207 s). The amplitude underestimation was confined to the vessel-driven channels (the recalcification peak and the early fibrinogen rise) rather than being systemic, and is consistent with the joint-fit architecture penalty (§2.3); it is reported as a known limitation (§4.6). The validation is therefore qualitative and directional — the model reproduces the timing and the group separation underlying the observed mortality — rather than a quantitative mortality model (Table 4).

**Table 4.** Group I versus Group II severity and validation against the observed Group I values. Modeled values are the median [95% CI] from the 100-member ensemble (pure Group I dynamics and the busulfan-modified Group II baseline). Observed Group I values are from the dissertation tables.

| Metric | Group I model [95% CI] | Group I observed | Agreement | Group II model [95% CI] |
| --- | --- | --- | --- | --- |
| Peak hypocoagulation (max Δrecalc, s) | 147 [122, 176] | 207 | model 29% below | 7 [3, 11] |
| Factor XIII nadir (min ΔXIII, %) | −77.1 [−94.4, −61.4] | −76.7 | within 1% | −13.8 [−19.7, −7.3] |
| Fibrinogen nadir (min Δfib, mg%) | −58.3 [−69.1, −46.4] | −52.6 | within 11% | −1.4 [−8.1, 0.0] |
| Time of peak (t at max recalc, d) | 11 [10, 11] | 11 | exact | 5 [5, 6] |
| **Group I / Group II separation (max Δrecalc)** | **22.2×** | — | — | — |

# 4. Discussion

**[Section 4 to be drafted by O. Boiarchuk. The scaffold below — provided by O.K. — fixes the intended structure and the four-pillar narrative; it is not finished prose.]**

4.1. **Summary of findings.** Restate the four-pillar narrative: (i) a prior-regularized mechanism split that quantifies and is consistent with (rather than independently confirms) the neutrophil contribution; (ii) a quantified busulfan kinetic effect of 2.5–7-fold; (iii) a narrow therapeutic window with a sharp 2.5–3-day transition; (iv) dose and timing thresholds that are both required.

4.2. **Biological interpretation of the mechanism split.** Vessel-dominant recalcification together with neutrophil-dominant fibrinogen and factor XIII — discuss in light of known DIC pathogenesis, and connect the strong factor XIII contribution to azurophilic-granule factor XIII storage [ref: Boiarchuk 2008].

4.3. **Implications for myelosuppressive therapy.** Translate the dose-response findings to clinical and veterinary practice. The observed Group II dose lies near the plateau of efficacy, so further dose escalation is unlikely to help; timing matters as much as dose. Provide practical guidance for anticoagulant-rodenticide intoxication presenting at different times after exposure. *[O.B. to expand the clinical context: the vitamin-K-antagonist mechanism of ethylphenacin invites a parallel with warfarin-reversal therapy — half-life, tissue selectivity, and the limits of the analogy.]*

4.4. **The two-phase therapeutic window.** Discuss the biological basis: the prevention phase (0–2.5 days) precedes cascade lock-in; the mitigation phase (2.5–6+ days) limits the extent of damage; the half-day transition reflects a sharp threshold in acid-phosphatase / effective-coagulation-load accumulation.

4.5. **Count reduction vs kinetic modification.** Pure Group I simulation (§3.8) produces ~22-fold greater hypocoagulation severity than the Group II kinetic scenario, indicating that busulfan protection operates substantially through reduction of neutrophil abundance rather than kinetic modification alone; discuss in light of the observed mortality pattern (30% Group I vs 0% Group II). Note the model limitation: the recalcification amplitude is underestimated ~30%, though peak timing and the XIII and fibrinogen nadirs are reproduced within 1–11% (§3.8).

4.6. **Limitations.** The structural under-determination of the factor XIII channel (robust to normalization, §3.2); the idealized busulfan pharmacokinetics (instantaneous effect); the flat extrapolation of the neutrophil interpolator beyond the last Group II timepoint; and veterinary-to-clinical translation caveats. The two vessel-driven channels (recalcification, fibrinogen) underestimate the early hypercoagulation amplitude while reproducing the late nadir well. For fibrinogen the cause is explicit in the channel decomposition (Supplementary §S1): the fibrinogen output is a small difference of two large opposing terms — the acid-phosphatase contribution (cf·AP) and the neutrophil-dependent contribution (−bf·gHn), each roughly four-fold larger in magnitude than their sum near days 5–7 — so minor phase mismatches between AP and gHn there produce a non-monotonic intermediate profile and suppress the early fibrinogen rise relative to observation. This is a consequence of the fixed, jointly-estimated parameterization and does not affect the channels carrying the main findings.

4.7. **Future directions.** Additional Group II timepoints to constrain the factor XIII channel; an explicit PK/PD layer for busulfan; and a fuller exploration of combined interventions.

# 5. Conclusions

**[PLACEHOLDER — one paragraph, to be written last.]**
To restate: the model decomposes neutrophil and vessel contributions to DIC; the busulfan kinetic effect is quantified and bracketed; the therapeutic window is characterized as two-phase with a sharp half-day transition between days 2.5 and 3; and protection requires both an adequate dose and timely administration.

# References

*Intermediate format (author, year, title, journal, volume:pages, DOI); final styling to JTB at submission. Entries flagged [TO VERIFY] still need a confirmed source and have deliberately not been fabricated.*

**Primary experimental sources (Boiarchuk series)**

- Boiarchuk OD (1998) Experimental model of DIC syndrome. Visnyk Problem Biolohii i Medytsyny (7):132–138. [dissertation basis; full protocol tables]
- Boiarchuk OD, Koval SB, Lunina NV (2000) Changes in the lysosomal apparatus of neutrophilic leukocytes in disseminated intravascular coagulation syndrome. Fiziolohichnyi Zhurnal 46(3):72–77.
- Boiarchuk OD (2008) Changes in neutrophil activity during formation of disseminated intravascular coagulation syndrome. Naukovyi Visnyk Mykolaivskoho Derzhavnoho Universytetu im. V.O. Sukhomlynskoho 23(3):14–17.
- Boiarchuk OD, Lunina NV (2012) Histochemical features of neutrophils in DIC syndrome. Visnyk LNU imeni Tarasa Shevchenka 17(252):19–25 (in Ukrainian).
- Boiarchuk OD (2013) Dynamics of granulocyte acid phosphatase in DIC syndrome. Visnyk LNU imeni Tarasa Shevchenka 19(278), Part I:6–13 (in Ukrainian).
- Boiarchuk OD (2023) Features of neutrophils in DIC syndrome. InterConf (Orléans). doi:10.51582/interconf.19-20.04.2023.042

**Methods (hemostasis, lysosomal apparatus)**

- Pigarevsky VE (1975) The lysosomal-cationic test. Patologicheskaya Fiziologiya i Eksperimentalnaya Terapiya (3):86–88.
- Baluda VP, Barkagan ZS, Goldberg ED (eds., 1980) Laboratory methods for studying the hemostatic system. Tomsk, 314 pp.
- Montsevichyute-Eringene EV (1964) Simplified mathematical-statistical methods in medical research. Patologicheskaya Fiziologiya i Eksperimentalnaya Terapiya (4):72–78.
- Busulfan: alkylating agent with selective depression of granulocytopoiesis at low doses; for the substance pharmacology see the Myleran (busulfan) prescribing information (FDA label). The two-stage suppression protocol (10 mg/day for 5–7 days to a 40–50% neutrophil reduction, then 4 mg/day for ~8 days) is the authors' own methodology, described in Boiarchuk (1998) and the authors' methodological notes, and was not published explicitly in the journal articles.

**Identifiability and uncertainty methodology**

- Raue A, Kreutz C, Maiwald T, Bachmann J, Schilling M, Klingmüller U, Timmer J (2009) Structural and practical identifiability analysis of partially observed dynamical models by exploiting the profile likelihood. Bioinformatics 25(15):1923–1929. doi:10.1093/bioinformatics/btp358
- Kreutz C, Raue A, Kaschek D, Timmer J (2013) Profile likelihood in systems biology. FEBS Journal 280(11):2564–2571. doi:10.1111/febs.12276
- Gutenkunst RN, Waterfall JJ, Casey FP, Brown KS, Myers CR, Sethna JP (2007) Universally sloppy parameter sensitivities in systems biology models. PLoS Computational Biology 3(10):e189. doi:10.1371/journal.pcbi.0030189
- Efron B, Tibshirani RJ (1993) An Introduction to the Bootstrap. Chapman & Hall, New York, 456 pp.
- Stone M (1974) Cross-validatory choice and assessment of statistical predictions. Journal of the Royal Statistical Society, Series B 36(2):111–133. doi:10.1111/j.2517-6161.1974.tb00994.x

**Inducer toxicology (anticoagulant rodenticides)**

- Watt BE, Proudfoot AT, Bradberry SM, Vale JA (2005) Anticoagulant rodenticides. Toxicological Reviews 24(4):259–269.
- Hadler MR, Buckle AP (1992) Forty-five years of anticoagulant rodenticides — past, present and future trends. Proceedings of the Fifteenth Vertebrate Pest Conference, Paper 36. University of California, Davis.

**DIC pathogenesis**

- Levi M, ten Cate H (1999) Disseminated intravascular coagulation. New England Journal of Medicine 341(8):586–592. doi:10.1056/NEJM199908193410807
- Barkagan ZS, Momot AP (2001) Diagnosis and controlled therapy of hemostasis disorders. Newdiamed, Moscow, 285 pp. (in Russian).
- [TO VERIFY] Bakhov 1988; Kuznik 1989 — neutrophil/Hageman-factor activation (cited §1); confirm full bibliographic details.
- [TO VERIFY] Introduction etiology/temporal-course citation (currently placeholder "Pavlovsky 1988; Chervyovy 1990") — confirm or replace with a verified DIC reference.

---

*Document log — 2026-05: draft v2 (cohesion/style harmonization pass over v1). Methods §2.3–§2.5 converted to narrative prose; verb tense unified to past for completed procedures; drug/inducer naming unified (busulfan / ethylphenacin, with Myelosan / "Efa-2" named once each in §2.1); state glossary fixed (N(t) input vs Hn pool; gHn = effective coagulation load; "hyaline" retired from the body, retained as an etymological note in S1); internal "Analysis NN" references remapped to Supplementary; figure captions trimmed to content + reading guidance; defensive repetition reduced. Numbers, structure, and argument left unchanged. Abstract, Discussion §4, and Conclusions remain placeholders/scaffold per ownership (O.B. leads Discussion).*

*2026-05-27: §2.3 corrected to match src/fit.py (population 12 not 15; maxiter 300 not 200; default init not Sobol; multi-seed pipeline made explicit). Numbers verified against src/fit.py lines 189-217.*

*2026-05-27: §2.4 corrected and clarified — the bootstrap, LOO, and perturbation analyses share a common lighter refit pipeline (DE 15/200/single-seed/Sobol + NM→Powell→NM polish), distinct from the §2.3 baseline pipeline. The previous wording "full estimation pipeline" implied the §2.3 pipeline and was misleading. Pipeline settings and the 168-refit total verified against src/fit.py and analyses/{20,21,22}/run.py.*
