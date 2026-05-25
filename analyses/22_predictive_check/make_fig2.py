"""Figure 2: identifiability and uncertainty (manuscript §3.2).

Two panels (shared style):
  (a) R² forest plot — median + 95% CI for all 6 observables x 2 groups
      (12 rows). Most channels are tight and high; xiii_G2 is the lone
      wide interval crossing R²=0.
  (b) xiii_G2 R² distribution across the 100-member bootstrap ensemble,
      with the fraction below 0 computed from these same members.

R² is computed via aggregate.compute_per_iter_r2 (the SAME function that
produced ensemble.json), so panel (b) and panel (a) share one source of truth.

Output: figures/fig2_identifiability.{png,pdf}
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ANALYSIS_DIR = Path(__file__).resolve().parent
RESULTS = ANALYSIS_DIR / "results"
FIG_DIR = ANALYSIS_DIR / "figures"
REPO = ANALYSIS_DIR.parent.parent

sys.path.insert(0, str(REPO))
from src.data import load_data  # noqa: E402
from analyses._fig_style import (apply_style, C_G1, C_G2, despine,  # noqa: E402
                                 panel_label, save_fig)

OBS_KEYS = ["recalc", "thrombin", "fib", "xiii", "AP", "D"]
OBS_LABEL = {"recalc": "Recalc.", "thrombin": "Thrombin", "fib": "Fibrinogen",
             "xiii": "Factor XIII", "AP": "Acid phosph.", "D": "Degranul."}


def _import_aggregate():
    """Import compute_per_iter_r2 from aggregate.py without running its main."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "agg22", ANALYSIS_DIR / "aggregate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.compute_per_iter_r2


def main():
    apply_style()
    compute_per_iter_r2 = _import_aggregate()

    ens = json.loads((RESULTS / "ensemble.json").read_text())
    raw = json.loads((RESULTS / "ensemble_raw.json").read_text())
    iters = raw["iter_records"]
    g1, g2 = load_data()

    # per-member R² (same function as aggregate.py)
    r2_records = compute_per_iter_r2(iters, g1, g2)
    xiii_g2_vals = np.array([r["r2_g2"]["xiii"] for r in r2_records], dtype=float)
    xiii_g2_vals = xiii_g2_vals[np.isfinite(xiii_g2_vals)]
    frac_below0 = float(np.mean(xiii_g2_vals < 0.0))
    n_used = xiii_g2_vals.size

    fig, (axA, axB) = plt.subplots(
        1, 2, figsize=(180 / 25.4, 90 / 25.4),
        gridspec_kw=dict(width_ratios=[1.5, 1.0]))

    # ---- panel (a): R² forest plot, 12 rows ----
    rows = []  # (y, median, lo, hi, color, marker, group)
    y = 0
    for k in OBS_KEYS:
        for grp, ci_key, color, marker in (
                ("I", "r2_g1", C_G1, "o"), ("II", "r2_g2", C_G2, "^")):
            ci = ens[ci_key][k]
            rows.append((y, ci["p50.0"], ci["p2.5"], ci["p97.5"],
                         color, marker, grp))
            y += 1
        y += 0.6  # gap between observables

    axA.axvline(0.0, color="0.6", lw=0.8, zorder=1)
    axA.axvline(1.0, color="0.8", lw=0.8, ls=":", zorder=1)
    yticks, ylabels = [], []
    for (yy, med, lo, hi, color, marker, grp) in rows:
        axA.plot([lo, hi], [yy, yy], "-", color=color, lw=1.0, zorder=2)
        axA.plot([med], [yy], marker, color=color, ms=5, mfc=color,
                 mec=color, zorder=3)
        yticks.append(yy)
        ylabels.append("")
    # observable labels at the midpoint of each G1/G2 pair
    pair_y = [rows[i][0] + 0.5 for i in range(0, len(rows), 2)]
    axA.set_yticks(pair_y)
    axA.set_yticklabels([OBS_LABEL[k] for k in OBS_KEYS])
    axA.set_xlabel(r"Coefficient of determination $R^2$")
    axA.set_xlim(-1.15, 1.05)
    axA.invert_yaxis()
    panel_label(axA, "(a)")
    despine(axA)
    # legend proxies
    from matplotlib.lines import Line2D
    axA.legend(handles=[
        Line2D([0], [0], color=C_G1, marker="o", ls="-", ms=5, label="Group I"),
        Line2D([0], [0], color=C_G2, marker="^", ls="-", ms=5, label="Group II"),
    ], loc="lower left", frameon=False)

    # ---- panel (b): xiii_G2 R² histogram ----
    axB.hist(xiii_g2_vals, bins=18, color=C_G2, alpha=0.8, edgecolor="white",
             linewidth=0.4, zorder=2)
    axB.axvline(0.0, color="0.2", lw=1.0, zorder=3)
    axB.set_xlabel(r"Factor XIII (Group II) $R^2$")
    axB.set_ylabel("Bootstrap members")
    axB.annotate(f"{frac_below0*100:.0f}% < 0  (n={n_used})",
                 xy=(0.04, 0.96), xycoords="axes fraction",
                 va="top", ha="left", fontsize=8)
    panel_label(axB, "(b)")
    despine(axB)

    fig.tight_layout()
    png, pdf = save_fig(fig, FIG_DIR, "fig2_identifiability")
    plt.close(fig)
    print(f"Saved: {png}")
    print(f"Saved: {pdf}")
    print(f"(caption: median +/- 95% CI from {raw['n_iters']}-member bootstrap; "
          f"xiii_G2 R2 < 0 in {frac_below0*100:.0f}% of {n_used} members)")


if __name__ == "__main__":
    main()
