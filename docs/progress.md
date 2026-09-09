# Project progress and next-chat handoff

Last updated: 2026-09-09

## Current state

All five phases are complete. Final approved output: `output/full-20260909-180513-3c502f76.pdf`, 224 essays, 1,348 pages, 16,420,926 bytes. Original illustrated orange cover, burnt-orange accents, apricot rules, 12 pt body / 1.25 spacing / 25% right / 3.75% bottom, no essay pictures, four pages of two-column contents and top-title/page-number return links. The 10 Lisp-section entries remain excluded. User confirmed iPad testing complete and approved the final cover/theme. Focused final checks passed; the refreshed reusable package example passed.

| Phase | Status | Evidence / remaining work |
| --- | --- | --- |
| 1 — Windows foundation | Complete | Fork and upstream history retained; clean Windows setup and repeat-run checks passed |
| 2 - Collection and sections | Complete | 234 saved entries; grouping approved by user on 2026-09-09; checks passed |
| 3 — Sample PDF and iPad trial | Complete | Revised sample approved on 2026-09-09; 19 tests and both PDF audits pass |
| 4 — Command-line workflow | Complete | Automatic private settings, explicit full selection, content checks, reset guidance and tested separate exports |
| 5 - Full reading edition | Complete | Final orange book approved; focused checks and reusable package exercise passed; user reported iPad testing complete |

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

The reader-intention page, lower-half credits and lighter disclaimer are implemented and checked in `output/sample-20260909-183140-26c6d24b.pdf`. To include them in the full book, run `.\.venv\Scripts\python.exe -m src.pdf_builder --full`; the new filename is printed under `output/`. The existing full PDF predates this update. All five phases are complete; no repeat device review or broad audit is needed for this change. Keep annotated copies separate.

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

### 2026-09-09 - Phase 3 closed after user approval

User feedback: "approved. close this phase and tell me next steps". Recorded approval of `output/sample-20260909-151107-0700791e.pdf` and its current settings. Phase 3 is Complete at the user's explicit request. This records sample acceptance, not invented results for Preview, Goodnotes, highlighting or handwriting; no app preference or individual interaction results were supplied. Full-book device review remains a Phase 5 requirement.

Updated public status, sample review, design decisions, configuration notes, draft-skill approval wording and plan checkboxes. Existing evidence remains 19 passing tests and two passing PDF audits (17-page sample and 94-page five-piece proof). Closeout verification passed: both PDF fingerprints and saved clean audits match; both build settings match the approved defaults; local links in all nine changed documents resolve; Phase 3 checkboxes are complete and later-phase checkboxes remain untouched; `git diff --check` passes. Documentation-only changes required no PDF rebuild or repeat browser/device test. Commit and push the closeout under existing source-sharing authorisation.

**Next command:** `Start phase 4` in a new chat in this project. Build the local app with saved content/layout choices and export controls using the approved sample builder. Phase 4 and Phase 5 remain Not started. Keep essay data, PDFs and annotations local; skill packaging and its independent example validation remain Phase 5 work.

### 2026-09-09 - App scope removed

The user confirmed that command-line PDF generation and asking an agent for changes are sufficient. Removed the browser/desktop app from the active specification, Phase 4 checklist, Phase 5 prerequisites, phase command and public guides; saved this preference in AGENTS.md. Earlier app references in the dated work log describe the superseded plan.

Phase 3 remains Complete. Phase 4 is now a smaller command-line workflow phase: inspect existing commands and saved settings first, then close actual gaps such as convenient full-collection selection, reset guidance and agent usage instructions. Do not rebuild features already delivered or start implementation from this documentation request. Phase 5 still produces and checks the full book and finalises/tests/packages the reusable skill. Full Roots of Lisp conversion remains outstanding.

Next: `Start phase 4` in a new project chat. This scope update changes documentation only; PDFs, source code and personal settings remain unchanged.

Verification for this scope update: inspected the existing builder/settings code and confirmed `python -m src.pdf_builder --help` exposes settings, essay selection, output folder and complete-selected-piece options. All 11 changed files are Markdown; local documentation links and `git diff --check` pass. Later-phase checkboxes remain unchecked. No implementation or PDF rebuild was performed. Source/document sharing follows existing authorisation.

### 2026-09-09 — Phase 4 complete

**Outputs:** extended `src/settings.py`, `src/catalog.py` and `src/pdf_builder.py`; four new tests plus expanded catalog coverage (23 total); updated configuration, setup, public README, design, decisions and phase plan. No new dependencies or app. Private configuration remains optional and ignored; no personal file was left in the real project's config folder.

Personal settings now load automatically, explicit settings/book files work per export, Windows UTF-8 encoding markers are accepted, invalid manual ordering is rejected, and `src.catalog --list` provides stable IDs without writing files. Added `--full` and `--check`; full selection always uses complete included essays in saved section/order choices. Content preparation gathers all failures before printing, progress includes counts, full/sample filenames differ, and records capture effective book choices as well as formatting and source versions. Backup/reset and agent-request examples use these same files and commands.

**Actual Windows checks:**

| Command/check | Result |
| --- | --- |
| `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` | 23 passed; final exit 0, output saved in `output/phase4-tests.log` |
| `.\.venv\Scripts\python.exe output/phase4_config_check.py` | Three fresh Python commands in a temporary folder with spaces loaded 20%, 20%, then reset 25%; backup and shipped defaults preserved |
| `.\.venv\Scripts\python.exe -m src.catalog --list` | Listed all 234 IDs/titles in book order, with inclusion/status; local capture `output/phase4-essay-ids.txt` |
| `.\.venv\Scripts\python.exe -m src.pdf_builder --help` | Shows sample/full/check/book/settings options and their meanings |
| `.\.venv\Scripts\python.exe -m src.pdf_builder --full --check` | Exit 1; all 11 preparation blockers reported; no PDF created |
| `.\.venv\Scripts\python.exe -m src.pdf_builder --full` | Exit 1 with the same blockers before printing; local capture `output/phase4-full-check.log`; no partial full PDF |
| `.\.venv\Scripts\python.exe -m src.pdf_builder` | New 17-page sample `output/sample-20260909-153709-7413129a.pdf`, with matching JSON record |
| `.\.venv\Scripts\python.exe scripts/check_pdf.py output/sample-20260909-153709-7413129a.pdf` | Zero issues; all five text-preservation checks passed, embedded fonts, 14 internal link rectangles, 13 outline entries, one image |
| `.\.venv\Scripts\python.exe scripts/check_collection.py` | 234/234 sources checked; zero issues |

The original-manuscript PDF test exercised the full branch twice with moved sections, a failed-but-explicitly-excluded record, saved 20% formatting, reset 25% formatting and distinct output paths; the first PDF and original source remained unchanged. Its full PDF passed the existing audit. Unknown/duplicate/excluded selections, empty full selection, conflicting full/excerpt selection, and multiple unready sources fail visibly. These temporary test PDFs are not the final collection or Phase 5's independent skill exercise.

**Full-collection preparation blockers:**

| Essay | ID | Current blocker |
| --- | --- | --- |
| The Hardware Renaissance | `c64f8cd576efd87393df` | Print preparation fails wording-preservation comparison |
| Maker's Schedule, Manager's Schedule | `3a1b1c09395f954b1d4d` | Same wording guard |
| Taste for Makers | `6f4d09308b9f6c26a061` | Same wording guard |
| The Founder Visa | `13bccc66a8130d0c864d` | Same wording guard |
| The Four Quadrants of Conformism | `ccb94d37806263bc4b4a` | Same wording guard |
| Orthodox Privilege | `279c4b18c7d555c1a95b` | Same wording guard |
| Succinctness is Power | `b4434856f6918768e576` | Same wording guard |
| A Plan for Spam | `f30fd7c5b278754bf92c` | Same wording guard |
| Revenge of the Nerds | `4c8e08e8bd00f258c08f` | Same wording guard |
| The Roots of Lisp | `bd06b77c3ca90aff1c4b` | Main page is an introduction; complete saved PostScript companion needs preparation |
| Lisp for Web-Based Applications | `e34d340bf9b9003f5a85` | Main page is an introduction; saved text companion needs explicit integration |

Successful source acquisition and failed print preparation are different results. These checks do not establish whether each of the nine wording differences is substantive or a structural conversion issue; inspect before fixing. None of the eleven entries was silently excluded, their saved sources were not edited, and approved grouping/default formatting remains intact. Phase 4 explicitly allows blocking incomplete full content; Phase 5 must repair it before claiming a complete edition. Do not disable the wording guard to make the full command pass.

**Inspection limits:** automated Chromium printing and PDF audit on Windows; no new visual page review, manual Windows-reader interaction or physical iPad test this phase. The user-approved Phase 3 layout remains the reference. No new layout approval is inferred from these exports.

**Restart:** `Start phase 5` in a new project chat. Read the required docs and this blocker list, fix preparation using preserved originals/companions, rerun full content checks, then generate/audit/inspect the final book with `--full`. Obtain full-book iPad feedback and finalise, independently validate and package the draft skill. Phase 5 is Not started. All generated books, logs, original essays and local diagnostics stay ignored; source/documentation sharing follows existing commit/push authorisation.

Final closeout checks: local Markdown links and `git diff --check` passed; both previously approved PDF fingerprints still match their records. The new sample is 666,798 bytes and matches its record. No `full-*.pdf` exists in the main output folder. Phase 4 checkboxes are complete; Phase 5 checkboxes are untouched. Approved book choices and the reading-default preset have no source changes.

Verified source sharing: commit `8e11b0351a21f837c17716ce52340aa160e0f4ce` was pushed to `origin/ipad-reading-edition`; `git ls-remote origin refs/heads/ipad-reading-edition` matched local HEAD and the working tree was clean. The 16 files contain only source, tests and documentation. PDFs, source downloads, diagnostics and personal settings remain ignored. This follow-up documentation commit records the verified push; no essay collection or separate skill release was published.


### 2026-09-09 ? Phase 5 generated; compact-layout discussion

Repaired nine content-preparation blockers without disabling wording comparison: literal angle brackets, nested quotation duplication, rowless layout tables and raw code entities. User chose to skip the 10-entry Lisp section, so both companion conversions were stopped and remain unprepared. Updated shipped inclusion choices and grouped review; originals retained. Visually inspected saved images, transcribed five section headings, and removed duplicate title images/known footer icons. Fixed contents pagination and removed inspected website promotions/labels.

Actual outputs: first draft `output/full-20260909-170109-3d59d4bc.pdf` (1,970 pages, 90,130,363 bytes); revised `output/full-20260909-170856-ab9fe596.pdf` (1,966 pages, 88,968,432 bytes); losslessly compacted new copy `output/full-20260909-171654-caa6fa25.pdf` (1,966 pages, 14,690,581 bytes), with companion build records. Stream compression is now in the builder. A changed-settings four-piece sample at 20% right margin is `output/sample-20260909-171610-020356c5.pdf` (13 pages). That sample is not a smaller-font trial.

Checks actually run: 27 tests passed, then the five focused full-content tests passed after adding image-heading coverage (28 test cases now exist). Full content preparation passed for all 224 included records. Rendered cover/title/contents, every section boundary, representative long essays, notes, pictures and flagged italic edges on Windows. Earlier audit flagged italic ink extending up to 2.89 pt beyond alignment edges, still in the 14 pt gap; recorded a 3 pt horizontal tolerance. No manual PDF-reader or iPad interaction was tested.

The revised full audit (`output/phase5-final-audit.log`) is NOT clean. Remaining flags include Type 3 fonts whose glyph drawings are stored inside the PDF but are not recognised by the checker's font-file rule, and numbered-list labels added by the browser but absent from the checker's plain-text expectation. Diagnostics show inserted list numbers, without detected source-word deletions in those cases. The compacted copy has not received a separate complete audit. These findings are limitations requiring honest reporting, not grounds for claiming clean validation. The user explicitly asked to stop the refinement loop; no further audit or full rebuild should run just to clear these flags.

Prepared `skills/book-design/` with renderer/templates, approved settings, permitted fonts/licences, manuscript adapter and original sample. Skill format validator passed. A separate original manuscript in `../book-design-original-trial-final-20260909/` produced a five-page PDF with a clean audit; another run in `../book-design-original-no-margins-20260909/` demonstrated zero writing margins and also passed. All five original-sample pages were visually inspected. Last stream-compression change still needs refreshing into the packaged runtime before final sharing. No separate skill release or essay publication occurred.

User's latest request: fewer tests per phase; explain and consider reducing the page count/file size. All relevant Python build/check processes had finished when inspected. Current work is uncommitted; source/doc review and authorised GitHub push remain pending. Keep Phase 5 open for the chosen layout, practical device feedback and brief final packaging/handoff work.


## Compact sample update - 2026-09-09

User requested no essay images, smaller two-column contents, and a link from the top title/page number back to Contents. Then requested slightly smaller essay text or tighter spacing. Implemented configurable `include_images=false`, `contents_size=10`, `contents_columns=2`; saved a personal trial of 13 pt body text and 1.35 line height in ignored `config/reading-settings.json`. The approved body defaults remain 14 pt / 1.45 until sample review. Writing margins remain 25% / 7.5%. Text headings transcribed from images remain; essay pictures are intentionally omitted and originals retained. The typographic cover remains.

Review sample: `output/sample-20260909-172648-ebf18356.pdf` (13 pages, 220,967 bytes), with matching settings/build record. The whole 224-title list is shown separately in `output/contents-preview-714398a3.pdf` (4 pages). That visual-only preview explicitly uses page numbers from the previous edition; it is not a newly rebuilt book and its entries are not navigation links.

Focused checks only: no image objects in the sample, correct internal Contents destinations on all 12 numbered pages, and image removal from What I Did this Summer (the essay on page 122 of the previous edition). Inspected sample contents/prose and all four dense contents-preview pages. A first short draft exposed numeric rather than page-object header destinations; fixed and regenerated the sample once. No full test suite, full-book rebuild or device test. Exact results are in `output/compact-sample-checks.json`.

Next: user reviews the compact sample, then explicitly agrees on the full rebuild. Phase 5 remains Awaiting user review. Previous full PDFs are unchanged. Sharing/packaged-runtime refresh and final phase closeout remain pending; current source edits are uncommitted.


### Smaller sample - 2026-09-09

At the user's request, generated another four-piece sample with 12 pt body text, 1.25 line height and bottom writing space halved from 7.5% to 3.75% (28.5 pt). Right writing space stays 25%; image omission, two-column 10 pt contents and header return links carry forward. Personal settings saved in `config/reading-settings.json`; prior 13 pt / 1.35 settings backed up to `output/reading-settings-before-smaller-9035f4f4.json`. Shipped body defaults remain unchanged pending review.

Output: `output/sample-20260909-173419-b81f54d6.pdf`, 11 pages, 216,531 bytes, versus the previous 13-page sample. Checked effective settings and verified the previous PDF fingerprint remains unchanged. Visually inspected rendered opening, continuation, notes and last page; no full test suite or full-book rebuild. iPad comfort and approval remain pending. Next: review this new sample and choose the preferred settings before rebuilding the whole book.


### Approved compact edition delivered - 2026-09-09

User approval: ?cool - go ahead and proceed? accepted the 12 pt / 1.25 / 3.75% bottom sample and authorised full production. Promoted those choices to reset defaults. Actual output: `output/full-20260909-173907-6e051f73.pdf` (224 essays, 1,348 pages, 13,603,725 bytes), with matching build record. Contents is four pages (3-6); every numbered page has the top return link. This saves 618 pages compared with the previous 1,966-page full edition. Ten Lisp-section entries are explicitly excluded; no essay pictures are included. Previous full PDF and approved sample fingerprints still match their original build records.

Commands/checks: `.\.venv\Scripts\python.exe -m src.pdf_builder --full` prepared all 224 selected sources successfully and generated the new file. `.\.venv\Scripts\python.exe scripts/check_navigation.py output/full-20260909-173907-6e051f73.pdf` passed with zero issues: selection/order, every selectable opening title, all contents/section/essay destinations, 1,347 header return links, embedded font data (including Type 3 glyph drawings), and zero reading images. This is a focused check, not an every-word comparison or exhaustive layout audit. No full unit suite or old comprehensive audit was rerun.

Rendered-PDF inspection covered pages 1-7, 78-79, 84, 545-546, 770-771, 796, 819-820, 995-996, 1110-1111, 1171-1172, 1233-1234, 1245 and 1348: full front matter, all section boundaries, representative long prose, notes, tables, code, the previously pictured essay and last page. Review images: `output/review/approved-full/`. No manual Windows-reader click/drag or physical iPad test is claimed.

Refreshed the shareable runtime via `scripts/package_book_design.py`, including approved defaults, current templates, lossless stream compression and correct header links. `skills/book-design/scripts/build_book.py` generated the original manuscript in `../book-design-approved-example-20260909/`; its five-page PDF and audit passed, and metadata correctly identifies the original author. Earlier separate example runs also established optional zero writing margins and visual treatment. The skill format validator passed. Bundled font/licence byte-preservation rules now cover the portable runtime. The package is ready in `skills/book-design/`; it has no essay collection and is not a separate public release.

Remaining: actual full-book iPad navigation/highlighting/handwriting/responsiveness feedback. Phase 5 is Awaiting user review, not Complete. Resume `Start phase 5` with feedback; if acceptable, close the phase without another rebuild or broad test loop. Source/docs are being committed and pushed under existing authorisation; generated PDFs, local sources, annotations and personal settings remain ignored.

Verified source sharing: delivery commit `99f58498b2d25c22f73f84b9081ea7c178db25d7` was pushed to `origin/ipad-reading-edition`; the remote branch matched local HEAD and the working tree was clean. Source, documentation and the permitted design package were shared; generated books and local data stayed ignored. This final documentation note records the successful push. Phase 5 remains Awaiting user review for the full-book iPad check.

### 2026-09-09 - Original orange cover preview

User confirmed iPad testing complete, requested original illustrated cover and orange palette, then authorised the proposed preview. Generated one original workbench illustration with the built-in image tool; saved it in `assets/covers/makers-workbench.png` with provenance. Author/title remain selectable typeset text. Added configurable cover artwork, cover colour and divider colour, and removed hardcoded green rules/dots from the active renderer/template. Approved 12 pt / 1.25 spacing and writing areas remain unchanged.

Preview: `output/sample-20260909-175902-8d07e568.pdf`, 11 pages, 3,031,766 bytes. Inspected rendered cover, contents and opening essay. Focused checks passed: cover title selectable, exactly one cover image, no reading-page images, and every numbered page has a contents-return destination. No full suite or full-book rebuild. Previous full book retained. The cover adds approximately 2.8 MB compared with the earlier sample.

Remaining: preview approval, one full export, packaged-runtime refresh and final documentation/source sharing. Device completion is user-reported; no claim of agent-operated iPad testing or individual unreported interactions.

### 2026-09-09 - Phase 5 complete: approved illustrated orange edition

User approved the cover/theme with "perfect - move ahead". Promoted the artwork to the shipped default and exported the full book once: `output/full-20260909-180513-3c502f76.pdf`, 1,348 pages, 224 essays, 16,420,926 bytes. No reading-layout changes. The previous full PDF hash still matches its record.

Focused final check passed with no issues: 224 selected essays/order/opening titles, four contents pages, bookmarks/destinations, 1,347 header-return links, embedded fonts and zero reading images. Cover text is selectable with exactly one cover image. Visually inspected cover, first contents and first essay page in `output/review/orange-final/`; earlier full-book inspection remains applicable to unchanged pagination. No broad test suite repeated.

Refreshed reusable runtime and guidance, retaining a generic typographic orange cover and optional artwork support. Independent original manuscript export: `../book-design-orange-final-20260909/output/full-20260909-180443-8619ff11.pdf`, five pages, no audit issues; cover and first chapter visually inspected. Updated README, settings/setup docs, design decisions, review and plan. All phases complete; no next phase or pending user approval. Source/docs/artwork sharing follows existing authorisation; books, essay data, annotations and private settings stay local. Device testing completion is based on user feedback.


## Title-page credit update - 2026-09-09

Added Compiled by Harsh Kankaria, the GitHub project link, a clickable LinkedIn icon (https://linkedin.com/in/harshkankaria9), and a disclaimer distinguishing essay ownership from compilation/layout and stating no author affiliation or endorsement. Removed font-family and generated-settings lines. Added version 1.0 and compilation date 2026-09-09; latest dated essay month is derived from all included records, currently August 2026 (How Universities Should Prepare Founders). Unknown dates remain unknown.

Checked `output/sample-20260909-182821-af5c8295.pdf`: 11 pages; page 2 visually inspected; credit/version/dates/disclaimer text and both external PDF links passed. Reusable renderer/template refreshed. No full rebuild or broad test suite: the user requested the command to generate the final file. The previous full book remains `output/full-20260909-180513-3c502f76.pdf` and does not contain these new credits. Run `.\.venv\Scripts\python.exe -m src.pdf_builder --full` from the project directory to produce the new complete edition; the command prints the new filename. All phases remain complete; this is a subsequent title-page change.


## Reader-intention page revision - 2026-09-10

Page 2 now begins with the selection introduction. Added About the format: right-side space for notes beside passages, bottom space for reflections/sketches/ideas, framed around active reading rather than any device. Moved compiler credit, edition details and links into the lower half; made the ownership disclaimer a lighter readable grey. Compilation date is 10 September 2026; version remains 1.0 and essay coverage August 2026.

Preview: `output/sample-20260909-183140-26c6d24b.pdf` (UTC filename), 11 pages. Visually inspected page 2, verified text order and both external link destinations. Refreshed the reusable renderer/template. No full rebuild or broad test suite. To create the complete updated book, run `.\.venv\Scripts\python.exe -m src.pdf_builder --full`. Existing full PDFs remain unchanged.
