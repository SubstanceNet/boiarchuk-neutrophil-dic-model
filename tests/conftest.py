"""Shared pytest fixtures."""

from __future__ import annotations
import sys
from pathlib import Path

# Ensure project root is on sys.path when running pytest from any cwd.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import pytest

from src import config as cfg
from src.data import load_data, build_neutrophil_interpolators
from src.model import make_fine_grids


@pytest.fixture(scope="session")
def groups():
    return load_data()


@pytest.fixture(scope="session")
def neutro_interps(groups):
    g1, g2 = groups
    return build_neutrophil_interpolators(g1, g2)


@pytest.fixture(scope="session")
def fine_grids():
    return make_fine_grids()


@pytest.fixture(scope="session")
def midpoint_params():
    """Parameter vector at the midpoint of all bounds — a deterministic test point."""
    return np.array([(lo + hi) / 2 for (lo, hi) in cfg.BOUNDS], dtype=float)
