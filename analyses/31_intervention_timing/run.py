"""
Analysis 31: myelosan intervention timing.

For each t_intervention scenario × 100 bootstrap ensemble members:
- Simulate G2 ODE in two segments (no myelosan → with myelosan at t_intervention).
- Compute severity + temporal metrics on fine grid (400 points, 0-19 days).
"""
from __future__ import annotations
import json
import pickle
import time
from pathlib import Path
import numpy as np
from scipy.integrate import odeint
from scipy.interpolate import interp1d

from src import config as cfg
from src.data import load_data, build_neutrophil_interpolators
from src.model import _rhs, _V

ANALYSIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ANALYSIS_DIR / "results"

# Fixed myelosan dose (G2 observed)
KM_DOSE = 4.93
TM_DOSE = 0.43

# Timing scenarios (∞ encoded as np.inf)
T_INTERVENTIONS = [0.0, 1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 6.0, np.inf]
T_INT_LABELS = ["t=0", "t=1", "t=2", "t=2.5", "t=3", "t=3.5", "t=4", "t=6", "no intervention"]

# Extended fine grid for analysis 31 (0-19 days, 400 points)
T_FINE = np.linspace(0.0, 19.0, 400)
T_END = T_FINE[-1]

SEVERITY_METRICS = [
    "max_gHn", "min_xiii", "max_recalc", "auc_recalc",
    "t_peak", "t_recovery", "acute_phase_duration",
]


def _build_output(pv, t_arr, y):
    """Compute observables from raw ODE state, mirroring solve_group formulas."""
    Hm = pv[7]
    D = np.clip(y[:, 0], 0.0, 1.0)
    AP = np.maximum(y[:, 1], 0.0)
    Hc = np.maximum(y[:, 2], 0.0)
    Hn = np.clip(y[:, 3], 0.0, Hm * 0.999)
    X = y[:, 4]
    V_at = _V(t_arr)
    gHn = Hn / np.maximum(1.0 - Hn / Hm, 0.005)
    return dict(
        D=D * 100.0,
        AP=AP, Hc=Hc, Hn=Hn, gHn=gHn, V=V_at, X=X,
        recalc=-pv[11] * V_at - pv[12] * AP + pv[13] * gHn,
        thrombin=-pv[14] * V_at + pv[15] * gHn,
        fib=+pv[16] * V_at + pv[17] * AP - pv[18] * gHn - pv[19] * Hc,
        xiii=X,
    )


def simulate_with_intervention(pv, n2_interp, t_intervention,
                                km_dose=KM_DOSE, tm_dose=TM_DOSE, t_fine=T_FINE):
    """Two-segment ODE simulation with myelosan introduced at t_intervention.
    
    Continuity: ODE state at t_intervention from segment 1 = initial condition
    for segment 2. Only kr_eff and tp2_eff change at the boundary.
    """
    kr_base = pv[1]
    tp2_base = pv[8]
    kr_post = kr_base * km_dose
    tp2_post = tp2_base * tm_dose
    
    # Case 1: no intervention ever (t_intervention >= t_end or inf)
    if not np.isfinite(t_intervention) or t_intervention >= t_fine[-1]:
        y = odeint(
            _rhs, y0=[0.0, 0.0, 0.0, 0.0, 0.0], t=t_fine,
            args=(pv, n2_interp, kr_base, tp2_base),
            rtol=cfg.ODE_RTOL, atol=cfg.ODE_ATOL, mxstep=cfg.ODE_MXSTEP,
        )
        if np.any(np.isnan(y)):
            return None
        return _build_output(pv, t_fine, y)
    
    # Case 2: intervention from t=0 (single segment with myelosan)
    if t_intervention <= t_fine[0]:
        y = odeint(
            _rhs, y0=[0.0, 0.0, 0.0, 0.0, 0.0], t=t_fine,
            args=(pv, n2_interp, kr_post, tp2_post),
            rtol=cfg.ODE_RTOL, atol=cfg.ODE_ATOL, mxstep=cfg.ODE_MXSTEP,
        )
        if np.any(np.isnan(y)):
            return None
        return _build_output(pv, t_fine, y)
    
    # Case 3: general two-segment
    # Segment 1: pre-intervention (no myelosan), [0, t_intervention]
    t_seg1 = t_fine[t_fine <= t_intervention]
    if t_seg1[-1] < t_intervention:
        t_seg1 = np.append(t_seg1, t_intervention)
    y_seg1 = odeint(
        _rhs, y0=[0.0, 0.0, 0.0, 0.0, 0.0], t=t_seg1,
        args=(pv, n2_interp, kr_base, tp2_base),
        rtol=cfg.ODE_RTOL, atol=cfg.ODE_ATOL, mxstep=cfg.ODE_MXSTEP,
    )
    if np.any(np.isnan(y_seg1)):
        return None
    y_at_intervention = y_seg1[-1].copy()
    
    # Segment 2: post-intervention (myelosan), [t_intervention, t_end]
    t_seg2 = t_fine[t_fine >= t_intervention]
    if t_seg2[0] > t_intervention:
        t_seg2 = np.insert(t_seg2, 0, t_intervention)
    y_seg2 = odeint(
        _rhs, y0=y_at_intervention.tolist(), t=t_seg2,
        args=(pv, n2_interp, kr_post, tp2_post),
        rtol=cfg.ODE_RTOL, atol=cfg.ODE_ATOL, mxstep=cfg.ODE_MXSTEP,
    )
    if np.any(np.isnan(y_seg2)):
        return None
    
    # Stitch onto t_fine via interpolation
    y_full = np.zeros((len(t_fine), 5))
    mask_pre = t_fine <= t_intervention
    mask_post = t_fine >= t_intervention
    for col in range(5):
        f1 = interp1d(t_seg1, y_seg1[:, col], kind="linear", fill_value="extrapolate")
        y_full[mask_pre, col] = f1(t_fine[mask_pre])
        f2 = interp1d(t_seg2, y_seg2[:, col], kind="linear", fill_value="extrapolate")
        y_full[mask_post, col] = f2(t_fine[mask_post])
    
    return _build_output(pv, t_fine, y_full)


def compute_severity(o, t_fine=T_FINE):
    """Compute severity + temporal metrics from output dict."""
    gHn = np.asarray(o["gHn"])
    xiii = np.asarray(o["xiii"])
    recalc = np.asarray(o["recalc"])
    
    max_ghn = float(np.max(gHn))
    min_xiii = float(np.min(xiii))
    max_recalc = float(np.max(recalc))
    auc_recalc = float(np.trapezoid(np.abs(recalc), t_fine))
    
    # t_peak: time of max gHn
    peak_idx = int(np.argmax(gHn))
    t_peak = float(t_fine[peak_idx])
    
    # t_recovery: first time after peak when gHn falls to 10% of peak value
    threshold = 0.1 * max_ghn
    t_recovery = float("nan")
    if max_ghn > 0 and peak_idx < len(gHn) - 1:
        post_peak = gHn[peak_idx:]
        below_mask = post_peak < threshold
        if np.any(below_mask):
            rel_idx = int(np.argmax(below_mask))  # first True
            t_recovery = float(t_fine[peak_idx + rel_idx])
    
    acute_duration = (t_recovery - t_peak) if np.isfinite(t_recovery) else float("nan")
    
    return dict(
        max_gHn=max_ghn,
        min_xiii=min_xiii,
        max_recalc=max_recalc,
        auc_recalc=auc_recalc,
        t_peak=t_peak,
        t_recovery=t_recovery,
        acute_phase_duration=acute_duration,
    )


def main():
    print("=" * 70)
    print("Analysis 31: myelosan intervention timing")
    print(f"Scenarios: {T_INT_LABELS}")
    print(f"Dose: km={KM_DOSE}, tm={TM_DOSE}")
    print(f"Fine grid: {len(T_FINE)} points, [0, {T_END}]")
    print("=" * 70)
    
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load data and ensemble
    g1, g2 = load_data()
    _, n2_interp = build_neutrophil_interpolators(g1, g2)
    
    bootstrap_cache = Path("analyses/22_predictive_check/results/_cache")
    ensemble_members = []
    good_basin_mask = []
    for p in sorted(bootstrap_cache.glob("iter_*.pkl")):
        with p.open("rb") as f:
            rec = pickle.load(f)
        if rec.get("failed"):
            continue
        ensemble_members.append(np.array(rec["best_x"]))
        # good basin: xiii_G2 R² >= 0.3
        xiii_pred = np.asarray(rec["g2_predictions"]["xiii"])
        ss_res = np.sum((xiii_pred - g2.xiii) ** 2)
        ss_tot = np.sum((g2.xiii - g2.xiii.mean()) ** 2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        good_basin_mask.append(r2 >= 0.3)
    good_basin_mask = np.array(good_basin_mask)
    print(f"Loaded {len(ensemble_members)} ensemble members "
          f"({good_basin_mask.sum()} in good basin)")
    
    # Run sweep
    print()
    print("Starting sweep...")
    t_start = time.time()
    all_predictions = []
    trajectory_samples = {}  # save 1 trajectory per scenario for plotting
    failed = 0
    
    for sc_idx, t_int in enumerate(T_INTERVENTIONS):
        label = T_INT_LABELS[sc_idx]
        sc_failed = 0
        for m_idx, pv in enumerate(ensemble_members):
            o = simulate_with_intervention(pv, n2_interp, t_int)
            if o is None:
                sc_failed += 1
                failed += 1
                continue
            sev = compute_severity(o)
            all_predictions.append(dict(
                t_intervention=float(t_int) if np.isfinite(t_int) else None,
                scenario_label=label,
                scenario_idx=int(sc_idx),
                member_idx=int(m_idx),
                good_basin=bool(good_basin_mask[m_idx]),
                **sev,
            ))
            # Save trajectory for first ensemble member of each scenario
            if m_idx == 0:
                trajectory_samples[label] = dict(
                    t=T_FINE.tolist(),
                    gHn=o["gHn"].tolist(),
                    recalc=o["recalc"].tolist(),
                    xiii=o["xiii"].tolist(),
                )
        print(f"  Scenario {label}: done ({sc_failed} failed)")
    
    elapsed = (time.time() - t_start) / 60
    print(f"\nSweep complete in {elapsed:.2f}m. Total failed: {failed}")
    
    # Save raw
    raw_path = RESULTS_DIR / "intervention_predictions_raw.pkl"
    with raw_path.open("wb") as f:
        pickle.dump(dict(
            t_interventions=[float(t) if np.isfinite(t) else None for t in T_INTERVENTIONS],
            scenario_labels=T_INT_LABELS,
            predictions=all_predictions,
            trajectory_samples=trajectory_samples,
            good_basin_mask=good_basin_mask.tolist(),
            t_fine=T_FINE.tolist(),
            km_dose=KM_DOSE,
            tm_dose=TM_DOSE,
        ), f)
    print(f"Saved raw: {raw_path}")
    
    # Aggregate per scenario
    summary = []
    for sc_idx, label in enumerate(T_INT_LABELS):
        sc_preds = [p for p in all_predictions if p["scenario_idx"] == sc_idx]
        sc_good = [p for p in sc_preds if p["good_basin"]]
        entry = dict(
            scenario=label,
            t_intervention=float(T_INTERVENTIONS[sc_idx]) if np.isfinite(T_INTERVENTIONS[sc_idx]) else None,
            n_total=len(sc_preds),
            n_good=len(sc_good),
        )
        for metric in SEVERITY_METRICS:
            vals = [p[metric] for p in sc_preds if np.isfinite(p[metric])]
            vals_good = [p[metric] for p in sc_good if np.isfinite(p[metric])]
            if vals:
                entry[metric] = dict(
                    median=float(np.median(vals)),
                    p2_5=float(np.percentile(vals, 2.5)),
                    p97_5=float(np.percentile(vals, 97.5)),
                    n_valid=len(vals),
                )
            if vals_good:
                entry[f"{metric}_good"] = dict(
                    median=float(np.median(vals_good)),
                    p2_5=float(np.percentile(vals_good, 2.5)),
                    p97_5=float(np.percentile(vals_good, 97.5)),
                    n_valid=len(vals_good),
                )
        summary.append(entry)
    
    summary_path = RESULTS_DIR / "summary_by_timing.json"
    summary_path.write_text(json.dumps(summary, indent=2, default=float))
    print(f"Saved summary: {summary_path}")
    
    # Print summary table
    print()
    print("=" * 90)
    print(f"{'scenario':>17} | {'max_recalc':>11} | {'auc_recalc':>11} | "
          f"{'min_xiii':>10} | {'t_peak':>7} | {'t_recovery':>10}")
    print("-" * 90)
    for entry in summary:
        max_r = entry.get("max_recalc", {}).get("median", float("nan"))
        auc_r = entry.get("auc_recalc", {}).get("median", float("nan"))
        min_x = entry.get("min_xiii", {}).get("median", float("nan"))
        t_p = entry.get("t_peak", {}).get("median", float("nan"))
        t_r = entry.get("t_recovery", {}).get("median", float("nan"))
        print(f"{entry['scenario']:>17} | {max_r:>11.2f} | {auc_r:>11.2f} | "
              f"{min_x:>10.2f} | {t_p:>7.2f} | {t_r:>10.2f}")


if __name__ == "__main__":
    main()
