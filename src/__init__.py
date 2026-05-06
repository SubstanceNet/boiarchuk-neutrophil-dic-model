"""
boiarchuk_neutrophil_dic_model
==============================

Mechanistic ODE model of neutrophil-driven DIC syndrome pathogenesis,
calibrated on Boyarchuk O. D. experimental data (1998-2023).

Group I:  control DIC (Эфа-2 venom challenge, n=40)
Group II: granulocytopoiesis-suppressed (myelosan + Эфа-2, n=40)

Joint fit: 24 shared biochemical parameters + 2 myelosan modifiers (km, tm).
Group differences enter only through:
  - N(t):     measured neutrophil count
  - kr_eff:   neutrophil clearance rate (G1: kr; G2: kr * km)
  - tp2_eff:  inflammatory peak time   (G1: tp2; G2: tp2 * tm)

Public API:
    from boiarchuk_dic import config, load_data, solve_group, joint_cost, run_fit
"""

__version__ = "0.1.0+phase0"
__authors__ = ["Olena D. Boiarchuk", "Oleksiy Onasenko"]
__status__ = "Research"

from .config import NAMES, BOUNDS, N1_BASE
from .data import load_data, build_neutrophil_interpolators
from .model import solve_group
from .fit import joint_cost, run_fit, r_squared

__all__ = [
    "NAMES",
    "BOUNDS",
    "N1_BASE",
    "load_data",
    "build_neutrophil_interpolators",
    "solve_group",
    "joint_cost",
    "run_fit",
    "r_squared",
]
