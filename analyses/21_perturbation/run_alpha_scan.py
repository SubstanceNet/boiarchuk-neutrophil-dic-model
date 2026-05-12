"""
Sub-analysis 21a: deterministic α scan on N(t).

For α ∈ {0.8, 0.9, 1.0, 1.1, 1.2}, scale neutrophil counts in both groups
by α, rebuild interpolators, refit v13 model.

5 quick-mode fits, ~1 hour wall-clock.
"""
from __future__ import annotations
import json
import pickle
import time
from pathlib import Path
from dataclasses import replace
import numpy as np

from src import config as cfg
from src.cost_v13 import joint_cost_v13, joint_cost_v13_decomposed
from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids, solve_group

ANALYSIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ANALYSIS_DIR / "results/alpha_scan"
CACHE_DIR = ANALYSIS_DIR / "results/_cache"

ALPHAS = [0.8, 0.9, 1.0, 1.1, 1.2]
OBS_KEYS = ["recalc", "thrombin", "fib", "xiii", "AP", "D"]
OBS_FIELD = {"recalc": "recalc", "thrombin": "thrombin", "fib": "fib",
             "xiii": "xiii", "AP": "AP", "D": "deg"}


def fit_with_perturbed_N(g1_pert, g2_pert, seed=42):
    """Full quick-mode fit on perturbed N(t)."""
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
    print("=" * 70)
    print("Sub-analysis 21a: α-scan of N(t)")
    print(f"α values: {ALPHAS}")
    print("=" * 70)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    g1, g2 = load_data()
    sweep_start = time.time()
    summary = []

    for alpha in ALPHAS:
        cache_path = CACHE_DIR / f"alpha_{alpha:.2f}.pkl"
        if cache_path.exists():
            with cache_path.open("rb") as f:
                rec = pickle.load(f)
            cached = True
        else:
            t_iter = time.time()
            g1_pert = replace(g1, neutrophils=g1.neutrophils * alpha)
            g2_pert = replace(g2, neutrophils=g2.neutrophils * alpha)

            best_x, best_cost = fit_with_perturbed_N(g1_pert, g2_pert)

            # Compute predictions on ORIGINAL data (not perturbed)
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
                alpha=alpha,
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
            (RESULTS_DIR / f"fit_alpha_{alpha:.2f}.json").write_text(
                json.dumps(rec, indent=2, default=float))
            cached = False

        summary.append(rec)
        elapsed_total = (time.time() - sweep_start) / 60
        print(f"α={alpha:.2f}: cost={rec['best_cost']:.4f}, "
              f"R²_G1={rec['avg_r2_g1']:.3f}, R²_G2={rec['avg_r2_g2']:.3f} "
              f"({rec['elapsed_s']:.0f}s){' (CACHED)' if cached else ''}, "
              f"total={elapsed_total:.1f}m")

    (RESULTS_DIR / "summary.json").write_text(json.dumps({
        "sub_analysis": "21a_alpha_scan",
        "alphas": ALPHAS,
        "results": summary,
    }, indent=2, default=float))

    print()
    print(f"{'α':>5} | {'cost':>7} | {'R²_G1':>7} | {'R²_G2':>7}")
    for r in summary:
        print(f"{r['alpha']:>5.2f} | {r['best_cost']:>7.4f} | "
              f"{r['avg_r2_g1']:>+7.4f} | {r['avg_r2_g2']:>+7.4f}")
    print(f"\nTotal: {(time.time() - sweep_start)/60:.1f}m")


if __name__ == "__main__":
    main()
