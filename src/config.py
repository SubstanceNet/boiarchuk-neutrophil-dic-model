"""
Centralised configuration: parameter names, bounds, fixed constants, weights.

Every numerical constant that influences the fit lives here. Changes to model
behaviour must go through this file (not buried in model.py or fit.py).

This is a verbatim port of constants from archive/v12/model_v12.py.
Phase 0 contract: numerical equivalence with v12. Any change to a value here
breaks tests/test_reproducibility.py by design.
"""

from __future__ import annotations
import numpy as np

# ============================================================
#  Parameter inventory: 26 = 24 shared + 2 myelosan modifiers
# ============================================================

NAMES: list[str] = [
    # Neutrophil dynamics (shared 0-4)
    "kd",    # 0  degranulation rate (per unit signal, per day)
    "kr",    # 1  recovery / clearance of degranulated state (G1 base; G2 = kr * km)
    "krl",   # 2  AP release rate from degranulated cells
    "kcl",   # 3  AP clearance rate
    "kca",   # 4  Hc accumulation from inducer (vessel-driven)
    # Hn dynamics (shared 5-7)
    "kna",   # 5  Hn formation rate (saturable in AP)
    "knd",   # 6  Hn decay rate
    "Hm",    # 7  Hn carrying capacity
    # Inflammatory pulse (shared 8-10)
    "tp2",   # 8  inflammatory peak time (G1 base; G2 = tp2 * tm)
    "s2",    # 9  inflammatory pulse width
    "a2",    # 10 inflammatory pulse amplitude
    # Recalcification observation (shared 11-13)
    "ar",    # 11 recalc / V coefficient
    "cr",    # 12 recalc / AP coefficient
    "br",    # 13 recalc / gHn coefficient
    # Thrombin observation (shared 14-15)
    "at",    # 14 thrombin / V coefficient
    "bt",    # 15 thrombin / gHn coefficient
    # Fibrinogen observation (shared 16-19)
    "af",    # 16 fib / V coefficient
    "cf",    # 17 fib / AP coefficient
    "bf",    # 18 fib / gHn coefficient
    "df",    # 19 fib / Hc coefficient
    # Factor XIII ODE (shared 20-23)
    "ax",    # 20 XIII production / V
    "cx",    # 21 XIII production / AP * Nr
    "bx",    # 22 XIII degradation / gHn
    "kx",    # 23 XIII liver-modulated resynthesis rate
    # Group-II myelosan modifiers (G2-only, 24-25)
    "km",    # 24 multiplier on kr   for G2 (>1: faster clearance)
    "tm",    # 25 multiplier on tp2  for G2 (<1: shifted-earlier peak)
]

BOUNDS: list[tuple[float, float]] = [
    (0.1,    5.0),    # kd
    (0.1,    5.0),    # kr  [expanded from (0.1, 3.0) in v11.x]
    (0.3,   20.0),    # krl
    (0.3,   20.0),    # kcl
    (0.1,  100.0),    # kca
    (1.0, 1500.0),    # kna [expanded from upper 800 in v11.x]
    (0.01,  10.0),    # knd
    (3.0, 1000.0),    # Hm
    (6.0,   12.0),    # tp2 [narrowed from wide; diagnostic showed 9-10 d]
    (0.8,    6.0),    # s2
    (0.1,   10.0),    # a2
    (1.0,  200.0),    # ar
    (5.0,  600.0),    # cr
    (0.005, 15.0),    # br
    (0.5,   25.0),    # at
    (0.001,  1.5),    # bt
    (1.0,  120.0),    # af
    (5.0,  350.0),    # cf
    (0.001,  8.0),    # bf [expanded from upper 5 in v11.x]
    (0.1,   30.0),    # df
    (1.0,  250.0),    # ax
    (10.0, 600.0),    # cx [bounded — prevents large-number cancellation
                      #     NB: v12 report quotes cx fitted at 1481 in some
                      #     run; that is OUTSIDE current bounds. Bounds here
                      #     match the script in archive/v12/. Discrepancy is
                      #     a known open issue, see notes/known_issues.md.]
    (0.001, 50.0),    # bx
    (0.05,  15.0),    # kx
    (1.5,   15.0),    # km — myelosan kr multiplier
    (0.2,    0.8),    # tm — myelosan tp2 multiplier
]

assert len(NAMES) == len(BOUNDS) == 26, "Parameter inventory mismatch"

# ============================================================
#  Fixed constants (not optimised)
# ============================================================

TV_FIX: float = 1.5      # inducer toxicity pulse time-scale (peak at t = TV_FIX)
KCD_FIX: float = 0.2     # Hc clearance rate

# Baseline neutrophil count for normalisation Nr = N(t) / N1_BASE.
# Equals group I value at t=0 (dissertation table 5.1).
# A test asserts data/csv/group1.csv at t=0 equals this exact value.
N1_BASE: float = 7.3

# ============================================================
#  Cost-function structure
# ============================================================

# Per-observable scale factors for normalised RMSE in cost.
# Approximately the dynamic range of each observable.
SC: dict[str, float] = {
    "recalc":   250.0,
    "thrombin":  22.0,
    "fib":       85.0,
    "xiii":     150.0,
    "AP":         0.85,
    "D":         62.0,
}

# Mechanism-split constraint weight on day-2 of group I.
# Forces neutrophil-share fractions to match experimentally derived ratios.
# NB: this is a strong empirical prior (W=2.0). For Phase 1 we will profile
# the parameters as a function of W to test how strongly results depend on it.
W_SPLIT: float = 2.0

# Target neutrophil-share fractions on day 2 (G1).
# Derived from G2/G1 day-1 ratios in dissertation tables 4.9 / 5.9.
# See v12_report.docx section 3.3 for derivation.
NEUTRO_FRAC: dict[str, float] = {
    "recalc": 0.24,   # 24% neutrophil-mediated, 76% vessel/inducer-mediated
    "fib":    0.76,   # 76% neutrophil-mediated (IL-6 hepatic stimulation)
    "xiii":   0.82,   # 82% neutrophil-mediated (XIII stored in azurophil granules)
}

# Survivor weighting for G1 cost (LEGACY: defined but NOT used by the v13
# cost function src.cost_v13.joint_cost_v13, which weights G1 uniformly;
# analysis 04 showed this down-weighting is non-influential). Retained for
# the v12 cost path (src.fit.joint_cost) and reference.
# 30% mortality occurred on days 10-12; weights downweight late timepoints
# proportionally to surviving sample size (qualitative, not exact n_t/N).
# Length 16 = len(T1).
W_SURV: np.ndarray = np.array([1.0] * 10 + [0.7] * 3 + [0.3] * 3, dtype=float)

# ============================================================
#  Numerical / integration settings
# ============================================================

ODE_RTOL: float = 1e-5
ODE_ATOL: float = 1e-7
ODE_MXSTEP: int = 5000
COST_PENALTY_NAN: float = 1e6
HN_SATURATION_PENALTY: float = 2.0  # added if any Hn value approaches Hm
