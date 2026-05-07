"""
Analysis 02: cx bound exploration.

Three fits at W=2.0, seed=42, varying upper bound of cx:
    (10, 600), (10, 2000), (10, 5000).

See README.md for full description.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

from src.fit_runner import run_with_overrides
from src.data import load_data, build_neutrophil_interpolators
from src.model import solve_group, make_fine_grids


CX_BOUNDS = [
    ("baseline", (10.0, 600.0)),
    ("expanded", (10.0, 2000.0)),
    ("wide",     (10.0, 5000.0)),
]
SEEDS = [42]
QUICK = True

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR = ANALYSIS_DIR / "results" / "_cache"
RESULTS_PATH = ANALYSIS_DIR / "results" / "sweep.json"


def measure_xiii_fraction(best_x: np.ndarray, g1, n1_interp, t_fine_g1) -> float:
    """Realised neutrophil-share fraction for XIII channel on G1 day 2."""
    pv = np.asarray(best_x)
    o1 = solve_group(pv, g1.T, n1_interp, t_fine_g1, pv[1], pv[8])
    V2, AP2, Nr2 = o1["V"][2], o1["AP"][2], o1["Nr"][2]
    xv = pv[20] * V2
    xn = pv[21] * AP2 * Nr2
    tot = abs(xv) + abs(xn)
    return float(abs(xn) / tot) if tot > 1e-12 else float("nan")


def main() -> int:
    g1, g2 = load_data()
    n1_interp, _ = build_neutrophil_interpolators(g1, g2)
    t_fine_g1, _ = make_fine_grids()

    print(f"=== cx bound sweep: {len(CX_BOUNDS)} runs ===")
    for label, (lo, hi) in CX_BOUNDS:
        print(f"  {label:>10s}: ({lo}, {hi})")
    print()

    rows = []
    for label, (lo, hi) in CX_BOUNDS:
        result = run_with_overrides(
            overrides={
                "W_SPLIT": 2.0,
                "BOUNDS_OVERRIDE": {"cx": (lo, hi)},
            },
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
            xiii_neutro_frac=xiii_frac,
            params=result["params_dict"],
            cached=result["cached"],
            wall_time=result["wall_time"],
        ))

    summary = dict(
        analysis="02_cx_bound",
        seeds=SEEDS, quick=QUICK,
        runs=rows,
    )
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("w") as f:
        json.dump(summary, f, indent=2, default=float)

    print()
    print("=== Summary ===")
    print(f"{'label':>10s} | {'cx_max':>7s} | {'cost':>8s} | {'R2_G1':>7s} | "
          f"{'R2_G2':>7s} | {'cx_fit':>9s} | {'ax':>7s} | {'bx':>7s} | "
          f"{'kx':>6s} | {'xiii_n':>6s}")
    print("-" * 100)
    for r in rows:
        x = r["xiii_channel"]
        print(f"{r['label']:>10s} | {r['cx_bound'][1]:>7.0f} | "
              f"{r['cost']:>8.4f} | {r['avg_r2_g1']:>7.4f} | "
              f"{r['avg_r2_g2']:>7.4f} | {x['cx']:>9.2f} | "
              f"{x['ax']:>7.2f} | {x['bx']:>7.2f} | "
              f"{x['kx']:>6.3f} | {r['xiii_neutro_frac']:>6.3f}")
    print()
    print(f"Saved -> {RESULTS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
