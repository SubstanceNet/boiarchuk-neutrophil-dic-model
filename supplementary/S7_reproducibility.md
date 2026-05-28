# S7. Reproducibility and data provenance

*Part of the Supplementary Information. Main-text cross-references: Methods §2.3 (parameter estimation), §2.4 (robustness pipeline), and §2.5 (virtual experiments). The repository-level reproduction guide is `docs/reproduction_protocol.md`; the per-value data provenance is `data/csv/PROVENANCE.md`.*

---

## S7.1 Software environment

The model and analyses are implemented in Python (≥ 3.10) on top of NumPy, SciPy, and Matplotlib, with the pinned versions recorded in `requirements.txt` (NumPy 2.2.6, SciPy ≥ 1.13, Matplotlib 3.10.3). The reference platform was an AMD Ryzen 9 8945HS (8 cores / 16 threads), 32 GB DDR5, running Pop!_OS 22.04 with Python 3.10.12. Exact bit-level reproduction requires matching Python, NumPy, and SciPy versions and the same worker count, because the global optimiser (`scipy.optimize.differential_evolution`) is sensitive to the ordering of parallel evaluations.

## S7.2 Three levels of reproduction

Reproduction is structured at three levels of computational cost, so that a reader can confirm the results at whatever depth they choose.

**Level 1 — verify (seconds).** The test suite (`pytest -m "not slow"`) confirms structural integrity and asserts the published conclusions directly from the tracked result artifacts, without re-running any fit. The scientific-invariant tests (`tests/test_invariants.py`) check the Group I vs Group II hypocoagulation separation (~22×), the factor XIII nadir (≈ −77 %), the day-11 peak, the mechanism-split fractions, the two-phase therapeutic window, the good-basin count (n = 27), and the dose/timing thresholds. The thresholds in those tests are deliberately wide: they fire when a *conclusion* changes, not when a value moves in its last digit.

**Level 2 — reproduce a key result (hours).** Re-running the baseline fit (analysis 05, ~12 min) and the bootstrap ensemble (analysis 22, ~23 h wall-clock for 100 members) regenerates the central artifacts; the aggregate step rewrites `ensemble.json` and `ensemble_members.json`, which should match the stored values within the reported confidence intervals. The dose-response phase diagram (analysis 30, ~2 h) is a cheaper Level-2 target that reuses the existing ensemble.

**Level 3 — reproduce everything (tens of hours).** The full pipeline (baseline → bootstrap → robustness → virtual experiments) takes roughly 1.5–2 days of compute on 16 threads; per-stage times are tabulated in `docs/reproduction_protocol.md`. Because the optimiser is stochastic, exact parameter values vary within the reported confidence intervals across full re-runs, while the qualitative conclusions are stable — which is exactly what the Level-1 invariant tests enforce.

## S7.3 The bootstrap-ensemble artifact

The virtual experiments (analyses 30–33) do not re-fit the model; they propagate the 100-member bootstrap ensemble produced by analysis 22. To make this reproducible from a fresh clone without re-running the ~23 h bootstrap, the ensemble is stored as a consolidated, version-controlled artifact, `analyses/22_predictive_check/results/ensemble_members.json`, holding each member's parameter vector (`best_x`, 26 values) and Group II factor XIII prediction (used for good-basin masking). All downstream analyses load it through `src.ensemble.load_ensemble()`, which reads the consolidated artifact when present and falls back to the per-iteration cache otherwise. The aggregate step of analysis 22 regenerates this artifact deterministically (each bootstrap member is fit from a fixed per-member seed).

## S7.4 Data provenance

Every value in `data/csv/group1.csv` and `group2.csv` is a delta from each animal's own pre-experiment baseline (the paired-difference convention of the original tables) and is mapped to its primary source — the Boiarchuk dissertation tables (1998) — in `data/csv/PROVENANCE.md`. That document records the source table for each observable, the unit and method, the standard-error sources, and the OCR/transcription corrections applied during reconstruction.

Three provenance points bear directly on interpretation. First, the Group II measurements are deltas from the post-suppression "M" state (after the busulfan protocol), not from the intact baseline; the M-state alignment was verified point-for-point during reconstruction, and Group II results must be read relative to M rather than to the Group I baseline. Second, a substantial portion of the Group II dynamics — the full neutrophil-count time course, the bone-marrow granulocytopoiesis, and the busulfan suppression protocol — was reconstructed from the dissertation and is reported here for the first time, not drawn from a peer-reviewed article; any use of this dataset should cite the dissertation as the primary source and include the data files for audit. Third, the Group I mortality is 30 % (12 of 40, days 10–12) per the dissertation and author commentary; the lower figure of 27 % that appears in the 2000 journal article is a less precise published value, and the manuscript uses 30 %.

## S7.5 Data integrity audit

All CSV values are byte-identical to the source arrays archived in `archive/v12/model_v12.py`, and this equivalence is checked automatically by `tests/test_data_integrity.py`. The same archived implementation underpins the model's reproducibility contract, verified by `tests/test_reproducibility.py`.

## S7.6 Versioned history

The repository history is tagged at each development milestone — 18 tags, from `phase0-complete` through `manuscript-skeleton-v2` — so any intermediate state of the model and analyses can be checked out for comparison.
