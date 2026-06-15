"""Figure 4: myelosan dose-response phase diagram (manuscript §3.5).

Three panels over the (km, tm) modifier grid, from the 100-member bootstrap
ensemble: two severity outcomes (peak hypocoagulation max Δrecalc; factor XIII
depletion nadir min ΔXIII) and one mechanistic driver (peak neutrophil load
max gHn). The driver panel illustrates the §3.5 thesis that myelosan acts by
reducing neutrophil load. Reference points: no-myelosan (1,1) and the observed
G2 operating point (km=4.93, tm=0.43).

Replaces the earlier 3-panel figure whose third panel was the defunct
liver_collapse metric (removed; Hn/Hm threshold was 0 by construction).

Output: figures/fig4_phase_diagram.{png,pdf}
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ANALYSIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ANALYSIS_DIR / "results"
FIG_DIR = ANALYSIS_DIR / "figures"
REPO = ANALYSIS_DIR.parent.parent

sys.path.insert(0, str(REPO))
from analyses._fig_style import apply_style, save_fig, panel_label  # noqa: E402

KM_BASELINE_G2 = 4.93
TM_BASELINE_G2 = 0.43

# (metric, panel title, colormap). magma/_r are perceptually uniform.
PANELS = [
    ("max_recalc", "(a)", "Peak hypocoagulation\n(max " + r"$\Delta$recalc, s)", "magma"),
    ("min_xiii", "(b)", "Factor XIII nadir\n(min " + r"$\Delta$XIII, %)", "magma_r"),
    ("max_gHn", "(c)", "Peak neutrophil load\n(max gHn)", "viridis"),
]


def load_phase(metric):
    return json.loads((RESULTS_DIR / f"phase_diagram_{metric}.json").read_text())


def main():
    apply_style()

    fig, axes = plt.subplots(1, 3, figsize=(180 / 25.4, 62 / 25.4))

    for ax, (metric, lbl, title, cmap) in zip(axes, PANELS):
        phase = load_phase(metric)
        km = np.array(phase["km_grid"])
        tm = np.array(phase["tm_grid"])
        Z = np.array(phase["median"])  # shape (km, tm)

        im = ax.pcolormesh(tm, km, Z, cmap=cmap, shading="auto",
                           vmin=float(np.nanmin(Z)), vmax=float(np.nanmax(Z)))
        ax.set_xscale("log")
        ax.set_yscale("log")
        # explicit ticks with clean labels (log minor labels overlap on
        # the narrow tm range)
        from matplotlib.ticker import FixedLocator, NullLocator, ScalarFormatter
        ax.xaxis.set_major_locator(FixedLocator([0.2, 0.5, 1.0]))
        ax.xaxis.set_minor_locator(NullLocator())
        ax.xaxis.set_major_formatter(ScalarFormatter())
        ax.yaxis.set_major_locator(FixedLocator([1, 2, 5, 10]))
        ax.yaxis.set_minor_locator(NullLocator())
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.set_xlabel(r"$t_m$ (timing modifier)")
        if ax is axes[0]:
            ax.set_ylabel(r"$k_m$ (rate modifier)")
        ax.set_title(title, fontsize=8)

        # reference points (neutral: white-edged)
        ax.plot(1.0, 1.0, marker="o", color="white", ms=7, mec="black",
                mew=1.0, zorder=5, label="No kinetic modification (k_m=t_m=1)")
        ax.plot(TM_BASELINE_G2, KM_BASELINE_G2, marker="*", color="white",
                ms=12, mec="black", mew=1.0, zorder=5,
                label="G2 observed")

        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.ax.tick_params(labelsize=7)

        # severity contours on the peak-hypocoagulation panel
        if metric == "max_recalc":
            try:
                cs = ax.contour(tm, km, Z, levels=[10, 20, 30, 40],
                                colors="white", linewidths=0.6, alpha=0.6)
                ax.clabel(cs, inline=True, fontsize=6, fmt="%d")
            except Exception:
                pass

        panel_label(ax, lbl, color="white")

    # one shared legend below
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False,
               bbox_to_anchor=(0.5, -0.04), fontsize=8)

    fig.tight_layout(rect=[0, 0.04, 1, 1])
    png, pdf = save_fig(fig, FIG_DIR, "fig4_phase_diagram")
    plt.close(fig)
    print(f"Saved: {png}")
    print(f"Saved: {pdf}")
    for metric, _, _, _ in PANELS:
        Z = np.array(load_phase(metric)["median"])
        print(f"  {metric:11s} median range: {float(np.nanmin(Z)):.2f} "
              f"- {float(np.nanmax(Z)):.2f}")


if __name__ == "__main__":
    main()
