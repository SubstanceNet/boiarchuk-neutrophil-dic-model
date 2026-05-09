"""
Fit-runner: thin wrapper around src.fit.run_fit for parametric studies.

Allows override of:
  - cfg.W_SPLIT (mechanism-split constraint weight)
  - cfg.NEUTRO_FRAC (target fractions)
  - bounds for individual parameters (e.g., expand cx)
  - fixed parameter values (replace optimisation with a constant)

Override mechanism: monkey-patch cfg attributes for the duration of one fit,
then restore. Thread-unsafe (do not call concurrently); fine for sequential
sweeps.

Cache: results are keyed by SHA256 of the canonicalised override dict +
the seed list. A previously-computed fit is loaded from disk, not recomputed.
Cache directory: analyses/<analysis_name>/results/_cache/
"""

from __future__ import annotations
import hashlib
import json
import pickle
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import numpy as np

from . import config as cfg
from .data import load_data
from .fit import run_fit, r_squared
from .model import solve_group, make_fine_grids
from .data import build_neutrophil_interpolators


# ============================================================
#  Override context manager
# ============================================================

@contextmanager
def patched_config(overrides: dict[str, Any]):
    """Temporarily replace attributes of src.config.

    Example:
        with patched_config({"W_SPLIT": 0.0}):
            run_fit(...)   # uses W_SPLIT = 0
        # cfg.W_SPLIT is restored here.
    """
    saved: dict[str, Any] = {}
    saved_bounds: dict[int, tuple] = {}
    try:
        for key, val in overrides.items():
            if key == "BOUNDS_OVERRIDE":
                # Special handling: val is dict {param_name: (lo, hi)}
                if not isinstance(val, dict):
                    raise TypeError("BOUNDS_OVERRIDE must be a dict {name: (lo, hi)}")
                for pname, new_bound in val.items():
                    if pname not in cfg.NAMES:
                        raise ValueError(f"Unknown parameter name: {pname!r}")
                    idx = cfg.NAMES.index(pname)
                    saved_bounds[idx] = cfg.BOUNDS[idx]
                    cfg.BOUNDS[idx] = tuple(new_bound)
                continue
            if not hasattr(cfg, key):
                raise AttributeError(f"src.config has no attribute {key!r}")
            saved[key] = getattr(cfg, key)
            setattr(cfg, key, val)
        yield
    finally:
        for key, val in saved.items():
            setattr(cfg, key, val)
        for idx, orig_bound in saved_bounds.items():
            cfg.BOUNDS[idx] = orig_bound


# ============================================================
#  Cache key
# ============================================================

def _canonical(obj: Any) -> Any:
    """Recursively convert obj to JSON-serialisable canonical form."""
    if isinstance(obj, dict):
        return {k: _canonical(obj[k]) for k in sorted(obj.keys())}
    if isinstance(obj, (list, tuple)):
        return [_canonical(x) for x in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    return obj


def cache_key(overrides: dict[str, Any], seeds: list[int], quick: bool) -> str:
    """SHA256 of canonical (overrides, seeds, quick) — first 16 hex chars."""
    payload = {
        "overrides": _canonical(overrides),
        "seeds": sorted(int(s) for s in seeds),
        "quick": bool(quick),
        "version": "1",
    }
    raw = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()[:16]


# ============================================================
#  Main runner
# ============================================================

def run_with_overrides(
    overrides: dict[str, Any],
    *,
    seeds: list[int] | None = None,
    quick: bool = True,
    workers: int = -1,
    cache_dir: Path | None = None,
    use_cache: bool = True,
    label: str | None = None,
    verbose: bool = True,
) -> dict:
    """Run a fit with cfg overrides, cached on disk.

    Returns a dict with:
      best_x, best_cost, params_dict, t_total, per_seed_costs (from run_fit)
      metrics_g1, metrics_g2  (per-observable R^2 + RMSE)
      overrides, seeds, quick, cache_key, cached (bool)
    """
    if seeds is None:
        seeds = [42] if quick else [42, 7, 123, 2024, 999]

    key = cache_key(overrides, seeds, quick)
    label_str = label or f"override={overrides}"

    if cache_dir is None:
        cache_dir = Path("analyses/_default_cache")
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"fit_{key}.pkl"

    if use_cache and cache_path.exists():
        with cache_path.open("rb") as f:
            result = pickle.load(f)
        result["cached"] = True
        if verbose:
            print(f"[{label_str}] CACHE HIT  ({key}, t={result['t_total']:.0f}s saved)")
        return result

    if verbose:
        print(f"[{label_str}] running fit (key={key}, quick={quick}, seeds={seeds})...")
    t0 = time.time()

    g1, g2 = load_data()
    n1_interp, n2_interp = build_neutrophil_interpolators(g1, g2)
    t_fine_g1, t_fine_g2 = make_fine_grids()

    with patched_config(overrides):
        fit_result = run_fit(
            g1, g2, quick=quick, seeds=seeds, workers=workers, verbose=False,
        )
        # While still inside the context, evaluate R^2 with the same overrides.
        best_x = fit_result["best_x"]
        kr_g1 = best_x[1]
        kr_g2 = best_x[1] * best_x[24]
        tp2_g1 = best_x[8]
        tp2_g2 = best_x[8] * best_x[25]
        o1 = solve_group(best_x, g1.T, n1_interp, t_fine_g1, kr_g1, tp2_g1)
        o2 = solve_group(best_x, g2.T, n2_interp, t_fine_g2, kr_g2, tp2_g2)

    metrics_g1 = {}
    for k, d in [("recalc", g1.recalc), ("thrombin", g1.thrombin),
                 ("fib", g1.fib), ("xiii", g1.xiii),
                 ("AP", g1.AP), ("D", g1.deg)]:
        m = o1[k]
        metrics_g1[k] = dict(R2=r_squared(m, d),
                             RMSE=float(np.sqrt(np.mean((m - d) ** 2))))

    metrics_g2 = {}
    for k, d in [("recalc", g2.recalc), ("thrombin", g2.thrombin),
                 ("fib", g2.fib), ("xiii", g2.xiii),
                 ("AP", g2.AP), ("D", g2.deg)]:
        m = o2[k][:len(d)]
        metrics_g2[k] = dict(R2=r_squared(m, d),
                             RMSE=float(np.sqrt(np.mean((m - d) ** 2))))

    result = dict(
        overrides=_canonical(overrides),
        seeds=list(seeds),
        quick=quick,
        cache_key=key,
        cached=False,
        wall_time=time.time() - t0,
        best_x=fit_result["best_x"].tolist(),
        best_cost=fit_result["best_cost"],
        params_dict=fit_result["params_dict"],
        t_total=fit_result["t_total"],
        per_seed_costs=fit_result["per_seed_costs"],
        metrics_g1=metrics_g1,
        metrics_g2=metrics_g2,
        avg_r2_g1=float(np.mean([v["R2"] for v in metrics_g1.values()])),
        avg_r2_g2=float(np.mean([v["R2"] for v in metrics_g2.values()])),
    )

    with cache_path.open("wb") as f:
        pickle.dump(result, f)
    if verbose:
        print(f"[{label_str}] DONE  ({result['t_total']:.0f}s, "
              f"cost={result['best_cost']:.4f}, "
              f"R2_G1={result['avg_r2_g1']:.3f}, R2_G2={result['avg_r2_g2']:.3f})")
    return result
    
# ============================================================
#  v13 group-specific fit pipeline (factory-based, generalised)
# ============================================================

def _run_fit_v13_gs_impl(
    g1, g2,
    *,
    groupspec_param: str = "cx",
    quick: bool = False,
    seeds: list[int] | None = None,
    workers: int = -1,
    w_group: tuple[float, float] | None = None,
    bounds_override: dict[str, tuple[float, float]] | None = None,
    verbose: bool = True,
) -> dict:
    """v13 group-specific fit pipeline. 27-param search space, with the
    parameter named `groupspec_param` duplicated as `<param>_g2` at index 26.

    Used internally by run_with_overrides_v13_gs.
    """
    import time
    from scipy.optimize import differential_evolution, minimize
    from .cost_v13_groupspec import make_cost_groupspec, W_GROUP_DEFAULT
    from .model import make_fine_grids
    from .data import build_neutrophil_interpolators

    if seeds is None:
        seeds = [42] if quick else [42, 7, 123, 2024, 999]
    if quick:
        de_pop, de_iter, nm_iter, pw_iter = 8, 120, 3000, 2000
    else:
        de_pop, de_iter, nm_iter, pw_iter = 12, 300, 10000, 8000

    if w_group is None:
        w_group = W_GROUP_DEFAULT

    gs = make_cost_groupspec(groupspec_param)
    bounds_local = list(gs.BOUNDS_GS)
    if bounds_override:
        for name, b in bounds_override.items():
            if name in gs.NAMES_GS:
                idx = gs.NAMES_GS.index(name)
                bounds_local[idx] = (float(b[0]), float(b[1]))
            else:
                raise KeyError(f"Unknown parameter for bounds_override: {name}")

    n1_interp, n2_interp = build_neutrophil_interpolators(g1, g2)
    t_fine_g1, t_fine_g2 = make_fine_grids()
    cost_args = (g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2, w_group)

    def _cost_bounded(pv):
        for i, (lo, hi) in enumerate(bounds_local):
            if pv[i] < lo or pv[i] > hi:
                penalty = 1.0 + max(lo - pv[i], pv[i] - hi, 0.0) / (hi - lo)
                return cfg.COST_PENALTY_NAN * penalty
        return gs.cost(pv, *cost_args)

    best_cost = cfg.COST_PENALTY_NAN
    best_x = None
    per_seed_costs: list[tuple[int, float]] = []
    t_start = time.time()

    for seed in seeds:
        if verbose:
            print(f"--- DE v13_gs[{groupspec_param}] seed={seed} ---", flush=True)
        ts = time.time()
        r = differential_evolution(
            gs.cost, bounds_local, args=cost_args,
            maxiter=de_iter, popsize=de_pop, seed=seed, tol=1e-7,
            workers=workers, mutation=(0.5, 1.5), recombination=0.85,
            disp=False, polish=False,
        )
        per_seed_costs.append((seed, float(r.fun)))
        if verbose:
            print(f"  cost={r.fun:.6f} ({time.time()-ts:.0f}s, {r.nfev} evals)", flush=True)
        if r.fun < best_cost:
            best_cost = float(r.fun)
            best_x = r.x.copy()
            if verbose:
                print("  -> best", flush=True)

    if best_x is None:
        raise RuntimeError(f"v13_gs[{groupspec_param}] DE failed for all seeds")

    if verbose:
        print(f"\nBest DE: {best_cost:.6f}", flush=True)

    for method, opts in [
        ("Nelder-Mead", {"maxiter": nm_iter, "xatol": 1e-9, "fatol": 1e-10}),
        ("Powell",      {"maxiter": pw_iter, "ftol": 1e-10}),
        ("Nelder-Mead", {"maxiter": nm_iter, "xatol": 1e-10, "fatol": 1e-11}),
    ]:
        try:
            r = minimize(_cost_bounded, best_x, method=method, options=opts)
            if np.isfinite(r.fun) and r.fun < best_cost:
                best_x = r.x.copy()
                best_cost = float(r.fun)
                if verbose:
                    print(f"  {method}: {r.fun:.6f} -> improved", flush=True)
            elif verbose:
                print(f"  {method}: {r.fun:.6f}", flush=True)
        except Exception as e:
            if verbose:
                print(f"  {method}: failed ({e})", flush=True)

    return dict(
        best_x=best_x,
        best_cost=best_cost,
        params_dict={n: float(best_x[i]) for i, n in enumerate(gs.NAMES_GS)},
        t_total=time.time() - t_start,
        per_seed_costs=per_seed_costs,
        bounds_used=bounds_local,
        groupspec_param=groupspec_param,
    )


def run_with_overrides_v13_gs(
    overrides: dict[str, Any] | None = None,
    *,
    groupspec_param: str = "cx",
    seeds: list[int] | None = None,
    quick: bool = True,
    workers: int = -1,
    w_group: tuple[float, float] | None = None,
    cache_dir: Path | None = None,
    use_cache: bool = True,
    label: str | None = None,
    verbose: bool = True,
) -> dict:
    """v13 group-specific cost runner with cache.

    Parameter `groupspec_param` selects which v13 parameter is duplicated
    into a G2-specific version. Default 'cx' for backward compatibility
    with analysis 07.

    The ONLY override currently honoured is BOUNDS_OVERRIDE — applied to
    bounds_local in _run_fit_v13_gs_impl. Other v12-style cfg attribute
    overrides are not used.

    Cache key includes 'v13_gs' marker AND groupspec_param to avoid
    collision across analyses.
    """
    from .cost_v13_groupspec import make_cost_groupspec, W_GROUP_DEFAULT
    from .model import solve_group, make_fine_grids
    from .data import build_neutrophil_interpolators

    if overrides is None:
        overrides = {}
    if seeds is None:
        seeds = [42] if quick else [42, 7, 123, 2024, 999]
    if w_group is None:
        w_group = W_GROUP_DEFAULT

    gs = make_cost_groupspec(groupspec_param)
    bounds_override = overrides.get("BOUNDS_OVERRIDE")

    payload = {
        "overrides": _canonical(overrides),
        "seeds": sorted(int(s) for s in seeds),
        "quick": bool(quick),
        "cost_version": "v13_gs",
        "groupspec_param": groupspec_param,
        "w_group": list(w_group),
        "version": "1",
    }
    raw = json.dumps(payload, sort_keys=True).encode()
    key = hashlib.sha256(raw).hexdigest()[:16]
    label_str = label or f"v13_gs[{groupspec_param}]/override={overrides}"

    if cache_dir is None:
        cache_dir = Path(f"analyses/_default_cache_v13_gs_{groupspec_param}")
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"fit_v13_gs_{groupspec_param}_{key}.pkl"

    if use_cache and cache_path.exists():
        with cache_path.open("rb") as f:
            result = pickle.load(f)
        result["cached"] = True
        if verbose:
            print(f"[{label_str}] CACHE HIT  ({key}, t={result['t_total']:.0f}s saved)")
        return result

    if verbose:
        print(f"[{label_str}] running v13_gs fit (key={key}, "
              f"quick={quick}, seeds={seeds}, w_group={w_group}, "
              f"groupspec_param={groupspec_param})...")
    t0 = time.time()

    g1, g2 = load_data()
    n1_interp, n2_interp = build_neutrophil_interpolators(g1, g2)
    t_fine_g1, t_fine_g2 = make_fine_grids()

    fit_result = _run_fit_v13_gs_impl(
        g1, g2,
        groupspec_param=groupspec_param,
        quick=quick, seeds=seeds, workers=workers,
        w_group=w_group, bounds_override=bounds_override, verbose=False,
    )
    best_x = fit_result["best_x"]

    pv_g1, pv_g2 = gs.split_params(best_x)
    kr_g1 = pv_g1[1]
    kr_g2 = pv_g2[1] * pv_g2[24]
    tp2_g1 = pv_g1[8]
    tp2_g2 = pv_g2[8] * pv_g2[25]
    o1 = solve_group(pv_g1, g1.T, n1_interp, t_fine_g1, kr_g1, tp2_g1)
    o2 = solve_group(pv_g2, g2.T, n2_interp, t_fine_g2, kr_g2, tp2_g2)

    decomp = gs.cost_decomposed(
        best_x, g1, g2, n1_interp, n2_interp, t_fine_g1, t_fine_g2,
        w_group=w_group,
    )

    metrics_g1 = {}
    for k, d in [("recalc", g1.recalc), ("thrombin", g1.thrombin),
                 ("fib", g1.fib), ("xiii", g1.xiii),
                 ("AP", g1.AP), ("D", g1.deg)]:
        m = o1[k]
        metrics_g1[k] = dict(R2=r_squared(m, d),
                             RMSE=float(np.sqrt(np.mean((m - d) ** 2))))

    metrics_g2 = {}
    for k, d in [("recalc", g2.recalc), ("thrombin", g2.thrombin),
                 ("fib", g2.fib), ("xiii", g2.xiii),
                 ("AP", g2.AP), ("D", g2.deg)]:
        m = o2[k][:len(d)]
        metrics_g2[k] = dict(R2=r_squared(m, d),
                             RMSE=float(np.sqrt(np.mean((m - d) ** 2))))

    g1_val = float(best_x[gs.idx])
    g2_val = float(best_x[gs.g2_index])
    ratio = float(g2_val / g1_val) if g1_val != 0 else float("nan")

    result = dict(
        cost_version="v13_gs",
        groupspec_param=groupspec_param,
        w_group=list(w_group),
        overrides=_canonical(overrides),
        seeds=list(seeds),
        quick=quick,
        cache_key=key,
        cached=False,
        wall_time=time.time() - t0,
        best_x=fit_result["best_x"].tolist(),
        best_cost=fit_result["best_cost"],
        params_dict=fit_result["params_dict"],
        t_total=fit_result["t_total"],
        per_seed_costs=fit_result["per_seed_costs"],
        # Legacy keys for backward compatibility (cx case)
        cx_g1=float(best_x[21]),
        cx_g2=float(best_x[gs.g2_index]) if groupspec_param == "cx" else None,
        cx_ratio=ratio if groupspec_param == "cx" else None,
        # Generic group-specific values
        g1_value=g1_val,
        g2_value=g2_val,
        ratio=ratio,
        decomposition={k: v for k, v in decomp.items() if k != "w_group"},
        metrics_g1=metrics_g1,
        metrics_g2=metrics_g2,
        avg_r2_g1=float(np.mean([v["R2"] for v in metrics_g1.values()])),
        avg_r2_g2=float(np.mean([v["R2"] for v in metrics_g2.values()])),
    )

    with cache_path.open("wb") as f:
        pickle.dump(result, f)
    if verbose:
        print(f"[{label_str}] DONE  ({result['t_total']:.0f}s, "
              f"cost={result['best_cost']:.4f}, "
              f"R2_G1={result['avg_r2_g1']:.3f}, R2_G2={result['avg_r2_g2']:.3f}, "
              f"{groupspec_param}_g1={g1_val:.1f}, {groupspec_param}_g2={g2_val:.1f}, "
              f"ratio={ratio:.3f})")
    return result
    
