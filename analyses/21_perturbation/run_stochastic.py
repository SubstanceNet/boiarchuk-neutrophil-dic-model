"""
Sub-analysis 21b/c: stochastic perturbation of N(t).

For each iteration: apply lognormal noise to N(t) per timepoint,
rebuild interpolators, refit v13 model.

Usage:
    python -m analyses.21_perturbation.run_stochastic --sigma 10
    python -m analyses.21_perturbation.run_stochastic --sigma 20

N=20 iterations per sigma. ~4.7 hours per sub-analysis.
"""
from __future__ import annotations
import argparse
import json
import pickle
import time
from pathlib import Path
from dataclasses import replace
import numpy as np

from src import config as cfg
from src.cost_v13 import joint_cost_v13
from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids, solve_group

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR_BASE = ANALYSIS_DIR / "results/_cache"

N_ITERS = 20
OBS_KEYS = ["recalc", "thrombin", "fib", "xiii", "AP", "D"]
OBS_FIELD = {"recalc": "recalc", "thrombin": "thrombin", "fib": "fib",
             "xiii": "xiii", "AP": "AP", "D": "deg"}


def make_perturbed_groups(g1, g2, sigma_log, seed):
    """Apply lognormal noise to neutrophil counts."""
    rng = np.random.default_rng(seed)
    z1 = rng.normal(0.0, sigma_log, size=len(g1.neutrophils))
    z2 = rng.normal(0.0, sigma_log, size=len(g2.neutrophils))
    n1_pert = g1.neutrophils * np.exp(z1)
    n2_pert = g2.neutrophils * np.exp(z2)
    g1_pert = replace(g1, neutrophils=n1_pert)
    g2_pert = replace(g2, neutrophils=n2_pert)
    return g1_pert, g2_pert


def fit_one(g1_pert, g2_pert, seed):
    """Quick-mode fit on perturbed N(t)."""
    from scipy.optimize import differential_evolution, minimize
    n1, n2 = build_neutrophil_interpolators(g1_pert, g2_pert)
    tfg1, tfg2 = make_fine_grids()
    cost_args = (g1_pert, g2_pert, n1, n2, tfg1, tfg2, (1.0, 1.0))

    def cost_bounded(pv):
        for i, (lo, hi) in enumerate(cfg.BOUNDS):
            if pv[i] < lo or pv[i] > hi:
                excess = max(lo - pv[i], pv[i] - hi, 0.0) / (hi - lo)
                return cfg.COST_PENALTY_NAN * (1.0 + excess)
        return joint_cost_v13(pv, *cost_args)

    de = differential_evolution(
        joint_cost_v13, cfg.BOUNDS, args=cost_args,
        maxiter=200, popsize=15, seed=seed, tol=1e-7,
        workers=-1, mutation=(0.5, 1.5), recombination=0.85,
        disp=False, polish=False, init='sobol',
    )
    best_x, best_cost = de.x.copy(), float(de.fun)

    for method, opts in [
        ("Nelder-Mead", dict(maxiter=3000, xatol=1e-8, fatol=1e-10)),
        ("Powell", dict(maxiter=2000, ftol=1e-10)),
        ("Nelder-Mead", dict(maxiter=3000, xatol=1e-9, fatol=1e-11)),
    ]:
        r = minimize(cost_bounded, best_x, method=method, options=opts)
        if np.isfinite(r.fun) and r.fun < best_cost:
            best_x, best_cost = r.x.copy(), float(r.fun)
    return best_x, best_cost


def r2(pred, obs):
    pred, obs = np.asarray(pred), np.asarray(obs)
    ss_res = np.sum((pred - obs) ** 2)
    ss_tot = np.sum((obs - obs.mean()) ** 2)
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sigma", type=int, required=True, choices=[10, 20],
                    help="CV percent for lognormal noise (10 or 20)")
    args = ap.parse_args()

    sigma_pct = args.sigma
    sigma_log = float(np.log(1.0 + sigma_pct / 100.0))
    sub_label = f"stochastic_{sigma_pct}"
    results_dir = ANALYSIS_DIR / "results" / sub_label
    cache_dir = CACHE_DIR_BASE / sub_label

    print("=" * 70)
    print(f"Sub-analysis 21{'b' if sigma_pct == 10 else 'c'}: stochastic σ={sigma_pct}%")
    print(f"  CV: {sigma_pct}% → σ_log = ln(1.{sigma_pct:02d}) ≈ {sigma_log:.4f}")
    print(f"  N iterations: {N_ITERS}")
    print("=" * 70)

    results_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    g1, g2 = load_data()
    sweep_start = time.time()
    results = []

    for i in range(1, N_ITERS + 1):
        seed = i
        cache_path = cache_dir / f"iter_{seed:03d}.pkl"
        if cache_path.exists():
            with cache_path.open("rb") as f:
                rec = pickle.load(f)
            cached = True
        else:
            t_iter = time.time()
            g1_pert, g2_pert = make_perturbed_groups(g1, g2, sigma_log, seed)
            best_x, best_cost = fit_one(g1_pert, g2_pert, seed)

            n1, n2 = build_neutrophil_interpolators(g1_pert, g2_pert)
            tfg1, tfg2 = make_fine_grids()
            pv = best_x[:26]
            o1 = solve_group(pv, g1.T, n1, tfg1, pv[1], pv[8])
            o2 = solve_group(pv, g2.T, n2, tfg2, pv[1]*pv[24], pv[8]*pv[25])

            r2_g1 = {k: r2(o1[k][:len(getattr(g1, OBS_FIELD[k]))],
                           getattr(g1, OBS_FIELD[k])) for k in OBS_KEYS}
            r2_g2 = {k: r2(o2[k][:len(getattr(g2, OBS_FIELD[k]))],
                           getattr(g2, OBS_FIELD[k])) for k in OBS_KEYS}

            rec = dict(
                seed=seed,
                sigma_pct=sigma_pct,
                best_x=best_x.tolist(),
                best_cost=best_cost,
                r2_g1=r2_g1,
                r2_g2=r2_g2,
                avg_r2_g1=float(np.mean(list(r2_g1.values()))),
                avg_r2_g2=float(np.mean(list(r2_g2.values()))),
                elapsed_s=time.time() - t_iter,
            )
            with cache_path.open("wb") as f:
                pickle.dump(rec, f)
            (results_dir / f"iter_{seed:03d}.json").write_text(
                json.dumps(rec, indent=2, default=float))
            cached = False

        results.append(rec)
        elapsed_total = (time.time() - sweep_start) / 60
        eta = (elapsed_total / i) * (N_ITERS - i) if i > 0 else 0
        print(f"[{i:>2}/{N_ITERS}] seed={seed} cost={rec['best_cost']:.4f} "
              f"R²_G1={rec['avg_r2_g1']:.3f} R²_G2={rec['avg_r2_g2']:.3f} "
              f"({rec['elapsed_s']:.0f}s){' (CACHED)' if cached else ''}, "
              f"total={elapsed_total:.1f}m ETA={eta:.1f}m")

    # Save summary
    (results_dir / "summary.json").write_text(json.dumps({
        "sub_analysis": f"21{'b' if sigma_pct == 10 else 'c'}_stochastic",
        "sigma_pct": sigma_pct,
        "sigma_log": sigma_log,
        "n_iters": N_ITERS,
        "results": results,
        "total_elapsed_s": time.time() - sweep_start,
    }, indent=2, default=float))

    print(f"\nTotal: {(time.time() - sweep_start)/3600:.2f}h")


if __name__ == "__main__":
    main()
