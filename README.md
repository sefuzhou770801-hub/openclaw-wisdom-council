# Wisdom Council

Dynamic historical-wisdom routing for real user dilemmas.

`Wisdom Council` is not a “ten ancient people take turns talking” prompt.
It is a routing system that:

1. classifies the user's dilemma,
2. selects the best-fit 10 wisdom lenses from a structured sage pool,
3. forces disagreement and counterbalance,
4. converges on a judgment, tradeoffs, and concrete actions.

## What It Does

- Turns messy user questions into a structured decision frame.
- Routes by domain, conflict type, blocked point, urgency, and decision scene.
- Builds a balanced 10-person council instead of reusing the same famous names.
- Prevents one-sided outputs like pure self-help, pure ethics, or pure strategy.
- Forces a final answer with `24-hour actions` and `7-day actions`.

## Why It Exists

Most “wise advisor” prompts fail in the same way:

- they always use the same people,
- they confuse topic with true blockage,
- they flatten disagreement into generic inspiration,
- they end with vague comfort instead of a judgment.

This skill is designed to do the opposite.

## Core Workflow

```text
User Question
  -> Router
  -> Retriever
  -> Council Builder
  -> Renderer + Synthesizer
  -> Quality Checker
```

## Key Features

- `Dynamic classification`
  Detects primary domain, secondary domains, conflict types, emotional tone, hidden intent, and blocked point.

- `Dynamic sage selection`
  Chooses the best-fit 10 sages from a structured pool of 32, instead of relying on a fixed roster.

- `Balanced council construction`
  Uses seat functions like anchor, coverage, counterbalance, action, context, and wildcard.

- `Anti-bias constraints`
  Prevents overuse of famous figures, repeated lens clusters, civilizational imbalance, and false consensus.

- `Action-first synthesis`
  Produces a judgment, names the cost, and ends with near-term actions.

## File Map

- [`SKILL.md`](./SKILL.md): top-level skill workflow and operating rules
- [`references/sages.json`](./references/sages.json): structured sage pool
- [`references/taxonomy.json`](./references/taxonomy.json): domains, conflicts, blocked points, seat functions, hard rules
- [`references/router_prompt.md`](./references/router_prompt.md): classification and selection logic
- [`references/renderer_prompt.md`](./references/renderer_prompt.md): output and convergence rules
- [`references/eval_cases.json`](./references/eval_cases.json): routing sanity checks with 12 test cases

## Typical Use Cases

- Should I get divorced?
- Should I quit and start a company?
- I feel anxious and life feels meaningless.
- My cofounder is unreliable. Do I confront or cut?
- I know what to do but keep procrastinating.
- I care too much about what people think.
- My parents keep interfering with my life.
- I want to win without becoming hollow or cynical.

## Output Contract

Every good response should contain:

1. Problem restatement
2. Why these 10 sages were selected
3. Ten distinct viewpoints
4. Major consensus
5. Key disagreements
6. Final judgment
7. 24-hour actions
8. 7-day actions
9. Next-round deepening path

## Guardrails

- Do not fabricate historical quotes.
- Do not confuse abuse or structural harm with “repair the relationship.”
- Do not answer high-stakes legal, medical, tax, or investment questions as if wisdom replaces professional verification.
- Do not end in abstract encouragement.

## Positioning

This skill is best understood as:

`user problem -> structured dilemma -> dynamic lens routing -> actionable judgment`

Not:

`pick ten famous thinkers -> generate inspirational monologues`
