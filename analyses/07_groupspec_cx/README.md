# Analysis 07 — Group-specific cx (v13_gs diagnostic)

> Rejected hypothesis; retained as evidence cited by S9/S10. Not part of the production pipeline.

## Question

Does making `cx` group-specific (separate `cx_g1` and `cx_g2` parameters)
resolve the multi-modal landscape and identifiability issues observed
under v13 baseline (analyses 05, 06; issues I-9, I-10)?

## Hypothesis

Splitting cx into group-specific parameters provides one extra degree
of freedom in the XIII channel, allowing the optimiser to fit G1 and G2
XIII dynamics independently. This should:

- Yield seed-stable convergence (single basin per seed, low spread).
- Improve xiii_G2 R² without sacrificing G1.
- Reveal whether the data prefer cx_g1 ≈ cx_g2 (no group difference)
  or cx_g1 ≠ cx_g2 (myelosan affects neutrophil-mediated XIII production).

## Method

Three v13_gs quick-mode fits, seeds {42, 7, 123}, all defaults except:
- 27-dim parameter space (26 v13 + 1 cx_g2)
- cx_g2 bounds: (10, 600), identical to cx_g1
- W_GROUP = (1.0, 1.0), W_SPLIT = 2.0, uniform W_SURV (v13 hard-coded)

## Decision rule

| Observation | Conclusion |
|-------------|------------|
| ΔR²_G2 > +0.05 vs analysis 05 baseline AND seed-stable AND |Δcx| > 100 | Group-specific cx resolves I-9/I-10. Promote to production. |
| ΔR²_G2 > +0.05 BUT seed-unstable | Identifiability shifted to {ax, bx, kx}. Try those next. |
| ΔR²_G2 < +0.02 | cx group-specific does not carry information. Try `c_f` or `kna` instead. |
| ΔR²_G2 > +0.05 BUT cx_g1 ≈ cx_g2 in all seeds | Data do not require group-specific cx; the gain is artefact of optimisation. |

## Run

```bash
python -m analyses.07_groupspec_cx.fit
```

Wall-clock: ~40 min on 16-thread workstation (3 quick fits, ~12 min each).
