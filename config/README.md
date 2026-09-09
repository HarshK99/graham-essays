# Saved configuration

Phase 1 creates the folder but does not settle book settings.

- `reading-defaults.json`: shipped layout preset, introduced in Phase 3.
- `reading-settings.json`: local user choices, excluded from Git.
- `book.json`: editable section ordering and essay inclusion, introduced in Phase 2.

Saved original content lives in `data/sources/`, source records in `data/catalog.json`, and new PDF exports and build records in `output/`. These paths are relative to the project folder, independent of the folder used to launch a command. Setup never clears them.
