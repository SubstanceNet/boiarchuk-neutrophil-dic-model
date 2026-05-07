# Analysis 01 — W_split profile

## Question

Does the mechanism-split constraint (`cfg.W_SPLIT`, default 2.0) drive the
parameter values and the v12 mechanistic conclusions, or is it a benign
optimisation aid?

This addresses issue **I-3** in `notes/known_issues.md` (circular evidence).

## Method

Run quick-mode joint fits at `W_split` ∈ {0.0, 0.3, 1.0, 2.0, 5.0}, single
seed (42), all other parameters identical to v12 baseline. Record best fit,
per-observable R², 26 parameter values, and the **realised** neutrophil-share
fractions on G1 day 2.

## Run

```bash
python -m analyses.01_w_split_profile.sweep
```

Wall-clock: ~65 minutes on 16-thread workstation. Subsequent runs use the
cache and are near-instant unless cache is cleared.

## Outputs

- `results/sweep.json` — all metrics, parameters, fractions per W_split
- `results/_cache/*.pkl` — individual fit results
- (figures will be added after sweep completes)

## Decision rule

| Observation                                  | Interpretation                                                                                          |
|----------------------------------------------|---------------------------------------------------------------------------------------------------------|
| All parameters stable; R² stable             | Constraint is benign optimisation hint. Mechanism-split is data-supported. Publication-safe.            |
| Parameters drift; R² stable                  | Constraint defines the decomposition. Cannot use mechanism-split as evidence; must justify externally.  |
| R² collapses at W=0                           | Data alone cannot determine the decomposition. Constraint is essential prior — needs literature backing.|
