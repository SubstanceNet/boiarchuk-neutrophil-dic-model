# Analysis 30 — Myelosan dose-response phase diagram (Phase 4.5)

**Status:** closed. 22,500 simulations completed (225 grid cells × 100
bootstrap ensemble members), ~2 minutes wall-clock, zero failures.

## Method

Grid: km ∈ [1.0, 10.0] log-spaced 15 vals × tm ∈ [0.2, 1.0] log-spaced 15 vals.
Per cell: 100 bootstrap ensemble members → 22,500 total simulations.
Per simulation: G2 ODE with kr_g2 = kr × km, tp2_g2 = tp2 × tm
(G2 neutrophil profile retained throughout). 6 severity metrics computed.

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

### 2. G2 neutrophil profile alone insufficient for liver collapse

Liver collapse (Hn/Hm > 0.99) occurs in 0/22,500 simulations,
including the no-kinetic-effect corner (km=1, tm=1).

G2-level neutrophil counts (peak ~60) cannot produce irreversible
liver-state bifurcation regardless of kinetic modification. G1-level
neutrophil counts (peak ~200) are required.

Interpretation: myelosan protective effect operates primarily through
reduction of neutrophil abundance, not kinetic modification alone.

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
> dose-response curve at intermediate severity. Crucially, irreversible
> liver-state collapse (Hn/Hm > 0.99) does not occur at any point in the
> (km, tm) grid when G2 neutrophil counts are retained — suggesting that
> the protective effect of myelosan operates primarily through reduction
> of neutrophil abundance, rather than kinetic modification alone.
> A complementary virtual experiment substituting G1 neutrophil counts
> into the myelosan-modified dynamics would decompose the relative
> contributions of neutrophil count reduction vs. rate constant
> modification — addressable by the current model framework but
> beyond the scope of the present study.

## Implications for analysis 31 (intervention timing)

Current sweep establishes that kinetic modification alone within
G2-context cannot cause liver collapse. Analysis 31 will explore:
- Does delayed myelosan administration reduce its effect?
- Is there a therapeutic window?
- Does delayed administration approach G1-like severity?

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
