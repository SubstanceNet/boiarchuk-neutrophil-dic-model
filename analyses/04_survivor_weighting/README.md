# Analysis 04 — Survivor weighting sensitivity

## Question

The default G1 survivor weights `W_SURV = [1.0]×10 + [0.7]×3 + [0.3]×3`
qualitatively reflect 30% mortality on days 10-12 and further dropout
afterwards, but the values 0.7 and 0.3 are ad hoc, not derived from a
likelihood justification. Does this weighting materially affect the
final fit?

This addresses **I-5** in `notes/known_issues.md`.

## Method

Run a quick-mode joint fit (W_split=2, default cx bound) with
`W_SURV = ones(16)` (uniform weighting), seed=42. Compare to the
analysis 02 baseline fit (which uses default W_SURV).

## Decision rule

| Observation | Conclusion |
|-------------|------------|
| Both fits converge to nearly identical parameters and R²s | W_SURV ad-hoc choice is non-influential. Document and proceed. |
| Parameters or R² shift substantially | W_SURV is doing real work. Need principled replacement (e.g., variance-based weights). |

## Run

```bash
python -m analyses.04_survivor_weighting.fit
```

Wall-clock: ~12 min on 16-thread workstation.
