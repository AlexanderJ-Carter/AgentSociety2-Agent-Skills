# Affordance Research Basis

## Model

Ecological affordance theory and constraint-based planning.

## Update Rule

For each candidate action, estimate:

```text
availability = environment_match * access * time_window
cost = weighted_sum(distance, money, fatigue, social_friction, risk)
feasibility = clamp(availability * (1 - cost), 0, 1)
```

Classify actions as:

- `feasible`: `feasibility >= 0.65`
- `costly`: `0.35 <= feasibility < 0.65`
- `blocked`: known access, time, money, physical, or social constraint prevents action
- `unknown`: missing evidence prevents a confident classification

## Variables

- `environment_match`: whether the object/place/action exists now, `[0, 1]`
- `access`: legal, social, physical, and role-based permission, `[0, 1]`
- `time_window`: whether the action can happen at the current time, `[0, 1]`
- `cost`: normalized burden across money, effort, distance, risk, and social friction, `[0, 1]`
- `perceived_control_hint`: feasibility signal for cognition, `[0, 1]`

## Defaults

Use conservative defaults when evidence is missing. Unknown is better than pretending an action is available.

## Sources

- Gibson, J. J. (1979). *The Ecological Approach to Visual Perception*.
- Norman, D. A. (1988). *The Psychology of Everyday Things*.
- Simon, H. A. (1955). A behavioral model of rational choice.
