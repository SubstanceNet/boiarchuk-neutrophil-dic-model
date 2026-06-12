# S9. Upper Bound on $c_x$ (Factor XIII Channel) as a Structural Prior

*Part of the Supplementary Information for Boiarchuk & Onasenko (2026). Cross-references from the main text: §2.2 ("Its relaxation opens a multimodal landscape in which factor XIII fitting competes with other Group II observables"). Related appendices: §S1.3 (role of $c_x$ in the $dX/dt$ equation), §S2.6 ($c_x$ bound saturation in Table S2 — median 545.8, upper CI 600.0), §S3.2 ($c_x$ classified as grid-truncated by profile likelihood), §S4.3 (mechanistic interpretation of the $b_x/k_x$ manifold from bootstrap).*

---

## S9.1 Settings

Two complementary series of experiments together establish the justification for the $c_x \leq 600$ bound:

- **Analysis 02 (`analyses/02_cx_bound/`):** 9 fits across three bound levels, testing what happens when the bound is removed.
- **Analysis 06 (`analyses/06_v13_cx_diagnostic/`):** 15 fits across five bound values ($c_x \leq 500, 600, 700, 1000, 2000$), three seeds each, mapping where the bound should sit.

All fits share the v13 base configuration ($W_{\text{SPLIT}} = 2.0$, uniform $W_{\text{SURV}}$, fast-mode optimisation per §S2.2). The 24-shared + 2-modifier architecture is identical across the scan; only the upper bound on $c_x$ varies.

---

## S9.2 Removing the bound: multimodal landscape

Analysis 02 ran 9 fits across three upper bound levels on $c_x$:

| **Bound** | **Seed** | **Cost** | **$c_x$ fitted** | **$R^2_{\text{xiii,G2}}$** | **$R^2_{\text{recalc,G2}}$** | **$R^2_{\text{AP,G2}}$** | **$R^2_{\text{D,G2}}$** | **$R^2_{\text{fib,G2}}$** |
|---|---|---|---|---|---|---|---|---|
| $c_x \leq 600$ (base) | 42 | 1.0431 | 599.7 | +0.728 | +0.684 | +0.678 | +0.505 | +0.293 |
| $c_x \leq 2000$ (extended) | 42 | 0.9512 | 1997.5 | −0.047 | +0.912 | +0.947 | +0.754 | +0.388 |
| $c_x \leq 2000$ (extended) | 7 | 0.9446 | 1249.0 | −0.404 | +0.908 | +0.955 | +0.766 | +0.442 |
| $c_x \leq 2000$ (extended) | 123 | 0.9496 | 1111.2 | −1.149 | +0.905 | +0.963 | +0.753 | +0.476 |
| $c_x \leq 5000$ (wide) | 42 | 0.9395 | 1890.4 | −0.472 | +0.914 | +0.958 | +0.763 | +0.448 |
| $c_x \leq 5000$ (wide) | 7 | 0.9975 | 1408.7 | +0.150 | +0.839 | +0.817 | +0.635 | +0.325 |
| $c_x \leq 5000$ (wide) | 123 | 1.0283 | 1621.1 | +0.625 | +0.737 | +0.718 | +0.522 | +0.303 |
| $c_x \leq 5000$ (wide) | 999 | 0.9458 | 1579.8 | −0.479 | +0.907 | +0.954 | +0.754 | +0.454 |
| $c_x \leq 5000$ (wide) | 2024 | 0.9401 | 2153.0 | −0.338 | +0.909 | +0.959 | +0.763 | +0.445 |

The unconstrained problem ($c_x \leq 2000$ or wider) is **multimodal**: at least two qualitatively different basins exist.

**Dominant basin ("sacrifice XIII"), 5 of 9 fits plus 2 transitional.** $R^2_{\text{xiii,G2}}$ varies in $[-1.149, -0.047]$; the remaining five Group II observables fit very well (recalc, AP, D in $[0.84, 0.96]$; fib in $[0.32, 0.48]$). $c_x$ settles widely in $[1111, 2153]$ with no narrow preferred value. Total cost: $[0.940, 0.951]$.

**Minority basin ("preserve XIII"), 2 of 9 fits.** $R^2_{\text{xiii,G2}}$ is positive ($+0.150$, $+0.625$); the remaining Group II observables fit moderately (recalc, AP, D in $[0.52, 0.84]$; fib in $[0.30, 0.33]$). $c_x$ in $[1408, 1621]$. Total cost notably higher: $[0.998, 1.028]$.

The differential-evolution optimiser falls into the minority basin in approximately 2 of 5 attempts under a wide bound. The cost difference between basins is small but consistent ($\approx 0.05$–$0.09$), and critically, **cost alone does not discriminate between basins** — they correspond to qualitatively different mechanistic interpretations of the factor XIII channel sitting at similar total costs.

---

## S9.3 Why $c_x$ alone does not determine the basin

Sorting the 8 unconstrained fits ($c_x \leq 2000$ and $c_x \leq 5000$) by fitted $c_x$ reveals that basin selection is not a simple function of $c_x$:

| **$c_x$ fitted** | **$R^2_{\text{xiii,G2}}$** | **Basin** |
|---|---|---|
| 1111.2 | −1.149 | sacrifice (deepest) |
| 1249.0 | −0.404 | sacrifice |
| 1408.7 | +0.150 | transitional / preserve |
| 1579.8 | −0.479 | sacrifice |
| 1621.1 | +0.625 | preserve (best XIII) |
| 1890.4 | −0.472 | sacrifice |
| 1997.5 | −0.047 | transitional |
| 2153.0 | −0.338 | sacrifice |

Two $c_x$ values 170 units apart (1408.7 and 1579.8, a $\approx 9\%$ difference) yield $R^2_{\text{xiii,G2}}$ of $+0.150$ and $-0.479$ — *opposite* basins. The factor XIII channel is governed by a four-parameter sloppy direction $\{a_x, c_x, b_x, k_x\}$ (§S3.2: all four classified as sloppy or grid-truncated by profile likelihood; §S4.3: the same manifold gives a broad, right-skewed bootstrap distribution via the $b_x/k_x$ ratio). $c_x$ is one component of this direction, not its primary determinant. Constraining $c_x$ with a fixed upper bound therefore selects a *subspace* of the manifold, not a single point.

---

## S9.4 Where to place the bound: zone structure (analysis 06)

Analysis 06 scanned five upper bound values, three seeds each (15 fits total):

| **Upper bound** | **Seed** | **Cost** | **$c_x$ fitted** | **$R^2_{\text{xiii,G2}}$** |
|---|---|---|---|---|
| 500 | 42 | 1.0521 | 500.0 | +0.7504 |
| 500 | 7 | 1.0524 | 498.6 | +0.7375 |
| 500 | 123 | 1.0522 | 500.0 | +0.7499 |
| 600 | 42 | 0.9589 | 570.9 | +0.0772 |
| 600 | 7 | 0.9666 | 600.0 | +0.3581 |
| 600 | 123 | 0.9622 | 599.9 | +0.4307 |
| 700 | 42 | 1.0420 | 700.0 | +0.7610 |
| 700 | 7 | 0.9595 | 700.0 | +0.3543 |
| 700 | 123 | 1.0389 | 700.0 | +0.7092 |
| 1000 | 42 | 0.9566 | 995.3 | −0.1590 |
| 1000 | 7 | 0.9534 | 1000.0 | +0.2552 |
| 1000 | 123 | 1.0401 | 999.6 | +0.6559 |
| 2000 | 42 | 1.0269 | 1319.0 | +0.6662 |
| 2000 | 7 | 0.9479 | 1999.8 | +0.2523 |
| 2000 | 123 | 1.0117 | 1247.4 | −0.1615 |

The landscape splits into two qualitatively distinct zones:

**Zone A ($c_x \leq 500$).** A unique, seed-stable optimum. Cost $\approx 1.052$ across all three seeds ($\Delta\text{cost} = 0.0003$); $R^2_{\text{xiii,G2}} \approx 0.74$ across all three seeds ($\Delta = 0.013$); fitted $c_x$ saturates near the upper bound (500.0, 498.6, 500.0). The bound acts strongly and reproducibly, but average $R^2_{\text{G2}}$ is lower than with wider bounds ($\approx 0.66$ vs. 0.69–0.75 in Zone B).

**Zone B ($c_x \geq 600$).** Multimodal. Different seeds find different local optima with widely varying $R^2_{\text{xiii,G2}}$ ($[-0.16, +0.76]$) at nearly equal total costs. Cost spreads across seeds for a fixed bound are 0.05–0.10; $R^2_{\text{xiii,G2}}$ spreads are 0.35–0.83 points. Fitted $c_x$ almost always saturates the upper bound (within 1%). The data alone do not constrain $c_x$ to a unique value in Zone B.

The transition between zones is sharp and falls between $c_x = 500$ and $c_x = 600$.

---

## S9.5 Choice of $c_x \leq 600$

The selected bound, $c_x \leq 600$, sits precisely at the transition between zones. Two of three seeds at this bound find optima with $c_x$ saturating near 600.0 (one with seed 42 settles slightly below, at 570.9), and three seeds give $R^2_{\text{xiii,G2}}$ of 0.077, 0.358, 0.431 — scattered but partial; the bound is too narrow to cleanly enter Zone B, and too wide to be in the stable Zone A.

The trade-off was discussed explicitly during the project and is reported transparently here: Zone A ($c_x \leq 500$) is methodologically clean (unique optimum) but biologically restrictive (lower average $R^2_{\text{G2}}$); Zone B ($c_x \geq 700+$) gives higher $R^2_{\text{G2}}$ in the favourable basin but is multimodal. The choice of $c_x \leq 600$ keeps the bound at the natural transition point, accepts residual factor XIII multimodality as a *characterised structural limitation* of the model (documented in §S3.2, §S4.3, and here), and avoids retreating to a tighter prior that would damage the rest of the Group II fit.

Alternative resolutions via group-specific $c_x$ or group-specific $c_f$ (additional G1/G2 modifiers in the factor XIII or fibrinogen channel) were tested in `analyses/07_*/` and `analyses/08_*/` and rejected: single-parameter group-specific extensions produced only minor regularisation side-effects, not the architectural correction the multimodality requires.

---

## S9.6 Validation by Group II observable balance

A second, independent criterion validates the $c_x \leq 600$ bound — not total cost, but the **per-observable $R^2$ balance of Group II**. Reading the per-observable Group II columns from the analysis 02 table (§S9.2):

- The constrained baseline ($c_x \leq 600$) keeps **all six Group II observables at positive $R^2$** simultaneously (the table shows five; the sixth, thrombin, is also positive in the baseline data).
- Every unconstrained fit ($n = 8$ across two basins at $c_x \leq 2000$ and $c_x \leq 5000$) has **at least one Group II observable with $R^2 < 0$** — either $R^2_{\text{xiii,G2}}$ in the dominant "sacrifice XIII" basin, or $R^2_{\text{fib,G2}}$ / $R^2_{\text{D,G2}}$ in the minority "preserve XIII" basin.

This is a stronger criterion than total cost (S9.2 already showed that cost does not discriminate between basins) and stronger than $R^2_{\text{xiii,G2}}$ alone (which can be raised by sacrificing other channels). It says that *the only configuration in which the shared model fits all six Group II observables consistently* is the $c_x \leq 600$ baseline. The bound is therefore motivated not only by identifiability (S9.3) but also chosen by a cost-free, per-observable validation.

---

## S9.7 Conclusion

Three points close the justification for the $c_x \leq 600$ prior:

- **The bound is necessary.** Its removal opens a multimodal landscape in which two qualitatively different mechanistic interpretations of the factor XIII channel sit at nearly equal cost (§S9.2). Cost cannot distinguish between basins, and $c_x$ alone does not determine which basin the optimiser finds (§S9.3).

- **The bound value is justified.** The cost landscape has a sharp zone transition between $c_x = 500$ and $c_x = 600$: a tight bound (Zone A) gives a unique optimum at the cost of average $R^2_{\text{G2}}$; a loose bound (Zone B) recovers $R^2_{\text{G2}}$ in the favourable basin at the cost of multimodality. The selected $c_x \leq 600$ sits at the transition, accepting partial multimodality as a characterised structural limitation rather than retreating to a tighter prior (§S9.4–S9.5).

- **The bound is validated.** Only the $c_x \leq 600$ configuration keeps all six Group II observables at positive $R^2$; every unconstrained fit fails on at least one Group II observable — a cost-free criterion the bound uniquely satisfies (§S9.6).

The $c_x$ upper bound saturates in the production baseline fit (Table S2: median 545.8, upper CI 600.0; §S2.6), as expected from a bound acting as a structural prior rather than a generous external constraint. This is the second of the two structural priors imposed by the joint cost function (the first — $W_{\text{SPLIT}} = 2.0$ — is §S8); together they pin the model to a biologically interpretable unique basin within the equicost manifold that the data alone would otherwise leave open.
