# Windows setup

Phase 1 prepares Python and local folders. It does not yet open an app, download essays, or generate a PDF.

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
