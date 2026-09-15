<task>
Create docs/standards/testing.md: the testing standard for this repo,
distilled from Unit Testing: Principles, Practices, and Patterns in the
library. Deliverable is that one file, presented for my review. Do not
commit.
</task>

<scope>
Resolve the book's exact folder by grepping library/INDEX.md for its title,
then read its manifest.json. This book is split into four PART files, not
per-chapter files. Read only the parts that carry the topics below, and
nothing else from the book:
- Part 1 (the bigger picture): the goal of unit testing.
- Part 2 (making your tests work for you): the four pillars of a good test,
  styles of unit testing, and mocks and test fragility (observable behavior
  versus implementation details). This part is large; read it in one focused
  pass.
- Part 3 (integration testing): integration testing and testing the database.
- Part 4 (unit testing anti-patterns): the anti-patterns to avoid.

The book's examples are C# and .NET. Translate every principle and
convention into your project's stack, as stated in the project brief. Drop
anything .NET-specific.
</scope>

<prerequisite>
This standard builds on docs/standards/engineering-principles.md, the output of
docs/prompts/distill-engineering-principles.md. Run that prompt first. If the
file does not exist yet, say so and stop, or proceed without the cross-reference
and flag it for me.
</prerequisite>

<method>
Work one part at a time: read one part file, append its distilled points to a
running draft, then move on. Do not hold multiple parts in context at once.
After the last part, edit the whole draft for overlap and order.
</method>

<output_requirements>
- Under 150 lines, two parts.
- Part 1, principles: numbered, each with a bold statement line, one or two
  sentences of meaning, and a "For this project:" line grounded only in facts
  from the project brief and PRD in docs/prd/. Do not repeat principles
  already in docs/standards/engineering-principles.md; reference them.
- Part 2, conventions: the concrete choices this project will follow. What
  gets a unit test versus an integration test, the mocking policy, the
  database testing approach, and test naming and placement. The test runner
  is not yet decided: propose one with one alternative. Prefix every
  convention that involves a choice I have not made with "PROPOSED:" so I
  can approve or change each in review.
- Each part ends with its citation: book title and chapter numbers used.
- Follows docs/standards/writing-style.md. No em-dash character anywhere.
</output_requirements>

<process>
1. Read the project brief and PRD in docs/prd/, docs/standards/writing-style.md,
   and docs/standards/engineering-principles.md first.
2. Distill per the method above.
3. Self-check: line count, PROPOSED marker on every unmade choice, citations
   present, no C# or .NET residue, no invented product facts, em-dash scan.
4. Write the file, present it with a short note on what you deliberately
   left out of the book and why, and suggest this commit for me to run:
   docs(standards): add testing standard
</process>
