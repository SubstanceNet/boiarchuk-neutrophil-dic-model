"""Analysis 34 aggregate: R2<0 fraction under per-group-std -> A/B decision.

Threshold rule (N=50):
  R2<0 count <= 3/50  (<6%)   -> Variant A: per-group-std resolves it;
                                 adopt per-group-std baseline.
  R2<0 count >= 8/50  (>=16%) -> Variant B: structural component remains;
                                 retain range-SC, document as sensitivity.
  in between (4-7/50, 8-15%)  -> ambiguous; extend to N=100.

Also reports the bx/kx ratio distribution: if good-fit and bad-fit
iterations occupy distinct bx/kx zones, the multimodality is structural
(consistent with the single-seed sensitivity finding), independent of SC.
"""
from __future__ import annotations
import json
import pickle
from pathlib import Path
import numpy as np

ANALYSIS_DIR = Path(__file__).resolve().parent
CACHE_DIR = ANALYSIS_DIR / "results" / "_cache"
OBS = ["recalc", "thrombin", "fib", "xiii", "AP", "D"]


def main():
    recs = []
    for p in sorted(CACHE_DIR.glob("iter_*.pkl")):
        rec = pickle.load(p.open("rb"))
        recs.append(rec)

    ok = [r for r in recs if not r.get("failed")]
    failed = [r for r in recs if r.get("failed")]
    n = len(ok)
    print("=" * 70)
    print(f"Analysis 34 aggregate — {n} successful iters ({len(failed)} failed)")
    print("=" * 70)
    if n == 0:
        print("No successful iterations yet.")
        return

    # xiii_G2 R2 distribution
    xiii_r2 = np.array([r["g2_r2"]["xiii"] for r in ok])
    n_neg = int(np.sum(xiii_r2 < 0))
    frac_neg = n_neg / n

    print(f"\nxiii_G2 R2 distribution (n={n}):")
    print(f"  median: {np.median(xiii_r2):+.3f}")
    print(f"  mean:   {np.mean(xiii_r2):+.3f}")
    print(f"  min:    {np.min(xiii_r2):+.3f}   max: {np.max(xiii_r2):+.3f}")
    print(f"  R2 >= 0.30 (good basin): {int(np.sum(xiii_r2 >= 0.30))}/{n}")
    print(f"  R2 in [0, 0.30):         {int(np.sum((xiii_r2 >= 0) & (xiii_r2 < 0.30)))}/{n}")
    print(f"  R2 < 0 (bad basin):      {n_neg}/{n}  ({frac_neg*100:.1f}%)")

    # all-channel medians
    print(f"\nG2 R2 median by channel (n={n}):")
    for k in OBS:
        vals = np.array([r["g2_r2"][k] for r in ok])
        print(f"  {k:>9}: median {np.median(vals):+.3f}  (R2<0 in {int(np.sum(vals<0))}/{n})")

    # bx/kx ratio by basin
    def bxkx(r):
        x = r["best_x"]
        return x[22] / x[23] if x[23] != 0 else float("nan")
    good = [bxkx(r) for r in ok if r["g2_r2"]["xiii"] >= 0.30]
    bad = [bxkx(r) for r in ok if r["g2_r2"]["xiii"] < 0]
    print(f"\nbx/kx ratio by XIII basin:")
    if good:
        print(f"  good basin (R2>=0.30): median {np.median(good):.2f} "
              f"[{np.min(good):.2f}, {np.max(good):.2f}], n={len(good)}")
    if bad:
        print(f"  bad basin  (R2<0):     median {np.median(bad):.2f} "
              f"[{np.min(bad):.2f}, {np.max(bad):.2f}], n={len(bad)}")

    # baseline (analysis 22) comparison
    base_cache = Path("analyses/22_predictive_check/results/_cache")
    base_neg = base_total = 0
    for p in sorted(base_cache.glob("iter_*.pkl")):
        r = pickle.load(p.open("rb"))
        if r.get("failed"):
            continue
        # analysis 22 may store g2 R2 differently; guard
        g2 = r.get("g2_r2") or {}
        if "xiii" in g2:
            base_total += 1
            if g2["xiii"] < 0:
                base_neg += 1
    if base_total:
        print(f"\nbaseline (analysis 22, range-SC): xiii_G2 R2<0 in "
              f"{base_neg}/{base_total} ({base_neg/base_total*100:.1f}%)")

    # verdict
    print("\n" + "=" * 70)
    print("DECISION")
    print("=" * 70)
    print(f"per-group-std xiii_G2 R2<0: {n_neg}/{n} ({frac_neg*100:.1f}%)")
    if n < 50:
        print(f"NOTE: only {n}/50 iters done — verdict provisional.")
    if frac_neg <= 0.06:
        verdict = "A"
        print("-> VARIANT A: per-group-std resolves the XIII under-determination.")
        print("   The 41% R2<0 was substantially a normalization artifact.")
        print("   Recommend adopting per-group-std baseline (needs N=100 for production).")
    elif frac_neg >= 0.16:
        verdict = "B"
        print("-> VARIANT B: a structural R2<0 component remains under per-group-std.")
        print("   XIII under-determination is real, not purely an SC artifact.")
        print("   Retain range-SC baseline; document per-group-std as sensitivity")
        print("   (and soften the 'structural' claim with the artifact contribution).")
    else:
        verdict = "AMBIGUOUS"
        print(f"-> AMBIGUOUS ({frac_neg*100:.1f}%, between 6% and 16%).")
        print("   Extend to N=100 before deciding.")

    out = dict(
        n=n, n_failed=len(failed),
        xiii_r2_neg_count=n_neg, xiii_r2_neg_frac=frac_neg,
        xiii_r2_median=float(np.median(xiii_r2)),
        bxkx_good_median=float(np.median(good)) if good else None,
        bxkx_bad_median=float(np.median(bad)) if bad else None,
        baseline_neg=base_neg, baseline_total=base_total,
        verdict=verdict,
    )
    (ANALYSIS_DIR / "results" / "aggregate.json").write_text(json.dumps(out, indent=2))
    print(f"\nSaved: {ANALYSIS_DIR / 'results' / 'aggregate.json'}")


if __name__ == "__main__":
    main()
