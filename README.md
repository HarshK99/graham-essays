# Paul Graham — iPad Reading Edition

A Windows project for turning Paul Graham's essays into a PDF with room to read, highlight, and write handwritten notes. The planned reading trial uses an iPad A16 with Preview or Goodnotes.

Status: Phase 2 collection tools implemented; setup verification is recorded in [progress](docs/progress.md). The upstream history and cover are preserved, and [the GitHub fork](https://github.com/HarshK99/graham-essays) exists. The collection can be downloaded locally and its proposed sections reviewed. No browser app or generated PDF exists yet.

## Windows setup

Install Python 3.14 and Git for Windows, then run these commands in PowerShell. Codex is not required to run the project.

```powershell
git clone --branch ipad-reading-edition https://github.com/HarshK99/graham-essays.git pg-essays-pdf
Set-Location pg-essays-pdf
python scripts/setup_windows.py
.\.venv\Scripts\python.exe run.py
```

This installs the collection foundation and checks local storage. It does not download essays or open an app. See [Windows setup](docs/windows-setup.md) for details.

Expected result: `Windows foundation ready.` Setup has been checked on Windows with Python 3.14.7, including a fresh folder with spaces in its name. Browser, PDF, and iPad checks are still ahead.

## Download and organise essays

After setup, run in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m src.collection
.\.venv\Scripts\python.exe -m src.catalog
.\.venv\Scripts\python.exe scripts/check_collection.py
```

The first command saves the article index, original pages, reading content and images in `data/`. It pauses between requests and saves progress after every essay. Run it again to retry failures without downloading successful essays again. Use `--refresh` only when you want to fetch the latest index and sources; older source bytes remain saved.

Read [the proposed essay order](docs/essay-review.md). `config/book.json` holds the shipped proposal; copy it to `config/book.local.json` before making personal changes. The catalog command prefers that local file when present. Changing a section or setting `included` to `false` preserves the downloaded original. All groupings await user review; Lisp is last by default. Missing dates are marked rather than guessed.

## What is available

| Stage | Status |
| --- | --- |
| Windows setup and local storage | Complete |
| Essay downloads and subject grouping | Available; proposed order awaits review |
| Sample PDF and iPad trial | Planned — Phase 3 |
| Local browser app with saved choices | Planned — Phase 4 |
| Full book and reusable book-design guide | Planned — Phase 5 |

This is an early development version, with no ready-to-read book or app download. The roadmap describes intended behaviour, not features already delivered.

## Project documents

- [Start a phase](docs/commands/phase.md): use `/phase N` in a new project chat, or `Start phase N` if the app intercepts the slash form.
- [Progress and handoff](docs/progress.md): what is complete and what the next chat should do.
- [Design specification](docs/design.md): agreed requirements, initial page settings, essay sections, and the proposed app experience.
- [Phased plan](docs/superpowers/plans/2026-09-09-ipad-reading-edition.md): delivery order, planned files, and checks for each phase.
- [Decisions and evidence](docs/decisions.md): confirmed choices, proposals, source links, and what has not been tested.
- [Documentation guide](docs/README.md): where to find setup, design, and development details.
- [Contributing](CONTRIBUTING.md): report problems or propose changes.

## Intended result

- One main PDF, divided into broad subject sections, with Lisp essays last.
- A cover, with PDF pages generated directly from essay content.
- A wide writing margin on the right and a smaller writing area at the bottom of every reading page.
- No extra blank notes page after each essay.
- Selectable text for highlighting, clickable contents, and section/essay bookmarks.
- A Windows app with adjustable fonts, spacing, margins, section order, and essay selection.
- A short sample export for checking the layout on the iPad before building the whole book.
- Published-book design quality and a reusable book-design skill, refined during sample design and finalised with the finished book.

The planned exporter will create a new file every time. Notes added in Preview or Goodnotes will belong to that particular PDF or app document; new exports will start without those notes.

## Starting point

Based on [ofou/graham-essays](https://github.com/ofou/graham-essays), revision `96885e3b4018f0f1d976634e26b27a86e94aacfc`, by Omar Olivares. The original macOS/Linux build remains as a reference; the Windows commands above use a separate setup. Development of this edition lives on `ipad-reading-edition`.

## Attribution and reuse status

The essays are Paul Graham's writing. The original cover and its attribution are preserved. No upstream licence was found at the inspected revision, and cover reuse permission remains unconfirmed. This repository does not establish redistribution permission for those materials. See the [source and cover review](docs/upstream/PROVENANCE.md) for the evidence.

Downloaded essays, generated PDFs, personal settings, and local Python environments are excluded from source commits. Sharing this repository is separate from publishing an essay collection.
