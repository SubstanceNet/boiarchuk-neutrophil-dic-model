# Boiarchuk Neutrophil DIC Model

Mechanistic ODE model of the role of neutrophilic lysosomal apparatus in the pathogenesis of disseminated intravascular coagulation (DIC) syndrome, calibrated on Boiarchuk O. D. experimental data (1998–2023).

**Authors.** Olena D. Boiarchuk (experimental; original data, biological interpretation). Oleksiy Onasenko (numerical simulation; model implementation, fitting, robustness analysis).

**Status.** Phase 0 — clean migration of v12 research prototype. Mathematics is byte-identical to `archive/v12/model_v12.py`; structure is publication-ready.

## What this project is

The dataset is a 25-year experimental series on rabbit DIC induced by Эфа-2 venom, with a control group (n=40) and a granulocytopoiesis-suppressed group (myelosan pre-treatment, n=40). Group II demonstrates that suppressing the neutrophil compartment prevents the clinically significant phase of DIC — a key piece of evidence for the central hypothesis that activated neutrophils are an active causal factor in DIC pathogenesis (rather than passive bystanders).

The wet lab in Luhansk has been lost as a result of the war. New experiments cannot be run. The mathematical model is therefore both (a) a tool for quantitative validation of the existing experimental record and (b) a platform for in-silico continuation experiments where physical follow-up is no longer possible.

## Repository layout

```
src/         Model code (current: v12 migration; future: v13 final)
data/csv/    Experimental data with full provenance metadata
analyses/    Robustness analyses (sensitivity, identifiability, bootstrap, MCMC)
tests/       Smoke + reproducibility tests
results/     Generated outputs (pickles, figures) — git-ignored
docs/        Model specification, parameter glossary, reproduction protocol
manuscript/  Paper draft and publication-quality figures
archive/     Frozen historical model versions (currently: v12)
notes/       Internal working notes (not for publication)
```

## Quick start

Tested on the reference workstation (HP Omen 17, AMD Ryzen 9 8945HS / 16 threads, 32 GB DDR5, Pop!_OS 22.04, Python 3.10.12).

```bash
# Activate existing venv
source ~/python_projects/my_env/bin/activate

# Move project to project SSD and install
cp -r boiarchuk_neutrophil_dic_model_final /media/ssd2/ai_projects/research/
cd /media/ssd2/ai_projects/research/boiarchuk_neutrophil_dic_model_final

# Install in editable mode
pip install -e .

# Verify Phase 0 contract: numerical equivalence with v12
pytest -m "not slow"           # ~10 s, must be all green

# Optional: verify full pipeline works (slow ~1 min)
pytest -m slow

# Quick joint fit (smoke-level, ~1-2 min on 16 threads)
python -m src.cli --quick

# Full fit (5 seeds, ~10-30 min on 16 threads)
python -m src.cli
```

## Reproducibility contract (Phase 0)

For any parameter vector `pv`, the migrated cost function in `src.fit.joint_cost` returns a value numerically identical (to ~1e-12) to the archived v12 cost function in `archive/v12/model_v12.py:_cost_core`. This is enforced by `tests/test_reproducibility.py`. Phase 0 is closed when this test is green.

Any change to the model that breaks this test is, by definition, a Phase 2 change and belongs to a labelled successor model (v13, v13.1, …) — not Phase 0.

## Roadmap

| Phase | Goal | Deliverable |
|-------|------|-------------|
| 0 ✓ | Migrate v12 to publication structure with full reproducibility | `src/` package; data CSV with provenance; smoke + reproducibility tests; archive/v12/ |
| 1   | Identifiability and uncertainty quantification | Profile likelihood per parameter; FIM eigenvalues; Sobol sensitivity; bootstrap or Bayesian (emcee) posterior |
| 2   | Model selection and improvement | v12-baseline vs alternatives (e.g. relaxed mechanism-split, structural fix for fib-G2); AIC/BIC; settle "v13_final" |
| 3   | Robustness | Leave-one-timepoint-out; perturbation tests; predictive checks |
| 4   | Documentation | Formal model specification; parameter glossary with biological meaning and source per parameter |
| 4.5 | Virtual experiments | Predictive simulation of variants (myelosan dose, timing, hypothetical interventions) with prediction intervals |
| 5   | Manuscript and figures | Draft manuscript; publication-quality figures; supplementary materials |

## Target venues

Q1/Q2 mathematical-biology / computational-biology journals: Bull. Math. Biol., J. Theor. Biol., PLOS Comput. Biol., J. R. Soc. Interface (or equivalent).

## License

- **Code** (`src/`, `tests/`, `analyses/`): Apache License 2.0 — see [`LICENSE`](LICENSE).
- **Data, documentation, manuscript sources, internal notes** (`data/`, `docs/`, `manuscript/`, `notes/`, README files): Creative Commons Attribution 4.0 International (CC-BY-4.0) — see [`LICENSE-DOCS`](LICENSE-DOCS).

Both licenses permit reuse with attribution. When citing this work, please cite the eventual publication and the underlying dataset (Boiarchuk O. D., 1998–2023; provenance in `data/csv/PROVENANCE.md`).
