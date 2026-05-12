"""Generate manuscript figures for analysis 30 myelosan dose-response."""
from __future__ import annotations
import json
import pickle
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

ANALYSIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ANALYSIS_DIR / "results"
FIGURES_DIR = ANALYSIS_DIR / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

# Load raw and aggregated data
raw = pickle.loads((RESULTS_DIR / "ensemble_predictions_raw.pkl").read_bytes())
km_grid = np.array(raw["km_grid"])
tm_grid = np.array(raw["tm_grid"])
preds = raw["predictions"]

N_GRID = len(km_grid)
KM_BASELINE_G2 = 4.93
TM_BASELINE_G2 = 0.43


def load_phase(metric):
    return json.loads((RESULTS_DIR / f"phase_diagram_{metric}.json").read_text())


# Build numpy arrays from phase data
def to_array(phase, key):
    arr = np.array(phase[key])
    return arr


# ============================================================
# FIGURE 1: 3-panel phase diagram (max_recalc, min_xiii, liver_collapse)
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

metric_specs = [
    ("max_recalc", "Peak hypocoagulation\n(max Δrecalc)", "magma", None),
    ("min_xiii", "XIII depletion nadir\n(min ΔXIII)", "magma_r", None),
    ("liver_collapse", "Liver collapse fraction\n(Hn/Hm > 0.99)", "Reds", (0, 1)),
]

for ax, (metric, title, cmap, vlim) in zip(axes, metric_specs):
    phase = load_phase(metric)
    Z = to_array(phase, "median")
    # phase data shape is (km_idx, tm_idx); imshow expects (rows=y, cols=x)
    # Use km on y-axis, tm on x-axis for natural reading
    Z_plot = Z  # shape (km, tm) — km row, tm col

    if vlim is None:
        vmin, vmax = float(np.nanmin(Z_plot)), float(np.nanmax(Z_plot))
    else:
        vmin, vmax = vlim

    im = ax.pcolormesh(tm_grid, km_grid, Z_plot, cmap=cmap,
                        vmin=vmin, vmax=vmax, shading="auto")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("tm (timing modifier)")
    ax.set_ylabel("km (rate modifier)")
    ax.set_title(title, fontsize=11)

    # Reference points
    ax.plot(1.0, 1.0, marker="o", color="cyan", markersize=11,
            markeredgecolor="black", markeredgewidth=1.5, label="No myelosan",
            zorder=5)
    ax.plot(TM_BASELINE_G2, KM_BASELINE_G2, marker="*", color="yellow",
            markersize=18, markeredgecolor="black", markeredgewidth=1.5,
            label="G2 baseline (observed)", zorder=5)

    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=9)

    if metric == "max_recalc":
        # Add contour lines at meaningful severity levels
        try:
            cs = ax.contour(tm_grid, km_grid, Z_plot, levels=[10, 20, 30, 40],
                            colors="white", linewidths=0.7, alpha=0.6)
            ax.clabel(cs, inline=True, fontsize=8, fmt="%d")
        except Exception:
            pass

axes[0].legend(loc="upper right", fontsize=8, framealpha=0.9)

plt.tight_layout()
fig_path = FIGURES_DIR / "fig1_phase_diagram_3panel.png"
plt.savefig(fig_path, dpi=200, bbox_inches="tight")
plt.close()
print(f"Saved: {fig_path}")


# ============================================================
# FIGURE 2: Dose-response slice at tm=0.43 (fixed timing, vary km)
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

# Find tm closest to 0.43
tm_slice_idx = int(np.argmin(np.abs(tm_grid - TM_BASELINE_G2)))
tm_slice_val = tm_grid[tm_slice_idx]

slice_metrics = [
    ("max_recalc", "Peak hypocoagulation", "Δrecalc (s)"),
    ("auc_recalc", "Coagulation disruption AUC", "AUC |Δrecalc|"),
    ("min_xiii", "XIII depletion nadir", "Δxiii"),
]

for ax, (metric, title, ylabel) in zip(axes, slice_metrics):
    phase = load_phase(metric)
    Z_med = to_array(phase, "median")[:, tm_slice_idx]
    Z_lo = to_array(phase, "p2_5")[:, tm_slice_idx]
    Z_hi = to_array(phase, "p97_5")[:, tm_slice_idx]
    Z_med_good = to_array(phase, "median_good")[:, tm_slice_idx]
    Z_lo_good = to_array(phase, "p2_5_good")[:, tm_slice_idx]
    Z_hi_good = to_array(phase, "p97_5_good")[:, tm_slice_idx]

    # Full ensemble (light)
    ax.fill_between(km_grid, Z_lo, Z_hi, alpha=0.18, color="steelblue",
                     label="Full ensemble CI95")
    ax.plot(km_grid, Z_med, color="steelblue", lw=1.8, label="Full ensemble median")

    # Good-basin subset (dark)
    ax.fill_between(km_grid, Z_lo_good, Z_hi_good, alpha=0.32, color="darkblue",
                     label="Good-basin CI95")
    ax.plot(km_grid, Z_med_good, color="darkblue", lw=1.8, ls="--",
            label="Good-basin median")

    # Reference markers
    ax.axvline(1.0, color="cyan", lw=1.2, ls=":", alpha=0.7)
    ax.axvline(KM_BASELINE_G2, color="orange", lw=1.2, ls=":", alpha=0.7)

    # Annotate
    y_anno = ax.get_ylim()[1] * 0.9
    ax.annotate("No myelosan", xy=(1.0, y_anno), xytext=(1.05, y_anno),
                 fontsize=8, color="darkcyan")
    ax.annotate("Observed", xy=(KM_BASELINE_G2, y_anno),
                xytext=(KM_BASELINE_G2*1.05, y_anno),
                 fontsize=8, color="darkorange")

    ax.set_xscale("log")
    ax.set_xlabel("km (rate modifier)")
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=11)
    ax.grid(True, alpha=0.3)

axes[2].legend(loc="best", fontsize=7, framealpha=0.9)
fig.suptitle(f"Dose-response at fixed tm={tm_slice_val:.2f}", fontsize=12, y=1.02)

plt.tight_layout()
fig_path = FIGURES_DIR / "fig2_dose_response_slice.png"
plt.savefig(fig_path, dpi=200, bbox_inches="tight")
plt.close()
print(f"Saved: {fig_path}")




# ============================================================
# Summary
# ============================================================
print()
print(f"Figures generated in: {FIGURES_DIR}")
for p in sorted(FIGURES_DIR.glob("*.png")):
    size = p.stat().st_size / 1024
    print(f"  {p.name}: {size:.0f} KB")
