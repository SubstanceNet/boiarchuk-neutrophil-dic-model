"""
Parametric bootstrap of v13 baseline.

100 iterations. Each iteration: sample synthetic data from baseline
predictions + Gaussian noise (sigma = baseline RMSE per-group per-observable),
refit using full quick-mode pipeline, save result.

Outputs ensemble of 100 best_x with CI on parameters and predictions.
"""
from __future__ import annotations
import json
import time
import hashlib
import pickle
from pathlib import Path
from dataclasses import replace
import numpy as np

from src import config as cfg
from src.cost_v13 import joint_cost_v13, joint_cost_v13_decomposed
from src.data import load_data, build_neutrophil_interpolators, GroupData
from src.model import make_fine_grids, solve_group
from src.fit_runner import run_with_overrides

ANALYSIS_DIR = Path(__file__).resolve().parent
N_ITERS = 100


def compute_baseline_predictions_and_sigmas():
    """Compute baseline model predictions on observed timepoints
    and per-group per-observable RMSE sigmas."""
    baseline = json.loads(Path("analyses/05_v13_baseline/results/fit.json").read_text())
    best_x = np.array(baseline["best_x"])

    g1, g2 = load_data()
    n1, n2 = build_neutrophil_interpolators(g1, g2)
    tfg1, tfg2 = make_fine_grids()

    pv = best_x[:26]
    kr_g1, tp2_g1 = pv[1], pv[8]
    kr_g2, tp2_g2 = pv[1] * pv[24], pv[8] * pv[25]

    o1 = solve_group(pv, g1.T, n1, tfg1, kr_g1, tp2_g1)
    o2 = solve_group(pv, g2.T, n2, tfg2, kr_g2, tp2_g2)

    obs_keys = ["recalc", "thrombin", "fib", "xiii", "AP", "D"]
    g1_data = {"recalc": g1.recalc, "thrombin": g1.thrombin, "fib": g1.fib,
               "xiii": g1.xiii, "AP": g1.AP, "D": g1.deg}
    g2_data = {"recalc": g2.recalc, "thrombin": g2.thrombin, "fib": g2.fib,
               "xiii": g2.xiii, "AP": g2.AP, "D": g2.deg}

    sigmas = {}
    g1_pred, g2_pred = {}, {}
    for k in obs_keys:
        m1 = o1[k][:len(g1_data[k])]
        m2 = o2[k][:len(g2_data[k])]
        sigmas[k] = (
            float(np.sqrt(np.mean((m1 - g1_data[k])**2))),
            float(np.sqrt(np.mean((m2 - g2_data[k])**2))),
        )
        g1_pred[k] = m1.copy()
        g2_pred[k] = m2.copy()

    return best_x, g1_pred, g2_pred, sigmas, g1, g2


def make_synthetic_groups(g1, g2, g1_pred, g2_pred, sigmas, seed):
    """Generate synthetic G1+G2 data: prediction + Gaussian noise."""
    rng = np.random.default_rng(seed)
    obs_keys = ["recalc", "thrombin", "fib", "xiii", "AP", "D"]

    def synth(pred_dict, real_data, sigma_idx):
        out = {}
        for k in obs_keys:
            sigma = sigmas[k][sigma_idx]
            out[k] = pred_dict[k] + rng.normal(0.0, sigma, size=len(pred_dict[k]))
        return out

    g1_synth = synth(g1_pred, g1, 0)
    g2_synth = synth(g2_pred, g2, 1)

    # Build new GroupData objects with synthetic observables
    g1_new = replace(g1,
        recalc=g1_synth["recalc"], thrombin=g1_synth["thrombin"],
        fib=g1_synth["fib"], xiii=g1_synth["xiii"],
        AP=g1_synth["AP"], deg=g1_synth["D"])
    g2_new = replace(g2,
        recalc=g2_synth["recalc"], thrombin=g2_synth["thrombin"],
        fib=g2_synth["fib"], xiii=g2_synth["xiii"],
        AP=g2_synth["AP"], deg=g2_synth["D"])
    return g1_new, g2_new


def fit_one_iteration(g1_synth, g2_synth, baseline_x, seed, verbose=False):
    """Fit v13 on synthetic data using quick-mode pipeline."""
    from scipy.optimize import differential_evolution, minimize
    from src.cost_v13 import joint_cost_v13

    n1_synth, n2_synth = build_neutrophil_interpolators(g1_synth, g2_synth)
    tfg1, tfg2 = make_fine_grids()

    cost_args = (g1_synth, g2_synth, n1_synth, n2_synth, tfg1, tfg2, (1.0, 1.0))

    def cost_bounded(pv):
        for i, (lo, hi) in enumerate(cfg.BOUNDS):
            if pv[i] < lo or pv[i] > hi:
                excess = max(lo - pv[i], pv[i] - hi, 0.0) / (hi - lo)
                return cfg.COST_PENALTY_NAN * (1.0 + excess)
        return joint_cost_v13(pv, *cost_args)

    # quick-mode DE
    de = differential_evolution(
        joint_cost_v13, cfg.BOUNDS, args=cost_args,
        maxiter=200, popsize=15, seed=seed, tol=1e-7,
        workers=-1, mutation=(0.5, 1.5), recombination=0.85,
        disp=False, polish=False, init='sobol',
    )
    best_x = de.x.copy()
    best_cost = float(de.fun)

    # Nelder-Mead refinement
    nm = minimize(cost_bounded, best_x, method="Nelder-Mead",
                  options=dict(maxiter=3000, xatol=1e-8, fatol=1e-10))
    if np.isfinite(nm.fun) and nm.fun < best_cost:
        best_x = nm.x.copy()
        best_cost = float(nm.fun)

    # Powell refinement
    pw = minimize(cost_bounded, best_x, method="Powell",
                  options=dict(maxiter=2000, ftol=1e-10))
    if np.isfinite(pw.fun) and pw.fun < best_cost:
        best_x = pw.x.copy()
        best_cost = float(pw.fun)

    # Final NM
    nm2 = minimize(cost_bounded, best_x, method="Nelder-Mead",
                   options=dict(maxiter=3000, xatol=1e-9, fatol=1e-11))
    if np.isfinite(nm2.fun) and nm2.fun < best_cost:
        best_x = nm2.x.copy()
        best_cost = float(nm2.fun)

    return best_x, best_cost


def main():
    print("=" * 70)
    print("Analysis 10 — Parametric bootstrap (N=100, v13 baseline)")
    print("=" * 70)

    out_dir = ANALYSIS_DIR / "results"
    cache_dir = out_dir / "_cache"
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    print("\nComputing baseline predictions and sigmas...")
    baseline_x, g1_pred, g2_pred, sigmas, g1, g2 = compute_baseline_predictions_and_sigmas()
    print(f"  baseline_x shape: {baseline_x.shape}")
    print(f"  sigmas: {sigmas}")

    (out_dir / "sigmas.json").write_text(json.dumps({
        "obs_keys": list(sigmas.keys()),
        "sigmas_g1": {k: v[0] for k, v in sigmas.items()},
        "sigmas_g2": {k: v[1] for k, v in sigmas.items()},
    }, indent=2))
    print(f"  saved: {out_dir / 'sigmas.json'}")

    sweep_start = time.time()
    iter_records = []

    for i in range(1, N_ITERS + 1):
        seed = i
        t_iter_start = time.time()

        cache_path = cache_dir / f"iter_{seed:03d}.pkl"
        if cache_path.exists():
            with cache_path.open("rb") as f:
                rec = pickle.load(f)
            cached = True
        else:
            try:
                g1_synth, g2_synth = make_synthetic_groups(g1, g2, g1_pred, g2_pred, sigmas, seed)
                best_x, best_cost = fit_one_iteration(g1_synth, g2_synth, baseline_x, seed)

                # Compute decomposition on synthetic data
                n1s, n2s = build_neutrophil_interpolators(g1_synth, g2_synth)
                tfg1, tfg2 = make_fine_grids()
                decomp = joint_cost_v13_decomposed(
                    best_x, g1_synth, g2_synth, n1s, n2s, tfg1, tfg2)

                # Compute predictions on REAL timepoints (for prediction CI later)
                pv = best_x[:26]
                kr_g1, tp2_g1 = pv[1], pv[8]
                kr_g2, tp2_g2 = pv[1] * pv[24], pv[8] * pv[25]
                n1, n2 = build_neutrophil_interpolators(g1, g2)
                o1_real = solve_group(pv, g1.T, n1, tfg1, kr_g1, tp2_g1)
                o2_real = solve_group(pv, g2.T, n2, tfg2, kr_g2, tp2_g2)

                rec = dict(
                    seed=seed,
                    best_x=best_x.tolist(),
                    best_cost=best_cost,
                    decomp_synth=decomp,
                    g1_predictions={k: o1_real[k][:len(getattr(g1, "deg" if k=="D" else k))].tolist()
                                    for k in ["recalc", "thrombin", "fib", "xiii", "AP", "D"]},
                    g2_predictions={k: o2_real[k][:len(getattr(g2, "deg" if k=="D" else k))].tolist()
                                    for k in ["recalc", "thrombin", "fib", "xiii", "AP", "D"]},
                    elapsed_s=time.time() - t_iter_start,
                    failed=False,
                )
            except Exception as e:
                rec = dict(seed=seed, failed=True, error=str(e),
                           elapsed_s=time.time() - t_iter_start)
                print(f"  ITER {seed} FAILED: {e}")

            with cache_path.open("wb") as f:
                pickle.dump(rec, f)
            cached = False

        iter_records.append(rec)
        elapsed_total = (time.time() - sweep_start) / 60
        eta_min = (elapsed_total / i) * (N_ITERS - i) if i > 0 else 0

        cache_str = " (CACHED)" if cached else ""
        if not rec.get("failed"):
            print(f"[{i:>3d}/{N_ITERS}] seed={seed} cost={rec['best_cost']:.4f} "
                  f"({rec['elapsed_s']:.0f}s){cache_str}, "
                  f"total={elapsed_total:.1f}m, ETA={eta_min:.1f}m")
        else:
            print(f"[{i:>3d}/{N_ITERS}] seed={seed} FAILED, "
                  f"total={elapsed_total:.1f}m, ETA={eta_min:.1f}m")

        # Save individual JSON
        if not rec.get("failed"):
            iter_path = out_dir / f"iter_{seed:03d}.json"
            iter_path.write_text(json.dumps(rec, indent=2, default=float))

    # Save raw ensemble
    raw_path = out_dir / "ensemble_raw.json"
    raw_path.write_text(json.dumps({
        "n_iters": N_ITERS,
        "iter_records": iter_records,
        "total_elapsed_s": time.time() - sweep_start,
    }, indent=2, default=float))

    print(f"\n=== Bootstrap complete in {(time.time() - sweep_start)/3600:.2f}h ===")
    print(f"Saved: {raw_path}")
    print()
    print("Run aggregation script next:")
    print("  python -m analyses.22_predictive_check.aggregate")


if __name__ == "__main__":
    main()
