# S2. Parameter estimation pipeline and full estimates

*Part of the Supplementary Information for the manuscript “A mechanistic model of neutrophil-driven disseminated intravascular coagulation…” Main-text cross-reference: see Methods §2 and Results §3.*

Differential-evolution settings, polish sequence, and convergence criteria (`src/fit.py`).

**Table S2.** Estimates and 95% bootstrap confidence intervals for all 26 parameters (100-member ensemble), sorted by relative CI width (an identifiability spectrum, tightest first). Parameters flagged † are the six classified as well-identified by profile likelihood (relative depth > 5%). Relative width is (upper − lower)/|median|.

| Parameter | Description | Median [95% CI] | Rel. width | Well-id. |
| --- | --- | --- | --- | --- |
| tp2 | Inducer-toxicity pulse peak time (Group I) | 9.217 [8.889, 10.03] | 0.12× | † |
| tm | Group II busulfan modifier on τp2 (timing) | 0.4267 [0.3918, 0.4675] | 0.18× | † |
| at | Thrombin / inducer-pulse coefficient | 5.659 [4.893, 6.437] | 0.27× | † |
| ar | Recalcification / inducer-pulse coefficient | 34.74 [28, 40.01] | 0.35× | |
| km | Group II busulfan modifier on kr (rate) | 4.918 [3.462, 5.734] | 0.46× | † |
| cr | Recalcification / AP coefficient | 35.61 [27.55, 45.11] | 0.49× | |
| cx | XIII production / AP·Nr (azurophil-granule store) | 545.8 [294.8, 600] | 0.56× | |
| s2 | Inducer-toxicity pulse width | 1.757 [1.513, 2.712] | 0.68× | † |
| ax | XIII production / inducer-pulse | 47.21 [25.63, 67.73] | 0.89× | |
| bf | Fibrinogen / gHn coefficient (consumption) | 6.219 [2.335, 7.999] | 0.91× | |
| cf | Fibrinogen / AP coefficient (neutrophil-secretion-driven) | 99.68 [59.87, 154.7] | 0.95× | |
| af | Fibrinogen / inducer-pulse coefficient | 9.949 [5.527, 15.03] | 0.96× | |
| kx | XIII liver-modulated resynthesis | 2.604 [1.408, 4.047] | 1.01× | |
| bx | XIII degradation / gHn | 34.07 [11.77, 49.01] | 1.09× | |
| br | Recalcification / gHn coefficient | 8.876 [3.043, 13.49] | 1.18× | |
| bt | Thrombin / gHn coefficient | 0.5546 [0.1854, 0.8652] | 1.23× | |
| kcl | AP clearance rate | 12.01 [3.372, 18.25] | 1.24× | |
| krl | AP release rate from degranulated cells | 12.69 [4.001, 19.97] | 1.26× | |
| knd | Hn decay rate | 6.167 [1.94, 9.999] | 1.31× | |
| a2 | Inducer-toxicity pulse amplitude | 3.423 [2.654, 8.312] | 1.65× | |
| kna | Hn formation rate (from AP²) | 257.4 [80.92, 644.6] | 2.19× | |
| kd | Degranulation rate constant | 0.2635 [0.2179, 1.054] | 3.17× | † |
| Hm | Hn carrying capacity | 290.5 [11.11, 999.8] | 3.40× | |
| kca | Hc accumulation from inducer | 3.834 [0.1334, 33.34] | 8.66× | |
| kr | Recovery/clearance of degranulated state (Group I) | 0.247 [0.1802, 2.693] | 10.17× | |
| df | Fibrinogen / Hc coefficient (inducer pathway) | 1.037 [0.1221, 13.01] | 12.43× | |
