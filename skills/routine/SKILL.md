---
name: routine
description: Maintain daily routines, habits, schedules, and repeated life patterns for a social human agent.
---

# Routine

## Purpose

Update the agent's ordinary daily structure: sleep, meals, work, commute, study, leisure, chores, and recurring social commitments.

## Internal Logic (One Sentence)

Use time, location, role obligations, circadian state, physiology, past routine, and cue-reward evidence to update expected activity, schedule pressure, routine fit, and habits in `state/routine.json` and `state/habits.json`.

Research basis: `references/research_basis.md`.

## Use When

Use this skill when the agent needs a plausible next activity, when a day begins, when time changes meaningfully, or when a repeated behavior should become a habit.

## Procedure

1. Read `state/observation_ctx.json`, `state/observation.txt`, `state/routine.json`, `state/habits.json`, `state/circadian.json`, `state/physiology.json`, and profile context if present.
2. Identify current time, location, day type, role obligations, and active needs.
3. Compare current behavior with the agent's usual routine.
4. Update routine expectations for the current time block.
5. Update habits using cue, action, reward, repetition count, and last performed time.
6. Write routine state for `cognition` and `plan`.

## Write

Write `state/routine.json` and `state/habits.json`.

## Output Schema

```json
{
  "current_time_block": "evening",
  "expected_activity": "dinner or leisure",
  "schedule_pressure": 0.35,
  "routine_fit": 0.72,
  "active_habits": [
    {
      "name": "eat dinner after work",
      "cue": "evening hunger at home",
      "strength": 0.68,
      "last_performed_tick": 110
    }
  ],
  "deviation": {
    "is_deviating": false,
    "reason": ""
  }
}
```

## Notes

Routines should make behavior stable without making it mechanical. Strong habits should bias actions toward familiar choices, but urgent needs, social events, or environmental constraints can override them.
