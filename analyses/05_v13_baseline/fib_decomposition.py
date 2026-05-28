"""Fibrinogen channel decomposition at the v13 baseline fit.

Documents the origin of two fib-channel artifacts visible in Figure 1:
  (1) underestimation of the early (hypercoagulation) fibrinogen rise, and
  (2) a non-monotonic "bump" in the model curve around days 5-7 (G1).

The fib observable is fib = +af*V + cf*AP - bf*gHn - df*Hc. Near days 5-7
the model output (~ -10) is a small difference of two large opposing terms,
cf*AP (~ +37) and -bf*gHn (~ -40), each ~4x larger in magnitude than their
sum. Small phase mismatches between AP and gHn therefore produce a
non-monotonic intermediate profile (catastrophic cancellation). The same
fast-rising -bf*gHn term suppresses the early fibrinogen rise relative to
observation. This is a known limitation of the fib channel; it is localized
to the early/intermediate phase and does not affect the channels that carry
the main findings. The late nadir is reproduced well (model -58 vs obs -53).

This is diagnostics on the FIXED baseline (analysis 05) — not a model change.

Output: results/fib_decomposition.json (terms on a dense grid + summary).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids, solve_group

ANALYSIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ANALYSIS_DIR / "results"


def main():
    g1, g2 = load_data()
    n1, n2 = build_neutrophil_interpolators(g1, g2)
    tfg1, tfg2 = make_fine_grids()
    pv = np.array(json.loads((RESULTS_DIR / "fit.json").read_text())["best_x"])

    af, cf, bf, df = pv[16], pv[17], pv[18], pv[19]

    t = np.linspace(0, 14, 29)
    o = solve_group(pv, t, n1, tfg1, pv[1], pv[8])
    V = np.asarray(o["V"]); AP = np.asarray(o["AP"])
    gHn = np.asarray(o["gHn"]); Hc = np.asarray(o["Hc"])
    fib = np.asarray(o["fib"])

    term_V = af * V
    term_AP = cf * AP
    term_gHn = -bf * gHn
    term_Hc = -df * Hc

    print(f"Fib decomposition: fib = +af*V + cf*AP - bf*gHn - df*Hc")
    print(f"af={af:.3f} cf={cf:.3f} bf={bf:.3f} df={df:.3f}\n")
    print(f"{'t':>5} {'af*V':>9} {'cf*AP':>9} {'-bf*gHn':>9} {'-df*Hc':>9} "
          f"{'sum':>9} {'data':>8}")
    rows = []
    for i, ti in enumerate(t):
        j = np.argmin(np.abs(g1.T - ti))
        d = float(g1.fib[j]) if abs(g1.T[j] - ti) < 0.6 else None
        print(f"{ti:5.1f} {term_V[i]:9.2f} {term_AP[i]:9.2f} {term_gHn[i]:9.2f} "
              f"{term_Hc[i]:9.2f} {fib[i]:9.2f} {('%.1f' % d) if d is not None else '':>8}")
        rows.append(dict(t=float(ti), V=float(term_V[i]), AP=float(term_AP[i]),
                         gHn=float(term_gHn[i]), Hc=float(term_Hc[i]),
                         fib=float(fib[i]), data=d))

    # quantify the cancellation around the bump (days 4.5-6.5)
    win = (t >= 4.5) & (t <= 6.5)
    ap_mag = float(np.mean(np.abs(term_AP[win])))
    ghn_mag = float(np.mean(np.abs(term_gHn[win])))
    sum_mag = float(np.mean(np.abs(fib[win])))
    ratio = (ap_mag + ghn_mag) / 2 / max(sum_mag, 1e-9)

    # early-phase underestimation (days 1-2)
    early = []
    for ti in (1.0, 2.0):
        i = int(np.argmin(np.abs(t - ti)))
        j = int(np.argmin(np.abs(g1.T - ti)))
        early.append(dict(t=ti, model=float(fib[i]), data=float(g1.fib[j])))

    summary = dict(
        coeffs=dict(af=float(af), cf=float(cf), bf=float(bf), df=float(df)),
        bump_window="days 4.5-6.5",
        mean_abs_AP_term=ap_mag,
        mean_abs_gHn_term=ghn_mag,
        mean_abs_fib=sum_mag,
        cancellation_ratio=float(ratio),
        early_phase=early,
        nadir_model=float(np.min(fib)),
        nadir_obs=-52.6,
        note=("Bump is catastrophic cancellation of cf*AP (~+37) and -bf*gHn "
              "(~-40); each term ~%.1fx the sum magnitude in the window. Early "
              "rise underestimated by the fast-rising -bf*gHn term." % ratio),
    )

    out = dict(grid=rows, summary=summary)
    (RESULTS_DIR / "fib_decomposition.json").write_text(json.dumps(out, indent=2))
    print(f"\ncancellation ratio (mean |large term| / |sum|) in days 4.5-6.5: "
          f"{ratio:.1f}x")
    print(f"early underestimation: " +
          ", ".join(f"t={e['t']:.0f} model {e['model']:.0f} vs data {e['data']:.0f}"
                    for e in early))
    print(f"Saved: {RESULTS_DIR / 'fib_decomposition.json'}")


if __name__ == "__main__":
    main()
