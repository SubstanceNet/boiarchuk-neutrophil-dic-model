"""
Analysis 08: v13 with group-specific cf.

Three quick-mode fits at seeds {42, 7, 123} using v13_gs with
groupspec_param='cf'. Compare to:
- analysis 05 v13 baseline (cf shared)
- analysis 07 v13_gs[cx] (negative result)

Outputs:
- results/fit_seed_42.json, fit_seed_7.json, fit_seed_123.json — individual results
- results/summary.json — combined seed-stability table
- results/_cache/*.pkl — hash-keyed fit caches
"""
from __future__ import annotations
import json
from pathlib import Path

from src.fit_runner import run_with_overrides_v13_gs

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR = ANALYSIS_DIR / "results" / "_cache"
SEEDS = [42, 7, 123]


def main():
    print("=" * 70)
    print("v13_gs[cf] (group-specific cf) — analysis 08")
    print("  parameter space: 27 (26 v13 + cf_g2)")
    print("  cf_g2 bounds: (5, 350) — same as cf_g1")
    print(f"  seeds: {SEEDS}, quick mode")
    print("=" * 70)

    results = []
    for seed in SEEDS:
        r = run_with_overrides_v13_gs(
            overrides={},
            groupspec_param="cf",
            seeds=[seed], quick=True,
            cache_dir=CACHE_DIR,
            label=f"v13_gs[cf] seed={seed}",
            verbose=True,
        )
        per_obs_g2 = {k: r["metrics_g2"][k]["R2"] for k in
                      ["recalc", "thrombin", "fib", "xiii", "AP", "D"]}
        per_obs_g1 = {k: r["metrics_g1"][k]["R2"] for k in
                      ["recalc", "thrombin", "fib", "xiii", "AP", "D"]}
        record = dict(
            seed=seed,
            cost=r["best_cost"],
            avg_r2_g1=r["avg_r2_g1"],
            avg_r2_g2=r["avg_r2_g2"],
            cf_g1=r["g1_value"],
            cf_g2=r["g2_value"],
            cf_ratio=r["ratio"],
            per_obs_g1=per_obs_g1,
            per_obs_g2=per_obs_g2,
            wall_time=r["wall_time"],
            cached=r["cached"],
        )
        results.append(record)

        out_path = ANALYSIS_DIR / "results" / f"fit_seed_{seed}.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps({
            **record,
            "params": r["params_dict"],
            "decomposition": r["decomposition"],
            "metrics_g1": r["metrics_g1"],
            "metrics_g2": r["metrics_g2"],
        }, indent=2, default=float))

    summary = dict(
        analysis="08_groupspec_cf",
        cost_version="v13_gs",
        groupspec_param="cf",
        seeds=SEEDS,
        results=results,
    )
    (ANALYSIS_DIR / "results" / "summary.json").write_text(
        json.dumps(summary, indent=2, default=float))

    print()
    print("=" * 110)
    print(f'{"seed":>4s} | {"cost":>7s} | {"R²_G1":>7s} | {"R²_G2":>7s} | '
          f'{"cf_g1":>6s} | {"cf_g2":>6s} | {"ratio":>6s} | '
          f'{"fib_G2":>8s} | {"xiii_G2":>8s} | {"AP_G2":>7s} | {"D_G2":>7s}')
    print("-" * 110)
    for r in results:
        print(f'{r["seed"]:>4d} | {r["cost"]:>7.4f} | '
              f'{r["avg_r2_g1"]:>+7.4f} | {r["avg_r2_g2"]:>+7.4f} | '
              f'{r["cf_g1"]:>6.1f} | {r["cf_g2"]:>6.1f} | '
              f'{r["cf_ratio"]:>6.3f} | '
              f'{r["per_obs_g2"]["fib"]:>+8.4f} | '
              f'{r["per_obs_g2"]["xiii"]:>+8.4f} | '
              f'{r["per_obs_g2"]["AP"]:>+7.4f} | '
              f'{r["per_obs_g2"]["D"]:>+7.4f}')
    print()

    print("Comparison to analysis 05 v13 baseline (cf shared, default):")
    print("  baseline R²_G2 avg by seed: [42: 0.6920, 7: 0.7141, 123: 0.7517]")
    print("  baseline fib_G2 R² by seed: [42: 0.4977, 7: 0.4460, 123: 0.4875]")
    print()

    costs = [r["cost"] for r in results]
    r2g2s = [r["avg_r2_g2"] for r in results]
    fib_g2s = [r["per_obs_g2"]["fib"] for r in results]
    cf_g1s = [r["cf_g1"] for r in results]
    cf_g2s = [r["cf_g2"] for r in results]
    ratios = [r["cf_ratio"] for r in results]
    print(f"Spreads across seeds:")
    print(f"  Δcost      = {max(costs) - min(costs):.4f}")
    print(f"  ΔR²_G2 avg = {max(r2g2s) - min(r2g2s):.4f}")
    print(f"  Δfib_G2    = {max(fib_g2s) - min(fib_g2s):.4f}")
    print(f"  Δcf_g1     = {max(cf_g1s) - min(cf_g1s):.1f}")
    print(f"  Δcf_g2     = {max(cf_g2s) - min(cf_g2s):.1f}")
    print(f"  Δratio     = {max(ratios) - min(ratios):.3f}")
    print()
    print(f"Saved -> {ANALYSIS_DIR / 'results' / 'summary.json'}")


if __name__ == "__main__":
    main()
