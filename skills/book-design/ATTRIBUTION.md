# Attribution and scope

The original design instructions, Python renderer/adapter and print styles were developed for this reading-edition project. The package contains those new components, not the inherited upstream downloader. See `LICENSE.txt` for their MIT terms. The two-chapter Morgan Vale manuscript is original example writing, released under CC0; the byline is fictional.

Source Serif 4, Source Sans 3 and Source Code Pro are Adobe fonts, supplied unmodified under their original SIL Open Font License notices. Preserve the three `assets/runtime/assets/fonts/*-LICENSE.md` files. `manifest.json` records upstream revisions, download URLs and SHA-256 fingerprints for the fonts and notices.

Dependencies are installed separately from the hash-pinned `assets/runtime/requirements.txt`; their own licences apply. Chromium is a separately installed Playwright dependency. Ghostscript is not a package dependency and is not included.

The parent project preserves an inherited cover and Paul Graham source links separately. This package includes neither the cover nor any downloaded essay, generated collection PDF, annotations or private settings. Preparing or sharing the software package does not grant rights to distribute someone else's manuscript.
