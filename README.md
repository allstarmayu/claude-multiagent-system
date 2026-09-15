# Claude Multi-Agent Scaffold

A reusable starting point for building software projects with Claude Code. It packages the
machinery you stand up before application code: a reference library of engineering books,
a prompt-engineer subagent that drafts every other prompt artifact from that library, house
writing and commit standards, and the tools that grow the library. Copy it, point it at a
new product brief, and let the prompt-engineer build the agent roster your project needs.

CLAUDE.md is the orientation every Claude Code session reads first. This README is the
human setup and reuse guide.

The repo ships everything except the books themselves: `library/` is gitignored because it
holds copyrighted full text (see "The library"). A fresh clone has the tools and prompts and
adds books locally.

## Getting started

This is a Claude Code scaffold, not an application you launch with a single command. Running
it the first time means cloning it, restoring the reference library (which is not part of the
repo), and opening it in Claude Code.

1. Clone the repo and enter it:

   ```
   git clone https://github.com/allstarmayu/claude-multiagent-system.git
   cd claude-multiagent-system
   ```

2. Restore the library. The `library/` folder is gitignored (it holds copyrighted books), so a
   fresh clone ships the tools and prompts but no books. Either drop your existing `library/`
   folder into place, or build it from PDFs. This needs Python 3.10 or newer:

   ```
   pip install -r tools/requirements.txt
   python tools/convert_book.py path/to/book.pdf --out library
   python tools/build_index.py --library library
   ```

   `build_index.py` writes `library/INDEX.md`, the file every agent greps first. See "The
   library" below for what the tools do. The scaffold works without a library, but the
   prompt-engineer and the distill prompts depend on it, so restore it before using them.

3. Open the folder in Claude Code. Every session reads `CLAUDE.md` first for orientation. Run
   `/status` for a state check, or `/init-project` to stand up a new project.

4. Enable the house-style guard (recommended). A git pre-commit hook blocks em-dashes and
   AI-attribution in authored files:

   ```
   git config core.hooksPath .githooks
   ```

   A Claude Code hook in `.claude/settings.json` also flags violations as files are written; it
   needs Python and a POSIX shell on PATH (Git Bash on Windows), and you can remove that file to
   disable it.

## What is in here

| Path | Role |
|---|---|
| `.claude/agents/prompt-engineer.md` | Agent number one. Drafts and reviews every prompt artifact by grounding it in the library and the standards. |
| `.claude/commands/commit.md` | Drafts a Conventional Commits message for staged changes, per the git standard. |
| `.claude/commands/status.md` | Reports project state from CLAUDE.md and docs/roadmap.md against the repo. |
| `.claude/commands/init-project.md` | Guided flow to stand up a new project: brief, standards, CLAUDE.md, roster, roadmap. |
| `.claude/settings.json` | Claude Code hook that flags house-rule violations as files are written. |
| `docs/standards/writing-style.md` | Writing rules for the whole repo. |
| `docs/standards/git-commits.md` | Commit message format, types, scopes, and the 50/72 rule. |
| `docs/standards/prompt-evaluation.md` | How runtime prompts get eval sets and release gates. |
| `docs/standards/ai-safety-guardrails.md` | Baseline AI safety and guardrails standard, a template to adapt per project. |
| `docs/prompts/bootstrap-prompt-engineer.md` | The prompt that creates the prompt-engineer, kept for reference and for regenerating it. |
| `docs/prompts/distill-engineering-principles.md` | Distill an engineering standard from a book in the library. |
| `docs/prompts/distill-testing-standard.md` | Distill a testing standard from a book in the library. |
| `docs/prompts/distill-ai-engineering-standard.md` | Distill an AI-engineering standard from the AI Engineering book. |
| `docs/prompts/draft-prd.md` | Draft a product requirements document from the brief. |
| `docs/prompts/draft-adr.md` | Draft an architecture decision record for a significant decision. |
| `docs/adr/` | Architecture decision records: a convention and template; the project adds records. |
| `library/` | Full-text books as per-chapter markdown, INDEX.md, and prompt-engineering-refs/. Gitignored. |
| `tools/` | Convert book PDFs into the library, rebuild the index, and check house style. |
| `tests/` | Unit tests for the tools. Run with `python -m unittest discover -s tests`. |
| `.githooks/pre-commit` | Blocks em-dashes and AI-attribution in staged files. Enable with git config core.hooksPath .githooks. |

## The idea

Agents answer better when they retrieve from primary sources instead of relying on memory.
This scaffold turns a shelf of engineering books into a grep-able library, then has a single
prompt-engineer agent draft the rest of your project's agents and prompts by citing that
library and a small set of house standards. Standards are written once and referenced
everywhere, so guidance has a single home and cannot drift.

## Start a new project from this scaffold

The fast path is the `/init-project` command in Claude Code, which walks these steps and stops
for your review at each. To do it by hand:

1. Copy this repo to a new folder, or use it as a template, and initialize git.
2. Write your product brief at `docs/prd/brief.md`. It is the source of truth for product
   facts. See `docs/prd/README.md`.
3. Use the prompt-engineer to draft the agents, commands, and CLAUDE.md files your project
   needs. In Claude Code, ask it to create one artifact at a time; it grounds each in the
   library and the standards and stops for your review.
4. Distill the house standards you want from the library. For example, run the task in
   `docs/prompts/distill-engineering-principles.md` against a book, review the result, and
   save it under `docs/standards/`. The testing standard builds on the engineering one, so
   if you want both, run `distill-engineering-principles.md` before `distill-testing-standard.md`.

The prompt-engineer itself was created by the prompt in
`docs/prompts/bootstrap-prompt-engineer.md`. Keep that prompt as the record of how agent
number one is built, and rerun it if you ever want to regenerate the agent from scratch.

## The library

### Copyright

The library holds the full text of copyrighted books, kept as personal reading copies for
retrieval. It is gitignored and must never be published or committed. Keep your own copies
local. Only the tooling and the standards distilled from the books are shareable.

### Add a book

Requires Python 3.10 or newer and the one dependency:

```
pip install -r tools/requirements.txt
```

Convert one or more PDFs into per-chapter markdown, then rebuild the index:

```
python tools/convert_book.py path/to/book.pdf --out library
python tools/build_index.py --library library
python tools/build_index.py --check --library library
```

`convert_book.py` splits by embedded bookmarks, falls back to scanning for chapter headings,
and flags scanned or image-only PDFs so you can OCR them first. `build_index.py` assembles
`library/INDEX.md`, one line per chapter with keywords, which is the retrieval entry point
every agent greps first. The `--check` run validates the library and writes nothing: it exits
non-zero when a book has manifest/disk drift or duplicate chapters, so a bad conversion cannot
slip a broken or doubled index past you. Run it after adding a book, or in CI.

## Tests

The tools carry unit tests (stdlib `unittest`, no extra dependency). Run them from the repo
root:

```
python -m unittest discover -s tests
```

They cover the house-style checker, the `build_index.py --check` integrity gate, and the
converter's chapter-detection helpers. The converter tests skip automatically when `pymupdf`
is not installed.

## House rules

- No AI attribution anywhere in the repo or in commit messages.
- The em-dash character does not appear in any authored file. The library books are
  third-party text and are exempt.
- Commits follow `docs/standards/git-commits.md`. Never commit on the agent's initiative;
  the `/commit` command commits only when you run it and approve the message.

See `docs/standards/` for the full rules and `CLAUDE.md` for how a session should behave.

## License

MIT, see `LICENSE`. It covers this repo's own content: the tooling, standards, prompts, and
docs. It does not cover the gitignored `library/`, which is third-party copyrighted material
kept as personal copies and never published.
