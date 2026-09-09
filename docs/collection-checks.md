# Collection checks

Checked on native Windows, 2026-09-09. Phase 2 source work is implemented; the proposed grouping awaits user review. No PDF, browser rendering or iPad behaviour has been tested.

## Snapshot and coverage

The saved [article index](https://paulgraham.com/articles.html) contains 234 unique entries. All 234 have saved originals, reading fragments and visible catalog status. None is intentionally excluded. The catalog also records 46 successfully saved image references, 338 explicitly decorative source-only image references, and ten successfully saved author-hosted companion documents. Some saved graphics are title graphics without reliable alternative text; preservation is deliberately conservative.

Five entries have no explicit publication date: What Languages Fix; Why Arc Isn't Especially Object-Oriented; Lisp for Web-Based Applications; and both ANSI Common Lisp chapters. Programming Bottom-Up prints 1993, which remains a year-only date. The April 2001 talk mentioned inside Lisp for Web-Based Applications is not labelled as its publication date.

Every included source appears once in the proposed list. Sections contain 83, 43, 38, 33, 27 and 10 entries respectively, with Lisp last. Initial full-content term matching was followed by a review of titles/openings and ambiguous cases. This is a proposed editorial organisation, not a line-by-line reading or user-approved table of contents. See [the complete list](essay-review.md).

## Preservation checks

`scripts/check_collection.py` checked all 234 saved main-source fingerprints, reading text, emphasis/structure counts, links and note anchors, saved image fingerprints, and companion fingerprints: zero issues. It compares the saved fragments with extraction from original bytes. This detects corruption and inconsistent conversion; it does not independently prove that every possible website layout has been understood.

Separate inspection of representative original page structure found and fixed sibling-row full-text links that were initially outside the extracted essay cell. The following cases were inspected:

| Source | Evidence / purpose |
| --- | --- |
| Writing, Briefly | Short prose; original text and emphasis preserved |
| How to Do Great Work | Long prose, 58 original essay-body links, and all internal note targets preserved; no unresolved original note targets in the inspected fragment |
| Modeling a Wealth Tax | Both nested data tables preserved; linked author note retained |
| Five Questions about Language Design | Five image references downloaded with recorded source URLs and fingerprints; links and surrounding text retained |
| Chapter 2 of ANSI Common Lisp | Plain-text chapter preserved as escaped HTML inside a preformatted block, retaining code indentation and line breaks |
| The Roots of Lisp | Introductory HTML preserved; complete-article and code links retained; linked originals saved separately |
| Lisp for Web-Based Applications | Introductory page and its separate BBN talk text both saved; talk date kept distinct from unknown publication date |

HTML author wording is not rewritten into Markdown. Relative links become absolute; internal note links stay internal. Scripts and event attributes are removed from reading fragments, while original bytes remain unchanged. Older promotional banners and some footer links are deliberately still present in fragments: the PDF phase must handle those separately from author prose. No generated book is claimed to be cleanly typeset yet.

## Linked document limitations

The Roots of Lisp's complete article is a saved PostScript file, a print-document format. Its `content_scope` says the main HTML is an introduction, and the companion's `content_status` requires conversion review before full export. The code companion is ready as text. Being Popular also links a PostScript version, but already supplies its essay in HTML. Lisp for Web-Based Applications has a ready text companion. Other companions are linked code and spam examples, not additional top-level essays.

Do not silently export just the Roots of Lisp introduction as its complete article. Phase 3 can use the ready ANSI chapter or Revenge of the Nerds for its code sample while resolving full-article conversion. A final full export must resolve or explicitly report any remaining incomplete conversion.

## Repeatable checks

Run from the project folder:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/check_collection.py
.\.venv\Scripts\python.exe -m src.collection
.\.venv\Scripts\python.exe -m src.catalog
```

Ten focused tests passed. They cover duplicated source URLs, cache-independent chapter identities, title changes, source version retention, explicit and unknown dates, bounded network failure, resuming without refetching successes, preserving code and note links, companion acquisition, ordering, private choices, and moving/excluding an essay without deleting its source. A deliberate connection failure remained visible and was successfully retried in the test; no live essay download remains failed.

The repeated real collection command reused successful originals and companions and returned zero failures. The six initial failed image requests were all the same YC footer icon; their explicit decorative classification preserves the reference without pretending the remote file downloaded. No meaningful image failure was hidden.

Downloaded material stays under ignored `data/`. The public repository shares tools, metadata-only proposed book choices and review documentation; it does not share the downloaded collection or generated books.
