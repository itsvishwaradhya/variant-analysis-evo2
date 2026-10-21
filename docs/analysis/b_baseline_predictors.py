"""
Analysis B: reference-baseline evaluation on the exact calibration slice used
by Evo2Serve.

`run_brca1_analysis` in evo2-backend/main.py calibrates the decision threshold
on the first 500 rows of the Findlay et al. BRCA1 saturation-genome-editing
workbook.  That same workbook carries pre-computed annotations for four
established variant effect predictors (CADD, PolyPhen-2, SIFT, aGVD) together
with a mammalian phyloP score, gnomAD allele frequency and a ClinVar call.
This script evaluates those predictors on the identical 500 rows, with the
identical label definition and the identical threshold-selection procedure
that the Evo2Serve calibration routine uses (Youden index on the ROC).

The result is a reproducible reference table: it fixes what a zero-shot
genomic language model deployed through Evo2Serve has to beat, and it is
computed without a GPU.

Run:
    evo2-backend/venv/Scripts/python.exe docs/analysis/b_baseline_predictors.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, roc_auc_score, roc_curve

REPO = Path(__file__).resolve().parents[2]
XLSX = REPO / "evo2-backend/evo2/notebooks/brca1/41586_2018_461_MOESM3_ESM.xlsx"
SLICE = 500
N_BOOT = 2000
SEED = 20240517

rng = np.random.default_rng(SEED)
out: dict = {}


def rule(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


# --------------------------------------------------------------------------
df = pd.read_excel(XLSX, header=2)
raw = df["func.class"].value_counts()
n = len(df)
out["workbook_rows"] = int(n)
out["workbook_class_counts"] = {str(k): int(v) for k, v in raw.items()}
out["workbook_class_pct"] = {str(k): float(v / n * 100) for k, v in raw.items()}

rule("B.1  Three-class composition of the full saturation genome editing set")
for k, v in raw.items():
    print(f"  {str(k):>8} : {int(v):>5}  ({v/n*100:5.2f}%)")
print(f"  {'total':>8} : {n:>5}")

# --------------------------------------------------------------------------
sub = df.iloc[:SLICE].copy()
sub["class"] = sub["func.class"].replace(["FUNC", "INT"], "FUNC/INT")
y = (sub["class"] == "LOF").to_numpy().astype(int)
out["slice_n"] = int(len(sub))
out["slice_pos"] = int(y.sum())
out["slice_neg"] = int((1 - y).sum())
out["slice_prevalence"] = float(y.mean())

rule("B.2  The 500-row calibration slice")
print(f"  rows            : {len(sub)}")
print(f"  LOF (positive)  : {int(y.sum())}")
print(f"  FUNC/INT (neg.) : {int((1-y).sum())}")
print(f"  prevalence      : {y.mean():.3f}")
print(f"  class counts by workbook order: first 250 rows -> "
      f"LOF={int(y[:250].sum())}, last 250 rows -> LOF={int(y[250:].sum())}")
out["slice_half_lof"] = [int(y[:250].sum()), int(y[250:].sum())]


# --------------------------------------------------------------------------
def bootstrap_auc(scores: np.ndarray, labels: np.ndarray, n_boot: int = N_BOOT):
    """Percentile bootstrap CI for AUROC, stratified by class."""
    aucs = []
    pos = np.where(labels == 1)[0]
    neg = np.where(labels == 0)[0]
    for _ in range(n_boot):
        bi = np.concatenate(
            [rng.choice(pos, size=len(pos), replace=True),
             rng.choice(neg, size=len(neg), replace=True)]
        )
        if len(np.unique(labels[bi])) < 2:
            continue
        aucs.append(roc_auc_score(labels[bi], scores[bi]))
    return float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))


def evaluate(col: str, direction: str, label: str) -> dict | None:
    """Evaluate one annotation column.

    direction '+': a higher raw value indicates loss of function.
    direction '-': a lower raw value indicates loss of function.

    The operating point is selected exactly as run_brca1_analysis selects it:
    maximise TPR - FPR on the ROC of the oriented score, then convert the
    threshold back into raw score space.
    """
    if col not in sub.columns:
        return None
    vals = pd.to_numeric(sub[col], errors="coerce")
    if vals.isna().all():
        return None
    s = vals.to_numpy(dtype=float)
    keep = ~np.isnan(s)
    s, yy = s[keep], y[keep]
    if len(np.unique(yy)) < 2:
        return None

    oriented = s if direction == "+" else -s
    auc = float(roc_auc_score(yy, oriented))
    lo, hi = bootstrap_auc(oriented, yy)

    fpr, tpr, thr = roc_curve(yy, oriented)
    idx = int((tpr - fpr).argmax())
    oriented_thr = float(thr[idx])
    raw_thr = oriented_thr if direction == "+" else -oriented_thr

    pred = (oriented >= oriented_thr).astype(int)
    tp = int(np.sum(pred & (yy == 1)))
    fp = int(np.sum(pred & (yy == 0)))
    fn = int(np.sum((1 - pred) & (yy == 1)))
    tn = int(np.sum((1 - pred) & (yy == 0)))
    prec = tp / (tp + fp) if tp + fp else float("nan")
    rec = tp / (tp + fn) if tp + fn else float("nan")
    spec = tn / (tn + fp) if tn + fp else float("nan")
    f1 = (2 * prec * rec / (prec + rec)) if prec + rec else float("nan")
    return {
        "label": label,
        "column": col,
        "direction": direction,
        "n_used": int(keep.sum()),
        "n_missing": int((~keep).sum()),
        "auroc": auc,
        "auroc_ci95_low": lo,
        "auroc_ci95_high": hi,
        "youden_j": float(tpr[idx] - fpr[idx]),
        "threshold_raw": raw_thr,
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": prec, "recall": rec, "specificity": spec, "f1": f1,
        "accuracy": (tp + tn) / len(yy),
        "balanced_accuracy": float(balanced_accuracy_score(yy, pred)),
    }


# ClinVar call recoded to a binary label (pathogenic-like = 1)
cl = sub["clinvar_simple"].astype(str).str.strip()
clinvar_bin = cl.map(
    {
        "Pathogenic": 1,
        "Likely pathogenic": 1,
        "Likely benign": 0,
        "Benign": 0,
        "Conflicting interpretations of pathogenicity": 0,
        "absent": np.nan,
    }
)
sub["_clinvar_bin"] = clinvar_bin

rule("B.3  Reference predictors on the identical 500-row slice")
print(f"{'predictor':<24}{'n':>5}{'AUROC':>8}{'95% CI':>20}"
      f"{'sens':>8}{'spec':>8}{'prec':>8}{'bal.acc':>10}")
results = []
for col, direction, label in [
    ("CADD.score", "+", "CADD score"),
    ("polyphen2", "+", "PolyPhen-2"),
    ("sift", "-", "SIFT"),
    ("aGVGD.diff", "-", "aGVD"),
    ("phyloP (mammalian)", "+", "phyloP (mammalian)"),
    ("gnomAD_AF", "-", "gnomAD allele frequency"),
    ("_clinvar_bin", "+", "ClinVar (recoded)"),
]:
    r = evaluate(col, direction, label)
    if r is None:
        print(f"{label:<24}  [column absent or non-numeric]")
        continue
    results.append(r)
    ci = f"[{r['auroc_ci95_low']:.3f}, {r['auroc_ci95_high']:.3f}]"
    print(f"{label:<24}{r['n_used']:>5}{r['auroc']:>8.3f}{ci:>20}"
          f"{r['recall']:>8.3f}{r['specificity']:>8.3f}{r['precision']:>8.3f}"
          f"{r['balanced_accuracy']:>10.3f}")
out["predictors"] = results

rule("B.4  What the slice can and cannot resolve")
usable = [r for r in results if r["column"] != "_clinvar_bin"]
best = max(usable, key=lambda r: r["auroc"])
out["best_non_clinvar_baseline"] = best["label"]
out["best_non_clinvar_baseline_auroc"] = best["auroc"]
out["best_non_clinvar_baseline_ci"] = [best["auroc_ci95_low"],
                                        best["auroc_ci95_high"]]
print(f"  strongest non-ClinVar reference predictor : {best['label']}")
print(f"  AUROC                                     : {best['auroc']:.3f} "
      f"[{best['auroc_ci95_low']:.3f}, {best['auroc_ci95_high']:.3f}]")
print(f"  samples per class                         : {out['slice_pos']} / "
      f"{out['slice_neg']}")
print(f"  one AUROC step on this slice              : "
      f"{1/min(out['slice_pos'], out['slice_neg']):.4f}")
print(f"  null AUROC                                : 0.500")
print(f"  prevalence of LOF                         : {out['slice_prevalence']:.3f}")
print("  Every AUROC reported here carries a bootstrap interval of roughly")
print(f"  +/- {(best['auroc_ci95_high']-best['auroc_ci95_low'])/2:.3f}.  Differences")
print("  between predictors that are smaller than that interval are not")
print("  resolvable on this slice.")

rule("B.5  Sampling of the 500-row slice")
out["slice_position_span"] = [int(sub["position (hg19)"].min()),
                               int(sub["position (hg19)"].max())]
out["workbook_position_span"] = [int(df["position (hg19)"].min()),
                                 int(df["position (hg19)"].max())]
out["slice_covers_pct_of_span"] = float(
    100 * (sub["position (hg19)"].max() - sub["position (hg19)"].min())
    / (df["position (hg19)"].max() - df["position (hg19)"].min())
)
out["slice_n_distinct_aa_positions"] = int(sub["aa_pos"].nunique())
out["slice_n_distinct_transcript_positions"] = int(
    sub["transcript_position"].nunique()
)
print(f"  slice span (hg19)    : {out['slice_position_span'][0]:,} .. "
      f"{out['slice_position_span'][1]:,}")
print(f"  workbook span (hg19) : {out['workbook_position_span'][0]:,} .. "
      f"{out['workbook_position_span'][1]:,}")
print(f"  slice covers         : {out['slice_covers_pct_of_span']:.2f}% of the "
      f"position range")
print(f"  distinct coding positions in slice: "
      f"{out['slice_n_distinct_transcript_positions']} transcript positions, "
      f"{out['slice_n_distinct_aa_positions']} amino-acid positions")
p = out["slice_pos"] / out["workbook_rows"]
out["slice_lof_expected_under_random"] = float(p * SLICE)
out["slice_lof_sd_under_random"] = float(np.sqrt(SLICE * p * (1 - p)))
print(f"  LOF under uniform random sampling of {SLICE} rows: "
      f"{p*SLICE:.1f} +/- {np.sqrt(SLICE*p*(1-p)):.1f} (sd)")
print(f"  LOF observed in the slice                    : "
      f"{out['slice_pos']}")
print(f"  ratio to the random expectation               : "
      f"{out['slice_pos']/out['slice_lof_expected_under_random']:.2f}x")
out["slice_consequence_counts"] = {
    str(k): int(v) for k, v in sub["consequence"].value_counts().items()
}
print(f"  consequence mix in the slice: {out['slice_consequence_counts']}")

dest = REPO / "docs/analysis/b_baseline_predictors.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
print(f"\nwrote {dest}")
