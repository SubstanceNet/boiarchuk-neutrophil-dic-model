"""
Joint-fit cost function and optimisation pipeline.

The cost function is byte-identical to archive/v12/model_v12.py._cost_core.
The optimisation pipeline is the same DE -> NM -> Powell -> NM2 sequence.

Phase 0 contract: numerical equivalence with v12 for the same seed.
"""

from __future__ import annotations
import time
import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.interpolate import interp1d

from . import config as cfg
from .data import GroupData, build_neutrophil_interpolators
from .model import solve_group, make_fine_grids


# ============================================================
#  Helpers
# ============================================================

def params_to_dict(pv: np.ndarray) -> dict[str, float]:
    """Convert parameter vector to dict by NAMES."""
    return {n: float(pv[i]) for i, n in enumerate(cfg.NAMES)}


def r_squared(model: np.ndarray, data: np.ndarray) -> float:
    """Coefficient of determination."""
    ss = float(np.sum((data - np.mean(data)) ** 2))
    if ss <= 1e-12:
        return 0.0
    return 1.0 - float(np.sum((model - data) ** 2)) / ss


# ============================================================
#  Cost function
# ============================================================

def joint_cost(
    pv: np.ndarray,
    g1: GroupData,
    g2: GroupData,
    n1_interp: interp1d,
    n2_interp: interp1d,
    t_fine_g1: np.ndarray,
    t_fine_g2: np.ndarray,
) -> float:
    """Joint cost over G1 (survivor-weighted) and G2 (uniform).

    Components:
      1. Per-observable normalised RMSE on G1 (weighted by W_SURV).
      2. Per-observable normalised RMSE on G2 (uniform).
      3. Hn-saturation penalty (added if any Hn approaches Hm).
      4. Mechanism-split constraint at G1 day 2 (W_SPLIT).

    Returns COST_PENALTY_NAN (1e6) if integration fails or produces NaN.
    """
    kr_g1 = pv[1]
    kr_g2 = pv[1] * pv[24]    # kr * km
    tp2_g1 = pv[8]
    tp2_g2 = pv[8] * pv[25]   # tp2 * tm

    try:
        o1 = solve_group(pv, g1.T, n1_interp, t_fine_g1, kr_g1, tp2_g1)
        o2 = solve_group(pv, g2.T, n2_interp, t_fine_g2, kr_g2, tp2_g2)
    except Exception:
        return cfg.COST_PENALTY_NAN

    keys_to_check = ("D", "AP", "recalc", "thrombin", "fib", "xiii")
    for o in (o1, o2):
        if any(np.any(np.isnan(o[k])) for k in keys_to_check):
            return cfg.COST_PENALTY_NAN

    c = 0.0

    # G1: survivor-weighted residuals
    g1_pairs = [
        ("recalc",   g1.recalc,   cfg.SC["recalc"]),
        ("thrombin", g1.thrombin, cfg.SC["thrombin"]),
        ("fib",      g1.fib,      cfg.SC["fib"]),
        ("xiii",     g1.xiii,     cfg.SC["xiii"]),
        ("AP",       g1.AP,       cfg.SC["AP"]),
        ("D",        g1.deg,      cfg.SC["D"]),
    ]
    for k, d, s in g1_pairs:
        c += float(np.sqrt(np.average(((o1[k] - d) / s) ** 2, weights=cfg.W_SURV)))

    # G2: uniform-weight residuals
    g2_pairs = [
        ("recalc",   g2.recalc),
        ("thrombin", g2.thrombin),
        ("fib",      g2.fib),
        ("xiii",     g2.xiii),
        ("AP",       g2.AP),
        ("D",        g2.deg),
    ]
    for k, d in g2_pairs:
        m = o2[k][:len(d)]
        c += float(np.sqrt(np.mean(((m - d) / cfg.SC[k]) ** 2)))

    # Hn-saturation penalty
    if np.any(o1["Hn"] > pv[7] * 0.99):
        c += cfg.HN_SATURATION_PENALTY

    # Mechanism-split constraint at G1 day 2
    # Forces neutrophil-share fractions to match NEUTRO_FRAC targets.
    idx2 = 2
    V2 = o1["V"][idx2]
    AP2v = o1["AP"][idx2]
    Nr2 = o1["Nr"][idx2]

    if V2 > 1e-6 and AP2v > 1e-6:
        # recalc: target neutro = 24%
        vr, nr = pv[11] * V2, pv[12] * AP2v
        if (vr + nr) > 1.0:
            c += cfg.W_SPLIT * ((nr / (vr + nr)) - cfg.NEUTRO_FRAC["recalc"]) ** 2

        # fib: target neutro = 76%
        vf, nf = pv[16] * V2, pv[17] * AP2v
        if (vf + nf) > 1.0:
            c += cfg.W_SPLIT * ((nf / (vf + nf)) - cfg.NEUTRO_FRAC["fib"]) ** 2

        # xiii: target neutro = 82%
        vx, nx = pv[20] * V2, pv[21] * AP2v * Nr2
        if (vx + nx) > 1.0:
            c += cfg.W_SPLIT * ((nx / (vx + nx)) - cfg.NEUTRO_FRAC["xiii"]) ** 2

    return c


def _cost_bounded(
    pv: np.ndarray,
    g1: GroupData,
    g2: GroupData,
    n1_interp: interp1d,
    n2_interp: interp1d,
    t_fine_g1: np.ndarray,
    t_fine_g2: np.ndarray,
) -> float:
    """Bounded version of cost: returns large penalty for out-of-bounds pv.

    Used by gradient-free local optimisers (NM, Powell) which do not respect
    bounds intrinsically.
    """
    for i, (lo, hi) in enumerate(cfg.BOUNDS):
        if pv[i] < lo or pv[i] > hi:
            penalty_factor = 1.0 + max(lo - pv[i], pv[i] - hi, 0.0) / (hi - lo)
            return cfg.COST_PENALTY_NAN * penalty_factor
    return joint_cost(pv, g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2)


# ============================================================
#  Optimisation pipeline
# ============================================================

def run_fit(
    g1: GroupData,
    g2: GroupData,
    *,
    quick: bool = False,
    seeds: list[int] | None = None,
    workers: int = -1,
    verbose: bool = True,
) -> dict:
    """Full fit pipeline: multi-seed DE -> NM -> Powell -> NM round 2.

    Parameters
    ----------
    g1, g2 : GroupData
    quick : if True, fewer seeds and shorter inner loops for smoke-tests
    seeds : explicit override of seed list
    workers : passed to differential_evolution (default -1: all cores)
    verbose : print progress to stdout

    Returns dict with keys:
      best_x, best_cost, params_dict, t_total, per_seed_costs
    """
    n1_interp, n2_interp = build_neutrophil_interpolators(g1, g2)
    t_fine_g1, t_fine_g2 = make_fine_grids()

    cost_args = (g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2)

    if seeds is None:
        seeds = [42, 7] if quick else [42, 7, 123, 2024, 999]
    if quick:
        de_pop, de_iter, nm_iter, pw_iter = 8, 120, 3000, 2000
    else:
        de_pop, de_iter, nm_iter, pw_iter = 12, 300, 10000, 8000

    best_cost = cfg.COST_PENALTY_NAN
    best_x: np.ndarray | None = None
    per_seed_costs: list[tuple[int, float]] = []
    t_start = time.time()

    for seed in seeds:
        if verbose:
            print(f"--- DE seed={seed} ---", flush=True)
        ts = time.time()
        r = differential_evolution(
            joint_cost,
            cfg.BOUNDS,
            args=cost_args,
            maxiter=de_iter,
            popsize=de_pop,
            seed=seed,
            tol=1e-7,
            workers=workers,
            mutation=(0.5, 1.5),
            recombination=0.85,
            disp=False,
            polish=False,
        )
        per_seed_costs.append((seed, float(r.fun)))
        if verbose:
            print(f"  cost={r.fun:.6f}  ({time.time() - ts:.0f}s, {r.nfev} evals)", flush=True)
        if r.fun < best_cost:
            best_cost = float(r.fun)
            best_x = r.x.copy()
            if verbose:
                print("  -> best", flush=True)

    if best_x is None:
        raise RuntimeError("Differential evolution failed for all seeds")

    if verbose:
        print(f"\nBest DE: {best_cost:.6f}", flush=True)

    for method, opts in [
        ("Nelder-Mead", {"maxiter": nm_iter, "xatol": 1e-9, "fatol": 1e-10}),
        ("Powell",      {"maxiter": pw_iter, "ftol": 1e-10}),
    ]:
        try:
            r = minimize(_cost_bounded, best_x, args=cost_args, method=method, options=opts)
            if np.isfinite(r.fun) and r.fun < best_cost:
                best_x = r.x.copy()
                best_cost = float(r.fun)
                if verbose:
                    print(f"  {method}: {r.fun:.6f} -> improved", flush=True)
            else:
                if verbose:
                    print(f"  {method}: {r.fun:.6f}", flush=True)
        except Exception as e:
            if verbose:
                print(f"  {method}: failed ({e})", flush=True)

    if verbose:
        print("--- NM round 2 ---", flush=True)
    try:
        r = minimize(
            _cost_bounded, best_x, args=cost_args, method="Nelder-Mead",
            options={"maxiter": nm_iter, "xatol": 1e-10, "fatol": 1e-11},
        )
        if np.isfinite(r.fun) and r.fun < best_cost:
            best_x = r.x.copy()
            best_cost = float(r.fun)
            if verbose:
                print(f"  {r.fun:.6f} -> improved", flush=True)
    except Exception as e:
        if verbose:
            print(f"  NM round 2 failed: {e}", flush=True)

    return dict(
        best_x=best_x,
        best_cost=best_cost,
        params_dict=params_to_dict(best_x),
        t_total=time.time() - t_start,
        per_seed_costs=per_seed_costs,
    )
