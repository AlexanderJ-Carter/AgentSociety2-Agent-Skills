---
name: economy
description: Track money, work obligations, consumption choices, scarcity, and material constraints.
script: scripts/update_economy.py
---

# Economy

## Purpose

Model the agent as an economic person: earning income, spending money, facing scarcity, choosing goods, attending work, and trading off time, cost, comfort, and obligation.

Research basis: `references/research_basis.md`.

## Internal Logic (One Sentence)

Update cash, debt, affordability, scarcity pressure, work obligation, and satisficing thresholds from current resources and context, then write `state/economy.json` and `state/resources.json` for `cognition` and `plan`.

## Use When

Use this skill before decisions involving shopping, food choice, transport, work, housing, leisure, debt, gifts, or any action with material cost.

## Procedure

1. Read `state/observation.txt`, `state/observation_ctx.json`, `state/economy.json`, `state/resources.json`, `state/routine.json`, `state/memory.jsonl`, and profile context if present.
2. Update cash, inventory, income expectations, recurring expenses, debt, and job obligations.
3. Estimate whether the agent can afford likely actions.
4. Identify scarcity pressure, budget stress, and an aspiration level for "good enough" choices.
5. For routine or time-limited choices, prefer the first feasible option that clears the aspiration threshold instead of pretending the agent optimizes across all possible alternatives.
6. Write economic state for `cognition` and affordability constraints for `plan`.

If deterministic baseline is preferred, run `scripts/update_economy.py` first, then optionally refine social/status-driven spending choices with LLM reasoning.

## Write

Write `state/economy.json` and `state/resources.json`.

## Output Schema

```json
{
  "cash": 42.5,
  "income_status": "employed",
  "next_income_expected": "weekly",
  "recurring_expenses_pressure": 0.4,
  "scarcity_pressure": 0.32,
  "budget_stress": 0.25,
  "choice_policy": {
    "mode": "satisficing",
    "aspiration_level": 0.62,
    "search_stopped_reason": "first option met budget, time, and dignity constraints"
  },
  "work_obligation": {
    "active": true,
    "next_shift": "09:00",
    "lateness_risk": 0.1
  },
  "affordability": {
    "meal": "affordable",
    "taxi": "expensive",
    "leisure": "limited"
  }
}
```

## Notes

Money should affect realistic choices without reducing every decision to utility maximization. Culture, relationships, dignity, habit, status, and urgency can make people spend or save in non-obvious ways.

Bounded rationality rule: when information, time, or attention is limited, do not require the agent to compare every possible purchase. Let aspiration levels move with experience: repeated disappointment raises caution; repeated success can lower search effort.
