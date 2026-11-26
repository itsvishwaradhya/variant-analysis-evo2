# How to publish the preprint on Zenodo (for the project team)

Zenodo (https://zenodo.org) is a free repository run by CERN. It gives your upload a permanent DOI. It does **not** peer review or edit anything, so what you upload is exactly what the world will see. The upload must be done by you, from your own account, because it is a public and permanent act in your names. Nothing has been uploaded for you.

## A. Before you upload (checklist: do every item)

1. **Make the GitHub repository public and add a licence.**
   - Repository: https://github.com/itsvishwaradhya/variant-analysis-evo2 (Settings > General > Danger Zone > Change visibility > Public).
   - Add an OSI-approved licence file, for example MIT or Apache-2.0 (GitHub: Add file > Create new file > name it `LICENSE`, and use the "Choose a license template" button). The paper says the code is in this repository, so it must be reachable.
   - Check that no secrets are committed: `.env` files, JWT secrets, database URLs, API keys. If any were ever committed, rotate them first.
2. **All authors consent.** All four student authors and Dr. Nandini K S must read the paper and agree to be listed, in this order: Nandish S Shet, Thippeswamy S, Vishwaradhya A C, Jeevan A M, Dr. Nandini K S. Get this in writing (a message in the group is enough). Also check with the department or guide whether any institute approval is required before a preprint is posted.
3. **Fill the five bracketed items in the paper** (Declarations section of `paper-preprint.tex`), then rebuild the PDF:
   - `Author contributions: [to be completed by the authors]` replace with an honest description of who did what.
   - `Competing interests: None declared [authors to confirm]` confirm, then delete the bracket.
   - `Funding: None declared [authors to confirm]` confirm, then delete the bracket. If your work was supported by a funding body or a student project programme, name it here and in the Acknowledgment.
   - `AI assistance ... [authors to confirm that they have read the whole manuscript, re-run the scripts and checked every reported number]` do this for real (re-run the scripts in `docs/analysis`, compare with the paper), then delete the bracket.
   - `Relation to earlier work ... [authors to confirm that no earlier version has been published elsewhere]` confirm, then delete the bracket.
4. **Re-read the whole paper** together. Check every number against the files in `docs/analysis`, check names and spellings, and make sure every author can explain every section. The AI-assistance statement is in the Declarations; keep it.
5. **Run a similarity check** (for example the one provided by your institute library, or any plagiarism checker your department uses) and fix any passage that is too close to another source.
6. **Rebuild the PDF** after your edits: `pdflatex paper-preprint.tex` twice. Open the PDF and look at every page.
7. Decide the licence. The recommendation is CC BY 4.0 for the paper.

## B. Upload steps on Zenodo

1. Go to https://zenodo.org and log in (a GitHub or ORCID login works). One team member uses his or her own account; the record will list all authors.
2. Click **Upload** (or **New upload**).
3. Drag in `paper-preprint.pdf` (the final one after step A.6).
4. Fill the form from `zenodo_metadata.md`: resource type **Publication / Preprint**, title, the five authors with affiliation (ORCID optional), description (the abstract), keywords, language English, licence CC BY 4.0, version 1, and the related identifier (is supplemented by, the repository URL).
5. Click **Save** and read the preview carefully. Use **Reserve DOI** if you want to print the DOI in the paper before you publish.
6. When everyone has agreed, click **Publish**. After publishing you cannot change the file of that version, but you can make a new version later (Zenodo "New version") and the DOI will point to all versions.

## C. After publishing

1. Open the record, copy the DOI, and add it to the repository README (for example "Preprint: https://doi.org/10.5281/zenodo.XXXXXXX").
2. To also get a DOI for the **code**, link the repository to Zenodo: in Zenodo go to your account > GitHub, switch the repository on, then create a GitHub **Release**. Zenodo archives that release and gives it its own DOI. Add the code DOI as a related identifier on the paper record (new version of the record).
3. You may later submit the same work to a journal or conference. Check that venue's preprint policy first; most allow it.

## D. Reminders

- This is a **research and education tool**, not a clinical classifier; keep that wording.
- The Evo 2 accuracy figure of about 0.73 in the paper is a **preliminary, non-archived** number. Do not quote it elsewhere as a validated result. If you re-run the calibration on the GPU and archive the per-variant output, update the paper and upload it as a new version.
- Do not add e-mail addresses or other personal data to the paper or the Zenodo record.
