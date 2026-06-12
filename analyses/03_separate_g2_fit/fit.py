"""
Analysis 03: Separate G2-only fit.

Bypasses src.fit.joint_cost. Constructs a G2-only cost function using
existing solve_group and r_squared from src. No modification to src/.
"""
from __future__ import annotations
import json
import time
import pickle
from pathlib import Path
import numpy as np
from scipy.optimize import differential_evolution, minimize

from src import config as cfg
from src.data import load_data, build_neutrophil_interpolators
from src.model import solve_group, make_fine_grids
from src.fit import r_squared

ANALYSIS_DIR = Path(__file__).resolve().parent
SEEDS = [42]


def g2_cost(pv, g2, n2_interp, t_fine_g2):
    """G2-only cost: sum of normalised RMSE across 6 observables.

    No G1 contribution. No mechanism-split constraint (it operates on
    G1 day 2). Hn-saturation penalty preserved as it's a numerical guard.
    """
    kr_g2 = pv[1] * pv[24]
    tp2_g2 = pv[8] * pv[25]
    try:
        o2 = solve_group(pv, g2.T, n2_interp, t_fine_g2, kr_g2, tp2_g2)
    except Exception:
        return cfg.COST_PENALTY_NAN
    keys = ("D", "AP", "recalc", "thrombin", "fib", "xiii")
    if any(np.any(np.isnan(o2[k])) for k in keys):
        return cfg.COST_PENALTY_NAN
    c = 0.0
    pairs = [
        ("recalc", g2.recalc), ("thrombin", g2.thrombin),
        ("fib", g2.fib), ("xiii", g2.xiii),
        ("AP", g2.AP), ("D", g2.deg),
    ]
    for k, d in pairs:
        m = o2[k][:len(d)]
        c += float(np.sqrt(np.mean(((m - d) / cfg.SC[k]) ** 2)))
    if np.any(o2["Hn"] > pv[7] * 0.99):
        c += cfg.HN_SATURATION_PENALTY
    return c


def cost_bounded(pv, *args):
    for i, (lo, hi) in enumerate(cfg.BOUNDS):
        if pv[i] < lo or pv[i] > hi:
            penalty = 1.0 + max(lo - pv[i], pv[i] - hi, 0.0) / (hi - lo)
            return cfg.COST_PENALTY_NAN * penalty
    return g2_cost(pv, *args)


def main():
    g1, g2 = load_data()
    _, n2_interp = build_neutrophil_interpolators(g1, g2)
    _, t_fine_g2 = make_fine_grids()
    args = (g2, n2_interp, t_fine_g2)

    print("=" * 65)
    print("Separate G2 fit (analysis 03)")
    print(f"  G2: {g2.n_datapoints} pts, 26 params")
    print(f"  Data/param: {g2.n_datapoints / 26:.2f}")
    print("=" * 65)

    best_x = None
    best_cost = cfg.COST_PENALTY_NAN
    t0 = time.time()

    for seed in SEEDS:
        print(f"--- DE seed={seed} ---", flush=True)
        ts = time.time()
        r = differential_evolution(
            g2_cost, cfg.BOUNDS, args=args,
            maxiter=120, popsize=8, seed=seed, tol=1e-7,
            workers=-1, mutation=(0.5, 1.5), recombination=0.85,
            disp=False, polish=False,
        )
        print(f"  cost={r.fun:.6f} ({time.time()-ts:.0f}s, {r.nfev} evals)", flush=True)
        if r.fun < best_cost:
            best_cost = float(r.fun)
            best_x = r.x.copy()
            print("  -> best", flush=True)

    print(f"\nBest DE: {best_cost:.6f}", flush=True)

    for method, opts in [
        ("Nelder-Mead", {"maxiter": 3000, "xatol": 1e-9, "fatol": 1e-10}),
        ("Powell",      {"maxiter": 2000, "ftol": 1e-10}),
        ("Nelder-Mead", {"maxiter": 3000, "xatol": 1e-10, "fatol": 1e-11}),
    ]:
        try:
            r = minimize(cost_bounded, best_x, args=args, method=method, options=opts)
            if np.isfinite(r.fun) and r.fun < best_cost:
                best_x = r.x.copy()
                best_cost = float(r.fun)
                print(f"  {method}: {r.fun:.6f} -> improved", flush=True)
            else:
                print(f"  {method}: {r.fun:.6f}", flush=True)
        except Exception as e:
            print(f"  {method}: failed ({e})", flush=True)

    o2 = solve_group(best_x, g2.T, n2_interp, t_fine_g2,
                     best_x[1] * best_x[24], best_x[8] * best_x[25])
    metrics = {}
    for k, d in [("recalc", g2.recalc), ("thrombin", g2.thrombin),
                 ("fib", g2.fib), ("xiii", g2.xiii),
                 ("AP", g2.AP), ("D", g2.deg)]:
        m = o2[k][:len(d)]
        metrics[k] = dict(R2=r_squared(m, d),
                          RMSE=float(np.sqrt(np.mean((m - d) ** 2))))
    avg_r2 = float(np.mean([v["R2"] for v in metrics.values()]))

    result = dict(
        analysis="03_separate_g2_fit",
        seeds=SEEDS,
        best_cost=best_cost,
        best_x=best_x.tolist(),
        params={n: float(best_x[i]) for i, n in enumerate(cfg.NAMES)},
        metrics_g2=metrics,
        avg_r2_g2=avg_r2,
        wall_time=time.time() - t0,
    )

    out = ANALYSIS_DIR / "results" / "fit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=float))

    print()
    print("=" * 65)
    print(f"Separate G2 R^2 (avg): {avg_r2:+.4f}")
    print("Per-observable G2 R^2:")
    for k, v in metrics.items():
        print(f"  {k:>10s}: R^2 = {v['R2']:+.4f}, RMSE = {v['RMSE']:.3f}")
    print()
    # NOTE: 0.6204 is the STALE v12 joint baseline (reference only, kept for
    # historical delta). The current v13 production joint baseline is 0.6920
    # (analyses/05_v13_baseline/results/fit.json avg_r2_g2). See S10.
    print("Comparison to joint-fit baseline (v12 reference 0.6204; v13 = 0.6920):")
    print("  joint  R^2_G2 avg:  +0.6204  [v12 reference, superseded]")
    print(f"  separate R^2_G2 avg: {avg_r2:+.4f}")
    print(f"  Δ = {avg_r2 - 0.6204:+.4f}")
    print()
    print(f"Saved -> {out}")


if __name__ == "__main__":
    main()
