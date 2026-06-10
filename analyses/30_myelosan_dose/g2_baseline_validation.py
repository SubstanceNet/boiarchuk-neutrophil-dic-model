# g2_baseline_validation.py -- Q16: code source of truth for the S6.1 table.
#
# Lives at: analyses/30_myelosan_dose/g2_baseline_validation.py
# Writes to: ./results/g2_baseline_validation.json (relative to this script).
# Replaces the previous manual extraction of S6.1 internal-validation numbers
# from phase_diagram_*.json. Computes model severity at the exact fitted dose
# (km=4.93, tm=0.43) on the good-basin subset, alongside observed G2 from CSV.
from __future__ import annotations
import json
import numpy as np
from pathlib import Path

from src import config as cfg
from src.data import load_data, build_neutrophil_interpolators
from src.model import solve_group
from src.ensemble import load_ensemble, good_basin_mask as compute_good_basin_mask

OUT = Path(__file__).parent / "results"
OUT.mkdir(parents=True, exist_ok=True)

# G2 baseline cell (exact fitted dose)
KM, TM = 4.93, 0.43


def severity(o, T):
    recalc = np.asarray(o["recalc"]); xiii = np.asarray(o["xiii"])
    return dict(
        max_recalc=float(np.max(recalc)),
        min_xiii=float(np.min(xiii)),
        auc_recalc=float(np.trapezoid(np.abs(recalc), T)),
    )


def main():
    g1, g2 = load_data()
    _, n2 = build_neutrophil_interpolators(g1, g2)
    tfg2 = np.linspace(0.0, float(g2.T[-1]), 200)

    ens = load_ensemble()
    gb = compute_good_basin_mask(ens, g2.xiii)
    members = [m["best_x"] for m, keep in zip(ens, gb) if keep]
    print(f"ensemble: {len(ens)} total, {int(gb.sum())} good basin -> using good basin only")

    # MODEL: G2-baseline cell (km=4.93, tm=0.43), across the ensemble
    mx, mn, au = [], [], []
    for pv in members:
        o = solve_group(pv, g2.T, n2, tfg2, pv[1] * KM, pv[8] * TM)
        if o is None:
            continue
        s = severity(o, g2.T)
        mx.append(s["max_recalc"]); mn.append(s["min_xiii"]); au.append(s["auc_recalc"])

    def stat(v):
        v = [x for x in v if np.isfinite(x)]
        return dict(median=float(np.median(v)), p2_5=float(np.percentile(v, 2.5)),
                    p97_5=float(np.percentile(v, 97.5)), n=len(v))

    model = dict(max_recalc=stat(mx), min_xiii=stat(mn), auc_recalc=stat(au))

    # OBSERVED G2 (from data, on the same g2.T grid) -- computed from CSV, not by hand
    obs_recalc = np.asarray(g2.recalc); obs_xiii = np.asarray(g2.xiii)
    observed = dict(
        max_recalc=float(np.max(obs_recalc)),
        min_xiii=float(np.min(obs_xiii)),
        auc_recalc=float(np.trapezoid(np.abs(obs_recalc), g2.T)),
    )

    print("=== S6.1 G2-baseline internal validation (km=4.93, tm=0.43) ===")
    print(f"{'metric':>12} | {'observed':>10} | {'model median':>13} | {'95% CI':>22}")
    for k in ("max_recalc", "min_xiii", "auc_recalc"):
        ci = f"[{model[k]['p2_5']:.2f}, {model[k]['p97_5']:.2f}]"
        print(f"{k:>12} | {observed[k]:>10.2f} | {model[k]['median']:>13.2f} | {ci:>22}")

    payload = dict(km=KM, tm=TM, n_members=len(members),
                   model=model, observed=observed, grid_points=len(tfg2))
    (OUT / "g2_baseline_validation.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"\nsaved: {OUT/'g2_baseline_validation.json'}")
    print("\nCompare 'observed' with the S6.1 numbers (9.10 / -9.30 / 70.55).")
    print("If they do not match, the source/grid behind the table must be revisited.")


if __name__ == "__main__":
    main()
