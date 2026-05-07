"""Visualisation of W_split sweep results.

Reads results/sweep.json, produces 4 figures in figures/:
  01_cost_r2_vs_W.png       — cost and R^2 vs W_split
  02_fractions_vs_W.png     — achieved neutro-fractions vs W_split + targets
  03_params_vs_W.png        — key 6 mechanism parameters vs W_split
  04_summary_panel.png      — combined panel for quick visual scan
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ANALYSIS_DIR = Path(__file__).resolve().parent
data = json.loads((ANALYSIS_DIR / "results" / "sweep.json").read_text())
rows = data["rows"]

W = np.array([r["W_split"] for r in rows])
cost = np.array([r["cost"] for r in rows])
r2g1 = np.array([r["avg_r2_g1"] for r in rows])
r2g2 = np.array([r["avg_r2_g2"] for r in rows])
fr_recalc = np.array([r["achieved_fractions"]["recalc_neutro_frac"] for r in rows])
fr_fib    = np.array([r["achieved_fractions"]["fib_neutro_frac"]    for r in rows])
fr_xiii   = np.array([r["achieved_fractions"]["xiii_neutro_frac"]   for r in rows])
TARGETS = dict(recalc=0.24, fib=0.76, xiii=0.82)

fig_dir = ANALYSIS_DIR / "figures"
fig_dir.mkdir(exist_ok=True)

# ----- 01: cost & R^2 -----
fig, ax1 = plt.subplots(figsize=(7, 4.5))
ax1.plot(W, cost, "o-", color="tab:red", label="cost")
ax1.set_xlabel(r"$W_{\rm split}$")
ax1.set_ylabel("cost", color="tab:red")
ax1.tick_params(axis="y", labelcolor="tab:red")
ax2 = ax1.twinx()
ax2.plot(W, r2g1, "s-", color="tab:blue", label=r"$R^2_{G1}$")
ax2.plot(W, r2g2, "^-", color="tab:green", label=r"$R^2_{G2}$")
ax2.set_ylabel(r"$R^2$ (avg)", color="black")
ax2.legend(loc="lower right")
ax1.set_title(r"Fit quality vs $W_{\rm split}$")
ax1.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(fig_dir / "01_cost_r2_vs_W.png", dpi=130)
plt.close()

# ----- 02: achieved fractions -----
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(W, fr_recalc, "o-", label="recalc realised", color="tab:blue")
ax.axhline(TARGETS["recalc"], ls=":", color="tab:blue", alpha=0.6, label="recalc target (0.24)")
ax.plot(W, fr_fib, "s-", label="fib realised", color="tab:orange")
ax.axhline(TARGETS["fib"], ls=":", color="tab:orange", alpha=0.6, label="fib target (0.76)")
ax.plot(W, fr_xiii, "^-", label="xiii realised", color="tab:green")
ax.axhline(TARGETS["xiii"], ls=":", color="tab:green", alpha=0.6, label="xiii target (0.82)")
ax.set_xlabel(r"$W_{\rm split}$")
ax.set_ylabel("achieved neutrophil-share fraction (G1 day 2)")
ax.set_title(r"Decomposition vs $W_{\rm split}$")
ax.legend(fontsize=8, ncol=2, loc="center right")
ax.set_ylim(-0.05, 1.05)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(fig_dir / "02_fractions_vs_W.png", dpi=130)
plt.close()

# ----- 03: key parameters vs W -----
key_params = ["ar", "cr", "af", "cf", "ax", "cx"]
fig, axs = plt.subplots(2, 3, figsize=(11, 6.5), sharex=True)
for ax, name in zip(axs.flat, key_params):
    vals = np.array([r["params"][name] for r in rows])
    ax.plot(W, vals, "o-")
    ax.set_title(name)
    ax.grid(alpha=0.3)
for ax in axs[1, :]:
    ax.set_xlabel(r"$W_{\rm split}$")
plt.suptitle(r"Mechanism-channel parameters vs $W_{\rm split}$")
plt.tight_layout()
plt.savefig(fig_dir / "03_params_vs_W.png", dpi=130)
plt.close()

# ----- 04: combined summary -----
fig, axs = plt.subplots(1, 2, figsize=(12, 4.5))
ax = axs[0]
ax.plot(W, cost, "o-", color="tab:red", label="cost")
ax2 = ax.twinx()
ax2.plot(W, r2g1, "s-", color="tab:blue", label=r"$R^2_{G1}$")
ax2.plot(W, r2g2, "^-", color="tab:green", label=r"$R^2_{G2}$")
ax.set_xlabel(r"$W_{\rm split}$"); ax.set_ylabel("cost", color="tab:red")
ax2.set_ylabel(r"$R^2$"); ax2.legend(loc="lower right")
ax.set_title("Fit quality"); ax.grid(alpha=0.3)
ax = axs[1]
ax.plot(W, fr_recalc, "o-", label="recalc", color="tab:blue")
ax.axhline(0.24, ls=":", color="tab:blue", alpha=0.6)
ax.plot(W, fr_fib, "s-", label="fib", color="tab:orange")
ax.axhline(0.76, ls=":", color="tab:orange", alpha=0.6)
ax.plot(W, fr_xiii, "^-", label="xiii", color="tab:green")
ax.axhline(0.82, ls=":", color="tab:green", alpha=0.6)
ax.set_xlabel(r"$W_{\rm split}$"); ax.set_ylabel("fraction (realised)")
ax.set_title("Decomposition"); ax.legend(loc="center right"); ax.set_ylim(-0.05, 1.05); ax.grid(alpha=0.3)
plt.suptitle("Analysis 01: W_split sweep — summary")
plt.tight_layout()
plt.savefig(fig_dir / "04_summary_panel.png", dpi=130)
plt.close()

print("Figures written:")
for p in sorted(fig_dir.glob("*.png")):
    print(f"  {p.name}  ({p.stat().st_size // 1024} KB)")
