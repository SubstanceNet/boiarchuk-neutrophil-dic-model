"""
Profile likelihood for v13 baseline parameters.

Workflow per parameter θ_i:
  1. Construct grid of values around the baseline best-fit value.
  2. For each grid point, fix θ_i and minimise cost over the remaining
     25 parameters using Nelder-Mead in a 25-dim space.
  3. Build profile cost C(θ_i) = min_{θ_{-i}} cost(θ_i, θ_{-i}).
  4. Identify 95% confidence interval where C(θ_i) - C_min < 1.92
     (chi-squared 1 d.o.f., alpha=0.05).
  5. Classify identifiability: well / weak / sloppy / unidentifiable.

Single-start: starting point for each grid minimisation is the baseline
best_x with θ_i overridden. No multi-start.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import minimize

from . import config as cfg
from .cost_v13 import joint_cost_v13


# Relative cost thresholds (calibrated for RMSE-style cost, not log-likelihood).
# 5% above baseline cost = boundary of 95% CI region.
# 2% above baseline = noise floor for "flat" classification.
CI_REL_THRESHOLD_95 = 0.05   # 5% relative cost increase
FLAT_REL_THRESHOLD = 0.02    # 2% relative variation = treated as flat


def _build_grid(
    baseline: float, lo: float, hi: float,
    n_points: int, span_factor: float, log_grid: bool,
) -> tuple[np.ndarray, dict]:
    """Construct grid of n_points around baseline within (lo, hi).

    Returns (grid, info_dict). info_dict contains:
      requested_lo, requested_hi: grid endpoints before clipping
      clipped_lo, clipped_hi: bool, whether grid was clipped at bound
      n_unique_values: int, number of distinct values after clipping
        (small means grid extensively saturates a bound)
    """
    if log_grid:
        if baseline <= 0:
            raise ValueError(f"log_grid requires baseline > 0, got {baseline}")
        log_b = np.log(baseline)
        # span_factor is in log_e units: span_factor=0.5 means ±0.5 in log,
        # i.e., factor of e^0.5 ≈ 1.65 (±65%) in linear space.
        delta = float(span_factor)
        grid_log = np.linspace(log_b - delta, log_b + delta, n_points)
        grid_raw = np.exp(grid_log)
    else:
        delta = abs(baseline) * span_factor
        if delta == 0:
            delta = span_factor
        grid_raw = np.linspace(baseline - delta, baseline + delta, n_points)

    requested_lo = float(grid_raw.min())
    requested_hi = float(grid_raw.max())
    clipped_lo = requested_lo < lo
    clipped_hi = requested_hi > hi

    grid = np.clip(grid_raw, lo, hi)
    n_unique = len(np.unique(np.round(grid, decimals=8)))

    info = dict(
        requested_lo=requested_lo,
        requested_hi=requested_hi,
        clipped_lo=clipped_lo,
        clipped_hi=clipped_hi,
        n_unique_values=n_unique,
    )
    return grid, info


def profile_param(
    param_name: str,
    best_x: np.ndarray,
    *,
    g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2,
    n_points: int = 11,
    span_factor: float = 0.5,
    log_grid: bool = True,
    w_group: tuple[float, float] = (1.0, 1.0),
    optimizer_options: dict | None = None,
    verbose: bool = False,
) -> dict:
    """Profile likelihood for one parameter.

    Returns:
      param_name, param_idx, baseline_value, baseline_cost,
      grid, profile_costs, profile_best_xs (26-dim each),
      ci_95: (lower, upper) or None,
      classification: well_identified | weakly_identified | sloppy | unidentifiable.
    """
    if param_name not in cfg.NAMES:
        raise ValueError(f"Unknown parameter {param_name!r}")
    idx = cfg.NAMES.index(param_name)
    lo, hi = cfg.BOUNDS[idx]

    baseline_x = np.asarray(best_x, dtype=float).copy()
    baseline_value = float(baseline_x[idx])
    baseline_cost = float(joint_cost_v13(
        baseline_x, g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2, w_group
    ))

    grid, grid_info = _build_grid(baseline_value, lo, hi, n_points, span_factor, log_grid)
    if verbose and (grid_info["clipped_lo"] or grid_info["clipped_hi"]):
        print(f"  WARNING: grid clipped at bound. requested=({grid_info['requested_lo']:.4g}, "
              f"{grid_info['requested_hi']:.4g}), bounds=({lo}, {hi}), "
              f"unique values: {grid_info['n_unique_values']}/{n_points}", flush=True)
    if optimizer_options is None:
        optimizer_options = dict(maxiter=2000, xatol=1e-7, fatol=1e-9)

    other_idxs = [j for j in range(len(cfg.NAMES)) if j != idx]
    other_bounds = [cfg.BOUNDS[j] for j in other_idxs]
    other_x0 = baseline_x[other_idxs].copy()

    def make_full_x(theta_other: np.ndarray, theta_fixed: float) -> np.ndarray:
        x = baseline_x.copy()
        x[other_idxs] = theta_other
        x[idx] = theta_fixed
        return x

    def cost_25dim(theta_other: np.ndarray, theta_fixed: float) -> float:
        # Soft penalty for bound violation in the 25-dim subspace
        for k, (b_lo, b_hi) in enumerate(other_bounds):
            v = theta_other[k]
            if v < b_lo or v > b_hi:
                excess = max(b_lo - v, v - b_hi, 0.0) / (b_hi - b_lo)
                return cfg.COST_PENALTY_NAN * (1.0 + excess)
        full_x = make_full_x(theta_other, theta_fixed)
        return joint_cost_v13(full_x, g1, g2, n1_interp, n2_interp,
                              t_fine_g1, t_fine_g2, w_group)

    profile_costs = np.full(n_points, np.nan)
    profile_best_xs = np.full((n_points, len(cfg.NAMES)), np.nan)

    for k, theta_fixed in enumerate(grid):
        x0 = other_x0.copy()
        try:
            r = minimize(
                cost_25dim, x0, args=(theta_fixed,),
                method="Nelder-Mead", options=optimizer_options,
            )
            profile_costs[k] = float(r.fun)
            profile_best_xs[k] = make_full_x(r.x, theta_fixed)
        except Exception as e:
            if verbose:
                print(f"  [{param_name} grid {k}] failed: {e}", flush=True)

        if verbose:
            print(f"  [{param_name} grid {k+1}/{n_points}] "
                  f"theta={theta_fixed:.4g}, cost={profile_costs[k]:.4f}",
                  flush=True)

    # Compute confidence interval and classification using RELATIVE cost.
    finite_mask = np.isfinite(profile_costs)
    if finite_mask.sum() < 3:
        ci_95 = None
        classification = "insufficient_data"
        cost_depth_abs = None
        cost_depth_rel = None
        ci_width_relative = None
        boundary_minimum = None
    else:
        finite_costs = profile_costs[finite_mask]
        finite_grid = grid[finite_mask]
        min_cost = float(np.min(finite_costs))
        max_cost = float(np.max(finite_costs))
        cost_depth_abs = float(max_cost - min_cost)
        cost_depth_rel = cost_depth_abs / min_cost if min_cost > 0 else None

        # CI threshold: cost may rise by up to CI_REL_THRESHOLD_95 (5%)
        # relative to the minimum cost within this profile.
        threshold = min_cost * (1.0 + CI_REL_THRESHOLD_95)
        in_ci = finite_mask & (profile_costs <= threshold)

        if in_ci.sum() == 0:
            ci_95 = None
            ci_width_relative = None
        else:
            ci_lo = float(grid[in_ci].min())
            ci_hi = float(grid[in_ci].max())
            ci_95 = (ci_lo, ci_hi)
            grid_span = float(grid[-1] - grid[0])
            ci_width_relative = (ci_hi - ci_lo) / grid_span if grid_span > 0 else None

        # Boundary minimum check (min at edge of grid)
        min_idx = int(np.argmin(finite_costs))
        boundary_minimum = (min_idx == 0 or min_idx == len(finite_costs) - 1)

        # Classification logic — relative thresholds
        if cost_depth_rel is not None and cost_depth_rel < FLAT_REL_THRESHOLD:
            # Profile is essentially flat across the explored range
            if grid_info["clipped_lo"] or grid_info["clipped_hi"]:
                classification = "grid_truncated_inconclusive"
            else:
                classification = "flat_profile_check_grid_or_unidentifiable"
        elif boundary_minimum:
            classification = "boundary_minimum_grid_too_narrow"
        elif ci_width_relative is None:
            classification = "unknown"
        elif ci_width_relative < 0.3:
            classification = "well_identified"
        elif ci_width_relative < 0.7:
            classification = "moderately_identified"
        else:
            classification = "weakly_identified"

        # Tag if grid was clipped (regardless of other classification)
        if grid_info["clipped_lo"] or grid_info["clipped_hi"]:
            classification = classification + "_grid_truncated"
            
    return dict(
        param_name=param_name,
        param_idx=idx,
        baseline_value=baseline_value,
        baseline_cost=baseline_cost,
        bounds=cfg.BOUNDS[idx],
        grid=grid.tolist(),
        profile_costs=profile_costs.tolist(),
        profile_best_xs=profile_best_xs.tolist(),
        ci_95=ci_95,
        classification=classification,
        n_points=n_points,
        span_factor=span_factor,
        log_grid=log_grid,
        cost_depth_abs=cost_depth_abs,
        cost_depth_rel=cost_depth_rel,
        ci_width_relative=ci_width_relative,
        boundary_minimum=boundary_minimum,
        grid_info=grid_info,
    )
