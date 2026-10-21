"""
Analysis A and B: characterisation of the BRCA1 saturation-genome-editing
calibration slice used by Evo2Serve, and verification of the two window
construction rules implemented in the repository.

The script reads only files that are checked into the repository, so every
number it prints is reproducible on a CPU without a GPU or network access.

Run:
    evo2-backend/venv/Scripts/python.exe docs/analysis/a_dataset_characterization.py
"""

from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from Bio import SeqIO

REPO = Path(__file__).resolve().parents[2]
XLSX = REPO / "evo2-backend/evo2/notebooks/brca1/41586_2018_461_MOESM3_ESM.xlsx"
FASTA_GZ = REPO / "evo2-backend/evo2/notebooks/brca1/GRCh37.p13_chr17.fna.gz"

WINDOW = 8192
HALF = WINDOW // 2
SLICE = 500

out: dict = {}


def rule(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


# --------------------------------------------------------------------------
rule("A.1  Workbook structure")
# --------------------------------------------------------------------------
df = pd.read_excel(XLSX, header=2)
out["workbook_rows"] = int(len(df))
out["workbook_columns"] = list(map(str, df.columns))
print(f"rows in workbook (header=2): {len(df)}")
print(f"columns: {list(map(str, df.columns))}")

keep = [
    "chromosome",
    "position (hg19)",
    "reference",
    "alt",
    "function.score.mean",
    "func.class",
]
missing = [c for c in keep if c not in df.columns]
print(f"columns required by run_brca1_analysis present: {not missing}")
if missing:
    print(f"  MISSING: {missing}")
    sys.exit(1)

df = df[keep].rename(
    columns={
        "chromosome": "chrom",
        "position (hg19)": "pos",
        "reference": "ref",
        "alt": "alt",
        "function.score.mean": "score",
        "func.class": "class",
    }
)
df["class"] = df["class"].replace(["FUNC", "INT"], "FUNC/INT")
out["raw_class_counts"] = {
    str(k): int(v) for k, v in df["class"].value_counts().items()
}
print(f"raw class counts (whole workbook): {out['raw_class_counts']}")

# --------------------------------------------------------------------------
rule("A.2  The 500-row calibration slice")
# --------------------------------------------------------------------------
sub = df.iloc[:SLICE].copy()
out["slice_rows"] = int(len(sub))
out["slice_class_counts"] = {
    str(k): int(v) for k, v in sub["class"].value_counts().items()
}
lof_n = int((sub["class"] == "LOF").sum())
func_n = int((sub["class"] == "FUNC/INT").sum())
out["slice_lof_n"] = lof_n
out["slice_func_n"] = func_n
out["slice_positive_fraction"] = lof_n / len(sub)
print(f"slice rows                : {len(sub)}")
print(f"slice class counts         : {out['slice_class_counts']}")
print(f"positive (LOF) fraction    : {lof_n}/{len(sub)} = {lof_n/len(sub):.4f}")
print(f"negative (FUNC/INT) count  : {func_n}")
print(f"slice position range (hg19): {int(sub['pos'].min())} .. {int(sub['pos'].max())}")
out["slice_pos_min"] = int(sub["pos"].min())
out["slice_pos_max"] = int(sub["pos"].max())
print(f"slice chromosomes          : {sorted(set(sub['chrom'].astype(str)))}")
out["slice_chroms"] = sorted(set(sub["chrom"].astype(str)))

# class balance inside each half of the slice (checks for ordering artefacts)
half = len(sub) // 2
for i, part in enumerate([sub.iloc[:half], sub.iloc[half:]]):
    c = part["class"].value_counts()
    print(
        f"  slice half {i + 1} (rows {i*half}..{(i+1)*half - 1 if i == 0 else len(sub)-1}): "
        f"LOF={int(c.get('LOF', 0))} FUNC/INT={int(c.get('FUNC/INT', 0))}"
    )
out["slice_half_class_counts"] = [
    {
        "LOF": int(p["class"].value_counts().get("LOF", 0)),
        "FUNC/INT": int(p["class"].value_counts().get("FUNC/INT", 0)),
    }
    for p in (sub.iloc[:half], sub.iloc[half:])
]

# --------------------------------------------------------------------------
rule("A.3  Reference-sequence integrity against GRCh37 chr17")
# --------------------------------------------------------------------------
with gzip.open(FASTA_GZ, "rt") as handle:
    rec = next(SeqIO.parse(handle, "fasta"))
chr17 = str(rec.seq)
out["chr17_length"] = len(chr17)
out["chr17_id"] = rec.id
print(f"chr17 record id            : {rec.id}")
print(f"chr17 length               : {len(chr17):,}")

p0 = sub["pos"].to_numpy(dtype=np.int64) - 1  # 0-based
ref_from_fasta = np.array([chr17[p] for p in p0])
ref_from_sheet = sub["ref"].astype(str).str.upper().to_numpy()
alt_from_sheet = sub["alt"].astype(str).str.upper().to_numpy()

match = ref_from_fasta == ref_from_sheet
out["ref_base_matches_sheet"] = int(match.sum())
out["ref_base_mismatches"] = int((~match).sum())
out["ref_base_match_rate"] = float(match.mean())
print(f"reference base == sheet ref: {int(match.sum())}/{len(match)} "
      f"({match.mean() * 100:.2f}%)")
bad = np.where(~match)[0][:10]
if len(bad):
    print("  first mismatches (row, sheet_ref, fasta_base):")
    for i in bad:
        print(f"    row {i}: sheet={ref_from_sheet[i]} fasta={ref_from_fasta[i]}")

alt_is_single = np.array([len(a) == 1 and a in "ACGT" for a in alt_from_sheet])
out["alt_single_acgt"] = int(alt_is_single.sum())
out["alt_not_single_acgt"] = int((~alt_is_single).sum())
print(f"alt is a single A/C/G/T    : {int(alt_is_single.sum())}/{len(alt_is_single)}")
alt_ne_ref = alt_from_sheet != ref_from_sheet
out["alt_differs_from_ref"] = int(alt_ne_ref.sum())
print(f"alt differs from reference : {int(alt_ne_ref.sum())}/{len(alt_ne_ref)}")
diff = np.where(alt_ne_ref & ~alt_is_single)[0][:10]
for i in diff:
    print(f"    row {i}: ref={ref_from_sheet[i]} alt={alt_from_sheet[i]}")

# --------------------------------------------------------------------------
rule("A.4  Reference-window construction and de-duplication")
# --------------------------------------------------------------------------
# Exactly the slicing rule used by run_brca1_analysis in evo2-backend/main.py
starts = np.maximum(0, p0 - HALF)
ends = np.minimum(len(chr17), p0 + HALF)
lengths = ends - starts
out["calib_window_len_min"] = int(lengths.min())
out["calib_window_len_max"] = int(lengths.max())
out["calib_window_len_mode"] = int(pd.Series(lengths).mode()[0])
print(f"calibration window length   : min={lengths.min()} max={lengths.max()} "
      f"mode={pd.Series(lengths).mode()[0]}")

ref_seqs: list[str] = []
seen: dict[str, int] = {}
offsets: list[int] = []
gc: list[float] = []
n_count = 0
for i in range(len(sub)):
    s, e = int(starts[i]), int(ends[i])
    w = chr17[s:e]
    offsets.append(p0[i] - s)
    gc.append((w.count("G") + w.count("C")) / len(w))
    n_count += w.count("N")
    if w not in seen:
        seen[w] = len(ref_seqs)
        ref_seqs.append(w)

out["calib_unique_ref_windows"] = len(ref_seqs)
out["calib_dedup_ratio"] = len(ref_seqs) / len(sub)
out["calib_variant_offset_unique"] = sorted(set(offsets))
out["calib_gc_mean"] = float(np.mean(gc))
out["calib_gc_min"] = float(np.min(gc))
out["calib_gc_max"] = float(np.max(gc))
out["calib_N_bases"] = int(n_count)
print(f"unique reference windows    : {len(ref_seqs)} of {len(sub)} variants "
      f"(de-duplication factor {len(ref_seqs)/len(sub):.3f})")
print(f"variant offset in window    : {sorted(set(offsets))}")
print(f"window GC content           : mean={np.mean(gc):.4f} "
      f"min={np.min(gc):.4f} max={np.max(gc):.4f}")
print(f"ambiguous (N) bases in slice: {n_count}")

# --------------------------------------------------------------------------
rule("A.5  Deployed endpoint window vs calibration window")
# --------------------------------------------------------------------------
# Endpoint rule (evo2-backend/main.py, get_genome_sequence):
#     start = max(0, position - 1 - HALF) ; end = position - 1 + HALF + 1
# Calibration rule (run_brca1_analysis):
#     start = max(0, p - HALF)            ; end = min(len, p + HALF)   with p = pos-1
interior = (p0 - HALF >= 0) & (p0 + HALF <= len(chr17))
out["interior_slice_rows"] = int(interior.sum())
ep_len = (p0 + HALF + 1) - np.maximum(0, p0 - HALF)
out["endpoint_window_len_min"] = int(ep_len.min())
out["endpoint_window_len_max"] = int(ep_len.max())
print(f"interior variants in slice  : {int(interior.sum())}/{len(sub)}")
print(f"endpoint window length      : min={ep_len.min()} max={ep_len.max()} "
      f"(interior value {ep_len[interior][0]})")
print(f"calibration window length   : {lengths[interior][0]} (interior)")

# Compare the two windows base by base at every interior position.
identical = 0
prefix_match = 0
extra_downstream = 0
for i in np.where(interior)[0]:
    p = int(p0[i])
    cal = chr17[p - HALF: p + HALF]              # 8192 bases
    dep = chr17[p - HALF: p + HALF + 1]          # 8193 bases
    if cal == dep[: len(cal)]:
        prefix_match += 1
    if dep == cal + dep[-1]:
        extra_downstream += 1
    if cal == dep:
        identical += 1

out["endpoint_vs_calib_identical"] = identical
out["endpoint_is_calib_plus_one_3prime"] = extra_downstream
out["endpoint_shares_calib_prefix"] = prefix_match
n_int = int(interior.sum())
print(f"endpoint window == calibration window          : {identical}/{n_int}")
print(f"endpoint window == calibration + 1 downstream 3' base: "
      f"{extra_downstream}/{n_int}")
print(f"endpoint window shares calibration prefix      : {prefix_match}/{n_int}")

# Offsets of the variant inside each window
ep_off = p0 - np.maximum(0, p0 - HALF)
cal_off = p0 - np.maximum(0, p0 - HALF)
out["endpoint_variant_offset_unique"] = sorted(set(ep_off.tolist()))
out["calib_variant_offset_unique"] = sorted(set(cal_off.tolist()))
print(f"endpoint variant offset      : {sorted(set(ep_off.tolist()))}")
print(f"calibration variant offset   : {sorted(set(cal_off.tolist()))}")
print(f"bases 5' of variant (endpoint) : {int(ep_off[interior][0])}")
print(f"bases 3' of variant (endpoint) : {int(ep_len[interior][0] - 1 - ep_off[interior][0])}")
print(f"bases 5' of variant (calib)    : {int(cal_off[interior][0])}")
print(f"bases 3' of variant (calib)    : {int(lengths[interior][0] - 1 - cal_off[interior][0])}")

# --------------------------------------------------------------------------
rule("A.6  De-duplication in the deployed online endpoint")
# --------------------------------------------------------------------------
# analyze_variant() calls score_sequences twice per request: once for the
# reference window and once for the edited window.  The offline calibration
# routine de-duplicates references.  Count the forward passes for both paths.
out["online_forward_passes_per_request"] = 2
out["offline_forward_passes_slice"] = len(ref_seqs) + len(sub)
out["offline_forward_passes_naive"] = 2 * len(sub)
out["offline_dedup_saving_pct"] = 100.0 * (
    1 - (len(ref_seqs) + len(sub)) / (2 * len(sub))
)
print(f"online endpoint passes/req    : 2 "
      f"({len(sub)} refs re-scored for every request, no cross-request cache)")
print(f"offline calibration passes    : {len(ref_seqs)} reference + "
      f"{len(sub)} variant = {len(ref_seqs) + len(sub)}")
print(f"offline without de-duplication: {2 * len(sub)} "
      f"(saved {out['offline_dedup_saving_pct']:.1f}%)")

# --------------------------------------------------------------------------
rule("A.7  Threshold constants: consistency arithmetic")
# --------------------------------------------------------------------------
TAU = -0.0009178519
SIG_LOF = 0.0015140239
SIG_FUNC = 0.0009016589
# A no-op edit (alternative == reference) produces an identical sequence, so the
# two model scores are equal and delta is exactly zero.
conf_noop = min(1.0, abs(0.0 - TAU) / SIG_FUNC)
out["tau"] = TAU
out["sigma_lof"] = SIG_LOF
out["sigma_func"] = SIG_FUNC
out["confidence_noop_snv"] = conf_noop
out["confidence_noop_indel"] = min(1.0, abs(0.0 - TAU) / SIG_LOF)
print(f"tau                          : {TAU}")
print(f"sigma_LOF / sigma_FUNC       : {SIG_LOF} / {SIG_FUNC}")
print(f"confidence for delta == 0 (SNV path, sigma_FUNC)  : {conf_noop:.6f}")
print(f"confidence for delta == 0 (indel path, sigma_LOF) : "
      f"{min(1.0, abs(0.0 - TAU) / SIG_LOF):.6f}")
print(f"tau / sigma_LOF  = {abs(TAU)/SIG_LOF:.4f} sigma units")
print(f"tau / sigma_FUNC = {abs(TAU)/SIG_FUNC:.4f} sigma units")

# --------------------------------------------------------------------------
rule("A.8  Assembly provenance")
# --------------------------------------------------------------------------
print("calibration data assembly : GRCh37 (hg19)  [position (hg19) column]")
print("deployed default assembly : hg38 (UCSC)    [frontend assembly selector]")
print("tau is applied to both assemblies without re-calibration.")

dest = REPO / "docs/analysis/a_dataset_characterization.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
print(f"\nwrote {dest}")
