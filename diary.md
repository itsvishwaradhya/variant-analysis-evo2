# VTU Project Work Diary

## Project Details

| Field | Value |
|-------|-------|
| Project Title | Variant Effect Prediction using Evo2 Large Language Model |
| Student Name | [Student Name] |
| University Seat Number (USN) | [USN] |
| College | [College Name] |
| Guide / Supervisor | [Guide Name] |
| Semester | [Semester / Academic Year] |
| Total Duration | 5 Weeks (4–5 hours per week) |

## Project Overview

This project builds a web application that predicts the pathogenicity of single nucleotide variants (SNVs) in human DNA using the Evo2 large language model. Users select a genome assembly, search or browse for a gene (e.g., BRCA1), view its reference sequence, and submit a mutation to get a pathogenic/benign prediction with a confidence score. Known ClinVar classifications are compared against Evo2 predictions. The project has a Python backend (written for serverless GPU execution on Modal) and a Next.js/React frontend. As of the end of Week 5, the backend code is written and tested locally, but **deployment to Modal is still pending**.

---

## Week 1 — Project Setup and Foundation

**Date Range:** [Start Date] – [End Date]

| Field | Details |
|-------|---------|
| **Work Summary** | Recapped the research done in the previous semester (Evo2 architecture, variant effect prediction, ClinVar database). Cloned the repository along with its `evo2` submodule (ArcInstitute/evo2). Created a Python 3.10 virtual environment for the backend and installed the required dependencies. Installed and authenticated the Modal CLI. Surveyed the external APIs needed for the project (UCSC genome API, NCBI E-utilities, ClinVar). Below is the backend dependency list: <br><br> `evo2-backend/requirements.txt` <br> `fastapi[standard]` <br> `matplotlib` <br> `pandas` <br> `seaborn` <br> `scikit-learn` <br> `openpyxl` <br> `requests` <br> `biopython` |
| **Hours Worked** | 4.5 hours |
| **Reference Links** | [Evo2 Paper (biorxiv)](https://www.biorxiv.org/content/10.1101/2025.02.18.638918v1) · [ArcInstitute/evo2 GitHub](https://github.com/ArcInstitute/evo2) · [UCSC Genome Browser API](https://api.genome.ucsc.edu/) · [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) · [Modal Docs](https://modal.com/docs) |
| **Learnings** | Understood the Evo2 model (7B parameter genomic foundation model) and how delta-likelihood scoring can rank variant effect. Learned how to manage Git submodules and set up an isolated Python environment. Understood the data sources: UCSC for reference sequences, NCBI/ClinVar for gene and variant annotations. |
| **Risk** | Dependency and CUDA version mismatches can break the Evo2 build. Mitigation: pinned versions in `requirements.txt` and planned the Modal container image carefully. |
| **Skills Used** | Git & submodules, Python virtual environments, pip, Modal CLI, REST API exploration. |

---

## Week 2 — Frontend Scaffold and Data Layer

**Date Range:** [Start Date] – [End Date]

| Field | Details |
|-------|---------|
| **Work Summary** | Bootstrapped the frontend using the T3 stack (Next.js 15, React 19, TypeScript, Tailwind CSS, Shadcn UI). Configured environment variables in `src/env.js` using `@t3-oss/env-nextjs` and Zod, exposing `NEXT_PUBLIC_ANALYZE_SINGLE_VARIANT_BASE_URL` for the analysis API. Implemented the entire data-access layer in `src/utils/genome-api.ts`, wrapping the UCSC, NCBI, and ClinVar APIs: <br><br> `getAvailableGenomes()` — fetches and groups UCSC genome assemblies (`genome-api.ts:68`) <br> `getGenomeChromosomes()` — lists chromosomes, filtered and sorted (`genome-api.ts:99`) <br> `searchGenes()` — searches genes via NCBI clinical tables API (`genome-api.ts:140`) <br> `fetchGeneDetails()` — gene genomic bounds via NCBI e-summary (`genome-api.ts:183`) <br> `fetchGeneSequence()` — reference sequence window from UCSC (`genome-api.ts:226`) <br> `fetchClinvarVariants()` — known variants via ClinVar E-utilities search + summary (`genome-api.ts:264`) <br> `analyzeVariantWithAPI()` — POSTs a variant to the backend analysis endpoint (`genome-api.ts:353`) |
| **Hours Worked** | 5 hours |
| **Reference Links** | [T3 Stack](https://create.t3.gg/) · [Next.js Docs](https://nextjs.org/docs) · [Tailwind CSS](https://tailwindcss.com/) · [Shadcn UI](https://ui.shadcn.com/) · [UCSC Genome API](https://api.genome.ucsc.edu/) · [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) |
| **Learnings** | Learned the T3 stack structure and Next.js App Router conventions. Practiced typed API wrappers with TypeScript interfaces. Learned the response formats of UCSC (genome/chromosome/sequence) and NCBI E-utilities (esearch/esummary JSON). |
| **Risk** | External API schemas can change and break parsing. Mitigation: centralized all API calls in `genome-api.ts` with error handling and default fallbacks, and used strict TypeScript interfaces. |
| **Skills Used** | TypeScript, Next.js 15, Tailwind CSS, Shadcn UI, REST client integration, Zod environment validation. |

---

## Week 3 — Frontend UI Components and Integration

**Date Range:** [Start Date] – [End Date]

| Field | Details |
|-------|---------|
| **Work Summary** | Built all the interactive UI components: <br><br> `src/app/page.tsx` — main page with genome assembly selector and Search/Browse tabs; searching for a gene or selecting a chromosome lists results (`page.tsx:36`) <br> `src/components/gene-viewer.tsx` — orchestrates the gene detail view: information, sequence, known variants, and analysis (`gene-viewer.tsx:23`) <br> `src/components/gene-sequence.tsx` — displays the reference genome sequence with color-coded nucleotides <br> `src/components/known-variants.tsx` — table of ClinVar variants with classification badges <br> `src/components/variant-analysis.tsx` — mutation input form with validation (position number, `A/C/G/T` nucleotides), auto-detection of a matching known variant, and result display with a confidence bar (`variant-analysis.tsx:86`) <br> `src/components/variant-comparison-modal.tsx` — modal comparing the ClinVar classification against the Evo2 prediction <br> `src/utils/coloring-utils.ts` — shared helpers for nucleotide and classification colors (`coloring-utils.ts:1`) |
| **Hours Worked** | 5 hours |
| **Reference Links** | [React Docs](https://react.dev/) · [Next.js App Router](https://nextjs.org/docs/app) · [Shadcn UI Components](https://ui.shadcn.com/docs/components/) · [Lucide Icons](https://lucide.dev/) |
| **Learnings** | Practiced React hooks (`useState`, `useEffect`, `useRef`, `useImperativeHandle`, `forwardRef`) and client-side components in Next.js. Learned how to compose Shadcn primitives (Card, Table, Tabs, Select) with Tailwind theming. Implemented inline validation and loading states for a good user experience. |
| **Risk** | The variant analysis component calls the backend endpoint, which is not deployed yet. Mitigation: built a clean API layer (`analyzeVariantWithAPI`) so the UI is decoupled; errors are caught and shown gracefully. |
| **Skills Used** | React 19, TypeScript, Tailwind CSS, Shadcn UI, lucide-react icons, component architecture. |

---

## Week 4 — Backend: Modal Image and BRCA1 Batch Analysis

**Date Range:** [Start Date] – [End Date]

| Field | Details |
|-------|---------|
| **Work Summary** | Wrote the backend code in `evo2-backend/main.py` for serverless GPU execution on Modal (code written, not yet deployed). Defined the container image with CUDA 12.6, PyTorch, flash-attention, and the cloned ArcInstitute/evo2 repo (`main.py:13`). Implemented `run_brca1_analysis` (`main.py:80`): loads `Evo2('evo2_7b')` (`main.py:95`), parses the BRCA1 FunSeq2 dataset, builds 8192bp windows around each variant, substitutes the alternate base to create variant sequences, and scores both reference and variant sequences (`main.py:136`). Computed delta-likelihood scores, derived an optimal pathogenic threshold from the ROC curve, and estimated LOF/FUNC standard deviations used later for confidence (`main.py:171`). |
| **Hours Worked** | 5 hours |
| **Reference Links** | [Evo2 GitHub (ArcInstitute)](https://github.com/ArcInstitute/evo2) · [Evo2 Paper](https://www.biorxiv.org/content/10.1101/2025.02.18.638918v1) · [Modal GPU Functions](https://modal.com/docs/guide/gpu) · [FlashAttention](https://github.com/Dao-AILab/flash-attention) |
| **Learnings** | Learned how to build a Modal container image (base image, apt packages, PyTorch with CUDA wheels, source install). Learned sequence windowing to keep inference tractable and how delta-likelihood scores rank loss-of-function variants. Learned ROC-curve threshold selection. |
| **Risk** | The container build is heavy and slow (CUDA + flash-attention + Evo2 from source). Mitigation: pinned exact versions, enabled Modal image caching, and did not block frontend work on the build. |
| **Skills Used** | Python, Modal, PyTorch/CUDA, pandas, NumPy, scikit-learn (ROC/AUROC), Biopython. |

---

## Week 5 — Backend API Endpoint and Deployment Preparation

**Date Range:** [Start Date] – [End Date]

| Field | Details |
|-------|---------|
| **Work Summary** | Implemented the single-variant analysis pipeline in `evo2-backend/main.py`: <br><br> `get_genome_sequence()` — fetches an 8192bp reference window from the UCSC API for a given position/genome/chromosome (`main.py:265`) <br> `analyze_variant()` — substitutes the alternative base, computes reference vs variant likelihoods, and classifies the variant using the pre-computed threshold and confidence from LOF/FUNC standard deviations (`main.py:301`) <br> `Evo2Model` class with a FastAPI endpoint `analyze_single_variant` via `@modal.fastapi_endpoint` (`main.py:330`, `main.py:340`) <br> Local entrypoint test that posts a BRCA1 example payload to the endpoint URL (`main.py:387`) <br><br> **Deployment status: PENDING.** The Modal commands (`modal setup`, `modal run main.py`, `modal deploy main.py`) are documented as next steps but have not been executed yet. Until deployment completes, `NEXT_PUBLIC_ANALYZE_SINGLE_VARIANT_BASE_URL` still points to a placeholder and the live end-to-end test cannot run. |
| **Hours Worked** | 5 hours |
| **Reference Links** | [Modal FastAPI Endpoints](https://modal.com/docs/guide/webhooks) · [UCSC Sequence API](https://api.genome.ucsc.edu/) · [FastAPI](https://fastapi.tiangolo.com/) · [Pydantic](https://docs.pydantic.dev/) |
| **Learnings** | Learned to expose a Modal GPU function as a FastAPI web endpoint and to validate requests with Pydantic models. Learned confidence estimation using per-class standard deviations around a ROC-derived threshold. Understood the end-to-end flow: frontend → Modal web URL → UCSC fetch → Evo2 scoring → prediction response. |
| **Risk** | **Backend not yet deployed to Modal.** Until `modal deploy main.py` is run and the returned web URL is set in `NEXT_PUBLIC_ANALYZE_SINGLE_VARIANT_BASE_URL`, the variant analysis feature will fail at runtime. Mitigation: frontend handles errors gracefully; deployment is the immediate next step, followed by an end-to-end test. |
| **Skills Used** | FastAPI, Pydantic, Modal web endpoints, HTTP request handling, deployment planning. |

---

## Next Steps (Pending)

- Run `modal setup` and deploy the backend with `modal deploy main.py`.
- Update `NEXT_PUBLIC_ANALYZE_SINGLE_VARIANT_BASE_URL` in `evo2-frontend/.env` with the deployed Modal web URL.
- Perform an end-to-end test (e.g., BRCA1 example) from the frontend and verify predictions against ClinVar classifications.

---

## Signatures

| Guide | Student |
|-------|---------|
| Date: __________ | Date: __________ |
| Signature: __________ | Signature: __________ |