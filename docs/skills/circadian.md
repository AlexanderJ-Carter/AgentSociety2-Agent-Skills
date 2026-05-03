# `circadian`

Maintain sleep-wake rhythm, circadian alertness, appetite rhythm, and chronotype-sensitive daily timing.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/circadian/`
- 说明文件 / Skill file: `skills/circadian/SKILL.md`
- 执行脚本 / Script baseline: `scripts/update_circadian.py`
- 最近更新 / Last updated: `2026-05-03`
- 理论依据 / Research basis:
  - `skills/circadian/references/research_basis.md`

## SKILL.md（原文）

```
---
name: circadian
description: Maintain sleep-wake rhythm, circadian alertness, appetite rhythm, and chronotype-sensitive daily timing.
script: scripts/update_circadian.py
---

# Circadian

## Purpose

Model the agent's biological time. This skill updates circadian alertness, appetite rhythm, sleep pressure, chronotype effects, and sleep tendency.

## Internal Logic (One Sentence)

Use clock time, chronotype, light exposure, prior sleep, and recent activity to update circadian phase, sleep pressure, appetite rhythm, and sleep tendency in `state/circadian.json` and `state/sleep.json`.

Research basis: `references/research_basis.md`.

## Use When

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

## Notes

If clock time is unavailable, keep prior phase if present. Otherwise initialize to midday and mark uncertainty in `notes`.
```

## 理论依据 / Research Basis

### `research_basis.md`

# Circadian Modeling Basis

## Why this matters

Human alertness, appetite, and sleep propensity are not static. They are shaped by at least two partially independent processes:

- Process S (homeostatic): sleep pressure increases while awake and decreases during sleep.
- Process C (circadian): an endogenous roughly 24-hour rhythm modulates alertness and sleep tendency.

## Evidence anchors

- Borbely's two-process framework for sleep regulation and later refinements in sleep science.
- Circadian appetite findings: internal clock increases hunger/appetite in evening independent of behavior context.
- Chronotype literature: morning/evening preference shifts peak performance and sleep timing.

## Simulation translation

Use bounded state variables in [0, 1]:

- sleep_pressure
- circadian_alertness
- circadian_appetite
- sleep_tendency
- effective_energy

Update template:

- sleep_pressure_next = clamp(sleep_pressure + wake_gain - sleep_recovery)
- circadian_alertness = f(clock_time, chronotype_shift)
- sleep_tendency = g(sleep_pressure, circadian_alertness)
- effective_energy = circadian_alertness - alpha * sleep_pressure - fatigue_modifier

## Practical notes

- This is a phenomenological approximation, not a clinical model.
- Keep chronotype as a per-agent latent trait, not a hard label for every behavior.
- Let social obligations and norms override biological tendency when needed, but record the resulting strain in fatigue/stress.
