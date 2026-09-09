# Trial workflow — not an approved preset

This reference applies to the surrounding reading-edition repository. The draft skill is not yet a standalone reproduction package. Phase 5 will supply the approved preset/templates and exercise it in a separate clean folder.

The actual engine is Python Playwright controlling Chromium's direct HTML-to-PDF print path. pypdf joins essay PDFs, installs the section/essay outline and contents destinations, and overlays global page numbers. PDFium renders pages and reads text positions for verification. See the repository's locked `requirements.txt`, `templates/book.css`, `src/print_content.py`, `src/pdf_builder.py`, and `scripts/check_pdf.py`.

The trial preset is `config/reading-defaults.json`: 612 × 880 pt, 36 pt outer margins, 24 pt header/footer bands, Source Serif 4 at 14 pt with 1.45 line height, 10 pt paragraph spacing, Source Sans 3 labels, and Source Code Pro at 11 pt. The 540 × 760 pt usable area yields a 364 × 646 pt reading column, 14 pt gap, 162 pt side notes, and 114 pt bottom notes. These are adjustable trial values, not universal book dimensions.

Fonts and original OFL licences are bundled in `assets/fonts/`; `manifest.json` records exact upstream revisions and file fingerprints. Font embedding and missing-file failures must be checked after changing families. The upstream image cover is preserved separately and is not part of the permitted skill asset package.

From the repository folder on Windows:

```powershell
python scripts/setup_windows.py
.\.venv\Scripts\python.exe -m src.pdf_builder
.\.venv\Scripts\python.exe scripts/check_pdf.py output/<actual-new-filename>.pdf
```

The normal sample uses explicitly labelled opening excerpts plus their linked notes for long material, and complete short/table essays. `--complete-essays` creates the longer five-piece proof. `--settings config/reading-settings.json` applies personal JSON overrides. `--essays <saved-id> ...` uses complete selected pieces in the configured book order. All commands require saved source data; this draft does not bundle a manuscript.

Read `docs/sample-review.md` for observed iterations and pending reader feedback. Review first/last pages, every section boundary, notes, code, images, tables and the audit's sparse-page list. In Phase 5, separate general manuscript adapters from collection-specific rules, copy the approved style resources into the package, and test with original writing outside `output/`.
