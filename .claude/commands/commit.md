---
description: Draft and make a commit that follows docs/standards/git-commits.md
argument-hint: [optional one-line intent hint]
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git commit:*), Read
---

## Context

- Status: !`git status --short`
- Staged diff: !`git diff --staged`
- Last five subjects, for style consistency: !`git log -5 --pretty=format:"%s"`

## Task

Create one commit for the currently staged changes. Optional intent hint
from me: $ARGUMENTS

Follow these steps exactly:

1. If nothing is staged, list what is unstaged and stop. Never run
   `git add` yourself; staging is my decision.
2. Read docs/standards/git-commits.md and draft the message from the
   staged diff. The hint above tells you intent, not wording.
3. If the staged diff mixes unrelated logical changes, do not commit.
   Say so and propose how to split it into separate commits.
4. Self-check the draft before showing it:
   - header matches `type(scope): subject` with a type and scope from the
     standard
   - subject is imperative, starts lowercase, no trailing period, max 50
     characters after the prefix
   - body explains motivation and contrasts previous behavior, wrapped at
     72 characters, and is present for anything non-trivial
   - footer carries `BREAKING CHANGE: ` or `Closes #N` when applicable
   - no AI attribution or co-author trailer, no em-dash character
5. Show me the complete message and wait for my explicit approval.
6. On approval, commit using multiple `-m` flags (one per paragraph) or
   `git commit -F` with a temp file you then delete. Never `--amend`,
   never push.
7. Confirm with `git log -1 --stat`.
