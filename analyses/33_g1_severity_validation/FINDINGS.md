# Analysis 33 — G1 hypocoagulation severity validation

**Status:** closed. Pure-G1 run of the joint v13 model through the 100-member
bootstrap ensemble, validated against Olena's observed G1 severity and the
observed mortality pattern. Replaces the defunct `liver_collapse` metric.

## Why this analysis exists

The mortality validation originally rested on `liver_collapse` (Hn/Hm > 0.99)
in analysis 30, reported as 0/22,500. That result is **invalid** for two
independent reasons, both verified directly:

1. **Code bug.** `compute_severity` reads `o["Hm"]`, but `solve_group` does
   not place `"Hm"` in its output dict. So `Hm = None`, the collapse branch
   `if Hm is not None` never executes, and `liver_collapse` is `False`
   unconditionally for all 22,500 simulations — independent of neutrophils,
   dose, or dynamics.

2. **Conceptually empty even if fixed.** With Hm taken correctly from pv[7],
   Hn reaches only ~1.15% of Hm (max Hn 10.5 vs Hm 908 for a representative
   member). The 0.99 threshold is structurally unreachable in the realistic
   parameter range. The 0.999·Hm integration clip never activates because Hn
   lives two orders of magnitude below Hm. "Liver collapse as Hn saturation"
   cannot detect anything and is not a usable mortality proxy.

The original "0/22,500" is therefore **0 by construction**, not a biological
finding. It is removed (analysis 30 cleanup). Mortality is re-validated here
through hypocoagulation severity — what was clinically observed (animals die
at the hypocoagulation peak, days 10-12) and what the model computes
correctly.

## Method

Each of 100 bootstrap ensemble members run as:
- **pure G1**: G1 neutrophil profile, no myelosan (kr=pv[1], tp2=pv[8]),
  G1 grids (eval 0-19 d, fine 0-20 d).
- **G2 baseline** (contrast): n2 profile, fitted km/tm.

The joint v13 architecture had never previously been run as pure G1 (analysis
30 retained the G2 neutrophil profile throughout; its "km=1" cell is not G1).

## Results: G1 vs G2 severity

| metric | G1 median [CI95] | G2 baseline median [CI95] |
|--------|------------------|---------------------------|
| max_recalc (s) | 147.1 [122.1, 175.5] | 6.6 [3.0, 11.5] |
| min_fib (mg%) | -58.3 [-69.1, -46.4] | -1.4 [-8.1, 0.0] |
| min_xiii (%) | -77.1 [-94.4, -61.4] | -13.8 [-19.7, -7.3] |
| max_gHn | 19.7 [13.2, 55.8] | 3.7 [2.3, 9.6] |
| t_max_recalc (d) | 11.0 [10.0, 11.0] | 5.0 [5.0, 6.0] |

**G1/G2 separation (max_recalc): 22.2x.** The model cleanly reproduces
that G1 enters severe hypocoagulation while G2 does not — the contrast
underlying the observed 30% (G1) vs 0% (G2) mortality difference.

## Validation: model G1 vs observed G1 (Olena)

| channel | model median | observed | ratio | agreement |
|---------|--------------|----------|-------|-----------|
| recalc peak (s) | 147.1 | 206.7 | 0.71 | within 29% |
| fib nadir (mg%) | -58.3 | -52.6 | 1.11 | within 11% |
| xiii nadir (%) | -77.1 | -76.7 | 1.01 | within 1% |
| peak timing (d) | 11 | 11 | 1.00 | exact |

## Differential diagnosis — underestimate is channel-localized

The peak-timing match is exact (day 11), and two of three severity channels
agree closely with observation:
- **factor XIII nadir**: model -77.1% vs observed -76.7% — within 1%.
- **fibrinogen nadir**: model -58.3 vs observed -52.6 mg% — within 11%.
- **recalcification peak**: model 147 vs observed 206.7 s —
  underestimated by ~29% (ratio 0.71).

The underestimate is **localized to the recalcification channel** (the
br·gHn term), not systemic: the two other severity channels and the peak
timing are reproduced within 1-11%. This is consistent with the joint-fit
architecture penalty quantified in analysis 03 (~22 pp of G2 R2 traded for
G1 compatibility), and is reported as a known model limitation rather than
addressed by further fitting (which would risk the rest of the joint fit on
the manuscript's critical path).

## Conclusion — mortality validation (qualitative, honest)

The model reproduces the **timing** (day 11) and **group separation** (22x)
of the hypocoagulation peak, consistent with observed G1 mortality
(days 10-12) versus its absence in G2. Two of three severity channels match
observation within 11%; the recalcification amplitude is underestimated ~30%
(channel-localized). This is a qualitative external validation of the
mortality pattern through hypocoagulation severity — NOT a quantitative
mortality model and NOT the defunct liver-collapse threshold.

## Run inventory

- `results/g1_severity.json` — full G1/G2 severity percentiles + validation
- `run.py` — reproducible analysis
- `README.md` — context and targets
