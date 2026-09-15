---
description: Report current project state from CLAUDE.md and docs/roadmap.md against the repo
allowed-tools: Bash(git log:*), Bash(git status:*), Read, Glob
---

## Context

- Recent commits: !`git log --oneline -15`
- Working tree: !`git status --short`

## Task

Give me a touch base on where the project stands, so a session can orient
without a pasted transcript. This is read only: never edit, stage, or
commit.

Follow these steps:

1. Read CLAUDE.md for stable orientation and docs/roadmap.md for the
   volatile state: Current status, Done, Open items, and Next milestone.
2. Verify the roadmap against the repo instead of trusting it. For each
   Done entry, check with Glob that the file it claims is present; for each
   Open item, check whether the file it would produce already exists. Take
   the git Context above as the true recent history and working tree.
3. Report these sections, each short:
   - Current milestone: the active milestone and its one-line status, from
     the roadmap's Current status.
   - Recent work: summarize the last commits from the git log Context; do
     not paste the raw log.
   - Next open items: the roadmap's Open items, nearest first, each with
     the run instruction it carries so I can act on it.
   - Drift: every place CLAUDE.md or docs/roadmap.md disagrees with the
     repo, whether from step 2 or a CLAUDE.md line the roadmap has moved
     past. If nothing disagrees, say "No drift."
4. Point to files and let me open them; do not restate whole sections of
   CLAUDE.md or the roadmap.
