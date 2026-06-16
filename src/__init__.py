"""
boiarchuk_neutrophil_dic_model
==============================

Mechanistic ODE model of neutrophil-driven DIC syndrome pathogenesis,
calibrated on Boyarchuk O. D. experimental data (1998-2023).

Group I:  control DIC (Эфа-2 / ethylphenacin challenge, n=40)
Group II: granulocytopoiesis-suppressed (myelosan + Эфа-2, n=40)

Joint fit: 24 shared biochemical parameters + 2 myelosan modifiers (km, tm).
Group differences enter only through:
  - N(t):     measured neutrophil count
  - kr_eff:   neutrophil clearance rate (G1: kr; G2: kr * km)
  - tp2_eff:  inflammatory peak time   (G1: tp2; G2: tp2 * tm)

Public API (the importable package root is ``src``):
    from src import config, load_data, solve_group, run_fit
    from src import joint_cost_v13        # canonical v13 cost (manuscript baseline)
    from src import joint_cost            # legacy v12 cost (reproducibility only)
"""

__version__ = "1.0.2"
__authors__ = ["Olena D. Boiarchuk", "Oleksiy Onasenko"]
__status__ = "Research"

from .config import NAMES, BOUNDS, N1_BASE
from .data import load_data, build_neutrophil_interpolators
from .model import solve_group
from .cost_v13 import joint_cost_v13          # canonical production cost (v13)
from .fit import joint_cost, run_fit, r_squared   # joint_cost is the legacy v12 cost

__all__ = [
    "NAMES",
    "BOUNDS",
    "N1_BASE",
    "load_data",
    "build_neutrophil_interpolators",
    "solve_group",
    "joint_cost_v13",   # canonical v13 cost
    "joint_cost",       # legacy v12 cost (kept for archive/v12 reproducibility)
    "run_fit",
    "r_squared",
]
