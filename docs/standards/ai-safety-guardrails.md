# AI safety and guardrails standard

A baseline safety and guardrails standard for any product that ships
model-generated output to users. It is a template: the structure and the patterns
are ready to use, and the bracketed [FILL IN] items are the domain-specific parts
your project decides from its brief. It is the safety policy that
docs/standards/writing-style.md rule 6 points user-facing copy to, and the canonical
home for the product's disclaimer text. It follows that standard.

Adapt it per project, then treat the result as binding. Where your brief settles a
value, state it here; mark anything finalized at build time under "Deferred to
implementation" rather than guessing.

## Scope and precedence

- These rules bind the model layer, any deterministic or authoritative logic, and
  every screen or export that shows model-generated output to a user.
- Ground each rule in your project brief. Cite it; do not restate it from memory.
- These are among the highest-risk paths in the product, so they are covered by
  tests and evals first (see docs/standards/prompt-evaluation.md).
- Weakening any rule here is a project-owner decision. Surface it for confirmation;
  never relax a guard locally.

## Domain limits

[FILL IN] The concrete limits your domain requires, each traceable to the brief and
each marked for re-check before it ships (for example clinical values against
current guidance, legal values against applicable law). Common examples:

- Eligibility or age gating, if your product has a minimum-age or eligibility rule.
- Hard floors or caps on any value where an unsafe setting could harm a user.
- Categories the product refuses to act on at all.

Delete this section only if your product genuinely has no domain limits.

## Authoritative values versus model output

Keep the model away from anything that must be correct. A deterministic or
authoritative source owns critical values; the model assembles, explains, and
adapts around them (this mirrors the separation-of-concerns principle in your
engineering standard).

The model layer may:
- Assemble, summarize, explain, and adapt output in plain language.
- Ask clarifying questions and route the user to the right next step.

The model layer may not:
- Produce or estimate a value that must be correct (prices, dosages, legal or
  financial figures, safety-critical numbers). Those come from authoritative
  computation or a trusted data source, never from the model.
- Make professional claims it is not qualified to make: medical, legal, financial,
  or other regulated advice. [FILL IN] which of these apply to your product.
- Override or restate a safety guard in a way a prompt can drift from. Every guard
  is a runtime check in code; the model runs behind it.

## Refusal cases and copy patterns

Each case lists a trigger, the action, and a reusable copy pattern with
{placeholders} the caller fills. Keep copy plain, non-judgmental, and free of any
claim the product is not qualified to make. [FILL IN] the cases your product needs;
these are common starting points.

**Out-of-scope professional advice**
- Trigger: a request for diagnosis, treatment, legal, or financial advice beyond
  the product's scope.
- Action: decline that part, restate scope, point to a qualified professional.
- Pattern: "I can't give {advice_type} advice. For that, please talk with a
  qualified professional. I can still help you {in_scope_action}."

**Ineligibility or gating**
- Trigger: the user does not meet an eligibility or age requirement.
- Action: gate access; do not create the account or the gated output.
- Pattern: "{product} is for {eligibility_rule}, so we can't set this up yet."

**Harmful or disallowed request**
- Trigger: a request that would produce harm or violate the product's use policy.
- Action: refuse plainly, without moralizing, and offer a safe alternative if one
  exists.
- Pattern: "I can't help with that. If you meant {safe_alternative}, I can help
  with that instead."

## Disclaimer copy

The canonical disclaimer text. Other copy links to or quotes it rather than
paraphrasing, so the wording has one home.

- Canonical text: [FILL IN] a plain-language statement of what the product is and
  is not. Template: "{product} offers general {domain} information, not
  professional advice. It does not replace a qualified professional. Talk with one
  before making {high_stakes} decisions."
- Where it applies: [FILL IN] onboarding, first generated output, any exported or
  shared report, and any screen that shows model-generated guidance.

## Data handling

Apply your engineering standard's security and least-privilege principles to user
data.

- Classify sensitive user data and protect it as such.
- Comply with applicable data-protection law (for example GDPR and CCPA): support
  data export and complete account deletion within the required window. [FILL IN]
  the laws and windows that apply to you; verify at implementation.
- Never use sensitive user data for advertising.
- Least privilege and privacy-first: grant each part the minimum access it needs,
  and default any social or sharing feature to private and off.

## Deferred to implementation

[FILL IN] The items you intentionally finalize later rather than leaving open, each
with its owner. Common examples: a detection ruleset tuned against current
guidance, or an external resource (helpline, policy URL) verified as current at
build time rather than hardcoded where it can go stale.
