"""Visualisation of cx-bound exploration: 4 regimes in one plot."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ANALYSIS_DIR = Path(__file__).resolve().parent
sweep = json.loads((ANALYSIS_DIR / "results" / "sweep.json").read_text())
seed_check = json.loads((ANALYSIS_DIR / "results" / "seed_check.json").read_text())
seed_check_extra_path = ANALYSIS_DIR / "results" / "seed_check_extra.json"
if seed_check_extra_path.exists():
    seed_check.extend(json.loads(seed_check_extra_path.read_text()))

records = []
for r in sweep["runs"]:
    records.append(dict(
        config=r["label"],
        seed=42,
        cost=r["cost"],
        cx=r["xiii_channel"]["cx"],
        xiii_G2=r["metrics_g2"]["xiii"]["R2"],
        recalc_G2=r["metrics_g2"]["recalc"]["R2"],
        AP_G2=r["metrics_g2"]["AP"]["R2"],
        D_G2=r["metrics_g2"]["D"]["R2"],
        fib_G2=r["metrics_g2"]["fib"]["R2"],
    ))
for r in seed_check:
    records.append(dict(
        config=r["label"],
        seed=r["seed"],
        cost=r["cost"],
        cx=r["cx"],
        xiii_G2=r["xiii_G2"],
        recalc_G2=r["recalc_G2"],
        AP_G2=r["AP_G2"],
        D_G2=r["D_G2"],
        fib_G2=r["fib_G2"],
    ))

fig, axs = plt.subplots(1, 2, figsize=(13, 5.5))

ax = axs[0]
colors = {"baseline": "tab:blue", "expanded": "tab:orange", "wide": "tab:red"}
markers = {42: "o", 7: "s", 123: "^", 999: "D", 2024: "P"}
for r in records:
    ax.scatter(r["cx"], r["xiii_G2"],
               color=colors[r["config"]], marker=markers[r["seed"]],
               s=140, edgecolors="black", linewidths=1.2, zorder=3)
    ax.annotate(f"{r['config'][:4]}/s{r['seed']}",
                (r["cx"], r["xiii_G2"]),
                xytext=(8, 5), textcoords="offset points", fontsize=8)
ax.axhline(0, color="gray", linestyle=":", alpha=0.6)
ax.axvline(600, color="tab:blue", linestyle=":", alpha=0.5,
           label="baseline bound (600)")
ax.set_xlabel("cx (fitted value)")
ax.set_ylabel("R-squared for XIII on G2")
ax.set_title("cx vs XIII G2 fit quality\n(no monotonic relation; regime depends on full param set)")
ax.grid(alpha=0.3)
ax.legend(loc="lower right", fontsize=9)

ax = axs[1]
obs_keys = ["xiii_G2", "recalc_G2", "AP_G2", "D_G2", "fib_G2"]
obs_labels = ["XIII", "recalc", "AP", "D", "fib"]
x_pos = np.arange(len(records))
width = 0.16
for i, (key, lab) in enumerate(zip(obs_keys, obs_labels)):
    vals = [r[key] for r in records]
    ax.bar(x_pos + i*width, vals, width, label=lab)
labels = [f"{r['config'][:4]}/s{r['seed']}" for r in records]
ax.set_xticks(x_pos + width * 2)
ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=9)
ax.axhline(0, color="black", linewidth=0.7)
ax.axhline(0.5, color="gray", linestyle=":", alpha=0.5)
ax.set_ylabel("R-squared (G2)")
ax.set_title("Per-observable G2 R-squared across all fits\n(only baseline keeps all six positive)")
ax.legend(fontsize=8, loc="lower right", ncol=2)
ax.grid(alpha=0.3, axis="y")
ax.set_ylim(-1.3, 1.05)

plt.suptitle("Analysis 02: cx bound exploration — four regimes")
plt.tight_layout()
fig_dir = ANALYSIS_DIR / "figures"
fig_dir.mkdir(exist_ok=True)
plt.savefig(fig_dir / "regimes.png", dpi=130)
plt.close()
print(f"Written: {fig_dir / 'regimes.png'}")
