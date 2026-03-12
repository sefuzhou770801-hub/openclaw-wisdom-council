[![中文](https://img.shields.io/badge/Language-%E4%B8%AD%E6%96%87-ff6b6b?style=for-the-badge)](./README.md)
[![English](https://img.shields.io/badge/Language-English-4c8bf5?style=for-the-badge)](./README.en.md)
[![Open Skill Spec](https://img.shields.io/badge/Page-Skill%20Spec-111111?style=for-the-badge)](./SKILL.md)

# Wisdom Council

A historical-wisdom decision system for real human dilemmas.

Many hard problems are not blocked by missing information.
They are blocked by missing judgment.

- Should I get divorced?
- Should I quit my job and start a company?
- My cofounder is becoming unreliable.
- I know what I should do, but I keep procrastinating.
- I care too much about what other people think.

These questions rarely have a clean “correct” answer, but they still require a decision.

`Wisdom Council` is built for one thing:

turn a human dilemma into a real clash of ideas, then converge on a decision you can act on.

This is not roleplay.
It is a decision-support thinking system.

## How to Use This Skill

The simplest way is to explicitly invoke `$wisdom-council` inside a skill-enabled agent, then describe your real dilemma as plainly as possible.

### Minimal usage

```text
Use $wisdom-council to help me decide whether I should quit my job and start a company.
```

### Better prompt shape

The system works much better when you include a little context. Try adding:

- your current situation
- the real options in front of you
- what you are most afraid of losing
- what outcome you cannot accept
- the time window for the decision

Example:

```text
Use $wisdom-council to help me decide:
I may quit my job within 3 months to start a company.
I currently have stable income and family responsibility.
I am afraid of running out of cash if I fail, but I am also afraid of missing the window if I wait too long.
Please prioritize risk, long-term upside, and family responsibility.
```

### Good follow-up patterns

After the first answer, you can continue with prompts like:

- Based on the last round, keep only the 3 most important voices and go deeper.
- Based on the last round, focus on the conflict between stability and freedom.
- Rebuild the council, but prioritize startup, risk, and organizational lenses this time.
- Keep the same judgment, but rewrite the action plan in a more conservative / more aggressive way.

### Best-fit problem types

- relationships, marriage, family, parenting
- career decisions, switching paths, startups, competition
- anxiety, meaning, emptiness, procrastination
- value conflicts, principle choices, boundary questions
- failure, rebuilding, mortality, and limited time

## Workflow

```text
User Question
  -> Router
  -> Retriever
  -> Council Builder
  -> Renderer
  -> Synthesizer
  -> Quality Checker
  -> Final Decision
```

In plain language:

```text
user problem
  -> analyze decision structure
  -> select the right wisdom lenses
  -> build a ten-seat council
  -> generate competing viewpoints
  -> synthesize a judgment
  -> return an action plan
```

## What the System Does

- identifies the domain, conflict type, emotional state, hidden motive, and true blockage
- dynamically selects the best ten wisdom lenses from the pool
- creates real disagreement instead of superficial variety
- converges on judgment, tradeoffs, and actions

## What the User Gets

Every response includes:

- a restatement of the problem
- why these ten lenses were selected
- ten distinct perspectives
- major consensus
- key disagreements
- final judgment
- 24-hour actions
- 7-day plan
- next-round deepening questions

The goal is not to give more opinions.
The goal is to help the user decide.

## Example Output Shape

User question:

> Should I quit my job and start a company?

A likely synthesis might look like this:

- Major consensus: if demand is still unvalidated, quitting now is too risky.
- Key disagreement: go all-in now vs validate through a side path first.
- Final judgment: build proof through a side path before quitting.
- 24-hour action: contact three potential customers to validate demand.
- 7-day plan: finish the first interview round and a rough prototype.

## Why This Skill Exists

Most “wise advisor” prompts fail in predictable ways:

- they reuse the same people every time,
- they sound diverse without creating real disagreement,
- they end in encouragement instead of a decision.

This skill is designed to do the opposite:

make wisdom collide, then turn that collision into action.

## File Structure

- [`SKILL.md`](./SKILL.md): skill workflow and operating rules
- [`references/sages.json`](./references/sages.json): structured sage pool
- [`references/taxonomy.json`](./references/taxonomy.json): domains, conflicts, and routing rules
- [`references/router_prompt.md`](./references/router_prompt.md): classification logic
- [`references/renderer_prompt.md`](./references/renderer_prompt.md): rendering and synthesis logic
- [`references/eval_cases.json`](./references/eval_cases.json): test cases

## Boundaries

The system does not:

- fabricate historical quotes,
- reframe obvious harm as relationship repair,
- treat legal, medical, tax, or investment questions as purely wisdom questions,
- end with abstract encouragement.

## One-Line Summary

Turn a human dilemma into a real clash of ideas, then converge on a decision you can act on.
