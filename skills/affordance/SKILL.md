---
name: affordance
description: Assess what actions are realistically available under environment, time, distance, access, money, body, and social constraints.
---

# Affordance

## Purpose

Prevent unrealistic action choices. This skill translates the current world and internal state into feasible, costly, risky, or unavailable actions.

## Use When

Use this skill before planning, travel, purchase, social approach, work attendance, event participation, or any action that may fail because of constraints.

## Procedure

1. Read `state/observation.txt`, `state/observation_ctx.json`, `state/affordances.json`, `state/economy.json`, `state/physiology.json`, `state/health.json`, `state/norms.json`, and `state/routine.json` if present.
2. Identify available actions from the environment.
3. Estimate constraints: distance, time, opening hours, money, access rights, weather, fatigue, pain, safety, crowding, queues, and social permission.
4. Classify candidate actions as feasible, costly, risky, blocked, or unknown.
5. Write action affordances for `plan`.

## Write

Write `state/affordances.json`.

## Output Schema

```json
{
  "feasible_actions": ["walk to cafe", "talk to Alice", "buy cheap meal"],
  "costly_actions": [
    {
      "action": "take taxi",
      "cost_type": "money",
      "severity": 0.65
    }
  ],
  "blocked_actions": [
    {
      "action": "enter office",
      "reason": "closed or no access"
    }
  ],
  "risks": [
    {
      "action": "walk far while fatigued",
      "risk": "increased exhaustion",
      "severity": 0.42
    }
  ],
  "perceived_control_hint": 0.7
}
```

## Notes

Affordance is not intention. It should not decide what the agent wants; it should clarify what the agent can realistically do and what each option costs.
