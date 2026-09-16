---
description: Stand up a new project on this scaffold, one artifact at a time
argument-hint: [optional one-line description of the project]
---

## Task

Guide me through turning this scaffold into a working project. Optional one-line
idea from me: $ARGUMENTS

This is a guided, review-gated flow. Do the steps in order, produce one artifact at a
time, and stop for my review after each. Never commit; suggest a Conventional Commits
message per artifact per docs/standards/git-commits.md and let me run it. Delegate every
prompt artifact to the prompt-engineer subagent so it grounds each in the library and
the standards. Read docs/standards/writing-style.md first and hold it throughout.

## Steps

1. Product brief. Check for docs/prd/brief.md. If it is missing, help me write it: ask
   for the product's goal, users, scope, constraints, and any safety or compliance
   rules, and for the full stack so later roles can be specialized: languages,
   frameworks, platform (web, mobile, desktop, backend, data, or ML), CI/CD system, and
   deploy target. Draft docs/prd/brief.md from my answers. Mark anything I have not
   decided as an open question rather than inventing it. See docs/prd/README.md. Stop
   for review before moving on. The brief is the source of truth for every step after
   this.

2. Standards. Distill the house standards the project wants from the library, using the
   prompts in docs/prompts/. Offer, in this order: engineering principles
   (distill-engineering-principles.md), the testing standard (distill-testing-standard.md,
   which builds on the engineering one), the AI-engineering standard
   (distill-ai-engineering-standard.md) if the project ships model output, and the
   runtime prompt evaluation and AI safety guardrails standards
   (docs/standards/prompt-evaluation.md and ai-safety-guardrails.md, which are templates
   to adapt). Run one at a time and stop for review after each.

3. Project CLAUDE.md. Have the prompt-engineer draft a CLAUDE.md that orients a session
   to this project: what it is, its repo map, the working method, and the standing rules,
   referencing the standards rather than restating them. Keep it under 150 lines. Replace
   the scaffold's CLAUDE.md content with the project's. Stop for review.

4. Agent roster. Propose the subagents the project needs based on the brief, drawing
   from the templates in docs/agent-catalog/ (see its README for the role to standard to
   source mapping). List the chosen roles for my approval, keeping the active roster
   small. For each approved role, first distill any standard it references that is
   missing, using the matching distiller in docs/prompts/ (a dedicated one where it
   exists, otherwise distill-standard.md), and stop for review. Then have the
   prompt-engineer specialize the template, filling every [FILL IN] from docs/prd/ and
   reconciling every reference to another role against the approved roster: rewrite or
   drop any that names a role not on it, falling back to docs/prd/ or to me. Write each
   instance to .claude/agents/, one at a time, stopping for review after each. Record
   architecturally significant decisions as ADRs using docs/prompts/draft-adr.md.

5. Roadmap. Fill in docs/roadmap.md with the project's current status, done, open items,
   and next milestone, so /status has real state to report.

## Close

When the steps are done, summarize what was created, what is still an open question from
the brief, and the suggested commits I can run. Do not commit anything yourself.
