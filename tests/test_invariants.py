"""
Level-1 scientific-invariant tests.

These do NOT re-run any fit or simulation. They read the tracked result
artifacts (analyses/*/results/*.json) and assert that the published
conclusions of the manuscript still hold. Thresholds are deliberately wide:
a test fires when a *conclusion* has changed, not when a value moves in its
last digit. Each datum traces to a specific artifact, recorded in the
docstring.

Run: pytest -m "not slow" tests/test_invariants.py
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
A05 = ROOT / "analyses/05_v13_baseline/results"
A22 = ROOT / "analyses/22_predictive_check/results"
A31 = ROOT / "analyses/31_intervention_timing/results"
A32 = ROOT / "analyses/32_combinations/results"
A33 = ROOT / "analyses/33_g1_severity_validation/results"


def _load(p: Path):
    if not p.exists():
        pytest.skip(f"artifact missing: {p} (run the analysis to regenerate)")
    return json.loads(p.read_text())


# --- Analysis 33: G1 severity & mortality-pattern validation -----------------

def test_g1_g2_separation_about_21x():
    """G1 vs G2 hypocoagulation separation ~21x (manuscript Table 3, S6).
    The raw median ratio is 147.05 / 6.63 = 22.2x; the manuscript reports
    21x from the rounded Group II baseline (147 / 7), consistent with Table 3.
    The tolerance below is wide on purpose: it flags a change of conclusion,
    not the last-digit rounding convention.
    Source: 33/g1_severity.json, g1/g2 max_recalc medians (147.05 / 6.63)."""
    d = _load(A33 / "g1_severity.json")
    g1 = d["g1"]["max_recalc"]["median"]
    g2 = d["g2"]["max_recalc"]["median"]
    ratio = g1 / g2
    assert 18.0 < ratio < 26.0, f"G1/G2 separation {ratio:.1f}x outside [18,26]"


def test_g1_xiii_nadir_matches_observed():
    """Modeled G1 XIII nadir ~ -77% (observed -76.7%). Source: 33/g1_severity.json."""
    d = _load(A33 / "g1_severity.json")
    med = d["g1"]["min_xiii"]["median"]
    assert -85.0 < med < -70.0, f"XIII nadir {med:.1f} outside [-85,-70]"


def test_g1_peak_timing_day11():
    """G1 hypocoagulation peak at day 11 (observed). Source: 33/g1_severity.json."""
    d = _load(A33 / "g1_severity.json")
    assert d["g1"]["t_max_recalc"]["median"] == pytest.approx(11.0, abs=0.5)


# --- Analysis 22: bootstrap ensemble integrity & mechanism split -------------

def test_ensemble_has_100_members():
    """Bootstrap ensemble N=100. Source: 22/ensemble.json n_iters,
    22/ensemble_members.json n_members."""
    d = _load(A22 / "ensemble.json")
    assert d["n_iters"] == 100
    m = _load(A22 / "ensemble_members.json")
    assert m["n_members"] == 100


def test_mechanism_split_fractions():
    """Day-2 neutrophil-attributable fractions: recalc~0.24, fib~0.76, xiii~0.81
    (manuscript Table 2 / §3.3). Source: 22/ensemble.json mechanism_split medians."""
    d = _load(A22 / "ensemble.json")
    ms = d["mechanism_split"]
    assert 0.20 < ms["recalc"]["p50.0"] < 0.28
    assert 0.72 < ms["fib"]["p50.0"] < 0.80
    assert 0.76 < ms["xiii"]["p50.0"] < 0.86


# --- Analysis 31: therapeutic window -----------------------------------------

def test_window_early_intervention_low_severity():
    """Early intervention (t=0) keeps peak hypocoagulation low; no-intervention
    is severe; severity is monotone non-decreasing across the window.
    Source: 31/summary_by_timing.json max_recalc medians."""
    d = _load(A31 / "summary_by_timing.json")
    by = {s["scenario"]: s["max_recalc"]["median"] for s in d}
    assert by["t=0"] < 12.0, f"t=0 severity {by['t=0']:.1f} too high"
    assert by["no intervention"] > 60.0, "no-intervention should be severe"
    assert by["t=0"] <= by["t=3"] <= by["no intervention"], "window not monotone"


def test_window_good_basin_27():
    """Good-basin subset is n=27 (xiii_G2 R^2 >= 0.3). Source: 31/summary_by_timing.json n_good."""
    d = _load(A31 / "summary_by_timing.json")
    assert all(s["n_good"] == 27 for s in d), "good-basin count drifted from 27"


# --- Analysis 32: dose x timing thresholds -----------------------------------

def test_dose_and_timing_both_required():
    """Half-dose-early (combo2) is WORSE than full-dose-late (combo1): dose and
    timing are independent thresholds, not a continuous trade-off (manuscript
    Results, Virtual experiments — dose x time; Table 4). Source:
    32/combinations_summary.json max_recalc medians."""
    d = _load(A32 / "combinations_summary.json")
    by = {s["scenario"]: s["max_recalc"]["median"] for s in d["scenarios"]}
    combo1 = by["combo1_high_dose_late"]
    combo2 = by["combo2_half_dose_early"]
    assert combo2 > combo1, f"combo2 ({combo2:.1f}) should exceed combo1 ({combo1:.1f})"


# --- Analysis 05 / 22: headline fit-quality numbers --------------------------

def test_baseline_mean_r2():
    """Joint baseline point-fit mean R^2: Group I ~0.83, Group II ~0.69
    (manuscript Results, 'Simultaneous model fitting'). Wide bands flag a change
    of conclusion, not last-digit drift.
    Source: 05_v13_baseline/results/fit.json avg_r2_g1 / avg_r2_g2."""
    d = _load(A05 / "fit.json")
    assert 0.78 < d["avg_r2_g1"] < 0.88, f"G1 mean R2 {d['avg_r2_g1']:.3f} outside [0.78,0.88]"
    assert 0.62 < d["avg_r2_g2"] < 0.76, f"G2 mean R2 {d['avg_r2_g2']:.3f} outside [0.62,0.76]"


def test_xiii_g2_negative_r2_fraction():
    """~41% of bootstrap members have a negative Group II factor XIII R^2 — the
    XIII channel is structurally under-determined (manuscript Results,
    'Identifiability analysis'; Supplementary §S4). Recomputed from each member's
    stored Group II XIII prediction vs. the data.
    Source: 22/ensemble_members.json g2_xiii + data/csv."""
    import numpy as np
    from src.data import load_data
    from src.fit import r_squared

    m = _load(A22 / "ensemble_members.json")["members"]
    _, g2 = load_data()
    n = len(g2.xiii)
    r2s = [r_squared(np.asarray(mem["g2_xiii"])[:n], g2.xiii)
           for mem in m if not mem.get("failed")]
    frac_neg = sum(r2 < 0 for r2 in r2s) / len(r2s)
    assert 0.30 < frac_neg < 0.52, (
        f"negative-R2 fraction {frac_neg:.2f} outside [0.30,0.52] (~0.41 expected)")
