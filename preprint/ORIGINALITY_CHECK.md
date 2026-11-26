# Originality / Similarity Check: Evo2Serve preprint

Paper checked: `preprint/paper-preprint.tex` (and the compiled `paper-preprint.pdf`, 9 pages; `pdftotext` was used to confirm the PDF carries the same text, including the AI-assistance statement).
Date of check: 2026-11-26. Read-only check: the paper was not edited, nothing was committed, nothing was rewritten.

**Scope and honesty note.** This is a limited, best-effort check. Parts 1 and 3 are exact and reproducible. Part 2 is a manual web-search check of about 30 phrases. It is **not** equivalent to Turnitin, iThenticate, Ouriginal or DrillBit. Those tools compare against proprietary databases of journals, student papers and web snapshots that nobody here can query. A clean result below does not guarantee a clean result there.

---

## 1. Local self-overlap (authors' own earlier texts)

Method (script: `/tmp/claude-0/-home-user-variant-analysis-evo2/093c9c38-9441-5cca-bac2-057af06592d6/scratchpad/overlap.py`, plus `runs10.py` in the same folder). LaTeX was stripped from the preprint and from each source: preamble, comments, figures, tables, TikZ, equations, math, `\cite`/`\ref`, bibliography. Markdown sources had code blocks and tables removed. Text was lower-cased and tokenised to words. The preprint has **4,973 prose words** and **4,966 distinct word 8-gram shingles**.

Columns: *8-gram overlap* is the share of the preprint's 8-gram shingles that also occur in the source. *Longest run* is the longest stretch of consecutive identical words. *Runs >= 12* is the number of separate verbatim runs of at least 12 words.

| Source | Source words | Shared 8-grams | 8-gram overlap | Longest verbatim run (words) | Runs >= 12 words |
|---|---:|---:|---:|---:|---:|
| `paper-ieee.tex` | 5,234 | 134 | 2.7% | 18 | 8 |
| `paper-kscst.tex` | 3,732 | 123 | 2.5% | 26 | 9 |
| `report/ch6.tex` | 2,934 | 23 | 0.5% | 12 | 1 |
| `report/ch5.tex` | 2,804 | 14 | 0.3% | 14 | 2 |
| `report/abstract.tex` | 391 | 6 | 0.1% | 10 | 0 |
| `report/ch7.tex` | 1,436 | 5 | 0.1% | 11 | 0 |
| `report/ch1.tex` | 1,967 | 4 | 0.1% | 10 | 0 |
| `report/ch4.tex` | 2,225 | 2 | 0.0% | 8 | 0 |
| `report/ch2.tex` | 2,219 | 0 | 0.0% | 0 | 0 |
| `report/ch3.tex` | 1,435 | 0 | 0.0% | 0 | 0 |
| `variant-analysis-ppt.tex` | 572 | 0 | 0.0% | 0 | 0 |
| `docs/research-findings.md` | 1,449 | 0 | 0.0% | 0 | 0 |
| `docs/paper-citations.md` | 9,398 | 0 | 0.0% | 0 | 0 |
| `README.md` | 461 | 0 | 0.0% | 0 | 0 |
| **Union of all sources** | | | **5.7%** | 26 | 20 runs in total |

About 17% of the preprint's words sit inside some matching 8-word run. Most of those runs are short stack descriptions or numbers (for example "Next.js 15 application written in TypeScript with React 19 Tailwind CSS"), not argument prose.

Interpretation:

- Overall self-overlap is low. The preprint is largely new prose. It reuses facts, numbers and some sentences from `paper-ieee.tex` (an earlier version of the same paper, titled "Validating a Web-Deployed Genomic Model Service...") and from `paper-kscst.tex`. The college report (`report/ch1-ch7`) and `docs/*` share almost no wording.
- `paper-kscst.pdf` and the report were produced for the KSCST programme and the DBIT/VTU major project. The preprint does **not** mention either (grep for "KSCST", "project report", "VTU" and "thesis" finds nothing in the .tex). The authors may want to disclose in the Zenodo description or a footnote that the preprint builds on their KSCST paper and college project report. Reasons: some venues and Turnitin will flag the overlap, and the report may be deposited in the institutional repository.

Verbatim runs of 12 or more words, longest first (all are exact word matches after normalisation). Line numbers refer to `paper-preprint.tex`.

| Words | Source | Preprint location | Passage (normalised text) |
|---:|---|---|---|
| 26 | paper-kscst.tex | Acknowledgment, line 657 | "the department of artificial intelligence and data science don bosco institute of technology for guidance and support and the arc institute for releasing evo 2 openly" |
| 19 | paper-kscst.tex | Sec. III-B, line 140 | "the same code base contains the calibration routine of section [x] which runs as a separate modal gpu job" |
| 18 | paper-ieee.tex | Sec. V (Evaluation Design), line 302-304 | "and the real zod schema extracted from the route handler ... we import the deployed window and" |
| 17 | paper-kscst.tex | Results, line 314 | "workbook contains 3893 variants 2821 functional 72.46 249 intermediate 6.40 and 823 non-functional 21.14" |
| 14 | report/ch5.tex | Front End, line 137 | "is a next.js 15 application written in typescript with react 19 tailwind css" |
| 14 | paper-kscst.tex | Keywords, line 69 | "variant effect prediction genomic language model evo 2 brca1 clinvar web application serverless gpu" (keyword list, same in report/abstract.tex) |
| 14 | paper-ieee.tex | Introduction, line 74 | "particular label attached to a particular coordinate entered by a particular person between the ..." |
| 13 | paper-kscst.tex | System, line 105 | "route checks the user's session and validates each analysis request a fastapi endpoint" |
| 13 | paper-kscst.tex | Decision rule, line 262 | "and reports a confidence value that grows with the distance of [delta] from [tau]" |
| 13 | paper-ieee.tex | Evaluation Design, line 298-300 | "with a fixed seed window and assembly contract we recompute both window rules" |
| 13 | paper-ieee.tex | Limitations, line 626 | "depend on the state of the database on the day of the run" |
| 13 | paper-ieee.tex | Related Work, line 97 | "a classical phylogenetic method has been reported to outperform large protein language models" |
| 13 | paper-ieee.tex | System, line 140 | "a 120-second scale-down window and two retries these are configuration values not measured" |
| 12 | report/ch6.tex | Results, line 314 | "functional 72.46 249 intermediate 6.40 and 823 non-functional 21.14" |
| 12 | report/ch5.tex | Evaluation Design, line 304 | "with a stand-in scorer a third-order markov background model estimated from the" |
| 12 | paper-kscst.tex | System, line 165 | "in an http-only cookie valid for seven days the next.js route" |
| 12 | paper-kscst.tex | Calibration, line 246 | "data following the zero-shot protocol of the evo 2 authors non-functional variants" |
| 12 | paper-kscst.tex | System, line 140 | "and the analysis function is exposed as a fastapi post endpoint modal" |
| 12 | paper-ieee.tex | Score difference, line 243 | "the endpoint scores the reference and the edited sequence on every request" |
| 12 | paper-ieee.tex | Context window, line 172 | "and the inserted string the window centre is for a substitution or" |

Shorter 10-11 word matches also occur with the same two files and with report ch6/ch7. Examples: "the deployed window is one base longer than the calibration window" (ch6, ch7 versus the Conclusion, line 636) and "the first 250 rows contain 30 non-functional variants" (ch6, paper-ieee). They come from sentences that state the same measured facts.

Reading: these are the authors' own descriptions of the same system and measurements, so repetition is natural. They are still verbatim, and a similarity tool will report them as matches to the KSCST paper or report if those are indexed anywhere. The matches that are prose rather than data are: the Acknowledgment sentence (26 words), the Section III-B sentence at line 140, the Sec. III-C and III-D sentences at lines 165 and 262, and the Introduction sentence at line 74 (exact in `paper-ieee.tex`, which looks like an unpublished draft).

---

## 2. External similarity (WebSearch, exact-phrase queries)

Limited manual check. 31 queries, each a distinctive 8-16 word phrase from the paper placed in quotation marks, spread over all sections. Q9-Q20 and Q26-Q27 are the phrases most likely to resemble published text (descriptions of other people's work). The search tool does not strictly enforce exact-phrase matching and has a US-only index, so "no match" means "no page in the top results contained this sentence", nothing stronger. Numbers, formulas, method names and standard terms were excluded from the quoted phrases.

| # | Section | Query phrase (abridged only where marked) | Result | Verdict |
|---|---|---|---|---|
| 1 | Abstract | "the label shown to a user also depends on a software contract" | Unrelated contract/label pages (EULA, patents, app-label research) | No match |
| 2 | Intro | "justify any particular label attached to a particular coordinate entered by a particular person" | Map-labelling documentation only | No match |
| 3 | Intro | "Between the benchmark and the user sits a software layer" | AI-benchmark papers on the benchmark/use gap; different wording | No match |
| 4 | Intro | "owes its users an account of how that word was produced" | Etymology pages | No match |
| 5 | Intro | "A coordinate taken from the wrong assembly, for example, yields a confident answer about a different base" | Genomics-QA paper and Galaxy FAQ on assembly mismatch; same idea, different wording | No match |
| 6 | Related | "Most of these methods are limited to coding changes or depend on precomputed annotations" | Unrelated (code-annotation papers) | No match |
| 7 | Related | "they say nothing about a service built on a small calibration subset" | Generic calibration pages | No match |
| 8 | Related | "Likelihoods from sequence-only models can reflect phylogenetic structure rather than function" | Papers on fitness identifiability and phylogeny in protein language models; same theme, different wording | No match |
| 9 | Related | "A classical phylogenetic method has been reported to outperform large protein language models" | Returns the cited NeurIPS 2024 paper (Prillo et al.); title is similar in meaning, sentence is not copied | No near-verbatim match; topic matches the cited work (correctly cited) |
| 10 | Related | "VarSome aggregates annotations from many sources behind one query box" | VarSome paper and site pages; they describe a search engine over 30+ databases, wording differs | No match |
| 11 | Related | "MobiDetails presents curated variant evidence online" | MobiDetails paper (EJHG 2021) and site; abstract says "online application which gathers useful data for the interpretation of DNA variants" | No match; similar topic only |
| 12 | Related | "SIFT estimates tolerance of an amino-acid change from conservation across homologous sequences" | SIFT paper and secondary reviews; different wording | No match |
| 13 | Related | "CADD integrates many genomic annotations into one deleteriousness score for any variant" | CADD papers: "a method for objectively integrating many diverse annotations into a single measure (C score) for each variant"; the draft's sentence is a loose paraphrase of the same idea | Weak thematic similarity only; not near-verbatim |
| 14 | Related | "wraps such tools in a standard annotation pipeline" (Ensembl VEP) | VEP paper and docs; no such sentence | No match |
| 15 | Related | "variant effect predictors as a group show ancestry-dependent behaviour" | Pathak et al. bioRxiv (cited) and later preprints; different wording | No match |
| 16 | Related | "has described how a computational score must be calibrated locally before it can be mapped to evidence strength" | Pejaver et al. and later ClinGen calibration preprints; one preprint says tools are calibrated "to local" likelihood ratios | No match; see Part 3 on accuracy of this sentence |
| 17 | Related | "guidelines give computational evidence at most supporting weight" | Unrelated evidence-grading pages | No match |
| 18 | Related | "AlphaMissense, for instance, scores missense variants at proteome scale" | AlphaMissense paper and news pages ("proteome-wide missense variant effect prediction") | No match; title-level similarity only, expected |
| 19 | Related | "Evo 2 extends this to 7B and 40B parameters and a one-million-token context" | Evo 2 model cards and Arc/NVIDIA pages: "trained with 7B and 40B parameters ... context window up to 1M tokens" | No match; same facts, different wording |
| 20 | Related | "Evo showed that a single model can be trained on genomes at scale" | Evo/Evo 2 pages; claim supported in substance, not in words | No match |
| 21 | Related/Results | "zero-shot Evo 2-7B is reported at AUROC 0.9037 on the full BRCA1 benchmark against 0.8763 for CADD" | NVIDIA BioNeMo BRCA1 tutorial pages (no such figures on those pages) | No match |
| 22 | Methods | "a negative [delta] means that the model finds the edited sequence less plausible" | NVIDIA BRCA1 tutorial ("the lower the delta, the more likely ... disruptive") and a ToolUniverse wrapper ("variant makes the sequence less likely") | No match; same convention, different wording |
| 23 | Methods | "It is a bounded distance and not a probability, and nothing in the repository shows it to be calibrated" | Generic ML-calibration pages | No match |
| 24 | Results | "variants that were engineered and not drawn from a population" (+ gnomAD) | gnomAD usage pages | No match |
| 25 | Results | "A request that changes nothing thus receives the maximum confidence" | Patents on confidence scoring | No match |
| 26 | Results | "neighbouring predictors are not reliably ordered on 500 variants" | Unrelated predictor-benchmark papers | No match |
| 27 | Discussion | "the stricter layer protects the weaker only on the path through the browser" | General layered-security pages | No match |
| 28 | Discussion | "They borrow the vocabulary of clinical classification without its evidentiary structure" | Psychiatric-nosology preprint with a loosely related idea; different wording | No match |
| 29 | Discussion | "Two hand-written validators disagree" + "generate validators from one schema" | npm package page and JSON-schema tooling | No match |
| 30 | Discussion | "The threshold should be refit on the full assay with a held-out split, under the window that is actually served" | ML threshold-selection pages | No match |
| 31 | Conclusion | "Evo2Serve is not an annotation aggregator" | Nothing relevant (only unrelated "annotation" pages) | No match |

**Result: 0 near-verbatim external matches in 31 queries.** The closest hits are thematic, not textual: Q9 (the cited NeurIPS 2024 paper whose title says the same thing as the draft's sentence), Q13 (CADD's own abstract, which describes the same idea in different words) and Q11 (the MobiDetails abstract). None needs rewording for similarity reasons. Only the Q13 sentence is close enough in content to be worth a glance (see Part 5).

**Recommendation.** Run the final PDF through the institution's licensed check (many Indian engineering colleges provide Turnitin, Ouriginal or DrillBit) before posting. Expect the bibliography, the standard method names and the authors' own KSCST paper and report (if indexed) to appear as matches.

---

## 3. Quotation and citation hygiene

Automated cross-check of `\cite{...}` keys against `\bibitem{...}` keys: 28 bibliography entries, 28 distinct keys cited, **no uncited entry and no missing entry**. No sentence in the paper uses quotation marks for words taken from other authors (the only quoted strings are the application's own labels: "likely pathogenic", "Likely benign", "benign"). No phrase looks lifted without quote marks.

Attribution of other people's work:

- Every sentence in Related Work that describes a named method or study carries a citation (SIFT, PolyPhen-2, CADD, VEP, AlphaMissense, ESM-2, DNABERT-2, Nucleotide Transformer, Enformer, Borzoi, GPN-MSA, Evo, Evo 2, StripedHyena 2, Pugh, Prillo, Pathak, ACMG, ClinGen SVI, VarSome, MobiDetails, EVEE).
- Unattributed or weakly attributed claims to fix or check:
  1. **Line 93:** "Most of these methods are limited to coding changes or depend on precomputed annotations." This is a general claim about others' work with no citation. It also sits awkwardly beside the preceding clause that says CADD scores "any variant". Either cite a review or soften it (for example, "SIFT and PolyPhen-2 are limited to missense changes").
  2. **Line 76:** "The interpretation standards ... treat computational predictions as supporting evidence only~\cite{richards2015acmg,pejaver2022svi}". This is accurate for ACMG/AMP 2015 but **not** for Pejaver et al. 2022, whose result is that calibrated missense tools can reach Moderate or Strong evidence. Line 97 states the two sources correctly. Line 76 should cite only Richards et al. for "supporting only", or be reworded.
  3. **Line 97:** "must be calibrated locally" attributed to ClinGen SVI. Pejaver et al. calibrate tools against curated reference sets of missense variants and give score thresholds per evidence strength. "Locally" overstates this. Please check the wording against the paper.
  4. **Line 97:** "variant effect predictors as a group show ancestry-dependent behaviour" cites a bioRxiv preprint (Pathak et al.). The searches also surfaced a 2026 preprint that finds comparable performance across ancestry groups after allele-frequency stratification. Check whether Pathak et al. has a peer-reviewed version, and consider "have been reported to show".
  5. **Line 99:** "The Evo 2 authors provide interactive tools for generation and scoring with the model~\cite{brixi2026evo2}". The cited Nature paper is unlikely to describe a hosted tool in detail. Cite the tool's web page or repository instead of (or as well as) the paper.
  6. **Line 95:** Enformer and Borzoi are listed under "Genomic language models" ("Models that read nucleotide sequences directly"). They are supervised sequence-to-function models, not language models. A reviewer may object to the category. Rename the heading or the sentence. AlphaMissense (line 93) is likewise described as a protein language model extension, which is only loosely true.
  7. **Line 492:** "the NCBI Gene model, which places BRCA1 at 43,044,294-43,170,326 on GRCh38" has no citation or access date. Add a citation or footnote for NCBI Gene with the accession and retrieval date.
  8. **Line 562:** the UCSC query-parameter behaviour is cited to the NAR "20th year" paper. The primary source is the UCSC REST API documentation page, which should be cited with an access date.
  9. **Lines 105-140:** software and services (Next.js, React, FastAPI, Modal, Pydantic, Zod, MongoDB, bcrypt, JWT, FlashAttention, PyTorch, NCBI E-utilities) are named without references. This is normal for a systems paper, but footnotes with URLs and versions would help reproducibility.
  10. **Line 314:** "reproduce the 72.5%, 6.4% and 21.1% reported for the assay~\cite{findlay2018brca1}". The authors should re-confirm these three percentages and the 3,893 count against the Findlay paper's text and supplement, since the claim is that they match.
- Reference-list formatting (not similarity issues): the key `brixi2025stripedhyena2` points to an entry whose first author is Ku (cosmetic only). arXiv:2503.01868 is a March 2025 identifier but the entry says "Feb. 2025". The key `dallatorre2024nt` has a Feb. 2025 date in the entry. Several entries (Pugh et al., EVEE) are very recent or preprints and could not be independently verified here; the authors should check each DOI and author list.

---

## 4. AI-assistance disclosure

Found at `paper-preprint.tex` line 642 (in the PDF, Declarations section): *"Portions of the drafting, code, figures and analysis scripts were produced with the assistance of an AI model (Claude, Anthropic). The authors reviewed and are responsible for the content."*

Assessment: **honest and present, but thin.** It names the tool and the kinds of work, and it places responsibility on the authors, which is the right principle. It could be made more adequate by saying:

- which parts were AI-drafted (prose, code, figures, analysis scripts) and roughly how much, since "portions" is vague for a paper whose scripts and numbers were largely produced this way;
- that the authors re-ran the analysis scripts and verified every number and citation (the submission notes say this should happen; the paper should say that it did);
- the model/version and approximate dates of use;
- the same statement in the Zenodo description.

Other Declarations items are still placeholders: "Author contributions [to be completed by the authors]", "Competing interests ... [authors to confirm]", "Funding ... [authors to confirm]". These must be completed before posting. The earlier KSCST paper, `paper-ieee.tex` and the report contain no AI statement. If any of those were submitted to the college or KSCST, the authors should check the institution's policy.

AI-detector scores: such tools are unreliable (false positives and negatives are common). The honest remedy is disclosure plus the authors reading the text and revising it in their own words where it does not reflect their understanding. This check did not run, and does not recommend, any detector, paraphrasing or "humanizer" tool.

---

## 5. Verdict and recommended actions

**Verdict.** No evidence of plagiarism or close external copying was found in this limited check: 0 of 31 phrase queries returned a near-verbatim match, and citations are complete (28/28, none missing, none uncited). Self-overlap with the authors' own earlier drafts is small (5.7% of 8-grams in total; at most 2.7% with any single file) and consists mainly of repeated system descriptions, numbers and a few shared sentences. The main residual risks are (a) the undisclosed relationship to the KSCST paper and college report, (b) three or four citation-accuracy points, and (c) the thin AI disclosure and unfilled declarations.

The authors, not this check, must make any edits. Suggested actions:

1. **Disclose lineage.** Add a sentence in the Zenodo description or a footnote saying the work builds on the authors' KSCST paper and DBIT/VTU project report (Acknowledgment, line 657, is a verbatim 26-word copy of the KSCST acknowledgment, which is harmless but shows the relationship).
2. **Fix attribution accuracy:** line 76 (Pejaver et al. does not say "supporting only"); line 97 ("calibrated locally", Pathak et al. as preprint); line 93 (uncited generalisation); line 99 (Evo 2 interactive tools cited to the Nature paper); line 95 (Enformer and Borzoi are not language models).
3. **Add missing sources:** NCBI Gene (line 492) and UCSC API documentation (line 562) with access dates; optionally URLs and versions for the software stack (lines 105-140).
4. **Check sentence similarity by eye:** line 93 (CADD "integrates many genomic annotations into one ... score") is close in content to CADD's own abstract; the authors should be sure it is in their own words. Lines 140, 165 and 262 and the Introduction sentence at line 74 repeat sentences from earlier drafts; leave them if the authors intend them, but expect these to show as self-matches.
5. **Complete the AI-assistance statement** (Part 4) and fill the three bracketed Declarations items (author contributions, competing interests, funding).
6. **Run the licensed check** (Turnitin, Ouriginal or DrillBit via the college) on the final PDF before uploading to Zenodo, and make the repository public with a licence so the Data and Code Availability statement is true (this is already flagged in the .tex header comment).
7. **Verify the numbers** that the paper takes from other sources against those sources (Evo 2 Table values, Findlay percentages), and verify the reference entries (arXiv date for 2503.01868, DOIs and author lists of the 2025-2026 items).


---

## Fixes applied after this check (by the parent session)

- Line 76: Pejaver et al. is no longer cited for "supporting evidence only"; that statement now cites Richards et al. alone.
- Line 97: the Pejaver et al. sentence now says continuous scores can be calibrated and mapped to graded evidence strengths, with some missense tools reaching moderate or strong strength.
- Line 95: Enformer and Borzoi are described as sequence-to-function networks, separate from the DNA language models.
- Line 93: "Most of these methods" softened to "Several of these methods".
- Bibliography: arXiv:2503.01868 dated Mar. 2025.
- Declarations: the AI-assistance statement is expanded (what the AI did, that numbers come from the script outputs, and a bracket for the authors to confirm they re-ran the scripts), and a "Relation to earlier work" paragraph discloses the college report and the KSCST draft.
- Not changed: line 99 (the Evo 2 interactive tools are listed in the Evo 2 paper's code-availability section per docs/paper-citations.md), the Acknowledgment sentence copied from the authors' own KSCST text, and the Findlay et al. percentages (documented in docs/research-findings.md from the published article). The NCBI/UCSC citation or footnote suggestions are left for the authors to decide.
- Remaining for the authors: the institutional similarity check (Turnitin / Ouriginal / DrillBit), the bracketed declarations, a public repository with a licence.
