<task>
Create this project's first Claude Code subagent: a prompt engineer responsible for
drafting and maintaining every prompt artifact in this repository, including CLAUDE.md
and AGENTS.md files, subagent definitions in .claude/agents/, and slash commands in
.claude/commands/. When an ai-engineer role is on the roster, the product's own runtime
prompts belong to it; otherwise the prompt-engineer covers them too.

Deliverable: exactly one new file at .claude/agents/prompt-engineer.md, then stop for
my review. Do not create any other agents or files, and do not run git commands.
</task>

<context>
This is a new project repository, currently pre-code. We are building agent
infrastructure before application code. The prompt-engineer is agent number one and
will draft the rest of the agent roster, so its quality compounds into everything that
follows.
</context>

<reference_material>
Read in this order and read nothing else:

1. The short technique refs in library/prompt-engineering-refs/: core_techniques,
   advanced_techniques, common_mistakes, prompt_templates, and claude_4_best_practices.
2. library/prompt-engineering-for-llms/manifest.json, then choose and read AT MOST
   three chapters, preferring those covering instruction writing, prompt structure
   and content assembly, and evaluation or testing of prompts. Never read the whole
   book; the library protocol is index first, matching chapters only.

The technique refs above are model-agnostic. The folder also holds current-model
behavior guides (claude_prompting_best_practices and prompting_claude_<model>) for the
finished agent to grep as needed; you do not need to read them now. Where an older ref
names "Claude 4.x" or "Opus 4", the technique still applies; the current-model guides
carry model-specific behavior.
</reference_material>

<output_requirements>
The file must be a valid Claude Code subagent definition:

- YAML frontmatter with:
  - name: prompt-engineer
  - description: written in third person for automatic delegation, stating clearly
    WHEN to use it (any time a prompt, agent definition, CLAUDE.md, AGENTS.md, or slash
    command is created, reviewed, or revised, plus the product's own runtime prompts when
    no ai-engineer role owns them)
  - tools: Read, Grep, Glob, Write, Edit
- Body: the agent's system prompt, under 150 lines, containing:
  - Role and scope. It drafts and reviews prompt artifacts; it never invents project
    facts, pulling them instead from docs/prd/ and docs/standards/ and asking when
    a needed fact does not exist yet.
  - Working method: gather inputs, draft, self-review against
    library/prompt-engineering-refs/common_mistakes.md, then present the file for
    human review. It never commits on its own; it suggests a Conventional Commits
    message for each artifact instead.
  - Retrieval protocol: grep library/INDEX.md first, read only matching chapter
    files, and consult library/prompt-engineering-refs/ when choosing techniques.
  - A distilled quality bar drawn from the refs: explicit instructions, motivation
    and context included, XML structure for Claude-targeted artifacts, examples only
    when they earn their space and always aligned with instructions, output format
    specified, minimum necessary context, and test cases defined for any runtime
    prompt. At most one short example in the whole file.
  - Project rules it must enforce in every artifact it writes or reviews: no AI
    attribution, co-author trailers, or generation notices anywhere; no em-dash
    characters in any file; instruction files stay short and reference
    docs/standards/ rather than restating them.
</output_requirements>

<hard_rules>
- ASCII punctuation only. The em-dash character must not appear anywhere in the file.
- No AI attribution of any kind, in file contents or in suggested commit messages.
- Modify nothing except creating .claude/agents/prompt-engineer.md.
</hard_rules>

<process>
1. Read the reference material exactly as scoped above.
2. Draft the agent file.
3. Self-check the draft against common_mistakes.md and the production readiness
   checklist in claude_4_best_practices.md. Scan the draft for em-dash characters
   and remove any found. Fix all violations before writing.
4. Write .claude/agents/prompt-engineer.md.
5. Reply with: the file contents, a five-line summary of your design choices, which
   book chapters you selected and why, and this suggested commit for me to run
   myself: feat(agents): add prompt-engineer subagent
</process>
