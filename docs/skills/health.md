# `health`

Track sickness, pain, chronic condition, recovery, exercise, stress load, and long-term wellbeing.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/health/`
- 说明文件 / Skill file: `skills/health/SKILL.md`
- 执行脚本 / Script baseline: none; use the natural-language procedure.
- 最近更新 / Last updated: `2026-05-03`
- 理论依据 / Research basis:
  - `skills/health/references/research_basis.md`

## SKILL.md（原文）

```
---
name: health
description: Track sickness, pain, chronic condition, recovery, exercise, stress load, and long-term wellbeing.
---

# Health

## Purpose

Maintain health as a slow-moving background state that affects energy, mood, mobility, appetite, social behavior, and plan feasibility.

## Internal Logic (One Sentence)

Combine symptoms, prior health, physiology, stress, recovery, exercise, medication, and memory evidence to update acute and chronic health effects in `state/health.json`.

Research basis: `references/research_basis.md`.

## Use When

Use this skill when the agent is sick, injured, exhausted, exercising, recovering, taking medication, under chronic stress, or making health-related choices.

## Procedure

1. Read `state/observation.txt`, `state/health.json`, `state/physiology.json`, `state/routine.json`, `state/memory.jsonl`, and profile context if present.
2. Update acute symptoms: pain, fever, nausea, cough, dizziness, injury, anxiety, or exhaustion.
3. Update slow variables: fitness, chronic condition, stress burden, recovery, resilience, and health habits.
4. Estimate how health affects mobility, appetite, social willingness, and perceived control.
5. Write health state.

## Write

Write `state/health.json`.

## Output Schema

```json
{
  "overall_health": 0.82,
  "acute_symptoms": {
    "pain": 0.0,
    "illness": 0.1,
    "nausea": 0.0
  },
  "chronic_factors": {
    "fitness": 0.56,
    "stress_burden": 0.34,
    "recovery_capacity": 0.68
  },
  "behavior_effects": {
    "mobility_limit": 0.05,
    "appetite_modifier": -0.02,
    "social_withdrawal": 0.1,
    "perceived_control_modifier": -0.04
  }
}
```

## Notes

Health should change slowly unless there is an acute event. Do not make every tired state an illness. Distinguish ordinary fatigue from sickness, pain, and chronic burden.
```

## 理论依据 / Research Basis

### `research_basis.md`

# Health Research Basis

## Model

Biopsychosocial health with allostatic load and recovery dynamics.

## Update Rule

```text
stress_burden_next = clamp(stress_burden + stressor_load - recovery, 0, 1)
recovery_capacity = clamp(sleep_quality + rest + support + fitness - illness_load, 0, 1)
overall_health = clamp(1 - weighted_sum(acute_symptoms, chronic_factors, stress_burden), 0, 1)
```

## Variables

- `overall_health`: broad health signal, `[0, 1]`.
- `acute_symptoms`: pain, illness, nausea, dizziness, fever, injury, each `[0, 1]`.
- `chronic_factors`: fitness, chronic condition burden, stress burden, recovery capacity, each `[0, 1]`.
- `behavior_effects`: mobility, appetite, social withdrawal, and perceived-control modifiers, usually `[-1, 1]`.

## Defaults

Health changes slowly unless observation or memory reports an acute event. Ordinary tiredness should usually stay in physiology rather than becoming illness.

## Sources

- Engel, G. L. (1977). The need for a new medical model.
- McEwen, B. S. (1998). Protective and damaging effects of stress mediators.
- WHO. (1948). Constitution of the World Health Organization.
