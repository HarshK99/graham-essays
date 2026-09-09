# Design specification

Date: 2026-09-09

## Purpose and scope

Build a personal Windows app that prepares a readable, annotatable collection of Paul Graham's essays for an iPad A16. Reading and handwriting happen in Preview or Goodnotes on the iPad; this app prepares the PDF on Windows.

The first release is a local app, opened in a browser on the same Windows computer. This is a proposed delivery approach, not a requirement to host a website or create an account. A packaged desktop installer is outside the first release.

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

## Initial page design

The cover is the first page and does not need handwriting margins. Cover selection should be configurable. The reading-page rules below apply to essay and author-note pages.

These are adjustable starting values, not an iPad-tested final layout.

| Setting | Initial proposal |
| --- | --- |
| Orientation | Portrait |
| Page proportions | Approximately the iPad A16 display proportions; refine using the actual app viewport |
| Essay font | Source Serif 4 |
| Section labels and page details | Source Sans 3 |
| Body size | 14 pt at the selected PDF page dimensions |
| Line height | 1.45 times the body size |
| Alignment | Left aligned, uneven right edge |
| Text and background | Dark text on white |
| Right writing area | 30% of usable page width |
| Bottom writing area | 15% of usable page height |
| Writing background | Blank |
| Essay opening | Start each essay on a new page |
| Page details | Small essay title and page number |

Usable page space means the area inside the outer margins, header, and footer. Reserve the bottom writing area first, then split the remaining area between essay text and right-side notes. Leave a small gap between text and handwriting space. This keeps the two writing areas from being counted twice.

The bottom area extends across the usable width. The right margin stays on the right on every page; do not alternate it as a printed book might. Do not place author footnotes in the handwriting areas. Prefer linked author notes at the end of each essay, with links back to their references.

Do not shrink text automatically to hit a target page count. Allow the book to become longer. Check long titles, quotations, lists, code, images, and footnotes for clipping or broken page breaks. Use a readable fixed-width font for code, with its exact choice settled during the sample phase.

A PDF font size has to be judged together with page dimensions and the app's toolbars. The 14 pt proposal is not a promise of comfortable full-page reading until it has been tried on the iPad.

## Section structure

The following labels and ordering are provisional editorial choices. Only Lisp's final position is already confirmed.

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

## Proposed app experience

1. Open the app locally on Windows.
2. Load the saved essay collection, or explicitly fetch updates.
3. Review sections, move essays, and choose what to include.
4. Adjust reading and writing-space settings.
5. Export a short sample using selected essays.
6. Export the full book with those settings.

Provide a saved default preset so the user can return to the original design after experimenting. Save changes across app restarts. Offer font family, text size, line height, paragraph spacing, page size, outer margins, right and bottom writing space, colours, and blank/faint-dot writing backgrounds. The default background is blank.

Treat the generated sample PDF as the accurate preview. A browser approximation alone cannot prove how page breaks or iPad highlighting will work.

Keep the first version focused: no accounts, cloud hosting, in-app handwriting tools, annotation import, automatic daily publishing, or EPUB export. A future EPUB would serve a different reading layout and is not required for this project.

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
