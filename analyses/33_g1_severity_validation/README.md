# Analysis 33 — G1 hypocoagulation severity validation

## Question

Does the joint v13 model reproduce the hypocoagulation severity observed in
Group I, and does the G1-vs-G2 contrast match the observed mortality pattern
(30% G1 on days 10-12 vs 0% G2)?

This replaces the defunct `liver_collapse` metric (analysis 30) as the basis
for mortality validation. That metric (Hn/Hm > 0.99) is unusable: Hn sits at
~1% of carrying capacity Hm in the realistic parameter range, so the
threshold is structurally unreachable, and a code bug (`o["Hm"]` absent →
`None`) kept it always False regardless. Mortality is instead validated
through hypocoagulation severity (max_recalc, min_fib, min_xiii), which the
model computes correctly and which is what was clinically observed (animals
die at the hypocoagulation peak).

## Method

Each of the 100 bootstrap ensemble members (analysis 22) run as:
- **pure G1**: G1 neutrophil profile (n1), no myelosan (kr=pv[1], tp2=pv[8]),
  G1 grids (t_eval 0-19 d, fine 0-20 d).
- **G2 baseline** (contrast): n2, myelosan km/tm as fitted.

Note: the joint v13 architecture had never been run as pure G1 — analysis 30
always retained the G2 neutrophil profile, so its "km=1" cell is NOT G1.

## Validation targets (Olena, dissertation / methodology paper)

| channel | observed G1 |
|---------|-------------|
| recalc peak | +206.7 s at day 11 |
| fibrinogen nadir | ~ -52.6 mg% (day 12) |
| factor XIII nadir | -76.7 % (day 11) |
| mortality | 30% (12/40), days 10-12 |
| G2 | hypocoagulation does not develop; 0% mortality |

## Run

```bash
python -m analyses.33_g1_severity_validation.run
```

~1 min (200 ODE solves). Outputs `results/g1_severity.json`.

## Key result

Model G1 vs observed: timing exact (day 11), xiii within 1%, fib within 11%,
recalc underestimated 29% (channel-localized in br·gHn, not systemic).
G1/G2 separation 22× — reproduces the group contrast underlying the
observed mortality difference.
