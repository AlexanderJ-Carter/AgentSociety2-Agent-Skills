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
