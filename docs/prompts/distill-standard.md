<task>
Create docs/standards/{STANDARD_FILE}: the distilled {DOMAIN} standard for this
repo, drawn from the transferable chapters of the source book(s) named below in
library/. Deliverable is that one file, presented for review. Do not commit.

This is the general distiller. Fill the placeholders below and run it for any domain
a role in docs/agent-catalog/ needs. The domain-specific distillers in this folder
(engineering, testing, ai-engineering) are worked examples of the same shape; prefer
this one for a new domain so the source book is never hardcoded.
</task>

<inputs>
Fill these from the project brief and the library index before running:
- {DOMAIN}: the standard's subject, for example "API design", "observability",
  "interface and visual design".
- {STANDARD_FILE}: the output filename, for example api-design.md.
- {SOURCES}: the exact chapter files to read, found by grepping library/INDEX.md for
  the domain keywords. Name each chapter file; never a whole book.
- {STACK}: the project's platform and stack, taken from docs/prd/ only.
</inputs>

<scope>
Read exactly the chapter files named in {SOURCES}, and nothing else from any book.
If {SOURCES} is empty, grep library/INDEX.md for the domain keywords first and
propose the matching chapters for approval before reading. Translate every principle
into its equivalent for {STACK}, and drop anything that only makes sense for a
platform this project does not target.
</scope>

<method>
Work one chapter at a time to keep context lean: read one chapter, append its
distilled points to a running draft, then move to the next. Do not hold multiple
chapters in context at once. After the last chapter, edit the draft down as a whole
for overlap and order.
</method>

<output_requirements>
- Under 200 lines total.
- Organized as numbered principles grouped into 4 or 5 sections.
- Each principle: one bold statement line, one or two sentences of meaning, and one
  line beginning "For this project:" applying it concretely using facts from
  docs/prd/ only.
- Each section ends with its citation: book title and the chapter files used.
- References sibling standards rather than restating them (for example, point at the
  engineering standard for security instead of repeating it).
- Follows docs/standards/writing-style.md. No em-dash character anywhere.
</output_requirements>

<process>
1. Read the project brief in docs/prd/ and docs/standards/writing-style.md first.
2. Confirm {SOURCES} against library/INDEX.md; propose chapters if none were given.
3. Distill per the method above.
4. Self-check: line count, citation per section, em-dash scan, no off-platform
   residue, every "For this project" line traceable to the brief.
5. Write docs/standards/{STANDARD_FILE}, show it with a short note on what you left
   out of the sources and why, and suggest this commit for me to run:
   docs(standards): add {DOMAIN} standard
</process>
