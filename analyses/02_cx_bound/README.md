# Analysis 02 — cx parameter bound exploration

## Question

In v12-baseline (W=2, seed=42, default bounds), `cx` fits at 599.7 — within
0.05% of the upper bound 600. The v12 internal report quotes a fitted value
of 1481 in some run, outside the current script's bounds. Is the upper bound
of 600 artificially constraining the optimum, or is cx genuinely sloppy
(uninformative direction in parameter space)?

This addresses issue **I-1** in `notes/known_issues.md`.

## Method

Three fits at W=2.0, seed=42, quick mode, varying only the cx upper bound:

| Run | cx bounds | Rationale |
|-----|-----------|-----------|
| baseline | (10, 600)  | matches v12 archive |
| expanded | (10, 2000) | tests whether v12-report value 1481 is reachable |
| wide     | (10, 5000) | tests for saturation of any cost improvement |

For each run, record:
- cost, R²_G1, R²_G2 (avg + per-observable)
- final cx and the entire XIII-channel parameter group {ax, cx, bx, kx}
- realised xiii_neutro_frac on G1 day 2

## Decision rule

| Observation | Conclusion |
|-------------|------------|
| Cost stable across all three runs; cx grows but xiii-fraction stays | cx is sloppy. Keep current bound (10, 600); document that the upper bound is non-binding in informational sense. |
| Cost improves with expansion, then saturates | Expand bound to where cost saturates; refit baseline. Document new bound. |
| Cost improves monotonically with no saturation | Pathology: cx is degenerate. Need structural model fix (issue I-1 escalates). |

## Run

```bash
python -m analyses.02_cx_bound.sweep
```

Wall-clock: ~36 min on 16-thread workstation.
