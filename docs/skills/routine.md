# `routine`

Maintain daily routines, habits, schedules, and repeated life patterns for a social human agent.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/routine/`
- 说明文件 / Skill file: `skills/routine/SKILL.md`
- 执行脚本 / Script baseline: none; use the natural-language procedure.
- 最近更新 / Last updated: `2026-05-03`
- 理论依据 / Research basis:
  - `skills/routine/references/research_basis.md`

## SKILL.md（原文）

```
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
```

## 理论依据 / Research Basis

### `research_basis.md`

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
