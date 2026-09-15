# Git Commit Standard

This project follows Conventional Commits with the 50/72 rule. This document
is the single source of truth; the /commit command and any future commitlint
config implement it.

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Header is mandatory. Scope is optional. Body and footer are optional but
expected for anything non-trivial.

## Types

- feat: a new feature
- fix: a bug fix
- docs: documentation only
- refactor: code change that neither fixes a bug nor adds a feature
- perf: code change that improves performance
- test: adding or correcting tests
- build: build system or external dependencies
- ci: CI configuration and scripts
- style: formatting only, no meaning change (kept separate so history
  tooling can filter these out)
- chore: maintenance that fits nothing above
- revert: starts with `revert: ` followed by the reverted commit's header;
  body says `This reverts commit <hash>.`

## Scopes

The area of the repo as a changelog reader would name it. Starter set for this
scaffold: agents, commands, tools, standards, prompts, library, docs, ci, deps.
Omit the scope when the change is repo-wide. Extend this list in this file as the
project grows, for example adding mobile, api, or web.

## Subject

- Imperative, present tense: "add" not "added" nor "adds". Test it as
  "This commit will <subject>."
- Lowercase first letter, no trailing period.
- Maximum 50 characters, not counting the `type(scope): ` prefix. Keep the
  whole header at or under 72 characters.

## Body

- Imperative, present tense, wrapped at 72 characters per line.
- Explain the motivation for the change and contrast with previous
  behavior. The diff shows what changed; the body says why.

## Footer

- Breaking changes start with `BREAKING CHANGE: ` followed by description
  and migration notes.
- Closed issues on their own line: `Closes #123` or `Closes #123, #245`.

## Atomicity

Make separate commits for logically separate changes. Never mix a
formatting pass with a logic change. If staged changes span unrelated
concerns, split them before committing.

## Project rules

- No AI attribution, co-author trailers, or generation notices in any
  commit message (writing-style.md rule 1).
- No em-dash character (writing-style.md rule 2).

## History hygiene (applies once PRs exist)

Rebase branches onto their target instead of merging the target in. Address
review feedback by amending the commit where the issue appears, not by
stacking "address review comments" commits; this keeps bisect and
changelog generation meaningful.

## Changelog

Releases generate a changelog with three sections: new features, bug
fixes, breaking changes, derived from commit headers. This is why header
discipline matters.

## Examples

```
docs(standards): adopt conventional commits

feat(tools): add chapter split fallback for unbookmarked pdfs

Books from some sources ship without a bookmark tree, which previously
produced a single unsplit file. Scan pages for chapter headings when
bookmarks are absent.

Closes #12
```
