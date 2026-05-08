"""
Analysis 06: cx-bound diagnostic under v13 cost.

Five v13 fits at seed=42, cx upper bound in {500, 600, 700, 1000, 2000}.
Compares to analysis 02 (same sweep under v12 cost) and analysis 05 (v13
baseline at default cx ≤ 600, seed 42).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

from src.fit_runner import run_with_overrides_v13
from src.data import load_data, build_neutrophil_interpolators
from src.model import solve_group, make_fine_grids


CX_BOUNDS = [
    ("tight",     (10.0, 500.0)),
    ("v12_prior", (10.0, 600.0)),
    ("loose",     (10.0, 700.0)),
    ("expanded",  (10.0, 1000.0)),
    ("wide",      (10.0, 2000.0)),
]
SEEDS = [42]
QUICK = True

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR = ANALYSIS_DIR / "results" / "_cache"
RESULTS_PATH = ANALYSIS_DIR / "results" / "sweep.json"


def measure_xiii_fraction(best_x, g1, n1_interp, t_fine_g1):
    pv = np.asarray(best_x)
    o1 = solve_group(pv, g1.T, n1_interp, t_fine_g1, pv[1], pv[8])
    V2, AP2, Nr2 = o1["V"][2], o1["AP"][2], o1["Nr"][2]
    xv = pv[20] * V2
    xn = pv[21] * AP2 * Nr2
    tot = abs(xv) + abs(xn)
    return float(abs(xn) / tot) if tot > 1e-12 else float("nan")


def main():
    g1, g2 = load_data()
    n1_interp, _ = build_neutrophil_interpolators(g1, g2)
    t_fine_g1, _ = make_fine_grids()

    print("=" * 70)
    print("v13 cx-bound diagnostic (analysis 06)")
    print(f"  seeds: {SEEDS}, quick: {QUICK}")
    print("  Configurations:")
    for label, (lo, hi) in CX_BOUNDS:
        print(f"    {label:>10s}: cx in ({lo}, {hi})")
    print("=" * 70)

    rows = []
    for label, (lo, hi) in CX_BOUNDS:
        result = run_with_overrides_v13(
            overrides={"BOUNDS_OVERRIDE": {"cx": (lo, hi)}},
            seeds=SEEDS, quick=QUICK,
            cache_dir=CACHE_DIR,
            label=f"cx_{label}",
            verbose=True,
        )
        best_x = np.asarray(result["best_x"])
        xiii_frac = measure_xiii_fraction(best_x, g1, n1_interp, t_fine_g1)
        rows.append(dict(
            label=label,
            cx_bound=[lo, hi],
            cost=result["best_cost"],
            avg_r2_g1=result["avg_r2_g1"],
            avg_r2_g2=result["avg_r2_g2"],
            metrics_g1=result["metrics_g1"],
            metrics_g2=result["metrics_g2"],
            xiii_channel={
                "ax": result["params_dict"]["ax"],
                "cx": result["params_dict"]["cx"],
                "bx": result["params_dict"]["bx"],
                "kx": result["params_dict"]["kx"],
            },
            xiii_neutro_frac_g1d2=xiii_frac,
            params=result["params_dict"],
            cached=result["cached"],
            wall_time=result["wall_time"],
        ))

    summary = dict(
        analysis="06_v13_cx_diagnostic",
        cost_version="v13",
        seeds=SEEDS, quick=QUICK,
        runs=rows,
    )
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(summary, indent=2, default=float))

    print()
    print("=" * 100)
    print(f"{'label':>10s} | {'cx_max':>7s} | {'cost':>7s} | {'R2_G1':>7s} | "
          f"{'R2_G2':>7s} | {'cx_fit':>7s} | {'xiii_n':>6s} | {'xiii_G2':>8s}")
    print("-" * 100)
    for r in rows:
        x = r["xiii_channel"]
        f = r["xiii_neutro_frac_g1d2"]
        print(f"{r['label']:>10s} | {r['cx_bound'][1]:>7.0f} | "
              f"{r['cost']:>7.4f} | {r['avg_r2_g1']:>+7.4f} | "
              f"{r['avg_r2_g2']:>+7.4f} | {x['cx']:>7.1f} | "
              f"{f:>6.3f} | {r['metrics_g2']['xiii']['R2']:>+8.4f}")
    print()
    print(f"Saved -> {RESULTS_PATH}")


if __name__ == "__main__":
    main()
