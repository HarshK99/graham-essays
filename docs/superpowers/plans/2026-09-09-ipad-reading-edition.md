# iPad Reading Edition Implementation Plan

**Goal:** Create a Windows command-line workflow that exports a configurable Paul Graham essay book with broad subject sections and handwriting space for an iPad A16.

**Architecture:** Keep source essays, editorial choices, page settings, and generated PDFs separate. Saved configuration files and command-line options select content and settings for the local PDF builder; an agent can edit these files and run commands. Reuse upstream components where they preserve content and work on Windows.

**Tech stack:** Native Windows Python tools; Playwright/Chromium prints PDF, pypdf assembles navigation, and PDFium checks output. Phase 3 selected these tools. No app framework is needed.

**Spec:** [Design specification](../../design.md). Read it together with [decisions and evidence](../../decisions.md).

This plan was saved during documentation-only planning. The user authorised Phase 1 on 2026-09-09; its completed work and exact setup commands are recorded in docs/progress.md and docs/windows-setup.md. Phase 2 is complete with user-approved grouping; Phase 3 is complete with user approval of the revised sample; Phase 4 is complete; Phase 5 remains unstarted. The writing-plans skill informed the file map, task checklists, and acceptance checks. No additional skills or subagents are required to read this document.

## Global constraints

- Include a cover; preserve the upstream cover for reuse after checking its terms.
- Generate the PDF directly from essay content, without requiring EPUB generation.
- Run directly on Windows without requiring Linux or macOS.
- Put writing space on the right side and at the bottom of every reading page.
- Do not add a blank notes page after each essay.
- Group essays into broad sections in one main book.
- Place Lisp essays at the end of the main book by default.
- Allow section order and essay inclusion to change without editing code.
- Allow fonts and page formatting to change without editing code.
- Create a separate file for each export; never silently replace an existing PDF.
- Do not transfer handwritten annotations between exports.
- Keep essay text selectable for highlighting.
- Provide clickable contents and section/essay bookmarks.

## Planned file map

At planning time only Markdown documentation existed. Phase 1 added scripts/setup_windows.py, run.py, requirements.in, a locked requirements.txt, config/README.md, and docs/upstream/; source and runtime folders are documented in docs/windows-setup.md. The remaining paths below describe future responsibilities. Confirm the map against the upstream checkout before creating implementation files; preserve upstream history and these planning documents.

| Planned path | Responsibility |
| --- | --- |
| README.md | Project introduction and Windows usage instructions |
| docs/design.md | Product and layout requirements |
| docs/decisions.md | Decisions, evidence, and verification status |
| docs/essay-review.md | Reviewable section assignments and uncertain cases |
| docs/sample-review.md | Windows checks and the user's iPad feedback |
| docs/windows-setup.md | Actual tested setup and launch instructions |
| config/reading-defaults.json | Shipped page and font settings |
| config/reading-settings.json | User's saved settings |
| config/book.json | Section order, essay assignments, and inclusion choices |
| src/collection.py | Downloading, source storage, and failure reporting |
| src/catalog.py | Stable essay records and editorial ordering |
| src/settings.py | Reading settings, validation, and saved presets |
| src/pdf_builder.py | Sample/full PDF generation and export records |
| templates/ | Page layout and print styles for the selected PDF tool |
| assets/fonts/ | Permitted font files and their licence notices |
| data/sources/ | Saved source essays, excluded from routine source commits |
| data/catalog.json | Source records, dates, titles, and download status |
| output/ | Unique PDF exports and companion build records |
| tests/ | Focused checks for content, settings, ordering, and exports |
| skills/book-design/SKILL.md | Reusable book-design workflow refined from the approved PDF |
| skills/book-design/references/ | Approved design preset, visual review checklist, and any supporting instructions |
| skills/book-design/assets/ | Reusable templates or original example assets needed to reproduce the design |
| skills/book-design/README.md | Usage, dependencies, example input, and sharing instructions |

## Phase 1 — Establish the Windows foundation

**Deliverable:** An upstream-based working project with a repeatable Windows setup and documented dependency choices.

**Files:** Upstream checkout and existing build files; README.md; docs/windows-setup.md; docs/decisions.md; dependency file appropriate to the selected tools.

- [x] Inspect upstream instructions, licence, current revision, downloading logic, and build dependencies.
- [x] Create the intended GitHub fork when implementation begins and account access is available; preserve this documentation while bringing in the source history. If account access is unavailable, prepare locally and state that the fork has not been created.
- [x] Record the upstream revision used and distinguish reusable downloading logic from platform-specific build commands.
- [x] Define a native Windows install and launch path without Bash, make, or Linux package managers.
- [x] Establish where source data, saved settings, and new exports live.
- [x] Document the actual setup and verify it from a clean project environment on Windows, including a path containing spaces.

**Pass condition:** Windows setup is repeatable without Linux, and the origin of reused code is recorded. Do not claim a finished app or PDF at this stage.

## Phase 2 — Build and organise the essay collection

**Deliverable:** A saved, checked collection and a reviewable proposed table of contents.

**Files:** src/collection.py; src/catalog.py; data/sources/; data/catalog.json; config/book.json; docs/essay-review.md; tests/test_collection.py; tests/test_catalog.py.

**Inputs:** Upstream source URLs and downloaded content. **Outputs:** Stable essay records plus section assignments independent of source files.

- [x] Save source content with source URL, title, known date, retrieval time, and a content fingerprint so later exports can record which version they used.
- [x] Use bounded retries and respectful request pacing. Surface download failures and allow retries without discarding successful downloads.
- [x] Preserve punctuation, emphasis, author notes, meaningful images/tables, and links; compare representative converted essays with their originals.
- [x] Prevent silent omissions: show how many essays succeeded, failed, or were intentionally excluded.
- [x] Assign every included essay to one primary section using the content; put Lisp-focused essays last and flag ambiguous assignments.
- [x] Produce the grouped review list with source links, uncertain dates, and explanations for ambiguous placements.
- [x] Check duplicate URLs, title changes, missing dates, one failed download, and moving/excluding an essay without deleting its source.

**Pass condition:** Every source entry has a visible status; each included essay appears once; Lisp is last; the proposed grouped list is available for user review. Unresolved classifications are explicit.

## Phase 3 — Prove the page layout with a small PDF

**Deliverable:** A selectable, navigable sample PDF that can be tried on the iPad.

**Files:** src/settings.py; src/pdf_builder.py; config/reading-defaults.json; templates/; assets/fonts/; output/; docs/sample-review.md; tests/test_settings.py; tests/test_pdf_sample.py.

**Inputs:** Selected essay records, book order, and page settings. **Outputs:** A uniquely named sample PDF and a record of its settings and content.

- [x] Select a direct PDF tool using a representative sample. Check precise margins, text selection, embedded fonts, links, and bookmarks; do not require an EPUB intermediate.
- [x] Include the cover as the first page, without essay handwriting margins, and keep cover selection configurable.
- [x] Include a short essay, a long essay, an essay with author notes, and Lisp/code content; cover meaningful images/tables where present.
- [x] Define exact page dimensions and outer margins alongside the initial fonts, 14 pt size, 1.45 line height, 30% right space, and 15% bottom space.
- [x] Embed permitted font files so the reading device does not substitute a different font. Detect missing fonts visibly.
- [x] Keep page titles, page numbers, code, images, and author notes clear of the handwriting areas.
- [x] Implement linked contents and section/essay bookmarks. Verify both in the generated PDF rather than assuming the export tool supplies them.
- [x] Reject settings that leave no usable text area, and explain the conflicting fields in plain language.
- [x] Inspect rendered sample pages on Windows for clipping, unwanted blank pages, broken notes, and unreadable code. Check selectable text and link destinations.
- [x] Record the chosen PDF tool and why it passed the sample checks.
- [x] Design and inspect a coherent cover, title page, contents, section/essay openings, reading pages, quotations, author notes, and page details. Refine typography and avoid stranded single lines and awkward breaks; judge the sample as a published book with intentional handwriting margins.
- [x] Begin skills/book-design/SKILL.md using the available skill-creator instructions at execution time. Capture design rules and a configurable preset as the sample evolves; keep trial settings distinct from user-approved choices. Record iteration feedback in docs/sample-review.md and update the draft accordingly.
- [x] Receive initial layout feedback and export a revised sample: 25% right, 7.5% bottom, faint bottom separator, top page numbers, justified prose, 12 pt notes, no return labels.
- [x] Obtain approval of the revised sample and record feedback: the user approved it and requested phase closure on 2026-09-09. No app choice or individual device-check results were reported; retain full-book device checks in Phase 5.

**Pass condition:** Windows sample checks pass and the user finds the layout comfortable on the iPad. If device feedback is pending, label the sample unapproved; independent command-line workflow work may continue, but do not describe the reading experience as validated.

**Closeout decision (2026-09-09):** The user explicitly approved the revised sample and requested closure. Phase 3 is Complete on that acceptance. No individual device interactions were reported, so none are marked tested; retain the explicit full-book device checks in Phase 5.

## Phase 4 - Finish saved settings and command-line exports

**Deliverable:** A documented Windows command-line workflow for saved book/layout choices and new PDF exports, usable directly or through an agent. The user removed the app scope on 2026-09-09.

**Files:** Existing src/settings.py, src/catalog.py, src/pdf_builder.py; config/reading-settings.json; config/book.local.json; docs/windows-setup.md; config/README.md; focused tests only for missing behaviour.

**Inputs:** The catalog, approved defaults and saved personal choices. **Outputs:** Validated settings and ordered selections consumed by the same sample/full PDF builder.

- [x] Audit existing commands, file overrides and checks; retain working features and implement only remaining gaps.
- [x] Document changing and resetting personal formatting without changing the approved defaults; verify choices persist between command runs.
- [x] Document section order, essay inclusion and moves through saved book choices; retain Lisp last in defaults.
- [x] Provide clear commands for selected-essay samples and all-included-essay export using the same settings. The current `--complete-essays` means complete selected pieces, not the whole collection.
- [x] Report progress, output filenames and specific failures. Resolve or explicitly block incomplete full-text sources before a complete collection can be claimed.
- [x] Document agent requests for changes and exports, using the same files and commands rather than a separate interface.
- [x] Verify changed settings, reset, inclusion/exclusion and separate outputs; reuse existing checks where they already cover the behaviour.

**Pass condition:** The user or agent can change saved book/layout choices and generate new PDFs through documented commands. Full-export selection is explicit, settings carry across runs, and failed/incomplete content is reported. Do not build a browser or desktop app.

### Phase 4 execution checklist — 2026-09-09

Execute in this session under the phase request. Retain the existing builder and PDF audit; full collection production remains Phase 5.

- [x] In `src/settings.py`, prefer `config/reading-settings.json` when no explicit settings path is supplied; explicit paths override that choice. Reject non-object JSON with a useful message and accept Windows UTF-8 files with a byte-order mark. Extend `tests/test_settings.py` with repeated loads, explicit defaults/reset and malformed-file checks in a temporary folder.
- [x] In `src/catalog.py`, add a read-only `--list` command for titles/IDs and validate optional essay `order` as a finite number and direct private edits to `book.local.json`. Extend the catalog test for invalid numeric order; retain existing move/exclude/source-preservation checks.
- [x] In `src/pdf_builder.py`, add `full=False`, `book_path=None`, `check_only=False` to `build`; select all included essays for full export, refuse conflicting selections/excerpts, prepare every selection and report all failures before printing. Add matching `--full`, `--book`, `--check` commands. Record full/sample scope, effective book choices and output kind; use accurate full-book front matter.
- [x] Extend `tests/test_pdf_sample.py` using its original manuscript fixture: render a full selection with saved section moves/order and an excluded failed record, audit it, verify separate names and settings, reject incomplete sources before output. Run `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`.
- [x] Run the actual saved collection through `--full --check` and `--full` to prove incomplete content is blocked without producing a partial PDF. Generate a new real sample and run `scripts/check_pdf.py` on its actual filename. Record remaining preparation failures individually; do not change approved inclusion to hide them.
- [x] Document settings precedence, safe backup/reset commands, private book changes, selected/full/check commands and agent examples in `config/README.md`, `docs/windows-setup.md` and `README.md`. Update progress, decisions and phase checkboxes; check whitespace and sharing scope, then commit and push source/docs under existing authorisation.

## Phase 5 — Finish the reading edition and reusable book-design skill

**Deliverable:** The complete selected book, a build record, practical usage instructions, and a reusable book-design skill that captures the final approved design and production workflow.

**Files:** src/pdf_builder.py; output/; tests/test_full_export.py; docs/sample-review.md; docs/windows-setup.md; README.md.

**Skill files:** skills/book-design/SKILL.md; skills/book-design/README.md; supporting references and assets where needed; licence and attribution notices for any reused material.

- [x] Apply the reviewed essay groupings and approved sample settings; exclude the final Lisp section per the user?s Phase 5 request.
- [x] Generate the full PDF with its cover, a unique filename and a companion record of settings, included source versions, ordering, and any exclusions or failures.
- [x] Verify exported essay headings against the selected catalog: no missing included essays, unintended duplicates, or excluded essays.
- [x] Check section order (Lisp excluded by user), contents links, bookmarks, font embedding, and selectable opening titles.
- [x] Inspect the first and last pages, section boundaries, long essays, author notes and code; use focused review under the user?s reduced-testing instruction.
- [x] Generate a second export with changed settings and confirm it is a separate file and the first export is unchanged.
- [ ] Have the user open the full book in the selected iPad app and check navigation, highlighting, handwriting, and responsiveness at full-book size.
- [x] Document commands, settings changes, sample/full export, importing into the reading app, and keeping annotated copies.
- [x] Finalise the book-design skill from the actual approved output and iteration history, using skill-creator guidance. Cover typography, page dimensions, cover/title/contents pages, section and essay openings, author notes, writing margins, navigation, content preservation, and visual PDF review. Do not freeze initial proposals that were changed during review.
- [x] Separate general book-design guidance from this book's configurable preset. Keep note-taking margins optional for other users; do not hard-code Paul Graham content, Lisp ordering, local machine paths, or iPad A16 as universal requirements.
- [x] Include the actual templates, settings, font/dependency information, and instructions needed to reproduce the approved style. A skill file guides the workflow; do not claim that prose alone guarantees identical output without the recorded tools and assets.
- [x] Validate the skill's format and referenced files, then exercise it with an original short sample in a clean folder. Check that it reproduces the approved design treatment, preserves text, and produces working PDF navigation. Record the result and any limitations.
- [x] Prepare a shareable skill folder with usage instructions, a redistributable example, and appropriate licence/attribution files. Do not bundle the essay collection or assets without redistribution permission. Public release is a separate explicit publishing action; report the prepared folder without claiming it is already published.

**Pass condition:** The full selected book passes content and layout checks and works acceptably on the user's iPad. The reusable skill reflects that approved design, passes its checks and example run, and is packaged for sharing. Report actual page count and file size only after generation.

## Completion and review boundaries

Use [the phase command](../../commands/phase.md) to start or resume one phase per chat. Each phase invocation authorises implementation of that phase. Read and update [progress](../../progress.md) so the next chat does not depend on conversation memory.

The planning stage is complete when these documents reflect the conversation and their links work. Implementation starts only after the user requests it. During implementation, use the grouped essay list and sample PDF as concrete review points; avoid asking the user to decide routine tool details without evidence.

The full project is complete when all five phase pass conditions are met. Do not substitute a generated file for the final device check or describe pending user feedback as a passed test.

## Phase 2 implementation notes

Delivered 2026-09-09. Added `src/__init__.py` for module commands and `scripts/check_collection.py` for offline collection checks; `config/book.local.json` holds ignored personal overrides. `docs/collection-checks.md` records preservation evidence and companion-document limitations. Original sources, reading fragments, images, companion files and the catalog remain local under `data/`. No extra conversion library was needed.

All Phase 2 checklist outputs are present. The user approved the grouped list on 2026-09-09; Phase 2 is complete. Ten tests pass. The complete Roots of Lisp PostScript companion is preserved but needs conversion before full export; its introduction is not the full article. Read the current progress and collection-check documents before Phase 3. No later-phase checklist is marked complete.

## Phase 3 execution record

- [x] Validate page geometry and bundled fonts in `src/settings.py`, with focused settings tests.
- [x] Separate print preparation into `src/print_content.py`; preserve wording while repairing tables and linking notes.
- [x] Render and assemble cover, title, contents, essays and navigation in `src/pdf_builder.py` with `templates/book.css`; save unique PDFs and build records.
- [x] Add actual PDF verification and a fresh Windows installation check in `scripts/`; inspect output and fix observed layout defects.
- [x] Draft the reusable book-design skill and update public setup/review/handoff records.
- [x] Receive layout feedback, revise the sample, and record explicit user approval and Phase 3 closure on 2026-09-09; do not infer unreported iPad interactions.

The 19-page trial uses labelled excerpts in `config/sample-selection.json`; the 110-page proof checks all five pieces in full. See `docs/sample-review.md` and `docs/progress.md` for exact files and evidence. Execution stayed in this session under the phase request. At Phase 3 closeout, no Phase 4/5 task was complete; Phase 4 delivery is recorded below. The builder's original-text test fixture does not replace Phase 5's independent reusable-skill exercise.


Initial feedback revision: 25% right / 7.5% bottom reserves, top numbering, faint bottom separator, justified prose, 12 pt notes and no return labels. Revised exports are 17 and 94 pages; 19 tests and both PDF audits pass. See sample-review.md for exact files. The user approved the revised sample and closed Phase 3 on 2026-09-09. Full-book iPad checks remain in Phase 5.

## Phase 4 execution record

Completed the checklist above without adding an app or new dependencies. Twenty-three tests, the 17-page regression sample audit, fresh-process settings persistence/reset and the 234-source preservation audit passed. Full selection was rendered and audited on an original manuscript. Both real full commands block the same eleven content-preparation failures before output; see `docs/progress.md` for the exact titles and restart instructions. Approved choices are unchanged. Phase 5 remains unstarted.


## Phase 5 execution checklist ? 2026-09-09

Execute in this session under the phase request. Retain the current approved compact defaults and the user-approved 224 included / 10 excluded choices.

- [ ] Repair `src/print_content.py` with original-text regression fixtures in `tests/test_full_export.py`: escape literal angle brackets, preserve nested quotation tables once, unwrap rowless layout tables, and preserve code entities. Keep the wording guard.
- [x] Superseded by user direction: skip the final Lisp section, including both unprepared companions. Preserve originals; keep explicit rejection if those entries are later re-enabled.
- [ ] Run `python -m src.pdf_builder --full --check`, then the full tests. Generate using `--full`; extend `scripts/check_pdf.py` to compare selected IDs/order, heading starts, section destinations and contents against the actual book record. Audit the resulting PDF and repair observed problems.
- [ ] Render first/last pages, all section boundaries, notes, code, images/tables and flagged pages into local review images; inspect them. Export again with an explicit changed-settings file and verify the first fingerprint stays unchanged.
- [ ] Package `skills/book-design/` with general instructions, approved preset, actual reusable renderer/templates/fonts, original manuscript, dependency and attribution files. Exercise only that package in a clean folder outside project output and run skill format/reference/PDF checks.
- [ ] Update README, setup, sample review, decisions and progress with exact outputs/checks/restart instructions. Keep full-book iPad feedback pending until supplied. Review sharing scope, commit and push source/docs only under existing authorisation.

Phase 5 pause: the user requested fewer checks, stopping low-value refinement loops, and a discussion of smaller page count/file size. See `docs/progress.md` for the actual 224-essay PDF and incomplete audit status. Companion conversion is superseded by the approved Lisp-section exclusion. Do not resume the old execution checklist unchanged.

- [x] Produce a compact 13 pt / 1.35 sample with essay images omitted, 10 pt two-column contents, and header return links; run only focused checks.
- [x] Receive compact-sample approval before rebuilding the full selection. See latest progress entry for actual filenames.

- [x] Supply an additional 12 pt / 1.25 sample with 3.75% bottom writing space; verify the saved choices, inspect representative pages and preserve the earlier PDF. Approval remains pending.

Phase 5 final production: the approved 224-essay edition is 1,348 pages / 13,603,725 bytes. Focused navigation/font/image/opening checks passed; reusable runtime and original example passed. Earlier broad-audit execution tasks are superseded by the user?s focused-check preference. Only full-book device review remains for acceptance; see `docs/progress.md`.
