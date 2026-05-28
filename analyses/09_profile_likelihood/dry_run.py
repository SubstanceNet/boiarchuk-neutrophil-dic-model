"""
Dry run for profile likelihood: test on 3 parameters before full sweep.

Selected parameters:
  km — modifier for kr (group-specific). Expected: well-identified.
  tm — modifier for tp2. Expected: well-identified.
  cx — XIII channel (sloppy direction). Expected: sloppy or weakly-identified.

This test verifies:
  - profile_param() runs without error
  - profile shape is sensible (smooth, U-shape near minimum)
  - timing per parameter is feasible for full sweep estimate
"""
from __future__ import annotations
import json
import time
from pathlib import Path
import numpy as np

from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids
from src.profile_likelihood import profile_param

ANALYSIS_DIR = Path(__file__).resolve().parent
PARAMS_TO_TEST = ["km", "tm", "cx"]


def main():
    # Load v13 baseline best_x from analysis 05 seed=42
    baseline_path = Path("analyses/05_v13_baseline/results/fit.json")
    baseline = json.loads(baseline_path.read_text())
    best_x = np.array(baseline["best_x"])
    print(f"Loaded v13 baseline best_x from {baseline_path}")
    print(f"  baseline cost: {baseline['best_cost']:.6f}")
    print(f"  shape: {best_x.shape}")
    print()

    # Load data
    g1, g2 = load_data()
    n1, n2 = build_neutrophil_interpolators(g1, g2)
    tfg1, tfg2 = make_fine_grids()

    # Use linear grid for modifiers, log for cx
    log_grid_map = {"km": False, "tm": False, "cx": True}

    out_dir = ANALYSIS_DIR / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    summary_records = []
    for param_name in PARAMS_TO_TEST:
        log_grid = log_grid_map[param_name]
        print(f"=" * 60)
        print(f"Profile param: {param_name}  (log_grid={log_grid})")
        print(f"=" * 60)
        ts = time.time()
        result = profile_param(
            param_name, best_x,
            g1=g1, g2=g2,
            n1_interp=n1, n2_interp=n2,
            t_fine_g1=tfg1, t_fine_g2=tfg2,
            n_points=11,
            span_factor=0.5,
            log_grid=log_grid,
            verbose=True,
        )
        elapsed = time.time() - ts

        # Save individual result
        out_path = out_dir / f"profile_dry_{param_name}.json"
        out_path.write_text(json.dumps(result, indent=2, default=float))
        print(f"  Saved: {out_path}")
        print(f"  Elapsed: {elapsed:.1f}s")
        print()

        summary_records.append(dict(
            param_name=param_name,
            baseline_value=result["baseline_value"],
            baseline_cost=result["baseline_cost"],
            ci_95=result["ci_95"],
            classification=result["classification"],
            elapsed_s=elapsed,
            min_profile_cost=float(np.nanmin(result["profile_costs"])),
            max_profile_cost=float(np.nanmax(result["profile_costs"])),
        ))

    # Summary
    summary_path = out_dir / "dry_run_summary.json"
    summary_path.write_text(json.dumps({
        "analysis": "09_profile_likelihood_dry_run",
        "baseline_seed": 42,
        "n_points": 11,
        "span_factor": 0.5,
        "params": summary_records,
    }, indent=2, default=float))

    print()
    print("=" * 80)
    print(f"{'param':>5s} | {'baseline':>10s} | {'min_C':>8s} | {'max_C':>8s} | "
          f"{'CI low':>10s} | {'CI hi':>10s} | {'class':>20s} | {'sec':>6s}")
    print("-" * 80)
    for r in summary_records:
        ci_lo = f"{r['ci_95'][0]:.4f}" if r['ci_95'] else "N/A"
        ci_hi = f"{r['ci_95'][1]:.4f}" if r['ci_95'] else "N/A"
        print(f"{r['param_name']:>5s} | {r['baseline_value']:>10.4f} | "
              f"{r['min_profile_cost']:>8.4f} | {r['max_profile_cost']:>8.4f} | "
              f"{ci_lo:>10s} | {ci_hi:>10s} | {r['classification']:>20s} | "
              f"{r['elapsed_s']:>6.1f}")
    print()
    total_time = sum(r["elapsed_s"] for r in summary_records)
    print(f"Total dry run time: {total_time:.1f}s")
    avg_per_param = total_time / len(summary_records)
    full_sweep_estimate = avg_per_param * 26 / 60
    print(f"Average per param: {avg_per_param:.1f}s")
    print(f"Estimated full sweep (26 params): {full_sweep_estimate:.0f} min "
          f"= {full_sweep_estimate/60:.1f} h")


if __name__ == "__main__":
    main()
