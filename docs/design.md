# Design specification

Date: 2026-09-09

## Purpose and scope

Prepare a readable, annotatable collection of Paul Graham's essays on Windows using commands and saved settings, with optional agent assistance. Reading and handwriting happen in Preview or Goodnotes on the iPad A16.

The user removed the app requirement on 2026-09-09. Run the Python commands directly or ask an agent to change configuration and generate a PDF. Chromium remains an internal PDF printing dependency; no browser interface or desktop app is needed.

## Confirmed requirements

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

## Approved sample page design

The cover is the first page and does not need handwriting margins. Cover selection should be configurable. The reading-page rules below apply to essay and author-note pages.

The user approved a more compact Phase 5 sample on 2026-09-09 and requested the full export. These are the current reset defaults. Approval does not establish which device interactions were tested.

| Setting | Approved sample default |
| --- | --- |
| Orientation | Portrait |
| Page proportions | Approximately the iPad A16 display proportions; refine using the actual app viewport |
| Essay font | Source Serif 4 |
| Section labels and page details | Source Sans 3 |
| Body size | 12 pt at the selected PDF page dimensions |
| Line height | 1.25 times the body size |
| Alignment | Justified prose with automatic word breaks; final lines stay left aligned |
| Text and background | Dark text on white |
| Right writing area | 25% of usable page width |
| Bottom writing area | 3.75% of usable page height |
| Writing background | Blank, with a very faint bottom separator only |
| Essay opening | Start each essay on a new page |
| Page details | Small essay title and page number on the same top line; both return to Contents when tapped |
| Author notes | 12 pt, with links to notes and no return labels |

Usable page space means the area inside the outer margins, header, and footer. Reserve the bottom writing area first, then split the remaining area between essay text and right-side notes. Leave a small gap between text and handwriting space. This keeps the two writing areas from being counted twice.

The bottom area extends across the usable width. The right margin stays on the right on every page; do not alternate it as a printed book might. Do not place author footnotes in the handwriting areas. Keep linked author notes at the end of each essay; the user requested no "Back to text" labels.

Do not shrink text automatically to hit a target page count. Allow the book to become longer. Check long titles, quotations, lists, code, images, and footnotes for clipping or broken page breaks. Use a readable fixed-width font for code, with its exact choice settled during the sample phase.

A PDF font size has to be judged together with page dimensions and the app's toolbars. The 14 pt proposal is not a promise of comfortable full-page reading until it has been tried on the iPad.

## Section structure

The user approved the following section labels, ordering and current essay assignments on 2026-09-09. See docs/essay-review.md for the approved grouping.

1. Startups & Building Companies
2. Work, Learning & Ambition
3. Thinking, Writing & Creativity
4. Society, Wealth & Power
5. Programming & Technology
6. Lisp & Technical Deep Dives

Assign each essay one primary section based on its content. Keep secondary topic labels for reviewing ambiguous cases, without duplicating the essay in the book. Put Lisp-focused essays in the last section; do not automatically put every programming essay there.

Proposed order within each section: oldest first, with manual reordering available. Missing or uncertain dates must be marked for review rather than invented. Preserve the website's source order as a fallback.

Before the full build, review a grouped essay list containing title, source URL, date if known, primary section, inclusion status, and a brief reason for uncertain placements. Moving or excluding an essay must not delete its saved source.

Show the hierarchy in both the book's clickable contents and PDF bookmarks: section, then essay. Start sections on a new page with the first essay beneath the section heading; dedicated decorative section pages are unnecessary for the first version.

## Command-line and agent workflow

1. Open PowerShell in the project folder, or ask an agent to work in this project.
2. Use the saved essay collection; fetch updates only when explicitly requested.
3. Edit saved book choices to reorder sections, move essays and choose what to include.
4. Edit personal reading settings to adjust fonts, spacing, margins and other page choices.
5. Generate and check a short sample using selected essays.
6. Generate the full book with the same saved settings once full export is ready.

Keep the approved default preset separate from personal settings. Settings files persist across command runs; provide documented reset instructions that preserve other user files. Support font family, text size, line height, paragraph spacing, page size, outer margins, right and bottom writing space, colours and blank/faint-dot writing backgrounds. The default writing background is blank with the approved bottom divider.

An agent request such as "make the right writing space 20% and export a sample" should update the personal settings, run the existing builder, check the output and report its new filename. Defaults change only when requested. The generated PDF is the accurate preview; there is no separate on-screen layout editor to build.

Keep the workflow local, without accounts, cloud hosting, annotation import, automatic publishing or EPUB export.

## Published-book quality and reusable skill

The intended visual standard is a thoughtfully typeset published book with integrated writing margins. Include a coherent cover and title page, designed contents, distinctive section and essay openings, balanced typography, consistent page details, and careful quotations and author notes. Inspect actual rendered pages for awkward breaks and single lines stranded at a page edge. Reading comfort and visual polish are both acceptance criteria.

Draft a reusable book-design skill during Phase 3 and finalise it in Phase 5 from the output the user approves through iteration. Its main file will be skills/book-design/SKILL.md, with supporting templates, an approved configurable preset, and verification instructions as needed. Keep general design rules separate from this collection's subject choices. Other users should be able to apply the style to their own manuscripts, with or without writing margins.

Validate it on an original short sample outside the project output folder. Package usage instructions and permitted assets for sharing; do not equate a prepared local package with a public release. The skill must describe the actual tested generation process, not promise identical results from instructions alone.

## Content preservation

Reuse useful upstream downloading and conversion work after inspecting it. Preserve wording, punctuation, emphasis, links, author notes, and meaningful images or tables. Report failed downloads and conversion problems visibly; do not describe an incomplete export as the complete collection.

Give essays stable identities based on source URLs rather than their position in the book. Store source content separately from section choices and design settings so changing layout or order does not require downloading everything again.

## Reading apps and acceptance

Preview and Goodnotes are both candidates. Export a short representative sample and try the same file in both. Select the app based on actual reading, highlighting, writing, and navigation comfort; do not require switching apps before this trial.

Acceptance requires a real iPad check: text is comfortable at a useful page view, highlights select the intended words, handwriting space is sufficient, and contents links work. Check section/essay bookmarks where the app exposes them. A Windows-only inspection cannot substitute for the user's handwriting trial.

## Export behaviour

Use a new, unique filename for every sample and full export. Store a companion build record with the chosen settings, essay order, source versions, and any exclusions or failures. A new export contains no personal annotations. The original annotated document stays independent in its reading app or saved file.

## Phase 3 trial implementation

The configurable preset now specifies 612 × 880 pt pages, 36 pt outer margins and 24 pt header/footer bands. Source Code Pro at 11 pt is the trial code family. The specified 14 pt body, 1.45 line height and 25%/7.5% writing reserves reflect the user-approved revised sample. An original typographic cover is the default while inherited image terms remain unresolved. Visible numbering matches PDF page positions; the cover has no visible number.

Direct Chromium printing with explicit pypdf navigation passed Windows checks. The short trial uses labelled excerpts plus referenced notes; the longer proof contains the five representative pieces in full. Sample cuts do not alter book inclusion. Short notes stay together; prose uses three-line widow/orphan settings, with actual pages inspected. Read `docs/sample-review.md` for iterations and the recorded sample approval. Full-book device acceptance remains Phase 5 work.

## Phase 4 workflow implementation

Sample and full exports now automatically reuse personal settings and book choices, with explicit file overrides and documented backup/reset commands. `--full` selects every included essay without sample cuts; `--check` prepares that selection without printing and reports all preparation failures. Full output uses its own unique filename prefix and saves effective book choices alongside settings and source evidence. See `docs/windows-setup.md` and `config/README.md` for commands. Full-collection content preparation has explicit blockers recorded in `docs/progress.md`; successful command tests do not establish final-book layout or device approval.

## Phase 5 selection change ? 2026-09-09

The user chose to skip Lisp essays rather than spend more effort preparing them. Exclude the 10 entries assigned to `Lisp & Technical Deep Dives`; keep their original files and section choices. The current edition contains 224 essays across the other five sections. Keep the optional Lisp section last if later re-enabled. Clear image-only section headings may be replaced with visually verified text; retain meaningful images.


Latest user change (2026-09-09): omit all essay images, including meaningful pictures, while preserving saved originals and text headings. This supersedes earlier image-retention requirements for this edition. Use smaller two-column contents and clickable top titles/page numbers returning to Contents. Trial 13 pt body / 1.35 spacing in a sample before a full rebuild; final approval is pending.

Current compact sample accepted: `sample-20260909-173419-b81f54d6.pdf` (12 pt / 1.25 / 3.75% bottom) is approved. Keep essay images omitted and 10 pt two-column contents. The 14 pt values in historical Phase 3 implementation notes describe earlier output.
