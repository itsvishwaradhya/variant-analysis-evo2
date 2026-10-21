"""
Analysis G: executable test of the deployed scoring contract.

The endpoint's scoring logic lives in two functions of
evo2-backend/main.py: get_genome_sequence(), which builds the context
window, and analyze_variant(), which edits the window and turns the two
model scores into a label and a confidence value.

This script imports those two functions unchanged and exercises them with a
stand-in scorer, so that the behaviour of the contract can be checked
without an H100.  The stand-in is a third-order Markov background model
estimated from the GRCh37 chr17 FASTA that ships with the repository, scored
with the same mean reduction that Evo 2's score_sequences applies.  The
stand-in is not Evo 2 and its scores are not Evo 2 scores; what the test
checks is the arithmetic of the deployed contract, which is independent of
the model that supplies the two log-likelihoods.

Run:
    evo2-backend/venv/Scripts/python.exe docs/analysis/g_scoring_contract.py
"""

from __future__ import annotations

import gzip
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from Bio import SeqIO

REPO = Path(__file__).resolve().parents[2]
MAIN_PY = REPO / "evo2-backend/main.py"
FASTA_GZ = REPO / "evo2-backend/evo2/notebooks/brca1/GRCh37.p13_chr17.fna.gz"

spec = importlib.util.spec_from_file_location("evo2_main", MAIN_PY)
mod = importlib.util.module_from_spec(spec)
sys.modules["evo2_main"] = mod
spec.loader.exec_module(mod)

analyze_variant = mod.analyze_variant
get_genome_sequence = mod.get_genome_sequence
TAU = mod.SNV_THRESHOLD
SIG_LOF = mod.SNV_LOF_STD
SIG_FUNC = mod.SNV_FUNC_STD

out: dict = {}


def rule(t: str) -> None:
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


# --------------------------------------------------------------------------
# Third-order Markov background model, scored with a mean reduction.
# --------------------------------------------------------------------------
with gzip.open(FASTA_GZ, "rt") as h:
    rec = next(SeqIO.parse(h, "fasta"))
chr17 = str(rec.seq).upper()

ORDER = 3
counts: dict = {}
for i in range(0, 200_000, 1):
    k = chr17[i:i + ORDER]
    if len(k) < ORDER:
        break
    c = chr17[i + ORDER]
    counts.setdefault(k, {})
    counts[k][c] = counts.get(k, {}).get(c, 0) + 1
alpha = 0.5
logp: dict = {}
for k, d in counts.items():
    tot = sum(d.values()) + 4 * alpha
    logp[k] = {c: float(np.log((d.get(c, 0) + alpha) / tot)) for c in "ACGT"}


class MarkovScorer:
    """Stand-in for Evo 2: returns a mean per-base log-likelihood in nats."""

    def __init__(self):
        self.calls = 0
        self.lengths = []

    def score_sequences(self, seqs):
        self.calls += len(seqs)
        out = []
        for s in seqs:
            self.lengths.append(len(s))
            total = 0.0
            for i in range(ORDER, len(s)):
                k = s[i - ORDER:i]
                c = s[i]
                total += logp.get(k, {}).get(c, np.log(0.25))
            out.append(total / max(1, len(s) - ORDER))
        return out


# --------------------------------------------------------------------------
rule("G.1  A substitution that changes the base")
scorer = MarkovScorer()
WINDOW = 8192
pos = 41_271_645                       # hg19 BRCA1, from the workbook region
center = pos
start = max(0, center - 1 - WINDOW // 2)
end = center - 1 + WINDOW // 2 + 1
window = chr17[start:end]
print(f"window length            : {len(window)}")
print(f"variant offset in window : {center - 1 - start}")

ref = window[center - 1 - start]
alt = next(c for c in "ACGT" if c != ref)
res = analyze_variant(
    relative_pos_in_window=center - 1 - start,
    reference=ref, alternative=alt, window_seq=window, model=scorer,
    variant_type="snv",
)
print(f"reference base           : {ref} -> {alt}")
print(f"delta score              : {res['delta_score']:.8f}")
print(f"prediction               : {res['prediction']}")
print(f"confidence               : {res['classification_confidence']:.6f}")
print(f"threshold used           : {res['threshold_used']}")
print(f"provisional              : {res['provisional_prediction']}")
out["snv"] = res
out["snv_delta_magnitude"] = abs(res["delta_score"])

# --------------------------------------------------------------------------
rule("G.2  A substitution that does not change the base")
scorer2 = MarkovScorer()
res_noop = analyze_variant(
    relative_pos_in_window=center - 1 - start,
    reference=ref, alternative=ref, window_seq=window, model=scorer2,
    variant_type="snv",
)
print(f"reference base           : {ref} -> {ref} (identical)")
print(f"delta score              : {res_noop['delta_score']!r}")
print(f"prediction               : {res_noop['prediction']}")
print(f"confidence               : {res_noop['classification_confidence']:.6f}")
print(f"forward passes           : {scorer2.calls}")
print()
print("  The edited window is byte-identical to the reference window, so the")
print("  two scores are equal and the difference is exactly zero.  A zero")
print("  difference lies above the threshold and therefore receives the")
print("  benign label, with a confidence of")
print(f"  min(1, |0 - tau| / sigma_FUNC) = "
      f"{min(1.0, abs(0.0 - TAU) / SIG_FUNC):.6f}.")
out["noop"] = res_noop
out["noop_confidence"] = res_noop["classification_confidence"]
out["noop_delta_is_exactly_zero"] = bool(res_noop["delta_score"] == 0.0)
out["noop_prediction"] = res_noop["prediction"]

# --------------------------------------------------------------------------
rule("G.3  A deletion changes the length of the scored sequence")
scorer3 = MarkovScorer()
n = 3
res_del = analyze_variant(
    relative_pos_in_window=center - 1 - start,
    reference=window[center - 1 - start:center - 1 - start + n],
    alternative=None, window_seq=window, model=scorer3,
    variant_type="deletion", deletion_length=n,
)
print(f"deletion length          : {n}")
print(f"scored sequence lengths  : {scorer3.lengths}")
print(f"reference sequence length: {len(window)} -> {len(window) - n}")
print(f"delta score              : {res_del['delta_score']:.8f}")
print(f"prediction               : {res_del['prediction']}")
print(f"confidence               : {res_del['classification_confidence']:.6f}")
print(f"provisional              : {res_del['provisional_prediction']}")
print()
print("  The two mean-reduced scores are averaged over different numbers of")
print("  positions, so the difference mixes a change in sequence content with")
print("  a change in the number of terms over which the mean is taken.")
out["deletion"] = res_del
out["deletion_scored_lengths"] = scorer3.lengths

# --------------------------------------------------------------------------
rule("G.4  An insertion lengthens the scored sequence")
scorer4 = MarkovScorer()
res_ins = analyze_variant(
    relative_pos_in_window=center - 1 - start,
    reference=ref, alternative=None, window_seq=window, model=scorer4,
    variant_type="insertion", inserted_sequence="GGC",
)
print(f"scored sequence lengths  : {scorer4.lengths}")
print(f"delta score              : {res_ins['delta_score']:.8f}")
print(f"prediction               : {res_ins['prediction']}")
print(f"confidence               : {res_ins['classification_confidence']:.6f}")
out["insertion"] = res_ins

# --------------------------------------------------------------------------
rule("G.5  Forward passes per request")
sc = MarkovScorer()
analyze_variant(relative_pos_in_window=center - 1 - start, reference=ref,
                alternative=alt, window_seq=window, model=sc,
                variant_type="snv")
print(f"forward passes for one request: {sc.calls}")
print(f"  the reference window is re-scored on every request; the offline")
print(f"  calibration routine de-duplicates reference windows instead.")
out["forward_passes_per_request"] = sc.calls

dest = REPO / "docs/analysis/g_scoring_contract.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
print(f"\nwrote {dest}")
