# Research Findings — Variant Analysis (Evo2) Project

Primary-source-only publication research. Every claim below cites the source that owns it
(official docs, source code, specs, first-party APIs). Claims that could not be verified
from a primary source are marked **UNVERIFIED**.

Repo under study: `C:\Users\vishw\OneDrive\Desktop\variant-analysis-evo2`
(Next.js frontend + Modal H100 backend running Evo2-7B for BRCA1 SNV scoring).

---

## 1. Model (Evo2)

### 1.1 Identity, architecture, context length
- Evo2 is "a state of the art DNA language model for long context modeling and design" that
  "models DNA sequences at single-nucleotide resolution at up to 1 million base pair context
  length using the StripedHyena 2 architecture" and "was trained autoregressively on
  OpenGenome2."
  Source: https://github.com/ArcInstitute/evo2 (README)
- StripedHyena 2 is described as a convolutional multi-hybrid architecture combining
  input-dependent convolution operators with attention (Nature paper page as surfaced in
  search; full text paywalled — architectural detail beyond the README so marked
  **UNVERIFIED** from a directly fetched primary source).
- The Evo2 preprint abstract states: "We train Evo 2 with 7B and 40B parameters to have an
  unprecedented 1 million token context window with single-nucleotide resolution" and that
  "Evo 2 learns from DNA sequence alone to accurately predict the functional impacts of
  genetic variation … without task-specific finetuning."
  Source: https://www.biorxiv.org/content/10.1101/2025.02.18.638918v1
- Published version: Brixi et al., "Genome modelling and design across all domains of life
  with Evo 2", Nature (2026), doi:10.1038/s41586-026-10176-5.
  Source: https://github.com/ArcInstitute/evo2 (README citation block)

### 1.2 Training data scale (note a primary-source discrepancy)
- GitHub README: OpenGenome2 "containing 8.8 trillion tokens from all domains of life."
  Source: https://github.com/ArcInstitute/evo2
- Hugging Face dataset card: "Total size: 8.8 trillion base pairs", "nearly 9 trillion base
  pairs of curated DNA"; two-stage training (Phase 1 pretraining at shorter length,
  Phase 2 context extension with tagged/long genomes).
  Source: https://huggingface.co/datasets/arcinstitute/opengenome2
- Preprint abstract: "trained on 9.3 trillion DNA base pairs."
  Source: https://www.biorxiv.org/content/10.1101/2025.02.18.638918v1
- Finding: 8.8T (code/dataset card) vs 9.3T (preprint abstract) differ across primary
  sources; do not quote a single number without naming the source.

### 1.3 Model sizes and context variants
- Checkpoints hosted on Hugging Face (`arcinstitute` org):
  `evo2_40b` (40B, 1M), `evo2_20b` (20B, 1M), `evo2_7b` (7B, 1M),
  `evo2_40b_base` (40B, 8K), `evo2_7b_base` (7B, 8K), `evo2_1b_base` (1B, 8K),
  `evo2_7b_262k` (7B, 262K), `evo2_7b_microviridae` (fine-tune).
  Source: https://github.com/ArcInstitute/evo2 (Checkpoints table)
- "8k pretrain" framing: the `_base` checkpoints are the 8K-context models; the 1M-context
  models are context-extended. Corroborated by the two-phase composition table.
  Sources: https://github.com/ArcInstitute/evo2 ;
  https://huggingface.co/datasets/arcinstitute/opengenome2
- Hardware mapping: 7B models run in bfloat16 without Transformer Engine/FP8 hardware;
  40B/20B/1B require FP8 via Transformer Engine on Hopper GPUs; "The 40B model requires
  multiple H100 GPUs."
  Source: https://github.com/ArcInstitute/evo2 (Requirements + Checkpoints note)

### 1.4 Zero-shot BRCA1 scoring method (the method this repo reimplements)
From the official Evo2 BRCA1 notebook (`notebooks/brca1/brca1_zero_shot_vep.ipynb`):
- Dataset loaded from `notebooks/brca1/41586_2018_461_MOESM3_ESM.xlsx` (Findlay et al.
  supplement), columns `chromosome / position (hg19) / reference / alt /
  function.score.mean / func.class`; `FUNC`+`INT` merged into `FUNC/INT` vs `LOF`.
- Reference: GRCh37 chr17 FASTA (`GRCh37.p13_chr17.fna.gz`); window `WINDOW_SIZE = 8192`
  centered on the variant (4096 bp each side, edge-clamped); variant sequence = window
  with single-base substitution; asserts lengths equal and ref/alt bases check out.
- Scoring: `model.score_sequences(ref_seqs)` and `model.score_sequences(var_seqs)` (unique
  refs deduplicated, 1326 refs / 3893 variants in the notebook run); delta =
  `var_score − ref_score[index]`; "the lower the delta, the more likely that the SNV is
  disruptive"; evaluated against classes by distribution/ stripplot and ROC AUC
  (`sklearn.metrics.roc_auc_score`).
  Source (raw notebook):
  https://raw.githubusercontent.com/ArcInstitute/evo2/main/notebooks/brca1/brca1_zero_shot_vep.ipynb
- This repo's reimplementation: 8192-bp window, `model.score_sequences` twice per unique
  case, ROC on −Δ, hard-coded τ/σ loaded from the BRCA1 run.
  Sources (repo-local): `paper-ieee.tex:220-240,305` ;
  `evo2-backend/main.py:292-310,452-470`

### 1.5 Efficiency primitives (RoPE, FlashAttention-2)
- FlashAttention-2: exact attention with IO-awareness; ~2× over FlashAttention-1 via
  reduced non-matmul FLOPs, parallelization across thread blocks, warp-level work
  partitioning; up to 225 TFLOPs/s per A100 (72% utilization) for GPT-style training.
  Source: https://arxiv.org/abs/2307.08691 (Dao, 2023 — author-owned preprint page)
- Evo2's install pins `flash-attn==2.8.0.post2`.
  Source: https://github.com/ArcInstitute/evo2 (Installation)
- RoPE: encodes absolute position with a rotation matrix while injecting explicit relative
  position dependence into self-attention; properties include flexible sequence length and
  decaying inter-token dependency with distance.
  Source: https://arxiv.org/abs/2104.09864 (Su et al., RoFormer — author-owned preprint page)
- **UNVERIFIED**: that Evo2/StripedHyena2 itself uses RoPE or FlashAttention-2 internally.
  The Evo2 README verifies the FlashAttention *install dependency* only; no fetched primary
  source states RoPE usage in Evo2. Do not claim either as an Evo2 architectural component
  without a further primary citation.
- **UNVERIFIED** (seen only in search snippets, not fetched from owner): "30× more data
  than Evo 1", "8× nucleotides at a time", "3× throughput at 1M context for 40B".
  Candidate owners: https://arcinstitute.org/news/evo2 ,
  https://www.nature.com/articles/s41586-026-10176-5.

---

## 2. Data (Findlay BRCA1 saturation editing)

- Paper: Findlay et al., "Accurate classification of BRCA1 variants with saturation genome
  editing", Nature 562:217–222 (2018), doi:10.1038/s41586-018-0461-z; PMCID PMC6181777,
  PMID 30209399.
  Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC6181777/
- Design: saturation genome editing (SGE) in HAP1 / HAP1-Lig4KO (1N-sorted) cells; "all
  possible SNVs" tiled across 13 exons encoding RING (exons 2–5) and BRCT (exons 15–23),
  transcript NM_007294.3; day-5 vs day-11 (gDNA) + day-5 cDNA (RNA) sequencing.
- Scale: function scores for **3,893 SNVs = 96.5%** of all possible SNVs in targeted
  exons; bimodal distribution; mixture-model classes functional / intermediate /
  non-functional (72.5% / 6.4% / 21.1%); 441/2086 missense SNVs non-functional.
- Clinical concordance: 162/169 ClinVar pathogenic SNVs non-functional; 20/22 benign
  functional; ROC "sensitivity 96.7% at 98.2% specificity" treating likely-path/likely-benign
  as pathogenic/benign; RNA scores separate expression-mediated from protein-mediated LOF.
- MaveDB hosts per-exon score sets (e.g. exon 20 replicate 1,
  `urn:mavedb:00000097-s-1`) — corroborating download location, not the paper of record.
  Source: https://www.mavedb.org/score-sets/urn:mavedb:00000097-s-1 (seen in search)
- Repo-local calibration slice: first 500 rows (`brca1_df.iloc[:500]`), FUNC/INT merged,
  τ = −0.0009178519, σLOF ≈ 0.0015140239, σFUNC ≈ 0.0009016589, AUROC ≈ 0.73 on −Δ.
  These numbers are **repo-local experimental results, not primary-source constants**.
  Sources (repo-local): `evo2-backend/main.py:31-47,252-310` ;
  `paper-ieee.tex:133,309` ; `variant-analysis-ppt.tex:174-286`

---

## 3. APIs

### 3.1 UCSC Genome Browser REST API
Base URL `https://api.genome.ucsc.edu/`.
Source for all bullets: https://genome.ucsc.edu/goldenpath/help/api.html

- Endpoint functions: `/findGenome`, `/list/publicHubs`, `/list/ucscGenomes`,
  `/list/genarkGenomes`, `/list/hubGenomes`, `/list/files`, `/list/tracks`,
  `/list/chromosomes`, `/list/schema`, `/getData/sequence`, `/getData/track`, `/search`.
- `/getData/sequence`: required `(genome OR (hubUrl AND genome)) AND chrom`; optional
  `start AND end` (must be given together), `revComp=1`. Example:
  `getData/sequence?genome=hg38;chrom=chrM` and
  `getData/sequence?genome=hg38;chrom=chrM;start=4321;end=5678`.
- `/list/chromosomes`: required `genome OR (hubUrl AND genome)`; optional `track`.
- Parameter syntax: `?` starts the query, `;` separates parameters
  (e.g. `?genome=hg38;chrom=chrM`).
- Coordinates: `start` is 0-relative, `end` is 1-relative; links to the UCSC coordinate
  counting explainer.
- Output caps: `maxItemsOutput` default/max 1,000,000; chromosome-scoped queries
  recommended for large tracks.
- Etiquette: "generally recommend a maximum of one hit every second", bot-delay enforced,
  excessive use may be restricted; bulk users should prefer Table Browser / MySQL /
  downloads / HTTP streaming of bigBed/bigWig.
- Mirrors use `https://<mirror>/cgi-bin/hubApi/` (e.g. genome-euro, genome-asia).
- Repo-local usage: `getData/sequence?genome;chrom;start;end` with length check and
  upper-casing. Source (repo-local): `paper-ieee.tex:305`

### 3.2 NCBI E-utilities + ClinVar
- E-utilities "are the public API to the NCBI Entrez system and allow access to all
  Entrez databases including PubMed, PMC, Gene, Nuccore and Protein"; "a suite of eight
  server-side programs that accept a fixed URL syntax"; companions: Entrez Direct (UNIX),
  Quick Start / Examples books.
  Source: https://www.ncbi.nlm.nih.gov/home/develop/api/
- ClinVar "can be accessed by E-utilities, through web services and through a UNIX command
  line as Entrez Direct. ClinVar supports a subset of the E-utilities functions: esearch,
  esummary, elink, and efetch." Workflow: esearch → ids → esummary (overview, JSON via
  `retmode=json`) / efetch (full record; `rettype=vcv` / `rettype=clinvarset`) /
  elink (related records). Default format XML. `assembly_set` carries GRCh37+GRCh38
  locations.
  Source: https://www.ncbi.nlm.nih.gov/clinvar/docs/programmatic_access/
- Canonical example endpoints (all on `https://eutils.nc
...[truncated 8536 chars]