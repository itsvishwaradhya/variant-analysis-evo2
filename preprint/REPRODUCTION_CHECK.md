# Reproduction and repository-safety check (done in the AI-assisted session, 26 Nov 2026)

This records checks made for step A of `SUBMISSION_STEPS.md`. It does **not** replace the authors' own confirmation: the paper's AI-assistance statement still has a bracket asking the authors to confirm they re-ran the scripts and checked every number. Repeat the commands below yourselves, then delete the bracket.

## 1. Analysis scripts re-run from a clean virtual environment

Packages: pandas, numpy, scikit-learn, biopython, openpyxl, matplotlib, seaborn, modal, fastapi, pydantic, pyjwt, requests. Each script was run from the repository root (`python docs/analysis/<script>.py`). After the runs, `git status` showed **no changed files** in `docs/analysis`, so every regenerated JSON file is byte-for-byte identical to the committed one.

| Script | What it produces | Result |
|---|---|---|
| `a_dataset_characterization.py` | assay composition, slice, 8193 vs 8192 window | identical |
| `b_baseline_predictors.py` | AUROC, bootstrap intervals, Youden points | identical |
| `d_validation_conformance.py` | Pydantic verdicts on the 55-case matrix (`d_pydantic_cases.json`) | identical |
| `f_cross_layer.py` | Pydantic vs Zod comparison | identical |
| `g_scoring_contract.py` | scoring contract with a stand-in scorer | identical |
| `h_figure_data.py` | figure data and `figure_data.tex` | identical |

Not re-run: `c_assembly_provenance.py` and `e_clinvar_conformance.mjs` query live UCSC and NCBI services, and the Evo 2 calibration job needs a GPU. Their committed outputs are what the paper reports. Note the limitation recorded in `docs/analysis/README.md`: the same-coordinate fields in `c_assembly_provenance.json` are artefacts and the paper does not use them.

`docs/analysis/d_validation_conformance.json` is an older output (65 cases, 61 conforming) that the current script no longer writes; the paper uses the 55-case files. Consider deleting that stale file.

To repeat: create a virtual environment, install the packages above, run the six commands, then run `git status docs/analysis` (it should print nothing).

## 2. Secrets scan of the repository (tracked files and all history)

- No `.env` file, key, token or credential is tracked or was ever committed. The only match is `evo2-frontend/.env.example`, which holds placeholders (`replace-with-64-hex-chars...`, a localhost MongoDB URL).
- `.gitignore` excludes `evo2-frontend/.env` and `evo2-backend/.env`.
- Patterns searched across all commits: JWT/Mongo values, `mongodb://user:pass@`, AWS keys, GitHub tokens, OpenAI/Hugging Face style keys, private-key blocks and Modal tokens. None found.
- Still do your own check before going public: look at the Modal secret (`auth-secret`) and your deployed `JWT_SECRET`; they are not in the repository, which is correct. Rotate them if they were ever pasted into a chat, issue or screenshot.

Limits: this is a pattern search, not a full secret-scanning service. GitHub's own secret scanning (Settings > Code security) can be switched on after the repository is public.
