"""
ODE model: 5 states [D, AP, Hc, Hn, X] and 4 hemostatic observables.

Mathematical content is byte-identical to archive/v12/model_v12.py.
Phase 0 contract: numerical equivalence (verified by tests/test_reproducibility.py).

State variables
---------------
D     dimensionless [0, 1]   fraction of degranulated neutrophils
AP    BO units                acid phosphatase activity in plasma
Hc    arbitrary               venom-driven coagulation factor reservoir
Hn    arbitrary, [0, Hm]      neutrophil-driven coagulation factor reservoir
X     %                       Factor XIII activity (delta)

Driving inputs
--------------
V(t)  gamma-like venom pulse,  V(t) = (t/tv) * exp(1 - t/tv)  with tv = TV_FIX
N(t)  measured neutrophil count, normalised as Nr = N(t) / N1_BASE
S(t)  inflammatory signal,  S = V + a2 * gauss(tp2, s2) * Nr * (1 - D)
      The (1 - D) factor enforces self-limiting inflammation: degranulated
      cells cannot sustain cytokine output.

Group differences
-----------------
G1 uses  kr_eff = kr,        tp2_eff = tp2
G2 uses  kr_eff = kr * km,   tp2_eff = tp2 * tm
All other parameters are shared.
"""

from __future__ import annotations
import numpy as np
from scipy.integrate import odeint
from scipy.interpolate import interp1d

from . import config as cfg


# ============================================================
#  Driving functions
# ============================================================

def _gauss(t: np.ndarray | float, mu: float, sig: float) -> np.ndarray | float:
    """Unnormalised Gaussian shape (peak = 1 at t = mu)."""
    return np.exp(-0.5 * ((t - mu) / sig) ** 2)


def _V_scalar(t: float, tv: float = cfg.TV_FIX) -> float:
    """Gamma-like venom pulse, scalar (used inside ODE rhs)."""
    if t <= 0:
        return 0.0
    r = t / tv
    return r * np.exp(1.0 - r)


def _V(t: np.ndarray | float, tv: float = cfg.TV_FIX) -> np.ndarray:
    """Vectorised venom pulse for post-hoc evaluation on time grids."""
    t = np.asarray(t, dtype=float)
    r = t / tv
    return np.where(t >= 0, r * np.exp(1.0 - r), 0.0)


# ============================================================
#  ODE right-hand side
# ============================================================

def _rhs(
    y: list[float],
    t: float,
    pv: np.ndarray,
    Nf: interp1d,
    kr_eff: float,
    tp2_eff: float,
) -> list[float]:
    """Right-hand side of the 5-state ODE.

    pv is an array of all 26 parameters in NAMES order. kr_eff and tp2_eff
    are precomputed group-effective values (G1: kr / tp2; G2: kr*km / tp2*tm).
    """
    D = max(min(y[0], 1.0), 0.0)
    AP = max(y[1], 0.0)
    Hc = max(y[2], 0.0)
    Hn = np.clip(y[3], 0.0, pv[7] * 0.999)   # Hm is pv[7]
    X = y[4]

    V = _V_scalar(t)
    Nr = Nf(t) / cfg.N1_BASE

    # Self-limiting inflammatory signal
    S = V + pv[10] * _gauss(t, tp2_eff, pv[9]) * Nr * (1.0 - D)

    dD = pv[0] * S * (1.0 - D) - kr_eff * D
    dAP = pv[2] * D - pv[3] * AP
    dHc = pv[4] * V - cfg.KCD_FIX * Hc

    cap = max(1.0 - Hn / pv[7], 0.005)
    dHn = pv[5] * min(AP * AP, 10.0) * cap - pv[6] * Hn

    gHn = Hn / max(1.0 - Hn / pv[7], 0.005)
    liver = max(1.0 - Hn / pv[7], 0.0)
    dX = pv[20] * V + pv[21] * AP * Nr - pv[22] * gHn - pv[23] * liver * X

    return [dD, dAP, dHc, dHn, dX]


# ============================================================
#  Solve and observe
# ============================================================

def solve_group(
    pv: np.ndarray,
    t_eval: np.ndarray,
    Nf: interp1d,
    t_fine: np.ndarray,
    kr_eff: float,
    tp2_eff: float,
) -> dict[str, np.ndarray]:
    """Integrate the ODE on `t_fine`, evaluate states + observables on `t_eval`.

    Returns a dict with keys:
      - state arrays: D (as %), AP, Hc, Hn, gHn, X
      - drivers:      V, Nr
      - observables:  recalc, thrombin, fib, xiii  (deltas, model output)

    Raises RuntimeError if the integrator returns NaN.
    """
    y = odeint(
        _rhs,
        y0=[0.0, 0.0, 0.0, 0.0, 0.0],
        t=t_fine,
        args=(pv, Nf, kr_eff, tp2_eff),
        rtol=cfg.ODE_RTOL,
        atol=cfg.ODE_ATOL,
        mxstep=cfg.ODE_MXSTEP,
    )
    if np.any(np.isnan(y)):
        raise RuntimeError("ODE integrator returned NaN")

    # Interpolate from fine integration grid onto evaluation grid
    interps = [
        interp1d(t_fine, y[:, i], kind="linear", fill_value="extrapolate")
        for i in range(5)
    ]
    D = np.clip(interps[0](t_eval), 0.0, 1.0)
    AP = np.maximum(interps[1](t_eval), 0.0)
    Hc = np.maximum(interps[2](t_eval), 0.0)
    Hn = np.clip(interps[3](t_eval), 0.0, pv[7] * 0.999)
    X = interps[4](t_eval)

    V_at = _V(t_eval)
    gHn = Hn / np.maximum(1.0 - Hn / pv[7], 0.005)
    Nr = Nf(t_eval) / cfg.N1_BASE

    return dict(
        D=D * 100.0,    # report as %
        AP=AP,
        Hc=Hc,
        Hn=Hn,
        gHn=gHn,
        V=V_at,
        Nr=Nr,
        X=X,
        recalc=-pv[11] * V_at - pv[12] * AP + pv[13] * gHn,
        thrombin=-pv[14] * V_at + pv[15] * gHn,
        fib=+pv[16] * V_at + pv[17] * AP - pv[18] * gHn - pv[19] * Hc,
        xiii=X,
    )


def make_fine_grids() -> tuple[np.ndarray, np.ndarray]:
    """Default fine integration grids for G1 (0..20 d) and G2 (0..9 d)."""
    return (
        np.linspace(0.0, 20.0, 250),   # G1: covers full 19-day observation
        np.linspace(0.0, 9.0, 200),    # G2: covers full 8-day observation
    )
