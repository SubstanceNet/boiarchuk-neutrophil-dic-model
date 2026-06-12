"""
Analysis 05: v13 baseline fit.

Single quick-mode fit using src.cost_v13.joint_cost_v13 in default
configuration (W_GROUP = (1.0, 1.0), W_SPLIT = 2.0, default cx bound,
uniform W_SURV hard-coded in v13). Single seed (42).

Reference point for subsequent v13 analyses.
"""
from __future__ import annotations
import json
from pathlib import Path

from src.fit_runner import run_with_overrides_v13

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR = ANALYSIS_DIR / "results" / "_cache"


def main():
    print("=" * 65)
    print("v13 baseline (analysis 05)")
    print("  cost = src.cost_v13.joint_cost_v13")
    print("  W_GROUP = (1.0, 1.0)  [v12-compatible scale]")
    print("  W_SPLIT = 2.0         [validated in analysis 01]")
    print("  cx bound = (10, 600)  [validated in analysis 02]")
    print("  W_SURV  = ones(16)    [hard-coded; per analysis 04]")
    print("  seed = 42, quick mode")
    print("=" * 65)

    result = run_with_overrides_v13(
        overrides={},   # all defaults
        seeds=[42], quick=True,
        cache_dir=CACHE_DIR,
        label="v13_baseline",
        verbose=True,
    )

    out = ANALYSIS_DIR / "results" / "fit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    serialisable = {
        "analysis": "05_v13_baseline",
        "cost_version": result["cost_version"],
        "w_group": result["w_group"],
        "best_cost": result["best_cost"],
        "best_x": result["best_x"],
        "params": result["params_dict"],
        "decomposition": result["decomposition"],
        "metrics_g1": result["metrics_g1"],
        "metrics_g2": result["metrics_g2"],
        "avg_r2_g1": result["avg_r2_g1"],
        "avg_r2_g2": result["avg_r2_g2"],
        "wall_time": result["wall_time"],
    }
    out.write_text(json.dumps(serialisable, indent=2, default=float))

    print()
    print("=" * 65)
    print(f"v13 baseline:")
    print(f"  cost = {result['best_cost']:.4f}")
    print(f"  R^2_G1 avg = {result['avg_r2_g1']:+.4f}")
    print(f"  R^2_G2 avg = {result['avg_r2_g2']:+.4f}")
    print()
    print("Per-observable R^2 G1:")
    for k in ["recalc", "thrombin", "fib", "xiii", "AP", "D"]:
        print(f"  {k:>10s}: {result['metrics_g1'][k]['R2']:+.4f}")
    print()
    print("Per-observable R^2 G2:")
    for k in ["recalc", "thrombin", "fib", "xiii", "AP", "D"]:
        print(f"  {k:>10s}: {result['metrics_g2'][k]['R2']:+.4f}")
    print()
    print("Comparison to analysis 02 baseline (v12 cost):")
    print("  v12 R^2_G1 avg: +0.8340")
    print(f"  v13 R^2_G1 avg: {result['avg_r2_g1']:+.4f}")
    print(f"  Δ = {result['avg_r2_g1'] - 0.8340:+.4f}")
    print()
    # 0.6204 is the v12 reference; 0.6920 (below, computed) is the v13 production
    # baseline cited in the manuscript and S10.
    print("  v12 R^2_G2 avg: +0.6204  [reference, superseded by v13 below]")
    print(f"  v13 R^2_G2 avg: {result['avg_r2_g2']:+.4f}")
    print(f"  Δ = {result['avg_r2_g2'] - 0.6204:+.4f}")
    print()
    print(f"Saved -> {out}")


if __name__ == "__main__":
    main()
