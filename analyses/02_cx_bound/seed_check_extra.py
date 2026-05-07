"""
Extra seed check for analysis 02 — two additional seeds at wide cx bound.

Question: is wide/s123 (xiii_G2 = +0.62 at cx = 1621) a stable alternative
basin or a single-seed convergence artefact?

Adds 2 fits at cx <= 5000, seeds {999, 2024}. Combined with the original
seed_check (seeds 7, 123) and main sweep (seed 42), gives 4-seed coverage
at the wide bound.
"""
from __future__ import annotations
import json
from pathlib import Path
from src.fit_runner import run_with_overrides

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR = ANALYSIS_DIR / "results" / "_cache"

SEEDS_EXTRA = [999, 2024]
CX_BOUND = (10.0, 5000.0)

results = []
for seed in SEEDS_EXTRA:
    r = run_with_overrides(
        overrides={"W_SPLIT": 2.0, "BOUNDS_OVERRIDE": {"cx": CX_BOUND}},
        seeds=[seed], quick=True,
        cache_dir=CACHE_DIR,
        label=f"cx_wide seed={seed}",
        verbose=True,
    )
    results.append(dict(
        label="wide", cx_max=CX_BOUND[1], seed=seed,
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

(ANALYSIS_DIR / "results" / "seed_check_extra.json").write_text(
    json.dumps(results, indent=2, default=float))

print()
print(f'{"label":>5s} | {"cx_max":>6s} | {"seed":>5s} | {"cost":>7s} | '
      f'{"cx_fit":>8s} | {"xiii_G2":>8s} | {"recalc_G2":>9s} | '
      f'{"AP_G2":>6s} | {"D_G2":>6s} | {"fib_G2":>6s}')
print("-" * 100)
for r in results:
    print(f'{r["label"]:>5s} | {r["cx_max"]:>6.0f} | {r["seed"]:>5d} | '
          f'{r["cost"]:>7.4f} | {r["cx"]:>8.1f} | {r["xiii_G2"]:>+8.4f} | '
          f'{r["recalc_G2"]:>+9.4f} | {r["AP_G2"]:>+6.3f} | '
          f'{r["D_G2"]:>+6.3f} | {r["fib_G2"]:>+6.3f}')
