"""Shared publication-figure style for the manuscript figures.

Single source of truth for fonts, colors, sizes, and common helpers so all
figures (Fig 1-6) render identically. Import and call apply_style() at the
top of each figure generator.

    from analyses._fig_style import apply_style, C_G1, C_G2, MORT_BAND, save_fig
    apply_style()
"""
from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Colorblind-safe ColorBrewer RdBu pair; works in grayscale too.
C_G1 = "#2166AC"  # Group I  — dark blue
C_G2 = "#B2182B"  # Group II — dark red

# G1 mortality / deep-hypocoagulation window (days). Use on G1 hemostatic panels.
MORT_BAND = (10, 12)

# Full-width single column (mm); revisit when target journal layout is finalised. Convert to inches at call sites: W_MM/25.4.
WIDTH_MM_FULL = 180.0

_SERIF = "Nimbus Roman"  # metrically Times-compatible, available in this env


def apply_style():
    """Apply the shared rcParams. Call once at the top of each generator."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": [_SERIF, "Liberation Serif", "DejaVu Serif"],
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


def despine(ax):
    """Remove top/right spines, outward ticks — house style for all panels."""
    ax.tick_params(direction="out", length=3)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)


def panel_label(ax, lbl, color="black"):
    """Bold (a)/(b)/... label in the top-right corner (clear of data).
    Use color="white" on dark backgrounds (e.g. heatmaps)."""
    ax.text(0.97, 0.95, lbl, transform=ax.transAxes, fontweight="bold",
            fontsize=10, va="top", ha="right", color=color)


def mortality_band(ax, band=MORT_BAND):
    """Light gray vertical band under everything (G1 mortality window)."""
    ax.axvspan(band[0], band[1], color="0.5", alpha=0.15, lw=0, zorder=0)


def save_fig(fig, fig_dir, stem):
    """Save both PNG (300 dpi) and vector PDF with the same stem."""
    fig_dir = Path(fig_dir)
    fig_dir.mkdir(parents=True, exist_ok=True)
    png = fig_dir / f"{stem}.png"
    pdf = fig_dir / f"{stem}.pdf"
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    return png, pdf
