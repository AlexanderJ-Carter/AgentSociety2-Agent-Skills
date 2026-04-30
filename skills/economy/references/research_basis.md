# Economy Modeling Basis

## Why this matters

Human economic behavior is constrained by money and obligations, but not reducible to pure optimization.

## Evidence anchors

- Bounded rationality and satisficing (Simon): people often stop search once an option is good enough under limited information, time, and computation.
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
- aspiration_level and search_stop_reason for bounded economic choice

Simple policy:

- update cash with incomes/expenses/purchases
- route negative cash into debt
- compute scarcity/budget stress from reserve gap and debt load
- choose by satisficing when search is costly: scan feasible options in context order, accept the first option whose estimated score clears `aspiration_level`
- adapt `aspiration_level` slowly: successful choices can lower search effort; regret, debt growth, or social embarrassment can raise the threshold

## Practical notes

- Keep affordability qualitative for planner handoff (affordable/limited/expensive).
- Allow non-economic modifiers (status, relationships, norms) to override strict least-cost behavior in LLM reasoning.
- Do not model the agent as a perfect optimizer unless a task explicitly demands careful comparison.

## References

- Simon, H. A. (1955). A behavioral model of rational choice. *The Quarterly Journal of Economics*, 69(1), 99-118. DOI: `10.2307/1884852`.
