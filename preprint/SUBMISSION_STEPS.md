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

1. Go to https://zenodo.org and sign up or log in (ORCID, GitHub or a local account all work). You must **confirm your e-mail address** before your first upload. One team member uses his or her own account; the record will list all authors.
2. Click the **plus icon** in the header and choose **New upload**.
3. Drag in `paper-preprint.pdf` (the final one after step A.6).
4. Fill the form from `zenodo_metadata.md`: resource type **Preprint**, title, the five authors with affiliation (ORCID optional), description (the abstract), keywords, language English, licence CC BY 4.0 (Zenodo's default), version 1, publisher left at its default "Zenodo", and the related identifier (is supplemented by, the repository URL). Resource type, creators, licence and publisher are the required fields.
5. Click **Save draft**, then **Preview**, and read the preview carefully. If you want to print the DOI in the paper before you publish, answer "No" to the question about an existing DOI and click **Get a DOI now!** (if you delete the draft, the reserved DOI is lost).
6. When everyone has agreed, click **Publish**. Do not rely on being able to change the PDF afterwards: Zenodo's help pages say files cannot be modified once published, with a short window for minor corrections (the pages quote 30 and 45 days) and later changes only in justified cases. Check the final PDF before you publish. Metadata can be edited at any time without changing the DOI. A corrected file needs a **New version**, which is a separate record with its own DOI, linked to the other versions. The owner can delete a record only within 30 days after publication.

## C. After publishing

1. Open the record, copy the DOI, and add it to the repository README (for example "Preprint: https://doi.org/10.5281/zenodo.XXXXXXX").
2. To also get a DOI for the **code**, link the repository to Zenodo: in Zenodo go to your account > GitHub, switch the repository on, then create a GitHub **Release**. Zenodo archives that release and gives it its own DOI. Add the code DOI as a related identifier on the paper record (this is a metadata edit; it does not need a new version).
3. You may later submit the same work to a journal or conference. Check that venue's preprint policy first; most allow it.

## D. Reminders

- This is a **research and education tool**, not a clinical classifier; keep that wording.
- The Evo 2 accuracy figure of about 0.73 in the paper is a **preliminary, non-archived** number. Do not quote it elsewhere as a validated result. If you re-run the calibration on the GPU and archive the per-variant output, update the paper and upload it as a new version.
- Do not add e-mail addresses or other personal data to the paper or the Zenodo record.

## E. What to expect, checked against the official pages (27 Nov 2026)

- **Zenodo** has no review before ordinary publication; the DOI is issued when you publish. Hosting is not an endorsement, and the uploader is responsible for the content. It has no rule against AI-assisted text; keep the honest AI statement in the paper anyway.
- **Research Square** (alternative or addition): free preprint with a DOI, typically posted within about 72 business hours, with screening for ethics and competing-interest statements and for inappropriate claims; no peer review. It requires complete methods and results sections, will not post work already published in a journal, and wants any use of an AI language model documented in the Methods. Check its current submission page before relying on it.
- **arXiv** is unlikely to be live within two weeks: new submitters need an endorsement from an established arXiv author, moderation can take days, and its pages say course projects and undergraduate research are typically not accepted unless the advisor supports them.
- **Peer-reviewed journals**: none could decide within two weeks. The fastest free (no-APC) DOAJ listings found state about 5 weeks or more from submission to publication; JOSS requires six months of public repository history and has strict scope rules (your repository's history is about three months); Bioinformatics Advances charges an article fee (up to USD 2620 per DOAJ, with a waiver policy). Plan a journal submission for after the preprint, and check each venue's preprint policy first.
