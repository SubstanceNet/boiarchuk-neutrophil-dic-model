"""Analysis 32: light combination scenarios for Discussion.

Two specific dose × timing combinations vs analysis 31 references.
"""
from __future__ import annotations
import json
import pickle
from pathlib import Path
import numpy as np

from src.data import load_data, build_neutrophil_interpolators
from src.ensemble import load_ensemble, good_basin_mask

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "31_intervention_timing"))
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location("a31", "analyses/31_intervention_timing/run.py")
a31 = module_from_spec(spec)
spec.loader.exec_module(a31)

ANALYSIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ANALYSIS_DIR / "results"


def main():
    print("=" * 70)
    print("Analysis 32: dose × timing combinations")
    print("=" * 70)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    g1, g2 = load_data()
    _, n2 = build_neutrophil_interpolators(g1, g2)

    # Load ensemble (shared consolidated artifact, _cache fallback)
    _ens = load_ensemble()
    members = [m["best_x"] for m in _ens]
    good_mask = good_basin_mask(_ens, g2.xiii)
    print(f"Loaded {len(members)} members ({good_mask.sum()} in good basin)")

    # Scenarios
    scenarios = [
        # (label, km_dose, tm_dose, t_intervention, comparison_note)
        ("combo1_high_dose_late",   10.0, 0.43, 4.0,
         "rescue attempt: 2x dose at late timing"),
        ("combo2_half_dose_early",  2.5,  0.6,  0.0,
         "trade-off: half dose at early timing"),
    ]

    # Reference points already computed in analysis 31 — re-import from there
    a31_summary = json.loads(
        Path("analyses/31_intervention_timing/results/summary_by_timing.json").read_text()
    )
    refs = {}
    for entry in a31_summary:
        if entry["scenario"] == "t=0":
            refs["full_t0"] = entry
        elif entry["scenario"] == "t=4":
            refs["full_t4"] = entry
        elif entry["scenario"] == "no intervention":
            refs["no_int"] = entry

    print()
    print("Running combinations...")
    all_results = []
    trajectory_samples = {}

    for label, km, tm, t_int, note in scenarios:
        print(f"  {label}: km={km}, tm={tm}, t={t_int}")
        per_member = []
        for m_idx, pv in enumerate(members):
            o = a31.simulate_with_intervention(pv, n2, t_int, km_dose=km, tm_dose=tm)
            if o is None:
                continue
            sev = a31.compute_severity(o)
            per_member.append(dict(member_idx=m_idx, good_basin=bool(good_mask[m_idx]),
                                    **sev))
            if m_idx == 0:
                trajectory_samples[label] = dict(
                    t=a31.T_FINE.tolist(),
                    gHn=o["gHn"].tolist(),
                    recalc=o["recalc"].tolist(),
                    xiii=o["xiii"].tolist(),
                )

        # Aggregate
        entry = dict(
            scenario=label,
            note=note,
            km_dose=km, tm_dose=tm, t_intervention=t_int,
            n_total=len(per_member),
            n_good=sum(1 for p in per_member if p["good_basin"]),
        )
        for metric in a31.SEVERITY_METRICS:
            vals = [p[metric] for p in per_member if np.isfinite(p[metric])]
            vals_good = [p[metric] for p in per_member
                          if np.isfinite(p[metric]) and p["good_basin"]]
            if vals:
                entry[metric] = dict(
                    median=float(np.median(vals)),
                    p2_5=float(np.percentile(vals, 2.5)),
                    p97_5=float(np.percentile(vals, 97.5)),
                )
            if vals_good:
                entry[f"{metric}_good"] = dict(
                    median=float(np.median(vals_good)),
                    p2_5=float(np.percentile(vals_good, 2.5)),
                    p97_5=float(np.percentile(vals_good, 97.5)),
                )
        all_results.append(entry)

    # Save
    raw_path = RESULTS_DIR / "combinations_raw.pkl"
    with raw_path.open("wb") as f:
        pickle.dump(dict(
            scenarios=scenarios,
            results=all_results,
            references=refs,
            trajectory_samples=trajectory_samples,
            t_fine=a31.T_FINE.tolist(),
        ), f)
    print(f"\nSaved raw: {raw_path}")

    summary_path = RESULTS_DIR / "combinations_summary.json"
    summary_path.write_text(json.dumps(dict(
        scenarios=all_results,
        references={k: {m: v[m] for m in ["max_recalc", "auc_recalc", "min_xiii",
                                            "t_peak", "t_recovery"]}
                    for k, v in refs.items()},
    ), indent=2, default=float))
    print(f"Saved summary: {summary_path}")

    # Print comparison table
    print()
    print("=" * 95)
    print(f"{'scenario':>30} | {'max_recalc':>10} | {'auc_recalc':>10} | "
          f"{'min_xiii':>9} | {'t_peak':>7} | {'t_recovery':>10}")
    print("-" * 95)

    # References
    for ref_key, ref_label in [("full_t0", "REF: full dose at t=0"),
                                ("full_t4", "REF: full dose at t=4"),
                                ("no_int", "REF: no intervention")]:
        e = refs[ref_key]
        print(f"{ref_label:>30} | "
              f"{e['max_recalc']['median']:>10.2f} | "
              f"{e['auc_recalc']['median']:>10.2f} | "
              f"{e['min_xiii']['median']:>9.2f} | "
              f"{e['t_peak']['median']:>7.2f} | "
              f"{e['t_recovery']['median']:>10.2f}")
    print("-" * 95)

    # Combinations
    for entry in all_results:
        print(f"{entry['scenario']:>30} | "
              f"{entry['max_recalc']['median']:>10.2f} | "
              f"{entry['auc_recalc']['median']:>10.2f} | "
              f"{entry['min_xiii']['median']:>9.2f} | "
              f"{entry['t_peak']['median']:>7.2f} | "
              f"{entry['t_recovery']['median']:>10.2f}")

    # Headline check
    print()
    print("=" * 70)
    print("HYPOTHESIS: 'timing > dose'")
    print("=" * 70)
    c1_max = all_results[0]["max_recalc"]["median"]   # combo1: high dose late
    c2_max = all_results[1]["max_recalc"]["median"]   # combo2: half dose early
    print(f"  Combo1 (high dose, t=4): max_recalc = {c1_max:.2f}")
    print(f"  Combo2 (half dose, t=0): max_recalc = {c2_max:.2f}")
    print(f"  Hypothesis 'timing > dose' supported: "
          f"{'YES — Combo2 < Combo1' if c2_max < c1_max else 'NO — Combo1 < Combo2'}")


if __name__ == "__main__":
    main()
