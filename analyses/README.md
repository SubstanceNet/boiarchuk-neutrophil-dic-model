# Analyses

Each subdirectory is a self-contained analysis: a runnable script (or scripts),
a `README.md` stating the question and method, and a `results/` directory with
saved outputs (JSON summaries are tracked; large `.pkl` caches under
`results/_cache/` are git-ignored and regenerated on demand). Shared figure
styling lives in `_fig_style.py`. Ad-hoc probes live under `_diagnostic/`
(git-ignored) and are not part of the formal record.

## Dependency order

Most analyses are independent, but the Phase-4.5 virtual experiments depend on
the bootstrap ensemble produced by analysis 22:

 05_v13_baseline      → establishes the baseline fit (results/fit.json)
 │
 22_predictive_check  → bootstrap ensemble (100 members)
 │                writes ensemble.json + ensemble_members.json
 ├── 30_myelosan_dose
 ├── 31_intervention_timing
 ├── 32_combinations
 └── 33_g1_severity_validation

Downstream analyses load the ensemble through `src.ensemble.load_ensemble()`,
which reads the consolidated `ensemble_members.json` (so a fresh clone needs no
re-run) and falls back to the `_cache/` pkls if that artifact is absent.

## Identifiability and model structure

| # | Analysis | Question | Entry point |
|---|----------|----------|-------------|
| 01 | W_split profile | Cost and mechanism-split fractions as a function of the prior weight W_split | `sweep.py` |
| 02 | cx bound | Why the factor XIII production bound cx ≤ 600 is required | `sweep.py` |
| 03 | Separate G2 fit | Group-II-only fit, to quantify the joint-architecture penalty | `fit.py` |
| 04 | Survivor weighting | Whether the ad-hoc late-G1 down-weighting is influential (it is not) | `fit.py` |
| 05 | v13 baseline | The reference joint fit; source of the baseline parameter vector | `fit.py` |
| 06 | cx diagnostic | Where the cx bound should sit (five bound levels × three seeds) | `sweep.py` |
| 07 | Group-specific cx | Tests a group-specific cx; rejected (sloppy direction) | `fit.py` |
| 08 | Group-specific cf | Tests a group-specific cf; rejected (sloppy direction) | `fit.py` |
| 09 | Profile likelihood | Per-parameter identifiability over all 26 parameters | `full_sweep.py` |

## Robustness

| # | Analysis | Question | Entry point |
|---|----------|----------|-------------|
| 20 | LOO timepoint | Leave-one-timepoint-out cross-validation (23 points) | `run.py` |
| 21 | Perturbation | Sensitivity to the neutrophil-count input N(t): deterministic α-scan and stochastic noise | `run_alpha_scan.py`, `run_stochastic.py` |
| 22 | Predictive check | Parametric bootstrap (N=100); produces the ensemble used downstream | `run.py` → `aggregate.py` |

## Virtual experiments

| # | Analysis | Question | Entry point |
|---|----------|----------|-------------|
| 30 | Busulfan dose-response | DIC severity over the (km, tm) dose grid — 15×15×100 simulations | `run.py` → `make_fig4.py`, `make_fig5.py` |
| 31 | Intervention timing | DIC severity vs busulfan intervention time — the therapeutic window | `run.py` → `make_fig6.py` |
| 32 | Combinations | Dose × timing: are they independent thresholds? | `run.py` |
| 33 | G1 severity validation | Pure-G1 dynamics vs the observed mortality pattern | `run.py` |
| 34 | Per-group-std bootstrap | Sensitivity of the XIII channel to the normalization choice | `run.py` → `aggregate.py` |

## Running an analysis

Analyses are run as modules from the repository root, e.g.:

```bash
python -m analyses.05_v13_baseline.fit
python -m analyses.22_predictive_check.run
python -m analyses.22_predictive_check.aggregate
python -m analyses.30_myelosan_dose.run
```

Figure scripts (`make_figN.py`) are run the same way and read the saved results
of their analysis. Wall-clock times vary from seconds (33) to hours (22, 30);
see each analysis README and `docs/reproduction_protocol.md`.
