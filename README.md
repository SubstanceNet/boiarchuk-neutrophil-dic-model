# Boiarchuk Neutrophil DIC Model

A mechanistic ODE model of the role of the neutrophil lysosomal apparatus in the
pathogenesis of disseminated intravascular coagulation (DIC), calibrated on the
Boiarchuk experimental dataset (rabbit model, 1998–2023).

**Authors.** Olena D. Boiarchuk (experimental: original data, biological
interpretation). Oleksiy Onasenko (numerical: model implementation, fitting,
robustness analysis).

## Overview

The dataset is an experimental series on rabbit DIC induced by ethylphenacin (a
vitamin-K-antagonist anticoagulant rodenticide), comparing a control DIC group
(Group I) with a group in which granulocytopoiesis was suppressed by busulfan
before induction (Group II). Group II shows that suppressing the
neutrophil compartment largely prevents the clinically significant phase of DIC —
evidence that activated neutrophils are an active contributor to DIC
pathogenesis rather than passive bystanders.

The model is a five-state system of ordinary differential equations with 26
parameters, fit jointly to both groups across six observables (recalcification
time, thrombin time, fibrinogen, factor XIII activity, acid phosphatase, and a
neutrophil degranulation index). Beyond reproducing the experimental record, it
serves as a platform for in-silico experiments: quantifying the neutrophil vs
vessel contribution to each coagulation defect, and predicting the dose-response
and timing dependence of myelosuppressive intervention.

## Repository layout

src/           Model, cost function, fitting pipeline, shared ensemble loader
data/csv/      Experimental data with provenance (PROVENANCE.md)
analyses/      Identifiability, robustness, and virtual-experiment analyses
tests/         Smoke, data-integrity, reproducibility, and invariant tests
docs/          Model specification, parameter glossary, reproduction protocol
manuscript/    Manuscript draft and figure scripts
supplementary/ Supplementary sections S1–S10
archive/       Frozen historical model version (v12)
results/       Top-level generated outputs (git-ignored except .gitkeep)

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
pip install -r requirements.txt   # exact pins — needed to reproduce the numbers
```

Requires Python ≥ 3.10. Runtime dependencies: NumPy, SciPy, Matplotlib. The
editable install (`pip install -e .`) only enforces compatible *version floors*
(see `pyproject.toml`); the second command pins the exact versions (NumPy 2.2.6,
SciPy 1.15.3, Matplotlib 3.10.6) used to produce the published results. Because
`scipy.optimize.differential_evolution` is sensitive to library versions,
installing the pins is required for bit-level reproduction (see
`docs/reproduction_protocol.md`).

## Quick start

Verify the installation and the published scientific conclusions (seconds):

```bash
pytest -m "not slow"
```

Reproduce the baseline fit and the bootstrap ensemble that the virtual
experiments depend on:

```bash
python -m analyses.05_v13_baseline.fit       # baseline joint fit
python -m analyses.22_predictive_check.run   # bootstrap ensemble (slow)
python -m analyses.22_predictive_check.aggregate
```

Run a virtual experiment and regenerate its figure:

```bash
python -m analyses.30_myelosan_dose.run      # dose-response (slow)
python -m analyses.30_myelosan_dose.make_fig4
```

See `docs/reproduction_protocol.md` for the full three-tier reproduction guide
(verify / reproduce-key / reproduce-all), including wall-clock times and
determinism notes.

## Reproducibility

Results are reproducible at three levels, described in
`docs/reproduction_protocol.md`:

- **Verify** (seconds) — `pytest -m "not slow"` checks structural integrity and
  asserts the manuscript's conclusions from the tracked result artifacts,
  without re-running any fit.
- **Reproduce key** (hours) — re-run an individual analysis from a fixed seed
  and compare against the stored ensemble.
- **Reproduce all** (tens of hours) — the full pipeline from scratch. Because
  the global optimizer is stochastic, exact parameter values vary within the
  reported confidence intervals; the scientific conclusions do not.

## Documentation

- `docs/model_spec.md` — state equations, observation equations, cost function.
- `docs/parameter_glossary.md` — all 26 parameters with bounds and meaning.
- `data/csv/PROVENANCE.md` — data sources and provenance.

### A note on `analyses/*/FINDINGS.md`

Each `analyses/NN_*/FINDINGS.md` is a **dated lab notebook**: it records what that analysis computed and how it was interpreted **at the time it was run**, and is retained for process transparency. These notebooks are **not** maintained as current claims. Where later work revised a number or overturned a conclusion, the canonical, up-to-date result lives in the manuscript and the Supplementary Information (S1–S10); where a notebook's conclusion was superseded, a dated note marks it at the top of that file. **In any discrepancy between a `FINDINGS.md` and the manuscript/SI, the manuscript and SI are authoritative.**

## License

- **Code** (`src/`, `tests/`, `analyses/`): Apache License 2.0 — see [`LICENSE`](LICENSE).
- **Data, documentation, manuscript** (`data/`, `docs/`, `manuscript/`, `supplementary/`, README files): Creative Commons Attribution 4.0 International (CC-BY-4.0) — see [`LICENSE-DOCS`](LICENSE-DOCS).

When citing this work, please cite the eventual publication and the underlying
dataset (Boiarchuk O. D., 1998–2023; provenance in `data/csv/PROVENANCE.md`).
