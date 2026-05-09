"""
v13 group-specific cost: extends v13 with a separate cx_g2 parameter.

Diagnostic implementation for Phase 2 step 2 (analysis 07). The XIII
channel parameter cx is split into cx_g1 (used for G1 group, stays at
parameter index 21) and cx_g2 (new parameter at index 26).

Both cx_g1 and cx_g2 share the same bounds (10, 600) — symmetric, not
modifier-style.

ARCHITECTURE NOTE. This is a PARALLEL implementation. It does NOT touch
src/fit.py, src/model.py, src/config.py, or src/cost_v13.py. v12 byte-
identical reproducibility (test_reproducibility.py) and v13 baseline
(analysis 05) remain valid.

If the experiment validates this candidate, promote to production
following TODO-1 in notes/known_issues.md.
"""
from __future__ import annotations
import numpy as np
from scipy.interpolate import interp1d

from . import config as cfg
from .data import GroupData
from .model import solve_group


# ============================================================
#  Extended parameter space: 26 v13 params + 1 group-specific cx_g2
# ============================================================
N_BASE = len(cfg.BOUNDS)               # 26
CX_G2_INDEX = N_BASE                   # 26
N_PARAMS_GS = N_BASE + 1               # 27

# Bounds for cx_g2 — identical to bounds for cx (parameter 21).
CX_BOUNDS = cfg.BOUNDS[21]             # (10.0, 600.0)
BOUNDS_GS = list(cfg.BOUNDS) + [CX_BOUNDS]
NAMES_GS = list(cfg.NAMES) + ["cx_g2"]

# Mirror v13 default group balance.
W_GROUP_DEFAULT: tuple[float, float] = (1.0, 1.0)


def _split_params(pv: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Given a 27-dim parameter vector, return two 26-dim views:
    pv_g1 (cx at index 21 = pv[21]) and pv_g2 (cx at index 21 = pv[26]).

    pv_g1 is the original first 26 elements (cx_g1 is the v13 cx).
    pv_g2 is a copy with cx (index 21) replaced by pv[26].
    """
    pv_g1 = np.asarray(pv[:N_BASE])
    pv_g2 = pv_g1.copy()
    pv_g2[21] = pv[CX_G2_INDEX]
    return pv_g1, pv_g2


def _group_residual_sum(o: dict, g: GroupData) -> tuple[float, dict[str, float]]:
    """Same as cost_v13: sum of normalised RMSE across 6 observables."""
    pairs = [
        ("recalc",   g.recalc),
        ("thrombin", g.thrombin),
        ("fib",      g.fib),
        ("xiii",     g.xiii),
        ("AP",       g.AP),
        ("D",        g.deg),
    ]
    per_obs: dict[str, float] = {}
    total = 0.0
    for k, d in pairs:
        m = o[k][:len(d)]
        contrib = float(np.sqrt(np.mean(((m - d) / cfg.SC[k]) ** 2)))
        per_obs[k] = contrib
        total += contrib
    return total, per_obs


def _solve_both(
    pv: np.ndarray,
    g1: GroupData, g2: GroupData,
    n1_interp: interp1d, n2_interp: interp1d,
    t_fine_g1: np.ndarray, t_fine_g2: np.ndarray,
) -> tuple[dict, dict] | None:
    """Run ODE for both groups with group-specific cx; None on failure."""
    pv_g1, pv_g2 = _split_params(pv)
    kr_g1 = pv_g1[1]
    kr_g2 = pv_g2[1] * pv_g2[24]
    tp2_g1 = pv_g1[8]
    tp2_g2 = pv_g2[8] * pv_g2[25]
    try:
        o1 = solve_group(pv_g1, g1.T, n1_interp, t_fine_g1, kr_g1, tp2_g1)
        o2 = solve_group(pv_g2, g2.T, n2_interp, t_fine_g2, kr_g2, tp2_g2)
    except Exception:
        return None
    keys = ("D", "AP", "recalc", "thrombin", "fib", "xiii")
    for o in (o1, o2):
        if any(np.any(np.isnan(o[k])) for k in keys):
            return None
    return o1, o2


def _mechanism_split_residual(o1: dict, pv: np.ndarray) -> float:
    """Mechanism-split constraint on G1 day 2.

    Identical to cost_v13: uses the G1 parameters (pv[:26]). Group-specific
    cx_g2 does not enter this constraint because the constraint operates
    on G1 only.
    """
    pv_g1 = pv[:N_BASE]
    idx2 = 2
    V2 = o1["V"][idx2]
    AP2 = o1["AP"][idx2]
    Nr2 = o1["Nr"][idx2]
    if V2 <= 1e-6 or AP2 <= 1e-6:
        return 0.0
    res = 0.0
    vr, nr = pv_g1[11] * V2, pv_g1[12] * AP2
    if (vr + nr) > 1.0:
        res += ((nr / (vr + nr)) - cfg.NEUTRO_FRAC["recalc"]) ** 2
    vf, nf = pv_g1[16] * V2, pv_g1[17] * AP2
    if (vf + nf) > 1.0:
        res += ((nf / (vf + nf)) - cfg.NEUTRO_FRAC["fib"]) ** 2
    vx, nx = pv_g1[20] * V2, pv_g1[21] * AP2 * Nr2
    if (vx + nx) > 1.0:
        res += ((nx / (vx + nx)) - cfg.NEUTRO_FRAC["xiii"]) ** 2
    return res


def joint_cost_v13_gs(
    pv: np.ndarray,
    g1: GroupData, g2: GroupData,
    n1_interp: interp1d, n2_interp: interp1d,
    t_fine_g1: np.ndarray, t_fine_g2: np.ndarray,
    w_group: tuple[float, float] = W_GROUP_DEFAULT,
) -> float:
    """v13 group-specific joint cost (scalar). pv is 27-dim."""
    sol = _solve_both(pv, g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2)
    if sol is None:
        return cfg.COST_PENALTY_NAN
    o1, o2 = sol
    g1_total, _ = _group_residual_sum(o1, g1)
    g2_total, _ = _group_residual_sum(o2, g2)
    constraint = _mechanism_split_residual(o1, pv)
    cost = (
        w_group[0] * g1_total
        + w_group[1] * g2_total
        + cfg.W_SPLIT * constraint
    )
    if np.any(o1["Hn"] > pv[7] * 0.99):
        cost += cfg.HN_SATURATION_PENALTY
    return float(cost)


def joint_cost_v13_gs_decomposed(
    pv: np.ndarray,
    g1: GroupData, g2: GroupData,
    n1_interp: interp1d, n2_interp: interp1d,
    t_fine_g1: np.ndarray, t_fine_g2: np.ndarray,
    w_group: tuple[float, float] = W_GROUP_DEFAULT,
) -> dict:
    """v13 group-specific joint cost: full decomposition for inspection.

    Same structure as joint_cost_v13_decomposed, plus reports cx_g1 vs cx_g2
    explicitly for diagnostic purposes.
    """
    sol = _solve_both(pv, g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2)
    if sol is None:
        return dict(
            total=cfg.COST_PENALTY_NAN,
            failed=True,
            g1_total=None, g2_total=None,
            g1_per_observable=None, g2_per_observable=None,
            constraint=None, constraint_weighted=None,
            saturation_penalty=None, w_group=w_group,
            cx_g1=float(pv[21]), cx_g2=float(pv[CX_G2_INDEX]),
        )
    o1, o2 = sol
    g1_total, g1_per_obs = _group_residual_sum(o1, g1)
    g2_total, g2_per_obs = _group_residual_sum(o2, g2)
    constraint = _mechanism_split_residual(o1, pv)
    constraint_weighted = cfg.W_SPLIT * constraint
    saturation_penalty = (
        cfg.HN_SATURATION_PENALTY
        if np.any(o1["Hn"] > pv[7] * 0.99) else 0.0
    )
    total = (
        w_group[0] * g1_total
        + w_group[1] * g2_total
        + constraint_weighted
        + saturation_penalty
    )
    return dict(
        total=float(total),
        failed=False,
        g1_total=float(g1_total),
        g2_total=float(g2_total),
        g1_per_observable=g1_per_obs,
        g2_per_observable=g2_per_obs,
        constraint=float(constraint),
        constraint_weighted=float(constraint_weighted),
        saturation_penalty=float(saturation_penalty),
        w_group=tuple(w_group),
        cx_g1=float(pv[21]),
        cx_g2=float(pv[CX_G2_INDEX]),
    )
