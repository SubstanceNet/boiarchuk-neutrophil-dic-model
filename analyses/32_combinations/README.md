# Analysis 32 — Dose × timing combinations (Phase 4.5)

## Question

Does higher myelosan dose rescue late intervention timing? Conversely,
is reduced dose at early timing sufficient for protection? These two
scenarios test the dose × timing interaction in a focused, hypothesis-
driven way (rather than full sweep).

## Hypothesis (pre-registered)

"Timing > dose": early intervention with half dose should outperform
late intervention with double dose. If supported, this would simplify
the clinical message to "timing is decisive".

## Method

Two specific scenarios using the analysis 31 simulation framework
(two-segment ODE with time-dependent kr/tp2):

| scenario | km | tm | t_intervention | rationale |
|----------|-----|-----|---------------|-----------|
| combo1_high_dose_late | 10.0 | 0.43 | 4.0 | rescue attempt — does stronger dose compensate for late timing? |
| combo2_half_dose_early | 2.5 | 0.6 | 0.0 | dose-vs-timing trade-off — is timing alone sufficient? |

Reference points (from analysis 31):
- Full dose at t=0 (G2 baseline): "gold standard"
- Full dose at t=4: "late timing reference"
- No intervention: "untreated reference"

100 bootstrap ensemble members per scenario. ~3 seconds wall-clock.

## Outputs

- `results/combinations_raw.pkl` — per-member predictions + trajectory samples
- `results/combinations_summary.json` — ensemble percentiles per scenario
- `FINDINGS.md` — interpretation
