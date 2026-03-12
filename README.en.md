[![中文](https://img.shields.io/badge/Language-%E4%B8%AD%E6%96%87-ff6b6b?style=for-the-badge)](./README.md)
[![English](https://img.shields.io/badge/Language-English-4c8bf5?style=for-the-badge)](./README.en.md)
[![Open Skill Spec](https://img.shields.io/badge/Page-Skill%20Spec-111111?style=for-the-badge)](./SKILL.md)

# Wisdom Council

An OpenClaw skill for historical-wisdom decision support.

Many difficult problems are not blocked by missing information.
They are blocked by missing judgment.

- Should I get divorced?
- Should I quit my job and start a company?
- My cofounder is becoming unreliable.
- I know what I should do, but I keep procrastinating.
- I care too much about what other people think.

These questions rarely have a clean answer, but they still require a decision.

The core of `Wisdom Council` is no longer “one shared template for ten names.”
Its main engine is now:

- a 100-person library of user-authored persona prompts
- a routing layer that classifies the problem first
- a retrieval layer that selects the best 10 figures from those 100
- an injection layer that fills each figure's original prompt with the user's dilemma
- a synthesis layer that lets them speak in sequence and then converge into an action plan

## How to Use This Skill in OpenClaw

This repository is built as an OpenClaw skill. The simplest way to use it is to explicitly invoke `$wisdom-council` inside an OpenClaw conversation.

### Minimal usage

```text
In OpenClaw, say:
Use $wisdom-council to help me decide whether I should quit my job and start a company.
```

### If you want to debug the 100-prompt library

```text
In OpenClaw, say:
Use $wisdom-council to analyze: how should I learn English?
Please show which figures were selected, the original prompt summary for each one, and how my dilemma was injected.
```

What matters here is:

- the system should call the original persona prompts you wrote, not regenerate them from a shared template
- normal mode should not dump the full internal prompts back to the user
- the visible output should stay readable while preserving each figure's judgment style
- if the result still feels templated, the routing or rendering has failed and should be rewritten

### Better prompt shape

Inside OpenClaw, the system works much better when you include:

- your current situation
- the real options in front of you
- what you are most afraid of losing
- what outcome you cannot accept
- the time window for the decision

## Output Structure

The default output order is:

1. Ten individual figure statements
2. A synthesized conclusion and action plan

## What Changed in This Version

- it is now “a 100-prompt persona library + dynamic routing + original prompt injection,” not “one shared template + ten renamed instances”
- the source of each figure's persona is the original prompt body
- the router is responsible for classification and selection, not persona rewriting
- the default output now emphasizes complementarity instead of forcing disagreements between figures
- the shared template remains only as a fallback for figures not yet covered by the 100-prompt library

## File Structure

- [`SKILL.md`](./SKILL.md): skill workflow and operating rules
- [`references/persona_prompt_library_100.md`](./references/persona_prompt_library_100.md): the original 100-person prompt library
- [`references/persona_prompt_index.json`](./references/persona_prompt_index.json): search index for the prompt library
- [`scripts/persona_prompt_library.py`](./scripts/persona_prompt_library.py): lookup and extraction tooling for the original prompts
- [`references/taxonomy.json`](./references/taxonomy.json): domains, conflicts, and rules
- [`references/router_prompt.md`](./references/router_prompt.md): classification and selection logic
- [`references/renderer_prompt.md`](./references/renderer_prompt.md): persona rendering and synthesis logic
- [`references/eval_cases.json`](./references/eval_cases.json): test cases

## Boundaries

The system does not:

- fabricate historical quotes,
- reframe obvious harm as relationship repair,
- treat legal, medical, tax, or investment questions as purely wisdom questions,
- silently overwrite existing persona prompts with a shared template,
- end with abstract encouragement.
