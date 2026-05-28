# Analysis 31 — Busulfan intervention timing

## Question

If myelosan is administered post-injury (rather than pre-injury as in
the original G2 protocol), how does the timing affect DIC severity?
Is there a therapeutic window?

This addresses the central clinical question: at what point is myelosan
intervention too late to attenuate DIC progression?

## Method

Simulate G2 dynamics with myelosan kinetic effect (km, tm) applied
**starting** at t_intervention, with no kinetic effect before.

ODE simulation in two segments:
- Segment 1, [0, t_intervention]: kr_eff = kr, tp2_eff = tp2 (no myelosan)
- Segment 2, [t_intervention, 19]: kr_eff = kr × km, tp2_eff = tp2 × tm (with myelosan)

ODE state (D, AP, Hc, Hn, X) is continuous across t_intervention;
only rate constants change instantaneously.

### Timing scenarios

| t_intervention | scenario |
|---|---|
| 0 | baseline G2 (myelosan from start) |
| 1 | early intervention (before V(t) peak at τ_v=1.5) |
| 2 | intervention after V(t) peak |
| 4 | mid-DIC intervention |
| 6 | late intervention |
| ∞ | no intervention (reference: G1-like) |

Dose fixed at G2-observed (km=4.93, tm=0.43).

### Compute

6 scenarios × 100 bootstrap ensemble members = 600 simulations.
~3 minutes wall-clock.

## Severity metrics

Per trajectory:
- **max_gHn** — peak hyaline-degranulation accumulation
- **min_xiii** — XIII channel nadir
- **max_recalc** — peak hypocoagulation
- **auc_recalc** — overall coagulation disruption
- **t_peak** — time of maximum gHn (clinical: time of crisis)
- **t_recovery** — time when gHn falls to 10% of peak (clinical: end of acute phase)
- **acute_phase_duration** — Δt = t_recovery − t_peak

## Outputs

- `results/intervention_predictions_raw.pkl` — all per-member predictions
- `results/summary_by_timing.json` — ensemble percentiles per scenario
- `figures/fig1_severity_vs_timing.png` — severity metrics vs t_intervention
- `figures/fig2_temporal_vs_timing.png` — t_peak, t_recovery vs t_intervention
- `figures/fig3_trajectories.png` — example gHn trajectories per scenario
- `FINDINGS.md` — interpretation

## Run

```bash
python -m analyses.31_intervention_timing.run
```

## Caveats

1. **Myelosan modeled as instantaneous rate constant change.** In reality,
   myelosuppression develops over 5-7 days. The simulation represents
   idealized scenario of immediate pharmacological effect.

2. **Neutrophil profile extrapolation.** G2 n2 interpolator extrapolates
   flat after t=8 (held at 3.73). This is biologically reasonable
   (close to G2 baseline ~3.9) but is a modeling choice.
