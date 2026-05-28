"""
Multi-start diagnostic for kca profile.

For each grid point of kca (same grid as full sweep), run Nelder-Mead
from 5 starting points (1 baseline + 4 random uniform within bounds).
Take min cost across 5 starts.

Compare to single-start results to test whether profile likelihood
result for "flat" parameters is robust or artefactual.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

from src import config as cfg
from src.cost_v13 import joint_cost_v13
from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids
from src.profile_likelihood import _build_grid

ANALYSIS_DIR = Path(__file__).resolve().parent
PARAM = "kca"
N_STARTS = 5
N_POINTS = 11
SPAN_FACTOR = 0.5
LOG_GRID = True


def main():
    rng = np.random.default_rng(42)

    # Baseline
    baseline = json.loads(Path("analyses/05_v13_baseline/results/fit.json").read_text())
    best_x = np.array(baseline["best_x"])
    print(f"Loaded v13 baseline: cost={baseline['best_cost']:.6f}")

    # Single-start result for comparison
    single = json.loads(Path("analyses/09_profile_likelihood/results/profile_kca.json").read_text())

    g1, g2 = load_data()
    n1, n2 = build_neutrophil_interpolators(g1, g2)
    tfg1, tfg2 = make_fine_grids()

    idx = cfg.NAMES.index(PARAM)
    lo, hi = cfg.BOUNDS[idx]
    other_idxs = [j for j in range(len(cfg.NAMES)) if j != idx]
    other_bounds = [cfg.BOUNDS[j] for j in other_idxs]

    grid, grid_info = _build_grid(
        baseline=best_x[idx], lo=lo, hi=hi,
        n_points=N_POINTS, span_factor=SPAN_FACTOR, log_grid=LOG_GRID,
    )
    print(f"Grid for {PARAM}: {grid.round(4).tolist()}")
    print()

    def make_full_x(theta_other, theta_fixed):
        x = best_x.copy()
        x[other_idxs] = theta_other
        x[idx] = theta_fixed
        return x

    def cost_25dim(theta_other, theta_fixed):
        for k, (b_lo, b_hi) in enumerate(other_bounds):
            v = theta_other[k]
            if v < b_lo or v > b_hi:
                excess = max(b_lo - v, v - b_hi, 0.0) / (b_hi - b_lo)
                return cfg.COST_PENALTY_NAN * (1.0 + excess)
        full_x = make_full_x(theta_other, theta_fixed)
        return joint_cost_v13(full_x, g1, g2, n1, n2, tfg1, tfg2, (1.0, 1.0))

    # Generate 4 random starts (1st start is always baseline)
    random_starts = np.zeros((N_STARTS - 1, len(other_idxs)))
    for s in range(N_STARTS - 1):
        for k, (b_lo, b_hi) in enumerate(other_bounds):
            random_starts[s, k] = rng.uniform(b_lo, b_hi)

    # Run multi-start for each grid point
    results = []
    t_start = time.time()
    options = dict(maxiter=2000, xatol=1e-7, fatol=1e-9)

    for gi, theta_fixed in enumerate(grid):
        starts = [best_x[other_idxs].copy()] + [random_starts[s].copy() for s in range(N_STARTS - 1)]
        per_start_costs = []
        for s, x0 in enumerate(starts):
            try:
                r = minimize(cost_25dim, x0, args=(theta_fixed,),
                             method="Nelder-Mead", options=options)
                per_start_costs.append(float(r.fun))
            except Exception as e:
                per_start_costs.append(float("inf"))
                print(f"  start {s} failed: {e}")
        min_cost = min(per_start_costs)
        single_cost = single["profile_costs"][gi]
        delta = single_cost - min_cost  # positive: multistart found lower
        elapsed = time.time() - t_start
        print(f"  [{gi+1}/{N_POINTS}] kca={theta_fixed:.4f}: "
              f"single={single_cost:.6f}, "
              f"per-start={[f'{c:.4f}' for c in per_start_costs]}, "
              f"min={min_cost:.6f}, Δ={delta:+.6f}, "
              f"elapsed={elapsed:.0f}s")
        results.append(dict(
            grid_idx=gi,
            kca_value=float(theta_fixed),
            single_cost=single_cost,
            multistart_costs=per_start_costs,
            min_cost=min_cost,
            delta_vs_single=delta,
        ))

    out_path = ANALYSIS_DIR / "results" / "multistart_diagnostic_kca.json"
    out_path.write_text(json.dumps({
        "param": PARAM,
        "n_starts": N_STARTS,
        "n_points": N_POINTS,
        "results": results,
        "total_elapsed_s": time.time() - t_start,
    }, indent=2, default=float))

    print()
    print("=" * 80)
    print(f"Summary: kca multi-start diagnostic")
    deltas = [r["delta_vs_single"] for r in results]
    print(f"  Δ range: [{min(deltas):+.6f}, {max(deltas):+.6f}]")
    print(f"  max improvement of multistart over single: {max(deltas):.6f}")
    print(f"  median Δ: {np.median(deltas):.6f}")
    print()
    if max(deltas) < 0.005:
        print("  CONCLUSION: profile likelihood single-start is RELIABLE.")
        print("  Interpretation A confirmed: kca is genuinely sloppy.")
    elif max(deltas) < 0.05:
        print("  CONCLUSION: marginal differences. Need more diagnostics.")
    else:
        print("  CONCLUSION: single-start MISSES better optima.")
        print("  Interpretation B confirmed: full sweep needs multi-start.")
    print()
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
