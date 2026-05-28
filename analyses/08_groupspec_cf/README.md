# Analysis 08 — Group-specific c_f (v13_gs[cf] diagnostic)

## Question

Does making `cf` group-specific (separate `cf_g1` and `cf_g2` parameters)
improve fib G2 fit quality (resolves I-4 partially) and/or the overall
G2 fit?

`cf` is the coefficient of neutrophil-mediated fibrinogen production:
the rate at which activated neutrophils contribute to fib synthesis.
Biologically: if myelosan reduces neutrophil-driven IL-6 signalling
to the liver, the effective `cf` should be lower in G2.

This is the second candidate after `cx` (analysis 07, rejected).

## Hypothesis

Splitting `cf` into group-specific parameters provides extra degree of
freedom for the fib channel. Expected:
- `cf_g2 < cf_g1` (myelosan-suppressed neutrophils produce less fib);
- ΔR²_G2 for fib > +0.10;
- ΔR²_G2 avg > +0.03;
- Possibly improved seed-stability if `cf_g2 != cf_g1` is informative.

## Method

Three v13_gs quick-mode fits at seeds {42, 7, 123} with `cf` as the
group-specific parameter, all defaults otherwise:
- 27-dim parameter space (26 v13 + cf_g2)
- cf_g2 bounds: (5, 350), identical to cf_g1
- W_GROUP = (1.0, 1.0), W_SPLIT = 2.0, uniform W_SURV (v13 hard-coded)

## Decision rule

| Observation | Conclusion |
|-------------|------------|
| ΔR²_G2 (fib) > +0.10 AND |cf_ratio - 1| > 0.2 in all seeds | Group-specific cf carries information. Promote candidate. |
| ΔR²_G2 (fib) > +0.10 BUT cf_ratio ≈ 1 | Optimisation artefact, similar to cx case (rejected). |
| cf_ratio ≈ 1 in all seeds | Data do not require group-specific cf. Reject. |
| Seed-instability in cf_g2 | Identifiability issue with cf as well; investigate full {af, bf, cf, df} channel. |

## Run

```bash
python -m analyses.08_groupspec_cf.fit
```

Wall-clock: ~40 min on 16-thread workstation.
