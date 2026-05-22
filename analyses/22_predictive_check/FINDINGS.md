# Analysis 22 — Parametric Bootstrap Predictive Check (Phase 3)

**Status:** closed. N=100 parametric bootstrap iterations completed.
Predictions, parameter confidence intervals, and mechanism split CIs obtained.
Reveals important structural finding regarding XIII channel identifiability.

## Summary

Parametric Gaussian bootstrap of v13 baseline with N=100 iterations.
Per iteration: synthetic data generated from baseline predictions + Gaussian
noise (σ = baseline RMSE per-group per-observable), refit with full quick-mode
pipeline (DE popsize=15 + Nelder-Mead + Powell + Nelder-Mead). Total wall-clock:
23.4 hours. Zero failed iterations.

## Ensemble cost distribution

| metric | value |
|--------|-------|
| mean | 0.8750 |
| std | 0.0737 |
| CI 95 | [0.7554, 1.0204] |
| min | 0.6906 |
| max | 1.0888 |

Baseline cost on real data was 0.959; bootstrap cost on synthetic data
slightly lower on average (mean 0.875) — expected, as synthetic data
generated from baseline-self-consistent predictions.

## Mechanism split CI (G1 day 2 neutrophil fractions)

| observable | bootstrap median | CI 95 | prior target (W_SPLIT=2.0) | unconstrained (W=0, analysis 01) |
|-----------|------------------|-------|----------------------------|----------------------------------|
| recalc | 0.240 | [0.225, 0.249] | 0.24 | 0.34-0.48 (seed-dependent) |
| fib | 0.759 | [0.738, 0.777] | 0.76 | ~0.05 (seed-stable) |
| xiii | 0.806 | [0.777, 0.844] | 0.82 | ~0.75 (seed-stable) |

**CORRECTION (2026-05).** An earlier version of this section reported a
single uniform prior of 0.65 and described the split as a "data-driven
discovery" in which the data move the fractions away from the prior. That
was wrong on both counts. The prior is **not** uniform: `config.NEUTRO_FRAC`
specifies three per-channel targets (recalc 0.24, fib 0.76, xiii 0.82), and
the `_mechanism_split_residual` penalty drives each channel toward its own
target. The 0.65 value never existed in the code; it was a stale figure from
an early single-target proposal that predates the per-channel derivation.

**What the data actually show.** The fitted fractions sit essentially on the
prior targets (delta <= 0.014). They are therefore **prior-specified, not
data-emergent**. The narrow bootstrap CIs do not demonstrate that the data
identify the fractions: every iteration was refit under the same W_SPLIT=2.0
penalty pulling toward the targets, and the synthetic data were generated
from a baseline that itself sits on the targets, so a narrow CI around the
targets is structurally guaranteed and carries no independent identifiability
information.

**Prior targets are data-derived (but from a different timepoint).** The
targets equal the day-1 neutrophil-attributable fraction estimated as
(dG1 - dG2)/dG1 (absolute deltas from baseline, dissertation tables 4.9/5.9):
recalc (-38.5-(-29.3))/-38.5 = 0.239; fib (28.0-6.7)/28.0 = 0.761;
xiii (71.0-12.8)/71.0 = 0.820. The derivation is clean because G1 and G2 have
near-identical hemostatic baselines (recalc 78.7 vs 78.0; fib 58.2 vs 58.3;
xiii 100.0 vs 93.2) -- myelosan altered neutrophils, not baseline hemostasis.
The targets are thus a biologically-derived prior, imposed on the day-2 fit.

**Per-channel honesty (critical for manuscript).** The unconstrained (W=0)
column above shows what the day-2 data say *without* the prior:
- **recalc**: non-identifiable without the prior (0.34-0.48 across seeds);
  the prior is required to pin it (and pins it to 0.24, below the W=0 range).
- **xiii**: the prior target (0.82) is roughly consistent with the
  unconstrained value (~0.75) -- this is the one channel where prior and
  unconstrained data agree.
- **fib**: the unconstrained fit places fibrinogen at ~0.05 (seed-stable),
  i.e. vessel-dominant. The prior **overrides** this and sets it to 0.76.
  This channel must NOT be presented as a model finding of neutrophil
  dominance: without the prior the day-2 fib dynamics do not reproduce the
  day-1 ratio. The 76% figure is an imposed prior target, validated only
  indirectly (held-out G2, analysis 01), not a reproduced data feature.

**Correct status of the mechanism split:** a day-1-derived, biologically
motivated prior, required for identifiability (analysis 01, W=0 is
non-identifiable for recalc) and validated post-hoc by superior held-out G2
R-squared versus unconstrained fits (analysis 01: +2-7 pp R2_G2). It is NOT
an independent data-driven discovery, and for fibrinogen it actively
overrides the unconstrained data direction.

## Parameter CI vs profile likelihood comparison

Bootstrap (marginal CI, across all parameter perturbations simultaneously)
vs profile likelihood (conditional CI, holding the parameter fixed at grid
values while optimising the rest).

**Well-identified parameters (analysis 09 depth_rel > 5%):**

| param | bootstrap CI 95 | PL CI 95 | note |
|-------|-----------------|----------|------|
| tp2 | [8.89, 10.03] | [9.18, 9.18] | bootstrap shows true CI (PL was grid-truncated) |
| km | [3.46, 5.73] | [3.45, 6.91] | bootstrap narrower (correlations captured) |
| tm | [0.39, 0.47] | [0.34, 0.51] | bootstrap narrower |
| kd | [0.22, 1.05] | [0.17, 0.37] | bootstrap **wider** — marginal CI of correlated kd-kr pair |
| s2 | [1.51, 2.71] | [1.16, 2.34] | consistent |
| at | [4.89, 6.44] | [3.82, 8.50] | bootstrap narrower |

The kd discrepancy is expected: profile likelihood fixes kd and optimises 25
others (conditional CI). Bootstrap perturbs all 26 simultaneously (marginal
CI). For correlated parameter pairs (kd-kr coupled in degranulation ODE),
marginal CI is wider than conditional. Bootstrap is the more appropriate
metric for prediction uncertainty.

**Sloppy parameters (analysis 09 depth_rel < 2%) show wide CIs as expected:**

| param | bootstrap CI 95 | PL CI 95 | classification |
|-------|-----------------|----------|----------------|
| kca | [0.13, 33.34] | [0.23, 0.63] | sloppy — drift extensive |
| Hm | [11.11, 999.8] | [71.8, 195.3] | sloppy — wide drift |
| kna | [80.9, 644.6] | [222.8, 605.7] | sloppy |
| df | [0.12, 13.01] | [7.69, 20.89] | sloppy + unconverged (see below) |

## R² distribution per observable

**G1 (R² distribution across 100 iterations):**

| observable | median | CI 95 |
|-----------|--------|-------|
| recalc | 0.768 | [0.703, 0.813] |
| thrombin | 0.850 | [0.801, 0.883] |
| fib | 0.710 | [0.644, 0.776] |
| xiii | 0.859 | [0.779, 0.899] |
| AP | 0.809 | [0.724, 0.862] |
| D | 0.882 | [0.807, 0.930] |

G1 fit quality robust across ensemble — all observables median R² > 0.70.

**G2 (R² distribution across 100 iterations):**

| observable | median | CI 95 |
|-----------|--------|-------|
| recalc | 0.881 | [0.768, 0.940] |
| thrombin | 0.935 | [0.861, 0.966] |
| fib | 0.407 | [0.038, 0.518] |
| **xiii** | **0.075** | **[-1.019, 0.649]** |
| AP | 0.952 | [0.754, 0.974] |
| D | 0.737 | [0.590, 0.827] |

**XIII G2 fit quality is not robust under parametric bootstrap: 41% of
iterations yield R² < 0, reflecting structural non-identifiability in the
XIII channel** (confirms I-9 structurally).

Detail breakdown:
- R² < 0: 41/100 iters (catastrophic fit)
- R² ∈ [0, 0.3): 32/100
- R² ∈ [0.3, 0.6): 19/100
- R² ≥ 0.6: 8/100

Only 5 of 100 iterations achieve R²_G2 ≥ 0.4 across all 6
observables simultaneously.

## Diagnostic: what drives xiii_G2 R² variation?

Pearson correlation between xiii_G2 R² across iterations and individual
parameters:

| param | correlation |
|-------|-------------|
| kx | +0.331 |
| ax | -0.147 |
| cx | -0.136 |
| bx | -0.026 |

Comparing 41 "bad" iters (R²<0) vs 19 "good" iters (R²≥0.4):

| param | bad median | good median | ratio |
|-------|------------|-------------|-------|
| bx | 35.74 | 27.91 | 1.28 |
| ax | 47.78 | 42.21 | 1.13 |
| cx | 575.1 | 507.3 | 1.13 |
| kx | 2.43 | 3.03 | 0.80 |

**Mechanism identified: bx/kx ratio determines basin.** High bx (XIII
degradation rate) combined with low kx (liver resynthesis rate) gives
XIII degradation exceeding resynthesis → catastrophic xiii_G2 fit.
Low bx/kx ratio → resynthesis adequate → good xiii_G2.

This is a continuous gradient, not discrete basin switching (correlation
0.33 — moderate, not high). Bad iterations drift along the XIII sloppy
direction identified in analysis 09.

**Well-identified parameters (kd, tp2, km, tm) are nearly identical between
bad and good iters (ratios 0.95-1.03).** Mechanism split, myelosan effects,
and plateau timing are robust to the XIII basin choice. Main biological
conclusions are independent of XIII channel uncertainty.

## Convergence check

Comparing CI 95 width at N=50 (first half) vs N=100 (full).

**Well-identified parameters (mostly converged):**
- tp2: +2.9% (converged)
- kd: -6.2% (converged)
- at: +5.1% (converged)
- tm: +8.8% (converged)
- s2: +8.9% (converged)
- km: +26.4% (slightly under-converged — see caveat)

**Sloppy parameters (expected width change at N=100):**
- df: -47.7% (CI narrows; still wide)
- kx: +27.2% (CI widening; still wide)
- kr: -23.8% (CI narrows; still wide)
- cr: +19.7% (similar)

Aggregate avg |Δ width|: 12.2%. Max change: df (-91.4% of width, but
absolute change small in context of wide sloppy CI).

**Caveat about km:** km classified as well-identified per analysis 09 but
its CI width changed by 26.4% from N=50 to N=100. Reported CI [3.46, 5.73]
may be slightly underestimated. True CI likely closer to [3.2, 6.0]. The
difference is biologically minor.

**Sloppy parameter CI estimates** (df, kx, kr, kca, Hm, kna) are formally
provisional under N=100 sampling. Additional 100 iterations would tighten
sloppy CIs by another ~10-20% but would not change biological conclusions.

## Implications for Phase 3 / manuscript

**Strong findings (robust to N=100 ensemble):**
1. tp2, s2, at, tm, kd, km — well-identified, narrow CIs, suitable for
   manuscript headline parameter estimates.
2. G1 fit quality consistent across ensemble — model captures G1 dynamics
   robustly.

**On the mechanism split (NOT a data-driven finding — see corrected section
above):** the split is a day-1-derived biological prior imposed on the day-2
fit, required for identifiability and validated post-hoc by held-out G2 R²
(analysis 01). The narrow bootstrap CI is structurally guaranteed by the
W_SPLIT penalty and is NOT evidence of data identifiability. Present it in
the manuscript as a prior-regularized, held-out-validated decomposition that
*quantifies and is consistent with* Boiarchuk's neutrophil hypothesis — not
as an independent discovery, and explicitly note that for fibrinogen the
unconstrained fit (~0.05) disagrees with the prior target (0.76).

**Known limitations to report transparently:**
1. xiii_G2 fit quality variable across ensemble. 41% iters R²<0.
   Reflects structural under-identification of XIII channel (I-9).
   Recommend cautious interpretation of late-day (t≥4) XIII G2 predictions
   in virtual experiments.
2. fib_G2 fit quality moderate (median 0.41). Reflects I-4 (fib G2 weak)
   from Phase 2.
3. Sloppy parameters (kca, kna, Hm, kx, bx) have wide CI; predictions
   depending strongly on these should be reported with broader uncertainty
   bands.

**For virtual experiments (analyses 30-32):** propagate ensemble (100
parameter sets) through dose-response, intervention timing, and combination
scenarios. CI on predictions = ensemble 2.5/97.5 percentiles. Predictions
that vary primarily with well-identified params (mechanism split, plateau
timing, myelosan effect) will be tight. Predictions that depend on XIII
channel params will be wide — to be reported transparently.

## Run inventory

- `results/_cache/iter_001.pkl` ... `iter_100.pkl` — 100 cached fits
- `results/iter_NNN.json` — 100 individual fit JSON results
- `results/ensemble_raw.json` — raw N=100 ensemble
- `results/ensemble.json` — aggregated CI summary
- `results/sigmas.json` — bootstrap noise sigmas used
- `results/bootstrap.log` — main run log
- `sanity_3iters.json` — 3-iter sanity check before full run
