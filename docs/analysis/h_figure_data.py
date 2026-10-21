"""
Analysis H: data for the manuscript figures.

Every coordinate series that appears in a figure of the paper is computed
here and written to docs/analysis/figure_data.tex, so the figures are
derived from the same measurements that populate the tables and can be
regenerated with one command.

Run:
    evo2-backend/venv/Scripts/python.exe docs/analysis/h_figure_data.py
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
from Bio import SeqIO
from sklearn.metrics import roc_curve

REPO = Path(__file__).resolve().parents[2]
XLSX = REPO / "evo2-backend/evo2/notebooks/brca1/41586_2018_461_MOESM3_ESM.xlsx"
FASTA_GZ = REPO / "evo2-backend/evo2/notebooks/brca1/GRCh37.p13_chr17.fna.gz"
SLICE = 500
WINDOW = 8192
HALF = WINDOW // 2

df = pd.read_excel(XLSX, header=2)
sub = df.iloc[:SLICE].copy()
sub["class"] = sub["func.class"].replace(["FUNC", "INT"], "FUNC/INT")
y = (sub["class"] == "LOF").to_numpy().astype(int)

lines: list[str] = []
out: dict = {}


def emit(name: str, body: str) -> None:
    lines.append(f"%% {name}")
    lines.append(body)
    lines.append("")


# --------------------------------------------------------------------------
# 1. Class composition of the assay and of the calibration slice
# --------------------------------------------------------------------------
whole = df["func.class"].value_counts()
whole_order = ["FUNC", "INT", "LOF"]
whole_vals = [int(whole.get(k, 0)) for k in whole_order]
slice_counts = sub["class"].value_counts()
slice_vals = [
    int(slice_counts.get("FUNC/INT", 0)),
    0,
    int(slice_counts.get("LOF", 0)),
]

emit("composition of the assay set and of the calibration slice",
     "\\def\\assayFUNC{%d}\\def\\assayINT{%d}\\def\\assayLOF{%d}\n"
     "\\def\\sliceFUNC{%d}\\def\\sliceINT{%d}\\def\\sliceLOF{%d}"
     % (*whole_vals, *slice_vals))
out["assay_class_counts"] = dict(zip(whole_order, whole_vals))
out["slice_class_counts"] = dict(zip(whole_order, slice_vals))

# --------------------------------------------------------------------------
# 2. Position coverage: the slice inside the assayed region
# --------------------------------------------------------------------------
pos_all = df["position (hg19)"].to_numpy(dtype=np.int64)
pos_sub = sub["position (hg19)"].to_numpy(dtype=np.int64)
lo, hi = int(pos_all.min()), int(pos_all.max())
NBIN = 40
edges = np.linspace(lo, hi, NBIN + 1)
hist_all, _ = np.histogram(pos_all, bins=edges)
hist_sub, _ = np.histogram(pos_sub, bins=edges)
# Bin left edges, plus a closing point at the right end so that the
# ybar-interval handler draws the final bar up to x = 1.
lefts = [(edges[i] - lo) / (hi - lo) for i in range(NBIN)]
coords = " ".join(f"({lefts[i]:.4f},{hist_all[i]})" for i in range(NBIN))
coords += f" (1.0000,0)"
coords_sub = " ".join(f"({lefts[i]:.4f},{hist_sub[i]})" for i in range(NBIN))
coords_sub += " (1.0000,0)"
emit("position coverage of the assayed region and of the calibration slice",
     f"\\def\\coverageAll{{{coords}}}\n\\def\\coverageSlice{{{coords_sub}}}\n"
     f"\\def\\coverageLo{{{lo}}}\n\\def\\coverageHi{{{hi}}}")
out["assayed_span"] = [lo, hi]
out["slice_span"] = [int(pos_sub.min()), int(pos_sub.max())]

# --------------------------------------------------------------------------
# 3. ROC curves of the reference predictors on the calibration slice
# --------------------------------------------------------------------------
PREDICTORS = [
    ("CADD", "CADD.score", "+"),
    ("aGVD", "aGVGD.diff", "-"),
    ("phyloP", "phyloP (mammalian)", "+"),
    ("PolyPhen-2", "polyphen2", "+"),
    ("SIFT", "sift", "-"),
]
roc_lines = []
roc_out = {}
for name, col, direction in PREDICTORS:
    vals = pd.to_numeric(sub[col], errors="coerce").to_numpy(dtype=float)
    keep = ~np.isnan(vals)
    s, yy = vals[keep], y[keep]
    oriented = s if direction == "+" else -s
    fpr, tpr, _ = roc_curve(yy, oriented)
    pts = " ".join(f"({fpr[i]:.4f},{tpr[i]:.4f})" for i in range(len(fpr)))
    roc_lines.append(f"\\def\\roc{name.replace('-', '')}{{{pts}}}")
    auc = float(pd.DataFrame({"y": yy, "s": oriented})
                .assign(rank=lambda d: d["s"].rank(method="average"))
                .pipe(lambda d: (d.loc[d["y"] == 1, "rank"].sum()
                                 - d.loc[d["y"] == 1, "rank"].count()
                                 * (d.loc[d["y"] == 1, "rank"].count() + 1) / 2)
                      / (d.loc[d["y"] == 1, "rank"].count()
                         * d.loc[d["y"] == 0, "rank"].count())))
    roc_out[name] = {"auroc": auc, "n": int(keep.sum())}
emit("ROC curves of the reference predictors on the calibration slice",
     "\n".join(roc_lines))
out["roc"] = roc_out

# --------------------------------------------------------------------------
# 4. Window construction: calibration 8192 vs endpoint 8193
# --------------------------------------------------------------------------
with gzip.open(FASTA_GZ, "rt") as h:
    rec = next(SeqIO.parse(h, "fasta"))
hg19 = str(rec.seq).upper()
c = int(pos_sub[0]) - 1
cal = hg19[c - HALF: c + HALF]
end = c + HALF + 1
dep = hg19[c - HALF: end]
out["calibration_window_length"] = len(cal)
out["endpoint_window_length"] = len(dep)
out["endpoint_equals_calibration_plus_one"] = bool(dep == cal + dep[-1])
out["variant_offset_calibration"] = c - (c - HALF)
out["variant_offset_endpoint"] = c - (c - HALF)

# --------------------------------------------------------------------------
# 5. Confidence heuristic, recomputed from the source constants
# --------------------------------------------------------------------------
TAU = -0.0009178519
SIG_LOF = 0.0015140239
SIG_FUNC = 0.0009016589
xs = np.linspace(-0.004, 0.002, 41)
lof = [(f"{x:.6f}", f"{min(1.0, abs(x - TAU) / SIG_LOF):.4f}") for x in xs
       if x <= TAU]
func = [(f"{x:.6f}", f"{min(1.0, abs(x - TAU) / SIG_FUNC):.4f}") for x in xs
        if x >= TAU]
emit("confidence heuristic sampled from the source constants",
     "\\def\\confLOF{" + " ".join(f"({a},{b})" for a, b in lof) + "}\n"
     "\\def\\confFUNC{" + " ".join(f"({a},{b})" for a, b in func) + "}\n"
     f"\\def\\confTau{{{TAU}}}\n\\def\\confSigLOF{{{SIG_LOF}}}\n"
     f"\\def\\confSigFUNC{{{SIG_FUNC}}}")
out["tau"] = TAU
out["sigma_lof"] = SIG_LOF
out["sigma_func"] = SIG_FUNC

dest = REPO / "docs/analysis/figure_data.tex"
dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
(REPO / "docs/analysis/h_figure_data.json").write_text(
    json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
print(f"wrote {dest}")
for k, v in out.items():
    print(f"  {k}: {v}")
