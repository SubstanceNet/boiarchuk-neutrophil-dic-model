"""Sensitivity check: per-group-std normalization vs range-based v12 SC.

Tests the colleague's hypothesis that the single range-based SC[xiii]=150
(driven by the larger G1 excursion) under-weights G2 XIII by ~24x, inflating
the 41% R2<0 rate. Per-group-std uses separate SC per group = std of that
group's observable.

Does NOT modify src/. Self-contained cost with group-specific SC. One seed
(quick mode) for a first read; seed-stability decided after.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
import numpy as np
from scipy.optimize import differential_evolution, minimize

from src import config as cfg
from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids, solve_group

OBS = [("recalc", "recalc"), ("thrombin", "thrombin"), ("fib", "fib"),
       ("xiii", "xiii"), ("AP", "AP"), ("D", "deg")]
SEED = 42


def per_group_std_sc(g):
    """SC = std of each observable for this group (floored to avoid /0)."""
    return {k: max(float(np.std(getattr(g, attr))), 1e-6) for k, attr in OBS}


def group_residual(o, g, sc):
    total = 0.0
    for k, attr in OBS:
        d = getattr(g, attr)
        m = o[k][:len(d)]
        total += float(np.sqrt(np.mean(((m - d) / sc[k]) ** 2)))
    return total


def mechanism_split_residual(o1, pv):
    idx2 = 2
    V2, AP2, Nr2 = o1["V"][idx2], o1["AP"][idx2], o1["Nr"][idx2]
    if V2 <= 1e-6 or AP2 <= 1e-6:
        return 0.0
    res = 0.0
    vr, nr = pv[11] * V2, pv[12] * AP2
    if (vr + nr) > 1.0:
        res += ((nr / (vr + nr)) - cfg.NEUTRO_FRAC["recalc"]) ** 2
    vf, nf = pv[16] * V2, pv[17] * AP2
    if (vf + nf) > 1.0:
        res += ((nf / (vf + nf)) - cfg.NEUTRO_FRAC["fib"]) ** 2
    vx, nx = pv[20] * V2, pv[21] * AP2 * Nr2
    if (vx + nx) > 1.0:
        res += ((nx / (vx + nx)) - cfg.NEUTRO_FRAC["xiii"]) ** 2
    return res


def make_cost(g1, g2, n1, n2, tfg1, tfg2, sc1, sc2):
    def cost(pv):
        for i, (lo, hi) in enumerate(cfg.BOUNDS):
            if pv[i] < lo or pv[i] > hi:
                excess = max(lo - pv[i], pv[i] - hi, 0.0) / (hi - lo)
                return cfg.COST_PENALTY_NAN * (1.0 + excess)
        try:
            o1 = solve_group(pv, g1.T, n1, tfg1, pv[1], pv[8])
            o2 = solve_group(pv, g2.T, n2, tfg2, pv[1] * pv[24], pv[8] * pv[25])
        except Exception:
            return cfg.COST_PENALTY_NAN
        for o in (o1, o2):
            if any(np.any(np.isnan(o[k])) for k in ("D", "AP", "recalc", "thrombin", "fib", "xiii")):
                return cfg.COST_PENALTY_NAN
        c = group_residual(o1, g1, sc1) + group_residual(o2, g2, sc2)
        c += cfg.W_SPLIT * mechanism_split_residual(o1, pv)
        if np.any(o1["Hn"] > pv[7] * 0.99):
            c += cfg.HN_SATURATION_PENALTY
        return float(c)
    return cost


def r2(pred, obs):
    ss_res = np.sum((pred - obs) ** 2)
    ss_tot = np.sum((obs - obs.mean()) ** 2)
    return float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")


def g2_r2(pv, g2, n2, tfg2):
    o = solve_group(pv, g2.T, n2, tfg2, pv[1] * pv[24], pv[8] * pv[25])
    out = {}
    for k, attr in OBS:
        d = getattr(g2, attr)
        out[k] = r2(np.array(o[k][:len(d)]), d)
    return out


def main():
    print("=" * 70)
    print("SC sensitivity: per-group-std vs range-based v12 SC")
    print("=" * 70)

    g1, g2 = load_data()
    n1, n2 = build_neutrophil_interpolators(g1, g2)
    tfg1, tfg2 = make_fine_grids()

    sc1 = per_group_std_sc(g1)
    sc2 = per_group_std_sc(g2)
    print("\nper-group-std SC:")
    for k, _ in OBS:
        print(f"  {k:>9}: G1={sc1[k]:7.2f}  G2={sc2[k]:7.2f}  (v12 SC={cfg.SC[k]:.1f})")

    cost = make_cost(g1, g2, n1, n2, tfg1, tfg2, sc1, sc2)

    print("\nFitting (quick mode, seed=42)...")
    t0 = time.time()
    de = differential_evolution(
        cost, cfg.BOUNDS, maxiter=200, popsize=15, seed=SEED, tol=1e-7,
        workers=1, mutation=(0.5, 1.5), recombination=0.85,
        disp=False, polish=False, init="sobol",
    )
    best_x, best_cost = de.x.copy(), float(de.fun)
    for method, opts in [("Nelder-Mead", dict(maxiter=3000, xatol=1e-8, fatol=1e-10)),
                         ("Powell", dict(maxiter=2000, ftol=1e-10)),
                         ("Nelder-Mead", dict(maxiter=3000, xatol=1e-9, fatol=1e-11))]:
        r = minimize(cost, best_x, method=method, options=opts)
        if np.isfinite(r.fun) and r.fun < best_cost:
            best_x, best_cost = r.x.copy(), float(r.fun)
    print(f"  done in {(time.time()-t0)/60:.1f} min, cost={best_cost:.4f}")

    # G2 R2 under per-group-std fit
    r2_new = g2_r2(best_x, g2, n2, tfg2)

    # baseline (analysis 05) G2 R2 for comparison
    base = json.loads(Path("analyses/05_v13_baseline/results/fit.json").read_text())
    base_x = np.array(base["best_x"])
    r2_base = g2_r2(base_x, g2, n2, tfg2)

    print("\nG2 per-observable R2:")
    print(f"  {'obs':>9} | {'baseline(range-SC)':>18} | {'per-group-std':>14}")
    print("-" * 50)
    for k, _ in OBS:
        print(f"  {k:>9} | {r2_base[k]:>18.4f} | {r2_new[k]:>14.4f}")

    # XIII channel params (for Zone A/B multimodality check)
    print(f"\nXIII channel params (per-group-std fit):")
    print(f"  ax={best_x[20]:.1f} cx={best_x[21]:.1f} bx={best_x[22]:.2f} kx={best_x[23]:.2f}")
    print(f"  bx/kx ratio={best_x[22]/best_x[23]:.2f}")
    print(f"baseline XIII params:")
    print(f"  ax={base_x[20]:.1f} cx={base_x[21]:.1f} bx={base_x[22]:.2f} kx={base_x[23]:.2f}")
    print(f"  bx/kx ratio={base_x[22]/base_x[23]:.2f}")

    out = dict(
        seed=SEED, cost=best_cost,
        sc1=sc1, sc2=sc2,
        g2_r2_baseline=r2_base, g2_r2_pergroupstd=r2_new,
        best_x=best_x.tolist(),
        xiii_params_new=dict(ax=best_x[20], cx=best_x[21], bx=best_x[22], kx=best_x[23]),
        xiii_params_base=dict(ax=base_x[20], cx=base_x[21], bx=base_x[22], kx=base_x[23]),
    )
    Path("_sc_sensitivity.json").write_text(json.dumps(out, indent=2, default=float))
    print("\nSaved: _sc_sensitivity.json")
    print("\nNOTE: single seed. The 41% R2<0 rate is a BOOTSTRAP property;")
    print("this single fit only shows whether per-group-std lifts the XIII-G2")
    print("fit at the baseline point. Full re-bootstrap under per-group-std")
    print("would be needed to re-measure the 41% — decide after seeing this.")


if __name__ == "__main__":
    main()
