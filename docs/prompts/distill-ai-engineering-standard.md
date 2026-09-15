<task>
Create docs/standards/ai-engineering.md: the distilled AI-engineering standard
for this repo, drawn from the transferable chapters of AI Engineering (Chip
Huyen) in library/ai-engineering-for-true-epub/. Deliverable is that one file,
presented for my review. Do not commit.
</task>

<scope>
This book is split per chapter. Resolve each chapter's file by grepping
library/INDEX.md for its title, and read only these chapters, nothing else:
- Chapter 1 (introduction to building AI applications with foundation models):
  use-case selection, build versus buy, planning.
- Chapter 3 (evaluation methodology) and Chapter 4 (evaluate AI systems): the core
  of the standard.
- Chapter 5 (prompt engineering).
- Chapter 6 (RAG and agents).
- Chapter 9 (inference optimization): latency, cost, and caching.
- Chapter 10 (AI engineering architecture and user feedback).

Read Chapter 2 (understanding foundation models) only if your project must select
or compare models, and Chapter 7 (finetuning) and Chapter 8 (dataset engineering)
only if your project finetunes. Otherwise skip them.

The book covers building applications on foundation models. Translate every point
into your project's stack, as stated in the project brief, and drop material that
only applies to training or serving your own models when your project uses hosted
model APIs.
</scope>

<method>
Work one chapter at a time to keep context lean: read one chapter, append its
distilled principles to a running draft, then move on. Do not hold multiple
chapters in context at once. After the last chapter, edit the draft down as a
whole for overlap and order.
</method>

<output_requirements>
- Under 200 lines total.
- Organized as numbered principles grouped into sections, for example: foundations
  and planning; evaluation; prompting and context; retrieval and agents; serving
  (latency, cost, reliability); architecture and feedback.
- Each principle: one bold statement line, one or two sentences of meaning, and one
  line beginning "For this project:" applying it concretely using facts from the
  project brief in docs/prd/ only.
- Where the project ships model-generated guidance, the evaluation and prompting
  sections must reference docs/standards/prompt-evaluation.md and, if it exists,
  docs/standards/ai-safety-guardrails.md, rather than restating them.
- Each section ends with its citation: book title and chapter numbers used.
- Follows docs/standards/writing-style.md. No em-dash character anywhere.
</output_requirements>

<process>
1. Read the project brief in docs/prd/ and docs/standards/writing-style.md first.
2. Distill per the method above.
3. Self-check: line count, citation per section, em-dash scan, no training-only
   residue when the project uses hosted models, every "For this project" line
   traceable to the brief.
4. Write the file, show it with a short note on what you deliberately left out of
   the book and why, and suggest this commit for me to run:
   docs(standards): add ai engineering standard
</process>
