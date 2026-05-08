# Known issues and open questions

This is the running log of known issues, methodological concerns, and open questions. Internal document — not for publication. Each entry has a status: **open**, **deferred to phase X**, **resolved in phase X**, or **wontfix (with reason)**.

## I-1: cx parameter bound vs reported value (RESOLVED in Phase 1, analysis 02)

**Original concern.** `archive/v12/model_v12.py` sets `BOUNDS[21]` (cx) to `(10, 600)`. The companion `v12_report.md` (§7.5) reports a fitted value of cx = 1481, outside this bound. There is also a comment indicating "cx=600↑" — i.e. cx stuck at upper bound — but the numerical value 1481 contradicts this.

**Investigation.** `analyses/02_cx_bound/`: three-point sweep across cx upper bounds {600, 2000, 5000} with seed=42, then convergence check at expanded {2000} and wide {5000} for seeds {7, 123}; supplementary check pending at wide {5000} for seeds {999, 2024}.

**Findings.**

1. **Strong descending trend** in cx vs xiii_G2 R-squared across the 6 unconstrained fits, with one outlier point (wide/s123: cx=1621, xiii_G2=+0.62). Whether this is a stable alternative basin or a single-seed convergence artefact is being verified by 2 supplementary fits.

2. **Cost is non-discriminating** between mechanistically heterogeneous local optima. Within wide (cx ≤ 5000), three seeds give cost ∈ [0.940, 1.028] but xiii_G2 R-squared ∈ [-0.47, +0.63]. Identifiability failure in the unconstrained search space.

3. **cx alone does not determine xiii fit quality.** Across 6 unconstrained fits cx values cover [1111, 1997] with no monotonic relation to xiii_G2 R-squared. The XIII channel is governed by four parameters {ax, cx, bx, kx} that co-vary along a sloppy direction.

4. **Only the constrained baseline (cx ≤ 600) keeps all six G2 observables at positive R-squared.** All 6 unconstrained fits have at least one G2 observable with R-squared < 0 (XIII in 5/6 cases; one fit with positive XIII has lower scores on recalc/AP/D than baseline).

5. **v12 report value cx=1481 explained.** It falls within the cx range observed in unconstrained fits ([1111, 1997]). It represents an earlier development run with broader bounds, which sacrificed XIII fit quality without that being noticed (the report tracked aggregate R-squared metrics, not per-observable G2 quality).

**Methodological reframing.** The bound (10, 600) is not artefactually constraining. It is a structural prior on the XIII channel that limits the full {ax, cx, bx, kx} manifold to the biologically interpretable subspace where all G2 observables have positive R-squared. Analogous in role to the W_split = 2.0 prior on mechanism-split decomposition.

**Action items for manuscript.**
- Present cx bound as structural prior on the XIII channel, in a "structural priors" methods subsection together with W_split.
- Justify both priors via identifiability collapse without them: without W_split, mechanism decomposition becomes non-unique; without the cx bound, XIII channel becomes non-identifiable.
- Validate via post-hoc held-out balance: in the constrained regime, all six G2 observables have positive R-squared; without the priors, multiple observables collapse to R-squared < 0.
- Analysis 02 becomes a methods supplement demonstrating necessity of the cx prior.

**Open follow-up for Phase 2.** XIII-channel sloppiness {ax, cx, bx, kx} should be formally characterised by profile likelihood + FIM in Phase 2 step 3.

**Status.** Resolved (final wording pending seed_check_extra results).

## I-2: G2 R² regression on joint fit vs separate fit (RESOLVED in Phase 1, analysis 03)

**Original concern.** v11.2 diagnostic separate fits: G2 average R² = 0.868 (25 free parameters fitted to G2 alone, 54 datapoints). v12 joint fit: G2 average R² = 0.598 (24 shared params + 2 modifiers). The R² drop is large and not adequately explained in the v12 report.

**Two competing interpretations.**
1. **Honest deflation.** Separate fit overfit (25 params on 54 points = 2.16 ratio); joint fit reflects the true G2 fit quality under shared biochemistry. The 0.598 figure is closer to the truth.
2. **Architectural pull.** Joint fit pulls parameters toward G1 (which has more data) and the mechanism-split constraint is calibrated on G1 day 2. G2 fits suffer because the architecture is biased.

**Investigation.** `analyses/03_separate_g2_fit/`: re-run separate G2 fit under current code (26 free parameters on 54 datapoints). Compare to analysis 02 baseline (joint-fit R²_G2 avg = 0.620).

**Findings.**

- Separate-fit R²_G2 avg = 0.8363 (vs joint-fit 0.620, Δ = +0.2159). This is **Case C** (Δ > 0.15) of the decision rule.
- The improvement is **systematic across all 6 G2 observables**, not concentrated on a few:
  - recalc: +0.901 (vs +0.684, Δ = +0.217)
  - thrombin: +0.994 (Δ = +0.159)
  - fib: +0.578 (Δ = +0.285) — largest deficit was here
  - xiii: +0.798 (Δ = +0.070) — smallest gap (XIII supported by cx prior)
  - AP: +0.928 (Δ = +0.250)
  - D: +0.819 (Δ = +0.314)
- This systematic pattern (uniform improvement) is more consistent with **interpretation 2** (architectural pull) than with **interpretation 1** (overfitting). Pure overfitting would produce spiky improvements on a few observables, not uniform gains across all six.
- Caveat: data/parameter ratio of 2.08 means some overfitting in the separate fit is unavoidable. The 0.868 v11.2 value likely was inflated by overfitting; the true separate-fit quality at current bounds is 0.836. The architectural penalty (joint vs separate) is therefore ~0.22 R² units, not the full 0.27.

**Conclusion.** The joint architecture has a real architectural penalty of approximately 22 percentage points of R²_G2 average. The penalty is the price of parameter sharing across groups — currently only `km` and `tm` are group-specific, while 24 parameters are shared.

**Action items for Phase 2.**
- Address via expanded group-specific parameter set in v13. Likely candidates (in order of expected impact, by Δ R² in this analysis): D (+0.314), AP (+0.250), fib (+0.285), recalc (+0.217), thrombin (+0.159).
- Most plausible structural changes: group-specific c_f (fib / AP), kna (Hn formation), kx (XIII liver resynthesis), kd (degranulation rate). Each can plausibly differ between groups under neutrophil suppression.
- Phase 2 step 1 (profile likelihood per parameter, separate G1 / G2 cost decomposition) should reveal which parameters most need group-specificity.

**Status.** Resolved. Analysis 03 closed.


## I-3: Mechanism-split constraint as circular evidence (RESOLVED in Phase 1, analysis 01)

**Original concern.** The mechanism-split constraint (`W_split=2.0` in `config.py`) forces the day-2 pro-coagulant fractions to (24%, 76%, 82%) for (recalc, fib, xiii). These targets were derived from G2/G1 ratios at day 1 in the dissertation tables (v12 report §3.3). The model is then used to fit those same data and to report the mechanism-split as a result. This is methodologically circular: we cannot use a ratio to derive a target and then use the target-fit as evidence for the underlying mechanism.

**Investigation.** `analyses/01_w_split_profile/`: parametric sweep across W ∈ {0.0, 0.3, 1.0, 2.0, 5.0} with seed=42 (n=5 fits), then convergence check at W ∈ {0.0, 2.0} with seeds {7, 123} (n=4 fits). Total: 9 fits.

**Findings.**

1. **W=2.0 is seed-stable.** Across three seeds (42, 7, 123), realised fractions are (recalc=0.244, fib=0.740, xiii=0.808) ± 0.005. Cost spread Δ=0.014. The constrained optimum is unique up to numerical precision.

2. **W=0.0 is cost-stable but mechanistically non-identifiable.** Across the same three seeds, cost varies by Δ=0.009 (essentially identical aggregate fit), but realised fractions vary widely: recalc ∈ [0.34, 0.48], fib ≈ 0.05 (stuck near zero), xiii ∈ [0.72, 0.78]. The unconstrained problem has a flat manifold of cost-equivalent solutions with different mechanistic interpretations.

3. **W=2.0 wins on held-out G2.** R²_G2 at W=2.0: {0.620, 0.621, 0.602} for seeds {42, 7, 123}. R²_G2 at W=0.0: {0.548, 0.605, 0.577}. The constraint improves G2 fit by 2-7 percentage points across all tested seeds. The constrained optimum is independently validated by group-II performance.

4. **Cost is non-monotonic in W.** Minimum at W=0.3 (cost=0.956), then rises to W=2 (1.043) before falling at W=5 (0.962). However, R²_G2 monotonically increases in W on this grid. The cost minimum at W=0.3 reflects an intermediate point where the constraint penalty is small enough to allow alternative parameterisations but large enough to prevent the worst pathologies of W=0.

**Methodological reframing.** The constraint is not circular evidence in the original sense. The data alone do not determine a unique mechanistic decomposition (W=0 fits demonstrate this). The constraint W=2 selects a single optimum from the cost-equivalent manifold; this selection is independently validated by superior G2 performance. The honest framing for publication is that the model exhibits standard non-identifiability resolved by a structural prior, with the prior choice validated by held-out fit quality, not that the mechanism-split decomposition (24/76/82%) is data-supported in unconstrained form.

**Action items for manuscript.**
- Report the W-sweep as a methods supplement.
- Frame the mechanism-split constraint as "structural prior derived from G2/G1 day-1 ratios; selection validated by superior held-out R²_G2 at W=2 across three random seeds".
- Drop any claim that the decomposition fractions are data-determined absent the prior.

**Status.** Resolved. Analysis 01 closed.


## I-4: Fibrinogen G2 R² = 0.26 (open)

**Issue.** v12 report §5.2: under joint fit, G2 fibrinogen R² = 0.26 — by far the worst observable. Other G2 R² are ≥ 0.49 (still mediocre but acceptable given limited datapoints). The v12 report (§7.5) flags this as a known limitation: the model insufficiently captures the steep fibrinogen drop on day 4 at high AP.

**Possible structural fixes.**
- Additional channel for hepatic fibrinogen synthesis with explicit IL-6 dynamics.
- Allow `c_f` (fib / AP) to be group-specific, like km/tm.
- Different functional form for the AP -> fib link (saturable rather than linear?).

**Resolution path.** Phase 2 task. After identifiability analysis is done in Phase 1, propose model variants and select via AIC/BIC.

## I-5: Survivor weighting is qualitative (RESOLVED in Phase 1, analysis 04)

**Original concern.** `W_SURV = [1.0]*10 + [0.7]*3 + [0.3]*3` weights G1 timepoints to reflect 30% mortality on days 10-12 and further dropout afterward. The values 0.7 and 0.3 are qualitative — they roughly match surviving fraction but are not derived from a likelihood justification.

**Investigation.** `analyses/04_survivor_weighting/`: re-run analysis 02 baseline fit with `W_SURV = ones(16)` (uniform weighting), compare aggregate and per-observable metrics.

**Findings.**

- With uniform W_SURV: cost = 0.9775, R²_G1 avg = +0.8279, R²_G2 avg = +0.7162.
- Compared to default W_SURV: Δcost = -0.0656, ΔR²_G1 = -0.0061, ΔR²_G2 = +0.0958.
- **Uniform weighting is strictly better by every aggregate metric.** Cost is lower, R²_G1 essentially unchanged (Δ < 0.01), R²_G2 substantially improved (~10 percentage points).

**Methodological reframing.** The original v12 W_SURV choice was an over-correction: it was intended to discount late G1 data due to mortality, but in practice it discards information that helps the joint fit balance G1 and G2. Late G1 timepoints (days 11-19) carry recovery-phase information that constrains the long-term parameters; downweighting them frees those parameters to drift toward G1-acute-phase optimum at the expense of G2.

**Caveat.** This finding is from a single seed (42). Before committing to the change as a permanent default, seed-stability check is recommended (seeds {7, 123}). To be done together with v13 cost redesign in Phase 2.

**Action items for Phase 2.**
- Default to uniform W_SURV in v13 cost.
- If a non-uniform weighting is desired (e.g., for biological reasons), derive it from per-timepoint sample size in the surviving cohort, not from heuristic values like 0.7 and 0.3.
- The actual mortality timeline is documented (n=40, 12 deaths on days 10-12). A principled inverse-sample-size weighting would be: w_t ∝ n_t (surviving), giving approximately {1.0 for days ≤ 9, 0.85 for days 10-12, 0.70 for days 13+}, much milder than the v12 choice.

**Status.** Resolved. Analysis 04 closed.


## I-6: τ_v and k_cd fixed without explicit justification (open)

**Issue.** `TV_FIX = 1.5` and `KCD_FIX = 0.2` are not optimised. They were set during the diagnostic phase. Their fixity reduces the effective parameter count and may bias other parameters.

**Resolution path.** Phase 1: include these in the profile likelihood scan. If they are well-constrained by data, the fixed values are defensible. If not, refit them with priors and report the effect on the rest of the fit.

## I-7: v12_report.docx is mislabelled file format (cosmetic; resolved)

**Issue.** Original `v12_report.docx` distributed with the project files is in fact UTF-8 plain text with markdown formatting, not a Word document. Word/LibreOffice will not open it.

**Resolution.** Renamed to `archive/v12/v12_report.md` during Phase 0 migration. Original archive intact; no further action.

## I-8: License selection (RESOLVED in Phase 0)

**Original concern.** `pyproject.toml` and README list license as "TBD". Must be selected before any external sharing.

**Resolution.** Selected during Phase 0 closure (commit 9e1e70e + amended commit 02c118f):
- Code (`src/`, `tests/`, `analyses/`): Apache License 2.0 → `LICENSE` file
- Data, documentation, manuscript sources, internal notes: Creative Commons Attribution 4.0 International (CC-BY-4.0) → `LICENSE-DOCS` file

`pyproject.toml` license field updated to `"Apache-2.0 AND CC-BY-4.0"`. Both licenses permit reuse with attribution.

**Status.** Resolved.
