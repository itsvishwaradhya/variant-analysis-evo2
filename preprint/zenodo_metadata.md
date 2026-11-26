# Zenodo upload fields (ready to paste)

Upload the file `paper-preprint.pdf` and fill the form as below. All text is plain, so it can be pasted directly.

**Resource type:** Publication / Preprint

**Title:**
Evo2Serve: A Web-Deployed Genomic Language Model Service for Zero-Shot Variant Scoring and a Verification Study of Its Scoring Pipeline

**Publication date:** the day you publish (Zenodo fills this in)

**Authors** (add in this order; students first, faculty guide last). Affiliation is the same for all five. ORCID is optional; leave it blank if an author has none.

| # | Name (Family, Given as you prefer to be indexed) | Affiliation | ORCID (optional) |
|---|---|---|---|
| 1 | Shet, Nandish S | Department of Artificial Intelligence and Data Science, Don Bosco Institute of Technology, Bengaluru, Karnataka, India | |
| 2 | Thippeswamy S | Department of Artificial Intelligence and Data Science, Don Bosco Institute of Technology, Bengaluru, Karnataka, India | |
| 3 | Vishwaradhya A C | Department of Artificial Intelligence and Data Science, Don Bosco Institute of Technology, Bengaluru, Karnataka, India | |
| 4 | Jeevan A M | Department of Artificial Intelligence and Data Science, Don Bosco Institute of Technology, Bengaluru, Karnataka, India | |
| 5 | Nandini K S (Dr.) | Department of Artificial Intelligence and Data Science, Don Bosco Institute of Technology, Bengaluru, Karnataka, India | |

Note on names: some authors have initials in place of a surname. Check how each person wants to be written and keep that spelling identical to the PDF. Do not add an e-mail address; Zenodo does not need one on the record.

> All four student authors and the faculty guide must agree to be listed and must agree to this upload before it is published. A Zenodo record with a DOI is public and permanent: authors can be corrected in a new version, but the first version cannot be deleted once published.

**Description (paste the abstract):**

Genomic language models such as Evo 2 can score the effect of a DNA change without task-specific training, but the label shown to a user also depends on a software contract (context window, coordinates, edit rules, threshold and request validation) that is rarely examined. We describe Evo2Serve, a web application that scores single-nucleotide variants, deletions, insertions and deletion-insertions of up to 500 bases with Evo 2-7B on a serverless NVIDIA H100 GPU, applies a threshold calibrated on BRCA1 saturation genome editing data, and shows the result beside ClinVar. We then verify the deployed pipeline without running the model. The 500-variant calibration slice contains 100 loss-of-function and 400 functional variants but covers only 10.69% of the assayed interval. On that slice, reference predictors reach AUROCs from 0.53 (gnomAD frequency) to 0.88 (Align-GVGD), CADD 0.79, with bootstrap half-widths of about 0.03 to 0.07 for most. The deployed endpoint fetches an 8193-base window where calibration used 8192. The GRCh37 and GRCh38 assemblies differ by a constant 1,847,983 bases at BRCA1, and the request carries no reference allele that could expose a coordinate from the wrong assembly. Across 55 request cases, the Pydantic and Zod validators conform on 43 and 47, disagree on 6, and both mishandle 7, including assembly and chromosome strings with separator characters that both accept. We list eight defects with proposed repairs. Latency and throughput were not measured. The tool is for research and education and is not a clinical classifier.

**Keywords** (one per line or comma separated, as the form allows):
variant effect prediction, genomic language model, Evo 2, BRCA1, ClinVar, web application, serverless GPU, software verification, bioinformatics

**Language:** English (eng)

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0) (recommended: it lets others reuse and cite the paper with credit)

**Version:** 1 (first public version; use 1.1, 2, ... for later corrected uploads)

**Publisher:** leave blank (Zenodo is the repository; this is not a journal publication)

**Related identifiers** (add one row):

| Relation | Identifier | Resource type |
|---|---|---|
| is supplemented by | https://github.com/itsvishwaradhya/variant-analysis-evo2 | Software |

(Identifier scheme: URL. Once the repository itself has a Zenodo DOI, replace or add that DOI here with the same relation, and cite the paper DOI in the repository README.)

**Additional notes / description footer (optional, paste at the end of the description):**
Preprint, not peer reviewed. Research and education tool; its output is not a clinical diagnosis. Source code, analysis scripts and machine-readable results are in the linked repository (folder docs/analysis).

**Funding / grants:** leave empty unless the authors declare funding (see the Declarations section of the paper; both must say the same thing).

**Communities (optional):** none required.

**Access:** Open access.

## Before you click Publish

- The PDF, this metadata and the paper's Declarations section must agree (authors, affiliation, funding, competing interests).
- Read `SUBMISSION_STEPS.md` and tick every item of its checklist.
