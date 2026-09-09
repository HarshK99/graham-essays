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

Run `.\.venv\Scripts\python.exe -m src.catalog --list` to see titles with their IDs; this command changes no files. Edit the private copy in a text editor. The top-level `sections` list controls section order; retain each exact section name once. The Lisp section stays last in the section list, but its 10 entries are currently excluded at the user?s request. Re-enabling the two introduction-only entries requires companion preparation. Within `essays`, find the matching ID key and keep it unchanged:

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

`image-text.json` records visually checked title/section graphics by source fingerprint. The builder replaces five section graphics with text headings and omits duplicate title graphics and known footer icons; meaningful pictures remain images.

Current image setting: `include_images: false` omits essay images while keeping transcribed text headings. Set it to true to restore pictures. `contents_size: 10` and `contents_columns: 2` control the compact contents; columns may be 1, 2 or 3. Every numbered page has a clickable header returning to the first Contents page.

The 12 pt body / 1.25 line height / 3.75% bottom-space sample is now approved and is the shipped reset preset. The right writing area remains 25%. Personal overrides still take precedence. Earlier 13 pt and 14 pt references above describe previous trials.


## Approved illustrated cover and orange palette

The shipped book uses `cover_artwork: "assets/covers/makers-workbench.png"` with `cover: "typographic"`: artwork plus selectable author/title lettering. Set `cover_artwork` to an empty string for a text-only cover. For a complete supplied cover image, clear `cover_artwork` and set `cover` to that local image path.

`accent_color: "#944018"` controls burnt-orange headings/links, `rule_color: "#EAD5C4"` controls apricot dividers, and `cover_color: "#ED7024"` controls the cover background. These do not alter the image's own colours. Body text stays charcoal on white. The cover is independent of `include_images`, which controls essay pictures.


## Title-page credits and edition details

`config/book.json` also holds optional `compiled_by`, `project_url`, `linkedin_url`, `disclaimer`, `edition_version` and `edition_updated` fields. The update date uses YYYY-MM-DD and describes the compilation; change it when preparing a revised edition. The latest dated essay month is calculated from the complete included selection, including in previews. Entries without dates are not assigned guessed dates. Current version: 1.0; compilation updated 2026-09-09; latest dated essay August 2026. If using `book.local.json`, copy these fields into that private file to override the shipped credits.

Build the complete PDF from the project folder with `.\.venv\Scripts\python.exe -m src.pdf_builder --full`. The command prints a new PDF path under `output/`; previous exports stay unchanged.

`format_note` supplies the reader-focused explanation of the writing margins on page 2. The page begins with the selection introduction; compiler credits and links sit in its lower half, followed by a lighter ownership note. Compilation date updated to 2026-09-10; latest dated included essay remains August 2026.
