---
name: book-design
description: Design and refine a book PDF from a manuscript, including typography, front matter, navigation, and optional handwriting margins. Use for book-length reading layouts and representative PDF trials, not slide decks or ordinary document conversion.
---

# Book design

This is a draft, informed by a Windows reading-edition trial. The user approved the revised sample layout on 2026-09-09; specific device interactions were not reported. Standalone validation and packaging remain Phase 5 work. Read [the trial workflow](references/trial-workflow.md) when using this repository's builder; other manuscripts may need a different content adapter.

Start with the actual manuscript and the reader's intended page view. Choose page dimensions together with type size; points alone cannot establish reading comfort. Establish one typographic hierarchy spanning cover, title page, contents, section openings, essay/chapter openings, body, notes, and page details. Use an original typographic cover when no permitted image is available.

For optional handwriting space, reserve bottom space first, then divide the remaining width between text, a gap, and side notes. Keep author notes in the reading column. Place page details outside the usable writing areas. A manuscript without handwriting requirements can use zero writing-space fractions; do not impose this project's device or section choices.

Keep body text selectable and embed permitted fonts, including italic and emphasis variants. Preserve the source's wording, punctuation, emphasis, code indentation, tables, meaningful images and attribution. Separate site promotions from author content using inspected evidence, and record each removal. Label excerpts and carry their referenced notes into the sample. Make note-return labels optional. Reject incomplete sources visibly.

Avoid shrinking text to meet a page count. Reflow prose, retain code structure, wrap long code visibly, and inspect any wrapping that could change its interpretation. Keep headings with following content; use at least three-line widow/orphan control for ordinary paragraphs. Inspect actual rendered pages for isolated headings, note markers, sparse continuations and awkward table breaks.

Choose left alignment or justified prose after inspecting word spacing at the actual column width. For justification, inspect automatic word breaks and retain left-aligned final lines; keep code spacing intact. Size author notes separately from body text. If requested, separate bottom writing space with a faint horizontal rule, and put title and number together above the text.

Generate directly to PDF with the tested engine. Verify the exported file independently: text preservation, embedded fonts, page bounds, clickable contents, correctly nested bookmarks, author-note destinations and optional returns, and clean writing areas. Account for print-added line-ending hyphens and measured font overhang without concealing missing words or overflow. Browser layout alone is not proof of PDF pagination. A selectable text layer does not prove a particular device's highlight interaction.

Export to new filenames with companion records of settings, source versions, excerpt boundaries, and tool versions. Keep annotated copies independent. Record each design iteration and distinguish automated checks, visual PDF inspection, and actual reader/device feedback.

Finalise reusable settings and assets only from the approved design. Validate the workflow on a separate original manuscript before packaging. Include only permitted assets; preparing a shareable folder does not publish it.
