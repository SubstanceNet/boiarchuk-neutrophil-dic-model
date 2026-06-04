# Supplementary Information

This directory contains the ten supplementary appendices for the manuscript
in `../manuscript/draft.md`. At submission they will be combined and
reformatted to the target journal's supplementary template; during
development they live as separate Markdown files for clean version control
and parallel editing.

## Index

| File | Title | Purpose |
|---|---|---|
| `S1_ode_formulation.md` | Full ODE Formulation and Observable Equations | Complete mathematical specification: five states, parameter table, three driving inputs, state equations, the gHn nonlinearity, observable mappings, fixed parameters, numerical integration, group-specific structure. |
| `S2_parameter_estimation.md` | Parameter Estimation Pipeline and Full Estimates | Cost function (data fit + W_SPLIT prior + Hn-saturation guard); two pipelines (base multi-seed vs. ensemble lightweight); Table S2 with all 26 parameter estimates and bootstrap CIs. |
| `S3_profile_likelihood.md` | Profile-likelihood Plots, All 26 Parameters | Per-parameter profiles and depth statistics; full identifiability classification (6 well-identified, 5 weakly identified, 12 sloppy, 3 grid-truncated); multi-start validation. |
| `S4_bootstrap_diagnostics.md` | Bootstrap Diagnostic Plots | Cost-distribution and convergence diagnostics; factor XIII basin classification and its bx/kx mechanism; per-observable R² across the ensemble; sensitivity to the normalisation choice. |
| `S5_intervention_timing.md` | Intervention-timing Trajectories and Temporal Metrics | Two-segment ODE protocol; full numerical table across nine timing scenarios; per-phase signature of the biphasic therapeutic window; rationale for t_recovery as the primary temporal metric; methodological caveats. |
| `S6_phase_diagrams.md` | Phase Diagrams for Dose–Response Severity Metrics | Dose–response setup with internal validation at the Group II baseline cell; the four valid severity metrics; methodological note on time-to-peak; documented retraction of the liver_collapse metric. |
| `S7_reproducibility.md` | Reproducibility and Data Provenance | Software environment; three reproduction levels (verify in seconds / reproduce key result in hours / reproduce everything in days); the bootstrap ensemble artefact; data provenance; data integrity audit. |
| `S8_mechanism_split_prior.md` | Sensitivity to the Mechanism-decomposition Prior Weight (W_SPLIT) | Empirical evidence that the W_SPLIT = 2.0 prior is necessary for identifiability and post-hoc validated by improved held-out (Group II) fit; full seed-stability and weight-sweep results. |
| `S9_xiii_bound.md` | Upper Bound on cx as a Structural Prior | Two-series experiment (analyses 02 and 06) establishing that the cx ≤ 600 bound is necessary, value-justified, and validated; the zone structure of the cost landscape; rejected alternatives. |
| `S10_joint_architecture.md` | Shared Architecture vs. Group-II-only | Per-observable comparison of joint fit vs. separate Group II fit; the ~22 pp average R² gap quantified; three arguments establishing the gap as architectural rather than overfitting; trade-off discussion. |

## Cross-referencing convention

Main-text references to "Supplementary §S⟨n⟩" throughout `manuscript/draft.md`
map to the files above by section number. The appendices in turn cross-
reference main-text sections (§1–§5) and each other; the citation network
is closed (every appendix is referenced from the main text; every main-text
§S⟨n⟩ pointer resolves to an existing appendix).

## Source artefacts

Most supplementary content is derived from analysis artefacts in `../analyses/`:

- S2 estimates table: `analyses/22_predictive_check/results/ensemble_members.json`
- S3 profile depths: `analyses/09_profile_likelihood/results/`
- S4 bootstrap ensemble: `analyses/22_predictive_check/` (range normalisation)
  and `analyses/34_pergroupstd_bootstrap/` (sensitivity check)
- S5 timing trajectories: `analyses/31_intervention_timing/results/`
- S6 dose–response: `analyses/30_myelosan_dose/results/`
- S8 W_SPLIT sweep: `analyses/01_w_split_profile/results/`
- S9 cx bound: `analyses/02_cx_bound/results/` and `analyses/06_v13_cx_diagnostic/results/`
- S10 separate Group II fit: `analyses/03_separate_g2_fit/results/`

The data underlying all numerical claims is therefore traceable from the
appendix prose to a JSON or CSV artefact in the analyses tree, and from
that artefact to a `run.py` script that produces it.
