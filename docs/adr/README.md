# Architecture decision records

This folder holds the project's architecture decision records (ADRs): short documents
that capture an architecturally significant decision, why it was made, and what follows
from it. It is empty in the scaffold; the project adds records as it makes decisions.

Write an ADR only for a decision that is costly to reverse or that shapes the
construction of the services built after it. For smaller choices, a code comment or a
line in the roadmap is enough. The prompt in docs/prompts/draft-adr.md drafts one,
grounded in library/fundamentals-of-software-architecture/ch21-architectural-decisions.md.

## Convention

- Name files `NNNN-short-slug.md`, numbered sequentially from `0001`. Numbers are never
  reused, even for a superseded record.
- Status is one of: Proposed, Accepted, Superseded by ADR-NNNN, or Deprecated. A decision
  that changes gets a new ADR that supersedes the old one; the old record stays for
  history.
- Keep each record short and specific. Cite the brief, the standards, and the source
  chapter for each claim.

## Template

```
# ADR-NNNN: <decision title>

- Status: Proposed | Accepted | Superseded by ADR-NNNN
- Date: YYYY-MM-DD. Milestone: <milestone, if relevant>
- Related: <other ADRs this builds on or supersedes>

## Context

The forces at play: the constraints, the product facts, and the one or two forces that
actually decide it. Cite docs/prd/ and the standards.

## Decision

What was decided, stated plainly. Mark anything not yet chosen as PROPOSED.

## Consequences

- Positive: what this makes easier.
- Negative, accepted: the cost taken on knowingly.
- Failure mode and safe state: the risk the decision carries and the fallback if it
  is hit.

## Alternatives considered

Each real alternative, and why it was rejected.

## References

The brief sections, standards, and library chapters cited above.
```
