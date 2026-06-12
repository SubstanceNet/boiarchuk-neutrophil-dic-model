# Analysis 30 — Myelosan dose-response phase diagram (Phase 4.5)

> **⚠ SUPERSEDED (v3.16) — two corrections.** (1) The severity separation quoted here as *"22×"* / *"~22-fold"* was unified to **21×** in later work (endpoint/rounding convention; main text §3.4). (2) The interpretation that *"myelosan operates substantially through reduction of neutrophil abundance"* (i.e. predominantly via neutrophil count) was **not supported** by the later 2×2 decomposition. With good-basin cells max_recalc = 150.8 / 39.6 / 44.5 / 7.1 s for (G1/off, G1/on, G2/off, G2/on), the protective effect splits into **comparable count and kinetic main effects with a positive interaction** (total ≈ 21×); **neither axis dominates.** **Canonical treatment: §S6.5** and main text §3.4–3.5. The "neutrophil abundance" framing below is superseded.

**Status:** closed. 22,500 simulations completed (225 grid cells × 100
bootstrap ensemble members), ~2 minutes wall-clock, zero failures.

## Method

Grid: km ∈ [1.0, 10.0] log-spaced 15 vals × tm ∈ [0.2, 1.0] log-spaced 15 vals.
Per cell: 100 bootstrap ensemble members → 22,500 total simulations.
Per simulation: G2 ODE with kr_g2 = kr × km, tp2_g2 = tp2 × tm
(G2 neutrophil profile retained throughout). 6 severity metrics computed
(time-to-peak gHn computed but not interpreted here; deferred to analysis 31).

## Reference points

- **(km=1.00, tm=1.00):** no kinetic effect of myelosan
- **(km=5.18, tm=0.45):** G2 baseline (observed dose)

## Internal validation

Model prediction at G2 baseline cell vs G2 observed values:

| metric | observed | model median | model CI95 | within CI? |
|--------|----------|--------------|------------|------------|
| max_recalc | 9.10 | 5.84 | [0.29, 13.04] | YES |
| min_xiii | -9.30 | -11.80 | [-22.47, 0.00] | YES |
| auc_recalc | 70.55 | 82.78 | [66.91, 102.59] | YES |

All G2 observed values within model CI95 at baseline cell.

## Headline findings

### 1. Myelosan kinetic effect reduces DIC severity 2.5x to 7x

Comparison km=1, tm=1 (no kinetic effect) vs km=4.93, tm=0.43 (observed):

| metric | km=1, tm=1 | G2 baseline | reduction |
|--------|------------|-------------|-----------|
| max_recalc | 41.57 | 5.84 | 7.1x |
| auc_recalc | 206.20 | 82.78 | 2.5x |
| min_xiii | -52.53 | -11.80 | 4.5x |

The myelosan-induced kinetic modification (km × tm in observed dose)
reduces peak hypocoagulation by ~7x, integrated coagulation disruption
by ~2.5x, and XIII depletion by ~4.5x.

### 2. [RETRACTED] liver_collapse metric was invalid — see analysis 33

**This section originally reported "liver collapse (Hn/Hm > 0.99) occurs in
0/22,500 simulations" and inferred that G2 neutrophil counts cannot produce
fatal DIC. That claim is withdrawn.** The metric is invalid on two
independent grounds, both verified directly (analysis 33):

1. **Code bug.** `compute_severity` read `o["Hm"]`, but `solve_group` never
   placed `"Hm"` in its output dict. `Hm` was therefore `None`, the collapse
   branch never executed, and `liver_collapse` was `False` for all 22,500
   simulations unconditionally — `0` by construction, not a result.
2. **Conceptually empty even if fixed.** Hn reaches only ~1.15% of carrying
   capacity Hm in the realistic parameter range; the 0.99 threshold is
   structurally unreachable. Hn/Hm saturation cannot detect anything.

The metric has been removed from `run.py`. Mortality is re-validated in
**analysis 33** through hypocoagulation severity (the clinically observed
endpoint): pure-G1 simulation yields max_recalc ~147 s (vs G2 ~7 s), a 22x
group separation reproducing the observed 30% G1 / 0% G2 mortality contrast,
with peak timing (day 11) and XIII/fib nadirs matching observation within
1-11%. The other analysis-30 severity metrics (max_recalc, min_xiii,
auc_recalc, max_gHn) are unaffected and remain valid.

### 3. Dose-response monotonic and smooth

Increasing km → decreasing severity (consistent: myelosan amplifies
suppression of kr).
Decreasing tm → decreasing severity (extended plateau timing shortens
DIC progression window).

No bimodal or paradoxical behavior, in contrast to multi-modal cost
landscape observed during fitting.

## Manuscript phrasing for Results

> Virtual experiments using the 100-member bootstrap ensemble reveal that
> myelosan-induced kinetic modification of neutrophil-derived rate constants
> reduces peak hypocoagulation by 7-fold and integrated coagulation
> disruption by 2.5-fold, relative to the same neutrophil profile without
> kinetic modification (Figure X, phase diagram in (km, tm) space).
> The observed experimental dose (km=4.93, tm=0.43) lies on the
> dose-response curve at intermediate severity. The kinetic modification
> alone, applied to the G2 neutrophil profile, does not reproduce G1-level
> **[SUPERSEDED — count and kinetics contribute comparably (2×2 decomposition); neither dominates. See top note + §S6.5.]**
> hypocoagulation severity; pure-G1 simulation (analysis 33) yields ~22-fold
> greater peak hypocoagulation, indicating that the protective effect of
> myelosan operates substantially through reduction of neutrophil abundance,
> not kinetic modification alone. (An earlier version of this analysis stated
> this via an "irreversible liver-state collapse" metric; that metric was
> found to be invalid and has been removed — see analysis 33.)

## Implications for analysis 31 (intervention timing)

Current sweep establishes that kinetic modification alone within the
G2-context does not reach G1-level hypocoagulation severity (analysis 33).
Analysis 31 will explore:
- Does delayed myelosan administration reduce its effect?
- Is there a therapeutic window?
- Does delayed administration approach G1-like severity?

## Note on time-to-peak metric deferral

A `time_to_peak_gHn` metric was computed during the sweep (one of the
6 severity metrics) but is **not interpreted in this analysis**, for two
reasons:

1. **Semantic alignment.** Time-to-peak biology addresses *when* the
   critical DIC event occurs, which is the central question of analysis
   31 (intervention timing), not the dose magnitude question of analysis
   30 (this analysis).

2. **Edge artifact from neutrophil interpolator extrapolation.** At
   km=1 (no myelosan effect), G2 trajectories exhibit a slow secondary
   rise in gHn between t=7 and t=8, exceeding the first peak by a small
   margin. This is attributed to constant extrapolation of the
   neutrophil interpolator beyond the last G2 data point (t=8 → N=3.73
   held constant). The `argmax` operation thus selects the last
   timepoint in these scenarios, producing a misleading "time-to-peak"
   value of 8 days. Properly addressing this requires a time-dependent
   N(t) model on the full 0-19 day interval, which is implemented in
   analysis 31.

The raw `phase_diagram_time_to_peak_gHn.json` is retained for
reference but is not promoted to a figure in this analysis.

## Caveat on initial sanity-check formulation

Original sanity check at km=1, tm=1 was intended to validate G1-like
severity. This was conceptually misformulated: km=1 within G2 simulation
retains G2 neutrophil profile, not G1's. Valid validation is G2-context
match (above), not G1-equivalence. The sanity_check_km1.json file
records observed values; interpretation is corrected here.

## Run inventory

- results/ensemble_predictions_raw.pkl — all 22,500 predictions
- results/phase_diagram_*.json — 6 phase diagrams (one per metric)
- results/sanity_check_km1.json — internal validation record
- results/run.log — main run log
