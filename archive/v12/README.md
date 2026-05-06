# Archive: v12 (research prototype)

## What is here

- `model_v12.py` — original v12 fit script, byte-identical copy of the file
  delivered in the project root before migration to `src/`. Self-contained:
  loads its own data as numpy literals, runs DE + NM + Powell + NM2 pipeline,
  saves `results_v12.pkl`.

- `v12_report.md` — internal modelling report (v9 -> v12 development trail).
  Originally distributed as `v12_report.docx`, but the file was UTF-8 text
  with an incorrect extension; renamed `.md` here to reflect actual content.
  Author: Oleksiy Onasenko. Companion document to `model_v12.py`.

## Status

v12 is a **research prototype**. Per Olena Boiarchuk: "the main goal of v12
was to establish whether a more sophisticated research model is feasible."
The answer is yes: v12 demonstrated joint-fittability of two experimental
groups under a shared 24-parameter mechanistic core plus 2 myelosan
modifiers, with mechanism-split decomposition of pro-coagulant action.

v12 is **NOT** the manuscript model. The migrated package in `src/` reproduces
v12 byte-for-byte (Phase 0 contract, verified by `tests/test_reproducibility.py`)
to provide a clean foundation for Phase 1 onwards. Substantive model decisions
are revisited in Phase 2:

- relaxation / replacement of the W=2.0 mechanism-split constraint;
- investigation of the G2 R^2 drop from 0.868 (separate fits, v11.2) to 0.598
  (joint fit, v12);
- structural alternatives for the fibrinogen-G2 channel (R^2 = 0.26 in v12);
- reconciliation of the cx parameter (v12 script bound at 600; v12 report
  text quotes a fitted value of 1481, which lies outside the script's bounds —
  see `notes/known_issues.md`).

## Provenance

- File `model_v12.py`: delivered by Oleksiy Onasenko on 2025-05-06,
  reflecting state of v12 development as of that date.
- File `v12_report.md`: produced concurrently with `model_v12.py`, describes
  the same model. Internal document; not intended for publication as-is.

## Do not modify

These files are the historical record of the v12 prototype. Bug-fixes,
refactoring, and improvements happen in `src/`. If a real defect is found
in v12 that affects historical claims, document it in `notes/known_issues.md`
rather than editing the archived files.
