# Project progress and next-chat handoff

Last updated: 2026-09-09

## Current state

Phase 1 is complete. The upstream Git history, original source, and cover are preserved; a GitHub fork exists; the native Windows setup passes in two clean Python environments, including a project path with spaces. Phase 1 source and sharing guides are committed and pushed to `ipad-reading-edition`, now the fork's default branch. No collection, browser app, or PDF has been built.

| Phase | Status | Evidence / remaining work |
| --- | --- | --- |
| 1 — Windows foundation | Complete | Fork and upstream history retained; clean Windows setup and repeat-run checks passed |
| 2 — Collection and sections | Not started | Requires the Windows foundation |
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

Open a new chat in `D:\FounderMode\Apps\pg-essays-pdf` and send `/phase 2`. If the app does not send that form, use `Start phase 2`.

Read AGENTS.md and docs/commands/phase.md, then the required project docs, docs/windows-setup.md, and docs/upstream/PROVENANCE.md. Run `.\.venv\Scripts\python.exe run.py` to check the foundation. Preserve the local changes and upstream history. Implement source collection and cataloging in Phase 2 without importing or running the old `graham.py`, which has download and deletion effects at import time. Do not restart the design discussion.

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
