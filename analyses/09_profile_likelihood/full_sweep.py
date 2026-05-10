"""
Full profile likelihood sweep over all 26 v13 parameters.

Uses v13 baseline (analysis 05, seed 42) as reference point.
Single-start Nelder-Mead in 25-dim space for each grid point.

Per-param defaults:
  - 11 grid points
  - span_factor 0.5 (linear: ±50%, log: factor of e^0.5 ≈ 1.65 each side)
  - log_grid for rate constants and concentration parameters,
    linear for modifiers (km, tm).
"""
from __future__ import annotations
import json
import time
from pathlib import Path
import numpy as np

from src import config as cfg
from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids
from src.profile_likelihood import profile_param

ANALYSIS_DIR = Path(__file__).resolve().parent

# Linear grid for parameters that are by-design modifiers/multipliers.
# Log grid for everything else (rate constants, concentrations, etc.).
LINEAR_GRID_PARAMS = {"km", "tm"}


def main():
    # Load v13 baseline best_x from analysis 05 seed=42
    baseline_path = Path("analyses/05_v13_baseline/results/fit.json")
    baseline = json.loads(baseline_path.read_text())
    best_x = np.array(baseline["best_x"])
    print(f"Loaded v13 baseline best_x from {baseline_path}")
    print(f"  baseline cost: {baseline['best_cost']:.6f}")
    print(f"  shape: {best_x.shape}")
    print(f"  total params to profile: {len(cfg.NAMES)}")
    print()

    g1, g2 = load_data()
    n1, n2 = build_neutrophil_interpolators(g1, g2)
    tfg1, tfg2 = make_fine_grids()

    out_dir = ANALYSIS_DIR / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    summary_records = []
    sweep_start = time.time()

    for i, param_name in enumerate(cfg.NAMES):
        log_grid = param_name not in LINEAR_GRID_PARAMS
        print(f"=" * 70)
        print(f"[{i+1}/{len(cfg.NAMES)}] Profile param: {param_name}  "
              f"(log_grid={log_grid})  "
              f"elapsed_total: {(time.time() - sweep_start)/60:.1f}m")
        print(f"=" * 70)
        ts = time.time()
        result = profile_param(
            param_name, best_x,
            g1=g1, g2=g2,
            n1_interp=n1, n2_interp=n2,
            t_fine_g1=tfg1, t_fine_g2=tfg2,
            n_points=11,
            span_factor=0.5,
            log_grid=log_grid,
            verbose=False,   # quiet for full sweep, summary printed below
        )
        elapsed = time.time() - ts

        out_path = out_dir / f"profile_{param_name}.json"
        out_path.write_text(json.dumps(result, indent=2, default=float))

        summary_records.append(dict(
            param_name=param_name,
            param_idx=result["param_idx"],
            baseline_value=result["baseline_value"],
            baseline_cost=result["baseline_cost"],
            cost_depth_abs=result["cost_depth_abs"],
            cost_depth_rel=result["cost_depth_rel"],
            ci_95=result["ci_95"],
            ci_width_relative=result["ci_width_relative"],
            classification=result["classification"],
            boundary_minimum=result["boundary_minimum"],
            grid_clipped_lo=result["grid_info"]["clipped_lo"],
            grid_clipped_hi=result["grid_info"]["clipped_hi"],
            elapsed_s=elapsed,
            log_grid=log_grid,
        ))

        # Brief progress line
        ci_str = f"[{result['ci_95'][0]:.4g}, {result['ci_95'][1]:.4g}]" if result['ci_95'] else "N/A"
        print(f"  {param_name:>5s}: baseline={result['baseline_value']:.4g}, "
              f"depth_rel={result['cost_depth_rel']:.4f}, "
              f"CI={ci_str}, "
              f"class={result['classification']}, "
              f"elapsed={elapsed:.0f}s")

    summary_path = out_dir / "full_summary.json"
    summary_path.write_text(json.dumps({
        "analysis": "09_profile_likelihood_full_sweep",
        "baseline_seed": 42,
        "n_points": 11,
        "span_factor": 0.5,
        "params": summary_records,
        "total_elapsed_s": time.time() - sweep_start,
    }, indent=2, default=float))

    # Print summary table
    print()
    print("=" * 100)
    print(f"{'param':>5s} | {'baseline':>10s} | {'depth':>8s} | "
          f"{'CI low':>10s} | {'CI hi':>10s} | {'CI/grid':>8s} | "
          f"{'classification':>40s}")
    print("-" * 100)
    for r in summary_records:
        ci_lo = f"{r['ci_95'][0]:.4g}" if r['ci_95'] else "N/A"
        ci_hi = f"{r['ci_95'][1]:.4g}" if r['ci_95'] else "N/A"
        ciw = f"{r['ci_width_relative']:.3f}" if r['ci_width_relative'] is not None else "N/A"
        depth = f"{r['cost_depth_rel']:.4f}" if r['cost_depth_rel'] is not None else "N/A"
        print(f"{r['param_name']:>5s} | {r['baseline_value']:>10.4g} | "
              f"{depth:>8s} | "
              f"{ci_lo:>10s} | {ci_hi:>10s} | {ciw:>8s} | "
              f"{r['classification']:>40s}")
    print()

    total = time.time() - sweep_start
    print(f"Full sweep completed in {total:.0f}s = {total/60:.1f}m = {total/3600:.2f}h")

    # Tally classifications
    from collections import Counter
    cls_counts = Counter(r["classification"] for r in summary_records)
    print()
    print("Classification tally:")
    for cls, n in cls_counts.most_common():
        print(f"  {n:>3d}  {cls}")


if __name__ == "__main__":
    main()
