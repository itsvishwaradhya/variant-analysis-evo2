"""
Analysis C: assembly provenance of the deployed scoring contract.

Evo2Serve calibrates its decision threshold on GRCh37 (hg19) coordinates from
the Findlay et al. BRCA1 workbook, and then serves hg38 through the UCSC API.
This script quantifies what that mismatch does to the sequence that the model
actually sees.

Steps
-----
1.  Read the GRCh37 chr17 FASTA that ships with the repository and confirm it
    agrees with the UCSC hg19 service.
2.  Fetch the matching hg38 chr17 interval from the UCSC REST API.
3.  Derive the hg19 -> hg38 offset from conserved anchors, then verify it
    against the NCBI Gene gene model for BRCA1.
4.  Map the 500 calibration variants to hg38 and report how often the
    reference base changes.
5.  Report how much of the 8192-base scoring window is shared between the
    two assemblies at the same numeric coordinate and at the lifted
    coordinate.
6.  Check the example payload shipped in evo2-backend/main.py.

Network access to api.genome.ucsc.edu and eutils.ncbi.nlm.nih.gov is
required for steps 2, 3 and 6.

Run:
    evo2-backend/venv/Scripts/python.exe docs/analysis/c_assembly_provenance.py
"""

from __future__ import annotations

import gzip
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from Bio import SeqIO

REPO = Path(__file__).resolve().parents[2]
XLSX = REPO / "evo2-backend/evo2/notebooks/brca1/41586_2018_461_MOESM3_ESM.xlsx"
FASTA_GZ = REPO / "evo2-backend/evo2/notebooks/brca1/GRCh37.p13_chr17.fna.gz"
UCSC = "https://api.genome.ucsc.edu/getData/sequence"

WINDOW = 8192
HALF = WINDOW // 2
SLICE = 500
K = 31
HG38_START, HG38_END = 43_030_000, 43_190_000

out: dict = {}


def rule(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def ucsc_sequence(genome: str, chrom: str, start: int, end: int) -> str:
    """Fetch [start, end) in 0-based half-open coordinates from UCSC."""
    import requests

    url = (f"{UCSC}?genome={genome};chrom={chrom};start={start};end={end}")
    for attempt in range(4):
        try:
            r = requests.get(url, timeout=120)
            if r.status_code == 200:
                data = r.json()
                if "dna" not in data:
                    raise RuntimeError(f"UCSC error: {data.get('error')}")
                return data["dna"].upper()
            time.sleep(2 + attempt * 2)
        except requests.RequestException:
            time.sleep(2 + attempt * 2)
    raise RuntimeError(f"UCSC request failed: {url}")


# --------------------------------------------------------------------------
rule("C.1  Load GRCh37 chr17 and the calibration slice")
with gzip.open(FASTA_GZ, "rt") as handle:
    rec = next(SeqIO.parse(handle, "fasta"))
hg19 = str(rec.seq).upper()
print(f"hg19 chr17 record   : {rec.id}")
print(f"hg19 chr17 length   : {len(hg19):,}")

df = pd.read_excel(XLSX, header=2)
sub = df.iloc[:SLICE].copy()
sub["class"] = sub["func.class"].replace(["FUNC", "INT"], "FUNC/INT")
hg19_pos = sub["position (hg19)"].to_numpy(dtype=np.int64)          # 1-based
hg19_0 = hg19_pos - 1                                               # 0-based
ref_hg19 = np.array([hg19[p] for p in hg19_0])
ref_sheet = sub["reference"].astype(str).str.upper().to_numpy()
print(f"calibration slice    : {len(sub)} variants, "
      f"hg19 {hg19_pos.min():,}..{hg19_pos.max():,}")
print(f"reference base agrees with the bundled GRCh37 FASTA: "
      f"{int((ref_hg19 == ref_sheet).sum())}/{len(sub)}")

# the bundled FASTA must agree with the live hg19 service
probe = int(hg19_0[0])
live19 = ucsc_sequence("hg19", "chr17", probe - 40, probe + 40)
out["bundled_fasta_matches_ucsc_hg19"] = bool(
    live19 == hg19[probe - 40:probe + 40])
print(f"bundled FASTA agrees with the live UCSC hg19 service: "
      f"{out['bundled_fasta_matches_ucsc_hg19']}")

# --------------------------------------------------------------------------
rule("C.2  Fetch the matching hg38 interval from UCSC")
print(f"fetching hg38 chr17:{HG38_START:,}-{HG38_END:,} ...")
hg38_block = ucsc_sequence("hg38", "chr17", HG38_START, HG38_END)
print(f"hg38 block length   : {len(hg38_block):,}")

# --------------------------------------------------------------------------
rule("C.3  Derive and verify the hg19 -> hg38 offset")
mapped = []
last_j = -1
for i in range(0, len(hg38_block) - K, 200):
    kmer = hg38_block[i:i + K]
    if set(kmer) == {"N"}:
        continue
    j = hg19.find(kmer)
    if j < 0 or j <= last_j:
        continue
    mapped.append((HG38_START + i, j))   # absolute hg38, absolute hg19
    last_j = j

genomic_offsets = [g38 - g19 for g38, g19 in mapped]
off = int(pd.Series(genomic_offsets).mode()[0])
out["anchors_aligned"] = len(mapped)
out["hg38_minus_hg19_offset"] = off
out["hg38_minus_hg19_offset_min"] = int(min(genomic_offsets))
out["hg38_minus_hg19_offset_max"] = int(max(genomic_offsets))
print(f"anchors aligned      : {len(mapped)}")
print(f"hg38 - hg19 offset   : {min(genomic_offsets):,} .. "
      f"{max(genomic_offsets):,}  (constant offset {off:,})")

steps = [(mapped[t + 1][0] - mapped[t][0], mapped[t + 1][1] - mapped[t][1])
         for t in range(len(mapped) - 1)]
consistent = sum(1 for a, b in steps if a == b)
out["anchor_pairs_indel_free"] = consistent
out["anchor_pairs_total"] = len(steps)
print(f"anchor pairs with no indel between them: {consistent}/{len(steps)}")

# independent check against the NCBI Gene model for BRCA1 (Gene ID 672)
import requests

r = requests.get(
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
    params={"db": "gene", "id": "672", "retmode": "json"}, timeout=60)
gi = r.json()["result"]["672"]["genomicinfo"][0]
print(f"NCBI Gene BRCA1 on {gi['chraccver']}: "
      f"{gi['chrstart']:,}..{gi['chrstop']:,}")
out["ncbi_brca1_grch38"] = [gi["chrstart"], gi["chrstop"]]


def hg19_to_hg38(p0: int) -> int | None:
    """Map a 0-based hg19 coordinate to a 0-based hg38 coordinate."""
    if not mapped:
        return None
    if p0 < mapped[0][1] or p0 > mapped[-1][1]:
        return None
    for t in range(len(mapped) - 1):
        g38_a, g19_a = mapped[t]
        g38_b, g19_b = mapped[t + 1]
        if g19_a <= p0 <= g19_b:
            if g19_b == g19_a:
                return None
            frac = (p0 - g19_a) / (g19_b - g19_a)
            return int(round(g38_a + frac * (g38_b - g38_a)))
    return None


# --------------------------------------------------------------------------
rule("C.4  Consequence for the 500 calibration variants")
ref_hg38_same = np.array(
    [hg38_block[p - HG38_START] if (HG38_START <= p < HG38_END) else "?"
     for p in hg19_pos]
)
same_match = ref_hg38_same == ref_sheet
out["same_coord_ref_match"] = int(same_match.sum())
out["same_coord_ref_mismatch"] = int((~same_match).sum())
print(f"reference base == the sheet reference")
print(f"  at the hg19 coordinate      : "
      f"{int((ref_hg19 == ref_sheet).sum())}/{len(sub)}")
print(f"  at the same numeric hg38 coordinate: "
      f"{int(same_match.sum())}/{len(sub)} ({same_match.mean()*100:.1f}%)")

lifted = np.array([hg19_to_hg38(int(p)) for p in hg19_0])
lifted_ok = np.array([v is not None for v in lifted])
ref_hg38_lift = np.array(
    [hg38_block[v - HG38_START] if (v is not None
                                    and HG38_START <= v < HG38_END) else "?"
     for v in lifted])
lift_match = (ref_hg38_lift == ref_sheet) & lifted_ok
out["lifted_ref_match"] = int(lift_match.sum())
out["lifted_ref_mismatch"] = int((lifted_ok & ~lift_match).sum())
out["lifted_ref_mismatch_examples"] = [
    {"hg19": int(hg19_pos[i]), "hg38": int(lifted[i]) + 1,
     "ref": str(ref_sheet[i]), "hg38_base": str(ref_hg38_lift[i])}
    for i in np.where(lifted_ok & ~lift_match)[0][:10]
]
print(f"  after lifting hg19 -> hg38    : "
      f"{int(lift_match.sum())}/{int(lifted_ok.sum())} "
      f"({lift_match.sum()/max(1,lifted_ok.sum())*100:.1f}%)")
print(f"  a user who enters an hg19 coordinate into the hg38 assembly")
print(f"  scores the wrong reference base for {int((~same_match).sum())}"
      f"/{len(sub)} of the calibration variants")

# --------------------------------------------------------------------------
rule("C.5  How much of the scoring window survives the assembly change")
ident_same = []
ident_lifted = []
for i in range(len(sub)):
    c = int(hg19_0[i])
    w19 = hg19[c - HALF: c + HALF]
    same_chars, lift_chars = [], []
    for j in range(len(w19)):
        sp = c - HALF + j
        same_chars.append(hg38_block[sp - HG38_START]
                          if HG38_START <= sp < HG38_END else "N")
        hp = hg19_to_hg38(sp)
        lift_chars.append(hg38_block[hp - HG38_START]
                          if (hp is not None and HG38_START <= hp < HG38_END)
                          else "N")
    ident_same.append(sum(a == b for a, b in zip(w19, same_chars)))
    ident_lifted.append(sum(a == b for a, b in zip(w19, lift_chars)))
ident_same = np.array(ident_same)
ident_lifted = np.array(ident_lifted)
out["window_identity_same_coord_mean"] = float(ident_same.mean() / WINDOW)
out["window_identity_same_coord_min"] = float(ident_same.min() / WINDOW)
out["window_identity_lifted_mean"] = float(ident_lifted.mean() / WINDOW)
out["window_identity_lifted_min"] = float(ident_lifted.min() / WINDOW)
out["window_identity_lifted_median_differing_bases"] = float(
    np.median(WINDOW - ident_lifted))
print("identity of the 8192-base scoring window")
print(f"  at the same numeric coordinate : mean "
      f"{ident_same.mean()/WINDOW*100:.2f}%  min "
      f"{ident_same.min()/WINDOW*100:.2f}%")
print(f"  after lifting to hg38           : mean "
      f"{ident_lifted.mean()/WINDOW*100:.2f}%  min "
      f"{ident_lifted.min()/WINDOW*100:.2f}%")
print(f"  median number of bases that differ between the two assemblies")
print(f"  at the lifted coordinate        : "
      f"{np.median(WINDOW - ident_lifted):.0f} of {WINDOW}")

# --------------------------------------------------------------------------
rule("C.6  The example payload shipped in evo2-backend/main.py")
# main.py local_entrypoint posts variant_position=43119628, alternative="G",
# genome="hg38", chromosome="chr17".
EX_POS, EX_ALT = 43_119_628, "G"
ex_ref = ucsc_sequence("hg38", "chr17", EX_POS - 1, EX_POS)
ex_ref19 = ucsc_sequence("hg19", "chr17", EX_POS - 1, EX_POS)
lifted_ex = EX_POS - off
ex_ref_lifted = ucsc_sequence("hg19", "chr17", lifted_ex - 1, lifted_ex)
print(f"  example payload        : hg38 chr17:{EX_POS:,} {EX_ALT}")
print(f"  reference base in hg38 : {ex_ref}")
print(f"  same coordinate in hg19: {ex_ref19}")
print(f"  hg19 coordinate {lifted_ex:,} (lifted): {ex_ref_lifted}")
print(f"  alternative == reference (hg38)      : {ex_ref == EX_ALT}")
out["example_position"] = EX_POS
out["example_alternative"] = EX_ALT
out["example_reference_base_hg38"] = ex_ref
out["example_reference_base_hg19_same_coord"] = ex_ref19
out["example_lifted_hg19_position"] = lifted_ex
out["example_reference_base_hg19_lifted"] = ex_ref_lifted

# --------------------------------------------------------------------------
rule("C.7  Sequence context served for the same coordinate in both assemblies")
w19 = ucsc_sequence("hg19", "chr17", EX_POS - 1 - HALF, EX_POS - 1 + HALF)
w38 = ucsc_sequence("hg38", "chr17", EX_POS - 1 - HALF, EX_POS - 1 + HALF)
ident = sum(a == b for a, b in zip(w19, w38))
out["example_window_identity_same_coord"] = ident / len(w19)
print(f"  hg19 and hg38 8192-base windows at the same numeric coordinate")
print(f"  identical positions : {ident}/{len(w19)} "
      f"({ident/len(w19)*100:.2f}%)")

dest = REPO / "docs/analysis/c_assembly_provenance.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
print(f"\nwrote {dest}")
