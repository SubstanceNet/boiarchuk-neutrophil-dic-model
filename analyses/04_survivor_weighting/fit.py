"""
Analysis 04: Survivor-weighting sensitivity.

Run a fit with W_SURV = ones(16), compare to the analysis 02 baseline.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

from src.fit_runner import run_with_overrides

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR = ANALYSIS_DIR / "results" / "_cache"


def main():
    print("=" * 65)
    print("Survivor-weighting sensitivity (analysis 04)")
    print("  W_SURV override: ones(16)  (vs default [1]*10+[0.7]*3+[0.3]*3)")
    print("=" * 65)

    result = run_with_overrides(
        overrides={"W_SURV": np.ones(16)},
        seeds=[42], quick=True,
        cache_dir=CACHE_DIR,
        label="W_SURV=ones",
        verbose=True,
    )

    out = ANALYSIS_DIR / "results" / "fit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    serialisable = {
        "analysis": "04_survivor_weighting",
        "best_cost": result["best_cost"],
        "best_x": result["best_x"],
        "params": result["params_dict"],
        "metrics_g1": result["metrics_g1"],
        "metrics_g2": result["metrics_g2"],
        "avg_r2_g1": result["avg_r2_g1"],
        "avg_r2_g2": result["avg_r2_g2"],
        "wall_time": result["wall_time"],
    }
    out.write_text(json.dumps(serialisable, indent=2, default=float))

    print()
    print("=" * 65)
    print(f"With W_SURV = ones(16):")
    print(f"  cost = {result['best_cost']:.6f}")
    print(f"  R^2_G1 avg = {result['avg_r2_g1']:+.4f}")
    print(f"  R^2_G2 avg = {result['avg_r2_g2']:+.4f}")
    print()
    print("Comparison to analysis 02 baseline (default W_SURV):")
    print("  baseline cost: 1.0431")
    # NOTE: 0.8340 / 0.6204 are STALE v12 baselines (reference only). The v13
    # production baselines are 0.8334 / 0.6920 (analyses/05). The W_SURV effect
    # measured here is unaffected: it isolates the weighting change within one
    # cost version. See S10.
    print("  baseline R^2_G1 avg: +0.8340  [v12 reference, superseded]")
    print("  baseline R^2_G2 avg: +0.6204  [v12 reference, superseded]")
    print()
    print(f"Δcost: {result['best_cost'] - 1.0431:+.4f}")
    print(f"ΔR^2_G1: {result['avg_r2_g1'] - 0.8340:+.4f}")
    print(f"ΔR^2_G2: {result['avg_r2_g2'] - 0.6204:+.4f}")
    print()
    print(f"Saved -> {out}")


if __name__ == "__main__":
    main()
