[![中文](https://img.shields.io/badge/Language-%E4%B8%AD%E6%96%87-ff6b6b?style=for-the-badge)](./README.md)
[![English](https://img.shields.io/badge/Language-English-4c8bf5?style=for-the-badge)](./README.en.md)
[![Open Skill Spec](https://img.shields.io/badge/Page-Skill%20Spec-111111?style=for-the-badge)](./SKILL.md)

# Wisdom Council

An OpenClaw skill for historical-wisdom decision support.

Many hard problems are not blocked by missing information.
They are blocked by missing judgment.

- Should I get divorced?
- Should I quit my job and start a company?
- My cofounder is becoming unreliable.
- I know what I should do, but I keep procrastinating.
- I care too much about what other people think.

These questions rarely have a clean answer, but they still require a decision.

The core of `Wisdom Council` is not “listing ten names.”
It instantiates one shared persona prompt template into ten historical figures by swapping in the figure's name, era, knowledge system, voice, and core thought, then lets them speak, debate, and only then produce an action plan.

## How to Use This Skill in OpenClaw

This repository is built as an OpenClaw skill. The simplest way to use it is to explicitly invoke `$wisdom-council` inside an OpenClaw conversation.

### Minimal usage

```text
In OpenClaw, say:
Use $wisdom-council to help me decide whether I should quit my job and start a company.
```

### If you want to debug the 10 sage templates

```text
In OpenClaw, say:
Use $wisdom-council to analyze: how can I improve my work efficiency?
Please show the persona-prompt summary for each selected figure, how the shared template is instantiated, their individual statements, and their roundtable debate.
```

The important part is:

- the internal reasoning should truly follow each figure's persona prompt
- the final wording should not dump that prompt back at the user
- what the user sees should be clear modern language that still carries that figure's distinct judgment style
- if the result feels obscure or templated, the rendering has failed and should be rewritten

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
2. Roundtable debate
3. Why these ten figures were selected
4. Action plan

## What Changed in This Version

- it is now “one shared template + 10 auto-instantiated sage prompts,” not 10 loose perspective labels

- figures are no longer treated as abstract lens labels
- each figure now has its own `persona_instruction`
- each figure must speak independently first
- debate is mandatory, not optional decoration
- the ending is a single action-plan synthesis instead of multiple summary blocks
- internal persona reasoning is separated from external user-facing rendering
- distinctiveness should come from priorities and judgment style, not from obscure wording

## File Structure

- [`SKILL.md`](./SKILL.md): skill workflow and operating rules
- [`references/sages.json`](./references/sages.json): structured sage pool plus persona prompts
- [`references/taxonomy.json`](./references/taxonomy.json): domains, conflicts, and rules
- [`references/router_prompt.md`](./references/router_prompt.md): classification logic
- [`references/renderer_prompt.md`](./references/renderer_prompt.md): persona rendering, debate, and synthesis logic
- [`references/eval_cases.json`](./references/eval_cases.json): test cases

## Boundaries

The system does not:

- fabricate historical quotes,
- reframe obvious harm as relationship repair,
- treat legal, medical, tax, or investment questions as purely wisdom questions,
- end with abstract encouragement.
