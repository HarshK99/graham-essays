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

Phase 4 regression check, 2026-09-09: `output/sample-20260909-153709-7413129a.pdf` is a new 17-page export using the same approved defaults. Its PDF audit passes all five text checks with zero issues. No new visual or device review was performed; sample approval still refers to the Phase 3 file above. Phase 4 is complete; next is `Start phase 5`, including the full preparation blockers listed in `docs/progress.md`.


## Compact sample update - 2026-09-09

User requested no essay images, smaller two-column contents, and a link from the top title/page number back to Contents. Then requested slightly smaller essay text or tighter spacing. Implemented configurable `include_images=false`, `contents_size=10`, `contents_columns=2`; saved a personal trial of 13 pt body text and 1.35 line height in ignored `config/reading-settings.json`. The approved body defaults remain 14 pt / 1.45 until sample review. Writing margins remain 25% / 7.5%. Text headings transcribed from images remain; essay pictures are intentionally omitted and originals retained. The typographic cover remains.

Review sample: `output/sample-20260909-172648-ebf18356.pdf` (13 pages, 220,967 bytes), with matching settings/build record. The whole 224-title list is shown separately in `output/contents-preview-714398a3.pdf` (4 pages). That visual-only preview explicitly uses page numbers from the previous edition; it is not a newly rebuilt book and its entries are not navigation links.

Focused checks only: no image objects in the sample, correct internal Contents destinations on all 12 numbered pages, and image removal from What I Did this Summer (the essay on page 122 of the previous edition). Inspected sample contents/prose and all four dense contents-preview pages. A first short draft exposed numeric rather than page-object header destinations; fixed and regenerated the sample once. No full test suite, full-book rebuild or device test. Exact results are in `output/compact-sample-checks.json`.

Next: user reviews the compact sample, then explicitly agrees on the full rebuild. Phase 5 remains Awaiting user review. Previous full PDFs are unchanged. Sharing/packaged-runtime refresh and final phase closeout remain pending; current source edits are uncommitted.


### Smaller sample - 2026-09-09

At the user's request, generated another four-piece sample with 12 pt body text, 1.25 line height and bottom writing space halved from 7.5% to 3.75% (28.5 pt). Right writing space stays 25%; image omission, two-column 10 pt contents and header return links carry forward. Personal settings saved in `config/reading-settings.json`; prior 13 pt / 1.35 settings backed up to `output/reading-settings-before-smaller-9035f4f4.json`. Shipped body defaults remain unchanged pending review.

Output: `output/sample-20260909-173419-b81f54d6.pdf`, 11 pages, 216,531 bytes, versus the previous 13-page sample. Checked effective settings and verified the previous PDF fingerprint remains unchanged. Visually inspected rendered opening, continuation, notes and last page; no full test suite or full-book rebuild. iPad comfort and approval remain pending. Next: review this new sample and choose the preferred settings before rebuilding the whole book.

## Approved compact full book - 2026-09-09

The user approved the 12 pt / 1.25 / 3.75% bottom sample and requested the full build. Latest file: `output/full-20260909-173907-6e051f73.pdf`, 1,348 pages, 13,603,725 bytes, with 224 included essays and 10 explicit Lisp-section exclusions. Contents occupies pages 3-6; the first essay starts on page 7. Every numbered page has a top return link to Contents. No essay images are included; source originals remain local and intact.

Rendered Windows review covered all front matter, every section boundary, long prose, notes, tables, code, the formerly pictured essay and the last page. Device interactions remain pending. Try Contents, the top return links, highlighting, handwriting and scrolling in your preferred iPad app. Keep annotated copies independently from future exports.


## Orange illustrated preview - 2026-09-09

The user confirmed iPad testing is done. New preview: `output/sample-20260909-175902-8d07e568.pdf` (11 pages, 3,031,766 bytes). Original workbench illustration, selectable cover lettering, burnt-orange accents and apricot rules. Reading geometry and typography unchanged. Rendered cover, contents and essay opening inspected; cover text, image exclusion and top return destinations passed focused checks. Awaiting cover/theme approval only; no repeat device review requested.


## Final approved orange edition - 2026-09-09

User feedback: "perfect - move ahead" approved the cover/theme preview. Final export: `output/full-20260909-180513-3c502f76.pdf`, 224 essays, 1,348 pages, 16,420,926 bytes. The cover adds 2,817,201 bytes compared with the previous full edition; page count is unchanged. Cover, contents and opening essay visually inspected. Cover lettering is selectable and the original illustration occurs once on the cover. The earlier full PDF's SHA-256 still matches its build record. User-reported iPad testing is complete; no additional device check is claimed for the colour-only finish.

Final focused check passed: 224 essays, four contents pages, 1,347 header returns, embedded fonts and no reading images. Phase 5 is complete.


## Title-page credit update - 2026-09-09

Added Compiled by Harsh Kankaria, the GitHub project link, a clickable LinkedIn icon (https://linkedin.com/in/harshkankaria9), and a disclaimer distinguishing essay ownership from compilation/layout and stating no author affiliation or endorsement. Removed font-family and generated-settings lines. Added version 1.0 and compilation date 2026-09-09; latest dated essay month is derived from all included records, currently August 2026 (How Universities Should Prepare Founders). Unknown dates remain unknown.

Checked `output/sample-20260909-182821-af5c8295.pdf`: 11 pages; page 2 visually inspected; credit/version/dates/disclaimer text and both external PDF links passed. Reusable renderer/template refreshed. No full rebuild or broad test suite: the user requested the command to generate the final file. The previous full book remains `output/full-20260909-180513-3c502f76.pdf` and does not contain these new credits. Run `.\.venv\Scripts\python.exe -m src.pdf_builder --full` from the project directory to produce the new complete edition; the command prints the new filename. All phases remain complete; this is a subsequent title-page change.


## Reader-intention page revision - 2026-09-10

Page 2 now begins with the selection introduction. Added About the format: right-side space for notes beside passages, bottom space for reflections/sketches/ideas, framed around active reading rather than any device. Moved compiler credit, edition details and links into the lower half; made the ownership disclaimer a lighter readable grey. Compilation date is 10 September 2026; version remains 1.0 and essay coverage August 2026.

Preview: `output/sample-20260909-183140-26c6d24b.pdf` (UTC filename), 11 pages. Visually inspected page 2, verified text order and both external link destinations. Refreshed the reusable renderer/template. No full rebuild or broad test suite. To create the complete updated book, run `.\.venv\Scripts\python.exe -m src.pdf_builder --full`. Existing full PDFs remain unchanged.


2026-09-10: Replaced the format explanation with How to use this book: writing margins, clickable Contents, top title/page-number return links, highlighting/handwriting and preserving annotated copies. Preview `output/sample-20260909-183304-83ec026b.pdf` remains 11 pages; page 2 text and rendered fit checked. Reusable renderer refreshed; no full rebuild. Generate the complete updated edition with `.\.venv\Scripts\python.exe -m src.pdf_builder --full`.


2026-09-10: Simplified page 2 to About this edition, an explicit essay/preview count, three bulleted reading tips, lower-half compiler credits and a short lighter disclaimer. Harsh Kankaria appears only in credits. Checked the rendered page in `output/sample-20260909-184202-5476b1b4.pdf` (11 pages). Awaiting this preview's approval before a full rebuild, as agreed.

Full exports now use `output_name` from book settings, shipped as `paul-graham-essays.pdf`. Existing named editions and companion records are moved to a uniquely named output/archive subfolder immediately before writing their replacement. Other books without this setting and samples keep unique filenames. The named full-export path has not been exercised with a new full build yet. The existing `output/paul-graham-essays.pdf` was already present (the user-renamed prior full edition) and is retained.

Requested stale-output deletion was rejected by automatic approval review with "blocked by policy" before the command ran. No cleanup was performed; stale outputs remain. Resume with preview approval for the full build; cleanup remains blocked by tool policy. The title-page changes are implemented and the reusable runtime refreshed.
