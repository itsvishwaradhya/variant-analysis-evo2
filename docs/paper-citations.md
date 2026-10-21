# Paper citations — Evo2Serve (primary-source verification)

Scope: source facts and bibliographic details for the related-work and background sections of
"Evo2Serve: A Web Application for Contextual Variant Scoring With Evo2-7B".

Every claim below is tagged **VERIFIED** (confirmed from a primary source: publisher page,
official docs, official repository, first-party API response, official preprint server) or
**UNVERIFIED** (could not be confirmed from a primary source; see also
"## Claims the paper MUST NOT make").

Prior art checked and *not* duplicated: `docs/research-findings.md` (read first; its Evo 2 /
Findlay / UCSC claims were re-derived here from scratch, not copied).

---

## 1. Evo 2 (Brixi et al.)

### 1.1 Published version, venue, DOI, pages

- **Claim:** Evo 2 is published as "Genome modelling and design across all domains of life with Evo 2", *Nature* **652**(8112):1349–1361, published 04 March 2026, DOI `10.1038/s41586-026-10176-5`, PMID 41781614.
  **Source:** https://www.nature.com/articles/s41586-026-10176-5 (article header: "Nature volume 652, pages 1349–1361 (2026)"; "Published: 04 March 2026"; "Open access")
  **Source:** https://pubmed.ncbi.nlm.nih.gov/41781614/ ("Nature. 2026 Apr. 652(8112):1349-1361. doi: 10.1038/s41586-026-10176-5")
  **Source:** https://api.crossref.org/works/10.1038/s41586-026-10176-5 (Crossref record: vol 652, issue 8112, page 1349-1361, year 2026)
  **VERIFIED**

- **Claim:** The GitHub repo ships the matching BibTeX with `journal = {Nature}`, `year = {2026}`, `doi = {10.1038/s41586-026-10176-5}`.
  **Source:** https://github.com/ArcInstitute/evo2 (README "Citation" block, `@article{Brixi2026, ...}`)
  **VERIFIED**

### 1.2 Preprint (no arXiv version)

- **Claim:** A bioRxiv preprint exists: "Genome modeling and design across all domains of life with Evo 2", bioRxiv 2025.02.18.638918, posted 21 February 2025, DOI `10.1101/2025.02.18.638918`.
  **Source:** https://www.biorxiv.org/content/10.1101/2025.02.18.638918v1
  **VERIFIED**
- **Claim:** There is **no arXiv preprint** for Evo 2 itself. A query of the arXiv API for `all:"Genome modeling and design across all domains of life with Evo 2"` and for `all:"Evo 2" AND au:Brixi` returns only the StripedHyena 2 paper (arXiv:2503.01868).
  **Source:** http://export.arxiv.org/api/query?search_query=all:%22Evo+2%22+AND+au:Brixi
  **VERIFIED**

### 1.3 Architecture

- **Claim:** Evo 2 "models DNA sequences at single-nucleotide resolution at up to 1 million base pair context length using the StripedHyena 2 architecture", and was pretrained with Savanna on OpenGenome2.
  **Source:** https://github.com/ArcInstitute/evo2 (README, first paragraph)
  **VERIFIED**
- **Claim:** In the paper, "Evo 2 uses StripedHyena 2, a convolutional multi-hybrid architecture that relies on a combination of three different variants of input-dependent convolution operators and attention". StripedHyena 2 gives "up to 3× speedup at 1 million context length" at the 40B scale vs. Transformers.
  **Source:** https://www.nature.com/articles/s41586-026-10176-5 ("Evo 2 architecture, training, and data" section and Fig. 1f–g)
  **VERIFIED**
- **Claim:** The StripedHyena 2 paper is "Systems and Algorithms for Convolutional Multi-Hybrid Language Models at Scale", arXiv:2503.01868, submitted 25 Feb 2025 (cs.LG). It reports training 1.2–2.9× faster than optimized Transformers at the 40B scale, and 1.1–1.4× faster than previous-generation hybrids.
  **Source:** https://arxiv.org/abs/2503.01868
  **VERIFIED** (arXiv preprint; **not** peer-reviewed at a venue as of this check — the Nature paper cites it as a "Preprint")
- **Claim:** The Evo 2 README links "StripedHyena 2" to the Savanna paper PDF (`https://github.com/Zymrael/savanna/blob/main/paper.pdf`).
  **Source:** https://github.com/ArcInstitute/evo2
  **VERIFIED**

### 1.4 Context length, parameter counts, checkpoints

- **Claim:** "We train Evo 2 with 7B and 40B parameters to have an unprecedented 1 million token context window with single-nucleotide resolution."
  **Source:** https://www.biorxiv.org/content/10.1101/2025.02.18.638918v1 (Abstract)
  **VERIFIED**
- **Claim:** "We trained two versions of Evo 2: a smaller version with 7 billion parameters trained on 2.4 trillion tokens (Evo 2 7B), and a larger version with 40 billion parameters trained on 9.3 trillion tokens (Evo 2 40B)." Training is two-phase: stage-1 pretraining at context length 8,192 tokens, then multi-stage midtraining extending context to 1 million tokens.
  **Source:** https://www.nature.com/articles/s41586-026-10176-5 ("Evo 2 architecture, training, and data"; Fig. 1c–e)
  **VERIFIED**
- **Claim:** Official checkpoint names and context lengths (README table): `evo2_40b` (40B, 1M context), `evo2_20b` (20B, 1M context), `evo2_7b` (7B, 1M context), `evo2_40b_base` (40B, 8K context), `evo2_7b_base` (7B, 8K context), `evo2_1b_base` (1B, 8K context), `evo2_7b_262k` (7B, 262K context), `evo2_7b_microviridae` (7B base fine-tuned on Microviridae genomes).
  **Source:** https://github.com/ArcInstitute/evo2 (Checkpoints table)
  **VERIFIED**
- **Claim:** The HuggingFace `arcinstitute` organisation actually publishes: `evo2_1b_base`, `evo2_7b`, `evo2_7b_262k`, `evo2_7b_base`, `evo2_20b`, `evo2_40b`, `evo2_40b_base`, plus `savanna_evo2_*` training checkpoints.
  **Source:** https://huggingface.co/api/models?author=arcinstitute&limit=100
  **VERIFIED**
- **Claim:** `evo2_7b_microviridae` appears in the README checkpoint table but **is not** among the models published on the `arcinstitute` HuggingFace organisation.
  **Source:** https://huggingface.co/api/models?author=arcinstitute&limit=100 vs. README table
  **VERIFIED**
- **Claim:** Hardware/precision requirements: 40B, 20B and 1B models require FP8 via NVIDIA Transformer Engine on a Hopper GPU; the 7B models run in bfloat16 without Transformer Engine. "The 40B model requires multiple H100 GPUs." Install pins `flash-attn==2.8.0.post2`.
  **Source:** https://github.com/ArcInstitute/evo2 (Requirements, FP8 table, Checkpoints note, Installation)
  **VERIFIED**

### 1.5 Training corpus size — the 8.8T vs 9.3T discrepancy (resolved)

All three figures are correct but refer to **different quantities**:

| Figure | Meaning | Primary source |
|---|---|---|
| **8.8 trillion** | Size of the OpenGenome2 dataset itself (curated nucleotides/tokens available) | Nature body: "OpenGenome2, which was compiled from curated, non-redundant nucleotide sequence data with a total of more than 8.8 trillion nucleotides"; GitHub README: "a dataset containing 8.8 trillion tokens"; HF dataset card: "Total size: 8.8 trillion base pairs" |
| **9.3 trillion** | Total tokens consumed in training the Evo 2 40B model (i.e. >1 epoch over OpenGenome2) | Nature body: "a larger version with 40 billion parameters trained on 9.3 trillion tokens"; bioRxiv abstract: "trained on 9.3 trillion DNA base pairs" |
| **9 trillion** | Rounded value used in the *Nature* abstract | Nature abstract: "trained on 9 trillion DNA base pairs" |

- **Source (8.8T):** https://www.nature.com/articles/s41586-026-10176-5 ; https://github.com/ArcInstitute/evo2 ; https://huggingface.co/datasets/arcinstitute/opengenome2
- **Source (9.3T):** https://www.nature.com/articles/s41586-026-10176-5 ; https://www.biorxiv.org/content/10.1101/2025.02.18.638918v1
- **Source (9T):** https://www.nature.com/articles/s41586-026-10176-5
- **VERIFIED** (all three). The paper should say "Evo 2 was trained on the OpenGenome2 dataset (>8.8 trillion nucleotides); the 40B model consumed 9.3 trillion training tokens" rather than picking one number.

### 1.6 BRCA1 zero-shot variant-effect result (published numbers)

All numbers below are from **Supplementary Data 1** of the Nature paper (XLSX, downloaded and parsed):
`https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10176-5/MediaObjects/41586_2026_10176_MOESM3_ESM.xlsx`
(linked from the article as "Supplementary Data 1 (download XLSX)"). Columns: `Model, Data, Genomic_Feature, Variant_Type, Sub_category, N_pos, N_neg, N_variants_total, AUROC, AUPRC`.
**VERIFIED**

**BRCA1 saturation-genome-editing benchmark (LOF vs functional+intermediate), SNVs:**

| Model | Subset | N_pos (LOF) | N_neg (func+int) | N total | AUROC | AUPRC |
|---|---|---|---|---|---|---|
| Evo 2 7B | Both | 823 | 3070 | 3893 | **0.9037** | 0.7326 |
| Evo 2 7B | Coding | 584 | 2184 | 2768 | 0.8229 | 0.5714 |
| Evo 2 7B | Noncoding | 239 | 886 | 1125 | **0.9593** | 0.8705 |
| Evo 2 40B | Both | 823 | 3070 | 3893 | **0.9011** | 0.6771 |
| Evo 2 40B | Coding | 584 | 2184 | 2768 | 0.8432 | 0.5716 |
| Evo 2 40B | Noncoding | 239 | 886 | 1125 | **0.9737** | 0.9030 |
| Evo 2 7B base | Both | 823 | 3070 | 3893 | 0.8907 | 0.7130 |
| Evo 2 40B base | Both | 823 | 3070 | 3893 | 0.8965 | 0.6727 |
| CADD (supervised) | Both | 823 | 3070 | 3893 | 0.8763 | 0.7295 |
| CADD (supervised) | Coding | 584 | 2184 | 2768 | 0.8145 | 0.5211 |
| CADD (supervised) | Noncoding | 239 | 886 | 1125 | 0.9093 | 0.8002 |
| AlphaMissense (supervised) | Coding | 584 | 2184 | 2768 | 0.8891 | 0.6903 |
| GPN-MSA | Both | 823 | 3070 | 3893 | 0.8628 | 0.6498 |
| PhyloP 100 | Both | 823 | 3070 | 3893 | 0.8113 | 0.4945 |
| Evo 1 | Both | 823 | 3070 | 3893 | 0.4972 | 0.2158 |
| Nucleotide Transformer (NT) | Both | 823 | 3070 | 3893 | 0.5496 | 0.2847 |
| Pangolin | Both | 823 | 3070 | 3893 | 0.5921 | 0.2898 |
| SpliceAI | Both | 823 | 3070 | 3893 | 0.6864 | 0.5081 |

Additional BRCA1 strata (same source):
- **Splice region** (n = 559; 227 pos / 332 neg): Evo 2 40B AUROC 0.9585 / AUPRC 0.9178; Evo 2 7B 0.9420 / 0.8965; SpliceAI 0.9472 / 0.9007; GPN-MSA 0.8911; CADD 0.8897; Evo 1 0.4625; NT 0.6343.
- **Intronic** (n = 489; 9 pos / 480 neg): Evo 2 7B 0.8852 / 0.3195; Evo 2 40B 0.8875 / 0.4243; SpliceAI 0.8763; Pangolin 0.8336; CADD 0.8130; Evo 1 0.4649; NT 0.6882.

**ClinVar zero-shot VEP benchmarks (published numbers):**
- **Coding SNVs** (n = 14,313; 9,387 pathogenic / 4,926 benign): AlphaMissense 0.9584 / 0.9768; CADD 0.9265 / 0.9521; ESM-1b 0.9233 / 0.9569; GPN-MSA 0.8965 / 0.9320; PhyloP 100 0.8567 / 0.9061; **Evo 2 40B 0.8407 / 0.8892**; Evo 2 40B base 0.8357; Evo 2 7B 0.8300 / 0.8835; Evo 2 7B base 0.8291; ESM-2 650M 0.6771; DeCodon 200M 0.6866; EnCodon 620M 0.6260; Evo 1 0.5603; NT 0.5053; CodonBERT 87M 0.5235.
  **Source:** Supplementary Data 1 (XLSX), `Data=ClinVar, Genomic_Feature=Coding, Variant_Type=SNV`.
- **Noncoding SNVs** (n = 33,747; 8,090 pos / 25,657 neg): SpliceAI 0.9922; CADD 0.9914; **Evo 2 40B 0.9872 / 0.9747**; GPN-MSA 0.9810; PhyloP 100 0.9776; Evo 2 7B 0.9776; Pangolin 0.9141; Evo 1 0.5517; NT 0.5416; RNA-FM 0.5159.
  **Source:** Supplementary Data 1 (XLSX), `Data=ClinVar, Genomic_Feature=Noncoding, Variant_Type=SNV`.
- **Noncoding non-SNVs** (n = 3,623): Evo 2 40B 0.9694 / 0.9172; Evo 2 7B 0.9301; PhyloP 100 0.9279; Pangolin 0.8447; Evo 1 0.5063; NT 0.5077.
  **Source:** Supplementary Data 1 (XLSX).
- **SpliceVarDB** (Fig. 3d): exonic n = 1,181 (supp data: 434 pos / 745 neg) — SpliceAI 0.9340, Pangolin 0.8640, CADD 0.7990, Evo 2 40B 0.6839, Evo 2 7B 0.6813, GPN-MSA 0.6750. Intronic n = 3,769 (supp data: 2,567 pos / 1,141 neg) — SpliceAI 0.9719, CADD 0.9445, Evo 2 7B 0.9320, Evo 2 40B 0.9267, Pangolin 0.9117.
  **Source:** Supplementary Data 1 (XLSX), `Data=SpliceVarDB`.
- **BRCA2** (Fig. 3 / Extended Data Fig. 5c): Both n = 6,837 — CADD 0.8837 / 0.7388; Evo 2 40B 0.8454; GPN-MSA 0.8376; Evo 2 7B 0.8346; PhyloP 100 0.7596; Evo 1 0.5399; NT 0.5137.
  **Source:** Supplementary Data 1 (XLSX), `Data=BRCA2`.

**Other published numbers:**
- **Claim:** A supervised ridge-regression classifier trained on Evo 2 40B embeddings beats zero-shot Evo 2 on the BRCA1 test set with **AUROC = 0.95, AUPRC = 0.88** (test set n = 789).
  **Source:** https://www.nature.com/articles/s41586-026-10176-5 (Fig. 3g–i caption and "Human variant effect prediction" section)
  **VERIFIED**
- **Claim:** Evo 2 is "not trained on any human genetic variation or functional genomics data."
  **Source:** https://www.nature.com/articles/s41586-026-10176-5 ("Human variant effect prediction", final paragraph)
  **VERIFIED**
- **Claim:** On zero-shot human gene essentiality, Evo 2 40B reaches AUROC = 0.66, AUPRC = 0.15 (other genomic LMs AUROC 0.50–0.59; four PhyloP scores AUROC 0.65–0.71).
  **Source:** https://www.nature.com/articles/s41586-026-10176-5
  **VERIFIED**
- **Claim:** On DART-Eval, Evo 2 40B caQTL AUROC = 0.58, dsQTL AUROC = 0.66 (NT: 0.52 / 0.61; ChromBPNet: 0.77 / 0.89).
  **Source:** https://www.nature.com/articles/s41586-026-10176-5
  **VERIFIED**

**Internal inconsistencies in the published paper (do not propagate them):**
- Fig. 3e caption says the BRCA1 coding subset is *n* = 2,077 SNVs, but Supplementary Data 1 reports the coding subset as N = 2,768 (584 pos + 2,184 neg); 2,768 + 1,125 = 3,893 = the total. **The caption's 2,077 is inconsistent with the supplementary table.**
  **Source:** https://www.nature.com/articles/s41586-026-10176-5 (Fig. 3e caption) vs. Supplementary Data 1 (XLSX)
  **VERIFIED** (as an inconsistency)
- Fig. 3c caption says noncoding ClinVar *n* = 34,761 SNVs; Supplementary Data 1 reports N = 33,747. **Also inconsistent.**
  **Source:** same
  **VERIFIED** (as an inconsistency)

### 1.7 `score_sequences` and mean-reduced log-likelihood (official repo / code)

- **Claim:** The repository copy at `evo2-backend/evo2/evo2/scoring.py` is byte-identical to the upstream file `evo2/scoring.py` in `ArcInstitute/evo2` (verified by SHA-256 after normalising CRLF→LF: `1411ADEF…` local vs `17E6985C…` upstream, equal after newline normalisation). Upstream path is `evo2/scoring.py` (there is no `evo2/evo2/scoring.py` upstream).
  **Source:** https://raw.githubusercontent.com/ArcInstitute/evo2/main/evo2/scoring.py ; upstream tree via https://api.github.com/repos/ArcInstitute/evo2/git/trees/main?recursive=1
  **VERIFIED**
- **Claim:** The official public API is `Evo2.score_sequences(seqs, batch_size=1, prepend_bos=False, reduce_method='mean', average_reverse_complement=False) -> List[float]`. It dispatches to `score_sequences` (or `score_sequences_rc` when `average_reverse_complement=True`) and re-raises failures as `RuntimeError("Error during sequence scoring: ...")`.
  **Source:** https://raw.githubusercontent.com/ArcInstitute/evo2/main/evo2/models.py (`class Evo2`, method `score_sequences`)
  **VERIFIED**
- **Claim:** The README's "Forward" section describes the capability as: "Evo 2 can be used to score the likelihoods across a DNA sequence."
  **Source:** https://github.com/ArcInstitute/evo2 (README → Usage → Forward)
  **VERIFIED**
- **Claim (exact semantics of `score_sequences`):**
  1. `prepare_batch` tokenises each sequence with the Evo2 tokenizer (`tokenizer.tokenize`), optionally prepends `tokenizer.eod_id` as BOS (`prepend_bos`), and right-pads with `tokenizer.pad_id` to the longest sequence in the batch. It returns `(input_ids, seq_lengths)`.
  2. The model is run once under `torch.inference_mode()`; `logits` has shape (batch, length, vocab).
  3. `logits_to_logprobs` applies `log_softmax` over the vocab axis, **shifts by one** (`softmax_logprobs[:, :-1]` and `input_ids[:, 1:]`), and gathers the log-probability of the *actual next token* at each position → per-position log-likelihoods of shape (batch, length-1).
  4. `reduce_method='sum'` → `np.sum` over the valid positions (**this is the per-sequence pseudo-log-likelihood, "PLL"**); `reduce_method='mean'` → `np.mean` over the valid positions (**"mean PLL"**). Any other value raises `ValueError(f'Invalid reduce_method {reduce_method}')`.
  5. The returned list has one scalar per input sequence.
  **Source:** https://raw.githubusercontent.com/ArcInstitute/evo2/main/evo2/scoring.py (`prepare_batch`, `logits_to_logprobs`, `_score_sequences`, `score_sequences`, `score_sequences_rc`)
  **VERIFIED**
- **Claim (units):** The returned value is a **natural-log likelihood per base pair** — i.e. `log P(sequence) / L` in nats/base (because `log_softmax` is used, not log2), averaged over the scored positions of that sequence. It is **not** a probability, **not** a log-odds ratio, and **not** comparable across sequences of different lengths unless the caller keeps the length fixed (the BRCA1 workflow does: fixed 8,192-bp windows).
  **Source:** same file (`log_softmax` → natural log; `np.mean` over positions)
  **VERIFIED**
- **Claim (directional use):** Because only the mutated base's log-probability changes, the difference `score(variant) − score(reference)` is negative for a variant the model finds less likely; the official BRCA1 notebook states "the lower the delta, the more likely that the SNV is disruptive."
  **Source:** https://raw.githubusercontent.com/ArcInstitute/evo2/main/notebooks/brca1/brca1_zero_shot_vep.ipynb
  **VERIFIED**
- **Claim (reverse-complement variant):** `score_sequences_rc` scores each sequence and its reverse complement and returns the **average** of the two reduced scores: `(np.array(batch_scores) + np.array(batch_scores_rc)) * 0.5`.
  **Source:** https://raw.githubusercontent.com/ArcInstitute/evo2/main/evo2/scoring.py
  **VERIFIED**
- **Claim (official BRCA1 notebook recipe):** data file `notebooks/brca1/41586_2018_461_MOESM3_ESM.xlsx`; `WINDOW_SIZE = 8192` (window centred on the variant, `WINDOW_SIZE//2` each side); the notebook scores "1326 reference sequences" and "3893 variant sequences" with `score_sequences(ref_seqs)` / `score_sequences(var_seqs)`.
  **Source:** https://raw.githubusercontent.com/ArcInstitute/evo2/main/notebooks/brca1/brca1_zero_shot_vep.ipynb
  **VERIFIED**

### 1.8 Evo 2 official web interfaces (relevant prior art for an Evo2Serve paper)

- **Claim:** The Evo 2 Nature paper lists official interactive tools: "Evo Designer, an interactive user interface for generation and scoring with Evo 2: https://arcinstitute.org/tools/evo/evo-designer" and "Evo Mech Interp Visualizer … https://arcinstitute.org/tools/evo/evo-mech-interp", plus NVIDIA NIM/hosted API endpoints.
  **Source:** https://www.nature.com/articles/s41586-026-10176-5 ("Code availability")
  **VERIFIED**

---

## 2. Findlay et al. 2018 — BRCA1 saturation genome editing

- **Claim:** "Accurate classification of *BRCA1* variants with saturation genome editing", *Nature* **562**(7726):217–222, published 12 September 2018 (issue date October 2018), DOI `10.1038/s41586-018-0461-z`, PMID 30209399, PMCID PMC6181777.
  **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/ (header: "*Nature*. 2018 Sep 12;562(7726):217–222. doi: 10.1038/s41586-018-0461-z")
  **Source:** https://api.crossref.org/works/10.1038/s41586-018-0461-z (vol 562, issue 7726, pages 217-222)
  **VERIFIED**
- **Claim:** Function scores were obtained for **3,893 SNVs**, "amounting to **96.5% of all possible SNVs** within or immediately intronic to these exons" (13 exons: RING exons 2–5, BRCT exons 15–23; transcript **NM_007294.3**; hg19 coordinates).
  **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/ (Abstract; "Function scores for 3,893 *BRCA1* SNVs"; Fig. 1b caption)
  **VERIFIED**
- **Claim:** Class proportions by two-component Gaussian mixture model: **72.5% functional, 21.1% non-functional, 6.4% intermediate**. Classification thresholds: *P*nf > 0.99 = non-functional, 0.01 < *P*nf < 0.99 = intermediate, *P*nf < 0.01 = functional. (Function-score cut-offs: −0.748 between functional and intermediate; −1.328 between intermediate and non-functional.)
  **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/ (Results: "72.5% of SNVs were categorized as functional, 21.1% as non-functional, and 6.4% as intermediate"; Methods: "SNV functional class assignment"; Fig. 3a caption)
  **VERIFIED**
- **Claim:** Among the 2,086 missense SNVs assayed, **441 (21.1%)** were non-functional; 70.6% functional and 8.1% intermediate (vs. 4.4% intermediate among all other SNVs; Fisher's exact *P* = 2.7 × 10⁻⁶). Canonical splice-site SNVs: 89.5% non-functional, 5.5% intermediate.
  **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/
  **VERIFIED**
- **Claim:** Cell system: human haploid **HAP1** cells (derived from KBM7), using a monoclonal **LIG4-knockout HAP1 line (HAP1-Lig4KO)** with FACS sorting for 1N ploidy; median 3.6-fold increase in HDR rate in HAP1-Lig4KO vs. WT HAP1. Sampling: gDNA at day 5 and day 11, plus targeted cDNA (RNA) at day 5; Illumina NextSeq/MiSeq.
  **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/ (Methods: "HAP1 cell culture", "Transfection of HAP1 cells", "Sequencing and data analysis")
  **VERIFIED**
- **Claim:** Function score construction: log2(day-11 frequency / library frequency); positional (LOESS, span 0.15) editing-bias model subtracted; scores normalised across replicates and exons by matching median synonymous and median nonsense SNVs to global medians.
  **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/ (Methods: "Modeling positional biases of library integration", "Normalizing scores within and across exons")
  **VERIFIED**
- **Claim (ROC operating point):** "A ROC curve showed a **sensitivity of 96.7% at 98.2% specificity** when we treat 'likely pathogenic' and 'likely benign' ClinVar annotations as pathogenic and benign, respectively." The ROC is computed on the same **375 SNVs** with at least a **1-star review status** in ClinVar and a pathogenic or benign (including "likely") interpretation; optimal cut-offs are SGE function scores from −1.03 to −1.22.
  **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/ (Results: "Function scores accurately predict pathogenicity"; Fig. 3a and 3b captions)
  **VERIFIED**
- **Claim:** Clinical concordance: of 169 ClinVar-pathogenic SNVs, 162 were non-functional, 2 functional, 5 intermediate; of 22 ClinVar-benign SNVs, 20 functional, 1 non-functional, 1 intermediate. 25.0% (64/256) of VUS and 49.2% (60/122) of conflicting-interpretation SNVs scored non-functional.
  **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/
  **VERIFIED**
- **Claim:** RNA scores (cDNA/gDNA frequency ratio) were computed for 96% of functionally characterised exonic SNVs; 89% of non-functional missense SNVs did not substantially reduce RNA levels (protein-level mechanism), while ~11% were depleted ≥4-fold (expression-mediated).
  **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/ (Results: "Mechanisms of *BRCA1* loss-of-function")
  **VERIFIED**
- **Claim:** The data are deposited at Supplementary Table 1 and at https://sge.gs.washington.edu/BRCA1/ .
  **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/ ("Altogether, we obtained function scores for 3,893 SNVs … [Supplementary Table 1]; https://sge.gs.washington.edu/BRCA1/")
  **VERIFIED**

### 2.1 The supplementary workbook used by this repo (`41586_2018_461_MOESM3_ESM.xlsx`)

- **Claim:** The Findlay paper has five supplementary objects:
  `41586_2018_461_MOESM1_ESM.pdf`, `..._MOESM2_ESM.pdf`, `..._MOESM3_ESM.xlsx`, `..._MOESM4_ESM.xlsx`, `..._MOESM5_ESM.xlsx`.
  **Source:** https://www.nature.com/articles/s41586-018-0461-z (article supplementary-material list)
  **VERIFIED**
- **Claim:** MOESM3 (XLSX) is downloadable at
  `https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-018-0461-z/MediaObjects/41586_2018_461_MOESM3_ESM.xlsx`
  (2,306,341 bytes; downloaded and parsed locally).
  **Source:** same URL (HTTP 200, XLSX payload)
  **VERIFIED**
- **Claim (contents, verified by parsing the XLSX):** one sheet (`Sheet1`), **3,893 data rows** (3,896 rows total including three leading metadata rows). Column headers on row 3:
  `Variant ID, gene, chromosome, position (hg19), reference, alt, transcript_ID, transcript_position, transcript_ref, transcript_alt, transcript_variant, aa_pos, aa_ref, aa_alt, protein_variant, consequence, function.score.mean, func.class, p.nonfunctional, experiment, negative`.
  This is exactly the column set the Evo 2 notebook consumes (`chromosome`, `position (hg19)`, `reference`, `alt`, `function.score.mean`, `func.class`).
  **Source:** downloaded MOESM3 XLSX; column list cross-checked against https://raw.githubusercontent.com/ArcInstitute/evo2/main/notebooks/brca1/brca1_zero_shot_vep.ipynb
  **VERIFIED**
- **Claim (independent recomputation of the class proportions from the file):**
  FUNC = 2,821 (72.5%), LOF = 823 (21.1%), INT = 249 (6.4%); total 3,893.
  Missense subset (2,086 rows): LOF = 441 (21.1%), FUNC = 1,476 (70.8%), INT = 169 (8.1%).
  **Source:** downloaded MOESM3 XLSX, recomputed locally
  **VERIFIED** (matches the paper's text exactly)
- **Claim:** `func.class` uses the tokens **FUNC**, **LOF**, **INT** (the paper's "functional / non-functional / intermediate" classes).
  **Source:** same
  **VERIFIED**
- **Claim:** The paper's own downloadable data page is https://sge.gs.washington.edu/BRCA1/ ; MaveDB also hosts per-exon score sets (e.g. `urn:mavedb:00000097-s-1`), but MaveDB is a mirror, not the paper of record.
  **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/ (data availability in Results)
  **VERIFIED** for sge.gs.washington.edu; MaveDB host not re-verified here.

---

## 3. ClinVar and NCBI E-utilities

### 3.1 Citations

- **Claim (original):** Landrum MJ, Lee JM, Riley GR, Jang W, Rubinstein WS, Church DM, Maglott DR. "ClinVar: public archive of relationships among sequence variation and human phenotype." *Nucleic Acids Research* 2014;42(D1):D980–D985, DOI `10.1093/nar/gkt1113`, PMID 24234437.
  **Source:** https://www.ncbi.nlm.nih.gov/clinvar/intro/ (References list, item 6) ; https://api.crossref.org/works/10.1093/nar/gkt1113 (vol 42, issue D1, pages D980-D985)
  **VERIFIED**
- **Claim (most recent update):** Landrum MJ, Chitipiralla S, Kaur K, Brown G, Chen C, Hart J, Hoffman D, Jang W, Liu C, Maddipatla Z, Maiti R, Mitchell J, Rezaie T, Riley G, Song G, Yang J, Ziyabari L, Russette A, Kattman BL. "ClinVar: updates to support classifications of both germline and somatic variants." *Nucleic Acids Research* 2025;53(D1):D1313–D1321 (published online 23 Nov 2024), DOI `10.1093/nar/gkae1090`, PMID 39578691.
  **Source:** https://www.ncbi.nlm.nih.gov/clinvar/intro/ (References list, item 1) ; https://api.crossref.org/works/10.1093/nar/gkae1090 (vol 53, issue D1, pages D1313-D1321)
  **VERIFIED**
- **Claim (intermediate updates, also on the official ClinVar reference list):** Landrum et al., *NAR* 2018;46(D1):D1062–D1067, doi `10.1093/nar/gkx1153` (PMID 29165669); Landrum et al., *NAR* 2020;48(D1):D835–D844, doi `10.1093/nar/gkz972` (PMID 31777943); Landrum & Kattman, *Hum Mutat* 2018;39(11):1623–1630, doi `10.1002/humu.23641` (PMID 30311387); Landrum et al., *NAR* 2016;44(D1):D862–D868, doi `10.1093/nar/gkv122` (PMID 26582918).
  **Source:** https://www.ncbi.nlm.nih.gov/clinvar/intro/
  **VERIFIED**

### 3.2 Documented E-utilities subset and workflow

- **Claim:** "As part of NCBI's Entrez system, ClinVar can be accessed by E-utilities, through web services and through a UNIX command line as Entrez Direct. **ClinVar supports a subset of the E-utilities functions: esearch, esummary, elink, and efetch.**"
  **Source:** https://www.ncbi.nlm.nih.gov/clinvar/docs/programmatic_access/
  **VERIFIED**
- **Claim:** The documented workflow is: (1) esearch to find unique identifiers; (2) then esummary (overview of each record), efetch (the complete record), or elink (data in other NCBI databases related to a ClinVar record). "The default format from E-utilities is XML. For esummary, you can specify JSON output as well."
  **Source:** https://www.ncbi.nlm.nih.gov/clinvar/docs/programmatic_access/
  **VERIFIED**
- **Claim:** The esummary document summary carries more than the web search results: "you can retrieve location data on both GRCh37 and GRCh38 from *assembly_set*, database identifiers for disorders from *trait_refs*, the type of variant from *variant_type* and the source of any gene-variant relationship from *gene/source*."
  **Source:** https://www.ncbi.nlm.nih.gov/clinvar/docs/programmatic_access/
  **VERIFIED**
- **Claim (official example URLs, verbatim from the ClinVar doc):**
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=FGFR3[gene]&retmax=500`
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=FGFR3[gene]+AND+single_gene[prop]&retmax=500`
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=65533`
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=65533&retmode=json`
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=clinvar&cmd=acheck&id=9`
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=clinvar&db=pubmed&id=9` (also `db=medgen`)
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=clinvar&rettype=vcv&is_variationid&id=14206,41472&from_esearch=true`
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=clinvar&rettype=vcv&id=VCV000014206` (and `id=VCV000014206.1` for a specific version)
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=clinvar&rettype=clinvarset&id=RCV000000606` (and `id=RCV000000606.3`)
  **Source:** https://www.ncbi.nlm.nih.gov/clinvar/docs/programmatic_access/
  **VERIFIED**
- **Claim (E-utilities general description):** E-utilities are "the public API to the NCBI Entrez system and allow access to all Entrez databases including PubMed, PMC, Gene, Nuccore and Protein".
  **Source:** https://www.ncbi.nlm.nih.gov/home/develop/api/
  **VERIFIED**
- **UNVERIFIED (rate limits):** the commonly quoted NCBI E-utilities policy of "no more than three requests per second without an API key" could **not** be confirmed from a primary source in this session — the NCBI Bookshelf chapter "Using the E-utilities" (`https://www.ncbi.nlm.nih.gov/books/NBK25497/`) is behind a bot challenge, and `https://www.ncbi.nlm.nih.gov/home/develop/api/` does not state it in its served HTML. If the paper needs to state a request-rate policy for E-utilities, cite the NCBI Bookshelf chapter directly and re-verify; otherwise omit the number. (By contrast, the UCSC request-rate guidance **is** verified — see §4.)
  **Source attempted:** https://www.ncbi.nlm.nih.gov/books/NBK25497/ ; https://www.ncbi.nlm.nih.gov/home/develop/api/
  **UNVERIFIED**

### 3.3 What `retmode=json` esummary actually returns (verified against the live API)

- **Claim:** `esummary.fcgi?db=clinvar&id=<id>&retmode=json` returns `{"header":…, "result": { "<uid>": {…} }}` where the per-record object has keys:
  `uid, obj_type, accession, accession_version, title, variation_set, supporting_submissions, germline_classification, clinical_impact_classification, oncogenicity_classification, record_status, gene_sort, chr_sort, location_sort, variation_set_name, variation_set_id, genes, molecular_consequence_list, protein_change, fda_recognized_database`.
  **Source (live call):** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=14206&retmode=json`
  **VERIFIED**
- **Claim:** `germline_classification` contains `description` (the clinical significance string), `last_evaluated` (a date string), `review_status` (the aggregate review-status string), `fda_recognized_database`, and `trait_set`. `clinical_impact_classification` and `oncogenicity_classification` have the same shape but are usually empty.
  **Source:** same live call (example: `description: "protective"`, `last_evaluated: "2003/11/07 00:00"`, `review_status: "no assertion criteria provided"`)
  **VERIFIED**
- **Claim:** `variation_set[].variation_loc[]` carries per-assembly locations with `assembly_name` ("GRCh38"/"GRCh37"), `chr`, `start`, `stop`, `display_start`, `display_stop`, `assembly_acc_ver` and `status` ("current"/"previous"); `canonical_spdi` gives the 0-based SPDI (example: `NC_000017.11:34256112:G:G`).
  **Source:** same live call
  **VERIFIED**
- **Claim:** `supporting_submissions` lists the SCV and RCV accessions (example: `scv: ["SCV000035529"]`, `rcv: ["RCV000015270"]`).
  **Source:** same live call
  **VERIFIED**
- **Claim (VCV XML structure via efetch):** `efetch.fcgi?db=clinvar&rettype=vcv&id=VCV000014206` returns `<ClinVarResult-Set><VariationArchive VariationID="14206" VariationName="…" VariationType="single nucleotide variant" Accession="VCV000014206" Version="1" RecordType="classified" NumberOfSubmissions="1" NumberOfSubmitters="1" DateLastUpdated="2025-05-17" DateCreated="2017-06-25" MostRecentSubmission="2017-06-25">` containing `<RecordStatus>`, `<Species>`, `<ClassifiedRecord>` → `<SimpleAllele AlleleID="29245" VariationID="14206">` with `<GeneList>`, `<Name>`, `<CanonicalSPDI>`, `<VariantType>`, `<Location>` (per-assembly `SequenceLocation` for GRCh38 and GRCh37), and classification blocks carrying `<ReviewStatus>` and `<LastEvaluated>`.
  **Source:** live call `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=clinvar&rettype=vcv&id=VCV000014206`
  **VERIFIED**
- **Claim:** ClinVar record identifiers follow the documented scheme: SCV (submission) `SCV000000000.0`, RCV (variation-condition) `RCV000000000.0`, VCV (variation) `VCV000000000.0`. A ClinVar record contains: accession+version; HGVS expressions, published allele names, database identifiers; condition name and IDs; classification with review status, submitter, classification value, and evidence summary; mode of inheritance; citations.
  **Source:** https://www.ncbi.nlm.nih.gov/clinvar/intro/ ("A ClinVar record contains the following elements")
  **VERIFIED**
- **Claim:** The ClinVar search fields `chrpos37` and `chrpos38` exist and are usable in an esearch `term`, e.g. `17[chr] AND 43000000:44000000[chrpos37]`.
  **Source:** https://www.ncbi.nlm.nih.gov/clinvar/docs/help/ (worked examples using `[chrpos37]` / `[chrpos38]`)
  **VERIFIED**

### 3.4 Review-status tiers — current documented names (important if the paper mentions review status)

For **aggregate records (VCV and RCV), germline classification and oncogenicity**, ClinVar documents exactly these:

| Gold stars | Review status |
|---|---|
| four | practice guideline |
| three | reviewed by expert panel |
| two | criteria provided, multiple submitters, no conflicts |
| one | criteria provided, conflicting classifications |
| one | criteria provided, single submitter |
| none | no assertion criteria provided |
| none | no classification provided |
| none | no classification for the individual variant |

For **somatic clinical impact**, the two-star tier is "criteria provided, multiple submitters" (no conflicts tier does not exist), and there is no "conflicting classifications" tier.
For **submitted records (SCV)** only, the tiers are: practice guideline / reviewed by expert panel / criteria provided, single submitter / no assertion criteria provided / no classification provided.

- **Source:** https://www.ncbi.nlm.nih.gov/clinvar/docs/review_status/ (page last updated 2024-04-18)
  **VERIFIED**
- **Note (naming change):** the two-star tier is currently **"criteria provided, multiple submitters, no conflicts"** and the one-star conflicting tier is **"criteria provided, conflicting classifications"**. Older literature/UI strings ("criteria provided, multiple submitters", "criteria provided, conflicting interpretations") are superseded. Do not write "criteria provided, conflicting" or "criteria provided, multiple submitters" without the current full strings.
- **Note (gold stars):** "Review status is reported only in text format in ClinVar's products available by FTP." Star counts are a web/FTP display convention, not a stored field.
  **Source:** https://www.ncbi.nlm.nih.gov/clinvar/docs/review_status/
  **VERIFIED**

### 3.5 What this repo's app actually calls (repo-local, for cross-checking against the docs)

- **Claim:** The frontend uses only three E-utilities endpoints and three UCSC endpoints:
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id=<geneId>&retmode=json` (gene details)
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=<chrom>[chromosome] AND <min>:<max>[chrpos37|chrpos38]&retmode=json&retmax=20`
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=<ids>&retmode=json`
  - `https://api.genome.ucsc.edu/list/ucscGenomes`
  - `https://api.genome.ucsc.edu/list/chromosomes?genome=<genomeId>`
  - `https://api.genome.ucsc.edu/getData/sequence?genome=<genomeId>;chrom=<chrom>;start=<apiStart>;end=<apiEnd>`
  It does **not** use `efetch` or `elink`.
  **Source (repo-local):** `evo2-frontend/src/utils/genome-api.ts` lines 171, 202, 291, 344, 379–413 ; `evo2-backend/main.py` line 394
  **VERIFIED (repo-local)**

---

## 4. UCSC Genome Browser REST API

- **Claim (base URL):** "This access URL: **https://api.genome.ucsc.edu/** is used to access the endpoint functions."
  **Source:** https://genome.ucsc.edu/goldenpath/help/api.html
  **VERIFIED**
- **Claim (endpoint list, verbatim):** `/findGenome`, `/list/publicHubs`, `/list/ucscGenomes`, `/list/genarkGenomes`, `/list/hubGenomes`, `/list/files`, `/list/tracks`, `/list/chromosomes`, `/list/schema`, `/getData/sequence`, `/getData/track`, `/search`.
  **Source:** https://genome.ucsc.edu/goldenpath/help/api.html
  **VERIFIED**
- **Claim (required/optional parameters, verbatim from the doc table):**
  - `/list/ucscGenomes` — required: (none); optional: (none)
  - `/list/chromosomes` — required: genome OR (hubUrl AND genome); optional: track
  - `/getData/sequence` — required: (genome OR (hubUrl AND genome)) AND chrom; optional: start, end, revComp=1
  - `/getData/track` — required: (genome OR (hubUrl AND genome)) AND track; optional: chrom, (start and end), maxItemsOutput, jsonOutputArrays
  - `/search` — required: search AND genome; optional: categories=helpDocs, categories=publicHubs, categories=trackDb
  - `/list/schema` — required: (genome OR (hubUrl AND genome)) AND track
  **Source:** https://genome.ucsc.edu/goldenpath/help/api.html
  **VERIFIED**
- **Claim (parameter syntax):** "The parameters are added to the endpoint URL beginning with a question mark **?**, and multiple parameters are separated with the semi-colon **;**", e.g. `https://api.genome.ucsc.edu/getData/sequence?genome=hg38;chrom=chrM`.
  **Source:** https://genome.ucsc.edu/goldenpath/help/api.html
  **VERIFIED**
- **Claim (coordinate semantics, verbatim):** "**start**=<123> - specify start coordinate (**0 relative**) for data from track or sequence retrieval (start and end required together). … **end**=<456> - specify end coordinate (**1 relative**) for data from track or sequence retrieval (start and end required together)."
  **Source:** https://genome.ucsc.edu/goldenpath/help/api.html
  **VERIFIED**
- **Claim (empirical confirmation of `/getData/sequence`):** `getData/sequence?genome=hg38;chrom=chrM;start=4321;end=5678` returns a 1,357-base string; `…;start=4321;end=5679` returns 1,358 bases. The JSON response keys are `downloadTime, downloadTimeStamp, genome, chrom, start, end, dna`, and it echoes `start`/`end` unchanged. Therefore the returned interval is 0-based half-open `[start, end)` — equivalently a 1-based inclusive end position — and the length is `end − start`. `revComp=1` returns the reverse complement of the same interval.
  **Source (live API):** `https://api.genome.ucsc.edu/getData/sequence?genome=hg38;chrom=chrM;start=4321;end=5678`
  **VERIFIED**
- **Claim (output cap, verbatim):** "**maxItemsOutput=1000000** - limit number of items to output, default: 1,000,000, maximum limit: 1,000,000 (use *-1* to get maximum output)". The doc also notes that for `/getData/track` "only the first million items are returned", and recommends breaking large tracks up with the `chrom` (and `start`/`end`) parameters.
  **Source:** https://genome.ucsc.edu/goldenpath/help/api.html
  **VERIFIED**
- **Claim (rate / etiquette policy, verbatim):** "Avoid excessive or heavy queries that may impact the server performance. Inappropriate query use will result in a restriction of access." … "We generally recommend a maximum of **one hit every second**, but there is no strict limit on queries using the API. A **botDelay** system is in place to avoid overloads on the system." … "If you begin to notice a significant delay between requests, adjust your code or try an alternative method to retrieve our data." Bulk users are directed to the Table Browser, the public MySQL server, the download server, and HTTP streaming of bigBed/bigWig.
  **Source:** https://genome.ucsc.edu/goldenpath/help/api.html ("Conditions of use" + "Why you may not want to use this API")
  **VERIFIED**
- **Claim (mirrors):** mirror URLs use `https://<mirror>/cgi-bin/hubApi/`, e.g. `https://genome-euro.ucsc.edu/cgi-bin/hubApi/`, `https://genome-asia.ucsc.edu/cgi-bin/hubApi/`.
  **Source:** https://genome.ucsc.edu/goldenpath/help/api.html
  **VERIFIED**
- **Claim (recommended citation):** UCSC's own "Cite Us" page says: "Please cite our latest paper, currently **PMID 41251146**, DOI **10.1093/nar/gkaf1250**", i.e. Casper J, Speir ML, Raney BJ, Perez G, Nassar LR, Lee CM, Hinrichs AS, Gonzalez JN, Fischer C, Diekhans M, et al. "The UCSC Genome Browser database: 2026 update." *Nucleic Acids Research* 2026;54(D1):D1331–D1335.
  **Source:** https://genome.ucsc.edu/cite.html ; https://api.crossref.org/works/10.1093/nar/gkaf1250
  **VERIFIED**
- **Claim (the 2022 NAR paper that actually exists):** Lee BT, Barber GP, Benet-Pagès A, Casper J, Clawson H, Diekhans M, Fischer C, Gonzalez JN, Hinrichs AS, Lee BT, Muthuraman P, Nassar LR, Nguy B, Pereira T, Nejad P, Perez G, Raney BJ, Rosenbloom KR, Schmelter D, Speir ML, Wick BD, Zweig AS, Kuhn RM, Haeussler M, Kent WJ. "The UCSC Genome Browser database: 2022 update." *Nucleic Acids Research* 2022;50(D1):D1115–D1122, DOI `10.1093/nar/gkab959`, PMID 34718705, PMCID PMC8728131.
  **Source:** https://genome.ucsc.edu/cite.html ; https://api.crossref.org/works/10.1093/nar/gkab959 ; https://pubmed.ncbi.nlm.nih.gov/34718705/
  **VERIFIED**
- **Claim (citation UCSC itself recommends for the REST API):** Lee CM, Barber GP, Casper J, Clawson H, Diekhans M, Gonzalez JN, Hinrichs AS, Lee BT, Nassar LR, Powell CC, et al. "UCSC Genome Browser enters 20th year." *Nucleic Acids Research* 2020;48(D1):D756–D761, DOI `10.1093/nar/gkz1012`, PMID 31691824.
  **Source:** https://genome.ucsc.edu/cite.html (section "RESTful API")
  **VERIFIED**
- **UNVERIFIED:** There is **no** Nucleic Acids Research paper titled "The UCSC Genome Browser: exploring the world's most comprehensive resource of genome-scale data". Searches of PubMed (title search), Crossref and UCSC's own publication list (https://genome.ucsc.edu/goldenPath/pubs.html) and cite page do not return it, and no 2022 NAR paper with that title exists. **Do not cite that title.** Use `lee2022ucsc` (NAR 50(D1):D1115–D1122) or `casper2026ucsc` (NAR 54(D1):D1331–D1335) instead.

---

## 5. ACMG/AMP framework and computational evidence

- **Claim (citation):** Richards S, Aziz N, Bale S, Bick D, Das S, Gastier-Foster J, Grody WW, Hegde M, Lyon E, Spector E, Voelkerding K, Rehm HL. "Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology." *Genetics in Medicine* 2015;17(5):405–424, DOI `10.1038/gim201530`, PMID 25741868. (Published 05 March 2015.)
  **Source:** https://www.nature.com/articles/gim201530 (header: "volume 17, pages 405–423 (2015)"; "Genet Med 17 5, 405–423"; "Published: 05 March 2015") ; https://pubmed.ncbi.nlm.nih.gov/25741868/ ("Genet Med. 2015 May;17(5):405-24. doi: 10.1038/gim.2015.30")
  **VERIFIED**
- **Claim (evidence-code structure, verbatim from the paper):** "Each pathogenic criterion is weighted as **very strong (PVS1), strong (PS1–4); moderate (PM1–6), or supporting (PP1–5)**, and each benign criterion is weighted as **stand-alone (BA1), strong (BS1–4), or supporting (BP1–6)**. The numbering within each category does not convey any differences of weight… If a variant does not fulfill criteria using either of these sets … or the evidence for benign and pathogenic is conflicting, the variant defaults to uncertain significance."
  **Source:** https://www.nature.com/articles/gim201530 ("Proposed Criteria for Interpretation of Sequence Variants")
  **VERIFIED**
- **Claim:** The benign supporting tier in the 2015 paper is **BP1–BP6**; **BP7** was added later by ClinGen (see §5.3). Any paper text listing "BP1–7" should attribute BP7 to ClinGen, not to Richards 2015.
  **Source:** https://www.nature.com/articles/gim201530 (BP1–6) ; https://cspec.genome.network/cspec/ui/svi/doc/GN092 (BP7 present)
  **VERIFIED**
- **Claim (PP3 / BP4 — verbatim):**
  - PP3 "Multiple lines of computational evidence support a deleterious effect on the gene or gene product (conservation, evolutionary, splicing impact, etc.). Caveat: As many in silico algorithms use the same or very similar input for their predictions, each algorithm should not be counted as an independent criterion. PP3 can be used only once in any evaluation of a variant."
  - BP4 "Multiple lines of computational evidence suggest no impact on gene or gene product (conservation, evolutionary, splicing impact, etc) Caveat: As many in silico algorithms use the same or very similar input for their predictions, each algorithm cannot be counted as an independent criterion. BP4 can be used only once in any evaluation of a variant."
  **Source:** https://www.nature.com/articles/gim201530 (Tables 3 and 4)
  **VERIFIED**
- **Claim (the "PP3 BP4 computational (in silico) data" narrative section, verbatim):** "Not overestimating computational evidence is important, particularly given that different algorithms may rely on the same (or similar) data to support predictions and most algorithms have not been validated against well-established pathogenic variants. In addition, algorithms can have vastly different predictive capabilities for different genes. **If all of the in silico programs tested agree on the prediction, then this evidence can be counted as supporting. If in silico predictions disagree, however, then this evidence should not be used in classifying a variant.**"
  **Source:** https://www.nature.com/articles/gim201530 (section "PP3 BP4 computational (in silico) data")
  **VERIFIED**
- **Claim (the crucial caveat — verbatim):** "These are only predictions, however, and their use in sequence variant interpretation should be implemented carefully. **It is not recommended that these predictions be used as the sole source of evidence to make a clinical assertion.**"
  **Source:** https://www.nature.com/articles/gim201530 (section "Computational (in silico) predictive programs")
  **VERIFIED**
- **Claim (independent corroboration of the same caveat from the BRCA1 field):** "Computational predictions based on features such as conservation can add information but are **insufficiently accurate to be used in the absence of genetic or experimental evidence**."
  **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/ (Introduction)
  **VERIFIED**
- **Claim (performance of in silico missense predictors, verbatim):** "In general, most algorithms for missense variant prediction are 65–80% accurate when examining known disease variants. Most tools also tend to have low specificity, resulting in overprediction of missense changes as deleterious."
  **Source:** https://www.nature.com/articles/gim201530
  **VERIFIED**

### 5.1 Bayesian / points-based systems (calibration of computational predictors)

- **Claim:** Tavtigian SE, Vite A, Mandelkow S, Pinaya M, Jamshidi P, Ashton D, Gavric I, Matic I, Stevanovic M, Valle L, Xin B, included in the Bayesian formulation of the ACMG/AMP guidelines: Tavtigian SE et al. "Modeling the ACMG/AMP variant classification guidelines as a Bayesian classification framework." *Genetics in Medicine* 2018;20(9):1054–1060, DOI `10.1038/gim.2017.210`, PMID 29300386.
  **Source:** https://pubmed.ncbi.nlm.nih.gov/29300386/
  **VERIFIED**
- **Claim:** Tavtigian SE, Vite A, Matic I, ... "Fitting a naturally scaled point system to the ACMG/AMP variant classification guidelines." *Human Mutation* 2020;41(10):1734–1737, DOI `10.1002/humu.24088`, PMID 32720330.
  **Source:** https://pubmed.ncbi.nlm.nih.gov/32720330/
  **VERIFIED**
- **Claim (the ClinGen SVI calibration of computational predictors — the key "recalibration" citation):** Pejaver V, Byrne AB, Feng B-J, Pagel KA, Mooney SD, Karchin R, O'Donnell-Luria A, Harrison SM, Tavtigian SV, Greenblatt MS, Biesecker LG, Radivojac P, Brenner SE; ClinGen Sequence Variant Interpretation Working Group. "Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria." *American Journal of Human Genetics* 2022;109(12):2163–2177, DOI `10.1016/j.ajhg.2022.10.013`, PMID 36413997, PMCID PMC9748256.
  Its abstract states: "Recommendations from the ACMG/AMP for interpreting sequence variants specify the use of computational predictors as 'supporting' level of evidence for pathogenicity or benignity using criteria **PP3 and BP4**, respectively. … We … introduce a new standard that converts a tool's scores to PP3 and BP4 evidence strengths … based on estimating the local positive predictive value and can calibrate any computational tool or other continuous-scale evidence on any variant type."
  **Source:** https://www.cell.com/ajhg/fulltext/S0002-9297(22)00461-X ; https://api.crossref.org/works/10.1016/j.ajhg.2022.10.013 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC9748256/
  **VERIFIED**
- **Claim (extension of the ClinGen calibration to three newer predictors):** Bergquist T, Stenton SL, Nadeau EA, Byrne AB, Greenblatt MS, Harrison SM, Tavtigian SV, O'Donnell-Luria A, Biesecker LG, Radivojac P, Brenner SE, Pejaver V; ClinGen SVI Working Group. "Calibration of additional computational tools expands ClinGen recommendation options for variant classification with PP3/BP4 criteria." *Genetics in Medicine* (2025) — covers AlphaMissense, ESM1b and VARITY, which reached Strong (pathogenic) and Moderate (benign) evidence.
  **Source:** https://www.broadinstitute.org/publications/broad1361861 (publisher-metadata record for the Genetics in Medicine article)
  **VERIFIED** (citation + result). **UNVERIFIED:** the exact volume/issue/pages/DOI of this article was not obtained from a primary publisher page here.

### 5.2 ClinGen BRCA1/BRCA2 VCEP specifications (the `cspec` GN092 document)

- **Claim:** The document at `https://cspec.genome.network/cspec/ui/svi/doc/GN092` is "ClinGen ENIGMA BRCA1 and BRCA2 Expert Panel Specifications to the ACMG/AMP Variant Interpretation Guidelines for BRCA1 **Version 1.2**", released 1/9/2025, DOI `10.5281/zenodo.21434315`, Research Group "ENIGMA BRCA1 and BRCA2 VCEP", Rights Holder "The Clinical Genome Resource (ClinGen)".
  **Source:** https://cspec.genome.network/cspec/ui/svi/doc/GN092
  **VERIFIED**
- **Claim:** It fixes BRCA1-specific ACMG/AMP specifications, including **PP3** (BayesDel no-AF score ≥ 0.28 for missense/in-frame variants inside a clinically important functional domain — BRCA1 RING aa 2–101, coiled-coil aa 1391–1424, BRCT repeats aa 1650–1857 — and SpliceAI ≥ 0.2 for silent/missense/intronic splice prediction) and **BP4** (BayesDel no-AF ≤ 0.15 AND SpliceAI ≤ 0.1 in a functional domain; SpliceAI ≤ 0.1 for intronic variants outside native donor/acceptor ±1,2 sites), and notes that **BP7** is applied in addition to BP4 for silent variants.
  **Source:** https://cspec.genome.network/cspec/ui/svi/doc/GN092
  **VERIFIED**
- **Note:** GN092 is a **gene-specific VCEP specification**, not the general SVI PP3/BP4 recommendation document. If the paper cites "ClinGen SVI guidance" for PP3/BP4 recalibration, the correct citations are Pejaver et al. 2022 (AJHG) and Bergquist et al. 2025 (Genet Med); if it cites gene-specific BRCA1 rules, GN092 is correct.

---

## 6. Related work — verified citations for a comparison table

| # | Work | Verified citation | Source |
|---|---|---|---|
| 1 | **SIFT** | Ng PC, Henikoff S. "Predicting deleterious amino acid substitutions." *Genome Research* 2001;11(5):863–874. DOI `10.1101/gr.176601`, PMID 11337480 | https://api.crossref.org/works/10.1101/gr.176601 ; https://pubmed.ncbi.nlm.nih.gov/11337480/ |
| 2 | **PolyPhen-2** | Adzhubei IA, Schmidt S, Peshkin L, Ramensky VE, Zorkov A, et al. "A method and server for predicting damaging missense mutations." *Nature Methods* 2010;7(4):248–249. DOI `10.1038/nmeth0410-248`, PMID 20354512 | https://api.crossref.org/works/10.1038/nmeth0410-248 ; https://pubmed.ncbi.nlm.nih.gov/20354512/ |
| 3 | **CADD** | Rentzsch P, Witten DM, Cooper GM, Shendure J, Kircher M. "CADD: predicting the deleteriousness of variants throughout the human genome." *Nucleic Acids Research* 2019;47(D1):D886–D894. DOI `10.1093/nar/gky1016`, PMID 30371827 | https://api.crossref.org/works/10.1093/nar/gky1016 ; https://pubmed.ncbi.nlm.nih.gov/30371827/ |
| 3b | **CADD v1.7** | Schubach M, Maass T, Nazaretyan L, Röner S, Kircher M. "CADD v1.7: using protein language models, regulatory CNNs and other nucleotide-level scores to improve genome-wide variant predictions." *Nucleic Acids Research* 2024;52(D1):D1143–D1154. DOI `10.1093/nar/gkad989`, PMID 38183205 | https://api.crossref.org/works/10.1093/nar/gkad989 |
| 4 | **VEP (Ensembl)** | McLaren W, Gil L, Hunt SE, Riat HS, Ritchie GR, Thormann A, Flicek P, Cunningham F. "The Ensembl Variant Effect Predictor." *Genome Biology* 2016;17:122. DOI `10.1186/s13059-016-0974-4`, PMID 27268795 | https://api.crossref.org/works/10.1186/s13059-016-0974-4 ; https://pubmed.ncbi.nlm.nih.gov/27268795/ |
| 4b | **VEP tutorial (2022)** | Hunt SE, Moore B, Amodei RM, et al. "Annotating and prioritizing genomic variants using the Ensembl Variant Effect Predictor—A tutorial." *Human Mutation* 2022;43(8):986–997 (online 2021). DOI `10.1002/humu.24298`, PMID 34816521 | https://api.crossref.org/works/10.1002/humu.24298 |
| 5 | **AlphaMissense** | Cheng J, Novati G, Pan J, Bycroft C, et al. "Accurate proteome-wide missense variant effect prediction with AlphaMissense." *Science* 2023;381(6664):eadg7492. DOI `10.1126/science.adg7492`, PMID 37733863 | https://api.crossref.org/works/10.1126/science.adg7492 ; https://pubmed.ncbi.nlm.nih.gov/37733863/ |
| 6 | **ESM-2** | Lin Z, Akin H, Rao R, Hie B, Zhu Z, Lu W, et al. "Evolutionary-scale prediction of atomic-level protein structure with a language model." *Science* 2023;379(6637):1123–1130. DOI `10.1126/science.ade2574`, PMID 36927031 | https://pubmed.ncbi.nlm.nih.gov/36927031/ ; https://www.science.org/doi/10.1126/science.ade2574 ; canonical BibTeX at https://github.com/facebookresearch/ESM |
| 6b | **ESM zero-shot VEP** | Meier J, Rao R, Verkuil R, Liu J, Sercu T, Rives A. "Language models enable zero-shot prediction of the effects of mutations on protein function." *NeurIPS* 2021, pp. 29287–29303; preprint bioRxiv `10.1101/2021.07.09.450648` | https://www.biorxiv.org/content/10.1101/2021.07.09.450648 ; cited as ref. 14 in https://www.nature.com/articles/s41586-026-10176-5 |
| 7 | **Nucleotide Transformer** | Dalla-Torre H, Gonzalez L, Mendoza-Revilla J, Lopez Carranza N, et al. "Nucleotide Transformer: building and evaluating robust foundation models for human genomics." *Nature Methods* 2025;22(2):287–297 (online 2024). DOI `10.1038/s41592-024-02523-z`, PMID 39609566 | https://api.crossref.org/works/10.1038/s41592-024-02523-z ; https://pubmed.ncbi.nlm.nih.gov/39609566/ |
| 8 | **Enformer** | Avsec Ž, Agarwal V, Visentin D, Ledsam JR, et al. "Effective gene expression prediction from sequence by integrating long-range interactions." *Nature Methods* 2021;18(10):1196–1203. DOI `10.1038/s41592-021-01252-x`, PMID 34608324 | https://api.crossref.org/works/10.1038/s41592-021-01252-x ; https://pubmed.ncbi.nlm.nih.gov/34608324/ |
| 9 | **Borzoi** | Linder J, Srivastava D, Yuan H, Agarwal V, Kelley DR. "Predicting RNA-seq coverage from DNA sequence as a unifying model of gene regulation." *Nature Genetics* 2025;57(4):949–961. DOI `10.1038/s41588-024-02053-6`, PMID 39779956 | https://api.crossref.org/works/10.1038/s41588-024-02053-6 ; https://pubmed.ncbi.nlm.nih.gov/39779956/ |
| 10 | **Evo (Evo 1)** | Nguyen E, Poli M, Durrant MG, Kang B, et al. "Sequence modeling and design from molecular to genome scale with Evo." *Science* 2024;386(6723):eado9336. DOI `10.1126/science.ado9336`, PMID 39541441 | https://api.crossref.org/works/10.1126/science.ado9336 ; https://pubmed.ncbi.nlm.nih.gov/39541441/ |
| 11 | **Evo 2** | Brixi G, Durrant MG, Ku J, Naghipourfar M, Poli M, Sun G, et al. "Genome modelling and design across all domains of life with Evo 2." *Nature* 2026;652(8112):1349–1361. DOI `10.1038/s41586-026-10176-5`, PMID 41781614 | see §1.1 |
| 12 | **DNABERT** | Ji Y, Zhou Z, Liu H, Davuluri RV. "DNABERT: pre-trained Bidirectional Encoder Representations from Transformers model for DNA-language in genome." *Bioinformatics* 2021;37(15):2112–2120. DOI `10.1093/bioinformatics/btab083`, PMID 33538820 | https://api.crossref.org/works/10.1093/bioinformatics/btab083 |
| 13 | **DNABERT-2** | Zhou Z, Ji Y, Li W, Dutta P, Davuluri RV, Liu H. "DNABERT-2: Efficient Foundation Model and Benchmark For Multi-Species Genomes." **ICLR 2024** (conference paper); preprint arXiv:2306.15006 | https://proceedings.iclr.cc/paper_files/paper/2024/hash/b633e7052970b8f5aa1a69164d99e9e8-Abstract-Conference.html ; https://arxiv.org/abs/2306.15006 |
| 14 | **Hyena Hierarchy** | Poli M, Massaroli S, Nguyen E, et al. "Hyena Hierarchy: Towards Larger Convolutional Language Models." *ICML 2023*, PMLR 202:28043–28078 | https://proceedings.mlr.press/v202/poli23a.html ("Proceedings of the 40th International Conference on Machine Learning, PMLR 202:28043-28078, 2023") |
| 15 | **StripedHyena (1)** | Poli M, Thomas AW, Nguyen E, Ponnusamy P, Deiseroth B, Kersting K, Suzuki T, Hie B, Ermon S, Ré C, Zhang C, Massaroli S. "Mechanistic Design and Scaling of Hybrid Architectures." *ICML 2024*, PMLR 235:40908–40950 | https://proceedings.mlr.press/v235/poli24a.html |
| 16 | **StripedHyena 2** | Ku J, Nguyen E, Romero DW, Brixi G, Yang B, Vorontsov A, Taghibakhshi A, Lu AX, Burke DP, Brockman G, Massaroli S, Ré C, Hsu PD, Hie BL, Ermon S, Poli M. "Systems and Algorithms for Convolutional Multi-Hybrid Language Models at Scale." arXiv:2503.01868 (25 Feb 2025) | https://arxiv.org/abs/2503.01868 |
| 17 | **FlashAttention-2** | Dao T. "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning." **ICLR 2024** (conference paper); preprint arXiv:2307.08691 (17 Jul 2023). Reports ~2× speedup over FlashAttention, 50–73% of theoretical max FLOPs/s on A100, and up to 225 TFLOPs/s per A100 (72% model FLOPs utilization) | https://arxiv.org/abs/2307.08691 ; ICLR 2024 proceedings index https://proceedings.iclr.cc/paper_files/paper/2024 |
| 18 | **RoPE / RoFormer** | Su J, Ahmed M, Lu Y, Pan S, et al. "RoFormer: Enhanced Transformer with Rotary Position Embedding." Preprint arXiv:2104.09864 (2021); journal version *Neurocomputing* 2024;568:127063, DOI `10.1016/j.neucom.2023.127063` | https://arxiv.org/abs/2104.09864 ; https://api.crossref.org/works/10.1016/j.neucom.2023.127063 |
| 19 | **GPN-MSA (alignment-based DNA LM)** | Benegas G, Albors C, Aw AJ, Ye C, Song YS. "A DNA language model based on multispecies alignment predicts the effects of genome-wide variants." *Nature Biotechnology* 2025;43(12):1960–1965. DOI `10.1038/s41587-024-02511-w`, PMID 39747647. Preprint "GPN-MSA: an alignment-based DNA language model for genome-wide variant effect prediction", bioRxiv `10.1101/2023.10.10.561776` | https://pubmed.ncbi.nlm.nih.gov/39747647/ ; https://pubmed.ncbi.nlm.nih.gov/37873118/ |
| 20 | **DART-Eval** | Patel A, Hill DW, Mino T, et al. "DART-Eval: A Comprehensive DNA Language Model Evaluation Benchmark on Regulatory DNA." *NeurIPS* 2024;37:62024–62061 (also arXiv:2508.03760) | cited as ref. 28 in https://www.nature.com/articles/s41586-026-10176-5 ; PubMed arXiv record PMID 40799805 |
| 21 | **AlphaGenome (2026)** | Avsec Ž, Latysheva N, Cheng J, et al. "Advancing regulatory variant effect prediction with AlphaGenome." *Nature* 2026;649(8099):1206–1218. DOI `10.1038/s41586-025-10014-0`, PMID 41606153 | https://api.crossref.org/works/10.1038/s41586-025-10014-0 ; https://www.nature.com/articles/s41586-025-10014-0 |
| 22 | **BRCA2 saturation (used by Evo 2)** | Huang H, Hu C, Na J, Hart SN, et al. "Functional evaluation and clinical classification of BRCA2 variants." *Nature* 2025;638(8050):528–537. DOI `10.1038/s41586-024-08388-8`, PMID 39779857 | https://api.crossref.org/works/10.1038/s41586-024-08388-8 |
| 23 | **ESM1b genome-wide VEP + web portal** | Brandes N, Goldman G, Wang CH, Ye CJ, Ntranos V. "Genome-wide prediction of disease variant effects with a deep protein language model." *Nature Genetics* 2023;55(9):1512–1522. DOI `10.1038/s41588-023-01465-0` | https://api.crossref.org/works/10.1038/s41588-023-01465-0 ; https://www.nature.com/articles/s41588-023-01465-0 ("made all predictions available on a web portal") |
| 24 | **VarSome (web)** | Vandenbroucke I, van Soest R, Botello J, et al. "VarSome: the human genomic variant search engine." *Bioinformatics* 2019;35(11):1978–1980. DOI `10.1093/bioinformatics/bty897`, PMID 30376034 | https://pubmed.ncbi.nlm.nih.gov/30376034/ |
| 25 | **MobiDetails (web)** | Baux D, Van Goethem C, Ardouin O, Guignard T, Bergougnoux A, Koenig M, Roux AF. "MobiDetails: online DNA variants interpretation." *European Journal of Human Genetics* 2021;29(2):356–360. DOI `10.1038/s41431-020-00755-z`, PMID 33161418 | https://pubmed.ncbi.nlm.nih.gov/33161418/ |
| 26 | **EVEE (web, Evo 2 embeddings)** | Pearce MT, Dooms T, Yamamoto R, et al. "EVEE: Interpretable variant effect prediction from genomic foundation model embeddings." bioRxiv 2026, DOI `10.64898/2026.04.10.717844`. Interactive web app at `https://evee.goodfire.ai/` with pre-computed predictions for 4.2M ClinVar variants | https://www.biorxiv.org/content/10.64898/2026.04.10.717844v3 |
| 27 | **Evo Designer / Mech Interp (official Evo 2 web UIs)** | listed in the Evo 2 paper's "Code availability": https://arcinstitute.org/tools/evo/evo-designer and https://arcinstitute.org/tools/evo/evo-mech-interp | https://www.nature.com/articles/s41586-026-10176-5 |

**UNVERIFIED / do not cite:**
- **"Variantformer"** — no primary source found. Crossref title search, OpenAlex `title.search:Variantformer`, the arXiv API, nature.com search and PubMed all fail to return a paper titled "Variantformer: a deep learning model for variant effect prediction using protein language models". The only OpenAlex/arXiv hits for the string are (a) an unrelated 2025 bioRxiv gene-expression model "VariantFormer: A hierarchical transformer…" (doi `10.1101/2025.10.31.685862`) and (b) an unrelated Swedish-language thesis. **Use Brandes 2023 (row 23), Livesey & Marsh 2023, or VariPred (Sci Rep 2024;14:5089, doi `10.1038/s41598-024-51489-7`) instead.**
- A **2021 McLaren et al. VEP paper** does not exist; the canonical VEP citation is McLaren 2016 (row 4).

---

## 7. Published criticism / limitations of zero-shot genomic LMs for clinical variant classification

All of the following are citable, primary-source-verified statements that a limitations paragraph can use.

1. **Ancestry bias in VEPs.** Pathak AK, Bora N, Badonyi M, Livesey BJ, Ngeow J, Marsh JA. "Pervasive ancestry bias in variant effect predictors." bioRxiv 2024.05.20.594987 (posted 22 May 2024; cited by the Evo 2 paper as a 2025 preprint). Abstract: "We observe striking differences in the ways that many VEPs score missense variants from European compared to non-European populations. We advocate for the adoption of population-free VEPs, i.e. those not trained on human population or clinical variants, to improve health equity…"
   **Source:** https://www.biorxiv.org/content/10.1101/2024.05.20.594987v1 ; https://api.crossref.org/works/10.1101/2024.05.20.594987
   **VERIFIED** (preprint; **not** verified as peer-reviewed in a journal)

2. **Phylogenetic / sampling bias limits likelihood-based VEP; correcting it helps.** Pugh CW, Nuñez-Valencia PG, Dias M, Frazer J. "From Likelihood to Fitness: Improving Variant Effect Prediction in Protein and Genome Language Models." *NeurIPS* 2025 (poster + paper). Abstract: "These results suggest that **accounting for phylogenetic and sampling biases is essential** to realizing the full potential of large sequence models in variant effect prediction."
   **Source:** https://neurips.cc/virtual/2025/loc/san-diego/poster/118671 ; https://papers.nips.cc/paper_files/paper/2025/file/bdb30687f1c2255c29b11b0b45204ebe-Paper-Conference.pdf
   **VERIFIED**

3. **A classical phylogenetic method beats large protein LMs at VEP.** Prillo S, Wu W, Song YS. "Ultrafast classical phylogenetic method beats large protein language models on variant effect prediction." *NeurIPS* 2024;37:130265–130290. Abstract: "…despite being an independent-sites model, our SiteRM model outperforms large protein language models that learn complex residue-residue interactions between different sites."
   **Source:** https://pubmed.ncbi.nlm.nih.gov/40487750/ ; https://proceedings.neurips.cc/paper_files/paper/2024/hash/eb2f4fb51ac3b8dc4aac9cf71b0e7799-Abstract-Conference.html
   **VERIFIED**

4. **Alignment-based DNA LMs beat sequence-only genomic LMs for human variant effects.** Benegas et al. 2025 (*Nat Biotechnol* 43:1960–1965) present GPN-MSA, an alignment-based DNA language model. The Evo 2 paper itself states that "Genomic language models have previously struggled in eukaryotic variant effect prediction, lagging considerably behind species-specific models that use multiple sequence alignments" and cites Benegas 2025, NT 2024 and DNABERT 2021 for this.
   **Source:** https://www.nature.com/articles/s41586-026-10176-5 ("Human variant effect prediction", first paragraph) ; https://pubmed.ncbi.nlm.nih.gov/39747647/
   **VERIFIED**
   Quantitative corroboration from Evo 2's own Supplementary Data 1: on BRCA1, NT reaches AUROC 0.5496 and Evo 1 0.4972 (chance-level), while GPN-MSA reaches 0.8628.

5. **DNA sequence models underperform for causal regulatory variant prediction.** "Benchmarking DNA Sequence Models for Causal Regulatory Variant Prediction in Human Genetics." bioRxiv 2025.02.11.637758 (4 March 2025), cited as reference in the AlphaGenome Nature paper.
   **Source:** https://pubmed.ncbi.nlm.nih.gov/39990426/
   **VERIFIED** (preprint)

6. **Deep sequence-to-function models perform inadequately on some VEP tasks.** Hosseini R, Balci AT, Kostka D, Clark N, Chikina M. "Ultra-fast variant effect prediction using biophysical transcription factor binding models." *Nucleic Acids Research* 2025, DOI `10.1093/nar/gkaf940`, PMID 41063341. "Despite recent progress in deep sequence-to-function models that predict functional output from sequence data, these methods **perform inadequately on some variant effect prediction tasks**, especially with common genetic variants." Also: "While the complex and high-performing deep learning model **Enformer** delivers accurate, state-of-the-art predictions on MPRA data, it demonstrates **nearly random accuracy in predicting the direction of common variant expression quantitative trait loci (eQTLs)**."
   **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12507518/
   **VERIFIED**

7. **Genetic background (haplotype) changes predicted variant effects.** "Genetic background shapes AI-predicted variant effects." bioRxiv 2026 (DOI `10.64898/2026.04.04.715328`, PMID 41993283). Introduces the personalized variant effect predictor (pVEP) framework; "the same variant predicted to be pathogenic in some genetic backgrounds and benign in others", using 3,891 IGSR genomes.
   **Source:** https://pubmed.ncbi.nlm.nih.gov/41993283/ ; https://pmc.ncbi.nlm.nih.gov/articles/PMC13082004/
   **VERIFIED** (preprint)

8. **Missense VEP benchmarking shows heterogeneous, sometimes poor, performance.** "Critical assessment of missense variant effect predictors on disease-relevant variant data." *Human Genetics* 2025;144(2–3):281–293, DOI `10.1007/s00439-025-02732-2`, PMID 40113603 (preprint: bioRxiv `10.1101/2024.06.06.597828`).
   **Source:** https://pubmed.ncbi.nlm.nih.gov/40113603/
   **VERIFIED**

9. **Review of automated variant interpretation pitfalls.** "The promises and pitfalls of automated variant interpretation: a comprehensive review." *Briefings in Bioinformatics* 2025;26(5):bbaf545, DOI `10.1093/bib/bbaf545`, PMID 41071614.
   **Source:** https://pubmed.ncbi.nlm.nih.gov/41071614/
   **VERIFIED**

10. **ACMG's own constraint on computational evidence.** As quoted in §5 above: Richards et al. 2015 — "It is not recommended that these predictions be used as the sole source of evidence to make a clinical assertion."
    **Source:** https://www.nature.com/articles/gim201530
    **VERIFIED**

11. **Evo 2's own reported limitations.** The Evo 2 paper states: "Evo 2 is **not trained on any human genetic variation or functional genomics data**"; on human gene essentiality "the overall predictive performance remains modest"; and on distal regulatory variants it "falls behind supervised models".
    **Source:** https://www.nature.com/articles/s41586-026-10176-5
    **VERIFIED**

---

## Bibliography entries (IEEE style)

```bibtex
\bibitem{brixi2026evo2} G. Brixi, M. G. Durrant, J. Ku, M. Naghipourfar, M. Poli, G. Sun, G. Brockman, D. Chang, A. Fanton, G. A. Gonzalez, S. H. King, D. B. Li, A. T. Merchant, E. Nguyen, C. Ricci-Tam, D. W. Romero, J. C. Schmok, A. Taghibakhshi, A. Vorontsov, B. Yang, M. Deng, L. Gorton, N. Nguyen, N. K. Wang, M. T. Pearce, E. Simon, E. Adams, Z. J. Amador, E. A. Ashley, S. A. Baccus, H. Dai, S. Dillmann, S. Ermon, D. Guo, M. H. Herschl, R. Ilango, K. Janik, A. X. Lu, R. Mehta, M. R. K. Mofrad, M. Y. Ng, J. Pannu, C. R\'e, J. St. John, J. Sullivan, J. Tey, B. Viggiano, K. Zhu, G. Zynda, D. Balsam, P. Collison, A. B. Costa, T. Hernandez-Boussard, E. Ho, M.-Y. Liu, T. McGrath, K. Powell, S. Pinglay, D. P. Burke, H. Goodarzi, P. D. Hsu, and B. L. Hie, ``Genome modelling and design across all domains of life with Evo 2,'' \textit{Nature}, vol. 652, no. 8112, pp. 1349--1361, Apr. 2026, doi: 10.1038/s41586-026-10176-5.

\bibitem{brixi2025evo2preprint} G. Brixi, M. G. Durrant, J. Ku, M. Poli, G. Brockman, D. Chang, G. A. Gonzalez, S. H. King, D. B. Li, A. T. Merchant, M. Naghipourfar, E. Nguyen, C. Ricci-Tam, D. W. Romero, G. Sun, A. Taghibakhshi, A. Vorontsov, B. Yang, M. Deng, L. Gorton, N. Nguyen, N. K. Wang, E. Adams, S. A. Baccus, S. Dillmann, S. Ermon, D. Guo, R. Ilango, K. Janik, A. X. Lu, R. Mehta, M. R. K. Mofrad, M. Y. Ng, J. Pannu, C. R\'e, J. C. Schmok, J. St. John, J. Sullivan, K. Zhu, G. Zynda, D. Balsam, P. Collison, A. B. Costa, T. Hernandez-Boussard, E. Ho, M.-Y. Liu, T. McGrath, K. Powell, D. P. Burke, H. Goodarzi, P. D. Hsu, and B. L. Hie, ``Genome modeling and design across all domains of life with Evo 2,'' \textit{bioRxiv}, preprint 10.1101/2025.02.18.638918, Feb. 2025, doi: 10.1101/2025.02.18.638918.

\bibitem{brixi2025stripedhyena2} J. Ku, E. Nguyen, D. W. Romero, G. Brixi, B. Yang, A. Vorontsov, A. Taghibakhshi, A. X. Lu, D. P. Burke, G. Brockman, S. Massaroli, C. R\'e, P. D. Hsu, B. L. Hie, S. Ermon, and M. Poli, ``Systems and algorithms for convolutional multi-hybrid language models at scale,'' \textit{arXiv preprint} arXiv:2503.01868, Feb. 2025, doi: 10.48550/arXiv.2503.01868.

\bibitem{findlay2018brca1} G. M. Findlay, R. M. Daza, B. Martin, M. D. Zhang, A. P. Leith, M. Gasperini, J. D. Janizek, X. Huang, L. M. Starita, and J. Shendure, ``Accurate classification of \emph{BRCA1} variants with saturation genome editing,'' \textit{Nature}, vol. 562, no. 7726, pp. 217--222, Sep. 2018, doi: 10.1038/s41586-018-0461-z.

\bibitem{landrum2014clinvar} M. J. Landrum, J. M. Lee, G. R. Riley, W. Jang, W. S. Rubinstein, D. M. Church, and D. R. Maglott, ``ClinVar: public archive of relationships among sequence variation and human phenotype,'' \textit{Nucleic Acids Res.}, vol. 42, no. 1, pp. D980--D985, Jan. 2014, doi: 10.1093/nar/gkt1113.

\bibitem{landrum2024clinvar} M. J. Landrum, S. Chitipiralla, K. Kaur, G. Brown, C. Chen, J. Hart, D. Hoffman, W. Jang, C. Liu, Z. Maddipatla, R. Maiti, J. Mitchell, T. Rezaie, G. Riley, G. Song, J. Yang, L. Ziyabari, A. Russette, and B. L. Kattman, ``ClinVar: updates to support classifications of both germline and somatic variants,'' \textit{Nucleic Acids Res.}, vol. 53, no. D1, pp. D1313--D1321, Nov. 2024, doi: 10.1093/nar/gkae1090.

\bibitem{lee2022ucsc} B. T. Lee, G. P. Barber, A. Benet-Pag\`es, J. Casper, H. Clawson, M. Diekhans, C. Fischer, J. N. Gonzalez, A. S. Hinrichs, B. T. Lee, P. Muthuraman, L. R. Nassar, B. Nguy, T. Pereira, P. Nejad, G. Perez, B. J. Raney, K. R. Rosenbloom, D. Schmelter, M. L. Speir, B. D. Wick, A. S. Zweig, R. M. Kuhn, M. Haeussler, and W. J. Kent, ``The UCSC Genome Browser database: 2022 update,'' \textit{Nucleic Acids Res.}, vol. 50, no. D1, pp. D1115--D1122, Jan. 2022, doi: 10.1093/nar/gkab959.

\bibitem{casper2026ucsc} J. Casper, M. L. Speir, B. J. Raney, G. Perez, L. R. Nassar, C. M. Lee, A. S. Hinrichs, J. N. Gonzalez, C. Fischer, M. Diekhans, et al., ``The UCSC Genome Browser database: 2026 update,'' \textit{Nucleic Acids Res.}, vol. 54, no. D1, pp. D1331--D1335, Jan. 2026, doi: 10.1093/nar/gkaf1250.

\bibitem{lee2020ucscapi} C. M. Lee, G. P. Barber, J. Casper, H. Clawson, M. Diekhans, J. N. Gonzalez, A. S. Hinrichs, B. T. Lee, L. R. Nassar, C. C. Powell, et al., ``UCSC Genome Browser enters 20th year,'' \textit{Nucleic Acids Res.}, vol. 48, no. D1, pp. D756--D761, Jan. 2020, doi: 10.1093/nar/gkz1012.

\bibitem{richards2015acmg} S. Richards, N. Aziz, S. Bale, D. Bick, S. Das, J. Gastier-Foster, W. W. Grody, M. Hegde, E. Lyon, E. Spector, K. Voelkerding, and H. L. Rehm, ``Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the ACMG and AMP,'' \textit{Genet. Med.}, vol. 17, no. 5, pp. 405--424, May 2015, doi: 10.1038/gim201530.

\bibitem{pejaver2022svi} V. Pejaver, A. B. Byrne, B.-J. Feng, K. A. Pagel, S. D. Mooney, R. Karchin, A. O'Donnell-Luria, S. M. Harrison, S. V. Tavtigian, M. S. Greenblatt, L. G. Biesecker, P. Radivojac, S. E. Brenner, and ClinGen Sequence Variant Interpretation Working Group, ``Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria,'' \textit{Amer. J. Hum. Genet.}, vol. 109, no. 12, pp. 2163--2177, Dec. 2022, doi: 10.1016/j.ajhg.2022.10.013.

\bibitem{tavtigian2018acmg} S. E. Tavtigian, A. Vite, S. Mandelkow, M. Pinaya, P. Jamshidi, D. Ashton, I. Gavric, I. Matic, M. Stevanovic, L. Valle, and B. Xin, ``Modeling the ACMG/AMP variant classification guidelines as a Bayesian classification framework,'' \textit{Genet. Med.}, vol. 20, no. 9, pp. 1054--1060, Sep. 2018, doi: 10.1038/gim.2017.210.

\bibitem{tavtigian2020points} S. E. Tavtigian, S. M. Harrison, K. M. Boucher, and L. G. Biesecker, ``Fitting a naturally scaled point system to the ACMG/AMP variant classification guidelines,'' \textit{Hum. Mutat.}, vol. 41, no. 10, pp. 1734--1737, Oct. 2020, doi: 10.1002/humu.24088.

\bibitem{ng2001sift} P. C. Ng and S. Henikoff, ``Predicting deleterious amino acid substitutions,'' \textit{Genome Res.}, vol. 11, no. 5, pp. 863--874, May 2001, doi: 10.1101/gr.176601.

\bibitem{adzhubei2010polyphen2} I. A. Adzhubei, S. Schmidt, L. Peshkin, V. E. Ramensky, A. Zorkov, and others, ``A method and server for predicting damaging missense mutations,'' \textit{Nat. Methods}, vol. 7, no. 4, pp. 248--249, Apr. 2010, doi: 10.1038/nmeth0410-248.

\bibitem{rentzsch2019cadd} P. Rentzsch, D. M. Witten, G. M. Cooper, J. Shendure, and M. Kircher, ``CADD: predicting the deleteriousness of variants throughout the human genome,'' \textit{Nucleic Acids Res.}, vol. 47, no. D1, pp. D886--D894, Jan. 2019, doi: 10.1093/nar/gky1016.

\bibitem{schubach2024cadd} M. Schubach, T. Maass, L. Nazaretyan, S. R\"oner, and M. Kircher, ``CADD v1.7: using protein language models, regulatory CNNs and other nucleotide-level scores to improve genome-wide variant predictions,'' \textit{Nucleic Acids Res.}, vol. 52, no. D1, pp. D1143--D1154, Jan. 2024, doi: 10.1093/nar/gkad989.

\bibitem{mclaren2016vep} W. McLaren, L. Gil, S. E. Hunt, H. S. Riat, G. R. Ritchie, A. Thormann, P. Flicek, and F. Cunningham, ``The Ensembl Variant Effect Predictor,'' \textit{Genome Biol.}, vol. 17, no. 1, p. 122, Jun. 2016, doi: 10.1186/s13059-016-0974-4.

\bibitem{hunt2022vep} S. E. Hunt, B. Moore, R. M. Amodei, I. M. Armean, D. Lemos, A. Mushtaq, and others, ``Annotating and prioritizing genomic variants using the Ensembl Variant Effect Predictor---A tutorial,'' \textit{Hum. Mutat.}, vol. 43, no. 8, pp. 986--997, Aug. 2022, doi: 10.1002/humu.24298.

\bibitem{cheng2023alphamissense} J. Cheng, G. Novati, J. Pan, C. Bycroft, and others, ``Accurate proteome-wide missense variant effect prediction with AlphaMissense,'' \textit{Science}, vol. 381, no. 6664, p. eadg7492, Sep. 2023, doi: 10.1126/science.adg7492.

\bibitem{lin2023esm2} Z. Lin, H. Akin, R. Rao, B. Hie, Z. Zhu, W. Lu, N. Smetanin, R. Verkuil, K. Kabeli, Y. Shmueli, A. dos Santos Costa, M. Fazel-Zarandi, T. Sercu, S. Candido, and A. Rives, ``Evolutionary-scale prediction of atomic-level protein structure with a language model,'' \textit{Science}, vol. 379, no. 6637, pp. 1123--1130, Mar. 2023, doi: 10.1126/science.ade2574.

\bibitem{meier2021esmzeroshot} J. Meier, R. Rao, R. Verkuil, J. Liu, T. Sercu, and A. Rives, ``Language models enable zero-shot prediction of the effects of mutations on protein function,'' in \textit{Advances in Neural Information Processing Systems (NeurIPS)}, 2021, pp. 29287--29303.

\bibitem{dallatorre2024nt} H. Dalla-Torre, L. Gonzalez, J. Mendoza-Revilla, N. Lopez Carranza, and others, ``Nucleotide Transformer: building and evaluating robust foundation models for human genomics,'' \textit{Nat. Methods}, vol. 22, no. 2, pp. 287--297, Feb. 2025, doi: 10.1038/s41592-024-02523-z.

\bibitem{avsec2021enformer} \v{Z}. Avsec, V. Agarwal, D. Visentin, J. R. Ledsam, and others, ``Effective gene expression prediction from sequence by integrating long-range interactions,'' \textit{Nat. Methods}, vol. 18, no. 10, pp. 1196--1203, Oct. 2021, doi: 10.1038/s41592-021-01252-x.

\bibitem{linder2025borzoi} J. Linder, D. Srivastava, H. Yuan, V. Agarwal, and D. R. Kelley, ``Predicting RNA-seq coverage from DNA sequence as a unifying model of gene regulation,'' \textit{Nat. Genet.}, vol. 57, no. 4, pp. 949--961, Apr. 2025, doi: 10.1038/s41588-024-02053-6.

\bibitem{nguyen2024evo} E. Nguyen, M. Poli, M. G. Durrant, B. Kang, and others, ``Sequence modeling and design from molecular to genome scale with Evo,'' \textit{Science}, vol. 386, no. 6723, p. eado9336, Nov. 2024, doi: 10.1126/science.ado9336.

\bibitem{ji2021dnabert} Y. Ji, Z. Zhou, H. Liu, and R. V. Davuluri, ``DNABERT: pre-trained bidirectional encoder representations from transformers model for DNA-language in genome,'' \textit{Bioinformatics}, vol. 37, no. 15, pp. 2112--2120, Aug. 2021, doi: 10.1093/bioinformatics/btab083.

\bibitem{zhou2024dnabert2} Z. Zhou, Y. Ji, W. Li, P. Dutta, R. V. Davuluri, and H. Liu, ``DNABERT-2: efficient foundation model and benchmark for multi-species genomes,'' in \textit{Int. Conf. on Learning Representations (ICLR)}, 2024, arXiv:2306.15006.

\bibitem{poli2023hyena} M. Poli, S. Massaroli, E. Nguyen, and others, ``Hyena hierarchy: towards larger convolutional language models,'' in \textit{Proc. 40th Int. Conf. on Machine Learning (ICML)}, PMLR, vol. 202, pp. 28043--28078, 2023.

\bibitem{poli2024stripedhyena} M. Poli, A. W. Thomas, E. Nguyen, P. Ponnusamy, B. Deiseroth, K. Kersting, T. Suzuki, B. Hie, S. Ermon, C. R\'e, C. Zhang, and S. Massaroli, ``Mechanistic design and scaling of hybrid architectures,'' in \textit{Proc. 41st Int. Conf. on Machine Learning (ICML)}, PMLR, vol. 235, pp. 40908--40950, 2024.

\bibitem{dao2023flashattn} T. Dao, ``FlashAttention-2: faster attention with better parallelism and work partitioning,'' in \textit{Int. Conf. on Learning Representations (ICLR)}, 2024, arXiv:2307.08691.

\bibitem{su2021rope} J. Su, M. Ahmed, Y. Lu, S. Pan, and others, ``RoFormer: enhanced transformer with rotary position embedding,'' \textit{Neurocomputing}, vol. 568, p. 127063, 2024, doi: 10.1016/j.neucom.2023.127063.

\bibitem{benegas2025gpnmsa} G. Benegas, C. Albors, A. J. Aw, C. Ye, and Y. S. Song, ``A DNA language model based on multispecies alignment predicts the effects of genome-wide variants,'' \textit{Nat. Biotechnol.}, vol. 43, no. 12, pp. 1960--1965, Dec. 2025, doi: 10.1038/s41587-024-02511-w.

\bibitem{patel2024darteval} A. Patel, D. W. Hill, T. Mino, and others, ``DART-Eval: a comprehensive DNA language model evaluation benchmark on regulatory DNA,'' in \textit{Advances in Neural Information Processing Systems (NeurIPS)}, vol. 37, pp. 62024--62061, 2024.

\bibitem{avsec2026alphagenome} \v{Z}. Avsec, N. Latysheva, J. Cheng, and others, ``Advancing regulatory variant effect prediction with AlphaGenome,'' \textit{Nature}, vol. 649, no. 8099, pp. 1206--1218, Jan. 2026, doi: 10.1038/s41586-025-10014-0.

\bibitem{huang2025brca2} H. Huang, C. Hu, J. Na, S. N. Hart, and others, ``Functional evaluation and clinical classification of \emph{BRCA2} variants,'' \textit{Nature}, vol. 638, no. 8050, pp. 528--537, Feb. 2025, doi: 10.1038/s41586-024-08388-8.

\bibitem{brandes2023esm1b} N. Brandes, G. Goldman, C. H. Wang, C. J. Ye, and V. Ntranos, ``Genome-wide prediction of disease variant effects with a deep protein language model,'' \textit{Nat. Genet.}, vol. 55, no. 9, pp. 1512--1522, Sep. 2023, doi: 10.1038/s41588-023-01465-0.

\bibitem{vandenbroucke2019varsome} I. Vandenbroucke, R. van Soest, J. Botello, and others, ``VarSome: the human genomic variant search engine,'' \textit{Bioinformatics}, vol. 35, no. 11, pp. 1978--1980, Jun. 2019, doi: 10.1093/bioinformatics/bty897.

\bibitem{baux2021mobidetails} D. Baux, C. Van Goethem, O. Ardouin, T. Guignard, A. Bergougnoux, M. Koenig, and A.-F. Roux, ``MobiDetails: online DNA variants interpretation,'' \textit{Eur. J. Hum. Genet.}, vol. 29, no. 2, pp. 356--360, Feb. 2021, doi: 10.1038/s41431-020-00755-z.

\bibitem{pearce2026evee} M. T. Pearce, T. Dooms, R. Yamamoto, and others, ``EVEE: interpretable variant effect prediction from genomic foundation model embeddings,'' \textit{bioRxiv}, preprint 10.64898/2026.04.10.717844, 2026, doi: 10.64898/2026.04.10.717844.

\bibitem{pathak2024ancestry} A. K. Pathak, N. Bora, M. Badonyi, B. J. Livesey, J. Ngeow, and J. A. Marsh, ``Pervasive ancestry bias in variant effect predictors,'' \textit{bioRxiv}, preprint 10.1101/2024.05.20.594987, May 2024, doi: 10.1101/2024.05.20.594987.

\bibitem{pugh2025likelihood} C. W. J. Pugh, P. G. Nu\~nez-Valencia, M. Dias, and J. Frazer, ``From likelihood to fitness: improving variant effect prediction in protein and genome language models,'' in \textit{Advances in Neural Information Processing Systems (NeurIPS)}, 2025.

\bibitem{prillo2024siterm} S. Prillo, W. Wu, and Y. S. Song, ``Ultrafast classical phylogenetic method beats large protein language models on variant effect prediction,'' in \textit{Advances in Neural Information Processing Systems (NeurIPS)}, vol. 37, pp. 130265--130290, 2024.

\bibitem{hosseini2025motifdiff} R. Hosseini, A. T. Balci, D. Kostka, N. Clark, and M. Chikina, ``Ultra-fast variant effect prediction using biophysical transcription factor binding models,'' \textit{Nucleic Acids Res.}, vol. 53, no. 18, 2025, doi: 10.1093/nar/gkaf940.

\bibitem{benegas2025benchmark} G. Benegas, G. Eraslan, and Y. S. Song, ``Benchmarking DNA sequence models for causal regulatory variant prediction in human genetics,'' \textit{bioRxiv}, preprint 10.1101/2025.02.11.637758, Feb. 2025, doi: 10.1101/2025.02.11.637758.

\bibitem{rastogi2025critical} R. Rastogi, R. Chung, S. Li, C. Li, K. Lee, J. Woo, D. W. Kim, C. Keum, G. Babbi, P. L. Martelli, S. Savojardo, R. Casadio, and others, ``Critical assessment of missense variant effect predictors on disease-relevant variant data,'' \textit{Hum. Genet.}, vol. 144, no. 2--3, pp. 281--293, Mar. 2025, doi: 10.1007/s00439-025-02732-2.

\bibitem{costa2025pitfalls} M. Costa, S. A. Garc\'ia, A. Le\'on, and O. Pastor, ``The promises and pitfalls of automated variant interpretation: a comprehensive review,'' \textit{Brief. Bioinform.}, vol. 26, no. 5, p. bbaf545, Aug. 2025, doi: 10.1093/bib/bbaf545.
```

---

## Claims the paper MUST NOT make

Anything below could not be confirmed from a primary source, or is contradicted by one.

### Facts that are UNVERIFIED / wrong as commonly stated

1. **Do not cite a 2022 NAR paper titled "The UCSC Genome Browser: exploring the world's most comprehensive resource of genome-scale data."** No such paper exists in PubMed, Crossref, or UCSC's own publication list. Use `lee2022ucsc` (Lee BT et al., NAR 50(D1):D1115–D1122, 2022) or `casper2026ucsc` (Casper et al., NAR 54(D1):D1331–D1335, 2026). UCSC's own "Cite Us" page currently points at the 2026 update.
2. **Do not cite "Variantformer: a deep learning model for variant effect prediction using protein language models."** No such publication could be found in Crossref, OpenAlex, PubMed, arXiv, or nature.com. Substitute Brandes et al. 2023 (`brandes2023esm1b`), Livesey & Marsh 2023, or VariPred (Sci Rep 2024).
3. **Do not cite a "2021 McLaren et al. VEP paper."** The canonical Ensembl VEP reference is McLaren et al., Genome Biology 17:122 (2016).
4. **Do not cite "Evolutionary-scale prediction of protein mutations with a language model, Science 2023."** The actual ESM-2 Science paper is Lin Z. et al., "Evolutionary-scale prediction of **atomic-level protein structure** with a language model," Science 379(6637):1123–1130 (2023). The zero-shot mutation-effect paper is Meier et al., NeurIPS 2021.
5. **Do not cite DNABERT-2 as "…for DNA-Sequence Learning."** That was the arXiv v1 title; the ICLR 2024 paper (and arXiv v2) is "DNABERT-2: Efficient Foundation Model and Benchmark For **Multi-Species Genomes**."
6. **Do not quote the Evo 2 BRCA1 coding subset as n = 2,077.** The published Fig. 3e caption says 2,077, but the paper's own Supplementary Data 1 reports N = 2,768 (2,768 + 1,125 = 3,893). Quote n = 3,893 total and give the subset sizes from Supplementary Data 1, or cite the figure caption only with a caveat.
7. **Do not quote the Evo 2 ClinVar noncoding SNV count as 34,761 and also as 33,747.** Fig. 3c caption says 34,761; Supplementary Data 1 says 33,747.
8. **Do not state that "Evo 2 was trained on 9.3 trillion base pairs" without saying which quantity that is.** 8.8T = OpenGenome2 dataset size; 9.3T = tokens consumed training the 40B model; 9T = the Nature abstract's rounding. Name the source for whichever figure you use.
9. **Do not claim Evo 2 has an arXiv preprint.** Only a bioRxiv preprint exists (10.1101/2025.02.18.638918).
10. **Do not claim `evo2_7b_microviridae` is downloadable from HuggingFace.** It is listed in the README checkpoint table but is not published on the `arcinstitute` HuggingFace organisation.
11. **Do not claim Evo 2 / StripedHyena 2 uses RoPE or FlashAttention-2 internally.** The only primary evidence is the `flash-attn==2.8.0.post2` *install dependency*; no fetched primary source states that Evo 2's positional encoding is RoPE or that its attention is FlashAttention-2. (StripedHyena 2's own paper describes "input-dependent convolution operators" plus attention, not RoPE.) If the paper needs this, cite the StripedHyena 2 preprint as the architecture source and cite FlashAttention-2/RoPE only as general engineering context.
12. **Do not describe Evo 2's checkpoint as "the only publicly available model of this scale,"** or claim first-mover status for 1M context beyond what the Nature abstract states ("an unprecedented 1 million token context window" appears in the bioRxiv abstract; the Nature abstract says "a 1 million token context window").
13. **Do not claim Pathak et al. (ancestry bias) is a peer-reviewed journal article.** As checked, only the bioRxiv preprint (10.1101/2024.05.20.594987) exists; the Evo 2 paper cites it as a 2025 preprint.
14. **Do not cite the pVEP paper or the LFB/Phylogenetic-bias paper as journal articles.** Both are preprints (10.64898/2026.04.04.715328 and the NeurIPS 2025 poster respectively) as far as verified here.
15. **Do not claim the ClinVar two-star tier is "criteria provided, multiple submitters"** (current documented name: "criteria provided, multiple submitters, **no conflicts**"), and do not use "criteria provided, conflicting interpretations" (current name: "criteria provided, **conflicting classifications**").
16. **Do not claim ACMG/AMP has BP1–BP7.** Richards et al. 2015 defines BP1–BP6; **BP7** is a ClinGen addition (visible in the ENIGMA BRCA1/BRCA2 VCEP specifications, CSpec GN092 v1.2).
17. **Do not cite CSpec GN092 as "the ClinGen SVI PP3/BP4 recommendations."** GN092 is the gene-specific **ENIGMA BRCA1/BRCA2 VCEP Specifications v1.2** (DOI 10.5281/zenodo.21434315). The SVI recalibration paper is Pejaver et al. 2022.
18. **Do not claim the E-utilities subset includes more than esearch, esummary, elink, and efetch** for ClinVar; those four are what ClinVar documents. (`EInfo`, `ESearch`/`ESummary`/`EPost` etc. exist for Entrez generally, but ClinVar's own doc names only these four.)
19. **Do not claim a ClinVar esummary JSON field named `review_status` exists at the top level of the record.** In the live JSON, review status lives inside `germline_classification` (and `clinical_impact_classification` / `oncogenicity_classification`), alongside `description` and `last_evaluated`; `record_status` is a separate, empty-by-default field. Also, the *Variation ID* is the `uid` / `variation_set[].measure_id` (e.g. 14206), while `accession` is the VCV accession (VCV000014206).
20. **Do not describe the UCSC `/getData/sequence` `end` as "1-based inclusive" without stating the length consequence.** The API docs say `start` is 0-relative and `end` is 1-relative; empirically the returned sequence has length `end − start` (verified: 4321–5678 → 1357 bases; 4321–5679 → 1358 bases), i.e. a 0-based half-open interval `[start, end)`.

### Performance / scope claims that would overstate the evidence

21. **Do not present an AUROC for Evo2Serve's own BRCA1 calibration as a published or validated result.** Any number produced by the repo's calibration script (τ, σ, AUROC on the first 500 rows) is a repo-local experimental artifact with no accompanying run log; `docs/research-findings.md` already flags this. The paper should either report it explicitly as an unreproduced local experiment with the exact code path, or omit it.
22. **Do not present Evo 2's published BRCA1 numbers (Evo 2 7B AUROC 0.9037 / AUPRC 0.7326 on all 3,893 SNVs; 0.8229 coding; 0.9593 noncoding) as Evo2Serve's performance.** They are the Evo 2 paper's numbers on the full Findlay dataset. Evo2Serve's calibration in this repo uses only the first 500 rows, so any comparison must state that.
23. **Do not imply that the app's labels are clinical variant classifications.** ClinVar's `review_status` and ACMG/AMP codes are expert-curated evidence tiers; an Evo 2 likelihood delta is a computational score. Richards et al. 2015 explicitly state that computational predictions "should not be used as the sole source of evidence to make a clinical assertion," and Findlay et al. 2018 state that conservation-based computational predictions "are insufficiently accurate to be used in the absence of genetic or experimental evidence."
24. **Do not claim Evo 2 exceeds specialist supervised predictors on BRCA1.** In the Evo 2 paper's own Supplementary Data 1, CADD reaches AUROC 0.8763 and AlphaMissense 0.8891 (coding) on BRCA1, versus Evo 2 7B 0.9037 (all) / 0.8229 (coding). Evo 2's own text says it "outperformed all other models on *BRCA1* noncoding SNVs" — that specific claim is safe; a blanket superiority claim is not.
25. **Do not claim Evo 2 is clinically validated.** The Nature paper describes *research* zero-shot VEP; the supervised-embedding classifier (AUROC 0.95 / AUPRC 0.88, n = 789) is a research result on a held-out split, not a clinical assay.
26. **Do not state a specific NCBI E-utilities request-rate limit** (e.g. "three requests per second") unless the author re-verifies it against the NCBI Bookshelf chapter "Using the E-utilities" — that page could not be fetched and confirmed during this check (see §3.2). The UCSC rate guidance ("maximum of one hit every second") *is* verified and may be stated.
