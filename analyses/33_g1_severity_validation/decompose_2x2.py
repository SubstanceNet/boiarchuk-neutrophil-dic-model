# decompose_2x2.py -- Q1: isolating 2x2 decomposition (neutrophil profile x kinetic modifier).
#
# Lives at: analyses/33_g1_severity_validation/decompose_2x2.py
# Writes to: ./results/decompose_2x2.json (relative to this script).
# Source for: S6.5 (2x2 decomposition table) and the count-vs-kinetics framing
# in 3.5/4.3 of the main text. Runs on the good-basin subset (R2_G2(XIII) >= 0.3),
# consistent with S6.5; per-member km, tm come from pv[24], pv[25] of each fitted member.
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


def severity(o, T):
    recalc = np.asarray(o["recalc"]); gHn = np.asarray(o["gHn"]); xiii = np.asarray(o["xiii"])
    return dict(
        max_recalc=float(np.max(recalc)),
        auc_recalc=float(np.trapezoid(np.abs(recalc), T)),
        max_gHn=float(np.max(gHn)),
        min_xiii=float(np.min(xiii)),
    )


def main():
    g1, g2 = load_data()
    n1, n2 = build_neutrophil_interpolators(g1, g2)
    tfg1 = np.linspace(0.0, float(g1.T[-1]), 250)
    tfg2 = np.linspace(0.0, float(g2.T[-1]), 200)

    ens = load_ensemble()
    gb = compute_good_basin_mask(ens, g2.xiii)
    members = [m["best_x"] for m, keep in zip(ens, gb) if keep]
    print(f"ensemble: {len(ens)} total, {int(gb.sum())} good basin -> using good basin only")

    # Four 2x2 cells: (profile G1/G2) x (kinetics off / G2-on).
    # kin_on=True takes per-member fitted km, tm from pv[24], pv[25].
    cells = {
        "G1_profile__kin_off": dict(T=g1.T, n=n1, tf=tfg1, kin_on=False),
        "G1_profile__kin_ON":  dict(T=g1.T, n=n1, tf=tfg1, kin_on=True),   # <-- isolating cell
        "G2_profile__kin_off": dict(T=g2.T, n=n2, tf=tfg2, kin_on=False),
        "G2_profile__kin_ON":  dict(T=g2.T, n=n2, tf=tfg2, kin_on=True),   # G2 baseline
    }

    results = {k: [] for k in cells}
    for pv in members:
        km_fit, tm_fit = float(pv[24]), float(pv[25])
        for name, c in cells.items():
            km = km_fit if c["kin_on"] else 1.0
            tm = tm_fit if c["kin_on"] else 1.0
            o = solve_group(pv, c["T"], c["n"], c["tf"], pv[1] * km, pv[8] * tm)
            if o is None or any(np.any(np.isnan(np.asarray(o[k]))) for k in ("recalc", "gHn", "xiii")):
                continue
            results[name].append(severity(o, c["T"]))

    def med(name, key="max_recalc"):
        vals = [r[key] for r in results[name] if np.isfinite(r[key])]
        return float(np.median(vals)) if vals else float("nan")

    a  = med("G1_profile__kin_off")   # ~150 -- G1 profile, kinetics off
    b  = med("G1_profile__kin_ON")    # isolating: G1 profile + G2 kinetics
    c_ = med("G2_profile__kin_off")   # ~44  -- G2 profile, kinetics off
    d  = med("G2_profile__kin_ON")    # ~7   -- G2 baseline (profile + kinetics)

    print("\n=== 2x2 max_recalc (median, good basin) ===")
    print(f"  [A] G1 profile, kin OFF : {a:8.2f}")
    print(f"  [B] G1 profile, kin ON  : {b:8.2f}   <-- isolating cell")
    print(f"  [C] G2 profile, kin OFF : {c_:8.2f}")
    print(f"  [D] G2 profile, kin ON  : {d:8.2f}")
    print("\n=== isolated effects (max_recalc ratios) ===")
    print(f"  KINETIC @ G1-profile  (A/B, profile fixed=G1)         : {a/b:6.2f}x")
    print(f"  KINETIC @ G2-profile  (C/D, profile fixed=G2)         : {c_/d:6.2f}x")
    print(f"  COUNT   @ kinetics-OFF (A/C, kinetics fixed=off)      : {a/c_:6.2f}x")
    print(f"  COUNT   @ kinetics-ON  (B/D, kinetics fixed=on)       : {b/d:6.2f}x")
    print(f"  TOTAL A/D                                              : {a/d:6.2f}x")
    print("\nInterpretation: if [B] ~ [A] -> count dominates (G2-kinetics without")
    print("reduced count does not rescue). If [B] ~ [D] -> kinetics is sufficient alone.")

    payload = {name: {
        "max_recalc_median": med(name),
        "auc_recalc_median": med(name, "auc_recalc"),
        "max_gHn_median":    med(name, "max_gHn"),
        "min_xiii_median":   med(name, "min_xiii"),
        "n_valid":           len(results[name]),
    } for name in cells}
    payload["_ratios"] = {
        "kinetic_at_G1": a / b,
        "kinetic_at_G2": c_ / d,
        "count_at_off":  a / c_,
        "count_at_on":   b / d,
        "total_A_over_D": a / d,
    }
    (OUT / "decompose_2x2.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"\nsaved: {OUT/'decompose_2x2.json'}")


if __name__ == "__main__":
    main()
