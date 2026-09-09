# Paul Graham — iPad Reading Edition

A Windows project for turning Paul Graham's essays into a PDF with room to read, highlight, and write handwritten notes. The planned reading trial uses an iPad A16 with Preview or Goodnotes.

Status: saved settings and sample/full PDF commands are available. Phase 3's revised sample and essay grouping are approved. Full-collection checks currently block 11 entries that need print preparation; the exporter reports them before creating a PDF. See [sample review](docs/sample-review.md), [Windows commands](docs/windows-setup.md#saved-choices-and-full-export-phase-4) and [tested progress](docs/progress.md). No app is required.

## Windows setup

Install Python 3.14 and Git for Windows, then run these commands in PowerShell. Codex is not required to run the project.

```powershell
git clone --branch ipad-reading-edition https://github.com/HarshK99/graham-essays.git pg-essays-pdf
Set-Location pg-essays-pdf
python scripts/setup_windows.py
.\.venv\Scripts\python.exe run.py
```

This installs the collection/PDF tools and Chromium, the browser used to print the PDF, and checks local storage. It does not download essays or open an app. See [Windows setup](docs/windows-setup.md) for details.

Expected result: `Windows foundation ready.` Setup has been checked on Windows with Python 3.14.7, including a fresh folder with spaces in its name. PDF checks are recorded in the sample review; sample layout approval is recorded, while detailed device checks remain for the full-book review.

## Download and organise essays

After setup, run in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m src.collection
.\.venv\Scripts\python.exe -m src.catalog
.\.venv\Scripts\python.exe scripts/check_collection.py
```

The first command saves the article index, original pages, reading content and images in `data/`. It pauses between requests and saves progress after every essay. Run it again to retry failures without downloading successful essays again. Use `--refresh` only when you want to fetch the latest index and sources; older source bytes remain saved.

Read [the approved essay order](docs/essay-review.md). `config/book.json` holds the approved grouping; copy it to `config/book.local.json` before making personal changes. The catalog command prefers that local file when present. Changing a section or setting `included` to `false` preserves the downloaded original. The current grouping is user-approved; Lisp is last by default. Missing dates are marked rather than guessed.

## Generate a reading trial

After downloading the collection, run:

```powershell
.\.venv\Scripts\python.exe -m src.pdf_builder
```

The command prints the new PDF location under `output/` and saves a companion JSON record of its settings and sources. The default trial contains complete short/table essays and labelled excerpts of longer prose and Lisp code, including referenced author notes. Use `--complete-essays` for the longer five-piece proof.

Create `config/reading-settings.json` for personal formatting; it is reused automatically by every sample/full export. Missing fields inherit approved defaults. See [configuration examples and backup/reset steps](config/README.md). You can also choose a settings file explicitly:

```powershell
.\.venv\Scripts\python.exe -m src.pdf_builder --settings config/reading-settings.json
```

Fonts, page dimensions, spacing, writing margins, colours and cover selection are configurable. The default is an original typographic cover; the inherited image remains preserved with unresolved reuse terms. Read [Windows setup](docs/windows-setup.md) for all options and [the iPad trial guide](docs/sample-review.md) for what to check. Keep annotated copies separately: new exports contain no notes from older copies.

## Selected essays and full export

```powershell
.\.venv\Scripts\python.exe -m src.catalog --list
.\.venv\Scripts\python.exe -m src.pdf_builder --essays 3855b9d49700d8423e1e
.\.venv\Scripts\python.exe -m src.pdf_builder --full --check
.\.venv\Scripts\python.exe -m src.pdf_builder --full
```

The first command lists titles and their stable IDs. The second exports complete Writing, Briefly. `--full --check` checks every included essay without printing; `--full` exports that complete selection using the same saved settings and book order. Unlike `--complete-essays`, `--full` selects all included entries. Both currently report the collection's 11 preparation blockers; no partial book is saved and no entries are silently dropped. Resolving those blockers and verifying the final book belongs to Phase 5.

You can ask an agent: “Make the right writing space 20% and export a sample.” It should update the personal file, run these same commands, check the resulting PDF and report its new filename.

## What is available

| Stage | Status |
| --- | --- |
| Windows setup and local storage | Complete |
| Essay downloads and subject grouping | Complete; grouping approved |
| Sample PDF and iPad trial | Complete; revised sample approved |
| Saved settings and command-line export workflow | Complete; full export reports remaining content blockers |
| Full book and reusable book-design guide | Planned — Phase 5 |

This is an early development version. Samples are generated locally; full-export mechanics are tested on an original manuscript, while the final collection PDF is still to come. The book-design skill is a draft, to be finalised and independently validated in Phase 5.

## Project documents

- [Start a phase](docs/commands/phase.md): use `/phase N` in a new project chat, or `Start phase N` if the app intercepts the slash form.
- [Progress and handoff](docs/progress.md): what is complete and what the next chat should do.
- [Design specification](docs/design.md): agreed requirements, initial page settings, essay sections, and the command-line and agent workflow.
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
- Windows commands and saved configuration files for fonts, spacing, margins, section order, and essay selection; an agent can make changes on request.
- A short sample export for checking the layout on the iPad before building the whole book.
- Published-book design quality and a reusable book-design skill, refined during sample design and finalised with the finished book.

The sample exporter creates a new file every time. Notes added in Preview or Goodnotes will belong to that particular PDF or app document; new exports will start without those notes.

## Starting point

Based on [ofou/graham-essays](https://github.com/ofou/graham-essays), revision `96885e3b4018f0f1d976634e26b27a86e94aacfc`, by Omar Olivares. The original macOS/Linux build remains as a reference; the Windows commands above use a separate setup. Development of this edition lives on `ipad-reading-edition`.

## Attribution and reuse status

The essays are Paul Graham's writing. The original cover and its attribution are preserved. No upstream licence was found at the inspected revision, and cover reuse permission remains unconfirmed. This repository does not establish redistribution permission for those materials. See the [source and cover review](docs/upstream/PROVENANCE.md) for the evidence.

Downloaded essays, generated PDFs, personal settings, and local Python environments are excluded from source commits. Sharing this repository is separate from publishing an essay collection.
