"""
Multi-seed convergence check for cx_expanded and cx_wide.

Question: does the XIII-G2 collapse (R^2 < 0) reproduce across seeds, or is
it a single-seed artefact?

Runs 4 fits: cx in {(10, 2000), (10, 5000)} times seeds in {7, 123}.
Reports per-observable R^2 for both groups, with focus on xiii_G2.
"""
from __future__ import annotations
import json
from pathlib import Path
from src.fit_runner import run_with_overrides

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR = ANALYSIS_DIR / "results" / "_cache"

CONFIGS = [
    ("expanded", (10.0, 2000.0)),
    ("wide",     (10.0, 5000.0)),
]
SEEDS = [7, 123]

results = []
for label, (lo, hi) in CONFIGS:
    for seed in SEEDS:
        r = run_with_overrides(
            overrides={"W_SPLIT": 2.0, "BOUNDS_OVERRIDE": {"cx": (lo, hi)}},
            seeds=[seed], quick=True,
            cache_dir=CACHE_DIR,
            label=f"cx_{label} seed={seed}",
            verbose=True,
        )
        results.append(dict(
            label=label, cx_max=hi, seed=seed,
            cost=r["best_cost"],
            avg_r2_g1=r["avg_r2_g1"], avg_r2_g2=r["avg_r2_g2"],
            cx=r["params_dict"]["cx"],
            xiii_G1=r["metrics_g1"]["xiii"]["R2"],
            xiii_G2=r["metrics_g2"]["xiii"]["R2"],
            recalc_G2=r["metrics_g2"]["recalc"]["R2"],
            AP_G2=r["metrics_g2"]["AP"]["R2"],
            D_G2=r["metrics_g2"]["D"]["R2"],
            fib_G2=r["metrics_g2"]["fib"]["R2"],
        ))

(ANALYSIS_DIR / "results" / "seed_check.json").write_text(
    json.dumps(results, indent=2, default=float))

print()
print(f'{"label":>9s} | {"cx_max":>6s} | {"seed":>4s} | {"cost":>7s} | '
      f'{"cx_fit":>8s} | {"xiii_G2":>8s} | {"recalc_G2":>9s} | '
      f'{"AP_G2":>6s} | {"D_G2":>6s} | {"fib_G2":>6s}')
print("-" * 100)
for r in results:
    print(f'{r["label"]:>9s} | {r["cx_max"]:>6.0f} | {r["seed"]:>4d} | '
          f'{r["cost"]:>7.4f} | {r["cx"]:>8.1f} | {r["xiii_G2"]:>+8.4f} | '
          f'{r["recalc_G2"]:>+9.4f} | {r["AP_G2"]:>+6.3f} | '
          f'{r["D_G2"]:>+6.3f} | {r["fib_G2"]:>+6.3f}')
