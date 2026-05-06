# Known issues and open questions

This is the running log of known issues, methodological concerns, and open questions. Internal document — not for publication. Each entry has a status: **open**, **deferred to phase X**, **resolved in phase X**, or **wontfix (with reason)**.

## I-1: cx parameter bound vs reported value (open)

**Issue.** `archive/v12/model_v12.py` sets `BOUNDS[21]` (cx) to `(10, 600)`. The companion `v12_report.md` (§7.5) reports a fitted value of cx = 1481, which lies outside this bound. There is also a comment in the report indicating "cx=600↑" — i.e. cx was stuck at the upper bound — but the numerical value 1481 contradicts this.

**Possible explanations.**
1. The report was written against a development version where bounds were wider; bounds were tightened to (10, 600) before the script was finalised, but the report numbers were not updated.
2. There were multiple v12 runs with different bound settings; the report aggregates across them inconsistently.
3. Typo in the report.

**Resolution path.** Phase 1 task. (a) Run a fresh v12 fit with current bounds and record cx. (b) Compare to historical fit results (if any are recoverable). (c) If cx is consistently at the upper bound (600), expand the bound and refit; track whether expanded bound improves any R². If yes, the bound is artefactual; if not, cx is well-determined inside [10, 600] and the 1481 figure was an error.

## I-2: G2 R² regression on joint fit vs separate fit (open)

**Issue.** v11.2 diagnostic separate fits: G2 average R² = 0.868 (25 free parameters fitted to G2 alone, 54 datapoints). v12 joint fit: G2 average R² = 0.598 (24 shared params + 2 modifiers). The R² drop is large and not adequately explained in the v12 report.

**Two competing interpretations.**
1. **Honest deflation.** Separate fit overfit (25 params on 54 points = 2.16 ratio); joint fit reflects the true G2 fit quality under shared biochemistry. The 0.598 figure is closer to the truth.
2. **Architectural pull.** Joint fit pulls parameters toward G1 (which has more data) and the mechanism-split constraint is calibrated on G1 day 2. G2 fits suffer because the architecture is biased.

**Resolution path.** Phase 2 task. (a) AIC/BIC comparison: v12 joint vs v12 separate-G2 vs intermediate (varying number of group-specific parameters). (b) Profile likelihood for each parameter under joint fit: are any parameters pulled to G1-side bounds at the cost of G2 fit?

## I-3: Mechanism-split constraint as circular evidence (open)

**Issue.** The mechanism-split constraint (W_split=2.0 in `config.py`) forces the day-2 pro-coagulant fractions to (24%, 76%, 82%) for (recalc, fib, xiii). These targets were derived from G2/G1 ratios at day 1 in the dissertation tables (v12 report §3.3). The model is then used to fit those same data and to report the mechanism-split as a result. This is methodologically circular: we cannot use a ratio to derive a target and then use the target-fit as evidence for the underlying mechanism.

**Resolution path.** Phase 1 task. (a) Profile the fit at W = 0, 0.3, 1.0, 2.0 — does relaxing the constraint change parameter values, R², or biological interpretation? (b) If the fit is robust to W, the constraint is harmless and we can drop it for the publication. (c) If the fit is W-dependent, the constraint must be either justified independently (external prior with citation) or dropped, in which case the mechanism-split decomposition must be presented as a *posterior result* of the unconstrained fit, not an enforced one.

## I-4: Fibrinogen G2 R² = 0.26 (open)

**Issue.** v12 report §5.2: under joint fit, G2 fibrinogen R² = 0.26 — by far the worst observable. Other G2 R² are ≥ 0.49 (still mediocre but acceptable given limited datapoints). The v12 report (§7.5) flags this as a known limitation: the model insufficiently captures the steep fibrinogen drop on day 4 at high AP.

**Possible structural fixes.**
- Additional channel for hepatic fibrinogen synthesis with explicit IL-6 dynamics.
- Allow `c_f` (fib / AP) to be group-specific, like km/tm.
- Different functional form for the AP -> fib link (saturable rather than linear?).

**Resolution path.** Phase 2 task. After identifiability analysis is done in Phase 1, propose model variants and select via AIC/BIC.

## I-5: Survivor weighting is qualitative (open)

**Issue.** `W_SURV = [1.0]*10 + [0.7]*3 + [0.3]*3` weights G1 timepoints to reflect 30% mortality on days 10–12 and further dropout afterward. The values 0.7 and 0.3 are qualitative — they roughly match surviving fraction but are not derived from a likelihood justification.

**Resolution path.** Phase 1 task, low priority. Replace with proper inverse-variance weighting where the per-timepoint variance accounts for measurement noise + survivor sampling bias. Likely cosmetic effect on parameter values; document the change either way.

## I-6: τ_v and k_cd fixed without explicit justification (open)

**Issue.** `TV_FIX = 1.5` and `KCD_FIX = 0.2` are not optimised. They were set during the diagnostic phase. Their fixity reduces the effective parameter count and may bias other parameters.

**Resolution path.** Phase 1: include these in the profile likelihood scan. If they are well-constrained by data, the fixed values are defensible. If not, refit them with priors and report the effect on the rest of the fit.

## I-7: v12_report.docx is mislabelled file format (cosmetic; resolved)

**Issue.** Original `v12_report.docx` distributed with the project files is in fact UTF-8 plain text with markdown formatting, not a Word document. Word/LibreOffice will not open it.

**Resolution.** Renamed to `archive/v12/v12_report.md` during Phase 0 migration. Original archive intact; no further action.

## I-8: License not yet selected (open)

**Issue.** `pyproject.toml` and README list license as "TBD". Must be selected before any external sharing of the repository.

**Resolution path.** Discuss with author. Options include MIT (permissive), CC-BY-4.0 (data + docs convention), or hybrid (code MIT, data + manuscript CC-BY).
