"""
v13 group-specific cost: factory pattern for any one parameter.

Generalised from initial implementation (analysis 07: cx group-specific).
Now supports any parameter from cfg.NAMES via make_cost_groupspec(name).

ARCHITECTURE NOTE. This is a PARALLEL implementation. It does NOT touch
src/fit.py, src/model.py, src/config.py, or src/cost_v13.py. v12 byte-
identical reproducibility (test_reproducibility.py) and v13 baseline
(analysis 05) remain valid.

Backward compatibility: the original analysis 07 API
(joint_cost_v13_gs, joint_cost_v13_gs_decomposed, BOUNDS_GS, NAMES_GS,
CX_G2_INDEX) is preserved via make_cost_groupspec('cx').
"""
from __future__ import annotations
import numpy as np
from scipy.interpolate import interp1d

from . import config as cfg
from .data import GroupData
from .model import solve_group


N_BASE = len(cfg.BOUNDS)               # 26
W_GROUP_DEFAULT: tuple[float, float] = (1.0, 1.0)


def _group_residual_sum(o: dict, g: GroupData) -> tuple[float, dict[str, float]]:
    """Sum of normalised RMSE across 6 observables. Same as cost_v13."""
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


def _mechanism_split_residual(o1: dict, pv: np.ndarray) -> float:
    """Mechanism-split constraint on G1 day 2.

    Uses pv[:N_BASE] (G1 parameters). Group-specific extension does not
    enter this constraint, which operates on G1 only.
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


class GroupspecCost:
    """One-parameter group-specific v13 cost.

    The chosen parameter (by name from cfg.NAMES) is duplicated:
    pv[:N_BASE] are the standard 26 v13 parameters used for G1.
    pv[N_BASE] is the corresponding G2-version of the chosen parameter,
    used to override pv[idx] when computing G2 dynamics.

    BOUNDS_GS, NAMES_GS extend cfg by one slot (same bounds as the
    duplicated parameter).
    """

    def __init__(self, param_name: str):
        if param_name not in cfg.NAMES:
            raise ValueError(f"Unknown parameter {param_name!r}; "
                             f"must be one of {cfg.NAMES}")
        self.param_name = param_name
        self.idx = cfg.NAMES.index(param_name)
        self.g2_index = N_BASE
        self.n_params = N_BASE + 1
        self.BOUNDS_GS = list(cfg.BOUNDS) + [cfg.BOUNDS[self.idx]]
        self.NAMES_GS = list(cfg.NAMES) + [f"{param_name}_g2"]

    def split_params(self, pv: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Return (pv_g1, pv_g2) — both 26-dim views.

        pv_g1 is pv[:N_BASE].
        pv_g2 is a copy with pv_g2[idx] replaced by pv[N_BASE].
        """
        pv_g1 = np.asarray(pv[:N_BASE])
        pv_g2 = pv_g1.copy()
        pv_g2[self.idx] = pv[self.g2_index]
        return pv_g1, pv_g2

    def _solve_both(
        self,
        pv: np.ndarray,
        g1: GroupData, g2: GroupData,
        n1_interp: interp1d, n2_interp: interp1d,
        t_fine_g1: np.ndarray, t_fine_g2: np.ndarray,
    ) -> tuple[dict, dict] | None:
        pv_g1, pv_g2 = self.split_params(pv)
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

    def cost(
        self, pv: np.ndarray,
        g1: GroupData, g2: GroupData,
        n1_interp: interp1d, n2_interp: interp1d,
        t_fine_g1: np.ndarray, t_fine_g2: np.ndarray,
        w_group: tuple[float, float] = W_GROUP_DEFAULT,
    ) -> float:
        sol = self._solve_both(pv, g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2)
        if sol is None:
            return cfg.COST_PENALTY_NAN
        o1, o2 = sol
        g1_total, _ = _group_residual_sum(o1, g1)
        g2_total, _ = _group_residual_sum(o2, g2)
        constraint = _mechanism_split_residual(o1, pv)
        c = (
            w_group[0] * g1_total
            + w_group[1] * g2_total
            + cfg.W_SPLIT * constraint
        )
        if np.any(o1["Hn"] > pv[7] * 0.99):
            c += cfg.HN_SATURATION_PENALTY
        return float(c)

    def cost_decomposed(
        self, pv: np.ndarray,
        g1: GroupData, g2: GroupData,
        n1_interp: interp1d, n2_interp: interp1d,
        t_fine_g1: np.ndarray, t_fine_g2: np.ndarray,
        w_group: tuple[float, float] = W_GROUP_DEFAULT,
    ) -> dict:
        sol = self._solve_both(pv, g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2)
        common = {
            "param_name": self.param_name,
            f"{self.param_name}_g1": float(pv[self.idx]),
            f"{self.param_name}_g2": float(pv[self.g2_index]),
            "w_group": tuple(w_group),
        }
        if sol is None:
            return dict(
                total=cfg.COST_PENALTY_NAN, failed=True,
                g1_total=None, g2_total=None,
                g1_per_observable=None, g2_per_observable=None,
                constraint=None, constraint_weighted=None,
                saturation_penalty=None, **common,
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
            total=float(total), failed=False,
            g1_total=float(g1_total), g2_total=float(g2_total),
            g1_per_observable=g1_per_obs, g2_per_observable=g2_per_obs,
            constraint=float(constraint),
            constraint_weighted=float(constraint_weighted),
            saturation_penalty=float(saturation_penalty),
            **common,
        )


def make_cost_groupspec(param_name: str) -> GroupspecCost:
    """Factory: build a GroupspecCost for the given parameter name."""
    return GroupspecCost(param_name)


# ============================================================
#  Backward-compat aliases for analysis 07 (cx group-specific)
# ============================================================
_cx_cost = make_cost_groupspec("cx")

BOUNDS_GS = _cx_cost.BOUNDS_GS
NAMES_GS = _cx_cost.NAMES_GS
N_PARAMS_GS = _cx_cost.n_params
CX_G2_INDEX = _cx_cost.g2_index   # 26


def joint_cost_v13_gs(pv, g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2,
                      w_group=W_GROUP_DEFAULT):
    """Legacy alias: cx group-specific cost (analysis 07 API)."""
    return _cx_cost.cost(pv, g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2, w_group)


def joint_cost_v13_gs_decomposed(pv, g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2,
                                 w_group=W_GROUP_DEFAULT):
    """Legacy alias: cx group-specific decomposition (analysis 07 API).

    Returns dict with same keys as before, plus 'cx_g1' and 'cx_g2'
    convenience keys.
    """
    d = _cx_cost.cost_decomposed(pv, g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2, w_group)
    # legacy keys:
    d["cx_g1"] = d["cx_g1"]
    d["cx_g2"] = d["cx_g2"]
    return d
