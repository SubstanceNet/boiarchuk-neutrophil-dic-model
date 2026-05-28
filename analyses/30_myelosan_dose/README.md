# Analysis 30 — Busulfan dose-response

## Question

How does the severity of DIC depend on the strength of neutrophil
suppression by busulfan? What dose-response surface in (km, tm)
parameter space defines the transition from full DIC progression to
DIC prevention?

This is the core biological prediction of the model: a phase diagram
quantifying the relationship between busulfan effect strength and
clinical outcome.

## Method

Two-parameter sweep over (km, tm) space:
- km ∈ log-spaced grid [1.0, 10.0], 15 values
- tm ∈ log-spaced grid [0.2, 1.0], 15 values
- Total: 15×15 = 225 grid cells

For each grid cell × each of 100 bootstrap ensemble members
(analysis 22 ensemble):
- Use ensemble member's baseline parameters.
- Override km, tm for G2 simulation: kr_g2 = kr × km, tp2_g2 = tp2 × tm.
- Solve G2 ODE system on full timeline (0-19 days).
- Compute severity metrics.

Total simulations: 225 × 100 = 22,500. Each ~0.3s → ~2 hours wall-clock
(can be parallelised via joblib).

## Severity metrics

Per-trajectory metrics:
- **max gHn** — peak effective coagulation load (neutrophil-derived)
- **min XIII** — XIII channel nadir (lowest fXIII delta)
- **max recalc** — peak hypocoagulation (largest positive recalcification time delta)
- **AUC recalc** — overall coagulation disruption (integrated |Δrecalc|)
- **time to peak gHn** — temporal indicator of DIC trajectory speed

(Mortality is validated separately in analysis 33; an earlier liver_collapse
proxy was removed as invalid — the Hn/Hm threshold was unreachable by
construction.)

## Reference points on phase diagrams

- **(km=1.0, tm=1.0)**: no busulfan effect → expected G1-like outcome.
  Internal validation: severity here should match G1 observed severity.
- **(km=4.93, tm=0.43)**: G2 baseline (observed experimental dose).
- **(km, tm) other**: hypothetical doses (lower or higher than observed).

## Outputs

- `results/phase_diagram_<metric>.json` — per-cell ensemble percentiles
  for each severity metric
- `results/ensemble_predictions_raw.pkl` — raw per-member predictions
  (for downstream conditional filtering in analysis 32)
- `results/sanity_check_km1.json` — validation that km=1 reproduces G1 severity
- `figures/phase_diagram_<metric>.png` — phase diagram plots (full + good-basin overlay)
- `FINDINGS.md` — interpretation

## Run

```bash
python -m analyses.30_myelosan_dose.run
```

Wall-clock: ~2 hours.
