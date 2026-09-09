# Production workflow and approved preset

Use the packaged runtime for reproduction. Playwright/Chromium prints HTML directly to PDF; pypdf joins chapters, installs contents destinations and nested bookmarks, then overlays global page numbers. PDFium independently reads text positions and renders pages. Exact package versions are locked in [requirements.txt](../assets/runtime/requirements.txt).

The approved preset is 612 ? 880 pt, 36 pt outer margins, 24 pt header/footer bands, Source Serif 4 at 12 pt and 1.25 line height, 10 pt paragraph spacing, Source Sans 3 labels, and Source Code Pro at 11 pt. Notes are 12 pt. Justified prose has automatic word breaks and left-aligned final lines. At those dimensions, the 540 ? 760 pt usable area yields a 391 ? 731.5 pt reading column, 14 pt gap, 135 pt side space (25%) and 28.5 pt bottom space (3.75%). Handwriting areas are optional for other books.

The typographic cover uses the same families. The title page, contents, chapter openings, quotations and page details follow the bundled `book.css`. Section openings share the first chapter's page. Each chapter starts a new page. Contents and bookmarks have two levels. Notes remain in the text column; note-return labels are off. Page number and title share the top line; the bottom writing area has a faint divider. No blank notes pages are inserted.

## Iteration evidence

The first trial had 30% side and 15% bottom space, left-aligned prose, larger notes and return labels. User feedback changed these to 25%, 7.5%, justification, 12 pt notes, top numbering, a faint bottom divider and no return labels. The revised sample was approved on 2026-09-09. Detailed iPad interactions were not reported; whole-book device review remains separate.

Production content repairs preserve literal angle brackets, nested quotations once, prose inside broken layout tables and raw code entities. Image-only headings may be transcribed after visual inspection; compare the text to the actual image and record the change. Duplicate title graphics are unnecessary when the book already supplies a text heading. Meaningful pictures stay pictures.

## Reproduction and checking

Use the commands and manuscript schema in [README.md](../README.md). The package's small manuscript adapter passes explicit author, book title and section names to the same renderer, so no particular author, topic order or device is required. It uses original text only, without collection downloads or old conversion tools.

Font files are unmodified Adobe Source releases; exact origins and fingerprints are in [the font manifest](../assets/runtime/assets/fonts/manifest.json). Preserve all OFL files. Dependency installation includes Chromium; export itself uses embedded assets and blocks network requests. Do not substitute another browser version and assume identical pagination.

Review [the checklist](review-checklist.md) after every design change. The audit checks wording, font embedding, geometry, selection order, headings, navigation, sparse pages and personal annotations. The full PDF is the page-layout preview. Windows automation and rendered-page review cannot establish physical iPad highlighting or writing comfort.


Final sample approval (2026-09-09): after the earlier 14 pt trial, the user approved 12 pt body text, 1.25 line height and 3.75% bottom space, retaining 25% right space. Essay images are omitted at this user?s request, while transcribed headings remain. The configurable preset uses 10 pt, two-column contents. The top title/number area on every numbered page links to the first Contents page. These choices describe this preset, not universal manuscript rules. Restore images with `include_images: true` when the manuscript needs them. Whole-book physical-device checks remain pending.

Validation record: the refreshed package produced its original five-page manuscript in a separate clean folder after the final preset/header-link changes, and its PDF audit passed. The collection?s final 224-entry export has 1,348 pages; focused selection, navigation, opening-title, font and image checks passed. Whole-book device interaction remains untested. No generated collection is included in this package.


## Approved orange finish

On 2026-09-09 the reader confirmed iPad testing complete and approved an original illustrated orange cover. The project defaults now use burnt-orange accents and apricot rules. The reusable runtime keeps the same palette and configurable illustration support, with an empty `cover_artwork` so a new manuscript does not inherit book-specific artwork. Live typeset lettering stays selectable over a supplied illustration.

The refreshed package was exercised in a new independent workspace, `book-design-orange-final-20260909`: original Morgan Vale manuscript, five pages, no audit issues. The cover and first chapter were visually inspected. This is a package exercise, not a claim of device testing for that manuscript.
