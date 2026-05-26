"""Figure 6: therapeutic window — severity vs intervention timing (§3.6).

Three severity metrics versus the myelosan intervention time, from the
100-member bootstrap ensemble: peak hypocoagulation (max Δrecalc), factor XIII
nadir (min ΔXIII), and peak neutrophil load (max gHn). Median + 95% CI band.
The critical transition (days 2.5-3, where severity roughly doubles) is
shaded. The no-intervention level is drawn as a reference ceiling on each
panel. Together the panels show the whole syndrome shares one therapeutic
window: a prevention phase (0-2.5 d) and a mitigation phase (2.5-6+ d).

Output: figures/fig6_severity_vs_timing.{png,pdf}
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
from analyses._fig_style import (apply_style, C_G1, despine,  # noqa: E402
                                 panel_label, save_fig)

TRANSITION = (2.5, 3.0)  # critical half-day transition

# (metric key, panel label, y-axis label)
PANELS = [
    ("max_recalc", "(a)", r"Peak hypocoag. (max $\Delta$recalc, s)"),
    ("min_xiii", "(b)", r"Factor XIII nadir (min $\Delta$XIII, %)"),
    ("max_gHn", "(c)", r"Peak neutrophil load (max gHn)"),
]


def main():
    apply_style()
    data = json.loads((RESULTS_DIR / "summary_by_timing.json").read_text())

    # split timed scenarios from the no-intervention reference
    timed = [e for e in data if e["t_intervention"] is not None]
    noint = next(e for e in data if e["t_intervention"] is None)
    t = np.array([e["t_intervention"] for e in timed])

    fig, axes = plt.subplots(1, 3, figsize=(180 / 25.4, 66 / 25.4))

    for ax, (key, lbl, ylab) in zip(axes, PANELS):
        med = np.array([e[key]["median"] for e in timed])
        lo = np.array([e[key]["p2_5"] for e in timed])
        hi = np.array([e[key]["p97_5"] for e in timed])
        noint_med = noint[key]["median"]

        # critical transition band
        ax.axvspan(TRANSITION[0], TRANSITION[1], color="0.5", alpha=0.15,
                   lw=0, zorder=0)
        # CI band + median
        ax.fill_between(t, lo, hi, color=C_G1, alpha=0.18, lw=0, zorder=2)
        ax.plot(t, med, "-o", color=C_G1, ms=3.5, lw=1.4, zorder=3)
        # no-intervention ceiling
        ax.axhline(noint_med, color="0.5", lw=0.9, ls=":", zorder=1)

        ax.set_xlabel("Intervention time (days)")
        ax.set_ylabel(ylab)
        ax.set_xlim(-0.3, 6.3)
        despine(ax)
        panel_label(ax, lbl)

    # annotate the no-intervention reference once (leftmost panel)
    axes[0].annotate("no intervention", xy=(6.0, noint["max_recalc"]["median"]),
                     xytext=(2.4, noint["max_recalc"]["median"] + 2),
                     fontsize=7, color="0.4", va="bottom")

    fig.tight_layout()
    png, pdf = save_fig(fig, FIG_DIR, "fig6_severity_vs_timing")
    plt.close(fig)
    print(f"Saved: {png}")
    print(f"Saved: {pdf}")
    print("max_recalc median by timing:")
    for e in timed:
        print(f"  t={e['t_intervention']:.1f}: {e['max_recalc']['median']:.2f} s")
    print(f"  no-intervention: {noint['max_recalc']['median']:.2f} s")
    print(f"transition: t=2.5 -> t=3.0: "
          f"{timed[3]['max_recalc']['median']:.2f} -> "
          f"{timed[4]['max_recalc']['median']:.2f} s")


if __name__ == "__main__":
    main()
