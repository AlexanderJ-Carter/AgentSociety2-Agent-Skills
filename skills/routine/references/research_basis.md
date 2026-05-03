# Routine Research Basis

## Model

Daily routine scheduling, habit loops, automaticity, and cue-action-reward learning.

## Update Rule

```text
habit_strength_next = clamp(habit_strength + repetition_gain + reward_gain - disruption_penalty, 0, 1)
schedule_pressure = clamp(role_obligation + time_block_expectation + social_commitment - flexibility, 0, 1)
routine_fit = clamp(match(current_activity, expected_activity), 0, 1)
```

## Variables

- `current_time_block`: morning, midday, afternoon, evening, night, or simulation-specific block.
- `expected_activity`: plausible routine activity for the block.
- `schedule_pressure`: urgency from commitments and role obligations, `[0, 1]`.
- `routine_fit`: how well current activity matches routine, `[0, 1]`.
- `active_habits[].strength`: learned automaticity, `[0, 1]`.

## Defaults

Routines bias behavior but should not override critical needs, social events, health problems, or environmental constraints.

## Sources

- Wood, W., & Neal, D. T. (2007). A new look at habits and the habit-goal interface.
- Lally, P. et al. (2010). How are habits formed: Modelling habit formation in the real world.
- Verplanken, B., & Orbell, S. (2003). Reflections on past behavior.
