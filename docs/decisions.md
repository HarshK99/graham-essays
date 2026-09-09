# Decisions and evidence

## Confirmed by the user

| Decision | Outcome |
| --- | --- |
| Device | iPad A16 |
| Reading apps available | Preview and Goodnotes |
| Writing space | Right margin plus some bottom space on every reading page |
| Extra notes pages | None after essays |
| Organisation | Broad subject sections in one book |
| Lisp placement | End of the main book |
| Formatting | Approved defaults, configurable through saved files, commands or agent requests |
| Current work | Phase 5 in progress; 224-essay selection, excluding the final Lisp section |
| New exports | New files, without notes from previous copies |
| Cover | Required; retain upstream cover for reuse after checking terms |
| PDF route | Generate directly from essay content, without EPUB as an intermediate |
| Phase execution | New project chat per phase using `/phase N` or `Start phase N` |

## Confirmed reusable skill deliverable

Additional confirmed deliverable: a reusable book-design skill, drafted during Phase 3 and finalised in Phase 5 from the iterated, approved PDF design. It must include the required supporting settings/templates, be tested on a separate original sample, and be prepared for others to use. Public publication is not part of this documentation update.

## Approved sample defaults and workflow

- Source Serif 4 body text and Source Sans 3 labels.
- Current approved body text is 12 pt with 1.25 line height, justified prose, white background; 12 pt author notes.
- Right notes area 25% of usable width; bottom area 3.75% of usable height, with a faint bottom separator. Title and page number share the top line; no note-return labels.
- Six sections listed in the design specification, with chronological order within each.
- Windows command-line tools with saved configuration files; an agent can edit choices and run exports. No browser or desktop app is required.

## Evidence already inspected

- [Upstream Makefile](https://github.com/ofou/graham-essays/blob/main/Makefile): explicitly recognises macOS and Linux, uses Unix shell commands, and rejects other systems. The PDF target uses Calibre's ebook-convert after EPUB generation. The default target does not include PDF generation.
- [Upstream downloader](https://github.com/ofou/graham-essays/blob/main/graham.py): retrieves essays and converts them to Markdown, a plain-text document format. It ignores images and tables and transforms author notes, so content fidelity needs review before reuse.
- [Apple Preview annotation guide](https://support.apple.com/guide/ipad/annotate-a-pdf-or-image-ipad158dad0a/ipados): documents text highlighting and handwritten markup on iPad.
- [Goodnotes features](https://www.goodnotes.com/features/): describes PDF annotation and handwriting search.
- [Goodnotes document outlines](https://support.goodnotes.com/hc/en-us/articles/7353757101071-Create-and-manage-document-outlines): describes importing and using PDF outlines for navigation.
- [Goodnotes PDF hyperlinks](https://support.goodnotes.com/hc/en-us/articles/13623343439631-Open-hyperlinks-in-imported-PDFs): describes following links within imported PDFs.

These observations came from source and documentation inspection during discussion. Recheck the upstream revision when implementation starts. No upstream build or iPad trial has been run.

## Choices to resolve through the planned work

| Choice | How it will be resolved |
| --- | --- |
| Final PDF generation tool | Compare output on Windows against text selection, font embedding, links, bookmarks, and page layout requirements |
| Page dimensions and typography | Export sample, then read and write on the actual iPad |
| Final subject assignments | Review essay content and the grouped list, flagging uncertain cases |
| Preview or Goodnotes | Try the same sample in both |
| Fork setup and reuse terms | Inspect upstream history, licence, and asset permissions before adapting or publishing; do not assume permission for public redistribution of essay text |

The font choices are proposals, not a verified claim that they are best for every reader. Font files, embedding permissions, and rendering still need to be checked during implementation.

## Phase 1 implementation — 2026-09-09

- Native Windows setup is implemented and tested with Python 3.14.7 in fresh project environments, including a path with spaces. Setup creates `.venv` and installs exact dependency versions with package hashes; it needs no Bash, make, or Linux tools.
- Requests and Beautiful Soup form the minimal collection foundation. The old downloader and build files are retained for reference but are not executed by setup. Phase 2 must preserve original HTML and avoid the old converter's losses and inferred dates.
- The GitHub fork exists at https://github.com/HarshK99/graham-essays. Local history starts from upstream revision `96885e3b4018f0f1d976634e26b27a86e94aacfc`; project adaptations are committed and pushed on `ipad-reading-edition`, now the fork's default branch.
- Original upstream instructions are archived, with this project's Windows/direct-PDF requirements taking precedence. Automatic EPUB build/release workflows are archived outside the active workflow folder.
- Original `cover.png` is preserved with a recorded fingerprint. No upstream licence was found and cover reuse permission remains unresolved; preservation is not approval for redistribution. A required cover can be original typography if the inherited asset remains unapproved at sample time.
- `run.py` currently checks readiness only. Data, saved settings, and output locations are established without claiming an app or PDF builder. Font, PDF-tool, visual, and iPad choices remain open as planned.

Details and evidence: [source review](upstream/PROVENANCE.md), [tested setup](windows-setup.md), and [phase log](progress.md).

## Phase 2 implementation - 2026-09-09

The live article index yielded 234 unique entries, all now saved locally. Sources retain URL, retrieval time, original-byte fingerprint, explicit date precision and status. Reading fragments preserve emphasis, notes, tables, code and links, including sibling-row download links. Known decorative spacers/footer icons are recorded rather than silently counted as missing essay images.

Ten linked author-hosted documents are also saved. The Roots of Lisp page is only an introduction: its complete PostScript article requires conversion before full export. Lisp for Web-Based Applications has a ready plain-text companion. A PostScript version of Being Popular is also retained, alongside its available HTML. Do not confuse successful acquisition with completed print-format conversion.

The six default sections and all 234 inclusion choices are shipped in `config/book.json`. Five unknown publication dates stay unknown; a printed year stays year-only. A content-based first pass plus review of openings and ambiguous cases produced the proposed grouping, with overlap reasons retained. The user approved this grouping on 2026-09-09. Personal edits belong in ignored `config/book.local.json`, which takes precedence; source data never depends on these choices.

The collector and catalog are command-line tools in this phase. `run.py` still checks the foundation. No new dependencies, PDF tool, app interface or iPad-approved settings have been introduced. See [collection checks](collection-checks.md) and [essay review](essay-review.md).

## Phase 3 implementation — 2026-09-09

Selected Playwright/Chromium for direct PDF printing after native Windows output checks. pypdf supplies explicit section/essay bookmarks, contents destinations and global numbering; PDFium independently renders and checks the PDF. Exact dependencies are locked. See [sample review](sample-review.md) for primary documentation links and actual evidence.

Bundled unmodified Source Serif 4, Source Sans 3 and Source Code Pro files from pinned Adobe repository revisions, with original OFL notices and fingerprints. Fonts used in the final PDFs are embedded. The original typographic cover avoids relying on unconfirmed upstream-image permission; configurable local image covers are supported.

Trial dimensions are 612 × 880 pt with 36 pt margins, 24 pt header/footer bands, 14 pt body at 1.45 line height and 11 pt code. The 19-page trial is explicitly excerpted; the 110-page proof contains complete representative pieces. Both remain local. Source originals are unchanged; table structure is repaired without duplicating words, inspected translation/purchase furniture is recorded as removed, and note-return links are added.

Windows automated and rendered-PDF checks pass. Physical iPad highlighting/handwriting and reading-app preference remain pending. The draft book-design skill captures tested mechanics and iterations; standalone packaging and independent validation remain Phase 5 work. Full Roots of Lisp conversion remains unresolved; the builder explicitly rejects its introduction if selected. No app, full collection or separate skill release is claimed.


Initial layout feedback applied: choose 25% from the requested 20%/25% right-space options, halve bottom space to 7.5%, use a faint bottom-only separator, share the top line between title and number, justify prose with automatic word breaks, and use 12 pt author notes without return labels. The revised 17-page trial and 94-page five-piece proof pass Windows checks. The user subsequently approved the revised layout and closed Phase 3; specific device checks were not reported; earlier dimensions and return labels above record the first trial.


Phase 3 closeout: the user explicitly approved the revised sample and requested closure on 2026-09-09. Carry its current settings into Phase 4 as the reset defaults. Individual device interactions and app preference were not reported; full-book iPad review and skill validation/packaging remain Phase 5 work. No later phase was started.


Scope change, 2026-09-09: the user removed the app requirement. Command-line generation and agent-driven configuration changes are sufficient. Phase 4 now finishes that workflow using existing tools; Phase 5 requires usable command-line exports, not an app. Earlier app references in implementation records are historical.

## Phase 4 implementation — 2026-09-09

Retained the working PDF builder and catalog. Personal reading settings now load automatically; explicit `--settings` files override that choice while inheriting omitted shipped defaults. Personal book files already took precedence; `--book` adds an explicit per-export choice. UTF-8 files with a Windows encoding marker are accepted. Reset instructions move only the named private file into an ignored, uniquely named backup.

Added `--full` for all included essays without excerpts, and `--check` for content preparation without printing. `--essays` still selects complete pieces, while `--complete-essays` still means the complete default five-piece proof. `src.catalog --list` gives titles and stable IDs without rewriting any files. Full PDFs have their own filename prefix, accurate front matter, and effective book choices in the build record.

Both full modes report every selected preparation failure and refuse partial output. The current collection has 11 blockers: two required companions and nine wording-preservation failures. These are explicit Phase 5 preparation work, not silent exclusions or evidence of lost original sources; the collection audit still passes all 234 entries. The original manuscript test proves the full-export command with moved sections, private settings and an excluded failed entry. It does not prove the final collection or replace Phase 5's separate reusable-skill exercise. See [progress](progress.md) for exact blockers, commands and output evidence.

## Phase 5 user steering ? 2026-09-09

The user authorised replacing image headings with text when easy, then chose to skip Lisp essays: ?lisp esssays don?t need so much effort - we can skip them?. Applied this to the 10 entries in the approved final Lisp section. No sources are deleted. Both unprepared companion articles are in that section, so their conversion is no longer required for this edition. Other programming essays remain in their approved sections. Five image headings were transcribed after visual inspection; duplicate title images and recognised footer icons are omitted with evidence in each build record.


Latest user change (2026-09-09): omit all essay images, including meaningful pictures, while preserving saved originals and text headings. This supersedes earlier image-retention requirements for this edition. Use smaller two-column contents and clickable top titles/page numbers returning to Contents. Trial 13 pt body / 1.35 spacing in a sample before a full rebuild; final approval is pending.

The user approved the 11-page compact sample with ?cool - go ahead and proceed?. Promoted 12 pt / 1.25 / 3.75% bottom to shipped defaults and began the full 224-essay export. Earlier trial settings remain only as historical evidence. Device-specific highlighting, handwriting and performance remain unreported.
