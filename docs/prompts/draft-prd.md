<task>
Create docs/prd/prd.md: the v1 product requirements document for this project,
drawn only from docs/prd/brief.md. Deliverable is that one file, presented for my
review. Do not commit.
</task>

<sources>
- docs/prd/brief.md is the only source of product facts.
- If docs/standards/ai-safety-guardrails.md exists, it governs every feature that
  ships model-generated output to a user; the relevant requirements must reference
  it rather than restating it.
- Do not consult the library for this task.
</sources>

<hard_rules>
- No scope invention. Every feature in the PRD must trace to the brief's MVP scope.
  Anything the brief lacks but the PRD seems to need (accounts, auth, onboarding,
  notifications, and whatever else you find) goes into an Open Questions section as a
  question for me, never as an invented requirement.
- New feature ideas that arise while writing go under a v2 candidates list, not into
  MVP scope.
- Follow CLAUDE.md and docs/standards/writing-style.md. No em-dash character anywhere.
</hard_rules>

<structure>
1. Overview: three sentences and a pointer to the brief. Do not restate it.
2. Personas: derive each user type from the brief only, noting which is primary.
3. User stories, grouped by MVP feature area. Each story: "As a ... I want ... so
   that ...", plus 2 to 5 testable acceptance criteria. Any feature that ships
   model-generated output must include acceptance criteria enforcing the safety
   guardrails (refusals, disclaimers, and any limits the brief sets).
4. Non-functional requirements: grounded in the brief only, with no invented numbers.
5. Out of scope: restate the brief's deferred list so no reader needs the brief open
   to know what v1 is not.
6. Success metrics: copy the metrics from the brief.
7. Open questions: every gap you found, each phrased as a decision for me with the
   options you see.
</structure>

<process>
1. Read the sources.
2. Draft to the structure above, under 300 lines.
3. Self-check: every requirement traces to the brief or is an open question; safety
   references present on every model-output feature when the guardrails standard
   exists; no invented product facts; no em-dash character; line count.
4. Present the file with a one-paragraph summary and the count of open questions,
   then suggest this commit for me to run:
   docs(prd): add prd v1
</process>
