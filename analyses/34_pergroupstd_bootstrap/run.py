"""Analysis 34: parametric bootstrap under per-group-std normalization.

Re-runs the analysis-22 bootstrap with ONE change: the cost function uses
per-group-std SC (each observable normalized by that group's std) instead of
the single range-based v12 SC. Everything else identical to analysis 22:
- same baseline predictions (analysis 05) as the synthetic-data mean
- same sigmas (analysis 22 sigmas.json) for the noise
- same seeds (1..100)
- same quick-mode pipeline (DE + NM + Powell + NM)

Purpose: a single per-group-std fit lifted xiii_G2 R2 from 0.08 to 0.93
(_sc_sensitivity). This re-bootstrap measures whether the analysis-22
finding of 41% xiii_G2 R2<0 is a normalization artifact (drops to <10% ->
adopt per-group-std baseline) or partly structural (stays 25-35% -> retain
range-SC, document as sensitivity). Threshold decision on the data.

Cost is module-level (picklable) so workers=-1 parallelism works.
"""
from __future__ import annotations
import json
import time
import pickle
from pathlib import Path
from dataclasses import replace
import numpy as np
from scipy.optimize import differential_evolution, minimize

from src import config as cfg
from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids, solve_group

ANALYSIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ANALYSIS_DIR / "results"
CACHE_DIR = RESULTS_DIR / "_cache"
N_ITERS = 50
OBS = [("recalc", "recalc"), ("thrombin", "thrombin"), ("fib", "fib"),
       ("xiii", "xiii"), ("AP", "AP"), ("D", "deg")]

def per_group_std_sc(g):
    return {k: max(float(np.std(getattr(g, attr))), 1e-6) for k, attr in OBS}


def _group_residual(o, g, sc):
    total = 0.0
    for k, attr in OBS:
        d = getattr(g, attr)
        m = o[k][:len(d)]
        total += float(np.sqrt(np.mean(((m - d) / sc[k]) ** 2)))
    return total


def _split_residual(o1, pv):
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


def cost_pergroupstd(pv, g1, g2, n1, n2, tfg1, tfg2, sc1, sc2):
    """Module-level, picklable. All data passed via args= (robust to
    multiprocessing fork; scipy distributes args to each worker)."""
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
    c = _group_residual(o1, g1, sc1) + _group_residual(o2, g2, sc2)
    c += cfg.W_SPLIT * _split_residual(o1, pv)
    if np.any(o1["Hn"] > pv[7] * 0.99):
        c += cfg.HN_SATURATION_PENALTY
    return float(c)


def compute_baseline_predictions():
    base = json.loads(Path("analyses/05_v13_baseline/results/fit.json").read_text())
    pv = np.array(base["best_x"])[:26]
    g1, g2 = load_data()
    n1, n2 = build_neutrophil_interpolators(g1, g2)
    tfg1, tfg2 = make_fine_grids()
    o1 = solve_group(pv, g1.T, n1, tfg1, pv[1], pv[8])
    o2 = solve_group(pv, g2.T, n2, tfg2, pv[1] * pv[24], pv[8] * pv[25])
    g1_pred, g2_pred = {}, {}
    for k, attr in OBS:
        g1_pred[k] = np.asarray(o1[k][:len(getattr(g1, attr))]).copy()
        g2_pred[k] = np.asarray(o2[k][:len(getattr(g2, attr))]).copy()
    return g1_pred, g2_pred, g1, g2


def make_synthetic(g1, g2, g1_pred, g2_pred, sig_g1, sig_g2, seed):
    rng = np.random.default_rng(seed)

    def synth(pred, sig):
        return {k: pred[k] + rng.normal(0.0, sig[k], size=len(pred[k])) for k, _ in OBS}

    s1 = synth(g1_pred, sig_g1)
    s2 = synth(g2_pred, sig_g2)
    g1n = replace(g1, recalc=s1["recalc"], thrombin=s1["thrombin"], fib=s1["fib"],
                  xiii=s1["xiii"], AP=s1["AP"], deg=s1["D"])
    g2n = replace(g2, recalc=s2["recalc"], thrombin=s2["thrombin"], fib=s2["fib"],
                  xiii=s2["xiii"], AP=s2["AP"], deg=s2["D"])
    return g1n, g2n


def fit_one(g1s, g2s, sc1, sc2, seed):
    n1s, n2s = build_neutrophil_interpolators(g1s, g2s)
    tfg1, tfg2 = make_fine_grids()
    args = (g1s, g2s, n1s, n2s, tfg1, tfg2, sc1, sc2)

    de = differential_evolution(
        cost_pergroupstd, cfg.BOUNDS, args=args, maxiter=200, popsize=15,
        seed=seed, tol=1e-7, workers=-1, mutation=(0.5, 1.5),
        recombination=0.85, disp=False, polish=False, init="sobol",
    )
    best_x, best_cost = de.x.copy(), float(de.fun)
    for method, opts in [("Nelder-Mead", dict(maxiter=3000, xatol=1e-8, fatol=1e-10)),
                         ("Powell", dict(maxiter=2000, ftol=1e-10)),
                         ("Nelder-Mead", dict(maxiter=3000, xatol=1e-9, fatol=1e-11))]:
        r = minimize(cost_pergroupstd, best_x, args=args, method=method, options=opts)
        if np.isfinite(r.fun) and r.fun < best_cost:
            best_x, best_cost = r.x.copy(), float(r.fun)
    return best_x, best_cost


def main():
    print("=" * 70)
    print("Analysis 34: bootstrap under per-group-std normalization (N=100)")
    print("=" * 70)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    g1_pred, g2_pred, g1, g2 = compute_baseline_predictions()

    # per-group-std SC
    sc1 = per_group_std_sc(g1)
    sc2 = per_group_std_sc(g2)
    print("per-group-std SC set. G2 xiii SC =", round(sc2["xiii"], 3),
          "(vs v12 range SC", cfg.SC["xiii"], ")")

    # reuse analysis-22 sigmas EXACTLY (identical synthetic data)
    sig = json.loads(Path("analyses/22_predictive_check/results/sigmas.json").read_text())
    sig_g1 = sig["sigmas_g1"]; sig_g2 = sig["sigmas_g2"]

    # real-data interpolators for computing R2 on real timepoints
    n1r, n2r = build_neutrophil_interpolators(g1, g2)
    tfg1, tfg2 = make_fine_grids()

    t_start = time.time()
    for i in range(1, N_ITERS + 1):
        seed = i
        cache = CACHE_DIR / f"iter_{seed:03d}.pkl"
        if cache.exists():
            print(f"[{i:>3}/{N_ITERS}] cached")
            continue
        t0 = time.time()
        try:
            g1s, g2s = make_synthetic(g1, g2, g1_pred, g2_pred, sig_g1, sig_g2, seed)
            best_x, best_cost = fit_one(g1s, g2s, sc1, sc2, seed)
            # G2 R2 on REAL data (predictions from fitted params)
            pv = best_x[:26]
            o2 = solve_group(pv, g2.T, n2r, tfg2, pv[1] * pv[24], pv[8] * pv[25])
            g2_r2 = {}
            for k, attr in OBS:
                d = getattr(g2, attr)
                m = np.array(o2[k][:len(d)])
                ss_res = np.sum((m - d) ** 2); ss_tot = np.sum((d - d.mean()) ** 2)
                g2_r2[k] = float(1 - ss_res / ss_tot) if ss_tot > 0 else float("nan")
            rec = dict(seed=seed, best_x=best_x.tolist(), best_cost=best_cost,
                       g2_r2=g2_r2, failed=False, elapsed_s=time.time() - t0)
        except Exception as e:
            rec = dict(seed=seed, failed=True, error=str(e), elapsed_s=time.time() - t0)
            print(f"  ITER {seed} FAILED: {e}")
        with cache.open("wb") as f:
            pickle.dump(rec, f)
        el = (time.time() - t_start) / 60
        eta = (el / i) * (N_ITERS - i)
        if not rec.get("failed"):
            print(f"[{i:>3}/{N_ITERS}] seed={seed} cost={rec['best_cost']:.4f} "
                  f"xiii_G2_R2={rec['g2_r2']['xiii']:+.3f} ({rec['elapsed_s']:.0f}s) "
                  f"total={el:.1f}m ETA={eta:.1f}m")
        else:
            print(f"[{i:>3}/{N_ITERS}] seed={seed} FAILED total={el:.1f}m ETA={eta:.1f}m")

    print(f"\n=== Done in {(time.time()-t_start)/3600:.2f}h ===")
    print("Run aggregate next: python -m analyses.34_pergroupstd_bootstrap.aggregate")


if __name__ == "__main__":
    main()
