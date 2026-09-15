<task>
Create docs/standards/engineering-principles.md: the distilled engineering
standard for this repo, drawn from the transferable chapters of Embedded
Software Design in library/embedded-software-design/. Deliverable is that one
file, presented for my review. Do not commit.
</task>

<scope>
Read exactly these chapter files, and nothing else from the book:
- ch01 (design philosophy)
- ch02 (architecture design)
- ch03 (secure application design)
- ch05 (design patterns)
- ch06 (quality, metrics, processes)
- ch08 (testing and TDD)
- ch10 (minimizing defects)
- ch12 (interfaces, contracts, assertions)

The book targets firmware. Translate every principle into its equivalent for
your project's stack, as stated in the project brief, and drop anything that
only makes sense for microcontrollers, RTOS, or hardware.
</scope>

<method>
Work chapter at a time to keep context lean: read one chapter, append its
distilled principles to a running draft, then move to the next. Do not hold
multiple chapters in context at once. After all eight, edit the draft down
as a whole for overlap and order.
</method>

<output_requirements>
- Under 200 lines total.
- Organized as numbered principles grouped into 4 or 5 sections (for
  example: design, architecture, quality, testing, contracts).
- Each principle: one bold statement line, one or two sentences of meaning,
  and one line beginning "For this project:" applying it concretely using
  facts from the project brief in docs/prd/ only.
- Each section ends with its citation: book title and chapter numbers used.
- Follows docs/standards/writing-style.md. No em-dash character anywhere.
</output_requirements>

<process>
1. Read the project brief in docs/prd/ and docs/standards/writing-style.md first.
2. Distill per the method above.
3. Self-check: line count, citation per section, em-dash scan, no firmware
   residue, every "For this project" line traceable to the brief.
4. Write the file, show it with a short note on what you deliberately left
   out of the book and why, and suggest this commit for me to run:
   docs(standards): add engineering principles
</process>
