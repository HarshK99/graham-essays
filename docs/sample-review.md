# Sample review

Status: Phase 3 Complete. The user approved the revised sample on 2026-09-09 and requested phase closure. Windows checks pass. The approval did not specify a reading app or individual device checks.

## Actual local files

- Short trial: `output/sample-20260909-151107-0700791e.pdf` — 17 pages, 666,949 bytes (about 0.67 MB).
- Complete five-piece proof: `output/sample-20260909-151222-d72d2864.pdf` — 94 pages.
- Matching `.json` build records and `.checks.json` audits sit beside each PDF. All remain local and excluded from Git. These filenames identify the actual exports on the development machine.

The trial contains cover (1), title page (2), linked contents (3), an opening excerpt of How to Do Great Work with its three referenced notes (4–7), complete Writing, Briefly (8–9), complete Modeling a Wealth Tax with both tables and its note (10–12), an opening language-design excerpt with a preserved heading image (13–14), and ANSI Common Lisp chapter 2’s opening and section 2.1 with code and attribution (15–17). Lisp remains last. The longer proof includes these five pieces in full, including all five language-design images and all chapter notes. Neither is the whole collection.

## Trial design

612 × 880 pt portrait pages; 36 pt outer margins; 24 pt header/footer bands. The 540 × 760 pt usable area yields a 391 × 703 pt reading column, 14 pt gap, 135 pt right writing area, and 57 pt bottom area across the usable width. This implements the revised 25% side / 7.5% bottom reserves without double counting.

Source Serif 4 body at 14 pt, 1.45 line height and 10 pt paragraph spacing; Source Sans 3 labels; Source Code Pro code at 11 pt. Justified prose with automatic word breaks and left-aligned final lines; 12 pt author notes. White reading pages, restrained green details, blank writing areas with a very faint bottom separator only. Page numbers share the essay title's top line. Links to notes remain; "Back to text" labels are removed. Embedded fonts retain their bundled original OFL licences. Page details sit outside writing areas. The original typographic cover uses the same families; the inherited cover remains preserved with reuse terms unresolved. These are the user-approved sample settings; full-book device review remains separate.

## Evidence and limitations

Selected Playwright 1.62.0 with Chromium 151.0.7922.34 for direct HTML-to-PDF printing, pypdf 6.18.0 for assembly and navigation, and pypdfium2 5.13.0 for independent rendering/text-position checks. No EPUB, Calibre or Unix setup is needed. [Playwright’s PDF API](https://playwright.dev/python/docs/api/class-page#page-pdf) and [pypdf’s merge guidance](https://pypdf.readthedocs.io/en/stable/user/merging-pdfs.html) informed implementation. Selection rests on successful Windows output, not an untested engine comparison.

Both exports pass text preservation, font embedding, internal destinations, bookmarks, text/image bounds, empty-page and personal-annotation checks. The trial has 14 internal link rectangles, one external link, 13 outline entries and one image. The complete proof has 44 internal rectangles, three external links, 13 outline entries and five images. Counts describe clickable rectangles, which can differ from source links when links wrap. Companion reports contain exact final counts.

Preparation compares source wording before/after structural repair, allowing recorded site-furniture removal and added navigation/ornaments. Original bytes remain unchanged. PDF comparison normalises whitespace, ligatures and PDFium's line-ending hyphen marker and print-added U+2010 hyphens at line ends, without ignoring ordinary missing words.

Nineteen tests cover settings conflicts, missing fonts, zero writing margins, original content with notes/quotes, table repair, incomplete companions, invalid selections, navigation, changed size/dotted margins, configurable cover and separate exports preserving the first file. During the initial trial, fresh setup in a spaced Windows path installed a separate Python environment and successfully exported/audited that trial; it reused the normal per-user Chromium cache.

Revised visual inspection covered all 17 trial pages in overview and enlarged prose, notes and code pages. Images are under `output/review/revision2/`. The revised 94-page proof passed automated checks; the earlier 110-page proof had representative visual inspection. Internal destination checks pass; return labels are disabled. The 2 pt text-bound tolerance allows measured serif ink overhang (up to 1.51 pt), not extra layout width.

These are automated checks and rendered-PDF inspection on Windows. No manual click-and-drag test in a Windows PDF reader, browser-app test or physical iPad check occurred. Device highlighting, handwriting and reading comfort remain user acceptance checks.

## Iterations — 2026-09-09

1. The full five-piece proof was too long for a quick trial. Added labelled excerpts with referenced notes; retained `--complete-essays` for complete pieces.
2. Fixed a duplicated table heading from nested, unclosed source cells; added a regression test and source-wording guard.
3. Removed trailing spacing ornaments that created an unwanted page. No blank notes pages are inserted.
4. Attached note markers to preceding words, replaced a fallback-font arrow with “Back to text”, and kept short notes/return labels together. Final files use only bundled Source fonts. Accepted an extra content page rather than shrinking text.
5. Removed a repeated editorial date while retaining the source date, chapter attribution and code indentation. Recorded removed translation/purchase furniture.
6. Drafted `skills/book-design/SKILL.md` and its workflow reference; the skill format validator passed. This is a repository draft, not an installed or separately published skill. Phase 5 still requires approved settings, packaging and a separate original-manuscript exercise.
7. Applied the initial user feedback above. Justification is a design choice, not a requirement for every book; the wider column was inspected for uneven spacing. Original exports `sample-20260909-145000-91927e03.pdf` (19 pages) and `sample-20260909-144810-3895d5e9.pdf` (110 pages) remain unchanged locally.

## Sample approval and remaining device checks

The user approved the revised sample and requested Phase 3 closure on 2026-09-09. No individual device results or app preference were supplied. Retain the following checks for the Phase 5 full-book review:

1. Read pages 4–6 and 8–9 at your normal page view with toolbars visible.
2. Highlight a sentence; write a few lines in the right and bottom spaces.
3. Use Contents (3), note 1 (4), and a section/essay bookmark if exposed. Check tables (11) and code (16–17). There are no return labels at the ends of notes.

Report which app feels better and whether text or writing space should change. Initial feedback received: use 20% or 25% right space, halve bottom space, add a faint bottom divider, move numbers beside the top title, try justified text, reduce note size, and remove return labels. Implemented 25%, 7.5% and 12 pt notes. Revised layout: approved on 2026-09-09. Individual device checks: not reported. Keep annotated copies independently from new exports.

Next: `Start phase 4` in a new project chat to finish the saved-settings and command-line export workflow; do not start automatically. The complete Roots of Lisp companion still needs preparation before full-collection export; the builder refuses to label its introduction a complete essay.
