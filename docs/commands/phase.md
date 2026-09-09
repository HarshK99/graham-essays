# Phase command

## Usage

Open a new chat in this project's folder and send `/phase 1`, `/phase 2`, `/phase 3`, `/phase 4`, or `/phase 5`. If the app intercepts an unknown slash command, send `Start phase 1` (or the appropriate number). Both forms have the same meaning under AGENTS.md.

This is a saved instruction for the assistant, not a shell command or an installed slash-menu entry. Its delivery through a fresh chat has not been tested during setup. Project instruction loading is documented in [OpenAI's AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md).

## Meaning and scope

Start or resume the requested phase of the iPad Reading Edition. The user's invocation authorises implementation and normal local setup, downloads, edits, and checks needed for that phase. Phase 1 includes the already requested upstream GitHub fork if account access is available. It does not authorise unrelated publishing, uploading the generated essay collection, deleting user work, or starting later phases.

If a number is absent or outside 1–5, ask one concise question for the phase number. If the user explicitly asks only for a phase explanation, provide that explanation without implementation.

## Required startup sequence

1. Announce the requested phase and its intended result in one plain sentence.
2. Read AGENTS.md and these files completely: README.md; docs/design.md; docs/decisions.md; docs/progress.md; docs/superpowers/plans/2026-09-09-ipad-reading-edition.md.
3. Read any existing docs/essay-review.md, docs/sample-review.md, or docs/windows-setup.md relevant to the phase. These files may not exist before their phases.
4. Inspect the workspace, applicable additional instructions, and Git status/remotes if a Git repository exists. Preserve unrelated or unfinished edits. Do not assume a fork, tools, or dependencies already exist.
5. Check prerequisites using files and recorded verification. Resume completed partial work instead of recreating it. If the phase is already complete, report the evidence and next command rather than rebuilding without reason.
6. Carry out the requested phase's checklist and relevant checks. Resolve routine implementation choices using the design and evidence. Document justified file-map changes. Do not execute command examples that have not been verified against the current project.
7. Continue all independent in-scope work before stopping for missing access or user feedback. Ask one concrete question only when needed. Explain what remains possible and what depends on the answer.

## Phase-specific instructions

| Invocation | Prerequisites | Work and handoff |
| --- | --- | --- |
| `/phase 1` | Planning files only; no Git repository is assumed | Inspect upstream and its terms, preserve its history and cover, establish the Windows foundation. Keep the user's docs when importing upstream. Record exact revision, fork URL if created, dependencies and tested setup commands. No PDF tool is final yet. |
| `/phase 2` | Phase 1's usable local Windows foundation | Download and check content, preserve sources, build the catalog and proposed section list. Record failed downloads and uncertain assignments. Ask for review of the concrete grouped list; the list may remain pending review while sample work proceeds. |
| `/phase 3` | A usable catalog with representative essays from Phase 2 | Choose and prove a direct PDF tool, include the cover, render the configurable sample, verify selection/links/bookmarks on Windows, and supply the actual sample file for the iPad trial. Record device feedback as pending if absent. |
| `/phase 4` | A working sample builder and settings from Phase 3 | Finish saved configuration and command-line sample/full export workflow; support agent-driven changes. Reuse existing commands and checks; do not build an app or infer layout approval from successful exports. |
| `/phase 5` | Usable command-line export workflow and collection; reviewed ordering and approved sample settings for the final edition | Build and verify the selected full book with cover and new filenames. If approval is absent, complete independent checks but do not silently treat the final layout as approved. Full-book iPad testing remains a separate recorded check. |

If a technical prerequisite is missing, identify the exact missing output and the earlier `/phase N` needed. Do not silently implement an entire different phase. A routine defect in an available prerequisite may be fixed when necessary for the requested phase; record that repair.

## Required phase closeout

Phase 3 also drafts skills/book-design/SKILL.md from the evolving published-book design. Phase 5 must finalise that skill using the approved settings and actual PDF workflow, test it on a separate original sample, and prepare the supporting files for sharing. Follow the available skill-creator instructions when creating the skill. A completed PDF alone does not complete Phase 5. Record pending design approval accurately; do not publish the skill automatically.

Update docs/progress.md with:

- Status: Not started, In progress, Awaiting user review, Blocked, or Complete.
- Date, actual outputs and their paths, key decisions and any upstream/fork details.
- Exact commands run and their results; clearly separate automated checks, manual Windows checks, and actual user iPad feedback.
- Remaining work, failures, or missing access; record no secrets.
- A brief handoff sufficient for a fresh chat: what exists, what to read, what to do next, and the correct next/resume command.

Update only genuinely completed plan checkboxes. Keep docs/design.md and docs/decisions.md aligned with accepted changes. Use Complete only when the phase pass condition is met. If Phase 3 awaits iPad feedback, preserve that status even if Phase 4 later completes.

End with a short report: what changed, what was checked, what still needs the user, and the next command. Stop at the requested phase boundary. Never start a new chat or the next phase on the user's behalf.
