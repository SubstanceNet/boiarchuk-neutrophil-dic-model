"""
LOO-CV: leave one timepoint out, refit, predict left-out observables.

Per LOO iteration:
- One timepoint t* removed from G1 or G2 (all 6 observables).
- Model refitted on reduced data.
- Predictions on t* compared to actual observed values via PRESS.
"""
from __future__ import annotations
import json
import time
import pickle
from pathlib import Path
from dataclasses import replace
import numpy as np

from src import config as cfg
from src.cost_v13 import joint_cost_v13
from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids, solve_group

ANALYSIS_DIR = Path(__file__).resolve().parent
OBS_KEYS = ["recalc", "thrombin", "fib", "xiii", "AP", "D"]

# Map our internal observable name -> data field name on GroupData
OBS_FIELD = {"recalc": "recalc", "thrombin": "thrombin", "fib": "fib",
             "xiii": "xiii", "AP": "AP", "D": "deg"}


def make_reduced_group(g, t_idx):
    """Return a GroupData with timepoint at index `t_idx` removed."""
    mask = np.ones(len(g.T), dtype=bool)
    mask[t_idx] = False

    def f(arr):
        return np.asarray(arr)[mask].copy()

    return replace(g,
        T=f(g.T),
        recalc=f(g.recalc),
        thrombin=f(g.thrombin),
        fib=f(g.fib),
        xiii=f(g.xiii),
        AP=f(g.AP),
        deg=f(g.deg),
        neutrophils=f(g.neutrophils),
    )


def fit_one(g1_used, g2_used, seed=42):
    """Quick-mode fit on reduced data."""
    from scipy.optimize import differential_evolution, minimize

    n1, n2 = build_neutrophil_interpolators(g1_used, g2_used)
    tfg1, tfg2 = make_fine_grids()
    cost_args = (g1_used, g2_used, n1, n2, tfg1, tfg2, (1.0, 1.0))

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
        ("Powell",      dict(maxiter=2000, ftol=1e-10)),
        ("Nelder-Mead", dict(maxiter=3000, xatol=1e-9, fatol=1e-11)),
    ]:
        r = minimize(cost_bounded, best_x, method=method, options=opts)
        if np.isfinite(r.fun) and r.fun < best_cost:
            best_x, best_cost = r.x.copy(), float(r.fun)
    return best_x, best_cost


def predict_at_timepoint(best_x, g_full, group_id, t_target_idx, n1_full, n2_full):
    """Use best_x to predict observables at t_target on the full G1/G2 timeline."""
    tfg1, tfg2 = make_fine_grids()
    pv = best_x[:26]
    if group_id == "G1":
        kr, tp2 = pv[1], pv[8]
        o = solve_group(pv, g_full.T, n1_full, tfg1, kr, tp2)
    else:
        kr, tp2 = pv[1] * pv[24], pv[8] * pv[25]
        o = solve_group(pv, g_full.T, n2_full, tfg2, kr, tp2)
    pred = {}
    for k in OBS_KEYS:
        pred[k] = float(o[k][t_target_idx])
    return pred


def main():
    print("=" * 70)
    print("LOO-CV: 15 G1 + 8 G2 = 23 LOO fits")
    print("=" * 70)

    g1, g2 = load_data()
    n1_full, n2_full = build_neutrophil_interpolators(g1, g2)
    tfg1, tfg2 = make_fine_grids()

    # Load baseline RMSE per observable per group (computed in analysis 10 sigmas)
    sigmas_path = Path("analyses/22_predictive_check/results/sigmas.json")
    if sigmas_path.exists():
        sigmas_data = json.loads(sigmas_path.read_text())
        rmse_g1 = sigmas_data["sigmas_g1"]
        rmse_g2 = sigmas_data["sigmas_g2"]
        print(f"Loaded baseline RMSEs from {sigmas_path}")
    else:
        # Fallback: compute on the fly
        baseline = json.loads(Path("analyses/05_v13_baseline/results/fit.json").read_text())
        best_x_baseline = np.array(baseline["best_x"])
        pv = best_x_baseline[:26]
        o1 = solve_group(pv, g1.T, n1_full, tfg1, pv[1], pv[8])
        o2 = solve_group(pv, g2.T, n2_full, tfg2, pv[1]*pv[24], pv[8]*pv[25])
        rmse_g1, rmse_g2 = {}, {}
        for k in OBS_KEYS:
            field = OBS_FIELD[k]
            d1 = getattr(g1, field)
            d2 = getattr(g2, field)
            rmse_g1[k] = float(np.sqrt(np.mean((o1[k][:len(d1)] - d1)**2)))
            rmse_g2[k] = float(np.sqrt(np.mean((o2[k][:len(d2)] - d2)**2)))
        print(f"Computed baseline RMSEs on the fly")

    out_dir = ANALYSIS_DIR / "results"
    cache_dir = out_dir / "_cache"
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # LOO targets: skip t=0 (anchor)
    g1_loo_targets = [(i, float(g1.T[i])) for i in range(1, len(g1.T))]
    g2_loo_targets = [(i, float(g2.T[i])) for i in range(1, len(g2.T))]
    all_targets = ([("G1", *t) for t in g1_loo_targets]
                 + [("G2", *t) for t in g2_loo_targets])

    print(f"Total LOO fits: {len(all_targets)}")
    print(f"  G1 targets (t_value): {[t[2] for t in all_targets if t[0]=='G1']}")
    print(f"  G2 targets (t_value): {[t[2] for t in all_targets if t[0]=='G2']}")
    print()

    sweep_start = time.time()
    summary = []

    for n_done, (group_id, t_idx, t_value) in enumerate(all_targets, start=1):
        cache_path = cache_dir / f"loo_{group_id}_t{t_value:g}.pkl"
        if cache_path.exists():
            with cache_path.open("rb") as f:
                rec = pickle.load(f)
            cached = True
        else:
            t_iter_start = time.time()
            try:
                if group_id == "G1":
                    g1_used = make_reduced_group(g1, t_idx)
                    g2_used = g2
                else:
                    g1_used = g1
                    g2_used = make_reduced_group(g2, t_idx)

                best_x, best_cost = fit_one(g1_used, g2_used, seed=42)

                # Predict at left-out timepoint using full timeline
                pred = predict_at_timepoint(
                    best_x,
                    g1 if group_id == "G1" else g2,
                    group_id, t_idx,
                    n1_full, n2_full,
                )

                # Actual values at left-out timepoint
                full_g = g1 if group_id == "G1" else g2
                actual = {k: float(getattr(full_g, OBS_FIELD[k])[t_idx]) for k in OBS_KEYS}

                # PRESS contribution per observable
                rmse = rmse_g1 if group_id == "G1" else rmse_g2
                press_per_obs = {
                    k: ((pred[k] - actual[k]) / rmse[k]) ** 2 for k in OBS_KEYS
                }

                rec = dict(
                    group=group_id,
                    t_value=t_value,
                    t_idx=t_idx,
                    best_cost=best_cost,
                    best_x=best_x.tolist(),
                    pred=pred,
                    actual=actual,
                    press_per_obs=press_per_obs,
                    elapsed_s=time.time() - t_iter_start,
                    failed=False,
                )
            except Exception as e:
                rec = dict(group=group_id, t_value=t_value, t_idx=t_idx,
                           failed=True, error=str(e),
                           elapsed_s=time.time() - t_iter_start)
                print(f"  LOO {group_id} t={t_value} FAILED: {e}")

            with cache_path.open("wb") as f:
                pickle.dump(rec, f)
            cached = False

        summary.append(rec)
        elapsed_total = (time.time() - sweep_start) / 60
        eta_min = (elapsed_total / n_done) * (len(all_targets) - n_done) if n_done > 0 else 0

        if not rec.get("failed"):
            press_total = sum(rec["press_per_obs"].values())
            print(f"[{n_done:>2}/{len(all_targets)}] {group_id} t={t_value:5.1f} "
                  f"cost={rec['best_cost']:.4f} PRESS={press_total:.3f} "
                  f"({rec['elapsed_s']:.0f}s){' (CACHED)' if cached else ''}, "
                  f"total={elapsed_total:.1f}m ETA={eta_min:.1f}m")
        else:
            print(f"[{n_done:>2}/{len(all_targets)}] {group_id} t={t_value:5.1f} FAILED, "
                  f"total={elapsed_total:.1f}m")

        # Save individual JSON
        if not rec.get("failed"):
            jsonpath = out_dir / f"loo_{group_id}_t{t_value:g}.json"
            jsonpath.write_text(json.dumps(rec, indent=2, default=float))

    # Aggregated summary
    aggregated = []
    for rec in summary:
        if not rec.get("failed"):
            aggregated.append(dict(
                group=rec["group"],
                t_value=rec["t_value"],
                cost=rec["best_cost"],
                press_total=sum(rec["press_per_obs"].values()),
                press_per_obs=rec["press_per_obs"],
                pred=rec["pred"],
                actual=rec["actual"],
            ))

    summary_path = out_dir / "summary.json"
    summary_path.write_text(json.dumps({
        "analysis": "20_loo_timepoint",
        "rmse_baseline_g1": rmse_g1,
        "rmse_baseline_g2": rmse_g2,
        "results": aggregated,
        "total_elapsed_s": time.time() - sweep_start,
    }, indent=2, default=float))

    # Print summary table
    print()
    print("=" * 90)
    print(f"{'group':>5} | {'t':>5} | {'cost':>7} | {'PRESS':>8} | "
          + " | ".join([f"{k:>7}" for k in OBS_KEYS]))
    print("-" * 90)
    for r in aggregated:
        per = r["press_per_obs"]
        print(f"{r['group']:>5} | {r['t_value']:>5.1f} | {r['cost']:>7.4f} | "
              f"{r['press_total']:>8.3f} | "
              + " | ".join([f"{per[k]:>7.3f}" for k in OBS_KEYS]))

    total = (time.time() - sweep_start) / 3600
    print(f"\nTotal: {total:.2f}h, {len([r for r in summary if not r.get('failed')])} OK, "
          f"{len([r for r in summary if r.get('failed')])} failed")


if __name__ == "__main__":
    main()
