---
name: circadian
description: Maintain sleep-wake rhythm, circadian alertness, appetite rhythm, and chronotype-sensitive daily timing.
script: scripts/update_circadian.py
---

# Circadian

## Purpose

Model the agent's biological time. This skill updates circadian alertness, appetite rhythm, sleep pressure, chronotype effects, and sleep tendency.

Research basis: `references/research_basis.md`.

## When to Use

Use once per tick before `physiology` and `cognition`, especially in simulations with day-night cycles, work schedules, meals, fatigue, or sleep.

## Read

Read if present:

- `state/observation_ctx.json`
- `state/observation.txt`
- `state/circadian.json`
- `state/physiology.json`
- `init_state.json`

Skip missing files.

## Write

Write:

- `state/circadian.json`
- `state/sleep.json`

## Procedure

1. Extract current clock time from `state/observation_ctx.json` or observation text.
2. Determine chronotype from previous circadian state, profile, or initialize as `neutral`.
3. Update circadian phase as a 24-hour cycle.
4. Update sleep pressure using the two-process sleep model:
   - Process S: sleep pressure rises while awake and falls during sleep.
   - Process C: circadian rhythm modulates alertness and sleep tendency.
5. Estimate appetite rhythm. Appetite should usually be lower in the biological morning and higher in the evening unless overridden by recent eating, illness, stress, or culture/routine.
6. Write both state files.

If deterministic baseline is preferred, run `scripts/update_circadian.py` first, then optionally refine with LLM reasoning.

## State Rules

Use values in `[0, 1]`.

```text
sleep_pressure_next = clamp(sleep_pressure + wake_gain - sleep_recovery, 0, 1)
```

```text
effective_alertness = clamp(circadian_alertness - sleep_pressure * 0.6 - fatigue_modifier, 0, 1)
```

Chronotype shifts preferred timing:

- `morning`: alertness peak earlier, sleep tendency earlier.
- `neutral`: standard daytime alertness.
- `evening`: alertness peak later, sleep tendency later.

## Output Schema

`state/circadian.json`:

```json
{
  "tick": 120,
  "clock_time": "18:30",
  "chronotype": "neutral",
  "phase_hour": 18.5,
  "circadian_alertness": 0.62,
  "circadian_appetite": 0.74,
  "sleep_tendency": 0.38,
  "light_exposure": 0.35,
  "notes": ["Evening appetite pressure is elevated."]
}
```

`state/sleep.json`:

```json
{
  "sleep_pressure": 0.48,
  "effective_energy": 0.56,
  "sleep_debt": 0.2,
  "last_sleep_tick": 20,
  "should_sleep_soon": false,
  "reasoning": "Sleep pressure is moderate and circadian alertness remains acceptable."
}
```

## Integration

- `physiology` should read `circadian_appetite`, `sleep_pressure`, and `effective_energy`.
- `routine` should use chronotype to schedule meals, work, leisure, and sleep.
- `cognition` should treat low alertness as lower perceived control and higher routine bias.

## Stop Conditions

If clock time is unavailable, keep prior phase if present. Otherwise initialize to midday and mark uncertainty in `notes`.
