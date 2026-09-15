# Writing Style Standard

Applies to everything in this repository: code comments, documentation,
commit messages, prompts, agent definitions, and user-facing copy.

## Rules

1. No AI attribution of any kind: no co-author trailers, no "generated with"
   notices, no model names in commits, comments, docs, or copy.
2. The em-dash character (U+2014) must not appear in any authored file. Use commas,
   colons, parentheses, or hyphens instead. Third-party reference text under
   library/ is exempt, since it is copied verbatim and not authored here.
3. Commit messages follow Conventional Commits and the 50/72 rule. See
   docs/standards/git-commits.md.
4. Documentation uses short, direct sentences, American English, and sentence
   case headings.
5. Instruction files (CLAUDE.md, agent definitions, slash commands) stay under
   150 lines and reference standards documents instead of restating them.
6. User-facing copy uses plain language and honors any domain safety or
   compliance rules the project defines in docs/standards/ (for example a safety
   policy), once such a document exists.

## Enforcement

A pre-commit hook will scan staged files for rule 1 phrases and the rule 2
character. Until the hook exists, reviewers check manually.
