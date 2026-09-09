# Saved configuration

- `book.json`: shipped section order and essay choices, approved on 2026-09-09.
- `book.local.json`: optional private copy of book choices; preferred when present, excluded from Git.
- `reading-defaults.json`: layout preset to be introduced in Phase 3.
- `reading-settings.json`: future personal layout choices, excluded from Git.

Copy `book.json` to `book.local.json` before personal edits. Each essay has one section, an `included` switch, optional numeric `order`, and review notes. Source identities are based on URLs. Run the catalog command to regenerate the grouped review list; it does not reset choices or delete sources.

Original content and images live in `data/sources/`, metadata and failures in `data/catalog.json`, and future PDF exports in `output/`. Setup never clears them.
