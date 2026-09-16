# Agent catalog

Reusable role templates for the project team, kept inert. Each file here is a
subagent definition the prompt-engineer specializes for one project and, only if the
project needs the role, writes to `.claude/agents/`. Nothing in this folder is an
active agent, so nothing here is loaded by a running session until it is instantiated.
The seven named roles are a starting set; `_TEMPLATE.md` plus the `/new-agent` command
create any role beyond them.

## Why templates and not active agents

Every file under `.claude/agents/` has its `description` loaded into every session so
the harness can route to it. A large standing roster is a permanent context tax on
every task, even a one-line fix. The catalog keeps the full team available without
paying for it up front: `/init-project` instantiates only the two to four roles a
brief actually needs, and the rest stay here as text.

## Template contract

Every catalog entry follows the same shape so instances stay small and consistent:

- **Stack neutral**: names no language, framework, CI system, or vendor. Every stack,
  platform, and tooling fact comes from `docs/prd/` at instantiation, so one template
  serves any project. The library sources it cites are principle-level and language
  agnostic.
- **Frontmatter** with `name`, a third-person `description` that states when to route
  to it, a minimal `tools` list, and a `model` tier (Haiku for mechanical roles,
  Sonnet for build and design roles, Opus only where deep reasoning earns it).
- **A read budget**: name the primary library chapters and cap reading at three per
  task. Grep `library/INDEX.md` first; never read a whole book.
- **Standards by reference**: point at the `docs/standards/` files the role must hold,
  and never restate a rule that lives in one.
- **Bracketed [FILL IN] items**: the project facts the prompt-engineer fills from
  `docs/prd/` at instantiation.
- **Cross-role references** name other roles only as a default. At instantiation the
  prompt-engineer reconciles each against the approved roster and rewrites or drops any
  role not on it, so a small roster never ships an agent that depends on a teammate that
  does not exist.

## Role to standard to source mapping

The library already carries the source books for most roles. A standard not yet in
`docs/standards/` is distilled first with the matching distiller in `docs/prompts/` (a
dedicated one where it exists, otherwise `distill-standard.md`).

| Role | Standards it holds | Source in `library/` |
|---|---|---|
| product-manager | brief and roadmap only | none required |
| solution-architect | api-design, systems-design, engineering-principles | patterns-for-api-design, designing-data-intensive-applications |
| cloud-engineer | observability, engineering-principles | observability-engineering |
| ux-designer | interface-design | refactoring-ui |
| fullstack-engineer | engineering-principles, testing, api-design | the-pragmatic-programmer, unit-testing-principles, patterns-for-api-design |
| ml-engineer | systems-design, testing (+ ai-safety-guardrails, prompt-evaluation if output ships) | designing-data-intensive-applications, unit-testing-principles |
| ai-engineer | ai-engineering, prompt-evaluation, ai-safety-guardrails | AI engineering book (add), plus existing standards |

## How to use it

1. `/init-project` proposes the roles a brief needs and lists them for approval.
2. For each approved role, distill any missing standard from the mapping above with the
   matching distiller in `docs/prompts/` (a dedicated one where it exists, otherwise
   `distill-standard.md`), and stop for review.
3. The prompt-engineer specializes the template, filling every [FILL IN] from
   `docs/prd/`, and writes the instance to `.claude/agents/`.
4. Keep the active roster small. Leave a role in the catalog until the project needs it.

## Roster in this catalog

- `product-manager.md`
- `solution-architect.md`
- `cloud-engineer.md`
- `ux-designer.md`
- `fullstack-engineer.md`
- `ml-engineer.md`
- `ai-engineer.md`

These seven are a starter set, not a fixed roster. To create any role they do not
cover, copy `_TEMPLATE.md` (the blank these seven specialize) and fill it, or run
`/new-agent`, which walks that template with the prompt-engineer and grounds the result
in the library and the standards. List a reusable new role in the mapping table above.
