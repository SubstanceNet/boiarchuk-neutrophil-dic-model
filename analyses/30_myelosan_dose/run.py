"""
Analysis 30: myelosan dose-response phase diagram.

Sweep (km, tm) ∈ log-spaced 15×15 grid, simulate G2 dynamics with
each of 100 bootstrap ensemble members, compute severity metrics.
"""
from __future__ import annotations
import json
import pickle
import time
from pathlib import Path
import numpy as np

from src import config as cfg
from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids, solve_group
from src.ensemble import load_ensemble, good_basin_mask as compute_good_basin_mask

ANALYSIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ANALYSIS_DIR / "results"

# Grid parameters
KM_RANGE = (1.0, 10.0)
TM_RANGE = (0.2, 1.0)
N_GRID = 15

# Reference points
KM_BASELINE_G1 = 1.0      # no myelosan
TM_BASELINE_G1 = 1.0
KM_BASELINE_G2 = 4.93     # observed G2 myelosan effect
TM_BASELINE_G2 = 0.43

# NOTE: liver_collapse (Hn/Hm > 0.99) removed — invalid metric.
# o['Hm'] is absent from solve_group output (-> None -> always False), and
# Hn reaches only ~1% of Hm in the realistic range so the threshold is
# structurally unreachable. Mortality validation: see analysis 33.
SEVERITY_METRICS = [
    "max_gHn", "min_xiii", "max_recalc", "auc_recalc",
    "time_to_peak_gHn",
]


def compute_severity(o, T):
    """Compute severity metrics from G2 ODE solution."""
    gHn = np.asarray(o["gHn"])
    xiii = np.asarray(o["xiii"])
    recalc = np.asarray(o["recalc"])
    
    # max gHn — peak accumulation
    max_ghn = float(np.max(gHn))
    
    # min xiii — nadir
    min_xiii = float(np.min(xiii))
    
    # max recalc — peak hypocoagulation
    max_recalc = float(np.max(recalc))
    
    # AUC recalc — using trapezoid rule on |recalc|
    auc_recalc = float(np.trapezoid(np.abs(recalc), T))
    
    # time to peak gHn
    peak_idx = int(np.argmax(gHn))
    time_to_peak_gHn = float(T[peak_idx])
    
    return dict(
        max_gHn=max_ghn,
        min_xiii=min_xiii,
        max_recalc=max_recalc,
        auc_recalc=auc_recalc,
        time_to_peak_gHn=time_to_peak_gHn,
    )


def simulate_one(pv_member, km_val, tm_val, g2, n2_interp, t_fine):
    """Simulate G2 dynamics for given ensemble member and (km, tm) override.
    
    Returns severity metrics dict.
    """
    pv = pv_member.copy()
    pv[24] = km_val   # override km
    pv[25] = tm_val   # override tm
    
    # G2 effective rate and timing
    kr_g2 = pv[1] * pv[24]
    tp2_g2 = pv[8] * pv[25]
    
    # Use G2's time grid for evaluation; solve_group internally uses t_fine
    try:
        o = solve_group(pv, g2.T, n2_interp, t_fine, kr_g2, tp2_g2)
    except Exception:
        return None  # ODE failure
    
    # Validate output
    keys_to_check = ["gHn", "xiii", "recalc", "Hn"]
    for k in keys_to_check:
        if k not in o or np.any(np.isnan(np.asarray(o[k]))):
            return None
    
    return compute_severity(o, g2.T)


def main():
    print("=" * 70)
    print("Analysis 30: myelosan dose-response")
    print("=" * 70)
    
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load data and ensemble
    g1, g2 = load_data()
    _, n2_interp = build_neutrophil_interpolators(g1, g2)
    t_fine_g1, t_fine_g2 = make_fine_grids()
    
    # Load bootstrap ensemble (shared consolidated artifact, _cache fallback)
    _ens = load_ensemble()
    ensemble_members = [m["best_x"] for m in _ens]
    print(f"Loaded {len(ensemble_members)} bootstrap ensemble members")
    
    # Build grid (log-spaced for km, log-spaced for tm)
    km_grid = np.logspace(np.log10(KM_RANGE[0]), np.log10(KM_RANGE[1]), N_GRID)
    tm_grid = np.logspace(np.log10(TM_RANGE[0]), np.log10(TM_RANGE[1]), N_GRID)
    print(f"km grid: {km_grid.round(2).tolist()}")
    print(f"tm grid: {tm_grid.round(3).tolist()}")
    
    # Identify good-basin ensemble members (xiii_G2 R² >= 0.3 from analysis 22)
    good_basin_mask = compute_good_basin_mask(_ens, g2.xiii)
    print(f"Good-basin members (xiii_G2 R²>=0.3): {good_basin_mask.sum()}/{len(good_basin_mask)}")
    
    # Sweep
    print()
    print("Starting sweep...")
    t_start = time.time()
    
    # Storage: ensemble_predictions[km_idx][tm_idx][member_idx] = severity_dict
    all_predictions = []  # list of (km_idx, tm_idx, member_idx, severity)
    failed_count = 0
    
    total_cells = N_GRID * N_GRID
    
    for km_idx, km_val in enumerate(km_grid):
        for tm_idx, tm_val in enumerate(tm_grid):
            for member_idx, pv_member in enumerate(ensemble_members):
                sev = simulate_one(pv_member, km_val, tm_val, g2, n2_interp, t_fine_g2)
                if sev is None:
                    failed_count += 1
                    continue
                all_predictions.append(dict(
                    km_idx=int(km_idx), tm_idx=int(tm_idx),
                    member_idx=int(member_idx),
                    km=float(km_val), tm=float(tm_val),
                    good_basin=bool(good_basin_mask[member_idx]),
                    **sev,
                ))
        
        elapsed = (time.time() - t_start) / 60
        done_cells = (km_idx + 1) * N_GRID
        eta = (elapsed / done_cells) * (total_cells - done_cells) if done_cells > 0 else 0
        print(f"  km={km_val:.2f} ({km_idx+1}/{N_GRID}) done. "
              f"elapsed={elapsed:.1f}m ETA={eta:.1f}m")
    
    elapsed_total = (time.time() - t_start) / 60
    print()
    print(f"Sweep complete in {elapsed_total:.1f}m. Failed: {failed_count}")
    
    # Save raw predictions
    raw_path = RESULTS_DIR / "ensemble_predictions_raw.pkl"
    with raw_path.open("wb") as f:
        pickle.dump(dict(
            km_grid=km_grid.tolist(),
            tm_grid=tm_grid.tolist(),
            predictions=all_predictions,
            good_basin_mask=good_basin_mask.tolist(),
            failed_count=failed_count,
        ), f)
    print(f"Saved raw: {raw_path}")
    
    # Aggregate per cell: percentiles across ensemble members
    print()
    print("Aggregating per cell...")
    phase_data = {}
    for metric in SEVERITY_METRICS:
        phase_data[metric] = dict(
            km_grid=km_grid.tolist(),
            tm_grid=tm_grid.tolist(),
            median=np.full((N_GRID, N_GRID), np.nan),
            p2_5=np.full((N_GRID, N_GRID), np.nan),
            p97_5=np.full((N_GRID, N_GRID), np.nan),
            median_good=np.full((N_GRID, N_GRID), np.nan),
            p2_5_good=np.full((N_GRID, N_GRID), np.nan),
            p97_5_good=np.full((N_GRID, N_GRID), np.nan),
        )
    
    # Reshape predictions into per-cell arrays
    for km_idx in range(N_GRID):
        for tm_idx in range(N_GRID):
            cell_preds = [p for p in all_predictions
                          if p["km_idx"] == km_idx and p["tm_idx"] == tm_idx]
            if not cell_preds:
                continue
            cell_good = [p for p in cell_preds if p["good_basin"]]
            for metric in SEVERITY_METRICS:
                vals = [p[metric] for p in cell_preds]
                vals_good = [p[metric] for p in cell_good]
                phase_data[metric]["median"][km_idx, tm_idx] = float(np.median(vals))
                phase_data[metric]["p2_5"][km_idx, tm_idx] = float(np.percentile(vals, 2.5))
                phase_data[metric]["p97_5"][km_idx, tm_idx] = float(np.percentile(vals, 97.5))
                if vals_good:
                    phase_data[metric]["median_good"][km_idx, tm_idx] = float(np.median(vals_good))
                    phase_data[metric]["p2_5_good"][km_idx, tm_idx] = float(np.percentile(vals_good, 2.5))
                    phase_data[metric]["p97_5_good"][km_idx, tm_idx] = float(np.percentile(vals_good, 97.5))
    
    # Save phase diagrams as JSON (per metric)
    for metric in SEVERITY_METRICS:
        d = {k: v.tolist() if isinstance(v, np.ndarray) else v
             for k, v in phase_data[metric].items()}
        out_path = RESULTS_DIR / f"phase_diagram_{metric}.json"
        out_path.write_text(json.dumps(d, indent=2, default=float))
        print(f"  Saved: {out_path}")
    


if __name__ == "__main__":
    main()
