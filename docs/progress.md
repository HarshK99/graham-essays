# Project progress and next-chat handoff

Last updated: 2026-09-09

## Current state

Phase 3's sample builder is implemented and Windows-checked. Initial layout feedback is applied in a revised 17-page trial and 94-page complete five-piece proof. Phase 3 awaits approval of the revised layout and actual iPad reading, highlighting and handwriting checks. Phase 2 remains complete with 234 saved entries and approved grouping. The browser app and full collection edition are not built. The complete Roots of Lisp companion still needs conversion before full export.

| Phase | Status | Evidence / remaining work |
| --- | --- | --- |
| 1 — Windows foundation | Complete | Fork and upstream history retained; clean Windows setup and repeat-run checks passed |
| 2 - Collection and sections | Complete | 234 saved entries; grouping approved by user on 2026-09-09; checks passed |
| 3 — Sample PDF and iPad trial | Awaiting user review | Revised 17-page trial and 94-page proof pass Windows checks; final iPad approval pending |
| 4 — Configurable app | Not started | Requires working sample generation |
| 5 — Full reading edition | Not started | Requires usable app, reviewed content order and approved layout |

## Latest confirmed additions

- The cover is required; preserve the upstream cover for reuse after checking its terms.
- Generate the PDF directly from essay content, without an EPUB intermediate.
- The user will start each phase in a new chat in this same project.
- `/phase N` and `Start phase N` both mean implement or resume that phase under AGENTS.md.
- Published-book visual quality is required, alongside the handwriting margins.
- Phase 3 drafts a reusable book-design skill; Phase 5 finalises, tests, and packages it from the design approved through iteration. The repository draft exists; it is not installed or separately released.

## Verification at instruction setup

Documentation-only inspection and local link checks. No phase code, browser workflow, fresh-chat command delivery, or iPad behaviour has been tested. Later phase workers should replace this general statement with their actual commands and outcomes in dated entries below.

## Next action

Try the revised 17-page PDF named in [sample review](sample-review.md) on the iPad A16 in Preview and Goodnotes. Grouping is already approved. Reading comfort, highlighting, handwriting and app navigation remain pending.

To revise, send `Start phase 3` with feedback; read the required project records and `docs/sample-review.md`, adjust personal settings or layout, then export and audit a new file. If the user requests independent app work first, the next command is `Start phase 4`; retain Phase 3's pending review status. Do not start later phases automatically. Resolve full-text companions before the final collection; the current builder rejects introduction-only sources.

## Phase work log

### 2026-09-09 — Phase 1 complete

**Outputs:** `scripts/setup_windows.py`, `run.py`, exact dependency versions and hashes in `requirements.txt`, direct dependency list `requirements.in`, `config/README.md`, `docs/windows-setup.md`, and `docs/upstream/PROVENANCE.md`. Updated README, decisions, and Phase 1 plan checkboxes. Original instructions, README, requirements, and automatic build workflows are archived in `docs/upstream/`. Existing project instructions and design requirements were preserved.

**Source:** full history from `ofou/graham-essays`, revision `96885e3b4018f0f1d976634e26b27a86e94aacfc`. Created and verified https://github.com/HarshK99/graham-essays as a fork of that repository. `origin` points to the fork and `upstream` to the original. Branch: `ipad-reading-edition`. At the initial Phase 1 handoff, adaptations were uncommitted and unpushed; the subsequent sharing request authorises their commit and push. The old automatic workflows are archived outside `.github/workflows`; no release or essay upload was performed.

**Decisions:** Python 3.14 (actual 3.14.7), standard Python environment creation and pip installation; Requests 2.34.2 and Beautiful Soup 4.15.0 with all indirect dependencies pinned and hashed. No PDF tool selected. Original downloader is reference-only because it discards content and has unsafe import behaviour for the planned app. Root `cover.png` is preserved byte-for-byte. No upstream licence was found, and the attributed cover page could not be opened; reuse permission remains unconfirmed. This does not block the Windows foundation, but must remain visible during cover selection and any sharing preparation.

**Commands and checks actually run on Windows:**

| Command/check | Outcome |
| --- | --- |
| `python --version` | Python 3.14.7 |
| `gh auth status` | Account access available; no credentials saved in project docs |
| `git clone https://github.com/ofou/graham-essays.git .phase1-upstream` | Full upstream history downloaded; imported without replacing project notes |
| `git -C .phase1-upstream rev-parse HEAD` | Revision recorded above, before transferring `.git` into project root |
| `gh api repos/ofou/graham-essays --jq '{license: .license, default_branch: .default_branch}'` | No licence reported; default branch `main` |
| `gh repo fork ofou/graham-essays --clone=false` | Fork URL returned |
| `gh api repos/HarshK99/graham-essays --jq '{url: .html_url, fork: .fork, parent: .parent.full_name}'` | Fork relationship verified |
| `git remote rename origin upstream`; `git remote add origin https://github.com/HarshK99/graham-essays.git`; `git switch -c ipad-reading-edition` | Remotes and local branch established |
| `Get-FileHash cover.png -Algorithm SHA256` | Matched preserved cover fingerprint in provenance document |
| `uv pip compile requirements.in --python-version 3.14 --generate-hashes --output-file requirements.txt` | Eight packages resolved and locked |
| `python scripts/setup_windows.py` | Fresh `.venv` installed all locked packages and passed readiness checks |
| `python '.phase1-checks/Clean Windows Project/scripts/setup_windows.py'` | Separate fresh environment installed and passed, with spaces in project path |
| `.\.venv\Scripts\python.exe run.py` | Offline checks passed: imports, HTML parsing, request preparation, cover fingerprint, writable folders |
| `.\.venv\Scripts\python.exe -m pip check` | No broken requirements |
| `git diff --check` | Passed; only Git's line-ending conversion notices |

Additional inline Python checks reran setup in the spaced-path copy with sample source, settings, and output files and compared their bytes afterward: all preserved. Launched the copy's readiness check from the parent folder: passed. Changed the copy's cover temporarily: returned failure with an explanatory message; original bytes restored. Ran `python run.py` outside the private environment: returned failure with the correct launch command. These checks used artificial local files, not downloaded essays. The ignored `.phase1-checks/` folder retains the test copy.

Final local-link checks passed across ten project documents, and a checklist check confirmed exactly six Phase 1 items completed with later phases untouched. Automatic approval review rejected removal of the redundant `.phase1-upstream/` source copy with “blocked by policy”; it remains ignored, without its `.git` directory (the history was already transferred to the project root). No cleanup deletion occurred. This does not affect setup or phase completion.

**Not tested:** browser interface, PDF generation or visual layout, actual essay acquisition, and iPad Preview/Goodnotes. None exists yet for testing. User layout and iPad review remain pending for Phase 3; section review belongs to Phase 2.

**Remaining:** Phase 2 source collection, preserved content and status records, catalog, and reviewable grouping. No Phase 2 implementation was started. Resume with `Start phase 2`; Phase 1 needs no user action.

### 2026-09-09 ? Sharing preparation

The user requested committing and pushing Phase 1 to GitHub and maintaining relevant README files for others. Added a newcomer quick start, clear feature status, attribution/reuse notes, `docs/README.md`, and `CONTRIBUTING.md`. Replaced the machine-specific install path with a clone-and-setup example. Saved the continuing README and commit/push preference in AGENTS.md. The Windows edition is the fork's default branch so the main repository link opens the relevant instructions; the upstream `main` branch is preserved.

Publication commands: `git push -u origin ipad-reading-edition`, then `gh repo edit HarshK99/graham-essays --default-branch ipad-reading-edition`. Remote verification confirmed the pushed commit and default branch. These publish source and documentation, not an essay collection or generated book. No later phase starts as part of this request.

Verified publication: commit `4c6493575fc1e15fce6ec7ca4b6e65d7a29bd522` was pushed successfully; `git ls-remote origin refs/heads/ipad-reading-edition` matched it, and `gh repo view HarshK99/graham-essays --json defaultBranchRef,url` confirmed the default branch. Public project link: https://github.com/HarshK99/graham-essays. The subsequent documentation-only commit records this result.

Sharing checks passed: current Markdown links, staged-file scope, a credential-pattern scan, the Windows readiness command, `pip check`, and `git diff --cached --check`. One trailing space in the archived upstream README was removed to pass the whitespace check; its wording is unchanged. No browser or iPad check was added. Continue with `Start phase 2`.

### 2026-09-09 - Phase 2 implementation; awaiting user review

**Outputs:** `src/collection.py`, `src/catalog.py`, `scripts/check_collection.py`, ten focused tests in `tests/`, the shipped proposal `config/book.json`, `docs/essay-review.md`, and `docs/collection-checks.md`. Updated public README, setup/configuration/contributing guides and decisions. Local-only outputs: `data/catalog.json`, fingerprint-named original HTML/text, reading fragments, image bytes and companion files in `data/sources/`. No essay text is staged for Git. `config/book.local.json` is the ignored personal override; the shipped book file is the initial proposal.

**Collection outcome:** 234 unique index entries, 234 successful main-source downloads, zero failed/pending main entries, zero intentional exclusions, 46 successful image references and 338 explicitly decorative source-only image references. Ten companion documents downloaded successfully, including two PostScript files. Five dates are unknown; the year-only 1993 date is kept without inventing a month or day. Index/page titles agree for every HTML source. Sections: Startups 83; Work 43; Thinking 38; Society 33; Programming 27; Lisp 10. All choices remain proposed, and overlaps are shown.

**Implementation decisions:** Requests are sequential with a one-second gap, three attempts and finite timeouts. Save progress after each essay and reuse successful downloads on restart. Explicit refresh preserves previous byte versions and metadata; changed source titles retain history. Keep emphasis, notes, code, tables and links as HTML, including text links in sibling rows. Use original UTF-8 reading fragments and byte-preserved sources. Store author-hosted linked text/code/print documents separately. Do not infer dates from narrative references to earlier talks. URL identities ignore changing cache timestamps on the two fixed ANSI chapter links. Initial content-term grouping received an editorial pass over titles/openings and ambiguous topic cases; it is not a claim of a line-by-line reading or user approval.

**Checks actually run on native Windows:**

| Command/check | Outcome |
| --- | --- |
| `.\.venv\Scripts\python.exe run.py` | Foundation passed before collection work |
| `.\.venv\Scripts\python.exe -m src.collection` | Initial run saved 232 HTML entries and two text originals; text parsing initially failed visibly; six failed remote footer icons recorded |
| `.\.venv\Scripts\python.exe -m src.collection --reprocess` | After fixes, all 234 parsed successfully offline; text chapters preserved; known YC footer icon classified explicitly as decorative; date-line and sibling-link fixes applied |
| `.\.venv\Scripts\python.exe -m src.collection` | Saved ten companion files; repeat run reused successful originals/companions and reported zero failures |
| `.\.venv\Scripts\python.exe -m src.catalog` | Wrote complete grouped review; preserves saved choices; Lisp last |
| `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` | Ten tests passed: duplicate identity, source/title updates, bounded failure/retry, private choices, date precision, moving/excluding without deleting sources, sibling links and companion preservation |
| `.\.venv\Scripts\python.exe scripts/check_collection.py` | Full collection verification; final outcome recorded in collection-checks.md |

Representative original/fragment comparisons covered short prose, long prose with linked notes, Lisp introductions, code, tables and image references. No browser or iPad visual check was performed. Two linked print documents remain unconverted; the Roots of Lisp full text depends on one of them. This is explicit in the review and must be handled before full-book export. The separate Being Popular PostScript file duplicates an available HTML article.

**Remaining:** Review/approve or revise grouped choices. Phase 3 selects the PDF tool, resolves full-text conversion as needed, removes site furniture from rendered content, creates the sample with cover, and drafts the reusable design skill. No Phase 3 implementation has started. Upstream cover reuse remains unconfirmed; iPad and layout feedback remain pending.

Final checks: the full collection audit returned `234/234` and `0 issues`; all ten tests, the readiness command, `pip check`, local documentation links, original chapter-code comparison and `git diff --check` passed. Commit `7c9eae2e2b86d3d82b306f403378f2fc21b3b19b` was pushed to `origin/ipad-reading-edition`; `git ls-remote origin refs/heads/ipad-reading-edition` matched the local commit, and the working tree was clean. Downloaded data and personal settings were excluded. This follow-up documentation commit records that verified publication; no essay collection or skill release was published.

### 2026-09-09 - Phase 2 closed after user approval

User feedback: "grouping looks right, close this phase". Marked Phase 2 Complete and saved approval for all 234 current assignments in `config/book.json`. Regenerated the review list with approved status and aligned the README, design, decisions, setup and plan. Topic overlap notes, five unknown dates and linked-document conversion flags are retained. Approval applies to grouping only; no PDF design or iPad approval is implied.

Verification: regenerated the catalog review and checked all 234 choices retain their section and inclusion settings; ran the existing ten tests and whitespace checks. These closeout changes are committed and pushed with the authorised project workflow. Next: `Start phase 3` in a new project chat. Phase 3 has not started.

### 2026-09-09 — Phase 3 implementation; awaiting iPad review

**Outputs:** `src/settings.py`, `src/print_content.py`, `src/pdf_builder.py`, reading defaults and excerpt choices in `config/`, `templates/book.css`, bundled OFL fonts/licences and pinned provenance in `assets/fonts/`, `scripts/check_pdf.py`, `scripts/check_windows_pdf_setup.py`, nine additional tests, and draft `skills/book-design/SKILL.md` with its workflow reference. Updated dependency lock, setup, public guides, design, decisions and plan. The added content-preparation module separates source handling from layout; the excerpt configuration keeps sample cuts separate from approved book inclusion.

**Actual local deliverables:** `output/sample-20260909-145000-91927e03.pdf` (19 pages, 665,885 bytes), `output/sample-20260909-144810-3895d5e9.pdf` (110-page complete five-piece proof), matching build/audit JSON files, and review images in `output/review/final/`. Earlier drafts remain separate files; use the named handoff trial. No generated book or downloaded essay belongs in source sharing.

**Commands and results on native Windows:**

| Command/check | Outcome |
| --- | --- |
| `.\.venv\Scripts\python.exe scripts/check_collection.py` | 234/234 saved sources, zero issues before implementation |
| `.\.venv\Scripts\python.exe -m pip install playwright pypdf pypdfium2 pillow` | Installed native Windows PDF candidates; selected after sample checks |
| `.\.venv\Scripts\python.exe -m playwright install chromium` | Matching browser available |
| `uv pip compile requirements.in --python-version 3.14 --generate-hashes --output-file requirements.txt` | Fourteen packages pinned and hashed |
| `python scripts/setup_windows.py` | Locked installation and readiness passed |
| `.\.venv\Scripts\python.exe -m src.pdf_builder` | Final 19-page trial generated under a unique name |
| `.\.venv\Scripts\python.exe -m src.pdf_builder --complete-essays` | Complete five-piece proof generated; not the whole collection |
| `.\.venv\Scripts\python.exe scripts/check_pdf.py output/sample-20260909-145000-91927e03.pdf` | Zero issues; 18 internal rectangles, one external, 13 outline entries, one image |
| `.\.venv\Scripts\python.exe scripts/check_pdf.py output/sample-20260909-144810-3895d5e9.pdf` | Zero issues; 78 internal rectangles, four external, 13 outline entries, five images |
| `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` | Nineteen tests passed, including custom image cover, changed settings and preserving prior exports |
| `.\.venv\Scripts\python.exe scripts/check_windows_pdf_setup.py` | Fresh Python environment in a spaced Windows path: setup, sample and audit passed; existing per-user Chromium cache reused |
| `uv run --with pyyaml python C:/Users/acer/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/book-design` | Skill format valid; the first plain-Python attempt lacked PyYAML, then passed with a temporary validator dependency |
| Rendered-PDF and destination inspection | Trial pages reviewed; proof boundaries, notes, code, quotation, images, tables and last page inspected; short notes refined to avoid stranded continuations |

The audit caught and prompted fixes for a duplicate table heading and a trailing-ornament page. PDFium's bounded text extraction marks some line-ending hyphens with U+0002; the audit normalises that marker. Serif ink can overhang the left alignment edge, so the left tolerance is 2 pt; writing-area tolerance remains 1 pt. The original slower text-diff diagnostic was replaced with a practical comparison. See `docs/sample-review.md` for design iterations and actual inspection limits.

**Not tested:** manual Windows PDF-reader click/drag interaction, browser app, physical iPad behaviour. The builder's original-text fixture is not Phase 5's independent reusable-skill exercise.

Final source checks: collection still reports 234/234 and zero issues; `pip check` passes; all new local documentation links resolve. Staged scope excludes essays, PDFs and personal settings. Font/licence fingerprints match pinned downloads. `.gitattributes` preserves those exact bytes across Windows clones; original licence trailing whitespace is retained under a narrowly scoped whitespace rule.

**Remaining / exact handoff:** Phase 3 is Awaiting user review, not Complete. Try the named trial using `docs/sample-review.md`; resume with `Start phase 3` and feedback to revise. Independent Phase 4 requires a separate request. Keep the skill a draft until Phase 5 approval, packaging and original-manuscript validation. Inherited cover terms remain unresolved; sample cover is original typography. Roots of Lisp still needs full-text preparation before a whole-collection edition. Source/doc commit and push follow existing authorisation; no separate skill release or essay publication is authorised.

**Verified source sharing:** commit `d62c37096b41a488daa1e5a85891dfabdec190d4` was pushed to `origin/ipad-reading-edition`; `git ls-remote origin refs/heads/ipad-reading-edition` matched the local commit and the working tree was clean. All 37 committed files are source, configuration, documentation or permitted fonts/notices. The PDFs and saved essays remain local. This follow-up documentation commit records the verified push; Phase 3 still awaits iPad feedback.

### 2026-09-09 - Phase 3 initial feedback applied

Changed the default right writing area to 25% and bottom to 7.5% (half its former size). The reading column is 391 x 703 pt, right space 135 pt, bottom space 57 pt. Numbers now share the top title line. Added a very faint horizontal separator above bottom writing space; prose is justified with automatic word breaks, notes are 12 pt, and return labels are off. These new text options are configurable. Updated the reusable skill draft and public design/settings guides.

**Outputs:** `output/sample-20260909-151107-0700791e.pdf` (17 pages, 666,949 bytes) and `output/sample-20260909-151222-d72d2864.pdf` (94 pages). Both have matching build and audit records, zero audit issues, all five source-preservation checks passing, embedded fonts and valid destinations. Original PDF files were retained. No annotations or essay files are included in the source changes.

**Checks:** `python -m unittest discover -s tests -v` using the project environment: 19 passed. Both `scripts/check_pdf.py` audits pass. Reviewed all 17 trial pages in overview and enlarged prose, note and code pages on Windows. Updated text checks to recognise print-added line-ending hyphens and measured serif overhang up to 1.51 pt (2 pt tolerance). The skill format validator passed, and both original PDF fingerprints still match. No browser-app or physical iPad test occurred.

**Restart:** Read the required project documents and `docs/sample-review.md`, then open the revised 17-page sample. Await user approval or apply further feedback through `Start phase 3`; export a new file and rerun PDF checks. Phase 3 remains Awaiting user review. Do not begin Phase 4 or 5 automatically.
