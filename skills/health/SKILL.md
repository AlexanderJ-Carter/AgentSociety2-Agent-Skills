---
name: health
description: Track sickness, pain, chronic condition, recovery, exercise, stress load, and long-term wellbeing.
---

# Health

## Purpose

Maintain health as a slow-moving background state that affects energy, mood, mobility, appetite, social behavior, and plan feasibility.

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
