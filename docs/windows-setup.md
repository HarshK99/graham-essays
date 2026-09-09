# Windows setup

Setup prepares Python and local folders. Phase 2 adds the collection commands below. There is no browser app or PDF builder yet.

## Requirements

Windows with Python 3.14 installed, including pip and venv. This machine uses Python 3.14.7. Internet access is needed for the first dependency installation. Git is needed to obtain the source, but not for the readiness check. No shell activation or administrator access is required.

## Install and check

In PowerShell, download the Windows edition and run:

```powershell
git clone --branch ipad-reading-edition https://github.com/HarshK99/graham-essays.git pg-essays-pdf
Set-Location pg-essays-pdf
python scripts/setup_windows.py
.\.venv\Scripts\python.exe run.py
```

If you already have the project, open its folder and skip the clone command. If `python` selects a different version, use `py -3.14 scripts/setup_windows.py`. The setup command locates the project from its own file path, creates `.venv`, installs the locked dependencies, and runs the readiness check. It can also be invoked from another folder with a quoted full path. No PowerShell execution-policy change is needed.

Success ends with `Windows foundation ready.` The check imports the collection libraries, parses a small in-memory HTML example, checks the original cover fingerprint, and checks that the storage folders are writable. It makes no network requests. This is a command-line foundation check, not the future browser app.

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

Setup never deletes or resets these folders. New export filenames are a later builder requirement, not an implemented Phase 1 feature.

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

Source HTML is retained alongside a reading fragment; emphasis, links, author-note anchors, code and tables remain HTML rather than being flattened into plain text. Image records map original URLs to saved local bytes. Small spacers and title graphics are recorded as decorative and retained in source HTML only. Older promotional banners are still present in reading fragments; Phase 3 must distinguish them from essay text before typesetting. No converted PDF has been checked yet.

If the source website changes structure, collection reports an error and keeps saved files. Do not treat a nonzero exit or failed image entry as a complete collection. Downloaded content is local and is not part of the GitHub repository.

Use `.\.venv\Scripts\python.exe -m src.collection --reprocess` to rebuild reading fragments from saved originals without network requests after extraction fixes. Then run the normal collection command to save any newly discovered companion documents. Text companions have reading fragments; PostScript/PDF companions are preserved with an explicit conversion-review flag. A successful download does not mean those print formats have been converted for the book.
