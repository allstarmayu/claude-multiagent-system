# Product requirements

This folder holds the product facts for your project. It ships with only this README; you
fill it in per project.

Start with `brief.md`: the single source of truth for scope, users, stack, and
constraints. The prompt-engineer and the distill prompts in `docs/prompts/` read product
facts from here and never invent them, so the quality of everything they produce depends
on this brief.

Add more files as the project grows, for example `prd.md` for detailed requirements. Keep
each file to facts that are decided; mark anything unresolved so agents flag it rather than
guessing.
