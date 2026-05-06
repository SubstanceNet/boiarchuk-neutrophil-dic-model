"""
Data integrity: verify that data/csv/group{1,2}.csv values are byte-identical
to the original numpy literals in archive/v12/model_v12.py.

Phase 0 contract: zero numerical difference between literal and CSV form.
"""

from __future__ import annotations
import importlib.util
from pathlib import Path
import numpy as np
import pytest

ARCHIVE_PATH = Path(__file__).resolve().parent.parent / "archive" / "v12" / "model_v12.py"


def _load_v12():
    """Import archive/v12/model_v12.py as a module without running its main()."""
    if not ARCHIVE_PATH.exists():
        pytest.skip(f"archive/v12/model_v12.py not present at {ARCHIVE_PATH}")
    spec = importlib.util.spec_from_file_location("v12_archive", str(ARCHIVE_PATH))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_g1_csv_matches_v12_literals(groups):
    v12 = _load_v12()
    g1, _ = groups

    np.testing.assert_array_equal(g1.T,           v12.T1)
    np.testing.assert_array_equal(g1.recalc,      v12.RECALC1)
    np.testing.assert_array_equal(g1.thrombin,    v12.THROMB1)
    np.testing.assert_array_equal(g1.fib,         v12.FIB1)
    np.testing.assert_array_equal(g1.xiii,        v12.XIII1)
    np.testing.assert_array_equal(g1.AP,          v12.AP1)
    np.testing.assert_array_equal(g1.deg,         v12.DEG1)
    np.testing.assert_array_equal(g1.neutrophils, v12.N1_DATA)


def test_g2_csv_matches_v12_literals(groups):
    v12 = _load_v12()
    _, g2 = groups

    np.testing.assert_array_equal(g2.T,           v12.T2)
    np.testing.assert_array_equal(g2.recalc,      v12.RECALC2)
    np.testing.assert_array_equal(g2.thrombin,    v12.THROMB2)
    np.testing.assert_array_equal(g2.fib,         v12.FIB2)
    np.testing.assert_array_equal(g2.xiii,        v12.XIII2)
    np.testing.assert_array_equal(g2.AP,          v12.AP2)
    np.testing.assert_array_equal(g2.deg,         v12.DEG2)
    np.testing.assert_array_equal(g2.neutrophils, v12.N2_DATA)


def test_baseline_constant_matches_v12():
    v12 = _load_v12()
    from src import config as cfg
    assert v12.N1_BASE == cfg.N1_BASE
