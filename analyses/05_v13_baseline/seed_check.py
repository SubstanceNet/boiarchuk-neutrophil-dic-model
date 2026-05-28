"""
Seed-stability check for v13 baseline.

Run two more fits at seeds {7, 123} with the same v13 default config.
Compare R²_G1, R²_G2, and per-observable G2 R² for stability.

If xiii_G2 R² varies wildly across seeds, the analysis 05 result is
basin-dependent. If stable, the low xiii_G2 R² is a robust feature of
v13 baseline that must be addressed in Phase 2 step 2.
"""
from __future__ import annotations
import json
from pathlib import Path

from src.fit_runner import run_with_overrides_v13

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR = ANALYSIS_DIR / "results" / "_cache"

results = []
for seed in [7, 123]:
    r = run_with_overrides_v13(
        overrides={}, seeds=[seed], quick=True,
        cache_dir=CACHE_DIR,
        label=f"v13_baseline seed={seed}",
        verbose=True,
    )
    results.append(dict(
        seed=seed,
        cost=r["best_cost"],
        avg_r2_g1=r["avg_r2_g1"],
        avg_r2_g2=r["avg_r2_g2"],
        per_obs_g2={k: r["metrics_g2"][k]["R2"] for k in
                    ["recalc", "thrombin", "fib", "xiii", "AP", "D"]},
        cx=r["params_dict"]["cx"],
    ))

(ANALYSIS_DIR / "results" / "seed_check.json").write_text(
    json.dumps(results, indent=2, default=float))

print()
print(f'{"seed":>5s} | {"cost":>7s} | {"R²_G1":>7s} | {"R²_G2":>7s} | '
      f'{"recalc":>7s} | {"thr":>7s} | {"fib":>7s} | {"xiii":>7s} | '
      f'{"AP":>7s} | {"D":>7s} | {"cx":>7s}')
print("-" * 100)
print(f'{42:>5d} | {0.9589:>7.4f} | {0.8334:>+7.4f} | {0.6920:>+7.4f} | '
      f'{0.9068:>+7.4f} | {0.9468:>+7.4f} | {0.4977:>+7.4f} | {0.0772:>+7.4f} | '
      f'{0.9638:>+7.4f} | {0.7594:>+7.4f} | {570.9:>7.1f}    [from analysis 05 main]')
for r in results:
    o = r["per_obs_g2"]
    print(f'{r["seed"]:>5d} | {r["cost"]:>7.4f} | {r["avg_r2_g1"]:>+7.4f} | '
          f'{r["avg_r2_g2"]:>+7.4f} | {o["recalc"]:>+7.4f} | {o["thrombin"]:>+7.4f} | '
          f'{o["fib"]:>+7.4f} | {o["xiii"]:>+7.4f} | {o["AP"]:>+7.4f} | '
          f'{o["D"]:>+7.4f} | {r["cx"]:>7.1f}')
