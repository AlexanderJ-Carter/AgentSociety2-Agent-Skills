# `economy`

Track money, work obligations, consumption choices, scarcity, and material constraints.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/economy/`
- 说明文件 / Skill file: `skills/economy/SKILL.md`
- 理论依据 / Research basis:
  - `skills/economy/references/research_basis.md`

## SKILL.md（原文）

```
---
name: economy
description: Track money, work obligations, consumption choices, scarcity, and material constraints.
script: scripts/update_economy.py
---

# Economy

## Purpose

Model the agent as an economic person: earning income, spending money, facing scarcity, choosing goods, attending work, and trading off time, cost, comfort, and obligation.

Research basis: `references/research_basis.md`.

## Use When

Use this skill before decisions involving shopping, food choice, transport, work, housing, leisure, debt, gifts, or any action with material cost.

## Procedure

1. Read `state/observation.txt`, `state/observation_ctx.json`, `state/economy.json`, `state/resources.json`, `state/routine.json`, `state/memory.jsonl`, and profile context if present.
2. Update cash, inventory, income expectations, recurring expenses, debt, and job obligations.
3. Estimate whether the agent can afford likely actions.
4. Identify scarcity pressure and budget stress.
5. Write economic state for `cognition` and affordability constraints for `plan`.

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
```

## 理论依据 / Research Basis

### `research_basis.md`

# Economy Modeling Basis

## Why this matters

Human economic behavior is constrained by money and obligations, but not reducible to pure optimization.

## Evidence anchors

- Scarcity and bandwidth findings in behavioral economics: resource pressure changes cognition and trade-offs.
- Prospect theory: outcomes are evaluated relative to reference points; losses are often overweighted.
- Household finance behavior studies (TPB applications): social influence and perceived control affect money decisions.

## Simulation translation

Track:

- cash
- debt
- recurring_expenses_pressure
- scarcity_pressure
- budget_stress
- work_obligation
- affordability tiers (meal/taxi/leisure)

Simple policy:

- update cash with incomes/expenses/purchases
- route negative cash into debt
- compute scarcity/budget stress from reserve gap and debt load

## Practical notes

- Keep affordability qualitative for planner handoff (affordable/limited/expensive).
- Allow non-economic modifiers (status, relationships, norms) to override strict least-cost behavior in LLM reasoning.
