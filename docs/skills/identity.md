# `identity`

Maintain self-concept, social identity, roles, values, status concerns, and identity threats. Use when behavior depends on who the agent thinks it is or how it is seen.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/identity/`
- 说明文件 / Skill file: `skills/identity/SKILL.md`
- 最近更新 / Last updated: `2026-04-27`
- 理论依据 / Research basis:
  - `skills/identity/references/theory.md`

## SKILL.md（原文）

```
---
name: identity
description: Maintain self-concept, social identity, roles, values, status concerns, and identity threats. Use when behavior depends on who the agent thinks it is or how it is seen.
---

# Identity

## Purpose

Model the agent's sense of self: roles, group memberships, values, dignity, status, aspirations, and threats to identity.

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
```

## 理论依据 / Research Basis

### `theory.md`

# Identity Theory Notes

Useful foundations:

- Social identity theory: people partly define themselves through group memberships.
- Role theory: behavior is constrained by expectations attached to roles.
- Self-discrepancy theory: distress can arise when actual self, ideal self, and ought self diverge.
- Status and dignity: people protect reputation, competence, autonomy, and social standing.
- Narrative identity: people maintain a story about who they are and what their life means.

Implementation guidance:

- Separate stable identity from temporary emotion.
- Track active role by context; the same person behaves differently at home, work, school, or public space.
- Identity threat can bias cognition toward defense, withdrawal, anger, shame, or status repair.
- Identity support can increase belonging, confidence, and prosocial behavior.
