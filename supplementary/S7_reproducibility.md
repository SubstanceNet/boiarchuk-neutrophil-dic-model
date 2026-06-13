# S7. Reproducibility and Data Provenance

*Part of the Supplementary Information for Boiarchuk & Onasenko (2026). Cross-references from the main text: Methods, Parameter estimation; Methods, Robustness analysis (robustness pipeline); and Methods, Virtual experiments. This appendix documents the provenance of every data value and the full repository-level reproduction protocol (`docs/reproduction_protocol.md`, `data/csv/PROVENANCE.md`).*

---

## S7.1 Software environment

The model and analyses are implemented in Python ($\geq 3.10$) on top of NumPy, SciPy, and Matplotlib, with exact pinned versions recorded in `requirements.txt` (NumPy 2.2.6, SciPy 1.15.3, Matplotlib 3.10.6; `pyproject.toml` records compatible version floors for installation). The reference platform was an AMD Ryzen 9 8945HS (8 cores / 16 threads), 32 GB DDR5, running Pop!\_OS 22.04 with Python 3.10.12. Exact bit-reproducible results require matching Python, NumPy, and SciPy versions and the same number of worker processes, because the global optimiser (`scipy.optimize.differential_evolution`) is sensitive to the order of parallel computations.

---

## S7.2 Three levels of reproduction

Reproduction is structured at three levels of computational cost, so that a reader can verify results to whatever depth they choose.

**Level 1 — verify (seconds).** The test suite (`pytest -m "not slow"`) confirms structural integrity and asserts the documented findings directly from tracked result artefacts, without re-running any fit. The scientific-invariant tests (`tests/test_invariants.py`) check Group I / Group II hypocoagulation separation (~21×), factor XIII nadir (~−77%), peak on day 11, mechanism decomposition fractions, biphasic therapeutic window, good-basin count ($n = 27$), and dose/time thresholds. Tolerances in these tests are deliberately wide: they trigger when a *conclusion* changes, not when a value shifts in the last digit.

**Level 2 — reproduce the key result (hours).** Re-running the baseline fit (analysis 05, ~12 min) and the bootstrap ensemble (analysis 22, ~23 h wall-clock for 100 members) regenerates the central artefacts; the aggregation step overwrites `ensemble.json` and `ensemble_members.json`, which should match the stored values within the reported confidence intervals. The dose–response phase diagram (analysis 30, ~2 min) is a cheaper Level 2 target that re-uses the existing ensemble.

**Level 3 — reproduce everything (tens of hours).** The full pipeline (baseline fit → bootstrap → robustness → virtual experiments) takes approximately 1.5–2 days of computation on 16 threads; per-step wall-clock times are tabulated in `docs/reproduction_protocol.md`. Because the optimiser is stochastic, exact parameter values vary within the reported confidence intervals across full re-runs, while qualitative conclusions are stable — which is precisely what the Level 1 invariant tests ensure.

---

## S7.3 Bootstrap ensemble artefact

The virtual experiments (analyses 30–33) do not re-fit the model; they propagate the 100-member bootstrap ensemble produced by analysis 22. To make this reproducible from a fresh clone without re-running the ~23-hour bootstrap, the ensemble is stored as a consolidated, version-controlled artefact `analyses/22_predictive_check/results/ensemble_members.json`, containing each member's parameter vector (`best_x`, 26 values) and the Group II factor XIII prediction (used for good-basin masking). All downstream analyses load it via `src.ensemble.load_ensemble()`, which reads the consolidated artefact if present and falls back to the per-iteration cache otherwise. The analysis 22 aggregation step regenerates this artefact deterministically (each bootstrap member is fitted from a per-member fixed seed).

---

## S7.4 Data provenance

Every value in `data/csv/group1.csv` and `group2.csv` is a delta from each animal's pre-experiment baseline (the paired-difference convention of the original tables) and is mapped to its primary source — the tables of the Boiarchuk (1998) dissertation — in `data/csv/PROVENANCE.md`. That document records the source table for each observable, the unit and method, sources of standard errors, and OCR/transcription corrections applied during reconstruction.

Three provenance points directly bear on interpretation. First, Group II measurements are deltas from the post-suppression state "M" (after the busulfan protocol), not from the intact baseline; the M-alignment was verified point-by-point during reconstruction, and Group II results should be read relative to M, not relative to the Group I baseline. Second, a substantial portion of the Group II dynamics — the full time course of neutrophil count, bone-marrow granulopoiesis, and the busulfan suppression protocol — was reconstructed from the dissertation and is presented here for the first time, not taken from a peer-reviewed article; any use of this dataset should cite the dissertation as the primary source and include the data files for audit. Third, Group I lethality is 30% (12 of 40, days 10–12) per the dissertation and author commentary; the lower figure of 27% that appears in one of the Boiarchuk series publications is a less precise published value, and the manuscript uses 30%.

---

## S7.5 Data integrity audit

All CSV values are byte-identical to the source arrays archived in `archive/v12/model_v12.py`, and this equivalence is verified automatically by `tests/test_data_integrity.py`. The same archived implementation underpins the model reproducibility contract verified by `tests/test_reproducibility.py`.

---

## S7.6 Versioned history

The repository history is tagged at every development milestone, allowing any intermediate state of the model and analyses to be checked out for comparison. The public release accompanying this manuscript is hosted at `https://github.com/SubstanceNet/boiarchuk-neutrophil-dic-model` (release tag `v1.0.0`) and archived at Zenodo under DOI `10.5281/zenodo.20673521`, which is the canonical citable reference for the code and the reconstructed dataset.
