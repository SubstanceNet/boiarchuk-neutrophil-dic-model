"""
Analysis 01: profile of joint fit across W_split values.

Question
--------
Is the mechanism-split constraint W_split (default 2.0) load-bearing for the
v12 conclusions, or merely an optimisation hint? See notes/known_issues.md
issue I-3 ("circular evidence in mechanism-split").

Method
------
Run 5 quick-mode fits at W_split in {0.0, 0.3, 1.0, 2.0, 5.0}, holding
everything else equal. Record:
  - best cost
  - per-observable R^2 for both groups
  - all 26 fitted parameter values
  - actual achieved neutrophil-share fractions on G1 day 2

Interpretation
--------------
- If parameters and R^2 are stable across W_split: constraint is benign.
  The mechanism-split decomposition (24/76/82%) is supported by the data
  itself, and the constraint merely accelerates convergence. Publication-safe.

- If parameters drift but R^2 is roughly constant: constraint defines the
  decomposition. We cannot present mechanism-split as evidence for the
  underlying biology — it is enforced. Either (a) document this honestly
  in the manuscript, or (b) replace constraint with an independent prior.

- If R^2 collapses at W_split=0: constraint compensates for under-determination
  in the data. Mechanism-split fractions are an essential prior, must be
  justified externally (literature, independent measurement).

Outputs
-------
  results/sweep.json     — all metrics, parameters, fractions per W_split
  results/_cache/*.pkl   — individual fit results (cache-keyed)
  figures/*.png          — visual summary

Runtime: ~5 x 13 min = ~65 min on 16-thread workstation.
"""

from __future__ import annotations
import json
from pathlib import Path

import numpy as np

from src.fit_runner import run_with_overrides
from src.data import load_data, build_neutrophil_interpolators
from src.model import solve_group, make_fine_grids


# ----------------------------------------------------------------
#  Configuration
# ----------------------------------------------------------------

W_GRID = [0.0, 0.3, 1.0, 2.0, 5.0]
SEEDS = [42]
QUICK = True

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR = ANALYSIS_DIR / "results" / "_cache"
RESULTS_PATH = ANALYSIS_DIR / "results" / "sweep.json"


# ----------------------------------------------------------------
#  Helpers
# ----------------------------------------------------------------

def measure_neutrophil_fractions(best_x: np.ndarray, g1, n1_interp, t_fine_g1) -> dict:
    """Compute the achieved neutrophil-share fractions on G1 day 2.

    These are what the mechanism-split constraint targets: 24/76/82%.
    Reports the actually-realised fractions, not the targets.
    """
    pv = np.asarray(best_x)
    o1 = solve_group(pv, g1.T, n1_interp, t_fine_g1, pv[1], pv[8])
    idx2 = 2  # day 2
    V2, AP2, Nr2 = o1["V"][idx2], o1["AP"][idx2], o1["Nr"][idx2]

    def _frac(v_term: float, n_term: float) -> float:
        tot = abs(v_term) + abs(n_term)
        return abs(n_term) / tot if tot > 1e-12 else float("nan")

    recalc_v = pv[11] * V2          # ar * V
    recalc_n = pv[12] * AP2         # cr * AP
    fib_v = pv[16] * V2             # af * V
    fib_n = pv[17] * AP2            # cf * AP
    xiii_v = pv[20] * V2            # ax * V
    xiii_n = pv[21] * AP2 * Nr2     # cx * AP * Nr

    return {
        "recalc_neutro_frac": _frac(recalc_v, recalc_n),
        "fib_neutro_frac":    _frac(fib_v, fib_n),
        "xiii_neutro_frac":   _frac(xiii_v, xiii_n),
        "day2_V":  float(V2),
        "day2_AP": float(AP2),
        "day2_Nr": float(Nr2),
    }


# ----------------------------------------------------------------
#  Sweep
# ----------------------------------------------------------------

def run_sweep() -> list[dict]:
    g1, g2 = load_data()
    n1_interp, _ = build_neutrophil_interpolators(g1, g2)
    t_fine_g1, _ = make_fine_grids()

    rows = []
    for w in W_GRID:
        result = run_with_overrides(
            overrides={"W_SPLIT": float(w)},
            seeds=SEEDS, quick=QUICK,
            cache_dir=CACHE_DIR,
            label=f"W_split={w}",
            verbose=True,
        )
        best_x = np.asarray(result["best_x"])
        fractions = measure_neutrophil_fractions(best_x, g1, n1_interp, t_fine_g1)
        rows.append(dict(
            W_split=float(w),
            cost=result["best_cost"],
            avg_r2_g1=result["avg_r2_g1"],
            avg_r2_g2=result["avg_r2_g2"],
            metrics_g1=result["metrics_g1"],
            metrics_g2=result["metrics_g2"],
            params=result["params_dict"],
            achieved_fractions=fractions,
            cached=result["cached"],
            wall_time=result["wall_time"],
        ))
    return rows


def main() -> int:
    print(f"=== W_split sweep: {len(W_GRID)} points ===")
    print(f"  grid: {W_GRID}")
    print(f"  seeds: {SEEDS}, quick: {QUICK}")
    print(f"  cache: {CACHE_DIR}")
    print()
    rows = run_sweep()

    summary = {
        "analysis": "01_w_split_profile",
        "grid": W_GRID,
        "seeds": SEEDS,
        "quick": QUICK,
        "rows": rows,
    }
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("w") as f:
        json.dump(summary, f, indent=2, default=float)
    print()
    print(f"=== Summary ===")
    print(f"{'W_split':>8} | {'cost':>8} | {'R2_G1':>7} | {'R2_G2':>7} | "
          f"{'recalc_n':>8} | {'fib_n':>6} | {'xiii_n':>6}")
    print("-" * 70)
    for r in rows:
        f = r["achieved_fractions"]
        print(f"{r['W_split']:>8.2f} | {r['cost']:>8.4f} | "
              f"{r['avg_r2_g1']:>7.4f} | {r['avg_r2_g2']:>7.4f} | "
              f"{f['recalc_neutro_frac']:>8.3f} | {f['fib_neutro_frac']:>6.3f} | "
              f"{f['xiii_neutro_frac']:>6.3f}")
    print()
    print(f"Saved -> {RESULTS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
