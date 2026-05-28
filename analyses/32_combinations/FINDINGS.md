# Analysis 32 — Dose × timing combinations (Phase 4.5)

**Status:** closed. 2 scenarios × 100 ensemble = 200 simulations, ~3
seconds wall-clock.

## Hypothesis test result

**Pre-registered hypothesis:** "Timing > dose" — half dose at early
timing would outperform double dose at late timing.

**Result: HYPOTHESIS REJECTED.**

Comparison:
- combo1 (km=10, t=4): max_recalc = 28.03
- combo2 (km=2.5, t=0): max_recalc = 34.02

Combo1 < Combo2. **High dose at late timing produces less severe DIC
than half dose at early timing.** The relationship is more nuanced
than "timing alone determines outcome".

## Results table

| scenario | max_recalc | auc_recalc | min_xiii | t_peak | t_recovery |
|----------|------------|------------|----------|--------|------------|
| **REFERENCES** | | | | | |
| full dose at t=0 (gold) | 7.13 | 91.52 | -14.56 | 3.86 | 8.24 |
| full dose at t=4 | 28.18 | 119.55 | -47.40 | 4.00 | 7.69 |
| no intervention | 75.57 | 606.00 | -108.27 | 10.52 | 17.14 |
| **COMBINATIONS** | | | | | |
| combo1: km=10, t=4 | 28.03 | 109.77 | -46.61 | 4.00 | 6.19 |
| combo2: km=2.5, t=0 | 34.02 | 209.81 | -46.04 | 6.19 | 10.76 |

## Interpretation: dose ceiling and dose floor

### Combo 1 — dose ceiling at late timing

Doubling the dose (km=4.93 → km=10) at late intervention (t=4) yields
**essentially no improvement** vs full dose at the same timing:
- full dose t=4: max_recalc = 28.18
- 2x dose t=4:  max_recalc = 28.03
- Difference: -0.15 (<1%)

**Mechanism:** by day 4, accumulated AP and Hn have driven the DIC
cascade well past the point where further kr suppression provides
benefit. The damage is largely done; myelosan modifies only the
recovery phase. There is a **dose ceiling** at late timing.

t_recovery actually improves with higher dose (6.19 vs 7.69), but
peak severity is largely set by the time of intervention, not the
dose magnitude.

### Combo 2 — dose floor at early timing

Reducing dose to half (km=2.5) at optimal timing (t=0) yields
**substantially worse** outcome vs full dose at the same timing:
- full dose t=0: max_recalc = 7.13
- half dose t=0: max_recalc = 34.02
- Severity multiplier: 4.8x

Notably, half-dose-early (34.02) is **worse**
than full-dose-late (28.18). Timing
alone is NOT sufficient; minimum effective dose threshold applies.

**Mechanism:** km=2.5 is sub-threshold for adequate kr suppression
during the first 2 days when V(t) is at peak. Insufficient suppression
allows AP accumulation and Hn cascade despite optimal timing.

## Refined clinical message

The simple "timing > dose" hypothesis is rejected. The actual finding is
stronger and more nuanced:

**Both adequate dose AND early timing are required.** Neither suffices
alone:
- Adequate dose (km ≥ ~5) is needed to suppress kr during peak V(t).
- Early timing (≤ 2.5 days) is needed before the cascade locks in.
- Late timing has a dose ceiling: stronger dose cannot rescue.
- Sub-threshold dose has a timing floor: optimal timing cannot
  compensate.

This is a **threshold-like response in both axes**, not a continuous
trade-off. Clinical implication: **myelosan therapy is a narrow window
intervention requiring both adequate dosing AND timely administration**.

## Manuscript phrasing for Discussion

> A focused virtual experiment tested whether dose × timing operate
> as continuous trade-offs or as independent thresholds. Doubling the
> myelosan dose at late intervention (t=4 days, km=10 instead of 4.93)
> produced no measurable improvement in peak severity (28.0
> vs 28.2), indicating a dose ceiling
> once the DIC cascade is established. Conversely, halving the dose at
> optimal timing (t=0, km=2.5) produced markedly worse outcome
> (34.0 vs 7.1),
> exceeding even the severity of late full-dose intervention. The
> protective effect of myelosan thus requires both adequate dose
> (above the kr-suppression threshold) AND timely administration
> (before cascade lock-in), not either alone.

## Caveats

1. **Two-point characterization.** Only two off-baseline combinations
   tested; full dose × timing surface would require larger sweep.
   Deferred as supplementary/future work.

2. **Same inherited caveats as analyses 30-31:** idealized
   instantaneous PK; flat n2 extrapolation after t=8; full ensemble
   includes XIII-channel sloppy basin (good-basin CI also reported in
   summary).

## Run inventory

- `results/combinations_raw.pkl` — all 200 predictions + trajectories
- `results/combinations_summary.json` — aggregated comparison
