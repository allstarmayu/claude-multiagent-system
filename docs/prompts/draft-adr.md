<task>
Create the next architecture decision record under docs/adr/ for a decision I will
name. Deliverable is that one file, numbered as the next in sequence, presented for
my review. Do not commit.
</task>

<scope>
Write an ADR only for an architecturally significant decision: one that is costly to
reverse or shapes the construction of the services built after it. For anything
smaller, say so and stop rather than writing an ADR. Ground the definition of
significance and the "last responsible moment" framing in
library/fundamentals-of-software-architecture/ch21-architectural-decisions.md; read
that chapter and nothing else from the library.

Product and stack facts come only from docs/prd/ and existing docs/adr/ records. Do
not invent them. Any choice I have not made is marked PROPOSED, not guessed.
</scope>

<output_requirements>
- File path docs/adr/NNNN-short-slug.md, where NNNN is the next number after the
  highest existing ADR (or 0001 if none), and the slug names the decision.
- Follow the template in docs/adr/README.md: Status, Date, Related; Context; Decision;
  Consequences (positive, negative accepted, and failure mode with the safe state);
  Alternatives considered; References.
- Cite the brief, the engineering principles, and the architecture chapter where each
  claim comes from. Keep it under 120 lines.
- Follows docs/standards/writing-style.md. No em-dash character anywhere.
</output_requirements>

<process>
1. Ask me for the decision and its context if I have not stated them.
2. Read ch21-architectural-decisions.md, the relevant docs/prd/ facts, and any related
   ADRs.
3. Confirm the decision is architecturally significant; if not, stop and say so.
4. Draft to the template, marking every unmade choice PROPOSED.
5. Self-check: correct next number, template sections present, citations present, no
   invented facts, no em-dash character, line count.
6. Present the file and suggest this commit for me to run, filling in the slug:
   docs(adr): add ADR-NNNN <slug>
</process>
