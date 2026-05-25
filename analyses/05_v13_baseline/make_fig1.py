"""Figure 1: baseline model fits vs experimental data, both groups.

6 panels (3 cols x 2 rows), one per observable. Each panel shows G1 and G2
data points (M+/-m error bars) and the baseline-fit model curve. Model curve
drawn only within each group's observed time range (G1 0-19 d, G2 0-8 d) —
no G2 extrapolation. Deltas from baseline (G1 from intact, G2 from state M;
see caption). No bootstrap CI (that is Figure 2).

Output: figures/fig1_baseline_fits.{png,pdf}
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids, solve_group

ANALYSIS_DIR = Path(__file__).resolve().parent
FIG_DIR = ANALYSIS_DIR / "figures"

# ---- style ----
SERIF = "Nimbus Roman"  # metrically Times-compatible, available here
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": [SERIF, "Liberation Serif", "DejaVu Serif"],
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "lines.linewidth": 1.4,
    "figure.dpi": 300,
})

C_G1 = "#2166AC"  # dark blue
C_G2 = "#B2182B"  # dark red
MORT_BAND = (10, 12)  # G1 mortality / hypocoagulation peak

# observable: (attr, panel label, y-axis label)
PANELS = [
    ("recalc", "(a)", r"$\Delta$ Recalcification time (s)", True),
    ("thrombin", "(b)", r"$\Delta$ Thrombin time (s)", True),
    ("fib", "(c)", r"$\Delta$ Fibrinogen (mg%)", True),
    ("xiii", "(d)", r"$\Delta$ Factor XIII activity (%)", True),
    ("AP", "(e)", r"$\Delta$ Acid phosphatase (Bodansky U.)", False),
    ("deg", "(f)", r"$\Delta$ Degranulation index (%)", False),
]
# model output key per attr (deg -> 'D')
MODEL_KEY = {"recalc": "recalc", "thrombin": "thrombin", "fib": "fib",
             "xiii": "xiii", "AP": "AP", "deg": "D"}
# sigma CSV column per attr
SE_COL = {"recalc": "recalc_se", "thrombin": "thrombin_se", "fib": "fib_se",
          "xiii": "xiii_se", "AP": "acid_phosphatase_se", "deg": "degranulation_se"}


def _load_sigma(path):
    """Load a sigma_group CSV ('#' comments) -> dict col -> ndarray."""
    import numpy as _np
    with open(path) as f:
        lines = [ln for ln in f if not ln.lstrip().startswith("#") and ln.strip()]
    header = lines[0].strip().split(",")
    rows = [ln.strip().split(",") for ln in lines[1:]]
    arr = _np.asarray(rows, dtype=float)
    return {name: arr[:, i] for i, name in enumerate(header)}


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    g1, g2 = load_data()
    n1, n2 = build_neutrophil_interpolators(g1, g2)
    tfg1, tfg2 = make_fine_grids()

    fit = json.loads((ANALYSIS_DIR / "results" / "fit.json").read_text())
    pv = np.array(fit["best_x"])
    r2_g1 = fit.get("avg_r2_g1")
    r2_g2 = fit.get("avg_r2_g2")

    # measurement SEM (M+/-m) for error bars
    DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "csv"
    se1 = _load_sigma(DATA_DIR / "sigma_group1.csv")
    se2 = _load_sigma(DATA_DIR / "sigma_group2.csv")

    # dense model curves on each group's own range (no extrapolation)
    tdense_g1 = np.linspace(0, 19, 300)
    tdense_g2 = np.linspace(0, 8, 200)
    o1 = solve_group(pv, tdense_g1, n1, tfg1, pv[1], pv[8])
    o2 = solve_group(pv, tdense_g2, n2, tfg2, pv[1] * pv[24], pv[8] * pv[25])

    # crude per-point error bars: not in CSV, so omit if unavailable.
    # We plot data points without error bars unless a sigma source exists.
    fig, axes = plt.subplots(2, 3, figsize=(180 / 25.4, 120 / 25.4))
    axes = axes.ravel()

    for ax, (attr, lbl, ylab, show_mort) in zip(axes, PANELS):
        mkey = MODEL_KEY[attr]
        d1 = getattr(g1, attr)
        d2 = getattr(g2, attr)

        # mortality band (G1-relevant panels only), under everything
        if show_mort:
            ax.axvspan(MORT_BAND[0], MORT_BAND[1], color="0.5",
                       alpha=0.15, lw=0, zorder=0)

        # data points with SEM error bars
        e1 = se1[SE_COL[attr]]
        e2 = se2[SE_COL[attr]]
        ax.errorbar(g1.T, d1, yerr=e1, fmt="o", color=C_G1, ms=4,
                    mfc=C_G1, mec=C_G1, ecolor=C_G1, elinewidth=0.7,
                    capsize=1.8, capthick=0.7, zorder=3, label="Group I (data)")
        ax.errorbar(g2.T, d2, yerr=e2, fmt="^", color=C_G2, ms=4,
                    mfc=C_G2, mec=C_G2, ecolor=C_G2, elinewidth=0.7,
                    capsize=1.8, capthick=0.7, zorder=3, label="Group II (data)")

        # model curves (within range only)
        ax.plot(tdense_g1, np.array(o1[mkey]), "-", color=C_G1, lw=1.4,
                zorder=2, label="Group I (model)")
        ax.plot(tdense_g2, np.array(o2[mkey]), "--", color=C_G2, lw=1.4,
                zorder=2, label="Group II (model)")

        ax.axhline(0, color="0.7", lw=0.6, zorder=1)
        ax.set_ylabel(ylab)
        ax.set_xlim(-0.5, 19.5)
        ax.set_xticks([0, 5, 10, 15])
        ax.text(0.97, 0.95, lbl, transform=ax.transAxes, fontweight="bold",
                fontsize=10, va="top", ha="right")
        # x-label only on bottom row
        ax.set_xlabel("Time (days)")
        ax.tick_params(direction="out", length=3)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)

    # shared legend (one), below the panels
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4,
               frameon=False, bbox_to_anchor=(0.5, -0.02))

    fig.tight_layout(rect=[0, 0.04, 1, 1])

    png = FIG_DIR / "fig1_baseline_fits.png"
    pdf = FIG_DIR / "fig1_baseline_fits.pdf"
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {png}")
    print(f"Saved: {pdf}")
    print(f"(caption: mean R2 G1={r2_g1:.2f}, G2={r2_g2:.2f}; "
          f"deltas from baseline — G1 intact, G2 state M)")


if __name__ == "__main__":
    main()
