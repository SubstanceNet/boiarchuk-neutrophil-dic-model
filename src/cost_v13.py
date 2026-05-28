"""
v13 cost function: symmetric per-group, hard-coded uniform weighting.

Drop-in replacement for src.fit.joint_cost. Mathematical content distinct
from v12; v12 lives untouched in src.fit (Phase 0 reproducibility preserved).

Design decisions (Phase 2 step 1, see notes/known_issues.md and
analyses/01-04 FINDINGS):

1. SYMMETRIC. G1 and G2 contribute through identical algebraic form
   (sum of normalised RMSE across 6 observables). No W_SURV asymmetry.

2. UNIFORM WEIGHTING. Hard-coded ones(n_timepoints) on both groups.
   Validated by analysis 04: ad-hoc W_SURV (down-weighting late G1)
   was load-bearing in the wrong direction.

3. EXPLICIT GROUP BALANCE. Linear combination W_GROUP[0] * G1 +
   W_GROUP[1] * G2. Default (1.0, 1.0) — v12-compatible scale, so the
   relative weight of structural priors (W_SPLIT, saturation_penalty)
   is preserved. Group balance can be re-tuned (e.g., to (0.5, 0.5)
   for symmetric weighting) as a sensitivity option in later analyses.

4. STRUCTURAL PRIORS UNCHANGED. W_SPLIT mechanism-split constraint
   (validated in analysis 01) and Hn-saturation penalty (numerical guard)
   carry over from v12.

5. PER-OBSERVABLE NORMALISATION = v12 SC[]. Kept for backward-compat
   conceptually; per-group-std normalisation can be added later as a
   sensitivity option without breaking the v13 baseline.

6. NO NONLINEAR TERMS. No max-penalty, no barrier on R^2 < 0. Phase 1
   showed the binding issue is architectural (I-2), not cost-nonlinearity.
   Adding nonlinearity here would mask the architectural penalty.
"""
from __future__ import annotations
import numpy as np
from scipy.interpolate import interp1d

from . import config as cfg
from .data import GroupData
from .model import solve_group


# ============================================================
#  Group balance (default symmetric)
# ============================================================
W_GROUP_DEFAULT: tuple[float, float] = (1.0, 1.0)


def _group_residual_sum(
    o: dict, g: GroupData,
) -> tuple[float, dict[str, float]]:
    """Sum of normalised RMSE across the 6 observables for one group.

    Returns (total, per_observable_dict) for both scalar use and
    decomposition inspection.
    """
    pairs = [
        ("recalc",   g.recalc),
        ("thrombin", g.thrombin),
        ("fib",      g.fib),
        ("xiii",     g.xiii),
        ("AP",       g.AP),
        ("D",        g.deg),
    ]
    per_obs = {}
    total = 0.0
    for k, d in pairs:
        m = o[k][:len(d)]
        # Uniform weighting (hard-coded), normalised by v12 SC.
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
    """Run ODE for both groups; None on failure."""
    kr_g1 = pv[1]
    kr_g2 = pv[1] * pv[24]
    tp2_g1 = pv[8]
    tp2_g2 = pv[8] * pv[25]
    try:
        o1 = solve_group(pv, g1.T, n1_interp, t_fine_g1, kr_g1, tp2_g1)
        o2 = solve_group(pv, g2.T, n2_interp, t_fine_g2, kr_g2, tp2_g2)
    except Exception:
        return None
    keys = ("D", "AP", "recalc", "thrombin", "fib", "xiii")
    for o in (o1, o2):
        if any(np.any(np.isnan(o[k])) for k in keys):
            return None
    return o1, o2


def _mechanism_split_residual(o1: dict, pv: np.ndarray) -> float:
    """Sum-of-squared-deviations from target neutrophil-share fractions
    on G1 day 2. Returns 0 if amplitudes too small to evaluate.

    This is identical to the v12 constraint (validated in analysis 01),
    but reorganised as a separate function for clarity and decomposition.
    """
    idx2 = 2
    V2 = o1["V"][idx2]
    AP2 = o1["AP"][idx2]
    Nr2 = o1["Nr"][idx2]
    if V2 <= 1e-6 or AP2 <= 1e-6:
        return 0.0
    res = 0.0
    # recalc
    vr, nr = pv[11] * V2, pv[12] * AP2
    if (vr + nr) > 1.0:
        res += ((nr / (vr + nr)) - cfg.NEUTRO_FRAC["recalc"]) ** 2
    # fib
    vf, nf = pv[16] * V2, pv[17] * AP2
    if (vf + nf) > 1.0:
        res += ((nf / (vf + nf)) - cfg.NEUTRO_FRAC["fib"]) ** 2
    # xiii
    vx, nx = pv[20] * V2, pv[21] * AP2 * Nr2
    if (vx + nx) > 1.0:
        res += ((nx / (vx + nx)) - cfg.NEUTRO_FRAC["xiii"]) ** 2
    return res


def joint_cost_v13(
    pv: np.ndarray,
    g1: GroupData, g2: GroupData,
    n1_interp: interp1d, n2_interp: interp1d,
    t_fine_g1: np.ndarray, t_fine_g2: np.ndarray,
    w_group: tuple[float, float] = W_GROUP_DEFAULT,
) -> float:
    """v13 joint cost: scalar.

    cost = w_group[0] * G1_residuals
         + w_group[1] * G2_residuals
         + W_SPLIT * mechanism_split_residual
         + (HN_SATURATION_PENALTY if Hn near saturation in G1)

    Returns COST_PENALTY_NAN on integration failure.
    """
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


def joint_cost_v13_decomposed(
    pv: np.ndarray,
    g1: GroupData, g2: GroupData,
    n1_interp: interp1d, n2_interp: interp1d,
    t_fine_g1: np.ndarray, t_fine_g2: np.ndarray,
    w_group: tuple[float, float] = W_GROUP_DEFAULT,
) -> dict:
    """v13 joint cost: full decomposition for inspection.

    Returns dict with keys:
      total              — same scalar as joint_cost_v13
      g1_total           — sum of G1 normalised RMSE
      g2_total           — sum of G2 normalised RMSE
      g1_per_observable  — per-observable G1 contributions
      g2_per_observable  — per-observable G2 contributions
      constraint         — raw mechanism-split residual
      constraint_weighted — W_SPLIT * constraint
      saturation_penalty — 0 or HN_SATURATION_PENALTY
      w_group            — group weights used
      failed             — True if integration failed (other fields are None)
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
    )
