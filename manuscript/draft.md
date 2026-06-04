# A mechanistic model of neutrophil-mediated disseminated intravascular coagulation predicts a narrow therapeutic window for myelosuppressive intervention

**Olena Boiarchuk¹** and **Oleksiy Onasenko²**

¹ *Candidate of Biological Sciences, Associate Professor. State Institution "Luhansk Taras Shevchenko National University", Department of Health and Rehabilitation. 2 Viktor Novikov St., Lubny, Poltava Region 37600, Ukraine.*

² *MD. Independent researcher in complex systems physics and emergence theory. 6d Mykoly Dmitrieva St., Poltava 36000, Ukraine.*

*Corresponding author:* Olena Boiarchuk, boiarchuk.helen@gmail.com

*ORCID:* O. Boiarchuk — 0000-0002-4388-6011; O. Onasenko — 0009-0007-7017-8161

*E-mail:* boiarchuk.helen@gmail.com (O.D.B.); olexxa62@gmail.com (O.O.)

---

## Highlights

- A mechanistic ODE model of DIC with shared biochemistry is fitted simultaneously to control and busulfan-suppressed experimental groups
- Parameter map: 6 of 26 parameters are well-identified; the remainder are *sloppy* — a structural property of models of this class
- Independent validation: the model reproduces the peak day (11), 22-fold group separation, and nadirs of factor XIII and fibrinogen to within 1% and 11%
- Prediction: a biphasic therapeutic window with a sharp transition between days 2.5 and 3
- Dose and timing act as independent thresholds — neither compensates for the absence of the other

---

## Abstract

**Problem.** Disseminated intravascular coagulation (DIC) progresses from a hypercoagulable phase to a deeply hypocoagulable one in which coagulation may nearly cease; the role of activated neutrophils in this phase has been established qualitatively but has not been formulated quantitatively or mechanistically.

**Model.** In an animal model of DIC induced by an anticoagulant rodenticide (ethylphenacin), two groups of rabbits are compared: a control group and a group with pharmacologically suppressed granulopoiesis (busulfan). We construct a mechanistic ODE model with five states and shared biochemistry for both groups and fit it simultaneously to both groups against six observables of haemostasis and neutrophil activity.

**Identifiability.** Profile likelihood, parametric bootstrap ($N = 100$), leave-one-out cross-validation, and neutrophil-count perturbation delineate the parameter map of the DIC model: six parameters are well-identified, twelve are *sloppy* — typical for mechanistic systems-biology models of this size.

**Validation.** After fitting, the model is tested against observations that did not enter its training data: the time to peak coagulopathy (day 11, coinciding with the lethality window in Group I), a 22-fold between-group difference in hypocoagulability severity, and the nadirs of factor XIII and fibrinogen — reproduced by the model to within 1% and 11%, respectively.

**Prediction.** According to the validated model, myelosuppressive intervention has a biphasic therapeutic window with a sharp transition between days 2.5 and 3; dose and timing act as independent thresholds rather than a continuous trade-off. Additionally, the model quantitatively decomposes the observed coagulation disturbances into two sources: recalcification disturbances are primarily attributable to direct vascular toxicity of the inducer, whereas fibrinogen and factor XIII depletion are primarily attributable to a neutrophil-mediated mechanism. This provides the longstanding qualitative hypothesis about the role of neutrophils with a quantitative, testable form.

**Keywords:** disseminated intravascular coagulation; neutrophil degranulation; mechanistic ODE model; parameter identifiability; mechanism decomposition; myelosuppressive intervention

---

## 1. Introduction

Disseminated intravascular coagulation (DIC) is a systemic acquired haemostatic disorder in which massive coagulation activation initially leads to microvascular thrombosis and consumption of coagulation factors, and subsequently — as these are depleted — to haemorrhagic diathesis. DIC is not a primary disease but a complication of shock, sepsis, trauma, burns, obstetric emergencies, and poisonings, and remains a significant contributor to mortality in these settings [Levi & ten Cate, 1999; Gando et al., 2016; Levi & Scully, 2018; Squizzato et al., 2020]. Its laboratory hallmark is a characteristic temporal sequence: an initial hypercoagulable phase, a transitional consumptive coagulopathy, and a terminal hypocoagulable phase in which coagulation may nearly cease.

Neutrophilic granulocytes are traditionally viewed as effectors of innate immunity and participants in the inflammatory response accompanying DIC. A body of experimental work argues, however, that neutrophils are not passive bystanders but active participants in the coagulopathy itself — acting through their lysosomal apparatus [Massberg et al., 2010; Engelmann & Massberg, 2013; Alhamdi & Toh, 2017]. Neutrophil serine proteases, primarily elastase and cathepsin G, are stored in azurophilic (primary) granules — the characteristic reservoir of acid hydrolases, for which acid phosphatase serves as a marker [Borregaard & Cowland, 1997]. Upon degranulation, these enzymes are released into the circulation and act on haemostasis through several parallel channels. On the one hand, they enhance coagulation: elastase cleaves tissue factor pathway inhibitor (TFPI), relieving inhibition of the tissue-factor- and factor-XII-dependent cascade [Massberg et al., 2010], while neutrophil extracellular traps (NETs) and nucleosomes activate factor XII via a negatively charged surface [Massberg et al., 2010; Alhamdi & Toh, 2017]. On the other hand, the same proteases destroy coagulation factors: elastase cleaves fibrinogen into low-molecular-weight fragments [Plow & Edgington, 1975; Bach-Gansmo et al., 1994] and, by limited proteolysis, activates plasma factor XIII into a truncated form that is rapidly consumed in the cascade [Henriksson et al., 1980; Bagoly et al., 2008]. This bidirectional influence places neutrophil degranulation mechanistically *upstream* of the deep consumptive and hypocoagulable phase, consistent with the modern reframing of DIC as a manifestation of *immunothrombosis*, in which coagulation and innate immunity are mutually coupled [Engelmann & Massberg, 2013].

The animal model underlying this study directly tests this hypothesis. DIC is induced in rabbits with a standardised inducer (preparation "Efa-2" based on ethylphenacin — a first-generation vitamin K antagonist from the 1,3-indanedione family of anticoagulant rodenticides [Watt et al., 2005]; 8,330 mg/kg orally), which reproduces the classic triphasic course of DIC — hypercoagulation (days 1–4), a transitional consumptive phase, and deep hypocoagulation (approximately days 6–11, with possible complete incoagulability), resolving by days 19–20 [Boiarchuk, 1998a; Boiarchuk, 1998b]. Two groups are compared: a control DIC group (Group I) and a group in which granulopoiesis is pharmacologically suppressed by the alkylating agent busulfan prior to induction (Group II) [Boiarchuk, 1998a; Boiarchuk, 2014].

Central finding: suppression of the neutrophil lineage largely prevents the deep hypocoagulable phase. In Group II, the clinically significant stage of DIC is shortened from ~14–15 to ~6 days, the hypercoagulable effect lasts only about 2 days and is 4–7 times less pronounced, and hypocoagulable shifts barely develop [Boiarchuk, 2023a]; peak acid phosphatase activity is approximately 2.5-fold lower [Boiarchuk, 2012; Boiarchuk, 2013; Boiarchuk, 2014], and the 30% lethality observed in Group I (days 10–12, at the peak of hypocoagulation) [Boiarchuk, 1998a] is virtually absent. Together these observations provide a causal, rather than merely correlational, argument in favour of a pathogenetic role for activated neutrophils in the hypocoagulable phase of DIC [Boiarchuk, 2008; Boiarchuk, 2023b].

This causal picture nonetheless leaves two questions unresolved — both quantitative rather than qualitative in nature. First, the observed coagulation disturbances (prolonged recalcification time, fibrinogen depletion, factor XIII loss) reflect a combination of a direct, inducer-mediated (vascular) contribution and an indirect, neutrophil-mediated one; the relative magnitude of these two contributions in each observable has not been characterised quantitatively. Second, busulfan attenuates DIC, but the mechanism of this protection is ambiguous: it may act either through a reduction in the number of neutrophils available for degranulation, or through a change in the kinetics of neutrophil-mediated processes, or through both simultaneously. The available data describe the protective effect without decomposing it.

Here we resolve these questions with a five-step sequence. First, we construct an ODE model of neutrophil-mediated DIC with shared biochemistry for both groups and fit it simultaneously to six observables in both groups (§3.1). Next, we delineate the parameter map of this model — analysing which parameters are supported by the data and which are not, and what this means for confidence in subsequent claims (§3.2). In the third step, we verify the internal consistency of the model with the between-group difference on day 1 of the experiment, derived independently from the contrast of the two groups (§3.3). In the fourth step, we validate the model against observations that did not enter its training data: the time to peak, group separation, and nadir amplitudes (§3.4). In the fifth step — given a validated model — we investigate what it predicts about the dose and timing of myelosuppressive intervention (§3.5). Each step has a clear success criterion, stated here and revisited in the Discussion.

---

## 2. Methods

### 2.1 Experimental data and protocols

**Animals and design.** Experiments were performed on 40 sexually mature rabbits of both sexes with body weight 2.5–3.0 kg, housed in standard vivarium conditions with free access to water and in accordance with bioethical principles for laboratory animals. Two groups were studied. In Group I (control DIC), disseminated intravascular coagulation was modelled with a single oral dose of the inducer "Efa-2" (8,330 mg/kg, administered on an empty stomach). "Efa-2" is a commercial anticoagulant-rodenticide bait based on ethylphenacin, a first-generation vitamin K antagonist of the 1,3-indanedione series; the 8,330 mg/kg figure is the dose of the ready bait (approximately 0.015% active ingredient), not of the purified compound. Mechanistically, ethylphenacin inhibits vitamin K epoxide reductase, depleting vitamin K-dependent coagulation factors (II, VII, IX, X) and proteins C and S, and damaging the vascular endothelium, thereby triggering secondary disseminated intravascular coagulation that progresses through the classic triphasic cycle. In Group II (suppressed granulopoiesis), the same inducer and the same dose were administered following pharmacological suppression of granulopoiesis.

**Granulopoiesis suppression (Group II).** Suppression was achieved with oral busulfan — an alkylating agent (1,4-butanediol dimethanesulfonate) that at low doses selectively suppresses granulopoiesis — administered as the preparation Myelosan (JSC "Zhovten", St. Petersburg) according to a two-stage regimen [Boiarchuk, 1998a; Boiarchuk, 2014]. In the first stage, busulfan was given at 10 mg/day for 5–7 days — until the absolute peripheral blood neutrophil count fell by 40–50% from the intact level. In the second stage, a maintenance dose of 4 mg/day was given for approximately 8 days to stabilise the reduced neutrophil count without deepening the cytopenia. The inducer was administered immediately, without an interval. This protocol established a distinct pre-induction state, designated "M" (post-busulfan), in which the absolute neutrophil count was reduced (from ~8.0 to ~3.9 × 10⁹/L), while haemostatic parameters were minimally but significantly shifted from the intact baseline (for factor XIII, $P < 0.001$) [Boiarchuk, 2014]; consequently, all changes in Group II are measured relative to state M, not to the intact baseline.

**Observables and measurements.** Six observables were measured. Four characterise the haemostatic system: plasma recalcification time (s), thrombin time (s), fibrinogen (mg%[^1]), and factor XIII activity (%). Two characterise the neutrophil compartment: serum acid phosphatase activity (lysosomal enzyme marker) and the degranulation index from the lysosomally granular formula (the fraction of neutrophils with pronounced degranulation, i.e. fewer than ten lysosomal granules) [Pigarevsky, 1975]. Group I was sampled at 16 time points over 19 days; Group II — at 8 time points over 8 days, after which its dynamics effectively stabilise. Data originate from the Boiarchuk (1998) dissertation and related publications; a substantial portion of the Group II dynamics is presented here for the first time. Full provenance is documented in Supplementary Appendix §S7.

[^1]: Fibrinogen is expressed in mg% (numerically equivalent to mg/dL), the unit used throughout the primary dataset.

### 2.2 Mathematical model

The model is a system of ODEs with five states tracking degranulation ($D$), acid phosphatase activity ($AP$), an inducer-derived coagulation pool ($H_c$), a neutrophil-derived coagulation pool ($H_n$), and factor XIII activity ($X$). $H_c$ and $H_n$ represent, respectively, the vascular-mediated (inducer-mediated) and neutrophil-mediated pools of consumed coagulation activity; $H_n$ has a limiting capacity $H_m$. The neutrophil-mediated effect entering the observable equations is the *effective coagulation load*

$$g_{Hn} = \frac{H_n}{1 - H_n/H_m},$$

a nonlinear function that rises sharply as the pool approaches saturation, reflecting accelerated consumption as $H_n$ approaches the limiting capacity $H_m$. The measured neutrophil count $N(t)$ is not a state variable: it is supplied as an experimental input for each group (one interpolator per group) — a choice justified by the fact that $N(t)$ is directly measured at each sampling point.

Six observables are computed as algebraic functions of the state vector. Four haemostatic observables (recalcification time, thrombin time, fibrinogen, factor XIII) are mapped from the states through observable-specific contribution coefficients; the remaining two (acid phosphatase and degranulation index) are read directly from the states $AP$ and $D$ and carry no separate coefficients. The model contains 26 parameters: rate constants for degranulation ($k_d$) and recovery/clearance of the degranulated state ($k_r$), acid phosphatase turnover ($k_{rl}$, $k_{cl}$), kinetics of the coagulation pools ($k_{ca}$, $k_{na}$, $k_{nd}$, $H_m$), the time and width of the inducer toxicity impulse ($t_{p2}$, $s_2$), and contribution coefficients for the four haemostatic channels. Group I and Group II share all parameters except two group-specific modifiers ($k_m$, $t_m$) that scale the effective rate constants in Group II to represent the busulfan effect; biologically, busulfan reduces the neutrophil count and shifts the impulse timing rather than per-cell production rates.

The model contains two structural priors — mathematical constraints that prevent solution ambiguity where the data alone are insufficient. The first — $W_{\text{SPLIT}} = 2.0$ — fixes the neutrophil-attributed fractions of three channels on day 2 to values derived independently from the day-1 contrast between the two groups (0.24 for recalcification, 0.76 for fibrinogen, 0.82 for factor XIII; full justification and $W$ scan in §S8). The second — $c_x \leq 600$ — constrains the factor XIII channel to a biologically interpretable subspace (full justification in §S9). Both priors were validated post-hoc by improved Group II fit relative to unconstrained alternatives. The full ODE formulation, parameter definitions, and observable equations are given in Supplementary Appendix §S1.

### 2.3 Parameter estimation

The model is fitted by minimising a joint cost function — a weighted sum of squared residuals across all six observables in both groups — using a multi-seed differential evolution pipeline with local refinement. Differential evolution (`scipy.optimize.differential_evolution`) is launched independently from five starting points (seeds); each global solution is refined by a Nelder-Mead → Powell → Nelder-Mead sequence (`scipy.optimize.minimize`). The result with the lowest cost among the five seeds is retained as the joint baseline. Full hyperparameters for the base pipeline are in §S2.2, for the ensemble pipeline in §S2.3; full estimates for all 26 parameters are in §S2.5 (Table S2). The implementation uses SciPy 1.15, NumPy 2.2, and Python 3.10; code and reproducibility tests are described in §S7.

The shared architecture (24 shared parameters plus two group-specific modifiers) trades some fit quality for individual groups against between-group consistency: separate fitting of Group II alone achieves approximately 22 percentage points higher average $R^2$ for Group II than joint fitting (§S10) — a gap that is predominantly architectural rather than due to overfitting. This penalty is accepted in exchange for a single shared mechanistic parametrisation for both groups.

### 2.4 Robustness analysis

Model robustness is assessed with four complementary protocols. Three of these, ensemble-based — parametric bootstrap, leave-one-out cross-validation, and neutrophil-count perturbation — share a common lightweight re-fitting pipeline distinct from the base pipeline of §2.3: one differential evolution seed per iteration followed by a three-stage local refinement Nelder-Mead → Powell → Nelder-Mead. This choice reflects the total number of re-fits — 168 across three analyses — for which the full multi-seed pipeline would be impractical. Full lightweight pipeline settings are in §S2.3.

Profile likelihood analysis of all 26 parameters [Raue et al., 2009; Kreutz et al., 2013] classifies each as well-identified (relative profile depth > 5%; six parameters: $t_{p2}$, $k_m$, $t_m$, $k_d$, $s_2$, $a_t$), weakly identified (five parameters), or *sloppy* (twelve parameters with relative depth < 2%). Parametric bootstrap ($N = 100$) [Efron & Tibshirani, 1993] generates synthetic datasets from baseline predictions with Gaussian noise ($\sigma$ equal to the baseline RMSE for each observable in each group) and re-fits the model on each, yielding individual confidence intervals for all parameters and prediction trajectories. Leave-one-out cross-validation [Stone, 1974] removes all six observables at each of the 23 non-anchor time points (15 in Group I, 8 in Group II) in turn, re-fits the model, and computes the PRESS statistic for the held-out point. Finally, sensitivity to the neutrophil input $N(t)$ is tested by perturbing it deterministically (scale factor $\alpha \in \{0.8,\, 0.9,\, 1.0,\, 1.1,\, 1.2\}$) and stochastically (log-normal noise per time point at CV = 10% and CV = 20%, $N = 20$ each).

### 2.5 Virtual experiments

Three virtual experiments propagate parameter uncertainty by running the 100-member bootstrap ensemble through prediction tasks. In the dose–response experiment, the Group II effective rate constants are redefined as $k_{r,G2} = k_r \times k_m$ and $t_{p2,G2} = t_{p2} \times t_m$ on a $15 \times 15$ log-uniform grid in $(k_m, t_m)$, with the Group II neutrophil profile preserved throughout (22,500 simulations in total). In the timing experiment, the busulfan effect is switched on at a variable time $t_{\text{intervention}}$ via two-segment ODE integration in which the state $(D, AP, H_c, H_n, X)$ is continuous across the boundary and only the rate constants change instantaneously; nine timing scenarios from $t = 0$ to no intervention are run at the observed Group II dose (900 simulations). In the dose × time experiment, two scenarios — high dose at late timing, half-dose at early timing — are run to directly test the dose–timing trade-off (200 simulations).

For each trajectory, four severity metrics are computed: peak hypocoagulation (maximum change in recalcification time), integrated coagulation disturbance (area under $|\Delta\text{recalcification}|$), factor XIII depletion nadir (minimum change in factor XIII activity), and peak effective coagulation load ($\max g_{Hn}$). For the timing experiment, three additional temporal metrics are computed: time to peak $g_{Hn}$, time to recovery ($g_{Hn}$ falls below 10% of its peak), and acute-phase duration (the interval between them). Severity metrics are evaluated on the Group II time scale (0–9 days) for the dose–response experiment and on the extended time scale (0–19 days) for the timing and dose × time experiments; the time to peak is defined as the first local maximum of $g_{Hn}(t)$, to avoid finite-horizon boundary artefacts.

---

## 3. Results

### 3.1 Step 1. Model fits the 19-day dynamics of both groups

Fitted simultaneously to both groups, the model reproduces the measured dynamics of all six observables. For Group I (15 fitting time points over 19 days), the mean coefficient of determination is $R^2 = 0.83$; for the busulfan-suppressed Group II (8 points over 8 days) — $R^2 = 0.69$. Most channels are reproduced well in both groups; the lower Group II average is caused by the factor XIII channel, which is structurally under-determined (§3.2).

Best agreement is achieved in the deep hypocoagulable phase, where the late-phase nadirs of factor XIII and fibrinogen are reproduced to within 1–11% (§3.4). The main discrepancy is in the early hypercoagulable phase, where the amplitude of two vascular-mediated channels — recalcification time and fibrinogen — is underestimated; the fibrinogen channel additionally exhibits a non-monotonic intermediate profile arising from near-mutual cancellation of two large opposing terms (§4.4). These discrepancies are confined to the early phase of vascular-mediated channels and do not affect the peak timing or group separation that underlies the main findings. Baseline fits are shown in Figure 1.

> **Figure 1.** Baseline model fits and experimental data for both groups, one panel per observable: (a) recalcification time, (b) thrombin time, (c) fibrinogen, (d) factor XIII activity, (e) acid phosphatase, (f) degranulation index. Group I — blue circles and solid line; Group II — red triangles and dashed line; points — group means ± SEM, curves — baseline fit with the lowest cost. All values are changes from each group's baseline (Group I from intact, Group II from state M); model curves are drawn only within the observed range for each group. The grey band (days 10–12) marks the window of deep hypocoagulation and Group I lethality.

### 3.2 Step 2. Parameter map of the model

Profile likelihood analysis reveals six well-identified parameters (relative profile depth > 5%: $t_{p2}$, $k_m$, $t_m$, $k_d$, $s_2$, $a_t$); the remaining twenty are weakly identified or *sloppy*. This is the universal *sloppiness* pattern typical of mechanistic systems-biology models [Gutenkunst, 2007]: the coexistence of a few stiff parametric directions with many soft ones is a structural property of ODE models whose parameter count exceeds the effective dimensionality of the available data, not a defect of an individual fit. Predictions depending on the well-identified parameters — impulse time $t_{p2}$, busulfan modifiers $k_m$ and $t_m$, degranulation rate constant $k_d$, impulse width $s_2$, thrombin–inducer coefficient $a_t$ — are robust to data limitations and carry narrow uncertainty bands.

Parametric bootstrap ($N = 100$) yields individual confidence intervals consistent with this classification: narrow for well-identified parameters and wide for *sloppy* ones (Table 1; the full set of 26 parameters is in Table S2).

**Table 1.** Well-identified parameters (relative profile depth > 5%): median and 95% confidence interval from the 100-member bootstrap ensemble. "Well-identified" refers to profile likelihood depth (local curvature of the cost surface); bootstrap intervals for $k_d$ and $s_2$ are wider, reflecting a heavy right tail in the global re-sampling distribution.

| **Parameter** | **Median [95% CI]** | **Role** |
|---|---|---|
| $t_{p2}$ | 9.217 [8.889, 10.034] | Time to peak of inducer toxicity impulse (days) |
| $k_m$ | 4.918 [3.462, 5.734] | Group II rate modifier (busulfan effect on rate constants) |
| $t_m$ | 0.427 [0.392, 0.467] | Group II time modifier (busulfan effect on impulse timing) |
| $k_d$ | 0.264 [0.218, 1.054] | Degranulation rate constant |
| $s_2$ | 1.757 [1.513, 2.712] | Width of the inducer toxicity impulse |
| $a_t$ | 5.659 [4.893, 6.437] | Thrombin / inducer impulse coefficient |

A special case is the factor XIII channel in Group II, which is structurally *under-determined* rather than merely *sloppy*. Among 100 bootstrap members, 41 yield a negative $R^2$ for Group II factor XIII, and the ensemble distribution is bimodal (Figure 2): the optimiser settles into different basins across re-samples. This reflects the limited information content of the available Group II data, not the estimation pipeline; the cost is otherwise stable across members. Sensitivity to the normalisation choice (range-based versus per-group standard deviations) only sharpens, rather than resolves, the multimodal landscape, confirming that the XIII under-determination is a structural property of the parameter manifold $\{a_x, c_x, b_x, k_x\}$, not a normalisation artefact (§S4).

> **Figure 2.** Parameter identifiability and structural under-determination of the factor XIII channel (100-member bootstrap ensemble). (a) Forest plot of coefficients of determination: median and 95% CI of $R^2$ for each of the six observables in both groups (Group I — blue circles; Group II — red triangles; 12 rows). Solid line — $R^2 = 0$, dashed line — $R^2 = 1$. Most channels are tightly and highly determined; the Group II factor XIII channel is the only interval extending below $R^2 = 0$. (b) Distribution of $R^2$ for Group II factor XIII across ensemble members (vertical line at $R^2 = 0$); the distribution is bimodal, reflecting optimiser settling into different basins: 41 of 100 members fall below zero.

Robustness of the fit to time-point removal and to neutrophil-input perturbations is bounded. Leave-one-out cross-validation shows that Group I predictions are robust to removal of any single time point (median PRESS = 6.5 across six observables; worst case $t = 11$, PRESS = 24.5, reflecting the role of the peak-DIC observation). Group II predictions are more sensitive to point removal (median PRESS = 21.5), consistent with the smaller sample size. The highest individual value — Group II at $t = 1$ (PRESS = 76.6, dominated by the acid phosphatase channel) — identifies early acid phosphatase dynamics as the least constrained aspect of the Group II fit. All re-fits converge to costs within 10% of the baseline (range 0.94–1.06), indicating stable parameter identification. Group I aggregate fit quality remains stable across all neutrophil-input perturbations ($R^2 \in [0.78, 0.83]$); well-identified parameters ($k_m$, $t_m$, $c_f$, $k_d$) show no systematic shift.

The model's parameter map is standard for its class. Well-identified parameters carry predictive content and are the foundation on which subsequent steps rest. *Sloppy* parameters limit the ability to make isolated counterfactual claims about individual rate constants, but do not affect aggregate predictions that depend on several parameters simultaneously.

### 3.3 Step 3. Internal consistency: mechanism decomposition

The third step is an internal consistency check of the model against the between-group difference on day 1 of the experiment. This is *not* external validation (that is in §3.4); it is a check of whether the imposed prior mechanism decomposition is reproduced by the model consistently across the re-sampling ensemble.

The prior targets are the neutrophil-attributed fractions on day 1, $(\Delta G_1 - \Delta G_2)/\Delta G_1$: 0.24 for recalcification, 0.76 for fibrinogen, 0.82 for factor XIII. The derivation is correctly posed, because the two groups have nearly identical haemostatic baselines (recalcification 78.7 vs. 78.0 s; fibrinogen 58.2 vs. 58.3 mg%; factor XIII 100.0 vs. 93.2%): busulfan altered the neutrophil count without shifting the haemostatic baseline. Imposing this prior ($W_{\text{SPLIT}} = 2.0$) yields fitted day-2 fractions: 0.240 [0.225, 0.249] for recalcification (vascular dominant) and 0.759 [0.738, 0.777] and 0.806 [0.777, 0.844] for fibrinogen and factor XIII (neutrophil dominant in both). The decomposition is shown in Figure 3.

> **Figure 3.** Mechanism decomposition: neutrophil-attributed fraction of each coagulation channel on day 2 of Group I (median and 95% CI, 100-member ensemble). Vertical dashed lines mark the prior targets derived from day 1 (recalcification 0.24; fibrinogen 0.76; factor XIII 0.82), imposed as soft constraints ($W_{\text{SPLIT}} = 2.0$).

**Table 2.** Mechanism decomposition: neutrophil-attributed fraction of each coagulation channel on day 2 of Group I. Prior targets are day-1 ratios $(\Delta G_1 - \Delta G_2)/\Delta G_1$; fitted values are median and 95% CI across the 100-member ensemble.

| **Channel** | **Prior target** | **Fitted median [95% CI]** | **Interpretation** |
|---|---|---|---|
| Recalcification time | 0.24 | 0.240 [0.225, 0.249] | Vascular dominant |
| Fibrinogen | 0.76 | 0.759 [0.738, 0.777] | Neutrophil dominant |
| Factor XIII | 0.82 | 0.806 [0.777, 0.844] | Neutrophil dominant |

The prior is necessary for identifiability: without it, the recalcification fraction is not identified across different optimiser seeds (0.34–0.48), and the decomposition is not unique (§S8). The decomposition is validated post-hoc by improved fit on the held-out (Group II) sample compared with unconstrained alternatives (+2–7 pp in $R^2_{\text{G2}}$). We therefore present these fractions as a regularised, prior-constrained, held-out-validated decomposition. One caveat applies to fibrinogen: without the prior, the model assigns a neutrophil fraction of approximately 0.05, so the value 0.76 is an *imposed* target derived from day 1, not an *independently reproduced* feature of day-2 dynamics.

The strong neutrophil contribution to factor XIII (~80%) is consistent with the mechanism of elastase-mediated activation of plasma XIII [Henriksson et al., 1980; Bagoly et al., 2008]: neutrophil elastase, released from the same azurophilic granules for which acid phosphatase serves as a marker, converts plasma XIII by limited proteolysis into an active truncated form that is subsequently rapidly consumed in the cascade (detailed in §4.2). The vascular dominance in recalcification is consistent with the rapid onset of hypocoagulation following inducer administration, before neutrophil-mediated effects have time to develop.

### 3.4 Step 4. External validation: the model reproduces observations not in the training data

This is the pivotal step. The first three steps established that the model fits (§3.1), that its parameter map is standard (§3.2), and that it is internally consistent with the day-1 between-group difference (§3.3). Here the model is tested against claims that did not enter its training data: the time to peak hypocoagulation, group separation, and factor XIII and fibrinogen nadirs.

The model is validated against the observed lethality contrast (30% in Group I, days 10–12; 0% in Group II) [Boiarchuk, 1998a] by simulating the pure Group I dynamics (Group I neutrophil profile, without busulfan) through the bootstrap ensemble. The model reproduces severe hypocoagulation in Group I (peak $\Delta$recalcification 147 s; factor XIII nadir −77%; fibrinogen nadir −58 mg%) versus near-absent hypocoagulation in the busulfan-modified Group II baseline (peak $\Delta$recalcification ~7 s) — a 22-fold separation, consistent with the observed lethality difference. The peak falls on day 11, coinciding with both the observed time of maximum hypocoagulation and the lethality window (days 10–12).

Channel-level agreement is differentiated: the factor XIII nadir matches the observation to within 1% (−77.1 vs. −76.7%), and the fibrinogen nadir to within 11% (−58.3 vs. −52.6 mg%); the recalcification peak is underestimated by ~29% (147 vs. 207 s). The amplitude underestimation is confined to vascular-mediated channels (recalcification peak and early fibrinogen rise), is not systemic, and is consistent with the shared-fitting architecture penalty (§2.3); it is reported as a known limitation (§4.4). Validation is therefore qualitative and directional — the model reproduces the timing and group separation underlying the observed lethality — rather than a quantitative lethality model (Table 3).

**Table 3.** Severity of Group I vs. Group II and validation against observed Group I values. Model values — median [95% CI] from the 100-member ensemble (pure Group I dynamics and busulfan-modified Group II baseline). Observed Group I values — from dissertation tables. Group I / Group II separation by peak recalcification: 22.2× (147 s / 6.6 s — the exact unrounded Group II value, displayed as 7 s in the table column).

| **Metric** | **Group I model [95% CI]** | **Observed (Group I)** | **Agreement** | **Group II model [95% CI]** |
|---|---|---|---|---|
| Peak hypocoagulation (max Δrecalc, s) | 147 [122, 176] | 207 | Model 29% lower | 7 [3, 11] |
| Factor XIII nadir (min ΔXIII, %) | −77.1 [−94.4, −61.4] | −76.7 | Within 1% | −13.8 [−19.7, −7.3] |
| Fibrinogen nadir (min Δfib, mg%) | −58.3 [−69.1, −46.4] | −52.6 | Within 11% | −1.4 [−8.1, 0.0] |
| Peak time (t at max recalc, days) | 11 [10, 11] | 11 | Exact | 5 [5, 6] |

Four claims are validated independently of the training data: peak timing (exact), group separation (22×), factor XIII nadir (1%), and fibrinogen nadir (11%). The model therefore merits the next step — its use as a prediction tool.

### 3.5 Step 5. Prediction: therapeutic window and dose × time thresholds

Based on the validated model, three virtual experiments investigate what it predicts about myelosuppressive intervention: dose–response dependence, timing dependence, and their interaction.

#### Dose–response dependence

The dose–response experiment shows that busulfan-mediated kinetic modification of neutrophil-mediated rate constants reduces peak hypocoagulation approximately 7-fold and integrated coagulation disturbance approximately 2.5-fold, relative to the same neutrophil profile without kinetic modification. The observed experimental dose ($k_m = 4.93$; $t_m = 0.43$) lies on the dose–response curve at intermediate severity. Kinetic modification alone, applied to the Group II neutrophil profile, does *not* reproduce Group I-level severity: substituting the Group I neutrophil profile into the model (§3.4) yields ~22-fold higher peak hypocoagulation. This indicates that the protective effect of busulfan acts predominantly through a reduction in neutrophil *count* rather than through kinetic modification per se. Phase diagrams are shown in Figure 4, and a dose–response slice at the observed timing is shown in Figure 5.

> **Figure 4.** Dose–response phase diagrams for busulfan in the parameter space $(k_m, t_m)$ (median per cell, 100-member ensemble): (a) peak hypocoagulation (max Δrecalcification, s; contours at 10, 20, 30, 40 s), (b) factor XIII nadir (min ΔXIII, %), (c) peak effective coagulation load (max $g_{Hn}$). Circle — no kinetic effect ($k_m = 1$; $t_m = 1$); star — observed Group II dose ($k_m = 4.93$; $t_m = 0.43$). The Group II neutrophil profile is preserved throughout, so severity reflects kinetic modification only. All four severity metrics are in §S6.

> **Figure 5.** Dose–response slice: peak hypocoagulation versus rate modifier $k_m$ at fixed time modifier $t_m \approx 0.45$ (median and 95% CI band, 100-member ensemble). Dashed line — severity without busulfan ($k_m = 1$); dash-dot line and triangle — observed Group II operating point ($k_m = 4.93$). The confidence band narrows with increasing $k_m$: the predicted attenuation is more certain at higher kinetic suppression.

#### Biphasic therapeutic window

Busulfan intervention achieves near-complete DIC attenuation when applied within 2.5 days of insult (peak recalcification change 7–8 s, comparable to the observed Group II outcome). A critical half-day transition occurs between days 2.5 and 3, over which peak severity approximately doubles (7.9 → 14.4 s). Beyond day 3, busulfan retains a partial protective effect — reducing peak severity 2–3-fold relative to no intervention — but cannot prevent acute DIC onset. The therapeutic window therefore comprises a *prevention phase* (0–2.5 days) and a *mitigation phase* (2.5–6+ days).

Intervention at $t = 0$ and $t = 1$ yields indistinguishable results: the inducer toxicity impulse $V(t)$ (peak at $\tau_v = 1.5$ days, reflecting the time to peak effect of ethylphenacin) does not accumulate sufficient effective coagulation load in the first 24 hours to independently trigger the cascade — consistent with the expected latency between anticoagulant exposure and measurable coagulopathy. The therapeutic window is shown in Figure 6.

> **Figure 6.** Therapeutic window: DIC severity versus busulfan intervention timing (median and 95% CI band, 100-member ensemble): (a) peak hypocoagulation, (b) factor XIII nadir, (c) peak effective coagulation load. Shaded band (days 2.5–3) — critical transition; dashed line on each panel — no-intervention reference. The transition is reported as occurring between sampled time points (days 2.5 and 3), not at a single interpolated value. Temporal metrics are in §S5.

#### Dose × time thresholds

A focused experiment tests whether dose and timing act as a continuous trade-off or as independent thresholds. Doubling the dose at late intervention ($t = 4$ days; $k_m = 10$ vs. 4.93) yields no measurable improvement in peak severity (28.0 vs. 28.2 s) — a dose ceiling once the cascade is established. Conversely, halving the dose at optimal timing ($t = 0$; $k_m = 2.5$) gives a substantially worse outcome (34.0 vs. 7.1 s), exceeding even the severity of late full-dose intervention. Busulfan's protective effect therefore requires both a sufficient dose (above the rate-suppression threshold) and timely administration (before cascade lock-in) — not just one of the two (Table 4).

**Table 4.** Dose × time combinations for testing whether dose and timing trade off continuously or act as independent thresholds. Peak hypocoagulation (max Δrecalcification, s) — median [95% CI] from the 100-member ensemble; each combination is compared with its full-dose reference at the same timing.

| **Scenario** | **Dose ($k_m$)** | **Timing (days)** | **Peak Δrecalc [95% CI]** | **Reference (full dose, same timing)** | **Outcome** |
|---|---|---|---|---|---|
| Double dose, late | 10.0 | 4 | 28.0 [0.0, 38.9] | 28.2 (full dose, $t = 4$) | No improvement (dose ceiling) |
| Half-dose, early | 2.5 | 0 | 34.0 [22.7, 44.0] | 7.1 (full dose, $t = 0$) | Substantially worse (dose floor) |
| *Full dose, early (ref)* | 4.93 | 0 | 7.1 [0.6, 14.7] | — | Prevention |
| *Full dose, late (ref)* | 4.93 | 4 | 28.2 [1.5, 39.0] | — | Mitigation |
| *No intervention (ref)* | — | — | 75.6 [60.5, 92.0] | — | No treatment |

---

## 4. Discussion

### 4.1 Summary: five steps and what each delivered

To our knowledge, this is the first mechanistic ODE model simultaneously fitted to two experimental groups — with and without neutrophil suppression — that makes testable predictions about the timing and strength of myelosuppressive intervention. The work proceeds in five steps. First, the model fits the 19-day dynamics of both groups with $R^2 = 0.83 / 0.69$ across all six observables (Step 1). Second, its parameter map — six well-identified and twelve *sloppy* parameters — is standard for its class and identifies which subsequent claims rest on data and which require additional constraints (Step 2). Third, the imposed prior mechanism decomposition is internally consistent with the between-group difference on day 1 of the experiment, derived independently (Step 3). Fourth, the model makes four claims not in the training data, and all four agree with observation: peak timing (exact), group separation (22-fold), factor XIII nadir (1%), fibrinogen nadir (11%) (Step 4). Fifth, this validated model predicts a narrow biphasic therapeutic window with a sharp transition between days 2.5 and 3, with dose and timing acting as independent thresholds rather than a continuous trade-off (Step 5).

### 4.2 Biological interpretation: mechanism decomposition and its limits

This subsection and the next move from the step-by-step structure of the Results to two overarching themes — biological (below) and clinical (§4.3) — that integrate material from several steps simultaneously.

The mechanism decomposition obtained in Step 3 is biologically interpretable. The vascular dominance in the recalcification channel is consistent with the rapid onset of hypocoagulation after inducer administration, before neutrophil-mediated effects have time to develop: early contact-phase disturbances reflect direct inducer toxicity to the vasculature and coagulation cascade. The strong neutrophil contribution to factor XIII (~80%) is consistent with the elastase-mediated activation mechanism: neutrophil elastase, released from azurophilic granules upon degranulation (the same granular population for which acid phosphatase is a marker [Borregaard & Cowland, 1997]), performs limited proteolysis of plasma factor XIII, generating an active truncated form independently of thrombin [Henriksson et al., 1980; Bagoly et al., 2008]; the prematurely activated XIII is then rapidly consumed in the cascade, producing the observed nadirs. This mechanism directly links degranulation (model input through $AP$) to XIII depletion (model output) in a way that requires no auxiliary assumption about intracellular XIII storage in neutrophils — a pool that modern literature associates more with platelets, monocytes, and macrophages than with neutrophils [Muszbek et al., 2011; Mitchell & Mutch, 2019]. The parallel neutrophil dominance in the fibrinogen channel is consistent with fibrinogenolysis driven by the same neutrophil serine proteases [Plow & Edgington, 1975; Bach-Gansmo et al., 1994]; this reinforces but does not mechanistically exhaust the explanation, because the fibrinogen channel also depends on the plasmin-mediated pathway (§S1.6).

An important methodological distinction applies here. The recalcification channel (0.24, vascular dominant) is what the data *independently* support: without the prior, different optimiser seeds give fractions in the range 0.34–0.48, consistent with the same vascular-dominant reading. The factor XIII channel (0.82, neutrophil dominant) is also relatively stable (without the prior — 0.73–0.78). The fibrinogen fraction of 0.76, however, is an *imposed* target derived from day 1: without the prior, the model assigns a neutrophil fraction of approximately 0.05, which is 15 times smaller. The interpretation of fibrinogen should therefore be read as a hypothesis that the model quantifies under the imposed prior, not as a feature independently reproduced by day-2 dynamics. This limitation is transparently documented (§3.3, §S8).

### 4.3 Clinical interpretation: the biphasic window as a hypothesis for testing

The Step 5 prediction carries clinical implications that should be read with explicit limitations. The observed Group II operating point ($k_m = 4.93$; $t_m = 0.43$) lies near the plateau of the modelled efficacy curve — further escalation of suppression would yield little additional benefit, while timing appears at least as influential as the degree of suppression. Within the model, intervention before cascade lock-in prevents the deep hypocoagulable phase; the same intervention after the 2.5 → 3 day transition can only limit its scale 2–3-fold.

The biphasic window consists of a prevention phase (0–2.5 days) and a mitigation phase (2.5–6+ days). The sharpness of the half-day transition is informative: it suggests a threshold in the accumulation of effective coagulation load — driven by degranulation marked by acid phosphatase — beyond which the consumptive process becomes self-sustaining. The observation that intervention at $t = 0$ and $t = 1$ yields indistinguishable results is consistent with the latency between inducer exposure and load accumulation, mirroring the expected delay between anticoagulant exposure and measurable coagulopathy.

The model also shows that the busulfan protective effect acts predominantly through a reduction in neutrophil *count* rather than through kinetic modification per se: substituting the Group I neutrophil profile into the busulfan-modified model yields approximately 22-fold higher peak hypocoagulation (§3.5). This is consistent with the observed lethality contrast (30% in Group I vs. effectively zero in Group II) [Boiarchuk, 1998a].

Since ethylphenacin is an anticoagulant rodenticide — a vitamin K antagonist — its poisoning mechanism invites a cautious parallel with the clinical management of vitamin K antagonist exposure, where the timing of reversal relative to the onset of coagulopathy is a recognised determinant of outcome [Schulman & Furie, 2015]. The parallel should be drawn carefully and with explicit limitations. The present model does not represent the vitamin K cycle explicitly: the inducer enters as a phenomenological toxicity impulse, not as a pharmacokinetic model of vitamin K epoxide reductase inhibition; the analogy holds at the level of the poisoning mechanism and the importance of intervention timing, not at the level of validated pharmacological correspondence. The prolonged tissue half-life of indanediones and related anticoagulants [Watt et al., 2005] and the distinction between suppressing the neutrophil contribution and replacing depleted coagulation factors further qualify the comparison.

### 4.4 Limitations by step

It is convenient to view the model's limitations through the same five-step structure — each step has its own boundaries, and it is important not to conflate them.

**Step 1 (fitting).** The two vascular-mediated channels (recalcification, fibrinogen) reproduce the late-phase nadir well but underestimate early hypercoagulable amplitude. For fibrinogen, the cause is explicit in the channel decomposition (§S1): fibrinogen output is a small difference of two much larger opposing terms (the acid-phosphatase contribution and the neutrophil-dependent contribution), each severalfold exceeding their sum near days 5–7, so small phase mismatches between them produce a non-monotonic intermediate profile. The shared-fitting architecture penalty adds ~22 pp to the average Group II $R^2$ compared with separate fitting (§S10), accepted in exchange for a shared mechanistic parametrisation.

**Step 2 (identifiability).** The factor XIII channel in Group II is structurally under-determined: across bootstrap re-samples its fit is bimodal and frequently poor, and this property is robust to normalisation choice (41% negative $R^2$ under range normalisation; 83% under per-group standard deviations — both extremes confirm the structural origin of the problem, §S4). The sloppiness of twelve parameters is a structural property of systems-biology models with parameter counts exceeding the effective data dimensionality [Gutenkunst, 2007], not a fitting defect.

**Step 3 (internal consistency).** The fibrinogen fraction 0.76 is an imposed target, not a derived feature of day-2 dynamics (§4.2). The biological interpretation of this channel reads as a hypothesis that the model quantifies, not its independent confirmation.

**Step 4 (validation).** Validation against the observed lethality contrast is qualitative and directional, not a quantitative lethality model. The recalcification peak is underestimated by ~29%, so quantitative predictions of early hypercoagulable amplitude should be read with appropriate caution; peak timing, group separation, and late-phase nadirs are reproduced exactly or within 11%.

**Step 5 (prediction).** Busulfan pharmacokinetics are idealised as an instantaneous kinetic effect, whereas real myelosuppression develops over 5–7 days under the two-stage protocol (§2.1). The timing-of-intervention simulation therefore represents an idealised scenario of immediate pharmacological effect, not a realistic pharmacokinetic–pharmacodynamic (PK/PD) model. The Group II neutrophil interpolator is extrapolated flat beyond the last measurement ($t = 8$ days), which is a model assumption, not data. The 2.5–3-day phase boundary reflects the 0.5-day grid resolution at this scanning point.

The experimental basis is a veterinary (rabbit) model, and extrapolation to clinical DIC carries the usual caveats of interspecies translation.

### 4.5 Future directions

Three extensions would strengthen the framework. Additional Group II time points, especially around early acid phosphatase dynamics and the factor XIII trajectory, would directly address Step 2: they could move the fibrinogen channel from imposed-prior to data-derived. An explicit PK/PD layer for busulfan would replace the idealised instantaneous effect in Step 5 and allow testing of dose–timing predictions against time-resolved exposure. Alternative cost function formulations, including per-observable adaptive normalisation, may partially alleviate factor XIII channel sensitivity, although our preliminary tests indicate that improvement is not straightforward (§S4).

The Step 5 predictions formulate experimental hypotheses awaiting testing. First: an intervention experiment with varying myelosuppression timing should show a sharp transition between days 2.5 and 3 in DIC severity. Second: doubling the dose at late intervention timing yields no measurable improvement, whereas halving the dose at optimal timing sharply worsens the outcome. Third: the protection acts predominantly through a reduction in neutrophil *count*, so alternative agents that reduce neutrophil count without busulfan kinetics should provide comparable protection if applied within the prevention window.

---

## 5. Conclusions

We constructed a mechanistic ODE model of neutrophil-mediated DIC with shared biochemistry for both experimental groups and carried it through five validation steps. The model's parameter map is standard for its class: six well-identified parameters carry predictive content, the remainder are *sloppy*, reflecting the universal property of mechanistic systems-biology models of this size. The model is internally consistent with the between-group difference on day 1 of the experiment and is externally validated against four claims not in the training data: peak timing (day 11, exact), group separation (22-fold), factor XIII nadir (1%), and fibrinogen nadir (11%). According to this validated model, myelosuppressive intervention has a narrow biphasic therapeutic window with a sharp transition between days 2.5 and 3, with dose and timing acting as independent thresholds. This prediction formulates the longstanding qualitative hypothesis about the role of neutrophils in the hypocoagulable phase of DIC as a quantitative, testable framework for future interventional experiments.

---

## Declarations

**Ethics approval.** Not applicable: no new animal experiments were performed. Experimental data are taken from previously published sources [Boiarchuk, 1998a; Boiarchuk, 2014].

**Funding.** The authors received no external funding; the work was carried out at personal expense.

**Conflict of interest.** The authors declare no conflict of interest.

**Data and code availability.** The experimental data (group time series with standard errors), model source code, analytical scripts, and result artefacts supporting the findings are available in the project repository [repository URL to be provided]; the provenance of each data value and the reproduction protocol are included therein. Additional details are in Supplementary Information (§S1–§S10).

**Author contributions.** O.D.B. developed and conducted the experimental work, provided biological interpretation, and led the Introduction and Discussion. O.O. developed the mathematical model, performed numerical estimation, robustness analyses, and virtual experiments, implemented the analytical code, and led the Methods and Results. Both authors reviewed and approved the manuscript.

---

## References

- Boiarchuk O.D. (1998a) The role of the lysosomal apparatus of neutrophilic leukocytes in the formation of disseminated intravascular coagulation syndrome: abstract of the thesis for the degree of Candidate of Biological Sciences, speciality 03.00.13. Institute of Physiology named after O.O. Bohomolets, NAS of Ukraine, Kyiv. 16 pp. *(in Ukrainian)*

- Boiarchuk O.D. (1998b) Experimental model of DIC syndrome. *Visnyk Problem Biolohii i Medytsyny* (7):132–138. *(in Russian)*

- Boiarchuk E.D. (2008) Changes in neutrophil activity during the formation of disseminated intravascular coagulation syndrome. *Scientific Bulletin of Mykolaiv State University named after V.O. Sukhomlynsky. Series: Biological Sciences* 23(3):14–17. *(in Russian)*

- Boiarchuk E.D., Lunina N.V. (2012) Histochemical characteristics of neutrophils in DIC syndrome. *Visnyk of Luhansk National University named after Taras Shevchenko. Medical and Biological Sciences* 17(252):19–25. *(in Russian)*

- Boiarchuk E.D. (2013) Dynamics of granulocyte acid phosphatase in DIC syndrome. *Visnyk of Luhansk National University named after Taras Shevchenko. Biological Sciences* 19(278), Part I:6–13. *(in Russian)*

- Boiarchuk O.D. (2014) Dynamics of neutrophil acid phosphatase in DIC syndrome under conditions of granulopoiesis suppression. *Visnyk of Luhansk National University named after Taras Shevchenko. Biological Sciences* 12(295), Part I:5–13. *(in Ukrainian)*

- Boiarchuk O.D. (2023a) Effect of granulopoiesis suppression on the haemostatic system in DIC syndrome. In: *Current Issues in Biology and Medicine: Proceedings of the XIX All-Ukrainian Scientific Conference* (Lubny, June 2, 2023). Lubny: State Institution "LNU named after Taras Shevchenko". pp. 9–10. *(in Ukrainian)*

- Boiarchuk O. (2023b) Characteristics of neutrophils in DIC syndrome. *Scientific Collection «InterConf+»* 32(151):410–414. doi:10.51582/interconf.19-20.04.2023.042

- Pigarevsky V.Ye. (1975) Lysosomal-cationic test. *Pathological Physiology and Experimental Therapy* (3):86–88. *(in Russian)*

- Alhamdi Y, Toh CH (2017) Recent advances in pathophysiology of disseminated intravascular coagulation: the role of circulating histones and neutrophil extracellular traps. *F1000Research* 6:2143. doi:10.12688/f1000research.12498.1

- Bach-Gansmo ET, Halvorsen S, Godal HC, Skjønsberg OH (1994) Degradation of the α-chain of fibrin by human neutrophil elastase reduces the stimulating effect of fibrin on plasminogen activation. *Thrombosis Research* 75(3):307–317. doi:10.1016/0049-3848(94)90241-0

- Bagoly Z, Fazakas F, Komáromi I, Haramura G, Tóth E, Muszbek L (2008) Cleavage of factor XIII by human neutrophil elastase results in a novel active truncated form of factor XIII A subunit. *Thrombosis and Haemostasis* 99(4):668–674. doi:10.1160/TH07-09-0577

- Borregaard N, Cowland JB (1997) Granules of the human neutrophilic polymorphonuclear leukocyte. *Blood* 89(10):3503–3521. doi:10.1182/blood.V89.10.3503

- Efron B, Tibshirani RJ (1993) *An Introduction to the Bootstrap.* Chapman & Hall, New York. 456 pp.

- Engelmann B, Massberg S (2013) Thrombosis as an intravascular effector of innate immunity. *Nature Reviews Immunology* 13(1):34–45. doi:10.1038/nri3345

- Gando S, Levi M, Toh CH (2016) Disseminated intravascular coagulation. *Nature Reviews Disease Primers* 2:16037. doi:10.1038/nrdp.2016.37

- Gutenkunst RN, Waterfall JJ, Casey FP, Brown KS, Myers CR, Sethna JP (2007) Universally sloppy parameter sensitivities in systems biology models. *PLoS Computational Biology* 3(10):e189. doi:10.1371/journal.pcbi.0030189

- Henriksson P, Nilsson IM, Ohlsson K, Stenberg P (1980) Granulocyte elastase activation and degradation of factor XIII. *Thrombosis Research* 18(3):343–351. doi:10.1016/0049-3848(80)90329-1

- Kreutz C, Raue A, Kaschek D, Timmer J (2013) Profile likelihood in systems biology. *FEBS Journal* 280(11):2564–2571. doi:10.1111/febs.12276

- Levi M, ten Cate H (1999) Disseminated intravascular coagulation. *New England Journal of Medicine* 341(8):586–592. doi:10.1056/NEJM199908193410807

- Levi M, Scully M (2018) How I treat disseminated intravascular coagulation. *Blood* 131(8):845–854. doi:10.1182/blood-2017-10-804096

- Massberg S, Grahl L, von Bruehl ML, Manukyan D, Pfeiler S, Goosmann C, Brinkmann V, Lorenz M, Bidzhekov K, Khandagale AB, Konrad I, Kennerknecht E, Reges K, Holdenrieder S, Braun S, Reinhardt C, Spannagl M, Preissner KT, Engelmann B (2010) Reciprocal coupling of coagulation and innate immunity via neutrophil serine proteases. *Nature Medicine* 16(8):887–896. doi:10.1038/nm.2184

- Mitchell JL, Mutch NJ (2019) Let's cross-link: diverse functions of the promiscuous cellular transglutaminase factor XIII-A. *Journal of Thrombosis and Haemostasis* 17(1):19–30. doi:10.1111/jth.14348

- Muszbek L, Bereczky Z, Bagoly Z, Komáromi I, Katona É (2011) Factor XIII: a coagulation factor with multiple plasmatic and cellular functions. *Physiological Reviews* 91(3):931–972. doi:10.1152/physrev.00016.2010

- Plow EF, Edgington TS (1975) An alternative pathway for fibrinolysis. I. The cleavage of fibrinogen by leukocyte proteases at physiologic pH. *Journal of Clinical Investigation* 56(1):30–38. doi:10.1172/JCI108076

- Raue A, Kreutz C, Maiwald T, Bachmann J, Schilling M, Klingmüller U, Timmer J (2009) Structural and practical identifiability analysis of partially observed dynamical models by exploiting the profile likelihood. *Bioinformatics* 25(15):1923–1929. doi:10.1093/bioinformatics/btp358

- Schulman S, Furie B (2015) How I treat poisoning with vitamin K antagonists. *Blood* 125(3):438–442. doi:10.1182/blood-2014-08-597781

- Squizzato A, Gallo A, Levi M, Iba T, Levy JH, Erez O, Ten Cate H, Solh Z, Gando S, Toh CH, Cuker A (2020) Underlying disorders of disseminated intravascular coagulation: Communication from the ISTH SSC Subcommittees on Disseminated Intravascular Coagulation and Perioperative and Critical Care Thrombosis and Hemostasis. *Journal of Thrombosis and Haemostasis* 18(9):2400–2407. doi:10.1111/jth.14946

- Stone M (1974) Cross-validatory choice and assessment of statistical predictions. *Journal of the Royal Statistical Society, Series B* 36(2):111–133. doi:10.1111/j.2517-6161.1974.tb00994.x

- Watt BE, Proudfoot AT, Bradberry SM, Vale JA (2005) Anticoagulant rodenticides. *Toxicological Reviews* 24(4):259–269. doi:10.2165/00139709-200524040-00005
