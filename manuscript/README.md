# Manuscript

This directory contains the manuscript for the research project on neutrophil-
mediated disseminated intravascular coagulation (DIC), prepared for submission
to *npj Systems Biology and Applications*.

## Scientific scope

The project develops a mechanistic ordinary-differential-equation model of DIC
in an experimental rabbit model induced by ethylphenacin (an anticoagulant
rodenticide and vitamin K antagonist). The model is fitted jointly to two
experimental groups — a control group with standard DIC course (Group I) and
a group with pharmacologically suppressed granulopoiesis via busulfan
(Group II) — across six observables of haemostasis and neutrophil activity,
using 24 shared parameters and two group-specific kinetic modifiers (k_m, t_m).

The manuscript follows a five-step narrative:

1. The model fits the dynamics of both groups (mean R² = 0.83 / 0.69 for
   Group I / Group II).
2. Its parameter map — six well-identified parameters (profile-likelihood
   relative depth > 5 %), the remaining twenty weakly identified, sloppy, or
   grid-truncated — is standard for mechanistic systems-biology models of this
   size.
3. The mechanism decomposition (vascular vs. neutrophil-mediated contributions
   to each coagulation channel) is internally consistent with the day-1
   between-group signal, used as a structural prior.
4. Independent corroboration: the model reproduces the peak day (11), the
   ~21-fold group separation in hypocoagulation severity (raw median ratio
   ≈22×, reported as 21× relative to the rounded Group II baseline of 7 s), and
   the factor XIII and fibrinogen nadirs to within 1 % and 11 %, respectively.
5. Prediction: a biphasic therapeutic window for myelosuppressive intervention,
   with a transition between days 2.5 and 3, and dose and timing acting as
   independent thresholds.

## Contents

- `draft.md` — the working manuscript (English, npj style). Unnumbered section
  headings in the order: Title/author block, Abstract, Introduction, Results,
  Discussion, Methods, Declarations (Data availability, Code availability,
  Competing interests, Funding, Ethics approval, Author contributions),
  References.
- `README.md` — this file.

## Figures and tables

Publication-quality figures are generated at run-time from analysis scripts,
not stored in `manuscript/`. Each figure corresponds to a single analysis
directory under `analyses/`:

| Figure | Generator | Output |
|---|---|---|
| Fig. 1. Baseline fits | `analyses/05_v13_baseline/make_fig1.py` | `fig1_baseline_fits.{png,pdf}` |
| Fig. 2. Identifiability + XIII under-determination | `analyses/22_predictive_check/make_fig2.py` | `fig2_identifiability.{png,pdf}` |
| Fig. 3. Mechanism decomposition | `analyses/22_predictive_check/make_fig3.py` | `fig3_mechanism_split.{png,pdf}` |
| Fig. 4. Dose–response phase diagrams | `analyses/30_myelosan_dose/make_fig4.py` | `fig4_phase_diagram.{png,pdf}` |
| Fig. 5. Dose–response slice | `analyses/30_myelosan_dose/make_fig5.py` | `fig5_dose_response_slice.{png,pdf}` |
| Fig. 6. Therapeutic window | `analyses/31_intervention_timing/make_fig6.py` | `fig6_severity_vs_timing.{png,pdf}` |

Tables 1–4 are inline in `draft.md` and contain values from the same analyses:
Table 1 (well-identified parameter CIs) and Table 2 (mechanism fractions) from
analysis 22; Table 3 (severity validation) from analysis 33; Table 4 (dose ×
time scenarios) from analysis 32.

## Supplementary information

Ten supplementary appendices (`S1`–`S10`) provide the full mathematical
specification, estimation pipeline, identifiability and bootstrap diagnostics,
intervention-timing trajectories, phase diagrams, reproducibility protocol,
and architectural justifications. They live in `../supplementary/` as separate
Markdown files; see that directory's README for the index and cross-referencing
convention (the main text cites appendices as "§S⟨n⟩"; the appendices refer
back to the main text by section *name*, since the manuscript uses unnumbered
headings). Every appendix S1–S10 is cited at least once from `draft.md`.

## Authorship and division of work

- **Olena Boiarchuk** — experimental work, biological interpretation,
  Introduction and Discussion. State Institution "Luhansk Taras Shevchenko
  National University", Department of Health and Rehabilitation. ORCID:
  0000-0002-4388-6011.
- **Oleksiy Onasenko** — mathematical model, numerical estimation,
  robustness analyses, virtual experiments, analytical code, Methods and
  Results. Independent researcher. ORCID: 0009-0007-7017-8161.

Corresponding author: Olena Boiarchuk, boiarchuk.helen@gmail.com.

## Editorial history

The manuscript was developed iteratively and reorganised into the current
npj-style draft from an earlier numbered-section version. Structural milestones
are recorded as git tags (e.g. `manuscript-v2-final`, `pre-submission-audit`,
`v1.0.0`). The released code+data snapshot accompanying the manuscript is tag
`v1.0.0`, archived on Zenodo (DOI 10.5281/zenodo.20673521); post-release
corrections are collected for a subsequent `v1.0.1` release.
