# `physiology`

Update body-level needs such as hunger, satiety, thirst, fatigue, and stress from time, activity, and recent events.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/physiology/`
- 说明文件 / Skill file: `skills/physiology/SKILL.md`
- 最近更新 / Last updated: `2026-04-27`
- 理论依据 / Research basis:
  - `skills/physiology/references/research_basis.md`

## SKILL.md（原文）

```
---
name: physiology
description: Update body-level needs such as hunger, satiety, thirst, fatigue, and stress from time, activity, and recent events.
script: scripts/update_physiology.py
---

# Physiology

## Purpose

Maintain the agent's body state for this tick. This skill turns time, activity, meals, sleep, illness, stress, and environment into physiological pressures that `cognition` and `plan` can use.

Research basis: `references/research_basis.md`.

## When to Use

Use this skill once per tick before `cognition` when bodily needs may affect intention selection or plan interruption.

## Read

Read any existing files if present:

- `state/observation.txt`
- `state/observation_ctx.json`
- `state/physiology.json`
- `state/circadian.json`
- `state/health.json`
- `state/memory.jsonl`

Skip missing files.

## Write

Always write:

- `state/physiology.json`
- `state/needs.json`

Append `state/body_events.jsonl` only when there is a notable event such as eating, drinking, sleeping, injury, sickness, heavy exertion, or critical hunger/fatigue.

## Procedure

1. Determine current tick and time from observation context, session state, or prior physiology.
2. Infer whether the agent recently ate, drank, slept, rested, worked, walked, exercised, experienced conflict, or encountered danger.
3. Update body variables from prior state. If prior state is missing, initialize from profile, current time, and observation.
4. Compute need urgencies from physiology.
5. Write `state/physiology.json` and `state/needs.json`.

If deterministic baseline is preferred, run `scripts/update_physiology.py` first, then optionally refine narrative and edge cases with LLM reasoning.

## State Rules

Use bounded continuous values in `[0, 1]`.

Hunger is a pressure, not a simple counter:

```text
hunger_pressure =
  time_since_meal_effect
  + circadian_appetite_effect
  + exertion_effect
  + stress_appetite_modifier
  - satiety_effect
```

Satiety rises after eating and decays with time:

```text
satiety_next = clamp(satiety_current * satiety_decay + meal_gain - exertion_cost, 0, 1)
```

Fatigue combines sleep pressure, exertion, cognitive load, illness, and stress:

```text
fatigue = clamp(0.45 * sleep_pressure + 0.25 * exertion + 0.15 * stress_load + 0.15 * illness, 0, 1)
```

Thirst rises faster under heat, walking, exercise, alcohol, salt, illness, or long time since drinking.

Stress load rises under threat, overload, conflict, uncertainty, and unmet needs. It recovers with rest, safety, sleep, social support, and successful coping.

## Output Schema

`state/physiology.json`:

```json
{
  "tick": 120,
  "time": "2026-04-27T18:30:00",
  "hunger_pressure": 0.71,
  "satiety": 0.22,
  "thirst": 0.55,
  "sleep_pressure": 0.48,
  "fatigue": 0.44,
  "stress_load": 0.31,
  "pain": 0.0,
  "illness": 0.0,
  "recent_activity": "walking",
  "last_meal_tick": 78,
  "last_drink_tick": 96,
  "last_sleep_tick": 20,
  "notes": ["Evening circadian appetite is increasing hunger."]
}
```

`state/needs.json`:

```json
{
  "current_need": "eat",
  "urgency": 0.71,
  "needs": {
    "satiety": 0.29,
    "hydration": 0.45,
    "energy": 0.56,
    "safety": 0.85,
    "social": 0.62
  },
  "interrupt_plan": false,
  "reasoning": "Hunger is rising but not yet critical."
}
```

## Integration

- `cognition` should read `state/physiology.json` and `state/needs.json` when choosing emotion and intention.
- `plan` should interrupt ongoing plans when `interrupt_plan` is true.
- `circadian` should provide `circadian_appetite` and alertness if available.

## Stop Conditions

If no bodily state can be inferred, initialize neutral physiology and write a short note explaining the uncertainty.
```

## 理论依据 / Research Basis

### `research_basis.md`

# Physiology Modeling Basis

## Why this matters

Believable social agents should not use a single static hunger or energy counter. Human body signals interact with rhythm, activity, stress, and health.

## Evidence anchors

- Homeostatic control and allostatic load concepts: stress and demand reshape physiological regulation.
- Sleep-pressure and circadian interaction affects fatigue and self-control.
- Appetite and hydration are context-sensitive and partially rhythmic.

## Simulation translation

Maintain continuous pressures in [0, 1]:

- hunger_pressure
- satiety
- thirst
- fatigue
- stress_load
- pain
- illness

Recommended structure:

- satiety_next = clamp(satiety * decay + meal_gain - exertion_cost)
- hunger_pressure = weighted(time_since_meal, circadian_appetite, exertion, stress, satiety)
- fatigue = weighted(sleep_pressure, exertion, stress, illness, pain)

Need projection (for cognition/plan):

- current_need from minimum satisfaction dimension
- urgency = 1 - satisfaction[current_need]
- interrupt_plan true only under high urgency/critical thresholds

## Practical notes

- Keep fast variables (hunger/thirst) and slow variables (illness/chronic stress) distinct.
- Avoid binary states when uncertain; write uncertainty notes rather than forcing extreme values.
