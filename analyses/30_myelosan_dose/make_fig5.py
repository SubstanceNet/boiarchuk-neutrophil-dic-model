"""Figure 5: myelosan dose-response slice (manuscript §3.5).

Peak hypocoagulation (max Δrecalc) versus the rate modifier km at fixed timing
modifier tm ≈ 0.447 (nearest grid value to the observed G2 tm = 0.43), from the
100-member bootstrap ensemble. Adds what the Figure 4 heatmaps cannot show:
the bootstrap CI band (p2.5-p97.5) along the dose axis. Markers indicate the
no-myelosan level (km=1) and the observed G2 operating point (km=4.93).

Output: figures/fig5_dose_response_slice.{png,pdf}
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
from analyses._fig_style import apply_style, C_G1, C_G2, despine, save_fig  # noqa: E402

KM_BASELINE_G2 = 4.93
TM_OBSERVED = 0.43


def main():
    apply_style()
    d = json.loads((RESULTS_DIR / "phase_diagram_max_recalc.json").read_text())
    km = np.array(d["km_grid"])
    tm = np.array(d["tm_grid"])
    j = int(np.argmin(np.abs(tm - TM_OBSERVED)))
    tm_used = float(tm[j])

    med = np.array(d["median"])[:, j]
    lo = np.array(d["p2_5"])[:, j]
    hi = np.array(d["p97_5"])[:, j]

    fig, ax = plt.subplots(figsize=(120 / 25.4, 80 / 25.4))

    # CI band + median dose-response curve
    ax.fill_between(km, lo, hi, color=C_G1, alpha=0.18, lw=0,
                    label="95% CI (bootstrap)")
    ax.plot(km, med, "-", color=C_G1, lw=1.6, label="Median")

    # no-myelosan level (km=1) reference
    ax.axhline(med[0], color="0.7", lw=0.7, ls=":", zorder=1)
    ax.annotate("k_m=1 (no rate modification)", xy=(km[0], med[0]), xytext=(km[0] + 0.3, med[0] - 6),
                fontsize=7, color="0.4", va="top")

    # observed G2 operating point (km=4.93)
    ax.axvline(KM_BASELINE_G2, color=C_G2, lw=1.0, ls="--", zorder=2)
    # interpolate median severity at the observed km for the marker
    sev_at_g2 = float(np.interp(KM_BASELINE_G2, km, med))
    ax.plot([KM_BASELINE_G2], [sev_at_g2], "^", color=C_G2, ms=7, mfc=C_G2,
            mec="white", mew=0.6, zorder=4, label=f"G2 dose (km={KM_BASELINE_G2})")

    ax.set_xlabel(r"$k_m$ (rate modifier)")
    ax.set_ylabel(r"Peak hypocoagulation (max $\Delta$recalc, s)")
    ax.set_xlim(km.min(), km.max())
    ax.set_ylim(bottom=-3)
    despine(ax)
    ax.legend(loc="upper right", frameon=False, fontsize=7.5)

    fig.tight_layout()
    png, pdf = save_fig(fig, FIG_DIR, "fig5_dose_response_slice")
    plt.close(fig)
    print(f"Saved: {png}")
    print(f"Saved: {pdf}")
    print(f"tm used: {tm_used:.3f} (nearest grid to observed {TM_OBSERVED})")
    print(f"median severity at km=1 (no myelosan): {med[0]:.1f} s")
    print(f"median severity at G2 km={KM_BASELINE_G2}: {sev_at_g2:.1f} s")
    print(f"CI width at km=1: [{lo[0]:.1f}, {hi[0]:.1f}]; "
          f"at km~5: [{np.interp(5,km,lo):.1f}, {np.interp(5,km,hi):.1f}]")


if __name__ == "__main__":
    main()
