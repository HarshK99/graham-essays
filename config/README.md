# Saved configuration

- `book.json`: shipped section order and essay choices, approved on 2026-09-09.
- `book.local.json`: optional private copy of book choices; preferred when present, excluded from Git.
- `reading-defaults.json`: shipped sample layout preset, approved by the user on 2026-09-09.
- `reading-settings.json`: personal layout overrides, excluded from Git; used automatically when present.

Copy `book.json` to `book.local.json` before personal edits. Each essay has one section, an `included` switch, optional numeric `order`, and review notes. Source identities are based on URLs. Run the catalog command to regenerate the grouped review list; it does not reset choices or delete sources.

Original content and images live in `data/sources/`, metadata and failures in `data/catalog.json`, and new PDF exports in `output/`. Setup never clears them.

`sample-selection.json` records the default short-trial excerpt boundaries. Complete selected pieces are available with `--complete-essays`. These sample cuts do not change book inclusion or saved sources.

The revised defaults use `right_notes: 0.25`, `bottom_notes: 0.075`, `alignment: "justify"`, `note_size: 12`, and `note_returns: false`. Alignment also accepts `"left"`; optional return labels can be enabled with `true`. Page numbers share the title's top line, and a faint horizontal rule marks the bottom writing area. These settings reflect the revised PDF approved by the user on 2026-09-09.

## Personal formatting and reset

For a new personal file, save this as `config/reading-settings.json`:

```json
{
  "right_notes": 0.20,
  "body_size": 14,
  "notes_background": "blank"
}
```

If the file already exists, edit the relevant fields while keeping other choices. Missing fields inherit the approved defaults. Unknown fields, invalid values and broken JSON stop the command. UTF-8 files saved by Windows PowerShell are supported, including its optional leading encoding marker.

Both sample and full exports automatically reuse this file. `--settings path/to/file.json` instead merges that specific file over the shipped defaults; it does not layer it over personal settings. For one export with the approved defaults, use `--settings config/reading-defaults.json`.

To reset future exports while keeping your personal choices as a backup, run from the project folder:

```powershell
if (Test-Path -LiteralPath config/reading-settings.json) {
    Move-Item -LiteralPath config/reading-settings.json -Destination ("output/reading-settings-backup-" + [guid]::NewGuid().ToString("N") + ".json")
}
```

Setup creates `output/`. The backup location is excluded from Git. With the personal file moved, future commands use approved defaults. To restore, copy that backup to `config/reading-settings.json` after keeping a backup of any newer personal choices. This reset only moves the named settings file; it does not affect books, sources or annotations.

## Book order and selection

Create the private book copy once:

```powershell
if (!(Test-Path -LiteralPath config/book.local.json)) {
    Copy-Item -LiteralPath config/book.json -Destination config/book.local.json
}
```

Run `.\.venv\Scripts\python.exe -m src.catalog --list` to see titles with their IDs; this command changes no files. Edit the private copy in a text editor. The top-level `sections` list controls section order; retain each exact section name once. Lisp stays last in the shipped defaults. Within `essays`, find the matching ID key and keep it unchanged:

- Change `section` to one of the six exact section names to move it.
- Change `included` to `false` to exclude it, or `true` to restore it.
- Add `"order": 1`, `"order": 2`, etc. to put pieces first within a section. Entries without `order` follow, oldest first; unknown dates use website order. Remove `order` to return to chronological order. Values must be finite numbers.

Run `.\.venv\Scripts\python.exe -m src.catalog` to update the review list. It writes `docs/essay-review.md` with your current choices, so review that change before sharing source commits. Export itself reads saved choices directly, without needing this command. `--book config/book.json` uses shipped choices for one export; `--book path/to/choices.json` uses another complete book file. Explicit book files must cover every catalog entry.

To reset future book choices, move only the private copy to a backup:

```powershell
if (Test-Path -LiteralPath config/book.local.json) {
    Move-Item -LiteralPath config/book.local.json -Destination ("output/book-choices-backup-" + [guid]::NewGuid().ToString("N") + ".json")
}
```

See [Windows commands](../docs/windows-setup.md#saved-choices-and-full-export-phase-4) for selected samples, full export, content checks and agent examples.
