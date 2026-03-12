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
- an independent-call layer that runs those 10 figures separately
- a final synthesis layer that runs once more as an 11th separate call

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
Please show which figures were selected, the original prompt summary for each one, the independent-call runbook, and how my dilemma was injected.
```

What matters here is:

- the system should call the original persona prompts you wrote, not regenerate them from a shared template
- the 10 sages must be run as 10 separate generations
- the synthesis must be a separate 11th generation
- normal mode should not dump the full internal prompts back to the user

## Output Structure

The default output order is:

1. Ten individual figure statements
2. A synthesized conclusion and action plan

## What Changed in This Version

- it is now “a 100-prompt persona library + dynamic routing + original prompt injection + 10 independent calls + 1 synthesis call”
- the source of each figure's persona is the original prompt body
- the router is responsible for classification and selection, not persona rewriting
- the default output emphasizes independent persona generation rather than a shared group voice
- the shared template remains only as a fallback for figures not yet covered by the 100-prompt library

## File Structure

- [`SKILL.md`](./SKILL.md): skill workflow and operating rules
- [`references/persona_prompt_library_100.md`](./references/persona_prompt_library_100.md): the original 100-person prompt library
- [`references/persona_prompt_index.json`](./references/persona_prompt_index.json): search index for the prompt library
- [`scripts/persona_prompt_library.py`](./scripts/persona_prompt_library.py): lookup and extraction tooling for the original prompts
- [`scripts/build_independent_council_runbook.py`](./scripts/build_independent_council_runbook.py): generates 10 independent sage calls plus 1 synthesis call
- [`references/synthesis_prompt.md`](./references/synthesis_prompt.md): prompt for the separate synthesis pass
- [`references/taxonomy.json`](./references/taxonomy.json): domains, conflicts, and rules
- [`references/router_prompt.md`](./references/router_prompt.md): classification and selection logic
- [`references/renderer_prompt.md`](./references/renderer_prompt.md): independent persona rendering and synthesis rules
- [`references/eval_cases.json`](./references/eval_cases.json): test cases

## Boundaries

The system does not:

- fabricate historical quotes,
- reframe obvious harm as relationship repair,
- treat legal, medical, tax, or investment questions as purely wisdom questions,
- silently overwrite existing persona prompts with a shared template,
- ask one response to play all 10 sages at once,
- end with abstract encouragement.
