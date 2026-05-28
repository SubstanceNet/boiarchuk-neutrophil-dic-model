# Data Provenance

This document maps every numerical value in `group1.csv` and `group2.csv` to its primary source. It is the single source of truth for "where did this number come from".

## Experimental design (both groups)

| Item | Value | Source |
|------|-------|--------|
| Animal model | Mature rabbits, 2.5–3.0 kg, both sexes | Boyarchuk diss. (1998), Methods |
| DIC inducer | "Efa-2" (ethylphenacin, first-generation 1,3-indandione vitamin-K-antagonist rodenticide bait), 8330 mg/kg ready bait, p.o., fasting | Boyarchuk diss. (1998), Methods; inducer identity confirmed by O.B. |
| Group I size | n = 40 (12 deaths, 30%, on days 10–12) | Boyarchuk commentary (mortality 30% — not in 2008 paper which states 27%) |
| Group II size | n = 40 (effectively 0% mortality) | Boyarchuk commentary |
| G2 busulfan protocol | 10 mg/day × 5–7 days + 4 mg/day × 8 days, p.o. | Boyarchuk commentary; **not published in any journal article** |
| Target G2 baseline | ~40–50% reduction in peripheral neutrophils | Boyarchuk commentary |

## Variable definitions and conventions

All hemostasis and neutrophil-activity values in CSV are **deltas from each animal's own pre-experiment baseline (t=0)**. This is the convention of the original tables — paired-difference design (метод прямих різниць за Монцевичюте-Ерінгене, 1964).

| CSV column | Original variable | Unit | Type | Method |
|------------|-------------------|------|------|--------|
| `recalc_delta_s` | Δ time of plasma recalcification | seconds | Δ | Standard recalcification test |
| `thrombin_delta_s` | Δ thrombin time | seconds | Δ | Standard thrombin time |
| `fib_delta_mg_dl` | Δ fibrinogen concentration | mg% (= mg/dL) | Δ | Standard fibrinogen assay |
| `fxiii_delta_pct` | Δ Factor XIII activity | % of baseline | Δ | Standard XIII activity |
| `acid_phosphatase_delta_BO` | Δ neutrophil acid phosphatase | Bodansky units | Δ | Bodansky method |
| `degranulation_delta_pct` | Δ % neutrophils with <10 granules | % | Δ | Pigarevsky 1975/1978; May-Grünwald stain; ×15 ocular, ×90 objective |
| `neutrophils_10_9_per_L` | Absolute neutrophil count | 10⁹/L | absolute | Standard differential WBC |

## Source-table mapping

Each row of each CSV is reconstructed from these dissertation tables (Boyarchuk O. D., 1998):

- Table 4.9 — recalcification, thrombin, fibrinogen, F.XIII (group I, 16 timepoints)
- Table 5.1 — neutrophil counts (groups I & II)
- Table 5.2 — degranulation (lysosomal formula, % distribution by granule content)
- Table 5.3 — absolute lysosomal-formula counts (×10⁹/L per category)
- Table 5.5 — bone marrow granulocytopoiesis (group I, group II) — **partially published**
- Table 5.7 — acid phosphatase activity (groups I & II, dynamics)
- Table 5.9 — recalcification, thrombin, fibrinogen, F.XIII (group II, 9 timepoints)

## Publication status of these data

Per the analytical summary (Boyarchuk 1998–2023 retrospective), the publication coverage of these primary data is approximately:

| Variable / Group | Published in journal | First publication |
|------------------|----------------------|-------------------|
| Hemostasis G1 (16 pts)                   | Partial (peak values, not full dynamics) | 2013 (Вісник ЛНУ) |
| Acid phosphatase G1 (16 pts)             | Yes, full dynamics | 2013 (Вісник ЛНУ) |
| Lysosomal formula G1 (% and absolute)    | Partial (% only, partial timepoints) | 2000 (Фізіол. журн.); 2012 (Вісник ЛНУ) |
| Neutrophil count G1 (absolute)           | Partial | 2000; 2008; 2012 |
| Hemostasis G2 (9 pts)                    | Aggregated by stage only | 2008 (Наук. вісник МДУ) |
| Acid phosphatase G2 (9 pts)              | Aggregated by stage only | 2008 |
| Lysosomal formula G2                     | Aggregated by stage only | 2008 |
| Neutrophil count G2 (absolute)           | **Not published** | — |
| Bone marrow granulocytopoiesis G2        | **Not published** | — |
| Mortality figures (30% / ~0%)            | Partially (27% in 2000) | 2000 |
| Busulfan protocol details                | **Not published** | — |

This means a substantial portion of `group2.csv` and the "M" pre-treatment state are reconstructed from the dissertation directly, not from any peer-reviewed article. Any publication using this dataset must:

1. cite the dissertation as primary source (Boyarchuk O. D., 1998);
2. include the data files (or equivalent supplementary tables) so reviewers can audit numbers;
3. acknowledge that the busulfan protocol description is original to the present work (per author commentary).

## Baseline (t=0) absolute values

For reconstructing original measurements from CSV deltas, baselines are:

| Variable | G1 baseline | G2 baseline | Source |
|----------|-------------|-------------|--------|
| Plasma recalcification time | 78.7 s | (~baseline shifted, see G2 table) | Diss. table 4.9 / 5.9 |
| Thrombin time | (per protocol) | (per protocol) | Diss. tables |
| Fibrinogen | (per protocol) | (per protocol) | Diss. tables |
| Factor XIII | 100% (by definition) | 100% (by definition) | Standard |
| Acid phosphatase | (low baseline, BO) | (low baseline, BO) | Diss. table 5.7 |
| Neutrophil count | 7.3 × 10⁹/L | 3.9 × 10⁹/L (post-busulfan, state M) | Diss. table 5.1 |

Baselines beyond neutrophil count are documented in the dissertation tables but are not numerically required by the model (which works on deltas). They will be added to `data/csv/baselines.csv` if needed for absolute-value plots in the manuscript.

## Standard errors (sigma_group1.csv, sigma_group2.csv)

Per-timepoint standard errors of the mean (SEM, the "m" in M±m) for all six
observables, for use as error bars in figures. Aligned point-for-point with
`group1.csv` / `group2.csv`. Values are SEM of the DELTA at each timepoint
(same paired-difference convention as the data).

Source rows (dissertation numbering / analytical-summary numbering):
- recalc, thrombin, fibrinogen, F.XIII — Table 4.9 (G1) / 5.9 (G2);
  summary Tables 2 (G1) / 5 (G2).
- acid phosphatase — Table 5.7; summary Table 3 (G1) AP row / 5.7 (G2).
- degranulation — Table 5.2 ("лізосомальна формула", % distribution);
  summary Tables 4a (G1) / 7a (G2), the "понад 30 лізосом %" row.

IMPORTANT — degranulation definition: `degranulation_delta_pct` in the data
CSVs is the NEGATIVE of the delta of the ">30 lysosomes %" category (the drop
in the intact-neutrophil fraction, expressed as positive degranulation), NOT
the "<10 lysosomes %" category. The SE is taken from the ">30 lysosomes %"
row accordingly. This was verified by matching CSV values against the summary
tables point-for-point.

OCR/transcription corrections applied (verified against the clean analytical
summary): factor XIII G1 day-5 SE = 2.61; fibrinogen G2 day-4 SE = 3.32;
degranulation G1 day-8 SE = 1.99, day-11 SE = 4.37. SEM reflect the surviving
cohort (n ~ 28) for G1 after day 12.

## Audit trail

All numerical values in `group1.csv` and `group2.csv` are byte-identical to the arrays in `archive/v12/model_v12.py` lines 42–58 (RECALC1, THROMB1, FIB1, XIII1, AP1, DEG1, N1_DATA; RECALC2 etc.). The migration from Python literals to CSV is verified by `tests/test_data_integrity.py`.
