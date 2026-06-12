# Archive: v12 (research prototype)

## What is here

- `model_v12.py` — the original v12 fit script, a byte-identical copy of the
  file delivered in the project root before migration to `src/`. Self-contained:
  loads its own data as numpy literals, runs the DE + NM + Powell + NM2 pipeline,
  saves `results_v12.pkl`. **This file is the reproducibility reference** against
  which `src/` is checked (see "Reproducibility role" below).

- `v12_report.md` — the internal v9->v12 model-development report (in Ukrainian,
  the language of the original work). A historical document; its numbers reflect
  the v12 era and were later revised (see the banner at the top of that file and
  the manuscript / Supplementary Information for current values).

## Status

v12 was the **research prototype** that established the feasibility of jointly
fitting both experimental groups under a shared mechanistic core plus two
myelosan modifiers. It is **not** the manuscript model. The production model,
its current parameter estimates, and all published numbers are in `src/`, the
manuscript, and the Supplementary Information (S1-S10).

## Reproducibility role

The migrated package in `src/` reproduces the v12 cost function and data
byte-for-byte. This equivalence is the "Phase 0 contract", verified
automatically by the test suite:

- `tests/test_reproducibility.py` — `src.fit.joint_cost` is numerically
  identical to `model_v12.py._cost_core` for the same parameter vector.
- `tests/test_data_integrity.py` — the CSV data files are byte-identical to the
  numpy literals embedded in `model_v12.py`.

This is why `model_v12.py` must remain unchanged: it is the fixed reference that
guarantees the refactored production code did not alter the underlying model.

## Provenance

- `model_v12.py`: delivered 2025-05-06, reflecting the state of v12 development
  at that date.
- `v12_report.md`: produced concurrently, describing the same model. Internal
  document, retained for provenance; not intended for publication as-is.

## Do not modify

These files are the historical record of the v12 prototype and the fixed
reproducibility reference. Bug-fixes, refactoring, and improvements happen in
`src/`. If a real defect in v12 is found that affects historical claims,
document it in `notes/known_issues.md` rather than editing the archived files.
