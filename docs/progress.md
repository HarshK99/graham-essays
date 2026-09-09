# Project progress and next-chat handoff

Last updated: 2026-09-09

## Current state

Phase 2 implementation is delivered locally: 234 index entries saved successfully, six proposed sections with Lisp last, and a grouped review list. No sources are intentionally excluded. User review of the proposed grouping is pending. The collection includes 10 author-hosted companion files; the complete Roots of Lisp PostScript document is saved but needs conversion before a full export. No browser app, PDF or iPad check exists yet. Phase 1 remains complete.

| Phase | Status | Evidence / remaining work |
| --- | --- | --- |
| 1 — Windows foundation | Complete | Fork and upstream history retained; clean Windows setup and repeat-run checks passed |
| 2 - Collection and sections | Awaiting user review | 234 saved entries; grouped list available; source checks recorded below |
| 3 — Sample PDF and iPad trial | Not started | Requires representative essay content; include cover |
| 4 — Configurable app | Not started | Requires working sample generation |
| 5 — Full reading edition | Not started | Requires usable app, reviewed content order and approved layout |

## Latest confirmed additions

- The cover is required; preserve the upstream cover for reuse after checking its terms.
- Generate the PDF directly from essay content, without an EPUB intermediate.
- The user will start each phase in a new chat in this same project.
- `/phase N` and `Start phase N` both mean implement or resume that phase under AGENTS.md.
- Published-book visual quality is required, alongside the handwriting margins.
- Phase 3 drafts a reusable book-design skill; Phase 5 finalises, tests, and packages it from the design approved through iteration. No skill has been created or installed yet.

## Verification at instruction setup

Documentation-only inspection and local link checks. No phase code, browser workflow, fresh-chat command delivery, or iPad behaviour has been tested. Later phase workers should replace this general statement with their actual commands and outcomes in dated entries below.

## Next action

Review [the proposed essay order](essay-review.md), especially the overlap notes and the ten essays in the last section. User approval has not been received. To revise grouping, provide the essay titles and destination sections; `Start phase 2` resumes collection/review work without recreating saved sources.

For independent sample work, open a new chat in this project and send `Start phase 3`. Read the required project docs plus `docs/collection-checks.md` and `docs/essay-review.md`. Run `.\.venv\Scripts\python.exe scripts/check_collection.py`. Use `writing44.html` for short prose, `greatwork.html` for long prose and notes, the second ANSI Common Lisp chapter for code, `wtax.html` for tables, and `langdes.html` for image handling. Handle `content_scope` and companion records explicitly: `rootsoflisp.html` is an introduction with the full text in saved PostScript, while `lwba.html` has a saved plain-text companion. Do not call an introductory page the complete essay. Strip identified site promotions from typesetting without changing the originals. Draft the book-design skill in Phase 3. Grouping and iPad/layout approval remain pending; do not start Phase 4 automatically.

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

Final checks: the full collection audit returned `234/234` and `0 issues`; all ten tests, the readiness command, `pip check`, local documentation links, original chapter-code comparison and `git diff --check` passed. Source and documentation are prepared for the authorised push to `origin/ipad-reading-edition`; downloaded data and personal settings are excluded. Publication result is recorded after remote verification.
