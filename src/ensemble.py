"""
Shared loader for the analysis-22 bootstrap ensemble.

Downstream virtual experiments (analyses 30/31/32/33) need, per member:
  - best_x        : (26,) parameter vector
  - g2_xiii       : (9,)  Group II XIII prediction (for good-basin masking)

This module reads a consolidated, version-control-tracked artifact
(results/ensemble_members.json) when present, and falls back to the raw
per-iteration cache (results/_cache/iter_*.pkl) otherwise. The consolidated
artifact lets a fresh clone reproduce the Phase-4.5 experiments without
re-running the expensive bootstrap (analysis 22).
"""
from __future__ import annotations

import json
import pickle
from pathlib import Path

import numpy as np

_PRED_DIR = Path("analyses/22_predictive_check/results")
_CONSOLIDATED = _PRED_DIR / "ensemble_members.json"
_CACHE_DIR = _PRED_DIR / "_cache"


def load_ensemble(include_failed: bool = False) -> list[dict]:
    """Return ensemble members as a list of dicts.

    Each dict has keys: best_x (np.ndarray, shape (26,)),
    g2_xiii (np.ndarray, shape (9,)), failed (bool).

    Prefers the consolidated JSON artifact; falls back to the _cache pkls.
    """
    if _CONSOLIDATED.exists():
        members = _load_consolidated()
    elif _CACHE_DIR.exists():
        members = _load_cache()
    else:
        raise FileNotFoundError(
            f"No ensemble source found: neither {_CONSOLIDATED} nor "
            f"{_CACHE_DIR} exists. Run analysis 22 (python -m "
            f"analyses.22_predictive_check.run) then its aggregate step."
        )
    if not include_failed:
        members = [m for m in members if not m["failed"]]
    return members


def _load_consolidated() -> list[dict]:
    raw = json.loads(_CONSOLIDATED.read_text())
    out = []
    for rec in raw["members"]:
        out.append(dict(
            best_x=np.array(rec["best_x"], dtype=float),
            g2_xiii=np.array(rec["g2_xiii"], dtype=float),
            failed=bool(rec.get("failed", False)),
        ))
    return out


def _load_cache() -> list[dict]:
    out = []
    for p in sorted(_CACHE_DIR.glob("iter_*.pkl")):
        with p.open("rb") as f:
            rec = pickle.load(f)
        out.append(dict(
            best_x=np.array(rec["best_x"], dtype=float),
            g2_xiii=np.array(rec["g2_predictions"]["xiii"], dtype=float),
            failed=bool(rec.get("failed", False)),
        ))
    return out


def good_basin_mask(members: list[dict], g2_xiii_ref: np.ndarray,
                    threshold: float = 0.3) -> np.ndarray:
    """Boolean mask: member's Group II XIII R^2 >= threshold (good basin)."""
    ref = np.asarray(g2_xiii_ref, dtype=float)
    ss_tot = np.sum((ref - ref.mean()) ** 2)
    mask = []
    for m in members:
        pred = m["g2_xiii"]
        ss_res = np.sum((pred - ref) ** 2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        mask.append(r2 >= threshold)
    return np.array(mask)
