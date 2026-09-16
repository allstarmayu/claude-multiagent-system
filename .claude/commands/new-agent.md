---
description: Draft one new subagent for a role you need, from the catalog blank template
argument-hint: [role name or one-line purpose]
---

## Task

Create one new Claude Code subagent for a role I need, grounded in the library and the
standards, from docs/agent-catalog/_TEMPLATE.md. Role or purpose from me: $ARGUMENTS

This is a guided, review-gated flow. Produce one artifact and stop for my review. Never
commit; suggest a Conventional Commits message per docs/standards/git-commits.md and let
me run it. Delegate the drafting to the prompt-engineer subagent so it grounds the agent
in the library and the standards. Read docs/standards/writing-style.md and
docs/agent-catalog/README.md first and hold them throughout.

## Steps

1. Scope the role. From $ARGUMENTS and docs/prd/, settle: the role's purpose, WHEN the
   harness should route to it, the minimal tools it needs, the model tier, the library
   topics it retrieves from, and the standards it must hold. Where it overlaps a role
   already on the roster, name the boundary. Ask me for anything docs/prd/ does not
   answer rather than inventing it. Stop for review.

2. Standards. If the role should hold a standard that does not exist yet, distill it
   first with the matching distiller in docs/prompts/ (a dedicated one where it exists,
   otherwise distill-standard.md), and stop for review.

3. Draft. Have the prompt-engineer draft the agent from docs/agent-catalog/_TEMPLATE.md:
   fill every section, set the tools, model tier, and read budget, reference the
   standards, reconcile any cross-role reference against the active roster, and hold the
   house rules (stack neutral, no AI attribution, no em-dash, under 150 lines). Write it
   to .claude/agents/<role>.md. Stop for review.

4. Reuse. If this is a role I will want on other projects, offer to add a specialized
   copy to docs/agent-catalog/ as a reusable template and list it in the README mapping.

## Close

Summarize the agent created, any open question from docs/prd/, and the suggested commit I
can run. Do not commit anything yourself.
