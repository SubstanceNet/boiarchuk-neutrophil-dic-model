"""
Aggregate bootstrap ensemble (100 iters) into:
  - Per-parameter CI 95 (2.5/97.5 percentiles) + median + spread metrics
  - Per-prediction CI 95 on observable trajectories
  - Per-observable R² distribution
  - Cost distribution
  - Mechanism split fractions CI
  - Convergence check (N=50 vs N=100 CI width)
  - Comparison to profile likelihood CI (from analysis 09)
"""
from __future__ import annotations
import json
import pickle
from pathlib import Path
import numpy as np

from src import config as cfg
from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids, solve_group

ANALYSIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ANALYSIS_DIR / "results"
CACHE_DIR = RESULTS_DIR / "_cache"
OBS_KEYS = ["recalc", "thrombin", "fib", "xiii", "AP", "D"]
OBS_FIELD = {"recalc": "recalc", "thrombin": "thrombin", "fib": "fib",
             "xiii": "xiii", "AP": "AP", "D": "deg"}


def load_ensemble():
    """Load all iteration records from cache."""
    iters = []
    for p in sorted(CACHE_DIR.glob("iter_*.pkl")):
        with p.open("rb") as f:
            rec = pickle.load(f)
        if not rec.get("failed"):
            iters.append(rec)
    return iters


def r2(pred, obs):
    """Coefficient of determination."""
    ss_res = np.sum((pred - obs) ** 2)
    ss_tot = np.sum((obs - obs.mean()) ** 2)
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan


def compute_per_iter_r2(iters, g1, g2):
    """For each iter, compute R² per observable per group."""
    r2_records = []
    for rec in iters:
        g1_pred = rec["g1_predictions"]
        g2_pred = rec["g2_predictions"]
        r2_g1, r2_g2 = {}, {}
        for k in OBS_KEYS:
            obs1 = getattr(g1, OBS_FIELD[k])
            obs2 = getattr(g2, OBS_FIELD[k])
            r2_g1[k] = r2(np.array(g1_pred[k]), obs1)
            r2_g2[k] = r2(np.array(g2_pred[k]), obs2)
        r2_records.append(dict(seed=rec["seed"], r2_g1=r2_g1, r2_g2=r2_g2))
    return r2_records


def percentiles(values, pcts=(2.5, 50.0, 97.5)):
    arr = np.asarray(values)
    arr = arr[np.isfinite(arr)]
    if len(arr) == 0:
        return None
    return {f"p{p}": float(np.percentile(arr, p)) for p in pcts}


def main():
    print("=" * 70)
    print("Aggregating bootstrap ensemble")
    print("=" * 70)

    iters = load_ensemble()
    print(f"Loaded {len(iters)} bootstrap iterations from cache")
    print()

    g1, g2 = load_data()

    # --- Parameter CI ---
    print("Computing per-parameter CI...")
    best_x_matrix = np.array([rec["best_x"] for rec in iters])  # (n_iters, 26)
    param_ci = {}
    for i, name in enumerate(cfg.NAMES):
        values = best_x_matrix[:, i]
        pcts = percentiles(values)
        param_ci[name] = dict(
            **pcts,
            mean=float(np.mean(values)),
            std=float(np.std(values)),
            min=float(values.min()),
            max=float(values.max()),
            n=int(len(values)),
        )

    # --- Cost distribution ---
    costs = np.array([rec["best_cost"] for rec in iters])
    cost_summary = dict(
        **percentiles(costs),
        mean=float(np.mean(costs)),
        std=float(np.std(costs)),
        min=float(costs.min()),
        max=float(costs.max()),
    )
    print(f"Cost ensemble: mean={cost_summary['mean']:.4f}, "
          f"CI95=[{cost_summary['p2.5']:.4f}, {cost_summary['p97.5']:.4f}]")

    # --- Per-iter R² ---
    print("Computing per-iter R²...")
    r2_records = compute_per_iter_r2(iters, g1, g2)
    r2_g1_dist = {k: percentiles([r["r2_g1"][k] for r in r2_records]) for k in OBS_KEYS}
    r2_g2_dist = {k: percentiles([r["r2_g2"][k] for r in r2_records]) for k in OBS_KEYS}

    print("\nR² per observable (G1):")
    print(f"  {'observable':>10s} | {'p2.5':>7} | {'median':>7} | {'p97.5':>7}")
    for k in OBS_KEYS:
        d = r2_g1_dist[k]
        print(f"  {k:>10s} | {d['p2.5']:>7.4f} | {d['p50.0']:>7.4f} | {d['p97.5']:>7.4f}")
    print("\nR² per observable (G2):")
    print(f"  {'observable':>10s} | {'p2.5':>7} | {'median':>7} | {'p97.5':>7}")
    for k in OBS_KEYS:
        d = r2_g2_dist[k]
        print(f"  {k:>10s} | {d['p2.5']:>7.4f} | {d['p50.0']:>7.4f} | {d['p97.5']:>7.4f}")

    # --- Prediction CI per timepoint per observable ---
    print("\nComputing per-timepoint prediction CI...")
    g1_pred_arr = {k: np.array([rec["g1_predictions"][k] for rec in iters]) for k in OBS_KEYS}
    g2_pred_arr = {k: np.array([rec["g2_predictions"][k] for rec in iters]) for k in OBS_KEYS}
    g1_pred_ci = {k: dict(
        median=np.median(g1_pred_arr[k], axis=0).tolist(),
        p2_5=np.percentile(g1_pred_arr[k], 2.5, axis=0).tolist(),
        p97_5=np.percentile(g1_pred_arr[k], 97.5, axis=0).tolist(),
    ) for k in OBS_KEYS}
    g2_pred_ci = {k: dict(
        median=np.median(g2_pred_arr[k], axis=0).tolist(),
        p2_5=np.percentile(g2_pred_arr[k], 2.5, axis=0).tolist(),
        p97_5=np.percentile(g2_pred_arr[k], 97.5, axis=0).tolist(),
    ) for k in OBS_KEYS}

    # --- Mechanism split (G1 day 2) ---
    # neutrophil fraction for recalc, fib, xiii at day index 2
    print("\nMechanism split (G1 day 2) ensemble:")
    n1, n2 = build_neutrophil_interpolators(g1, g2)
    tfg1, tfg2 = make_fine_grids()
    splits = []
    for rec in iters:
        pv = np.array(rec["best_x"])[:26]
        o1 = solve_group(pv, g1.T, n1, tfg1, pv[1], pv[8])
        idx2 = 2
        V2, AP2, Nr2 = o1["V"][idx2], o1["AP"][idx2], o1["Nr"][idx2]
        if V2 < 1e-6 or AP2 < 1e-6:
            continue
        vr, nr = pv[11] * V2, pv[12] * AP2
        vf, nf = pv[16] * V2, pv[17] * AP2
        vx, nx = pv[20] * V2, pv[21] * AP2 * Nr2
        splits.append(dict(
            recalc=nr / (vr + nr) if (vr+nr) > 0 else None,
            fib=nf / (vf + nf) if (vf+nf) > 0 else None,
            xiii=nx / (vx + nx) if (vx+nx) > 0 else None,
        ))
    split_ci = {}
    for k in ("recalc", "fib", "xiii"):
        vals = [s[k] for s in splits if s[k] is not None]
        split_ci[k] = percentiles(vals) if vals else None
        if split_ci[k]:
            d = split_ci[k]
            print(f"  {k:>7}: median={d['p50.0']:.3f}, CI95=[{d['p2.5']:.3f}, {d['p97.5']:.3f}]")

    # --- Convergence check: N=50 vs N=100 ---
    print("\nConvergence check (N=50 first half vs N=100):")
    half = len(iters) // 2
    iters_half = iters[:half]
    half_param_ci = {}
    for i, name in enumerate(cfg.NAMES):
        values_half = np.array([rec["best_x"][i] for rec in iters_half])
        half_param_ci[name] = percentiles(values_half)

    width_change = []
    for name in cfg.NAMES:
        full_w = param_ci[name]["p97.5"] - param_ci[name]["p2.5"]
        half_w = half_param_ci[name]["p97.5"] - half_param_ci[name]["p2.5"]
        if full_w > 0:
            change = (full_w - half_w) / full_w
            width_change.append((name, change, full_w, half_w))
    avg_change = np.mean([abs(c[1]) for c in width_change])
    max_change = max(width_change, key=lambda x: abs(x[1]))
    print(f"  Avg |Δ width|: {avg_change*100:.1f}%")
    print(f"  Max change: {max_change[0]} ({max_change[1]*100:+.1f}%)")
    converged = avg_change < 0.10  # less than 10% width change
    print(f"  Converged: {'YES' if converged else 'NO (consider more iters)'}")

    # --- Compare to profile likelihood CI ---
    print("\nComparison to profile likelihood CI (from analysis 09):")
    pl_summary_path = Path("analyses/09_profile_likelihood/results/full_summary.json")
    if pl_summary_path.exists():
        pl = json.loads(pl_summary_path.read_text())
        pl_by_name = {p["param_name"]: p for p in pl["params"]}
        print(f"  {'param':>5} | {'bootstrap p2.5':>14} | {'bootstrap p97.5':>15} | "
              f"{'PL CI lo':>10} | {'PL CI hi':>10}")
        for name in cfg.NAMES:
            bs = param_ci[name]
            pl_p = pl_by_name.get(name, {})
            pl_ci = pl_p.get("ci_95")
            pl_lo = f"{pl_ci[0]:.4g}" if pl_ci else "N/A"
            pl_hi = f"{pl_ci[1]:.4g}" if pl_ci else "N/A"
            print(f"  {name:>5} | {bs['p2.5']:>14.4g} | {bs['p97.5']:>15.4g} | "
                  f"{pl_lo:>10} | {pl_hi:>10}")
    else:
        print("  No profile likelihood summary found.")

    # --- Save ---
    out = dict(
        analysis="10_bootstrap_aggregated",
        n_iters=len(iters),
        cost=cost_summary,
        param_ci=param_ci,
        r2_g1=r2_g1_dist,
        r2_g2=r2_g2_dist,
        g1_pred_ci=g1_pred_ci,
        g2_pred_ci=g2_pred_ci,
        mechanism_split=split_ci,
        convergence=dict(
            avg_width_change=avg_change,
            max_change_param=max_change[0],
            max_change_value=float(max_change[1]),
            converged=converged,
        ),
    )
    out_path = RESULTS_DIR / "ensemble.json"
    out_path.write_text(json.dumps(out, indent=2, default=float))
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
