# Sample review

Status: Awaiting user review. Windows checks pass; iPad comfort and app behaviour are unapproved.

## Actual local files

- Short trial: `output/sample-20260909-145000-91927e03.pdf` — 19 pages, 665,885 bytes (about 0.67 MB).
- Complete five-piece proof: `output/sample-20260909-144810-3895d5e9.pdf` — 110 pages.
- Matching `.json` build records and `.checks.json` audits sit beside each PDF. All remain local and excluded from Git. These filenames identify the actual exports on the development machine.

The trial contains cover (1), title page (2), linked contents (3), an opening excerpt of How to Do Great Work with its three referenced notes (4–7), complete Writing, Briefly (8–9), complete Modeling a Wealth Tax with both tables and its note (10–12), an opening language-design excerpt with a preserved heading image (13–15), and ANSI Common Lisp chapter 2’s opening and section 2.1 with code and attribution (16–19). Lisp remains last. The longer proof includes these five pieces in full, including all five language-design images and all chapter notes. Neither is the whole collection.

## Trial design

612 × 880 pt portrait pages; 36 pt outer margins; 24 pt header/footer bands. The 540 × 760 pt usable area yields a 364 × 646 pt reading column, 14 pt gap, 162 pt right writing area, and 114 pt bottom area across the usable width. This implements the proposed 30% side / 15% bottom reserves without double counting.

Source Serif 4 body at 14 pt, 1.45 line height and 10 pt paragraph spacing; Source Sans 3 labels; Source Code Pro code at 11 pt. Left alignment, white reading pages, restrained green details, blank writing areas. Embedded fonts retain their bundled original OFL licences. Page details sit outside writing areas. The original typographic cover uses the same families; the inherited cover remains preserved with reuse terms unresolved. These are trial values, not iPad-approved choices.

## Evidence and limitations

Selected Playwright 1.62.0 with Chromium 151.0.7922.34 for direct HTML-to-PDF printing, pypdf 6.18.0 for assembly and navigation, and pypdfium2 5.13.0 for independent rendering/text-position checks. No EPUB, Calibre or Unix setup is needed. [Playwright’s PDF API](https://playwright.dev/python/docs/api/class-page#page-pdf) and [pypdf’s merge guidance](https://pypdf.readthedocs.io/en/stable/user/merging-pdfs.html) informed implementation. Selection rests on successful Windows output, not an untested engine comparison.

Both exports pass text preservation, font embedding, internal destinations, bookmarks, text/image bounds, empty-page and personal-annotation checks. The trial has 18 internal link rectangles, one external link, 13 outline entries and one image. The complete proof has 78 internal rectangles, four external links, 13 outline entries and five images. Counts describe clickable rectangles, which can differ from source links when links wrap. Companion reports contain exact final counts.

Preparation compares source wording before/after structural repair, allowing recorded site-furniture removal and added navigation/ornaments. Original bytes remain unchanged. PDF comparison normalises whitespace, ligatures and PDFium’s line-ending hyphen marker, without ignoring ordinary missing words.

Nineteen tests cover settings conflicts, missing fonts, zero writing margins, original content with notes/quotes, table repair, incomplete companions, invalid selections, navigation, changed size/dotted margins, configurable cover and separate exports preserving the first file. Fresh setup in a spaced Windows path installed a separate Python environment and successfully exported/audited the trial; it reused the normal per-user Chromium cache.

Visual inspection covered every page of the short trial. Complete-proof inspection covered front matter, essay boundaries, notes, quotation, table/image examples, code and the last page. Rechecked the note run after keeping short notes together. Review images are under `output/review/final/`. Direct destination inspection confirmed contents jumps, author-note targets and returns.

These are automated checks and rendered-PDF inspection on Windows. No manual click-and-drag test in a Windows PDF reader, browser-app test or physical iPad check occurred. Device highlighting, handwriting and reading comfort remain user acceptance checks.

## Iterations — 2026-09-09

1. The full five-piece proof was too long for a quick trial. Added labelled excerpts with referenced notes; retained `--complete-essays` for complete pieces.
2. Fixed a duplicated table heading from nested, unclosed source cells; added a regression test and source-wording guard.
3. Removed trailing spacing ornaments that created an unwanted page. No blank notes pages are inserted.
4. Attached note markers to preceding words, replaced a fallback-font arrow with “Back to text”, and kept short notes/return labels together. Final files use only bundled Source fonts. Accepted an extra content page rather than shrinking text.
5. Removed a repeated editorial date while retaining the source date, chapter attribution and code indentation. Recorded removed translation/purchase furniture.
6. Drafted `skills/book-design/SKILL.md` and its workflow reference; the skill format validator passed. This is a repository draft, not an installed or separately published skill. Phase 5 still requires approved settings, packaging and a separate original-manuscript exercise.

## iPad trial — pending

Transfer the short trial to the iPad A16 and try the same file in Preview and Goodnotes:

1. Read pages 4–6 and 8–9 at your normal page view with toolbars visible.
2. Highlight a sentence; write a few lines in the right and bottom spaces.
3. Use Contents (3), note 1 (4), its return (7), and a section/essay bookmark if exposed. Check tables (11–12) and code (17–18).

Report which app feels better and whether text or writing space should change. Feedback: not received. Approved layout: none. Keep annotated copies independently from new exports.

Resume with `Start phase 3` and feedback to revise. `Start phase 4` may begin independent app work if requested while Phase 3 awaits review; do not start automatically. The complete Roots of Lisp companion still needs preparation before full-collection export; the builder refuses to label its introduction a complete essay.
