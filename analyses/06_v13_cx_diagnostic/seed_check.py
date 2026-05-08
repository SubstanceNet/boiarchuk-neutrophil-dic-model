"""
Seed-stability check for v13 cx-bound diagnostic.

Question: is the alternating pattern of xiii_G2 (good/sacrifice/good/sacrifice
/good across cx bounds {500, 600, 700, 1000, 2000} at seed=42) a robust
property of the v13 landscape, or a single-seed artefact?

Runs 10 fits: 5 cx bounds × 2 additional seeds {7, 123}.
Cached results from main sweep (seed 42) are available for combined view.
"""
from __future__ import annotations
import json
from pathlib import Path

from src.fit_runner import run_with_overrides_v13

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR = ANALYSIS_DIR / "results" / "_cache"

CX_BOUNDS = [
    ("tight",     (10.0, 500.0)),
    ("v12_prior", (10.0, 600.0)),
    ("loose",     (10.0, 700.0)),
    ("expanded",  (10.0, 1000.0)),
    ("wide",      (10.0, 2000.0)),
]
SEEDS_EXTRA = [7, 123]


def main():
    results = []
    for label, (lo, hi) in CX_BOUNDS:
        for seed in SEEDS_EXTRA:
            r = run_with_overrides_v13(
                overrides={"BOUNDS_OVERRIDE": {"cx": (lo, hi)}},
                seeds=[seed], quick=True,
                cache_dir=CACHE_DIR,
                label=f"cx_{label} seed={seed}",
                verbose=True,
            )
            results.append(dict(
                label=label,
                cx_max=hi,
                seed=seed,
                cost=r["best_cost"],
                avg_r2_g1=r["avg_r2_g1"],
                avg_r2_g2=r["avg_r2_g2"],
                cx=r["params_dict"]["cx"],
                xiii_G1=r["metrics_g1"]["xiii"]["R2"],
                xiii_G2=r["metrics_g2"]["xiii"]["R2"],
                recalc_G2=r["metrics_g2"]["recalc"]["R2"],
                AP_G2=r["metrics_g2"]["AP"]["R2"],
                D_G2=r["metrics_g2"]["D"]["R2"],
                fib_G2=r["metrics_g2"]["fib"]["R2"],
                thrombin_G2=r["metrics_g2"]["thrombin"]["R2"],
            ))

    (ANALYSIS_DIR / "results" / "seed_check.json").write_text(
        json.dumps(results, indent=2, default=float))

    print()
    print(f'{"label":>10s} | {"cx_max":>6s} | {"seed":>4s} | {"cost":>7s} | '
          f'{"cx_fit":>7s} | {"xiii_G2":>8s} | {"recalc":>7s} | '
          f'{"AP":>7s} | {"D":>7s}')
    print("-" * 95)
    for r in results:
        print(f'{r["label"]:>10s} | {r["cx_max"]:>6.0f} | {r["seed"]:>4d} | '
              f'{r["cost"]:>7.4f} | {r["cx"]:>7.1f} | '
              f'{r["xiii_G2"]:>+8.4f} | {r["recalc_G2"]:>+7.4f} | '
              f'{r["AP_G2"]:>+7.4f} | {r["D_G2"]:>+7.4f}')


if __name__ == "__main__":
    main()
