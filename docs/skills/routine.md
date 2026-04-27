# `routine`

Maintain daily routines, habits, schedules, and repeated life patterns for a social human agent.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/routine/`
- 说明文件 / Skill file: `skills/routine/SKILL.md`
- 理论依据 / Research basis: no bundled reference file.

## SKILL.md（原文）

```
---
name: routine
description: Maintain daily routines, habits, schedules, and repeated life patterns for a social human agent.
---

# Routine

## Purpose

Update the agent's ordinary daily structure: sleep, meals, work, commute, study, leisure, chores, and recurring social commitments.

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
