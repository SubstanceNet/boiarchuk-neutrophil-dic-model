"""
LEGACY: v12 cost function. The canonical v13 baseline is produced by
analyses/05_v13_baseline/fit.py via src.fit_runner (src.cost_v13.joint_cost_v13).
This module is retained for v12 reproducibility (the archive/v12 contract
checked by tests/test_reproducibility.py) and historical reference.

Command-line entry point for fitting.

Usage:
    python -m src.cli --quick
    python -m src.cli
    python -m src.cli --output results/run_001.pkl

The script prints fit metrics to stdout and saves a pickle with the full
result for downstream analysis.
"""

from __future__ import annotations
import argparse
import pickle
import sys
from pathlib import Path

import numpy as np

from . import config as cfg
from .data import load_data, build_neutrophil_interpolators
from .model import solve_group, make_fine_grids
from .fit import run_fit, r_squared, params_to_dict


def _print_metrics(label: str, model_out: dict, group, metric_keys, sc_keys) -> dict:
    print(f"\n{'=' * 65}")
    print(f"{label}")
    print("-" * 40)
    metrics = {}
    for key, data in metric_keys:
        m = model_out[key][:len(data)] if len(model_out[key]) != len(data) else model_out[key]
        r2 = r_squared(m, data)
        rmse = float(np.sqrt(np.mean((m - data) ** 2)))
        metrics[key] = dict(R2=r2, RMSE=rmse)
        print(f"  {key:10s}: R^2={r2:+.4f}  RMSE={rmse:.3f}")
    avg_r2 = float(np.mean([v["R2"] for v in metrics.values()]))
    print(f"  {'AVERAGE':10s}: R^2={avg_r2:+.4f}")
    return metrics


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Joint fit of v12 model on G1+G2")
    parser.add_argument("--quick", action="store_true", help="quick run (smoke-test mode)")
    parser.add_argument("--workers", type=int, default=-1, help="DE workers (-1 = all cores)")
    parser.add_argument("--output", type=Path, default=None, help="output pickle path")
    parser.add_argument("--seeds", type=int, nargs="+", default=None, help="DE seed list")
    args = parser.parse_args(argv)

    g1, g2 = load_data()
    n1_interp, n2_interp = build_neutrophil_interpolators(g1, g2)
    t_fine_g1, t_fine_g2 = make_fine_grids()

    print("=" * 65)
    print("v12 phase-0 migration: JOINT FIT")
    print(f"  {len(cfg.NAMES)} params = 24 shared + km + tm")
    print(f"  G1: {g1.n_datapoints}pts (surv-weighted) + G2: {g2.n_datapoints}pts "
          f"= {g1.n_datapoints + g2.n_datapoints}")
    print(f"  Data/param: {(g1.n_datapoints + g2.n_datapoints) / len(cfg.NAMES):.1f}")
    print(f"  Mechanism-split weight: W={cfg.W_SPLIT}")
    print(f"  Mode: {'QUICK' if args.quick else 'FULL'}")
    print("=" * 65)

    result = run_fit(g1, g2, quick=args.quick, seeds=args.seeds, workers=args.workers)
    best_x = result["best_x"]
    best_cost = result["best_cost"]
    p = result["params_dict"]
    p["tv"] = cfg.TV_FIX
    p["kcd"] = cfg.KCD_FIX
    p["kr_g2"] = p["kr"] * p["km"]
    p["tp2_g2"] = p["tp2"] * p["tm"]

    o1 = solve_group(best_x, g1.T, n1_interp, t_fine_g1, p["kr"], p["tp2"])
    o2 = solve_group(best_x, g2.T, n2_interp, t_fine_g2, p["kr_g2"], p["tp2_g2"])

    g1_keys = [
        ("recalc",   g1.recalc),
        ("thrombin", g1.thrombin),
        ("fib",      g1.fib),
        ("xiii",     g1.xiii),
        ("AP",       g1.AP),
        ("D",        g1.deg),
    ]
    g2_keys = [
        ("recalc",   g2.recalc),
        ("thrombin", g2.thrombin),
        ("fib",      g2.fib),
        ("xiii",     g2.xiii),
        ("AP",       g2.AP),
        ("D",        g2.deg),
    ]
    metrics_g1 = _print_metrics(f"GROUP I  (cost={best_cost:.6f})", o1, g1, g1_keys, None)
    metrics_g2 = _print_metrics("GROUP II (jointly fit)", o2, g2, g2_keys, None)

    print(f"\n{'=' * 65}")
    print("MYELOSAN MODIFIERS")
    print("-" * 40)
    print(f"  kr:  G1={p['kr']:.3f}, G2={p['kr_g2']:.3f}  (x{p['km']:.2f})")
    print(f"  tp2: G1={p['tp2']:.2f} d, G2={p['tp2_g2']:.2f} d  (x{p['tm']:.3f})")

    print(f"\n{'=' * 65}")
    print("PARAMETERS")
    print("-" * 40)
    at_bound = 0
    for i, n in enumerate(cfg.NAMES):
        lo, hi = cfg.BOUNDS[i]
        flag = ""
        if best_x[i] - lo < 0.01 * (hi - lo):
            flag = "  <-- LOW"
            at_bound += 1
        elif hi - best_x[i] < 0.01 * (hi - lo):
            flag = "  <-- HIGH"
            at_bound += 1
        print(f"  {n:6s} = {best_x[i]:12.6f}  [{lo}, {hi}]{flag}")
    if at_bound:
        print(f"\n  WARNING: {at_bound}/{len(cfg.NAMES)} parameters at bounds")
    print(f"\nTotal time: {result['t_total']:.0f} s ({result['t_total'] / 60:.1f} min)")

    out = dict(
        model="v12_phase0_migration",
        version="0.1.0-phase0",
        params=p,
        cost=float(best_cost),
        metrics_g1=metrics_g1,
        metrics_g2=metrics_g2,
        elapsed=result["t_total"],
        per_seed_costs=result["per_seed_costs"],
        best_x=best_x.tolist(),
        T1=g1.T.tolist(),
        T2=g2.T.tolist(),
        o1={k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in o1.items()},
        o2={k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in o2.items()},
    )

    if args.output is None:
        out_path = Path(__file__).resolve().parent.parent / "results" / "phase0_run.pkl"
    else:
        out_path = args.output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as f:
        pickle.dump(out, f)
    print(f"\nSaved -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
