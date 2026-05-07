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
