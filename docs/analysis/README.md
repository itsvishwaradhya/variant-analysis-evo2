# Analysis artifacts for the Evo2Serve paper

Every number in `paper-ieee.tex` is produced by one of the scripts in this
directory. The scripts read only files that are already in the repository,
except where noted, so the results are reproducible without a graphics
processor.

## Requirements

```
evo2-backend/venv/Scripts/python.exe -m pip install pandas numpy scikit-learn \
    biopython openpyxl matplotlib seaborn
```

Node.js 22 or later is needed for the browser-side script. The scripts use
`node --experimental-strip-types` and import the real TypeScript sources, so
no transpilation step is required.

## Scripts

| Script | Produces | Network |
|---|---|---|
| `a_dataset_characterization.py` | Composition of the BRCA1 assay and of the 500-row calibration slice; reference-window construction; the 8193 versus 8192 window difference; de-duplication counts | no |
| `b_baseline_predictors.py` | AUROC, bootstrap intervals and Youden operating points for CADD, PolyPhen-2, SIFT, aGVD, phyloP, gnomAD allele frequency and a recoded ClinVar call | no |
| `c_assembly_provenance.py` | The GRCh37 to GRCh38 offset at BRCA1, the reference-base and window-identity consequences, and the shipped example payload | yes (UCSC, NCBI) |
| `d_validation_conformance.py` | The verdict of the Pydantic model in `evo2-backend/main.py` over the canonical case list | no |
| `e_clinvar_conformance.mjs` | The verdict of the Zod schema in `evo2-frontend/src/app/api/analyze/route.ts` over the same case list, plus the live ClinVar conformance measurements | yes (NCBI) |
| `f_cross_layer.py` | The agreement between the two validators, joined on the canonical case list | no |
| `g_scoring_contract.py` | The behaviour of the deployed scoring contract, exercised with a stand-in scorer | no |
| `h_figure_data.py` | `figure_data.tex`, the coordinate series consumed by the figures | no |

## Running everything

```powershell
$py = "evo2-backend\venv\Scripts\python.exe"
& $py docs/analysis/a_dataset_characterization.py
& $py docs/analysis/b_baseline_predictors.py
& $py docs/analysis/c_assembly_provenance.py
& $py docs/analysis/d_validation_conformance.py
node --experimental-strip-types docs/analysis/e_clinvar_conformance.mjs
& $py docs/analysis/f_cross_layer.py
& $py docs/analysis/g_scoring_contract.py
& $py docs/analysis/h_figure_data.py
```

Each script also writes a JSON file next to itself, so the numbers in the
paper can be checked against the machine-readable output.

## The canonical request matrix

`validation_cases.json` holds the 55 request cases used by scripts `d`, `e`
and `f`. Each case carries an expected verdict derived from the request
schema and the documented limits, not from either implementation, so a
disagreement between the two layers is a defect.

## Building the paper

The paper reads `figure_data.tex` from this directory, so compile it from
the repository root:

```powershell
pdflatex -interaction=nonstopmode paper-ieee.tex
pdflatex -interaction=nonstopmode paper-ieee.tex
```

## What is not reproduced here

No Evo 2 score is generated, because the evaluation environment has no
graphics processor. The paper therefore reports no AUROC for the deployed
service, and states which claims follow from the contract alone and which
would require a run on a graphics processor.
