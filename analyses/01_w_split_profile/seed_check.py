"""Multi-seed convergence check for W_split=0 and W_split=2.

Question: does the W=0 fit consistently find the alternative decomposition
across different seeds, or is it a single-seed artefact?
"""
import json
from pathlib import Path
import numpy as np
from src.fit_runner import run_with_overrides
from src.data import load_data, build_neutrophil_interpolators
from src.model import solve_group, make_fine_grids

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR = ANALYSIS_DIR / "results" / "_cache"

g1, g2 = load_data()
n1_interp, _ = build_neutrophil_interpolators(g1, g2)
t_fine_g1, _ = make_fine_grids()

results = []
for w in [0.0, 2.0]:
    for seed in [7, 123]:    # 42 already done in main sweep
        r = run_with_overrides(
            overrides={"W_SPLIT": w}, seeds=[seed], quick=True,
            cache_dir=CACHE_DIR, label=f"W={w} seed={seed}", verbose=True,
        )
        pv = np.asarray(r["best_x"])
        o1 = solve_group(pv, g1.T, n1_interp, t_fine_g1, pv[1], pv[8])
        V2, AP2, Nr2 = o1["V"][2], o1["AP"][2], o1["Nr"][2]
        def _f(v, n): t = abs(v) + abs(n); return abs(n)/t if t > 1e-12 else float("nan")
        results.append(dict(
            W=w, seed=seed, cost=r["best_cost"],
            avg_r2_g1=r["avg_r2_g1"], avg_r2_g2=r["avg_r2_g2"],
            recalc_n=_f(pv[11]*V2, pv[12]*AP2),
            fib_n=_f(pv[16]*V2, pv[17]*AP2),
            xiii_n=_f(pv[20]*V2, pv[21]*AP2*Nr2),
        ))

(ANALYSIS_DIR / "results" / "seed_check.json").write_text(
    json.dumps(results, indent=2, default=float)
)
print()
print(f'{"W":>5} | {"seed":>5} | {"cost":>8} | {"R2_G1":>7} | {"R2_G2":>7} | {"recalc":>7} | {"fib":>7} | {"xiii":>7}')
print("-" * 75)
for r in results:
    print(f'{r["W"]:>5.1f} | {r["seed"]:>5d} | {r["cost"]:>8.4f} | {r["avg_r2_g1"]:>7.4f} | '
          f'{r["avg_r2_g2"]:>7.4f} | {r["recalc_n"]:>7.3f} | {r["fib_n"]:>7.3f} | {r["xiii_n"]:>7.3f}')
