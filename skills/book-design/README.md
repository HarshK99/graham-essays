# Book design package

Generate a book PDF from an original manuscript with the included Windows-tested renderer. This folder is a prepared sharing package, not a separate public release. Copy the entire folder; instructions alone do not reproduce the style.

## Run the original example

In PowerShell, from this folder, with Python 3.14 installed:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --require-hashes -r assets/runtime/requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe scripts/build_book.py assets/original-example.json --workspace "../original book trial"
```

Choose a new workspace name for every run. The command writes sources and settings there, then creates a PDF, build record and independent PDF audit under its `output/`. It refuses an existing workspace to protect previous work. Keep annotated copies separately.

For another manuscript, copy `assets/original-example.json` and change `title`, `author`, `source_credit`, `date`, `sections` and `chapters`. Each chapter has a unique `id`, `title`, `section` and `html`. Use paragraphs, emphasis, headings, quotations, lists, tables, code blocks and linked note anchors. Every chapter must belong to one of your named sections. This compact adapter accepts text HTML; manuscripts with images need saved image records added to the content adapter. It never downloads images automatically.

Use `--settings my-settings.json` for overrides. To remove handwriting margins, use `{"right_notes": 0, "bottom_notes": 0}`. Body size, page size, line spacing, notes size, colours, alignment, cover and writing areas are configurable. The schema/defaults are in `assets/runtime/config/reading-defaults.json`; validation is in `assets/runtime/src/settings.py`.

## What is included

- `SKILL.md`: design guidance for an agent.
- `assets/runtime/`: the actual renderer, print CSS, PDF audit, approved preset, fonts with their licences, and pinned dependencies.
- `assets/original-example.json`: original, redistributable prose, note, table and code example.
- `scripts/build_book.py`: manuscript adapter, fresh-workspace export and audit.
- `references/`: workflow, iteration history and visual checks.
- `LICENSE.txt` and `ATTRIBUTION.md`: reuse terms and boundaries.

This package has no essay collection, inherited image cover, annotations, credentials, personal settings or installed tools. Windows automation checks are distinct from manual reading-app interaction. Check the actual PDF after changing content or formatting; automatic text checks do not judge visual polish or handwriting comfort.

The current approved preset uses 12 pt essay text, 1.25 line spacing, 25% side space and 3.75% bottom space. Contents use 10 pt in two columns, and top titles/numbers link back to Contents. These are configurable choices; `include_images` controls essay pictures separately from the cover.


The approved colour treatment uses burnt-orange accents and apricot rules, charcoal text and white reading pages. The reusable preset keeps a typographic orange cover; this book's specific workbench art is not required or bundled. For your own illustration, set `cover_artwork` to an absolute local image path (with `cover: "typographic"`); title and author remain selectable. `accent_color`, `rule_color` and `cover_color` control page colours. The source reading edition's user confirmed iPad testing complete; other manuscripts still need their own reader review.
