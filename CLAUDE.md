# Claude Multi-Agent Scaffold

Orientation for every Claude Code session and subagent that opens this repo. Read this
file first, then read the specific files it points to just in time. Do not pull whole
books or the whole repo into context up front. Cite what you read.

<what_this_is>
This is a reusable scaffold for building software projects with Claude Code. It is not an
application. It provides the machinery you stand up before writing application code:

- A reference library of full-text books converted to per-chapter markdown, with an index
  agents grep first (library/INDEX.md).
- A prompt-engineer subagent that drafts and maintains every other prompt artifact in the
  repo (agents, commands, CLAUDE.md files, runtime prompts) by grounding each one in the
  library and the house standards.
- House standards that every artifact references rather than restates.
- Tools that convert new book PDFs into the library and rebuild the index.

Copy this repo as the starting point for a new project, add your product brief under
docs/prd/, then use the prompt-engineer to build the agent roster your project needs.
README.md has the full setup and reuse guide.
</what_this_is>

## Repo map

Read a file only when your task needs it.

- .claude/agents/ - subagent definitions. prompt-engineer.md ships here; the roster grows here.
- .claude/commands/ - slash commands: commit.md, status.md, and init-project.md (stand up a new project).
- .claude/settings.json - a Claude Code hook that flags house-rule violations as files are written.
- docs/prd/ - product requirements for your project. Ships with only a README; you add brief.md here.
- docs/adr/ - architecture decision records. Ships with only a README and template; the project adds records.
- docs/prompts/ - reusable task prompts: bootstrap the prompt-engineer, distill standards from books, draft a PRD or an ADR.
- docs/standards/ - house standards every artifact references, not restates.
- docs/roadmap.md - volatile project state: current status, done, open items, next milestone. The /status command reads it.
- library/ - full-text reference books as markdown, INDEX.md, and the short prompt-engineering-refs/. Gitignored.
- tools/ - scripts: build the index (build_index.py), convert PDFs (convert_book.py), check house style (check_house_style.py).
- .githooks/ - a pre-commit hook that blocks house-rule violations. Enable with: git config core.hooksPath .githooks

<working_method>
Project facts come only from docs/prd/ and docs/standards/. Never invent product goals,
user types, data models, naming, or house rules. When a needed fact is not written down
yet, stop and ask, or state the assumption plainly and flag it for confirmation. A
confident guess becomes a defect in every artifact that follows.

Library retrieval is INDEX-first:
1. Grep library/INDEX.md for topic keywords to find the relevant chapter.
2. Read only the matching chapter file or files. Never read a whole book.
3. Cite what you read (file and chapter) in your notes to the human.

The short refs in library/prompt-engineering-refs/ guide prompt-artifact technique
choices. When a lookup answers a real project question, propose promoting the answer into
docs/standards/ with its citation, so each standard keeps one home.
</working_method>

<using_this_scaffold>
Run /init-project to walk the whole flow interactively, or do it by hand, in order:
1. Write your product brief at docs/prd/brief.md. It is the source of truth for product facts.
2. The prompt-engineer already exists (.claude/agents/prompt-engineer.md). Use it to draft the
   agents, commands, and CLAUDE.md files your project needs, one at a time.
3. Distill house standards from the library with the prompts in docs/prompts/ (engineering,
   testing, and ai-engineering), then review and keep them in docs/standards/. Two standards
   ship as ready-to-adapt templates: prompt-evaluation.md and ai-safety-guardrails.md.
4. Add more books with tools/convert_book.py and rebuild the index with tools/build_index.py.
See README.md for the commands.
</using_this_scaffold>

<standing_rules>
These bind every artifact in the repo. They live in docs/standards/ and are referenced,
not restated.

- docs/standards/writing-style.md governs writing across the repo: code, docs, commits,
  prompts, agent definitions, and user-facing copy.
- No AI attribution of any kind, anywhere in the repo or in a commit message you suggest
  (writing-style rule 1).
- The em-dash character (U+2014) must not appear in any authored file (writing-style rule 2).
  Scan every draft and remove any before presenting it. The library books are third-party
  reference text and are exempt.
- docs/standards/git-commits.md is the source of truth for commit messages: format, types,
  scopes, and the 50/72 rule (writing-style rule 3). Follow it; do not restate it.
- Instruction files (CLAUDE.md, agent definitions, slash commands) stay under 150 lines and
  reference standards instead of restating them (writing-style rule 5).
- Never commit on your own initiative. Suggest one Conventional Commits message per artifact
  and stop for review. The /commit command is the human-invoked path.
- The em-dash and AI-attribution rules are enforced two ways: a git pre-commit hook
  (.githooks/pre-commit, enabled with git config core.hooksPath .githooks) and a Claude Code hook
  (.claude/settings.json) that flags violations as files are written. Both call
  tools/check_house_style.py. The other rules here are held by review.
</standing_rules>

## Agent roster

Agent definitions live in .claude/agents/, each drafted by the prompt-engineer and bound by
this file and docs/standards/. The prompt-engineer is agent number one: it drafts, reviews,
and revises every prompt artifact in the repo, including the rest of the roster. Slash
commands live in .claude/commands/.
