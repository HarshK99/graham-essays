# Windows setup

Setup prepares Python, local folders, the collection tools and the direct PDF builder. Use commands or ask an agent to update saved choices and generate PDFs. Phase 4 will finish this workflow; no app is planned.

## Requirements

Windows with Python 3.14 installed, including pip and venv. This machine uses Python 3.14.7. Internet access is needed for the first dependency installation and Chromium download. Chromium is installed in the per-user Playwright browser cache; exports use local saved content without network requests. Git is needed to obtain the source, but not for the readiness check. No shell activation or administrator access is required.

## Install and check

In PowerShell, download the Windows edition and run:

```powershell
git clone --branch ipad-reading-edition https://github.com/HarshK99/graham-essays.git pg-essays-pdf
Set-Location pg-essays-pdf
python scripts/setup_windows.py
.\.venv\Scripts\python.exe run.py
```

If you already have the project, open its folder and skip the clone command. If `python` selects a different version, use `py -3.14 scripts/setup_windows.py`. The setup command locates the project from its own file path, creates `.venv`, installs the locked dependencies, and runs the readiness check. It can also be invoked from another folder with a quoted full path. No PowerShell execution-policy change is needed.

Success ends with `Windows foundation ready.` The check imports the collection libraries, parses a small in-memory HTML example, checks the original cover fingerprint, and checks that the storage folders are writable. It makes no network requests. This command checks setup; use the PDF builder command below to export.

Rerun the setup command after dependency changes or an interrupted install. It preserves data and settings. If `.venv` belongs to a different Python version, rename it before rerunning setup. If you move the project, recreate `.venv` at the new location; Python environments should not be copied between folders.

## Storage

| Location | Purpose |
| --- | --- |
| `.venv/` | This project's Python and packages; excluded from Git |
| `data/sources/` | Original essay downloads in Phase 2; excluded from Git |
| `data/catalog.json` | Source metadata and download status in Phase 2; excluded from Git |
| `config/` | Shipped defaults and book ordering introduced in later phases |
| `config/reading-settings.json` | Personal saved settings; excluded from Git |
| `output/` | New PDFs and companion records; excluded from Git |
| `cover.png` | Unchanged original cover; reuse permission unresolved |

Setup never deletes or resets these folders. Every sample export uses a new filename and saves a companion settings/source record.

## Dependency maintenance

The root lock file includes exact versions and package hashes. The smaller `requirements.in` describes the direct dependencies. Maintainers can regenerate the lock with:

```powershell
uv pip compile requirements.in --python-version 3.14 --generate-hashes --output-file requirements.txt
```

Normal setup only needs Python, not uv. Do not run `make` or `graham.py` as part of this Windows workflow; the archived pipeline does not meet this edition's content-preservation requirements.

See [progress](progress.md) for the actual commands tested, outcomes, and next phase. See [source review](upstream/PROVENANCE.md) for upstream history, cover terms, and dependency decisions.

## Collect and review (Phase 2)

From the project folder:

```powershell
.\.venv\Scripts\python.exe -m src.collection
.\.venv\Scripts\python.exe -m src.catalog
.\.venv\Scripts\python.exe scripts/check_collection.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Collection uses one request at a time, at least one second between requests, up to three attempts, and finite connection/read timeouts. Progress is saved after each essay. Rerun the collection command after interruption or failure; successful sources are reused. `--refresh` fetches a new index and all sources explicitly. Original versions use filenames based on their content fingerprints and are retained when content changes. A failed refresh is reported even if an older saved version exists.

The catalog command writes `docs/essay-review.md`, with every entry, date precision, status and section. It preserves existing choices. For private edits, copy `config/book.json` to `config/book.local.json`; that file is excluded from Git and takes precedence. Change `section`, `included`, or optional numeric `order`, then rerun the catalog command. The six section names must each appear once. Unknown dates sort last, in website order. The current grouping was approved by the user on 2026-09-09.

Source HTML is retained alongside a reading fragment; emphasis, links, author-note anchors, code and tables remain HTML rather than being flattened into plain text. Image records map original URLs to saved local bytes. Small spacers and title graphics are recorded as decorative and retained in source HTML only. Older promotional banners are still present in reading fragments; Phase 3 must distinguish them from essay text before typesetting. The sample builder removes inspected title/translation/purchase furniture from print output, records removals, and leaves original bytes untouched. See sample-review.md for actual PDF checks.

If the source website changes structure, collection reports an error and keeps saved files. Do not treat a nonzero exit or failed image entry as a complete collection. Downloaded content is local and is not part of the GitHub repository.

Use `.\.venv\Scripts\python.exe -m src.collection --reprocess` to rebuild reading fragments from saved originals without network requests after extraction fixes. Then run the normal collection command to save any newly discovered companion documents. Text companions have reading fragments; PostScript/PDF companions are preserved with an explicit conversion-review flag. A successful download does not mean those print formats have been converted for the book.

## Sample PDF (Phase 3)

Rerun setup after updating to this phase. It installs the pinned PDF libraries and the Chromium version required by Playwright. Then use:

```powershell
.\.venv\Scripts\python.exe -m src.pdf_builder
```

The builder prints the exact new filename. A `.json` file beside it records settings, font versions, source fingerprints, order, excerpts, removals and excluded/outside-sample entries. The normal sample is a short trial of five pieces: complete Writing, Briefly and Modeling a Wealth Tax; opening excerpts of How to Do Great Work, Five Questions about Language Design and the second ANSI Common Lisp chapter. Referenced author notes accompany excerpts; return labels are disabled in the approved preset. The complete chapter attribution stays in the code sample.

For the longer proof containing all five complete pieces:

```powershell
.\.venv\Scripts\python.exe -m src.pdf_builder --complete-essays
```

For personal page settings:

```powershell
Copy-Item config/reading-defaults.json config/reading-settings.json
.\.venv\Scripts\python.exe -m src.pdf_builder --settings config/reading-settings.json
```

Copy the preset only the first time, so you retain your changes. Settings files can contain only the fields you want to override. Sizes are PDF points, with 72 points per inch; writing-space fractions use `0.25` for the approved 25% right space and `0.075` for 7.5% bottom space. Available font families are the three bundled Source families. Keep their font files and licence notices in `assets/fonts/`. Invalid geometry, missing fonts and unknown settings produce a visible error.

Set `notes_background` to `blank` or `dots`. Set `cover` to `typographic` or the path of a local image you are entitled to use. Relative cover paths are resolved from the project folder. `--essays` accepts saved catalog IDs and exports complete selected pieces in the current book order; it rejects excluded, unknown and repeated IDs. `--output` changes the export folder. Every export has a unique filename and contains no personal annotations.

To audit the actual PDF, use its filename from the export message:

```powershell
.\.venv\Scripts\python.exe scripts/check_pdf.py output/<actual-new-filename>.pdf
```

Replace the angle-bracket filename with the real filename; it is not a literal command argument. The audit writes `.checks.json` beside the PDF and exits with an error if it finds a problem. It checks text against prepared sources, font embedding, text/image bounds, internal links, bookmarks and empty reading pages. It does not replace visual inspection or the iPad trial.

Transfer the trial to Files on the iPad using your usual file-transfer method, then open/import the same file in Preview and Goodnotes. Use [the sample review guide](sample-review.md) for the trial. Keep any annotated copy under its own name; generating a new PDF never brings across your previous highlights or handwriting. The full-collection export workflow remains to be finished. Sources with unresolved full-text companions are rejected rather than exported as complete articles.
