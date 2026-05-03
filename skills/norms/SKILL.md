---
name: norms
description: Track social norms, roles, obligations, permissions, sanctions, and place-specific expectations.
---

# Norms

## Purpose

Model the agent as someone living under social rules. Norms shape what the agent feels expected, allowed, forbidden, admired, or punishable.

## Internal Logic (One Sentence)

Use place, role, audience, culture, relationship, routine, and observation context to estimate active norms, permissions, sanctions, visibility, and moral emotion risk in `state/norms.json`.

Research basis: `references/research_basis.md`.

## Use When

Use this skill in workplaces, schools, homes, public spaces, queues, restaurants, hospitals, religious places, legal settings, or any situation involving role expectations.

## Procedure

1. Read `state/observation.txt`, `state/observation_ctx.json`, `state/norms.json`, `state/culture.json`, `state/relationships.json`, `state/routine.json`, and profile context if present.
2. Identify active roles: worker, customer, parent, friend, stranger, patient, student, neighbor, host, guest.
3. Identify place-specific expectations and forbidden behaviors.
4. Estimate norm pressure, witness visibility, sanction risk, and moral emotion risk.
5. Write norm state for `cognition` and `plan`.

## Write

Write `state/norms.json`.

## Output Schema

```json
{
  "active_roles": ["customer", "stranger"],
  "active_norms": [
    {
      "norm": "wait in line",
      "pressure": 0.83,
      "violation_risk": 0.7,
      "likely_sanction": "disapproval"
    }
  ],
  "permissions": ["order food", "sit at available table"],
  "forbidden_or_costly": ["skip queue", "shout at staff"],
  "witness_visibility": 0.65,
  "moral_emotion_risk": {
    "shame": 0.35,
    "guilt": 0.2
  }
}
```

## Notes

Norms should influence `subjective_norm` in intention selection. A norm can be violated, but the violation should have social, emotional, or institutional consequences when visible or important.
