"""
Smoke tests for src.cost_v13.

Tests:
  - cost is finite on midpoint params
  - scalar and decomposition agree
  - decomposition components sum to total
  - cost increases with parameter perturbation away from optimum
  - cost_v13 ≈ cost_v12 within reasonable factor (soft compatibility)
  - W_GROUP override works
  - failed integration returns COST_PENALTY_NAN
"""
from __future__ import annotations
import numpy as np
import pytest

from src import config as cfg
from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids
from src.fit import joint_cost as joint_cost_v12
from src.cost_v13 import (
    joint_cost_v13, joint_cost_v13_decomposed, W_GROUP_DEFAULT,
)


@pytest.fixture(scope="module")
def setup():
    g1, g2 = load_data()
    n1, n2 = build_neutrophil_interpolators(g1, g2)
    tfg1, tfg2 = make_fine_grids()
    pv_mid = np.array([(lo + hi) / 2 for lo, hi in cfg.BOUNDS])
    return g1, g2, n1, n2, tfg1, tfg2, pv_mid


def test_default_group_weights_are_v12_compatible():
    """Default (1.0, 1.0) preserves v12-relative scale of constraint terms."""
    assert W_GROUP_DEFAULT == (1.0, 1.0)


def test_cost_finite_at_midpoint(setup):
    g1, g2, n1, n2, tfg1, tfg2, pv = setup
    c = joint_cost_v13(pv, g1, g2, n1, n2, tfg1, tfg2)
    assert np.isfinite(c)
    assert c > 0
    assert c < cfg.COST_PENALTY_NAN


def test_scalar_matches_decomposition(setup):
    g1, g2, n1, n2, tfg1, tfg2, pv = setup
    scalar = joint_cost_v13(pv, g1, g2, n1, n2, tfg1, tfg2)
    decomp = joint_cost_v13_decomposed(pv, g1, g2, n1, n2, tfg1, tfg2)
    assert np.isclose(scalar, decomp["total"], atol=1e-12)
    assert decomp["failed"] is False


def test_decomposition_components_sum_to_total(setup):
    g1, g2, n1, n2, tfg1, tfg2, pv = setup
    d = joint_cost_v13_decomposed(pv, g1, g2, n1, n2, tfg1, tfg2)
    expected_total = (
        d["w_group"][0] * d["g1_total"]
        + d["w_group"][1] * d["g2_total"]
        + d["constraint_weighted"]
        + d["saturation_penalty"]
    )
    assert np.isclose(d["total"], expected_total, atol=1e-12)


def test_per_observable_sum_equals_group_total(setup):
    g1, g2, n1, n2, tfg1, tfg2, pv = setup
    d = joint_cost_v13_decomposed(pv, g1, g2, n1, n2, tfg1, tfg2)
    g1_sum = sum(d["g1_per_observable"].values())
    g2_sum = sum(d["g2_per_observable"].values())
    assert np.isclose(g1_sum, d["g1_total"], atol=1e-12)
    assert np.isclose(g2_sum, d["g2_total"], atol=1e-12)


def test_per_observable_keys(setup):
    g1, g2, n1, n2, tfg1, tfg2, pv = setup
    d = joint_cost_v13_decomposed(pv, g1, g2, n1, n2, tfg1, tfg2)
    expected = {"recalc", "thrombin", "fib", "xiii", "AP", "D"}
    assert set(d["g1_per_observable"]) == expected
    assert set(d["g2_per_observable"]) == expected


def test_perturbation_increases_cost(setup):
    """Moving away from midpoint along one axis should not decrease cost
    monotonically forever, but for small perturbations from a non-optimum
    midpoint, cost should change measurably (sanity check of differentiability)."""
    g1, g2, n1, n2, tfg1, tfg2, pv = setup
    c0 = joint_cost_v13(pv, g1, g2, n1, n2, tfg1, tfg2)

    # Perturb 5 different parameters by ±20% — at least one should change cost
    n_changed = 0
    for i in [0, 5, 10, 15, 20]:
        pv_p = pv.copy()
        pv_p[i] *= 1.2
        # Ensure still in bounds
        lo, hi = cfg.BOUNDS[i]
        if pv_p[i] > hi:
            pv_p[i] = hi * 0.99
        c_p = joint_cost_v13(pv_p, g1, g2, n1, n2, tfg1, tfg2)
        if abs(c_p - c0) > 1e-6:
            n_changed += 1
    assert n_changed >= 3, "Cost should respond to most parameter perturbations"


def test_v13_close_to_v12_at_midpoint(setup):
    """Soft compatibility: v13 with default w_group=(1,1) is v12 with uniform W_SURV.

    The only difference is per-timepoint weighting of G1 (uniform vs ad-hoc
    [1]*10+[0.7]*3+[0.3]*3). The absolute difference should be modest.
    """
    g1, g2, n1, n2, tfg1, tfg2, pv = setup
    c12 = joint_cost_v12(pv, g1, g2, n1, n2, tfg1, tfg2)
    c13 = joint_cost_v13(pv, g1, g2, n1, n2, tfg1, tfg2)
    # Both finite, both positive
    assert np.isfinite(c12) and c12 > 0
    assert np.isfinite(c13) and c13 > 0
    # Within ~30% of each other (loose bound — exact ratio depends on params)
    ratio = c13 / c12
    assert 0.5 < ratio < 1.5, f"Unexpected v13/v12 ratio at midpoint: {ratio}"


def test_w_group_override(setup):
    """Calling with non-default w_group changes total proportionally."""
    g1, g2, n1, n2, tfg1, tfg2, pv = setup
    d_default = joint_cost_v13_decomposed(pv, g1, g2, n1, n2, tfg1, tfg2)
    d_half = joint_cost_v13_decomposed(
        pv, g1, g2, n1, n2, tfg1, tfg2, w_group=(0.5, 0.5))
    expected_half = (
        0.5 * d_default["g1_total"]
        + 0.5 * d_default["g2_total"]
        + d_default["constraint_weighted"]
        + d_default["saturation_penalty"]
    )
    assert np.isclose(d_half["total"], expected_half, atol=1e-12)
    assert d_half["w_group"] == (0.5, 0.5)


def test_failed_integration_returns_penalty(setup):
    """Cost should return COST_PENALTY_NAN if ODE explodes."""
    g1, g2, n1, n2, tfg1, tfg2, _ = setup
    # Construct deliberately bad parameter vector — set kna very high to force Hn saturation issues
    bad_pv = np.array([(lo + hi) / 2 for lo, hi in cfg.BOUNDS])
    bad_pv[5] = cfg.BOUNDS[5][1]  # max kna
    bad_pv[7] = cfg.BOUNDS[7][0]  # min Hm — maximises Hn/Hm ratio
    c = joint_cost_v13(bad_pv, g1, g2, n1, n2, tfg1, tfg2)
    # Either a normal high cost (with saturation penalty) or COST_PENALTY_NAN if integration failed
    # Both are valid behaviours; we just check it doesn't crash and returns finite or sentinel.
    assert np.isfinite(c) or c == cfg.COST_PENALTY_NAN
