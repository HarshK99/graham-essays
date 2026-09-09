# Project instructions

## How to talk to the user

- Use plain words. Explain a technical term in the same sentence.
- Ask one question at a time, with concrete choices when needed.
- Say what you are about to do in one short line before doing it.
- Explain a skill, command, or subagent in one line the first time you use it.
- Report what was actually tested. Never imply a browser or iPad check happened when it did not.
- Avoid condescending language, keep answers proportional to the request, and push back gently when evidence warrants it.
- If the user says "explain that like I've only used ChatGPT", rewrite the explanation in familiar words.

## Start or resume a phase

When the user sends `/phase N` or `Start phase N`, where N is 1 through 5, treat it as a request to implement that phase, not merely explain its plan. Read and follow [the phase command](docs/commands/phase.md). This is a project instruction convention, not a registered built-in slash menu command.

Do not start implementation merely because these instructions exist. Requests to discuss, review, or change documentation remain scoped to those actions.

Before any phase work, read README.md, docs/design.md, docs/decisions.md, docs/progress.md, and docs/superpowers/plans/2026-09-09-ipad-reading-edition.md completely. Inspect actual files and Git state; do not assume previous chat history is available or that a progress label proves completion.

Preserve these instructions and project docs when bringing in upstream source. Reconcile upstream instructions with the user's confirmed requirements rather than overwriting this file.

## Product essentials

- Native Windows setup; reading on iPad A16 in Preview or Goodnotes.
- Include a cover. Preserve the upstream cover for reuse after checking its terms.
- Generate PDF directly from essay content; EPUB is not a required intermediate or deliverable.
- Right-side and bottom writing space on reading pages; no blank notes pages after essays.
- Broad sections; Lisp last in the main book.
- Configurable typography, spacing, page settings, and essay organisation.
- Every export is a new file without annotations from older copies.
- Initial fonts and proportions are trial settings, not iPad-tested final values.
- Aim for published-book design quality, including title page, contents, section openings, careful typography, and clean page breaks.
- Draft a reusable book-design skill during Phase 3; finalise and validate it in Phase 5 from the approved output. Preserve iteration decisions and package it for sharing without claiming public publication.

## Handoff

Before ending phase work, update docs/progress.md and the corresponding plan checkboxes with changes, checks and outcomes, remaining work, and exact restart instructions. Mark iPad/user review as pending until feedback arrives. Do not run subsequent phases automatically.

The user has authorised committing and pushing this project's work to the GitHub fork for sharing. Keep the public README and relevant setup/documentation guides current as phases are delivered, with a final pass at project completion. Exclude local data, generated books, annotations, credentials, and personal settings. This does not authorise publishing the essay collection or a separate skill release.
