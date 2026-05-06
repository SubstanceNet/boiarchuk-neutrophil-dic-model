"""
Smoke tests: model loads, ODE integrates, cost is finite.

These should run in seconds. If any of them fails, the package is broken
at a structural level and other tests are not meaningful.
"""

from __future__ import annotations
import time
import numpy as np

from src import config as cfg
from src.model import solve_group
from src.fit import joint_cost


def test_param_inventory_consistent():
    assert len(cfg.NAMES) == 26
    assert len(cfg.BOUNDS) == 26
    assert len(set(cfg.NAMES)) == 26   # no duplicate names


def test_data_loads(groups):
    g1, g2 = groups
    assert g1.name == "G1"
    assert g2.name == "G2"
    assert g1.n_timepoints == 16
    assert g2.n_timepoints == 9
    assert g1.T[0] == 0.0
    assert g1.T[-1] == 19.0
    assert g2.T[0] == 0.0
    assert g2.T[-1] == 8.0


def test_baseline_neutrophil_count(groups):
    """N1_BASE constant equals G1 day-0 neutrophil count from CSV."""
    g1, _ = groups
    assert float(g1.neutrophils[0]) == cfg.N1_BASE


def test_ode_integrates_at_midpoint(midpoint_params, neutro_interps, fine_grids, groups):
    """ODE integrates without error at a midpoint parameter vector."""
    g1, g2 = groups
    n1, n2 = neutro_interps
    t_fine_g1, t_fine_g2 = fine_grids
    pv = midpoint_params

    o1 = solve_group(pv, g1.T, n1, t_fine_g1, kr_eff=pv[1], tp2_eff=pv[8])
    o2 = solve_group(pv, g2.T, n2, t_fine_g2, kr_eff=pv[1] * pv[24], tp2_eff=pv[8] * pv[25])

    for o, label in [(o1, "G1"), (o2, "G2")]:
        for k in ("D", "AP", "Hc", "Hn", "X", "recalc", "thrombin", "fib", "xiii"):
            assert np.all(np.isfinite(o[k])), f"{label}: NaN/Inf in {k}"


def test_cost_is_finite_at_midpoint(midpoint_params, groups, neutro_interps, fine_grids):
    g1, g2 = groups
    n1, n2 = neutro_interps
    t_fine_g1, t_fine_g2 = fine_grids
    cost = joint_cost(midpoint_params, g1, g2, n1, n2, t_fine_g1, t_fine_g2)
    assert np.isfinite(cost)
    assert cost < cfg.COST_PENALTY_NAN


def test_cost_evaluation_speed(midpoint_params, groups, neutro_interps, fine_grids):
    """One cost evaluation should take less than 1 second on any reasonable machine.

    On reference workstation (Ryzen 9 8945HS) it takes ~50-150 ms per call.
    A regression to >1 s means an ODE-stiffness or integration-tolerance issue.
    """
    g1, g2 = groups
    n1, n2 = neutro_interps
    t_fine_g1, t_fine_g2 = fine_grids

    # Warm up
    _ = joint_cost(midpoint_params, g1, g2, n1, n2, t_fine_g1, t_fine_g2)

    t0 = time.time()
    n_repeats = 5
    for _ in range(n_repeats):
        joint_cost(midpoint_params, g1, g2, n1, n2, t_fine_g1, t_fine_g2)
    avg_ms = (time.time() - t0) / n_repeats * 1000
    assert avg_ms < 1000, f"Cost eval too slow: {avg_ms:.0f} ms"
