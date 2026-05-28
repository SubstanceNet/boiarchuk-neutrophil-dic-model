"""Figure 3: mechanism-split decomposition (manuscript §3.3).

Neutrophil-attributable fraction of three coagulation channels (recalc, fib,
factor XIII) at Group I day 2. Median + 95% CI from the 100-member bootstrap
(analysis 22 ensemble.json). Dashed vertical lines mark the prior targets
(config.NEUTRO_FRAC), imposed as soft constraints (W_SPLIT). The decomposition
is PRIOR-REGULARIZED, not a free data inference: narrow CIs reflect both data
consistency and prior strength; the figure is read together with §3.3, which
explains the prior derivation and held-out validation.

Both the medians/CIs (ensemble.json) and the prior targets (config.py) are
read at runtime — no number is hard-coded here.

Output: figures/fig3_mechanism_split.{png,pdf}
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
from src.config import NEUTRO_FRAC  # noqa: E402  (prior targets, source of truth)
from analyses._fig_style import (apply_style, C_G2, despine,  # noqa: E402
                                 panel_label, save_fig)

# display order (top to bottom) + labels
CHANNELS = [
    ("recalc", "Recalcification\ntime"),
    ("fib", "Fibrinogen"),
    ("xiii", "Factor XIII"),
]


def main():
    apply_style()
    ens = json.loads((RESULTS / "ensemble.json").read_text())
    ms = ens["mechanism_split"]

    fig, ax = plt.subplots(figsize=(120 / 25.4, 70 / 25.4))

    ys = list(range(len(CHANNELS)))[::-1]  # top channel highest y
    # prior targets as full-height reference lines (standard forest-plot
    # convention): each line passes through its own channel's row at the
    # correct x; on other rows the CI is far away, so there is no ambiguity.
    for key, _label in CHANNELS:
        ax.axvline(NEUTRO_FRAC[key], ls="--", color="0.4", lw=0.9,
                   alpha=0.4, zorder=1)
    for y, (key, _label) in zip(ys, CHANNELS):
        med = ms[key]["p50.0"]
        lo, hi = ms[key]["p2.5"], ms[key]["p97.5"]
        # 95% CI bar
        ax.plot([lo, hi], [y, y], "-", color=C_G2, lw=1.3, zorder=3)
        ax.plot([med], [y], "o", color=C_G2, ms=6, mfc=C_G2, mec="white",
                mew=0.6, zorder=4)

    ax.set_yticks(ys)
    ax.set_yticklabels([lbl for _k, lbl in CHANNELS])
    ax.set_xlabel("Neutrophil-attributable fraction")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-0.6, len(CHANNELS) - 0.4)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    despine(ax)

    # legend: median+CI vs prior target
    from matplotlib.lines import Line2D
    ax.legend(handles=[
        Line2D([0], [0], color=C_G2, marker="o", ls="-", ms=6, mec="white",
               mew=0.6, label="Median, 95% CI (bootstrap)"),
        Line2D([0], [0], color="0.4", ls="--", lw=0.9, alpha=0.6,
               label="Prior target"),
    ], loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2,
       frameon=False, fontsize=8)

    fig.tight_layout(rect=[0, 0.06, 1, 1])
    png, pdf = save_fig(fig, FIG_DIR, "fig3_mechanism_split")
    plt.close(fig)
    print(f"Saved: {png}")
    print(f"Saved: {pdf}")
    print("medians (ensemble) vs prior targets (config):")
    for key, _ in CHANNELS:
        print(f"  {key:7s} median={ms[key]['p50.0']:.3f}  "
              f"CI=[{ms[key]['p2.5']:.3f}, {ms[key]['p97.5']:.3f}]  "
              f"prior={NEUTRO_FRAC[key]:.2f}")


if __name__ == "__main__":
    main()
