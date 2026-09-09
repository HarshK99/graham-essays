# Upstream source and reuse review

Inspected on 2026-09-09.

- Original repository: https://github.com/ofou/graham-essays
- Exact revision: `96885e3b4018f0f1d976634e26b27a86e94aacfc` (2026-08-25, “Fix invisible EPUB text on iOS Books dark mode (#27)”).
- GitHub fork: https://github.com/HarshK99/graham-essays ; API confirmed its parent is `ofou/graham-essays`.
- The full Git history is retained locally. Local branch: `ipad-reading-edition`; `upstream` points to the original, `origin` to the fork. The user authorised sharing project adaptations on this branch on 2026-09-09.
- `graham.py`, `Makefile`, `epub.css`, `metadata.yaml`, `cover.png`, and `scripts/fix_epub_ibooks.py` are retained as upstream references. The Windows path does not execute the old pipeline.
- Original README, instructions, dependency list, and workflows are archived in this folder. Existing project instructions and planning documents were preserved. Workflows were moved out of `.github/workflows` because they run the old EPUB pipeline and can publish releases automatically.

## Terms and cover

No licence or copying notice file exists in the inspected Git tree; the GitHub repository API returns `license: null`. No general code redistribution permission has been established. Do not describe the code as permissively licensed or add a licence purporting to cover upstream work.

The upstream [metadata](https://github.com/ofou/graham-essays/blob/96885e3b4018f0f1d976634e26b27a86e94aacfc/metadata.yaml) attributes the writing to Paul Graham, the generating code to Omar Olivares, and the cover to https://startupquote.com/post/868392835. The cover source could not be opened with the web tool during this review. Attribution is recorded, but permission to reuse or redistribute the image is unconfirmed. Preserve the image for later reuse review; do not treat it as an approved asset. Phase 3 still requires a cover and can use an original typographic cover if permission remains unresolved.

Preserved file: `cover.png`, SHA-256 (a fingerprint used to detect changes):
`fe6dd55d10b385ba423c3e3852e80f9885895c63451beae1a26c04403f7b9155`.

No essay collection or generated book was uploaded. The fork preserves upstream files and carries the Windows edition on `ipad-reading-edition`.

## Download and build findings

`graham.py` discovers links from the live article index using Requests and Beautiful Soup. It reverses the index order. These libraries and the source URL are useful starting points for Phase 2; no downloader functions have been copied into the new foundation.

The old script executes network requests when imported, removes its previous CSV at startup, has no explicit request timeout or bounded retry policy, and relies on a pre-existing `essays/` folder. It discards images and tables, rewrites whitespace and notes, assigns positional numbers, and can infer a full date from a month-only source. Failures print but do not create a persistent per-source status record. Its 0.05-second delay disagrees with the accompanying half-second comment. These behaviours do not meet the preservation and review requirements.

The Makefile explicitly uses Bash, recognises only macOS/Linux, installs system tools, and has a cleanup step that deletes the environment and previous outputs. Its PDF target converts from EPUB with Calibre. It is retained for provenance, not used by Windows setup.

## Foundation choices

Use the installed Windows Python 3.14 line (tested interpreter: 3.14.7). Standard-library `venv` creates a private `.venv`; pip installs the exact versions and hashes in root `requirements.txt`. `requirements.in` lists Requests and Beautiful Soup for subsequent HTML collection; their complete dependency set is locked. The original broader list is archived as `docs/upstream/requirements.txt`.

No Bash, make, Linux subsystem, Pandoc, Calibre, Node, or PDF library is needed for Phase 1. `uv` was used only to generate the dependency lock; it is not required to run setup. PDF tool and app framework remain Phase 3/4 decisions.

File-map additions: `scripts/setup_windows.py` owns Windows setup; `run.py` provides an offline readiness check until later commands exist; `config/README.md` documents storage. No collection, catalog, settings engine, or app is claimed yet.
