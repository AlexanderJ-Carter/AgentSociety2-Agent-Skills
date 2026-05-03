---
name: identity
description: Maintain self-concept, social identity, roles, values, status concerns, and identity threats. Use when behavior depends on who the agent thinks it is or how it is seen.
---

# Identity

## Purpose

Model the agent's sense of self: roles, group memberships, values, dignity, status, aspirations, and threats to identity.

## Internal Logic (One Sentence)

Use profile, relationship, culture, norms, reflections, and current events to estimate active roles, identity salience, belonging, status concern, support, and threat in `state/identity.json`.

## Use When

Use this skill when actions involve family role, job role, class, gender, age, community, religion, ethnicity, profession, reputation, pride, shame, discrimination, belonging, or life goals.

## Procedure

1. Read profile context, `state/observation.txt`, `state/relationships.json`, `state/culture.json`, `state/norms.json`, `state/reflections.jsonl`, and previous `state/identity.json` if present.
2. Identify active identities and roles in the current situation.
3. Estimate identity salience: which identity matters most right now.
4. Detect identity support or threat.
5. Update self-concept, status concern, belonging, dignity, and aspiration signals.
6. Write `state/identity.json`.

## Write

Write `state/identity.json`.

## Output Schema

```json
{
  "_meta": {
    "skill": "identity",
    "purpose": "Current self-concept, active roles, group belonging, and identity pressure."
  },
  "_summary": "Work identity is salient; being seen as reliable matters right now.",
  "active_roles": ["employee", "colleague"],
  "salient_identity": "reliable worker",
  "values_in_play": ["responsibility", "competence"],
  "belonging": 0.66,
  "status_concern": 0.48,
  "identity_threat": {
    "active": false,
    "source": "",
    "severity": 0.0
  },
  "behavior_bias": "Prefer actions that preserve reliability and competence."
}
```

## Notes

Identity should change slowly. Momentary embarrassment is emotion; repeated evidence about who the agent is or how others see it belongs here.

For theory notes, see `references/theory.md`.
