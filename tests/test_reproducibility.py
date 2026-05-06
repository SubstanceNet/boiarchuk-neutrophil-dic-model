"""
Reproducibility: the migrated cost function (src.fit.joint_cost) must produce
NUMERICALLY IDENTICAL output to the archived v12 cost function (archive/v12/
model_v12.py:_cost_core) for the same parameter vector.

This is the Phase-0 contract. A failure here means refactoring changed
model behaviour — which is forbidden in Phase 0.

Tolerance: 1e-12 absolute. The two implementations share scipy.integrate.odeint
under the hood with identical args, so they should agree to floating-point.
"""

from __future__ import annotations
import importlib.util
from pathlib import Path
import numpy as np
import pytest

ARCHIVE_PATH = Path(__file__).resolve().parent.parent / "archive" / "v12" / "model_v12.py"


def _load_v12():
    if not ARCHIVE_PATH.exists():
        pytest.skip(f"archive/v12/model_v12.py not present at {ARCHIVE_PATH}")
    spec = importlib.util.spec_from_file_location("v12_archive", str(ARCHIVE_PATH))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def test_param_vectors():
    """Several distinct parameter vectors to test reproducibility on."""
    from src import config as cfg
    rng = np.random.default_rng(42)
    pvs = []
    # Midpoint of bounds
    pvs.append(np.array([(lo + hi) / 2 for lo, hi in cfg.BOUNDS]))
    # Several random points in bounds
    for _ in range(5):
        pv = np.array([rng.uniform(lo, hi) for lo, hi in cfg.BOUNDS])
        pvs.append(pv)
    return pvs


def test_cost_byte_identical(test_param_vectors, groups, neutro_interps, fine_grids):
    """src.fit.joint_cost must match archive v12._cost_core for every test pv."""
    v12 = _load_v12()
    from src.fit import joint_cost
    g1, g2 = groups
    n1, n2 = neutro_interps
    tfg1, tfg2 = fine_grids

    for i, pv in enumerate(test_param_vectors):
        c_old = v12._cost_core(pv)
        c_new = joint_cost(pv, g1, g2, n1, n2, tfg1, tfg2)
        # Both can be 1e6 (NaN penalty); accept that as match.
        if c_old >= 1e6 - 1 and c_new >= 1e6 - 1:
            continue
        assert np.isclose(c_old, c_new, atol=1e-12, rtol=1e-12), (
            f"Test pv #{i}: c_old={c_old:.15e}, c_new={c_new:.15e}, "
            f"|delta|={abs(c_old - c_new):.3e}"
        )


def test_solve_states_byte_identical(midpoint_params, groups, neutro_interps, fine_grids):
    """ODE state trajectories must match between v12._solve and src.model.solve_group."""
    v12 = _load_v12()
    from src.model import solve_group
    g1, g2 = groups
    n1, n2 = neutro_interps
    tfg1, tfg2 = fine_grids
    pv = midpoint_params

    o_old = v12._solve(pv, g1.T, n1, tfg1, pv[1], pv[8])
    o_new = solve_group(pv, g1.T, n1, tfg1, pv[1], pv[8])

    for k in ("D", "AP", "Hc", "Hn", "X", "recalc", "thrombin", "fib", "xiii"):
        np.testing.assert_allclose(
            o_new[k], o_old[k], atol=1e-12, rtol=1e-12,
            err_msg=f"State {k!r} differs between v12 and src",
        )


def test_quick_fit_runs(groups):
    """Quick fit completes without error and produces sensible output.

    This does NOT pin the optimal cost (DE+NM is sensitive to scipy version),
    but it verifies that the full pipeline is wired up correctly. Slow test
    (~30-60 s); marked accordingly.
    """
    from src.fit import run_fit
    g1, g2 = groups
    result = run_fit(g1, g2, quick=True, seeds=[42], workers=-1, verbose=False)
    assert np.isfinite(result["best_cost"])
    assert result["best_cost"] < 100.0   # any sensible fit lands well under this
    assert result["best_x"].shape == (26,)


# Mark slow test so it can be skipped: pytest -m "not slow"
test_quick_fit_runs = pytest.mark.slow(test_quick_fit_runs)
