# iPad Reading Edition Implementation Plan

**Goal:** Create a Windows app that exports a configurable Paul Graham essay book with broad subject sections and handwriting space for an iPad A16.

**Architecture:** Keep source essays, editorial choices, page settings, and generated PDFs separate. A local browser interface will select content and settings and call a local PDF builder. Reuse upstream components where they preserve content and work on Windows.

**Tech stack:** Proposed Python foundation, a local browser interface, and a PDF generation tool selected by the sample checks in Phase 3. No framework or PDF library is committed before those checks.

**Spec:** [Design specification](../../design.md). Read it together with [decisions and evidence](../../decisions.md).

This plan was saved during documentation-only planning. The user authorised Phase 1 on 2026-09-09; its completed work and exact setup commands are recorded in docs/progress.md and docs/windows-setup.md. Phase 2 implementation is now delivered with grouping awaiting user review; Phases 3-5 remain unstarted. The writing-plans skill informed the file map, task checklists, and acceptance checks. No additional skills or subagents are required to read this document.

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
| src/app.py | Local application launch and requests from the interface |
| src/ui/ | Content selection, formatting controls, and export progress |
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

- [ ] Select a direct PDF tool using a representative sample. Check precise margins, text selection, embedded fonts, links, and bookmarks; do not require an EPUB intermediate.
- [ ] Include the cover as the first page, without essay handwriting margins, and keep cover selection configurable.
- [ ] Include a short essay, a long essay, an essay with author notes, and Lisp/code content; cover meaningful images/tables where present.
- [ ] Define exact page dimensions and outer margins alongside the initial fonts, 14 pt size, 1.45 line height, 30% right space, and 15% bottom space.
- [ ] Embed permitted font files so the reading device does not substitute a different font. Detect missing fonts visibly.
- [ ] Keep page titles, page numbers, code, images, and author notes clear of the handwriting areas.
- [ ] Implement linked contents and section/essay bookmarks. Verify both in the generated PDF rather than assuming the export tool supplies them.
- [ ] Reject settings that leave no usable text area, and explain the conflicting fields in plain language.
- [ ] Inspect rendered sample pages on Windows for clipping, unwanted blank pages, broken notes, and unreadable code. Check selectable text and link destinations.
- [ ] Record the chosen PDF tool and why it passed the sample checks.
- [ ] Design and inspect a coherent cover, title page, contents, section/essay openings, reading pages, quotations, author notes, and page details. Refine typography and avoid stranded single lines and awkward breaks; judge the sample as a published book with intentional handwriting margins.
- [ ] Begin skills/book-design/SKILL.md using the available skill-creator instructions at execution time. Capture design rules and a configurable preset as the sample evolves; keep trial settings distinct from user-approved choices. Record iteration feedback in docs/sample-review.md and update the draft accordingly.
- [ ] Ask the user to try reading, highlighting, and handwriting in Preview and Goodnotes on the iPad A16. Record actual feedback and adjust the sample.

**Pass condition:** Windows sample checks pass and the user finds the layout comfortable on the iPad. If device feedback is pending, label the sample unapproved; independent app work may continue, but do not describe the reading experience as validated.

## Phase 4 — Make content and formatting configurable in the app

**Deliverable:** A local Windows app that saves choices and exports new samples without code edits.

**Files:** src/app.py; src/ui/; src/settings.py; src/catalog.py; config/reading-settings.json; config/book.json; tests/test_saved_settings.py; tests/test_book_selection.py; docs/windows-setup.md.

**Inputs:** The catalog, default settings, and saved user choices. **Outputs:** Validated saved settings and ordered essay selections consumed by the same sample/full PDF builder.

- [ ] Provide a local launch action and show a useful error if required dependencies or fonts are missing.
- [ ] Present section ordering, essay inclusion, and moves between sections with Lisp last in the default book.
- [ ] Add font, size, line/paragraph spacing, page dimensions, margins, colours, and blank/faint-dot background controls.
- [ ] Save user settings across restarts and offer an explicit reset to the original preset.
- [ ] Provide selected-essay sample export and full-book export using the same layout settings.
- [ ] Show progress, the output location, and specific download or conversion failures.
- [ ] Check that changed settings survive restart, reset restores defaults, exclusions affect the PDF, and sample/full exports use the same settings.

**Pass condition:** The user can change the book layout and section choices through the app, restart it, and generate a new sample with those choices intact.

## Phase 5 — Finish the reading edition and reusable book-design skill

**Deliverable:** The complete selected book, a build record, practical usage instructions, and a reusable book-design skill that captures the final approved design and production workflow.

**Files:** src/pdf_builder.py; output/; tests/test_full_export.py; docs/sample-review.md; docs/windows-setup.md; README.md.

**Skill files:** skills/book-design/SKILL.md; skills/book-design/README.md; supporting references and assets where needed; licence and attribution notices for any reused material.

- [ ] Apply the reviewed essay groupings and approved sample settings.
- [ ] Generate the full PDF with its cover, a unique filename and a companion record of settings, included source versions, ordering, and any exclusions or failures.
- [ ] Verify exported essay headings against the selected catalog: no missing included essays, unintended duplicates, or excluded essays.
- [ ] Check section order, Lisp last, contents links, bookmarks, font embedding, and text selection.
- [ ] Inspect the first and last pages, section boundaries, long essays, author notes, code, and any pages identified by layout checks.
- [ ] Generate a second export with changed settings and confirm it is a separate file and the first export is unchanged.
- [ ] Have the user open the full book in the selected iPad app and check navigation, highlighting, handwriting, and responsiveness at full-book size.
- [ ] Document launch, settings changes, sample/full export, importing into the reading app, and keeping annotated copies.
- [ ] Finalise the book-design skill from the actual approved output and iteration history, using skill-creator guidance. Cover typography, page dimensions, cover/title/contents pages, section and essay openings, author notes, writing margins, navigation, content preservation, and visual PDF review. Do not freeze initial proposals that were changed during review.
- [ ] Separate general book-design guidance from this book's configurable preset. Keep note-taking margins optional for other users; do not hard-code Paul Graham content, Lisp ordering, local machine paths, or iPad A16 as universal requirements.
- [ ] Include the actual templates, settings, font/dependency information, and instructions needed to reproduce the approved style. A skill file guides the workflow; do not claim that prose alone guarantees identical output without the recorded tools and assets.
- [ ] Validate the skill's format and referenced files, then exercise it with an original short sample in a clean folder. Check that it reproduces the approved design treatment, preserves text, and produces working PDF navigation. Record the result and any limitations.
- [ ] Prepare a shareable skill folder with usage instructions, a redistributable example, and appropriate licence/attribution files. Do not bundle the essay collection or assets without redistribution permission. Public release is a separate explicit publishing action; report the prepared folder without claiming it is already published.

**Pass condition:** The full selected book passes content and layout checks and works acceptably on the user's iPad. The reusable skill reflects that approved design, passes its checks and example run, and is packaged for sharing. Report actual page count and file size only after generation.

## Completion and review boundaries

Use [the phase command](../../commands/phase.md) to start or resume one phase per chat. Each phase invocation authorises implementation of that phase. Read and update [progress](../../progress.md) so the next chat does not depend on conversation memory.

The planning stage is complete when these documents reflect the conversation and their links work. Implementation starts only after the user requests it. During implementation, use the grouped essay list and sample PDF as concrete review points; avoid asking the user to decide routine tool details without evidence.

The full project is complete when all five phase pass conditions are met. Do not substitute a generated file for the final device check or describe pending user feedback as a passed test.

## Phase 2 implementation notes

Delivered 2026-09-09. Added `src/__init__.py` for module commands and `scripts/check_collection.py` for offline collection checks; `config/book.local.json` holds ignored personal overrides. `docs/collection-checks.md` records preservation evidence and companion-document limitations. Original sources, reading fragments, images, companion files and the catalog remain local under `data/`. No extra conversion library was needed.

All Phase 2 checklist outputs are present. The grouped list is proposed and awaits user review. Ten tests pass. The complete Roots of Lisp PostScript companion is preserved but needs conversion before full export; its introduction is not the full article. Read the current progress and collection-check documents before Phase 3. No later-phase checklist is marked complete.
