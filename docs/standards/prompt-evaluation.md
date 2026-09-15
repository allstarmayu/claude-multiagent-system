# Runtime prompt evaluation standard

How this repo evaluates the prompts it ships to a model. Prompts sent to a model in
production are non-deterministic, so they are evaluated against a fixed set of cases,
not eyeballed once and trusted. This operationalizes the evaluation principles in
AI Engineering (Huyen) for runtime prompts; if docs/standards/ai-engineering.md
exists it holds the broader system-level methodology, and this file is its concrete
convention for prompt-level evals. Follows docs/standards/writing-style.md.

## What gets an eval set

- Every runtime prompt: a prompt the product sends to a model to produce output a
  user sees or the system acts on.
- Not the authoring prompts in docs/prompts/ or agent definitions; those are
  reviewed by a human, not run against users.

## What an eval set contains

Each runtime prompt has an eval set covering, at minimum:

- Happy path: the common inputs the prompt exists to serve.
- Edge cases: empty, oversized, ambiguous, or adversarial inputs.
- Failure modes: inputs that must be refused or that have no valid answer, so the
  prompt is measured on what it must not do as well as what it must.
- Safety cases: for any prompt covered by docs/standards/ai-safety-guardrails.md,
  one case per refusal rule and disclaimer that applies to it.

## How cases are judged

- Prefer deterministic checks: exact match, a required field, valid JSON, a value in
  range, a required refusal. These are cheap, stable, and trustworthy.
- Use a rubric or a model-as-judge only for genuinely open-ended output. A judge is
  itself a prompt: give it explicit criteria and validate it against human-labeled
  examples before trusting it (AI Engineering, evaluation chapters).
- Record the score and the judgment method with each result, not just pass or fail.

## Where evals live

PROPOSED (choose per project and record the choice here): store eval sets under
`evals/<prompt-name>/` next to the prompt they cover, with the cases and their
expected criteria in a format your test runner reads. Keep them in source control.

## Release gate and versioning

- A runtime prompt changes only behind its eval set. A change that regresses the set
  does not ship.
- Version runtime prompts, and record which prompt version each eval run covered, so
  a regression can be traced to the change that caused it.

Source: AI Engineering (Huyen), chapters 3 and 4; Prompt Engineering for LLMs, the
chapter on evaluating LLM applications.
