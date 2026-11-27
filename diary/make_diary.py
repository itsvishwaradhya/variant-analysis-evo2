#!/usr/bin/env python3
"""Generate diary_entries.tex (one table page per weekly entry) for the project diary.

Run:  python3 make_diary.py   then   lualatex diary.tex   (twice is not needed)
"""
import re

# (date lines, hours, summary, [links], learnings, risk, skills)
E = []

def add(date, hours, summary, links, learn, risk, skill):
    E.append(dict(date=date, hours=hours, summary=summary, links=links, learn=learn, risk=risk, skill=skill))

add(("27", "Jul", "2026"), 3,
    "With the planning and Phase Review 2 completed, our team started the implementation phase of the genomic mutation analysis platform. We turned the approved methodology into a task list covering the Modal GPU backend, the Next.js frontend, the genomic APIs and the calibration of the pathogenicity threshold. We studied the official Evo 2 repository and its BRCA1 zero-shot notebook line by line to understand how reference and variant windows of 8,192 bases are built, how \\texttt{score\\_sequences} returns log-likelihoods, and how a ROC curve is used to choose a threshold. We decided to keep the code in one repository with separate \\texttt{evo2-backend} and \\texttt{evo2-frontend} folders, agreed a simple Git workflow, and fixed the order of work: data access first, then the user interface, then the GPU backend.",
    ["https://github.com/ArcInstitute/evo2", "https://www.biorxiv.org/content/10.1101/2025.02.18.638918v1"],
    "We learned how the notebook turns a nucleotide change into a score: the variant is placed in the centre of a fixed window, both sequences are scored, and the difference is compared with a threshold chosen on labelled data.",
    "The main risk was trying to build every feature at once. Action: we planned single-nucleotide variants first and left insertions and deletions for a later stage.",
    "Project Planning, Code Reading, Git")

add(("03", "Aug", "2026"), 4,
    "This week we prepared the development environment. We cloned the project with the Evo 2 repository as a Git submodule, created a Python 3.10 virtual environment for the backend and installed the packages listed in \\texttt{requirements.txt} (FastAPI, pandas, scikit-learn, seaborn, openpyxl, requests and Biopython). We installed the Modal command line tool and authenticated it with \\texttt{modal setup}. For the frontend we created a Next.js 15 application with the T3 stack, using TypeScript, Tailwind CSS and shadcn/ui, and we declared the typed environment variables in \\texttt{src/env.js} with Zod so that a missing setting stops the application at start-up instead of failing later at run time.",
    ["https://modal.com/docs", "https://create.t3.gg/", "https://nextjs.org/"],
    "We learned that a pinned requirements file and typed environment variables remove most set-up problems, and that Modal runs the code in a container, so our own machines do not need a GPU.",
    "Version differences between CUDA, PyTorch and the Evo 2 package can break the build. Action: we pinned the versions and kept the GPU code separate from the local scripts.",
    "Environment Setup, Python, Next.js")

add(("10", "Aug", "2026"), 4,
    "We built the data-access layer of the frontend in \\texttt{src/utils/genome-api.ts}. It wraps the public services in typed functions: \\texttt{getAvailableGenomes} reads the human assemblies from the UCSC API, \\texttt{getGenomeChromosomes} lists the chromosomes of an assembly, \\texttt{searchGenes} queries the NCBI clinical tables service, \\texttt{fetchGeneDetails} reads the gene coordinates from NCBI E-summary and \\texttt{fetchGeneSequence} retrieves the reference sequence from the UCSC \\texttt{getData/sequence} endpoint. We limited the sequence shown on screen to 10,000 bases, handled the 0-based start and 1-based end convention of UCSC, and added error handling and default values so that a failing service does not break the page.",
    ["https://genome.ucsc.edu/goldenpath/help/api.html", "https://www.ncbi.nlm.nih.gov/books/NBK25501/", "https://clinicaltables.nlm.nih.gov/"],
    "We learned the JSON formats of UCSC and NCBI, and that coordinate conventions (0-based versus 1-based, assembly-specific positions) have to be handled explicitly.",
    "Public service schemas and rate limits can change. Action: all calls are kept in one file with strict TypeScript interfaces, so a change is repaired in one place.",
    "TypeScript, REST APIs, Data Handling")

add(("17", "Aug", "2026"), 4,
    "This week we built the main interface. The home page lets the user pick a genome assembly (hg38 by default) and switch between Search Genes and Browse Chromosomes; the matching genes are listed and a Try BRCA1 example button fills in the search. Selecting a gene opens the gene viewer, which combines a gene information card with the reference sequence. We wrote \\texttt{coloring-utils.ts} to colour nucleotides and classifications and made every base clickable, so that the position and the reference base fill the variant form. The components use React hooks, Tailwind CSS and the shadcn/ui card, tabs, table and select primitives. Before committing this work we refactored the folder structure for readability.",
    ["https://react.dev/", "https://ui.shadcn.com/", "https://tailwindcss.com/"],
    "We learned React hooks and the Next.js App Router, and how to compose shadcn/ui components with Tailwind so that the layout stays consistent.",
    "The selected assembly, gene and chromosome can become inconsistent when several requests overlap. Action: loading and error states were added and the results are cleared whenever the assembly changes.",
    "React, Tailwind CSS, UI Design")

add(("24", "Aug", "2026"), 4,
    "We added the clinical side of the interface. \\texttt{fetchClinvarVariants} searches ClinVar through NCBI E-search and E-summary, limited to 20 records, using the \\texttt{chrpos37} field for hg19 and \\texttt{chrpos38} for the other assemblies, and returns every variant with its type, position and clinical classification. The \\texttt{KnownVariants} component shows them in a table with coloured classification badges. We also wrote the variant-analysis form for single-nucleotide variants, with input checks (numeric position, bases A, C, G or T), automatic detection of a matching known variant and a confidence bar for the result. Clicking a ClinVar row prepares the same request.",
    ["https://www.ncbi.nlm.nih.gov/clinvar/docs/programmatic_access/", "https://www.ncbi.nlm.nih.gov/clinvar/", "https://lucide.dev/"],
    "We learned how ClinVar stores positions for each assembly and how clinical significance and review status are reported for a variant.",
    "ClinVar titles are free text, so reading the variant type from a title is fragile. Action: the parsing is isolated in helper functions and the first version supports single-nucleotide variants only.",
    "ClinVar, API Integration, Form Validation")

add(("31", "Aug", "2026"), 4,
    "We started the GPU backend in \\texttt{evo2-backend/main.py}. We defined the Modal container image: CUDA 12.6.3 on Ubuntu 22.04 with Python 3.12, PyTorch 2.7.1, FlashAttention 2.8.0 and the official Evo 2 package cloned from GitHub, followed by the remaining requirements. A persistent volume named \\texttt{hf\\_cache} keeps the Hugging Face model files so the weights are downloaded only once, and the model class loads \\texttt{Evo2('evo2\\_7b')} when a container starts, on an H100 GPU with at most three containers, two retries and a 120-second scale-down window. We wrote the calibration function \\texttt{run\\_brca1\\_analysis}, updated the dependencies and installation commands after testing the image, changed \\texttt{analyzeVariantWithAPI} to send a JSON body, and prepared the first project presentation.",
    ["https://modal.com/docs/guide/gpu", "https://github.com/Dao-AILab/flash-attention", "https://huggingface.co/arcinstitute"],
    "We learned how to describe a GPU environment as code, why model weights are cached on a volume and why the model is loaded once per container instead of once per request.",
    "The image build is slow and sensitive to package versions. Action: exact versions are pinned and the frontend work continues while the image builds.",
    "Modal, PyTorch, Cloud GPU")

add(("07", "Sep", "2026"), 4,
    "We completed the scoring pipeline. The calibration job reads the BRCA1 saturation genome editing workbook, merges the functional and intermediate classes, builds 8,192-base windows from the GRCh37 chromosome 17 sequence, scores the unique reference windows and the mutated windows with Evo 2 and computes the delta log-likelihood of every variant. From the first 500 variants we computed the ROC curve of the negative delta, selected the threshold with the highest Youden index and measured the spread of each class; these values became the constants \\texttt{SNV\\_THRESHOLD}, \\texttt{SNV\\_LOF\\_STD} and \\texttt{SNV\\_FUNC\\_STD}. We then wrote \\texttt{get\\_genome\\_sequence} (UCSC window around the variant), \\texttt{analyze\\_variant} (score the reference and the mutated sequence, label and confidence) and the FastAPI endpoint \\texttt{analyze\\_single\\_variant} with the Pydantic model \\texttt{VariantRequest}.",
    ["https://fastapi.tiangolo.com/", "https://docs.pydantic.dev/", "https://modal.com/docs/guide/webhooks"],
    "We learned that a log-likelihood difference is only meaningful after it is calibrated on labelled data, and how Youden's index selects an operating point on a ROC curve.",
    "A threshold fitted on a small slice of the data can be over-fitted. Action: we recorded that only 500 rows were used and planned a wider evaluation for later.",
    "ROC Analysis, FastAPI, scikit-learn, Biopython")

add(("14", "Sep", "2026"), 4,
    "We added user authentication so that the GPU cannot be used anonymously. In the Next.js application we created the routes \\texttt{/api/auth/signup}, \\texttt{/api/auth/login}, \\texttt{/api/auth/logout} and \\texttt{/api/auth/me}, a Mongoose \\texttt{User} model, password hashing with bcryptjs (10 rounds) and a \\texttt{lib/auth.ts} module that signs and verifies HS256 tokens with the jose library; the token is kept in an HTTP-only cookie valid for seven days. We built the sign-in and create-account page and a \\texttt{useAuth} hook, and the known-variants table now shows Sign in to analyze to visitors. On the backend, \\texttt{verify\\_jwt\\_token} checks the bearer token with PyJWT before any computation, using a secret read from the environment.",
    ["https://pyjwt.readthedocs.io/", "https://mongoosejs.com/", "https://github.com/panva/jose"],
    "We learned that passwords must never be stored in plain text, that a signed token is only as strong as its secret, and that the server must check the token again even when the browser hides a button.",
    "A weak or shared secret makes tokens forgeable, and error messages must not reveal internal details. Action: the secret comes from environment variables and both tiers return short 401 messages.",
    "Authentication, JWT, MongoDB, Security")

add(("21", "Sep", "2026"), 4,
    "We connected the frontend and the backend. The Next.js route \\texttt{/api/analyze} checks the session cookie, validates the request with a Zod schema and forwards it to the Modal endpoint with the token as a bearer header; \\texttt{analyzeVariantWithAPI} posts the JSON body and the \\texttt{AnalysisResult} type carries the delta score, label, confidence and threshold. We wrote the variant comparison modal, which shows the Evo 2 label and confidence bar next to the ClinVar classification and states whether the two agree. We tested the complete path with the example request for hg38 chr17:43,119,628 (alternate G) and with several known BRCA1 variants taken from the ClinVar table.",
    ["https://nextjs.org/docs", "https://zod.dev/"],
    "We learned how a request travels through the layers (browser, Next.js route, GPU endpoint, UCSC, model) and where each layer must validate its input.",
    "A change in the response format of one layer can break the next. Action: the shared result type was defined once in TypeScript and every field is checked before it is shown.",
    "System Integration, Zod, Next.js Routes")

add(("28", "Sep", "2026"), 4,
    "We prepared and tested the deployment. The Modal service is deployed with \\texttt{modal deploy main.py}, which returns the endpoint URL that is stored in \\texttt{NEXT\\_PUBLIC\\_ANALYZE\\_SINGLE\\_VARIANT\\_BASE\\_URL}; the signing key is shared through the \\texttt{JWT\\_SECRET} variable of the frontend and a Modal secret. We added a \\texttt{.env.example} without secrets and a local entry point in \\texttt{main.py} that posts the example payload and mints a short-lived development token when no token is supplied, so that the deployed endpoint can be checked from the command line. We noted that the first request after an idle period is slower because the container has to load the model, while later requests reuse the loaded model.",
    ["https://modal.com/docs/guide/secrets", "https://create.t3.gg/en/usage/env-variables"],
    "We learned how serverless GPU functions scale from zero, why configuration belongs in environment variables and secrets, and how to test a protected endpoint without exposing a real token.",
    "A secret copied into code or a screenshot would be exposed. Action: secrets stay in ignored .env files and Modal secrets, and only .env.example is committed.",
    "Deployment, Cloud Configuration, Testing")

add(("05", "Oct", "2026"), 4,
    "We tested and hardened the application. Through the comparison modal we checked the predictions for known pathogenic and benign BRCA1 variants against their ClinVar classifications, and we tested invalid inputs: a missing session, out-of-range positions, wrong bases and unreachable services. We improved the error messages returned by the Next.js route (401 without a valid session, 400 for an invalid payload, upstream errors passed on with a short text) and added loading and empty states to the known-variants table and the variant panel. We ran ESLint on the frontend and fixed the warnings reported in the components.",
    ["https://eslint.org/", "https://owasp.org/www-project-top-ten/"],
    "We learned that an application should fail with a clear message instead of a blank page, and that each error status code tells the user a different thing.",
    "Manual checks on a few variants can give a false impression of accuracy. Action: we treated them as functional tests only and planned a systematic evaluation.",
    "Testing, Error Handling, Code Quality")

add(("12", "Oct", "2026"), 3,
    "We extended the system beyond single-nucleotide variants. \\texttt{analyze\\_variant} now supports deletion, insertion and deletion--insertion (delins): a deletion removes n bases, an insertion adds the new bases after the anchor base and a delins replaces n bases by the new bases, with lengths limited to 500; for deletions the window is centred on the middle of the affected bases. \\texttt{VariantRequest} validates each type, and the responses for the indel types carry a provisional flag because the threshold was calibrated on substitutions. In the frontend we added the variant-type selector, the deletion-length and inserted-sequence inputs, helpers that read deletions and insertions from ClinVar titles, a Provisional note in the comparison modal and an improved result display.",
    ["https://docs.pydantic.dev/", "https://react.dev/"],
    "We learned how insertions and deletions change the length of the scored sequence, and why a threshold calibrated on one mutation type cannot simply be reused for another.",
    "Edge cases such as a deletion near the end of the window can fail silently. Action: the backend checks the window bounds and returns a clear error.",
    "Algorithm Design, Pydantic, React, Edge Cases")

add(("19", "Oct", "2026"), 4,
    "We evaluated the system. In \\texttt{docs/analysis} we wrote eight scripts: \\texttt{a\\_dataset\\_characterization} checks the composition of the BRCA1 workbook and compares the 8,192-base and 8,193-base windows; \\texttt{b\\_baseline\\_predictors} computes AUROC, bootstrap intervals and Youden points for CADD, PolyPhen-2, SIFT, Align-GVGD, phyloP and gnomAD frequency on the same 500 rows; \\texttt{c\\_assembly\\_provenance} measures the GRCh37--GRCh38 offset; \\texttt{d}, \\texttt{e} and \\texttt{f} run a generated set of 55 request cases against the Pydantic model and the Zod schema and compare them; \\texttt{g} exercises the scoring contract with a stand-in scorer; \\texttt{h} writes the figure data. Each script saves a JSON file, so every number can be re-checked without a GPU. We also collected citations and source notes and began the research paper.",
    ["https://scikit-learn.org/", "https://pandas.pydata.org/", "https://nodejs.org/"],
    "We learned how to evaluate a deployed system and not only the model: the data, the window, the coordinates and the validators can all change a prediction.",
    "Reporting numbers that cannot be reproduced would weaken the work. Action: every script writes a machine-readable result and the statements in the paper refer to those files.",
    "Evaluation, Statistics, Technical Writing")

add(("26", "Oct", "2026"), 4,
    "We polished and documented the application. We refined the layout, colours and login page with Tailwind CSS and shadcn/ui, checked the interface at several screen widths and re-ran the complete flow after the changes. The README lists the set-up steps (clone with submodules, install the backend packages, \\texttt{modal setup}, \\texttt{modal run}, \\texttt{modal deploy}, \\texttt{npm i} and \\texttt{npm run dev}), and the analysis folder has its own README that describes each script and how to run it. We reviewed the findings of the verification and listed the improvements they suggest: carry the reference allele in the request, use one window rule, cache the reference score, use one shared validation schema and recalibrate the threshold on the full dataset.",
    ["https://tailwindcss.com/", "https://nextjs.org/docs"],
    "We learned that clear set-up instructions and a written list of limitations are part of the deliverable, and that a user interface is easier to maintain when its styles come from shared tokens.",
    "Instructions that only work on the author's machine are a hidden risk. Action: the steps were followed again from a clean clone.",
    "UI Polish, Documentation, Review")

add(("02", "Nov", "2026"), 3,
    "We froze the code and prepared the final deliverables. We repeated the end-to-end flow once more, checked that a new machine can follow the README steps and stopped adding features. We prepared the presentation slides and the structure of the project report and the research paper in LaTeX, and we stated the limits of the work plainly: the threshold was calibrated on 500 BRCA1 substitutions, indel predictions are provisional, the confidence value is a distance and not a probability, and latency and throughput were not measured. This week closed the implementation phase.",
    ["https://www.overleaf.com/", "https://www.nature.com/articles/s41586-026-10176-5"],
    "We learned to plan, build, test and report in one cycle, and that a report must say what was measured and what was not.",
    "A late change can break a working system. Action: a code freeze before the final run, and two team members checked each statement of the report against the source code.",
    "Technical Writing, Code Freeze, Presentation")


def chunk_url(u, width=14):
    parts = []
    s = u
    while len(s) > width:
        window = s[:width]
        cut = max(window.rfind("/"), window.rfind("."), window.rfind("-"))
        if cut < 6:
            cut = width - 1
        parts.append(s[:cut + 1])
        s = s[cut + 1:]
    parts.append(s)
    return parts


def link_tex(u):
    chunks = chunk_url(u)
    body = r" \\ ".join(r"\textcolor{blue}{\underline{%s}}" % c.replace("%", r"\%").replace("_", r"\_").replace("#", r"\#").replace("&", r"\&") for c in chunks)
    return r"\href{%s}{\begin{tabular}[t]{@{}l@{}}%s\end{tabular}}" % (u, body)


out = []
total = sum(e["hours"] for e in E)
for i, e in enumerate(E):
    date = r"\\".join(e["date"])
    links = r"\\[8pt]".join(link_tex(u) for u in e["links"])
    header = r"\hline Date & Work Summary & Hours worked & Reference Links & Learnings & Risk & Skill \\ \hline" + "\n" if i == 0 else r"\hline" + "\n"
    out.append(r"\begin{tabular}{|p{23pt}|p{146pt}|p{34pt}|p{72pt}|p{66pt}|p{93pt}|p{58pt}|}")
    out.append(header)
    br = lambda t: t.replace("\\_", "\\_\\allowbreak{}")
    out.append(r"\entry{%s}{%d}{%s}{%s}{%s}{%s}{%s}\\ \hline" % (date, e["hours"], br(e["summary"]), links, br(e["learn"]), br(e["risk"]), e["skill"].replace("Authentication","Authen\\-tication").replace("Configuration","Configu\\-ration").replace("Documentation","Docu\\-mentation")))
    out.append(r"\end{tabular}")
    out.append(r"\newpage")
out.append(r"\def\totalhours{%d}" % total)
open("diary_entries.tex", "w").write("\n".join(out) + "\n")
print("entries:", len(E), "total hours:", total, "max hours:", max(e["hours"] for e in E))
