"""
Data loading and neutrophil-count interpolation.

CSV files in data/csv/ are the authoritative source of experimental values.
Provenance is documented in data/csv/PROVENANCE.md.

Load functions return numpy arrays in the column order expected by fit.py;
that order matches the original v12 script (RECALC, THROMB, FIB, XIII, AP, DEG, N).
"""

from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
import numpy as np
from scipy.interpolate import interp1d

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "csv"


@dataclass(frozen=True)
class GroupData:
    """Container for one experimental group's data.

    All hemostatic and neutrophil-activity arrays are DELTAS from baseline.
    `neutrophils` is ABSOLUTE (10^9/L). `T` is observation times in days.
    Arrays are aligned by index: `recalc[i]` is observed at `T[i]`.
    """

    name: str
    T: np.ndarray
    recalc: np.ndarray
    thrombin: np.ndarray
    fib: np.ndarray
    xiii: np.ndarray
    AP: np.ndarray
    deg: np.ndarray
    neutrophils: np.ndarray

    @property
    def n_timepoints(self) -> int:
        return len(self.T)

    @property
    def n_observables(self) -> int:
        return 6  # recalc, thrombin, fib, xiii, AP, deg

    @property
    def n_datapoints(self) -> int:
        return self.n_timepoints * self.n_observables


def _load_csv(path: Path) -> dict[str, np.ndarray]:
    """Load CSV with `#` comment lines, return dict of column -> ndarray."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    with path.open() as f:
        lines = [ln for ln in f if not ln.lstrip().startswith("#") and ln.strip()]
    header = lines[0].strip().split(",")
    rows = [ln.strip().split(",") for ln in lines[1:]]
    arr = np.asarray(rows, dtype=float)
    return {name: arr[:, i] for i, name in enumerate(header)}


def load_group(name: str, csv_path: Path | None = None) -> GroupData:
    """Load one group's data from CSV.

    Parameters
    ----------
    name : "G1" or "G2"
    csv_path : explicit override (default: data/csv/group1.csv or group2.csv)
    """
    if name not in ("G1", "G2"):
        raise ValueError(f"name must be 'G1' or 'G2', got {name!r}")
    if csv_path is None:
        fname = "group1.csv" if name == "G1" else "group2.csv"
        csv_path = DATA_DIR / fname
    cols = _load_csv(csv_path)
    return GroupData(
        name=name,
        T=cols["time_d"],
        recalc=cols["recalc_delta_s"],
        thrombin=cols["thrombin_delta_s"],
        fib=cols["fib_delta_mg_dl"],
        xiii=cols["fxiii_delta_pct"],
        AP=cols["acid_phosphatase_delta_BO"],
        deg=cols["degranulation_delta_pct"],
        neutrophils=cols["neutrophils_10_9_per_L"],
    )


def load_data() -> tuple[GroupData, GroupData]:
    """Load both groups. Returns (G1, G2)."""
    return load_group("G1"), load_group("G2")


def build_neutrophil_interpolators(
    g1: GroupData, g2: GroupData
) -> tuple[interp1d, interp1d]:
    """Return (N1_interp, N2_interp): callables giving N(t) in 10^9/L.

    Linear interpolation between observed points; constant extrapolation
    (clamps to first / last observation) outside the observed range.

    These are passed into the ODE rhs to drive group-specific dynamics
    via the time-varying neutrophil count.
    """
    n1 = interp1d(
        g1.T, g1.neutrophils,
        kind="linear", bounds_error=False,
        fill_value=(float(g1.neutrophils[0]), float(g1.neutrophils[-1])),
    )
    n2 = interp1d(
        g2.T, g2.neutrophils,
        kind="linear", bounds_error=False,
        fill_value=(float(g2.neutrophils[0]), float(g2.neutrophils[-1])),
    )
    return n1, n2
