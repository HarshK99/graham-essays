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
| Formatting | Good starting defaults, configurable later in the app |
| Current work | Phase 2 complete on 2026-09-09; grouping approved; no app or PDF yet |
| New exports | New files, without notes from previous copies |
| Cover | Required; retain upstream cover for reuse after checking terms |
| PDF route | Generate directly from essay content, without EPUB as an intermediate |
| Phase execution | New project chat per phase using `/phase N` or `Start phase N` |

## Confirmed reusable skill deliverable

Additional confirmed deliverable: a reusable book-design skill, drafted during Phase 3 and finalised in Phase 5 from the iterated, approved PDF design. It must include the required supporting settings/templates, be tested on a separate original sample, and be prepared for others to use. Public publication is not part of this documentation update.

## Proposed defaults, not yet approved through use

- Source Serif 4 body text and Source Sans 3 labels.
- 14 pt body text, line height 1.45, left alignment, white background.
- Right notes area 30% of usable width; bottom area 15% of usable height.
- Six sections listed in the design specification, with chronological order within each.
- A local browser app on Windows, with no hosted service.

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
